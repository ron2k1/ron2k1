"""Draw the library shelf in assets/shelf/ for the profile README.

The shelf runs the full width of the README. Each project is one cloth-bound book, its own SVG so the
README can wrap it in its own link, shelved in Dewey Decimal order with a typed call-number sticker
near the foot of the spine. A last file holds the bookend and two textbooks lying on their side, so
the plank reaches the right edge.

Every file is CANVAS_H units tall and as many units wide as it is thousandths of the README column.
The README gives each image width="<units / 10>%", so all of them render at the same height and stand
on one plank at any column width. Titles are Libre Baskerville Bold and stickers Courier Prime Bold,
both outlined to paths, so the files carry no fonts, styles, scripts or external references.

Run from the repo root: python scripts/shelf.py          (writes the SVGs)
                        python scripts/shelf.py --readme (prints the README's shelf line)
"""
from __future__ import annotations

import functools
import pathlib
import sys
from typing import NamedTuple

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
TITLE_FONT = ROOT / "fonts" / "LibreBaskerville-Bold-caps.ttf"
LABEL_FONT = ROOT / "fonts" / "CourierPrime-Bold-label.ttf"
OUT = ROOT / "assets" / "shelf"
REPO_URL = "https://github.com/ron2k1/"

CANVAS_H = 320                  # every file is this tall
FLOOR = 306                     # books stand on y = FLOOR, the plank fills FLOOR..CANVAS_H
GAP = 1.2                       # each file pads its book this much per side
TRACKING = 0.08                 # extra space between title letters, in ems
TITLE_MAX = 24                  # largest title size in units
LABEL_SIZE, LABEL_PITCH = 12, 13
STICKER_INSET, STICKER_LIFT = 8, 16

PLANK_TOP, PLANK_FRONT, PLANK_EDGE = "#a07a55", "#765236", "#573b26"
STICKER, STICKER_INK = "#f3ecdc", "#2a2622"
OUTLINE = "#1b1b1f"


class Book(NamedTuple):
    key: str
    title: str
    call: tuple[str, ...]       # sticker lines, top to bottom
    width: int                  # units, so width / 10 is the README percentage
    height: int                 # body height in units
    cloth: str
    foil: str
    repo: str
    alt: str


# Shelved by call number. Each class is the real Dewey Decimal heading for what the project is about.
BOOKS = (
    Book("concurrency", "CONCURRENCY", ("005.43", "BAS"), 82, 280, "#2f5d42", "#e6c77f",
         "claude-code-structured-concurrency", "claude-code-structured-concurrency, 005.43 operating systems"),
    Book("hazardcam", "HAZARDCAM", ("363.11", "BAS"), 92, 292, "#2a2c31", "#f2a93b",
         "HazardCam", "HazardCam, 363.11 occupational and industrial safety"),
    Book("marginalia", "MARGINALIA", ("371.3", "0281", "BAS"), 84, 262, "#a466d9", "#1f0d36",
         "marginalia", "marginalia, 371.30281 study skills"),
    Book("crash", "CRASH", ("381.142", "BAS"), 70, 236, "#7c2832", "#ecd08f",
         "crash-app", "crash-app, 381.142 electronic commerce"),
    Book("cluely", "CLUELY", ("658.456", "BAS"), 74, 270, "#253c63", "#dfe5ee",
         "Ronils-Cluely-OPENSOURCE", "Cluely, 658.456 conducting meetings"),
    Book("spotify", "SPOTIFY", ("780.285", "BAS"), 78, 248, "#c9993f", "#2b1e06",
         "spotify-cleaner", "spotify-cleaner, 780.285 computer applications in music"),
    Book("courtside", "COURTSIDE", ("796.323", "BAS"), 82, 284, "#b65a2f", "#fbecd4",
         "courtside-showcase", "courtside-showcase, 796.323 basketball"),
)

HAZARD_KEY = "hazardcam"        # this book gets a hazard-tape band instead of plain head bands


class Lying(NamedTuple):
    title: str
    x: float
    width: float
    height: float
    cloth: str
    foil: str


