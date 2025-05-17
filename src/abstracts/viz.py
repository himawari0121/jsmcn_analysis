# =============================
# File: src/abstracts/viz.py
# =============================
"""Matplotlib / Plotly helper charts."""
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import networkx as nx
from wordcloud import WordCloud

__all__ = [
    "plot_yearly_keyword", "plot_wordcloud", "plot_cooccurrence_network"
]


def plot_yearly_keyword(df: pd.DataFrame, keyword: str, ax=None):
    data = df[df["abstract"].str.contains(keyword, case=False, na=False)]
    cts = data.groupby("year").size()
    ax = ax or plt.gca()
    cts.plot(kind="bar", ax=ax, title=f"Yearly frequency of '{keyword}'")
    ax.set_ylabel("count")
    return ax


def plot_wordcloud(freq_dict: dict[str, int]):
    wc = WordCloud(width=1200, height=600, background_color="white")
    img = wc.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(12, 6))
    plt.imshow(img, interpolation="bilinear")
    plt.axis("off")


def plot_cooccurrence_network(df: pd.DataFrame, top_n: int = 50):
    from itertools import combinations
    import collections

    counter = collections.Counter()
    for toks in df["tokens"]:
        unique = set(toks)
        for a, b in combinations(sorted(unique), 2):
            counter[(a, b)] += 1
    most_common = counter.most_common(top_n)
    G = nx.Graph()
    for (a, b), w in most_common:
        G.add_edge(a, b, weight=w)
    pos = nx.spring_layout(G, k=0.5, seed=42)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=100, alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=[d["weight"] * 0.1 for _, _, d in G.edges(data=True)], alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Keyword Co‑occurrence Network")
    plt.axis("off")
