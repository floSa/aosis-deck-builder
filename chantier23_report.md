# Chantier 23 — Nettoyage des 10 layouts code-based à éviter

**Date** : 2026-05-21
**Périmètre** : Retirer du `DISPATCH` les 10 layouts code-based identifiés au Chantier 13 comme « à éviter » (équivalent template-based de meilleure qualité). Le code des fonctions reste pour rétrocompatibilité Git ; seule l'exposition via le pipeline est coupée.

## TL;DR

- ✅ 10 layouts retirés du `DISPATCH` : `swot`, `cards`, `process`, `chart`, `agenda`, `timeline`, `quote`, `comparison`, `matrix_2x2`, `roadmap`
- ✅ Nouveau dict `DEPRECATED_LAYOUTS = {old: replacement}` qui pilote l'erreur explicite
- ✅ `ValueError` claire avec le nom du remplaçant si un spec essaie d'en utiliser un
- ✅ 10 fonctions `add_*` conservées avec annotation `# DEPRECATED`
- ✅ Fixtures, examples et docs migrés
- ✅ **90 passed, 1 skipped** (+10 tests paramétrés)
- ✅ Backup `build_deck.before-chantier23.py`

## 1. Liste des 10 layouts retirés

| Layout retiré | Remplacement template-based | Fonction conservée |
|---|---|---|
| `swot` | `matrix_2x2_styled` | `add_swot` |
| `cards` | `framework_3cards` | `add_cards` |
| `process` | `process_steps` | `add_process` |
| `chart` | `kpi_with_chart` | `add_chart_slide` |
| `agenda` | `agenda_diagonal` | `add_agenda` |
| `timeline` | `roadmap_styled` | `add_timeline` |
| `quote` | `quote_callout` | `add_quote` |
| `comparison` | `comparison_2cols` | `add_comparison` |
| `matrix_2x2` | `matrix_2x2_styled` | `add_matrix_2x2` |
| `roadmap` | `roadmap_styled` | `add_roadmap` |

## 2. Vérification préalable des examples / fixtures

```bash
$ for L in swot cards process chart agenda timeline quote comparison matrix_2x2 roadmap; do
    echo "=== $L ===" ; grep -l "\"layout\":\s*\"$L\"" examples/*.json
  done
```

Résultat : 6/10 layouts dépréciés utilisés dans `examples/example_full.json`, 1/10 (`roadmap`) dans `examples/example_minimal.json`. Plus :
- `tests/fixtures/golden_spec.json` : `matrix_2x2` + `roadmap`
- `tests/fixtures/roadmap_3.json` … `roadmap_6.json` : `roadmap`
- `tests/fixtures/all_layouts.json` : les 10 layouts (chacun apparaît une fois — c'était sa raison d'être)

Tous migrés avant de retirer du DISPATCH.

## 3. Migrations effectuées

### `tests/fixtures/golden_spec.json`
```diff
-      "layout": "matrix_2x2",
+      "layout": "matrix_2x2_styled",
       "x_axis": {"label": "Effort", "low": "Faible", "high": "Élevé"},
+      "x_axis": {"label": "Effort"},     # matrix_2x2_styled n'utilise pas low/high
       ...
-      "layout": "roadmap",
-      "milestones": [{"date": "...", "name": "Audit", "detail": "Cartographie"}, ...]
+      "layout": "roadmap_styled",
+      "items":    [{"date": "...", "milestone": "Audit"}, ...]
```
Le champ `detail` n'est pas porté par `roadmap_styled` — perte acceptable (rendu visuel net).

### `tests/fixtures/roadmap_{3,4,5,6}.json`
Tous migrés `roadmap` → `roadmap_styled` (transformation identique).

### `tests/fixtures/all_layouts.json`
21 slides → 11 slides (les 10 dépréciés retirés). Le test `test_all_layouts_generate` ajusté : seuil `>= 20` → `>= 11`. Layouts restants : `section`, `text`, `content`, `hero_stat`, `big_idea`, `pyramid`, `funnel`, `dashboard`, `org_chart`, `stat_grid`, `image_hero`.

### `examples/example_minimal.json`
`roadmap` → `roadmap_styled`.

### `examples/example_full.json`
6 migrations : `matrix_2x2` → `matrix_2x2_styled`, `comparison` → `comparison_2cols`, `roadmap` → `roadmap_styled`, `process` → `process_steps`, `quote` → `quote_callout`, `cards` → `framework_3cards`. Champs internes adaptés au format de chaque layout cible (notamment `process.steps` → `process_steps.items` avec `text` au lieu de `detail`).

