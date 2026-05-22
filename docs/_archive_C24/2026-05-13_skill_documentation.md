# Skill `aosis-deck-builder` — Documentation complète

> Document de référence interne. Vue macro → vue détaillée du skill packagé dans `aosis-deck-builder.skill` à la racine du projet.

---

## 1. Vue macro — c'est quoi ce skill ?

Le fichier `aosis-deck-builder.skill` à la racine est une **archive ZIP** contenant un *Claude Skill*, c'est-à-dire un bundle activable par Claude (Claude Code, Claude.ai, Claude API via la fonctionnalité Skills) pour exécuter une tâche spécialisée.

**Mission du skill** : générer des présentations PowerPoint (`.pptx`) au style **AOSIS**, avec un rendu « consulting top-tier » (McKinsey / BCG / Bain), à partir d'une simple **spécification JSON**.

| Élément | Valeur |
|---|---|
| Nom | `aosis-deck-builder` |
| Format | Archive `.skill` (= ZIP) |
| Taille | ~591 Ko |
| Trigger | Demandes contenant "powerpoint", "pptx", "deck", "slides", "présentation", proposition commerciale, restitution, CODIR… |
| Sortie | Un fichier `.pptx` AOSIS-brandé prêt à livrer |
| Dépendances runtime | `python-pptx`, `matplotlib` (pour les charts) |

**Principe fondamental** : le skill **n'invente pas la charte graphique**. Il part du template officiel AOSIS (`assets/AOSIS_template.pptx`) — couleurs, logo, footers, polices sont hérités. Le code Python ajoute uniquement le **contenu** et la **composition visuelle** des slides.

---

## 2. Structure de l'archive

Une fois dépackée, l'archive contient :

```
aosis-deck-builder/
├── SKILL.md                          # Manifeste + doc pour Claude (frontmatter YAML + corps)
├── scripts/
│   └── build_deck.py                 # Générateur Python (1368 lignes)
└── assets/
    └── AOSIS_template.pptx           # Template PowerPoint officiel AOSIS
```

### 2.1 `SKILL.md`
Le fichier d'entrée que Claude lit. Il contient :
- Un **frontmatter YAML** avec `name` et `description` (la `description` sert au routage : c'est ce que Claude inspecte pour décider d'activer le skill).
- Le **corps Markdown** : règles d'or, catalogue des layouts, workflow, schéma JSON, exemples, instructions de QA.

### 2.2 `scripts/build_deck.py`
Le moteur de génération. Utilisé en CLI :
```bash
python scripts/build_deck.py <spec.json> <output.pptx>
```

### 2.3 `assets/AOSIS_template.pptx`
Le squelette PowerPoint officiel. Contient les **slide masters** (couches de design) qui posent automatiquement logo, footers, fonds, palette. Le script Python ne touche **jamais** aux masters.

---

## 3. Philosophie et règles d'or

Le SKILL.md formalise **trois règles d'or** que Claude doit suivre :

### Règle 1 — Ne jamais recréer la charte AOSIS dans le code
Le template porte le design. Si le code commence à manipuler `slide.background.fill.solid()` ou à injecter un logo manuellement, c'est un signal qu'on contourne le template au lieu de l'utiliser.

### Règle 2 — Toujours préférer un layout visuel au texte
Le réflexe par défaut **n'est pas** « titre + bullets ». L'ordre de préférence :
1. Ouvrir avec `hero_stat` ou `big_idea`.
2. Structurer les arguments avec `comparison`, `matrix_2x2`, `roadmap`.
3. Appuyer avec un `chart` pour les données.
4. Ancrer avec `quote`.
5. Ne tomber sur `text` / `content` **que** quand le message *est* littéralement des mots (mentions légales, tarification, prochaines étapes).

### Règle 3 — Toujours écrire des titres d'action, jamais descriptifs
Un titre d'action **livre le message**, un titre descriptif se contente d'étiqueter.

| ❌ Descriptif | ✅ Action |
|---|---|
| "Approche méthodologique" | "Notre approche en 4 phases pour livrer la cible à T+12 mois" |
| "Chiffres clés" | "1,2 M€ pour reprendre 6h sur chaque cycle de reporting" |
| "Équipe" | "L'équipe que nous mobilisons : 6 consultants, 50 ans d'expérience cumulée" |

