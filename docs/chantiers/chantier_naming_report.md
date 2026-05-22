# Chantier — Nommage des slides dans AOSIS_template.pptx

**Date** : 2026-05-19
**Périmètre** : Appliquer un `cSld@name` à chaque slide de `assets/AOSIS_template.pptx` (17 slides au total) selon la table fournie. Renommer `cover_diagonal` → `cover` côté code si applicable.

## TL;DR

- ✅ **17/17 slides nommées** selon la table fournie (6 nouveaux noms + 11 existants confirmés).
- ✅ `discover_template_layouts()` retourne désormais **17 layouts** (vs 11 auparavant).
- ⚠️ Aucune référence à `cover_diagonal` n'existait dans le code (uniquement dans 2 rapports historiques laissés intacts).
- ❌ **1 test pytest échoue** : `test_template_kpi_with_chart`. Cause = édition manuelle utilisateur antérieure (suppression de la shape `chart_bg`). Diagnostic complet en §5. **Non corrigé** car la fix sort du périmètre strict (« Ne modifie pas le contenu des slides »).

## 1. État initial (avant nommage)

```
Slides: 17
Named: 11/17
```

| pos | layout | cSld.name (avant) |
|---:|---|---|
| 1 | Cover | _(none)_ |
| 2 | Sommaire_Section_Contact | _(none)_ |
| 3 | Sommaire_Section_Contact | _(none)_ |
| 4 | Texte | _(none)_ |
| 5 | Texte | `executive_summary` |
| 6 | Texte | `kpi_with_chart` |
| 7 | Texte | `comparison_2cols` |
| 8 | Texte | `comparison_before_after` |
| 9 | Texte | `framework_3cards` |
| 10 | Texte | `roadmap_styled` |
| 11 | Texte | `next_steps` |
| 12 | Texte | `process_steps` |
| 13 | Texte | `text_dense_3cols` |
| 14 | Texte | `quote_callout` |
| 15 | Texte | `matrix_2x2_styled` |
| 16 | Sommaire_Section_Contact | _(none)_ |
| 17 | Closing | _(none)_ |

Note : le fichier contient 17 slides et non 16 comme observé en fin de chantier consolidation. Le 17ᵉ slide ainsi que le renommage du layout `Closing` en `Sommaire_Section_Contact` (3 slides) proviennent vraisemblablement d'édits utilisateur en PowerPoint entre les deux chantiers — voir §5 pour conséquences.

## 2. État final (après nommage)

```
Slides: 17
Named: 17/17  ✅
```

| pos | cSld.name (avant) | cSld.name (après) |
|---:|---|---|
| 1 | _(none)_ | **`cover`** |
| 2 | _(none)_ | **`agenda_diagonal`** |
| 3 | _(none)_ | **`section_diagonal`** |
| 4 | _(none)_ | **`canvas_blank`** |
| 5 | `executive_summary` | `executive_summary` |
| 6 | `kpi_with_chart` | `kpi_with_chart` |
| 7 | `comparison_2cols` | `comparison_2cols` |
| 8 | `comparison_before_after` | `comparison_before_after` |
| 9 | `framework_3cards` | `framework_3cards` |
| 10 | `roadmap_styled` | `roadmap_styled` |
| 11 | `next_steps` | `next_steps` |
| 12 | `process_steps` | `process_steps` |
| 13 | `text_dense_3cols` | `text_dense_3cols` |
| 14 | `quote_callout` | `quote_callout` |
| 15 | `matrix_2x2_styled` | `matrix_2x2_styled` |
| 16 | _(none)_ | **`closing_diagonal`** |
| 17 | _(none)_ | **`final_branding`** |

6 nouveaux noms appliqués, 11 noms préexistants confirmés. Aucune valeur préexistante n'a été écrasée (la mission anticipait un renommage `cover_diagonal` → `cover` mais le `cSld.name` de la slide 1 était en fait `None`).

## 3. Mise à jour des références au code

Recherche `cover_diagonal` dans le périmètre demandé (`scripts/`, `tests/`, `tests/fixtures/`, `references/`, `SKILL.md`, `CHANGELOG.md`, `README.md`) :

```
$ grep -rn "cover_diagonal" aosis-deck-builder/ CHANGELOG.md README.md
(aucun résultat)
```

Présent uniquement dans 2 rapports historiques (à ne PAS toucher selon le périmètre) :
- `chantier_consolidation_report.md` (l.65, l.210) — référence narrative à l'ancien nommage de fait
- `chantier_exhibits_report.md` (l.11, l.226) — référence narrative à l'ancien nommage de fait

**Aucune modification de code n'a donc été nécessaire.**

## 4. Vérification

### a. `cSld.name` sur les 17 slides
```python
prs = Presentation("aosis-deck-builder/assets/AOSIS_template.pptx")
# Slides: 17
# All have cSld.name: YES
```

### b. `discover_template_layouts` retourne 17 layouts
```
discover_template_layouts → 17 layouts:
  [ 0] cover
  [ 1] agenda_diagonal
  [ 2] section_diagonal
  [ 3] canvas_blank
  [ 4] executive_summary
  [ 5] kpi_with_chart
  [ 6] comparison_2cols
  [ 7] comparison_before_after
  [ 8] framework_3cards
  [ 9] roadmap_styled
  [10] next_steps
  [11] process_steps
  [12] text_dense_3cols
  [13] quote_callout
  [14] matrix_2x2_styled
  [15] closing_diagonal
  [16] final_branding
```
✅ Confirme 17 layouts (vs 11 auparavant). Les 6 décor (`cover`, `agenda_diagonal`, `section_diagonal`, `canvas_blank`, `closing_diagonal`, `final_branding`) sont maintenant adressables comme template-based layouts à part entière.