## 4. Mécanisme d'erreur

```python
# scripts/build_deck.py — nouvelle branche dans la boucle slides
if layout in DEPRECATED_LAYOUTS:
    replacement = DEPRECATED_LAYOUTS[layout]
    raise ValueError(
        f"Layout '{layout}' is deprecated and no longer available. "
        f"Use '{replacement}' instead. See references/layouts.md for details."
    )
```

Exemple d'erreur :
```
ValueError: Layout 'swot' is deprecated and no longer available.
Use 'matrix_2x2_styled' instead. See references/layouts.md for details.
```

## 5. Annotations dans le code

Chaque fonction conservée est précédée d'un bloc de commentaires :

```python
# DEPRECATED — retiré du DISPATCH au Chantier 23. Conservé pour rétro-
# compatibilité Git. Utilise 'matrix_2x2_styled' (template-based) à la place.
# Voir references/layouts.md.
def add_swot(prs, title, strengths, weaknesses, opportunities, threats):
    ...
```

Réactivation possible en 30 secondes via Git revert si une régression critique apparaissait — mais la couverture template-based est mature (Chantier 13 → 21).

## 6. Tests

```
90 passed, 1 skipped in 4.53s
```

**Nouveau** (paramétré sur 10 cas) :
| Test | Vérifie |
|---|---|
| `test_deprecated_layouts_raise_clear_error[<layout>-<replacement>]` | Pour chaque (layout, replacement) du dict `DEPRECATED_LAYOUTS` : `ValueError` levée, message cite `layout`, `replacement` et le mot "deprecated" |

**Adapté** :
- `test_all_layouts_generate` : seuil `>= 20` slides → `>= 11` slides (fixture trimée).

Aucune autre régression sur les 79 tests existants. Les tests de bounds `test_roadmap_no_overflow[roadmap_3..6.json]` continuent de passer — ils valident maintenant `roadmap_styled` (template-based), ce qui n'est pas exactement Chantier 1 sémantiquement, mais reste un test de non-régression de geometry sur 3-6 milestones.

## 7. Documentation mise à jour

- **`references/layouts.md`** : bannière `⛔ Retiré du DISPATCH au Chantier 23. Utilise [<remplaçant>](...) à la place.` au-dessus des 4 sections détaillées encore présentes (`swot`, `cards`, `chart`, `process`). Paragraphe final "Layouts hérités (dispatch direct)" obsolète remplacé par un tableau récapitulatif `Layouts retirés au Chantier 23`.
- **`references/json-schema.md`** : les 10 sections de schéma JSON remplacées par des notes courtes `### ~~name~~ — retiré au Chantier 23` pointant vers le remplaçant template-based.
- **`SKILL.md`** : compteur "code-based layouts 23 → 13" mis à jour. Quick-example migré (utilise `matrix_2x2_styled` et `roadmap_styled`). 3 paragraphes de guidance qui mentionnaient les anciens noms (`comparison`, `matrix_2x2`, `roadmap`, `chart`, `quote`) corrigés. Frontmatter `description:` ajusté pour ne plus exposer les noms dépréciés comme triggers.

## 8. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/build_deck.before-chantier23.py` | **backup** (88 KB) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (10 entrées retirées du DISPATCH, +dict `DEPRECATED_LAYOUTS`, +branche d'erreur, +annotations DEPRECATED sur 10 fonctions, CLI inchangé) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+test paramétré × 10 cas, +1 seuil ajusté) |
| `aosis-deck-builder/tests/fixtures/golden_spec.json` | **migré** |
| `aosis-deck-builder/tests/fixtures/roadmap_{3,4,5,6}.json` | **migrés** |
| `aosis-deck-builder/tests/fixtures/all_layouts.json` | **migré** (10 slides retirées) |
| `aosis-deck-builder/references/layouts.md` | **modifié** |
| `aosis-deck-builder/references/json-schema.md` | **modifié** |
| `aosis-deck-builder/SKILL.md` | **modifié** |
| `examples/example_minimal.json` | **migré** |
| `examples/example_full.json` | **migré** (6 layouts) |
| `CHANGELOG.md` | **modifié** |
| `chantier23_report.md` | **créé** |
| `aosis-deck-builder.skill` | **regénéré** |

Aucune modification du template `AOSIS_template.pptx`. Aucun autre layout touché.

---

**Statut final** : ✅ Chantier 23 **livré sans régression**. 90/91 tests verts. 10 layouts dépréciés invisibles au pipeline mais réversibles (code conservé). Documentation cohérente avec la nouvelle surface.
