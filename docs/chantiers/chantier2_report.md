# Chantier 2 — Nettoyage et unification du template `AOSIS_template.pptx`

> Date : 2026-05-13 · Scope strict : `aosis-deck-builder/assets/AOSIS_template.pptx` + documentation. Aucun touch sur `scripts/build_deck.py` ni `SKILL.md`.

---

## TL;DR

| Objectif | Statut |
|---|---|
| Cover/Closing utilisent désormais la palette AOSIS (navy `#14163C` + orange `#F26622`) | ✅ |
| Cover/Closing utilisent désormais Arial (vs Aptos avant) | ✅ |
| Zéro occurrence de la couleur rouille `#D34817` dans un deck généré | ✅ |
| Template ouvre sans erreur dans python-pptx | ✅ |
| Template ouvre sans erreur dans PowerPoint | ✅ |
| Réduction de la taille du template | ✅ (−725 octets / −0.13 %) |
| **Un seul theme XML embarqué** | ❌ **Impossible** — contrainte PowerPoint découverte en cours de route. Voir §4 et §6. |

---

## 1. État initial — référencement des themes

| Fichier | Théme name | colorScheme | Polices | Référencé par |
|---|---|---|---|---|
| `ppt/theme/theme1.xml` | `01 - Blue` | **Orange rouge** (`#D34817`) | Aptos Display / Aptos | `slideMaster1.xml.rels`, `presentation.xml.rels` (rId10) |
| `ppt/theme/theme2.xml` | `02 - White` | **AOSIS** (`#F26622`, `#14163C`) | Arial / Arial | `slideMaster2.xml.rels` |
| `ppt/theme/theme3.xml` | `Thème Office` | Office | Calibri Light / Calibri | `notesMaster1.xml.rels` |
| `ppt/theme/theme4.xml` | `Thème Office` | Office | Aptos Display / Aptos | `handoutMaster1.xml.rels` |

`[Content_Types].xml` listait 4 Override pour theme1.xml..theme4.xml.

### Le bug

`slideMaster1` (Cover + Closing) résolvait `accent1` via `theme1` = **`#D34817`** (rouille) et héritait des polices **Aptos**. Les slides de contenu (master2) résolvaient correctement `accent1` = `#F26622` (orange AOSIS) et utilisaient Arial. Cassure visuelle d'ouverture/fermeture.

---

## 2. Plan initial vs plan exécuté

### Plan initial (énoncé du chantier)

1. Réassigner `slideMaster1.xml.rels` → `theme2.xml`.
2. Supprimer `theme1.xml`, `theme3.xml`, `theme4.xml`.
3. Renommer `theme2.xml` → `theme1.xml`.
4. Mettre à jour `[Content_Types].xml` et tous les `.rels`.
5. Résultat attendu : un seul theme dans le package.

### Pourquoi le plan initial a échoué — découverte d'une contrainte PowerPoint

J'ai d'abord exécuté le plan complet (en mode binaire pour préserver les CRLF). **python-pptx ouvrait le résultat sans erreur**, mais **PowerPoint le rejetait** avec :

```
Le fichier ou le répertoire est endommagé et illisible.
(Exception de HRESULT : 0x80070570 — BadImageFormatException)
```

J'ai bisecté en isolant chaque modification :

| Étape testée | Résultat PowerPoint |
|---|---|
| Re-zip sans aucun changement | ✅ OK (élimine une faute de zipfile) |
| Remplacer le **contenu** de `theme1.xml` par la palette AOSIS | ✅ OK |
| Remplacer `theme1` + repointer `slideMaster1` vers `theme2.xml` | ❌ rejeté |
| Remplacer `theme1` + repointer `slideMaster2` (qui pointait sur theme2) vers `theme1` | ❌ rejeté |
| Remplacer `theme1` + dupliquer le contenu dans `theme2` (sans toucher les rels) | ✅ OK |
| Idem + supprimer `theme3`/`theme4` + repointer notes/handout sur `theme1` | ❌ rejeté |

**Conclusion** : PowerPoint impose qu'**à chaque master (slideMaster, notesMaster, handoutMaster) corresponde une part-theme dédiée**. Le partage d'une même `theme.xml` entre plusieurs masters n'est pas toléré, même si python-pptx l'accepte. La spec OOXML laisse cette possibilité ouverte mais Microsoft PowerPoint resserre la contrainte.

### Plan révisé (exécuté)

1. **Remplacer le contenu** de `theme1.xml` par celui de `theme2.xml` (la palette AOSIS) — sans renommer.
2. Idem pour `theme2.xml` (qui reste identique à lui-même par construction).
3. Renommer le `name` interne des deux themes de `"02 - White"` → `"AOSIS Brand"` (cosmétique mais utile dans le sélecteur PowerPoint).
4. **Laisser intacts** `theme3.xml`, `theme4.xml`, les rels et `[Content_Types].xml`. Notes et handouts gardent leurs themes Office par défaut ; ils ne sont pas user-visibles dans les decks livrés.

