# Layout catalogue

Le skill expose **deux familles** de layouts :

1. **Template-based** (17) — sourcés depuis des slides nommées dans `assets/AOSIS_template.pptx`. Découpés au pixel par le designer, ils héritent automatiquement de la charte (diagonale, logo, footer, masters). À privilégier.
2. **Code-based** (14) — dessinés programmatiquement par `scripts/build_deck.py`. Plus anciens, conservés pour rétrocompatibilité mais d'un rendu moins consulting. À utiliser comme fallback uniquement.

Pour le schéma JSON des champs accepté par chaque layout, voir [`json-schema.md`](json-schema.md).

---

## Comment choisir un layout

Pour chaque slide à générer :

1. Identifie le **type de message** à faire passer (donnée chiffrée, comparaison, planning, etc.)
2. Trouve le **layout dont le domaine correspond** dans la liste ci-dessous
3. Vérifie que ton contenu **rentre dans la composition** et **respecte les limites techniques**
4. Si aucun layout ne convient parfaitement, utilise `canvas_blank` (cf. fiche dédiée) en respectant les règles AOSIS (palette, police, grammaire consulting)

**Priorité aux layouts template-based**. Les layouts code-based sont conservés pour rétrocompatibilité mais offrent un rendu moins consulting.

### Domaines

| Domaine | Layouts |
|---|---|
| Navigation | `cover`, `agenda_diagonal`, `section_diagonal`, `closing_diagonal`, `final_branding` |
| Synthèse | `executive_summary`, `framework_3cards`, `text_dense_3cols`, `big_idea`, `hero_stat` |
| Données chiffrées | `kpi_with_chart`, `chart`, `stat_grid`, `dashboard`, `funnel` |
| Comparaison | `comparison_2cols`, `comparison_before_after`, `matrix_2x2_styled`, `swot` |
| Planning | `roadmap_styled`, `next_steps`, `process_steps`, `process` |
| Process / pyramide | `pyramid`, `org_chart` |
| Citation | `quote_callout` |
| Liberté | `canvas_blank`, `content`, `text`, `cards`, `image_hero` |

---

# Layouts template-based

## `cover`

**Domaine** : Navigation

**Description** : Slide de couverture du deck. Grand titre centré sur la moitié gauche, pastille orange en parallélogramme en haut à droite portant la date / référence, sous-titre en bas. Pas d'image actuellement dans le template.

**Composition** : `{{TITLE}}`, `{{SUBTITLE}}`, `{{REF}}` (pastille date/réf). Le logo est inséré automatiquement par le slide master.

**Quand l'utiliser** : Toujours en première slide d'un deck client / interne, pour poser le titre principal de la présentation et son contexte (mois, version, destinataire).

**Quand ne pas l'utiliser** : Pour une seconde slide-titre intermédiaire — préférer `section_diagonal`.

**Limites techniques** : Pas de `{{IMAGE}}` placeholder aujourd'hui. Si le titre dépasse ~70 caractères, il wrap et peut chevaucher le sous-titre — viser ≤ 60 chars.

**Exemple JSON minimal** :
```json
{
  "layout": "cover",
  "title": "Migration vers le cloud",
  "subtitle": "Une feuille de route pour TechnoLog SA",
  "ref": "Mai 2026"
}
```

## `agenda_diagonal`

**Domaine** : Navigation

**Description** : Slide de sommaire. Liste verticale de sections numérotées (01, 02, …) sur la moitié gauche, photo (auto-fetched) découpée par la diagonale sur la moitié droite.

**Composition** : `{{TITLE}}` (souvent "SOMMAIRE"), `{{REPEAT_ITEM}}` (groupe contenant `{{ITEM_NUMBER}}` + `{{ITEM_TITLE}}`), `{{IMAGE}}` (placeholder photo diagonale).

**Quand l'utiliser** : En 2e slide juste après la cover, pour annoncer la structure du deck (3 à 7 sections). Le moteur **pagine automatiquement** au-delà de 7 items (continuité de numérotation 08, 09… sur page 2).

**Quand ne pas l'utiliser** : Pour un sommaire à 2-3 sections (trop léger pour cette slide pleine). Pour un planning daté avec milestones, préférer `roadmap_styled`.

**Limites techniques** : 7 items max par page (pagination auto au-delà). Numérotation auto (01-07 puis 08-14).

**Exemple JSON minimal** :
```json
{
  "layout": "agenda_diagonal",
  "title": "Sommaire",
  "image_keyword": "business meeting overview",
  "items": [
    {"title": "Diagnostic"},
    {"title": "Vision"},
    {"title": "Roadmap"}
  ]
}
```

## `section_diagonal`

**Domaine** : Navigation

**Description** : Slide d'intercalaire entre deux grandes parties du deck. Numéro de section géant à gauche, titre de la partie, photo découpée par la diagonale à droite.

**Composition** : `{{TITLE}}`, `{{ITEM_NUMBER}}` (numéro de section, ex. "01"), `{{IMAGE}}`.

**Quand l'utiliser** : Pour structurer un deck en parties claires : Diagnostic → Vision → Plan → Next steps. Insérer une `section_diagonal` au début de chaque grande partie.

**Quand ne pas l'utiliser** : Pour un titre de slide ordinaire (utiliser le `{{TITLE}}` standard d'un autre layout).

**Limites techniques** : Le `item_number` est une chaîne libre (`"01"`, `"02"`), à fournir explicitement dans le spec — pas d'auto-incrément côté moteur (champ top-level, pas un REPEAT_ITEM).

**Exemple JSON minimal** :
```json
{
  "layout": "section_diagonal",
  "title": "Diagnostic du SI actuel",
  "item_number": "01",
  "image_keyword": "data center server room"
}
```

## `canvas_blank`

**Domaine** : Liberté

**Description** : Canevas freeform avec composition automatique. Deux modes : (1) **vide pur** (juste un titre) si la spec ne contient pas de `blocks` — ancien comportement ; (2) **freeform composé** (Chantier 14, durci au Chantier 15) si `blocks: [...]` est fourni, le titre est filled dans le `{{TITLE}}` du template (position/police héritées) et les blocks sont disposés sur une grille intelligente sous le titre.

**Composition** :
- Mode vide : `{{TITLE}}` du template uniquement
- Mode freeform : `{{TITLE}}` (rempli par le simple-placeholder processor, position+police+couleur du template) + `blocks: [...]` (disposés dans la zone disponible sous le titre)