END_KEY, END_WIDTH = "end", 434   # the bookend and the textbooks, out to 99.6 % of the column
BOOKEND = "#34383f"
LYING = (                        # bottom to top
    Lying("STATISTICS", 118, 236, 34, "#3d4a57", "#e9e1cf"),
    Lying("DATA SCIENCE", 132, 210, 30, "#5b6b4f", "#f1ead6"),
)


def _num(v: float) -> str:
    text = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


@functools.lru_cache(maxsize=None)
def _font(path: pathlib.Path) -> TTFont:
    return TTFont(path)


def top(b: Book) -> float:
    return FLOOR - b.height


def sticker_box(b: Book) -> tuple[float, float, float, float]:
    h = 10 + LABEL_PITCH * len(b.call)
    return STICKER_INSET, FLOOR - STICKER_LIFT - h, b.width - 2 * STICKER_INSET, h


def title_region(b: Book) -> tuple[float, float]:
    """The stretch of spine the title may use, between the head bands and the tail band."""
    return top(b) + 34, sticker_box(b)[1] - 14


def bands(b: Book) -> tuple[tuple[float, float], ...]:
    """The (y, height) of every foil band render() draws: the head bands, then the tail band last."""
    t, sy = top(b), sticker_box(b)[1]
    head = ((t + 12, 11),) if b.key == HAZARD_KEY else ((t + 12, 2.2), (t + 18, 1.2))
    return head + ((sy - 9, 1.2),)


def _advance(text: str, scale: float, size: float) -> float:
    font = _font(TITLE_FONT)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    return sum(glyphs[cmap[ord(c)]].width * scale for c in text) + TRACKING * size * (len(text) - 1)


def title_size(b: Book) -> float:
    """The largest size up to TITLE_MAX whose caps fit across the spine and whose run fits along it."""
    font = _font(TITLE_FONT)
    upm, cap = font["head"].unitsPerEm, font["OS/2"].sCapHeight
    lo, hi = title_region(b)
    by_width = (b.width - 2 * GAP) * 0.42 * upm / cap
    # Fitted on advance widths, so keep 2 % spare: an A or a V draws a little past its advance box.
    by_length = 0.98 * (hi - lo) / (_advance(b.title, 1 / upm, 1) or 1)
    return min(TITLE_MAX, by_width, by_length)


def _title_glyphs(b: Book):
    """Yield each title glyph with the transform that turns it 90 degrees clockwise onto the spine.

    A glyph point (gx, gy) lands at (bx + s*gy, y + s*gx): the run goes down the spine and the tops of
    the letters face right, which is how an English-language spine reads.
    """
    font = _font(TITLE_FONT)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    size = title_size(b)
    s = size / font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight * s
    lo, hi = title_region(b)
    y = (lo + hi) / 2 - _advance(b.title, s, size) / 2
    bx = b.width / 2 - cap / 2
    for ch in b.title:
        g = glyphs[cmap[ord(ch)]]
        yield g, (0, s, s, 0, bx, y)
        y += g.width * s + TRACKING * size


def _label_glyphs(b: Book):
    font = _font(LABEL_FONT)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    s = LABEL_SIZE / font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight * s
    x0, y0, w, h = sticker_box(b)
    first = y0 + (h - LABEL_PITCH * (len(b.call) - 1) - cap) / 2 + cap
    for i, line in enumerate(b.call):
        run = sum(glyphs[cmap[ord(c)]].width for c in line) * s
        x = x0 + (w - run) / 2
        for ch in line:
            g = glyphs[cmap[ord(ch)]]
            yield g, (s, 0, 0, -s, x, first + LABEL_PITCH * i)
            x += g.width * s


def _bounds(placed, font_path) -> list[tuple[float, float, float, float]]:
    out = []
    for glyph, transform in placed:
        pen = BoundsPen(_font(font_path).getGlyphSet())
        glyph.draw(TransformPen(pen, transform))
        if pen.bounds:
            out.append(pen.bounds)
    return out


def title_bounds(b: Book):
    return _bounds(_title_glyphs(b), TITLE_FONT)


def label_bounds(b: Book):
    return _bounds(_label_glyphs(b), LABEL_FONT)