Coût : la dette de "bruit XML" (themes 3 et 4 inutiles dans le workflow utilisateur) reste là. Bénéfice : le bug brand est résolu, le template fonctionne dans PowerPoint et python-pptx, taille comparable.

---

## 3. Liste exhaustive des fichiers modifiés / supprimés / renommés

| Action | Fichier | Détail |
|---|---|---|
| **Modifié (contenu)** | `ppt/theme/theme1.xml` | Contenu remplacé par celui de theme2 (palette AOSIS). Inner `name` attribute changé en `"AOSIS Brand"`. |
| **Modifié (contenu)** | `ppt/theme/theme2.xml` | Inner `name` attribute changé en `"AOSIS Brand"` (le reste inchangé). |
| Pas touché | `ppt/theme/theme3.xml` | Theme Office, lié à notesMaster1. Conservé. |
| Pas touché | `ppt/theme/theme4.xml` | Theme Office, lié à handoutMaster1. Conservé. |
| Pas touché | `[Content_Types].xml` | 4 Override theme conservés. |
| Pas touché | `ppt/_rels/presentation.xml.rels` | rId10 → theme/theme1.xml (résout désormais sur AOSIS). |
| Pas touché | `ppt/slideMasters/_rels/slideMaster1.xml.rels` | Pointe sur theme1.xml (désormais AOSIS). **Le bug est résolu sans modifier ce fichier.** |
| Pas touché | `ppt/slideMasters/_rels/slideMaster2.xml.rels` | Pointe sur theme2.xml (AOSIS, inchangé). |
| Pas touché | `ppt/notesMasters/_rels/notesMaster1.xml.rels` | Pointe sur theme3.xml (Office, inchangé). |
| Pas touché | `ppt/handoutMasters/_rels/handoutMaster1.xml.rels` | Pointe sur theme4.xml (Office, inchangé). |

Tous les autres fichiers (slideMasters, slideLayouts, médias, etc.) sont inchangés byte-pour-byte (re-zippés tels quels).

---

## 4. État final

### Theme effectif côté Cover/Closing (`slideMaster1` → `theme1.xml`)

| Slot | Avant | Après | Cible canonique |
|---|---|---|---|
| dk1 | sys windowText (`#000000`) | `#14163C` ✅ | `#14163C` |
| lt1 | sys window (`#FFFFFF`) | `#FAFAF7` ✅ | `#FAFAF7` |
| accent1 | `#D34817` (rouille) | `#F26622` ✅ | `#F26622` |
| accent2 | `#9B2D1F` | `#1E2261` ✅ | (variante AOSIS) |
| majorFont | Aptos Display | **Arial** ✅ | Arial |
| minorFont | Aptos | **Arial** ✅ | Arial |

### Theme effectif côté Content (`slideMaster2` → `theme2.xml`)

Identique à `theme1.xml` désormais (palette AOSIS, Arial). Inchangé par rapport à l'état initial.

### Themes notes / handout

`theme3.xml` (notes) et `theme4.xml` (handout) restent les themes Office par défaut. Pertinents uniquement pour les vues notes/handout de PowerPoint qui ne sont pas exposées dans le workflow du skill.

---

## 5. Vérifications effectuées

### 5.1 Validité structurelle

```text
✓ python-pptx opened OK: 0 slides, 2 masters, 10.0"x5.625"
  master 0: 2 layouts: 'Cover', 'Closing'
  master 1: 2 layouts: 'Contenu + texte', 'Texte'
```

PowerPoint COM (via PowerShell) confirme :

```text
OK: designs=2
  Design 1: name=AOSIS Brand
  Design 2: name=AOSIS Brand
```

LibreOffice / `soffice` toujours indisponibles dans cet environnement WSL (apt restreint). Validation visuelle via PowerPoint Windows automatisé.

### 5.2 Inventaire post-modification

| Élément | Valeur |
|---|---|
| Themes XML embarqués | **4** (theme1=AOSIS, theme2=AOSIS, theme3=Office/notes, theme4=Office/handout) |
| Masters | **2** (Cover/Closing + Contenu) |
| Layouts | **4** (Cover, Closing, Contenu + texte, Texte) |
| `accent1` résolu côté slideMaster1 (Cover/Closing) | `#F26622` (AOSIS) ✅ |
| `accent1` résolu côté slideMaster2 (Contenu) | `#F26622` (AOSIS) ✅ |

### 5.3 Test fonctionnel — deck golden

[`tests/fixtures/golden_spec.json`](aosis-deck-builder/tests/fixtures/golden_spec.json) — 5 slides : cover, hero_stat, matrix_2x2, roadmap, closing.

```text
Generated: 5 slides
Fonts (explicit runs): {'Arial': 35}
Colors (explicit runs): {'#14163C': 17, '#4A4D6B': 10, '#FFFFFF': 3, '#F26622': 5}
Rust #D34817 occurrences: 0
```

