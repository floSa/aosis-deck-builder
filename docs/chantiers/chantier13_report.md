# Chantier 13 — Fiches détaillées des layouts dans `references/layouts.md`

**Date** : 2026-05-20
**Périmètre** : Réécrire `references/layouts.md` comme un guide de décision structuré pour Claude Code et tout opérateur du skill.

## Confirmation

- **32 fiches rédigées** (17 template-based + 15 code-based incluant `gantt` signalé non-implémenté) au format demandé : Domaine / Description / Composition / Quand l'utiliser / Quand ne pas l'utiliser / Limites techniques / Exemple JSON minimal.
- **Inspection préalable** réalisée pour les 17 template-based directement dans `AOSIS_template.pptx` (placeholders et groupes listés).
- **Lecture code** réalisée pour les 14 code-based dans `build_deck.py` (signatures `add_*` + DISPATCH).
- **Section d'intro** "Comment choisir un layout" ajoutée avec table par domaine.
- **Aucun code modifié**, mission purement documentaire.

## Layouts marqués "à éviter" / alternative recommandée

| Layout code-based | Alternative template-based recommandée | Raison |
|---|---|---|
| `swot` | **`matrix_2x2_styled`** | Rendu plus consulting, axes personnalisables, max 3 bullets par quadrant enforcé |
| `cards` | **`framework_3cards`** | Cartes stylisées avec icônes Iconify, alternance de couleurs, format plus impactant |
| `process` | **`process_steps`** | Markers circulaires colorés avec alternance, axe horizontal, rendu visuel plus riche |
| `chart` | **`kpi_with_chart`** | Combo KPI + chart sur la même slide, 8 types de chart vs 5, rendu consulting |
| `agenda` (code-based, dispatch direct) | **`agenda_diagonal`** | Diagonale + photo auto + pagination 7-items |
| `timeline` (code-based) | **`roadmap_styled`** | Markers diamants alternés above/below, photo |
| `quote` (code-based) | **`quote_callout`** | Bandeau takeaway, attribution mise en forme |
| `comparison` (code-based) | **`comparison_2cols`** / **`comparison_before_after`** | Cartes stylisées avec REPEAT_ITEM |
| `matrix_2x2` (code-based) | **`matrix_2x2_styled`** | Quadrants colorés, axes annotés, max 3 bullets |
| `roadmap` (code-based) | **`roadmap_styled`** | Markers diamants, photos, alternance |

## Layouts qui restent légitimes en code-based

| Layout | Pourquoi le garder |
|---|---|
| `hero_stat` | Format unique (nombre géant 150pt) que le template n'expose pas |
| `big_idea` | Format manifesto unique, 1-2 par deck max |
| `dashboard` | Cas dense > 3 KPI + chart, complément de `kpi_with_chart` |
| `pyramid` | Cas spécifique (hiérarchie stratifiée), pas couvert par template |
| `funnel` | Cas spécifique (entonnoir de conversion), pas couvert par template |
| `org_chart` | Cas spécifique (leader + N reports), pas couvert par template |
| `stat_grid` | Grille N>3 KPI sans chart, complémentaire à `hero_stat` / `kpi_with_chart` |
| `image_hero` | Image pleine page locale (`{{IMAGE}}` placeholder ne couvre que les diagonal layouts) |
| `content` | Combo bullets + image locale, pas couvert par template |
| `text` | Fallback minimal pour cas "vraiment text-only" (mentions légales, etc.) |

## Frictions / signaux pour l'avenir

1. **`gantt` listé dans la mission mais non implémenté** : il n'existe pas dans le DISPATCH actuel. Fiche dédiée le documente comme "Non implémenté — pour un planning utiliser `roadmap_styled` ou un graphique externe". Si besoin futur, candidat Chantier 14 pour ajout.

2. **Layouts code-based dont la dépréciation pourrait être étudiée** :
   - `swot`, `matrix_2x2`, `comparison`, `timeline`, `quote`, `cards`, `chart`, `process`, `roadmap`, `agenda` : tous redondants avec un équivalent template-based plus riche. **À retirer du DISPATCH dans un chantier 14+** après vérification qu'aucun fixture pytest / exemple ne les utilise plus.
   - Garderaient leur place : `hero_stat`, `big_idea`, `pyramid`, `funnel`, `dashboard`, `org_chart`, `stat_grid`, `image_hero`, `content`, `text`.

3. **Note sur les dispatchs en `DISPATCH` qui chevauchent** : `cover`, `section`, `closing`, `agenda`, `matrix_2x2`, `roadmap`, `comparison`, `timeline`, `quote` existent dans DISPATCH ET dans TEMPLATE_BASED_LAYOUTS. Le routing `if layout in TEMPLATE_BASED_LAYOUTS: render_template_slide else DISPATCH` envoie vers template par défaut. Le code-based reste accessible si l'utilisateur passe un layout qui n'a PAS d'équivalent template, mais pour `cover` / `closing` etc. c'est dead code. À nettoyer dans le chantier de dépréciation.

4. **Section "Comment choisir un layout"** : structure linéaire (1 → 4 étapes) + table par domaine. Devrait suffire à Claude Code pour matcher rapidement un message à un layout sans recours à du jugement subjectif.

## Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/references/layouts.md` | **réécrit intégralement** (32 fiches structurées + intro guide de décision) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 13) |
| `chantier13_report.md` | **créé** (ce fichier) |

Aucun code Python touché. Aucun test ajouté/modifié (purement documentation).

---

**Statut final** : ✅ Chantier 13 **livré sans régression**. 32 fiches structurées, 10 recommandations de migration code → template explicitées, 1 layout (`gantt`) signalé non-implémenté.
