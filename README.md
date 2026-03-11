# CASP LLM Verification Study

An automated evaluation pipeline to test LLM-generated ACSL specifications on [CASP](https://huggingface.co/datasets/nicher92/CASP_dataset) benchmark using Frama-C WP.

For each CASP benchmark pair:

- We generated C code annotated by different LLMs.
- Run Frama-C with Alt-Ergo on each version.
- Collect proof results _(proved goals, total goals, time, solver stats)_.
- Compare each LLM result against the reference verification (from casp).
- Aggregated everything into a **CSV** for statistical analysis.

Enables measurement of :
- How often each model fully verifies.
- How close each model is to the reference proof.
- How robust each model is across different programs.

## Documentation

For further details on the aggregated csv file _(columns, rows, etc)_ and steps to reproduce pipeline, please refer to _the documentation inside [docs](./docs/)_