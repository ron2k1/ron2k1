"""One human move plus the bot's answer, applied to the JSON state."""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

from . import engine as E
from .bot import choose_move
from .hall import ON_THE_WALL


@dataclass(frozen=True)
class Outcome:
    accepted: bool
    message: str
    subject: str


def new_state(game_no: int = 1, record: dict | None = None, movers: dict | None = None,
              last_game: dict | None = None, hall: list | None = None, revision: int = 0) -> dict:
    return {"game_no": game_no, "board": ["." * E.COLS for _ in range(E.ROWS)], "to_play": E.RED, "moves": [],
            "finished": False, "result": None, "last_move": None, "last_bot": None,
            "record": record or {"humans": 0, "bot": 0, "draws": 0}, "last_game": last_game,
            "movers": movers or {}, "hall": hall or [], "revision": revision}


def load(path: str | pathlib.Path) -> dict:
    state = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    state.setdefault("hall", [])          # states written before the wall existed
    return state


def save(path: str | pathlib.Path, state: dict) -> None:
    pathlib.Path(path).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def _drop(state: dict, pos: E.Position, col: int, by: str, issue: int | None, actor: str) -> E.Position:
    nxt = E.play(pos, col)
    state["board"] = E.to_rows(nxt)
    state["to_play"] = E.to_play(nxt)
    state["moves"].append({"col": col, "by": by, "issue": issue, "actor": actor})
    state["last_move"] = {"row": E.ROWS - E.column_height(nxt, col), "col": col}
    return nxt


def _finish(state: dict, pos: E.Position) -> bool:
    w = E.winner(pos)
    if w:
        state["finished"], state["result"] = True, w
        state["record"]["humans" if w == E.RED else "bot"] += 1
        if w == E.RED:                     # moves[-1] is the red drop that just won, by the issue author
            state["hall"].append({"game_no": state["game_no"], "by": state["moves"][-1]["by"],
                                  "moves": len(state["moves"])})
        return True
    if E.is_draw(pos):
        state["finished"], state["result"] = True, "draw"
        state["record"]["draws"] += 1
        return True
    return False


def apply_human_move(state: dict, col: int, actor: str, issue: int | None, budget: float = 2.0) -> tuple[dict, Outcome]:
    if not isinstance(col, int) or not 0 <= col < E.COLS:
        return state, Outcome(False, "That is not a column between 1 and 7. Nothing changed.", "c4: rejected move")
    st = json.loads(json.dumps(state))
    if st["finished"]:
        last = st["moves"][-1] if st["moves"] else {}
        st = new_state(game_no=st["game_no"] + 1, record=st["record"], movers=st["movers"],
                       last_game={"game_no": st["game_no"], "result": st["result"], "moves": len(st["moves"]),
                                  "winning_move_by": None if st["result"] == "draw" else last.get("by")},
                       hall=st["hall"], revision=st["revision"])
    pos = E.from_rows(st["board"])
    if E.to_play(pos) != E.RED:
        return state, Outcome(False, "It is the bot's turn. Try again in a minute.", "c4: rejected move")
    if not E.can_play(pos, col):
        return state, Outcome(False, f"Column {col + 1} is full. Pick another one.", "c4: rejected move")
    g = st["game_no"]
    pos = _drop(st, pos, col, actor, issue, E.RED)
    st["movers"][actor] = st["movers"].get(actor, 0) + 1
    st["revision"] += 1
    subject = f"c4: game {g} move {len(st['moves'])} by @{actor}"
    if _finish(st, pos):
        if st["result"] == E.RED:
            return st, Outcome(True, f"@{actor} dropped in column {col + 1} and won game {g}. {ON_THE_WALL} "
                                     f"The next drop starts game {g + 1}.", subject)
        return st, Outcome(True, f"@{actor} dropped in column {col + 1} and drew game {g}. "
                                 f"The next drop starts game {g + 1}.", subject)
    reply = choose_move(pos, budget=budget)
    pos = _drop(st, pos, reply.col, "bot", None, E.BLUE)
    st["last_bot"] = {"col": reply.col, "depth": reply.depth, "nodes": reply.nodes, "seconds": round(reply.seconds, 2)}
    if _finish(st, pos):
        what = "won" if st["result"] == E.BLUE else "drew"
        return st, Outcome(True, f"@{actor} dropped in column {col + 1}. The bot answered in column {reply.col + 1} "
                                 f"and {what} game {g}. The next drop starts game {g + 1}.", subject)
    return st, Outcome(True, f"@{actor} dropped in column {col + 1}. The bot answered in column {reply.col + 1} "
                             f"(depth {reply.depth}, {reply.seconds:.1f} s). Red to play.", subject)


def apply_issues(state: dict, issues: list[dict], budget: float = 2.0) -> tuple[dict, list[dict]]:
    """Apply every open move issue in order. Returns the new state and one outcome dict per issue."""
    outcomes = []
    for it in issues:
        state, out = apply_human_move(state, it["col"], it["actor"], it["number"], budget=budget)
        outcomes.append({"number": it["number"], "actor": it["actor"], "accepted": out.accepted,
                         "message": out.message, "subject": out.subject})
    return state, outcomes


def commit_subject(outcomes: list[dict]) -> str:
    accepted = [o for o in outcomes if o["accepted"]]
    if len(accepted) == 1:
        return accepted[0]["subject"]
    actors = list(dict.fromkeys(o["actor"] for o in accepted))
    return f"c4: {len(accepted)} moves by " + ", ".join(f"@{a}" for a in actors)
