"""image_engine.py — fetch a stock photo for a `{{IMAGE}}` placeholder.

Provider order (Chantier 12 — migrated from Unsplash to Pexels):

1. **Pexels API** (https://api.pexels.com/) — if env var ``PEXELS_API_KEY``
   is set. Free dev tier = 200 req/hour, automated use explicitly allowed
   (unlike Unsplash whose ToS forbid automated downloads). Returns
   keyword-relevant photos.
2. **Lorem Picsum** (https://picsum.photos/) — fallback when Pexels is
   unavailable. No API key, no keyword matching (random photo seeded by
   the keyword string), but always reachable.

Public API
----------
- ``fetch_image_for_slide(keyword, width_emu, height_emu, timeout=8.0)
    -> bytes | None``
- ``extract_keyword_from_title(title, max_words=3) -> str``
- ``LAYOUT_DEFAULT_KEYWORDS`` — fallback keywords by layout name.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


EMU_PER_PX_96 = 9525  # 1 px @ 96 DPI = 9525 EMU


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

    # Strategy 1: Pexels API (keyword-relevant photos)
    pexels_key = os.environ.get('PEXELS_API_KEY')
    if pexels_key:
        try:
            return _fetch_pexels(keyword, width_px, height_px, pexels_key, timeout)
        except Exception:
            pass

    # Strategy 2: Lorem Picsum (always available, deterministic by seed)
    try:
        return _fetch_picsum(keyword, width_px, height_px, timeout)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------
def _fetch_pexels(keyword: str, w: int, h: int, api_key: str,
                  timeout: float = 5.0) -> bytes:
    """Pexels API — keyword search, return the first landscape result.

    Pexels' ToS explicitly allow automated downloads via the API (unlike
    Unsplash). Free tier: 200 req/hour, 20 000/month.
    """
    q = urllib.parse.quote(keyword or 'corporate business')
    api_url = (
        f"https://api.pexels.com/v1/search"
        f"?query={q}&per_page=1&orientation=landscape"
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
    photo_url = (
        photos[0].get('src', {}).get('large')
        or photos[0].get('src', {}).get('large2x')
        or photos[0].get('src', {}).get('medium')
    )
    if not photo_url:
        raise ValueError("Pexels photo has no usable src URL")
    req2 = urllib.request.Request(photo_url, headers={
        'User-Agent': 'aosis-deck-builder/1.0',
    })
    with urllib.request.urlopen(req2, timeout=timeout) as r2:
        return r2.read()


def _fetch_picsum(keyword: str, w: int, h: int, timeout: float) -> bytes:
    """Lorem Picsum fallback — seed = keyword (deterministic). One retry."""
    # Strip non-ASCII so urllib doesn't choke on accents
    ascii_kw = unicodedata.normalize('NFD', keyword or '').encode('ascii', 'ignore').decode('ascii')
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
