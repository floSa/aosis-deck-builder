#!/usr/bin/env bash
# test_skill.sh — Smoke test du skill aosis-deck-builder.
# Lance pytest puis génère deux decks d'exemple (minimal + full).
# Usage: ./test_skill.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILL="$ROOT/aosis-deck-builder"
EXAMPLES="$ROOT/examples"
OUT_DIR="${OUT_DIR:-/tmp/aosis-deck-builder-test}"

# Pick a Python interpreter: prefer venv at /tmp/pptx_venv, else fall back to python3
PY="${PYTHON:-/tmp/pptx_venv/bin/python}"
if ! command -v "$PY" >/dev/null 2>&1; then
    PY=python3
fi

mkdir -p "$OUT_DIR"

echo "==> pytest"
cd "$SKILL"
"$PY" -m pytest tests/ --no-header -q
cd "$ROOT"

echo
echo "==> Generate example_minimal.pptx"
"$PY" "$SKILL/scripts/build_deck.py" \
    "$EXAMPLES/example_minimal.json" \
    "$OUT_DIR/example_minimal.pptx"

echo
echo "==> Generate example_full.pptx"
"$PY" "$SKILL/scripts/build_deck.py" \
    "$EXAMPLES/example_full.json" \
    "$OUT_DIR/example_full.pptx"

echo
echo "==> All green. Generated files:"
ls -lh "$OUT_DIR"/*.pptx
