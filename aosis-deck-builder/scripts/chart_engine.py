"""chart_engine.py — Render matplotlib charts to PNG bytes for embedding
inside the `kpi_with_chart` template slide.

Public entry point: ``render_chart_to_png(chart_spec, width_emu, height_emu)``

Supported chart types (chart_spec['type']):
  - bar           : vertical bars, single series
  - barh          : horizontal bars, single series
  - bar_stacked   : vertical bars, multiple series stacked
  - line          : line chart, 1+ series
  - donut         : donut chart with optional center_text
  - pie           : pie chart
  - combo         : bars + line (line on secondary Y axis)
  - waterfall     : cumulative gain/loss bars

The brand palette is read at call time from ``brand.BRAND_OR_NONE`` set by
the caller, or defaults to a hard-coded fallback if no brand was injected.
This keeps chart_engine.py decoupled from build_deck.py's import chain.
"""
from __future__ import annotations

import io
from typing import Optional


EMU_PER_INCH = 914400


# ---------------------------------------------------------------------------
# Brand injection — callers pass a BrandPalette via set_brand() to keep
# this module decoupled from the build_deck import chain.
# ---------------------------------------------------------------------------
_BRAND = None


def set_brand(palette) -> None:
    """Inject the active BrandPalette so chart colors track the active theme."""
    global _BRAND
    _BRAND = palette


def _hex(color, fallback: str) -> str:
    """Resolve an RGBColor-like attribute on _BRAND, returning '#RRGGBB'.
    Fallback if no brand is set yet (covers stand-alone calls / early tests)."""
    if _BRAND is None:
        return fallback
    val = getattr(_BRAND, color, None)
    if val is None:
        return fallback
    # python-pptx RGBColor → repr like '14163C'; lowercase OK
    return f"#{val}"


def _palette():
    """Resolve the active palette as a dict of hex strings."""
    return {
        "navy":       _hex("navy",       "#14163C"),
        "navy_alt":   _hex("navy_alt",   "#1E2261"),
        "orange":     _hex("orange",     "#F26622"),
        "accent3":    _hex("accent3",    "#C2491A"),
        "accent4":    _hex("accent4",    "#F9B233"),
        "accent5":    _hex("accent5",    "#7CB342"),
        "accent6":    _hex("accent6",    "#E63946"),
        "gray":       _hex("gray",       "#4A4D6B"),
        "gray_light": _hex("gray_light", "#E8E9F2"),
        "light":      _hex("light",      "#FAFAF7"),
    }


