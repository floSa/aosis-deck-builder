# Audit — Skill `aosis-deck-builder`

> Date : 2026-05-13 · Périmètre : archive `aosis-deck-builder.skill` à la racine du projet. Aucun code modifié.

---

## 1. Inventaire du template `assets/AOSIS_template.pptx`

### 1.1 Slide masters et layouts

Le template contient **2 slide masters** et **4 slide layouts** au total.

| Master | Layout (fichier) | Nom exact | Placeholders | Theme rattaché |
|---|---|---|---|---|
| `slideMaster1.xml` | `slideLayout1.xml` | **Cover** | `title/idx=0`, `body/idx=10` | `theme1.xml` |
| `slideMaster1.xml` | `slideLayout2.xml` | **Closing** | (aucun) | `theme1.xml` |
| `slideMaster2.xml` | `slideLayout3.xml` | **Contenu + texte** | `title/idx=0`, `content/idx=10` | `theme2.xml` |
| `slideMaster2.xml` | `slideLayout4.xml` | **Texte** | `title/idx=0`, `body/idx=10` | `theme2.xml` |

> ⚠️ **Anomalie d'architecture détectée** : les deux masters utilisent des **thèmes différents**. Master 1 (Cover / Closing) → `theme1.xml` ; Master 2 (les slides de contenu) → `theme2.xml`. Les deux schémas couleurs et polices ne sont pas alignés (voir §1.2 et §1.3).

### 1.2 Palettes définies dans les themes

Le `.pptx` embarque **4 themes** (`theme1`–`theme4`). Seuls `theme1` et `theme2` sont effectivement rattachés à des masters utilisés ; `theme3` et `theme4` sont des résidus de manipulations PowerPoint (themes Office par défaut).

#### `theme1.xml` — name = "01 - Blue", colorScheme = "Orange rouge" — rattaché au master 1 (Cover/Closing)

| Slot | Hex |
|---|---|
| dk1 | sys windowText (`#000000`) |
| lt1 | sys window (`#FFFFFF`) |
| dk2 | `#696464` |
| lt2 | `#E9E5DC` |
| accent1 | `#D34817` |
| accent2 | `#9B2D1F` |
| accent3 | `#A28E6A` |
| accent4 | `#956251` |
| accent5 | `#918485` |
| accent6 | `#855D5D` |
| hlink | `#CC9900` |
| folHlink | `#96A9A9` |

#### `theme2.xml` — name = "02 - White", colorScheme = "AOSIS" — rattaché au master 2 (contenu)

| Slot | Hex |
|---|---|
| dk1 | `#14163C` (navy AOSIS) |
| lt1 | `#FAFAF7` (off-white) |
| dk2 | `#4A4D6B` (gray) |
| lt2 | `#E8E9F2` (gray light) |
| accent1 | `#F26622` (orange AOSIS) |
| accent2 | `#1E2261` (navy variant) |
| accent3 | `#C2491A` |
| accent4 | `#F9B233` |
| accent5 | `#7CB342` |
| accent6 | `#E63946` |
| hlink | `#F26622` |
| folHlink | `#C2491A` |

#### `theme3.xml` / `theme4.xml`
Themes Office par défaut (`Office`, `Calibri`/`Aptos`), **non rattachés** à un master utilisé — bruit résiduel.

### 1.3 Polices définies

| Theme | majorFont (titres) | minorFont (corps) |
|---|---|---|
| `theme1` (Cover/Closing) | **Aptos Display** | **Aptos** |
| `theme2` (Contenu) | **Arial** | **Arial** |
| `theme3` | Calibri Light | Calibri |
| `theme4` | Aptos Display | Aptos |

> ⚠️ Cover et Closing héritent d'**Aptos** ; toutes les slides de contenu héritent d'**Arial**. Le code force par ailleurs `font="Arial"` sur tous les textboxes générés (cf. §2.4). À l'écran, le titre de cover ne sera donc pas en Arial — incohérence typographique d'ouverture/fermeture vs corps du deck.

---

## 2. Audit du code `scripts/build_deck.py`

### 2.1 Lignes totales

**1368 lignes** (Python pur, monolithique, sans découpage en modules).

