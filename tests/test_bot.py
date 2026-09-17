from connect4 import engine as E
from connect4.bot import choose_move, evaluate


def test_takes_immediate_win():
    rows = ["......." , "......." , "......." , "......." , "......." , "RRR.BBB"]
    p = E.from_rows(rows)            # 6 pieces, red to play, red wins in column 3
    assert E.to_play(p) == E.RED
    assert choose_move(p, budget=0.5).col == 3


def test_blocks_immediate_loss():
    rows = ["......." , "......." , "......." , "......." , "B......" , "RRR..B."]
    p = E.from_rows(rows)            # 5 pieces, blue to play, must block column 3
    assert E.to_play(p) == E.BLUE
    assert choose_move(p, budget=0.5).col == 3


def test_never_plays_full_column():
    p = E.Position()
    for _ in range(6):
        p = E.play(p, 3)
    m = choose_move(p, budget=0.3)
    assert m.col != 3 and E.can_play(p, m.col)


def test_reports_depth_and_time():
    m = choose_move(E.Position(), budget=0.4)
    assert m.depth >= 1
    assert m.nodes >= 1
    assert m.seconds < 1.5


def test_prefers_faster_win():
    # red can win now in column 3; the bot must not dither
    rows = ["......." , "......." , "......." , "......." , "B.B...." , "RRR.B.."]
    p = E.from_rows(rows)
    assert choose_move(p, budget=0.5).col == 3


def test_evaluate_symmetry():
    assert evaluate(E.Position()) == 0
