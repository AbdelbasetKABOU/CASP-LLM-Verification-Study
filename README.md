# CASP-LLM-Verification-Study

An automated evaluation pipeline to test LLM-generated ACSL specifications on [CASP](https://huggingface.co/datasets/nicher92/CASP_dataset) dataset using Frama-C WP.

For each CASP benchmark pair:

- We generated C code annotated by different LLMs.
- We ran Frama-C with Alt-Ergo on each version.
- We collected proof results (proved goals, total goals, time, solver stats).
- We compared each LLM result against the reference verification (from meta.txt).
- We aggregated everything into a **CSV** for statistical analysis.

Allows us to measure:
- How often each model fully verifies.
- How close each model is to the reference proof.
- How robust each model is across different programs.
