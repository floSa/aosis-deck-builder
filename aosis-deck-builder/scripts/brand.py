"""brand.py — AOSIS palette read dynamically from the template's theme XML.

The theme XML inside `assets/AOSIS_template.pptx` is the single source of truth
for brand colours. To change the charte, edit `ppt/theme/theme1.xml` of the
template — never hardcode a hex value in any Python script.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

from pptx.dml.color import RGBColor


_NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
_THEME_PART = "ppt/theme/theme1.xml"


class BrandError(Exception):
    """Raised when a template's theme cannot be parsed or is missing required slots."""


@dataclass(frozen=True)
class BrandPalette:
    """AOSIS brand palette. Each field is an `RGBColor` (python-pptx native).

    Slot mapping to the OOXML theme:
      navy        ← dk1       (primary dark, page text on light, fills)
      light       ← lt1       (off-white background)
      gray        ← dk2       (secondary text)
      gray_light  ← lt2       (separators, soft fills)
      orange      ← accent1   (primary AOSIS accent)
      navy_alt    ← accent2   (navy variant; replaces ad-hoc NAVY_SOFT)
      accent3..6  ← accent3..6 (charts and decorative use)

    The fields `white` and `black` are universal constants, kept on the palette
    for ergonomic uniformity (so callers always say `BRAND.white` rather than
    mixing palette references with stray module constants).
    """

    navy: RGBColor
    light: RGBColor
    gray: RGBColor
    gray_light: RGBColor
    orange: RGBColor
    navy_alt: RGBColor
    accent3: RGBColor
    accent4: RGBColor
    accent5: RGBColor
    accent6: RGBColor
    white: RGBColor = RGBColor(0xFF, 0xFF, 0xFF)
    black: RGBColor = RGBColor(0x00, 0x00, 0x00)

    @classmethod
    def from_template(cls, template_path: "str | Path") -> "BrandPalette":
        """Read the theme XML from a .pptx and build a palette.

        Raises BrandError with a useful message if the template path is
        missing, not a valid pptx, or has a malformed/incomplete theme.
        """
        path = Path(template_path)
        if not path.exists():
            raise BrandError(f"Template not found: {path}")

        try:
            with zipfile.ZipFile(str(path)) as zf:
                try:
                    xml = zf.read(_THEME_PART)
                except KeyError as e:
                    raise BrandError(
                        f"'{_THEME_PART}' is missing inside {path}"
                    ) from e
        except zipfile.BadZipFile as e:
            raise BrandError(f"{path} is not a valid .pptx (ZIP error: {e})") from e

        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            raise BrandError(f"'{_THEME_PART}' in {path} is not well-formed XML: {e}") from e

        clr_scheme = root.find(f".//{_NS_A}clrScheme")
        if clr_scheme is None:
            raise BrandError(f"'{_THEME_PART}' in {path} has no <a:clrScheme>")

        def slot(name: str) -> RGBColor:
            elt = clr_scheme.find(f"{_NS_A}{name}")
            if elt is None:
                raise BrandError(
                    f"Theme slot <a:{name}> is missing in '{_THEME_PART}' of {path}"
                )
            srgb = elt.find(f"{_NS_A}srgbClr")
            if srgb is not None and srgb.get("val"):
                return RGBColor.from_string(srgb.get("val").upper())
            sysclr = elt.find(f"{_NS_A}sysClr")
            if sysclr is not None and sysclr.get("lastClr"):
                return RGBColor.from_string(sysclr.get("lastClr").upper())
            raise BrandError(
                f"Theme slot <a:{name}> has neither <a:srgbClr@val> nor "
                f"<a:sysClr@lastClr> in '{_THEME_PART}' of {path}"
            )

        return cls(
            navy=slot("dk1"),
            light=slot("lt1"),
            gray=slot("dk2"),
            gray_light=slot("lt2"),
            orange=slot("accent1"),
            navy_alt=slot("accent2"),
            accent3=slot("accent3"),
            accent4=slot("accent4"),
            accent5=slot("accent5"),
            accent6=slot("accent6"),
        )

    def hex(self, color: RGBColor) -> str:
        """Return a matplotlib-compatible hex string like '#14163C' from any
        palette colour. python-pptx's `str(RGBColor(...))` yields uppercase
        hex without `#`, so this is a thin convenience wrapper."""
        return f"#{color}"
