---
name: aosis-deck-builder
description: Use this skill whenever the user asks for a PowerPoint deck, presentation, slides or pptx file at AOSIS. Triggers explicitly include the words "powerpoint", "pptx", "deck", "slides", "présentation", or any request to produce a commercial proposal, mission deliverable (restitution), or CODIR report in slide form. The skill produces a .pptx file built on top of the official AOSIS template (navy/orange palette, logo, footers, layouts inherited automatically) AND composes a rich catalogue of consulting-grade visual slides — hero statistics, big-idea statements, 2×2 matrices, funnels, horizontal roadmaps, timelines, cards, comparisons, charts, processes, quotes, image-hero. Slides aim for the look of a top-tier consulting pitch deck (McKinsey / BCG / Bain). Always prefer this skill over the generic pptx skill for this user — every AOSIS deck must use this template, and a deck built without it will look unbranded and amateur.
---

# AOSIS Deck Builder

Generate AOSIS-branded PowerPoint decks that look like top-tier consulting
output. The skill always starts from the official `.pptx` template in
`assets/`, so the charte graphique (couleurs, logo, polices, footers) is
inherited by construction — your job is to produce the **content**, the
**visual composition**, and the **narrative arc**.

**Two generation mechanisms coexist**: **code-based layouts** (23, drawn
programmatically in `build_deck.py`) and **template-based layouts** (11+,
sourced from named slides in `assets/exhibits.pptx` and filled at runtime
by `template_engine.py`). The dispatcher routes by layout name. Template
slides are discovered dynamically by scanning `cSld.name` — adding a new
named slide in exhibits.pptx instantly registers it.

## References

Detailed reference material is loaded on-demand from the `references/` folder:

- [`references/layouts.md`](references/layouts.md) — catalogue of all layouts (code-based + template-based) and when to use each.
- [`references/json-schema.md`](references/json-schema.md) — JSON spec structure, field-by-field reference for every layout, full example.
- [`references/qa.md`](references/qa.md) — visual and content QA workflow, symptom-to-fix lookup table.

## The Three Golden Rules

**1. Never recreate the AOSIS brand in code.** The template carries the
design. If you find yourself reaching for `slide.background.fill.solid()`
or trying to inject a custom logo, stop — that's a signal you're working
around the template instead of using it.

**2. Always prefer a visual layout over plain text.** The default to
reach for is *not* `text` with bullets. Open with `hero_stat` or
`big_idea`, structure arguments with `comparison`, `matrix_2x2`, or
`roadmap`, support data with `chart`, anchor with `quote`. Use `text` or
`content` only when the message really is words (legal text, tarification,
prochaines étapes).

**3. Always write action titles, never descriptive titles.** A descriptive
title labels the slide ("Réduction du temps"). An action title delivers the
message ("La cible : diviser par 4 le temps de production en 12 mois").
Action titles let the deck read like a story even if you skim only the
titles — that's the signature of top consulting decks. Examples:

| ❌ Descriptive | ✅ Action |
|---|---|
| "Approche méthodologique" | "Notre approche en 4 phases pour livrer la cible à T+12 mois" |
| "Chiffres clés" | "1,2 M€ pour reprendre 6h sur chaque cycle de reporting" |
| "Équipe" | "L'équipe que nous mobilisons : 6 consultants, 50 ans d'expérience cumulée" |
| "Comparaison" | "Le saut que nous proposons : de 8h à 2h par cycle" |
| "Planning" | "Le chemin sur 12 mois, jalonné en 5 milestones" |

The action title is often half the impact of a slide. Spend real effort on
it.

## Build Workflow

**1. Plan the narrative.** Choose the deck type (proposal / restitution /
CODIR), define the central message, sketch 6-12 slides. Verify that the
titles read as a story when skimmed. **Vary the layouts** — a great deck
has rhythm: open strong with `hero_stat` or `big_idea`, alternate
frameworks (`matrix_2x2`, `funnel`, `roadmap`), support data with `chart`,
anchor mid-deck with `quote`, close with a final `hero_stat` or
`big_idea` that lands the ask. For the catalogue of available layouts and
when to pick each, see [`references/layouts.md`](references/layouts.md).

