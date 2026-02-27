# ----------------------------------------------
# download + sample 10 pairs into a local folder
# ----------------------------------------------
import os
import random
from datasets import load_dataset

OUT_DIR = "casp_10"
N = 10
SEED = 42

random.seed(SEED)
os.makedirs(OUT_DIR, exist_ok=True)

ds = load_dataset("nicher92/CASP_dataset", split="train")  # 506 rows
idxs = random.sample(range(len(ds)), N)

for k, idx in enumerate(idxs):
    row = ds[idx]
    pair_id = f"{k:02d}_{idx}"
    pair_dir = os.path.join(OUT_DIR, pair_id)
    os.makedirs(pair_dir, exist_ok=True)

    # Minimal artifacts for your tasks
    with open(os.path.join(pair_dir, "code.c"), "w") as f:
        f.write(row.get("c_code_snippet", row.get("function_implementation", "")))

    with open(os.path.join(pair_dir, "spec.acsl"), "w") as f:
        f.write(row.get("acsl_snippet", ""))

    # Useful metadata (what CASP already verified)
    with open(os.path.join(pair_dir, "meta.txt"), "w") as f:
        f.write(f"file_name: {row.get('file_name')}\n")
        f.write(f"verified: {row.get('verified')}\n")
        f.write(f"verified_goals: {row.get('verified_goals')}\n")
        f.write(f"total_goals: {row.get('total_goals')}\n")
