import re
import string
import xml.etree.ElementTree as ET

import pytest

from comic import draw as D
from connect4 import game as G
from connect4 import hall as HL

NS = "{http://www.w3.org/2000/svg}"
BANNED = ("\u2014", "\u2013", ";", "\u25cf")


def _texts(svg: str) -> list[str]:
    return ["".join(t.itertext()) for t in ET.fromstring(svg).iter(f"{NS}text")]


def _strings(svg: str) -> list[str]:
    return _texts(svg) + [ET.fromstring(svg).get("aria-label", "")]


def _entry(by: str, game_no: int, moves: int = 9) -> dict:
    return {"game_no": game_no, "by": by, "moves": moves}


def _state(hall: list, game_no: int = 1, finished: bool = False, result: str | None = None) -> dict:
    s = G.new_state(game_no=game_no)
    s["hall"], s["finished"], s["result"] = hall, finished, result
    return s


POPULATED = _state([_entry("octocat", 3, 9), _entry("hubot", 5, 12)], game_no=7, finished=True, result="B")


def test_empty_wall_says_nobody_yet():
    svg = HL.render_hall(G.new_state())
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg") and root.get("viewBox") == "0 0 720 200"
    texts = _texts(svg)
    for want in ("BEAT THE BOT", "NOBODY YET.", "WIN ONE AND YOUR HANDLE GOES HERE", "NO GAME FINISHED YET"):
        assert want in texts
    assert not any("@" in t for t in texts)
    invite = next(t for t in root.iter(f"{NS}text") if "".join(t.itertext()) == "WIN ONE AND YOUR HANDLE GOES HERE")
    assert float(invite.get("font-size")) >= 22            # still legible once GitHub mobile halves the wall
    assert svg.count("data:font/woff2;base64,") == 2


def test_latest_five_rows_keep_all_time_rank():
    hall = [_entry(f"u{i}", i, i + 6) for i in range(1, 8)]
    svg = HL.render_hall(_state(hall, game_no=8))
    texts = _texts(svg)
    assert ET.fromstring(svg).get("viewBox") == "0 0 720 330"
    for r in range(3, 8):
        assert f"#{r}" in texts and f"@u{r}" in texts
    for gone in ("#1", "#2", "@u1", "@u2"):
        assert gone not in texts
    assert "GAME 7 · 13 MOVES" in texts


def test_rank_one_star_is_the_only_yellow():
    one = HL.render_hall(_state([_entry("octocat", 1)], game_no=2))
    assert ET.fromstring(one).get("viewBox") == "0 0 720 146"
    assert one.count(f"fill='{D.YELLOW}'") == 1 and re.search(rf"<polygon[^>]*fill='{D.YELLOW}'", one)
    seven = HL.render_hall(_state([_entry(f"u{i}", i) for i in range(1, 8)], game_no=8))
    assert seven.count(f"fill='{D.YELLOW}'") == 0


@pytest.mark.parametrize("game_no,finished,result,hall,unbeaten,chip", [
    (1, False, None, [], 0, "NO GAME FINISHED YET"),
    (1, True, "B", [], 1, "BOT UNBEATEN · 1 GAME"),
    (2, False, None, [], 1, "BOT UNBEATEN · 1 GAME"),
    (2, True, "R", [_entry("octocat", 2)], 0, "A HUMAN WON THE LAST GAME"),
    (3, True, "draw", [_entry("octocat", 2)], 1, "BOT UNBEATEN · 1 GAME"),      # a draw counts as unbeaten
    (6, False, None, [_entry("octocat", 2)], 3, "BOT UNBEATEN · 3 GAMES"),
])
def test_unbeaten_count_and_chip_text(game_no, finished, result, hall, unbeaten, chip):
    s = _state(hall, game_no, finished, result)
    assert HL.unbeaten(s) == unbeaten and HL.chip_text(s) == chip