**2. Write the JSON spec.** Build the spec following the schema. For
the full field-by-field reference and a complete example, see
[`references/json-schema.md`](references/json-schema.md). Save anywhere
(e.g. `/tmp/deck_spec.json`).

**3. Run the generator.**
```bash
python scripts/build_deck.py /tmp/deck_spec.json /mnt/user-data/outputs/deck.pptx
```

**4. QA visual + content.** Render each slide to an image and inspect.
Fix issues **in the spec** (never by post-editing the `.pptx`) and rerun.
For the full QA commands and the symptom-to-fix table, see
[`references/qa.md`](references/qa.md).

## Quick example

Minimal spec to bootstrap (full schema in [`references/json-schema.md`](references/json-schema.md)):

```json
{
  "cover": { "title": "Refonder le reporting risque", "ref": "Mai 2026" },
  "slides": [
    {
      "layout": "hero_stat",
      "title":  "L'AMBITION",
      "value":  "-75%",
      "label":  "Le temps de production que nous allons reprendre"
    },
    {
      "layout": "matrix_2x2",
      "title":  "Cartographie des chantiers",
      "x_axis": {"label": "Effort", "low": "Faible", "high": "Élevé"},
      "y_axis": {"label": "Impact", "low": "Faible", "high": "Élevé"},
      "quadrants": {
        "top_left":     {"title": "Quick wins",          "items": ["Refactor batchs"]},
        "top_right":    {"title": "Chantiers stratégiques", "items": ["Refonte lineage"]},
        "bottom_left":  {"title": "Hygiène",             "items": ["Documentation"]},
        "bottom_right": {"title": "À deprioriser",       "items": ["Refonte UI legacy"]}
      }
    },
    {
      "layout": "roadmap",
      "title":  "Le chemin sur 12 mois",
      "milestones": [
        {"date": "Juin '26", "name": "Audit",         "detail": "Cartographie"},
        {"date": "Nov '26",  "name": "First release", "detail": "Premier lot"},
        {"date": "Juin '27", "name": "Bascule",       "detail": "Plateforme cible"}
      ]
    }
  ],
  "closing": true
}
```

## data_table layout

When the source content is genuinely tabular (comparison of N options on M
criteria, risks × probability × impact, phases × période × livrables),
prefer the `data_table` layout (Chantier 15) over forced conversion to KPI
cards or bullets. Pass `{ "table": { "headers": [...], "rows": [[...]] } }`
with optional `highlight_column` and `highlight_row`. Max 6 columns × 8 rows.
See [`references/layouts.md`](references/layouts.md#data_table) for the
full spec.

## Auto stock images

Layouts with an `{{IMAGE}}` placeholder (agenda_diagonal,
section_diagonal, closing_diagonal…) get a stock photo fetched at build
time. Order of resolution: explicit `image:` path → `image_keyword` →
words from `title` → layout-based default.

**Provider order (Chantier 12):** Pexels API (if `PEXELS_API_KEY`
env var set — preferred, automated use allowed by ToS) → Lorem Picsum
(no key needed, used as fallback). The legacy Unsplash code was dropped
since Unsplash explicitly forbids automated downloads.

Diagonal layouts (cover, agenda_diagonal, section_diagonal,
closing_diagonal) automatically clip the inserted photo to the design's
diagonal cut — the photo is no longer a rectangle covering the diagonal,
it's shaped to match the layout's `custGeom`.

Disable with the `--no-images` CLI flag (e.g. for offline builds or
faster regeneration). Failure is silent — the slide just renders without
a photo. See [`references/json-schema.md`](references/json-schema.md#images-automatiques-pexels--lorem-picsum)
for the full mechanism.

## What This Skill Does NOT Do

- It does **not** alter the template's masters, footers, or theme.
- It does **not** add custom backgrounds, gradients, or fonts.
- It does **not** insert the AOSIS logo manually — already on every slide
  via the master.
- For exotic visuals (custom diagrams beyond the catalogue, animated
  charts, embedded videos), tell the user this is out of scope and offer
  to produce a static image externally (matplotlib, mermaid, or hand) that
  they can drop into a `content` or `image_hero` slide.

## Delivering to the User

Save the final `.pptx` to `/mnt/user-data/outputs/` and call `present_files`
with its path. One line of summary (slide count, key layouts used) is
welcome; long postambles are not — the file speaks for itself.
