"""image_engine.py — fetch a stock photo for a `{{IMAGE}}` placeholder.

Provider order (Chantier 12 — migrated from Unsplash to Pexels):

1. **Pexels API** (https://api.pexels.com/) — if env var ``PEXELS_API_KEY``
   is set. Free dev tier = 200 req/hour, automated use explicitly allowed.
2. **Lorem Picsum** (https://picsum.photos/) — fallback when Pexels is
   unavailable. No API key, no keyword matching.

Chantier 22 — disk cache for Pexels downloads under
``~/.cache/aosis-deck-builder/pexels/``. Cache key = SHA-256 of
(keyword, orientation, target_dimensions). Each cached image gets a
companion ``.json`` with provenance (photo id, URL, photographer,
download timestamp). Cache MISS triggers a real fetch and populates
the cache; cache HIT returns the bytes immediately. Bypass with
``set_cache_enabled(False)`` or ``--no-cache-images`` in build_deck.

Public API
----------
- ``fetch_image_for_slide(keyword, width_emu, height_emu, timeout=8.0)
    -> bytes | None``
- ``extract_keyword_from_title(title, max_words=3) -> str``
- ``set_cache_enabled(enabled: bool)`` — toggle cache (default: enabled)
- ``clear_image_cache() -> int`` — wipe the cache dir, return count removed
- ``LAYOUT_DEFAULT_KEYWORDS`` — fallback keywords by layout name.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


EMU_PER_PX_96 = 9525  # 1 px @ 96 DPI = 9525 EMU


# ---------------------------------------------------------------------------
# Cache configuration (Chantier 22)
# ---------------------------------------------------------------------------
CACHE_DIR = Path(os.environ.get(
    'AOSIS_IMAGE_CACHE_DIR',
    str(Path.home() / '.cache' / 'aosis-deck-builder' / 'pexels')
))

_cache_enabled = True


def set_cache_enabled(enabled: bool) -> None:
    """Toggle the image cache. Disabling forces every call to hit the
    network (Pexels or Picsum)."""
    global _cache_enabled
    _cache_enabled = bool(enabled)


def _cache_key(keyword: str, orientation: str, w_px: int, h_px: int) -> str:
    """SHA-256 hash of (keyword, orientation, dimensions). Truncated to
    12 chars in the filename for readability."""
    raw = f"{keyword.strip().lower()}|{orientation}|{w_px}x{h_px}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _cache_paths(key: str) -> tuple[Path, Path]:
    short = key[:12]
    return (CACHE_DIR / f"{short}.jpg", CACHE_DIR / f"{short}.json")


def _cache_read(key: str) -> Optional[bytes]:
    img_path, _ = _cache_paths(key)
    if img_path.exists():
        try:
            return img_path.read_bytes()
        except OSError:
            return None
    return None


def _cache_write(key: str, image_bytes: bytes, metadata: dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        img_path, meta_path = _cache_paths(key)
        img_path.write_bytes(image_bytes)
        meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    except OSError as e:
        print(f"image cache: write failed ({e})", file=sys.stderr)


def clear_image_cache() -> int:
    """Remove every cached image and metadata file. Returns the count
    of files removed."""
    if not CACHE_DIR.exists():
        return 0
    removed = 0
    for p in CACHE_DIR.iterdir():
        if p.is_file():
            try:
                p.unlink()
                removed += 1
            except OSError:
                pass
    return removed


# ---------------------------------------------------------------------------
# Keyword extraction
# ---------------------------------------------------------------------------
_STOP_WORDS = {
    # French
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'd', 'à', 'au', 'aux',
    'et', 'ou', 'pour', 'par', 'sur', 'avec', 'sans', 'dans', 'en', 'vers',
    'notre', 'votre', 'nos', 'vos', 'leur', 'leurs',
    'ce', 'cet', 'cette', 'ces', 'que', 'qui', 'quel', 'quels', 'quelle',
    'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    'ne', 'pas', 'plus', 'si', 'oui', 'non',
    # English
    'the', 'a', 'an', 'of', 'to', 'and', 'or', 'for', 'on', 'with',
    'in', 'by', 'is', 'are', 'this', 'that', 'these', 'those',
    'we', 'you', 'they', 'i', 'our', 'your', 'their',
    # Filler nouns
    'page', 'slide', 'section', 'partie', 'chapter',
}


def extract_keyword_from_title(title: Optional[str], max_words: int = 3) -> str:
    """Pick up to ``max_words`` significant words from a title.
    Strips stop words and tokens shorter than 3 chars."""
    if not title:
        return ''
    tokens = re.findall(r"[A-Za-zÀ-ÿ]+", title.lower())
    significant = [t for t in tokens if t not in _STOP_WORDS and len(t) >= 3]
    return ' '.join(significant[:max_words])


LAYOUT_DEFAULT_KEYWORDS = {
    'cover':              'business technology',
    'agenda_diagonal':    'planning strategy',
    'section_diagonal':   'abstract corporate',
    'closing_diagonal':   'team success',
    'final_branding':     'team success',
    'canvas_blank':       'corporate',
    'quote_callout':      'leadership office',
}


# ---------------------------------------------------------------------------
# Public fetch
# ---------------------------------------------------------------------------
def fetch_image_for_slide(keyword: str, width_emu: int, height_emu: int,
                          timeout: float = 8.0) -> Optional[bytes]:
    """Fetch a stock image. Returns image bytes (JPEG/PNG) or None on failure."""
    width_px = max(400, int(width_emu / EMU_PER_PX_96))
    height_px = max(300, int(height_emu / EMU_PER_PX_96))
    keyword = (keyword or '').strip()
    orientation = 'landscape' if width_px >= height_px else 'portrait'

    # Cache lookup (Chantier 22) — only for Pexels (Picsum is already
    # deterministic by seed and effectively free)
    pexels_key = os.environ.get('PEXELS_API_KEY')
    if pexels_key and _cache_enabled:
        key = _cache_key(keyword, orientation, width_px, height_px)
        cached = _cache_read(key)
        if cached is not None:
            print(f"image cache HIT: {keyword!r} ({orientation}, "
                  f"{width_px}×{height_px})", file=sys.stderr)
            return cached

    # Strategy 1: Pexels API (keyword-relevant photos)
    if pexels_key:
        try:
            result = _fetch_pexels(keyword, width_px, height_px, pexels_key,
                                    orientation, timeout)
            image_bytes, metadata = result
            if _cache_enabled:
                key = _cache_key(keyword, orientation, width_px, height_px)
                _cache_write(key, image_bytes, metadata)
                print(f"image cache MISS → fetched & cached: {keyword!r} "
                      f"({orientation}, {width_px}×{height_px})",
                      file=sys.stderr)
            return image_bytes
        except Exception as e:
            print(f"image: Pexels failed ({e}), falling back to Picsum",
                  file=sys.stderr)

    # Strategy 2: Lorem Picsum (always available, deterministic by seed)
    try:
        return _fetch_picsum(keyword, width_px, height_px, timeout)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------
def _fetch_pexels(keyword: str, w: int, h: int, api_key: str,
                  orientation: str = 'landscape',
                  timeout: float = 5.0) -> tuple[bytes, dict]:
    """Pexels API — keyword search, return image bytes + provenance metadata."""
    q = urllib.parse.quote(keyword or 'corporate business')
    api_url = (
        f"https://api.pexels.com/v1/search"
        f"?query={q}&per_page=1&orientation={orientation}"
    )
    req = urllib.request.Request(api_url, headers={
        'Authorization': api_key,
        'User-Agent': 'aosis-deck-builder/1.0',
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode('utf-8'))
    photos = payload.get('photos', [])
    if not photos:
        raise ValueError(f"Pexels returned no photos for query {keyword!r}")
    photo = photos[0]
    photo_url = (
        photo.get('src', {}).get('large')
        or photo.get('src', {}).get('large2x')
        or photo.get('src', {}).get('medium')
    )
    if not photo_url:
        raise ValueError("Pexels photo has no usable src URL")
    req2 = urllib.request.Request(photo_url, headers={
        'User-Agent': 'aosis-deck-builder/1.0',
    })
    with urllib.request.urlopen(req2, timeout=timeout) as r2:
        image_bytes = r2.read()

    metadata = {
        'keyword': keyword,
        'orientation': orientation,
        'pexels_photo_id': str(photo.get('id', '')),
        'pexels_url': photo.get('url', ''),
        'photographer': photo.get('photographer', ''),
        'photographer_url': photo.get('photographer_url', ''),
        'src_url': photo_url,
        'target_px': f"{w}x{h}",
        'downloaded_at': datetime.now(timezone.utc).strftime(
            '%Y-%m-%dT%H:%M:%SZ'),
    }
    return image_bytes, metadata


def _fetch_picsum(keyword: str, w: int, h: int, timeout: float) -> bytes:
    """Lorem Picsum fallback — seed = keyword (deterministic). One retry."""
    # Strip non-ASCII so urllib doesn't choke on accents
    ascii_kw = unicodedata.normalize('NFD', keyword or '').encode(
        'ascii', 'ignore').decode('ascii')
    seed = re.sub(r'[^a-z0-9]+', '-', ascii_kw.lower()).strip('-') or 'corporate'
    url = f"https://picsum.photos/seed/{seed}/{w}/{h}"
    headers = {'User-Agent': 'aosis-deck-builder/1.0'}
    last_err = None
    for _ in range(2):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
    raise last_err
