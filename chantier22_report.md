# Chantier 22 — Cache disque pour les images Pexels

**Date** : 2026-05-21
**Périmètre** : Mise en cache local des images Pexels téléchargées. Re-générer un deck devient quasi-instantané côté images.

## TL;DR

- ✅ Cache sous `~/.cache/aosis-deck-builder/pexels/`, clé = SHA-256 de `(keyword, orientation, dimensions)`
- ✅ Métadonnées JSON co-stockées (provenance Pexels)
- ✅ Logs `image cache HIT/MISS` en stderr
- ✅ Nouveaux flags : `--no-cache-images`, `--clear-image-cache`
- ✅ 80 passed, 1 skipped (+3 tests)
- ✅ **-40 % de temps** sur régénération avec cache chaud

## 1. Temps observés

Deck `examples/test_migration_cloud.pptx` (5 images Pexels, layouts cover / agenda / section_diagonal × 2 / closing) :

```
=== RUN 1 (cold cache : 5 MISS + downloads) ===
image cache MISS → fetched & cached: 'business meeting overview' (landscape, 556×540)
image cache MISS → fetched & cached: 'data center server room' (landscape, 556×540)
image cache MISS → fetched & cached: 'business strategy whiteboard' (landscape, 556×540)
image cache MISS → fetched & cached: 'project timeline planning' (landscape, 556×540)
image cache MISS → fetched & cached: 'business handshake success' (landscape, 556×540)
real    0m1.682s

=== RUN 2 (warm cache : 5 HIT depuis disque) ===
image cache HIT: 'business meeting overview' (landscape, 556×540)
image cache HIT: 'data center server room' (landscape, 556×540)
image cache HIT: 'business strategy whiteboard' (landscape, 556×540)
image cache HIT: 'project timeline planning' (landscape, 556×540)
image cache HIT: 'business handshake success' (landscape, 556×540)
real    0m1.012s
```

| Scénario | Temps | Réseau | Quota Pexels consommé |
|---|---:|---|---:|
| Cold cache (1ʳᵉ génération) | **1.68 s** | 5 GET API + 5 GET image | 5 / 200 |
| Warm cache (régénération) | **1.01 s** | 0 | 0 / 200 |
| Gain | **−40 %** | total | total |

Pour un deck avec 10-15 images, le gain absolu serait plus important (Pexels API latence variable 200-500 ms par requête + ~50-150 KB par image).

## 2. Structure du cache sur disque

```
~/.cache/aosis-deck-builder/pexels/
├── 05a3dfae5bad.jpg     (65 KB)
├── 05a3dfae5bad.json    (514 B)
├── 1d2a77be4304.jpg     (58 KB)
├── 1d2a77be4304.json    (487 B)
├── 64ddc1c9282f.jpg     (33 KB)
├── 64ddc1c9282f.json    (504 B)
├── d5fe7b04d2d7.jpg     (36 KB)
├── d5fe7b04d2d7.json    (467 B)
├── e5c0d86895aa.jpg     (119 KB)
└── e5c0d86895aa.json    (475 B)
```

Format du fichier `.json` (provenance + traçabilité) :

```json
{
  "keyword": "business strategy whiteboard",
  "orientation": "landscape",
  "pexels_photo_id": "5439481",
  "pexels_url": "https://www.pexels.com/photo/.../5439481/",
  "photographer": "Tima Miroshnichenko",
  "photographer_url": "https://www.pexels.com/@tima-miroshnichenko",
  "src_url": "https://images.pexels.com/photos/5439481/pexels-photo-5439481.jpeg?...",
  "target_px": "556x540",
  "downloaded_at": "2026-05-21T13:16:00Z"
}
```

Permet de :
- Tracer le photographer credit (utile pour mentions légales)
- Retrouver le permalink Pexels (re-télécharger manuellement si besoin)
- Vérifier l'âge d'une image cachée

## 3. Clé de cache et collisions

```python
raw = f"{keyword.strip().lower()}|{orientation}|{w_px}x{h_px}"
key = hashlib.sha256(raw.encode('utf-8')).hexdigest()  # 64 chars
filename = f"{key[:12]}.jpg"                            # 12 chars = ~10²² combinaisons
```

