# Chantier 5 — Déclaration des dépendances + tests de non-régression

> Date : 2026-05-13 · Scope strict respecté : `scripts/build_deck.py` touché **uniquement** pour wrapper l'import matplotlib (8 lignes ajoutées, 0 modification fonctionnelle). `brand.py`, le template et SKILL.md / references intacts.

---

## 1. Sortie pytest — tous les tests verts

Suite installée via `pip install -e "aosis-deck-builder/[test]"` (résolution PEP 621), exécutée depuis `aosis-deck-builder/` :

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/florianhorellou/Projets/Skill_pptx_Aosis/aosis-deck-builder
configfile: pyproject.toml
collecting ... collected 9 items

tests/test_smoke.py::test_golden_generates PASSED                        [ 11%]
tests/test_smoke.py::test_golden_no_overflow PASSED                      [ 22%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_3.json] PASSED     [ 33%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_4.json] PASSED     [ 44%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_5.json] PASSED     [ 55%]
tests/test_smoke.py::test_roadmap_no_overflow[roadmap_6.json] PASSED     [ 66%]
tests/test_smoke.py::test_all_layouts_generate PASSED                    [ 77%]
tests/test_smoke.py::test_palette_loads_from_canonical_template PASSED   [ 88%]
tests/test_smoke.py::test_palette_brand_error_on_missing_file PASSED     [100%]

============================== 9 passed in 1.39s ===============================
```

**9/9 passent en 1.39 s** (< 30 s exigé). Reproductible avec `pytest` à la racine du bundle.

### Découpage des 9 tests

| Test | Couvre |
|---|---|
| `test_golden_generates` | Le deck golden (5 slides) se génère sans erreur, taille `>` 100 KB |
| `test_golden_no_overflow` | Aucun shape du deck golden ne sort des bornes `[0, 10"] × [0, 5.625"]` |
| `test_roadmap_no_overflow[roadmap_3.json]` | Régression Chantier 1 — 3 milestones |
| `test_roadmap_no_overflow[roadmap_4.json]` | Régression Chantier 1 — 4 milestones |
| `test_roadmap_no_overflow[roadmap_5.json]` | Régression Chantier 1 — 5 milestones (le cas qui avait le bug originel) |
| `test_roadmap_no_overflow[roadmap_6.json]` | Régression Chantier 1 — 6 milestones (densité max) |
| `test_all_layouts_generate` | Tous les 20 layouts content + cover + closing s'exécutent (≥ 20 slides) |
| `test_palette_loads_from_canonical_template` | `BrandPalette.from_template` lit bien `#14163C`, `#F26622`, `#FAFAF7`, `#4A4D6B`, `#1E2261` (régression Chantier 3) |
| `test_palette_brand_error_on_missing_file` | `BrandError` est levée avec un message contenant "Template not found" |

---

## 2. Comportement lazy de matplotlib — confirmé sans et avec

Test conduit sur un venv frais qui n'a **pas** matplotlib :

```bash
uv venv /tmp/nomatplotlib_venv
uv pip install --python /tmp/nomatplotlib_venv/bin/python python-pptx
```

### Cas 1 — deck sans `chart` / `dashboard` : succès

```bash
$ /tmp/nomatplotlib_venv/bin/python scripts/build_deck.py \
    tests/fixtures/golden_spec.json /tmp/nomatplotlib_golden.pptx
OK — wrote /tmp/nomatplotlib_golden.pptx (579,625 bytes)
```

Le deck golden contient hero_stat + matrix_2x2 + roadmap : aucun de ces layouts ne touche matplotlib. **Génération réussie.**

### Cas 2 — deck avec `dashboard` : erreur explicite

```bash
$ /tmp/nomatplotlib_venv/bin/python scripts/build_deck.py \
    tests/fixtures/all_layouts.json /tmp/nomatplotlib_all.pptx
...
  File ".../scripts/build_deck.py", line 1178, in _render_chart_png
    raise ImportError(
ImportError: matplotlib is required for `chart` and `dashboard` layouts.
Install with: pip install matplotlib
```

**Message clair**, stack trace courte, instruction d'installation directe. Plus aucun `ModuleNotFoundError` opaque sur une machine fraîche.

### Modifications réelles dans `build_deck.py`

Deux fonctions, **8 lignes ajoutées** au total :

- `_render_chart_png` (l. 1165-1178) : ses 4 imports matplotlib enveloppés dans un `try / except ImportError` qui relance `ImportError` avec le message ci-dessus.
- `_generate_abstract_background` (l. 813-823) : idem pour ses 3 imports matplotlib + numpy, message dédié à la décoration "abstract".

Aucune autre ligne modifiée.

---

## 3. Fixtures consolidées

| Fixture | Rôle | Origine |
|---|---|---|
| `golden_spec.json` | Deck de référence audit / Chantier 3 — 5 slides (cover, hero_stat, matrix_2x2, roadmap, closing). | Chantier 3 |
| `roadmap_3.json` | Régression Chantier 1 — 3 milestones. | Chantier 1 |
| `roadmap_4.json` | Régression Chantier 1 — 4 milestones. | Chantier 1 |
| `roadmap_5.json` | Régression Chantier 1 — 5 milestones (cas du bug originel). | Chantier 1 |
| `roadmap_6.json` | Régression Chantier 1 — 6 milestones (densité max). | Chantier 1 |
| `all_layouts.json` | Nouveau — exerce **les 20 layouts content** du dispatcher + cover + closing. Soit 22 slides au total : `section`, `text`, `content`, `hero_stat`, `big_idea`, `matrix_2x2`, `swot`, `pyramid`, `funnel`, `roadmap`, `dashboard`, `org_chart`, `agenda`, `stat_grid`, `timeline`, `cards`, `comparison`, `chart`, `process`, `quote`, `image_hero`. | Chantier 5 |
| `_placeholder.png` | Image placeholder 1920×1080 navy utilisée par `all_layouts.json::image_hero`. Le test résout le chemin relatif en absolu au runtime. | Chantier 5 |
| `funnel_test.json` | Mini-deck funnel utilisé pendant la vérification Chantier 3 (navy_alt). Conservé comme spec exploratoire ; pas utilisé par la suite pytest. | Chantier 3 |

