"""Connect Four rules on bitboards.

Each column is 7 bits: rows 0..5 are playable (0 = bottom) and bit 6 is a sentinel that keeps
carries and window checks from spilling into the next column. `current` holds the pieces of the
player to move, `mask` holds every piece. Red always moves first, so parity of `moves` gives the
side to move.
"""
from __future__ import annotations

from dataclasses import dataclass

COLS, ROWS = 7, 6
H = ROWS + 1
RED, BLUE, EMPTY = "R", "B", "."
BOTTOM = sum(1 << (c * H) for c in range(COLS))
BOARD_MASK = BOTTOM * ((1 << ROWS) - 1)
CENTER_MASK = ((1 << ROWS) - 1) << (3 * H)
ORDER = (3, 2, 4, 1, 5, 0, 6)


@dataclass(frozen=True)
class Position:
    current: int = 0
    mask: int = 0
    moves: int = 0


def bottom_mask(col: int) -> int:
    return 1 << (col * H)


def top_mask(col: int) -> int:
    return 1 << (col * H + ROWS - 1)


def to_play(pos: Position) -> str:
    return RED if pos.moves % 2 == 0 else BLUE


def can_play(pos: Position, col: int) -> bool:
    return 0 <= col < COLS and (pos.mask & top_mask(col)) == 0


def legal_moves(pos: Position) -> list[int]:
    return [c for c in range(COLS) if can_play(pos, c)]


def play(pos: Position, col: int) -> Position:
    if not can_play(pos, col):
        raise ValueError(f"column {col} is not playable")
    new_mask = pos.mask | (pos.mask + bottom_mask(col))
    return Position(current=pos.current ^ pos.mask, mask=new_mask, moves=pos.moves + 1)


def is_win(bb: int) -> bool:
    for shift in (1, H, H - 1, H + 1):
        m = bb & (bb >> shift)
        if m & (m >> (2 * shift)):
            return True
    return False


def last_mover_board(pos: Position) -> int:
    return pos.current ^ pos.mask


def bitboards(pos: Position) -> tuple[int, int]:
    """(red, blue) bitboards regardless of who is to move."""
    other = pos.current ^ pos.mask
    return (pos.current, other) if to_play(pos) == RED else (other, pos.current)


def winner(pos: Position) -> str | None:
    red, blue = bitboards(pos)
    if is_win(red):
        return RED
    if is_win(blue):
        return BLUE
    return None


def is_draw(pos: Position) -> bool:
    return pos.moves == COLS * ROWS and winner(pos) is None


def column_height(pos: Position, col: int) -> int:
    return ((pos.mask >> (col * H)) & ((1 << H) - 1)).bit_count()


def to_rows(pos: Position) -> list[str]:
    red, blue = bitboards(pos)
    rows = []
    for r in range(ROWS - 1, -1, -1):
        row = []
        for c in range(COLS):
            bit = 1 << (c * H + r)
            row.append(RED if red & bit else BLUE if blue & bit else EMPTY)
        rows.append("".join(row))
    return rows


def from_rows(rows: list[str]) -> Position:
    if len(rows) != ROWS or any(len(r) != COLS for r in rows):
        raise ValueError("board must be 6 rows of 7 cells")
    red = blue = 0
    for r_index, row in enumerate(rows):
        r = ROWS - 1 - r_index
        for c, ch in enumerate(row):
            bit = 1 << (c * H + r)
            if ch == RED:
                red |= bit
            elif ch == BLUE:
                blue |= bit
            elif ch != EMPTY:
                raise ValueError(f"bad cell {ch!r}")
    moves = (red | blue).bit_count()
    current = red if moves % 2 == 0 else blue
    return Position(current=current, mask=red | blue, moves=moves)