def _paths(placed, font_path, fill: str) -> str:
    d = []
    for glyph, transform in placed:
        pen = SVGPathPen(_font(font_path).getGlyphSet(), ntos=_num)
        glyph.draw(TransformPen(pen, transform))
        d.append(pen.getCommands())
    return f'<path d="{"".join(d)}" fill="{fill}"/>'


def _defs() -> str:
    # Shading across the spine: dark at both edges, a soft highlight left of centre, like a rounded back.
    return ('<defs><linearGradient id="r" x1="0" x2="1" y1="0" y2="0">'
            '<stop offset="0" stop-color="#000" stop-opacity=".34"/>'
            '<stop offset=".14" stop-color="#fff" stop-opacity=".12"/>'
            '<stop offset=".42" stop-color="#fff" stop-opacity=".03"/>'
            '<stop offset=".86" stop-color="#000" stop-opacity=".1"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".38"/>'
            '</linearGradient></defs>')


def _plank(width: float) -> str:
    return (f'<rect x="0" y="{FLOOR}" width="{_num(width)}" height="4" fill="{PLANK_TOP}"/>'
            f'<rect x="0" y="{FLOOR + 4}" width="{_num(width)}" height="{CANVAS_H - FLOOR - 4}" fill="{PLANK_FRONT}"/>'
            f'<rect x="0" y="{CANVAS_H - 1.5}" width="{_num(width)}" height="1.5" fill="{PLANK_EDGE}"/>')


def _band(x: float, y: float, w: float, h: float, fill: str) -> str:
    return f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="{_num(h)}" fill="{fill}"/>'


def _hazard_band(b: Book, y: float, h: float) -> str:
    """Amber and charcoal diagonal stripes, clipped to the spine, like hazard tape."""
    x0, x1 = GAP + 1, b.width - GAP - 1
    stripes, step = [], 12
    x = x0 - h
    while x < x1:
        stripes.append(f"M{_num(x)} {_num(y + h)}L{_num(x + h)} {_num(y)}L{_num(x + h + step / 2)} {_num(y)}"
                       f"L{_num(x + step / 2)} {_num(y + h)}Z")
        x += step
    return (f'<clipPath id="t"><rect x="{_num(x0)}" y="{_num(y)}" width="{_num(x1 - x0)}" height="{_num(h)}"/></clipPath>'
            f'<rect x="{_num(x0)}" y="{_num(y)}" width="{_num(x1 - x0)}" height="{_num(h)}" fill="{b.foil}"/>'
            f'<path d="{"".join(stripes)}" fill="#16171a" clip-path="url(#t)"/>')


def render(b: Book) -> str:
    w, t = b.width, top(b)
    bw = w - 2 * GAP
    sx, sy, sw, sh = sticker_box(b)
    inset = 6
    parts = [_defs(),
             f'<rect x="{_num(GAP)}" y="{_num(t)}" width="{_num(bw)}" height="{b.height}" rx="2.5" fill="{b.cloth}"/>',
             f'<rect x="{_num(GAP)}" y="{_num(t)}" width="{_num(bw)}" height="{b.height}" rx="2.5" fill="url(#r)"/>']
    *head, (tail_y, tail_h) = bands(b)
    if b.key == HAZARD_KEY:
        parts.append(_hazard_band(b, *head[0]))
    else:
        parts += [_band(GAP + inset, y, bw - 2 * inset, h, b.foil) for y, h in head]
    parts.append(_band(GAP + inset, tail_y, bw - 2 * inset, tail_h, b.foil))
    parts.append(_paths(_title_glyphs(b), TITLE_FONT, b.foil))
    parts.append(f'<rect x="{_num(sx)}" y="{_num(sy)}" width="{_num(sw)}" height="{_num(sh)}" rx="2" '
                 f'fill="{STICKER}" stroke="#000" stroke-opacity=".22" stroke-width=".8"/>')
    parts.append(_paths(_label_glyphs(b), LABEL_FONT, STICKER_INK))
    parts.append(f'<rect x="{_num(GAP + .5)}" y="{_num(t + .5)}" width="{_num(bw - 1)}" height="{b.height - 1}" rx="2.5" '
                 f'fill="none" stroke="{OUTLINE}" stroke-opacity=".55" stroke-width="1"/>')
    parts.append(_plank(w))
    return _svg(w, b.alt, parts)


