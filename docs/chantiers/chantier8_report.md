# Chantier 8 — Câblage matplotlib pour le layout `kpi_with_chart`

**Date** : 2026-05-19
**Périmètre** : Rendre le placeholder `{{CHART_PLACEHOLDER}}` du layout `kpi_with_chart` exploitable en générant un chart matplotlib aux dimensions exactes de la zone réservée, avec 8 types supportés (bar, barh, bar_stacked, line, donut, pie, combo, waterfall).

## TL;DR

- ✅ Nouveau module **`scripts/chart_engine.py`** (8 renderers + palette injectable).
- ✅ Pipeline `template_engine` étendu d'une étape **`_process_chart_placeholder`** entre indexed et simple placeholders.
- ✅ **22 tests pytest verts** (+1 skip soffice), dont 8 nouveaux (un par type de chart) et reactivation de l'assertion chart sur `test_template_kpi_with_chart`.
- ✅ Fixture `tests/fixtures/chart_specs.json` + section dédiée dans `references/json-schema.md`.
- ✅ Deck de validation [chantier8_assets/validation_chart_deck.pptx](chantier8_assets/validation_chart_deck.pptx) — 10 slides (cover + 8 charts + closing).
- ⚠️ Refactorisation potentielle du code chart code-based (`_render_chart_png` dans `build_deck.py`) **non effectuée** — voir §5.

## 1. Architecture

```
┌──────────────────────────────────────────────────────────┐
│ build_deck.py                                            │
│   ├─ at module load:                                     │
│   │     chart_engine.set_brand(BRAND)                    │
│   │     # BRAND read live from theme XML                 │
│   ├─ on build_deck(--template custom):                   │
│   │     BRAND = BrandPalette.from_template(...)          │
│   │     chart_engine.set_brand(BRAND)  # rebind          │
│   └─ template_engine.render_template_slide(...)          │
│       └─ _process_chart_placeholder(slide, spec):        │
│           if {{CHART_PLACEHOLDER}} exists AND spec.chart:│
│               import chart_engine  (lazy)                │
│               png = render_chart_to_png(spec.chart,      │
│                                         placeholder.w,   │
│                                         placeholder.h)   │
│               slide.shapes.add_picture(BytesIO(png),     │
│                                        left, top, w, h)  │
│               remove placeholder                         │
└──────────────────────────────────────────────────────────┘
```

Trois découplages clés :

