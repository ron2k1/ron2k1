"""CLI used by the workflow.

    python -m connect4 drain --outcomes out.json   # play every open move issue, write files
    python -m connect4 close --outcomes out.json   # close those issues with their results
    python -m connect4 move --title 'c4|drop|3' --actor octocat --issue 12   # one move, local use
    python -m connect4 init | render
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib

from . import game as G
from . import issues as I
from . import readme as R
from .render import render_board

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = "ron2k1/ron2k1"


def _write_all(state: dict, root: pathlib.Path) -> None:
    game_dir = root / "game"
    game_dir.mkdir(exist_ok=True)
    G.save(game_dir / "state.json", state)
    board = root / R.board_path(state)
    board.write_text(render_board(state), encoding="utf-8", newline="\n")
    for old in game_dir.glob("board*.svg"):          # one board file per revision, never two
        if old != board:
            old.unlink()
    readme = root / "README.md"
    readme.write_text(R.rewrite(readme.read_text(encoding="utf-8"), state), encoding="utf-8", newline="\n")


def _output(**kv: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}<<C4EOF\n{v}\nC4EOF\n")


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="connect4")
    sub = ap.add_subparsers(dest="cmd", required=True)
    mv = sub.add_parser("move")
    mv.add_argument("--title", required=True)
    mv.add_argument("--actor", required=True)
    mv.add_argument("--issue", type=int, required=True)
    mv.add_argument("--budget", type=float, default=2.0)
    dr = sub.add_parser("drain")
    dr.add_argument("--outcomes", required=True)
    dr.add_argument("--repo", default=REPO)
    dr.add_argument("--budget", type=float, default=2.0)
    cl = sub.add_parser("close")
    cl.add_argument("--outcomes", required=True)
    cl.add_argument("--repo", default=REPO)
    sub.add_parser("init")
    sub.add_parser("render")
    for p in (mv, dr, cl, sub.choices["init"], sub.choices["render"]):
        p.add_argument("--root", default=str(ROOT))
    return ap


def main(argv: list[str] | None = None) -> int:
    a = _parser().parse_args(argv)
    root = pathlib.Path(a.root)
    if a.cmd == "init":
        _write_all(G.new_state(), root)
        return 0
    if a.cmd == "render":
        _write_all(G.load(root / "game" / "state.json"), root)
        return 0
    if a.cmd == "close":
        outcomes = json.loads(pathlib.Path(a.outcomes).read_text(encoding="utf-8"))
        for o in outcomes:
            I.close_issue(a.repo, o["number"], o["message"])
        print(f"closed {len(outcomes)} issue(s)")
        return 0
    if a.cmd == "drain":
        pending = I.list_open_moves(a.repo)
        state, outcomes = G.apply_issues(G.load(root / "game" / "state.json"), pending, budget=a.budget)
        changed = any(o["accepted"] for o in outcomes)
        if changed:
            _write_all(state, root)
        pathlib.Path(a.outcomes).write_text(json.dumps(outcomes, indent=2), encoding="utf-8")
        for o in outcomes:
            print(f"#{o['number']}: {o['message']}")
        _output(changed="1" if changed else "0", subject=G.commit_subject(outcomes) if changed else "")
        return 0
    col = I.parse_title(a.title)
    if col is None:
        print("not a move")
        _output(accepted="0", message="That title is not a move. Use the column links on the profile.",
                subject="c4: ignored")
        return 0
    state, out = G.apply_human_move(G.load(root / "game" / "state.json"), col, a.actor, a.issue, budget=a.budget)
    if out.accepted:
        _write_all(state, root)
    print(out.message)
    _output(accepted="1" if out.accepted else "0", message=out.message, subject=out.subject)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