### 2.2 Lignes par fonction (toutes les fonctions `add_*` et helpers privés)

| Fonction | Lignes | Type |
|---|---|---|
| `_resolve_layout` | 7 | helper |
| `_placeholder_by_idx` | 7 | helper |
| `_set_text` | 6 | helper |
| `_remove_body_placeholder` | 6 | helper |
| `_blank_canvas` | 8 | helper |
| `_add_text` | 25 | helper |
| `_add_rect` | 21 | helper |
| `_add_rounded_rect` | 23 | helper |
| `_add_circle_number` | 22 | helper |
| `add_cover` | 7 | template-based |
| `add_section` | 4 | template-based |
| `add_closing` | 4 | template-based |
| `add_text_slide` | 19 | template-based |
| `add_content_slide` | 47 | template-based |
| `add_stat_grid` | 44 | composé |
| `add_cards` | 43 | composé |
| `add_comparison` | 43 | composé |
| `add_timeline` | 34 | composé |
| `add_process` | 34 | composé |
| `add_quote` | 25 | composé |
| `add_image_hero` | 22 | composé |
| `add_hero_stat` | 55 | inspirational |
| `add_big_idea` | 51 | inspirational |
| `add_matrix_2x2` | 68 | inspirational |
| `add_funnel` | 45 | inspirational |
| **`add_roadmap`** | **70** | inspirational |
| `_generate_abstract_background` | 47 | helper |
| `add_swot` | 46 | inspirational |
| `add_pyramid` | 50 | inspirational |
| **`add_org_chart`** | **101** | inspirational (plus grosse fonction) |
| `add_agenda` | 47 | inspirational |
| `add_dashboard` | 61 | inspirational |
| `_render_chart_png` | 94 | matplotlib |
| `add_chart_slide` | 76 | wrap chart |
| `build_deck` | 26 | orchestrateur |
| `main` | 16 | CLI |

> Aucune fonction n'est dramatiquement longue, mais `add_org_chart` (101 lignes) est candidate à découpage.

### 2.3 Constantes de couleur hardcodées dans le code

Définies aux lignes 33-39 :

| Constante Python | Hex code | Correspondance dans le theme |
|---|---|---|
| `NAVY` | `#14163C` | = `theme2.dk1` ✅ |
| `ORANGE` | `#F26622` | = `theme2.accent1` ✅ |
| `LIGHT` | `#FAFAF7` | = `theme2.lt1` ✅ |
| `GRAY` | `#4A4D6B` | = `theme2.dk2` ✅ |
| `GRAY_LIGHT` | `#E8E9F2` | = `theme2.lt2` ✅ |
| `WHITE` | `#FFFFFF` | générique (theme1.lt1 / theme2.dk1.contrast) |
| `NAVY_SOFT` | `#2A2D5C` | ❌ **N'existe dans aucun theme** — couleur inventée |

#### Verdict duplication / divergence

- **Duplication systémique** : 5 constantes sur 7 (`NAVY`, `ORANGE`, `LIGHT`, `GRAY`, `GRAY_LIGHT`) reproduisent exactement la palette `theme2.xml`. Si la charte évolue, il faudra modifier deux endroits (theme XML + code Python) → **risque de désynchronisation**.
- **Couleur inventée** : `NAVY_SOFT` (`#2A2D5C`) n'est définie ni dans `theme1` ni dans `theme2`. Elle est utilisée localement dans le code sans traçabilité brand. À documenter ou supprimer.
- **Aucune référence à `theme1`** : la palette "Orange rouge" du master Cover/Closing (`#D34817`, `#9B2D1F`, `#696464`) n'est jamais utilisée dans le code. Le code suppose implicitement que tout est theme2 — alors que master 1 est theme1. Cohérence visuelle non garantie pour cover/closing.

### 2.4 Imports et dépendances externes

```python
# Stdlib
import argparse, json, os, sys, tempfile
from pathlib import Path

# Externes
from pptx import Presentation                            # python-pptx
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt
```

