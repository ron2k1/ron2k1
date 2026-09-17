import xml.etree.ElementTree as ET

from connect4.render import W, column_center, render_board, status_text

BASE = {"game_no": 3, "board": ["......." , "......." , "...R..." , "...B..." , "..RRB.." , ".BRBRB."],
        "to_play": "R", "moves": [{}] * 10, "finished": False, "result": None,
        "last_move": {"row": 4, "col": 4}, "last_bot": {"col": 4, "depth": 9, "nodes": 41213, "seconds": 0.83}}


def test_board_has_42_holes_and_ring_on_last_move():
    s = render_board(BASE)
    ET.fromstring(s)
    assert s.count("<circle") >= 42 * 2 + 10     # holes, their shadows, discs' glints
    assert "#ffc400" in s                         # yellow ring
    assert "MOVE 10 · RED TO PLAY" in s
    assert "DEPTH 9 · 0.8 S" in s


def test_columns_line_up_with_the_button_row():
    # The README draws seven 14%-wide drop buttons over a 100%-wide board, so each column's
    # centre must be exactly its button's centre, or a tap lands beside the disc it drops.
    for c in range(7):
        assert abs(column_center(c) - W * (0.07 + 0.14 * c)) < 1e-6


def test_status_when_finished():
    st = dict(BASE, finished=True, result="R")
    assert status_text(st) == "GAME OVER · RED WINS"
    st = dict(BASE, finished=True, result="draw")
    assert status_text(st) == "GAME OVER · DRAW"


def test_no_bot_line_before_first_bot_move():
    st = dict(BASE, last_bot=None)
    assert "DEPTH" not in render_board(st)


def test_status_labels_leave_a_gap():
    # Both labels sit on one 632 px line at ~9.6 px per character (13 px mono, .14em tracking).
    # The longest left label plus the longest right label must stay under 56 characters so the
    # two never read as one run-on line.
    st = dict(BASE, finished=True, result="B", last_bot={"col": 0, "depth": 12, "nodes": 1, "seconds": 2.0})
    s = render_board(st)
    assert "BOT · NEGAMAX · DEPTH 12 · 2.0 S" in s
    left, right = "GAME OVER · BLUE WINS", "BOT · NEGAMAX · DEPTH 12 · 2.0 S"
    assert left in s and right in s
    assert len(left) + len(right) <= 56
