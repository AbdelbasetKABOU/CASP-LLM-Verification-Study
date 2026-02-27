
# -----------------------------------------------------------------------
# Runs Frama-C WP over ALL matching C files inside each subdirectory:
#     (e.g. code_with_llm_spec_openai_gpt-5.2.c)
#    - Saves one log per input C file inside the same directory.
#    - Produces a CSV that includes provider + model parsed from filename.
# -------------------------------------------------------------------------

import argparse
import subprocess
import re
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

import pandas as pd

WP_SCHEDULED_RE = re.compile(r"\[wp\]\s*(\d+) goals scheduled")
PROVED_RE = re.compile(r"Proved goals:\s*(\d+)\s*/\s*(\d+)")
TIMEOUT_RE = re.compile(r"Timeout:\s*(\d+)")
UNREACHABLE_RE = re.compile(r"Unreachable:\s*(\d+)")
TERMINATING_RE = re.compile(r"Terminating:\s*(\d+)")
META_KV_RE = re.compile(r"^\s*([a-zA-Z0-9_]+)\s*:\s*(.*?)\s*$")

# Example solver lines can vary; this tries to be flexible:
#   [wp] Alt-Ergo 2.5.0: 12 (10ms - 30ms - 50ms)
#   Z3: 7
SOLVER_RE = re.compile(
    r"^(?:\[wp\]\s*)?\s*(Qed|Alt-?Ergo(?:\s+[0-9.]+)?|Z3|CVC4|CVC5|Coq|Why3[^:]*)\s*:\s*(\d+)(?:\s*\(([^)]*)\))?",
    re.IGNORECASE,
)

FUNCTION_RE = re.compile(r"\[rte:annot\]\s+annotating function\s+([a-zA-Z_][a-zA-Z0-9_]*)")
MS_TRIPLE_RE = re.compile(r"(?:(\d+)ms)\s*-\s*(?:(\d+)ms)\s*-\s*(?:(\d+)ms)")


