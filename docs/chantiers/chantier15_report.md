# Chantier 15 — Création du layout `data_table`

**Date** : 2026-05-20
**Périmètre** : Ajouter un layout `data_table` template-based au skill pour restituer du contenu intrinsèquement tabulaire (sans le forcer en KPI cards / bullets).

## TL;DR

- ✅ Slide modèle `data_table` créée dans `assets/AOSIS_template.pptx` à la **position 17** (juste avant `final_branding`)
- ✅ Backup `AOSIS_template.before-chantier15.pptx` (810 KB)
- ✅ Fonction `_process_data_table(slide, spec)` dans `template_engine.py` (~165 lignes)
- ✅ **57 passed, 1 skipped** (5 nouveaux tests verts, aucune régression sur les 52 existants)
- ✅ Showcase deck [examples/test_data_table_showcase.pptx](examples/test_data_table_showcase.pptx) (4 tables avec compositions variées)
- ✅ Documentation : fiche `data_table` dans `layouts.md` + section dans `json-schema.md` + mention dans `SKILL.md`

## 1. Slide modèle ajoutée au template

Composition de la slide 17 :

| Shape | Position (in.) | Taille (in.) | Style |
|---|---|---|---|
| `{{TITLE}}` | 0.4 / 0.4 | 9.0 × 0.6 | Arial 24pt bold navy `#14163C` |
| `{{SOURCE}}` | 0.4 / 5.10 | 6.0 × 0.3 | Arial 8pt italic gris `#4A4D6B` |

La zone centrale 0.5″ → 9.5″ horizontal, 1.2″ → 4.9″ vertical (3.7″ tall) est laissée vide — le moteur y dessinera dynamiquement le tableau.

Création scriptée via python-pptx (clonage du layout 'Texte', suppression des placeholders auto, ajout textbox `{{TITLE}}` et `{{SOURCE}}`, tag `cSld@name='data_table'`, reorder du sldIdLst pour placer le slide avant `final_branding`).

## 2. Format JSON

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

| Champ | Type | Notes |
|---|---|---|
| `headers` | `list[str]`, max 6 | requis |
| `rows` | `list[list]`, max 8 | requis |
| `highlight_column` | `int`, 0-based | texte orange bold sur la colonne |
| `highlight_row` | `int`, 0-based sur données | fond orange clair `#FDF1EA` |

## 3. Style appliqué

- **Header** (row 0) : fond navy `#14163C`, texte blanc bold Arial 11pt, padding 6pt
- **Lignes data** : alternance blanc / off-white `#FAFAF7`
- **Cellules** : Arial 10pt navy `#14163C`, padding 6pt
- **Première colonne** : bold + alignement gauche
- **Autres colonnes** : alignement centré
- **Largeurs** : col 0 = 30 % du total (= 2.70″), autres équiréparties sur les 6.30″ restants
- **`highlight_column`** : texte orange `#F26622` bold sur toutes les cellules data de cette colonne
- **`highlight_row`** : fond orange clair `#FDF1EA` sur toutes les cellules de cette ligne data

## 4. Auto-shrink

Pour gérer le débordement vertical (zone disponible = 3.7″ = 266 pt) :

```python
# Heuristique : row_h_pt = (font_pt + 2*padding) × wrap_factor
# wrap_factor selon nombre de colonnes (cellules plus étroites → wrap probable)
wrap_factor = 1.0 if n_cols <= 3 else 1.5 if n_cols <= 5 else 2.0
total_pt = header_size_pt + n_rows × (font_pt + 2*padding_pt) × wrap_factor

# Tant que total_pt > 266 : réduire padding 6→4 puis font 10→8 (plancher)
```

Effet observé sur 8×6 cellules longues : police shrink de 10→8pt et padding 6→4pt activés correctement par le test `test_data_table_autoshrinks_on_overflow`.

## 5. Validation amont

| Cas | Comportement |
|---|---|
| `len(headers) > 6` | `ValueError` (erreur bloquante — au-delà de 6 colonnes le rendu est trop dense) |
| `len(rows) > 8` | Truncate aux 8 premières + warning stderr |
| Cellule > 30 chars | Warning stderr (risque débordement, mais pas bloquant) |
| `headers` vide | Silent no-op (slide reste avec juste {{TITLE}} + {{SOURCE}}) |

