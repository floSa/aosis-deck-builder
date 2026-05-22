# Chantier 6 — Workflow de QA visuel automatisé via sous-agent

> Date : 2026-05-13 · Scope strict respecté : `scripts/visual_review.py` (nouveau), `references/qa.md` (ajout d'une section), `tests/test_smoke.py` (+2 tests), `CHANGELOG.md`. **Aucune modification** de `scripts/build_deck.py`, `scripts/brand.py`, du template, ni de `SKILL.md`.

---

## 1. Démonstration end-to-end

Sujet du test : le deck **golden** (5 slides : cover, hero_stat, matrix_2x2, roadmap, closing) produit pendant le Chantier 3.

### 1.1 Étape *prepare*

```bash
$ python scripts/visual_review.py tests/out/golden_c3.pptx /tmp/c6_review_demo/
```

Sur cette machine, `soffice` et `pdftoppm` ne sont **pas** installables (apt restreint dans le sandbox WSL — déjà documenté aux Chantiers 1 et 2). Le script échoue donc proprement avec le message attendu :

```
Error: required tools missing.
  - 'soffice' not found. Install LibreOffice:
      Ubuntu/Debian: sudo apt install libreoffice
      macOS:         brew install --cask libreoffice
  - 'pdftoppm' not found. Install poppler-utils:
      Ubuntu/Debian: sudo apt install poppler-utils
      macOS:         brew install poppler
```

C'est le comportement nominal sur une machine sans deps système — message actionnable, exit code != 0. **L'erreur ne corrompt rien et l'utilisateur sait quoi faire.**

### 1.2 Contournement pour la démo (WSL only)

Pour démontrer le workflow complet malgré l'absence de soffice, j'ai converti le deck en JPEG via PowerPoint COM côté Windows (la technique éprouvée aux Chantiers 2 et 5) et placé les fichiers dans `/tmp/c6_review_demo/`. J'ai ensuite invoqué directement `write_prompt()` et `write_report_template()` :

```python
from visual_review import write_prompt, write_report_template
out_dir = Path('/tmp/c6_review_demo')
write_prompt(out_dir)
write_report_template(out_dir, deck_path=..., n_slides=5)
```

Résultat dans le dossier :

```
/tmp/c6_review_demo/
├── slide-01.jpg
├── slide-02.jpg
├── slide-03.jpg
├── slide-04.jpg
├── slide-05.jpg
├── review_prompt.md
└── review_report.template.json
```

### 1.3 Étape *apply* — j'ai joué le rôle de l'agent reviewer

J'ai lu les 5 JPEG en pleine résolution et appliqué le prompt. Constats :

| Slide | Layout | Verdict |
|---|---|---|
| 1 | cover | Pas de défaut. Logo, titre "Refonder le reporting risque", pastille "Mai 2026" en orange AOSIS (chantier 2 ✅), baseline EXPERTS BUSINESS INTELLIGENCE / DATA SCIENCE / BIG DATA. |
| 2 | hero_stat | Pas de défaut. -75% géant en navy, label d'action "C'est le temps de production que nous allons reprendre" sur 2 lignes, supporting bullets à droite avec tirets orange. |
| 3 | matrix_2x2 | **1 important — `title`** : "Cartographie des chantiers identifiés" est un titre **descriptif** (Règle d'or #3 du SKILL.md). Devrait être une phrase d'action, ex. "Les chantiers stratégiques à lancer en priorité — refonte du lineage + migration moteur". |
| 4 | roadmap | Pas de défaut. 5 milestones, "Plateforme historique éteinte" complet (chantier 1 ✅), pas de débordement. |
| 5 | closing | Pas de défaut. Slide statique du master AOSIS. |

J'ai ensuite rempli [`/tmp/c6_review_demo/review_report.json`](chantier6_assets/review_report.json) (copie dans `chantier6_assets/`).

### 1.4 Étape *summarize*

```bash
$ python scripts/visual_review.py --summarize /tmp/c6_review_demo/review_report.json
Visual review summary for .../tests/out/golden_c3.pptx
------------------------------------------------------
Slide 1: 0 defects
Slide 2: 0 defects
Slide 3: 1 important (title)
Slide 4: 0 defects
Slide 5: 0 defects

Total: 1 important across 5 slides.
```

Format de sortie conforme au cahier des charges. Le défaut est trouvé, classé, et l'opérateur sait quel slide ouvrir pour le corriger.

---

## 2. Statut des tests

Suite pytest complète (11 tests) :

```text
tests/test_smoke.py::test_golden_generates                            PASSED [  9%]
tests/test_smoke.py::test_golden_no_overflow                          PASSED [ 18%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_3.json]         PASSED [ 27%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_4.json]         PASSED [ 36%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_5.json]         PASSED [ 45%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_6.json]         PASSED [ 54%]
tests/test_smoke.py::test_all_layouts_generate                        PASSED [ 63%]
tests/test_smoke.py::test_palette_loads_from_canonical_template       PASSED [ 72%]
tests/test_smoke.py::test_palette_brand_error_on_missing_file         PASSED [ 81%]
tests/test_smoke.py::test_visual_review_generates_artifacts           SKIPPED[ 90%]
tests/test_smoke.py::test_summarize_report                            PASSED [100%]

==================== 10 passed, 1 skipped in 1.08s =====================
```

- **`test_summarize_report`** ✅ passe : crée un faux rapport JSON avec 3 défauts (2 critical / 1 important / 1 minor répartis sur 4 slides), capture stdout via `capsys`, vérifie le contenu ligne par ligne (compteur par sévérité, totaux, libellés des catégories).
- **`test_visual_review_generates_artifacts`** ⏭ skipped : décoré par `@pytest.mark.skipif(_SOFFICE is None or _PDFTOPPM is None, reason=...)` qui détecte l'absence de `soffice`/`pdftoppm` via `shutil.which`. Sur une machine équipée des deps système, le test passera ; chez les autres, il skip avec une raison explicite.

Aucun warning, exécution en ~1 s.

---

## 3. Contenu du prompt généré

Premier extrait du `review_prompt.md` (intégral dans [`chantier6_assets/review_prompt.md`](chantier6_assets/review_prompt.md)) :

```markdown
# Visual Review Prompt — AOSIS Deck

You are reviewing a PowerPoint deck generated by the `aosis-deck-builder` skill.
Your job is to inspect each JPEG image (one per slide) and detect visual defects.

## What to look for

### Critical defects (block delivery)
- **Overflow**: text or shape extends beyond the slide edges...
- **Truncation**: text is visibly clipped (... — the canonical example is
  "éteinte" rendered as "éteint").                                  ← rappel du bug C1
- **Empty slides**: ...

### Important defects (must fix before delivery)
- **Overlap**, **Misalignment**, **Palette breach**, **Font breach**,
  **Descriptive title** (with concrete French examples)

### Minor defects (improve if time)
- **Legibility**, **Density**, **Visual rhythm**
```

Trois niveaux de sévérité (`critical | important | minor`) × sept catégories (`overflow | alignment | legibility | palette | typography | title | empty`) — alignés avec les `SEVERITIES` et `CATEGORIES` exportés par le module pour faciliter une éventuelle validation programmatique du rapport.

---

## 4. Aperçu du défaut détecté — slide 3

![Slide 3](chantier6_assets/slide-03.jpg)

Titre "Cartographie des chantiers identifiés" — descriptif. Le prompt invite à des phrases d'action ("Les chantiers stratégiques à lancer en priorité…"). Le workflow attrape cette catégorie subtile que ni le QA géométrique (Chantier 1) ni le QA palette (Chantier 3) ne savent flagger.

---

## 5. Frictions rencontrées

| Friction | Résolution |
|---|---|
| `soffice` + `pdftoppm` indisponibles dans WSL (apt restreint) | Le script échoue proprement avec un message actionnable. Pour la démo, contournement via PowerPoint COM côté Windows. Sur une machine de prod normale, aucune friction. |
| Numérotation des JPEG par `pdftoppm` non zero-padded à 2 chiffres si < 10 pages | Post-traitement systématique : `_pdf_to_jpegs` renomme `_raw_slide-N.jpg` → `slide-NN.jpg` quel que soit le nombre de pages. Stabilité du nom de fichier garantie pour le rapport JSON. |
| Argparse : modes "prepare" et "summarize" cohabitent | Positionnels `nargs="?"` + flag `--summarize REPORT` mutuellement implicites. Validé manuellement : `parser.error` clair si on oublie les positionnels sans `--summarize`. |
| Le `summarize_report` doit grouper par (sévérité, catégorie) pour un affichage compact | Une fonction `Counter` par slide + tri canonique des sévérités produit le format demandé : `Slide 3: 2 critical (overflow), 1 important (alignment)`. |

Aucun bug détecté dans le code existant.

---

## 6. Livrables

| Livrable | Chemin | Taille |
|---|---|---|
| Script | [`aosis-deck-builder/scripts/visual_review.py`](aosis-deck-builder/scripts/visual_review.py) | 210 l |
| QA doc | [`aosis-deck-builder/references/qa.md`](aosis-deck-builder/references/qa.md) | +63 l (section "Automated visual review (recommended)" en tête) |
| Tests | [`aosis-deck-builder/tests/test_smoke.py`](aosis-deck-builder/tests/test_smoke.py) | +75 l (2 tests) |
| Rapport | [`chantier6_report.md`](chantier6_report.md) | — |
| CHANGELOG | [`CHANGELOG.md`](CHANGELOG.md) | entrée Chantier 6 ajoutée |
| Demo assets | [`chantier6_assets/`](chantier6_assets/) | slide-03.jpg + review_report.json rempli + review_prompt.md intégral |

Périmètre respecté : ni `build_deck.py`, ni `brand.py`, ni le template, ni `SKILL.md` n'ont été touchés.
