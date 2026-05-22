# Chantier 24 — Nettoyage et réorganisation du repo

**Date** : 2026-05-22
**Périmètre** : Suppression définitive des résidus (`a_supprimer/`), récupération de 11 rapports historiques, archivage hors-repo des templates RH client, déplacement du PDF de test, refresh de `examples/README.md`.

## TL;DR

- ✅ Vérification sécurité : **0 fichier Template RH/Ressources jamais commité** (présent ni dans `git ls-files`, ni dans `git log --all --full-history`)
- ✅ Backup défensif tar.gz **113 MB** créé hors repo
- ✅ 11 rapports historiques (C1-C8 + 3 spéciaux) récupérés vers `docs/chantiers/` (17 → 28 rapports)
- ✅ 2 templates RH client (70 MB) archivés vers `~/Templates_RH_Client_archive/` (hors repo)
- ✅ 2 .md uniques sur le skill récupérés vers `docs/_archive_C24/`
- ✅ `a_supprimer/` supprimé (**111 MB libérés**)
- ✅ `examples/` réduit à **5 JSON + README** (de 8 → 5)
- ✅ PDF de test déplacé vers `docs/test_inputs/`
- ✅ **90 passed, 1 skipped** (pytest) + `test_skill.sh` OK

## 1. Vérification sécurité

```bash
$ git log --all --full-history --oneline -- "*Template RH*" "*template_rh*" "Ressources/*"
(vide)
$ git ls-files | grep -iE "template.rh|ressources"
(vide)
```

✅ **Aucun fichier sensible n'a jamais touché le repo Git**, ni dans l'index, ni dans l'historique des 6 commits depuis l'initial. Les fichiers RH étaient uniquement sur disque local, sous `a_supprimer/Ressources/` (lui-même gitignored).

## 2. Backup défensif

```bash
$ ls -lh ~/Skill_pptx_Aosis_backup_*.tar.gz
-rw-r--r-- 113M /home/florianhorellou/Skill_pptx_Aosis_backup_before_chantier24_20260522_100503.tar.gz
```

Exclusions tar : `.git/` (versionné déjà) + `Skill_pptx_Aosis/a_supprimer/Ressources/Template*.pptx` (70 MB).

**Action utilisateur** : conserver ce backup au moins jusqu'à validation visuelle complète. Suppression manuelle ensuite.

## 3. Fichiers récupérés depuis `a_supprimer/_archive/reports/`

11 rapports historiques copiés vers `docs/chantiers/` (aucune collision détectée) :

| Origine | Destination |
|---|---|
| `a_supprimer/_archive/reports/chantier1_report.md` | `docs/chantiers/chantier1_report.md` |
| `a_supprimer/_archive/reports/chantier2_report.md` | `docs/chantiers/chantier2_report.md` |
| `a_supprimer/_archive/reports/chantier3_report.md` | `docs/chantiers/chantier3_report.md` |
| `a_supprimer/_archive/reports/chantier4_report.md` | `docs/chantiers/chantier4_report.md` |
| `a_supprimer/_archive/reports/chantier5_report.md` | `docs/chantiers/chantier5_report.md` |
| `a_supprimer/_archive/reports/chantier6_report.md` | `docs/chantiers/chantier6_report.md` |
| `a_supprimer/_archive/reports/chantier7_report.md` | `docs/chantiers/chantier7_report.md` |
| `a_supprimer/_archive/reports/chantier8_report.md` | `docs/chantiers/chantier8_report.md` |
| `a_supprimer/_archive/reports/chantier_consolidation_report.md` | idem |
| `a_supprimer/_archive/reports/chantier_exhibits_report.md` | idem |
| `a_supprimer/_archive/reports/chantier_naming_report.md` | idem |

**Total `docs/chantiers/`** : 17 → **28 rapports** (couverture complète C1 → C24).

## 4. Fichiers récupérés vers `docs/_archive_C24/`

2 .md à contenu unique sur le skill (vérifié par `grep -rln` : aucune copie ailleurs dans le repo) :

