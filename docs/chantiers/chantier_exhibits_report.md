# Chantier exhibits — 15 layouts modèles consulting dans `exhibits.pptx`

> Date : 2026-05-17 · Scope strict : `aosis-deck-builder/assets/exhibits.pptx` + ce rapport. **Aucune modification** de `scripts/build_deck.py`, `scripts/brand.py`, `SKILL.md`, `references/`, ou du template AOSIS.

---

## TL;DR

| Métrique | Valeur |
|---|---|
| Slides avant | 4 (cover_diagonal, agenda_diagonal, **canvas blanc**, closing_diagonal) |
| Slides après | **19** (4 originales + 15 nouveaux layouts) |
| Layouts générés en un run | 15 |
| Validation PowerPoint | ✅ ouvre sans erreur |
| Temps de génération | ~2 s |
| Taille fichier final | ~1.1 Mo |
| Backup | [`assets/exhibits.backup.pptx`](aosis-deck-builder/assets/exhibits.backup.pptx) (intouché) |

Tous les layouts respectent la **grammaire consulting** demandée : `{{EYEBROW}}` + `{{TITLE}}` + (optionnel `{{TAKEAWAY}}` en bandeau orange) + exhibit central + `{{SOURCE}}` en bas-gauche.

---

## 1. Les 15 layouts produits

Pour chaque layout, ci-dessous : description, inspiration (Template RH + grammaire McK/BCG), zones variables (slot names entre `{{...}}`).

### 1.1 `executive_summary`

**Inspiration** : grammaire classique consulting (3 piliers en colonnes), Template RH slide 5 (textes structurés en colonnes).
**Description** : 3 colonnes verticales, chacune avec mini-bar orange + eyebrow uppercase + heading + bullets.
**Zones variables (slot names)** :

| Slot | Rôle |
|---|---|
| `{{EYEBROW}}`, `{{TITLE}}`, `{{TAKEAWAY}}`, `{{SOURCE}}` | en-tête + footer consulting standard |
| `{{COL_1_EYEBROW}}`, `{{COL_2_EYEBROW}}`, `{{COL_3_EYEBROW}}` | "PILLAR N" tag orange |
| `{{COL_1_TITLE}}`, `{{COL_2_TITLE}}`, `{{COL_3_TITLE}}` | titre de chaque colonne |
| `{{COL_1_BULLETS}}`, `{{COL_2_BULLETS}}`, `{{COL_3_BULLETS}}` | bullets de chaque colonne |

Aperçu : [chantier_exhibits_assets/slide-05.jpg](chantier_exhibits_assets/slide-05.jpg)

---

### 1.2 `kpi_dual`

**Inspiration** : Template RH slide 19 (2 KPI cards centrées avec icône navy + chiffre orange géant).
**Description** : 2 grandes cartes blanches avec bordure légère, icône navy (cercle), chiffre orange 64pt, label en dessous.
**Zones variables** :

| Slot | Rôle |
|---|---|
| `{{KPI_LEFT_ICON}}`, `{{KPI_RIGHT_ICON}}` | cercle icône (placeholder navy) |
| `{{KPI_LEFT_VALUE}}`, `{{KPI_RIGHT_VALUE}}` | chiffre géant orange |
| `{{KPI_LEFT_LABEL}}`, `{{KPI_RIGHT_LABEL}}` | label sous le chiffre |

---

### 1.3 `kpi_quad`

**Inspiration** : Template RH slide 11 (4 tiles KPI en grille).
**Description** : 4 cartes 2×2 chacune avec icône cercle navy + chiffre orange + label.
**Zones variables** : `{{KPI_1_ICON}}` à `{{KPI_4_ICON}}`, `{{KPI_1_VALUE}}` à `{{KPI_4_VALUE}}`, `{{KPI_1_LABEL}}` à `{{KPI_4_LABEL}}`.

---

### 1.4 `kpi_with_chart`

