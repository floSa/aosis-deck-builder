# QA — Visual and Content Checks

The first render of a deck almost always exposes one or two real issues. **Do not deliver a deck without running the visual QA pass at least once.** Skipping QA is the most common cause of "amateur-looking" output reaching the user.

---

## 0. Automated visual review (recommended)

The skill ships with `scripts/visual_review.py` that automates the JPEG conversion and produces a review prompt + report template. A vision-capable Claude (or a human) then inspects the JPEGs and fills the report. The defects are surfaced sorted by severity.

### One-shot prepare

```bash
python scripts/visual_review.py /mnt/user-data/outputs/deck.pptx /tmp/review/
```

This produces in `/tmp/review/`:

- `slide-NN.jpg` — one JPEG per slide (zero-padded, 150 dpi by default).
- `review_prompt.md` — the inspection prompt (what defects to look for, severity scale, output format).
- `review_report.template.json` — empty report skeleton, one entry per slide.

Requires `soffice` (LibreOffice) and `pdftoppm` (poppler-utils) on `$PATH`. If either is missing, the script fails with an actionable message telling you how to install them.

### Apply the prompt

Have Claude read every JPEG, follow `review_prompt.md`, and fill the report as `review_report.json` (drop the `.template` suffix) in the same directory. Each defect entry follows:

```json
{
  "severity": "critical | important | minor",
  "category": "overflow | alignment | legibility | palette | typography | title | empty",
  "description": "Be specific: which element, where on the slide."
}
```

### Summarize

```bash
python scripts/visual_review.py --summarize /tmp/review/review_report.json
```

Sample output:

```
Visual review summary for /mnt/user-data/outputs/deck.pptx
----------------------------------------------------------
Slide 1: 0 defects
Slide 2: 1 minor (legibility)
Slide 3: 1 critical (overflow), 1 important (alignment)
Slide 4: 0 defects
Slide 5: 0 defects

Total: 1 critical, 1 important, 1 minor across 5 slides.
```

Fix defects in the spec JSON (never in the `.pptx`), regenerate the deck, and re-run the prepare/apply/summarize loop until critical and important columns are empty.

### Manual fallback

If LibreOffice or poppler are not available, fall back to the manual workflow below.

---

## 1. Visual QA (manual)

Render the deck to per-slide JPEG images, then view each one.

### Commands

```bash
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless \
  --convert-to pdf /mnt/user-data/outputs/deck.pptx --outdir /tmp/
rm -f /tmp/aosis-slide-*.jpg
pdftoppm -jpeg -r 100 /tmp/deck.pdf /tmp/aosis-slide
ls -1 /tmp/aosis-slide-*.jpg
```

Then `view` each `.jpg` and scan for the symptoms below.

### Symptom → fix lookup table

| Symptom | Fix in spec |
|---|---|
| **Hero stat value too wide** — spans more than half the slide | Shorten the `value` (move `"mois"` / `"M€"` into the `label`). Keep `value` ≤ 7 chars. |
| **Stat values wrapping** in `stat_grid` | Switch to a shorter form (`"12 m"` not `"12 mois"`) and put the unit in the `label`. Keep `value` ≤ 6 chars. |
| **Matrix quadrant items overflowing** | Cap at 3 items per quadrant, keep each item to 5-6 words. |
| **Roadmap labels colliding** | Too many milestones too close together. Reduce to 5 milestones max for safety. |
| **Funnel value column overflowing** | Keep `value` short (`"85"` not `"85 reports validés"`). |
| **Chart highlight semantics off** | `"highlight": "min"` when smallest = good outcome; `"highlight": "max"` when largest = good outcome. |

---

## 2. Content QA

After visual QA, sweep for stray placeholder text — the kind of artefact left over from quickly-edited specs.

```bash
extract-text /mnt/user-data/outputs/deck.pptx \
  | grep -iE "\bx{3,}\b|lorem|\bTODO|\[insert|\[à remplir"
```

Patterns caught :

- `xxxx` (three or more x's in a row) — leftover stub
- `lorem` — Lorem ipsum placeholder
- `TODO` — author note never resolved
- `[insert` — bracketed instruction never resolved
- `[à remplir` — French bracketed instruction never resolved

A clean run prints nothing.

---

## 3. The iron rule

**Always fix in the spec JSON, never by post-editing the `.pptx`.**

Post-editing creates two problems :
1. The next regeneration overwrites your manual fix.
2. The skill's invariants (template inheritance, palette, fonts) cease to be guaranteed once the file has been hand-touched.

When QA flags an issue, change the spec, rerun the build script, and re-QA. **Stop after one fix-and-verify pass** unless a new user-visible defect appears — chasing micro-defects past the second pass usually means the spec needs structural rework, not another tweak.
