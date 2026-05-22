#!/usr/bin/env bash
set -euo pipefail

# build_bundle.sh — Génère aosis-deck-builder.zip pour distribution sur Claude.ai.
#
# Le ZIP contient un dossier racine aosis-deck-builder/ avec SKILL.md à
# l'intérieur (structure requise par Claude.ai). Les fichiers parasites
# (caches Python, lock files PowerPoint, Zone.Identifier, .pyc) sont
# explicitement exclus pour éviter les rejets côté upload.

SKILL_NAME="aosis-deck-builder"
BUNDLE_FILE="${SKILL_NAME}.zip"

cd "$(dirname "$0")"

# 0. Nettoyer les fichiers parasites présents sur disque + ancien bundle
echo "Nettoyage des fichiers parasites..."
find "${SKILL_NAME}" -name "~\$*" -type f -delete 2>/dev/null || true
find "${SKILL_NAME}" -name "*.Zone.Identifier" -type f -delete 2>/dev/null || true
rm -f "${BUNDLE_FILE}"
rm -f "${SKILL_NAME}.skill"

# 1. Vérifier que SKILL.md existe
if [ ! -f "${SKILL_NAME}/SKILL.md" ]; then
    echo "ERREUR : ${SKILL_NAME}/SKILL.md introuvable"
    exit 1
fi

# 2. Vérifier le frontmatter YAML (champ 'name' dans les 10 premières lignes)
if ! head -10 "${SKILL_NAME}/SKILL.md" | grep -q "^name:"; then
    echo "ERREUR : frontmatter YAML invalide dans SKILL.md (pas de champ 'name')"
    exit 1
fi

# 3. Créer le ZIP via Python (zip/unzip non installés sur ce poste).
#    Le script Python reproduit le comportement `zip -r ... -x patterns...`
#    avec les mêmes exclusions que le brief.
echo "Création du bundle ${BUNDLE_FILE}..."
python3 - <<PY
import os, fnmatch, zipfile
SKILL = "${SKILL_NAME}"
OUT = "${BUNDLE_FILE}"

# Patterns d'exclusion (équivalents aux -x de zip)
EXCLUDE_GLOBS = [
    f"{SKILL}/__pycache__/*",
    "*/__pycache__/*",
    f"{SKILL}/.pytest_cache/*",
    "*/~\$*",
    "*.pyc",
    "*.Zone.Identifier",
]

def excluded(path):
    return any(fnmatch.fnmatch(path, g) for g in EXCLUDE_GLOBS)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(SKILL):
        # Skip excluded directories early to avoid descending into them
        dirs[:] = [d for d in dirs if not excluded(os.path.join(root, d) + "/")]
        for fname in files:
            path = os.path.join(root, fname)
            if excluded(path):
                continue
            z.write(path, arcname=path)
PY

# 4. Vérification du contenu (équivalent unzip -l, via Python)
echo ""
echo "Vérification du contenu du bundle :"
python3 -c "
import zipfile
with zipfile.ZipFile('${BUNDLE_FILE}') as z:
    for i, n in enumerate(z.namelist()):
        if i < 10: print(f'  {n}')
    total = len(z.namelist())
    print(f'  ... ({total} entrées au total)' if total > 10 else f'  ({total} entrées)')
"

echo ""
echo "Recherche de fichiers parasites éventuels :"
if python3 -c "
import re, sys, zipfile
with zipfile.ZipFile('${BUNDLE_FILE}') as z:
    bad = [n for n in z.namelist() if re.search(r'~\\\$|Zone\\.Identifier|__pycache__|\\.pyc\$', n)]
print('\\n'.join(bad))
sys.exit(0 if not bad else 1)
"; then
    echo "OK — aucun fichier parasite"
else
    echo "ATTENTION : fichiers parasites détectés (voir ci-dessus)"
    exit 1
fi

# 5. Vérifier la structure (SKILL.md doit être à aosis-deck-builder/SKILL.md)
if ! python3 -c "
import zipfile
with zipfile.ZipFile('${BUNDLE_FILE}') as z:
    names = z.namelist()
import sys
sys.exit(0 if '${SKILL_NAME}/SKILL.md' in names else 1)
"; then
    echo "ERREUR : ${SKILL_NAME}/SKILL.md manquant dans le bundle (structure incorrecte)"
    exit 1
fi

SIZE=$(du -h "${BUNDLE_FILE}" | cut -f1)
echo ""
echo "Bundle créé avec succès : ${BUNDLE_FILE} (${SIZE})"
echo "Prêt à partager."