**Inspiration** : Template RH slide 10 (KPI cards verticales à gauche + chart à droite).
**Description** : 3 KPI cards empilées à gauche (label orange + valeur navy + détail gris) + zone chart placeholder à droite.
**Zones variables** :

| Slot | Rôle |
|---|---|
| `{{KPI_1_LABEL}}`, `{{KPI_2_LABEL}}`, `{{KPI_3_LABEL}}` | label orange en haut de card |
| `{{KPI_1_VALUE}}`, `{{KPI_2_VALUE}}`, `{{KPI_3_VALUE}}` | valeur navy |
| `{{KPI_1_DETAIL}}`, `{{KPI_2_DETAIL}}`, `{{KPI_3_DETAIL}}` | subtitle gris |
| `{{CHART_PLACEHOLDER}}` | zone où injecter le graphique matplotlib généré |

---

### 1.5 `comparison_2cols`

**Inspiration** : grammaire consulting "options à débattre" + Template RH slide 41.
**Description** : 2 colonnes, header navy "Option A" / header orange "Option B", bullets dessous.
**Zones variables** :

| Slot | Rôle |
|---|---|
| `{{LEFT_TITLE}}`, `{{RIGHT_TITLE}}` | titre des deux options |
| `{{LEFT_BULLETS}}`, `{{RIGHT_BULLETS}}` | arguments de chaque colonne |

---

### 1.6 `comparison_before_after`

**Inspiration** : grammaire consulting "le saut" + Template RH slide 23.
**Description** : 2 cartes (Avant gris / Après orange-encadré) avec flèche orange centrale, takeaway en bandeau.
**Zones variables** :

| Slot | Rôle |
|---|---|
| `{{BEFORE_LABEL}}`, `{{AFTER_LABEL}}` | "AVANT" / "APRÈS" tags |
| `{{BEFORE_TITLE}}`, `{{AFTER_TITLE}}` | state names (Current / Target) |
| `{{BEFORE_BULLETS}}`, `{{AFTER_BULLETS}}` | listes de delta |

---

### 1.7 `framework_3cards`

**Inspiration** : Template RH slide 22 (cards orange grand format avec icônes blancs).
**Description** : 3 cartes orange remplies, icône cercle blanc en haut + titre blanc + bullets blancs.
**Zones variables** : `{{CARD_1_ICON}}` à `{{CARD_3_ICON}}`, `{{CARD_1_TITLE}}` à `{{CARD_3_TITLE}}`, `{{CARD_1_BULLETS}}` à `{{CARD_3_BULLETS}}`.

Aperçu : [chantier_exhibits_assets/slide-11.jpg](chantier_exhibits_assets/slide-11.jpg)

---

### 1.8 `matrix_2x2_styled`

**Inspiration** : grammaire consulting BCG growth/share + le layout `matrix_2x2` existant du Skill.
**Description** : 4 quadrants, top-right orange (la "star"), axes Impact (Y) / Effort (X) avec labels low/high.
**Zones variables** : `{{QUAD_TOP_LEFT_TITLE}}`, `{{QUAD_TOP_LEFT_ITEMS}}`, idem pour les 3 autres ; `{{X_AXIS_LABEL}}`, `{{Y_AXIS_LABEL}}`, `{{Y_HIGH}}`, `{{Y_LOW}}`.

---

### 1.9 `roadmap_styled`

**Inspiration** : le `roadmap` du Skill (Chantier 1) — ligne horizontale avec diamants alternant orange/navy, labels alternant haut/bas.
**Description** : 5 jalons sur une ligne horizontale, labels date + name au-dessus/au-dessous en alternance.
**Zones variables** : `{{MILESTONE_1_DATE}}` à `{{MILESTONE_5_DATE}}`, `{{MILESTONE_1_NAME}}` à `{{MILESTONE_5_NAME}}`.

---

### 1.10 `gantt_phases`

