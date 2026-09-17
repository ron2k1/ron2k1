"""Draw game/board.svg in the comic style."""
from __future__ import annotations

from comic import draw as D

W, H = 720, 724
OX, OY, CELL = 44, 126, 90
NAMES = {"R": "RED", "B": "BLUE"}
FILLS = {".": D.PAPER, "R": D.RED, "B": D.BLUE}


def status_text(state: dict) -> str:
    if state.get("finished"):
        r = state.get("result")
        return "GAME OVER · DRAW" if r == "draw" else f"GAME OVER · {NAMES[r]} WINS"
    return f"MOVE {len(state['moves']):02d} · {NAMES[state['to_play']]} TO PLAY"


def render_board(state: dict) -> str:
    b = [
        D.panel(8, 8, 698, 700),
        f"<rect x='8' y='8' width='698' height='64' fill='{D.RED}' stroke='{D.INK}' stroke-width='3'/>"
        f"<rect x='8' y='8' width='698' height='64' fill='url(#dotsp)'/>",
        f"<text class='d' x='30' y='55' font-size='40' fill='{D.PAPER}' letter-spacing='.03em'>CONNECT FOUR</text>",
        D.chip(470, 24, "YOU: RED · BOT: BLUE", D.PAPER2, D.INK, size=12, pad=12)[0],
    ]
    for c in range(7):
        b.append(f"<text class='d' x='{OX + c * CELL + CELL / 2}' y='{OY - 14}' font-size='28' text-anchor='middle' "
                 f"fill='{D.INK}'>{c + 1}</text>")
    b.append(f"<rect x='{OX}' y='{OY}' width='{7 * CELL}' height='{6 * CELL}' fill='{D.PAPER2}' stroke='{D.INK}' "
             "stroke-width='3'/>")
    last = state.get("last_move") or {}
    for r, row in enumerate(state["board"]):
        for c, v in enumerate(row):
            cx, cy = OX + c * CELL + CELL / 2, OY + r * CELL + CELL / 2
            if last.get("row") == r and last.get("col") == c:
                b.append(f"<circle cx='{cx}' cy='{cy}' r='40' fill='{D.YELLOW}'/>")
            b.append(f"<circle cx='{cx + 3}' cy='{cy + 3}' r='33' fill='{D.INK}' opacity='{.25 if v == '.' else 1}'/>")
            b.append(f"<circle cx='{cx}' cy='{cy}' r='33' fill='{FILLS[v]}' stroke='{D.INK}' stroke-width='3'/>")
            if v != ".":
                b.append(f"<circle cx='{cx - 9}' cy='{cy - 9}' r='7' fill='{D.PAPER}' opacity='.55'/>")
    b.append(f"<text class='m' x='44' y='694' font-size='13' font-weight='500' letter-spacing='.14em' "
             f"fill='{D.INKSOFT}'>{status_text(state)}</text>")
    bot = state.get("last_bot")
    if bot:
        b.append(f"<text class='m' x='674' y='694' font-size='13' font-weight='500' letter-spacing='.14em' "
                 f"fill='{D.INKSOFT}' text-anchor='end'>BOT · NEGAMAX ALPHA-BETA · DEPTH {bot['depth']} "
                 f"· {bot['seconds']:.1f} S</text>")
    label = f"Connect Four, game {state['game_no']}, {status_text(state).lower()}"
    return D.svg(W, H, label, "".join(b))
