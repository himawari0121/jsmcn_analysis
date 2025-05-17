# =============================
# File: src/abstracts/topic.py
# =============================
"""Topic modelling utilities (TF‑IDF + LDA, optional BERTopic)."""
from __future__ import annotations

from typing import Tuple, List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_score
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import optuna

__all__ = [
    "lda_topics",
    "bertopic_topics",
]


def lda_topics(texts: List[str], n_topics: int = 20, max_features: int = 5000):
    vect = CountVectorizer(max_features=max_features, min_df=5)
    X = vect.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, learning_method="batch")
    W = lda.fit_transform(X)
    H = lda.components_  # shape (n_topics, vocab)
    vocab = vect.get_feature_names_out()
    topic_words = {
        i: [vocab[idx] for idx in H[i].argsort()[::-1][:15]] for i in range(n_topics)
    }
    return W, topic_words


def _objective_bertopic(trial, docs: List[str]):
    n_neighbors = trial.suggest_int("n_neighbors", 5, 50)
    n_components = trial.suggest_int("n_components", 5, 20)
    hdb_min_cluster_size = trial.suggest_int("min_cluster_size", 5, 80)
    model = BERTopic(
        embedding_model=SentenceTransformer("all-MiniLM-L6-v2"),
        hdbscan_model_kwargs={"min_cluster_size": hdb_min_cluster_size},
        umap_model_kwargs={"n_neighbors": n_neighbors, "n_components": n_components},
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = model.fit_transform(docs)
    score = model.get_coherence()
    return score


def bertopic_topics(docs: List[str], optimize: bool = False):
    if optimize:
        study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
        study.optimize(lambda tr: _objective_bertopic(tr, docs), n_trials=30, show_progress_bar=True)
        best_params = study.best_params
        print("[Optuna] best params", best_params)
        model = BERTopic(
            embedding_model=SentenceTransformer("all-MiniLM-L6-v2"),
            hdbscan_model_kwargs={"min_cluster_size": best_params["min_cluster_size"]},
            umap_model_kwargs={
                "n_neighbors": best_params["n_neighbors"],
                "n_components": best_params["n_components"],
            },
        )
    else:
        model = BERTopic(embedding_model="all-MiniLM-L6-v2")
    topics, probs = model.fit_transform(docs)
    return model, topics, probs
