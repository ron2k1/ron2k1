"""Draw game/board-<rev>.svg in the comic style.

The grid runs from panel edge to panel edge so the README's row of seven drop buttons (each 14%
wide, over a 100%-wide board) lands on the columns: column c is centred at OX + (c + 1/2) * CELL,
which stays within 10 px of the button centre at W * (0.07 + 0.14 * c).
"""
from __future__ import annotations

from comic import draw as D

W, H = 720, 740
PX, PY, PW, PH = 8, 8, 704, 724          # panel; its 6 px shadow stays inside the viewBox
OX, OY, CELL = 10, 88, 100               # grid origin and cell pitch
NAMES = {"R": "RED", "B": "BLUE"}
FILLS = {".": D.PAPER, "R": D.RED, "B": D.BLUE}


def column_center(c: int) -> float:
    return OX + c * CELL + CELL / 2


def status_text(state: dict) -> str:
    if state.get("finished"):
        r = state.get("result")
        return "GAME OVER · DRAW" if r == "draw" else f"GAME OVER · {NAMES[r]} WINS"
    return f"MOVE {len(state['moves']):02d} · {NAMES[state['to_play']]} TO PLAY"


def render_board(state: dict) -> str:
    grid_bottom = OY + 6 * CELL
    b = [
        D.panel(PX, PY, PW, PH),
        f"<rect x='{PX}' y='{PY}' width='{PW}' height='64' fill='{D.RED}' stroke='{D.INK}' stroke-width='3'/>"
        f"<rect x='{PX}' y='{PY}' width='{PW}' height='64' fill='url(#dotsp)'/>",
        f"<text class='d' x='30' y='55' font-size='40' fill='{D.PAPER}' letter-spacing='.03em'>CONNECT FOUR</text>",
        D.chip(520, 24, "YOU: RED · BOT: BLUE", D.PAPER2, D.INK, size=12, pad=12)[0],
        # The panel border is the grid's side wall; two ink bars close it at the top and bottom.
        f"<rect x='{PX + 1.5}' y='{OY}' width='{PW - 3}' height='{6 * CELL}' fill='{D.PAPER2}'/>",
        f"<rect x='{PX + 1.5}' y='{OY - 1.5}' width='{PW - 3}' height='3' fill='{D.INK}'/>",
        f"<rect x='{PX + 1.5}' y='{grid_bottom - 1.5}' width='{PW - 3}' height='3' fill='{D.INK}'/>",
    ]
    last = state.get("last_move") or {}
    for r, row in enumerate(state["board"]):
        for c, v in enumerate(row):
            cx, cy = column_center(c), OY + r * CELL + CELL / 2
            if last.get("row") == r and last.get("col") == c:
                b.append(f"<circle cx='{cx}' cy='{cy}' r='44' fill='{D.YELLOW}'/>")
            b.append(f"<circle cx='{cx + 3}' cy='{cy + 3}' r='36' fill='{D.INK}' opacity='{.25 if v == '.' else 1}'/>")
            b.append(f"<circle cx='{cx}' cy='{cy}' r='36' fill='{FILLS[v]}' stroke='{D.INK}' stroke-width='3'/>")
            if v != ".":
                b.append(f"<circle cx='{cx - 10}' cy='{cy - 10}' r='8' fill='{D.PAPER}' opacity='.55'/>")
    y = grid_bottom + 26
    b.append(f"<text class='m' x='{OX + 10}' y='{y}' font-size='13' font-weight='500' letter-spacing='.14em' "
             f"fill='{D.INKSOFT}'>{status_text(state)}</text>")
    bot = state.get("last_bot")
    if bot:
        b.append(f"<text class='m' x='{PX + PW - 12}' y='{y}' font-size='13' font-weight='500' letter-spacing='.14em' "
                 f"fill='{D.INKSOFT}' text-anchor='end'>BOT · NEGAMAX · DEPTH {bot['depth']} "
                 f"· {bot['seconds']:.1f} S</text>")
    label = f"Connect Four, game {state['game_no']}, {status_text(state).lower()}"
    return D.svg(W, H, label, "".join(b))