- **Dépendance directe déclarée** : `python-pptx` (testé en 1.0.2).
- **Dépendance implicite (non déclarée)** : `matplotlib` (utilisée dans `_render_chart_png` lignes 1158+). Aucun `requirements.txt`, `pyproject.toml`, ou `setup.py` dans l'archive → **dépendance silencieuse**, à découvrir à l'exécution la première fois qu'un layout `chart` ou `dashboard` est sollicité.
- `tempfile` est importé mais utilisé seulement par `_render_chart_png` ; `os` n'est pratiquement plus utilisé après refactos passés.

### 2.5 Tests et fixtures

**Aucun**. Recherche `test*`, `*_test.py`, `fixtures/`, `conftest*` dans l'archive : 0 résultat. Pas de spec JSON d'exemple non plus dans l'archive (seul l'exemple inline du SKILL.md fait foi). **Régression visuelle non détectable automatiquement.**

---

## 3. Audit du `SKILL.md`

### 3.1 Longueur

**384 lignes**.

### 3.2 Sections de premier niveau (`##`)

| Ligne | Section |
|---|---|
| 14 | The Three Golden Rules |
| 45 | Layout Catalogue |
| 88 | The Build Workflow |
| 109 | JSON Spec Schema |
| 329 | QA — Always Verify Visually |
| 360 | Content QA |
| 369 | What This Skill Does NOT Do |
| 380 | Delivering to the User |

### 3.3 Sections volumineuses, candidates à fichiers de référence séparés

| Section | Plage | ~Lignes | Candidat ? |
|---|---|---|---|
| **JSON Spec Schema** (incl. exemple complet + reference par layout) | 109 → 328 | ~220 | ⭐ Oui — sortir en `references/json-schema.md` (et optionnellement un JSON Schema strict pour validation) |
| **Layout Catalogue** | 45 → 87 | ~43 | Oui — `references/layouts.md` |
| **Three Golden Rules + intro** | 6 → 44 | ~38 | Garder dans SKILL.md (philosophie) |
| **QA + Content QA** | 329 → 367 | ~38 | Possiblement sortir en `references/qa.md` |

Le **JSON Spec Schema** monopolise plus de la moitié du SKILL.md. Le pattern Claude Skills recommande de garder SKILL.md court (≤ 200 lignes) et de déporter les références volumineuses dans `references/`. Ici, la migration est mûre :

```
aosis-deck-builder/
├── SKILL.md                       # règles d'or, workflow, pointeurs (≤ 200 l)
├── references/
│   ├── layouts.md                 # catalogue détaillé
│   ├── json-schema.md             # champs par layout + exemple complet
│   └── qa.md                      # commandes QA visuel + contenu
├── scripts/
└── assets/
```

---

## 4. Test de fonctionnement

### 4.1 Environnement

- `python-pptx 1.0.2` + `matplotlib 3.10.9` installés dans un venv via `uv`.
- **LibreOffice / `soffice` / `pdftoppm` indisponibles** dans cet environnement WSL (apt restreint). Impossible de produire des JPEG de rendu — **l'inspection visuelle a été remplacée par une inspection géométrique** du `.pptx` généré (positions et tailles de shapes en EMU, polices effectives, couleurs effectives). Plus rigoureuse qu'un coup d'œil JPEG sur des défauts précis, mais ne révèle pas les défauts purement esthétiques (équilibre des blancs, hiérarchie typographique perçue).

### 4.2 Spec utilisé

Sujet : *Refonte d'un système de reporting risque*. 5 slides : `cover` → `hero_stat` → `matrix_2x2` → `roadmap` → `closing`. Spec sauvegardé dans `/tmp/audit_spec.json`, deck dans `/tmp/audit_deck.pptx` (580 590 octets).

### 4.3 Inspection géométrique slide par slide

Dimensions slide : **10.000" × 5.625"** (16:9 PowerPoint standard).

| # | Layout | Shapes | Débordements | Polices runs | Couleurs textes |
|---|---|---|---|---|---|
| 1 | `Cover` | 2 (placeholders uniquement) | 0 | héritées (Aptos) | héritées |
| 2 | `Texte` (hero_stat) | 11 | 0 | Arial | NAVY, GRAY |
| 3 | `Texte` (matrix_2x2) | 23 | 0 | Arial | NAVY, GRAY, WHITE |
| 4 | `Texte` (roadmap) | 22 | **6 ⚠️** | Arial | ORANGE, NAVY, GRAY |
| 5 | `Closing` | 0 | 0 | héritées | héritées |

