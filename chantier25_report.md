# Chantier 25 (expérimental) — Communication-first philosophy

**Branche** : `experiment/communication-first-philosophy`
**Date** : 2026-05-26
**Statut** : Expérimental — à valider en usage réel avant merge sur `main`
**Périmètre** : 100 % documentaire. Aucun code Python, aucun template, aucun
test modifié.

---

## 1. Contexte & inspiration

Le repo public [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill)
(323 ★ GitHub) défend une thèse forte : un skill PowerPoint doit
**remplacer l'approche design-forward par défaut de Claude par des
standards communication-first**. Sa structure mise sur une couche
philosophique explicite (action titles obligatoires, ghost deck test,
discipline éditoriale) plutôt que sur le code technique.

Notre skill `aosis-deck-builder` est techniquement abouti (24 chantiers,
90 tests verts, 17 layouts template-based + canvas_blank, cache disque
images, KPI XXL anti-overflow). Mais sa philosophie éditoriale était
**implicite et noyée dans le code** : "The Three Golden Rules" dans
`SKILL.md` posaient le terrain, mais la thèse communication-first n'était
pas exprimée comme telle.

Ce chantier expérimental renforce la **couche philosophique** sans
toucher au code. L'objectif : qu'un Claude exécutant le skill comprenne
non seulement *comment* construire un deck, mais *pourquoi* chaque règle
existe — et puisse arbitrer sur les cas non-couverts par les fiches
layouts.

---

## 2. Modifications apportées

### 2.1 — `aosis-deck-builder/SKILL.md`
- Ajout d'une section **`## Philosophie`** (24 lignes) juste après le
  frontmatter YAML, avant tout autre contenu.
- Thèse fondatrice en 7 points (action titles, structure narrative,
  ghost deck test, une slide = un message, sources, clôture obligatoire,
  charte AOSIS).
- Renvois explicites vers `references/philosophy.md`, `references/layouts.md`,
  `references/json-schema.md`.
- Ajout d'une ligne `references/philosophy.md` (en tête, marquée "À lire en
  premier") dans la section "References".
- **Aucun contenu existant supprimé** : The Three Golden Rules, Build
  Workflow, Quick example, data_table, Auto stock images, etc. restent
  intacts.

### 2.2 — `aosis-deck-builder/references/philosophy.md` (nouveau)
~290 lignes en 9 sections :
1. Structure narrative consulting (canevas classique, variante Pyramid
   Principle "Answer First", variante restitution).
2. Action titles obligatoires (règle, tableau de 12 bons/mauvais
   exemples consulting, ghost deck test détaillé, longueur recommandée).
3. Discipline des exhibits (une slide = un message, exhibit gagne sa
   place, annoter le finding, test de slide auto-suffisante, graphes vs
   tableaux).
4. Sources et attribution (sources internes, données client, externes,
   frameworks, citations stakeholders).
5. Structure obligatoire du deck (enveloppe cover → agenda → sections
   → contenu → closing → final_branding).
6. Discipline du texte (40 mots/slide max, Arial, 18-20 pt, pas de
   jargon non explicité).
