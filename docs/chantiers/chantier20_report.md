# Chantier 20 — Polish KPI cards : positionnement dynamique et anti-débordement

**Date** : 2026-05-21
**Périmètre** : Trois bugs visuels résiduels après le Chantier 19 sur le deck V3 (cards courtes label long, valeurs M€ qui wrappent, débordement vertical). Tous causés par un positionnement vertical **fixe** dans la card (60% value / 35% label) qui ne s'adapte pas à la hauteur réelle du label.

## TL;DR

- ✅ Nouveau helper `_cb_kpi_card_dynamic_layout(value, label, rect, override_size_pt, floor_pt=14)` — positionnement vertical centré/tassé selon hauteur dispo, anti-overflow garanti
- ✅ Plancher abaissé à **14pt** dans canvas_blank kpi_card ET kpi_with_chart pour gérer les shapes étroites avec chars larges (M€)
- ✅ **76 passed, 1 skipped** (3 nouveaux tests + 1 seuil ajusté)
- ✅ Backup `template_engine.before-chantier20.py` créé
- ✅ 3 decks régénérés et vérifiés

## 1. Inspection du template kpi_with_chart

| Shape | Position | Dimensions |
|---|---|---|
| `{{TITLE}}` | (0.26", 0.19") | 9.48" × 0.28" |
| `{{REPEAT_ITEM}}` | (0.40", 1.73") | 2.91" × 0.87" |
| ↳ `kpi_card` (bg) | (0.40", 1.73") | 2.90" × 0.87" |
| ↳ `{{KPI_LABEL}}` | (0.53", 2.03") | 1.64" × 0.30" |
| ↳ `{{KPI_VALUE}}` | (2.31", 1.94") | **1.00" × 0.47"** |
| `{{CHART_PLACEHOLDER}}` | (3.60", 1.73") | 6.00" × 3.00" |
| `{{SOURCE}}` | (0.40", 5.20") | 5.00" × 0.25" |

