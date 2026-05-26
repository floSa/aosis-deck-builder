# AOSIS Deck Builder

Claude Skill qui génère des présentations PowerPoint à la charte AOSIS (`.pptx`) — style consulting top-tier (hero stats, KPI XXL avec drop shadows, matrices 2×2, roadmaps, charts matplotlib, data tables, layout libre `canvas_blank`) — depuis une **spec JSON** unique.

Le skill part toujours du template officiel `AOSIS_template.pptx`, donc la charte graphique (navy/orange, logo, Arial, footers) est héritée par construction. **17 layouts template-based** + **canvas_blank** freeform à 6 blocs (kpi_card, bullets, text, image, chart, quote).

## Philosophy — Communication first, design second

Ce skill remplace l'approche design-forward par défaut de Claude par les standards consulting AOSIS. La thèse : **un deck consulting n'est pas une collection de slides jolies, c'est un argument structuré qui convainc un COMEX/CODIR de trancher**.

Concrètement, quand le skill est actif, Claude doit :

- Écrire chaque titre comme une **phrase d'action** qui énonce le take-away (jamais un mot-clé).
- Structurer le deck selon le canevas consulting **Diagnostic → Vision → Stratégie → Plan → Next Steps**.
- Appliquer le **ghost deck test** : les titres lus en séquence doivent raconter l'histoire complète.
- Respecter **une slide = un message**, exhibits annotés, sources systématiques, clôture `closing_diagonal` + `final_branding`.

Le détail (structure narrative, action titles, ghost deck test, discipline des exhibits, anti-patterns, checklist QA) est codé en dur dans [`aosis-deck-builder/references/philosophy.md`](aosis-deck-builder/references/philosophy.md).

## 📚 Documentation

Toute la documentation se trouve dans [`docs/`](docs/) :

- **[`docs/GUIDE_INSTALLATION.md`](docs/GUIDE_INSTALLATION.md)** — installation pas-à-pas (venv, dépendances, clé Pexels, premier build)
- **[`docs/GUIDE_OPERATIONNEL.md`](docs/GUIDE_OPERATIONNEL.md)** — mode d'emploi au quotidien : choisir les layouts, écrire des specs JSON, debugger
- **[`docs/chantiers/`](docs/chantiers/)** — historique de décisions par chantier (17 rapports détaillés)
- **[`CHANGELOG.md`](CHANGELOG.md)** — vue synthétique du changelog

## Quick start

```bash
# 1. Installer
pip install -e aosis-deck-builder/

# 2. Copier le .env exemple et remplir la clé Pexels (optionnel)
cp .env.example .env
# éditer .env → PEXELS_API_KEY=...

# 3. Générer un deck depuis une spec JSON
python aosis-deck-builder/scripts/build_deck.py \
    examples/example_minimal.json out.pptx \
    --template aosis-deck-builder/assets/AOSIS_template.pptx
```

Détails complets dans [`docs/GUIDE_INSTALLATION.md`](docs/GUIDE_INSTALLATION.md) et [`docs/GUIDE_OPERATIONNEL.md`](docs/GUIDE_OPERATIONNEL.md).

CLI flags : `--debug-layouts`, `--no-images`, `--no-cache-images`, `--clear-image-cache`, `--template <path>`.

## Structure du projet

```
.
├── README.md                          # vous êtes ici
├── CHANGELOG.md                       # changelog synthétique
├── .env.example                       # template de configuration (.env gitignored)
├── build_bundle.sh                    # regénère aosis-deck-builder.zip
├── test_skill.sh                      # smoke-test rapide
│
├── aosis-deck-builder/                # le skill Claude (source)
│   ├── SKILL.md                       # entry point Claude (≤200 l)
│   ├── pyproject.toml
│   ├── references/                    # progressive-disclosure references
│   │   ├── layouts.md                 # fiches détaillées (17 template + 11 code)
│   │   ├── json-schema.md             # schéma JSON exhaustif
│   │   ├── qa.md                      # workflow QA visuel + contenu
│   │   └── icons_suggested.md         # icônes Iconify recommandées
│   ├── scripts/
│   │   ├── build_deck.py              # orchestrateur (CLI + dispatch layouts)
│   │   ├── template_engine.py         # rendu template-based + canvas_blank + data_table
│   │   ├── chart_engine.py            # 8 types de charts matplotlib
│   │   ├── image_engine.py            # Pexels API + cache disque + Picsum
│   │   ├── icon_engine.py             # Iconify API
│   │   ├── brand.py                   # palette extraite du theme XML
│   │   └── visual_review.py           # capture screenshots + détection défauts
│   ├── assets/
│   │   └── AOSIS_template.pptx        # template canonique, source unique de charte
│   └── tests/test_smoke.py            # 90 tests pytest
│
├── aosis-deck-builder.zip             # bundle zippé, uploadable dans Claude.ai
│
├── docs/                              # documentation
│   ├── README.md                      # index des docs
│   ├── GUIDE_INSTALLATION.md
│   ├── GUIDE_OPERATIONNEL.md
│   └── chantiers/                     # 17 rapports de décision
│
└── examples/                          # specs JSON + PDF de référence
```

## Tests

```bash
pip install -e "aosis-deck-builder/[test]"
cd aosis-deck-builder && pytest
```

**90 tests** (1 skipped si LibreOffice/pdftoppm absent — visual review optionnel) : generation golden-deck + tous layouts, 8 types de charts matplotlib, canvas_blank freeform, KPI sizing dynamique, uniformité de police REPEAT_ITEM, data_table, cache disque Pexels, deprecation des 10 layouts retirés au Chantier 23.

## Regénérer le bundle skill

Après toute modif source (`scripts/`, `references/`, `SKILL.md`, `assets/`), regénérer le bundle uploadable dans Claude :

```bash
./build_bundle.sh
```

Produit `aosis-deck-builder.zip` (~700 KB) avec dossier racine `aosis-deck-builder/`, prêt à uploader sur Claude.ai. Exclut caches, lock files, Zone.Identifier.

## Brand customisation

Source unique de charte : `aosis-deck-builder/assets/AOSIS_template.pptx` → `ppt/theme/theme1.xml`. **Pour changer une couleur ou police, éditer le theme XML — le code Python suit automatiquement** (aucun hex hardcodé).

`matplotlib` est lazy-imported : un deck sans chart se génère sur un venv qui n'a que `python-pptx`.

## License

Propriétaire — usage interne AOSIS.
