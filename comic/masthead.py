"""The profile masthead: comic splash with the diagonal ink split and the game burst."""
from __future__ import annotations

import math

from . import draw as D

W, H = 880, 300
CX, CY = 715, 150
LABEL = "The Incredible Ronil Basu, Issue 27. Data science and AI, Rutgers 2027. Now with a game."


def build() -> str:
    rays = "".join(
        f"<line x1='{CX}' y1='{CY}' x2='{CX + 520 * math.cos(math.radians(a)):.0f}' "
        f"y2='{CY + 520 * math.sin(math.radians(a)):.0f}' stroke='{D.PAPER}' stroke-width='2' opacity='.13'/>"
        for a in range(0, 360, 9))
    clip = "<clipPath id='redzone'><polygon points='490,0 880,0 880,300 637,300'/></clipPath>"
    b = [
        f"<rect width='{W}' height='{H}' fill='{D.PAPER}'/><rect width='{W}' height='{H}' fill='url(#dots)'/>",
        f"<polygon points='481,0 880,0 880,300 628,300' fill='{D.INK}'/>",
        f"<polygon points='490,0 880,0 880,300 637,300' fill='{D.REDDEEP}'/>"
        f"<polygon points='490,0 880,0 880,300 637,300' fill='url(#dotsp)'/>",
        f"<g clip-path='url(#redzone)'>{rays}</g>",
        f"<rect x='42' y='28' width='8' height='8' fill='{D.RED}'/>",
        f"<text class='m' x='60' y='36' font-size='10' font-weight='500' letter-spacing='.18em' fill='{D.INKSOFT}'>"
        "ISSUE #27 · GITHUB PROFILE · NEW BRUNSWICK, NJ</text>",
        "<g transform='rotate(-2 42 150)'>",
        D.shadowed_text(42, 124, "THE INCREDIBLE", 46, D.INK, [(5, 5, D.RED, .45), (2.5, 2.5, D.PAPER, 1)],
                        extra="letter-spacing='.02em'"),
        D.shadowed_text(41, 222, "RONIL BASU", 112, D.RED, [(5, 5, D.INK, 1), (2.5, 2.5, D.PAPER, 1)],
                        extra="letter-spacing='.01em'"),
        "</g>",
    ]
    x = 44
    for t, f, c in (("DATA SCIENCE × AI", D.YELLOW, D.INK), ("RUTGERS '27", D.PAPER2, D.INK),
                    ("BUILD · SHIP · REPEAT", D.BLUE, D.PAPER)):
        s, w = D.chip(x, 246, t, f, c, size=12, pad=12, sh=3)
        b.append(s)
        x += w + 12
    b.append(
        f"<g transform='rotate(4 {CX} {CY})'><polygon points='{D.star(CX + 4, CY + 4, 130, 104)}' fill='{D.INK}'/>"
        f"<polygon points='{D.star(CX, CY, 130, 104)}' fill='{D.YELLOW}' stroke='{D.INK}' stroke-width='3'/>"
        f"<text class='d' x='{CX}' y='{CY - 16}' font-size='22' text-anchor='middle' fill='{D.INK}' "
        "letter-spacing='.04em'>NOW WITH</text>"
        f"<text class='d' x='{CX}' y='{CY + 27}' font-size='44' text-anchor='middle' fill='{D.RED}' stroke='{D.INK}' "
        "stroke-width='1.2'>A GAME</text>"
        f"<text class='m' x='{CX - 6}' y='{CY + 50}' font-size='9' font-weight='500' text-anchor='middle' fill='{D.INK}' "
        "letter-spacing='.14em'>SCROLL DOWN</text>"
        f"<polygon points='{CX + 38},{CY + 43} {CX + 48},{CY + 43} {CX + 43},{CY + 51}' fill='{D.INK}'/></g>")
    return D.svg(W, H, LABEL, "".join(b), clip)


if __name__ == "__main__":
    D.write(D.ROOT / "assets" / "masthead.svg", build())
    print("assets/masthead.svg written")
