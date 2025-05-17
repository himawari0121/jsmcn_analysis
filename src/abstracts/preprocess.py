# =============================
# File: src/abstracts/preprocess.py
# =============================
"""Text cleaning + spaCy pipeline wrapper."""
from __future__ import annotations

import re
from functools import lru_cache
from typing import List
import pandas as pd
import spacy
from tqdm import tqdm

__all__ = ["load_spacy", "clean_text", "tokenize_df"]


@lru_cache(maxsize=4)
def load_spacy(lang: str = "ja"):
    if lang == "en":
        return spacy.load("en_core_web_sm")
    if lang == "ja":
        return spacy.load("ja_core_news_sm")
    raise ValueError(f"Unsupported language: {lang}")


def clean_text(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\s一-龯ぁ-んァ-ン]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def tokenize_df(df: pd.DataFrame, text_col: str = "abstract", lang: str = "ja") -> pd.DataFrame:
    nlp = load_spacy(lang)
    tokens_col, lemmas_col = [], []
    for doc in tqdm(nlp.pipe(df[text_col].astype(str).tolist(), batch_size=64)):
        toks = [t.text for t in doc if not t.is_stop and not t.is_punct]
        lems = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
        tokens_col.append(toks)
        lemmas_col.append(lems)
    df = df.copy()
    df["tokens"] = tokens_col
    df["lemmas"] = lemmas_col
    return df
