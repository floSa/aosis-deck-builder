# JSON Spec — Field-by-Field Reference

The skill consumes a single JSON specification. This file documents its structure, layout by layout.

For a high-level view of **which layout to pick**, see [`layouts.md`](layouts.md). For visual QA after building, see [`qa.md`](qa.md).

---

## Root structure

```json
{
  "cover":   { "title": "...", "ref": "..." },
  "slides":  [ /* ordered array of slide objects */ ],
  "closing": true
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `cover` | object | required | The deck's first slide. `title` (string) and `ref` (string, ~10 chars). |
| `slides` | array | required | Ordered list of slide objects. Each must include a `layout` key matching one of the 23 valid layout names. |
| `closing` | bool | optional (default `true`) | Append the AOSIS closing slide. Set to `false` to omit. |

---

## General conventions

- Every slide object **must** have a `layout` key. Valid values : `cover`, `section`, `closing`, `text`, `content`, `hero_stat`, `big_idea`, `matrix_2x2`, `swot`, `pyramid`, `funnel`, `roadmap`, `dashboard`, `org_chart`, `agenda`, `stat_grid`, `timeline`, `cards`, `comparison`, `chart`, `process`, `quote`, `image_hero`.
- Most slides have a `title` (string) — this is the **action title** (cf. SKILL.md Three Golden Rules § 3).
- Image fields (`image`) must be **absolute paths** on disk readable by the Python process.
- Colour controls (`accent: "orange" | "navy"`) appear on a few layouts — they pick between the two AOSIS accents.

---

## Full example

The example below illustrates 12 different layouts in a single coherent deck — use it as a template to bootstrap a new spec.

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
        {"title": "Maîtriser le lineage",     "detail": "Avant tout autre arbitrage."},
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
        "top_left":     {"title": "Quick wins",          "items": ["Refactor batchs critiques"]},
        "top_right":    {"title": "Chantiers stratégiques", "items": ["Refonte data lineage", "Migration moteur"]},
        "bottom_left":  {"title": "Hygiène technique",   "items": ["Documentation"]},
        "bottom_right": {"title": "À deprioriser",       "items": ["Refonte UI legacy"]}
      }
    },

    {
      "layout": "funnel",
      "title":  "Du chantier à la valeur produite",
      "stages": [
        {"name": "Périmètre initial",  "value": "120 reports", "detail": "À l'audit"},
        {"name": "Périmètre validé",   "value": "85",          "detail": "Après priorisation"},
        {"name": "Refondus",           "value": "65",          "detail": "Au build"},
        {"name": "Industrialisés",     "value": "65",          "detail": "100% en run"}
      ]
    },

    {
      "layout":     "roadmap",
      "title":      "Le chemin sur 12 mois",
      "milestones": [
        {"date": "Juin '26",  "name": "Audit",         "detail": "Cartographie + quick wins"},
        {"date": "Août '26",  "name": "Conception",    "detail": "Architecture cible validée"},
        {"date": "Nov '26",   "name": "First release", "detail": "Premier lot en production"},
        {"date": "Mars '27",  "name": "Build complet", "detail": "Modules livrés"},
        {"date": "Juin '27",  "name": "Bascule",       "detail": "Plateforme historique éteinte"}
      ]
    },

    {
      "layout": "stat_grid",
      "title":  "Ce que nous engageons",
      "stats": [
        {"value": "1,2 M€", "label": "Investissement total HT"},
        {"value": "6",      "label": "Consultants dédiés"},
        {"value": "12 m",   "label": "Pour atteindre la cible"},
        {"value": "100%",   "label": "Couverture BCBS livrée"}
      ]
    },

    {
      "layout":  "timeline",
      "title":   "Approche en 4 phases",
      "phases": [
        {"name": "Audit",      "duration": "6 sem",  "detail": "Cartographie et quick wins"},
        {"name": "Conception", "duration": "8 sem",  "detail": "Architecture et choix techno"},
        {"name": "Build",      "duration": "6 mois", "detail": "Développement itératif"},
        {"name": "Run",        "duration": "4 mois", "detail": "Bascule progressive"}
      ]
    },

    {
      "layout":  "cards",
      "title":   "L'équipe que nous mobilisons",
      "columns": 3,
      "cards": [
        {"badge": "01", "title": "Directeur de mission", "body": "10 ans BFI, pilotage."},
        {"badge": "02", "title": "Architecte data",     "body": "Conception cible."},
        {"badge": "03", "title": "3 data engineers",    "body": "Build et industrialisation."}
      ]
    },

    {
      "layout": "comparison",
      "title":  "Le saut que nous proposons",
      "left":  {"title": "Aujourd'hui", "subtitle": "(2014)",      "items": ["8h", "40+ batchs"]},
      "right": {"title": "Cible",       "subtitle": "(T+12 mois)", "items": ["2h", "Orchestré"]}
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
    },

    {
      "layout":   "image_hero",
      "image":    "/abs/path/to/team-photo.jpg",
      "title":    "Une équipe qui s'engage",
      "subtitle": "Paris · Lyon · Toulouse · Aix"
    }
  ],
  "closing": true
}
```