def parse_solver_times(timestr: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    m = MS_TRIPLE_RE.search(timestr or "")
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None, None, None


def parse_output(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "wp_goals_scheduled": None,
        "proved_goals": None,
        "total_goals": None,
        "timeout": None,
        "unreachable": None,
        "terminating": None,
        "solvers": {},  # solver -> {count, t_min_ms, t_mid_ms, t_max_ms}
        "function": None,
    }

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        m = WP_SCHEDULED_RE.search(line)
        if m:
            data["wp_goals_scheduled"] = int(m.group(1))
            continue

        m = PROVED_RE.search(line)
        if m:
            data["proved_goals"] = int(m.group(1))
            data["total_goals"] = int(m.group(2))
            continue

        m = TIMEOUT_RE.search(line)
        if m:
            data["timeout"] = int(m.group(1))
            continue

        m = UNREACHABLE_RE.search(line)
        if m:
            data["unreachable"] = int(m.group(1))
            continue

        m = TERMINATING_RE.search(line)
        if m:
            data["terminating"] = int(m.group(1))
            continue

        m = SOLVER_RE.search(line)
        if m:
            solver = m.group(1).strip()
            count = int(m.group(2))
            tmin, tmid, tmax = parse_solver_times(m.group(3))
            bucket = data["solvers"].setdefault(
                solver,
                {"count": 0, "t_min_ms": None, "t_mid_ms": None, "t_max_ms": None},
            )
            bucket["count"] += count
            if tmin is not None:
                bucket["t_min_ms"] = tmin
            if tmid is not None:
                bucket["t_mid_ms"] = tmid
            if tmax is not None:
                bucket["t_max_ms"] = tmax
            continue

        m = FUNCTION_RE.search(line)
        if m:
            data["function"] = m.group(1)
            continue

    return data


def infer_provider_model_from_filename(path: Path, prefix: str) -> Tuple[str, str]:
    """
    Expects: <prefix><provider>_<model>.c
    Example: code_with_llm_spec_openai_gpt-5.2.c
             prefix='code_with_llm_spec_'
             -> provider='openai', model='gpt-5.2'
    If it doesn't match nicely, returns ('unknown','unknown').
    """
    stem = path.stem  # filename without .c
    if not stem.startswith(prefix):
        return "unknown", "unknown"

    rest = stem[len(prefix):]  # provider_model...
    if not rest:
        return "unknown", "unknown"

    parts = rest.split("_", 1)
    provider = parts[0] if parts[0] else "unknown"
    model = parts[1] if len(parts) > 1 and parts[1] else "unknown"
    return provider, model


def safe_slug(s: str) -> str:
    # for log filenames / column keys
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", s).strip("_")


def run_framac(path: Path, prover: str, provider: str, model: str) -> Tuple[int, str, float]:
    cmd = ["frama-c", "-wp", "-wp-rte", "-wp-prover", prover, str(path)]
    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    elapsed = time.perf_counter() - start

    header = [
        "# Reproducibility header",
        f"# date_utc: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"# provider: {provider}",
        f"# model: {model}",
        f"# prover: {prover}",
        f"# cwd: {Path.cwd()}",
        f"# file: {path}",
        f"# cmd: {' '.join(cmd)}",
        "# --- Begin frama-c output ---",
    ]
    composed = "\n".join(header) + "\n" + (proc.stdout or "")
    return proc.returncode, composed, elapsed


def flatten_row(
    dir_name: str,
    file_path: Path,
    provider: str,
    model: str,
    rc: int,
    parsed: Dict[str, Any],
    elapsed: float,
    date_str: str,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "directory": dir_name,
        "file": str(file_path),
        "filename": file_path.name,
        "provider": provider,
        "model": model,
        "returncode": rc,
        "elapsed_s": elapsed,
        "date": date_str,
        "wp_goals_scheduled": parsed.get("wp_goals_scheduled"),
        "proved_goals": parsed.get("proved_goals"),
        "total_goals": parsed.get("total_goals"),
        "timeout": parsed.get("timeout"),
        "unreachable": parsed.get("unreachable"),
        "terminating": parsed.get("terminating"),
        "function": parsed.get("function"),
    }

    for sname, sdata in (parsed.get("solvers") or {}).items():
        base = safe_slug(sname.lower().replace(" ", "_").replace("-", "_").replace(".", "_"))
        row[f"{base}_count"] = sdata.get("count")
        row[f"{base}_t_min_ms"] = sdata.get("t_min_ms")
        row[f"{base}_t_mid_ms"] = sdata.get("t_mid_ms")
        row[f"{base}_t_max_ms"] = sdata.get("t_max_ms")
        row.update(meta)

    proved = row.get("proved_goals")
    total = row.get("total_goals")
    meta_vg = row.get("meta_verified_goals")
    meta_tg = row.get("meta_total_goals")

    # Ratios
    row["proved_ratio"] = (proved / total) if (proved is not None and total) else None
    row["vs_meta_ratio"] = (proved / meta_tg) if (proved is not None and meta_tg) else None

    # Deltas vs reference
    row["delta_proved_vs_meta_verified_goals"] = (proved - meta_vg) if (proved is not None and meta_vg is not None) else None
    row["delta_total_vs_meta_total_goals"] = (total - meta_tg) if (total is not None and meta_tg is not None) else None

    return row


def read_meta(meta_path: Path) -> Dict[str, Any]:
    """
    Reads meta.txt like:
      file_name: ...
      verified: True
      verified_goals: 19
      total_goals: 19
    Returns dict with keys:
      meta_file_name, meta_verified, meta_verified_goals, meta_total_goals
    Missing file -> values None.
    """
    out: Dict[str, Any] = {
        "meta_file_name": None,
        "meta_verified": None,
        "meta_verified_goals": None,
        "meta_total_goals": None,
    }
    if not meta_path.exists():
        return out

    for line in meta_path.read_text(encoding="utf-8").splitlines():
        m = META_KV_RE.match(line)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        if k == "file_name":
            out["meta_file_name"] = v
        elif k == "verified":
            out["meta_verified"] = v.strip().lower() in ("true", "1", "yes", "y")
        elif k == "verified_goals":
            try: out["meta_verified_goals"] = int(v)
            except: pass
        elif k == "total_goals":
            try: out["meta_total_goals"] = int(v)
            except: pass
    return out

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="casp_10", help="Root directory containing case subdirectories.")
    ap.add_argument("--pattern", default="code_with_llm_spec_*.c", help="Glob pattern within each case directory.")
    ap.add_argument("--prefix", default="code_with_llm_spec_", help="Prefix used to infer provider/model from filename.")
    ap.add_argument("--prover", default="alt-ergo", help="WP prover (passed to -wp-prover).")
    ap.add_argument("--csv", default="framac_results.csv", help="Output CSV file.")
    ap.add_argument("--include", default="", help="Optional regex filter applied to filenames (after glob).")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    include_re = re.compile(args.include) if args.include else None

    rows = []
    for d in sorted([x for x in root.iterdir() if x.is_dir()], key=lambda p: p.name):
        files = sorted(d.glob(args.pattern))
        meta = read_meta(d / "meta.txt")
        if include_re:
            files = [f for f in files if include_re.search(f.name)]

        for f in files:
            provider, model = infer_provider_model_from_filename(f, args.prefix)
            print(f"[run] {f}  (provider={provider}, model={model})")

            rc, out, elapsed = run_framac(f, args.prover, provider, model)

            # One log per C file (inside same dir)
            log_name = f"framac_log_{safe_slug(provider)}_{safe_slug(model)}.log"
            (d / log_name).write_text(out, encoding="utf-8")

            parsed = parse_output(out)
            ## rows.append(flatten_row(d.name, f, provider, model, rc, parsed, elapsed, date_str))
            rows.append(flatten_row(d.name, f, provider, model, rc, parsed, elapsed, date_str, meta))

    df = pd.DataFrame(rows)
    df.to_csv(args.csv, index=False)
    print(f"Saved CSV {args.csv} (rows={len(df)})")


if __name__ == "__main__":
    main()
