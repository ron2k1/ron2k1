"""Draw the six book spines in assets/shelf/ for the profile README.

Each spine is its own SVG so the README can wrap each one in its own link. Every file is 171 px tall
and carries its slice of the plank, so the six images stand on one shared baseline and the plank runs
under the whole row. At 1x, 2x and 3x it joins cleanly. At fractional pixel ratios the browser can
leave a one-device-pixel hairline where two images meet, which no markup can prevent while each spine
is its own link. The letters are Inter Bold outlined to paths, so the files look the same on any
machine and carry no fonts, styles, or external references.

Run from the repo root: python scripts/shelf.py
"""
from __future__ import annotations

import functools
import pathlib
from typing import NamedTuple

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts" / "Inter-Bold-caps.ttf"
OUT = ROOT / "assets" / "shelf"

CANVAS_H, BASE = 171, 168      # every file is this tall and every spine stands on y = BASE
MARGIN = 1                     # each file pads its spine 1 px per side, so neighbours sit 2 px apart
SIZE, PITCH = 11, 12           # letter size and baseline step in px
FIRST_BASELINE = 28            # from the spine's top edge
PLANK = "#8c959f"              # 3.0:1 on GitHub's light background, 6.2:1 on its dark one


class Spine(NamedTuple):
    key: str
    label: str
    width: int
    fill: str
    stroke: str
    ink: str
    repo: str


# Greens are GitHub's light-mode contribution levels. The purple is the avatar's, the same as the snake.
# The six canvases add up to 230 px so the row fits the profile page's 238 px column on a 320 px phone.
SPINES = (
    Spine("marginalia", "MARGINALIA", 40, "#a466d9", "#6f3fa6", "#1a0b2e", "marginalia"),
    Spine("concurrency", "CONCURRENCY", 36, "#216e39", "#0e4429", "#ffffff", "claude-code-structured-concurrency"),
    Spine("crash", "CRASH", 33, "#9be9a8", "#30a14e", "#04260f", "crash-app"),
    Spine("cluely", "CLUELY", 36, "#40c463", "#216e39", "#04260f", "Ronils-Cluely-OPENSOURCE"),
    Spine("spotify", "SPOTIFY", 40, "#30a14e", "#216e39", "#04260f", "spotify-cleaner"),
    Spine("courtside", "COURTSIDE", 33, "#9be9a8", "#30a14e", "#04260f", "courtside-showcase"),
)


def height(s: Spine) -> int:
    return PITCH * len(s.label) + 36


def _num(v: float) -> str:
    text = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


@functools.lru_cache(maxsize=1)
def _font() -> TTFont:
    return TTFont(FONT)


def _placed(s: Spine):
    """Yield each letter's glyph and the transform that puts it on the spine, centred and upright."""
    font = _font()
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = SIZE / font["head"].unitsPerEm
    top, centre = BASE - height(s), MARGIN + s.width / 2
    for i, ch in enumerate(s.label):
        glyph = glyphs[cmap[ord(ch)]]
        x0 = centre - glyph.width * scale / 2
        y0 = top + FIRST_BASELINE + PITCH * i
        yield glyph, (scale, 0, 0, -scale, x0, y0)


def letter_bounds(s: Spine) -> list[tuple[float, float, float, float]]:
    out = []
    for glyph, transform in _placed(s):
        pen = BoundsPen(_font().getGlyphSet())
        glyph.draw(TransformPen(pen, transform))
        out.append(pen.bounds)
    return out


def render(s: Spine) -> str:
    w, h = s.width, height(s)
    top, canvas_w, x = BASE - h, w + 2 * MARGIN, _num(MARGIN + 0.75)
    parts = [
        f'<rect x="{x}" y="{_num(top + 0.75)}" width="{_num(w - 1.5)}" height="{_num(h - 1.5)}" rx="2" '
        f'fill="{s.fill}" stroke="{s.stroke}" stroke-width="1.5"/>',
        f'<rect x="{x}" y="{top + 6}" width="{_num(w - 1.5)}" height="2" fill="{s.stroke}"/>',
        f'<rect x="{x}" y="{top + h - 8}" width="{_num(w - 1.5)}" height="2" fill="{s.stroke}"/>',
    ]
    for glyph, transform in _placed(s):
        pen = SVGPathPen(_font().getGlyphSet(), ntos=_num)
        glyph.draw(TransformPen(pen, transform))
        parts.append(f'<path d="{pen.getCommands()}" fill="{s.ink}"/>')
    parts.append(f'<rect x="0" y="{BASE}" width="{canvas_w}" height="3" fill="{PLANK}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{CANVAS_H}" '
            f'viewBox="0 0 {canvas_w} {CANVAS_H}" role="img" aria-label="{s.label.title()}">'
            + "".join(parts) + "</svg>\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    keep = {f"{s.key}.svg" for s in SPINES}
    for old in OUT.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
    for s in SPINES:
        (OUT / f"{s.key}.svg").write_text(render(s), encoding="utf-8", newline="\n")
        print(f"assets/shelf/{s.key}.svg  {s.width + 2 * MARGIN}x{CANVAS_H}")


if __name__ == "__main__":
    main()
