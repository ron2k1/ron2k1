"""Draw assets/drop-1.svg to drop-7.svg: the tappable column buttons that sit over the board.

Each one is wrapped in an issue link by connect4/readme.py. Seven at 14% of the README column
land over the seven columns of the 100%-wide board (see connect4/render.py for the geometry).
"""
from __future__ import annotations

from . import draw as D

W, H = 100, 84


def build(n: int) -> str:
    body = (D.panel(3, 3, 88, 72, fill=D.YELLOW)
            + D.shadowed_text(47, 54, str(n), 46, D.INK, [(2.5, 2.5, D.RED, 1)], anchor="middle")
            + f"<polygon points='36,60 58,60 47,72' fill='{D.RED}' stroke='{D.INK}' stroke-width='2.5' "
              "stroke-linejoin='round'/>")
    return D.svg(W, H, f"Drop in column {n}", body, mono=False)


if __name__ == "__main__":
    for n in range(1, 8):
        D.write(D.ROOT / "assets" / f"drop-{n}.svg", build(n))
    print("assets/drop-1.svg to drop-7.svg written")