### c. Résultats pytest

```
======================== 13 passed, 1 failed, 1 skipped in 1.32s ========================

FAILED tests/test_smoke.py::test_template_kpi_with_chart - AssertionError: Chart placeholder shape missing
SKIPPED tests/test_smoke.py::test_visual_review_generates_artifacts (soffice/pdftoppm absents — pré-existant)
```

13/14 verts. Détail du failure en §5.

## 5. Friction technique — Test `test_template_kpi_with_chart`

### Diagnostic

Le test (l.260-296 de `tests/test_smoke.py`) :
1. Construit un deck avec la spec `kpi_with_chart` (3 KPIs, sans clé `chart_placeholder`).
2. Récupère la slide générée.
3. Cherche une shape dont le `name` contient `{{CHART_PLACEHOLDER}}` **OU** `chart_bg`.
4. Assert la présence.

Source actuelle (slide 6 du template, `kpi_with_chart`) :
```
  name='{{SOURCE}}'
  name='{{REPEAT_ITEM}}'
  name='{{CHART_PLACEHOLDER}}'
  name='{{TITLE}}'
```

Source historique (snapshot `exhibits.pptx` archive) :
```
  name='{{TITLE}}', '{{EYEBROW}}', '{{SOURCE}}', '{{REPEAT_ITEM}}', 'chart_bg', '{{CHART_PLACEHOLDER}}'
```

**Constat** : la shape `chart_bg` (rectangle de fond du chart, nom NON conforme au pattern placeholder donc préservée à l'output) a été supprimée par édit manuel utilisateur en PowerPoint entre le chantier consolidation et le chantier nommage. Il ne reste que `{{CHART_PLACEHOLDER}}`, qui MATCH le pattern `^\{\{[A-Z]...\}\}$` et est donc **supprimé par `_process_simple_placeholders`** lorsque la spec ne fournit pas la clé correspondante.

Conséquence : au build, ni `chart_bg` ni `{{CHART_PLACEHOLDER}}` ne survivent dans la slide générée → l'assert échoue.

### Pourquoi je n'ai pas corrigé

La mission stipule :
> Ne touche à rien d'autre que les cSld.name et les références au nom cover_diagonal dans le code. **Ne modifie pas le contenu des slides**, ni la palette, ni les masters/layouts.

Trois fixes possibles, tous hors périmètre :
1. **Restaurer `chart_bg` dans la slide source** — modifie le contenu de slide.
2. **Renommer `{{CHART_PLACEHOLDER}}` en `chart_placeholder` (sans accolades)** — modifie le contenu de slide.
3. **Exempter `chart_placeholder` dans `_process_simple_placeholders`** (comme `image` l'est) — modifie le code engine.
4. **Mettre à jour le test pour ne plus s'attendre au shape** — modifie le test.

Toutes sortent du périmètre strict. La fix la plus naturelle est l'option 3 (~3 lignes dans `template_engine.py`), à proposer dans une mini-mission séparée.

### Vérification que le failure n'est PAS lié à mon changement

Le test cherche `cSld.get('name') == 'kpi_with_chart'`. Cette slide était DÉJÀ nommée `kpi_with_chart` avant mon intervention. Mon edit n'a écrasé aucune valeur préexistante (cf. §2). Le failure est causé exclusivement par la suppression de `chart_bg` opérée en amont par l'utilisateur dans PowerPoint, et serait survenu indépendamment du renommage des cSld.

## 6. Frictions secondaires

- **Lock files PowerPoint** : `~$AOSIS_template.pptx` toujours présent au démarrage. Le `prs.save()` a réussi mais si PowerPoint était actif sur le fichier, l'utilisateur peut voir un conflit à la prochaine ouverture.
- **17 slides au lieu de 16** : le fichier a évolué entre les deux chantiers. Une slide (`final_branding`) a été ajoutée en position 17 ; les 3 slides anciennement « Closing » ont été migrées vers le layout `Sommaire_Section_Contact`. Aucune incidence sur le nommage, mais constat important pour cohérence des rapports.

## 7. Livrables

| Fichier | Statut | Description |
|---|---|---|
| `aosis-deck-builder/assets/AOSIS_template.pptx` | **modifié** | 17 slides désormais nommées |
| `aosis-deck-builder/assets/AOSIS_template.before-naming.pptx` | **créé** | Backup pré-nommage |
| `chantier_naming_report.md` | **créé** | Ce rapport |

Aucun changement de code (pas de référence `cover_diagonal` trouvée dans le périmètre code).

## 8. Suites recommandées

- **Mini-fix `chart_bg`** : choisir l'option 3 ou 4 (cf. §5) pour rétablir `test_template_kpi_with_chart`. ~3 lignes de modification.
- **Re-vérifier la palette** après les édits PowerPoint utilisateur (le passage `Closing` → `Sommaire_Section_Contact` au niveau layout name peut indiquer une réorganisation plus large).
- **Documenter les 6 nouveaux layouts** (`cover`, `agenda_diagonal`, `section_diagonal`, `canvas_blank`, `closing_diagonal`, `final_branding`) dans `references/layouts.md` et `references/json-schema.md` pour qu'ils soient découvrables par les agents qui construisent les decks.

---

**Statut final** : ✅ Nommage **livré comme spécifié**. 17/17 slides ont leur `cSld@name`. 1 test échoue pour cause indépendante (édit manuel utilisateur antérieur), diagnostic complet ci-dessus.