| Origine | Destination |
|---|---|
| `a_supprimer/Ressources/audit_report.md` (322 lignes) | `docs/_archive_C24/2026-05-13_audit_report.md` |
| `a_supprimer/Ressources/skill_aosis_deck_builder_documentation.md` (485 lignes) | `docs/_archive_C24/2026-05-13_skill_documentation.md` |

+ un nouveau `docs/_archive_C24/README.md` explique le contenu de ce dossier.

## 5. Templates RH client → hors repo

```bash
$ ls -lh ~/Templates_RH_Client_archive/
-rw-r--r--  35M  Template RH - Copie.pptx
-rw-r--r--  25   Template RH - Copie.pptx:Zone.Identifier
-rw-r--r--  35M  Template RH.pptx
drwxr-xr-x      template_rh_inventory/      (PNG slides Template RH)
-rw-r--r--  6.1K template_rh_inventory.md    (inventaire textuel)
drwxr-xr-x      template_rh_patterns/       (JPG patterns)
-rw-r--r--  14K  template_rh_patterns.md     (patterns visuels)
```

**Action utilisateur recommandée** : transférer `~/Templates_RH_Client_archive/` sur un cloud privé sécurisé (OneDrive AOSIS, drive perso) puis supprimer localement. Ces fichiers sont des templates client, ne doivent ni rester sur le poste indéfiniment ni jamais entrer dans Git.

## 6. Fichiers supprimés

### `a_supprimer/` (111 MB libérés)

| Élément | Taille | Note |
|---|---:|---|
| 5 × `*.before-chantier*.py` (Python backups) | 341 KB | Historique Git couvre |
| 2 × `AOSIS_template.before-*.pptx` | 1.4 MB | Idem |
| 7 × `.pptx` générés (cloud_*, test_*) | 6.0 MB | Regénérables |
| `cloud_computing_rapport.pdf:Zone.Identifier` | 25 B | Artefact WSL |
| `.pytest_cache/` | 28 KB | Cache pytest |
| `_archive/{assets,backups,snapshots,test_outputs}` | 103 MB | (`_archive/reports/` récupéré, voir §3) |

### `examples/` (3 JSON résidus)

| Fichier | Raison |
|---|---|
| `cloud_2026_v2.json` | Aucune référence dans le code/tests/docs. Itération obsolète |
| `cloud_2026_v3.json` | Idem |
| `cloud_computing_2026.json` | Que des mentions textuelles dans 6 rapports (texte uniquement, jamais lu par du code). V1 obsolète |

## 7. Fichiers déplacés

| Avant | Après |
|---|---|
| `examples/cloud_computing_rapport.pdf` | `docs/test_inputs/cloud_computing_rapport.pdf` |

## 8. Fichiers modifiés

| Fichier | Modification |
|---|---|
| `examples/README.md` | Réécrit : liste les 5 JSON restants, distingue "automatique" (`test_skill.sh`) vs "validation visuelle manuelle", remplace `roadmap` (déprécié C23) par `roadmap_styled`, mentionne `docs/test_inputs/` |

## 9. `.gitignore` — vérifié, complet

Patterns demandés vs présents :
- ✅ `.env`, `.pytest_cache/`, `__pycache__/`, `~$*`, `before-chantier`, `a_supprimer/`, `_archive/`, `Ressources/`
- ✅ `*.pyc` couvert par `*.py[cod]`
- N/A `Templates_RH_Client_archive/` : hors repo (sous `~/`), pas besoin d'ignore
- N/A `aosis-deck-builder.skill` : décidé trackable au Chantier 20 (livrable utilisateur)

**Aucune modification nécessaire.**

## 10. Tests de non-régression

```
$ pytest tests/test_smoke.py
======================== 90 passed, 1 skipped in 9.28s =========================

$ bash test_skill.sh
==> pytest : 90 passed, 1 skipped
==> Generate example_minimal.pptx → /tmp/.../example_minimal.pptx (568 KB)
==> Generate example_full.pptx     → /tmp/.../example_full.pptx (624 KB)
==> All green.
```

Zéro régression. Tous les layouts générés correctement.

## 11. Arborescence finale

