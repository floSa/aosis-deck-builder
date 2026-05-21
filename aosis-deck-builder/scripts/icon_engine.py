"""icon_engine.py — Fetch icons from Iconify and convert to PNG.

Used by `template_engine` to fill `{{ITEM_ICON}}` placeholders with brand-
coloured icons inside layouts like `framework_3cards`.

Public API
----------
- ``fetch_icon_png(name, size_px=200, color=None, timeout=5.0) -> bytes``
  Fetch an icon SVG from Iconify and rasterize it to PNG.

Lazy import: cairosvg is only imported on first call so the rest of the
skill stays usable without it (icons gracefully degrade to "no image" then).

Notes
-----
Iconify (https://iconify.design/) exposes 200 000+ icon sets via a simple
HTTP API. Identifiers follow ``<prefix>:<name>``, e.g. ``mdi:cloud``,
``material-symbols:rocket-launch``, ``carbon:security``. No API key needed.
"""
from __future__ import annotations

import urllib.error
import urllib.request
from typing import Optional


ICONIFY_BASE = "https://api.iconify.design"


class IconNotFound(Exception):
    """Raised when an icon cannot be fetched or rendered."""


def fetch_icon_svg(name: str, color: Optional[str] = None,
                   timeout: float = 5.0) -> bytes:
    """Fetch the raw SVG bytes from Iconify. Raises IconNotFound on any error.

    Args:
        name: ``<prefix>:<icon>`` identifier (e.g. ``"mdi:cloud"``)
        color: optional hex (with or without leading ``#``); when given, the
            icon's ``currentColor`` is forced to this value via the Iconify
            ``color`` query parameter.
        timeout: HTTP timeout in seconds.
    """
    if ':' not in name:
        raise IconNotFound(f"Iconify name must be 'prefix:icon', got {name!r}")
    path = name.replace(':', '/')
    url = f"{ICONIFY_BASE}/{path}.svg"
    if color:
        hex_value = color.lstrip('#')
        url += f"?color=%23{hex_value}"
    req = urllib.request.Request(url, headers={'User-Agent': 'aosis-deck-builder/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if getattr(r, 'status', 200) != 200:
                raise IconNotFound(f"HTTP {r.status} for {name}")
            return r.read()
    except urllib.error.URLError as e:
        raise IconNotFound(f"Network error fetching {name}: {e}") from e


def fetch_icon_png(name: str, size_px: int = 200,
                   color: Optional[str] = None,
                   timeout: float = 5.0) -> bytes:
    """Fetch an Iconify icon and rasterize it to PNG at ``size_px`` square.

    Raises:
        IconNotFound: network failure, 404, or invalid identifier.
        ImportError: ``cairosvg`` is not installed.
    """
    try:
        import cairosvg
    except ImportError as e:
        raise ImportError(
            "cairosvg is required to render icons. Install with: "
            "pip install cairosvg"
        ) from e

    svg_bytes = fetch_icon_svg(name, color=color, timeout=timeout)
    return cairosvg.svg2png(
        bytestring=svg_bytes,
        output_width=size_px,
        output_height=size_px,
    )
