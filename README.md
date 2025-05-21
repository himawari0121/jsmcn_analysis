# Abstracts ETL Platform

This project provides a small toolkit for parsing OCR text files of scientific abstracts and performing some basic NLP analysis. The code is intentionally minimal so it can run in constrained environments.

## Installation

Use Python 3.11+. Install required packages via pip:

```bash
pip install -r requirements.txt
```

You can also install the package in editable mode:

```bash
pip install -e .
```

## Command line usage

Several CLI commands are provided through `abstracts-cli`:

```bash
# Ingest OCR text files and produce a parquet dataset
abstracts-cli ingest <txt_dir> --rule conf/extract/jscn.yml

# Run a quick analysis pipeline and output figures
abstracts-cli analyze <parquet_file>
```

## Development workflow

- Format code with [black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/).
- Type check with [mypy](https://mypy-lang.org/).
- Run tests with:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Repository layout

```
conf/       # configuration files
src/        # library & CLI code
notebooks/  # analysis notebooks
tests/      # unit tests
```