---

## Layout-specific field reference

### `hero_stat`
`value` (the giant number — string, e.g. `"75%"`, `"1,2 M€"`, `"12 m"`), `label` (action sentence under the number), optional `context` (small gray secondary line), optional `supporting` (list of bullet strings shown on the right with orange tick marks). Keep `value` ≤ 7 characters for max impact — anything longer auto-shrinks.

### `big_idea`
`idea` (the bold statement — 1-3 sentences max), optional `title` (eyebrow tag at the top — render it in UPPERCASE for an editorial feel), optional `attribution` (small tag in orange uppercase under the idea), optional `supports` (list of strings, or list of `{title, detail}` for richer entries — max 5).

### `matrix_2x2`
`x_axis` and `y_axis`, each `{label, low, high}`. `quadrants` is `{top_left, top_right, bottom_left, bottom_right}`, each with `title` and `items` list. Convention : the top-right quadrant is the "star" — put the strategic priority there. Cap at 4 items per quadrant.

### `swot`
`strengths`, `weaknesses`, `opportunities`, `threats`, each `{title, items}`. Cap at **3 items per quadrant** — the cells are not as roomy as `matrix_2x2`. Use this only for classic SWOT; for anything else, use `matrix_2x2`.

### `pyramid`
`levels` list, 2-5 entries, listed **bottom-to-top** by default (base first, apex last). Set `inverted: true` to flip when the narrative is top-down. The apex (or base, if inverted) is highlighted in orange. Each level : `name` (rendered inside) and optional `detail` (rendered to the right).

### `org_chart`
Two levels max. `leader` = `{name, role}`. `reports` is a list of up to 5 entries, each `{name, role, members?}` where `members` is an optional list of up to 3 names rendered as a stack under the report's box. Keep names + roles concise (≤ 25 chars combined per line) so the boxes don't overflow.

### `funnel`
`stages` list, 3 to 6 entries. Each : `name`, optional `value` (rendered to the right of the funnel in big type), optional `detail` (small gray text under the value). The last stage is highlighted in orange to suggest the "conversion".

### `roadmap`
`milestones` list, 2 to 6 entries. Each : `date` (short — `"Juin '26"`, `"Q3 2026"`), `name` (the milestone label), optional `detail` (one-line explanation). Labels alternate above/below the line to avoid collisions.

### `stat_grid`
1 to 4 stats. Each : `value`, `label`, optional `accent: "orange"|"navy"`. Optional `footnote`. Keep `value` ≤ 6 chars.