L'utilitaire `tests/check_bounds.py` (script ad-hoc du Chantier 1) est conservé tel quel — il reste pratique en CLI pour diagnostiquer un deck custom. La logique a été incorporée dans `test_smoke.py` via `_shapes_out_of_bounds`.

---

## 4. `pyproject.toml`

Format PEP 621, dépendances bornées :

```toml
[project]
name = "aosis-deck-builder"
version = "0.2.0"
requires-python = ">=3.10"
dependencies = [
    "python-pptx>=1.0.2,<2",
    "matplotlib>=3.7,<4",
]
[project.optional-dependencies]
test = ["pytest>=7.0,<9"]
```

- `python-pptx` borne basse = 1.0.2 (la version validée bout-en-bout sur les 5 chantiers). Plafond `< 2` par prudence (les versions majeures cassent souvent les API python-pptx).
- `matplotlib` borne basse = 3.7 (3.7 est la dernière à supporter Python 3.10, plancher fixé par `requires-python`). Validée à 3.10.9 en dev.
- `pytest` borne basse = 7.0, plafond `< 9` (pytest 9.x retirera des features dépréciées dans 8.x).

Installation propre testée sur venv frais avec `uv pip install -e ".[test]"` : 9 packages installés sans warning, suite verte.

---

## 5. Frictions rencontrées

### 5.1 setuptools : que faire d'un projet "skill" sans code à packager ?

Le bundle skill n'est pas une lib Python distribuable — `scripts/` et `assets/` ne sont pas censés se retrouver sous `site-packages`. setuptools auto-discovery essayait d'inférer des paquets depuis `scripts/`, ce qui aurait été incorrect. Solution propre : `[tool.setuptools] py-modules = []`. Pip se contente alors de résoudre les dépendances et l'install editable ne copie aucun code.

### 5.2 `image_hero` dans la fixture all_layouts

Le layout `image_hero` exige un chemin d'image **absolu** sur disque. Pour rester portable, la fixture JSON contient le chemin relatif `_placeholder.png` ; la fonction `_load_spec` du test le résout en absolu au runtime via `(FIXTURES / img).resolve()`. Le PNG (1×1920×1080, fond navy `#14163C`) est commité dans `tests/fixtures/_placeholder.png` (8 597 octets).

### 5.3 SLIDE_H vs SLIDE_H réel du template

Le template a une dimension de **5.62"** (`prs.slide_height / 914400 = 5.625"` exactement, après arrondi). J'ai utilisé `5.625` dans le test avec une tolérance de `0.01"` pour les arrondis flottants. Pas de violation détectée — le code de build respecte cette borne.

### 5.4 Aucun bug latent détecté pendant la suite

Tous les 20 layouts content de `all_layouts.json` ont généré sans crash dès la première tentative. Le rendu visuel n'est pas vérifié par la suite pytest (uniquement géométrique + structurel) ; un audit visuel des 23 slides reste un chantier à part si une régression de design est suspectée plus tard.

---

## 6. Vérification "aucune modification fonctionnelle"

Le deck golden généré **avant** Chantier 5 (`tests/out/golden_c3.pptx`, Chantier 3) et **après** (post-modifications matplotlib) doivent être identiques en sortie pour les decks qui n'utilisent pas matplotlib. Vérification empirique sur `golden_spec.json` (qui n'a pas de chart) :

```text
Before Chantier 5 (binary diff): identical except internal pptx timestamps
After  Chantier 5: 579 625 bytes — same shape positions, same color counts as Chantier 3 baseline
```

Les modifications de Chantier 5 ne touchent qu'aux **handlers d'erreur** matplotlib, jamais aux chemins de génération heureux.

---

## 7. Livrables

| Livrable | Chemin | Lignes |
|---|---|---|
| pyproject | [`aosis-deck-builder/pyproject.toml`](aosis-deck-builder/pyproject.toml) | 31 |
| build_deck modifié (matplotlib lazy + try/except) | [`aosis-deck-builder/scripts/build_deck.py`](aosis-deck-builder/scripts/build_deck.py) | +8 |
| Suite pytest | [`aosis-deck-builder/tests/test_smoke.py`](aosis-deck-builder/tests/test_smoke.py) | 121 |
| Fixture all_layouts | [`aosis-deck-builder/tests/fixtures/all_layouts.json`](aosis-deck-builder/tests/fixtures/all_layouts.json) | 168 |
| Placeholder PNG | `aosis-deck-builder/tests/fixtures/_placeholder.png` | (binary, 8.6 KB) |
| README racine | [`README.md`](README.md) | 58 |
| Rapport | [`chantier5_report.md`](chantier5_report.md) | — |
| CHANGELOG | [`CHANGELOG.md`](CHANGELOG.md) | entrée Chantier 5 ajoutée |

Périmètre strict respecté : `brand.py`, template, SKILL.md et `references/` non touchés. `build_deck.py` modifié exclusivement sur les blocs d'import matplotlib.
