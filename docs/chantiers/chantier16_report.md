# Chantier 16 — Fix bugs visuels : `closing_diagonal` titre long + uniformité REPEAT_ITEM

**Date** : 2026-05-20
**Périmètre** : 2 bugs visuels remontés sur le deck `cloud_computing_2026.pptx`.

## TL;DR

| Fix | Statut |
|---|---|
| `closing_diagonal` titre long → césure dans les mots + débordement sur le bloc auteur | ✅ auto-shrink agressif 60→40→36pt |
| `roadmap_styled` (et 6 autres layouts) tailles inégales entre items | ✅ helper d'uniformisation `_apply_uniform_font_size_to_repeats` |

**Tests** : **63 passed, 1 skipped** (6 nouveaux tests, 0 régression).

## 1. Inspection `closing_diagonal`

Lecture XML de la slide 16 (`closing_diagonal`) dans `AOSIS_template.pptx` :

| Shape | Position (L, T) | Taille (W × H) | Typo | Notes |
|---|---|---|---|---|
| `{{IMAGE}}` | 4.21″, -0.01″ | 5.80″ × 5.63″ | — | Image diagonale avec custGeom |
| `{{TITLE}}` | 0.50″, 1.23″ | **3.71″** × 1.43″ | sz=6000 b=1 | `noAutofit`, wrap='square', vertOverflow='overflow' |
| `{{QUESTION}}` | 0.58″, 2.25″ | 4.03″ × 0.42″ | sz=1600 | — |
| `{{AUTHOR_NAME}}` | 0.51″, 4.22″ | 3.71″ × 0.34″ | sz=1400 | — |
| `{{AUTHOR_EMAIL}}` | 0.50″, 4.49″ | 3.71″ × 0.34″ | sz=1400 | — |
| `{{AUTHOR_PHONE}}` | 0.50″, 4.77″ | 3.71″ × 0.34″ | sz=1400 | — |
| `website` | 0.50″, 5.05″ | 3.71″ × 0.34″ | sz=1400 | Texte fixe `www.aosis.net` |

