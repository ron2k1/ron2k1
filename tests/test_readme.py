import pytest

from connect4 import game as G
from connect4 import readme as R

DOC = "# hi\n\n<!-- c4:start -->\nold\n<!-- c4:end -->\n\nfooter\n"


def test_rewrite_replaces_only_the_region():
    s = G.new_state()
    out = R.rewrite(DOC, s)
    assert out.startswith("# hi\n\n<!-- c4:start -->\n") and out.endswith("<!-- c4:end -->\n\nfooter\n")
    assert "old" not in out
    assert 'src="game/board-0.svg"' in out
    assert R.rewrite(out, s) == out           # idempotent
    s["revision"] = 7
    assert 'src="game/board-7.svg"' in R.rewrite(out, s)


def test_links_and_status_lines():
    s = G.new_state()
    s["movers"] = {"octocat": 3, "hubot": 5}
    s["moves"] = [{"col": 3, "by": "octocat", "issue": 1, "actor": "R"}]
    s["to_play"] = "B"
    r = R.region(s)
    assert r.count("issues/new?title=c4%7Cdrop%7C") == 7
    buttons = next(line for line in r.splitlines() if line.startswith("<a href="))
    assert buttons.count("<a href=") == 7 and buttons.count('src="assets/drop-') == 7   # one line, no gaps
    assert 'width="14%"' in buttons and 'alt="Drop in column 7"' in buttons
    assert 'src="game/board-0.svg"' in r and 'width="100%"' in r
    assert "Tap a column" in r
    assert "Bot is thinking" in r
    assert "@octocat" in r and "Humans 0, bot 0, draws 0" in r
    assert "@hubot (5)" in r


def test_finished_line():
    s = G.new_state()
    s.update(finished=True, result="B", game_no=7, moves=[{}] * 10)
    assert "Blue wins game 7" in R.region(s) and "starts game 8" in R.region(s)


def test_missing_markers_raises():
    with pytest.raises(ValueError):
        R.rewrite("no markers", G.new_state())