def _series_colors(p):
    """Default cycling order for multi-series charts."""
    return [p["orange"], p["navy_alt"], p["accent4"], p["accent5"], p["accent3"]]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def render_chart_to_png(chart_spec: dict, width_emu: int, height_emu: int):
    """Render ``chart_spec`` and return ``(png_bytes, render_w_emu, render_h_emu)``.

    For most chart types ``(render_w_emu, render_h_emu) == (width_emu, height_emu)``.
    For ``pie`` and ``donut`` the figure is squared to
    ``min(width_emu, height_emu)`` to avoid horizontal stretching — the
    caller is expected to centre the image inside the original frame.

    Raises ImportError if matplotlib is unavailable.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import rcParams
    except ImportError as e:
        raise ImportError(
            "matplotlib is required to render charts in the kpi_with_chart "
            "layout. Install with: pip install matplotlib"
        ) from e

    p = _palette()

    # For circular charts, force a square figure to preserve aspect ratio
    kind_for_size = chart_spec.get("type", "bar")
    if kind_for_size in ("pie", "donut"):
        side = min(width_emu, height_emu)
        render_w_emu, render_h_emu = side, side
    else:
        render_w_emu, render_h_emu = width_emu, height_emu

    # Global rc — consulting look
    rcParams["font.family"] = "DejaVu Sans"
    rcParams["axes.spines.top"] = False
    rcParams["axes.spines.right"] = False
    rcParams["axes.edgecolor"] = p["gray"]
    rcParams["axes.labelcolor"] = p["navy"]
    rcParams["xtick.color"] = p["navy"]
    rcParams["ytick.color"] = p["navy"]
    rcParams["axes.titlecolor"] = p["navy"]
    rcParams["text.color"] = p["navy"]

    # Figure sized to render frame (possibly squared for pie/donut), 150 dpi
    w_in = max(1.0, render_w_emu / EMU_PER_INCH)
    h_in = max(1.0, render_h_emu / EMU_PER_INCH)
    fig, ax = plt.subplots(figsize=(w_in, h_in), dpi=150)

    kind = chart_spec.get("type", "bar")
    dispatch = {
        "bar":          _render_bar,
        "barh":         _render_barh,
        "bar_stacked":  _render_bar_stacked,
        "line":         _render_line,
        "donut":        _render_donut,
        "pie":          _render_pie,
        "combo":        _render_combo,
        "waterfall":    _render_waterfall,
    }
    renderer = dispatch.get(kind)
    if renderer is None:
        ax.text(0.5, 0.5, f"unsupported chart type {kind!r}",
                ha="center", va="center", transform=ax.transAxes,
                color=p["accent6"])
    else:
        renderer(ax, chart_spec, p, fig)

    # Optional axis labels (sober, lowercase)
    if chart_spec.get("y_label") and kind not in ("donut", "pie"):
        ax.set_ylabel(str(chart_spec["y_label"]).lower(), fontsize=9)
    if chart_spec.get("x_label") and kind not in ("donut", "pie"):
        ax.set_xlabel(str(chart_spec["x_label"]).lower(), fontsize=9)

    # Light horizontal gridline only (cartesian charts)
    if kind in ("bar", "barh", "bar_stacked", "line", "combo", "waterfall"):
        if kind == "barh":
            ax.xaxis.grid(True, color=p["gray_light"], linewidth=0.6)
            ax.yaxis.grid(False)
        else:
            ax.yaxis.grid(True, color=p["gray_light"], linewidth=0.6)
            ax.xaxis.grid(False)
        ax.set_axisbelow(True)

    fig.tight_layout(pad=0.4)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    png_bytes = buf.getvalue()

    # Chantier 18 — subtle gray border around the chart for a framed look.
    try:
        from PIL import Image, ImageDraw
        img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        # 2px gray-blue border (#E8E9F2)
        draw.rectangle([0, 0, w - 1, h - 1], outline=(232, 233, 242, 255), width=2)
        out = io.BytesIO()
        img.save(out, format="PNG")
        png_bytes = out.getvalue()
    except ImportError:
        pass  # Pillow not installed → keep chart without border

    return png_bytes, render_w_emu, render_h_emu


# ---------------------------------------------------------------------------
# Type-specific renderers
# ---------------------------------------------------------------------------
def _render_bar(ax, spec, p, fig):
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    bars = ax.bar(labels, values, width=0.6, color=p["orange"])
    _data_labels_above(ax, bars, values)
    _trim_yaxis_for_labels(ax, values)


def _render_barh(ax, spec, p, fig):
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    bars = ax.barh(labels, values, height=0.6, color=p["orange"])
    _data_labels_right(ax, bars, values)
    # Invert so first label is on top (consulting convention)
    ax.invert_yaxis()


def _render_bar_stacked(ax, spec, p, fig):
    import numpy as np
    labels = spec.get("labels", [])
    series = spec.get("series", [])
    colors = _series_colors(p)
    x = np.arange(len(labels))
    bottoms = np.zeros(len(labels))
    for i, s in enumerate(series):
        values = np.array(s.get("values", []))
        ax.bar(x, values, width=0.6, bottom=bottoms,
               color=colors[i % len(colors)],
               label=s.get("name", f"Série {i+1}"))
        bottoms += values
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    # Totals on top
    for xi, total in enumerate(bottoms):
        ax.text(xi, total, f" {total:g}", ha="center", va="bottom",
                fontsize=8, color=p["navy"])
    if series:
        ax.legend(frameon=False, loc="upper left", fontsize=8)


def _render_line(ax, spec, p, fig):
    labels = spec.get("labels", [])
    series = spec.get("series", [])
    colors = _series_colors(p)
    for i, s in enumerate(series):
        values = s.get("values", [])
        ax.plot(labels, values, marker="o", linewidth=2.2,
                color=colors[i % len(colors)],
                label=s.get("name", f"Série {i+1}"))
        # Data labels on each point
        for xi, yi in zip(range(len(labels)), values):
            ax.annotate(f"{yi:g}", (labels[xi], yi),
                        textcoords="offset points", xytext=(0, 6),
                        ha="center", fontsize=8, color=p["navy"])
    if len(series) > 1:
        ax.legend(frameon=False, loc="best", fontsize=8)


def _render_donut(ax, spec, p, fig):
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    center_text = spec.get("center_text")
    colors = _series_colors(p)[: len(values)] if values else _series_colors(p)
    wedges, texts, autotexts = ax.pie(
        values, labels=labels,
        colors=colors,
        autopct="%1.0f%%", startangle=90, pctdistance=0.75,
        wedgeprops={"linewidth": 2, "edgecolor": "white", "width": 0.5},
        textprops={"fontsize": 9, "color": p["navy"]},
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    if center_text:
        ax.text(0, 0, str(center_text), ha="center", va="center",
                fontsize=14, fontweight="bold", color=p["navy"])
    ax.set_aspect("equal")


def _render_pie(ax, spec, p, fig):
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    colors = _series_colors(p)[: len(values)] if values else _series_colors(p)
    wedges, texts, autotexts = ax.pie(
        values, labels=labels,
        colors=colors,
        autopct="%1.0f%%", startangle=90,
        wedgeprops={"linewidth": 1.5, "edgecolor": "white"},
        textprops={"fontsize": 9, "color": p["navy"]},
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
    ax.set_aspect("equal")


def _render_combo(ax, spec, p, fig):
    import numpy as np
    labels = spec.get("labels", [])
    bars_spec = spec.get("bars", {})
    line_spec = spec.get("line", {})
    bar_values = bars_spec.get("values", [])
    line_values = line_spec.get("values", [])

    x = np.arange(len(labels))
    bars = ax.bar(x, bar_values, width=0.6, color=p["orange"],
                  label=bars_spec.get("name", "Barres"))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    _data_labels_above(ax, bars, bar_values)

    ax2 = ax.twinx()
    ax2.plot(x, line_values, marker="o", linewidth=2.2, color=p["navy_alt"],
             label=line_spec.get("name", "Ligne"))
    ax2.tick_params(axis="y", colors=p["navy"])
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color(p["gray_light"])
    for xi, yi in zip(x, line_values):
        ax2.annotate(f"{yi:g}", (xi, yi), textcoords="offset points",
                     xytext=(0, 7), ha="center", fontsize=8,
                     color=p["navy_alt"], fontweight="bold")
    _trim_yaxis_for_labels(ax, bar_values)

    # Combined legend
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    if h1 or h2:
        ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=8)


def _render_waterfall(ax, spec, p, fig):
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    if not values:
        return

    # Walk: first and last bars are totals (absolute); intermediates are deltas
    # whose sum bridges values[0] → values[-1]. If the user passes raw bridge
    # deltas (i.e. values[0]=total, values[-1]=total, intermediates=deltas),
    # we accept that; otherwise we derive deltas.
    # Heuristic: if values[0] + sum(intermediates) == values[-1] → already
    # in delta form. Otherwise treat values as ordered cumulative levels and
    # derive deltas.
    n = len(values)
    if n >= 2 and abs((values[0] + sum(values[1:-1])) - values[-1]) < 1e-6:
        deltas = list(values)  # already total/delta/.../delta/total
    else:
        deltas = [values[0]]
        for i in range(1, n - 1):
            deltas.append(values[i] - values[i - 1])
        deltas.append(values[-1])

    running = 0
    for i, (label, dv) in enumerate(zip(labels, deltas)):
        is_total = (i == 0) or (i == n - 1)
        if is_total:
            color = p["navy_alt"]
            bottom = 0
            height = dv if i == 0 else values[-1]
            bar = ax.bar(i, height, width=0.6, color=color, bottom=bottom)
            top_y = height
        else:
            color = p["accent5"] if dv >= 0 else p["accent6"]
            if dv >= 0:
                bar = ax.bar(i, dv, width=0.6, bottom=running, color=color)
                top_y = running + dv
            else:
                bar = ax.bar(i, -dv, width=0.6, bottom=running + dv, color=color)
                top_y = running
            running += dv
        if i == 0:
            running = dv
        # Data label
        label_y = top_y
        ax.text(i, label_y, f" {dv:+g}" if not is_total else f" {dv:g}",
                ha="center", va="bottom", fontsize=8, color=p["navy"])
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _data_labels_above(ax, bars, values):
    p = _palette()
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f" {v:g}", ha="center", va="bottom", fontsize=8,
                color=p["navy"])


def _data_labels_right(ax, bars, values):
    p = _palette()
    for bar, v in zip(bars, values):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f" {v:g}", ha="left", va="center", fontsize=8,
                color=p["navy"])


def _trim_yaxis_for_labels(ax, values):
    """Add ~10% headroom so data labels above bars don't get clipped."""
    if not values:
        return
    try:
        mx = max(v for v in values if v is not None)
        mn = min(v for v in values if v is not None)
    except ValueError:
        return
    if mx == mn:
        return
    span = mx - mn
    ax.set_ylim(min(0, mn - span * 0.05), mx + span * 0.12)
