# Chantier 12 — Pexels API + découpe diagonale des images

**Date** : 2026-05-20
**Périmètre** : Remplacer Unsplash (interdit en automatisation par CGU) par Pexels API + faire respecter la découpe diagonale du design sur les slides `cover`/`agenda_diagonal`/`section_diagonal`/`closing_diagonal`.

## TL;DR

| Fix | Statut |
|---|---|
| 1. Migration Unsplash → Pexels | ✅ |
| 2. Découpe diagonale via custGeom du layout | ✅ |

**Tests** : **46 passed, 1 skipped** (5 nouveaux tests).
**Deck régénéré** : `examples/test_migration_cloud.pptx` (855 KB).

## 1. Inspection des 4 slides diagonales

### 1.1 — `cover` (layout = `Cover`)

| Shape | Geom | Pos (in.) | Fill | Rôle |
|---|---|---|---|---|
| `{{SUBTITLE}}` | rect | L=-0.01, T=3.84, 10.01×0.37 | — | sous-titre |
| `{{REF}}` | **parallelogram** | L=7.96, T=0.28, 2.09×0.97 | scheme:accent1 (orange) | pastille date |
| `{{TITLE}}` | rect | L=1.28, T=1.95, 7.44×1.31 | — | titre principal |

**Pas de `{{IMAGE}}` placeholder dans la cover actuelle**. Le `Cover` layout n'a pas non plus de PLACEHOLDER `Image` avec custGeom. La diagonale, si elle existe visuellement, vient probablement du master.

→ Conclusion : la découpe diagonale ne s'applique pas réellement à `cover` aujourd'hui car il n'y a pas de photo à découper. Le nom est gardé dans `SLIDES_WITH_DIAGONAL_OVERLAY` au cas où l'utilisateur ajoute un `{{IMAGE}}` plus tard dans le template.

### 1.2 — `agenda_diagonal`, `section_diagonal`, `closing_diagonal` (layout = `Sommaire_Section_Contact`)

Tous les trois partagent le même layout, donc le même découpage.

**Côté slide content** :
| cSld.name | `{{IMAGE}}` Pos | Taille |
|---|---|---|
| `agenda_diagonal` | L=4.21, T=-0.01 | 5.80×5.63" |
| `section_diagonal` | L=4.21, T=-0.01 | 5.80×5.63" |
| `closing_diagonal` | L=4.21, T=-0.01 | 5.80×5.63" |

Identiques. Le `{{IMAGE}}` est un grand rectangle qui couvre la moitié droite + une mince marge basse.

**Côté slide layout `Sommaire_Section_Contact`** :
| Shape | Geom | Pos (in.) | Rôle |
|---|---|---|---|
| `Logo` (Picture) | rect | L=4.34, T=4.96, 1.32×0.65" | logo AOSIS bottom-right |
| `Image` (PLACEHOLDER) | **custGeom** | L=4.21, T=-0.01, 5.80×5.63" | **placeholder Image avec découpe diagonale** |
| `Rectangle 5` | rect | L=9.33, T=5.18, 0.67×0.34" | déco accent1 bottom-right |
| (TextBox déco) | rect | L=9.33, T=5.19, 0.61×0.30" | — |

**Le `Image` placeholder du layout porte un `<a:custGeom>`** — c'est elle qui définit la forme diagonale. Extrait du path actif (dernier dans `gdLst`) :
- Point 0 : (898 072, 0) — angle haut, à 17 % depuis la gauche
- Point 1 : (5 282 973, 775 608) — angle haut-droit, descendu de 15 %
- Point 2 : (5 291 137, 5 152 118) — coin bas-droit
- Point 3 : (0, 5 152 118) — coin bas-gauche
- Point 4 : retour au point 0

C'est un quadrilatère où le coin haut-gauche est coupé par une diagonale qui descend de gauche à droite (de y=0 à y=775 608 EMU = ~15 % de la hauteur).

## 2. Approche retenue — copier custGeom sur la photo insérée

Plutôt que d'overlayer une forme par-dessus la photo (complexe à positionner et z-ordre), nous **remplaçons le `<a:prstGeom prst="rect"/>` de la photo par le `<a:custGeom>` du layout**. La photo prend ainsi la forme exacte du placeholder Image du layout.

Avantages :
- Implémentation simple (3 lignes de XML manipulation)
- Rendu identique à ce que PowerPoint affiche pour le placeholder du layout
- Aucune modif du template AOSIS_template.pptx requise
- Aucun problème de z-ordre

