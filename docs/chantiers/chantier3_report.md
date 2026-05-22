# Chantier 3 — Lecture dynamique de la palette depuis le theme XML

> Date : 2026-05-13 · Scope strict : code Python (`scripts/build_deck.py` + nouveau `scripts/brand.py`). Aucun touch sur template, SKILL.md ou références.

---

## 1. Analyse de `NAVY_SOFT` dans `build_deck.py`

### Usages identifiés

`NAVY_SOFT` (`#2A2D5C`) apparaît **5 fois** au total dans le fichier, dont **1 déclaration** et **4 utilisations** réparties dans 4 fonctions :

| Ligne | Fonction | Code | Rôle visuel |
|---|---|---|---|
| 39 | (déclaration) | `NAVY_SOFT = RGBColor(0x2A, 0x2D, 0x5C)` | — |
| 415 | `add_timeline` | `bg = NAVY if i % 2 == 0 else NAVY_SOFT` | Fond des boîtes de phase, en alternance navy / navy-soft pour créer un rythme visuel |
| 716 | `add_funnel` | `color = NAVY if i % 2 == 0 else NAVY_SOFT` | Fond des barres de funnel (sauf la dernière en orange), même alternance |
| 877 | `add_swot` | `(weaknesses, "W", ..., LIGHT, NAVY, NAVY_SOFT)` | Couleur de la lettre "W" dans le quadrant Weaknesses |
| 937 | `add_pyramid` | `color = NAVY if render_pos % 2 == 0 else NAVY_SOFT` | Fond des bandes de pyramide en alternance |

### Pattern dominant : **3 usages sur 4 sont une alternance** `NAVY / NAVY_SOFT` pour produire un rythme visuel dans une séquence de boîtes/bandes navy. Le 4ᵉ usage (swot W lettre) est ponctuel et cosmétique.

### Décision : Option C — utiliser `accent2` du theme (`#1E2261`)

**Pourquoi Option C** :
- L'audit (cf. [Ressources/audit_report.md §2.3](Ressources/audit_report.md)) avait précisément identifié `NAVY_SOFT` comme "couleur inventée non-AOSIS, sans traçabilité brand". L'objectif principal du chantier est de supprimer cette dette de couleur orpheline.
- Le theme officiel embarque déjà un **navy variant** dans `accent2` (`#1E2261`). C'est la couleur "officielle" prévue pour ce rôle. La réutiliser scelle la traçabilité brand.
- L'usage est l'**alternance** dans des séquences sombres. Cette alternance doit rester perceptible. Comparaison de luminance perçue :

| Couleur | Hex | Luminance (Rec.601) |
|---|---|---|
| navy | `#14163C` | 26 |
| navy_alt (accent2) | `#1E2261` | 40 |
| ex-NAVY_SOFT | `#2A2D5C` | 49 |

Le nouveau contraste navy ↔ navy_alt = 14 (vs 23 avant). L'alternance est **plus subtile** mais reste visible, et reste cohérente avec la palette officielle.

**Pourquoi pas Option A** (`gray`/`gray_light`) : `gray_light` est très clair (`#E8E9F2`), il aurait créé un contraste agressif blanc-sur-clair avec le texte des boîtes (qui est en `WHITE`). Inadmissible.

**Pourquoi pas Option B** (`lighten(navy, 0.12)` programmatique) : un calcul reproductible est cohérent mais ne s'ancre dans **aucun slot du theme** — donc ne profite pas du chantier (la source de vérité reste un comportement codé, pas le theme). L'option C ancre la couleur dans le theme.

---

## 2. `scripts/brand.py` — la nouvelle source de vérité

Module autonome (90 lignes), à plat dans `scripts/`. Expose :

```python
@dataclass(frozen=True)
class BrandPalette:
    navy: RGBColor          # ← theme.dk1
    light: RGBColor         # ← theme.lt1
    gray: RGBColor          # ← theme.dk2
    gray_light: RGBColor    # ← theme.lt2
    orange: RGBColor        # ← theme.accent1
    navy_alt: RGBColor      # ← theme.accent2  (remplace NAVY_SOFT inventé)
    accent3: RGBColor       # ← theme.accent3
    accent4: RGBColor       # ← theme.accent4
    accent5: RGBColor       # ← theme.accent5
    accent6: RGBColor       # ← theme.accent6
    white: RGBColor = RGBColor(0xFF, 0xFF, 0xFF)
    black: RGBColor = RGBColor(0x00, 0x00, 0x00)

    @classmethod
    def from_template(cls, template_path) -> "BrandPalette":
        # Lit ppt/theme/theme1.xml du .pptx, parse <a:clrScheme>,
        # extrait dk1, lt1, dk2, lt2, accent1..6 (srgbClr ou sysClr@lastClr).
        ...

    def hex(self, color: RGBColor) -> str:
        # Renvoie "#XXXXXX" pour matplotlib.
        return f"#{color}"


class BrandError(Exception): ...
```

