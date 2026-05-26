# Guide opérationnel — aosis-deck-builder

**Skill custom AOSIS pour générer des decks PowerPoint consulting**
**Date** : Mai 2026
**Auteur du skill** : Florian Horellou (AOSIS / FPT Company)
**État** : Production-ready après 20 chantiers de polish

---

## 1. Vue d'ensemble

Le skill `aosis-deck-builder` est un outil propriétaire AOSIS qui transforme un brief, un audit ou un rapport en une présentation PowerPoint conforme à la charte AOSIS. Il combine des layouts pré-conçus dans un template PowerPoint avec un moteur Python qui dispose intelligemment le contenu, applique la palette, gère les images Pexels et les charts matplotlib.

**Capacités principales** :
- 17 layouts template-based + 14 code-based (10 marqués "à éviter")
- Charts matplotlib intégrés (8 types : bar, barh, line, donut, pie, etc.)
- Images Pexels automatiques avec keywords contrôlés
- Tableaux structurés via `data_table`
- Slides libres via `canvas_blank` freeform (6 types de blocs)
- Découpe diagonale automatique sur les slides cover/agenda/section/closing
- Effets premium : drop shadows, chiffres XXL, charts encadrés
- Anti-débordement et anti-chevauchement par calcul
- 76 tests automatisés (1 skip standard)

---

## 2. Localisation du projet

```
~/Projets/Skill_pptx_Aosis/
├── aosis-deck-builder/           # Le skill principal
│   ├── SKILL.md                  # Doc principale
│   ├── references/
│   │   ├── layouts.md            # 32 fiches détaillées des layouts
│   │   ├── json-schema.md        # Schéma JSON par layout
│   │   └── qa.md                 # Tests de validation
│   ├── scripts/
│   │   ├── build_deck.py         # Point d'entrée principal
│   │   ├── template_engine.py    # Moteur de composition
│   │   ├── chart_engine.py       # Charts matplotlib
│   │   ├── image_engine.py       # Pexels + Picsum fallback
│   │   ├── icon_engine.py        # Iconify API
│   │   ├── brand.py              # Palette dynamique
│   │   └── visual_review.py      # QA automatisé
│   ├── tests/
│   │   └── test_smoke.py         # 76 tests automatisés
│   ├── assets/
│   │   └── AOSIS_template.pptx   # Template canonique (18 slides)
│   └── pyproject.toml
├── examples/                     # Decks d'exemple et tests
│   ├── cloud_computing_rapport.pdf       # Document source test
│   ├── cloud_computing_2026.pptx         # Test final V2
│   ├── cloud_computing_2026_v3.pptx      # Test stress canvas_blank
│   ├── test_canvas_blank_showcase.pptx   # Showcase freeform
│   ├── test_data_table_showcase.pptx     # Showcase tableaux
│   └── test_migration_cloud.pptx         # Premier test
└── .env                          # PEXELS_API_KEY (gitignored)
```

---

## 3. Configuration initiale

### 3.1 — Variables d'environnement

Le skill utilise une clé API Pexels pour les images automatiques. Configurée dans `.env` à la racine du projet :

```
PEXELS_API_KEY=ta_cle_pexels_ici
```

Le module `build_deck.py` charge automatiquement ce fichier au démarrage (`_load_dotenv()`).

Pour vérifier que ta clé est active :
```bash
cd ~/Projets/Skill_pptx_Aosis
cat .env
```

### 3.2 — Dépendances Python

Installées dans l'environnement Claude Code, pas dans ton shell utilisateur global.

Pour vérifier :
```bash
python3 -c "from pptx import Presentation; print('OK')"
```

Si ça ne marche pas, c'est normal côté shell utilisateur — utilise Claude Code pour exécuter le skill.

---

## 4. Workflow quotidien — Générer un deck

### Étape 1 — Ferme PowerPoint

Toujours fermer le fichier de destination avant régénération (sinon erreur de write).

### Étape 2 — Ouvre Claude Code dans le projet

```bash
cd ~/Projets/Skill_pptx_Aosis
code .   # ou ouvre VS Code et lance Claude Code
```

### Étape 3 — Lance le prompt-template renforcé

Copie-colle le prompt-template dans Claude Code, complète avec ton contenu source à la fin (PDF, brief, audit, etc.).

Le prompt-template est en section 7 de ce guide.

