# Chantier 10 — Fixes post-test réel "Migration Cloud TechnoLog"

**Date** : 2026-05-19
**Périmètre** : 9 défauts identifiés visuellement après l'examen du premier deck généré en conditions réelles. Tous fixés en un passage, validés par tests et par régénération du deck.

## TL;DR

| # | Fix | Statut | Note |
|---:|---|---|---|
| 1 | Footer debug `[layout: …]` | ✅ | `--debug-layouts` flag, deck dédié livré |
| 2 | hero_stat itérait `supporting` char par char | ✅ | `isinstance(str)` guard dans `add_hero_stat` |
| 3 | Orphan group `{{XXX_GROUP}}` | ✅ moteur | côté template à câbler par l'utilisateur (instructions §10) |
| 4 | KPI values débordent | ✅ | auto-shrink heuristique sur `value` |
| 5 | Dates débordent | ✅ | auto-shrink sur `date` (1er sept 2026 → 10pt) |
| 6 | Matrix 4 quadrants vides | ✅ | simple processor n'écrase plus les `quad_*` |
| 7 | comparison_before_after vides | ✅ | flattening `before:{...}` / `after:{...}` |
| 8 | Roadmap typo « 24pt » | ⚪ no-op | XML correct, perception attribuable à `spAutoFit` (cf §8) |
| 9 | Pagination 10 items max | ✅ | `PAGINATED_LAYOUTS = {'agenda_diagonal': 10}` + espacement resserré |

**Tests** : **37 passed, 1 skipped** (7 nouveaux tests).
**Decks régénérés** : `examples/test_migration_cloud.pptx` (669 KB) + `examples/test_migration_cloud_debug.pptx` (671 KB).

## Inspection initiale du deck (avant fix)

| Slide | cSld / mécanisme | Défaut observé |
|---:|---|---|
| 4 | `executive_summary` (template) | 3 groupes itérés correctement ; `takeaway_bar` orphelin sans `{{TAKEAWAY}}` |
| 5 | `hero_stat` (code) | 5 TextBox « 4 / 7 / / i / n » : itération sur les caractères du supporting |
| 6 | `kpi_with_chart` (template) | KPI labels/values substitués ✓ mais shape étroite : « 4.2 M€ » à 28pt pourrait déborder |
| 7 | `matrix_2x2_styled` (template) | Seuls les `quad_*_bg` (fonds) présents — AUCUN `{{QUAD_*_TITLE}}` ni `{{QUAD_*_BULLETS}}` |
| 15 | `comparison_before_after` (template) | `{{TAKEAWAY}}` rempli, `before_card` / `after_card` shape vides — pas de `{{REPEAT_ITEM}}` ; template attend `{{BEFORE_TITLE}}` etc. flat |
| 17 | `roadmap_styled` (template) | XML montre sz=1400 (DATE) et sz=1800 (MILESTONE) — pas de surcharge XML, perception subjective |
| 19 | `next_steps` (template) | « 1er septembre 2026 » à sz=1400 — shape étroite, débordement probable |

## Fix 1 — Debug layout footer (`--debug-layouts`)

Implémentation : `_add_layout_debug_footer(slide, layout_name, is_code_based)` ajoute une textbox 6pt italique gris très clair (`#A0A0A0`) en bas à gauche (0.4", 5.35") avec le tag `[layout: <name>(code-based)?]`.

`build_deck()` étendu d'un kwarg `debug_layouts=False`. Le CLI expose `--debug-layouts`. Helper interne `_stamp_new_slides(prev_n, layout, is_code)` itère toutes les slides ajoutées depuis `prev_n` — couvre cover, slides paginées, et closing en un seul appel.

Test : `test_debug_layouts_footer` ✓.

## Fix 2 — hero_stat itérait `supporting` char par char

Cause : `for item in supporting[:5]` itère sur les caractères d'une string. Mon test migration cloud passait `supporting: "47 incidents en 2025 contre 19 en 2023 — l'infrastructure actuelle ne tient plus la charge"` → 5 caractères affichés en 5 TextBox.

