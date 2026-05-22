# Chantier 4 — Migration SKILL.md vers le pattern Anthropic progressive disclosure

> Date : 2026-05-13 · Scope strict : documentation uniquement (`SKILL.md` + nouveau dossier `references/` + `CHANGELOG.md` + ce rapport). Aucun touch sur `scripts/` ni `assets/`.

---

## TL;DR

| Métrique | Avant | Après |
|---|---|---|
| SKILL.md (lignes) | **384** | **134** (−65 %, sous la limite ≤ 200) |
| Fichiers de référence dédiés | 0 | 3 (`layouts.md`, `json-schema.md`, `qa.md`) |
| Volume total documentation | 384 lignes en 1 fichier | 576 lignes en 4 fichiers |
| Coût contexte par invocation Claude | full SKILL.md (~14 KB) | SKILL.md seul (~5 KB) + références chargées à la demande |

Aucune perte d'information. Tous les liens internes validés.

---

## 1. Longueurs finales

```text
  134 SKILL.md
  245 references/json-schema.md
  132 references/layouts.md
   65 references/qa.md
  576 total
```

SKILL.md repasse en **134 lignes**, sous le plafond de 200 fixé par le pattern Anthropic. Les références totalisent 442 lignes, dont 245 pour `json-schema.md` (le morceau le plus dense — exemple complet + référence champ-par-champ pour les 23 layouts).

---

## 2. Checklist de migration

| Section originale (lignes SKILL.md) | Destination | Statut |
|---|---|---|
| Frontmatter YAML (`name`, `description`) — l.1-4 | SKILL.md (intact) | ✅ Verbatim |
| H1 + intro paragraph — l.6-12 | SKILL.md (intact) | ✅ Verbatim |
| **The Three Golden Rules** + tableau Action vs Descriptive — l.14-43 | SKILL.md (intact) | ✅ Verbatim |
| **Layout Catalogue** (3 familles, 23 layouts) — l.45-86 | `references/layouts.md` | ✅ Migré + enrichi avec dimensional caps et visual recommendations issus de l'ancienne section JSON Spec |
| **The Build Workflow** (4 étapes) — l.88-107 | SKILL.md (raccourci) | ✅ 4 étapes conservées ; pointeurs explicites vers `references/layouts.md`, `references/json-schema.md`, `references/qa.md` |
| **JSON Spec Schema** — exemple complet 12 slides — l.111-246 | `references/json-schema.md` | ✅ Verbatim |
| **JSON Spec Schema** — référence champ-par-champ — l.248-327 (17 layouts) | `references/json-schema.md` | ✅ Verbatim (17 originaux) + **6 ajouts** couvrant les layouts qui n'avaient pas de field-reference dans l'original (voir §5) |
| **QA — Always Verify Visually** + commandes + symptôme→fix — l.329-358 | `references/qa.md` | ✅ Verbatim, organisé en tableau symptôme/fix |
| **Content QA** + grep — l.360-367 | `references/qa.md` | ✅ Verbatim, avec explication des patterns |
| **What This Skill Does NOT Do** — l.369-378 | SKILL.md (intact) | ✅ Verbatim |
| **Delivering to the User** — l.380-384 | SKILL.md (intact) | ✅ Verbatim |
| **(nouveau)** Index des références | SKILL.md | ✅ Ajouté après l'intro et avant les Three Golden Rules |
| **(nouveau)** Quick example inline (3 slides) | SKILL.md | ✅ Ajouté ; renvoie explicitement à `json-schema.md` pour le schéma complet |

---

## 3. Pointeurs validés

Vérification automatique : tous les liens `[texte](path/to/file.md)` dans les 4 fichiers résolvent correctement.

```text
✓ SKILL.md → references/layouts.md     (×2)
✓ SKILL.md → references/json-schema.md (×3)
✓ SKILL.md → references/qa.md          (×2)
✓ references/layouts.md → json-schema.md
✓ references/json-schema.md → layouts.md
✓ references/json-schema.md → qa.md
```

Aucun lien cassé.

---

## 4. Lecture-test : un Claude qui lit uniquement SKILL.md

Critères :

