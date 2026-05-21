# Chantier — Ménage du dossier de travail + repackaging du `.skill`

**Date** : 2026-05-19
**Périmètre** : Repackager le bundle `.skill` à jour, archiver l'historique des chantiers, ne conserver dans `aosis-deck-builder/` que l'essentiel pour faire tourner le skill et ses tests.

## TL;DR

- ✅ `aosis-deck-builder.skill` régénéré (**648 KB**, 11 entrées, ZIP intègre).
- ✅ `aosis-deck-builder/` réduit à **1.1 MB** (essentiel uniquement).
- ✅ `_archive/` créé (**102 MB**) avec reports, assets, backups, snapshot, anciens test outputs.
- ✅ `examples/` créé avec 2 specs JSON + README.
- ✅ `test_skill.sh` à la racine : **22 passed, 1 skipped** + 2 decks générés en une commande.
- ✅ Snapshot complet sauvegardé : `_archive/snapshots/aosis-deck-builder-snapshot-2026-05-19.tar.gz` (50 MB, 130 entries).

## 1. Mouvements de fichiers

### Vers `_archive/reports/` (11 rapports)
```
chantier1_report.md, chantier2_report.md, chantier3_report.md, chantier4_report.md,
chantier5_report.md, chantier6_report.md, chantier7_report.md, chantier8_report.md,
chantier_consolidation_report.md, chantier_exhibits_report.md, chantier_naming_report.md
```
(Le présent rapport reste à la racine — c'est le rapport courant.)

### Vers `_archive/assets/` (7 dossiers)
```
chantier1_assets/, chantier2_assets/, chantier6_assets/, chantier7_assets/,
chantier8_assets/, chantier_consolidation_assets/, chantier_exhibits_assets/
```

### Vers `_archive/backups/`
```
AOSIS_template.backup-before-merge.pptx
AOSIS_template.backup.pptx
AOSIS_template.before-naming.pptx
AOSIS_template_v2.pptx          (36 MB, exploration Template RH non utilisée)
exhibits.backup-before-merge.pptx
exhibits.backup.pptx
exhibits.pptx                    (source historique des 16 slides modèles)
```

### Vers `_archive/snapshots/`
```
aosis-deck-builder-snapshot-2026-05-19.tar.gz  (50 MB, état complet pré-ménage)
```

### Vers `_archive/test_outputs/`
```
aosis-deck-builder/tests/out/      (anciens .pptx résiduels)
aosis-deck-builder/tests/out_before/
aosis-deck-builder/tests/out_png/
aosis-deck-builder/tests/out_png_c2/
```

### Supprimés
```
aosis-deck-builder/.pytest_cache/
aosis-deck-builder/aosis_deck_builder.egg-info/
aosis-deck-builder/scripts/__pycache__/
aosis-deck-builder/tests/__pycache__/
aosis-deck-builder/assets/~$exhibits.pptx       (lock files PowerPoint)
aosis-deck-builder/assets/Template RH.pptx:Zone.Identifier  (NTFS metadata stub)
```

## 2. Tailles avant / après

### Avant ménage (estimation depuis snapshot tar.gz)
| Élément | Taille |
|---|---|
| `Skill_pptx_Aosis/` total (sans `_archive/`) | **~100 MB** |
| `aosis-deck-builder/` (avec caches, egg-info, backups, ancien v2) | **~46 MB** |
| Rapports + assets en vrac à la racine | ~6 MB |
| Bundle `.skill` (obsolète au 13 mai) | 591 KB |

### Après ménage
| Élément | Taille |
|---|---|
| `aosis-deck-builder/` | **1.1 MB** ✅ |
| `aosis-deck-builder.skill` (à jour) | **648 KB** ✅ |
| `examples/` | 20 KB |
| `test_skill.sh` | 4 KB |
| `_archive/` (total) | **102 MB** (historique complet préservé) |
| ↳ `_archive/backups/` | 41 MB |
| ↳ `_archive/snapshots/` | 51 MB |
| ↳ `_archive/test_outputs/` | 7.8 MB |
| ↳ `_archive/assets/` | 3.8 MB |
| ↳ `_archive/reports/` | 152 KB |

→ **Dossier de travail actif** = `aosis-deck-builder/` + `aosis-deck-builder.skill` + `examples/` + `test_skill.sh` ≈ **1.8 MB** (réduction × 25).

## 3. Contenu du bundle `.skill` à jour

```
SKILL.md                                7 163 bytes
pyproject.toml                          1 064
scripts/template_engine.py             27 824
scripts/visual_review.py               12 416
scripts/brand.py                        4 521
scripts/build_deck.py                  61 851
scripts/chart_engine.py                14 234
references/qa.md                        4 718
references/layouts.md                  12 342
references/json-schema.md              19 230
assets/AOSIS_template.pptx            605 763
─────────────────────────────────────────────
Uncompressed total                    771 126
Compressed on disk                    648 356  (< 5 MB ✅)
ZIP integrity                              OK
Entries                                    11
```

Exclus du bundle (présents dans le repo mais pas dans le `.skill`
distribué) : `tests/`, caches, `*.egg-info/`, anciens backups, `exhibits.pptx`.

## 4. Structure finale du projet

```
Skill_pptx_Aosis/
├── CHANGELOG.md                  (historique compact des chantiers)
├── README.md                     (quickstart projet)
├── aosis-deck-builder.skill      (bundle distribuable, 648 KB)
├── test_skill.sh                 (pytest + génération exemples en 1 commande)
├── chantier_menage_report.md     (ce rapport)
├── aosis-deck-builder/           (dossier source du skill, 1.1 MB)
│   ├── SKILL.md
│   ├── pyproject.toml
│   ├── scripts/                  (build_deck, template_engine, chart_engine,
│   │                              brand, visual_review)
│   ├── references/               (layouts.md, json-schema.md, qa.md)
│   ├── assets/
│   │   └── AOSIS_template.pptx   (template canonique, 17 slides nommées)
│   └── tests/
│       ├── test_smoke.py         (23 tests, ~2 s)
│       └── fixtures/             (10 fixtures JSON)
├── examples/
│   ├── README.md
│   ├── example_minimal.json      (cover + 3 + closing)
│   └── example_full.json         (cover + 12 + closing, 11 layouts)
├── _archive/                     (historique complet, 102 MB)
│   ├── README.md
│   ├── reports/                  (11 rapports chantier)
│   ├── assets/                   (7 dossiers chantier_*_assets)
│   ├── backups/                  (templates et exhibits historiques)
│   ├── snapshots/                (tar.gz pré-ménage)
│   └── test_outputs/             (anciens outputs résiduels)
└── Ressources/                   (intacte — source RH d'origine)
```

## 5. Vérifications finales

### a) pytest
```
22 passed, 1 skipped in 1.76s
```
Le skip est `test_visual_review_generates_artifacts` (soffice/pdftoppm absent — comportement pré-existant, neutre).

### b) Génération des exemples
```
==> Generate example_minimal.pptx
OK — wrote /tmp/aosis-deck-builder-test/example_minimal.pptx (581,390 bytes)

==> Generate example_full.pptx
OK — wrote /tmp/aosis-deck-builder-test/example_full.pptx (637,186 bytes)
```

### c) `.skill` intègre
```
$ python -c "import zipfile; print(zipfile.ZipFile('aosis-deck-builder.skill').testzip() or 'OK')"
OK
```
**648 KB** < 5 MB ✅. 11 entrées, conforme à la liste d'inclusion/exclusion spécifiée.

## 6. Friction technique

**Un test cassait après archivage de `exhibits.pptx`** : `test_template_layouts_discovery` pointait en dur sur `assets/exhibits.pptx`. Ce comportement était documenté dans le chantier consolidation comme « conservé tel quel parce que exhibits.pptx existait encore comme archive en place ». Avec le ménage, exhibits.pptx est passé dans `_archive/backups/`, donc l'assertion échouait.

**Fix appliqué** : rebascule du test sur `TEMPLATE` (constante du test = `assets/AOSIS_template.pptx`), qui héberge désormais les layouts nommés depuis le chantier consolidation. Une ligne modifiée dans `tests/test_smoke.py` (l.208-209). Le test continue de vérifier la même invariante (≥10 layouts nommés découverts, dont 4 layouts canonical).

**Périmètre** : modifier un test pour qu'il reste valide après une réorganisation du repo est dans l'esprit du « Ne supprime aucun test » — le test est **conservé et fonctionnel**, simplement pointé sur le nouveau chemin canonique.

## 7. Livrables

| Livrable | Statut | Taille |
|---|---|---|
| `aosis-deck-builder.skill` (bundle distribuable, à jour) | ✅ créé | 648 KB |
| `aosis-deck-builder/` (rangé) | ✅ nettoyé | 1.1 MB |
| `_archive/` (historique structuré) | ✅ créé | 102 MB |
| `examples/example_minimal.json` | ✅ créé | 1.2 KB |
| `examples/example_full.json` | ✅ créé | 3.9 KB |
| `examples/README.md` | ✅ créé | 0.9 KB |
| `test_skill.sh` (1 commande) | ✅ créé | 1.0 KB |
| `chantier_menage_report.md` | ✅ créé | (ce fichier) |

---

**Statut final** : ✅ Ménage **livré sans régression**. Bundle `.skill` à jour disponible, dossier de travail réduit × 25, historique préservé intégralement.
