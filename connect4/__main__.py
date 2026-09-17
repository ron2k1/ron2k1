"""CLI used by the workflow: python -m connect4 move --title 'c4|drop|3' --actor octocat --issue 12"""
from __future__ import annotations

import argparse
import os
import pathlib
import re

from . import game as G
from . import readme as R
from .render import render_board

ROOT = pathlib.Path(__file__).resolve().parents[1]
TITLE = re.compile(r"^\s*c4\|drop\|([1-7])\s*$")


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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="connect4")
    sub = ap.add_subparsers(dest="cmd", required=True)
    mv = sub.add_parser("move")
    mv.add_argument("--title", required=True)
    mv.add_argument("--actor", required=True)
    mv.add_argument("--issue", type=int, required=True)
    mv.add_argument("--budget", type=float, default=2.0)
    mv.add_argument("--root", default=str(ROOT))
    for name in ("init", "render"):
        sub.add_parser(name).add_argument("--root", default=str(ROOT))
    a = ap.parse_args(argv)
    root = pathlib.Path(a.root)
    if a.cmd == "init":
        (root / "game").mkdir(exist_ok=True)
        _write_all(G.new_state(), root)
        return 0
    if a.cmd == "render":
        _write_all(G.load(root / "game" / "state.json"), root)
        return 0
    m = TITLE.match(a.title)
    if not m:
        print("not a move")
        _output(accepted="0", message="That title is not a move. Use the column links on the profile.",
                subject="c4: ignored")
        return 0
    state = G.load(root / "game" / "state.json")
    state, out = G.apply_human_move(state, int(m.group(1)) - 1, a.actor, a.issue, budget=a.budget)
    if out.accepted:
        _write_all(state, root)
    print(out.message)
    _output(accepted="1" if out.accepted else "0", message=out.message, subject=out.subject)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