### `dashboard`
Editorial mix of stats and a chart. `stats` is a list of up to 4 entries (`{value, label}` — restrained styling, no big colored boxes). `chart` is the same as the standalone `chart` layout's spec; `chart_title` is an optional small label rendered above the chart in uppercase. Either `stats` or `chart` can be omitted.

### `agenda`
Numbered list, up to 6 items. Each : `title` (the agenda heading) and optional `detail` (rendered in orange on the right of the same row — typically a timing or duration). Use as a deck's second slide to set expectations.

### `timeline`
`phases`, 2-6. Each : `name`, `duration`, optional `detail` rendered under the box.

### `cards`
List `cards`, each `{title, body, badge?}`. Optional top-level `columns` (2/3/4). Cap at 6-8 cards.

### `comparison`
`left`/`right`, each `{title, subtitle?, items}`. 4-5 items per side is the sweet spot.

### `chart`
`chart` object with `type` (`bar`, `barh`, `line`, `pie`), `labels`, `data` (single series) or `series` (multi-series). Optional `ylabel`, `xlabel`, `highlight` (`"max"` / `"min"` / int index). Top-level `commentary` (list of bullets) places bullets next to the chart instead of letting it fill the slide.

### `quote`
`text` (required), `author` (optional, rendered in orange uppercase). One idea per slide.

### `image_hero`
`image` (absolute path), optional `title` / `subtitle` shown on a navy band at the bottom.

### `cover` / `section`
`title` (string, required), `ref` (string, optional, ~10 characters — date or reference shown in the top-right orange callout). `section` renders identically to `cover` and is used as a divider between major parts of the deck.

### `closing`
No fields. The closing slide is appended automatically at the end of the deck. To omit it, set `"closing": false` at the spec root (not in a slide object).

### `text`
`title` (string), `bullets` (list of strings, or list of `{text, level}` objects where `level` is 0-4 for indented bullets).

### `content`
`title` (string), `bullets` (same shape as `text`), `image` (absolute path to a screenshot/photo shown next to the bullets).

### `process`
`title` (string), `steps` (list of step objects). Each step is rendered as a numbered orange circle with title and optional detail in a vertical sequence.

---

## Template-based layouts (Chantier 7)

These layouts source their visual design from `assets/exhibits.pptx` and fill `{{...}}` placeholders from the spec.

### Common fields (all template-based layouts)

| Field | Type | Notes |
|---|---|---|
| `eyebrow` | string | Small uppercase tag at top-left (e.g., `"EXECUTIVE SUMMARY"`). Optional — omitted shapes are removed. |
| `title` | string | Action title in big navy. |
| `takeaway` | string | One-line key insight in orange-bar banner. Optional. |
| `source` | string | Footnote at bottom-left (e.g., `"Source: AOSIS analysis"`). Optional. |
| `image` | string | Absolute path to an image, replaces `{{IMAGE}}` shapes. Optional. |
| `items` | list | List of objects feeding the `{{REPEAT_ITEM}}` group of the layout. Schema varies per layout (see below). |

### `executive_summary`

```json
{
  "layout": "executive_summary",
  "eyebrow": "EXECUTIVE SUMMARY",
  "title": "Three convictions that frame our proposal",
  "takeaway": "Decouple, refactor, industrialise",
  "source": "Source: AOSIS analysis, May 2026",
  "items": [
    {"eyebrow": "PILLAR 1", "title": "Decouple storage from compute",
     "bullets": "• First bullet\n• Second bullet"},
    {"eyebrow": "PILLAR 2", "title": "Refactor fragile data models",
     "bullets": "• First bullet\n• Second bullet"},
    {"eyebrow": "PILLAR 3", "title": "Industrialise delivery",
     "bullets": "• First bullet\n• Second bullet"}
  ]
}
```

> Note: as of 2026-05-17 the user has not yet renamed the template's column group to `{{REPEAT_ITEM}}` — only the first column renders. Once the user polishes the slide (renames `Groupe 19` → `{{REPEAT_ITEM}}`), all N columns will render dynamically.

