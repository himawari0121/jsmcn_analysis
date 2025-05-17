# =============================
# File: src/cli/build_dashboard.py
# =============================
"""CLI: build or serve Plotly Dash dashboard."""
from __future__ import annotations

import pathlib as _pl
import duckdb as ddb
import pandas as pd
import typer
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = typer.Typer(add_help=False)


def _load_df(parquet_path: str):
    con = ddb.connect()
    return con.execute(f"SELECT * FROM parquet_scan('{parquet_path}')").df()


@app.command()
def serve(
    parquet_file: str = typer.Argument(...),
    host: str = "0.0.0.0",
    port: int = 8050,
):
    df = _load_df(parquet_file)
    years = sorted(df["year"].dropna().unique().astype(int))

    dash_app = Dash(__name__)
    dash_app.layout = html.Div([
        dcc.Slider(id="year-slider", min=min(years), max=max(years), value=min(years),
                    marks={int(y): str(int(y)) for y in years}, step=None),
        dcc.Graph(id="yearly-counts"),
    ])

    @dash_app.callback(
        Output("yearly-counts", "figure"),
        Input("year-slider", "value"),
    )
    def _update(year_value):
        sub = df[df["year"] == year_value]
        cnts = sub.groupby("session").size().reset_index(name="count")
        return px.bar(cnts, x="session", y="count", title=f"Session counts {year_value}")

    dash_app.run_server(host=host, port=port, debug=False)


if __name__ == "__main__":
    app()