Bonne pratique : un deck dont on lit seulement les titres doit raconter l'histoire.

---

## 4. Le catalogue de layouts (22 layouts)

Le catalogue est organisé en **trois familles**. La majorité du travail visuel doit se concentrer sur la famille **inspirational**.

### 4.1 Famille « Inspirational » — boîte à outils principale (16 layouts)

| Layout | Quand l'utiliser |
|---|---|
| `hero_stat` | Un chiffre énorme porte le message. Excellent opener et "pourquoi nous". Une stat (≥150pt), un label d'action, optionnel : liste à droite. |
| `big_idea` | Énoncé de thèse, conviction, principe de cadrage. Texte gras 40pt à gauche, bullets de support à droite. 1 à 2 par deck. |
| `matrix_2x2` | Frameworks stratégiques avec axes (priorité, impact/effort, BCG…). Le quadrant top-right est mis en valeur (la « star »). |
| `swot` | SWOT classique. Limite : 3 items par quadrant. Sinon préférer `matrix_2x2`. |
| `pyramid` | Frameworks hiérarchiques (Maslow, value chain). Base → sommet par défaut ; `inverted: true` pour inverser. |
| `funnel` | Processus de conversion ou de réduction (leads → closed, périmètre → livré). 3 à 5 étapes décroissantes. |
| `roadmap` | Jalons temporels sur une ligne horizontale. Marqueurs en losange, dates au-dessus/au-dessous. |
| `dashboard` | Snapshot exécutif : ligne de stats + chart en-dessous, style éditorial / FT. Idéal pour openers CODIR. |
| `org_chart` | Organigramme 2 niveaux : leader + N managers + équipiers optionnels. Pour slides « équipe » / « gouvernance ». |
| `agenda` | Sommaire numéroté. Grands chiffres orange à gauche, titres et timings à droite. Recommandé comme slide 2 d'un deck >8 slides. |
| `stat_grid` | 2 à 4 KPIs en ligne, alternance navy/orange. Pour « chiffres clés », hook post-cover, slide de recap. |
| `timeline` | 2 à 6 phases numérotées. Méthodologie / plan projet. |
| `cards` | Grilles d'items équivalents : équipe, services, références, principes. 2 à 8 cartes en 2/3/4 colonnes. |
| `comparison` | Avant/après, problème/solution, notre approche vs alternative. Deux colonnes, headers orange + navy. |
| `chart` | Données quantitatives. Génère matplotlib (bar / barh / line / pie) dans la palette AOSIS. Commentaire latéral possible. |
| `process` | Étape par étape vertical. Cercles orange numérotés reliés par une ligne. Idéal pour processus de gouvernance. |
| `quote` | Pull-quote éditoriale avec barre latérale. 1 à 2 par deck pour ancrer une thèse. |
| `image_hero` | Image pleine page avec bandeau navy en bas pour titre/sous-titre. Pour ouvertures de section. |

### 4.2 Famille « Opening / Closing » (3 layouts)

| Layout | Rôle |
|---|---|
| `cover` | Première slide. Fond navy, titre centré, callout orange en haut à droite (~10 caractères, date/référence). |
| `section` | Séparateur entre parties majeures. Même rendu que cover. |
| `closing` | Slide finale AOSIS statique. Ajoutée automatiquement sauf `"closing": false`. |

### 4.3 Famille « Plain text fallback » (2 layouts)

| Layout | Rôle |
|---|---|
| `text` | Titre + bullets pleine largeur. Réservé aux cas où les mots **sont** le message (légal, tarification, prochaines étapes). |
| `content` | Titre + bullets + visuel côte à côte. Réservé aux slides où on a une vraie image (screenshot, photo). |

---

## 5. Workflow de construction (4 étapes)

### Étape 1 — Planifier la narration
- Définir le type de deck : *proposal*, *restitution*, *CODIR*.
- Choisir le message central.
- Esquisser 6 à 12 slides en s'assurant que les **titres lus en séquence racontent l'histoire**.
- **Varier les layouts** : ouvrir fort (`hero_stat` / `big_idea`), alterner frameworks (`matrix_2x2`, `funnel`, `roadmap`), supporter avec `chart`, ancrer à mi-deck avec `quote`, clore avec un dernier `hero_stat` / `big_idea` qui pose la demande.

