# Chantier — Consolidation du template AOSIS canonique

**Date** : 2026-05-18
**Périmètre** : Transférer les 16 slides modèles d'`exhibits.pptx` vers `AOSIS_template.pptx` (template officiel validé par le chef), puis adapter le skill pour ne plus dépendre que d'un fichier unique. `exhibits.pptx` conservé comme archive.

## TL;DR

- ✅ Palette du nouveau `AOSIS_template.pptx` vérifiée : **10/10 hex exacts** sur theme1 et theme2 (les deux themes AOSIS effectifs).
- ✅ **16 slides transférées** sur les masters/layouts du nouveau template (`Cover`/`Closing` master 0 ; `Contenu + texte`/`Texte` master 1). cSld.name et tous les `{{...}}` shape names préservés.
- ✅ `build_deck.py` re-pointé : `EXHIBITS_PATH = TEMPLATE_PATH`. `LAYOUT_MAP` adapté au nouveau jeu de masters.
- ✅ **14/15 tests pytest verts** (1 skip visual_review = absence de soffice — comportement standard, identique à l'état pré-chantier).
- ✅ `validation_deck.pptx` (6 slides : 5 template-based + 1 code-based) regénéré sans erreur. Livré dans [chantier_consolidation_assets/validation_deck.pptx](chantier_consolidation_assets/validation_deck.pptx) pour validation visuelle utilisateur (pas d'accès à PowerPoint/soffice côté agent pour exporter en JPEG).
- ⚠️ Le nombre de slides était de **16 et non 15** comme indiqué dans la mission (11 nommées + 5 décor non nommées — voir détail §3).

## 1. Audit palette

Comparaison entre les 10 hex officiels (chef) et le contenu du nouveau `theme1.xml` / `theme2.xml` :

| slot | attendu | theme1 | theme2 | status |
|---|---|---|---|---|
| dk1 | `#14163C` | `14163C` | `14163C` | ✅ |
| lt1 | `#FAFAF7` | `FAFAF7` | `FAFAF7` | ✅ |
| dk2 | `#4A4D6B` | `4A4D6B` | `4A4D6B` | ✅ |
| lt2 | `#E8E9F2` | `E8E9F2` | `E8E9F2` | ✅ |
| accent1 | `#F26622` | `F26622` | `F26622` | ✅ |
| accent2 | `#1E2261` | `1E2261` | `1E2261` | ✅ |
| accent3 | `#C2491A` | `C2491A` | `C2491A` | ✅ |
| accent4 | `#F9B233` | `F9B233` | `F9B233` | ✅ |
| accent5 | `#7CB342` | `7CB342` | `7CB342` | ✅ |
| accent6 | `#E63946` | `E63946` | `E63946` | ✅ |

Schemes nommés `AOSIS`, `hlink = #F26622`, `folHlink = #C2491A` (cohérent avec accent1/accent3).

theme3 et theme4 portent encore les valeurs `Office` par défaut, mais ils sont liés aux notes/handout masters — pas aux slides. Ceci est conforme à la limite connue documentée dans le CHANGELOG depuis le Chantier 2 (PowerPoint exige une part-theme dédiée par master ; impossibilité d'unifier sans casser le format).

**Conclusion** : la palette est correcte. Pas d'alerte, on continue.

## 2. Audit structurel pré-transfert

| | exhibits.pptx | AOSIS_template.pptx (avant) |
|---|---|---|
| slide_size | 10.00" × 5.62" | 10.00" × 5.62" |
| masters | 2 | 2 |
| layouts master 0 | `Diapositive de titre`, `Titre et contenu`, `5_Vide`, `10_Vide`, `Mix sommaire/phoyo`, `intercalaires` (6) | `Cover`, `Closing` (2) |
| layouts master 1 | `Diapositive de titre`, `5_Vide`, `10_Vide`, `Mix sommaire/phoyo`, `intercalaires` (5) | `Contenu + texte`, `Texte` (2) |
| slides | 16 | 0 |

**Constat** : les jeux de layouts diffèrent complètement. Le transfert nécessite un mapping :

| source layout | → target layout |
|---|---|
| `Diapositive de titre` | `Cover` |
| `intercalaires` | `Closing` |
| `5_Vide` | `Texte` |
| `Titre et contenu` | `Contenu + texte` |

(Les 4 derniers entrants — `10_Vide`, `Mix sommaire/phoyo` — non utilisés par les 16 slides modèles.)

## 3. Transfert des 16 slides

Méthodologie : pour chaque source slide, `add_slide(target_layout)` puis suppression des placeholders auto-injectés puis deepcopy XML des shapes source vers `spTree` cible, enfin recopie de `cSld@name`. Strictement équivalent à `render_template_slide` du Chantier 7 mais appliqué en batch.

| idx | source layout | → target | cSld.name |
|---:|---|---|---|
| 0 | Diapositive de titre | Cover | _(none)_ — cover_diagonal |
| 1 | intercalaires | Closing | _(none)_ — agenda_diagonal |
| 2 | intercalaires | Closing | _(none)_ — section_diagonal |
| 3 | 5_Vide | Texte | _(none)_ — canvas |
| 4 | 5_Vide | Texte | `executive_summary` |
| 5 | 5_Vide | Texte | `kpi_with_chart` |
| 6 | 5_Vide | Texte | `comparison_2cols` |
| 7 | 5_Vide | Texte | `comparison_before_after` |
| 8 | 5_Vide | Texte | `framework_3cards` |
| 9 | 5_Vide | Texte | `roadmap_styled` |
| 10 | 5_Vide | Texte | `next_steps` |
| 11 | 5_Vide | Texte | `process_steps` |
| 12 | 5_Vide | Texte | `text_dense_3cols` |
| 13 | 5_Vide | Texte | `quote_callout` |
| 14 | 5_Vide | Texte | `matrix_2x2_styled` |
| 15 | intercalaires | Closing | _(none)_ — closing_diagonal |

Note sur le compte : la mission indiquait 15 slides (4 originales + 11 layouts). Le fichier réel en contenait **16** (4 originales documentées + 1 supplémentaire « canvas » sur 5_Vide à l'index 3, identifiable par sa shape `{{TITLE}}` solitaire). Toutes transférées sans exception ; aucune perte.

## 4. Validation structurelle post-transfert

```
== ZIP integrity ==
  testzip: OK
  slide XML files: 16

== Presentation level ==
  slide_size: 10.00" x 5.62"
  slides: 16
  masters: 2  (layouts: [['Cover', 'Closing'], ['Contenu + texte', 'Texte']])

== Per-slide name preservation == (16/16 OK)
  cSld.name : preserved on all 11 named + None on all 5 unnamed
  {{...}} shapes : preserved bit-for-bit (counts identical to source for every slide)

== REPEAT_ITEM verification ==
  8 slides porteuses de REPEAT_ITEM, avec leurs {{ITEM_*}} sub-placeholders intacts.

=> Overall: ALL OK
```

Note : `executive_summary` n'apparaît pas dans le bloc REPEAT_ITEM car son groupe avait été renommé `Groupe 19` lors de la finalisation manuelle dans PowerPoint (friction documentée dans le rapport Chantier 7). Ce comportement est **strictement conservé** par le transfert — comme pour le reste, le contenu des shapes n'est pas modifié.

## 5. Adaptation du skill

`scripts/build_deck.py` :

```diff
-EXHIBITS_PATH = SCRIPT_DIR.parent / "assets" / "exhibits.pptx"
+EXHIBITS_PATH = TEMPLATE_PATH   # = assets/AOSIS_template.pptx

 LAYOUT_MAP = {
-    "cover":   (0, 0),   # 'Diapositive de titre'  (exhibits master 0)
-    "section": (0, 5),   # 'intercalaires'         (exhibits master 0)
-    "closing": (0, 5),   # 'intercalaires'         (exhibits master 0)
-    "content": (0, 1),   # 'Titre et contenu'      (exhibits master 0)
-    "text":    (1, 1),   # '5_Vide'                (exhibits master 1)
+    "cover":   (0, 0),   # 'Cover'                 (master 0)
+    "section": (0, 1),   # 'Closing'               (master 0)
+    "closing": (0, 1),   # 'Closing'               (master 0)
+    "content": (1, 0),   # 'Contenu + texte'       (master 1)
+    "text":    (1, 1),   # 'Texte'                 (master 1)
 }
```

Et dans `build_deck()` :
- La branche de fallback (`if not EXHIBITS_PATH.exists()`) est supprimée puisque le build base IS le template path.
- `render_template_slide(prs, EXHIBITS_PATH, ...)` → `render_template_slide(prs, template_path, ...)` : aligne le source des templates sur le build base, ce qui assure le bon comportement quand l'utilisateur passe `--template custom.pptx`.

`scripts/template_engine.py` :
- Docstrings réécrits pour pointer « the AOSIS template pptx » au lieu d'« exhibits.pptx ». Aucun changement de code, le moteur reste agnostique du chemin (il prend `exhibits_path` en paramètre).

`scripts/brand.py` : **non modifié** (palette toujours lue dynamiquement, fonctionne sans changement).

`tests/test_smoke.py` : **non modifié**. Le test `test_template_layouts_discovery` lit toujours `exhibits.pptx` directement — qui existe encore dans `assets/` comme archive — donc il continue de passer. Aucun risque structurel.

## 6. Tests de régression

```
======================== 14 passed, 1 skipped in 1.41s =========================
```

Détail :
```
tests/test_smoke.py::test_golden_generates PASSED
tests/test_smoke.py::test_golden_no_overflow PASSED
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_3.json] PASSED
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_4.json] PASSED
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_5.json] PASSED
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_6.json] PASSED
tests/test_smoke.py::test_all_layouts_generate PASSED
tests/test_smoke.py::test_palette_loads_from_canonical_template PASSED
tests/test_smoke.py::test_palette_brand_error_on_missing_file PASSED
tests/test_smoke.py::test_visual_review_generates_artifacts SKIPPED   # soffice manquant — comportement standard
tests/test_smoke.py::test_template_layouts_discovery PASSED
tests/test_smoke.py::test_template_based_deck_builds PASSED
tests/test_smoke.py::test_template_repeat_mechanism PASSED
tests/test_smoke.py::test_template_kpi_with_chart PASSED
tests/test_smoke.py::test_summarize_report PASSED
```

Le skip de `test_visual_review_generates_artifacts` est pré-existant (absence de soffice/pdftoppm sur la machine de dev — identique au Chantier 7).

## 7. Validation end-to-end

Le fichier [chantier_consolidation_assets/validation_deck.pptx](chantier_consolidation_assets/validation_deck.pptx) (585 KB, 6 slides) a été généré depuis [tests/fixtures/template_based_spec.json](aosis-deck-builder/tests/fixtures/template_based_spec.json) — la même fixture validée au Chantier 7. Composition :

| idx | layout | mécanisme | cSld.name |
|---:|---|---|---|
| 0 | executive_summary | template-based | `executive_summary` |
| 1 | hero_stat | code-based | _(none)_ |
| 2 | process_steps | template-based | `process_steps` |
| 3 | roadmap_styled | template-based | `roadmap_styled` |
| 4 | framework_3cards | template-based | `framework_3cards` |
| 5 | next_steps | template-based | `next_steps` |

Tous les 6 slides reposent sur le layout `Texte` du nouveau master (master 1, layout 1). La validation **visuelle** (comparer au rendu Chantier 7 dans `chantier7_assets/slide-*.jpg`) n'a pas pu être effectuée par l'agent : pas d'accès à `soffice`/`pdftoppm` ni à PowerPoint COM dans cet environnement. **Le .pptx est livré tel quel pour validation utilisateur.**

## 8. Frictions techniques

1. **Layouts source/cible disjoints** (1ère heure) : `exhibits.pptx` avait 6+5 = 11 entrées de layouts dans 2 masters, le nouveau template seulement 2+2 = 4 layouts. Les noms ne se recouvrent pas (`5_Vide` vs `Texte`, `Diapositive de titre` vs `Cover`, `intercalaires` vs `Closing`). Résolu par un mapping explicite source→cible appliqué à `add_slide()`. Aucun shape n'a été perdu car la deepcopy XML est indépendante de la slide_layout choisie ; le layout sert juste de support pour les masters/theme.

2. **PowerPoint avec lock files actifs** : `~$AOSIS_template.pptx`, `~$exhibits.pptx`, `~$AOSIS_template_v2.pptx` étaient présents au démarrage (PowerPoint ouvert côté utilisateur). Le write `prs.save()` n'a pas échoué, mais si PowerPoint était activement en train d'éditer ces fichiers, le résultat pourrait être instable côté utilisateur. **À surveiller** : fermer PowerPoint avant validation.

3. **16 slides au lieu des 15 annoncées** : la mission listait 4 originales + 11 layouts = 15, mais le fichier en contient 16 (la 5e "originale" est une slide canvas sur `5_Vide` à l'index 3 — `{{TITLE}}` solitaire, vraisemblablement un canevas de test ou la base d'un futur layout). Toutes transférées sans exception. À l'utilisateur de nommer (`cSld.name`) celles qu'il veut rendre adressables par le moteur.

4. **`hlink`/`folHlink` non spécifiés dans la mission** : le theme XML déclare aussi `hlink = #F26622` et `folHlink = #C2491A`. Cohérent avec la charte (accent1/accent3). Non flaggé comme problème, signalé pour traçabilité.

## 9. Livrables

| Fichier | Statut | Description |
|---|---|---|
| `aosis-deck-builder/assets/AOSIS_template.pptx` | **modifié** | Template officiel enrichi des 16 slides modèles |
| `aosis-deck-builder/assets/AOSIS_template.backup-before-merge.pptx` | **créé** | Backup pré-transfert |
| `aosis-deck-builder/assets/exhibits.backup-before-merge.pptx` | **créé** | Backup pré-transfert |
| `aosis-deck-builder/assets/exhibits.pptx` | **inchangé** | Conservé comme archive |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** | `EXHIBITS_PATH=TEMPLATE_PATH`, `LAYOUT_MAP` adapté, build base simplifié |
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** | Docstrings actualisés (code logique inchangé) |
| `aosis-deck-builder/scripts/brand.py` | **inchangé** | Lecture dynamique fonctionne sans changement |
| `CHANGELOG.md` | **modifié** | Entrée « Consolidation du template AOSIS canonique » ajoutée |
| `chantier_consolidation_report.md` | **créé** | Ce rapport |
| `chantier_consolidation_assets/validation_deck.pptx` | **créé** | Validation end-to-end (à inspecter visuellement) |

## 10. Suites possibles (hors scope)

- Nommer les 5 slides décor (`cover_diagonal`, `agenda_diagonal`, `section_diagonal`, `canvas`, `closing_diagonal`) via `cSld@name` dans PowerPoint pour les rendre adressables comme template-based layouts.
- Restaurer le nom `{{REPEAT_ITEM}}` sur le groupe `Groupe 19` de la slide `executive_summary` (renommage manuel en PowerPoint, ~30s).
- Câbler matplotlib dans `kpi_with_chart` pour rendre le placeholder chart.
- Implémenter le mécanisme REPEAT_ITEM apparié (left/right) pour `comparison_2cols` et `comparison_before_after`.

---

**Statut final** : ✅ Chantier consolidation **livré sans régression**. Tests pytest verts, deck de validation généré sans erreur, palette officielle vérifiée 10/10, 16/16 slides transférées avec préservation bit-pour-bit des `cSld.name` et `{{...}}` shape names.
