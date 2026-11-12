"""Geometry figures for the Advanced Math lesson banks, drawn with cetz. (Not a bank.)

Every coordinate is worked out here, in Python; cetz only draws polylines,
dots, and labels. Lengths are in units of `unit` (1cm on a sheet; a slide
passes a bigger one), and labels take the text size around them.

    PREAMBLE                          the cetz import (graphs.PREAMBLE); a bank that draws sets its PREAMBLE to this
    sector(angle, shaded, label)      a circle with one sector, centered on the right: shaded (the rest
                                      white) or unshaded (the rest shaded); its angle labeled inside it
    crossing(angle, labels)           two lines crossing; `angle` is the left and right angles' measure;
                                      labels: {"left": markup, "top": ..., "right": ..., "bottom": ...}
    parallel(top, bottom, sides, below)  points on two parallel lines (name -> x), the segments
                                      `sides` (pairs of names) drawn, lengths `below` (pair -> markup)
"""
import math
from ..graphs import PREAMBLE, _num

R = 1.15                                        # a sector's circle radius
SHADE = "luma(175)"

def _pt(x, y):
    return f"({_num(x)}, {_num(y)})"

def _canvas(cmds, unit):
    body = "\n    ".join(cmds)
    return f"#box(cetz.canvas(length: {unit}, {{\n    import cetz.draw: *\n    {body}\n  }}))"

def _arc(r, a0, a1, n=48):
    """Points on a circle of radius r around the origin, from a0 to a1 degrees."""
    return [(r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def _poly(pts, extra=""):
    return f"line({', '.join(_pt(*p) for p in pts)}{extra})"

def sector(angle, shaded, label, unit="1cm"):
    """The sector of `angle` degrees is centered on the positive x direction.
    shaded: the sector is shaded and the rest of the circle white; else the
    sector is white and the rest shaded. The label sits inside the sector, or
    just outside the circle when the sector is too narrow for it."""
    a0, a1 = -angle / 2, angle / 2
    if shaded:
        gray = [(0, 0)] + _arc(R, a0, a1)
    else:
        gray = [(0, 0)] + _arc(R, a1, 360 + a0)
    cmds = [_poly(gray, f", close: true, fill: {SHADE}, stroke: none"),
            f"circle((0, 0), radius: {_num(R)}, stroke: 0.8pt)",
            _poly([_arc(R, a0, a0, 1)[0], (0, 0), _arc(R, a1, a1, 1)[0]], ", stroke: 0.8pt"),
            _poly(_arc(0.2, a0, a1), ", stroke: 0.6pt"),
            "circle((0, 0), radius: 0.045, fill: black, stroke: none)"]
    if angle >= 70:
        cmds.append(f"content({_pt(0.62 * R, 0)}, [{label}])")
    else:
        cmds.append(f'content({_pt(R + 0.12, 0)}, anchor: "west", [{label}])')
    return _canvas(cmds, unit)

def crossing(angle, labels, unit="1cm"):
    """Two lines crossing at the origin, symmetric about the x-axis: the left
    and right angles measure `angle` degrees, the top and bottom 180 - angle.
    Each label sits on its angle's bisector. Drawn between 50° and 130° (a
    figure not to scale past them), so every label fits between the lines."""
    angle = min(max(angle, 50), 130)
    h = math.radians(angle / 2)
    L = 1.9
    ends = [(L * math.cos(h), L * math.sin(h)), (L * math.cos(h), -L * math.sin(h))]
    cmds = [_poly([(-x, -y), (x, y)], ", stroke: 0.8pt") for x, y in ends]
    where = {"right": (1, 0, "west"), "left": (-1, 0, "east"), "top": (0, 1, "south"), "bottom": (0, -1, "north")}
    for pos, text in labels.items():
        dx, dy, anchor = where[pos]
        half = math.radians(angle / 2 if dx else 90 - angle / 2)
        # Far enough out that the label fits between the lines: its height (left, right)
        # or its width (top, bottom), estimated from its characters.
        across = 0.42 if dx else 0.2 * width(text) + 0.15
        d = max(0.18, across / 2 / math.tan(half))
        cmds.append(f'content({_pt(dx * d, dy * d)}, anchor: "{anchor}", padding: 2pt, [{text}])')
    return _canvas(cmds, unit)

def width(markup):
    """About how many characters wide a label shows: "$(2 B)°$" is 5."""
    return len(markup.replace("$", "").replace(" ", "").replace("degree", "°"))

def parallel(top, bottom, sides, below=None, height=2.0, unit="1cm"):
    """top, bottom: {name: x}, the points on the line y = height and on y = 0.
    The two segments along the lines carry an arrowhead at their middle (they're
    parallel); `sides` are the other segments; `below` labels a bottom segment's
    length under it."""
    cmds = []
    for pts, y in ((top, height), (bottom, 0)):
        xs = sorted(pts.values())
        cmds.append(_poly([(xs[0], y), (xs[-1], y)], ", stroke: 0.8pt"))
        mid = (xs[0] + xs[-1]) / 2
        cmds.append(_poly([(mid - 0.01, y), (mid + 0.12, y)],
                          ', stroke: 0.8pt, mark: (end: ">", fill: black, scale: 0.7)'))
    at = {n: (x, height) for n, x in top.items()} | {n: (x, 0) for n, x in bottom.items()}
    for a, b in sides:
        cmds.append(_poly([at[a], at[b]], ", stroke: 0.8pt"))
    for n, (x, y) in at.items():
        cmds.append(f'content({_pt(x, y)}, anchor: "{"south" if y else "north"}", padding: 4pt, [${n}$])')
    for (a, b), text in (below or {}).items():
        cmds.append(f'content({_pt((at[a][0] + at[b][0]) / 2, -0.5)}, anchor: "north", [{text}])')
    return _canvas(cmds, unit)