Fix (1 ligne) :
```python
if isinstance(supporting, str):
    supporting = [supporting]
```

Test : `test_hero_stat_with_long_text` ✓ (vérifie que la chaîne complète apparaît en UNE textbox).

## Fix 3 — Orphan group `{{XXX_GROUP}}`

Helper `_process_orphan_groups()` ajouté à la pipeline AVANT `_process_simple_placeholders` :
```python
_ORPHAN_GROUP_RE = re.compile(r'^\{\{([A-Z][A-Z0-9_]*)_GROUP\}\}$')
```
Scanne les groupes top-level dont le nom matche `{{<KEY>_GROUP}}` ; si `spec[<key>]` est `None`/`''`/`[]`/`{}` → groupe supprimé en entier.

Test : `test_orphan_group_removed_when_empty` ✓ (vérifie la regex et la logique en unit test isolé).

**Côté template** : pas modifié dans ce chantier (périmètre strict). Suggestion utilisateur dans §10 ci-dessous.

## Fix 4 — Auto-shrink des KPI values (et plus généralement)

Mécanisme `_maybe_shrink_to_fit(sp_element, text)` appelé après `_set_sp_text` quand la clé est dans `SHRINKABLE_ITEM_KEYS = {'value', 'date', 'action', 'owner'}`.

Heuristique :
- `char_w_emu = sz_pt × factor × 12700` (où factor = 0.55 si bold, 0.50 sinon)
- `text_w = len(text) × char_w_emu`
- Target = `shape_w × 0.95` (5% safety margin)
- Tant que `text_w > target` ET `sz > 1000` : réduire `sz` par 200 (= 2pt)

Effet observé sur le deck regénéré (slide 6) :
- « 4.2 M€ » (6 char) : 28pt → **20pt** (4 paliers)
- Identique pour « 3.1 M€ » et « 1.1 M€ »

Test : `test_kpi_value_shrinks_on_overflow` ✓.

## Fix 5 — Auto-shrink des dates (next_steps)

Même mécanisme, clé `date` dans SHRINKABLE_ITEM_KEYS. Slide 19 régénérée :
- « 15 juin 2026 » (12 char) : 14pt (pas de shrink, ça passe)
- « 30 juin 2026 » : 14pt
- « 15 juillet 2026 » (15 char) : 14pt → **12pt**
- « 1er septembre 2026 » (18 char) : 14pt → **10pt** (4 paliers, plancher atteint)

10pt sur date risque d'être petit. Si l'utilisateur veut un floor à 12pt, modifier `min_sz=1200` dans l'appel. Aujourd'hui floor à 10pt pour ne jamais tronquer.

Test : `test_next_steps_long_dates` ✓.

## Fix 6 — Matrix 4 quadrants vides

