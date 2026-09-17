"""Rewrite the README region between the c4 markers from the game state."""
from __future__ import annotations

from urllib.parse import quote

START, END = "<!-- c4:start -->", "<!-- c4:end -->"
BODY = quote("Press Submit new issue. The bot answers here within a minute.", safe="")
NAMES = {"R": "Red", "B": "Blue"}


def board_path(state: dict) -> str:
    """One file per revision: a new path is the only cache key every proxy in the chain respects."""
    return f"game/board-{state['revision']}.svg"


def issue_link(col: int, repo: str = "ron2k1/ron2k1") -> str:
    return f"https://github.com/{repo}/issues/new?title=c4%7Cdrop%7C{col + 1}&body={BODY}"


def _alt(state: dict) -> str:
    if state["finished"]:
        r = state["result"]
        return (f"Connect Four, game {state['game_no']} over, "
                + ("draw" if r == "draw" else f"{NAMES[r].lower()} wins"))
    return (f"Connect Four, game {state['game_no']}, move {len(state['moves'])}, "
            f"{NAMES[state['to_play']].lower()} to play")


BUTTON_WIDTH = "14%"     # seven of these fill 98% of the README column, over the 100%-wide board


def button_row(repo: str = "ron2k1/ron2k1") -> str:
    """Seven linked drop buttons on ONE line with no whitespace between anchors, or the browser draws gaps."""
    return "".join(f'<a href="{issue_link(c, repo)}"><img src="assets/drop-{c + 1}.svg" width="{BUTTON_WIDTH}" '
                   f'alt="Drop in column {c + 1}"></a>' for c in range(7))


def region(state: dict, repo: str = "ron2k1/ron2k1") -> str:
    rec = state["record"]
    record = f"Humans {rec['humans']}, bot {rec['bot']}, draws {rec['draws']}"
    if state["finished"]:
        r = state["result"]
        head = (("Draw" if r == "draw" else f"{NAMES[r]} wins")
                + f" game {state['game_no']} · Next drop starts game {state['game_no'] + 1}")
    else:
        head = "Red to play" if state["to_play"] == "R" else "Bot is thinking"
        human = next((m["by"] for m in reversed(state["moves"]) if m.get("actor") == "R"), None)
        if human:
            head += f" · Last move by @{human}"
    top = sorted(state["movers"].items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    movers = " · Most moves: " + ", ".join(f"@{u} ({n})" for u, n in top) if top else ""
    # The buttons and the board share one paragraph so the board sits right under the buttons.
    return ("Red is you. Tap a column to drop.\n\n"
            f"{button_row(repo)}\n"
            f'<img src="{board_path(state)}" alt="{_alt(state)}" width="100%">\n\n'
            f"{head} · {record}{movers}\n")


def rewrite(text: str, state: dict, repo: str = "ron2k1/ron2k1") -> str:
    a, b = text.find(START), text.find(END)
    if a < 0 or b < 0 or b < a:
        raise ValueError("README is missing the c4 markers")
    return text[: a + len(START)] + "\n" + region(state, repo) + text[b:]
