# Chantier 1 — Fix bug `roadmap` : labels qui débordent hors slide

> Date : 2026-05-13 · Scope strict : `add_roadmap` dans [`aosis-deck-builder/scripts/build_deck.py`](aosis-deck-builder/scripts/build_deck.py). Aucun autre fichier du skill touché.

---

## 1. Approche retenue : **Approche 2** — réduction de l'amplitude horizontale du tracé

### Décision

Le tracé original utilise `line_left = 0.8"` / `line_right = 9.2"` (span = 8.4"). Les labels (et surtout le bloc `detail` de 2.3" de large) centrés sur les marqueurs extrêmes débordaient.

**Nouvelle plage** : `line_left = 1.2"`, `line_right = 8.8"`, span = 7.6".

### Raisonnement quantitatif (et pourquoi pas `0.5"` / `9.5"` comme suggéré)

Le textbox `detail` a une largeur de **2.3"** (`label_w` 1.9" + un débord latéral `Inches(0.4)`) et reste **centré sur la position du marqueur**. Pour qu'il ne déborde pas :

```
marker_x − 1.15"  ≥  0      ⇒  marker_x  ≥  1.15"
marker_x + 1.15"  ≤  10"    ⇒  marker_x  ≤  8.85"
```

Avec le `0.5"`/`9.5"` proposé dans l'énoncé, le premier marqueur à 0.5" aurait toujours un `detail` qui sort à −0.65" — l'overflow aurait juste été divisé par deux, pas supprimé. La valeur correcte calculée est `[1.15", 8.85"]`. J'ai retenu **`[1.2", 8.8"]`** pour conserver 0.05" de marge de sécurité contre d'éventuels arrondis EMU.

### Pourquoi pas l'approche 1 (clamp asymétrique)

L'approche 1 aurait gardé `line_left = 0.8"` et clampé les labels des milestones extrêmes à `max(0, ...)` / `min(10−w, ...)`. Conséquence : les labels du **premier** et du **dernier** milestone auraient été visuellement décalés vers le bord, perdant la symétrie centre/centre. Pour 5 milestones, ce sont 2 labels sur 5 — soit 40 % — qui auraient une règle de positionnement différente des autres. Inacceptable pour un rendu consulting top-tier.

L'approche 2 préserve **une seule règle de placement** (label centré sur le marqueur, toujours) au prix d'un tracé légèrement plus court (7.6" vs 8.4", soit −9 %).

### Commit dans le code

Commentaire posé au-dessus de la fonction [`add_roadmap`](aosis-deck-builder/scripts/build_deck.py) :

```python
# Chantier 1 (fix overflow) — approche 2 : amplitude horizontale réduite.
# Contrainte limitante = textbox `detail` de largeur 2.3" centrée sur le marker
# (label_w 1.9 + Inches(0.4) de débord lat.). Pour qu'elle reste dans [0, 10"],
# il faut marker_x ∈ [1.15", 8.85"]. On prend [1.2", 8.8"] (0.05" de cushion).
# La symétrie centre/centre des labels est préservée — pas de clamp asymétrique.
```

Modification réelle (2 lignes) :

```diff
-    line_left = Inches(0.8)
-    line_right = Inches(9.2)
+    line_left = Inches(1.2)
+    line_right = Inches(8.8)
```

Le reste de la fonction (calcul de `x` à partir de `line_left + span * i / (n-1)`, dessin des diamants, alternance label au-dessus/en-dessous) **n'a pas changé**.

---

## 2. Avant / Après — positions des 4 textboxes les plus extrêmes

Mesures faites sur les `.pptx` réellement générés via [`tests/check_bounds.py`](aosis-deck-builder/tests/check_bounds.py). Limites de slide : **[0, 10"] × [0, 5.625"]**.

### Cas n=3 milestones — [`tests/fixtures/roadmap_3.json`](aosis-deck-builder/tests/fixtures/roadmap_3.json)

| Extrême | Avant fix | Après fix | Dans bornes ? |
|---|---|---|---|
| Most-left | `TextBox 6` left = **−0.350"** ❌ | `TextBox 6` left = **0.050"** ✅ | OK |
| Most-top | `Title 1` top = 0.188" | `Title 1` top = 0.188" | OK (inchangé) |
| Most-right | `TextBox 14` right = **10.350"** ❌ | `TextBox 14` right = **9.950"** ✅ | OK |
| Most-bottom | `TextBox 10` bottom = 4.950" | `TextBox 10` bottom = 4.950" | OK (inchangé) |

