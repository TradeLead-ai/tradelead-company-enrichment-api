# Python Examples

This directory contains examples of how to use the TradeLead Company Enrichment API with Python.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key as an environment variable:
   ```bash
   export TRADELEAD_API_KEY="tl_live_your_key_here"
   ```

## Examples

### 1. `quickstart.py`
A minimal, dependency-free (only uses the built-in `requests` library) script that submits a single company, polls the API for completion, and prints the enriched profile.

**Run it:**
```bash
python quickstart.py
```

### 2. `enrich_from_excel.py`
A complete, real-world script that reads a list of companies from an Excel or CSV file, submits them as a batch to the API, polls until the job finishes, and writes the enriched data (including firmographics, contacts, and trade data) to a new file.

This example uses `pandas` for easy data manipulation.

**Run it:**
```bash
python enrich_from_excel.py --input sample_companies.csv --output enriched_companies.csv
```
