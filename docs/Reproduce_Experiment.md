## Reproduce Experiment

Following steps allow rebuilding dataset and regenerating final verification results _(framac_results.csv)_.

#### 01. Install dependencies

```python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure Frama-C _(with WP + Alt-Ergo)_ is installed :

```bash
frama-c -version
alt-ergo --version
```

Before running the pipeline, create a .env file containing API credentials used to generate ACSL. You can copy the provided template and fill in your keys:

`cp example_of_.env_file .env`

n.b. CASP dataset is publicly available on [HuggingFace](https://huggingface.co/datasets/nicher92/CASP_dataset) and does not require authentication for download.

#### 2. Sample CASP benchmark pairs

Download and sample a subset of CASP : `python 01_sample_casp.py`. 

- This creates the directory structure:

```bash
casp_10/
   00_327/
   01_57/
   ...
   09_52/
```

- Each folder contains:

    - **code.c** : original CASP program,
    
    - **spec.acsl** : reference specification,
    
    - **meta.txt** : reference verification metadata,

#### 3. Generate LLM specifications

Generate ACSL using multiple LLM providers : `python 02_generate_acsl_specs.py`
- This produces files such as:
    - _code\_with\_llm\_spec\_openai\_gpt-5.2.c_
    - _code\_with\_llm\_spec\_openai\_gpt-4o-mini.c_
    - _code\_with\_llm\_spec\_gemini\_gemini-2.5-flash.c_
    - _code\_with\_llm\_spec\_deepseek\_deepseek-chat.c_

#### 4. Run Frama-C verification

Execute Frama-C WP on each generated specification and collect results : `python 03_run_framac_collect.py`

- For every CASP pair, the script:
    - runs Frama-C with Alt-Ergo
    - stores verification logs in each directory
    - extracts proof statistics

#### 5. Final output

The pipeline produces `framac_results.csv`. 
- The file aggregates ***all verification results across models and CASP pairs*** 
- _(usefull for statistical analysis, comparison of LLM-generation, etc)_.
- For details on columns, please refer to _[CSV_Description.md](./CSV_Description.md)_