### 4.4 Défauts précis constatés

#### ⚠️ Défaut #1 — `roadmap` : textboxes hors slide

Le layout `roadmap` (slide 4) produit **6 textboxes qui débordent** des limites de slide (10.00" × 5.625") :

```
TextBox 4   pos=(-0.15", 1.05")  size=(1.90" × 0.30")  → left edge < 0
TextBox 5   pos=(-0.15", 1.40")  size=(1.90" × 0.40")  → left edge < 0
TextBox 6   pos=(-0.35", 1.85")  size=(2.30" × 0.80")  → left edge < 0
TextBox 20  pos=(8.25", 1.05")   size=(1.90" × 0.30")  → right edge 10.15" > 10.00"
TextBox 21  pos=(8.25", 1.40")   size=(1.90" × 0.40")  → right edge 10.15" > 10.00"
TextBox 22  pos=(8.05", 1.85")   size=(2.30" × 0.80")  → right edge 10.35" > 10.00"
```

→ Cause : `add_roadmap` ne contraint pas la position des labels date/name/detail aux marges. Le **premier** et le **dernier** milestone sortent par construction quand 5 milestones sont espacés équirépartiquement. Le SKILL.md mentionne ce risque ("Roadmap labels qui se chevauchent — réduire à 5 max"), mais le défaut documenté est le chevauchement, pas le débordement hors slide. Le débordement n'est pas mentionné.

#### ⚠️ Défaut #2 — incohérence typographique cover ↔ contenu

- Slides 2-4 (corps) : tous les runs sont en **Arial** (forcé par `_add_text(font="Arial")`).
- Slides 1 (Cover) et 5 (Closing) : aucun run stylé → héritage du master 1 → **Aptos Display / Aptos** (theme1).
- Le deck final mélange donc deux familles de polices. Pour un rendu consulting top-tier, cette incohérence est visible.

#### ⚠️ Défaut #3 — palette du cover/closing potentiellement non-AOSIS

Master 1 est rattaché à `theme1` ("Orange rouge", accent1 = `#D34817`). Si un élément du master référence `accent1` (vs une couleur hardcodée), il s'affichera en rouille `#D34817` et **non** en orange AOSIS `#F26622`. À vérifier en ouvrant le pptx dans PowerPoint avec l'outil "Format → Theme colors" sur la cover.

#### Cohérence positive constatée

- Toutes les couleurs textes effectives appartiennent à la palette AOSIS (`#14163C`, `#F26622`, `#4A4D6B`, `#FFFFFF`).
- Le `hero_stat` rend bien la valeur en 120pt (mesuré dans les runs).
- Le `matrix_2x2` (slide 3) ne déborde pas avec 2-3 items par quadrant.
- La grille de tailles de polices reste lisible (10pt minimum pour les labels, 11-14pt pour les contenus).

### 4.5 Reproduire l'inspection visuelle (recommandation)

Sur une machine équipée :

```bash
soffice --headless --convert-to pdf /tmp/audit_deck.pptx --outdir /tmp/
pdftoppm -jpeg -r 150 /tmp/audit_deck.pdf /tmp/audit-slide
# puis ouvrir /tmp/audit-slide-*.jpg
```

---

## 5. Synthèse

### 5.1 Top 5 — problèmes prioritaires pour atteindre un rendu pro

