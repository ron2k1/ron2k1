"""The GitHub side of a move: which open issues are drops, and closing them with a result.

Every workflow run drains all open move issues in number order. A run that GitHub evicts from
the concurrency queue therefore loses nothing: the next run finds its issue still open.
"""
from __future__ import annotations

import json
import re
import subprocess

TITLE = re.compile(r"^\s*c4\|drop\|([1-7])\s*$")
PROFILE = "https://github.com/ron2k1"


def parse_title(title: str) -> int | None:
    """0-based column for a move title, else None."""
    m = TITLE.match(title or "")
    return int(m.group(1)) - 1 if m else None


def list_open_moves(repo: str, run=subprocess.run) -> list[dict]:
    """Open issues whose title is a drop, oldest first: [{number, col, actor}]."""
    cmd = ["gh", "issue", "list", "--repo", repo, "--state", "open", "--limit", "100",
           "--json", "number,title,author"]
    out = run(cmd, capture_output=True, text=True, check=True).stdout
    moves = []
    for it in json.loads(out or "[]"):
        col = parse_title(it.get("title", ""))
        if col is None:
            continue
        actor = (it.get("author") or {}).get("login") or "someone"
        moves.append({"number": int(it["number"]), "col": col, "actor": actor})
    return sorted(moves, key=lambda m: m["number"])


def close_issue(repo: str, number: int, message: str, run=subprocess.run) -> None:
    run(["gh", "issue", "close", str(number), "--repo", repo, "--comment", f"{message} See the board at {PROFILE}."],
        capture_output=True, text=True, check=True)
