"""SVG primitives for the comic-issue look: palette, embedded fonts, halftone, panels, chips."""
from __future__ import annotations

import base64
import math
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
PAPER, PAPER2, INK, INKSOFT = "#fbfaf5", "#f2efe6", "#15151c", "#4a4a58"
RED, REDDEEP, BLUE, YELLOW = "#e0202f", "#b30e1e", "#2342d6", "#ffc400"


def esc(text: str) -> str:
    return escape(str(text), {"'": "&#39;"})


def _b64(name: str) -> str:
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def font_css() -> str:
    return ("@font-face{font-family:'Bangers';src:url(data:font/woff2;base64," + _b64("Bangers-Regular.woff2")
            + ") format('woff2')}"
            "@font-face{font-family:'JetBrains Mono';src:url(data:font/woff2;base64," + _b64("JetBrainsMono.woff2")
            + ") format('woff2')}"
            ".d{font-family:'Bangers',Impact,sans-serif}.m{font-family:'JetBrains Mono',Consolas,monospace}")


def defs(extra: str = "") -> str:
    return ("<defs><style>" + font_css() + "</style>"
            f"<pattern id='dots' width='9' height='9' patternUnits='userSpaceOnUse'>"
            f"<circle cx='1.5' cy='1.5' r='1' fill='{INK}' opacity='.07'/></pattern>"
            f"<pattern id='dotsp' width='9' height='9' patternUnits='userSpaceOnUse'>"
            f"<circle cx='1.5' cy='1.5' r='1' fill='{INK}' opacity='.32'/></pattern>"
            + extra + "</defs>")


def svg(width: int, height: int, label: str, body: str, extra_defs: str = "") -> str:
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {width} {height}' width='{width}' height='{height}' "
            f"role='img' aria-label='{esc(label)}'>" + defs(extra_defs) + body + "</svg>")


def panel(x: float, y: float, w: float, h: float, fill: str = PAPER, sh: int = 6, stroke: int = 3) -> str:
    return (f"<rect x='{x + sh}' y='{y + sh}' width='{w}' height='{h}' fill='{INK}'/>"
            f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{fill}' stroke='{INK}' stroke-width='{stroke}'/>")


def chip_width(text: str, size: int, pad: int) -> int:
    return int(len(text) * size * 0.62 + pad * 2)


def chip(x: float, y: float, text: str, fill: str = PAPER2, color: str = INK, size: int = 13, pad: int = 14,
         sh: int = 3) -> tuple[str, int]:
    w, h = chip_width(text, size, pad), size + 16
    out = (f"<rect x='{x + sh}' y='{y + sh}' width='{w}' height='{h}' fill='{INK}'/>"
           f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{fill}' stroke='{INK}' stroke-width='2.5'/>"
           f"<text class='m' x='{x + w / 2}' y='{y + h / 2 + size * 0.36:.1f}' font-size='{size}' font-weight='500' "
           f"text-anchor='middle' fill='{color}' letter-spacing='.04em'>{esc(text)}</text>")
    return out, w


def shadowed_text(x: float, y: float, text: str, size: int, fill: str, layers, cls: str = "d",
                  anchor: str = "start", extra: str = "") -> str:
    out = ""
    for dx, dy, col, op in layers:
        out += (f"<text class='{cls}' x='{x + dx}' y='{y + dy}' font-size='{size}' fill='{col}' opacity='{op}' "
                f"text-anchor='{anchor}' {extra}>{esc(text)}</text>")
    return out + (f"<text class='{cls}' x='{x}' y='{y}' font-size='{size}' fill='{fill}' text-anchor='{anchor}' "
                  f"{extra}>{esc(text)}</text>")


def star(cx: float, cy: float, ro: float, ri: float, n: int = 14, rot: float = 3) -> str:
    jit = [0, 6, -4, 3, -6, 5, -2, 4, -5, 2, 6, -3, 1, -4, 5, -1, 3, -6, 2, 4, -3, 6, -2, 1, -5, 3, 0, -4]
    pts = []
    for i in range(2 * n):
        r = (ro if i % 2 == 0 else ri) + jit[i % len(jit)] * ro / 178
        a = math.radians(rot + i * 180 / n)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