### Étape 4 — Valide le plan proposé par Claude Code

Claude Code te propose un plan en bullet list (position → layout → justification → take-away).

**Lis-le attentivement et redresse si besoin** avant de valider. C'est l'étape où tu peux infléchir les choix éditoriaux.

### Étape 5 — Génération

Une fois validé, Claude Code génère le JSON spec et lance :

```bash
python aosis-deck-builder/scripts/build_deck.py \
  --spec specs/mon_deck.json \
  --out examples/mon_deck.pptx
```

Tu vois les logs de génération (appels Pexels, charts matplotlib, etc.).

### Étape 6 — Ouvre et valide visuellement

Ouvre le `.pptx` dans PowerPoint et vérifie :
- Cohérence narrative globale
- Pas de débordement, pas de chevauchement
- Images pertinentes
- Tableaux lisibles
- Clôture propre (closing + final_branding)

Si tout est OK : tu présentes ou tu retouches manuellement.

---

## 5. Catalogue des layouts disponibles

### 5.1 — Layouts template-based (à privilégier)

| Layout | Domaine | Quand l'utiliser |
|---|---|---|
| `cover` | Navigation | Page de garde du deck |
| `agenda_diagonal` | Navigation | Sommaire (7 items max par page, paginé auto) |
| `section_diagonal` | Navigation | Intercalaire de section |
| `closing_diagonal` | Navigation | Slide MERCI / Q&R |
| `final_branding` | Navigation | Slide finale corporate AOSIS |
| `canvas_blank` | Liberté | Slide libre avec composition de blocs |
| `executive_summary` | Synthèse | Récap haut niveau avec 4 points clés |
| `kpi_with_chart` | Données chiffrées | 3 KPI + 1 chart matplotlib |
| `comparison_2cols` | Comparaison | 2 options côte à côte |
| `comparison_before_after` | Comparaison | Avant / Après |
| `framework_3cards` | Synthèse | 3-4 cartes thématiques |
| `roadmap_styled` | Planning | Timeline horizontale avec 3-5 jalons |
| `next_steps` | Planning | Plan d'actions avec ACTION / OWNER / DATE |
| `process_steps` | Process | 4-5 étapes de process |
| `text_dense_3cols` | Synthèse | 3 colonnes de texte structuré |
| `quote_callout` | Citation | Citation stakeholder mise en valeur |
| `matrix_2x2_styled` | Comparaison | Matrice 2×2 (3 bullets max par quadrant) |
| `data_table` | Données | Tableau structuré (6 col × 8 lignes max) |

### 5.2 — Layouts code-based (à éviter)

Ces 10 layouts existent mais sont marqués comme "à éviter" car ils ont un équivalent template-based plus consulting :

| Code-based à éviter | Template recommandé à la place |
|---|---|
| `swot` | `matrix_2x2_styled` |
| `cards` | `framework_3cards` |
| `process` | `process_steps` |
| `chart` | `kpi_with_chart` |
| `agenda` | `agenda_diagonal` |
| `timeline` | `roadmap_styled` |
| `quote` | `quote_callout` |
| `comparison` | `comparison_2cols` |
| `matrix_2x2` | `matrix_2x2_styled` |
| `roadmap` | `roadmap_styled` |

### 5.3 — Layouts code-based encore légitimes

10 layouts code-based restent utiles pour des cas spécifiques :
`hero_stat`, `big_idea`, `dashboard`, `pyramid`, `funnel`, `org_chart`, `stat_grid`, `image_hero`, `content`, `text`.

**Note** : à utiliser avec parcimonie. Si possible, préférer une composition libre via `canvas_blank`.

---

## 6. Limites techniques à respecter

| Layout | Limite |
|---|---|
| `agenda_diagonal` | 7 items max par page (paginé auto au-delà) |
| `matrix_2x2_styled` | 3 bullets max par quadrant |
| `roadmap_styled` | 5 milestones max |
| `process_steps` | 4-5 étapes max |
| `framework_3cards` | 3-4 cartes max |
| `data_table` | 6 colonnes max, 8 lignes max |
| `canvas_blank` | 6 blocs max |
| Bullets en général | 4 max par bloc, 8 mots max par bullet |

### Longueurs de texte recommandées

