# Chantier 14 — `canvas_blank` freeform composition

**Date** : 2026-05-20
**Périmètre** : Transformer `canvas_blank` d'un canevas vide en un moteur de composition freeform accepant N blocs typés et les disposant automatiquement sur une grille consulting.

## TL;DR

- ✅ Nouveau moteur `_render_canvas_blank_freeform()` ajouté à `template_engine.py` (~400 lignes), 6 types de blocs (`kpi_card`, `bullets`, `text`, `image`, `chart`, `quote`).
- ✅ Grille automatique 1/2/3/4/5/6 blocs + asymétrique pour image/chart isolé.
- ✅ Header band (eyebrow + title + takeaway + source) + validation amont (limites de longueur, troncature à 6 blocs).
- ✅ **51 passed, 1 skipped** (5 nouveaux tests).
- ✅ Deck showcase 8 slides livré : `examples/test_canvas_blank_showcase.pptx` (815 KB, 1.5 s à générer).
- ✅ Documentation : fiche layouts.md enrichie + section dédiée dans json-schema.md.

## Architecture

```
render_template_slide(prs, exhibits_path, "canvas_blank", spec)
    ↓ (pipeline standard inchangé)
    if layout_name == 'canvas_blank' and spec.get('blocks'):
        _render_canvas_blank_freeform(slide, spec)
            ↓
            1. Remove default {{TITLE}} placeholder (sera repositionné)
            2. _cb_add_eyebrow / _cb_add_title / _cb_add_takeaway / _cb_add_source
            3. _cb_compute_block_rects(blocks, area) → grid layout
            4. _cb_render_block × N → kpi_card / bullets / text / image / chart / quote
```

Le moteur est **non-invasif** : si le spec ne contient pas `blocks`, le comportement legacy (titre seul) est préservé. Tests existants ne sont pas affectés (`test_no_diagonal_overlay_on_canvas_blank` reste vert).

## Coordonnées de mise en page

| Zone | y_top | hauteur | Notes |
|---|---:|---:|---|
| eyebrow | 0.30" | 0.25" | 10pt orange UPPERCASE |
| title | 0.55" | 0.70" | 24pt navy bold |
| takeaway (bandeau orange clair `#FDF1EA`) | 1.30" | 0.40" | 12pt orange italic, optionnel |
| blocks (avec takeaway) | 1.90" | 3.20" | grille |
| blocks (sans takeaway) | 1.30" | 3.80" | grille élargie |
| source | 5.10" | 0.25" | 8pt italic gris |

Marges horizontales : 0.40" gauche/droite → largeur utile 9.20".

## Logique de grille

```python
def _cb_compute_block_rects(blocks, base_left, base_top, area_w, area_h):
    n = len(blocks)
    gap = 0.15"
    # Asymétrique : 1 visuel (image/chart) parmi 2+ blocs → moitié droite (45%)
    visual_indices = [i for i, b in enumerate(blocks) if b['type'] in ('image','chart')]
    if n >= 2 and len(visual_indices) == 1:
        # left half stacked, right half visual
        ...
    if n == 1: 1×1
    elif n == 2: 1×2
    elif n == 3: 1×3
    elif n == 4: 2×2
    elif n == 5: 3-top + 2-bottom (asymétrique)
    else: 3×2 (6 max)
```

## Renderers par type

| Type | Implémentation | Particularités |
|---|---|---|
| `kpi_card` | textbox value (36/28/22pt selon longueur, orange/navy/green/red) + textbox label (10pt navy UPPERCASE) | Adaptive font size |
| `bullets` | textbox multi-runs (puce orange • + texte navy) | Max 5 items |
| `text` | textbox 12pt navy word-wrap | — |
| `image` | `image_engine.fetch_image_for_slide` ou path local | Pexels → Picsum |
| `chart` | `chart_engine.render_chart_to_png` | 8 types (réutilise le moteur du chantier 8) |
| `quote` | textbox 14pt italic navy avec guillemets « » + attribution UPPERCASE orange | — |

## Showcase deck — 8 slides

Le deck `examples/test_canvas_blank_showcase.pptx` (815 KB) illustre chaque composition. Structure XML vérifiée :

