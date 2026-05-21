# AOSIS Deck Builder

Claude Skill qui génère des présentations PowerPoint à la charte AOSIS (`.pptx`) — style consulting top-tier (hero stats, KPI XXL avec drop shadows, matrices 2×2, roadmaps, charts matplotlib, data tables, layout libre `canvas_blank`) — depuis une **spec JSON** unique.

Le skill part toujours du template officiel `AOSIS_template.pptx`, donc la charte graphique (navy/orange, logo, Arial, footers) est héritée par construction. **17 layouts template-based** + **canvas_blank** freeform à 6 blocs (kpi_card, bullets, text, image, chart, quote).

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

Une spec `spec.json` minimale est dans [`aosis-deck-builder/SKILL.md`](aosis-deck-builder/SKILL.md). Schéma JSON complet et catalogue des layouts dans [`aosis-deck-builder/references/`](aosis-deck-builder/references/).

CLI flags : `--debug-layouts` (badges debug par slide), `--no-images` (désactive Pexels), `--template <path>` (template alternatif).

## Configuration (`.env`)

Le skill charge automatiquement un `.env` à la racine du projet (auto-discovery depuis `scripts/build_deck.py`). Voir [`.env.example`](.env.example).

```dotenv
PEXELS_API_KEY=your-pexels-key-here
```

- **`PEXELS_API_KEY`** (optionnel) : photos stock pertinentes via [pexels.com/api](https://www.pexels.com/api/) (gratuit, 200 req/h, 20 000/mois, automation autorisée par ToS). Sans clé → fallback Lorem Picsum (photos aléatoires seedées par mot-clé).

## Structure du projet

```
.
├── aosis-deck-builder/              # le skill Claude (source)
│   ├── SKILL.md                     # entry point Claude (≤200 l)
│   ├── references/
│   │   ├── layouts.md               # 33 fiches détaillées (17 template + 14 code)
│   │   ├── json-schema.md           # schéma JSON exhaustif
│   │   ├── qa.md                    # workflow QA visuel + contenu
│   │   └── icons_suggested.md       # icônes Iconify recommandées
│   ├── scripts/
│   │   ├── build_deck.py            # orchestrateur (CLI + dispatch layouts)
│   │   ├── template_engine.py       # rendu template-based + canvas_blank + data_table
│   │   ├── chart_engine.py          # 8 types de charts matplotlib
│   │   ├── image_engine.py          # Pexels API + fallback Picsum
│   │   ├── icon_engine.py           # Iconify API (mdi:*, etc.)
│   │   ├── brand.py                 # palette extraite du theme XML
│   │   └── visual_review.py         # capture screenshots + détection défauts
│   ├── assets/
│   │   └── AOSIS_template.pptx      # template canonique, source unique de charte
│   ├── tests/test_smoke.py          # 76 tests pytest
│   └── pyproject.toml
├── aosis-deck-builder.skill         # bundle zippé, uploadable dans Claude
├── build_bundle.sh                  # regénère le bundle depuis aosis-deck-builder/
├── examples/                        # specs JSON + PDF de référence
├── chantier*_report.md              # decision records par chantier (1-20)
├── CHANGELOG.md
└── .env.example
```

## Tests

```bash
pip install -e "aosis-deck-builder/[test]"
cd aosis-deck-builder && pytest
```

76 tests (1 skipped si LibreOffice/pdftoppm absent — visual review optionnel) :
- generation golden-deck + tous layouts (17 template + canvas_blank + data_table)
- charts matplotlib (8 types : bar/barh/bar_stacked/line/donut/pie/combo/waterfall)
- canvas_blank freeform (1-6 blocs, asymétrique image/chart, anti-overflow footer)
- KPI sizing dynamique (anti-overlap value/label, XXL preserved when room)
- uniformité de police REPEAT_ITEM (chantier 16) + quadrants matrix
- data_table (auto-shrink police, highlight col/row)
- non-régression de geometry pour roadmaps, drop shadows, palette dynamique

## Regénérer le bundle skill

Après toute modif source (`scripts/`, `references/`, `SKILL.md`, `assets/`), regénérer le bundle uploadable :

```bash
./build_bundle.sh
```

Produit `aosis-deck-builder.skill` (~670 KB), exclut tests/, caches, backups.

## Brand customisation

Source unique de charte : `aosis-deck-builder/assets/AOSIS_template.pptx` → `ppt/theme/theme1.xml`. **Pour changer une couleur ou police, éditer le theme XML — le code Python suit automatiquement** (aucun hex hardcodé). Détails dans les rapports `chantier3_report.md` / `chantier_alternances_report.md`.

`matplotlib` est lazy-imported : un deck sans chart se génère sur un venv qui n'a que `python-pptx`.

## License

Propriétaire — usage interne AOSIS.