| Champ | Longueur max |
|---|---|
| Title (slide) | 70 caractères |
| Subtitle | 90 caractères |
| Eyebrow | 25 caractères |
| Takeaway | 130 caractères |
| Bullet item | 80 caractères |
| KPI label | 30 caractères |
| KPI value | 8 caractères |
| Closing title (MERCI) | 30 caractères |
| Section title | 35 caractères |

---

## 7. Le prompt-template renforcé

Voici le prompt à utiliser à chaque génération de deck. Copie-le tel quel dans Claude Code et complète avec ton contenu à la fin.

```
Mission — Génération d'un deck consulting via aosis-deck-builder

Tu as accès au skill dans `aosis-deck-builder/`. Avant toute génération, lis impérativement et dans cet ordre :

1. SKILL.md
2. references/philosophy.md — philosophie éditoriale consulting (action titles, ghost deck test, structure narrative)
3. references/layouts.md — fiches de tous les layouts disponibles
4. references/json-schema.md — formats JSON par layout

RÈGLES STRICTES DE QUALITÉ ÉDITORIALE

A. Principe fondamental
- Une slide = un message. Une seule idée par slide.
- Le titre est une phrase d'action, jamais un mot-clé.

B. Structure obligatoire du deck
1. Slide 1 : cover
2. Slide 2 : agenda_diagonal
3. Slide 3 : section_diagonal (1re partie)
4. ... slides de contenu ...
5. Avant-dernière : closing_diagonal
6. Dernière : final_branding

C. Choix des layouts
Pour CHAQUE slide :
- Identifie le type de message
- Lis la fiche du layout dans references/layouts.md
- Vérifie "Quand l'utiliser" et "Quand ne pas l'utiliser"

D. Règles spécifiques
D.1 — Tableaux : utilise data_table (ne convertis JAMAIS un tableau en KPI cards)
D.2 — Au moins 1 canvas_blank libre par deck 10+ slides
D.3 — Layouts code-based réservés à l'exceptionnel
D.4 — Sections claires : Diagnostic → Vision → Stratégie → Plan → Next steps

E. Limites techniques (voir tableau ci-dessus)

F. Sources et images
F.1 — Chaque slide doit avoir une source dans le JSON
F.2 — image_keyword en anglais concret, 2-4 mots

G. Texte : voir tableau de longueurs ci-dessus

WORKFLOW OBLIGATOIRE

Avant de générer le JSON spec, propose-moi un plan en bullet list :
- Position de chaque slide
- Layout choisi
- Justification en 1 phrase
- Take-away en 1 phrase

Attends ma validation du plan avant de générer.

Étape supplémentaire — Ghost deck test (obligatoire avant génération)

Une fois ton plan validé, AVANT de générer le JSON :

1. Liste uniquement les titres de toutes les slides en séquence
2. Lis-les comme s'ils formaient un texte continu
3. Vérifie que :
   - Chaque titre est une phrase d'action complète (jamais un mot-clé)
   - La séquence raconte une histoire logique et complète
   - Aucun titre ne pourrait être déplacé sans perte de sens
4. Si un titre échoue à un de ces critères, reformule-le avant de
   générer le JSON
5. Présente brièvement le résultat du ghost deck test dans le chat
   (les titres en séquence) pour validation finale par l'utilisateur

Confirme à la fin :
- Layouts effectivement utilisés
- Présence d'au moins 1 canvas_blank
- Présence d'au moins 1 data_table si le source contenait un tableau
- Confirmation clôture closing_diagonal + final_branding
- Temps de génération

CONTENU À METTRE EN FORME

[Ici tu colles ton contenu : brief, PDF, audit, données, citations, contexte client, etc.]
```

---

## 8. Bonnes pratiques sur les image keywords

Toujours en **anglais et concret** (2-4 mots). Pas d'abstraction.

| ❌ Mauvais | ✅ Bon |
|---|---|
| `strategy` | `business strategy meeting` |
| `infrastructure` | `data center server room` |
| `digital transformation` | `laptop modern office` |
| `growth` | `upward graph success` |
| `team` | `team collaboration desk` |
| `innovation` | `scientist laboratory` |
| `merci` | `business handshake success` |
| `sommaire` | `business meeting overview` |
| `diagnostic` | `data center server room` |
| `vision stratégique` | `business strategy whiteboard` |
| `plan d'exécution` | `project timeline planning` |

---

## 9. Commandes utiles

