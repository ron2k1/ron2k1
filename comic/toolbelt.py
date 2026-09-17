"""Four skill panels drawn from data/toolbelt.json (the resume's four groups)."""
from __future__ import annotations

import json

from . import draw as D

W, GAP, CHIP, PAD, ROWH, SHADOW = 880, 24, 12, 11, 32, 6
PW = (W - GAP - 2 - SHADOW) // 2        # two panels, origin offset 2, ink shadow inside the viewBox
BANDS = {"red": (D.RED, D.PAPER), "blue": (D.BLUE, D.PAPER), "yellow": (D.YELLOW, D.INK), "ink": (D.INK, D.YELLOW)}


def _layout(chips: list[str]) -> tuple[list[tuple[int, int, str]], int]:
    placed, x, y = [], 0, 0
    for c in chips:
        w = D.chip_width(c, CHIP, PAD)
        if x + w > PW - 36:
            x, y = 0, y + ROWH
        placed.append((x, y, c))
        x += w + 8
    return placed, 60 + y + ROWH + 16


def build(groups: list[dict]) -> str:
    layouts = [_layout(g["chips"]) for g in groups]
    row_h = [max(layouts[0][1], layouts[1][1]), max(layouts[2][1], layouts[3][1])]
    height = row_h[0] + row_h[1] + GAP + 10
    b = []
    for i, g in enumerate(groups):
        px, py = (i % 2) * (PW + GAP) + 2, (i // 2) * (row_h[0] + GAP) + 2
        band, tcol = BANDS[g["band"]]
        b.append(D.panel(px, py, PW, row_h[i // 2]))
        b.append(f"<rect x='{px}' y='{py}' width='{PW}' height='46' fill='{band}' stroke='{D.INK}' stroke-width='3'/>"
                 f"<rect x='{px}' y='{py}' width='{PW}' height='46' fill='url(#dotsp)'/>")
        b.append(f"<text class='d' x='{px + 16}' y='{py + 33}' font-size='24' fill='{tcol}' letter-spacing='.04em'>"
                 f"{D.esc(g['title'])}</text>")
        for x, y, c in layouts[i][0]:
            s, _ = D.chip(px + 16 + x, py + 60 + y, c, D.PAPER2, D.INK, size=CHIP, pad=PAD, sh=2)
            b.append(s)
    label = "The toolbelt: " + "; ".join(g["title"].title() + ": " + ", ".join(g["chips"]) for g in groups)
    return D.svg(W, height, label, "".join(b))


if __name__ == "__main__":
    groups = json.loads((D.ROOT / "data" / "toolbelt.json").read_text(encoding="utf-8"))
    D.write(D.ROOT / "assets" / "toolbelt.svg", build(groups))
    print("assets/toolbelt.svg written")