Smoke test à l'import :

```
navy        -> #14163C
light       -> #FAFAF7
gray        -> #4A4D6B
gray_light  -> #E8E9F2
orange      -> #F26622
navy_alt    -> #1E2261     ← ex-NAVY_SOFT (était #2A2D5C, désormais accent2)
accent3     -> #C2491A
accent4     -> #F9B233
accent5     -> #7CB342
accent6     -> #E63946
white       -> #FFFFFF
black       -> #000000
```

---

## 3. Refactoring de `build_deck.py`

### Suppressions

- 7 constantes hex hardcodées (lignes 33-39 dans l'ancien fichier) : `NAVY`, `ORANGE`, `LIGHT`, `GRAY`, `GRAY_LIGHT`, `WHITE`, `NAVY_SOFT`. Total **0** constante hex restante après refactor.
- `from pptx.dml.color import RGBColor` retiré (plus utilisé directement dans build_deck.py — c'est `brand.py` qui en a besoin).

### Ajouts

```python
from brand import BrandPalette  # sibling module in scripts/

# ...

BRAND = BrandPalette.from_template(TEMPLATE_PATH)
```

### Substitutions appliquées (script reproductible, mode regex avec word-boundaries)

| Pattern | Remplacement | Occurrences |
|---|---|---|
| `\bNAVY_SOFT\b` | `BRAND.navy_alt` | 4 |
| `\bGRAY_LIGHT\b` | `BRAND.gray_light` | 10 |
| `\bNAVY\b` | `BRAND.navy` | 37 |
| `\bORANGE\b` | `BRAND.orange` | 30 |
| `\bGRAY\b` | `BRAND.gray` | 22 |
| `\bWHITE\b` | `BRAND.white` | 13 |
| `\bLIGHT\b` | `BRAND.light` | 5 |

Ordre choisi pour éviter les remplacements partiels (NAVY_SOFT avant NAVY, GRAY_LIGHT avant GRAY).

### Substitutions matplotlib (bonus — hex strings dans `_render_chart_png` et `_generate_abstract_background`)

Le fichier contenait également des `'#XXXXXX'` en clair pour matplotlib (qui n'accepte pas `RGBColor`). Remplacés par f-strings `f"#{BRAND.attr}"` :

| Hex source | f-string remplacement | Occurrences |
|---|---|---|
| `"#14163C"` | `f"#{BRAND.navy}"` | 6 |
| `"#F26622"` | `f"#{BRAND.orange}"` | 3 |
| `"#FAFAF7"` | `f"#{BRAND.light}"` | 2 |
| `"#4A4D6B"` | `f"#{BRAND.gray}"` | 4 |
| `"#7CB342"` | `f"#{BRAND.accent5}"` | 1 |
| `"#F9B233"` | `f"#{BRAND.accent4}"` | 1 |

Soit **17 hex strings matplotlib** remplacés en plus.

### Audit post-refactor

```bash
$ grep -nE "'#[0-9A-Fa-f]{6}'|\"#[0-9A-Fa-f]{6}\"|RGBColor\(0x" scripts/build_deck.py
# (no output)
$ grep -nE "\b(NAVY|ORANGE|LIGHT|GRAY|GRAY_LIGHT|WHITE|NAVY_SOFT)\b" scripts/build_deck.py | grep -v "BRAND\."
# (no output)
```

**Zéro hex hardcodé, zéro constante orpheline.**

### Pièges anticipés et résolus

#### Piège 1 — late binding des défauts d'argument

Les fonctions `_add_text(..., color=BRAND.navy)` et `_add_circle_number(..., fill=BRAND.orange)` auraient eu leurs défauts **gelés à l'import time**. Si `build_deck()` rebinde `BRAND` (cas `--template`), les défauts auraient pointé sur l'ancien `BRAND`. Fix : sentinelle `None` et résolution dans le corps de la fonction.

```python
def _add_text(..., color=None, ...):
    if color is None:
        color = BRAND.navy
    ...
```

Les **autres** références à `BRAND.*` dans les corps de fonctions ne souffrent pas du problème — Python résout `BRAND` à l'appel via les globals du module, donc une rebind globale est prise en compte.

#### Piège 2 — propagation `--template` à la palette

`build_deck()` rebinde explicitement `BRAND` au début pour garantir que la palette correspond au template effectivement utilisé :

```python
def build_deck(spec, output_path, template_path=None):
    template_path = Path(template_path or TEMPLATE_PATH)
    ...
    global BRAND
    BRAND = BrandPalette.from_template(template_path)
    prs = Presentation(str(template_path))
    ...
```

---

## 4. Tests de validation

### 4.1 Stabilité — deck `golden_spec.json` (5 slides cover/hero_stat/matrix_2x2/roadmap/closing)

Comparaison shape-par-shape, run-par-run :

```
PRE-C3 colors:  {'#14163C': 19, '#F26622': 12, '#4A4D6B': 10, '#FAFAF7': 2, '#FFFFFF': 3, '#E8E9F2': 1}
POST-C3 colors: {'#14163C': 19, '#F26622': 12, '#4A4D6B': 10, '#FAFAF7': 2, '#FFFFFF': 3, '#E8E9F2': 1}
PRE-C3 shapes counted: 47
POST-C3 shapes counted: 47

✓ All effective colors identical pre/post C3.
```

Le golden ne sollicite pas `NAVY_SOFT` (qui est exclusivement dans timeline / funnel / swot / pyramid). Aucun changement de teinte.

### 4.2 Stabilité ciblée — deck avec `funnel` (qui utilise `NAVY_SOFT`)

Comparaison des fills sur les barres de funnel :

```
PRE-C3 (NAVY_SOFT=#2A2D5C):
  Rounded Rectangle 2     fill=#14163C   (stage 0)
  Rounded Rectangle 5     fill=#2A2D5C   (stage 1, alternance)  ←
  Rounded Rectangle 8     fill=#14163C   (stage 2)
  Rounded Rectangle 11    fill=#F26622   (stage 3, conversion)

POST-C3 (navy_alt=#1E2261):
  Rounded Rectangle 2     fill=#14163C   (stage 0)
  Rounded Rectangle 5     fill=#1E2261   (stage 1, alternance)  ←
  Rounded Rectangle 8     fill=#14163C   (stage 2)
  Rounded Rectangle 11    fill=#F26622   (stage 3, conversion)
```

Changement attendu et documenté : `#2A2D5C` (NAVY_SOFT inventé) → `#1E2261` (accent2 du theme, navy variant officiel).

### 4.3 Dynamicité — preuve que le theme est bien la source de vérité

J'ai créé un template temporaire `redtheme_template.pptx` en patchant `accent1` à `#FF0000` (rouge vif) **sans toucher au code**.

```bash
python scripts/build_deck.py tests/fixtures/golden_spec.json /tmp/deck_redtheme.pptx \
    --template /tmp/redtheme_template.pptx
```

Couleurs effectives du deck généré :

```
fill:14163C   -> 2x
fill:E8E9F2   -> 1x
fill:FAFAF7   -> 2x
fill:FF0000   -> 7x       ← ex-orange, désormais rouge
text:14163C   -> 17x
text:4A4D6B   -> 10x
text:FF0000   -> 5x       ← ex-orange, désormais rouge
text:FFFFFF   -> 3x

red #FF0000 occurrences:    12
orange #F26622 occurrences: 0

✓ dynamic palette loading proven
```

Zéro occurrence de l'ancien orange. La palette suit le theme. **Source de vérité = theme XML, prouvé.**

### 4.4 Robustesse — 6 cas de theme cassé

Tous lèvent une `BrandError` avec un message utile, jamais un `KeyError` / `AttributeError` opaque :

| Cas | Message |
|---|---|
| Fichier inexistant | `Template not found: /tmp/nonexistent.pptx` |
| Pas un ZIP | `/tmp/notazip.pptx is not a valid .pptx (ZIP error: File is not a zip file)` |
| `theme1.xml` absent du zip | `'ppt/theme/theme1.xml' is missing inside /tmp/no_theme1.pptx` |
| XML mal formé | `'ppt/theme/theme1.xml' in /tmp/bad_xml.pptx is not well-formed XML: unbound prefix: line 1, column 0` |
| `<a:accent1>` manquant | `Theme slot <a:accent1> is missing in 'ppt/theme/theme1.xml' of /tmp/no_accent1.pptx` |
| `<a:dk1>` sans srgb ni sysClr | `Theme slot <a:dk1> has neither <a:srgbClr@val> nor <a:sysClr@lastClr> in 'ppt/theme/theme1.xml' of /tmp/empty_dk1.pptx` |

---

## 5. Bugs détectés au passage (non corrigés — hors scope)

Aucun bug latent détecté pendant le refactor. Le code refactor s'est compilé / exécuté du premier coup pour les 4 fixtures de roadmap + golden + funnel.

---

## 6. Livrables

| Livrable | Chemin |
|---|---|
| Nouveau module | [`aosis-deck-builder/scripts/brand.py`](aosis-deck-builder/scripts/brand.py) |
| Refactor | [`aosis-deck-builder/scripts/build_deck.py`](aosis-deck-builder/scripts/build_deck.py) (constantes lignes 33-39 supprimées ; 6 imports inchangés ; 1 import `from brand import …` ajouté ; ~120 références remplacées par BRAND.*) |
| Rapport | [`chantier3_report.md`](chantier3_report.md) |
| CHANGELOG | [`CHANGELOG.md`](CHANGELOG.md) — entrée Chantier 3 ajoutée |

Aucun fichier de référence, template, ou SKILL.md modifié. Périmètre strictement respecté.