def lying_top(book: Lying) -> float:
    """The top edge of a lying book's cover. LYING is stacked bottom to top on the plank."""
    return FLOOR - sum(x.height for x in LYING[:LYING.index(book) + 1])


def _lying_glyphs(book: Lying):
    """Yield each glyph of a lying book's title, upright and centred on the cover."""
    font = _font(TITLE_FONT)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    size = book.height * 0.44
    s = size / font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight * s
    baseline = lying_top(book) + book.height / 2 + cap / 2
    x = book.x + (book.width - _advance(book.title, s, size)) / 2
    for ch in book.title:
        g = glyphs[cmap[ord(ch)]]
        yield g, (s, 0, 0, -s, x, baseline)
        x += g.width * s + TRACKING * size


def lying_title_bounds(book: Lying):
    return _bounds(_lying_glyphs(book), TITLE_FONT)


def render_end() -> str:
    """The bookend against the last book, then two textbooks lying on their side."""
    parts = []
    # A plain iron bookend: a slab with a quarter-round top, 150 units tall.
    parts.append(f'<path d="M{GAP} {FLOOR}V{FLOOR - 120}A30 30 0 0 1 {GAP + 30} {FLOOR - 150}H{GAP + 40}V{FLOOR}Z" '
                 f'fill="{BOOKEND}"/>')
    parts.append(f'<rect x="{GAP + 34}" y="{FLOOR - 150}" width="6" height="150" fill="#fff" fill-opacity=".08"/>')
    for book in LYING:
        y = lying_top(book)
        parts.append(f'<rect x="{_num(book.x)}" y="{_num(y)}" width="{_num(book.width)}" height="{_num(book.height)}" '
                     f'rx="2.5" fill="{book.cloth}"/>')
        parts.append(f'<rect x="{_num(book.x + 10)}" y="{_num(y + 3)}" width="1.6" height="{_num(book.height - 6)}" '
                     f'fill="{book.foil}"/>')
        parts.append(f'<rect x="{_num(book.x + book.width - 11.6)}" y="{_num(y + 3)}" width="1.6" '
                     f'height="{_num(book.height - 6)}" fill="{book.foil}"/>')
        parts.append(_paths(_lying_glyphs(book), TITLE_FONT, book.foil))
        parts.append(f'<rect x="{_num(book.x + .5)}" y="{_num(y + .5)}" width="{_num(book.width - 1)}" '
                     f'height="{_num(book.height - 1)}" rx="2.5" fill="none" stroke="{OUTLINE}" stroke-opacity=".55"/>')
    parts.append(_plank(END_WIDTH))
    return _svg(END_WIDTH, "A bookend, then Statistics and Data Science lying on the shelf", parts)


def _svg(width: float, label: str, parts: list[str]) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_num(width)}" height="{CANVAS_H}" '
            f'viewBox="0 0 {_num(width)} {CANVAS_H}" role="img" aria-label="{label}">'
            + "".join(parts) + "</svg>\n")


def percent(units: float) -> str:
    return _num(units / 10) + "%"


def readme_line() -> str:
    """The shelf as one README line: no whitespace between anchors, or the books drift apart."""
    books = "".join(f'<a href="{REPO_URL}{b.repo}"><img src="assets/shelf/{b.key}.svg" width="{percent(b.width)}" '
                    f'alt="{b.alt}"></a>' for b in BOOKS)
    end = f'<img src="assets/shelf/{END_KEY}.svg" width="{percent(END_WIDTH)}" alt="Statistics and Data Science">'
    return books + end


def main() -> None:
    if "--readme" in sys.argv:
        print(readme_line())
        return
    OUT.mkdir(parents=True, exist_ok=True)
    files = {f"{b.key}.svg": render(b) for b in BOOKS} | {f"{END_KEY}.svg": render_end()}
    for old in OUT.glob("*.svg"):
        if old.name not in files:
            old.unlink()
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8", newline="\n")
        print(f"assets/shelf/{name}  {len(svg)} bytes")


if __name__ == "__main__":
    main()
