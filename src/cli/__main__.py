
# =============================
# File: src/cli/__main__.py
# =============================
"""Aggregate all sub‑CLI via Typer multi‑command."""
import typer
from cli import ingest as _ingest
from cli import run_analysis as _run
from cli import build_dashboard as _dash

app = typer.Typer(add_help=False)
app.add_typer(_ingest.app, name="ingest")
app.add_typer(_run.app, name="analyze")
app.add_typer(_dash.app, name="dash")

if __name__ == "__main__":
    app()