> ⚠️ **Strict template compliance** (Chantier 15) : le moteur ne dessine plus d'eyebrow/takeaway/source par-dessus le template. Si la spec contient ces champs mais que le template n'a pas de `{{EYEBROW}}` / `{{TAKEAWAY}}` / `{{SOURCE}}` placeholder, ils sont **ignorés** (warning stderr `canvas_blank: eyebrow ignored — no {{EYEBROW}} placeholder in template`). Pour les activer, il faut ajouter le placeholder correspondant dans `assets/AOSIS_template.pptx` slide 4 directement dans PowerPoint — le simple processor s'en charge ensuite automatiquement.

**Blocs supportés** (mode freeform) :
- `kpi_card` : `{value, label, color}` — chiffre géant + label uppercase. `color` ∈ `orange|navy|green|red` (orange par défaut)
- `bullets` : `{items: [...]}` — liste à puces orange, max 5 items
- `text` : `{content}` — paragraphe simple navy 12pt
- `image` : `{keyword}` (Pexels/Picsum auto) ou `{path}` (chemin local)
- `chart` : `{chart_spec: {type, labels, ...}}` — chart matplotlib (8 types via chart_engine)
- `quote` : `{content, author}` — citation italique + attribution orange UPPERCASE

**Mise en page automatique** :
- 1 block → plein cadre
- 2 blocks → 2 colonnes
- 3 blocks → 3 colonnes
- 4 blocks → grille 2×2
- 5 blocks → 3 en haut + 2 en bas (asymétrique)
- 6 blocks → grille 3×2
- **Asymétrique image/chart** : si exactement UN block est `image` ou `chart` parmi 2+ blocks, ce visuel prend la moitié droite (45 %), les autres blocks empilés à gauche

**Quand l'utiliser** :
- Slide de diagnostic combinant KPI + bullets explicatifs
- Slide de synthèse avec chart + take-aways autour
- Slide-citation enrichie d'une photo de contexte
- Tout cas hybride où un seul autre layout n'aurait pas couvert le mix

**Quand ne pas l'utiliser** : Dès qu'un layout dédié existe — `executive_summary` pour 3 piliers, `kpi_with_chart` pour 3 KPI + 1 chart, `framework_3cards` pour 3 cartes thématiques. Le freeform est puissant mais reste moins « ciselé » qu'un template spécifique.

**Limites techniques** :
- Max **6 blocks** (au-delà, tronqué + warning stderr)
- Max **5 items** par bloc `bullets` (idem)
- `title` > 120 chars → warning (peut wrapper)
- `takeaway` > 180 chars → warning

**Exemple JSON minimal (mode vide, ancien comportement)** :
```json
{"layout": "canvas_blank", "title": "Schéma d'architecture cible"}
```

**Exemple JSON freeform — 4 KPI cards en grille 2×2** :
```json
{
  "layout": "canvas_blank",
  "eyebrow": "DIAGNOSTIC",
  "title": "Quatre KPI clés du diagnostic",
  "takeaway": "Le SI atteint plusieurs limites simultanément.",
  "blocks": [
    {"type": "kpi_card", "value": "87 %", "label": "saturation"},
    {"type": "kpi_card", "value": "23 j", "label": "provisionnement"},
    {"type": "kpi_card", "value": "47",   "label": "incidents"},
    {"type": "kpi_card", "value": "62 %", "label": "effort DSI"}
  ],
  "source": "Audit AOSIS"
}
```

**Exemple JSON freeform — bullets + image (asymétrique)** :
```json
{
  "layout": "canvas_blank",
  "title": "Bullets à gauche, image à droite",
  "blocks": [
    {"type": "bullets", "items": ["Point A", "Point B", "Point C"]},
    {"type": "image", "keyword": "data center server room"}
  ]
}
```

## `executive_summary`

**Domaine** : Synthèse

**Description** : Slide de synthèse en 3 colonnes, chaque colonne portant un numéro (01/02/03), un titre court, et 2-4 bullets. Bandeau orange "takeaway" optionnel en haut.

**Composition** : `{{TITLE}}`, `{{TAKEAWAY}}` (phrase de synthèse, optionnel), `{{REPEAT_ITEM}}` (groupe = bar verticale + `{{ITEM_NUMBER}}` + `{{ITEM_TITLE}}` + `{{ITEM_BULLETS}}`), `{{SOURCE}}`.

**Quand l'utiliser** : Slide de synthèse exécutive en début ou fin de section. Format classique consulting : 3 messages clés. Excellent pour "Diagnostic / Recommandation / Engagement".

**Quand ne pas l'utiliser** : Pour 2 messages seulement (utiliser `comparison_2cols`). Pour > 4 messages (utiliser `text_dense_3cols` ou plusieurs slides).

**Limites techniques** : 3 colonnes optimales (le template). Au-delà, la lisibilité chute. Bullets : 3-4 par colonne max, 8 mots max par bullet.

**Exemple JSON minimal** :
```json
{
  "layout": "executive_summary",
  "title": "Synthèse en 3 messages",
  "takeaway": "Une transformation mesurable en 22 mois.",
  "source": "Source: AOSIS",
  "items": [
    {"title": "Le SI atteint ses limites", "bullets": "Disponibilité 96.4 %\n47 incidents"},
    {"title": "Replatform AWS recommandé", "bullets": "Gain TCO -26 %\n22 mois d'exécution"},
    {"title": "AOSIS accompagne", "bullets": "Cadrage + exécution\n4 consultants"}
  ]
}
```

## `kpi_with_chart`

**Domaine** : Données chiffrées

**Description** : 3 cartes KPI empilées sur la moitié gauche (label + valeur en grand orange/navy), chart matplotlib généré dynamiquement sur la moitié droite. Synthétise des chiffres clés et leur évolution.

**Composition** : `{{TITLE}}`, `{{REPEAT_ITEM}}` (groupe = `kpi_card` background + `{{KPI_LABEL}}` + `{{KPI_VALUE}}`), `{{CHART_PLACEHOLDER}}` (rempli par chart_engine), `{{SOURCE}}`.

**Quand l'utiliser** : Pour mettre en avant 3 KPI chiffrés ET montrer leur évolution / décomposition graphique. Ex: TCO actuel + cible + économie + courbe d'évolution.

**Quand ne pas l'utiliser** : Pour 1 seul KPI (utiliser `hero_stat`). Pour > 3 KPI (utiliser `stat_grid` ou plusieurs slides). Sans chart pertinent (utiliser `executive_summary`).