**Diagnostic** :
- Le `{{TITLE}}` ne fait que **3.71″** de large (le reste de la slide est occupé par l'image diagonale)
- À 60pt bold (sz=6000), un mot de 11 caractères comme "trajectoire" occupe ≈ 4.61″ → ne tient pas
- `noAutofit` + `vertOverflow="overflow"` → PowerPoint casse au milieu des mots ET déborde verticalement
- Le débordement vertical depuis y=1.23″ atteint le bloc auteur (commence à y=4.22″) si plusieurs lignes empilées
- **Pas d'overlap horizontal mathématique** : bloc auteur right=4.21″ = left image=4.21″, juste collé

## 2. Fix 1 — `_shrink_closing_title`

Nouvelle fonction appelée en fin de pipeline quand `layout_name == 'closing_diagonal'`.

**Algorithme** :
```python
target_emu = shape_width × 0.95            # 5% safety margin
char_emu = (sz/100) × factor × 12700       # factor = 0.55 (bold) ou 0.50
word_w = len(longest_word) × char_emu

while sz > 3600 and word_w(sz) > target_emu:
    sz -= 400                              # paliers de 4pt
```

Aussi force `bodyPr@wrap="square"` pour garantir le break sur les espaces.

**Résultats observés** :
| Texte | Mot le plus long | sz initial | sz final |
|---|---|---:|---:|
| "MERCI" | "MERCI" (5 chars) | 6000 | 6000 (no shrink) |
| "Discutons de votre trajectoire vers le cloud en toute sérénité" | "trajectoire" (11) | 6000 | **4000** (40pt) |
| "Échanges" | "Échanges" (8) | 6000 | 5200 (52pt) |
| "Décommissionnement définitif" | "Décommissionnement" (18) | 6000 | 3600 (36pt, floor) |

Au-delà du floor 36pt + 18-char word : le texte continue de déborder (wrap multi-ligne) mais la lisibilité reste acceptable. Si l'utilisateur a besoin de mots encore plus longs, il faut ajuster le template (élargir la zone titre).

## 3. Inspection bug `roadmap_styled`

Avant ce chantier, sur un deck à 5 milestones :
```
copy 0  {{ITEM_MILESTONE}}  sz=1800  text="Audit"                       (no shrink — court)
copy 1  {{ITEM_MILESTONE}}  sz=1400  text="Cadrage cible architecture" (shrunk 1 step)
copy 2  {{ITEM_MILESTONE}}  sz=1000  text="Décommissionnement complet..." (shrunk to floor)
copy 3  {{ITEM_MILESTONE}}  sz=1600  text="Validation"                  (shrunk 1 step)
copy 4  {{ITEM_MILESTONE}}  sz=1800  text="Bascule"                     (no shrink)
```

5 tailles différentes — non-uniforme visuellement.

## 4. Fix 2 — `_apply_uniform_font_size_to_repeats`

Nouveau helper générique appelé en fin de `_process_repeat_items` selon une table per-layout.

**Algorithme** :
1. Parcourir tous les `<p:grpSp>` (copies REPEAT_ITEM) de la slide
2. Pour chaque sub-placeholder ciblé (ex: `{{ITEM_MILESTONE}}`) : collecter le `sz` du `<a:rPr>` de chaque copie
3. Calculer le minimum observé
4. Appliquer ce minimum à toutes les copies

**Table per-layout** :
```python
_UNIFORM_REPEAT_SHAPES = {
    'roadmap_styled':   ['{{ITEM_DATE}}', '{{ITEM_MILESTONE}}'],
    'next_steps':       ['{{ITEM_ACTION}}', '{{ITEM_OWNER}}', '{{ITEM_DATE}}'],
    'kpi_with_chart':   ['{{KPI_VALUE}}', '{{KPI_LABEL}}'],
    'agenda_diagonal':  ['{{ITEM_TITLE}}'],
    'process_steps':    ['{{ITEM_TITLE}}', '{{ITEM_TEXT}}'],
    'framework_3cards': ['{{ITEM_TITLE}}', '{{ITEM_BULLETS}}'],
    'text_dense_3cols': ['{{ITEM_TITLE}}', '{{ITEM_TEXT}}'],
}
```

**Résultats post-fix** sur le même cas roadmap :
```
copy 0  {{ITEM_MILESTONE}}  sz=1000  text="Audit"
copy 1  {{ITEM_MILESTONE}}  sz=1000  text="Cadrage cible architecture"
copy 2  {{ITEM_MILESTONE}}  sz=1000  text="Décommissionnement complet..."
copy 3  {{ITEM_MILESTONE}}  sz=1000  text="Validation"
copy 4  {{ITEM_MILESTONE}}  sz=1000  text="Bascule"
```

Toutes les copies à sz=1000 (10pt) — uniforme, déterminé par le milestone le plus long qui a forcé le shrink le plus agressif.

## 5. Avant / Après sur les 7 layouts impactés

| Layout | Shape harmonisé | Avant | Après |
|---|---|---|---|
| `roadmap_styled` | `{{ITEM_DATE}}`, `{{ITEM_MILESTONE}}` | 4-5 sizes mélangées | 1 size uniforme |
| `next_steps` | `{{ITEM_ACTION}}`, `{{ITEM_OWNER}}`, `{{ITEM_DATE}}` | dates à 14/12/10pt | dates uniformes |
| `kpi_with_chart` | `{{KPI_VALUE}}`, `{{KPI_LABEL}}` | values 28/22/20pt | values uniformes |
| `agenda_diagonal` | `{{ITEM_TITLE}}` | mélange si items mixtes | uniforme |
| `process_steps` | `{{ITEM_TITLE}}`, `{{ITEM_TEXT}}` | shrinks variables | uniforme |
| `framework_3cards` | `{{ITEM_TITLE}}`, `{{ITEM_BULLETS}}` | shrinks variables | uniforme |
| `text_dense_3cols` | `{{ITEM_TITLE}}`, `{{ITEM_TEXT}}` | shrinks variables | uniforme |

## 6. Validation visuelle — `examples/cloud_computing_2026.pptx` régénéré

```
OK — wrote examples/cloud_computing_2026.pptx (1,020,889 bytes)
```

Inspection XML post-régénération :

**Slide 12 (`roadmap_styled`) — 5 milestones du plan TechnoLog** :
```
sz=1000  Cadrage — Landing Zone, FinOps
sz=1000  Quick wins — 10-15 apps non critiques
sz=1000  Apps support — 15-20 applications
sz=1000  Apps critiques — ERP, CRM, métier
sz=1000  Optimisation — FinOps avancé, décom
```
→ uniforme ✓ (5 × sz=1000)

**Slide 17 (`closing_diagonal`)** :
```
sz=4000  text="Discutons de votre trajectoire"
```
→ shrink de 60pt → 40pt ✓ (le mot "trajectoire" force la limite, 5 paliers parcourus)

Le titre tient maintenant sur ≤ 2 lignes dans la zone 3.71″ × 1.43″, sans déborder sur le bloc auteur.

## 7. Tests

```
======================== 63 passed, 1 skipped in 4.78s =========================
```

6 nouveaux tests :
| Test | Vérifie |
|---|---|
| `test_closing_diagonal_long_title` | Titre long → sz ≤ 4400 et ≥ 3600 + bloc auteur reste dans la slide |
| `test_closing_diagonal_short_title_not_shrunk` | "MERCI" garde son 60pt original |
| `test_roadmap_uniform_font_size` | 5 milestones → toutes mêmes sz (milestone + date) |
| `test_next_steps_uniform_dates` | 4 actions → dates toutes mêmes sz |
| `test_kpi_with_chart_uniform_values` | 3 KPI dont 1 long → values toutes mêmes sz |
| `test_agenda_uniform_items` | 4 items dont 1 long → titles tous mêmes sz |

Aucune régression sur les 57 tests précédents.

## 8. Frictions résiduelles / suite

1. **Closing : mot ultra-long > floor 36pt** : si l'utilisateur passe un titre avec un mot de 18+ chars (ex: "Décommissionnement"), la shrink atteint le floor 36pt mais le texte peut encore déborder horizontalement. Solution : élargir la zone titre du template (passer de 3.71″ à ~5″) — modification template non comprise dans ce chantier (périmètre strict).
2. **Uniformité = "minimum-vote"** : la plus petite taille observée gagne. Conséquence : si un seul item est long, TOUS les autres rétrécissent à son niveau. Acceptable pour la cohérence visuelle mais peut donner des slides "petites" si un seul label déborde. Recommandation éditoriale : raccourcir les milestones les plus longs (ou mieux : éviter le débordement à la source).
3. **`comparison_2cols` et `comparison_before_after` non couverts** : ils n'ont pas d'auto-shrink agressif aujourd'hui (texte généralement court). Si besoin futur, les ajouter à `_UNIFORM_REPEAT_SHAPES`.

## 9. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+95 lignes : `_UNIFORM_REPEAT_SHAPES`, `_apply_uniform_font_size_to_repeats`, `_shrink_closing_title`, dispatch) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+6 tests + helper `_collect_sz_for_shape_name`) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 16) |
| `chantier16_report.md` | **créé** (ce fichier) |
| `examples/cloud_computing_2026.pptx` | **régénéré** (1.02 MB) avec les 2 fixes appliqués |

`AOSIS_template.pptx` **non modifié** comme demandé. Aucune autre logique touchée.

---

**Statut final** : ✅ Chantier 16 **livré sans régression**. 63/64 tests verts, 2 fixes visuels appliqués, deck cloud computing régénéré.