### 9.1 — Lancer les tests

```bash
cd ~/Projets/Skill_pptx_Aosis
python -m pytest aosis-deck-builder/tests/ -v
```

Tu dois voir : **76 passed, 1 skipped**.

### 9.2 — Générer un deck

```bash
python aosis-deck-builder/scripts/build_deck.py \
  --spec examples/mon_deck.json \
  --out examples/mon_deck.pptx
```

Options utiles :
- `--no-images` : pas d'images Pexels (génération plus rapide pour tests)
- `--debug-layouts` : affiche les layouts disponibles et leurs placeholders

### 9.3 — Régénérer un deck existant

Tous les decks d'exemple ont leur JSON spec gardé. Pour régénérer :

```bash
python aosis-deck-builder/scripts/build_deck.py \
  --spec examples/cloud_computing_2026_v3.json \
  --out examples/cloud_computing_2026_v3.pptx
```

---

## 10. Architecture du projet

### 10.1 — Flux de génération

```
1. Spec JSON utilisateur
    ↓
2. build_deck.py charge la spec
    ↓
3. Pour chaque slide :
   a. Identifie le layout
   b. Si template-based : template_engine.py charge la slide modèle, remplit les placeholders
   c. Si code-based : crée la slide via python-pptx (legacy)
    ↓
4. Pour les éléments dynamiques :
   - Charts → chart_engine.py (matplotlib → PNG → insertion)
   - Images → image_engine.py (Pexels API → bytes → insertion)
   - Icônes → icon_engine.py (Iconify API)
   - Tableaux → _process_data_table dans template_engine.py
    ↓
5. Post-processing :
   - Découpe diagonale (custGeom layout)
   - Uniformité de police (REPEAT_ITEM et matrix)
   - Anti-débordement (closing, KPI)
   - Effets premium (drop shadows, encadrement charts)
    ↓
6. Sauvegarde du .pptx
```

### 10.2 — Conventions de nommage

Placeholders dans les slides du template utilisent `{{...}}` :
- `{{TITLE}}`, `{{SUBTITLE}}`, `{{EYEBROW}}`, `{{TAKEAWAY}}`, `{{SOURCE}}`
- `{{IMAGE}}`, `{{REF}}`
- `{{REPEAT_ITEM}}` groupe contenant `{{ITEM_*}}` variants
- `{{QUAD_*_TITLE}}`, `{{QUAD_*_BULLETS}}` pour la matrix
- `{{AUTHOR_NAME}}`, `{{AUTHOR_EMAIL}}`, `{{AUTHOR_PHONE}}`, `{{ORGANIZATION_SITE}}` pour la clôture

### 10.3 — Palette AOSIS

Lue dynamiquement depuis `brand.py` qui parse le theme1.xml du template :

| Variable | Couleur | Code |
|---|---|---|
| dk1 (navy principal) | Bleu marine | `#14163C` |
| lt1 (fond) | Blanc cassé | `#FAFAF7` |
| dk2 (gris foncé) | Gris bleu | `#4A4D6B` |
| lt2 (gris clair) | Gris très clair | `#E8E9F2` |
| accent1 (orange) | Orange AOSIS | `#F26622` |
| accent2 (navy alt) | Bleu plus clair | `#1E2261` |
| accent3 (orange foncé) | Orange foncé | `#C2491A` |
| accent4 (jaune) | Jaune | `#F9B233` |
| accent5 (vert) | Vert | `#7CB342` |
| accent6 (rouge) | Rouge | `#E63946` |

Police principale : **Arial** uniquement (charte AOSIS).

---

## 11. Maintenance et évolutions

### 11.1 — Modifier le template AOSIS_template.pptx

Si tu veux modifier un layout existant ou en ajouter un nouveau :

1. **Backup obligatoire** :
   ```bash
   cp aosis-deck-builder/assets/AOSIS_template.pptx \
      aosis-deck-builder/assets/AOSIS_template.backup-$(date +%Y%m%d).pptx
   ```

2. **Modifie le template** dans PowerPoint :
   - Mode "Slide Master" pour modifier les layouts
   - Ajouter des placeholders nommés `{{XXX}}` pour les zones dynamiques
   - Renommer la slide via `cSld.name` (via python-pptx, le nommer dans le code)

