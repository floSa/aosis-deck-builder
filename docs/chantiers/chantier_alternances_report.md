# Chantier — Alternances dans 3 layouts template-based

**Date** : 2026-05-19
**Périmètre** : Câbler dans le moteur 3 règles d'alternance qui n'étaient pas appliquées au runtime sur les layouts `framework_3cards`, `roadmap_styled`, `process_steps`.

## TL;DR

- ✅ Nouvelle constante `ALTERNATION_RULES` dans `template_engine.py` + helper `_apply_alternation()` appelé après chaque deepcopy de `REPEAT_ITEM`.
- ✅ Brand palette injectée dans `template_engine` via `set_brand()` (même pattern que `chart_engine`).
- ✅ **25 passed, 1 skipped** — 3 nouveaux tests structurels (`test_framework_3cards_alternates_colors`, `test_process_steps_alternates_colors`, `test_roadmap_alternates_position`).
- ✅ Deck de validation [validation_alternances_deck.pptx](_archive/assets/chantier_alternances_assets/validation_alternances_deck.pptx) (3 slides ciblées + cover + closing) à inspecter visuellement.

## 1. Inspection des 3 slides modèles

Lecture XML directe (python-pptx + lxml) sur `aosis-deck-builder/assets/AOSIS_template.pptx`.