### `process_steps`

```json
{
  "layout": "process_steps",
  "eyebrow": "PROCESS",
  "title": "Four steps to deliver the target state",
  "source": "Source: AOSIS methodology",
  "items": [
    {"title": "Audit",  "text": "Map the current state"},
    {"title": "Design", "text": "Define target architecture"},
    {"title": "Build",  "text": "Implement iteratively"},
    {"title": "Run",    "text": "Cutover and stabilise"}
  ]
}
```

`{{ITEM_NUMBER}}` auto-fills with the 0-padded index (`01`, `02`, …) if `number` is not in the item.

### `roadmap_styled`

```json
{
  "layout": "roadmap_styled",
  "eyebrow": "TIMELINE",
  "title": "The path on 12 months",
  "source": "Source: AOSIS plan",
  "items": [
    {"date": "Jun '26", "milestone": "Audit"},
    {"date": "Aug '26", "milestone": "Design validated"},
    {"date": "Nov '26", "milestone": "First model in prod"}
  ]
}
```

Item keys mirror the placeholders inside the template's REPEAT_ITEM group: `{{ITEM_DATE}}` ← `item.date`, `{{ITEM_MILESTONE}}` ← `item.milestone`.

### `next_steps`

```json
{
  "layout": "next_steps",
  "eyebrow": "NEXT STEPS",
  "title": "The four actions to launch this week",
  "source": "Source: AOSIS action plan",
  "items": [
    {"action": "Kickoff workshop", "owner": "Director",  "date": "12/06/26"},
    {"action": "Architecture review", "owner": "Architect", "date": "15/06/26"}
  ]
}
```

### `framework_3cards`

```json
{
  "layout": "framework_3cards",
  "eyebrow": "FRAMEWORK",
  "title": "Three pillars",
  "icons": ["mdi:account-tie", "mdi:school", "mdi:tools"],
  "items": [
    {"title": "Quick wins",      "bullets": "• Refactor batches\n• Index optimization"},
    {"title": "Strategic moves", "bullets": "• Engine migration\n• CDC pipelines"},
    {"title": "Tech hygiene",    "bullets": "• Cleanup\n• Documentation"}
  ]
}
```

The optional `icons` array lists [Iconify](https://icon-sets.iconify.design/)
identifiers (`<prefix>:<name>`). One icon per item, in the same order. The
moteur fetches each SVG from the Iconify API, recolors it navy, and overlays
it on the `{{ITEM_ICON}}` shape. Failure (network down, cairosvg missing,
unknown icon) is silent — the card simply renders without an icon. See
[`icons_suggested.md`](icons_suggested.md) for a curated catalogue of 40+
identifiers ranked by consulting context.

### `kpi_with_chart`

```json
{
  "layout": "kpi_with_chart",
  "title": "Three indicators over time",
  "source": "Source: AOSIS analysis",
  "kpis": [
    {"label": "Coverage", "value": "85 %"},
    {"label": "Latency",  "value": "30 m"},
    {"label": "Cost",     "value": "−40 %"}
  ],
  "chart": { "type": "bar", "labels": ["Q1","Q2","Q3","Q4"], "values": [120,145,132,168] }
}
```

The template's REPEAT_ITEM uses `{{KPI_LABEL}}` and `{{KPI_VALUE}}` (Chantier 9
extended `ITEM_PLACEHOLDER_RE` to accept the `KPI_` prefix). Provide one
`{label, value}` dict per KPI; the moteur substitutes the texts in each card.

### Auto-shrink for numeric values, dates, owners

Pour les clés `value`, `date`, `action`, `owner` (typiquement des valeurs courtes
mais à unité variable comme `4.2 M€` ou `1er septembre 2026`), le moteur
auto-réduit la taille de police par paliers de 2pt jusqu'à ce que le texte
tienne sur la largeur de la shape (avec un plancher à 10pt). Les autres clés
(`title`, `text`, `bullets`, `milestone`) gardent leur taille originale et
peuvent wrapper sur plusieurs lignes via `<a:spAutoFit/>`.