12 chars hex = 48 bits = 2.8×10¹⁴ combinaisons → collision improbable avant 16M images cachées (birthday paradox). Largement suffisant pour un cache local. La normalisation `keyword.strip().lower()` garantit `"Data Center"` et `"data center"` partagent la même entrée.

## 4. Picsum NON caché — intentionnel

Lorem Picsum (fallback sans clé Pexels) n'est **pas** mis en cache car :
- Déjà déterministe par seed (`https://picsum.photos/seed/<kw>/<w>/<h>` → toujours la même image)
- Pas de quota
- Latence faible (~200 ms)

Ajouter le cache à Picsum aurait dupliqué la logique sans bénéfice net. Implémenter si un besoin offline se présente.

## 5. Politique d'expiration — suggestion pour V2

V1 (livré) : pas d'expiration auto. Cache croît indéfiniment, utilisateur vide manuellement.

**Pour V2**, suggestions par ordre de complexité :

1. **TTL fixe** (e.g. 30 jours) : à chaque HIT, vérifier `downloaded_at` ; si > TTL, ré-fetch et écraser. Simple, bornées.
2. **LRU avec taille max** (e.g. 500 MB) : ajouter un timestamp `last_accessed` aux meta, purge LRU quand taille dépasse seuil. Plus complexe, garantit borne disque.
3. **Versioning Pexels** : Pexels expose un `updated_at` par photo via API ; au HIT, comparer avec `downloaded_at` cache et refresh si plus récent. Latence d'1 appel HEAD au cache HIT — défait partiellement l'intérêt.

Recommandation V2 : TTL 30 jours, suffisant pour la plupart des workflows. À discuter.

## 6. Tests

```
80 passed, 1 skipped in 4.48s
```

| Test | Vérifie |
|---|---|
| `test_image_cache_hit_avoids_network_call` | 2ᵉ appel avec mêmes args HIT, `_fetch_pexels` appelé 1× pas 2× |
| `test_image_cache_miss_calls_pexels` | Cache vide → Pexels appelé, fichier créé sur disque |
| `test_image_cache_can_be_cleared` | `clear_image_cache()` retire tous les fichiers du dir |

Test existant `test_pexels_api_used_when_key_present` adapté :
- Nouvelle signature `_fetch_pexels(..., orientation=...)` (+1 paramètre)
- Mock retourne `(bytes, metadata)` au lieu de `bytes` seul
- Cache désactivé en début de test pour ne pas court-circuiter le mock

Override d'env `AOSIS_IMAGE_CACHE_DIR` (utilisé par tests via `monkeypatch.setattr(image_engine, "CACHE_DIR", tmp_path / "cache")`) garantit isolement test.

## 7. Livrables

| Fichier | Statut |
|---|---|
| `aosis-deck-builder/scripts/image_engine.before-chantier22.py` | **backup** |
| `aosis-deck-builder/scripts/image_engine.py` | **modifié** (+cache, +metadata, +set/clear helpers, nouvelle signature `_fetch_pexels`) |
| `aosis-deck-builder/scripts/build_deck.py` | **modifié** (+`--no-cache-images`, +`--clear-image-cache`) |
| `aosis-deck-builder/tests/test_smoke.py` | **modifié** (+3 tests, +1 adapté) |
| `aosis-deck-builder/SKILL.md` | **modifié** (section image cache + nouveaux flags) |
| `CHANGELOG.md` | **modifié** (entrée Chantier 22) |
| `chantier22_report.md` | **créé** (ce fichier) |
| `aosis-deck-builder.skill` | **regénéré** |

Aucune modification de `template_engine.py` ou `chart_engine.py`. Pas de migration des images existantes (le cache se construit au fur et à mesure des prochains builds).

---

**Statut final** : ✅ Chantier 22 **livré sans régression**. 80/81 tests verts. Régénération de deck ~40 % plus rapide sur warm cache, zéro consommation du quota Pexels API.
