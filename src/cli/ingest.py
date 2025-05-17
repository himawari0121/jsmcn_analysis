# =============================
# File: src/cli/ingest.py
# =============================
"""CLI: txt → structured parquet"""
from __future__ import annotations

import pathlib as _pl
import typer
import duckdb as ddb
import pyarrow as pa
import pyarrow.parquet as pq
from abstracts.extract import parse_directory

app = typer.Typer(add_help=False)


@app.command()
def main(
    txt_dir: str = typer.Argument(..., help="Directory containing OCR txt files"),
    rule: str = typer.Option("conf/extract/jscn.yml", help="YAML rule file"),
    out: str = typer.Option("data/warehouse/abstracts.parquet", help="Output Parquet file"),
):
    """Parse directory & write parquet."""
    df = parse_directory(txt_dir, rule)
    out_path = _pl.Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, out_path, compression="zstd")
    typer.echo(f"[ingest] wrote {len(df):,} rows → {out}")


if __name__ == "__main__":
    app()