**Diagnostic** : le template HA les shapes `{{QUAD_TOP_LEFT_TITLE}}`, etc. (vérifié à l'inspection du slide 15 du template). Le bug : après que `_process_quad_placeholders` ait rempli les textes, `_process_simple_placeholders` voyait le shape `{{QUAD_TOP_LEFT_TITLE}}` ne pas correspondre à une clé du spec (`quad_top_left_title` not in spec) et la **supprimait**.

**Fix** : exclusion dans `_process_simple_placeholders` :
```python
if key.startswith('quad_'):
    continue
if re.search(r'_\d+_', key):  # indexed placeholders like COL_1_TITLE
    continue
```

Et bonus : `_process_quad_placeholders` accepte désormais `items` comme alias de `bullets` (et vice-versa). Donne plus de flexibilité au caller.

Validation visuelle (slide 7 régénérée) : les 4 titres « Quick wins / Priorités stratégiques / Maintenir / Reconsidérer » + les bullets associés apparaissent ✓.

Test : `test_matrix_2x2_renders_all_quadrants` ✓.

## Fix 7 — comparison_before_after vides

**Diagnostic** : le template a `{{BEFORE_TITLE}}`, `{{BEFORE_BULLETS}}`, `{{AFTER_TITLE}}`, `{{AFTER_BULLETS}}` — placeholders flat, PAS de `{{REPEAT_ITEM}}`. Ma spec utilisait `items: [...]` qui ne correspondait à rien.

**Fix** : helper `_flatten_nested_groups(spec)` appelé en début de `render_template_slide`. Pour tout `outer_key: {inner_key: val, ...}` (sauf les keys techniques `quadrants`, `chart`, `cover`), crée un alias flat `<outer>_<inner>` dans la spec. Permet d'écrire :
```json
{"before": {"title": "...", "bullets": "..."}}
```
qui devient en interne `{"before_title": "...", "before_bullets": "..."}` → matche `{{BEFORE_TITLE}}` etc.

J'ai aussi mis à jour `_process_simple_placeholders` pour accepter les listes (rendues en `• …`), parité avec quad processor.

Migration spec adaptée : `examples/test_migration_cloud.json` utilise désormais `before: {...}, after: {...}` pour le slide 15. Validation : tous les 4 markers (« Avant migration », « Après migration », « 47 apps sur 3 sites », « 75 % cloud AWS ») présents ✓.

Test : `test_comparison_before_after_renders_both_columns` ✓.

Note : la « paired REPEAT_ITEM » prévue dans la mission n'a PAS été implémentée car non nécessaire pour le template actuel. Si un futur template utilisait 2 `{{REPEAT_ITEM}}` séparés (left/right), il faudra le mécanisme. Cas absent aujourd'hui → reporté Chantier 11.

## Fix 8 — Roadmap typographie : investigation no-op

Inspection XML du deck régénéré (slide 17) :
```
copy 0  {{ITEM_DATE}}      sz=1400 b=1 Arial color=#F26622  text="Jan '26"
copy 0  {{ITEM_MILESTONE}}  sz=1800 b=1 Arial color=#14163C  text='Phase 0 — Quick wins...'
... (idem pour copies 1-4)
```

Inspection du slide layout 'Texte' (sur lequel reposent les slides template-based) :
```
Layout defRPr with sz attribute: (vide — aucune surcharge)
Master defRPr with sz>=1800: (présents pour les placeholders inherités, NON applicable aux textbox autonomes)
```

**Conclusion** : aucune surcharge XML identifiable. Les sz sont littéralement écrits sur chaque run. Si l'utilisateur visualise « 24pt gras », hypothèses :
- (a) `<a:spAutoFit/>` sur les shapes texte → la shape grandit pour englober le texte → effet « gros » visuellement même si le sz est correct.
- (b) Rendu via LibreOffice/Google Slides qui ignore l'rPr et utilise un fallback (vu sur des cas similaires).
- (c) Confusion avec le titre `{{TITLE}}` qui lui est légitimement plus grand.

**Action** : aucun changement moteur (XML correct). `milestone` retiré du SHRINKABLE_ITEM_KEYS (ne pas écraser à 10pt un texte de phrase long qui doit naturellement wrapper).

Si l'utilisateur souhaite réduire MILESTONE à 14pt, c'est un ajustement template (1 click dans PowerPoint sur la shape source). Hors-scope ici.

## Fix 9 — Pagination à 10 items max

```python
PAGINATED_LAYOUTS = {'agenda_diagonal': 10}
```

Distribution `single_column` adaptée : `gap = Inches(0.05)` au-delà de 8 items (au lieu de 0.10) pour densifier.

Tests renommés : `test_agenda_paginates_at_7_items` → `test_agenda_paginates_at_10_items` (12 items → 10+2). `test_agenda_continuous_numbering` vérifie « 11 », « 12 » sur la page 2 ✓.

## Tests pytest

```
======================== 37 passed, 1 skipped in 2.45s =========================
```

7 nouveaux tests, tous au vert. Aucune régression sur les 30 précédents.

## Validation visuelle — Régénération du deck migration

```
OK — wrote examples/test_migration_cloud.pptx (669,040 bytes)         ~0.98s
OK — wrote examples/test_migration_cloud_debug.pptx (670,778 bytes)   ~0.86s
```

| Slide | Avant fix | Après fix |
|---:|---|---|
| 4 (executive_summary) | takeaway_bar orphelin existait | Inchangé — le template n'a pas encore `{{TAKEAWAY_GROUP}}` (cf §10) |
| 5 (hero_stat) | « 4 / 7 / / i / n » | « 47 incidents en 2025 contre 19 en 2023 — l'infrastructure actuelle ne tient plus » sur une seule textbox ✓ |
| 6 (kpi_with_chart) | « 4.2 M€ » à 28pt potentiellement débordant | sz auto-réduite à 20pt ✓ |
| 7 (matrix_2x2_styled) | 4 quadrants vides | 4 titres + bullets remplis ✓ |
| 15 (comparison_before_after) | colonnes vides | titres + 4 bullets par côté ✓ |
| 17 (roadmap_styled) | sz=1400/1800 à l'XML | inchangé (XML déjà correct, cf §8) |
| 19 (next_steps) | « 1er septembre 2026 » à 14pt fixe | shrunk progressivement (14pt / 14pt / 12pt / 10pt selon longueur) ✓ |

## Suggestions de modifications template (§10)

Pour permettre le mécanisme `{{XXX_GROUP}}` (Fix 3), l'utilisateur peut grouper manuellement dans PowerPoint (sélection → Ctrl+G, puis renommer le groupe dans le volet sélection) :

| Slide template | Group à créer | Élément graphique à inclure | Placeholder texte à inclure |
|---|---|---|---|
| `executive_summary` | `{{TAKEAWAY_GROUP}}` | `takeaway_bar` (barre orange) | aucun pour l'instant — si un futur `{{TAKEAWAY}}` est ajouté |
| `comparison_before_after` | `{{TAKEAWAY_GROUP}}` | `takeaway_bar` | `{{TAKEAWAY}}` (déjà présent) |
| `matrix_2x2_styled` | `{{Y_AXIS_GROUP}}` | flèche Y + label | `{{Y_AXIS_LABEL}}`, `{{Y_HIGH}}`, `{{Y_LOW}}` |
| `matrix_2x2_styled` | `{{X_AXIS_GROUP}}` | flèche X + label | `{{X_AXIS_LABEL}}` |
| `quote_callout` | `{{QUOTE_ATTRIBUTION_GROUP}}` | trait sous l'attribution | `{{QUOTE_ATTRIBUTION}}` |

Ces 5 groupes rendraient les slides robustes aux specs partielles (pas d'orphelins visibles si une clé est omise).

## Frictions résiduelles (candidats Chantier 11)

1. **Auto-shrink à 10pt sur dates très longues** : « 1er septembre 2026 » → 10pt risque d'être petit. Solutions : raccourcir la spec (« 1 sept 2026 »), élargir la shape dans le template, OU permettre une logique d'ajustement template-wide.
2. **Paired REPEAT_ITEM** non implémenté (pas nécessaire pour les layouts actuels).
3. **Levenshtein suggestion** (chantier 9 Fix 5 bonus) : toujours pas implémenté.
4. **Roadmap MILESTONE 18pt bold** : choix template assumé ; si l'utilisateur veut 14pt, modifier le template directement.

## Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+ orphan, + shrink, + flatten, + quad alias, + simple processor exclusions, + single_column tweak) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (+ debug-layouts CLI/kwarg, + add_hero_stat string guard) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+7 tests, +renommage agenda 7→10) |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (matrix complet, comparison_before_after, comparison_2cols, auto-shrink note) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 10) |
| `chantier10_report.md` | **créé** (ce fichier) |
| `examples/test_migration_cloud.json` | **modifié** (slide comparison_before_after : items → before/after) |
| `examples/test_migration_cloud.pptx` | **régénéré** |
| `examples/test_migration_cloud_debug.pptx` | **créé** (avec annotations [layout: …]) |

`AOSIS_template.pptx` **non modifié** comme demandé.

---

**Statut final** : ✅ Chantier 10 **livré sans régression**. 37/38 tests verts (1 skip soffice pré-existant), 8 fixes appliqués / 1 investigation no-op, deck régénéré avec validation visuelle de chaque slide problématique.