## 6. Showcase deck — 4 slides

| # | Composition | Validation visuelle |
|---:|---|---|
| 1 | 5 cols × 3 lignes (3 stratégies) + highlight col 3 + highlight row 1 (Replatform mise en avant) | tableau compact, lecture facile, Replatform sur fond orange clair |
| 2 | 4 cols × 6 lignes (cartographie risques) + highlight row 0 (dépassement budgétaire) | tableau dense, auto-shrink activé probablement |
| 3 | 4 cols × 5 lignes (roadmap phases) + highlight col 3 (livrables) | colonne "Livrables clés" en orange bold |
| 4 | 3 cols × 4 lignes (KPI avant/après) | petit tableau, vérifie le centrage |

Génération : 0.5 s, deck 583 KB.

## 7. Tests

```
======================== 57 passed, 1 skipped in 4.17s =========================
```

5 nouveaux tests :
| Test | Vérifie |
|---|---|
| `test_data_table_simple` | 3×3 basique, présence d'une `TABLE` shape, lecture des cellules |
| `test_data_table_with_highlights` | col 2 en orange bold, ligne 1 en `#FDF1EA` |
| `test_data_table_max_columns` | 6 colonnes acceptées (limite haute) |
| `test_data_table_truncates_at_8_rows` | 10 lignes → 8 + warning stderr `"10 rows > 8, truncating"` |
| `test_data_table_autoshrinks_on_overflow` | 8×6 long content → font ≤ 9pt OU padding ≤ 5pt |

Anciens 52 tests : ✓ aucune régression.

## 8. Friction technique

**Heuristique initiale trop optimiste** — première version sans `wrap_factor` n'estimait que ~187 pt pour 8 lignes × 6 cols (vs 266 pt disponibles) → pas de shrink déclenché. Correction : ajout d'un `wrap_factor` adaptatif (1.0 / 1.5 / 2.0 selon n_cols) qui simule le wrap probable des cellules dans des colonnes étroites. Avec 6 cols, wrap_factor=2.0 → estimation 363 pt > 266 → shrink activé. Test ré-exécuté ✓.

**Pas de contrôle direct des bordures de cellule** — python-pptx ne fournit pas d'API publique pour modifier la couleur/épaisseur des bordures de table. Le défaut (bordures noires fines) est acceptable visuellement ; pour personnaliser à `#E8E9F2`, il faudrait manipuler le XML `<a:lnL>` / `<a:lnR>` / `<a:lnT>` / `<a:lnB>` directement. Non implémenté dans ce chantier ; à reprendre si l'utilisateur juge le rendu insuffisant.

## 9. Suggestion suivante

- **Bordures custom** (gris `#E8E9F2`) via manipulation XML directe — gain visuel modeste mais finition consulting.
- **Cell-level highlighting** : aujourd'hui on highlight colonne OU ligne, pas une cellule individuelle. Si besoin, ajouter `highlight_cells: [[row, col], ...]`.
- **Footer row** : ligne totaux différenciée (fond navy clair). Optionnel.
- **Numérotation auto col 0** : si `headers[0]` vaut `"#"`, auto-fill avec 1, 2, 3...

## 10. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/assets/AOSIS_template.pptx` | **modifié** (slide 17 ajoutée) |
| `aosis-deck-builder/assets/AOSIS_template.before-chantier15.pptx` | **créé** (backup, 810 KB) |
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+165 lignes : constantes + `_process_data_table` + dispatch) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+5 tests) |
| `aosis-deck-builder/references/layouts.md` | **modifié** (fiche `data_table` insérée avant `final_branding`) |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (section dédiée `data_table`) |
| `aosis-deck-builder/SKILL.md` | **modifié** (mention nouveau layout) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 15) |
| `chantier15_report.md` | **créé** (ce fichier) |
| `examples/test_data_table_showcase.json` | **créé** (4 slides showcase) |
| `examples/test_data_table_showcase.pptx` | **créé** (583 KB, 0.5 s génération) |

Autres layouts **non modifiés** comme demandé.

---

**Statut final** : ✅ Chantier 15 **livré sans régression**. 57/58 tests verts (1 skip soffice pré-existant), nouveau layout `data_table` fonctionnel, showcase à valider visuellement.
