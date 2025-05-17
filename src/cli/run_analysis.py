# =============================
# File: src/cli/run_analysis.py
# =============================
"""CLI: run entire analysis pipeline."""
from __future__ import annotations

import pathlib as _pl
import json
import typer
import duckdb as ddb
import pandas as pd
from abstracts.preprocess import clean_text, tokenize_df
from abstracts.topic import lda_topics
from abstracts.viz import plot_yearly_keyword
import matplotlib.pyplot as plt

app = typer.Typer(add_help=False)


@app.command()
def main(
    parquet_file: str = typer.Argument(...),
    out_dir: str = typer.Option("reports/figures", help="Output dir"),
):
    out_dir = _pl.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # --- Load parquet via DuckDB ---
    con = ddb.connect()
    df = con.execute(f"SELECT * FROM parquet_scan('{parquet_file}')").df()
    df["abstract_clean"] = df["abstract"].map(clean_text)
    df = tokenize_df(df, text_col="abstract_clean")
    # --- LDA quick demo ---
    W, topics = lda_topics(df["abstract_clean"].tolist(), n_topics=10)
    # dump topics json
    (_pl.Path(out_dir) / "lda_topics.json").write_text(json.dumps(topics, ensure_ascii=False, indent=2))
    # --- Plot keyword trend example ---
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_yearly_keyword(df, "ai", ax=ax)
    fig.tight_layout()
    fig.savefig(out_dir / "ai_trend.png", dpi=300)
    typer.echo("[analysis] done → " + str(out_dir))

if __name__ == "__main__":
    app()