| # | Problème | Impact | Effort |
|---|---|---|---|
| **1** | `roadmap` produit des labels qui débordent à gauche (-0.35") et à droite (10.35") dès 5 milestones — défaut systématique, pas une exception. Visible immédiatement à l'ouverture du pptx. | Élevé (rendu cassé) | Bas (rework de `add_roadmap` lignes 736-805 — clamper les positions des labels aux marges, ou réduire l'amplitude horizontale du tracé). |
| **2** | **Incohérence typographique** : cover/closing en Aptos (theme1), contenu en Arial (theme2 + force code). Cassure visuelle d'ouverture du deck. | Élevé (perception "amateur") | Bas (option A : aligner theme1 sur la même font que theme2 dans le template ; option B : forcer Arial sur les placeholders cover/closing dans `add_cover`/`add_closing`). |
| **3** | **Le master 1 utilise un theme "Orange rouge" (`#D34817`) au lieu de l'orange AOSIS (`#F26622`)** — risque de rendu cover/closing aux mauvaises couleurs si un élément du master référence `accent1` du theme. | Moyen à élevé (selon ce que le master référence) | Bas (réassigner `theme2` à `slideMaster1.xml.rels`, ou supprimer theme1/3/4 redondants). |
| **4** | **Palette dupliquée code↔theme sans source unique** : `NAVY`, `ORANGE`, `LIGHT`, `GRAY`, `GRAY_LIGHT` existent à la fois en hex hardcodé Python et dans `theme2.xml`. Une évolution charte casse la cohérence. | Moyen (dette future) | Moyen (lire la palette via `python-pptx` depuis le theme au chargement, ou centraliser dans un `brand.py` avec un commentaire renvoyant au theme). |
| **5** | **SKILL.md sur-chargé (384 lignes, schéma JSON = 220 lignes)** → coût de chargement contexte élevé à chaque invocation Claude, et difficulté de maintenir SKILL.md court. | Moyen (perf + DX Claude) | Moyen (déporter `Layout Catalogue` + `JSON Spec Schema` + `QA` dans `references/` ; SKILL.md devient un index opérationnel ≤ 200 l). |

### 5.2 Top 3 — risques techniques (dette, fragilité, dépendances)

| # | Risque | Détail |
|---|---|---|
| **1** | **Aucun test, aucune fixture**. Pas même un golden JSON d'exemple dans l'archive. Toute évolution de `build_deck.py` est validée à la main par QA visuel. Régression de mise en page (style le défaut roadmap ci-dessus) indétectable sans œil humain. **Très exposé** quand le code passera 1500+ lignes. |
| **2** | **`matplotlib` est une dépendance silencieuse** non déclarée. Aucun `requirements.txt`/`pyproject.toml` dans l'archive. Premier appel à `chart` ou `dashboard` plante avec `ModuleNotFoundError`. À fixer avec un fichier de deps minimal et idéalement un check à l'import au top de `build_deck.py`. |
| **3** | **Bruit XML dans le template** : 4 themes embarqués alors que 2 sont utilisés, plus un colorScheme exotique "Orange rouge" rattaché au master Cover/Closing. Le `.pptx` est plus lourd que nécessaire (591 Ko avec un seul template, dont beaucoup d'inerte) et l'incohérence theme1/theme2 est un cliquet à incidents. À nettoyer en passant le template dans LibreOffice/PowerPoint et en supprimant les masters/themes non utilisés. |

---

## Annexes

### A. Mapping `LAYOUT_MAP` (build_deck.py l.54-60) → réalité du template

| Clé code | (master, layout) attendu | Nom layout réel | Cohérent ? |
|---|---|---|---|
| `cover` | (0, 0) | `Cover` (master1, layout1) | ✅ |
| `section` | (0, 0) | `Cover` (master1, layout1) — réutilisé | ✅ par design |
| `closing` | (0, 1) | `Closing` (master1, layout2) | ✅ |
| `content` | (1, 0) | `Contenu + texte` (master2, layout3) | ✅ |
| `text` | (1, 1) | `Texte` (master2, layout4) | ✅ |

### B. Catalogue des 23 layouts du dispatcher (cohérence SKILL.md)

`cover`, `section`, `closing`, `text`, `content`, `stat_grid`, `cards`, `comparison`, `timeline`, `process`, `quote`, `image_hero`, `chart`, `hero_stat`, `big_idea`, `matrix_2x2`, `funnel`, `roadmap`, `swot`, `pyramid`, `org_chart`, `agenda`, `dashboard` → **23 layouts**, tous documentés dans SKILL.md (catalogue § 4 du document de référence).

### C. Couleurs effectivement utilisées dans le deck généré (test slide 4)

`#F26622` (orange), `#14163C` (navy), `#4A4D6B` (gray) — toutes issues de la palette AOSIS theme2. Aucune fuite de couleurs theme1 / theme3 / theme4 dans les runs.