def test_bad_login_draws_as_someone_and_is_escaped():
    s = _state([_entry("<script>alert(1)</script>", 1), _entry("a'b", 2), _entry("octocat", 3)], game_no=4)
    svg = HL.render_hall(s)
    texts = _texts(svg)
    assert "@someone" in texts and "@octocat" in texts
    assert "<script" not in svg and "alert" not in svg and "a'b" not in svg
    assert "someone" in HL.label(s) and "octocat" in HL.label(s)


def test_login_never_reaches_the_game_label():
    assert HL.login_size("octocat") == (28, False)
    assert HL.login_size("claude-code-structured-concurrency-xyz") == (21, False)
    assert HL.width("@claude-code-structured-concurrency-xyz", 21) <= HL.AVAIL
    assert HL.login_size("m" * 39) == (16, True)
    squeezed = HL.render_hall(_state([_entry("m" * 39, 1)], game_no=2))
    layers = re.findall(r"<text[^>]*>@m{39}</text>", squeezed)
    assert len(layers) >= 2 and all(f"textLength='{HL.AVAIL}' lengthAdjust='spacingAndGlyphs'" in t for t in layers)
    assert "textLength" not in HL.render_hall(_state([_entry("octocat", 1)], game_no=2))


def test_bangers_advances_match_the_font():
    TTFont = pytest.importorskip("fontTools.ttLib").TTFont
    f = TTFont(str(D.ROOT / "fonts" / "Bangers-Regular.woff2"))
    assert f["head"].unitsPerEm == 1000
    assert set(HL.ADV) == set("@" + string.ascii_letters + string.digits + "-")
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    for c, adv in HL.ADV.items():
        assert hmtx[cmap[ord(c)]][0] == adv, c


def test_widest_label_leaves_the_gap():
    TTFont = pytest.importorskip("fontTools.ttLib").TTFont

    def width(font, text, size, track):
        f = TTFont(str(D.ROOT / "fonts" / font))
        cmap, hmtx = f.getBestCmap(), f["hmtx"]
        return sum(hmtx[cmap[ord(c)]][0] for c in text) / f["head"].unitsPerEm * size + track * size * (len(text) - 1)

    assert HL.LABEL_X - width("JetBrainsMono.woff2", "GAME 999 · 42 MOVES", 12, .14) >= HL.LOGIN_X + HL.AVAIL + 15
    assert 30 + width("Bangers-Regular.woff2", "BEAT THE BOT", 40, .03) < 482       # the widest chip starts at 482


def test_label_text():
    assert HL.label(G.new_state()) == "Beat the bot: nobody yet. No game finished yet."
    assert HL.label(POPULATED) == ("Beat the bot: 1 octocat, game 3 in 9 moves. 2 hubot, game 5 in 12 moves. "
                                   "Bot unbeaten, 2 games.")


def test_no_banned_glyphs_in_any_wall_string():
    pool = _strings(HL.render_hall(G.new_state())) + _strings(HL.render_hall(POPULATED))
    pool += [HL.CHIP_NONE, HL.CHIP_HUMAN, HL.chip_text(_state([], 1, True, "B")), HL.chip_text(_state([], 6)),
             HL.ON_THE_WALL, HL.label(G.new_state()), HL.label(POPULATED), HL.TITLE, HL.EMPTY_TEXT, HL.INVITE]
    for s in pool:
        assert not any(ch in s for ch in BANNED), s


def test_write_all_leaves_one_hall_file(tmp_path):
    from connect4.__main__ import main

    (tmp_path / "README.md").write_text("# hi\n\n<!-- c4:start -->\nold\n<!-- c4:end -->\n", encoding="utf-8")
    assert main(["init", "--root", str(tmp_path)]) == 0
    game = tmp_path / "game"
    assert (game / "hall-0.svg").exists() and (game / "board-0.svg").exists()
    st = G.load(game / "state.json")
    assert st["hall"] == []
    st["revision"] = 3
    G.save(game / "state.json", st)
    assert main(["render", "--root", str(tmp_path)]) == 0
    assert [p.name for p in game.glob("hall-*.svg")] == ["hall-3.svg"]
    assert [p.name for p in game.glob("board-*.svg")] == ["board-3.svg"]
    assert 'src="game/hall-3.svg"' in (tmp_path / "README.md").read_text(encoding="utf-8")