```python
SLIDES_WITH_DIAGONAL_OVERLAY = {
    'cover', 'agenda_diagonal', 'section_diagonal', 'closing_diagonal'
}

def _apply_layout_custgeom_to_picture(slide, pic_shape):
    """Copy the layout placeholder's custGeom onto the picture's spPr."""
    layout = slide.slide_layout
    src_custgeom = None
    for lsh in layout.shapes:
        spPr = lsh._element.find(qn('p:spPr'))
        cust = spPr.find(qn('a:custGeom')) if spPr is not None else None
        if cust is not None:
            src_custgeom = cust
            break
    if src_custgeom is None:
        return
    pic_spPr = pic_shape._element.find(qn('p:spPr'))
    for prst in pic_spPr.findall(qn('a:prstGeom')):
        pic_spPr.remove(prst)
    pic_spPr.append(deepcopy(src_custgeom))
```

Appelé après `add_picture` dans `_process_image_placeholders` quand le `cSld.name` est dans `SLIDES_WITH_DIAGONAL_OVERLAY`.

## 3. Migration Unsplash → Pexels

### Pourquoi

Les CGU Unsplash interdisent explicitement le téléchargement automatisé (cf. §2.3 de l'Unsplash API Terms). Pexels au contraire **autorise explicitement l'automated downloads** via leur API (cf. Pexels API Terms §5).

### Implémentation

```python
def _fetch_pexels(keyword, w, h, api_key, timeout=5.0):
    q = urllib.parse.quote(keyword or 'corporate business')
    api_url = f"https://api.pexels.com/v1/search?query={q}&per_page=1&orientation=landscape"
    req = urllib.request.Request(api_url, headers={
        'Authorization': api_key,
        'User-Agent': 'aosis-deck-builder/1.0',
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode('utf-8'))
    photos = payload.get('photos', [])
    if not photos:
        raise ValueError(f"Pexels returned no photos for query {keyword!r}")
    photo_url = photos[0]['src'].get('large') or photos[0]['src'].get('large2x')
    req2 = urllib.request.Request(photo_url, ...)
    with urllib.request.urlopen(req2, timeout=timeout) as r2:
        return r2.read()
```

### Chaîne de providers (simplifiée)

```
1. PEXELS_API_KEY env var → Pexels API (keyword-relevant, free 200 req/h)
2. Lorem Picsum (no key, deterministic seed, no semantic match)
3. None → silent failure, slide renders without photo
```

Le code Unsplash (`_fetch_unsplash_api`, `_fetch_unsplash_source`) a été **retiré du module** — pas seulement désactivé, pour bien signaler l'incompatibilité ToS.

## 4. Photos téléchargées dans le deck régénéré

L'environnement bash de l'agent **ne voit pas `PEXELS_API_KEY`** (probablement exportée dans le shell utilisateur ou dans la config VSCode/extension mais pas propagée au subprocess via lequel j'invoque `build_deck.py`). Conséquence : la régénération est tombée sur **Lorem Picsum**.

Les 5 photos téléchargées (seeds dérivées du title via extract_keyword_from_title) :

| Slide | cSld | Keyword effectif | Provider effectif (cet run) | Geom appliquée |
|---:|---|---|---|---|
| 2 | agenda_diagonal | `sommaire` | Picsum seed=`sommaire` | **custGeom (diagonale)** ✓ |
| 3 | section_diagonal | `diagnostic actuel` | Picsum seed=`diagnostic-actuel` | custGeom ✓ |
| 9 | section_diagonal | `vision recommandation strat` | Picsum seed=`vision-recommandation-strategique` | custGeom ✓ |
| 14 | section_diagonal | `plan execution` | Picsum seed=`plan-execution` | custGeom ✓ |
| 20 | closing_diagonal | `merci` (puis fallback layout default `team success`) | Picsum seed=`team-success` | custGeom ✓ |

**Quand l'utilisateur run avec `PEXELS_API_KEY` exportée correctement** (`export PEXELS_API_KEY=...` avant `python build_deck.py …`), il obtiendra des photos sémantiquement pertinentes au lieu de photos aléatoires. Tests automatiques `test_pexels_api_used_when_key_present` valident le routage.

### Vérification structurale (sans rendu visuel)

Inspection des PICTURE générés :

```
slide  2 (agenda_diagonal): picture 'Picture 31'  geom=DIAG (custGeom)
slide  3 (section_diagonal): picture 'Picture 31'  geom=DIAG
slide  6 (kpi_with_chart): picture 'Picture 17'  geom=prst:rect   ← chart, hors-overlay
slide  9 (section_diagonal): picture 'Picture 31'  geom=DIAG
slide 11 (framework_3cards): picture 'Picture 18'  geom=prst:rect ← icônes, hors-overlay
slide 11 (framework_3cards): picture 'Picture 19'  geom=prst:rect
slide 11 (framework_3cards): picture 'Picture 20'  geom=prst:rect
slide 14 (section_diagonal): picture 'Picture 31'  geom=DIAG
slide 20 (closing_diagonal): picture 'Picture 17'  geom=DIAG
```

Les 5 photos auto-fetched des diagonales **portent toutes le custGeom**. Les pictures techniques (chart matplotlib slide 6, icônes Iconify slide 11) gardent leur `prst:rect` natif. ✓

## 5. Tests

```
======================== 46 passed, 1 skipped in 4.36s =========================
```

5 nouveaux tests :
| Test | Vérifie |
|---|---|
| `test_pexels_api_used_when_key_present` | mock fetch_pexels, vérifie keyword + Authorization header |
| `test_image_engine_falls_back_to_picsum_on_pexels_error` | mock pexels=fail, picsum=ok → result = bytes Picsum |
| `test_image_engine_handles_total_failure` | mock pexels + picsum = fail → None, build deck ne crash pas |
| `test_diagonal_overlay_applied_on_agenda` | agenda_diagonal → picture porte custGeom, prstGeom absent |
| `test_no_diagonal_overlay_on_canvas_blank` | invariant : canvas_blank ∉ SLIDES_WITH_DIAGONAL_OVERLAY |

Anciens 41 tests : ✓ aucune régression.

## 6. Défauts résiduels

1. **Pertinence des photos sans Pexels** : si l'utilisateur lance sans `PEXELS_API_KEY`, les photos sont Picsum (aléatoires). C'est moins bien qu'avant l'API key mais identique au comportement Chantier 11. Pour de vraies photos pertinentes : exporter la clé.
2. **Cover sans `{{IMAGE}}`** : le layout `Cover` n'a actuellement pas d'image placeholder, donc le membre `'cover'` dans `SLIDES_WITH_DIAGONAL_OVERLAY` est inert. Cohérent si l'utilisateur ajoute un `{{IMAGE}}` plus tard dans le template — la machinerie est prête.
3. **Rendu visuel non vérifié par l'agent** : pas d'accès à PowerPoint / soffice → impossibilité de prendre des captures pour confirmer la découpe à l'œil. Tests structurels XML confirment que le custGeom est bien appliqué, à valider visuellement côté utilisateur.
4. **Latence de génération** : ~4.7 s avec auto-images vs 0.93 s sans (Picsum × 5 + 1 Pexels échec = 5 round-trips réseau). Optimisation possible : cache disque + parallélisme (candidat Chantier 13).

## 7. Suggestion de modification template (non appliquée)

Aucune modification de template n'est requise par ce chantier — l'approche custGeom-from-layout exploite ce qui existe déjà.

**Suggestion optionnelle** pour l'utilisateur : si la diagonale ne rend pas comme attendu visuellement, ajuster le `<a:custGeom>` dans le placeholder `Image` du slide layout `Sommaire_Section_Contact` directement dans PowerPoint (Edit Slide Master → Edit Layout → sélectionner la zone image → Edit Points). Le moteur reprendra automatiquement la nouvelle découpe à la prochaine génération.

## 8. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/image_engine.py` | **réécrit** (Pexels primary, Picsum fallback, Unsplash retiré) |
| `aosis-deck-builder/scripts/template_engine.py` | **modifié** (+ `SLIDES_WITH_DIAGONAL_OVERLAY`, + `_apply_layout_custgeom_to_picture`, refactor `_process_image_placeholders`) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (3 nouveaux tests Pexels, 2 nouveaux tests diagonale, 1 ancien test Unsplash supprimé) |
| `aosis-deck-builder/references/json-schema.md` | **modifié** (section "Images automatiques" + sous-section "Découpe diagonale automatique") |
| `aosis-deck-builder/SKILL.md` | **modifié** (mention Pexels + découpe diagonale) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 12) |
| `chantier12_report.md` | **créé** (ce fichier) |
| `examples/test_migration_cloud.pptx` | **régénéré** (5 photos avec custGeom) |

`AOSIS_template.pptx` **non modifié** comme demandé.

---

**Statut final** : ✅ Chantier 12 **livré sans régression**. 46/47 tests verts (1 skip soffice pré-existant), 2 fixes appliqués, deck régénéré avec custGeom diagonale validée structurellement.
