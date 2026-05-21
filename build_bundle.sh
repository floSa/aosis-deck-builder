#!/usr/bin/env bash
# Regenerate `aosis-deck-builder.skill` (zip bundle of the skill) from the
# current state of `aosis-deck-builder/`. Run this after any change to the
# scripts, references, SKILL.md, or assets before uploading the bundle to
# Claude. Excludes tests, caches, and chantier backups.

set -euo pipefail
cd "$(dirname "$0")"

python3 - <<'PY'
import zipfile
from pathlib import Path

src = Path("aosis-deck-builder")
out = Path("aosis-deck-builder.skill")

EXCLUDE_DIRS = {"tests", "__pycache__", ".pytest_cache"}
EXCLUDE_SUFFIX = (".pyc",)
EXCLUDE_NAME_CONTAINS = (".before-chantier",)

entries = []
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(src.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if p.suffix in EXCLUDE_SUFFIX:
            continue
        if any(s in p.name for s in EXCLUDE_NAME_CONTAINS):
            continue
        z.write(p, arcname=str(rel))
        entries.append(str(rel))

size_kb = out.stat().st_size / 1024
print(f"Built {out} — {len(entries)} entries, {size_kb:.1f} KB")
for e in entries:
    print(f"  {e}")
PY
