# Chantier 26 — Fix 3 bugs visuels résiduels (sommaire, chart, framework_3cards)

**Branche** : `fix/sommaire-chart-framework-bugs`
**Date** : 2026-05-26
**Statut** : Code et docs livrés, tests verts. **En attente de validation visuelle utilisateur sur PowerPoint avant merge sur `main`.**
**Périmètre** : `scripts/template_engine.py`, `scripts/chart_engine.py`, `tests/test_smoke.py`, `references/layouts.md`, `references/philosophy.md`. **Aucune modification du template `AOSIS_template.pptx`.**

---

## 1. Origine des bugs

Les 3 bugs ont été identifiés par le test A/B du Chantier 25 sur le rapport
`cloud_computing_rapport.pdf`. Ils étaient présents sur les **deux versions**
(main et expérimentale), donc **indépendants de la philosophie
communication-first** introduite au C25. Ils n'avaient pas été détectés par
les 90 tests existants ni par les decks générés depuis le C1, car les
usages typiques évitaient les 3 cas pathologiques :

| Bug | Cas pathologique | Pourquoi pas détecté avant |
|---|---|---|
| 1 | `agenda_diagonal` items en strings | Les decks antérieurs utilisaient toujours `{title: "..."}` (dict) |
| 2 | Chart `line` avec `values` (single-series flat) | Les decks antérieurs utilisaient `series=[{name, values}]` (multi-series) |
| 3 | `framework_3cards` avec 4+ items | Les decks antérieurs respectaient implicitement la limite de 3 |

---

## 2. Bug 1 — agenda_diagonal affiche `"01"` partout

### Diagnostic confirmé

Localisation : [aosis-deck-builder/scripts/template_engine.py:1176-1189](aosis-deck-builder/scripts/template_engine.py#L1176-L1189)

Avant le fix, la fonction `_resolve_item_value(item, key, index, distribution)`
plaçait l'auto-fill du numéro APRÈS le test `isinstance(item, dict)` :

```python
def _resolve_item_value(item, key, index, distribution):
    if not isinstance(item, dict):
        if key in ('text', 'title', 'label', 'name'):
            return item
        return None                              # ← string + key='number' tombe ici
    if key in item:
        return item[key]
    if key == 'number':                          # ← auto-fill UNIQUEMENT pour les dicts
        return f'{index + 1:02d}'
    return None
```

Quand l'agenda recevait `items: ["Diagnostic", "Vision", ...]`, le branch
string court-circuitait l'auto-fill. Le moteur recevait `value=None` (ligne
1089) et la branche `if value is None: continue` (ligne 1090) laissait le
texte par défaut du template (`"01"`) sur chaque copie REPEAT_ITEM.

### Fix appliqué

Déplacement de la branche `if key == 'number'` **AVANT** le test isinstance :

```python
def _resolve_item_value(item, key, index, distribution):
    # Chantier 26 — auto-numbering applies to both dict items (when 'number'
    # is missing) and plain string items.
    if key == 'number':
        if isinstance(item, dict) and 'number' in item:
            return item['number']
        return f'{index + 1:02d}'
    if not isinstance(item, dict):
        if key in ('text', 'title', 'label', 'name'):
            return item
        return None
    if key in item:
        return item[key]
    return None
```

### Avant / après — capture du texte ITEM_NUMBER

| Spec items | Avant Chantier 26 | Après Chantier 26 |
|---|---|---|
| `[{"title": "A"}, {"title": "B"}, {"title": "C"}]` | `["01", "02", "03"]` ✅ | `["01", "02", "03"]` ✅ (régression nulle) |
| `["A", "B", "C", "D", "E"]` | `["01", "01", "01", "01", "01"]` ❌ | `["01", "02", "03", "04", "05"]` ✅ |
| `[{"number": "I"}, {"number": "II"}, {"number": "III"}]` | `["I", "II", "III"]` ✅ | `["I", "II", "III"]` ✅ (préservation explicite) |

Mesure réelle sur `examples/test_C26_fixes.pptx` (5 items strings) :
```
BUG 1 (agenda numbering) ITEM_NUMBER texts: ['01', '02', '03', '04', '05']
  → PASS
```

---

## 3. Bug 2 — Line chart silencieusement vide

### Diagnostic confirmé