1. **`chart_engine` ne dépend d'aucun autre module du skill**. Il expose `set_brand(palette)` et `render_chart_to_png(chart_spec, w_emu, h_emu) → bytes`. Cela permet d'utiliser le moteur en isolation (futurs usages : génération de charts pour d'autres layouts, batch report, etc.).
2. **Lazy import matplotlib** au runtime dans `chart_engine` ET dans `template_engine` : si matplotlib est absent, l'engine se contente de retomber sur le pipeline normal (le placeholder sera traité par `_process_simple_placeholders` → suppression). Le skill reste opérationnel.
3. **Palette injectée par valeur, pas par référence d'import** : `chart_engine` ne fait pas `from build_deck import BRAND`. Aucun risque de cycle.

## 2. Types de chart supportés

| Type | Données attendues | Convention couleur |
|---|---|---|
| `bar` | `labels[]`, `values[]` | `accent1` (orange) |
| `barh` | `labels[]`, `values[]` (premier label en haut) | `accent1` (orange) |
| `bar_stacked` | `labels[]`, `series[].{name, values}` | cycle `accent1, accent2, accent4, accent5, accent3` |
| `line` | `labels[]`, `series[].{name, values}` | cycle multi-séries + data labels par point |
| `donut` | `labels[]`, `values[]`, optionnel `center_text` | cycle multi-séries, trou central 50 % |
| `pie` | `labels[]`, `values[]` | cycle multi-séries, % blancs gras |
| `combo` | `labels[]`, `bars.{name,values}`, `line.{name,values}` | bars orange + line navy_alt sur axe Y² |
| `waterfall` | `labels[]`, `values[]` (deltas OU niveaux cumulatifs) | gains vert (`accent5`), pertes rouge (`accent6`), totaux navy (`accent2`) |

Conventions visuelles communes (héritées de la charte AOSIS) :
- **Pas de titre matplotlib** (le titre vient du `{{TITLE}}` de la slide).
- **Pas de bordure** : spines top/right désactivées ; bottom/left gris discret.
- **Grille horizontale** très légère (`gray_light` = `lt2`).
- **Largeur barres 0.6**, **trou donut 0.5**, **DPI 150**.
- **Data labels** : au-dessus de chaque barre, sur chaque point line, % sur chaque part donut/pie.
- **Police DejaVu Sans** (matplotlib n'a pas Arial bundled mais DejaVu Sans est un sosie quasi-identique). Texte/axes couleur `dk1` (navy `#14163C`).

## 3. Modifications du code

### Nouveaux fichiers
- `aosis-deck-builder/scripts/chart_engine.py` (314 lignes)
- `aosis-deck-builder/tests/fixtures/chart_specs.json` (8 specs)

### Modifications
- `aosis-deck-builder/scripts/template_engine.py` :
  - Nouvelle fonction `_process_chart_placeholder(slide, spec)` (~ 30 lignes).
  - Insertion dans le pipeline de `render_template_slide` entre indexed et simple placeholders (1 ligne).
  - Aucune autre modification.
- `aosis-deck-builder/scripts/build_deck.py` :
  - Bloc `try/except ImportError` au module load pour `chart_engine.set_brand(BRAND)`.
  - Idem dans `build_deck()` pour rebind sur `--template custom`.
- `aosis-deck-builder/tests/test_smoke.py` :
  - 8 nouveaux tests `test_kpi_with_chart_<type>`.
  - Helper `_build_kpi_chart_slide()` factorisé pour éviter duplications.
  - Reactivation des assertions chart dans `test_template_kpi_with_chart` (PICTURE shape présente + placeholder retiré).
- `aosis-deck-builder/references/json-schema.md` :
  - Section « Charts in `kpi_with_chart` layout » documente les 8 types.
- `aosis-deck-builder/references/layouts.md` :
  - Ligne `kpi_with_chart` enrichie avec mention du rendu matplotlib + pointeur vers la section dédiée.
- `CHANGELOG.md` : entrée Chantier 8.

## 4. Tests

```
======================== 22 passed, 1 skipped in 2.09s =========================
```

| Test | Statut |
|---|---|
| `test_template_kpi_with_chart` | ✅ PASS (assertion chart re-activée) |
| `test_kpi_with_chart_bar` | ✅ PASS |
| `test_kpi_with_chart_barh` | ✅ PASS |
| `test_kpi_with_chart_bar_stacked` | ✅ PASS |
| `test_kpi_with_chart_line` | ✅ PASS |
| `test_kpi_with_chart_donut` | ✅ PASS |
| `test_kpi_with_chart_pie` | ✅ PASS |
| `test_kpi_with_chart_combo` | ✅ PASS |
| `test_kpi_with_chart_waterfall` | ✅ PASS |
| ...13 autres tests existants | ✅ PASS (aucune régression) |
| `test_visual_review_generates_artifacts` | ⏭ SKIP (soffice absent — pré-existant) |

Chaque test chart vérifie deux invariants :
1. Au moins une shape `PICTURE` (type 13) est insérée dans la slide → le chart a bien été rendu.
2. Aucune shape nommée `{{CHART_PLACEHOLDER}}` ne subsiste → la substitution a eu lieu.

## 5. Refactorisation non effectuée — `_render_chart_png` dans build_deck.py

Le skill possède déjà un layout `chart` code-based qui appelle `_render_chart_png(chart_spec, output_path)` dans `build_deck.py` (l.1193+). Cette fonction couvre `bar`, `column`, `barh`, `line`, `pie` mais pas les 4 types nouveaux (`bar_stacked`, `donut`, `combo`, `waterfall`).

Deux options ont été pesées :

**(A) Refactoriser `_render_chart_png` pour appeler `chart_engine.render_chart_to_png`** et garder une wrapper trivial.
- Pour : élimine une duplication partielle.
- Contre : `_render_chart_png` écrit sur fichier (`output_path`) alors que `chart_engine` retourne des bytes. Le wrapper devrait faire `Path(output_path).write_bytes(chart_engine.render_chart_to_png(...))`. Trivial, mais change la signature d'EMU vs inches (le layout `chart` code-based utilise figsize en inches `(7.5, 4.2)` hardcodé, alors que `chart_engine` lit la taille du placeholder en EMU). Une conversion serait nécessaire (passer figsize en EMU via Inches(7.5) etc.).
- Le périmètre stipule : *« Ne touche pas aux layouts code-based existants (sauf si tu repères du code de chart réutilisable que tu peux factoriser […]) »*. La factorisation est techniquement possible mais introduit une convergence partielle (les paramètres optionnels diffèrent légèrement : `highlight: max/min` existait dans l'ancien, je ne l'ai pas porté). **Non effectuée pour ne pas risquer de régression sur le layout `chart` code-based** que les tests `test_all_layouts_generate` exerce.

**(B) Laisser cohabiter les deux moteurs.**
- Choix retenu. Coût : ~50 lignes de logique de chart dupliquées (palette + types `bar/barh/line/pie` couverts par les deux).
- Bénéfice : aucun risque de régression sur le layout code-based, périmètre Chantier 8 strict.

**Suite recommandée (hors Chantier 8)** : un Chantier 9 dédié à la factorisation. Il faudra (a) étendre `chart_engine` pour supporter `highlight: max/min/<index>`, (b) ajouter un wrapper `render_chart_to_file(chart_spec, output_path, figsize_inches)`, (c) remplacer `_render_chart_png` par l'appel au wrapper, (d) vérifier visuellement que les decks `chart`/`dashboard` code-based rendent identique.

## 6. Validation end-to-end

[chantier8_assets/validation_chart_deck.pptx](chantier8_assets/validation_chart_deck.pptx) — 10 slides :

| # | layout | type chart | titre |
|---:|---|---|---|
| 1 | cover | — | Validation Chantier 8 — 8 types de chart |
| 2 | kpi_with_chart | bar | Revenu trimestriel — répartition par trimestre |
| 3 | kpi_with_chart | barh | Parts de marché — top 4 pays européens |
| 4 | kpi_with_chart | bar_stacked | Volume par produit, trimestre après trimestre |
| 5 | kpi_with_chart | line | Trajectoire réelle vs cible — 5 mois |
| 6 | kpi_with_chart | donut | Mix d'infrastructure — 100 % couvert |
| 7 | kpi_with_chart | pie | Funnel commercial — 60 % d'acquis |
| 8 | kpi_with_chart | combo | Revenu et marge trimestriels |
| 9 | kpi_with_chart | waterfall | Décomposition du gain net 2024 |
| 10 | closing | — | — |

Validation visuelle utilisateur attendue dans PowerPoint. L'agent n'a pas accès à `soffice`/PowerPoint COM, donc pas de JPEG côté agent.

## 7. Frictions techniques

1. **Pas de Arial bundled dans matplotlib** : par défaut matplotlib utilise sa propre police. Choix `DejaVu Sans` (sosie d'Arial, métrique très proche). Si l'utilisateur tient à du Arial strict dans les charts, on peut `rcParams["font.family"] = ["Arial", "DejaVu Sans"]` mais matplotlib loggera un warning si Arial absent. **Non implémenté** — le rendu reste consulting-grade avec DejaVu Sans.

2. **Waterfall — ambiguïté delta vs niveau cumulatif** : le format JSON est `values: [100, 30, 20, -15, 135]`. Deux interprétations : (a) `values[0]=start`, `values[1..-2]=deltas`, `values[-1]=end` ; (b) tous niveaux cumulatifs. Heuristique implémentée : si `start + sum(intermediates) == end` (à 1e-6 près), traiter comme deltas ; sinon dériver des deltas par différences successives. Couvre les deux conventions naturelles.

3. **Combo — légende combinée** : matplotlib ne combine pas automatiquement les légendes de deux axes (`ax` et `ax.twinx()`). Code explicite pour fusionner `handles1+handles2`.

4. **Test sur `test_template_kpi_with_chart`** : le test précédent (assoupli au chantier précédent) attendait uniquement que titre + KPIs soient remplis. La spec de test a été enrichie d'un `chart: {...}` afin de pouvoir réactiver l'assertion PICTURE / placeholder absent.

## 8. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/chart_engine.py` | **créé** (314 lignes) |
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+33 lignes) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (+12 lignes, injections palette) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+8 tests, helper, reactivation) |
| `aosis-deck-builder/tests/fixtures/chart_specs.json` | **créé** |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (section charts) |
| `aosis-deck-builder/references/layouts.md` | **modifié** (1 ligne) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 8) |
| `chantier8_report.md` | **créé** (ce fichier) |
| `chantier8_assets/validation_chart_deck.pptx` | **créé** (10 slides) |

## 9. Suites possibles (hors scope Chantier 8)

- **Chantier 9 — Refactorisation** : faire converger `build_deck._render_chart_png` vers `chart_engine.render_chart_to_png` pour supprimer la duplication. ~150 lignes de réduction, ~2h de travail incluant validation visuelle des layouts `chart`/`dashboard` code-based.
- **Ajout de types** : `radar`, `bubble`, `sankey`, `heatmap`. Pas dans la spec utilisateur, à demander au chef si besoin.
- **Annotations** : permettre une clé `annotations: [{x, y, text}]` pour ajouter des callouts sur les charts (cas typique : pointer sur le pic d'un line chart).
- **Theme override** : permettre `chart.colors: ["#XXXXXX", ...]` pour forcer une palette ad-hoc sur un chart précis (cas typique : reproduire un benchmark publié).

---

**Statut final** : ✅ Chantier 8 **livré sans régression**. 22/23 tests verts (1 skip soffice pré-existant), 8 types de chart câblés, deck de validation disponible.
