#!/usr/bin/env bash
set -euo pipefail

# プロジェクトのルート
ROOT="/Users/tanakamasaya/jsmcn_analysis"

# ── ① つくるフォルダ一覧 ─────────────────────────
DIRS=(
  conf/extract
  data/raw_pdf
  data/raw
  data/staged
  data/warehouse
  notebooks
  reports/figures
  src/abstracts
  src/cli
  tests
)

# ── ② つくるファイル一覧（空ファイル） ───────────────
FILES=(
  README.md
  pyproject.toml
  requirements.txt
  conf/extract/jscn.yml
  notebooks/01_data_inspection.ipynb
  notebooks/02_text_mining.ipynb
  notebooks/03_visualization.ipynb
  src/abstracts/__init__.py
  src/abstracts/extract.py
  src/abstracts/preprocess.py
  src/abstracts/topic.py
  src/abstracts/viz.py
  src/cli/__init__.py
  src/cli/__main__.py
  src/cli/ingest.py
  src/cli/run_analysis.py
  src/cli/build_dashboard.py
  tests/test_extract.py
)

# ── ③ ディレクトリを作成 ────────────────────────
for d in "${DIRS[@]}"; do
  mkdir -p "${ROOT}/${d}"
done

# ── ④ 空ファイルを作成（既にあればスキップ） ─────────
for f in "${FILES[@]}"; do
  file="${ROOT}/${f}"
  [[ -e "${file}" ]] || touch "${file}"
done

echo "✅  Scaffolding complete under ${ROOT}"
