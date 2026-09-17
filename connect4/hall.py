"""Draw game/hall-<rev>.svg: the wall of GitHub logins whose red drop beat the bot.

Everything is derived from game/state.json at render time. `hall` is the list of human wins in
the order they happened; the wall shows the latest five with their all-time rank and says
NOBODY YET. until the list has an entry. Same 720 px viewBox and 704 px panel as the board, so
the two line up at width="100%" in the README.
"""
from __future__ import annotations

import re

from comic import draw as D

W = 720
PX, PW = 8, 704
TITLE = "BEAT THE BOT"
EMPTY_TEXT = "NOBODY YET."
INVITE = "WIN ONE AND YOUR HANDLE GOES HERE"
CHIP_NONE = "NO GAME FINISHED YET"
CHIP_HUMAN = "A HUMAN WON THE LAST GAME"
ON_THE_WALL = "You're on the wall now."
LOGIN = re.compile(r"^[A-Za-z0-9-]{1,39}$")      # GitHub's login alphabet; anything else draws as "someone"
ROWS_SHOWN = 5
ROW_H, ROW_Y0 = 46, 103
LOGIN_X, LABEL_X, AVAIL = 140, 700, 353          # login column, right edge of GAME · MOVES, room for a login
LOGIN_MAX, LOGIN_MIN = 28, 16
CHIP_RIGHT = 692                                 # the board's chip ends here too

# Bangers advance widths in units per 1000 em for "@" and the login alphabet, read from
# fonts/Bangers-Regular.woff2 with fontTools (tests/test_hall.py pins them to the file).
ADV = {"@": 987, "a": 433, "b": 428, "c": 414, "d": 441, "e": 341, "f": 341, "g": 499, "h": 441, "i": 202,
       "j": 279, "k": 462, "l": 302, "m": 619, "n": 452, "o": 493, "p": 379, "q": 525, "r": 444, "s": 430,
       "t": 362, "u": 419, "v": 379, "w": 601, "x": 411, "y": 384, "z": 431, "A": 433, "B": 428, "C": 414,
       "D": 441, "E": 341, "F": 341, "G": 499, "H": 442, "I": 200, "J": 279, "K": 462, "L": 302, "M": 619,
       "N": 453, "O": 493, "P": 379, "Q": 525, "R": 444, "S": 430, "T": 362, "U": 419, "V": 379, "W": 601,
       "X": 411, "Y": 384, "Z": 431, "0": 474, "1": 320, "2": 467, "3": 458, "4": 459, "5": 450, "6": 478,
       "7": 339, "8": 518, "9": 489, "-": 360}


def width(text: str, size: float) -> float:
    return sum(ADV[c] for c in text) / 1000 * size


def login_size(login: str) -> tuple[int, bool]:
    """Largest size from 28 down to 16 at which "@login" fits AVAIL; (16, True) means squeeze with textLength."""
    text = "@" + login
    for size in range(LOGIN_MAX, LOGIN_MIN - 1, -1):
        if width(text, size) <= AVAIL:
            return size, False
    return LOGIN_MIN, True


def finished_games(state: dict) -> int:
    return state["game_no"] if state.get("finished") else state["game_no"] - 1


def unbeaten(state: dict) -> int:
    """Games since the last human win. Draws count."""
    hall = state.get("hall") or []
    return finished_games(state) - (hall[-1]["game_no"] if hall else 0)


def chip_text(state: dict) -> str:
    if finished_games(state) == 0:
        return CHIP_NONE
    n = unbeaten(state)
    if n == 0:
        return CHIP_HUMAN
    return "BOT UNBEATEN · 1 GAME" if n == 1 else f"BOT UNBEATEN · {n} GAMES"


def entries(state: dict) -> list[tuple[int, str, int, int]]:
    """The latest five wins as (rank, login, game_no, moves); rank is the position in the full list."""
    hall = state.get("hall") or []
    first = max(0, len(hall) - ROWS_SHOWN)
    return [(i + 1, e["by"] if LOGIN.match(str(e["by"])) else "someone", e["game_no"], e["moves"])
            for i, e in enumerate(hall) if i >= first]


def label(state: dict) -> str:
    """Alt text for the README image and the SVG aria-label, built only from validated logins and integers."""
    chip = chip_text(state).lower().replace(" · ", ", ")
    rows = entries(state)
    body = " ".join(f"{r} {by}, game {g} in {m} moves." for r, by, g, m in rows) if rows else "nobody yet."
    return f"Beat the bot: {body} {chip[0].upper()}{chip[1:]}."


def render_hall(state: dict) -> str:
    rows = entries(state)
    h = 200 if not rows else 100 + ROW_H * len(rows)
    chip = chip_text(state)
    b = [
        D.panel(PX, 8, PW, h - 16),
        f"<rect x='{PX}' y='8' width='{PW}' height='64' fill='{D.BLUE}' stroke='{D.INK}' stroke-width='3'/>"
        f"<rect x='{PX}' y='8' width='{PW}' height='64' fill='url(#dotsp)'/>",
        f"<text class='d' x='30' y='55' font-size='40' fill='{D.PAPER}' letter-spacing='.03em'>{TITLE}</text>",
        D.chip(CHIP_RIGHT - D.chip_width(chip, 12, 12), 24, chip, D.PAPER2, D.INK, size=12, pad=12, sh=3)[0],
    ]
    if not rows:
        b.append(D.shadowed_text(360, 136, EMPTY_TEXT, 44, D.RED, [(3, 3, D.INK, 1)], anchor="middle"))
        b.append(f"<text class='d' x='360' y='172' font-size='24' fill='{D.INK}' letter-spacing='.04em' "
                 f"text-anchor='middle'>{INVITE}</text>")
    for i, (rank, by, g, m) in enumerate(rows):
        cy = ROW_Y0 + ROW_H * i
        if rank == 1:                                     # the only yellow on the wall
            b.append(f"<polygon points='{D.star(47, cy + 3, 26, 17)}' fill='{D.INK}'/>")
            b.append(f"<polygon points='{D.star(44, cy, 26, 17)}' fill='{D.YELLOW}' stroke='{D.INK}' stroke-width='2'/>")
        b.append(f"<circle cx='47' cy='{cy + 3}' r='16' fill='{D.INK}'/>"
                 f"<circle cx='44' cy='{cy}' r='16' fill='{D.RED}' stroke='{D.INK}' stroke-width='3'/>"
                 f"<circle cx='39' cy='{cy - 5}' r='4' fill='{D.PAPER}' opacity='.55'/>")
        b.append(f"<text class='d' x='80' y='{cy + 9}' font-size='26' fill='{D.INK}'>#{rank}</text>")
        size, squeeze = login_size(by)
        extra = f"textLength='{AVAIL}' lengthAdjust='spacingAndGlyphs'" if squeeze else ""
        b.append(D.shadowed_text(LOGIN_X, cy + 10, "@" + by, size, D.RED, [(2, 2, D.INK, 1)], extra=extra))
        b.append(f"<text class='m' x='{LABEL_X}' y='{cy + 4}' font-size='12' font-weight='500' letter-spacing='.14em' "
                 f"fill='{D.INKSOFT}' text-anchor='end'>GAME {g} · {m} MOVES</text>")
        if i < len(rows) - 1:
            b.append(f"<line x1='80' y1='{cy + 23}' x2='690' y2='{cy + 23}' stroke='{D.INKSOFT}' "
                     f"stroke-width='1.5' opacity='.25'/>")
    return D.svg(W, h, label(state), "".join(b))
