
# ------------------------------------------------
# Building an << LLM -> ACSL annotator>> for CASP.
#
# Example commands -->-
#     - python 02_generate_acsl_specs.py --root casp_10 \
#              --provider deepseek --model deepseek-chat --overwrite
#     - python 02_generate_acsl_specs.py --root casp_10 \
#              --provider openai --model gpt-5.2 --overwrite
#     - python 02_generate_acsl_specs.py --root casp_10 \
#              --provider gemini --model gemini-2.5-flash --overwrite
#     - python 02_generate_acsl_specs.py --root casp_10 \
#              --provider openai --model gpt-4o-mini --overwrite
# ----------------------------------------------
import os
import re
import sys
import argparse
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:
    tqdm = None

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from llm_provider import LLMProvider

import logging
import traceback

SYSTEM_PROMPT = (
    "You are a formal verification assistant for Frama-C ACSL.\n"
    "Given this C function, write ACSL contract annotations (requires/ensures/assigns, and loop invariants if needed).\n"
    "Return ONLY a valid ACSL comment block and the C function (with the ACSL inserted above it)."
)

HUMAN_PROMPT_TEMPLATE = (
    "Here is the C function. Produce the ACSL block and the function as requested.\n\n"
    "```c\n{code}\n```\n"
)


def safe_slug(s: str) -> str:
    s = s.strip()
    # Replace filesystem-unfriendly characters
    s = re.sub(r"[^\w.\-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "unknown"


def ensure_only_acsl_and_c(text: str) -> str:
    out = text.strip()
    if out.startswith("```"):
        first_newline = out.find("\n")
        if first_newline != -1:
            out = out[first_newline + 1 :]
        if out.endswith("```"):
            out = out[:-3]
        out = out.strip()
    return out


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def call_model(llm, code: str) -> str:
    # Keep it simple: use llm.invoke with plain string prompt
    prompt = SYSTEM_PROMPT + "\n\n" + HUMAN_PROMPT_TEMPLATE.format(code=code)
    resp = llm.invoke(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)


def process_one(llm, code_path: Path, output_path: Path, overwrite: bool):
    if output_path.exists() and not overwrite:
        return False, f"Skip (exists): {output_path}"

    code = read_text(code_path)
    raw = call_model(llm, code)
    cleaned = ensure_only_acsl_and_c(raw)
    write_text(output_path, cleaned)
    return True, f"Wrote: {output_path}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="casp_10")
    parser.add_argument("--provider", type=str, default=os.getenv("LLM_PROVIDER", "openai"))
    parser.add_argument("--model", type=str, default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--log-level", type=str, default="INFO",
                        help="DEBUG | INFO | WARNING | ERROR")
    parser.add_argument("--log-file", type=str, default="run.log",
                        help="Optional path to a log file (e.g., run.log)")
        
    args = parser.parse_args()

    root = Path(args.root).resolve()
    pairs = []
    for child in root.iterdir():
        if child.is_dir():
            code_path = child / "code.c"
            if code_path.exists():
                pairs.append(code_path)

    if not pairs:
        print(f"No code.c files found under {root}")
        sys.exit(1)

    level = getattr(logging, args.log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if args.log_file: handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))    
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=handlers
    )    
    logging.info("Starting ACSL generation")
    logging.info("provider=%s model=%s root=%s overwrite=%s", args.provider, args.model, root, args.overwrite)


    llm = LLMProvider.load(args.provider, args.model, temperature=0.0)

    provider_slug = safe_slug(args.provider)
    model_slug = safe_slug(args.model)

    iterator = tqdm(pairs, desc="Generating ACSL", unit="file") if tqdm else pairs
    ok_count, skip_count, err_count = 0, 0, 0

    for code_path in iterator:
        out_name = f"code_with_llm_spec_{provider_slug}_{model_slug}.c"
        out_path = code_path.parent / out_name
        try:
            ok, msg = process_one(llm, code_path, out_path, args.overwrite)
            if ok:
                ok_count += 1
            else:
                skip_count += 1
            # If tqdm is used, you still get a useful postfix
            if tqdm and iterator is not pairs:
                iterator.set_postfix_str(f"ok={ok_count} skip={skip_count} err={err_count}")
            else:
                print(msg)
        except Exception as e:
            err_count += 1
            logging.error("Failed on %s", code_path)
            logging.error("Exception: %s: %s", type(e).__name__, str(e))
            logging.debug("Traceback:\n%s", traceback.format_exc())            
            ## if tqdm and iterator is not pairs:
            ##     iterator.set_postfix_str(f"ok={ok_count} skip={skip_count} err={err_count}")
            ## else:
            ##     print(f"Error on {code_path}: {e}", file=sys.stderr)

    print(f"Done. ok={ok_count}, skipped={skip_count}, errors={err_count}, total={len(pairs)}")


if __name__ == "__main__":
    main()