PowerPoint COM confirme l'ouverture du deck : `PPT OK: slides=5`.

### 5.4 Taille

| Fichier | Taille (octets) |
|---|---|
| `AOSIS_template.backup.pptx` | 573 578 |
| `AOSIS_template.pptx` (après C2) | **572 853** |
| Différence | **−725** (−0.13 %) |

La baisse est modeste car nous n'avons supprimé aucun fichier (seul le contenu de theme1.xml a été remplacé). L'ancien theme1 (`8733` octets non compressés) est légèrement plus gros que le nouveau theme1 (`4334` octets après edit) — d'où le gain résiduel après compression.

---

## 6. Captures Cover et Closing avant / après

Rendus via PowerPoint COM (PNG 1500×844, ~150 dpi). PNG complets dans [`aosis-deck-builder/tests/out_png_c2/`](aosis-deck-builder/tests/out_png_c2/).

### Cover

| Avant | Après |
|---|---|
| ![](chantier2_assets/cover_before.png) | ![](chantier2_assets/cover_after.png) |

Observation : la pastille "Mai 2026" en haut à droite passe d'un **rouille `#D34817`** (theme `accent1` = Orange rouge) à un **orange AOSIS `#F26622`** (theme `accent1` = AOSIS). Le bug brand est éliminé.

Le titre principal a également migré d'Aptos Display vers Arial — différence subtile à cette résolution mais perceptible en zoom. Tous les éléments restants (logo, baseline, fond navy) sont inchangés.

### Closing

Visuellement identique avant/après — toutes les couleurs du closing sont **hardcodées dans l'image logo** (raster) et dans des shapes statiques du master ; aucune ne référence `accent1` du theme. Le fix n'a donc rien à corriger sur cette slide. (Conséquence intéressante : le closing AOSIS était déjà correct.)

---

## 7. Périmètre strict respecté

- ✅ Seul le template `aosis-deck-builder/assets/AOSIS_template.pptx` a été modifié.
- ✅ Backup intouché à `aosis-deck-builder/assets/AOSIS_template.backup.pptx` (573 578 octets, identique au fichier d'origine).
- ✅ `scripts/build_deck.py` non touché.
- ✅ `SKILL.md` non touché.
- ✅ Rapport et CHANGELOG ajoutés à la racine ; rien d'autre.

---

## 8. Recommandations pour les chantiers suivants

1. **Chantier 3 (synchronisation code-template)** : les constantes `NAVY`, `ORANGE`, etc. dans `build_deck.py` peuvent désormais être confirmées comme alignées sur `theme1.xml` (la seule source canonique côté slide masters). L'audit avait noté la duplication ; après C2, les valeurs concordent partout (`#14163C`, `#F26622`, `#FAFAF7`, `#4A4D6B`, `#E8E9F2`).
2. **Bruit XML résiduel** : `theme3.xml` + `theme4.xml` (notes/handout) restent des themes Office. Suppression possible uniquement en retirant `notesMaster1` + `handoutMaster1` du package — opération nettement plus invasive (édition de `presentation.xml` + `Content_Types` + suppression de parts). À évaluer si gain justifie le risque. Mon avis : non-prioritaire — ces parts ne contaminent jamais les slides livrées.
3. **Test d'ouverture PowerPoint en CI** : la découverte de la contrainte "une theme par master" suggère d'ajouter au workflow de validation un check automatique d'ouverture par PowerPoint (ou LibreOffice si dispo). python-pptx seul est trop indulgent.

---

## 9. Reproduire les modifications

Le script Python qui produit le template final tient en ~25 lignes. Pour un patch reproductible :

```python
import zipfile, os, shutil, tempfile

SRC = 'aosis-deck-builder/assets/AOSIS_template.backup.pptx'
DST = 'aosis-deck-builder/assets/AOSIS_template.pptx'

tmp = tempfile.mkdtemp()
with zipfile.ZipFile(SRC) as zf:
    zf.extractall(tmp)

# Lire le contenu AOSIS (depuis theme2 d'origine)
with open(os.path.join(tmp, 'ppt/theme/theme2.xml'), 'rb') as fh:
    aosis = fh.read()
aosis_renamed = aosis.replace(b'name="02 - White"', b'name="AOSIS Brand"', 1)

# Écraser theme1 (et theme2 pour cohérence) avec ce contenu
for tgt in ('ppt/theme/theme1.xml', 'ppt/theme/theme2.xml'):
    with open(os.path.join(tmp, tgt), 'wb') as fh:
        fh.write(aosis_renamed)

# Re-zipper (Content_Types.xml en tête)
files = []
for d, _, fs in os.walk(tmp):
    for fn in fs:
        files.append(os.path.relpath(os.path.join(d, fn), tmp))
files.sort(key=lambda x: (0 if x == '[Content_Types].xml' else 1, x))
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zf:
    for rel in files:
        zf.write(os.path.join(tmp, rel), rel.replace(os.sep, '/'))
shutil.rmtree(tmp)
```
