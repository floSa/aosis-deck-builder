# Documentation

Documentation utilisateur et historique du projet `aosis-deck-builder`.

## Guides

| Document | Public | Description |
|---|---|---|
| [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md) | Utilisateur / Devops | Installation pas-à-pas (venv, dépendances, clé Pexels, premier build). |
| [GUIDE_OPERATIONNEL.md](GUIDE_OPERATIONNEL.md) | Utilisateur / Consultant | Mode d'emploi du skill au quotidien : choisir les bons layouts, écrire des specs JSON solides, debugger, regénérer. |

## Historique des chantiers

Chaque chantier (= mini-mission de modification) a son rapport de décision détaillé dans [`chantiers/`](chantiers/). Le `CHANGELOG.md` à la racine donne la vue synthétique ; les rapports détaillés expliquent le **pourquoi** des choix techniques et les arbitrages.

| Chantier | Sujet | Rapport |
|---:|---|---|
| 1 | Roadmap geometry bounds fix | [chantier1_report.md](chantiers/chantier1_report.md) |
| 2 | (cf rapport) | [chantier2_report.md](chantiers/chantier2_report.md) |
| 3 | Dynamic palette loading depuis theme XML | [chantier3_report.md](chantiers/chantier3_report.md) |
| 4 | (cf rapport) | [chantier4_report.md](chantiers/chantier4_report.md) |
| 5 | (cf rapport) | [chantier5_report.md](chantiers/chantier5_report.md) |
| 6 | Visual review pipeline | [chantier6_report.md](chantiers/chantier6_report.md) |
| 7 | Template-based layouts via exhibits.pptx | [chantier7_report.md](chantiers/chantier7_report.md) |
| 8 | Wiring matplotlib charts pour kpi_with_chart (8 types) | [chantier8_report.md](chantiers/chantier8_report.md) |
| Consolidation | Fusion `exhibits.pptx` dans `AOSIS_template.pptx` | [chantier_consolidation_report.md](chantiers/chantier_consolidation_report.md) |
| Exhibits | Construction des slides modèles exhibits | [chantier_exhibits_report.md](chantiers/chantier_exhibits_report.md) |
| Naming | Nommage de toutes les slides via cSld.name | [chantier_naming_report.md](chantiers/chantier_naming_report.md) |
| Ménage | Repackaging du dossier de travail (`examples/`, `_archive/`) | [chantier_menage_report.md](chantiers/chantier_menage_report.md) |
| Alternances | Fix alternances visuelles 3 layouts (framework, roadmap, process) | [chantier_alternances_report.md](chantiers/chantier_alternances_report.md) |
| 9 | Polish : sommaire, roadmap, kpi_with_chart, icônes Iconify | [chantier9_report.md](chantiers/chantier9_report.md) |
| 10 | 9 fixes post-test réel "Migration Cloud TechnoLog" | [chantier10_report.md](chantiers/chantier10_report.md) |
| 11 | Polish post-deck réel : roadmap, matrix, sommaire, images | [chantier11_report.md](chantiers/chantier11_report.md) |
| 12 | Images : migration Unsplash → Pexels + découpe diagonale | [chantier12_report.md](chantiers/chantier12_report.md) |
| 13 | Fiches détaillées de tous les layouts dans references/ | [chantier13_report.md](chantiers/chantier13_report.md) |
| 14 | Layout `canvas_blank` freeform intelligent (6 types de blocs) | [chantier14_report.md](chantiers/chantier14_report.md) |
| 15 | Nouveau layout `data_table` (template-based) | [chantiers/chantier15_report.md](chantiers/chantier15_report.md) |
| 16 | Fix `closing_diagonal` long titre + uniformité REPEAT_ITEM | [chantier16_report.md](chantiers/chantier16_report.md) |
| 17 | Uniformité de police sur `matrix_2x2_styled` (quadrants) | [chantier17_report.md](chantiers/chantier17_report.md) |
| 18 | Rendu premium : drop shadows, KPI XXL, encadrement charts | [chantier18_report.md](chantiers/chantier18_report.md) |
| 19 | Anti-chevauchement KPI XXL (auto-shrink height-aware) | [chantier19_report.md](chantiers/chantier19_report.md) |
| 20 | Positionnement vertical dynamique dans `kpi_card` | [chantier20_report.md](chantiers/chantier20_report.md) |
| 21 | Refonte `kpi_with_chart` : horizontal → vertical | [chantier21_report.md](chantiers/chantier21_report.md) |
| 22 | Cache disque pour les images Pexels | [chantier22_report.md](chantiers/chantier22_report.md) |
| 23 | Nettoyage : retrait de 10 layouts code-based dépréciés | [chantier23_report.md](chantiers/chantier23_report.md) |
| 24 | Nettoyage et réorganisation du repo | [chantier24_report.md](chantiers/chantier24_report.md) |

## Archive

- [`_archive_C24/`](_archive_C24/) — 2 documents internes datés 2026-05-13 (audit + documentation skill) récupérés au Chantier 24
- [`test_inputs/`](test_inputs/) — PDF source ayant servi à générer le deck Cloud Computing 2026