### Slide 9 — `framework_3cards`
| shape (à l'intérieur du `{{REPEAT_ITEM}}`) | fill | rôle |
|---|---|---|
| `{{ITEM_BOXE}}` | `srgb:#211948` (variante dark navy) | **fond de la carte** ← shape à alterner |
| `{{ITEM_ICON}}` | `srgb:#FFFFFF` | rond blanc d'icône |
| `{{ITEM_TITLE}}` | (texte) | titre du pilier |
| `{{ITEM_BULLETS}}` | (texte) | bullets |

**Couleur de référence** : le template utilise actuellement `#211948` (dark navy custom, proche de `navy_alt`). On override les 3 copies au runtime avec `accent1` (orange) / `accent2` (navy_alt) / `accent1`.

### Slide 10 — `roadmap_styled`
| shape | fill | pos (y EMU) | rôle |
|---|---|---|---|
| `timeline_axis` (TOP-LEVEL LINE) | — | y≈2800k | axe horizontal global |
| `{{ITEM_MARKER}}` | `srgb:#F26622` (orange) | y=2647527, h=320040 | losange orange ← **reste orange** |
| `{{ITEM_DATE}}` | (texte) | y=1710267 | date AU-DESSUS du marker |
| `{{ITEM_MILESTONE}}` | (texte) | y=2076027 | label AU-DESSUS du marker |

**Position de référence** : par défaut le texte est AU-DESSUS du marker (template porte la position « impair »). Pour les copies paires (i=1, 3 en 0-indexed → positions 2, 4 en 1-indexed), il faut basculer les deux textes EN-DESSOUS.

Calcul du delta vertical :
- `marker.bottom = 2647527 + 320040 = 2967567` EMU
- `new_top_text = marker.bottom + 150000 (margin) = 3117567` EMU
- `delta_y = 3117567 - 1710267 = +1407300` EMU (≈ 1.54")

Appliqué uniformément à `{{ITEM_DATE}}` et `{{ITEM_MILESTONE}}` → leur écart relatif (365 760 EMU) est préservé.

### Slide 12 — `process_steps`
| shape | fill | rôle |
|---|---|---|
| `process_axis` (TOP-LEVEL LINE) | — | axe horizontal |
| `{{ITEM_MARKER}}` | `srgb:#F26622` (orange) | disque numéroté ← shape à alterner |
| `{{ITEM_NUMBER}}` | (texte) | numéro 01/02/… superposé |
| `{{ITEM_TITLE}}` | (texte) | titre étape |
| `{{ITEM_TEXT}}` | (texte) | description |

## 2. Règles `ALTERNATION_RULES`

```python
ALTERNATION_RULES = {
    "framework_3cards": {
        "type": "fill_color",
        "shape_names": ["{{ITEM_BOXE}}"],
        "colors": ["orange", "navy_alt"],
    },
    "process_steps": {
        "type": "fill_color",
        "shape_names": ["{{ITEM_MARKER}}"],
        "colors": ["orange", "navy_alt"],
    },
    "roadmap_styled": {
        "type": "vertical_flip",
        "text_shape_names": ["{{ITEM_DATE}}", "{{ITEM_MILESTONE}}"],
        "anchor_shape_name": "{{ITEM_MARKER}}",
        "margin_emu": 150000,
    },
}
```

Deux types de règle :
- **`fill_color`** : pour chaque copie d'index `i`, mute le `<a:solidFill><a:srgbClr>` des shape(s) listées avec la couleur `colors[i % len(colors)]`. Pour les 2 layouts concernés (`framework_3cards`, `process_steps`), `colors = ["orange", "navy_alt"]` donne le motif orange/navy/orange/navy/…
- **`vertical_flip`** : pour les copies d'index impair (i=1, 3, …), translate les `text_shape_names` vers le bas pour qu'elles passent sous le `anchor_shape_name`. La marge `margin_emu` règle l'espace entre le bas du marker et le haut du texte. Les positions sont **calculées à partir des shapes réelles** (pas hardcodées) → robuste si l'utilisateur ajuste le template.

Les couleurs sont résolues dynamiquement via `_resolve_color()` : il interroge `_BRAND.<attr>` (injecté par `build_deck.py` au load et sur `--template` override), avec fallback canonique si le brand n'a pas été injecté.

## 3. Mécanique d'intégration

```python
# scripts/template_engine.py
def _process_repeat_items(slide, layout_name, spec):
    ...
    for i, item in enumerate(items):
        new_el = deepcopy(template_el)
        _rename_group(new_el, f'repeat_item_copy_{i+1}')
        _shift_group(new_el, dx, dy)
        _fill_item_placeholders(new_el, item, i, distribution)
        _apply_alternation(new_el, layout_name, i)   # ← nouvelle ligne
        parent.insert(template_idx + 1 + i, new_el)
```

`_apply_alternation()` agit directement sur le XML de la copie *avant* son insertion dans le `spTree` parent. Pour les règles `fill_color`, il mute le `<a:srgbClr val="...">` à l'intérieur du `<a:solidFill>` du `<p:sp>` ciblé. Pour `vertical_flip`, il modifie le `<a:off y="...">` des shapes texte.

Note technique : modifier `<a:off>` du child d'un groupe affecte sa position d'écran via la formule OOXML `screen = group.off + (child.off − group.chOff) × (group.ext / group.chExt)`. Comme `_shift_group` ne modifie que `group.off` (pas `chOff`) — voir commentaire codé du chantier 7 — translater `child.off` translate l'écran d'un montant identique. C'est la convention attendue.

## 4. Injection du brand

`build_deck.py` au module load (et sur rebind `--template`) :
```python
import template_engine as _template_engine
if hasattr(_template_engine, "set_brand"):
    _template_engine.set_brand(BRAND)
```

Symétrique de l'injection `chart_engine.set_brand()` du Chantier 8. Aucun cycle d'import, palette propagée naturellement.

## 5. Vérification post-mutation (smoke)

Génération d'un deck-test (3+4+5 items respectivement) :

```
=== framework_3cards ===
  copy 0  {{ITEM_BOXE}}   fill=#F26622   (orange)
  copy 1  {{ITEM_BOXE}}   fill=#1E2261   (navy)
  copy 2  {{ITEM_BOXE}}   fill=#F26622   (orange)

=== process_steps ===
  copy 0  {{ITEM_MARKER}} fill=#F26622   (orange)
  copy 1  {{ITEM_MARKER}} fill=#1E2261   (navy)
  copy 2  {{ITEM_MARKER}} fill=#F26622   (orange)
  copy 3  {{ITEM_MARKER}} fill=#1E2261   (navy)

=== roadmap_styled ===
  copy 0  marker y=2647527  date y=1710267   → above ✓
  copy 1  marker y=2647527  date y=3117567   → below ✓
  copy 2  marker y=2647527  date y=1710267   → above ✓
  copy 3  marker y=2647527  date y=3117567   → below ✓
  copy 4  marker y=2647527  date y=1710267   → above ✓
  All 5 markers stay #F26622 (orange) ✓
```

## 6. Tests

```
======================== 25 passed, 1 skipped in 2.49s =========================
```

| Nouveau test | Statut |
|---|---|
| `test_framework_3cards_alternates_colors` | ✅ vérifie `[orange, navy_alt, orange]` sur les 3 `{{ITEM_BOXE}}` |
| `test_process_steps_alternates_colors` | ✅ vérifie `[orange, navy_alt, orange, navy_alt]` sur les 4 `{{ITEM_MARKER}}` |
| `test_roadmap_alternates_position` | ✅ vérifie `[above, below, above, below, above]` sur 5 `{{ITEM_DATE}}` ET tous markers restent orange |
| ...22 tests existants | ✅ aucune régression |
| `test_visual_review_generates_artifacts` | ⏭ skip (soffice absent, pré-existant) |

Les tests structurels lisent directement les attributs XML (`<a:srgbClr val>`, `<a:off y>`), donc indépendants du rendu PowerPoint. Suffisants comme harness de non-régression.

## 7. Validation visuelle (à confirmer côté utilisateur)

Deck à inspecter : [_archive/assets/chantier_alternances_assets/validation_alternances_deck.pptx](_archive/assets/chantier_alternances_assets/validation_alternances_deck.pptx) — 5 slides (cover + 3 layouts ciblés + closing).

**Slide 2 — framework_3cards** : 3 cartes (Pillar 1/2/3). Pillar 1 et Pillar 3 doivent apparaître en **orange `#F26622`**, Pillar 2 en **navy_alt `#1E2261`**.

**Slide 3 — process_steps** : 4 étapes (Audit / Cadrage / Build / Bascule). Les cercles numérotés alternent **orange / navy / orange / navy**. Le numéro blanc et l'axe horizontal restent inchangés.

**Slide 4 — roadmap_styled** : 5 milestones. Les marqueurs (losanges) restent **tous orange**. Le texte (date + libellé) est :
- au-DESSUS pour Juin 26, Nov 26, Juin 27 (positions 1, 3, 5)
- au-DESSOUS pour Sept 26, Mars 27 (positions 2, 4)

## 8. Frictions techniques

1. **`{{ITEM_BOXE}}` portait `#211948` (variante dark navy) dans le template**, pas une couleur de palette officielle. La règle écrase systématiquement avec `accent1`/`accent2` → la couleur originale du template est sacrifiée par design. C'est le comportement attendu : l'alternance par layout impose orange/navy/…, pas la couleur arbitraire que l'utilisateur aurait posée manuellement.

2. **Modification du fill sans casser l'ordering OOXML** : `_set_solid_srgb_fill()` mute le `<a:srgbClr val>` quand `<a:solidFill>` existe déjà (cas du template), sinon insère un `<a:solidFill>` en fin de `<p:spPr>` (cas dégradé, non rencontré sur ces 3 shapes). Pas de réordonnancement nécessaire pour ces layouts.

3. **`vertical_flip` calcule la position dynamiquement** au lieu de hardcoder un offset. Avantage : si l'utilisateur réorganise le template (marker plus bas, marge plus large), la règle suit sans modification du code. Inconvénient : 4 lectures XML (anchor.y + h, texte topmost.y) par copie impaire → coût négligeable.

## 9. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+ALTERNATION_RULES, +set_brand, +_apply_alternation, +5 helpers, ~+130 lignes) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (injection brand vers template_engine, +6 lignes) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+3 tests + 4 helpers, ~+130 lignes) |
| `_archive/assets/chantier_alternances_assets/validation_alternances_deck.pptx` | **créé** (5 slides) |
| `chantier_alternances_report.md` | **créé** (ce fichier) |

`AOSIS_template.pptx` **non modifié** comme demandé.

## 10. Suites possibles (hors scope)

- Ajouter une règle similaire pour `comparison_2cols` / `comparison_before_after` quand le mécanisme paired-REPEAT_ITEM sera câblé.
- Permettre des alternances paramétrables via le spec JSON (`alternate_colors: ["#hex1", "#hex2"]`) plutôt que codées en dur dans `ALTERNATION_RULES`. Tradeoff : flexibilité vs cohérence du brand. À discuter selon les besoins futurs.

---

**Statut final** : ✅ Chantier alternances **livré sans régression**. 25/26 tests verts (1 skip soffice pré-existant), 3 règles câblées et testées, deck de validation à inspecter visuellement.
