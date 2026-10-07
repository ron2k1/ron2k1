"""The shelf: seven cloth-bound books and an end piece that scripts/shelf.py draws from the two fonts in fonts/."""
import pathlib
import re
import xml.etree.ElementTree as ET

import pytest

from scripts import shelf as SH

ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"
ALLOWED_TAGS = {"svg", "defs", "linearGradient", "stop", "clipPath", "rect", "path"}


def _luminance(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def all_files():
    return {f"{b.key}.svg": SH.render(b) for b in SH.BOOKS} | {f"{SH.END_KEY}.svg": SH.render_end()}


def test_committed_files_match_the_generator():
    folder = ROOT / "assets" / "shelf"
    files = all_files()
    assert sorted(p.name for p in folder.glob("*.svg")) == sorted(files)
    for name, svg in files.items():
        assert (folder / name).read_text(encoding="utf-8") == svg, name


@pytest.mark.parametrize("name", sorted(all_files()))
def test_every_file_is_plain_shapes_with_no_fonts_or_outside_references(name):
    svg = all_files()[name]
    root = ET.fromstring(svg)
    width = SH.END_WIDTH if name == f"{SH.END_KEY}.svg" else next(b.width for b in SH.BOOKS if f"{b.key}.svg" == name)
    assert root.get("viewBox") == f"0 0 {width} {SH.CANVAS_H}"
    assert {el.tag.replace(NS, "") for el in root.iter()} <= ALLOWED_TAGS
    for banned in ("href", "<text", "<style", "<script", "<image", "foreignObject", "@font-face"):
        assert banned not in svg, banned
    assert re.findall(r"https?://[^\"']+", svg) == ["http://www.w3.org/2000/svg"]
    assert all(ref.startswith("#") for ref in re.findall(r"url\(([^)]*)\)", svg))
    # Every reference resolves inside the file, and nothing is defined that no shape uses.
    ids = re.findall(r'\bid="([^"]+)"', svg)
    assert len(ids) == len(set(ids))
    assert set(re.findall(r"url\(#([^)]*)\)", svg)) == set(ids)


@pytest.mark.parametrize("book", SH.BOOKS, ids=lambda b: b.key)
def test_title_stays_on_the_spine_between_the_bands(book):
    lo, hi = SH.title_region(book)
    bounds = SH.title_bounds(book)
    assert len(bounds) == len(book.title.replace(" ", ""))
    for x0, y0, x1, y1 in bounds:
        assert SH.GAP + 4 < x0 and x1 < book.width - SH.GAP - 4
        assert lo - 0.5 <= y0 and y1 <= hi + 0.5
    # Checked against the bands render() draws, so moving a band onto the title fails here.
    *head, (tail_y, tail_h) = SH.bands(book)
    assert max(y + h for y, h in head) < min(b[1] for b in bounds)
    assert max(b[3] for b in bounds) < tail_y
    assert tail_y + tail_h < SH.sticker_box(book)[1]
    assert contrast(book.foil, book.cloth) >= 3       # large text: WCAG AA asks 3:1


@pytest.mark.parametrize("book", SH.BOOKS, ids=lambda b: b.key)
def test_call_number_is_typed_inside_its_sticker(book):
    sx, sy, sw, sh = SH.sticker_box(book)
    bounds = SH.label_bounds(book)
    assert len(bounds) == sum(len(line) for line in book.call)
    for x0, y0, x1, y1 in bounds:
        assert sx + 1 < x0 and x1 < sx + sw - 1
        assert sy + 1 < y0 and y1 < sy + sh - 1
    assert contrast(SH.STICKER_INK, SH.STICKER) >= 7


@pytest.mark.parametrize("book", SH.LYING, ids=lambda b: b.title)
def test_lying_titles_sit_inside_their_covers_between_the_foil_rules(book):
    y = SH.lying_top(book)
    bounds = SH.lying_title_bounds(book)
    assert len(bounds) == len(book.title.replace(" ", ""))
    for x0, y0, x1, y1 in bounds:
        assert book.x + 12 < x0 and x1 < book.x + book.width - 12
        assert y + 2 < y0 and y1 < y + book.height - 2
    assert SH.GAP + 40 < book.x and book.x + book.width < SH.END_WIDTH - SH.GAP
    assert contrast(book.foil, book.cloth) >= 3


def test_books_are_shelved_in_call_number_order_with_the_author_cutter_last():
    numbers = ["".join(b.call[:-1]) for b in SH.BOOKS]
    assert all(re.fullmatch(r"\d{3}\.\d+", n) for n in numbers), numbers
    assert numbers == sorted(numbers, key=float)
    assert {b.call[-1] for b in SH.BOOKS} == {"BAS"}
    assert len({b.key for b in SH.BOOKS}) == len(SH.BOOKS)


def test_shelf_spans_the_column_without_wrapping():
    # Widths are thousandths of the README column. Under 1000 so rounding never pushes the end to a
    # second line, and close to it so the plank reaches the right edge.
    total = sum(b.width for b in SH.BOOKS) + SH.END_WIDTH
    assert 990 <= total <= 997
    assert all(0 < SH.top(b) for b in SH.BOOKS)
    assert SH.FLOOR - sum(x.height for x in SH.LYING) > 0


@pytest.mark.parametrize("name", sorted(all_files()))
def test_plank_runs_edge_to_edge_so_neighbours_join(name):
    svg = all_files()[name]
    width = re.search(r'viewBox="0 0 ([\d.]+) ', svg).group(1)
    assert f'<rect x="0" y="{SH.FLOOR}" width="{width}" height="4" fill="{SH.PLANK_TOP}"/>' in svg
    assert contrast(SH.PLANK_FRONT, "#ffffff") >= 3 and contrast(SH.PLANK_TOP, "#0d1117") >= 3