```
Skill_pptx_Aosis/
├── README.md
├── CHANGELOG.md
├── .env.example                       (.env gitignored)
├── .gitignore
├── build_bundle.sh                    regénère le bundle .skill
├── test_skill.sh                      smoke test
│
├── aosis-deck-builder/                # le skill Claude (source)
│   ├── SKILL.md
│   ├── pyproject.toml
│   ├── assets/AOSIS_template.pptx     (un seul template, pas de backup)
│   ├── references/                    (4 docs)
│   ├── scripts/                       (7 modules .py, pas de backup)
│   └── tests/                         (test_smoke.py + fixtures/)
│
├── aosis-deck-builder.skill           bundle uploadable Claude (~690 KB)
│
├── docs/                              # documentation
│   ├── README.md                      index
│   ├── GUIDE_INSTALLATION.md
│   ├── GUIDE_OPERATIONNEL.md
│   ├── chantiers/                     28 rapports (C1 → C24 + 3 spéciaux)
│   ├── _archive_C24/                  2 docs internes historiques + README
│   └── test_inputs/                   cloud_computing_rapport.pdf
│
└── examples/                          # specs JSON
    ├── README.md                      (refresh post-C24)
    ├── example_minimal.json           smoke test
    ├── example_full.json              vitrine catalogue
    ├── test_canvas_blank_showcase.json  régression manuelle
    ├── test_data_table_showcase.json    régression manuelle
    └── test_migration_cloud.json        gros deck client référence
```

Hors repo (sur disque local seulement) :
- `~/Templates_RH_Client_archive/` (70 MB de templates client + .md d'inventaire)
- `~/Skill_pptx_Aosis_backup_before_chantier24_*.tar.gz` (113 MB, à supprimer manuellement après validation)

## 12. Livrables

| Catégorie | Fichiers |
|---|---|
| Supprimés | `a_supprimer/` (entier), `examples/cloud_2026_v2.json`, `examples/cloud_2026_v3.json`, `examples/cloud_computing_2026.json` |
| Déplacés | `examples/cloud_computing_rapport.pdf` → `docs/test_inputs/` |
| Récupérés | 11 rapports historiques → `docs/chantiers/` ; 2 .md skill → `docs/_archive_C24/` |
| Modifiés | `examples/README.md` |
| Hors repo (action user) | 2 Templates RH + inventaires → `~/Templates_RH_Client_archive/` ; backup tar.gz → `~/` |

## 13. Friction / arbitrages

1. **Le `~` dans la commande tar du brief pointait au mauvais endroit** : `cd ~ && tar Skill_pptx_Aosis/` ne marchait pas car le projet est sous `~/Projets/`. J'ai corrigé en `cd ~/Projets` + même commande tar.

2. **`a_supprimer/Ressources/` contenait 4 .md (pas 3 comme indiqué dans l'audit)** : j'avais manqué `template_rh_patterns.md` dans l'audit initial. Catégorisation finale : 2 sur le skill (récupérés vers `docs/_archive_C24/`), 2 sur le Template RH (suivent les .pptx hors repo). Le couplage logique avec les .pptx clients est la bonne réponse.

3. **`docs/_archive_C24/` plutôt que de simplement supprimer** : ces 2 docs sont des photographies du skill au 2026-05-13, hors flux des chantiers. Pas un "rapport de chantier" (donc pas dans `docs/chantiers/`), mais du contenu unique mémoriel utile pour l'onboarding ou la lecture rétro. Choix conservateur assumé.

4. **Templates RH archivés sous `~/` plutôt que supprimés** : ces fichiers client ne doivent pas rester indéfiniment sur le poste mais leur destruction définitive est la décision de l'utilisateur (potentiellement contractuel). Position hors repo + hors backup tar.gz garantit qu'ils ne reviendront jamais dans Git par erreur.

---

**Statut final** : ✅ Chantier 24 **livré sans régression**. 90/91 tests verts. Repo Git nettoyé (-111 MB locaux + 4 fichiers supprimés du tracking), historique complet préservé (28 rapports), templates client sécurisés hors repo.
