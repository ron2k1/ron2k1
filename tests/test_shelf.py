"""The shelf: six book-spine SVGs that scripts/shelf.py draws from fonts/Inter-Bold-caps.ttf."""
import pathlib
import xml.etree.ElementTree as ET

import pytest

from scripts import shelf as SH

ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


def _luminance(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_committed_spines_match_the_generator():
    folder = ROOT / "assets" / "shelf"
    assert sorted(p.name for p in folder.glob("*.svg")) == sorted(f"{s.key}.svg" for s in SH.SPINES)
    for s in SH.SPINES:
        assert (folder / f"{s.key}.svg").read_text(encoding="utf-8") == SH.render(s), s.key


@pytest.mark.parametrize("spine", SH.SPINES, ids=lambda s: s.key)
def test_spine_is_plain_shapes_with_one_path_per_letter(spine):
    svg = SH.render(spine)
    root = ET.fromstring(svg)
    assert root.get("viewBox") == f"0 0 {spine.width + 2} 171"
    assert root.get("width") == str(spine.width + 2) and root.get("height") == "171"
    assert {el.tag.replace(NS, "") for el in root.iter()} <= {"svg", "rect", "path"}
    assert len(root.findall(f"{NS}path")) == len(spine.label)
    for banned in ("href", "<text", "<style", "<script", "@font-face", "url("):
        assert banned not in svg


@pytest.mark.parametrize("spine", SH.SPINES, ids=lambda s: s.key)
def test_letters_sit_between_the_bands_and_read_clearly(spine):
    top = 168 - SH.height(spine)
    for x0, y0, x1, y1 in SH.letter_bounds(spine):
        assert 1 + 1.5 < x0 and x1 < 1 + spine.width - 1.5
        assert top + 8 < y0 and y1 < top + SH.height(spine) - 8
    assert contrast(spine.ink, spine.fill) >= 4.5


def test_shelf_fits_a_phone_and_every_spine_fits_its_canvas():
    # On github.com/ron2k1 the README column is the viewport minus 82 px, so 238 px on a 320 px phone.
    # Wider than that and the last spines wrap onto a second shelf.
    assert sum(s.width + 2 for s in SH.SPINES) <= 238
    assert all(SH.height(s) <= 168 for s in SH.SPINES)
    assert len({s.key for s in SH.SPINES}) == len(SH.SPINES)


@pytest.mark.parametrize("spine", SH.SPINES, ids=lambda s: s.key)
def test_plank_runs_edge_to_edge_so_neighbours_join(spine):
    assert f'<rect x="0" y="168" width="{spine.width + 2}" height="3" fill="{SH.PLANK}"/>' in SH.render(spine)
    assert contrast(SH.PLANK, "#ffffff") >= 3 and contrast(SH.PLANK, "#0d1117") >= 3