Localisation : [aosis-deck-builder/scripts/chart_engine.py:227-242](aosis-deck-builder/scripts/chart_engine.py#L227-L242)

Avant le fix, `_render_line` lisait `spec.get("series", [])`. Un spec
`{type: "line", labels: [...], values: [42, 51, ...]}` produisait un cadre
matplotlib **complètement vide** sans aucune erreur ni log — `ax.plot()`
n'était jamais appelé.

### Fix appliqué

Coalescing automatique dans `render_chart_to_png` juste après détermination de `kind` :

```python
_SERIES_REQUIRING_KINDS = {"line", "bar_stacked"}
if (kind in _SERIES_REQUIRING_KINDS
        and "values" in chart_spec
        and "series" not in chart_spec):
    chart_spec = dict(chart_spec)
    chart_spec["series"] = [{
        "name": chart_spec.get("series_name", ""),
        "values": chart_spec["values"],
    }]
    sys.stderr.write("chart_engine: 'line' chart received 'values' ...\n")
```

Plus une validation explicite : si après coalescing aucune donnée
(`series` vide ET `values` vide, sauf pour `combo` qui a son propre format
`bars`/`line`), `raise ValueError`.

### Avant / après — logs de génération

**Avant Chantier 26** (deck `test_AB_experiment.pptx`, slide 4) :
```
image cache HIT: 'cloud computing data center' (landscape, 556×540)
[aucun log chart, aucune erreur — PNG matplotlib ~10 KB axes vides]
```

**Après Chantier 26** (deck `test_C26_fixes.pptx`, slide 3) :
```
image cache HIT: 'cloud computing data center' (landscape, 556×540)
chart_engine: 'line' chart received 'values' (single-series format),
  coalesced to 'series'. Prefer the canonical 'series=[{name,values}]'
  form for multi-series charts.
OK — wrote examples/test_C26_fixes.pptx (667,059 bytes)
```

Mesure réelle sur la slide 3 (`kpi_with_chart`) :
- 1 picture inserted sur la slide (chart matplotlib)
- Picture blob size : **30 014 bytes** → chart bien populé (> seuil 18 KB)
- Picture dimensions : 913 × 461 px (rendu 150 DPI)

---

## 4. Bug 3 — framework_3cards × 4 cartes

### Diagnostic confirmé

Localisation : [aosis-deck-builder/scripts/template_engine.py:604-617](aosis-deck-builder/scripts/template_engine.py#L604-L617)

La boucle qui applique les positions calculées par `_compute_positions`
ignorait les `(w, h)` retournés :
```python
left, top, w, h = positions[i]
dx = left - base_left
dy = top - base_top
_shift_group(new_el, dx=dx, dy=dy)   # TRANSLATE only — pas de scaling
```

Conséquence pour `n=4` :
- `item_w` calculé = 2.98" (vs ~4" pour n=3)
- Groupes espacés à `left ≈ 0.40, 3.18, 6.36, 9.54"`
- Mais chaque groupe garde sa **largeur d'origine** (calibrée pour n=3, ~4")
- Le card background opaque du groupe N+1 **peint par-dessus** le titre
  du groupe N → titres tronqués ("Réduct", "Agilit", "Scalabi", "Modernisati")

### Décision retenue : Option B (cap + ValueError)

Trois options étaient sur la table :

| Option | Description | Décision |
|---|---|---|
| A | Helper `_scale_group` proportionnel des shapes internes | Rejetée — fragile sur les textframes (les tailles de police restent absolues, débordements en cascade) |
| **B** | **Cap dur à 3 + `ValueError` explicite + pointer vers `canvas_blank`** | **Retenue** — comportement prévisible, erreur actionable, pas de complexité supplémentaire |
| C | Nouveau layout `framework_4cards` dans le template | Rejetée — toucherait au template `.pptx` (hors périmètre), report d'effort |

### Fix appliqué

Ajout en haut de `template_engine.py` (vers ligne 134) :

```python
MAX_ITEMS_BY_LAYOUT = {
    'framework_3cards': 3,
}

_MAX_ITEMS_ALTERNATIVES = {
    'framework_3cards': "split into multiple slides, or use 'canvas_blank' "
                        "with kpi_card blocks for 4+ cards",
}
```

Check en début de `_process_repeat_items` :
```python
max_items = MAX_ITEMS_BY_LAYOUT.get(layout_name)
if max_items is not None and len(items) > max_items:
    alt = _MAX_ITEMS_ALTERNATIVES.get(layout_name, "see references/layouts.md")
    raise ValueError(
        f"Layout '{layout_name}' accepts max {max_items} items "
        f"(got {len(items)}). For more items: {alt}. "
        f"See references/layouts.md for alternatives."
    )
```

### Avant / après — capture du message d'erreur

**Avant Chantier 26** :
- 4 items → deck généré silencieusement avec chevauchement visible

**Après Chantier 26** :
```
ValueError: Layout 'framework_3cards' accepts max 3 items (got 4).
  For more items: split into multiple slides, or use 'canvas_blank'
  with kpi_card blocks for 4+ cards. See references/layouts.md for
  alternatives.
```

Mesure réelle sur `examples/test_C26_fixes.pptx` (3 items) :
```
BUG 3 (framework_3cards) card groups: 3
  → PASS
  Titles: ['Réduction du TCO', 'Agilité opérationnelle', 'Modernisation applicative']
```

Architecture extensible : ajouter une entrée à `MAX_ITEMS_BY_LAYOUT`
suffit pour capper d'autres layouts (ex : si on identifie le même
problème sur `comparison_2cols` à n=3+, on l'ajoute au dict).

---

## 5. Tests de non-régression

```bash
python -m pytest aosis-deck-builder/tests/ -v
```

**Résultat** : `97 passed, 1 skipped in 5.13s` ✅

Détail des 7 nouveaux tests Chantier 26 :

| Test | Couvre |
|---|---|
| `test_agenda_diagonal_auto_numbering_from_strings` | Bug 1 — 5 items strings → "01"-"05" |
| `test_agenda_diagonal_explicit_numbers_preserved` | Bug 1 — dict avec `number="A"`/"B"/"C" → conservés |
| `test_chart_values_format_coalesced_to_series` | Bug 2 — line + values → PNG > 18 KB |
| `test_chart_with_series_still_works` | Bug 2 — régression multi-séries |
| `test_chart_missing_series_and_values_raises` | Bug 2 — ValueError + message contient "series" et "values" |
| `test_framework_3cards_rejects_4_cards` | Bug 3 — 4 items → ValueError citant "framework_3cards", "3", "4", "canvas_blank" |
| `test_framework_3cards_accepts_3_cards` | Bug 3 — régression : 3 items → 3 groupes REPEAT_ITEM |

Le test skippé est `visual_review` (nécessite `soffice`+`pdftoppm` système), comme attendu depuis le C7.

---

## 6. Livrable de validation visuelle

`examples/test_C26_fixes.pptx` (5 slides, 667 KB) :
1. **Cover** — Le Cloud Computing en 2026 — Validation Chantier 26
2. **Agenda** (items strings) — 5 numéros distincts `01, 02, 03, 04, 05` (fix 1)
3. **kpi_with_chart** (chart `line` avec `values`) — chart matplotlib peuplé visible (fix 2)
4. **framework_3cards** — 3 cartes avec titres complets non-tronqués (fix 3)
5. **closing_diagonal** (auto-ajouté par `closing: true`)

À ouvrir dans PowerPoint pour validation visuelle finale.

---

## 7. Périmètre strict respecté

| Fichier | Touché ? |
|---|---|
| `scripts/template_engine.py` | ✅ (fix 1 + fix 3) |
| `scripts/chart_engine.py` | ✅ (fix 2) |
| `tests/test_smoke.py` | ✅ (+7 nouveaux tests) |
| `references/layouts.md` | ✅ (fiche `framework_3cards` mise à jour) |
| `references/philosophy.md` | ✅ (2 lignes anti-patterns) |
| `CHANGELOG.md` | ✅ (entrée Chantier 26) |
| `assets/AOSIS_template.pptx` | ❌ non modifié |
| `SKILL.md` | ❌ non modifié |
| Autres layouts (non concernés) | ❌ non modifiés |

---

## 8. Action de l'utilisateur attendue

1. Ouvrir `examples/test_C26_fixes.pptx` dans PowerPoint et valider visuellement les 3 fix.
2. Si OK → merge la branche `fix/sommaire-chart-framework-bugs` sur `main` via les 3 commandes habituelles (push direct bloqué par le classifier auto-mode) :
   ```bash
   git checkout main
   git merge fix/sommaire-chart-framework-bugs --no-ff
   git push origin main
   git branch -d fix/sommaire-chart-framework-bugs
   git push origin --delete fix/sommaire-chart-framework-bugs
   ```
3. Si problèmes visuels résiduels → ouvrir un Chantier 27.