| Slide | Composition | Shapes générées |
|---:|---|---|
| 1 | 1 block texte | 4 textboxes (eyebrow + title + source + texte plein cadre) |
| 2 | 4 KPI cards (grille 2×2) + takeaway | 13 textboxes (incl. 8 KPI = value+label×4) + 1 AUTO_SHAPE (bandeau takeaway) |
| 3 | bullets + image (asymétrique) | 3 textboxes + 1 PICTURE (image Pexels à droite) |
| 4 | 2 KPI + 1 chart (3 blocs avec visuel asymétrique) + takeaway | 8 textboxes + 1 PICTURE (chart matplotlib) + 1 AUTO_SHAPE |
| 5 | 6 KPI cards (grille 3×2) | 15 textboxes (12 KPI + 3 header) |
| 6 | 1 quote + 1 image (asymétrique) | 4 textboxes (incl. quote + attribution) + 1 PICTURE |
| 7 | 3 bullets + 1 chart + takeaway | 5 textboxes + 1 PICTURE (bar chart) + 1 AUTO_SHAPE |
| 8 | 5 blocs mixtes (3 KPI + 1 bullets + 1 text) | 13 textboxes + 1 AUTO_SHAPE (takeaway) |

Rendu visuel à valider côté utilisateur (l'agent n'a pas accès à PowerPoint/soffice pour capture d'écran). Tests structurels XML confirment la conformité aux specs.

## Validation des contenus

```
canvas_blank: 8 blocks > 6, truncating to first 6                # test_canvas_blank_truncates_at_6_blocks
canvas_blank bullets block: 6 items > 5, truncating              # implicite si > 5 bullets
canvas_blank: title length 137 exceeds 120 (will likely wrap)    # warning soft
canvas_blank: takeaway length 195 exceeds 180 (will likely wrap) # warning soft
```

Warnings stderr → l'utilisateur peut les filtrer ou les corriger. La génération n'échoue pas pour autant.

## Respect de la charte (test_canvas_blank_respects_palette)

Inspection XML d'une slide générée : sur les ~6 runs créés (eyebrow + title + KPI value + KPI label), **tous portent `<a:latin typeface="Arial"/>`** et **les couleurs sont dans la palette brand** (`#14163C` navy, `#F26622` orange, `#4A4D6B` gray). Aucun fallback Calibri / couleur ad-hoc.

## Tests

```
======================== 51 passed, 1 skipped in 5.82s =========================
```

5 nouveaux :
| Test | Vérifie |
|---|---|
| `test_canvas_blank_with_4_kpi_cards` | 4 KPI → values + labels (uppercased) présents |
| `test_canvas_blank_with_text_and_image` | text + image avec mock → 1 PICTURE + text préservé |
| `test_canvas_blank_with_chart` | chart bar → 1 PICTURE matplotlib insérée |
| `test_canvas_blank_respects_palette` | ≥ 3 runs Arial + ≥ 3 runs aux couleurs brand |
| `test_canvas_blank_truncates_at_6_blocks` | 8 blocks → 6 rendus, warning stderr `truncating to first 6` |

Anciens 46 tests : ✓ aucune régression.

## Frictions / suite

1. **Pas de mode "card avec icône"** dans `kpi_card` — si l'utilisateur veut une icône Iconify devant le chiffre, ajouter un block `kpi_card_icon` au Chantier 15. Aujourd'hui : seuls les 4 colors prédéfinis (orange/navy/green/red).
2. **Pas de validation cross-block** : par exemple, si l'utilisateur met 2 charts (assymétrique non géré), les charts ne sont pas mis côte à côte intelligemment. Simple fallback : grille standard 1×2. À enrichir si besoin.
3. **Latence images** : si plusieurs blocks `image` dans le même deck, chaque fetch est séquentiel (1-2 s par photo Pexels). Cache disque + parallélisme = candidat futur.
4. **Mode hybride** : pour 7+ blocks, on tronque silencieusement à 6. Alternative future : auto-pagination sur 2 slides (comme `agenda_diagonal`).

## Suggestion non implémentée

`canvas_blank` accepte actuellement `blocks` à plat sans groupes. Pour des slides plus complexes, on pourrait introduire des **sections** : `{type: "row", blocks: [{...}, {...}]}` pour permettre des layouts récursifs. Hors-scope ici, à discuter pour un Chantier 15+.

## Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+~400 lignes : freeform engine, grid, renderers) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+5 tests) |
| `aosis-deck-builder/references/layouts.md` | **modifié** (fiche `canvas_blank` réécrite, +blocs supportés + grille + exemples) |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (nouvelle section "`canvas_blank` freeform composition") |
| `CHANGELOG.md` | **modifié** (entrée Chantier 14) |
| `chantier14_report.md` | **créé** (ce fichier) |
| `examples/test_canvas_blank_showcase.json` | **créé** (8 slides showcase) |
| `examples/test_canvas_blank_showcase.pptx` | **créé** (815 KB, 1.5 s génération) |

`AOSIS_template.pptx` **non modifié** comme demandé.

---

**Statut final** : ✅ Chantier 14 **livré sans régression**. 51/52 tests verts (1 skip soffice pré-existant), nouveau moteur freeform fonctionnel, showcase deck à valider visuellement.