**Limites techniques** : 3 KPI optimaux (le template est calibré). Les valeurs longues type "1 234 567 K€" sont auto-shrunk. 8 types de chart supportés : `bar`, `barh`, `bar_stacked`, `line`, `donut`, `pie`, `combo`, `waterfall` (cf. [`json-schema.md`](json-schema.md#charts-in-kpi_with_chart-layout)).

**Exemple JSON minimal** :
```json
{
  "layout": "kpi_with_chart",
  "title": "TCO trajectoire 2025-2029",
  "source": "Source: AOSIS analysis",
  "kpis": [
    {"label": "TCO 2025",    "value": "4.2 M€"},
    {"label": "Cible 2028",  "value": "3.1 M€"},
    {"label": "Économie/an", "value": "1.1 M€"}
  ],
  "chart": {
    "type": "line",
    "labels": ["2025","2026","2027","2028","2029"],
    "series": [{"name": "TCO", "values": [4.2, 4.4, 3.8, 3.1, 2.9]}]
  }
}
```

## `comparison_2cols`

**Domaine** : Comparaison

**Description** : Comparaison side-by-side de deux options / scénarios / approches. Deux cartes (template REPEAT_ITEM dupliqué) avec marker, titre, bullets.

**Composition** : `{{TITLE}}`, `{{REPEAT_ITEM}}` (groupe = `{{ITEM_MARKER}}` + `{{ITEM_TITLE}}` + `left_body_bg` + `{{ITEM_BULLETS}}`), `{{SOURCE}}`.

**Quand l'utiliser** : Comparer 2 options (Option A vs Option B), 2 fournisseurs (AWS vs Azure), 2 axes de réflexion (court terme vs long terme).

**Quand ne pas l'utiliser** : Pour une comparaison avant/après (utiliser `comparison_before_after` qui a une flèche entre les deux et un format dédié). Pour 3+ options (utiliser plusieurs slides comparison_2cols paire-à-paire OU un `text_dense_3cols`).

**Limites techniques** : 2 items optimaux (template à un seul `{{REPEAT_ITEM}}` distribué horizontalement). 3-4 bullets par colonne max.

**Exemple JSON minimal** :
```json
{
  "layout": "comparison_2cols",
  "title": "Option A vs Option B",
  "items": [
    {"title": "Option A — Lift & Shift", "bullets": "14 mois\nRisque faible"},
    {"title": "Option B — Replatform",   "bullets": "22 mois\nROI -26 %"}
  ]
}
```

## `comparison_before_after`

**Domaine** : Comparaison

**Description** : Comparaison "avant migration" vs "après migration" avec une flèche orange entre les deux, et un bandeau takeaway en haut. Format dédié au saut de transformation.

**Composition** : `{{TITLE}}`, `{{TAKEAWAY}}` (synthèse haut), `before_card` + `{{BEFORE_LABEL}}` + `{{BEFORE_TITLE}}` + `{{BEFORE_BULLETS}}`, `arrow` (flèche), `after_card` + `{{AFTER_LABEL}}` + `{{AFTER_TITLE}}` + `{{AFTER_BULLETS}}`, `{{SOURCE}}`.

**Quand l'utiliser** : Montrer le saut quantifié entre un état actuel et un état cible. Cas classique : KPI avant/après transformation, processus refactorisé, organisation restructurée.

**Quand ne pas l'utiliser** : Pour une comparaison neutre (sans direction "avant→après"), utiliser `comparison_2cols`.

**Limites techniques** : Format fixe — 2 cartes, pas plus. Les dicts `before` / `after` sont flattenés automatiquement en `before_title`, `before_bullets`, etc. 4 bullets par carte max.

**Exemple JSON minimal** :
```json
{
  "layout": "comparison_before_after",
  "title": "Avant / Après migration",
  "takeaway": "Une transformation mesurable sur 4 KPI",
  "before": {"title": "2025", "bullets": "8h par cycle\nManuel"},
  "after":  {"title": "2028", "bullets": "2h par cycle\nAutomatisé"}
}
```

## `framework_3cards`

**Domaine** : Synthèse

**Description** : 3 cartes verticales colorées (alternance orange/navy/orange par défaut) portant chacune une icône, un titre, des bullets. Format classique consulting "les N piliers du succès".

**Composition** : `{{TITLE}}`, `{{REPEAT_ITEM}}` (groupe = `{{ITEM_BOXE}}` fond + `{{ITEM_ICON}}` cercle + `{{ITEM_TITLE}}` + `{{ITEM_BULLETS}}`), `{{SOURCE}}`, champ optionnel `icons: [...]` pour télécharger des icônes Iconify.

**Quand l'utiliser** : Synthétiser un framework / méthodologie en 3 piliers. Ex: "Sponsorship / Compétences / Méthode". Le champ `icons` permet d'ajouter une icône par carte via Iconify (cf. [`icons_suggested.md`](icons_suggested.md)).

**Quand ne pas l'utiliser** : Pour 4+ piliers (le layout est calibré pour exactement 3 cartes — voir Limites techniques). Pour des items à expliquer en > 4 bullets chacun (utiliser `text_dense_3cols`).

**Limites techniques** : **Maximum 3 cartes — cap dur depuis le Chantier 26.** Au-delà de 3 items, le moteur lève une `ValueError` explicite (`"Layout 'framework_3cards' accepts max 3 items..."`) pointant vers les alternatives. Raison : la distribution horizontale repositionne les groupes REPEAT_ITEM mais ne redimensionne pas les shapes internes — à 4 items, les cards se chevauchent et les titres sont tronqués par le card voisin. **Alternatives pour 4+ piliers** : splitter en deux slides `framework_3cards` (3+1 ou 2+2), ou composer un `canvas_blank` avec N `kpi_card` blocks libres. Alternance de fond gérée par le moteur ; icônes téléchargées depuis Iconify (skip silencieux si réseau down).

**Exemple JSON minimal** :
```json
{
  "layout": "framework_3cards",
  "title": "Les 3 piliers du succès",
  "icons": ["mdi:account-tie", "mdi:school", "mdi:tools"],
  "items": [
    {"title": "Sponsorship", "bullets": "CODIR\nReporting trim."},
    {"title": "Compétences", "bullets": "Upskilling\nCertifications"},
    {"title": "Méthode",     "bullets": "Agile\nIaC"}
  ]
}
```

## `roadmap_styled`

**Domaine** : Planning

**Description** : Roadmap horizontale stylisée. Ligne d'axe horizontal, milestones (losanges orange) répartis le long de la ligne, labels date/milestone alternés au-dessus et en-dessous.

**Composition** : `{{TITLE}}`, `timeline_axis` (ligne), `{{REPEAT_ITEM}}` (groupe = `{{ITEM_MARKER}}` losange + `{{ITEM_DATE}}` + `{{ITEM_MILESTONE}}`), `{{SOURCE}}`.

**Quand l'utiliser** : Présenter un planning sur 3-6 milestones daté. Format consulting standard pour roadmap projet, plan de déploiement, jalons stratégiques.

**Quand ne pas l'utiliser** : Pour une suite d'étapes méthodologiques (utiliser `process_steps` qui a des numéros circulaires). Pour > 6 milestones (saturer visuellement, splitter le deck).

**Limites techniques** : 3 à 6 milestones optimaux. Au-delà, l'axe se serre. Alternance above/below auto pour éviter le chevauchement avec l'axe. Markers tous orange (pas d'alternance de couleur sur les markers).

**Exemple JSON minimal** :
```json
{
  "layout": "roadmap_styled",
  "title": "Roadmap sur 22 mois",
  "items": [
    {"date": "Jan '26",  "milestone": "Phase 0"},
    {"date": "Mai '26",  "milestone": "Phase 1"},
    {"date": "Oct '26",  "milestone": "Phase 2"},
    {"date": "Avr '27",  "milestone": "Phase 3"},
    {"date": "Nov '27",  "milestone": "Décom datacenter"}
  ]
}
```

## `next_steps`

**Domaine** : Planning

**Description** : Liste verticale d'actions à mener, avec colonnes Action / Owner / Date. Format tableau-light avec marker orange et numéro pour chaque ligne. Slide d'engagement de fin de deck.

**Composition** : `{{TITLE}}`, headers (`header_action`, `header_owner`, `header_date`), `{{REPEAT_ITEM}}` (groupe = row + `{{ITEM_MARKER}}` + `{{ITEM_NUMBER}}` + `{{ITEM_ACTION}}` + `{{ITEM_OWNER}}` + `{{ITEM_DATE}}`), `{{SOURCE}}`.

**Quand l'utiliser** : En fin de deck pour proposer un plan d'action concret (3-5 actions). Cas classique : "4 actions pour démarrer dans les 90 jours". Le owner peut être une personne, une équipe, ou un comité.

**Quand ne pas l'utiliser** : Pour une roadmap longue avec phases (utiliser `roadmap_styled`). Pour une checklist sans owner / sans date (utiliser `text`).

**Limites techniques** : 3 à 5 actions optimales. Dates auto-shrunk si longues ("1er septembre 2026" → 10pt si > 1.5"). Numérotation auto 01, 02, …

**Exemple JSON minimal** :
```json
{
  "layout": "next_steps",
  "title": "4 actions à 90 jours",
  "items": [
    {"action": "Validation comité", "owner": "CODIR",         "date": "15 juin 2026"},
    {"action": "Cadrage Phase 0",   "owner": "DSI + AOSIS",   "date": "30 juin 2026"},
    {"action": "Choix partenaire",  "owner": "Achats + DSI",  "date": "15 juillet 2026"},
    {"action": "Kick-off",          "owner": "COO + DSI",     "date": "1 septembre 2026"}
  ]
}
```

## `process_steps`

**Domaine** : Process

**Description** : Suite horizontale d'étapes méthodologiques avec cercles numérotés (alternance orange/navy) reliés par un axe horizontal. Chaque étape porte un titre court et une description.

**Composition** : `{{TITLE}}`, `process_axis` (ligne), `{{REPEAT_ITEM}}` (groupe = `{{ITEM_MARKER}}` disque coloré + `{{ITEM_NUMBER}}` + `{{ITEM_TITLE}}` + `{{ITEM_TEXT}}`), `{{SOURCE}}`.

**Quand l'utiliser** : Présenter une méthodologie en 3-5 étapes séquentielles. Ex: "Assessment → Design → Build → Optimize" (4 phases de migration), "Découverte → Cadrage → Build → Bascule".

**Quand ne pas l'utiliser** : Pour un planning avec dates précises (utiliser `roadmap_styled`). Pour un workflow non-séquentiel / cyclique (utiliser `canvas_blank` avec un schéma custom).

**Limites techniques** : 4-5 étapes optimales (au-delà serre). Markers alternent orange/navy. Description (`text`) wrappe mais à garder ≤ 15 mots.

**Exemple JSON minimal** :
```json
{
  "layout": "process_steps",
  "title": "Notre méthode en 4 étapes",
  "items": [
    {"title": "Assessment", "text": "Audit + cartographie"},
    {"title": "Design",     "text": "Architecture cible"},
    {"title": "Migrate",    "text": "Exécution par vague"},
    {"title": "Optimize",   "text": "Right-sizing + FinOps"}
  ]
}
```

## `text_dense_3cols`

**Domaine** : Synthèse

**Description** : 3 colonnes de texte dense, séparées par un trait fin. Chaque colonne a un numéro (01/02/03), un titre, et un paragraphe explicatif. Format proche d'un article éditorial.

**Composition** : `{{TITLE}}`, `{{REPEAT_ITEM}}` (groupe = `{{ITEM_NUMBER}}` + `{{ITEM_TITLE}}` + `{{ITEM_TEXT}}` + `sep` séparateur), `{{SOURCE}}`.

**Quand l'utiliser** : Quand un message exige 3 angles d'analyse complémentaires détaillés. Cas typique : "Angle technique / Angle économique / Angle organisationnel". Chaque colonne porte 1 paragraphe (30-60 mots).

**Quand ne pas l'utiliser** : Pour des bullets courts (utiliser `framework_3cards` ou `executive_summary`). Pour des paragraphes très longs (>80 mots, splitter le deck).

**Limites techniques** : 3 colonnes optimales. Paragraphes : 30-60 mots chacun. Au-delà, le texte se densifie trop.

**Exemple JSON minimal** :
```json
{
  "layout": "text_dense_3cols",
  "title": "3 angles d'analyse",
  "items": [
    {"title": "Angle technique",      "text": "La replatformisation permet d'utiliser les managed services AWS qui réduisent l'effort opérationnel."},
    {"title": "Angle économique",     "text": "L'investissement de 3.4 M€ se rentabilise sur 32 mois. ROI 5 ans : 280 %."},
    {"title": "Angle organisationnel","text": "Upskilling de 12 IT sur 18 mois, création d'un Cloud Center of Excellence."}
  ]
}
```

## `quote_callout`

**Domaine** : Citation

**Description** : Slide-citation avec une grande phrase entre guillemets, attribution en dessous, et un bandeau orange `takeaway` au-dessus pour donner le contexte / l'insight de la voix.

**Composition** : `{{TITLE}}` (souvent "Ce que nous ont dit les stakeholders"), `{{TAKEAWAY}}` (synthèse), `quote_bar`, `{{QUOTE_TEXT}}`, `{{QUOTE_ATTRIBUTION}}`, `{{SOURCE}}`.

**Quand l'utiliser** : Pour ancrer un argument avec la voix d'un dirigeant ou stakeholder. Cas classique : "Ce que nous ont dit les dirigeants — citation du COO". Force éditoriale forte, à user avec parcimonie (1 max par deck en général, 2 si le deck est long).

**Quand ne pas l'utiliser** : Pour rapporter de simples opinions internes (utiliser `text`). Pour 2+ citations (utiliser `text_dense_3cols` avec une colonne par voix).

**Limites techniques** : `quote_text` : 15-30 mots optimal, au-delà la typo de citation est diluée. Attribution : `— Prénom Nom, Rôle` en majuscules.

**Exemple JSON minimal** :
```json
{
  "layout": "quote_callout",
  "title": "Ce que nous a dit le COO",
  "takeaway": "Le board a déjà tranché.",
  "quote_text": "Notre ERP doit être disponible 24/7 pendant les pics de production.",
  "quote_attribution": "— Marc Lefèvre, COO TechnoLog"
}
```

## `matrix_2x2_styled`

**Domaine** : Comparaison

**Description** : Matrice 2×2 stylisée avec quatre quadrants colorés, axes annotés (label + low/high), titre par quadrant et bullets. Format classique strategy consulting (impact/effort, importance/urgence, ...).

**Composition** : `{{TITLE}}`, 4 fonds `quad_<position>_bg`, 4 `{{QUAD_<position>_TITLE}}`, 4 `{{QUAD_<position>_BULLETS}}` (anchored bottom-left), `{{Y_AXIS_LABEL}}`, `{{Y_HIGH}}`, `{{Y_LOW}}`, `{{X_AXIS_LABEL}}`, `{{SOURCE}}`.

**Quand l'utiliser** : Cadrer un choix stratégique sur deux axes : Impact/Effort (priorité), Importance/Urgence (Eisenhower), Croissance/Part de marché (BCG). Le top-right est conventionnellement la zone "stratégique" (high/high).

**Quand ne pas l'utiliser** : Pour un SWOT classique (utiliser `swot` code-based, mais préférer `matrix_2x2_styled` avec axes Faiblesses/Forces et Menaces/Opportunités). Pour 2 dimensions discrètes non-comparatives (utiliser `comparison_2cols`).

**Limites techniques** : **Max 3 bullets par quadrant** (au-delà, tronqué automatiquement avec warning stderr). Titre court (3-5 mots) par quadrant. Auto-shrink des bullets si débordement.

**Exemple JSON minimal** :
```json
{
  "layout": "matrix_2x2_styled",
  "title": "Priorisation des chantiers",
  "x_axis": {"label": "Effort", "low": "Faible", "high": "Élevé"},
  "y_axis": {"label": "Impact", "low": "Faible", "high": "Élevé"},
  "quadrants": {
    "top_left":     {"title": "Quick wins",   "items": ["A", "B", "C"]},
    "top_right":    {"title": "Stratégique",  "items": ["D", "E", "F"]},
    "bottom_left":  {"title": "Hygiène",      "items": ["G"]},
    "bottom_right": {"title": "À deprioriser","items": ["H"]}
  }
}
```

## `closing_diagonal`

**Domaine** : Navigation

**Description** : Slide de fin "Merci / Questions" avec photo (auto-fetched) découpée par diagonale à droite, et coordonnées de l'auteur (nom + email + téléphone) à gauche.

**Composition** : `{{IMAGE}}` (photo diagonale), `{{TITLE}}` (souvent "Merci"), `{{QUESTION}}` ("Des questions ?"), `{{AUTHOR_NAME}}`, `{{AUTHOR_EMAIL}}`, `{{AUTHOR_PHONE}}`, `website` (fixe).

**Quand l'utiliser** : Dernière slide du deck (avant l'éventuelle `final_branding`). Donne au lecteur les coordonnées du point de contact.

**Quand ne pas l'utiliser** : Pour un deck strictement interne sans audience externe (utiliser une `section_diagonal` de conclusion à la place).

**Limites techniques** : 1 seul auteur supporté. Pour une équipe, utiliser `cards` à la place.

**Exemple JSON minimal** :
```json
{
  "layout": "closing_diagonal",
  "title": "Merci",
  "image_keyword": "business handshake success",
  "question": "Des questions ?",
  "author_name": "Florian Horellou",
  "author_email": "florian.horellou@aosis.net",
  "author_phone": "+33 6 36 26 17 47"
}
```

## `data_table`

**Domaine** : Données chiffrées / Comparaison

**Description** : Tableau structuré pour restituer des données tabulaires : comparaison de stratégies, cartographie de risques, roadmap par phases, KPI avant/après. Le moteur dessine dynamiquement un tableau stylé AOSIS (header navy + texte blanc, lignes alternées blanc/off-white, première colonne bold gauche, autres colonnes centrées) avec highlight optionnel d'une colonne (texte orange bold) et d'une ligne (fond orange clair).

**Composition** : `{{TITLE}}` (24pt navy bold, 0.4" 0.4") + `{{SOURCE}}` (8pt italic gris, 0.4" 5.10") + un tableau dessiné à partir de `spec.table` au centre (0.5" 1.2", 9.0" × max 3.7").

**Quand l'utiliser** : Quand le contenu source EST un tableau ; quand 4+ lignes × 3+ colonnes valent plus qu'une mise en page graphique (chart, KPI cards). Cas typiques : comparaison de N options sur M critères, matrice risque × probabilité × impact, planning phases × période × livrables.

**Quand ne pas l'utiliser** : Pour 2-3 KPI isolés (utiliser `stat_grid` ou `kpi_with_chart`). Pour une comparaison 2 options (utiliser `comparison_2cols`). Pour une matrice 2×2 conceptuelle (utiliser `matrix_2x2_styled`).

**Limites techniques** :
- **Max 6 colonnes** (au-delà → `ValueError` côté moteur)
- **Max 8 lignes** (au-delà → truncate silencieux + warning stderr)
- Cellule > 30 chars → warning stderr (risque de débordement vertical)
- Auto-shrink police 10→9→8pt + padding 6→5→4pt selon densité

**Exemple JSON minimal** :
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

`highlight_column` (0-based) → texte orange bold sur toute cette colonne.
`highlight_row` (0-based sur les données, sans le header) → fond orange clair sur toute cette ligne.

## `final_branding`

**Domaine** : Navigation

**Description** : Slide de fin pure branding (logo + diagonale, sans contenu textuel). Variante minimaliste de `closing_diagonal` quand on ne veut pas exposer les coordonnées de l'auteur.

**Composition** : Vide côté contenu — la slide n'expose aucun placeholder. Le rendu vient entièrement du slide layout (masters, logo, diagonale).

**Quand l'utiliser** : Tout dernier slide d'un deck destiné à être imprimé ou diffusé largement, où on ne veut pas montrer de coordonnées personnelles. Ou en complément de `closing_diagonal`.

**Quand ne pas l'utiliser** : Si l'audience attend un point de contact (préférer `closing_diagonal`).

**Limites techniques** : Aucun champ accepté côté spec — tout vient du template.

**Exemple JSON minimal** :
```json
{"layout": "final_branding"}
```

---

# Layouts code-based

Ces layouts sont dessinés programmatiquement (pas issus du template `.pptx`). Rendu moins consulting mais ils couvrent des cas que le template n'expose pas encore.

## `hero_stat`

**Domaine** : Données chiffrées / Synthèse

**Description** : Slide-impact avec un nombre géant (150pt) sur la gauche, label court en dessous, contexte gris optionnel, et une liste optionnelle de bullets de support à droite. Format magazine.

**Composition** : `title` (eyebrow petit en haut), `value` (le nombre géant), `label` (caption sous le nombre), `context` (texte gris optionnel), `supporting` (liste de bullets à droite, optionnel).

**Quand l'utiliser** : Quand UN seul chiffre EST le message. Ex: "+147 %", "-26 %", "1.2 M€/an". Killer opener pour la slide "L'AMBITION" ou "L'AMPLEUR".

**Quand ne pas l'utiliser** : Pour 2+ chiffres (utiliser `kpi_with_chart` ou `stat_grid`). Pour un chiffre sans contexte percutant (utiliser `big_idea` pour porter une conviction).

**Limites techniques** : Le `value` doit faire ≤ 7 caractères pour ne pas auto-shrinker (au-delà, taille adaptative). `supporting` doit être une **liste** ; passer une string donnera un bug d'itération caractère par caractère (fix Chantier 10).

**Exemple JSON minimal** :
```json
{
  "layout": "hero_stat",
  "title": "L'AMPLEUR",
  "value": "+147 %",
  "label": "Incidents critiques 2023 → 2025",
  "supporting": ["47 incidents en 2025", "vs 19 en 2023"]
}
```

## `big_idea`

**Domaine** : Synthèse

**Description** : Slide-thèse avec une phrase audacieuse en gros caractères (40pt) sur la gauche, bullets de support à droite. Format manifesto.

**Composition** : `idea` (phrase thèse), `title` (eyebrow optionnel), `supports` (bullets droite optionnel), `attribution` (signature orange UPPERCASE optionnelle).

**Quand l'utiliser** : Porter une conviction, un parti pris, le point de vue de l'auteur. À user **1-2 fois max par deck** sinon l'effet se dilue.

**Quand ne pas l'utiliser** : Pour un titre de section (utiliser `section_diagonal`). Pour une citation extérieure (utiliser `quote_callout`).

**Limites techniques** : `idea` : 15-25 mots optimal. `supports` : 3-4 bullets max.

**Exemple JSON minimal** :
```json
{
  "layout": "big_idea",
  "idea": "Passer au cloud n'est plus une option : c'est la condition de notre capacité d'innovation.",
  "title": "Notre conviction",
  "attribution": "— Direction AOSIS"
}
```

## `swot`

> ⛔ **Retiré du DISPATCH au Chantier 23.** Utilise [`matrix_2x2_styled`](#matrix-2x2-styled) (template-based) à la place. Le code de cette fonction reste dans le repo pour rétro-compatibilité Git mais n'est plus exposé au pipeline. Tenter d'utiliser `swot` dans un JSON spec lèvera maintenant une `ValueError` explicite.

**Domaine** : Comparaison

**Description** : Matrice SWOT classique 2×2 (Forces / Faiblesses / Opportunités / Menaces) avec 4 quadrants et bullets.

**Composition** : `title`, 4 dicts `strengths`, `weaknesses`, `opportunities`, `threats` (chacun avec `items: [...]`).

**Quand l'utiliser** : SWOT canonique d'analyse stratégique d'entreprise / produit / marché.

**Quand ne pas l'utiliser** : **Préférer `matrix_2x2_styled`** qui offre un rendu plus consulting et permet des axes personnalisés. Le `swot` code-based est conservé pour rétrocompatibilité mais le rendu visuel est plus pauvre.

**Limites techniques** : 3 items par quadrant max (visuellement). Pas d'icônes ni de couleur conditionnelle.

**Exemple JSON minimal** :
```json
{
  "layout": "swot",
  "title": "SWOT TechnoLog SA",
  "strengths":     {"items": ["Marque forte", "Bilan sain"]},
  "weaknesses":    {"items": ["SI vieillissant", "Dette technique"]},
  "opportunities": {"items": ["Cloud public mature", "Marché en croissance"]},
  "threats":       {"items": ["Compétiteurs natifs cloud", "Talents IT"]}
}
```

## `pyramid`

**Domaine** : Process / pyramide

**Description** : Pyramide à N niveaux (3-5 typiquement) illustrant une hiérarchie ou une stratification : Maslow-style, value chain, "this rests on that".

**Composition** : `title`, `levels: [...]` (du bas vers le haut), `inverted: false` (true pour pointe en bas).

**Quand l'utiliser** : Hiérarchie naturelle entre couches qui se reposent l'une sur l'autre. Ex: pyramide des besoins, pyramide de Kelsen, escalier de maturité.

**Quand ne pas l'utiliser** : Pour des phases temporelles (utiliser `roadmap_styled` ou `process_steps`). Pour comparer 2 visions (utiliser `comparison_2cols`).

**Limites techniques** : 3-5 niveaux optimaux. Au-delà la lisibilité baisse rapidement.

**Exemple JSON minimal** :
```json
{
  "layout": "pyramid",
  "title": "Stratification du SI",
  "levels": ["Infra physique", "Plateforme cloud", "Applications", "Services métier", "UX client"]
}
```

## `funnel`

**Domaine** : Données chiffrées

**Description** : Entonnoir vertical à N étapes, chaque palier étant plus étroit que le précédent. Le label et la valeur de chaque étape sont affichés à droite.

**Composition** : `title`, `stages: [{label, value}, ...]` (du haut large vers le bas étroit).

**Quand l'utiliser** : Représenter une **conversion / déperdition séquentielle** sur un flux : leads → opportunités → deals → revenus. Ou une qualification de données : 100 % brut → 60 % retraité → 20 % livrable.

**Quand ne pas l'utiliser** : Pour **comparer N options en valeur absolue** (utiliser `chart` type `bar`). C'est un piège fréquent : un funnel implique une logique de déperdition séquentielle, pas un classement.

**Limites techniques** : 3-5 étapes optimales.

**Exemple JSON minimal** :
```json
{
  "layout": "funnel",
  "title": "Funnel qualité des données",
  "stages": [
    {"label": "Données brutes",  "value": "100 %"},
    {"label": "Après contrôles", "value": "85 %"},
    {"label": "Retraitement",    "value": "60 %"},
    {"label": "Livrable final",  "value": "20 %"}
  ]
}
```

## `dashboard`

**Domaine** : Données chiffrées

**Description** : Tableau de bord exécutif : ligne de stats compactes en haut + chart en dessous. Format dense, beaucoup d'info sur une slide.

**Composition** : `title`, `stats: [{label, value}, ...]` (cartes du haut), `chart` (spec matplotlib, type/labels/series), `chart_title` (label au-dessus du chart).

**Quand l'utiliser** : Slide de monitoring / pilotage. Cas d'usage : revue mensuelle, bilan trimestriel avec 4-6 KPI + une courbe d'évolution.

**Quand ne pas l'utiliser** : Pour 3 KPI seulement (préférer `kpi_with_chart` template-based, rendu plus consulting). Pour un seul chart sans stats (utiliser `chart`).

**Limites techniques** : 4-6 stats max en ligne, chart matplotlib (mêmes types que `kpi_with_chart`). Rendu denser que template-based.

**Exemple JSON minimal** :
```json
{
  "layout": "dashboard",
  "title": "Pilotage trimestriel",
  "stats": [
    {"label": "Disponibilité", "value": "99.6 %"},
    {"label": "Incidents",     "value": "3"},
    {"label": "TCO/mois",      "value": "265 K€"}
  ],
  "chart": {"type": "line", "labels": ["Jan","Fév","Mar"], "series": [{"name": "Coût", "values": [280, 270, 265]}]}
}
```

## `org_chart`

**Domaine** : Process / pyramide

**Description** : Organigramme à 2 niveaux : un leader en haut centré, ses N reports directs en bas. Cartes avec nom + rôle.

**Composition** : `title`, `leader: {name, role}`, `reports: [{name, role}, ...]`.

**Quand l'utiliser** : Présenter l'équipe projet, la structure de gouvernance d'un programme, ou l'organigramme cible post-transformation. 4-6 reports max.

**Quand ne pas l'utiliser** : Pour une équipe sans hiérarchie (utiliser `cards`). Pour un organigramme à 3+ niveaux (utiliser `canvas_blank` avec un schéma externe).

**Limites techniques** : 2 niveaux uniquement. 4-6 reports lisibles, au-delà serre.

**Exemple JSON minimal** :
```json
{
  "layout": "org_chart",
  "title": "Équipe projet",
  "leader": {"name": "Floriane M.", "role": "Directrice projet"},
  "reports": [
    {"name": "Karim T.", "role": "Architecte data"},
    {"name": "Léa B.",   "role": "Lead développeuse"},
    {"name": "Yann R.",  "role": "FinOps"}
  ]
}
```

## `stat_grid`

**Domaine** : Données chiffrées

**Description** : Grille de N stats (jusqu'à 6) en 2-3 colonnes. Chaque case porte un grand chiffre orange/navy et un label court.

**Composition** : `title`, `stats: [{label, value}, ...]`, `footnote` (optionnel).

**Quand l'utiliser** : Aligner 4-6 KPI sur une slide quand chacun mérite d'être vu, sans hiérarchie particulière entre eux.

**Quand ne pas l'utiliser** : Pour 3 KPI avec un chart (utiliser `kpi_with_chart`). Pour 1 KPI dominant (utiliser `hero_stat`).

**Limites techniques** : 4-6 stats optimaux. Valeurs ≤ 8 caractères pour ne pas dégrader la lisibilité.

**Exemple JSON minimal** :
```json
{
  "layout": "stat_grid",
  "title": "Chiffres clés 2025",
  "stats": [
    {"label": "CA",         "value": "280 M€"},
    {"label": "Employés",   "value": "850"},
    {"label": "Sites",      "value": "3"},
    {"label": "Applis",     "value": "47"},
    {"label": "Datacenter", "value": "87 %"},
    {"label": "Incidents",  "value": "47/an"}
  ],
  "footnote": "Source : DSI TechnoLog"
}
```

## `cards`

> ⛔ **Retiré du DISPATCH au Chantier 23.** Utilise [`framework_3cards`](#framework-3cards) (template-based) à la place. Le code de cette fonction reste dans le repo pour rétro-compatibilité Git mais n'est plus exposé au pipeline. Tenter d'utiliser `cards` dans un JSON spec lèvera maintenant une `ValueError` explicite.

**Domaine** : Liberté

**Description** : Grille de cartes (2-4 colonnes) avec titre, sous-titre, body texte. Format profil ou portfolio.

**Composition** : `title`, `cards: [{title, subtitle, body}, ...]`, `columns: 2|3|4`.

**Quand l'utiliser** : Présenter une équipe (nom + rôle + bio), un portfolio de cas clients, une liste d'offres / produits.

**Quand ne pas l'utiliser** : **Préférer `framework_3cards`** quand on veut une vraie carte stylisée avec icône et alternance de couleurs. `cards` reste utile pour 4+ cartes ou pour exposer des contenus profils plus longs.

**Limites techniques** : 4 cartes max recommandé. Body : 30-50 mots par carte.

**Exemple JSON minimal** :
```json
{
  "layout": "cards",
  "title": "L'équipe",
  "cards": [
    {"title": "Floriane M.", "subtitle": "Directrice projet", "body": "12 ans en transformation finance"},
    {"title": "Karim T.",    "subtitle": "Architecte data",    "body": "Ex-BNP, expert lineage"},
    {"title": "Léa B.",      "subtitle": "Lead dev",           "body": "Python/Airflow, 8 ans"}
  ]
}
```

## `chart`

> ⛔ **Retiré du DISPATCH au Chantier 23.** Utilise [`kpi_with_chart`](#kpi-with-chart) (template-based) à la place. Le code de cette fonction reste dans le repo pour rétro-compatibilité Git mais n'est plus exposé au pipeline. Tenter d'utiliser `chart` dans un JSON spec lèvera maintenant une `ValueError` explicite.

**Domaine** : Données chiffrées

**Description** : Slide avec un chart matplotlib en pleine page, titre simple en haut, commentary optionnel à côté du chart sous forme de bullets.

**Composition** : `title`, `chart: {type, labels, series/data, ...}`, `commentary: [...]` (bullets droite optionnels).

**Quand l'utiliser** : Quand une donnée est plus parlante en chart qu'en chiffres bruts. Si pas de commentaire, slide plein chart.

**Quand ne pas l'utiliser** : **Préférer `kpi_with_chart`** pour un combo KPI + chart car rendu plus consulting. `chart` reste utile pour un chart pleine page sans KPI.

**Limites techniques** : 5 types : `bar`, `barh`, `line`, `pie`, `column`. (Note : `kpi_with_chart` template-based supporte 8 types via `chart_engine`, plus complet.)

**Exemple JSON minimal** :
```json
{
  "layout": "chart",
  "title": "Évolution TCO 2025-2029",
  "chart": {
    "type": "line",
    "labels": ["2025","2026","2027","2028","2029"],
    "data": [4.2, 4.4, 3.8, 3.1, 2.9]
  }
}
```

## `process`

> ⛔ **Retiré du DISPATCH au Chantier 23.** Utilise [`process_steps`](#process-steps) (template-based) à la place. Le code de cette fonction reste dans le repo pour rétro-compatibilité Git mais n'est plus exposé au pipeline. Tenter d'utiliser `process` dans un JSON spec lèvera maintenant une `ValueError` explicite.

**Domaine** : Process

**Description** : Suite horizontale d'étapes avec carrés numérotés, titre court et description, reliés par des flèches.

**Composition** : `title`, `steps: [{title, detail}, ...]`.

**Quand l'utiliser** : Méthodologie séquentielle 3-5 étapes, rendu plus simple que `process_steps`.

**Quand ne pas l'utiliser** : **Préférer `process_steps` template-based** qui a un rendu visuel plus riche (markers circulaires colorés, alternance, axe horizontal). `process` reste utile en fallback si le template n'est pas dispo.

**Limites techniques** : 3-5 étapes optimales.

**Exemple JSON minimal** :
```json
{
  "layout": "process",
  "title": "Méthodologie en 4 phases",
  "steps": [
    {"title": "Audit",     "detail": "Cartographie de l'existant"},
    {"title": "Cadrage",   "detail": "Architecture cible"},
    {"title": "Build",     "detail": "Refonte par lots"},
    {"title": "Bascule",   "detail": "Mise en service"}
  ]
}
```

## `image_hero`

**Domaine** : Liberté

**Description** : Image pleine page avec un titre + sous-titre en surimpression. Format magazine, slide d'ouverture spectaculaire.

**Composition** : `image` (chemin local obligatoire), `title`, `subtitle` (optionnel).

**Quand l'utiliser** : Slide d'introduction visuelle quand on veut donner un effet "wow" : photo d'industriel, paysage corporate, datacenter. À insérer en début de chapitre ou en transition.

**Quand ne pas l'utiliser** : Si on n'a pas d'image hi-res qui porte le message visuellement. Pour une cover de deck, préférer `cover` (template).

**Limites techniques** : L'image **doit être un chemin local** (pas auto-fetché — le moteur `image_engine` est branché sur `{{IMAGE}}` placeholder uniquement). Idéal : 1920×1080 ou + grand.

**Exemple JSON minimal** :
```json
{
  "layout": "image_hero",
  "image": "/home/user/photos/datacenter.jpg",
  "title": "Une infrastructure pour décennies",
  "subtitle": "Cloud-first, edge-ready, FinOps-driven"
}
```

## `content`

**Domaine** : Liberté

**Description** : Slide bullets + image optionnelle en colonne droite. Format texte-image classique.

**Composition** : `title`, `bullets: [...]`, `image` (chemin local optionnel).

**Quand l'utiliser** : Pour une slide texte avec une image illustrative à droite. Cas d'usage : description d'un produit, profil d'une initiative, présentation d'un service.

**Quand ne pas l'utiliser** : Pour des bullets simples sans image (utiliser `text`). Pour 3+ angles d'analyse (utiliser `text_dense_3cols`).

**Limites techniques** : 4-6 bullets max. Image carrée ou portrait recommandé pour matcher la colonne droite.

**Exemple JSON minimal** :
```json
{
  "layout": "content",
  "title": "Notre offre cloud migration",
  "bullets": [
    "Audit + design en 6 semaines",
    "Migration par vagues de 8 apps",
    "FinOps intégré dès J0",
    "Accompagnement upskilling"
  ],
  "image": "/path/to/diagram.png"
}
```

## `text`

**Domaine** : Liberté

**Description** : Slide de bullets pure : titre + liste de bullets. Le fallback minimal.

**Composition** : `title`, `bullets: [...]`.

**Quand l'utiliser** : Quand aucun layout visuel ne convient et qu'on a vraiment besoin de bullets. Cas typiques : prochaines étapes courtes, tarification, mentions légales.

**Quand ne pas l'utiliser** : Dès qu'un layout plus visuel existe pour la même info. **Règle d'or AOSIS** : "Always prefer a visual layout over plain text" — `text` doit rester l'exception.

**Limites techniques** : 4-6 bullets max idéal. Au-delà, splitter le deck.

**Exemple JSON minimal** :
```json
{
  "layout": "text",
  "title": "Prochaines étapes",
  "bullets": [
    "Cadrage détaillé avec le sponsor — S+1",
    "Constitution de l'équipe projet — S+2",
    "Kick-off et début de l'audit — S+3"
  ]
}
```

## `gantt`

**Domaine** : Planning

**Description** : Non implémenté à ce jour. **Le layout `gantt` n'existe pas dans le DISPATCH du skill**.

**Quand l'utiliser** : —

**Quand ne pas l'utiliser** : Toujours. Pour un planning daté, utiliser `roadmap_styled`. Pour un planning détaillé multi-tracks, produire un graphique externe et l'insérer via `canvas_blank` ou `image_hero`.

**Limites techniques** : N/A.

**Exemple JSON minimal** : N/A.

---

# Layouts retirés au Chantier 23

Les 10 layouts code-based suivants ont été **retirés du DISPATCH** car leur équivalent template-based est systématiquement de meilleure qualité visuelle. Toute tentative d'utilisation dans un JSON spec lève désormais une `ValueError` explicite qui pointe vers le remplaçant.

| Layout retiré | Remplacement template-based |
|---|---|
| `swot` | `matrix_2x2_styled` |
| `cards` | `framework_3cards` |
| `process` | `process_steps` |
| `chart` | `kpi_with_chart` |
| `agenda` | `agenda_diagonal` |
| `timeline` | `roadmap_styled` |
| `quote` | `quote_callout` |
| `comparison` | `comparison_2cols` |
| `matrix_2x2` | `matrix_2x2_styled` |
| `roadmap` | `roadmap_styled` |

Le code des 10 fonctions (`add_swot`, `add_cards`, etc.) reste dans `scripts/build_deck.py` annoté `# DEPRECATED — retiré du DISPATCH au Chantier 23` pour permettre une réactivation rapide via Git revert si nécessaire.
