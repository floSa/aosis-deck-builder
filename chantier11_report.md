# Chantier 11 — Polish post-deck réel : roadmap, matrix, sommaire, images

**Date** : 2026-05-19
**Périmètre** : 4 défauts identifiés sur `examples/test_migration_cloud.pptx` après Chantier 10. Fixés en un seul passage.

## TL;DR

| # | Fix | Statut |
|---:|---|---|
| 1 | Roadmap labels : anchor bottom au-dessus, anchor top en-dessous, auto-shrink | ✅ |
| 2 | Matrix : max 3 bullets, auto-shrink, anchor bottom-left | ✅ |
| 3 | Sommaire : retour à 7 max + espacement plus aéré (gap = 0.5 × item_h) | ✅ |
| 4 | Images Unsplash automatiques sur `{{IMAGE}}` | ✅ via Lorem Picsum (Unsplash Source mort) |

**Tests** : **42 passed, 1 skipped** (5 nouveaux tests).
**Deck régénéré** : `examples/test_migration_cloud.pptx` (852 KB, 7 photos Picsum téléchargées en ~12 s).

## Fix 1 — Roadmap labels anchored to bottom (above) / top (below)

Nouvelle fonction `_apply_layout_postprocess(grp_element, layout_name, index)` appelée après `_apply_alternation` sur chaque copie REPEAT_ITEM. Pour `roadmap_styled` :
- Copies à index pair (0, 2, 4 = 1, 3, 5 en 1-indexed) → above-axis → `bodyPr@anchor="b"` sur `{{ITEM_DATE}}` et `{{ITEM_MILESTONE}}`. Le texte grandit vers le haut.
- Copies à index impair (1, 3) → below-axis → `bodyPr@anchor="t"` (défaut explicite).
- Auto-shrink sur le texte (clé `value`/`date`/`action`/`owner` n'est pas requise — le shrink est appliqué sur le contenu littéral, pas via SHRINKABLE_ITEM_KEYS).

Helpers ajoutés :
- `_set_text_anchor(sp_element, anchor)` patche `<a:bodyPr@anchor>`.
- `_read_sp_text(sp_element)` extrait le texte d'un `<p:sp>` pour le shrink.

Test : `test_roadmap_labels_dont_overlap_axis` ✓ (vérifie l'attribut anchor sur les 5 copies).

## Fix 2 — Matrix : max 3 bullets + auto-shrink + bottom-anchor

Dans `_process_quad_placeholders` :
- Si `value` est une liste pour la clé `bullets`/`items` ET `len > 3` → tronque à 3, warning stderr.
- Après substitution : `_set_text_anchor(sh._element, 'b')` (text-bottom-aligned dans le quadrant).
- `_maybe_shrink_to_fit(sh._element, str(value), min_sz=1000)` (chantier 10) appliqué pour éviter débordement.

Test : `test_matrix_truncates_bullets_to_3` ✓ (5 bullets → A1/A2/A3 conservés, A4/A5 absents, warning détecté).

Effet sur le deck migration :
```
matrix_2x2_styled: quad 'top_left' has 4 bullets, truncated to 3
matrix_2x2_styled: quad 'top_right' has 4 bullets, truncated to 3
```
4 items → 3 affichés sur top_left et top_right.

## Fix 3 — Sommaire : retour à 7 max + spacious

```python
PAGINATED_LAYOUTS = {'agenda_diagonal': 7}
```

Distribution `single_column` retravaillée :
- Target gap = `0.5 × base_h` quand le total `n × base_h + (n-1) × gap` rentre dans `slide_h - base_top - 0.5"`.
- Si ne rentre pas : réduit le gap (plancher `0.05"`) puis compresse `item_h`.

Pour 7 items avec `base_h = 0.38"` :
- Target : `7 × 0.38 + 6 × 0.19 = 3.80"` qui rentre dans ~4.12" available.
- Gap effectif : `0.19"` (= 0.5 × 0.38). Aéré.

Tests renommés : `test_agenda_paginates_at_10_items` → `test_agenda_paginates_at_7_items` (9 items → 7+2). Numérotation continue 01-07 / 08-09 vérifiée.

## Fix 4 — Images automatiques

### Nouveau module `scripts/image_engine.py` (150 lignes)

**API publique** :
```python
fetch_image_for_slide(keyword, width_emu, height_emu, timeout=8.0) -> bytes | None
extract_keyword_from_title(title, max_words=3) -> str
LAYOUT_DEFAULT_KEYWORDS  # dict {layout_name: keyword}
```

**Providers chainés** :
1. **Unsplash API officielle** si `UNSPLASH_API_KEY` env var — query `?query=<kw>&per_page=1&orientation=landscape`, télécharge l'URL `regular`.
2. **Unsplash Source** (`source.unsplash.com`) — déprécié par Unsplash en 2023, retourne 503 ; gardé pour le jour où ils le ressusciteront.
3. **Lorem Picsum** (`picsum.photos`) — fallback, pas d'API key, seed déterministe pour stabilité. Retry léger (1 attempt en cas d'erreur transient).

**Extraction de mot-clé** : tokenize les caractères Unicode latins de `title`, filtre stop-words FR/EN (`le`, `de`, `the`, `our`…) et tokens < 3 chars, garde les 3 premiers.

Pour « Migration vers le cloud » → `"migration cloud"`.
Pour « Vision & recommandation stratégique » → `"vision recommandation stratégique"`.

**Mot-clé par défaut par layout** :
- `cover` → `"business technology"`
- `agenda_diagonal` → `"planning strategy"`
- `section_diagonal` → `"abstract corporate"`
- `closing_diagonal` → `"team success"`
- `final_branding` → `"team success"`
- `quote_callout` → `"leadership office"`

### Intégration dans `template_engine._process_image_placeholders`

Ordre de résolution :
1. `spec.image` (chemin local) — comportement legacy
2. `spec._auto_images` est `True` (par défaut) → fetch automatique
3. Sinon laisse le `{{IMAGE}}` placeholder en place

### Flag CLI / kwarg

```bash
python build_deck.py spec.json out.pptx --no-images   # désactive auto-fetch
```

`build_deck(spec, out, ..., auto_images=True)` — kwarg propage en injection `spec._auto_images` par slide.

### Bug Unicode corrigé

Premier essai : le seed `"vision recommandation stratégique"` cassait avec `UnicodeEncodeError` (urllib n'accepte que des URLs ASCII). Fix :
```python
import unicodedata
ascii_kw = unicodedata.normalize('NFD', keyword).encode('ascii', 'ignore').decode('ascii')
seed = re.sub(r'[^a-z0-9]+', '-', ascii_kw.lower()).strip('-')
```
« stratégique » → « strategique » → URL ASCII pure.

### Performance

- `--no-images` : **0.93 s** (identique à pré-chantier 11)
- Avec auto-images sur deck migration (7 placeholders à remplir) : **~12 s** (~1.5s par image, dominé par latence réseau + le 503 d'Unsplash Source comptant pour ~0.3s par essai).

Optimisations possibles (Chantier 12 candidat) :
- Cache disque (`~/.cache/aosis-deck-builder/images/`) par seed
- Téléchargements parallèles via `concurrent.futures.ThreadPoolExecutor`
- Skip directement Unsplash Source par défaut (ajouter check de disponibilité au module load)

### Tests

| Test | Couvre |
|---|---|
| `test_image_engine_keyword_extraction` | extraction du mot-clé, stop words FR/EN |
| `test_image_engine_handles_network_failure` | mock fail sur les 3 providers → return None, build ne crash pas |
| `test_image_inserted_in_cover` | mock fetch retournant PNG 1×1 → vérif PICTURE inséré + `{{IMAGE}}` supprimé |

Tous ✓.

## Validation visuelle — `examples/test_migration_cloud.pptx`

```
OK — wrote examples/test_migration_cloud.pptx (852,435 bytes)  ~12s
```

| Slide | Avant Chantier 11 | Après |
|---:|---|---|
| 2 (agenda_diagonal, 6 items) | dense | espacement aéré 0.5×item_h ✓ |
| 3, 9, 14 (section_diagonal) | `{{IMAGE}}` placeholder visible | photo Picsum téléchargée et insérée ✓ |
| 7 (matrix_2x2_styled) | 4 bullets par quadrant top_left/top_right | tronqué à 3, anchor bottom, warning stderr ✓ |
| 17 (roadmap_styled) | labels grandissant vers la ligne | anchor bottom sur copies 0,2,4 (above) ; top sur 1,3 (below) ✓ |
| 20 (closing_diagonal) | `{{IMAGE}}` visible | photo « team success » téléchargée ✓ |

## Frictions résiduelles

1. **Unsplash Source mort** → on dépend de Picsum. Avantage : aucune clé requise, sémantiquement les images sont aléatoires (Picsum sert des photos Unsplash mais indexées par seed, pas par mot-clé). Si l'utilisateur veut des photos qui matchent vraiment le keyword, configurer `UNSPLASH_API_KEY` (clé Dev gratuite sur unsplash.com/developers).
2. **Latence de génération** : 12s avec auto_images, principalement à cause du séquentiel HTTP. Cache disque + parallélisme → candidat Chantier 12.
3. **Mot-clé par défaut roadmap_styled / matrix_2x2_styled / executive_summary / etc.** : non défini. Ces layouts n'ont pas de `{{IMAGE}}` aujourd'hui donc neutre, mais si un futur template en ajoute un, fallback sur `"corporate"` générique.

## Suggestion template (non-modif AOSIS_template.pptx ici)

Pour permettre `bodyPr@anchor` de fonctionner pleinement sur roadmap_styled, le user pourrait augmenter légèrement la hauteur des shapes `{{ITEM_DATE}}` et `{{ITEM_MILESTONE}}` dans le template (passer de ~0.30" à ~0.50") — ainsi le bottom-anchor a de la marge pour empêcher le texte de toucher la ligne. **Aujourd'hui** le combiné anchor + shrink fonctionne pour les milestones courts, peut être tendu pour les plus longs.

## Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+ `_apply_layout_postprocess`, `_set_text_anchor`, `_read_sp_text`, distribution single_column retravaillée, matrix bullets cap + anchor, image_engine integration) |
| `aosis-deck-builder/scripts/image_engine.py` | **créé** (150 lignes) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (+ kwarg `auto_images`, CLI `--no-images`, `_auto_images` injection per-slide) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+5 tests, renommage 10→7) |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (matrix max 3, section "Images automatiques") |
| `aosis-deck-builder/SKILL.md` | **modifié** (section "Auto stock images") |
| `CHANGELOG.md` | **modifié** (entrée Chantier 11) |
| `chantier11_report.md` | **créé** (ce fichier) |
| `examples/test_migration_cloud.pptx` | **régénéré** (852 KB, 7 photos Picsum) |

`AOSIS_template.pptx` **non modifié**. `brand.py`, `chart_engine.py`, `icon_engine.py` **non modifiés**.

---

**Statut final** : ✅ Chantier 11 **livré sans régression**. 42/43 tests verts (1 skip soffice pré-existant), 4 fixes appliqués, 7 photos Picsum téléchargées dans le deck régénéré.