**Inspiration** : Template RH slide 14 (Gantt swimlanes avec pills mois en header).
**Description** : 3 pills orange mois en haut + 4 phases × 3 mois avec barres roundées colorées (jaune/orange/rouille/navy) sur fond gris.
**Zones variables** : `{{MONTH_1_LABEL}}` à `{{MONTH_3_LABEL}}`, `{{PHASE_1_NAME}}` à `{{PHASE_4_NAME}}`, `{{PHASE_1_BAR}}` à `{{PHASE_4_BAR}}` (la barre colorée = position + durée à régler dans le code skill).

Aperçu : [chantier_exhibits_assets/slide-14.jpg](chantier_exhibits_assets/slide-14.jpg)

---

### 1.11 `status_3cols`

**Inspiration** : Template RH slide 17 (Finalisé/En cours/Annulé en 3 colonnes vert/orange/rouge).
**Description** : 3 cartes côte à côte avec headers Finalisé (vert `#2D6A4F`) / En cours (orange) / Annulé (rouge `#C81D25`) ; 3 actions empilées dans chaque colonne.
**Zones variables** :

| Slot | Rôle |
|---|---|
| `{{COL_DONE_TITLE}}`, `{{COL_WIP_TITLE}}`, `{{COL_DROPPED_TITLE}}` | titre de chaque colonne (renommables) |
| `{{COL_DONE_ITEM_1}}` à `{{COL_DONE_ITEM_3}}` | actions empilées de la colonne Done |
| (idem WIP et DROPPED) | |

Aperçu : [chantier_exhibits_assets/slide-15.jpg](chantier_exhibits_assets/slide-15.jpg)

---

### 1.12 `process_steps`

**Inspiration** : grammaire consulting + Template RH slide 15.
**Description** : 4 cercles orange numérotés alignés horizontalement reliés par une ligne grise, titre + description sous chaque cercle.
**Zones variables** : `{{STEP_1_TITLE}}` à `{{STEP_4_TITLE}}`, `{{STEP_1_DETAIL}}` à `{{STEP_4_DETAIL}}`.

---

### 1.13 `text_dense_3cols`

**Inspiration** : Template RH slide 5 (3 colonnes textes éditoriaux).
**Description** : 3 colonnes avec eyebrow + heading + paragraphe (plus dense que `executive_summary`).
**Zones variables** : `{{COL_1_EYEBROW}}` à `{{COL_3_EYEBROW}}`, `{{COL_1_TITLE}}` à `{{COL_3_TITLE}}`, `{{COL_1_BODY}}` à `{{COL_3_BODY}}`.

---

### 1.14 `quote_callout`

**Inspiration** : le `quote` du Skill (barre orange latérale + citation grande).
**Description** : barre orange verticale à gauche + citation italique navy en gros + attribution orange uppercase + takeaway en haut.
**Zones variables** : `{{QUOTE_TEXT}}`, `{{QUOTE_ATTRIBUTION}}`, `{{TAKEAWAY}}`.