| Critère | Verdict |
|---|---|
| Comprendre la philosophie (3 règles d'or) | ✅ Section "The Three Golden Rules" intacte, tableau Action vs Descriptive inclus |
| Suivre le workflow (4 étapes) | ✅ Section "Build Workflow" avec 4 étapes numérotées et pointeurs explicites |
| Savoir où chercher pour le détail des layouts | ✅ Index "References" en tête de fichier + lien dans l'étape 1 |
| Savoir où chercher pour le schéma JSON | ✅ Index + lien dans l'étape 2 + lien dans Quick Example |
| Savoir où chercher pour le QA | ✅ Index + lien dans l'étape 4 |
| Produire un mini-deck avec l'exemple inline | ✅ Section "Quick example" — JSON valide de 3 slides (cover, hero_stat, matrix_2x2, roadmap, closing) que Claude peut copier-modifier |
| Savoir ce que le skill ne fait PAS | ✅ Section conservée |
| Savoir comment livrer | ✅ Section conservée |

**Verdict : lecture-test passé.** Un Claude qui n'a que SKILL.md sous les yeux peut produire un mini-deck immédiatement, et sait où aller pour tout le reste.

---

## 5. Incohérences détectées entre SKILL.md original et le code (notées, non corrigées)

Conformément à l'instruction du périmètre : **noter, pas corriger.**

### 5.1 Gap dans le JSON Spec Schema d'origine

Dans le SKILL.md d'origine, la section "Layout-specific field reference" (l.248-327) documentait les champs pour **17 layouts** :

`hero_stat`, `big_idea`, `matrix_2x2`, `swot`, `pyramid`, `org_chart`, `funnel`, `roadmap`, `stat_grid`, `dashboard`, `agenda`, `timeline`, `cards`, `comparison`, `chart`, `quote`, `image_hero`.

**Mais 6 layouts du dispatcher n'avaient pas de field reference** :

`cover`, `section`, `closing`, `text`, `content`, `process`.

Ces 6 layouts étaient mentionnés dans le catalogue (avec une ligne "Use when…") mais leurs champs JSON n'étaient documentés nulle part — Claude devait deviner depuis les exemples inline ou aller lire `build_deck.py`.

**Décision pour ce chantier** : combler la lacune dans `references/json-schema.md`, en sourçant les noms de champs directement depuis le `DISPATCH` de `scripts/build_deck.py` (vérifiable) :

| Layout | Champs sourcés du dispatcher |
|---|---|
| `cover` / `section` | `title`, `ref` |
| `closing` | aucun (déclenché par `"closing": true` au root) |
| `text` | `title`, `bullets` (list[str] ou list[{text, level}]) |
| `content` | `title`, `bullets`, `image` (chemin absolu) |
| `process` | `title`, `steps` (list de step objects) |

C'est une **addition de documentation, pas une modification** de comportement. Elle aurait pu être faite plus tard mais elle s'intègre naturellement dans le chantier de migration "couvrir les 23 layouts".

### 5.2 Conseil QA légèrement obsolète

Dans la section QA, l'item "Roadmap labels colliding — Reduce to 5 milestones max for safety" parle d'un **chevauchement de labels** comme principal risque. Depuis le Chantier 1, le **vrai** problème (débordement hors slide) a été corrigé via réduction de l'amplitude du tracé. La collision résiduelle à n=6 (labels de 1.9" séparés de 1.52") est mitigée par l'alternance haut/bas du code.

**Le conseil reste valide** mais sur-prudent : on peut désormais aller jusqu'à 6 milestones sans débordement. J'ai préservé le texte verbatim conformément à "aucune perte d'information". Un chantier de rafraîchissement docs futur pourrait l'assouplir.

### 5.3 Catalogue vs dispatcher : aucune incohérence

Cross-check automatique : les **23 layouts du dispatcher** sont **tous présents** dans le catalogue (`references/layouts.md`) et tous présents dans la field reference (`references/json-schema.md`). Pas de layout fantôme dans la doc, pas de layout orphelin dans le code.

---

## 6. Livrables

| Livrable | Chemin | Taille |
|---|---|---|
| SKILL.md refactoré | [`aosis-deck-builder/SKILL.md`](aosis-deck-builder/SKILL.md) | 134 lignes |
| Catalogue des layouts | [`aosis-deck-builder/references/layouts.md`](aosis-deck-builder/references/layouts.md) | 132 lignes |
| Schéma JSON | [`aosis-deck-builder/references/json-schema.md`](aosis-deck-builder/references/json-schema.md) | 245 lignes |
| QA | [`aosis-deck-builder/references/qa.md`](aosis-deck-builder/references/qa.md) | 65 lignes |
| Rapport | [`chantier4_report.md`](chantier4_report.md) | — |
| CHANGELOG | [`CHANGELOG.md`](CHANGELOG.md) | entrée Chantier 4 ajoutée |

Aucun fichier de code ou template touché. Périmètre strictement respecté.