3. **Lance les tests** pour vérifier qu'aucun layout existant n'est cassé :
   ```bash
   python -m pytest aosis-deck-builder/tests/ -v
   ```

4. **Documente** dans `references/layouts.md` la fiche du nouveau layout.

### 11.2 — Ajouter un nouveau type de chart

Dans `chart_engine.py`, ajoute une fonction `_chart_<type>(spec, ax)` qui dessine le graphique. Ajoute le type dans le dispatcher principal.

Documente dans `references/json-schema.md` le nouveau type.

### 11.3 — Ajouter un nouveau bloc canvas_blank

Dans `template_engine.py`, ajoute un helper `_cb_render_<type>(slide, block, rect)` qui dessine le bloc dans le rectangle fourni par la grille.

Documente dans `references/json-schema.md` et `references/layouts.md`.

---

## 12. Historique des chantiers (résumé)

Pour comprendre l'évolution du skill :

| Chantier | Apport principal |
|---|---|
| 1-7 | Polish initial et consolidation |
| 8 | Charts matplotlib (8 types) |
| 9-11 | Fixes layout réels (roadmap, matrix, sommaire, images) |
| 12 | Migration Unsplash → Pexels + découpe diagonale |
| 13 | Fiches détaillées des 32 layouts |
| 14 | Freeform canvas_blank intelligent |
| 15 | Layout data_table |
| 16 | Closing + uniformité REPEAT_ITEM |
| 17 | Uniformité matrix 2×2 |
| 18 | Rendu premium (drop shadows, XXL, charts encadrés) |
| 19 | Anti-chevauchement KPI XXL |
| 20 | Positionnement dynamique KPI cards |

Chaque chantier a un rapport détaillé dans `chantier<N>_report.md` à la racine.

---

## 13. Troubleshooting fréquent

### 13.1 — "ModuleNotFoundError: No module named 'pptx'"

Tu lances depuis ton shell utilisateur. Utilise plutôt Claude Code qui a le bon environnement.

### 13.2 — "PermissionError: cannot write to file"

Le `.pptx` est ouvert dans PowerPoint. Ferme-le et relance.

### 13.3 — Photos Pexels random / pas pertinentes

Vérifie que `PEXELS_API_KEY` est bien chargée :
```bash
cat .env
```

Et que les `image_keyword` dans le JSON spec sont en anglais et concrets.

### 13.4 — Texte qui déborde malgré le post-processing

Probablement un layout pas couvert par l'anti-débordement. Documente le cas, ajoute un test, et patche au cas par cas dans `template_engine.py`.

### 13.5 — Régression de tests après modification

Lance `pytest -v` pour identifier les tests cassés. Si le test reflète le comportement attendu (avant ta modification), c'est ta modification qui pose problème. Si le test reflète un comportement obsolète, adapte-le.

---

## 14. Quand tu reviens sur le projet après une pause

1. **Re-vérifie l'état** : `python -m pytest aosis-deck-builder/tests/ -v` doit donner 76 passed.
2. **Re-lis** ce guide opérationnel et `SKILL.md`.
3. **Re-vérifie la clé Pexels** : `cat .env`.
4. **Lance une génération test** :
   ```bash
   python aosis-deck-builder/scripts/build_deck.py \
     --spec examples/test_canvas_blank_showcase.json \
     --out /tmp/test.pptx
   ```
5. **Ouvre le résultat** pour valider que rien n'a régressé.

---

## 15. Pistes d'amélioration futures (non urgentes)

Si un jour tu veux pousser plus loin :

1. **Module de validation visuelle** : un "linter" qui ouvre le `.pptx` généré, détecte les overlaps de bounding boxes et émet des warnings.
2. **Suppression progressive des 10 layouts code-based à éviter** : les retirer du DISPATCH pour clarifier le skill.
3. **Layouts manquants** : `org_chart_template`, `hero_stat_template`, `image_hero_template` en template-based propre (au lieu de code-based).
4. **Cache d'images Pexels** : éviter de re-télécharger les mêmes images entre régénérations.
5. **Mode `--minimal-style`** : désactiver les effets premium pour des rendus plus sobres.
6. **Refonte du `kpi_with_chart`** : passage horizontal → vertical (proposition documentée en §5.1 du rapport Chantier 20).
7. **Gantt** : implémenter le layout `gantt` qui est documenté mais pas codé.

---

**Fin du guide. Bon usage du skill.**
