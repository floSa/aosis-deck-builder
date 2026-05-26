# Philosophie éditoriale — AOSIS Deck Builder

> Communication d'abord, design ensuite.

Ce document code en dur les standards éditoriaux du consulting AOSIS.
Il complète `SKILL.md` (en-tête) et précède `layouts.md` / `json-schema.md`
(qui codent les règles techniques par layout). **À lire en premier avant
toute génération de deck.**

Un deck consulting n'est pas un objet visuel : c'est un argument structuré
adressé à des décideurs (COMEX, CODIR, sponsor) qui doivent trancher.
Chaque slide existe pour faire avancer cet argument. Si une slide n'avance
pas l'argument, elle n'a pas sa place.

---

## 1. Structure narrative consulting

### 1.1 — Le canevas classique : Diagnostic → Vision → Stratégie → Plan → Next Steps

C'est la colonne vertébrale par défaut d'un deck AOSIS, hérité du framework
McKinsey/BCG. Convient à 80 % des missions (proposition commerciale,
restitution d'audit, business case, comité de pilotage).

| Phase            | Question à laquelle la phase répond                       | Layouts typiques                                          |
|------------------|-----------------------------------------------------------|-----------------------------------------------------------|
| **Diagnostic**   | Où en est-on ? Quel est le problème ?                     | `hero_stat`, `kpi_with_chart`, `data_table`, `matrix_2x2_styled` |
| **Vision**       | Où veut-on aller ? Quel est l'état cible ?                | `big_idea`, `comparison_2cols`, `hero_stat`               |
| **Stratégie**    | Comment combler l'écart ? Quels leviers ?                 | `framework_3cards`, `matrix_2x2_styled`, `pyramid`        |
| **Plan**         | Qui fait quoi, quand ?                                    | `roadmap_styled`, `process_steps`, `data_table`           |
| **Next Steps**   | Quelle décision attendons-nous ? Quand ?                  | `text`, `content`, `big_idea`                             |

**Quand l'utiliser** : par défaut. Tout deck AOSIS suit ce canevas sauf
contre-indication explicite (deck très court < 6 slides, audience COMEX
très pressée, exercice purement informatif).

### 1.2 — Variante "Pyramid Principle" : Answer First

Pour les audiences COMEX/CODIR très pressées (15 min de slot, lecture du
deck en amont). La conclusion arrive en slide 3 ou 4, le reste du deck
soutient l'argumentation.

```
Slide 1  — cover
Slide 2  — agenda_diagonal
Slide 3  — big_idea : LA RECOMMANDATION (Answer First)
Slide 4  — hero_stat : LE CHIFFRE QUI JUSTIFIE
Slides 5+ — Diagnostic / Preuves / Risques (soutien de l'argument)
Avant-dernière — closing_diagonal
Dernière — final_branding
```

**Quand l'utiliser** : restitution finale au COMEX, recommandation
stratégique forte, audience qui a déjà le contexte. **À éviter** pour les
propositions commerciales (le suspense fait partie du processus de vente).

### 1.3 — Variante "Mission deliverable" pour restitutions

Structure adaptée aux fins de mission : on rend compte du travail effectué
ET on projette la suite.

```
1. cover
2. agenda_diagonal
3. section_diagonal — "Ce que nous avons fait"
4-6. Synthèse du travail (data_table, kpi_with_chart)
7. section_diagonal — "Ce que nous avons trouvé"
8-12. Findings (hero_stat, matrix_2x2_styled, quote_callout)
13. section_diagonal — "Ce que nous recommandons"
14-17. Recommandations (framework_3cards, roadmap_styled)
18. closing_diagonal
19. final_branding
```

---

## 2. Action titles obligatoires

### 2.1 — La règle

Chaque titre de slide est une **phrase complète qui énonce le take-away**.
Jamais un mot-clé descriptif. Le test : si on lit uniquement les titres,
on doit comprendre l'argument complet du deck (cf. ghost deck test).

### 2.2 — Tableau bons / mauvais exemples (contexte consulting)

| ❌ Topic label (à bannir)           | ✅ Action title (à viser)                                                  |
|--------------------------------------|----------------------------------------------------------------------------|
| "Diagnostic"                         | "Le SI atteint ses limites de capacité et de disponibilité"                |
| "Marché"                             | "Le marché cloud croît de 22 % par an, porté par l'IA"                     |
| "Recommandations"                    | "Le Replatform AWS offre le meilleur ratio coût/risque"                    |
| "Risques"                            | "Trois risques majeurs nécessitent une mitigation immédiate"               |
| "Chiffres clés"                      | "1,2 M€ pour reprendre 6 h sur chaque cycle de reporting"                  |
| "Approche méthodologique"            | "Notre approche en 4 phases pour livrer la cible à T+12 mois"              |
| "Équipe"                             | "L'équipe mobilisée : 6 consultants, 50 ans d'expérience cumulée"          |
| "Planning"                           | "Le chemin sur 12 mois, jalonné en 5 milestones"                           |
| "Comparaison des scénarios"          | "Le scénario Replatform divise le coût par 2 versus Refactor"              |
| "Coûts"                              | "850 k€ d'investissement initial, ROI atteint à T+18 mois"                 |
| "Synthèse"                           | "Trois constats convergent vers une bascule cloud à 18 mois"               |
| "Next Steps"                         | "Décision attendue au CODIR du 15 juillet pour démarrage en septembre"     |

### 2.3 — Le ghost deck test

Une fois ton plan validé, **avant** de générer le JSON, fais l'exercice
suivant :

1. Liste tous les titres dans l'ordre, sans le reste.
2. Lis-les comme un seul paragraphe continu.
3. Vérifie :
   - Chaque titre est une phrase d'action complète ;
   - La séquence raconte une histoire logique et complète ;
   - Aucun titre ne pourrait être déplacé sans perte de sens (sinon il
     manque de spécificité, il faut le réécrire) ;
   - Si tu retirais une slide, l'argument serait clairement amputé.
4. Si un titre échoue : reformule-le. Si une slide n'a aucun take-away
   spécifique : supprime-la ou fusionne-la.

C'est le test le plus discriminant entre un deck pro et un deck moyen.

### 2.4 — Longueur recommandée

- **60-80 caractères**, **1-2 lignes maximum**.
- Si tu dépasses 100 caractères : le titre est trop dense, scinde-le
  (split en deux slides) ou condense.
- Si tu fais 1 seul mot : c'est un mot-clé, pas un titre — reformule.

---

## 3. Discipline des exhibits

### 3.1 — Une slide = un message

Chaque slide porte **un seul take-away**. Si tu as deux idées, fais deux
slides. La densité visuelle peut être élevée (un chart riche, un tableau
détaillé), mais l'idée à retenir est unique.

### 3.2 — Chaque exhibit doit gagner sa place

Un chart, une matrice, un tableau, un KPI : chaque exhibit doit servir
explicitement le take-away du titre. Si l'exhibit est joli mais n'illustre
pas le titre : retire-le ou change le titre.

### 3.3 — Annoter le finding clé directement sur l'exhibit

Ne laisse pas l'audience deviner où regarder. Sur un chart : un callout
orange sur la barre clé, un label "+22 %" en gras, une zone de focus
ombrée. Sur un tableau : `highlight_column` ou `highlight_row` pour
pointer la colonne/ligne décisive.

### 3.4 — Test de la slide auto-suffisante

Imagine que la slide soit imprimée et lue **sans** la voix du présentateur.
Le take-away passe-t-il quand même ? Si non : retravaille le titre,
l'annotation de l'exhibit, ou la sous-légende.

C'est crucial dans le monde post-COVID où les decks circulent en PDF par
mail davantage qu'ils ne sont projetés en réunion.

### 3.5 — Graphes > tableaux pour les résultats

Pour montrer un **résultat** (tendance, comparaison, écart), préférer un
chart (`kpi_with_chart`, layout `bar`/`column`/`line`/`donut`). Pour
montrer des **données détaillées** que l'audience doit pouvoir consulter
ligne par ligne (scénarios × critères, risques × probabilité × impact),
utiliser `data_table`.

---

## 4. Sources et attribution

### 4.1 — Chaque chiffre, citation, framework = une source

En consulting, la rigueur factuelle est non négociable. Chaque slide doit
porter un champ `source: "..."` dans le JSON. Ce champ s'affiche en pied
de slide (footer ou note discrète).

### 4.2 — Sources acceptées

- **Internes AOSIS** : "Analyse AOSIS", "Audit interne", "Modélisation AOSIS",
  "Benchmark sectoriel AOSIS 2026".
- **Données client** : "Données client 2025", "Système RH client", "Audit
  initial mars 2026".
- **Sources externes** : citer le nom + l'année ("Gartner 2025", "IDC
  Worldwide Cloud 2026", "Étude IFOP 2024").
- **Frameworks** : citer le créateur ("Porter, 1985", "McKinsey 7S",
  "Kaplan-Norton Balanced Scorecard").

### 4.3 — Citations stakeholders

- Avec autorisation : "Jean Dupont, DSI, ACME Corp"
- Sans autorisation : "DSI d'une ETI de l'industrie, 800 M€ CA"
- Anonyme générique : "un stakeholder du COMEX"

Jamais de citation inventée sans le signaler dans le chat à l'utilisateur.

---

## 5. Structure obligatoire du deck

Tout deck AOSIS respecte cette structure d'enveloppe :

```
Slide 1       — cover                  (page de garde, titre + sous-titre + ref)
Slide 2       — agenda_diagonal        (sommaire visuel)
Slide 3       — section_diagonal       (1re partie : DIAGNOSTIC)
Slides 4..N   — Slides de contenu      (action titles + layouts variés)
Slide N+1     — section_diagonal       (partie suivante : VISION)
...
Avant-dernière — closing_diagonal      (MERCI / Q&R, visuel diagonal AOSIS)
Dernière      — final_branding         (signature corporate AOSIS)
```

### Règles d'enveloppe

- **JAMAIS** terminer sur une slide de contenu.
- **JAMAIS** terminer sur un "Thank You" blanc générique.
- **TOUJOURS** terminer par `closing_diagonal` + `final_branding`.
- **TOUJOURS** ouvrir par `cover` puis `agenda_diagonal`.
- Chaque grande section doit être annoncée par un `section_diagonal`.

### Layouts template-based prioritaires

Quand un layout existe en version template-based ET code-based, prendre
toujours le template-based. Voir `layouts.md` pour le mapping complet.

---

## 6. Discipline du texte

### 6.1 — Quantités maximales par slide

- **Body text** : ~40 mots maximum.
- **Bullets** : 4 maximum, 8 mots par bullet.
- **Pas de phrases complètes** dans le body : style télégraphique.

### 6.2 — Charte typographique AOSIS

- **Police** : Arial uniquement (héritée du template).
- **Body** : 18-20 pt minimum (16 pt dans des cas exceptionnels denses).
- **Titres** : 24-28 pt typiquement (selon layout).
- **KPI values** : XXL 48-60 pt (auto-shrink à 24-30 pt si chars larges).

Tout cela est géré par le template + le code, mais il faut résister à la
tentation de "remplir" une slide avec du texte qui force des polices plus
petites. Si ça ne rentre pas : c'est qu'il y a trop d'idées sur la slide.

### 6.3 — Pas de jargon non explicité

- "ROI", "TCO", "KPI" : OK (connus du COMEX).
- "Replatform vs Refactor vs Rehost" : à expliquer en 1 ligne la 1re fois.
- Acronymes maison client : à éviter ou à expliciter.

---

## 7. Erreurs courantes (anti-patterns)

Tableau des erreurs fréquemment observées sur de vrais decks et leur
correction :

| Erreur                                                       | Fix                                                                       |
|--------------------------------------------------------------|---------------------------------------------------------------------------|
| Titre = mot-clé ("Diagnostic", "Marché")                     | Phrase d'action complète énonçant le take-away                            |
| Convertir un tableau source en KPI cards                     | Garder le tableau via layout `data_table`                                 |
| Pas de slide libre dans un deck 10+ slides                   | Insérer 1-2 `canvas_blank` pour la composition libre                      |
| Slide de clôture floue ou absente                            | Toujours `closing_diagonal` + `final_branding`                            |
| Verbiage en body text                                        | Télégraphique, max 40 mots/slide                                          |
| Layouts code-based exotiques (funnel, pyramid, swot)         | Préférer template-based ou `canvas_blank`                                 |
| Pas de source citée                                          | Toujours un `source: "..."` dans le JSON, même fictif                     |
| Image keyword en français                                    | Toujours en anglais et concret (ex: "data center server room")            |
| Exhibit sans annotation du finding                           | Callout orange, highlight, label sur la valeur clé                        |
| Deck qui se termine par "Thank You" générique                | Toujours `closing_diagonal` AOSIS + `final_branding`                      |
| Deux idées sur une même slide                                | Splitter en deux slides (une = un message)                                |
| Citation inventée non signalée                               | Signaler à l'utilisateur dans le chat ou retirer la citation              |
| 4 cartes (ou plus) dans `framework_3cards`                   | Cap dur à 3 cartes — splitter en deux slides (3+1 ou 2+2), ou composer un `canvas_blank` avec N `kpi_card` blocks libres. Le moteur lève une `ValueError` au-delà de 3. |
| Chart `line` avec `values` (single-series) au lieu de `series` | Le moteur coalesce automatiquement depuis le Chantier 26, mais la forme canonique reste `series=[{name, values}]`. Pour multi-séries, c'est obligatoire. |

---

## 8. Tests de qualité avant validation

Checklist mentale à appliquer **avant** de générer le JSON final :

- [ ] Tous les titres sont des phrases d'action complètes (pas de mots-clés).
- [ ] **Ghost deck test** : la séquence des titres raconte une histoire
      cohérente et complète.
- [ ] Au moins 1 `canvas_blank` libre dans le deck si 10+ slides.
- [ ] Au moins 1 `data_table` si le contenu source contenait un tableau.
- [ ] Chaque slide a une `source` dans le JSON.
- [ ] Tous les `image_keyword` sont en anglais concrets (2-4 mots).
- [ ] Clôture par `closing_diagonal` + `final_branding`.
- [ ] Aucun layout code-based déprécié (`swot`, `cards`, `process`, `chart`,
      `agenda`, `timeline`, `quote`, `comparison`, `matrix_2x2`, `roadmap`).
- [ ] Limites techniques respectées (3 bullets/quadrant `matrix_2x2_styled`,
      5 milestones `roadmap_styled`, 6 colonnes × 8 lignes `data_table`, etc.).
- [ ] Chaque exhibit (chart, table, KPI) sert explicitement le take-away
      du titre de la slide.
- [ ] Aucune slide ne pourrait être supprimée sans amputer l'argument.

Si une ligne n'est pas cochée : **retravaille avant de générer**, pas
après. Le post-fix sur le `.pptx` est interdit (cf. `qa.md`).

---

## 9. Pour aller plus loin

- **Règles techniques par layout** : [`layouts.md`](layouts.md)
- **Schémas JSON par layout** : [`json-schema.md`](json-schema.md)
- **Workflow QA visuel + contenu** : [`qa.md`](qa.md)
- **Charte AOSIS** : extraite automatiquement de `AOSIS_template.pptx`
  (theme XML — pas de hex hardcodé dans le code).

Pour le prompt-template renforcé à coller dans Claude, voir
`docs/GUIDE_OPERATIONNEL.md` section 7.
