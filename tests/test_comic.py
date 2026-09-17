import json
import pathlib
import xml.etree.ElementTree as ET

from comic import buttons, draw, masthead, stats, toolbelt

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _svg(text):
    root = ET.fromstring(text)
    assert root.tag.endswith("svg")
    return text


def test_fonts_embedded_once():
    css = draw.font_css()
    assert css.count("data:font/woff2;base64,") == 2
    assert "Bangers" in css and "JetBrains Mono" in css


def test_font_css_can_skip_the_mono_font():
    assert draw.font_css(mono=False).count("data:font/woff2;base64,") == 1
    assert "font-family:'JetBrains Mono';src:" not in draw.font_css(mono=False)


def test_drop_buttons_are_small_and_carry_only_bangers():
    for n in range(1, 8):
        s = _svg(buttons.build(n))
        assert "viewBox='0 0 100 84'" in s
        assert f">{n}<" in s
        assert s.count("data:font/woff2;base64,") == 1      # Bangers only, seven of these load per page
        assert draw.YELLOW in s and "<polygon" in s         # yellow chip with a drawn down arrow


def test_masthead_labels_and_size():
    s = _svg(masthead.build())
    assert "viewBox='0 0 880 300'" in s
    for label in ("THE INCREDIBLE", "RONIL BASU", "ISSUE #27", "A GAME"):
        assert label in s
    assert "capsule-render" not in s and "shields.io" not in s


def test_toolbelt_uses_data_file():
    groups = json.loads((ROOT / "data" / "toolbelt.json").read_text(encoding="utf-8"))
    s = _svg(toolbelt.build(groups))
    assert len(groups) == 4
    for g in groups:
        assert draw.esc(g["title"]) in s
        for c in g["chips"]:
            assert draw.esc(c) in s


def test_stats_renders_values():
    s = _svg(stats.build({"public_repos": 11, "contributions_past_year": 1796, "hackathon_awards": 2, "ai_roles": 3}))
    assert ">11<" in s and ">1,796<" in s and "HACKATHON AWARDS" in s


def test_stats_merge_keeps_old_numbers_when_fetch_fails():
    old = {"public_repos": 11, "contributions_past_year": 1796, "hackathon_awards": 2, "ai_roles": 3}
    assert stats.merge(old, None) == old
    merged = stats.merge(old, {"public_repos": 12, "contributions_past_year": 1800})
    assert merged["public_repos"] == 12 and merged["hackathon_awards"] == 2
