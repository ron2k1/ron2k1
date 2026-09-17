import pytest
from connect4 import engine as E


def test_empty_position_red_to_play():
    p = E.Position()
    assert E.to_play(p) == E.RED
    assert E.legal_moves(p) == [0, 1, 2, 3, 4, 5, 6]
    assert E.to_rows(p) == ["......."] * 6


def test_gravity_and_turns():
    p = E.play(E.Position(), 3)
    assert E.to_rows(p)[-1] == "...R..."
    assert E.to_play(p) == E.BLUE
    p = E.play(p, 3)
    assert E.to_rows(p)[-2] == "...B..."
    assert E.column_height(p, 3) == 2


def test_full_column_is_illegal():
    p = E.Position()
    for _ in range(6):
        p = E.play(p, 0)
    assert not E.can_play(p, 0)
    assert 0 not in E.legal_moves(p)
    with pytest.raises(ValueError):
        E.play(p, 0)


@pytest.mark.parametrize("rows,expected", [
    (["......." , "......." , "......." , "......." , "......." , "RRRRBBB"], E.RED),   # horizontal
    (["......." , "......." , "R......" , "RB....." , "RB....." , "RB....."], E.RED),   # vertical
    (["......." , "......." , "...R..." , "..RB..." , "RRBB..." , "RBRB..."], E.RED),   # diagonal up-right
    (["......." , "......." , "...R..." , "...BR.." , "...BBRR" , "...RBBR"], E.RED),   # diagonal up-left
    (["......." , "......." , "......." , "......." , "B......" , "BRRR..."], None),    # nothing yet
])
def test_win_detection(rows, expected):
    p = E.from_rows(rows)
    assert E.winner(p) == expected


def test_no_false_win_across_column_wrap():
    # three at the top of column 0 and one at the bottom of column 1 must not count
    rows = ["R......", "R......", "R......", "B......", "B......", "BR....."]
    assert E.winner(E.from_rows(rows)) is None


def test_draw_when_board_full_without_winner():
    rows = ["RBRBRBR", "RBRBRBR", "BRBRBRB", "BRBRBRB", "RBRBRBR", "RBRBRBR"]
    p = E.from_rows(rows)
    assert E.is_draw(p)
    assert E.winner(p) is None


def test_rows_roundtrip():
    rows = ["......." , "......." , "...R..." , "...B..." , "..RRB.." , ".BRBRB."]
    p = E.from_rows(rows)
    assert E.to_rows(p) == rows
    assert p.moves == 10
    assert E.to_play(p) == E.RED