7. Erreurs courantes (tableau d'anti-patterns + fix).
8. Tests de qualité avant validation (checklist QA mentale).
9. Pour aller plus loin (renvois vers `layouts.md`, `json-schema.md`,
   `qa.md`, GUIDE_OPERATIONNEL.md).

### 2.3 — `docs/GUIDE_OPERATIONNEL.md`
- Ajout d'une étape **"Ghost deck test (obligatoire avant génération)"**
  dans le prompt-template renforcé (section 7), positionnée juste après
  la section "WORKFLOW OBLIGATOIRE" / validation du plan.
- Ajout de `references/philosophy.md` dans la liste de lecture
  obligatoire du prompt-template (position 2, juste après `SKILL.md`).

### 2.4 — `README.md` (racine)
- Ajout d'une section **"Philosophy — Communication first, design
  second"** entre l'introduction et "Documentation".
- 5 lignes de thèse + 4 bullets résumant les principes clés + pointeur
  vers `aosis-deck-builder/references/philosophy.md`.

### 2.5 — `CHANGELOG.md`
- Ajout d'une entrée "Chantier 25 (expérimental) — Communication-first
  philosophy" en tête de `[Unreleased]`, marquée explicitement
  "expérimental — à valider avant merge sur main".

---

## 3. Tests de non-régression

```bash
python -m pytest aosis-deck-builder/tests/ -v
```

**Résultat** : `90 passed, 1 skipped in 4.28s` ✅

Le test skippé est `visual_review` (nécessite `soffice` + `pdftoppm`
système), comme attendu et documenté depuis le Chantier 7. **Aucune
régression** introduite par les modifications documentaires.

---

## 4. Suggestions de tests utilisateur pour valider l'expérimentation

L'objectif de l'expérimentation est de mesurer si la couche
philosophique change effectivement le comportement de Claude lors de la
génération d'un deck. Suggestions :

### 4.1 — Test A/B sur la même mission
1. Sur la branche `main` : générer un deck pour une mission type
   (restitution audit cloud, proposition commerciale, CODIR).
2. Sur la branche `experiment/communication-first-philosophy` : générer
   le **même deck** avec la même spec source.
3. Comparer :
   - La qualité des titres (action titles vs descriptifs).
   - La cohérence narrative quand on ne lit que les titres (ghost deck
     test).
   - Le respect de la structure Diagnostic → Vision → Stratégie → Plan
     → Next Steps.
   - La présence du test ghost deck dans le chat avant génération.

### 4.2 — Test du ghost deck explicite
Demander à Claude (avec le skill chargé sur la nouvelle branche) :
> "Génère-moi le plan d'un deck de restitution d'audit SI. Applique le
> ghost deck test et présente-moi le résultat avant de générer le JSON."

Vérifier que Claude :
- Liste les titres en séquence dans le chat.
- Reformule les titres faibles avant la génération.
- Demande validation utilisateur sur la séquence des titres.

### 4.3 — Test de robustesse anti-patterns
Donner à Claude une source contenant un tableau (CSV de risques, matrice
de scénarios) et vérifier qu'il :
- Garde le tableau via `data_table` (au lieu de le convertir en KPI
  cards).
- Cite la source dans le JSON.
- Termine le deck par `closing_diagonal` + `final_branding`.

### 4.4 — Test de la slide auto-suffisante
Générer un deck, exporter en PDF, et **lire chaque slide sans contexte**.
Vérifier que chaque slide porte un take-away identifiable sans avoir
besoin de la narration du présentateur.

### 4.5 — Mesure quantitative (optionnelle)
Sur un échantillon de 5 decks générés avant/après :
- Compter les titres qui passent le ghost deck test (% / total).
- Compter les slides ayant un champ `source` rempli (% / total).
- Compter les decks ouvrant par `cover` + `agenda_diagonal` et fermant
  par `closing_diagonal` + `final_branding` (% / total).

---

## 5. Décision de merge

À l'issue des tests utilisateur, trois scénarios :

- **A. La couche philosophique change effectivement le comportement de
  Claude en mieux** → merge sur `main` (devient le Chantier 25 officiel).
- **B. Changement marginal mais documentation utile** → merge en tant
  que documentation enrichie, sans prétention de changement
  comportemental.
- **C. Aucun changement observable** → garder la branche en référence
  documentaire, mais ne pas merger pour éviter d'alourdir `SKILL.md`.

À ce stade : pas de merge sur `main`. La branche reste isolée pour
expérimentation.

---

## 6. Périmètre strict respecté

Vérifications :
- ✅ Aucune modification dans `aosis-deck-builder/scripts/`
- ✅ Aucune modification de `aosis-deck-builder/assets/AOSIS_template.pptx`
- ✅ Aucune modification dans `aosis-deck-builder/tests/`
- ✅ Aucune modification de `aosis-deck-builder/references/json-schema.md`
- ✅ Aucune modification de `aosis-deck-builder/references/layouts.md`
- ✅ Aucune modification de `aosis-deck-builder/references/qa.md`
- ✅ Aucune modification de `aosis-deck-builder/references/icons_suggested.md`

Modifications cantonnées à :
- `aosis-deck-builder/SKILL.md` (section Philosophie ajoutée en tête)
- `aosis-deck-builder/references/philosophy.md` (nouveau)
- `docs/GUIDE_OPERATIONNEL.md` (étape ghost deck test ajoutée)
- `README.md` (section Philosophy ajoutée)
- `CHANGELOG.md` (entrée Chantier 25)
- `chantier25_report.md` (ce fichier)
