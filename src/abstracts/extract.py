# =============================
# File: src/abstracts/extract.py
# =============================
"""PDF/OCR‑TXT ingestion & structure module."""
from __future__ import annotations

import re
import json
import pathlib as _pl
from typing import Iterator, List, Dict, Any
import yaml
import pandas as pd
from tqdm import tqdm

__all__ = ["Extractor", "parse_directory"]


class Extractor:
    """Parse OCR‑text files into structured records using YAML rule-set."""

    def __init__(self, rule_path: _pl.Path | str):
        self.rule_path = _pl.Path(rule_path)
        with self.rule_path.open("r", encoding="utf-8") as fp:
            cfg = yaml.safe_load(fp)
        self.header_patterns = {
            h["name"]: re.compile(h["pattern"], re.MULTILINE)
            for h in cfg.get("header", [])
        }
        self.splitter = re.compile(cfg["splitter"], re.MULTILINE)

    # ------------------------------------------------------------------
    def split_abstracts(self, text: str) -> List[str]:
        """Split raw OCR text into individual abstract blocks."""
        parts = re.split(self.splitter, text)
        # drop empty strings / whitespace-only
        return [p.strip() for p in parts if p.strip()]

    # ------------------------------------------------------------------
    def _extract_header(self, block: str) -> Dict[str, str]:
        meta: Dict[str, str] = {}
        for key, pat in self.header_patterns.items():
            m = pat.search(block)
            if m:
                meta[key] = m.group(key)
        return meta

    # ------------------------------------------------------------------
    def parse_block(self, block: str) -> Dict[str, Any]:
        meta = self._extract_header(block)
        content = block.split("\n", maxsplit=10)
        meta["abstract"] = "\n".join(content)
        return meta

    # ------------------------------------------------------------------
    def parse_file(self, path: _pl.Path | str, year: int | None = None) -> List[Dict[str, Any]]:
        path = _pl.Path(path)
        with path.open("r", encoding="utf-8", errors="ignore") as fp:
            text = fp.read()
        blocks = self.split_abstracts(text)
        recs = [self.parse_block(b) for b in blocks]
        if year:
            for r in recs:
                r["year"] = year
        return recs
