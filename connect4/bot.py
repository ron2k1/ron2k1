"""Negamax with alpha-beta pruning and iterative deepening over the bitboard engine."""
from __future__ import annotations

import time
from dataclasses import dataclass

from . import engine as E

WIN = 10_000
EXACT, LOWER, UPPER = 0, 1, 2


@dataclass(frozen=True)
class BotMove:
    col: int
    depth: int
    nodes: int
    seconds: float
    score: int


class _Timeout(Exception):
    pass


def _threes(p: int, empty: int) -> int:
    """Windows of four holding three of `p` and one empty cell, counted once per window."""
    total = 0
    for s in (1, E.H, E.H - 1, E.H + 1):
        t = ((empty & (p >> s) & (p >> 2 * s) & (p >> 3 * s))
             | (p & (empty >> s) & (p >> 2 * s) & (p >> 3 * s))
             | (p & (p >> s) & (empty >> 2 * s) & (p >> 3 * s))
             | (p & (p >> s) & (p >> 2 * s) & (empty >> 3 * s)))
        total += t.bit_count()
    return total


def evaluate(pos: E.Position) -> int:
    """Static score from the side to move's point of view."""
    me = pos.current
    them = pos.current ^ pos.mask
    empty = E.BOARD_MASK & ~pos.mask
    center = (me & E.CENTER_MASK).bit_count() - (them & E.CENTER_MASK).bit_count()
    return 6 * _threes(me, empty) - 7 * _threes(them, empty) + 3 * center


class _Search:
    def __init__(self, deadline: float):
        self.deadline = deadline
        self.nodes = 0
        self.table: dict[tuple[int, int], tuple[int, int, int]] = {}

    def negamax(self, pos: E.Position, depth: int, alpha: int, beta: int, ply: int) -> int:
        self.nodes += 1
        if (self.nodes & 1023) == 0 and time.perf_counter() > self.deadline:
            raise _Timeout
        if pos.moves and E.is_win(E.last_mover_board(pos)):
            return -(WIN - ply)
        if pos.moves == E.COLS * E.ROWS:
            return 0
        if depth == 0:
            return evaluate(pos)
        key = (pos.current, pos.mask)
        hit = self.table.get(key)
        if hit and hit[0] >= depth:
            flag, score = hit[1], hit[2]
            if flag == EXACT:
                return score
            if flag == LOWER:
                alpha = max(alpha, score)
            elif flag == UPPER:
                beta = min(beta, score)
            if alpha >= beta:
                return score
        best = -WIN * 2
        alpha0 = alpha
        for col in E.ORDER:
            if not E.can_play(pos, col):
                continue
            score = -self.negamax(E.play(pos, col), depth - 1, -beta, -alpha, ply + 1)
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        flag = EXACT if alpha0 < best < beta else (UPPER if best <= alpha0 else LOWER)
        self.table[key] = (depth, flag, best)
        return best

    def root(self, pos: E.Position, depth: int) -> tuple[int, int]:
        best_col, best_score = -1, -WIN * 2
        alpha, beta = -WIN * 2, WIN * 2
        for col in E.ORDER:
            if not E.can_play(pos, col):
                continue
            score = -self.negamax(E.play(pos, col), depth - 1, -beta, -alpha, 1)
            if score > best_score:
                best_col, best_score = col, score
            alpha = max(alpha, score)
        return best_col, best_score


def choose_move(pos: E.Position, budget: float = 2.0, max_depth: int = 12) -> BotMove:
    start = time.perf_counter()
    legal = E.legal_moves(pos)
    if not legal:
        raise ValueError("no legal moves")
    for col in legal:                      # win now if possible
        if E.winner(E.play(pos, col)):
            return BotMove(col, 1, len(legal), time.perf_counter() - start, WIN - 1)
    search = _Search(deadline=start + budget)
    best_col, best_score, best_depth = legal[0], 0, 0
    for depth in range(1, max_depth + 1):
        try:
            col, score = search.root(pos, depth)
        except _Timeout:
            break
        best_col, best_score, best_depth = col, score, depth
        if abs(score) >= WIN - 100:        # proven result, deeper search cannot change it
            break
    return BotMove(best_col, best_depth, search.nodes, time.perf_counter() - start, best_score)