Violations totales : **6 → 0**.

### Cas n=4 milestones — [`tests/fixtures/roadmap_4.json`](aosis-deck-builder/tests/fixtures/roadmap_4.json)

| Extrême | Avant fix | Après fix | Dans bornes ? |
|---|---|---|---|
| Most-left | `TextBox 6` left = **−0.350"** ❌ | `TextBox 6` left = **0.050"** ✅ | OK |
| Most-top | `Title 1` top = 0.188" | `Title 1` top = 0.188" | OK |
| Most-right | `TextBox 18` right = **10.350"** ❌ | `TextBox 18` right = **9.950"** ✅ | OK |
| Most-bottom | `TextBox 10` bottom = 4.950" | `TextBox 10` bottom = 4.950" | OK |

Violations totales : **6 → 0**.

### Cas n=5 milestones — [`tests/fixtures/roadmap_5.json`](aosis-deck-builder/tests/fixtures/roadmap_5.json) *(cas de l'audit initial)*

| Extrême | Avant fix | Après fix | Dans bornes ? |
|---|---|---|---|
| Most-left | `TextBox 6` left = **−0.350"** ❌ | `TextBox 6` left = **0.050"** ✅ | OK |
| Most-top | `Title 1` top = 0.188" | `Title 1` top = 0.188" | OK |
| Most-right | `TextBox 22` right = **10.350"** ❌ | `TextBox 22` right = **9.950"** ✅ | OK |
| Most-bottom | `TextBox 10` bottom = 4.950" | `TextBox 10` bottom = 4.950" | OK |

Violations totales : **6 → 0**.

### Cas n=6 milestones — [`tests/fixtures/roadmap_6.json`](aosis-deck-builder/tests/fixtures/roadmap_6.json)

| Extrême | Avant fix | Après fix | Dans bornes ? |
|---|---|---|---|
| Most-left | `TextBox 6` left = **−0.350"** ❌ | `TextBox 6` left = **0.050"** ✅ | OK |
| Most-top | `Title 1` top = 0.188" | `Title 1` top = 0.188" | OK |
| Most-right | `TextBox 26` right = **10.350"** ❌ | `TextBox 26` right = **9.950"** ✅ | OK |
| Most-bottom | `TextBox 10` bottom = 4.950" | `TextBox 10` bottom = 4.950" | OK |

Violations totales : **6 → 0**.

### Synthèse

| n | Violations avant | Violations après | Marge gauche après | Marge droite après |
|---|---|---|---|---|
| 3 | 6 | **0** | 0.050" | 0.050" |
| 4 | 6 | **0** | 0.050" | 0.050" |
| 5 | 6 | **0** | 0.050" | 0.050" |
| 6 | 6 | **0** | 0.050" | 0.050" |

Les valeurs `0.050"` correspondent exactement au cushion calculé (`1.2 − 1.15 = 0.05`). Cohérent avec le raisonnement.

---

## 3. Confirmation visuelle (rendu PNG)

LibreOffice / `soffice` / `pdftoppm` **ne sont pas installables** dans cet environnement WSL (apt restreint, ensurepip indisponible). À la place, j'ai utilisé **PowerPoint Windows** (déjà installé côté WSL `/mnt/c/`) automatisé en COM via PowerShell — même technique que celle utilisée pour [`Ressources/template_rh_inventory.md`](Ressources/template_rh_inventory.md).

Les 8 PNG (4 cas × before/after) sont dans [`aosis-deck-builder/tests/out_png/`](aosis-deck-builder/tests/out_png/).

### Cas n=5 — illustration du défaut résolu

**Avant** ([roadmap_5_before.png](chantier1_assets/roadmap_5_before.png)) — le détail du 5ᵉ milestone est tronqué à droite ("Plateforme historique éteint" sans le "e" final) et le 1ᵉʳ détail colle à `x=0` :

![Avant](chantier1_assets/roadmap_5_before.png)

**Après** ([roadmap_5_after.png](chantier1_assets/roadmap_5_after.png)) — le texte "Plateforme historique éteinte" est complet, le 1ᵉʳ détail a sa marge gauche, le tracé est mécaniquement raccourci de chaque côté :

![Après](chantier1_assets/roadmap_5_after.png)