**Disposition** : label **à gauche** (1.64" wide), valeur **à droite** (1.00" wide × 0.47" tall) — disposition horizontale dans une card 2.90"×0.87". Cette disposition est intrinsèquement contrainte : la valeur n'a que 1.00" de largeur, ce qui force un shrink important pour les valeurs avec caractères larges comme `M€` ou `Mds$`.

**Suggestion de modification template (non appliquée)** : passer en disposition verticale (label SOUS la valeur, valeur pleine largeur 2.7" + label 2.7") permettrait de garder le 60pt XXL même pour les valeurs longues. À discuter — pour l'instant Option B (restreindre la taille de police au shape réel) est retenue.

## 2. Solution — 3 fixes

### Fix 1 — Positionnement dynamique dans canvas_blank kpi_card

Nouveau helper retournant rects + taille :

```python
def _cb_kpi_card_dynamic_layout(value, label, rect, override_size_pt=None, floor_pt=14):
    L, T, W, H = rect
    pad = int(0.10 * 914400)        # 0.10" inner padding
    spacing = int(0.05 * 914400)    # 0.05" gap value→label
    available_w = W - 2 * pad

    # Estimate label height (10pt UPPERCASE, char width 0.60×pt, line h 1.25)
    label_text = (label or '').upper()
    chars_per_line = max(1, int(available_w / (10 * 12700 * 0.60)))
    n_lines = max(1, (len(label_text) + chars_per_line - 1) // chars_per_line)
    label_h = int(n_lines * 10 * 12700 * 1.25)

    # Cap label to 50% of inner (so XXL has room)
    inner_h = H - 2 * pad
    label_h = min(label_h, max(int(10*12700*1.25), inner_h // 2))

    # Compute value size from remaining budget
    value_max_h = inner_h - label_h - spacing
    if value_max_h < 14*12700:
        value_max_h = max(int(14*12700), inner_h // 2)
        label_h = max(int(10*12700*1.25), inner_h - value_max_h - spacing)
    value_size_pt = override_size_pt or _compute_max_kpi_font_size(
        value, available_w, value_max_h, floor_pt=floor_pt)

    # Center vertically if room, tight-pack otherwise
    value_h = int(value_size_pt * 12700 * 1.05)
    total_h = value_h + spacing + label_h
    top_margin = (pad + (inner_h - total_h)//2) if total_h <= inner_h else pad
    if total_h > inner_h:
        label_h = max(int(0.13 * 914400), H - top_margin - value_h - spacing - pad)

    value_rect = (L+pad, T+top_margin, available_w, value_h)
    label_rect = (L+pad, T+top_margin+value_h+spacing, available_w, label_h)
    return value_size_pt, value_rect, label_rect
```

`_cb_render_kpi_card` consomme directement ces rects (plus de calcul interne).
La logique de slide-level uniformity utilise le même helper pour calculer per-card MIN.

### Fix 2 — floor_pt=14 dans kpi_with_chart

Dans la branche `kpi_with_chart` de `_process_repeat_items`, ajout du paramètre :

```python
per_kpi_max.append(
    _compute_max_kpi_font_size(text, w_emu, h_emu, floor_pt=14)
)
```

Avant : "4.2 M€" sur 1.00"×0.47" → 24pt floor → wrap.
Après : raw_pt = min(33.8pt height, 21.8pt width) = 21.8 → snap 18 → max(14, 18) = **18pt** → fit single line.

### Fix 3 — Anti-débordement vertical asymétrique

Les rects calculés par `_cb_compute_block_rects` (branche asym 1 visual + N stacked) tiennent déjà dans `[blocks_top, _CB_CONTENT_BOTTOM]` (= 4.675"). L'overflow rapporté sur slide 10 venait du texte intérieur (label multi-lignes) qui débordait du rect, pas du rect lui-même. **Fix 1 résout ça** en bornant `label_rect.bottom ≤ card.bottom - pad`. Aucune modification du code de grille — un test `test_canvas_blank_5_blocks_no_footer_overlap` verrouille la propriété.

## 3. Avant / Après par slide

### V3 deck `cloud_computing_2026_v3.pptx`

| Slide | Composition | Card H | Avant C20 | Après C20 |
|---|---|---:|---:|---:|
| 5 Adoption | 4 blocs asym (3 KPI + chart) | 1.07" | 36pt label overflow | **48pt**, B=3.11" propre |
| 10 Statu quo | 4 blocs asym (3 KPI + chart) | 1.07" | 36pt, last B=4.35" mais label overflow | **48pt**, last B=4.35" sans overflow |
| 15 Piliers | 4 blocs 2×2 | 1.67" | 60pt OK | **60pt** XXL maintenu |
| 16 Quatre actions | 6 blocs asym (4 KPI + 1 text + 1 image) | 0.58" | 24pt floor → label chevauche value | **14pt** value above label, no overlap |

### V1 deck `test_migration_cloud.pptx`

| Slide | Composition | Avant C20 | Après C20 |
|---|---|---:|---:|
| 6 TCO trajectoire (kpi_with_chart) | 3 KPI "4.2 M€" / "3.1 M€" / "1.1 M€" | 24pt → wrap "M€" sur ligne 2 | **18pt** single-line uniforme |

### Mesures exactes slide 16 V3

```
KPI 'M1'      sz=14.0pt T=1.20"  B=1.40"   (value)
LBL 'AUDIT…'  sz=10.0pt T=1.45"  B=1.59"   (label, 0.05" sous value)
KPI 'M2'      sz=14.0pt T=1.94"  B=2.14"
LBL 'ÉVAL…'   sz=10.0pt T=2.19"  B=2.34"
KPI 'M2-3'    sz=14.0pt T=2.69"  B=2.89"
LBL 'CHOIX…'  sz=10.0pt T=2.94"  B=3.08"
KPI 'M3'      sz=14.0pt T=3.43"  B=3.63"
LBL 'CADR…'   sz=10.0pt T=3.68"  B=3.83"   (last card → footer reserve 0.92" libre)
```

Tout est dans l'enveloppe `[card_top, card_bottom]`. Aucun chevauchement.

## 4. Tests

```
======================== 76 passed, 1 skipped in 5.20s =========================
```

3 nouveaux :

| Test | Vérifie |
|---|---|
| `test_kpi_card_label_below_value_no_overlap` | Unit du helper : `label_rect.top ≥ value_rect.bottom` + card non débordée |
| `test_canvas_blank_5_blocks_no_footer_overlap` | 5 blocs asym (4 KPI + chart) : aucun shape ≤ 4.75" du haut |
| `test_kpi_with_chart_value_fits_width` | "5.9 M€" sur shape 1.00" wide : `n_chars × 0.55 × sz_pt ≤ 72pt × 1.05` (no wrap) |

1 ajusté :
- `test_kpi_value_shrinks_on_overflow` : seuil `>= 2400` → `>= 1400` (cohérent avec `floor_pt=14` dans kpi_with_chart codepath)

Aucune régression sur les 73 tests existants.

## 5. Friction et arbitrages

1. **Disposition horizontale du template kpi_with_chart** : le shape `{{KPI_VALUE}}` n'est que 1.00" de large car le template place le label à sa GAUCHE. Pour les valeurs avec chars larges (M€, Mds$, %, K€), cela force un shrink important. Option B retenue (restreindre la police). Si une modification template est souhaitée, je suggère :
   ```
   {{KPI_VALUE}}  L=0.53", T=1.83", W=2.34", H=0.50"   # pleine largeur, sur le top
   {{KPI_LABEL}}  L=0.53", T=2.33", W=2.34", H=0.25"   # sous, smaller
   ```
   Cela permettrait de garder 60pt XXL même sur "5.9 M€" (1.97" estimé < 2.34" dispo).

2. **floor_pt=14 vs 24** : le floor 24pt du C19 a été établi comme "minimum visuel acceptable" pour un KPI. Sur les cards genuinely petites (0.58" sur slide 16, ou shape 0.47" kpi_with_chart), 24pt produit un overflow qui est pire qu'un 14-18pt qui rentre proprement. Le floor 24 reste le default du helper (préserve XXL sur les unit tests existants) ; on passe 14 spécifiquement aux codepaths qui composent des cards potentiellement très étroites.

3. **char width factor 0.60 pour le label** (vs 0.55 pour les digits dans la value) : le label est en UPPERCASE bold Arial — les caractères majuscules sont sensiblement plus larges que les digits. 0.60 est plus pessimiste donc plus safe pour estimer le wrap.

4. **Slide 6 V3 mentionnée par l'utilisateur n'est pas kpi_with_chart** : c'est en réalité un `data_table` ("Bénéfices observés sur 30 missions à 24 mois"). La vraie kpi_with_chart "TCO trajectoire" est dans `test_migration_cloud.pptx` slide 6. Le brief mentionnait V3 par confusion ; le fix s'applique de toute façon par mécanisme générique.

## 6. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.before-chantier20.py` | **backup** |
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+`_cb_kpi_card_dynamic_layout`, refactor `_cb_render_kpi_card`, floor_pt=14 dans kpi_with_chart) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+3 tests, +1 seuil ajusté) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 20) |
| `chantier20_report.md` | **créé** (ce fichier) |
| `examples/cloud_computing_2026_v3.pptx` | **régénéré** (1.06 MB) |
| `examples/test_canvas_blank_showcase.pptx` | **régénéré** (818 KB) |
| `examples/test_migration_cloud.pptx` | **régénéré** (980 KB) — KPI M€ fix |

Aucun autre layout touché. Template AOSIS_template.pptx **non modifié** (suggestion en §5.1 à discuter).

---

**Statut final** : ✅ Chantier 20 **livré sans régression**. 76/77 tests verts. Tous les chevauchements value/label éliminés sur canvas_blank kpi_card (slides 5/10/15/16 V3). Wrap "M€" éliminé sur kpi_with_chart (test_migration_cloud slide 6).