### `matrix_2x2_styled` — format complet

```json
{
  "layout": "matrix_2x2_styled",
  "title": "Priorisation",
  "x_axis": {"label": "Effort"},
  "y_axis": {"label": "Impact"},
  "quadrants": {
    "top_left":     {"title": "Quick wins",   "items": ["A", "B"]},
    "top_right":    {"title": "Strategic",    "items": ["C", "D"]},
    "bottom_left":  {"title": "Hygiene",      "items": ["E"]},
    "bottom_right": {"title": "Deprioritise", "items": ["F"]}
  }
}
```

Le moteur accepte `items` ET `bullets` comme alias dans chaque quadrant
(Chantier 10). Les listes sont rendues sous forme de bullets `• ...`.

**Maximum 3 bullets par quadrant** (Chantier 11). Au-delà, les items
supplémentaires sont ignorés et un warning est imprimé sur stderr :
`matrix_2x2_styled: quad 'top_left' has 5 bullets, truncated to 3`. Les
bullets sont ancrés en bas-gauche du quadrant (anchor=b) et auto-réduits
en taille si besoin (jusqu'à plancher 10pt).

## Images automatiques (Pexels / Lorem Picsum)

Pour les layouts ayant un placeholder `{{IMAGE}}` (agenda_diagonal,
section_diagonal, closing_diagonal, et tout futur layout en exposant un),
le moteur télécharge automatiquement une photo stock au runtime. Activé
par défaut, désactivable via :

```bash
python build_deck.py spec.json out.pptx --no-images
```

Ordre de résolution du mot-clé pour chaque slide :
1. `spec.image` (chemin local) — si fourni, prioritaire (comportement legacy)
2. `spec.image_keyword` — mot-clé explicite (préférer l'anglais concret/visuel : `"cloud computing data center"`, `"team meeting whiteboard"`)
3. Mots-clés extraits du `spec.title` (stop words FR/EN filtrés)
4. Mot-clé par défaut selon le layout (`cover` → `"business technology"`, etc.)

Ordre de résolution du provider (Chantier 12) :
1. **Pexels API** si env var `PEXELS_API_KEY` exportée — endpoint `api.pexels.com/v1/search`, free tier 200 req/h, **automated use explicitly allowed by ToS**. Retourne des photos sémantiquement liées au keyword.
2. **Lorem Picsum** (`picsum.photos`, toujours dispo, no API key) — fallback. Seed déterministe (= keyword normalisé) mais photo aléatoire (pas de matching sémantique).

Échec silencieux si tous les providers échouent. Pour forcer une image
locale plutôt qu'un fetch :

```json
{"layout": "cover", "title": "...", "image": "/chemin/local/photo.jpg"}
```

## `data_table` (Chantier 15)

Tableau structuré dessiné dynamiquement sur la slide modèle `data_table`.

```json
{
  "layout": "data_table",
  "title": "Comparaison des 3 stratégies de migration",
  "source": "Analyse AOSIS — 30 missions",
  "table": {
    "headers": ["Stratégie", "Durée", "Coût", "Gain TCO", "Risque"],
    "rows": [
      ["Lift & Shift", "12-18 mois", "€",   "-8 à -15 %",  "Faible"],
      ["Replatform",   "18-24 mois", "€€",  "-20 à -30 %", "Modéré"],
      ["Refactor",     "30-48 mois", "€€€", "-35 à -50 %", "Élevé"]
    ],
    "highlight_column": 3,
    "highlight_row": 1
  }
}
```

| Champ | Type | Description |
|---|---|---|
| `headers` | `list[str]` (req., ≤ 6) | En-têtes de colonnes |
| `rows` | `list[list]` (req., ≤ 8) | Lignes de données ; chaque liste interne ≤ 6 cellules |
| `highlight_column` | `int` (optionnel, 0-based) | Met cette colonne en orange bold |
| `highlight_row` | `int` (optionnel, 0-based sur les données) | Fond orange clair sur cette ligne |

**Style appliqué automatiquement** :
- Headers : fond navy `#14163C`, texte blanc bold 11pt Arial
- Lignes data : alternance blanc / off-white `#FAFAF7`, texte navy 10pt Arial
- Première colonne : bold + alignement gauche
- Autres colonnes : alignement centré
- Largeurs : col 0 = 30 % de la largeur, autres équiréparties
- Auto-shrink (10→9→8pt + padding 6→5→4pt) si débordement vertical estimé

**Validation amont** : `len(headers) > 6` → `ValueError` ; `len(rows) > 8` → truncate + warning stderr ; cellule > 30 chars → warning stderr (risque de débordement).

## `canvas_blank` freeform composition (Chantier 14, durci au Chantier 15)

Mode freeform du layout `canvas_blank` activé dès que la spec contient `blocks: [...]`.

**Schéma général** :

```json
{
  "layout": "canvas_blank",
  "title": "Titre principal de la slide",
  "blocks": [ {...}, {...}, ... ]
}
```

Seuls `title` (rempli dans le placeholder `{{TITLE}}` du template) et `blocks` sont rendus. Les champs `eyebrow`, `takeaway`, `source` sont **ignorés** si les placeholders correspondants `{{EYEBROW}}`, `{{TAKEAWAY}}`, `{{SOURCE}}` ne sont pas présents dans le template (warning stderr).

### Types de blocks

#### `kpi_card`
```json
{"type": "kpi_card", "value": "87 %", "label": "saturation datacenter", "color": "orange"}
```
- `value` : chaîne courte (≤ 5 chars → 36pt, ≤ 8 chars → 28pt, sinon 22pt)
- `label` : forcé en UPPERCASE à l'affichage (10pt navy bold)
- `color` ∈ `orange|navy|green|red`, défaut `orange`

#### `bullets`
```json
{"type": "bullets", "items": ["Point A", "Point B", "Point C"]}
```
Max 5 items (tronqué silencieusement avec warning stderr au-delà). Puces orange, texte navy 12pt.

#### `text`
```json
{"type": "text", "content": "Un paragraphe libre, navy Arial 12pt, word-wrap activé."}
```

#### `image`
```json
{"type": "image", "keyword": "data center server room"}
{"type": "image", "path": "/abs/path/to/photo.jpg"}
```
Provider order : Pexels (si `PEXELS_API_KEY` configurée) → Lorem Picsum. Le `path` local prend la priorité s'il est fourni.

#### `chart`
```json
{"type": "chart", "chart_spec": {
  "type": "bar",
  "labels": ["Q1","Q2","Q3","Q4"],
  "values": [10, 20, 15, 25]
}}
```
Mêmes 8 types que `kpi_with_chart` (bar, barh, bar_stacked, line, donut, pie, combo, waterfall). Voir [Charts in kpi_with_chart layout](#charts-in-kpi_with_chart-layout) pour le détail.

#### `quote`
```json
{"type": "quote",
 "content": "La phrase de citation, entre guillemets français.",
 "author": "Prénom Nom — Fonction"}
```

### Mise en page automatique

| N blocks | Disposition |
|---:|---|
| 1 | plein cadre |
| 2 | 2 colonnes (50/50) |
| 3 | 3 colonnes (33/33/33) |
| 4 | grille 2×2 |
| 5 | 3 colonnes en haut, 2 colonnes en bas |
| 6 | grille 3×2 |
| 7+ | tronqué à 6, warning stderr |

**Cas spécial asymétrique** : si exactement **un seul** bloc est de type `image` ou `chart` parmi 2+ blocks → le visuel prend la moitié droite (45 % de la largeur), les autres blocks empilés verticalement à gauche.

### Limites de validation

| Champ | Limite | Comportement au dépassement |
|---|---|---|
| `title` | 120 chars | warning stderr |
| `takeaway` | 180 chars | warning stderr |
| `blocks` | 6 | tronqué + warning stderr |
| `bullets.items` | 5 | tronqué + warning stderr |

### Découpe diagonale automatique

Pour les layouts `cover`, `agenda_diagonal`, `section_diagonal`,
`closing_diagonal`, le moteur copie le `<a:custGeom>` du layout
PowerPoint vers la photo insérée (Chantier 12) — la photo est ainsi
découpée par la diagonale du design plutôt que d'apparaître en rectangle
plein masquant la diagonale.

### Image keywords — bonnes pratiques

L'extraction automatique de keyword depuis le `title` francophone produit
souvent des photos hors sujet ou trop littérales (« diagnostic actuel »
→ photo d'un dossier médical, « vision stratégique » → fond rose).
**Toujours fournir un `image_keyword` explicite** pour les slides à
image — c'est un coût rédactionnel marginal pour un gain visuel important.

Convention :
- **Anglais** (Pexels indexe surtout en anglais)
- **Concret et visuel** : décrire une SCÈNE (qui + où + quoi) plutôt qu'un concept abstrait
- **2 à 4 mots** : assez précis pour matcher, pas trop pour ne pas réduire le pool
- **Pas d'articles** (`the`, `a`, etc.) ni mots-charnières (`with`, `of`, …)

Exemples bons / mauvais :

| ❌ Mauvais (abstrait) | ✅ Bon (concret) |
|---|---|
| `strategy` | `business strategy meeting` |
| `infrastructure` | `data center server room` |
| `digital transformation` | `laptop modern office` |
| `growth` | `upward graph success` |
| `team` | `team collaboration desk` |
| `innovation` | `scientist laboratory` |
| `migration` | `cloud computing data center` |
| `process` | `engineers whiteboard planning` |
| `vision` | `business strategy whiteboard` |
| `excellence` | `award trophy ceremony` |
| `success` | `business handshake success` |

L'`image_keyword` est lu en priorité par le moteur — l'extraction depuis
le titre n'est utilisée que si la clé n'est pas présente.

### `comparison_before_after` — format complet

```json
{
  "layout": "comparison_before_after",
  "title": "Avant / Après",
  "takeaway": "Phrase de synthèse au-dessus",
  "before": {"title": "Aujourd'hui", "bullets": "8h par cycle\nManuel"},
  "after":  {"title": "Cible T+12",  "bullets": "2h par cycle\nAutomatisé"}
}
```

Les dicts `before` / `after` sont automatiquement flattenés en `before_title`,
`before_bullets`, `after_title`, `after_bullets` par le moteur (Chantier 10).
Si la clé `takeaway` est vide, le bandeau orange l'accompagnant peut être
groupé dans un `{{TAKEAWAY_GROUP}}` côté template — le moteur supprime alors
le groupe entier.

### `comparison_2cols`

```json
{
  "layout": "comparison_2cols",
  "title": "Option A vs Option B",
  "items": [
    {"title": "Option A", "bullets": "Court terme\nFaible risque"},
    {"title": "Option B", "bullets": "ROI long terme\nRisque modéré"}
  ]
}
```

Template à un seul `{{REPEAT_ITEM}}` avec distribution horizontale —
2 items donnent 2 cards side-by-side.

The `chart` key drives the matplotlib-rendered chart in the right half of
the slide. See **Charts in `kpi_with_chart` layout** below for the 8
supported types and their parameters.

## Charts in `kpi_with_chart` layout

The `chart` object is rendered by `chart_engine.render_chart_to_png()` and
inserted as an image at the `{{CHART_PLACEHOLDER}}` shape's position. The
brand palette is read live so a custom `--template` propagates.

Common keys (all types):

| key | required | description |
|---|---|---|
| `type` | yes | `"bar"`, `"barh"`, `"bar_stacked"`, `"line"`, `"donut"`, `"pie"`, `"combo"`, `"waterfall"` |
| `y_label` | no | Y-axis label (lowercased on render). Not used by donut/pie. |
| `x_label` | no | X-axis label. Not used by donut/pie. |

Type-specific keys:

### `bar` / `barh`
Vertical (`bar`) or horizontal (`barh`) bars, single series.
```json
{ "type": "bar",  "labels": ["Q1","Q2","Q3","Q4"], "values": [120,145,132,168] }
{ "type": "barh", "labels": ["FR","DE","IT","ES"], "values": [38,27,19,16] }
```

### `bar_stacked`
Vertical bars, multiple series stacked.
```json
{
  "type": "bar_stacked",
  "labels": ["Q1","Q2","Q3","Q4"],
  "series": [
    {"name": "Produit A", "values": [50,60,55,70]},
    {"name": "Produit B", "values": [70,85,77,98]}
  ]
}
```

### `line`
One or several line series. Each point is labelled with its value.
```json
{
  "type": "line",
  "labels": ["Jan","Fév","Mar","Avr","Mai"],
  "series": [
    {"name": "Réel",  "values": [100,105,112,120,128]},
    {"name": "Cible", "values": [100,110,120,130,140]}
  ]
}
```

### `donut`
Donut chart with optional centre text.
```json
{
  "type": "donut",
  "labels": ["Cloud","On-Prem","Hybrid"],
  "values": [45,30,25],
  "center_text": "100 %"
}
```

### `pie`
Pie chart (donut without the hole).
```json
{ "type": "pie", "labels": ["Acquis","En cours","Pipeline"], "values": [60,25,15] }
```

### `combo`
Bars + line on a secondary Y axis.
```json
{
  "type": "combo",
  "labels": ["Q1","Q2","Q3","Q4"],
  "bars": { "name": "Revenu",  "values": [120,145,132,168] },
  "line": { "name": "Marge %", "values": [25,28,26,31] }
}
```

### `waterfall`
Cumulative gain/loss; first and last bars are totals (navy), gains green,
losses red. Pass intermediate values as deltas OR as cumulative levels
(the renderer auto-detects).
```json
{
  "type": "waterfall",
  "labels": ["Start","Gain A","Gain B","Loss","End"],
  "values": [100,30,20,-15,135]
}
```

### `comparison_2cols` / `comparison_before_after`

The current templates have a single `{{REPEAT_ITEM}}` group. To produce two columns you can:
- duplicate the group in PowerPoint manually (recommended), or
- wait for the engine extension that handles paired REPEAT_ITEM (Chantier 8 candidate).

### `quote_callout`

```json
{
  "layout": "quote_callout",
  "eyebrow": "VOICE OF THE CLIENT",
  "title": "What stakeholders told us",
  "takeaway": "One-line takeaway",
  "quote_text": "The single sentence that captures the strategic stance.",
  "quote_attribution": "— STAKEHOLDER NAME, ROLE"
}
```

### `matrix_2x2_styled`

```json
{
  "layout": "matrix_2x2_styled",
  "eyebrow": "PRIORITISATION",
  "title": "Where to invest first",
  "quadrants": {
    "top_left":     {"title": "Quick wins",      "bullets": "• Item A"},
    "top_right":    {"title": "Strategic",       "bullets": "• Item B\n• Item C"},
    "bottom_left":  {"title": "Hygiene",         "bullets": "• Item D"},
    "bottom_right": {"title": "Deprioritise",    "bullets": "• Item E"}
  },
  "x_axis_label": "Effort",
  "y_axis_label": "Impact",
  "y_high": "High",
  "y_low": "Low"
}
```
