# Chantier 21 — Refonte kpi_with_chart : passage horizontal → vertical

**Date** : 2026-05-21
**Périmètre** : Refonte de la slide modèle `kpi_with_chart` (slide 6) dans `AOSIS_template.pptx`. Avant : valeur à droite + label à gauche (horizontal). Après : valeur en haut + label en bas (vertical), pleine largeur de la card.

## TL;DR

- ✅ Slide 6 du template modifiée : KPI_VALUE et KPI_LABEL re-positionnés en disposition verticale, pleine largeur card, anchor=center, algn=center
- ✅ Aucune modification du moteur `template_engine.py` — les helpers C19/C20 fonctionnent tels quels avec les nouvelles dimensions
- ✅ **77 passed, 1 skipped** (+1 nouveau test `test_kpi_vertical_layout`, 2 seuils ajustés pour nouveau template)
- ✅ Backups `AOSIS_template.before-chantier21.pptx` + `template_engine.before-chantier21.py`
- ✅ Bundle skill regénéré
- ✅ 2 decks vérifiés (V3 n'a pas de kpi_with_chart — slide TCO est sur `test_migration_cloud`)

## 1. Inspection avant modification

```
┌── Slide 6 'kpi_with_chart' (avant C21) ───────────────────────────────────┐
│ {{TITLE}}              L=0.26"  T=0.19"  W=9.48"  H=0.28"                │
│ {{REPEAT_ITEM}} group  L=0.40"  T=1.73"  W=2.91"  H=0.87"                │
│   ├─ kpi_card (bg)     L=0.40"  T=1.73"  W=2.90"  H=0.87"                │
│   ├─ {{KPI_LABEL}}     L=0.53"  T=2.03"  W=1.64"  H=0.30"  ← LEFT side   │
│   └─ {{KPI_VALUE}}     L=2.31"  T=1.94"  W=1.00"  H=0.47"  ← RIGHT side  │
│ {{CHART_PLACEHOLDER}}  L=3.60"  T=1.73"  W=6.00"  H=3.00"                │
│ {{SOURCE}}             L=0.40"  T=5.20"  W=5.00"  H=0.25"                │
└───────────────────────────────────────────────────────────────────────────┘

Schema interne d'une card (avant) :
┌───────────────────────────────────────────┐  ← card 2.90" × 0.87"
│  KPI label             |     85 %         │
│  (orange, 18pt)        |   (navy, 28pt)   │
│  W=1.64" H=0.30"       |  W=1.00" H=0.47" │
└───────────────────────────────────────────┘

Problème : value shape limité à 1.00" de large → "4.2 M€" (6 chars × 24pt × 0.55 ≈ 79pt)
déborde de 1.00" × 72pt = 72pt → "M€" wrap à la ligne suivante.
```

## 2. Inspection après modification

```
┌── Slide 6 'kpi_with_chart' (après C21) ───────────────────────────────────┐
│ {{TITLE}}              L=0.26"  T=0.19"  W=9.48"  H=0.28"   (inchangé)   │
│ {{REPEAT_ITEM}} group  L=0.40"  T=1.73"  W=2.91"  H=0.87"   (inchangé)   │
│   ├─ kpi_card (bg)     L=0.40"  T=1.73"  W=2.90"  H=0.87"   (inchangé)   │
│   ├─ {{KPI_VALUE}}     L=0.40"  T=1.73"  W=2.90"  H=0.48"  ← TOP, full W │
│   └─ {{KPI_LABEL}}     L=0.40"  T=2.25"  W=2.90"  H=0.35"  ← BOTTOM, fullW│
│ {{CHART_PLACEHOLDER}}  L=3.60"  T=1.73"  W=6.00"  H=3.00"   (inchangé)   │
│ {{SOURCE}}             L=0.40"  T=5.20"  W=5.00"  H=0.25"   (inchangé)   │
└───────────────────────────────────────────────────────────────────────────┘

Schema interne d'une card (après) :
┌───────────────────────────────────────────┐  ← card 2.90" × 0.87"
│             85 %                          │  ← 55% du card H = 0.48"
│      (navy, 30pt baseline, centered)     │      (anchor=ctr, algn=ctr)
├───────────────────────────────────────────┤  ← gap 5% = 0.04"
│            KPI label                      │  ← 35% du card H = 0.35"
│   (orange, 18pt bold, centered)          │
└───────────────────────────────────────────┘
```

**Proportions internes appliquées** :
- VALUE_H = 55 % × CARD_H = 435 864 EMU = 0.48"
- GAP     = 5 % × CARD_H  = 39 624 EMU = 0.04"
- LABEL_H = 35 % × CARD_H = 316 992 EMU = 0.35"
- Total = 95 % de la card (5 % de marge libre, absorbée par les anchors centrés)

**Modifications XML** :
- `<a:off>` et `<a:ext>` ajustés sur les 2 shapes
- `<a:bodyPr>` : `anchor="ctr"` (vertical centering), suppression de `<a:spAutoFit/>`
- `<a:pPr>` : `algn="ctr"` (horizontal centering) sur tous les paragraphes
- Couleurs et tailles de police de base **inchangées** (le moteur C19/C20 override la value à 30pt runtime, label reste à 18pt orange du template)

## 3. Adaptation du moteur

**Aucune modification de code nécessaire** — les helpers existants utilisent `_read_sp_dimensions()` pour lire les nouvelles dimensions du shape `{{KPI_VALUE}}` (2.90" × 0.48") et `_compute_max_kpi_font_size(text, w_emu, h_emu, floor_pt=14)` calcule la bonne taille naturellement.

Calcul auto-shrink pour le nouveau shape (2.90" × 0.48") :

| Value text | n_chars | max_h_pt | max_w_pt | min | snap | résultat |
|---|---:|---:|---:|---:|---:|---:|
| "87 %" | 4 | 34.6 | 91.6 | 34.6 | 30 | **30pt** |
| "4.2 M€" | 6 | 34.6 | 63.5 | 34.6 | 30 | **30pt** |
| "1 234 567 K€" | 12 | 34.6 | 32.5 | 32.5 | 30 | **30pt** |

Toutes les valeurs landent à 30pt single-line. **Wrap éliminé pour tous les cas, y compris longues valeurs avec chars larges "M€" / "K€".**

L'uniformité collective (C16 `_apply_uniform_font_size_to_repeats`) continue de fonctionner : MIN des 3 sz observées appliqué à tous → cohérence visuelle préservée.

## 4. Validation visuelle

### `examples/test_migration_cloud.pptx` slide 6 (TCO trajectoire)

```
=== Slide 6: positions absolues per KPI card ===
  card #1: V '4.2 M€'  @ (0.40, 1.73) 2.90×0.48" | L 'TCO 2025'    @ (0.40, 2.25) 2.90×0.35"
  card #2: V '3.1 M€'  @ (0.40, 2.91) 2.90×0.48" | L 'Cible 2028'  @ (0.40, 3.43) 2.90×0.35"
  card #3: V '1.1 M€'  @ (0.40, 4.09) 2.90×0.48" | L 'Économie/an' @ (0.40, 4.61) 2.90×0.35"
```

- **Disposition** : ✅ verticale (VALUE T=1.73", LABEL T=2.25" pour card 1)
- **Taille de police value** : ✅ **30pt** uniforme (vs 24pt floor + wrap C20)
- **Chevauchement value/label** : ✅ aucun (V_bottom=2.21" < L_top=2.25")
- **Largeur value/label** : ✅ identique 2.90"
- **Stack vertical** : ✅ card 1 1.73-2.60", card 2 2.91-3.78", card 3 4.09-4.96"

### `examples/cloud_computing_2026_v3.pptx`

V3 n'a **pas** de slide `kpi_with_chart` — tous les KPI y sont sur canvas_blank. Régénération OK (rendu inchangé pour les autres layouts). Le brief mentionnait V3 slide 6 par confusion ; la vraie slide TCO `kpi_with_chart` est dans `test_migration_cloud`.

## 5. Tests

```
======================== 77 passed, 1 skipped in 5.00s =========================
```

**Nouveau** :
| Test | Vérifie |
|---|---|
| `test_kpi_vertical_layout` | 3 cards : `value.bottom ≤ label.top`, même width, même x — pas de chevauchement, alignement vertical strict |

**Ajustés** (mêmes seuils, doc mise à jour) :
- `test_kpi_value_xxl_default` : commentaire updated (shape 2.90"×0.48" au lieu de 1.00"×0.47"). Seuil `>= 3000` (30pt) inchangé — value zone H reste similaire (0.48").
- `test_kpi_with_chart_value_fits_width` : `shape_width_pt` corrigé `1.00" × 72 → 2.90" × 72` pour matcher le nouveau shape. Le seuil rend maintenant beaucoup plus de marge (208pt vs 72pt), donc le test passe trivialement.

Aucune régression sur les 73 autres tests.

## 6. Friction et arbitrages

1. **Hauteur de card inchangée (0.87")** : ne pas augmenter pour ne pas casser le stacking vertical (3 cards × 0.87" + 2 gaps × 0.15" = 2.91" → laisse de la marge sous le chart à 3.00" tall). Conséquence : value zone limitée à 0.48" → max 30pt (pas 60pt XXL). Compromis assumé : XXL "vertical" à 30pt avec value claire au-dessus du label, vs XXL horizontal 60pt qui forçait wrap des valeurs longues. 30pt vertical est largement plus lisible.

2. **Couleurs préservées** : label reste orange (`F26622`), value reste navy (`14163C`). Cette convention est inversée par rapport à canvas_blank `kpi_card` (orange value, navy label), mais reflète le branding original du template. Hors scope C21 d'harmoniser.

3. **Taille label inchangée (18pt)** : le brief suggérait 10pt comme dans canvas_blank, mais le shape label (W=2.90" × H=0.35") accommode confortablement le 18pt (0.25" line height). 10pt aurait été perdu sur cette card de 2.90" de large. 18pt préservé pour la cohérence visuelle.

4. **Aucune modification du moteur** : C19/C20 ont rendu le code totalement dimension-aware. Changer le template **suffit** pour propager la nouvelle géométrie. Beau payoff de l'architecture.

## 7. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/assets/AOSIS_template.before-chantier21.pptx` | **backup** (810 KB) |
| `aosis-deck-builder/assets/AOSIS_template.pptx` | **modifié** (slide 6 disposition verticale) |
| `aosis-deck-builder/scripts/template_engine.before-chantier21.py` | **backup** (no engine changes needed) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+1 test, 2 seuils ajustés) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 21) |
| `chantier21_report.md` | **créé** (ce fichier) |
| `aosis-deck-builder.skill` | **regénéré** (bundle à jour) |
| `examples/cloud_computing_2026_v3.pptx` | **régénéré** (1.06 MB) |
| `examples/test_migration_cloud.pptx` | **régénéré** (980 KB) — slide 6 TCO en mode vertical |

Aucun autre layout touché. Helpers `_compute_max_kpi_font_size` et `_apply_uniform_font_size_to_repeats` non modifiés.

---

**Statut final** : ✅ Chantier 21 **livré sans régression**. 77/78 tests verts. Disposition verticale active sur kpi_with_chart, KPI longs ("4.2 M€" et plus) rendus en 30pt single-line propre — wrap définitivement éliminé.
