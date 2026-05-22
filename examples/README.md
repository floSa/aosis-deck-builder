# Examples

Specs JSON de démonstration et de validation visuelle du skill.

## 📘 Specs génériques de référence

| Fichier | Slides | Utilisé par | Sert à |
|---|---:|---|---|
| [`example_minimal.json`](example_minimal.json) | 3 + closing | `test_skill.sh` (smoke) | Smoke test ultra-rapide : `hero_stat` + `roadmap_styled` + `text` |
| [`example_full.json`](example_full.json) | 12 + closing | `test_skill.sh` (smoke) | Vitrine du catalogue : mix code-based (`hero_stat`, `big_idea`, `funnel`, `text`) + template-based (`matrix_2x2_styled`, `kpi_with_chart`, `roadmap_styled`, `process_steps`, `quote_callout`, `framework_3cards`, `comparison_2cols`) |

## 🛠️ Specs de validation visuelle

Utilisés manuellement après une modif structurelle pour vérifier visuellement le rendu. **Pas branchés à pytest** — c'est de la régression visuelle à l'œil.

| Fichier | Slides | Sert à |
|---|---:|---|
| [`test_canvas_blank_showcase.json`](test_canvas_blank_showcase.json) | 8 | Démontre toutes les compositions de `canvas_blank` (1 / 2 / 3 / 4 / 5 / 6 blocs, asymétriques, 6 types de blocs : `kpi_card`, `bullets`, `text`, `image`, `chart`, `quote`) |
| [`test_data_table_showcase.json`](test_data_table_showcase.json) | 4 | Démontre `data_table` (highlight col + row, 5 / 6 colonnes, centrage, auto-shrink police) |
| [`test_migration_cloud.json`](test_migration_cloud.json) | 20 | Gros deck client "Migration Cloud TechnoLog" couvrant la quasi-totalité des layouts template-based. Référence pour les régressions visuelles type C19/C20/C21 (slide 6 `kpi_with_chart` "TCO trajectoire") |

## 🏃 Lancer la génération

Depuis la racine du projet :

```bash
python aosis-deck-builder/scripts/build_deck.py \
    examples/example_full.json \
    /tmp/example_full.pptx \
    --template aosis-deck-builder/assets/AOSIS_template.pptx
```

Ou via le smoke test global qui génère `example_minimal` + `example_full` :

```bash
./test_skill.sh
```

## 📄 Source documentaire de test

Le PDF source ayant servi à générer le deck Cloud Computing 2026 est dans [`docs/test_inputs/cloud_computing_rapport.pdf`](../docs/test_inputs/cloud_computing_rapport.pdf) — matière brute, non spec JSON.

## 📚 Référence

- Schéma JSON exhaustif : [`aosis-deck-builder/references/json-schema.md`](../aosis-deck-builder/references/json-schema.md)
- Catalogue des layouts (17 template-based + 11 code-based, post-Chantier 23) : [`aosis-deck-builder/references/layouts.md`](../aosis-deck-builder/references/layouts.md)
