# =============================
# File: src/abstracts/extract.py
# =============================
"""PDF/OCR‑TXT ingestion & structure module."""
from __future__ import annotations

import re
import pathlib as _pl
from functools import lru_cache
from typing import Iterator, List, Dict, Any
import pandas as pd


def _parse_simple_yaml(text: str) -> Dict[str, Any]:
    header: List[Dict[str, str]] = []
    current: Dict[str, str] | None = None
    cfg: Dict[str, Any] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("header:"):
            continue
        if line.lstrip().startswith("- name:"):
            if current:
                header.append(current)
            current = {
                "name": line.split(":", 1)[1].strip().strip("'\"")
            }
        elif line.lstrip().startswith("pattern:") and current is not None:
            val = line.split(":", 1)[1].strip().strip("'\"")
            current["pattern"] = val.replace("\\\\", "\\")
        elif line.startswith("splitter:"):
            val = line.split(":", 1)[1].strip().strip("'\"")
            cfg["splitter"] = val.replace("\\\\", "\\")
    if current:
        header.append(current)
    cfg["header"] = header
    return cfg


@lru_cache(maxsize=8)
def _load_rule(path: str | _pl.Path) -> Dict[str, Any]:
    """Load YAML rule file with a simple cache."""
    p = _pl.Path(path)
    try:
        import yaml
    except ModuleNotFoundError:
        return _parse_simple_yaml(p.read_text(encoding="utf-8"))
    with p.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

__all__ = ["Extractor", "parse_directory"]


class Extractor:
    """Parse OCR‑text files into structured records using YAML rule-set."""

    def __init__(self, rule_path: _pl.Path | str):
        self.rule_path = _pl.Path(rule_path)
        cfg = _load_rule(self.rule_path)
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

    # ------------------------------------------------------------------
    def parse_directory(self, txt_dir: _pl.Path | str) -> pd.DataFrame:
        """Parse all `.txt files under a directory into a DataFrame."""
        dir_path = _pl.Path(txt_dir)
        records: list[dict[str, Any]] = []
        for txt_file in sorted(dir_path.glob("*.txt")):
            year_match = re.search(r"(\d{4})", txt_file.stem)
            year = int(year_match.group(1)) if year_match else None
            recs = self.parse_file(txt_file, year=year)
            for r in recs:
                r.setdefault("file", txt_file.name)
            records.extend(recs)
        return pd.DataFrame(records)


def parse_directory(txt_dir: _pl.Path | str, rule: _pl.Path | str) -> pd.DataFrame:
    """Convenience wrapper around :class:Extractor for one-off use."""
    extractor = Extractor(rule)
    return extractor.parse_directory(txt_dir)
