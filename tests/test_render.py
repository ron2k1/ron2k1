import xml.etree.ElementTree as ET

from connect4.render import render_board, status_text

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


def test_status_when_finished():
    st = dict(BASE, finished=True, result="R")
    assert status_text(st) == "GAME OVER · RED WINS"
    st = dict(BASE, finished=True, result="draw")
    assert status_text(st) == "GAME OVER · DRAW"


def test_no_bot_line_before_first_bot_move():
    st = dict(BASE, last_bot=None)
    assert "DEPTH" not in render_board(st)