### Cas n=6 — vérification que ce n'est pas serré

![n=6 après](chantier1_assets/roadmap_6_after.png)

Six marqueurs sur 7.6" → step = 1.52". L'alternance des labels au-dessus / en-dessous (déjà présente dans le code original) maintient un écart vertical entre labels voisins. Visuellement aéré, lisible. **Pas d'effet de bord visible**.

---

## 4. Effets de bord constatés

| Effet | Mesure | Verdict |
|---|---|---|
| Tracé plus court | 8.4" → 7.6" (−9 %) | Discret visuellement, acceptable |
| Marqueurs plus serrés | step n=6 : 1.68" → 1.52" (−10 %) | Toujours lisibles (image n=6 après confirme), alternance label haut/bas suffit |
| Marqueurs n=2 | étaient à `0.8" / 9.2"`, désormais à `1.2" / 8.8"` | Le tracé est plus centré, sans inconvénient |
| Détails adjacents même côté (n=5) | step de 2.1" → 1.9" entre milestones same-side ; les détails (2.3") seraient maintenant en chevauchement | **Non observé** car alternance haut/bas : adjacents same-side restent à 2×step = 3.8", largement supérieur à 2.3" |
| Alignement des marges du body slide | Le tracé `1.2" → 8.8"` est moins large que le footer/header de la slide qui s'étend de 0 à 10" | Sans incidence — la roadmap reste un dessin centré, le visuel reste équilibré |

Aucun effet de bord bloquant. Le seul changement perceptible est le tracé légèrement plus court ; le bénéfice (zéro débordement, "éteinte" non tronqué) compense largement.

---

## 5. Livrables

| Livrable | Chemin |
|---|---|
| Code modifié | [`aosis-deck-builder/scripts/build_deck.py`](aosis-deck-builder/scripts/build_deck.py) (fonction `add_roadmap`, lignes ~736-810) |
| Fixture 3 milestones | [`aosis-deck-builder/tests/fixtures/roadmap_3.json`](aosis-deck-builder/tests/fixtures/roadmap_3.json) |
| Fixture 4 milestones | [`aosis-deck-builder/tests/fixtures/roadmap_4.json`](aosis-deck-builder/tests/fixtures/roadmap_4.json) |
| Fixture 5 milestones | [`aosis-deck-builder/tests/fixtures/roadmap_5.json`](aosis-deck-builder/tests/fixtures/roadmap_5.json) |
| Fixture 6 milestones | [`aosis-deck-builder/tests/fixtures/roadmap_6.json`](aosis-deck-builder/tests/fixtures/roadmap_6.json) |
| Script de vérification géométrique | [`aosis-deck-builder/tests/check_bounds.py`](aosis-deck-builder/tests/check_bounds.py) |
| Decks générés (after) | [`aosis-deck-builder/tests/out/roadmap_{3,4,5,6}.pptx`](aosis-deck-builder/tests/out/) |
| Decks générés (before, pour comparaison) | [`aosis-deck-builder/tests/out_before/`](aosis-deck-builder/tests/out_before/) |
| PNG before/after | [`aosis-deck-builder/tests/out_png/`](aosis-deck-builder/tests/out_png/) |

### Reproduire les tests

```bash
cd aosis-deck-builder
# Générer les 4 decks
for n in 3 4 5 6; do
  python scripts/build_deck.py tests/fixtures/roadmap_${n}.json tests/out/roadmap_${n}.pptx
done
# Vérifier
python tests/check_bounds.py tests/out/roadmap_*.pptx
# → Code de sortie 0, "all within bounds" pour chaque fichier
```

---

## 6. Périmètre strict respecté

- ✅ Seule la fonction `add_roadmap` a été modifiée (2 lignes de valeurs + un commentaire en bloc).
- ✅ `SKILL.md` non touché.
- ✅ Template `assets/AOSIS_template.pptx` non touché.
- ✅ Aucune autre fonction `add_*` modifiée.
- ✅ Aucun import ajouté.
- ➕ Ajout d'infrastructure de test sous `tests/` (fixtures + script de vérification + outputs). Cohérent avec la recommandation de l'audit ("Top 3 risques techniques #1 : aucun test, aucune fixture") et nécessaire à la validation du chantier. Si vous préférez que les fichiers `tests/` soient déplacés hors du bundle skill (par exemple à la racine du projet), c'est trivial.