### Étape 2 — Écrire le spec JSON
Sauvegarder dans `/tmp/deck_spec.json` (ou n'importe où). Voir schéma section 6.

### Étape 3 — Lancer le générateur
```bash
python scripts/build_deck.py /tmp/deck_spec.json /mnt/user-data/outputs/deck.pptx
```

### Étape 4 — QA visuel
Convertir en PDF puis en images JPEG et inspecter (voir section 8).
Fixer dans le **spec JSON** (jamais en post-éditant le `.pptx`) puis relancer.

---

## 6. Schéma JSON — structure de la spec

### 6.1 Squelette racine

```json
{
  "cover":   { "title": "...", "ref": "..." },
  "slides":  [ /* tableau ordonné de slides */ ],
  "closing": true
}
```

- `cover` (obligatoire) : `title` et `ref` (~10 caractères, ex. "Mai 2026").
- `slides` (obligatoire) : tableau d'objets, chacun avec une clé `layout` parmi les 22 disponibles.
- `closing` (optionnel, défaut `true`) : ajoute la slide finale AOSIS.

### 6.2 Champs par layout (référence détaillée)

#### `hero_stat`
| Champ | Type | Détail |
|---|---|---|
| `value` | string | Le chiffre géant. **≤ 7 caractères** sinon auto-shrink ("75%", "1,2 M€", "12 m"). |
| `label` | string | Phrase d'action sous le chiffre. |
| `context` | string optionnel | Ligne secondaire en gris. |
| `supporting` | list[string] optionnel | Bullets avec tick orange à droite. |
| `title` | string optionnel | Eyebrow tag en haut. |

#### `big_idea`
| Champ | Détail |
|---|---|
| `idea` | Énoncé en gras, 1-3 phrases max. |
| `title` | Eyebrow tag (UPPERCASE conseillé). |
| `attribution` | Petit tag orange uppercase sous l'idée. |
| `supports` | List[string] **ou** list[{title, detail}] — max 5. |

#### `matrix_2x2`
| Champ | Détail |
|---|---|
| `x_axis` | `{label, low, high}` |
| `y_axis` | `{label, low, high}` |
| `quadrants` | `{top_left, top_right, bottom_left, bottom_right}` chacun `{title, items}` |
| Convention | Le `top_right` = la "star" (priorité stratégique). Cap : 4 items / quadrant. |

#### `swot`
- `strengths`, `weaknesses`, `opportunities`, `threats` — chacun `{title, items}`.
- **Cap : 3 items par quadrant** (cellules moins spacieuses que `matrix_2x2`).

#### `pyramid`
- `levels` : 2 à 5 entrées, ordre **bas → haut** par défaut.
- `inverted: true` pour inverser. Apex (ou base si inversé) mis en orange.
- Chaque niveau : `name` (à l'intérieur) + `detail` optionnel (à droite).

#### `funnel`
- `stages` : 3 à 6 entrées : `name`, `value` optionnel (gros chiffre à droite), `detail` optionnel.
- Dernière étape highlight orange (conversion).

#### `roadmap`
- `milestones` : 2 à 6 entrées : `date` (court, "Juin '26"), `name`, `detail` optionnel.
- Labels alternent au-dessus/en-dessous de la ligne pour éviter collisions.

#### `stat_grid`
- `stats` : 1 à 4 entrées : `value`, `label`, `accent: "orange"|"navy"` optionnel.
- `footnote` global optionnel. `value` ≤ 6 caractères.

#### `dashboard`
- `stats` : jusqu'à 4 `{value, label}` (styling sobre).
- `chart` : même spec que le layout `chart` standalone.
- `chart_title` : petit label uppercase au-dessus du chart.
- `stats` ou `chart` peut être omis.

#### `agenda`
- `items` : jusqu'à 6 entrées : `title`, `detail` optionnel (timing en orange à droite).

#### `org_chart`
- `leader` : `{name, role}`.
- `reports` : jusqu'à 5 entrées `{name, role, members?}` (`members` = jusqu'à 3 noms empilés).
- Garder `name + role` ≤ 25 caractères combinés/ligne.

#### `timeline`
- `phases` : 2 à 6 entrées : `name`, `duration`, `detail` optionnel.

#### `cards`
- `cards` : liste `{title, body, badge?}`. Cap 6-8.
- `columns` global : 2 / 3 / 4.

#### `comparison`
- `left` / `right` : chacun `{title, subtitle?, items}`. Sweet spot : 4-5 items / côté.

#### `chart`
- Objet `chart` : `type` (`bar` / `barh` / `line` / `pie`), `labels`, `data` (mono-série) **ou** `series` (multi-séries).
- Optionnel : `ylabel`, `xlabel`, `highlight` (`"max"` / `"min"` / index int).
- Top-level `commentary` (list[string]) → bullets latérales au lieu de laisser le chart prendre toute la slide.

#### `quote`
- `text` (obligatoire), `author` (optionnel, orange uppercase).

#### `image_hero`
- `image` (chemin absolu), `title` / `subtitle` (bandeau navy en bas).

#### `text` / `content`
- `bullets` : list[string].
- `content` ajoute `image` (chemin absolu).

#### `cover` / `section`
- `title`, `ref` optionnel.

---

## 7. Le moteur Python — `scripts/build_deck.py`

### 7.1 Architecture
Le script (1368 lignes) est organisé en sections claires :

1. **Constantes** : palette AOSIS (`NAVY`, `ORANGE`, `LIGHT`, `GRAY`, etc.), géométrie 16:9 (10" × 5.62"), mapping vers les layouts de base du template.
2. **Helpers bas niveau** : `_resolve_layout`, `_placeholder_by_idx`, `_set_text`, `_add_text`, `_add_rect`, `_add_rounded_rect`, `_add_circle_number`, `_blank_canvas`.
3. **Layouts du template** (issus du `.pptx`) : `add_cover`, `add_section`, `add_closing`, `add_text_slide`, `add_content_slide`.
4. **Layouts composés** (dessinés en Python) : `add_stat_grid`, `add_cards`, `add_comparison`, `add_timeline`, `add_process`, `add_quote`, `add_image_hero`.
5. **Layouts inspirational avancés** : `add_hero_stat`, `add_big_idea`, `add_matrix_2x2`, `add_funnel`, `add_roadmap`, `add_swot`, `add_pyramid`, `add_org_chart`, `add_agenda`, `add_dashboard`.
6. **Génération de charts** : `_render_chart_png` (matplotlib avec palette AOSIS) + `add_chart_slide`.
7. **Dispatcher** : table `DISPATCH` qui mappe chaque clé `layout` du JSON vers la fonction Python correspondante.
8. **Orchestrateur** : `build_deck(spec, output_path, template_path=None)` qui ouvre le template, ajoute le cover, dispatche chaque slide, optionnellement ajoute le closing, sauvegarde.
9. **CLI** : `main()` parse `<spec>`, `<output>`, `--template` optionnel.

### 7.2 Palette AOSIS (extraite du theme)

| Constante | Hex | Usage |
|---|---|---|
| `NAVY` | `#14163C` | Couleur primaire, textes forts, fonds de section |
| `ORANGE` | `#F26622` | Accent, mise en valeur, "star" |
| `LIGHT` | `#FAFAF7` | Fond off-white |
| `GRAY` | `#4A4D6B` | Textes secondaires |
| `GRAY_LIGHT` | `#E8E9F2` | Séparateurs, fonds doux |
| `WHITE` | `#FFFFFF` | Texte sur fond navy/orange |
| `NAVY_SOFT` | `#2A2D5C` | Variante navy adoucie |

### 7.3 Layouts de base du template

Le `.pptx` source contient 2 slide masters, donc le mapping :
```
"cover"   → master 0, layout 0
"section" → master 0, layout 0
"closing" → master 0, layout 1
"content" → master 1, layout 0
"text"    → master 1, layout 1
```

Les layouts inspirational repartent du layout `text` puis suppriment le body placeholder (helper `_blank_canvas`) pour libérer la zone de contenu et la redessiner en shapes Python.

### 7.4 Dispatcher
Chaque entrée du dict `DISPATCH` est un lambda qui mappe une slide spec JSON vers un appel `add_*` typé. Si un `layout` inconnu apparaît dans la spec, `build_deck` lève une `ValueError` explicite avec la liste des layouts valides.

---

## 8. Quality Assurance

### 8.1 QA visuel — toujours rendu en images avant livraison

```bash
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless \
  --convert-to pdf /mnt/user-data/outputs/deck.pptx --outdir /tmp/
rm -f /tmp/aosis-slide-*.jpg
pdftoppm -jpeg -r 100 /tmp/deck.pdf /tmp/aosis-slide
ls -1 /tmp/aosis-slide-*.jpg
```

Inspecter chaque image, surveiller :

| Symptôme | Correction |
|---|---|
| `hero_stat value` > moitié de slide | Raccourcir (passer "mois" / "M€" dans le `label`) |
| Stats qui wrappent | Forme courte : "12 m" pas "12 mois", unité dans le label |
| Items de matrix qui débordent | Cap 3 / quadrant, items 5-6 mots max |
| Roadmap labels qui se chevauchent | Réduire à 5 milestones max |
| Funnel value column qui déborde | Garder `value` court ("85" pas "85 reports validés") |
| Sémantique `highlight` de chart | `"min"` quand petit = bien, `"max"` quand grand = bien |

Règle de fer : corriger **dans la spec JSON**, jamais en post-éditant le `.pptx`. **Une seule passe** fix-and-verify sauf nouveau défaut visible.

### 8.2 QA contenu — chasse aux placeholders

```bash
extract-text /mnt/user-data/outputs/deck.pptx \
  | grep -iE "\bx{3,}\b|lorem|\bTODO|\[insert|\[à remplir"
```

---

## 9. Ce que le skill ne fait PAS

- **N'altère pas** les masters, footers, ou theme du template.
- **N'ajoute pas** de fonds custom, gradients, ou polices.
- **N'insère pas** le logo manuellement (déjà sur chaque slide via le master).
- Pour des **visuels exotiques** (diagrammes custom hors catalogue, charts animés, vidéos embarquées) : hors scope. La consigne est de produire une image statique externe (matplotlib, mermaid, à la main) que l'utilisateur drope dans un slide `content` ou `image_hero`.

---

## 10. Livraison

- Sauvegarder le `.pptx` final dans `/mnt/user-data/outputs/`.
- Appeler `present_files` avec son chemin.
- Une ligne de résumé (nombre de slides + layouts clés utilisés). Pas de postambule long — le fichier parle pour lui-même.

---

## 11. Exemple complet de spec JSON

Repris du SKILL.md, illustrant la diversité des layouts dans un seul deck :

```json
{
  "cover": {
    "title": "Refonder le reporting risque",
    "ref":   "Mai 2026"
  },
  "slides": [
    {
      "layout": "hero_stat",
      "title":  "L'AMBITION",
      "value":  "-75%",
      "label":  "C'est le temps de production que nous allons reprendre à votre plateforme actuelle",
      "context": "De 8h à 2h par cycle, en 12 mois",
      "supporting": [
        "BCBS 239 conforme par construction",
        "Lineage bout-en-bout traçable"
      ]
    },
    {
      "layout": "big_idea",
      "title":  "NOTRE CONVICTION",
      "idea":   "Refonder une plateforme de reporting risque n'est pas un projet IT — c'est une transformation des pratiques de production de la donnée.",
      "supports": [
        {"title": "Maîtriser le lineage",       "detail": "Avant tout autre arbitrage."},
        {"title": "Choisir la valeur par lots", "detail": "Plutôt qu'un big-bang risqué."}
      ],
      "attribution": "Direction AOSIS"
    },
    {
      "layout": "matrix_2x2",
      "title":  "Cartographie des chantiers identifiés",
      "x_axis": {"label": "Effort de mise en œuvre", "low": "Faible", "high": "Élevé"},
      "y_axis": {"label": "Impact business",         "low": "Faible", "high": "Élevé"},
      "quadrants": {
        "top_left":     {"title": "Quick wins",             "items": ["Refactor batchs critiques"]},
        "top_right":    {"title": "Chantiers stratégiques", "items": ["Refonte data lineage", "Migration moteur"]},
        "bottom_left":  {"title": "Hygiène technique",      "items": ["Documentation"]},
        "bottom_right": {"title": "À deprioriser",          "items": ["Refonte UI legacy"]}
      }
    },
    {
      "layout": "roadmap",
      "title":  "Le chemin sur 12 mois",
      "milestones": [
        {"date": "Juin '26", "name": "Audit",         "detail": "Cartographie + quick wins"},
        {"date": "Août '26", "name": "Conception",    "detail": "Architecture cible validée"},
        {"date": "Nov '26",  "name": "First release", "detail": "Premier lot en production"},
        {"date": "Mars '27", "name": "Build complet", "detail": "Modules livrés"},
        {"date": "Juin '27", "name": "Bascule",       "detail": "Plateforme historique éteinte"}
      ]
    },
    {
      "layout": "chart",
      "title":  "La trajectoire de gains, mois après mois",
      "chart": {
        "type": "line",
        "labels": ["T0", "T+3", "T+6", "T+9", "T+12"],
        "series": [
          {"name": "Temps de production (h)", "values": [8, 7.5, 6.5, 4, 2]},
          {"name": "Couverture BCBS (%)",     "values": [60, 65, 80, 95, 100]}
        ]
      },
      "commentary": ["Premiers gains à T+3", "Convergence à T+12"]
    },
    {
      "layout": "quote",
      "text":   "Nous ne livrons pas une plateforme. Nous livrons une nouvelle façon de produire de la donnée.",
      "author": "Direction AOSIS"
    }
  ],
  "closing": true
}
```

---

## 12. Référence rapide — cheat sheet

### 12.1 Liste exhaustive des `layout` valides
`cover`, `section`, `closing`, `text`, `content`, `hero_stat`, `big_idea`, `matrix_2x2`, `swot`, `pyramid`, `funnel`, `roadmap`, `dashboard`, `org_chart`, `agenda`, `stat_grid`, `timeline`, `cards`, `comparison`, `chart`, `process`, `quote`, `image_hero`.

### 12.2 Limites dimensionnelles à mémoriser
| Élément | Limite |
|---|---|
| `hero_stat.value` | ≤ 7 caractères |
| `stat_grid.value` | ≤ 6 caractères |
| `matrix_2x2` items | ≤ 4 / quadrant |
| `swot` items | ≤ 3 / quadrant |
| `pyramid.levels` | 2 à 5 |
| `funnel.stages` | 3 à 6 |
| `roadmap.milestones` | 2 à 6 (5 recommandé pour éviter collisions) |
| `timeline.phases` | 2 à 6 |
| `cards.cards` | ≤ 8 |
| `cards.columns` | 2 / 3 / 4 |
| `agenda.items` | ≤ 6 |
| `dashboard.stats` | ≤ 4 |
| `org_chart.reports` | ≤ 5, members ≤ 3 chacun |
| `big_idea.supports` | ≤ 5 |
| `comparison` items | 4-5 / côté (sweet spot) |

### 12.3 Workflow CLI résumé
```bash
# 1. Écrire le JSON dans /tmp/deck_spec.json
# 2. Lancer le build
python aosis-deck-builder/scripts/build_deck.py /tmp/deck_spec.json /mnt/user-data/outputs/deck.pptx

# 3. QA visuel
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless \
  --convert-to pdf /mnt/user-data/outputs/deck.pptx --outdir /tmp/
pdftoppm -jpeg -r 100 /tmp/deck.pdf /tmp/aosis-slide

# 4. QA contenu
extract-text /mnt/user-data/outputs/deck.pptx \
  | grep -iE "\bx{3,}\b|lorem|\bTODO|\[insert|\[à remplir"
```

---

## 13. Comment Claude active ce skill

Le `description` du frontmatter YAML de `SKILL.md` agit comme **prompt de routage**. Quand l'utilisateur mentionne PowerPoint / pptx / deck / slides / présentation / proposition / restitution / CODIR dans un contexte AOSIS, Claude charge le skill, lit SKILL.md, et suit le workflow :

1. Planifier la narration (vu en section 5).
2. Composer la spec JSON (vu en sections 6 & 11).
3. Appeler `build_deck.py`.
4. Lancer le QA visuel et contenu.
5. Livrer dans `/mnt/user-data/outputs/`.

Le skill est explicitement étiqueté comme **toujours préférer** à un éventuel skill `pptx` générique sur ce projet : chaque deck AOSIS doit passer par lui pour rester branded.