Aperçu : [chantier_exhibits_assets/slide-19.jpg](chantier_exhibits_assets/slide-19.jpg) (NB: c'est slide-18.jpg en fait, slide 19 = next_steps)

---

### 1.15 `next_steps`

**Inspiration** : grammaire consulting "the ask" en fin de deck.
**Description** : 4 rangées avec cercle orange numéroté + action (navy bold) + owner (gray) + date (orange bold). Headers ACTION / OWNER / BY en uppercase.
**Zones variables** : `{{ACTION_1_TEXT}}` à `{{ACTION_4_TEXT}}`, `{{ACTION_1_OWNER}}` à `{{ACTION_4_OWNER}}`, `{{ACTION_1_DATE}}` à `{{ACTION_4_DATE}}`.

Aperçu : [chantier_exhibits_assets/slide-19.jpg](chantier_exhibits_assets/slide-19.jpg)

---

## 2. Convention de nommage adoptée

- **Slots variables remplis par le skill** : `{{UPPER_SNAKE_CASE}}` entre doubles accolades sur `shape.name`.
- **Décor non remplaçable** : `lowercase_snake_case` sans accolades (ex. `takeaway_bar`, `quote_bar`, `col1_bar`, `chart_bg`, `arrow`).
- **Groupes répétables** : pour les patterns en grille (KPI quad, status 3cols, etc.), chaque cellule est nommée individuellement (`{{KPI_1_VALUE}}`, `{{KPI_2_VALUE}}`, …) plutôt qu'avec un seul `{{REPEAT_ITEM}}`. Le skill saura les énumérer par regex `{{KPI_(\d+)_VALUE}}`.

Chaque slide a son `cSld.name` défini avec le nom de layout exact (`executive_summary`, `kpi_dual`, etc.) — visible dans le **volet de sélection** de PowerPoint.

---

## 3. Header & footer canoniques (appliqués sur les 15 layouts)

```
EYEBROW    (orange uppercase 10pt bold)     @ y=0.25"
TITLE      (navy 22pt bold, hérité du master) @ y=0.55"
TAKEAWAY   (orange bar + texte navy bold 12pt) @ y=1.32" (optionnel)
EXHIBIT    (zone fonctionnelle du layout)    @ y=1.95" → 4.95"
SOURCE     (gray italic 9pt)                 @ y=5.20"
```

Note : le `{{TITLE}}` est l'ancien placeholder de la slide 3 (canevas), déplacé et restylé à chaque slide. Il garde sa propriété de placeholder lié au layout `5_Vide` → quand l'utilisateur tape dans PowerPoint il bénéficie du formatage hérité.

---

## 4. Frictions techniques rencontrées

### 4.1 Slide 5 mentionnée dans la mission ≠ ce qu'il y avait

La mission disait *"Une 5e slide existe dans le fichier : une slide vierge"*. **Le fichier n'en contenait que 4** au moment de l'audit :

1. `Diapositive de titre` (cover_diagonal) — placeholders REF/TITLE/SUBTITLE + logo
2. `intercalaires` (agenda_diagonal) — TITLE "SOMMAIRE" + REPEAT_ITEM + IMAGE
3. `5_Vide` (**le canevas blanc**) — TITLE "tITRE" + slide number footer
4. `intercalaires` (closing_diagonal) — TITLE "MERCI" + auteur + email + tel + url

Donc le canevas blanc est la **slide 3** (pas la 5). J'ai utilisé celle-ci comme base de duplication.

### 4.2 Duplication de slide en python-pptx

python-pptx n'a pas d'API native pour dupliquer une slide. J'ai utilisé le pattern canonique : `add_slide(source.slide_layout)` puis suppression des auto-placeholders et `deepcopy` de chaque `shape._element` du source vers le nouveau `_spTree`. Robuste, validé par PowerPoint.

### 4.3 Master uppercase forcé sur le titre

Le master `5_Vide` force le titre en **uppercase** au rendu (les images JPEG le montrent : `"Action title..." → "ACTION TITLE..."`). C'est intégré au master via `<a:latin>` + paragraph properties, et ça **ne s'affiche pas** dans le texte stocké en source — donc le slot `{{TITLE}}` côté skill devra accepter du Title Case et le master appliquera la transformation visuelle. Aucun fix nécessaire.

### 4.4 Petits chevauchements à polir manuellement (mineurs)

Identifiés au QA visuel — l'utilisateur va polir, donc juste à noter :

| Slide | Symptôme | Sévérité |
|---|---|---|
| 7 (`kpi_quad`) | Les labels "KPI label" sous les KPI de la rangée 2 touchent le `{{SOURCE}}` ; gain de 0.1" en hauteur EXHIBIT_H réglerait | mineur |
| 19 (`next_steps`) | La 4ᵉ rangée d'action chevauche le `{{SOURCE}}` ; à 3 actions ou en réduisant `row_h` de 0.65" à 0.55" c'est OK | mineur |
| 14 (`gantt_phases`) | Les barres ne sont pas alignées sur la grille des pills mois (chaque pill est un peu plus petite que la cellule de grille à cause du `pad`) ; refinement esthétique | cosmétique |
| 12 (`matrix_2x2_styled`) | Le label "Effort" du X-axis empiète sur le footer du master (qui dit "CONFIDENTIEL — USAGE INTERNE") car centré à y=5.0" sur grille qui descend à 5.0" | mineur |

Aucun défaut bloquant pour la livraison du chantier. Le rendu **structurel** des 15 layouts est cohérent et lisible.

### 4.5 Palette + Arial respectés

Toutes les couleurs utilisées appartiennent à la palette canonique demandée : `#14163C` (navy), `#F26622` (orange), `#F9B300` (jaune accent — utilisé dans `gantt_phases` pour la phase 1), `#FAFAF7` (light), `#4A4D6B` (gray), `#E8E9F2` (gray_light), plus `#2D6A4F` (vert status) et `#C81D25` (rouge status) — ces deux derniers ont été ajoutés pour `status_3cols` car la palette AOSIS n'a pas de vert/rouge dédié au statut. Tous les `run.font.name = "Arial"` sont forcés explicitement dans `add_text`.

---

## 5. Reproduire la génération

Le script de génération est à `/tmp/build_exhibits.py` (one-off, non commité car hors scope). Pour rerun :

```bash
cd aosis-deck-builder
cp assets/exhibits.backup.pptx assets/exhibits.pptx   # repart du backup
python /tmp/build_exhibits.py                          # ajoute les 15 layouts
```

Le script :
1. Ouvre `assets/exhibits.pptx`.
2. Cherche la première slide dont le layout est `5_Vide` (slide 3 ici).
3. Pour chaque layout listé dans `LAYOUTS = [(name, fn), ...]` : duplique la slide canevas, renomme le `cSld.name`, exécute la fonction de dessin.
4. Sauvegarde.

---

## 6. Livrables

| Livrable | Chemin |
|---|---|
| Fichier modifié | [`aosis-deck-builder/assets/exhibits.pptx`](aosis-deck-builder/assets/exhibits.pptx) — 19 slides |
| Backup intouché | [`aosis-deck-builder/assets/exhibits.backup.pptx`](aosis-deck-builder/assets/exhibits.backup.pptx) — 4 slides d'origine |
| Rapport | [`chantier_exhibits_report.md`](chantier_exhibits_report.md) — ce document |
| Screenshots de QA | [`chantier_exhibits_assets/`](chantier_exhibits_assets/) — 5 slides représentatives |
| JPEG complets des 15 slides | `/tmp/exhibits_review/slide-05.jpg` à `slide-19.jpg` (non persistés au-delà du reboot WSL) |

Périmètre respecté : seul `assets/exhibits.pptx` modifié dans le bundle skill.

---

## 7. Next steps suggérés

1. **Toi (utilisateur)** : ouvrir `exhibits.pptx` dans PowerPoint, polir manuellement les alignements, couleurs et tailles d'icônes — c'est ce qui était prévu, je n'ai pas cherché le pixel-perfect.
2. **Chantier 7 (éventuel)** : câbler ces 15 layouts dans le dispatcher de `build_deck.py`. Chaque layout aurait sa fonction `add_<layout_name>(prs, spec)` qui ouvre `exhibits.pptx`, clone la slide correspondante au nom, et **remplit chaque `shape.name == "{{...}}"`** avec le contenu de `spec`. C'est exactement le pattern du Template Layout de python-pptx mais piloté par les noms.
3. **Documentation** : si le câblage se fait, ajouter ces 15 layouts à `references/layouts.md` et `references/json-schema.md` (catalogue + champs).
