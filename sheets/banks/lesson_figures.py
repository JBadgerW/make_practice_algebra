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
    mapping(domain, range_, arrows)   Lesson 21: a mapping diagram, two ovals of members and arrows
    rule_mapping(left, right, rule)   Lesson 21: a mapping by a rule, x ∈ ℝ -> x + 2
    number_line(lo, hi, pieces, dots) Lesson 22: a number line, blank or with a graph drawn on it
    triangles(tris)                   Lesson 3: triangles with sides labeled and angles marked (arcs, right angles)
    nested(outer, foot, top, labels)  Lesson 3: a right triangle with a segment inside it, labeled and marked
    construction(prims, key)          Lesson 4: a figure and its compass construction (shown on the key only), true size
    protractor(rays, vertex)          Lesson 4: rays from the center of a protractor with both scales
    solid(w, d, h, names, edges)      Lesson 5: a rectangular solid, corners and edges labeled, its diagonal drawn on the key
    altitude(names)                   Lesson 8: a right triangle and the altitude to its hypotenuse, vertices named
    transversals(labels, ratio)       Lesson 8: three parallel lines cut by two transversals, segments labeled
    bisector(names, lengths, labels)  Lesson 8: a triangle and an angle's bisector, to scale, sides labeled
    marked(pts, chains, ...)          Lesson 9: points joined by straight chains, vertices named, and the
                                      equal parts marked: ticks, arcs, right-angle boxes, a circle on a shared side
    circled(center, r, chains, ...)   Lesson 11: a circle with chains of segments, angle arcs, and labels, all
                                      at coordinates the bank works out (in cm)
    polygon(n, triangulated)          Lesson 12: a regular n-gon, a vertex at the left; triangulated, the
                                      diagonals from that vertex drawn and the triangles numbered
"""
import math
from ..graphs import PREAMBLE, SLIDE_STATE, SLIDE_TEXT, INK, _num, _minus

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

# ------------------------------------------------------------------
# Lesson 2: bases of solids, and two solids
# ------------------------------------------------------------------
def _dash(a, b):
    return _poly([a, b], ', stroke: (thickness: 0.7pt, dash: "dashed")')

def _right_angle(corner, u, v, k=0.18):
    """A right-angle mark at corner, its sides along unit vectors u and v."""
    (x, y), (ux, uy), (vx, vy) = corner, u, v
    return _poly([(x + k * ux, y + k * uy), (x + k * (ux + vx), y + k * (uy + vy)), (x + k * vx, y + k * vy)],
                 ", stroke: 0.6pt")

def _label(x, y, text, anchor="center"):
    return f'content({_pt(x, y)}, anchor: "{anchor}", padding: 2pt, [{text}])'

def capped_base(w, h, right, left, labels, size=4.2, unit="1cm"):
    """A w-by-h rectangle with a semicircle on its right side (right: True) and,
    on its left (left: 0 none, h a semicircle on that side, d > h a semicircle
    of diameter d standing on the bottom, the rest of its diameter a segment
    above the rectangle). labels: dict(top, bottom, side, rise, radius) markup,
    each optional: side labels the straight left or right side, rise the
    segment above the rectangle, radius a drawn radius of a semicircle."""
    span_x = w + (h / 2 if right else 0) + (left / 2 if left else 0)
    span_y = max(h, left)
    k = size / max(span_x, 1.4 * span_y)
    W, H, D = w * k, h * k, left * k
    cmds = [_poly([(0, H), (W, H)], ", stroke: 0.8pt"), _poly([(0, 0), (W, 0)], ", stroke: 0.8pt")]
    if right:
        cmds.append(_poly([(W + x, H / 2 + y) for x, y in _arc(H / 2, -90, 90)], ", stroke: 0.8pt"))
        cmds.append(_dash((W, 0), (W, H)))
    else:
        cmds.append(_poly([(W, 0), (W, H)], ", stroke: 0.8pt"))
        cmds += [_right_angle((W, H), (-1, 0), (0, -1)), _right_angle((W, 0), (-1, 0), (0, 1))]
    if left:
        cmds.append(_poly([(x, D / 2 + y) for x, y in _arc(D / 2, 90, 270)], ", stroke: 0.8pt"))
        cmds.append(_dash((0, 0), (0, H)))
        if left > h:
            cmds.append(_poly([(0, H), (0, D)], ", stroke: 0.8pt"))
            cmds.append(_right_angle((0, H), (1, 0), (0, 1)))
    else:
        cmds.append(_poly([(0, 0), (0, H)], ", stroke: 0.8pt"))
        cmds += [_right_angle((0, H), (1, 0), (0, -1)), _right_angle((0, 0), (1, 0), (0, 1))]
    if labels.get("top"):
        cmds.append(_label(W / 2, H, labels["top"], "south"))
    if labels.get("bottom"):
        cmds.append(_label(W / 2, 0, labels["bottom"], "north"))
    if labels.get("side"):
        cmds.append(_label(W, H / 2, labels["side"], "west") if not right else _label(0, H / 2, labels["side"], "east"))
    if labels.get("rise"):
        cmds.append(_label(0, (H + D) / 2, labels["rise"], "west"))
    if labels.get("radius"):
        cx, cy, r, a = (W, H / 2, H / 2, 40) if right else (0, D / 2, D / 2, 140)
        ex, ey = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        cmds += [f"circle({_pt(cx, cy)}, radius: 0.06, fill: black, stroke: none)",
                 _poly([(cx, cy), (ex, ey)], ", stroke: 0.7pt"),
                 _label((cx + ex) / 2, (cy + ey) / 2, labels["radius"], "north-west" if right else "north-east")]
    return _canvas(cmds, unit)

def prism(cells, side, length, size=4.4, unit="1cm"):
    """A right prism whose base is made of unit squares (cells: (col, row)), drawn
    in oblique projection, the length going back and up to the right. Every
    edge of the front face is labeled `side`; the top-left receding edge, `length`."""
    cs = set(cells)
    n = max(max(c, r) for c, r in cs) + 1
    k = size / (n + 1.2)
    dx, dy = 0.55, 0.45                                  # the receding direction, per unit of length drawn
    depth = 1.6 / k                                      # drawn depth, in squares
    # The boundary edges, each with its outward direction.
    edges = []
    for c, r in cs:
        for (oc, orow), seg in (((0, 1), ((c, r + 1), (c + 1, r + 1))), ((0, -1), ((c, r), (c + 1, r))),
                                ((1, 0), ((c + 1, r), (c + 1, r + 1))), ((-1, 0), ((c, r), (c, r + 1)))):
            if (c + oc, r + orow) not in cs:
                edges.append(((oc, orow), seg))
    P = lambda x, y, z=0: (k * (x + z * dx), k * (y + z * dy))
    faces = []
    for (oc, orow), (a, b) in edges:
        if oc > 0 or orow > 0:                           # facing up or right: seen
            quad = [P(*a), P(*b), P(*b, depth), P(*a, depth)]
            faces.append((-(a[0] + b[0] + a[1] + b[1]), quad, "luma(150)" if oc else "luma(215)"))
    cmds = [_poly(q, f", close: true, fill: {f}, stroke: 0.6pt") for _, q, f in sorted(faces, key=lambda t: t[0])]
    for c, r in cs:
        cmds.append(_poly([P(c, r), P(c + 1, r), P(c + 1, r + 1), P(c, r + 1)],
                          ", close: true, fill: luma(240), stroke: none"))
    for _, (a, b) in edges:
        cmds.append(_poly([P(*a), P(*b)], ", stroke: 0.8pt"))
        (ox, oy) = _
        mx, my = P((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        cmds.append(_label(mx - 0.2 * ox, my - 0.2 * oy, side))          # inside the front face, as the book does
    # The length, along the receding edge from the top-left corner of the topmost row.
    top = max(r for _, r in cs)
    c0 = min(c for c, r in cs if r == top)
    a, b = P(c0, top + 1), P(c0, top + 1, depth)
    cmds.append(_label((a[0] + b[0]) / 2 - 0.1, (a[1] + b[1]) / 2 + 0.1, length, "south-east"))
    return _canvas(cmds, unit)

def oblique_cylinder(radius, height, unit="1cm"):
    """A circular cylinder leaning right: its top's radius labeled, its height marked H at the right."""
    rx, ry, h, s = 1.2, 0.35, 2.2, 0.6
    bottom = [(rx * math.cos(math.radians(t)), ry * math.sin(math.radians(t))) for t in range(0, 361, 6)]
    front = [p for p in bottom if p[1] <= 0.0001]
    back = [p for p in bottom if p[1] >= -0.0001]
    top = [(x + s, y + h) for x, y in bottom]
    cmds = [_poly(top, ", close: true, fill: luma(225), stroke: 0.8pt"),
            _poly(sorted(front), ", stroke: 0.8pt"),
            _poly(sorted(back), ', stroke: (thickness: 0.6pt, dash: "dashed")'),
            _poly([(-rx, 0), (-rx + s, h)], ", stroke: 0.8pt"), _poly([(rx, 0), (rx + s, h)], ", stroke: 0.8pt"),
            f"circle({_pt(s, h)}, radius: 0.05, fill: black, stroke: none)",
            _poly([(s, h), (s + rx * 0.97, h + 0.05)], ", stroke: 0.8pt"),
            _label(s + rx / 2, h + ry, radius, "south"),
            _poly([(rx + s + 0.35, 0), (rx + s + 0.35, h)],
                  ', stroke: 0.6pt, mark: (start: ">", end: ">", fill: black, scale: 0.6)'),
            _label(rx + s + 0.35, h / 2, height, "west")]
    return _canvas(cmds, unit)

def wedge_base(leg, side, angle, size=4.2, unit="1cm"):
    """A right triangle (legs `leg` along the bottom and `side` up the right) joined
    along that right leg to a sector of radius `side`, its center at the top, its
    angle measured from the leg toward the right. The arguments are (value, markup)."""
    (a, la), (b, lb), t = leg, side, angle
    k = size / max(a + b * math.sin(math.radians(t)), 1.6 * b)
    A, Bv = a * k, b * k
    apex = (A, Bv)
    arc = [(A + Bv * math.sin(math.radians(u)), Bv - Bv * math.cos(math.radians(u))) for u in range(0, int(t) + 1, 2)]
    cmds = [_poly([(A, Bv), (0, 0), (A, 0)], ", stroke: 0.8pt"),
            _dash((A, 0), apex),
            _poly(arc, ", stroke: 0.8pt"), _poly([apex, arc[-1]], ", stroke: 0.8pt"),
            _right_angle((A, 0), (-1, 0), (0, 1)),
            _label(A / 2, 0, la, "north"), _label(A, Bv / 3, lb, "east"),
            _label((A + arc[-1][0]) / 2, (Bv + arc[-1][1]) / 2, lb, "south-west"),
            _label(A + 0.5 * Bv * math.sin(math.radians(t / 2)), Bv - 0.5 * Bv * math.cos(math.radians(t / 2)),
                   f"${t:g}°$")]
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 21: mapping diagrams
# ------------------------------------------------------------------
def _oval(cx, cy, rx, ry, n=60):
    return _poly([(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                  for i in range(n + 1)], ", stroke: 0.8pt")

def _arrow(a, b, gap=0.22):
    """A segment from a to b, stopped short of each label, with its arrowhead partway along."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    p, q = (x0 + gap * ux, y0 + gap * uy), (x1 - gap * ux, y1 - gap * uy)
    mid = (p[0] + 0.62 * (q[0] - p[0]), p[1] + 0.62 * (q[1] - p[1]))
    return [_poly([p, q], ", stroke: 0.8pt"),
            _poly([(mid[0] - 0.01 * ux, mid[1] - 0.01 * uy), mid],
                  ', stroke: 0.8pt, mark: (end: "stealth", fill: black, scale: 0.8)')]

def mapping(domain, range_, arrows, names=True, unit="1cm"):
    """A mapping diagram: the domain's members (markup) listed down a left oval, the
    range's down a right one, an arrow for each (domain index, range index) pair;
    names: "Domain" and "Range" under the ovals."""
    step = 0.62
    def column(items):
        top = step * (len(items) - 1) / 2
        return [top - step * i for i in range(len(items))]
    ly, ry = column(domain), column(range_)
    lx, rx = 0.0, 2.9
    h = max(len(domain), len(range_), 2) * step / 2 + 0.25
    cmds = [_oval(lx, 0, 0.55, step * len(domain) / 2 + 0.3), _oval(rx, 0, 0.5, step * len(range_) / 2 + 0.3)]
    for x, ys, items in ((lx, ly, domain), (rx, ry, range_)):
        for y, t in zip(ys, items):
            cmds.append(_label(x, y, t))
    for i, j in arrows:
        cmds += _arrow((lx, ly[i]), (rx, ry[j]))
    if names:
        low = -max(step * len(domain) / 2 + 0.3, step * len(range_) / 2 + 0.3)
        cmds += [_label(lx, low, "Domain", "north"), _label(rx, low, "Range", "north")]
    return _canvas(cmds, unit)

def rule_mapping(left, right, rule, unit="1cm"):
    """A mapping by a rule: one oval holding `left` (x ∈ ℝ), an arrow labeled `rule`, one holding `right`."""
    cmds = [_oval(0, 0, 0.95, 0.42), _oval(4.4, 0, 0.95, 0.42), _label(0, 0, left), _label(4.4, 0, right)]
    cmds += _arrow((0.95, 0), (3.45, 0), gap=0.0)
    cmds.append(_label(2.2, 0.05, rule, "south"))
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 22: number lines
# ------------------------------------------------------------------
def number_line(lo, hi, pieces=(), dots=(), ink="black", width=7.6, slide_width=22.0):
    """The integers lo..hi on a line with arrows at both ends, each one ticked and numbered.
    pieces: (a, b) heavy parts of a graph; None for a or b is a ray off that end, with an
    arrowhead. dots: (x, solid?) circles, solid or open. Drawn `width` cm wide on a sheet and
    slide_width on a slide (graphs.SLIDE_STATE), its numbers larger and its graph heavier there;
    a slide gives it room, as it does a graph."""
    u = width / (hi - lo + 2)
    x = lambda v: u * (v - lo + 1)
    color = INK.get(ink, ink)
    size = _num(min(9, max(6, 17 * u)))                       # the numbers: as big as their spacing allows
    cmds = [f'line((0, 0), ({_num(width)}, 0), stroke: 0.7pt, mark: (start: ">", end: ">", fill: black, scale: 0.6))']
    for v in range(lo, hi + 1):
        cmds.append(f"line(({_num(x(v))}, -0.09), ({_num(x(v))}, 0.09), stroke: 0.7pt)")
        cmds.append(f'content(({_num(x(v))}, -0.13), anchor: "north", text(size: {size}pt * gs)[{_minus(v)}])')
    for a, b in pieces:
        start = 0.04 if a is None else x(a)
        end = width - 0.04 if b is None else x(b)
        pts = (end, start) if a is None else (start, end)          # a ray's arrowhead at its far end
        mark = f', mark: (end: ">", fill: {color}, scale: 0.75)' if a is None or b is None else ""
        cmds.append(f"line(({_num(pts[0])}, 0), ({_num(pts[1])}, 0), stroke: 2pt * gw + {color}{mark})")
    for v, solid in dots:
        cmds.append(f"circle(({_num(x(v))}, 0), radius: 0.085, fill: {color if solid else 'white'}, stroke: 1pt + {color})")
    body = "\n    ".join(cmds)
    return (f"#context {{ let t = {SLIDE_STATE}.get()\n"
            f"  let gs = 1 + t * {_num(SLIDE_TEXT - 1)}\n"
            f"  let gw = 1 + t\n"
            f"  cetz.canvas(length: (1 + t * {_num(slide_width / width - 1)}) * 1cm, {{\n"
            f"    import cetz.draw: *\n    {body}\n  }}) }}")

# ------------------------------------------------------------------
# Lesson 3: triangles, with their sides labeled and their angles marked
# ------------------------------------------------------------------
def _fit(pts, wide, tall):
    """The scale that fits the points in a wide-by-tall box, and the offset to put them at the origin."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    k = min(wide / w if w else 9e9, tall / h if h else 9e9)
    return k, min(xs), min(ys)

def _side_label(a, b, inside, text, gap=0.3):
    """A side's label at its middle, set off from the side away from the point `inside`."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if (inside[0] - mx) * nx + (inside[1] - my) * ny > 0:
        nx, ny = -nx, -ny
    return _label(mx + gap * nx, my + gap * ny, text)

def _angle_arcs(v, p, q, count, r0=0.3, step=0.08):
    """`count` arcs marking the angle at v between the sides toward p and q."""
    a0 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]))
    a1 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0]))
    sweep = (a1 - a0) % 360
    if sweep > 180:
        a0, sweep = a1, 360 - sweep
    out = []
    for i in range(count):
        r = r0 + step * i
        out.append(_poly([(v[0] + x, v[1] + y) for x, y in _arc(r, a0, a0 + sweep, 24)], ", stroke: 0.6pt"))
    return out

def _unit(p, q):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    return ((q[0] - p[0]) / L, (q[1] - p[1]) / L)

def triangles(tris, wide=5.6, tall=2.8, unit="1cm"):
    """Triangles drawn to fit a wide-by-tall box. Each is dict(pts: three points,
    labels: {side index i (from pts[i] to pts[i+1]): markup}, marks: {vertex index:
    arcs (1, 2) or "right"}), its points in any units: they're scaled here, and the
    labels and marks are set at a fixed size after."""
    k, x0, y0 = _fit([p for t in tris for p in t["pts"]], wide, tall)
    cmds = []
    for t in tris:
        P = [(k * (x - x0), k * (y - y0)) for x, y in t["pts"]]
        cmds.append(_poly(P, ", close: true, stroke: 0.8pt"))
        c = (sum(x for x, _ in P) / 3, sum(y for _, y in P) / 3)
        for i, text in t.get("labels", {}).items():
            cmds.append(_side_label(P[i], P[(i + 1) % 3], c, text))
        for i, m in t.get("marks", {}).items():
            v, p, q = P[i], P[(i + 1) % 3], P[(i + 2) % 3]
            if m == "right":
                cmds.append(_right_angle(v, _unit(v, p), _unit(v, q)))
            else:
                cmds += _angle_arcs(v, p, q, m)
    return _canvas(cmds, unit)

def nested(outer, foot, top, labels, marks=(), wide=5.0, tall=2.6, unit="1cm"):
    """A right triangle and lines inside it, drawn to fit: outer is its three points
    (the vertex with the marked angle, the right angle's vertex, the third), the segment
    foot-top is drawn too; labels: (a, b, inside point, markup) for segments a-b; marks:
    ("right", corner, toward p, toward q) or (arcs, vertex, toward p, toward q)."""
    k, x0, y0 = _fit(list(outer), wide, tall)
    S = lambda p: (k * (p[0] - x0), k * (p[1] - y0))
    cmds = [_poly([S(p) for p in outer], ", close: true, stroke: 0.8pt"), _poly([S(foot), S(top)], ", stroke: 0.8pt")]
    for a, b, inside, text in labels:
        cmds.append(_side_label(S(a), S(b), S(inside), text))
    for m, v, p, q in marks:
        v, p, q = S(v), S(p), S(q)
        cmds += [_right_angle(v, _unit(v, p), _unit(v, q))] if m == "right" else _angle_arcs(v, p, q, m)
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 4: compass-and-straightedge constructions, and a protractor
# ------------------------------------------------------------------
KEY_INK = INK["red"]

def construction(prims, key, unit="1cm", pad=0.35):
    """A construction drawn from primitives, every coordinate in centimeters (on a sheet, unit
    1cm: lengths print true, so a compass and ruler work on the page). A primitive is a tuple
    whose first item says what it is and whose last says whose it is, "given" or "key":
        ("seg", p, q, arrows, who)      arrows: "" none, "end" at q, "both"
        ("dot", p, who)
        ("label", p, markup, who)       centered at p (the bank sets it off from its point)
        ("arc", center, r, a0, a1, who) degrees, counterclockwise from a0 to a1
        ("box", corner, u, v, who)      a right-angle mark, its sides along unit vectors u, v
    The key's parts are drawn in red only when key is true; either way they count toward the
    figure's size (an invisible box around everything), so the question's figure and the key's
    are the same size and nothing moves between them."""
    xs, ys, cmds = [], [], []
    for pr in prims:
        kind, who = pr[0], pr[-1]
        if kind == "seg":
            pts = [pr[1], pr[2]]
        elif kind == "arc":
            (cx, cy), r, a0, a1 = pr[1:5]
            pts = [(cx + x, cy + y) for x, y in _arc(r, a0, a1, 24)]
        else:
            pts = [pr[1]]
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
        if who == "key" and not key:
            continue
        ink = KEY_INK if who == "key" else "black"
        if kind == "seg":
            mark = {"": "", "end": f', mark: (end: "stealth", fill: {ink}, scale: 0.7)',
                    "both": f', mark: (start: "stealth", end: "stealth", fill: {ink}, scale: 0.7)'}[pr[3]]
            cmds.append(_poly(pts, f", stroke: {'1pt' if who == 'given' else '0.9pt'} + {ink}{mark}"))
        elif kind == "arc":
            cmds.append(_poly(pts, f", stroke: 0.6pt + {ink}"))
        elif kind == "dot":
            cmds.append(f"circle({_pt(*pr[1])}, radius: 0.06, fill: {ink}, stroke: none)")
        elif kind == "label":
            body = pr[2] if who == "given" else f"#text(fill: {ink})[{pr[2]}]"
            cmds.append(f"content({_pt(*pr[1])}, [{body}])")
        elif kind == "box":
            (x, y), (ux, uy), (vx, vy) = pr[1], pr[2], pr[3]
            k = 0.2
            cmds.append(_poly([(x + k * ux, y + k * uy), (x + k * (ux + vx), y + k * (uy + vy)),
                               (x + k * vx, y + k * vy)], f", stroke: 0.6pt + {ink}"))
    box = f"rect({_pt(min(xs) - pad, min(ys) - pad)}, {_pt(max(xs) + pad, max(ys) + pad)}, stroke: none)"
    return _canvas([box] + cmds, unit)

def protractor(rays, vertex, radius=3.0, unit="1cm", text_scale=1.0):
    """A protractor on its baseline, its origin at the angle's vertex, and rays from the vertex:
    rays is [(direction in degrees, 0 to 180 counterclockwise from the right, label markup)].
    The inner scale reads 0 at the right, the outer 0 at the left, as the book's does."""
    R = radius
    small = _num(5.2 * text_scale)
    cmds = [_poly([(-R - 0.15, 0), (-R - 0.15, -0.4), (R + 0.15, -0.4), (R + 0.15, 0)], ", stroke: 0.6pt"),
            _poly(_arc(R, 0, 180, 90), ", stroke: 0.7pt"),
            _poly(_arc(R - 1.2, 0, 180, 60), ", stroke: 0.4pt + luma(120)"),
            _poly([(-R - 0.15, 0), (R + 0.15, 0)], ", stroke: 0.5pt")]
    for i in range(181):
        t = math.radians(i)
        k = 0.32 if i % 10 == 0 else 0.2 if i % 5 == 0 else 0.11
        c, s = math.cos(t), math.sin(t)
        cmds.append(_poly([(R * c, R * s), ((R - k) * c, (R - k) * s)], ", stroke: 0.35pt"))
        if i % 10 == 0:
            for rr, v in ((R - 0.52, 180 - i), (R - 0.88, i)):
                cmds.append(f"content({_pt(rr * c, rr * s)}, angle: {i - 90}deg, "
                            f"text(size: {small}pt)[{v}])")
    for d, name in rays:
        t = math.radians(d)
        end = ((R + 0.7) * math.cos(t), (R + 0.7) * math.sin(t))
        cmds.append(_poly([(0, 0), end], ', stroke: 1pt, mark: (end: "stealth", fill: black, scale: 0.7)'))
        lab = ((R + 1.0) * math.cos(t), (R + 1.0) * math.sin(t) + (0.0 if 0 < d < 180 else 0.3))
        cmds.append(f"content({_pt(*lab)}, [{name}])")
    cmds += ["circle((0, 0), radius: 0.06, fill: white, stroke: 0.7pt)",
             f"content((0, -0.7), [{vertex}])"]
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 5: a rectangular solid and its diagonal
# ------------------------------------------------------------------
# The corners, by where they are: front or back, bottom or top, left or right.
CORNERS = ("fbl", "fbr", "ftr", "ftl", "bbl", "bbr", "btr", "btl")

def solid_corners(w, d, h, size=4.2, tall=2.8):
    """Where the corners of a w-by-d-by-h solid fall when drawn: the front face w wide and
    h tall, the depth d going back and up to the right at 30 degrees, drawn at 0.55 of its
    length (as the book's figures are). Scaled to fit `size` wide and `tall` high."""
    dx, dy = 0.55 * d * math.cos(math.radians(30)), 0.55 * d * math.sin(math.radians(30))
    k = min(size / (w + dx), tall / (h + dy))
    w, h, dx, dy = w * k, h * k, dx * k, dy * k
    front = {"fbl": (0, 0), "fbr": (w, 0), "ftr": (w, h), "ftl": (0, h)}
    back = {"b" + c[1:]: (x + dx, y + dy) for c, (x, y) in front.items()}
    return front | back

def solid(w, d, h, names, edges, key_lines=(), size=4.2, tall=2.8, unit="1cm"):
    """A rectangular solid drawn as the book draws it: the top face darkest, the hidden
    edges from the back-bottom-left corner dashed. names: {corner: markup} for the corners
    labeled; edges: {"width": markup, "depth": markup, "height": markup}, labeled on the front
    bottom edge, the right bottom edge going back, and the front left edge. key_lines:
    [(corner, corner)] drawn in red on the key; the figure's size doesn't change with them
    (they lie inside the solid), so nothing moves between the question and the key."""
    P = solid_corners(w, d, h, size, tall)
    cmds = [_poly([P[c] for c in ("ftl", "ftr", "btr", "btl")], ", close: true, stroke: none, fill: luma(150)"),
            _poly([P[c] for c in ("fbl", "fbr", "ftr", "ftl")], ", close: true, stroke: none, fill: luma(215)"),
            _poly([P[c] for c in ("fbr", "bbr", "btr", "ftr")], ", close: true, stroke: none, fill: luma(240)")]
    for a, b in (("bbl", "fbl"), ("bbl", "bbr"), ("bbl", "btl")):
        cmds.append(_dash(P[a], P[b]))
    for path in (("fbl", "fbr", "ftr", "ftl", "fbl"), ("ftl", "btl", "btr", "ftr"), ("fbr", "bbr", "btr")):
        cmds.append(_poly([P[c] for c in path], ", stroke: 0.9pt"))
    for a, b in key_lines:
        cmds.append(_poly([P[a], P[b]], f", stroke: 1.1pt + {KEY_INK}"))
    out = {"fbl": "north-east", "fbr": "north", "ftr": "north-east", "ftl": "south-east",
           "bbl": "south-west", "bbr": "west", "btr": "south-west", "btl": "south"}
    off = {"fbl": (-0.12, -0.05), "fbr": (0, -0.08), "ftr": (-0.06, -0.06), "ftl": (-0.1, 0.05),
           "bbl": (0.08, 0.06), "bbr": (0.1, 0), "btr": (0.05, 0.05), "btl": (0, 0.08)}
    for c, m in names.items():
        x, y = P[c]
        ox, oy = off[c]
        cmds.append(f'content({_pt(x + ox, y + oy)}, anchor: "{out[c]}", padding: 1pt, [{m}])')
    (x0, y0), (x1, _), (x2, y2), (_, y3) = P["fbl"], P["fbr"], P["bbr"], P["ftl"]
    if edges.get("width"):
        cmds.append(_label((x0 + x1) / 2, -0.12, edges["width"], "north"))
    if edges.get("depth"):
        cmds.append(_label((x1 + x2) / 2 + 0.14, (y0 + y2) / 2 - 0.06, edges["depth"], "north-west"))
    if edges.get("height"):
        cmds.append(_label(-0.12, (y0 + y3) / 2, edges["height"], "east"))
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 8: the altitude to the hypotenuse, parallel lines and transversals,
# an angle bisector
# ------------------------------------------------------------------
def _name(p, text, anchor):
    return f'content({_pt(*p)}, anchor: "{anchor}", padding: 3pt, [${text}$])'

def altitude(names, a=1.0, b=1.8, wide=4.6, tall=2.2, unit="1cm"):
    """names: (left, right-angle vertex, right, foot). The hypotenuse lies flat, the
    right angle on top; legs a (left) and b (right); right angles marked at the top
    and at the foot of the altitude."""
    c = math.hypot(a, b)
    pts = [(0, 0), (a * a / c, a * b / c), (c, 0), (a * a / c, 0)]
    k, x0, y0 = _fit(pts, wide, tall)
    L, T, R, F = [(k * (x - x0), k * (y - y0)) for x, y in pts]
    cmds = [_poly([L, T, R], ", close: true, stroke: 0.8pt"), _poly([T, F], ", stroke: 0.8pt"),
            _right_angle(T, _unit(T, L), _unit(T, R)), _right_angle(F, _unit(F, R), _unit(F, T))]
    for p, n, anchor in zip((L, T, R, F), names, ("east", "south", "west", "north")):
        cmds.append(_name(p, n, anchor))
    return _canvas(cmds, unit)

def transversals(labels, ratio, width=5.4, height=2.4, unit="1cm"):
    """Three parallel lines (arrowheads), cut by two transversals. labels: (left upper,
    left lower, right upper, right lower) markup; ratio: upper over lower, the spacing
    of the lines (the same on both transversals, so the figure is to scale)."""
    lo = height / (1 + ratio)
    ys = (0, lo, height)
    cmds = []
    for y in ys:
        cmds.append(_poly([(0, y), (width, y)], ", stroke: 0.8pt"))
        cmds.append(_poly([(width - 1.0, y), (width - 0.86, y)],
                          ', stroke: 0.8pt, mark: (end: ">", fill: black, scale: 0.7)'))
    x1 = lambda y: 0.9 + 0.12 * y                                 # nearly upright, on the left
    x2 = lambda y: 1.9 + 0.95 * y                                 # leaning right
    for f in (x1, x2):
        cmds.append(_poly([(f(-0.4), -0.4), (f(height + 0.4), height + 0.4)], ", stroke: 0.8pt"))
    up1, lo1, up2, lo2 = labels
    for f, (up, low), side in ((x1, (up1, lo1), -1), (x2, (up2, lo2), 1)):
        for text, (ya, yb) in ((up, (lo, height)), (low, (0, lo))):
            ym = (ya + yb) / 2
            cmds.append(f'content({_pt(f(ym) + 0.18 * side, ym)}, anchor: "{"west" if side > 0 else "east"}", '
                        f'padding: 2pt, [{text}])')
    return _canvas(cmds, unit)

def bisector(names, lengths, labels, wide=4.8, tall=2.4, unit="1cm"):
    """names: (bisected vertex V, P, Q, foot D on PQ); lengths: VP, VQ, PD, DQ (numbers,
    the triangle drawn to scale); labels: their markup (None: no label). The base PQ
    lies flat, V above; the two halves of the angle at V are marked alike."""
    VP, VQ, PD, DQ = lengths
    PQ = PD + DQ
    vx = (VP * VP - VQ * VQ + PQ * PQ) / (2 * PQ)
    pts = [(vx, math.sqrt(max(VP * VP - vx * vx, 0))), (0, 0), (PQ, 0), (PD, 0)]
    k, x0, y0 = _fit(pts, wide, tall)
    V, P, Q, D = [(k * (x - x0), k * (y - y0)) for x, y in pts]
    cmds = [_poly([V, P, Q], ", close: true, stroke: 0.8pt"), _poly([V, D], ", stroke: 0.8pt")]
    cmds += _angle_arcs(V, P, D, 1, r0=0.42) + _angle_arcs(V, D, Q, 1, r0=0.42)
    cmds += _angle_arcs(V, P, D, 1, r0=0.5) + _angle_arcs(V, D, Q, 1, r0=0.5)
    c = ((V[0] + P[0] + Q[0]) / 3, (V[1] + P[1] + Q[1]) / 3)
    for (a, b, inside), text in zip(((V, P, c), (V, Q, c), (P, D, V), (D, Q, V)), labels):
        if text is not None:
            cmds.append(_side_label(a, b, inside, text))
    for p, n, anchor in zip((V, P, Q, D), names, ("south", "north-east", "north-west", "north")):
        cmds.append(_name(p, n, anchor))
    return _canvas(cmds, unit)


# ------------------------------------------------------------------
# Lesson 9: a figure of segments with its equal parts marked
# ------------------------------------------------------------------
ANCHORS = ("west", "south-west", "south", "south-east", "east", "north-east", "north", "north-west")

def _away(d):
    """The anchor that sets a label off from its point in the direction d (the label's side nearest the point)."""
    a = math.degrees(math.atan2(d[1], d[0])) % 360
    return ANCHORS[int(((a + 22.5) % 360) // 45)]

def _ticks(a, b, n, half=0.1, gap=0.07):
    """n tick marks across the segment a-b at its middle."""
    (ux, uy), m = _unit(a, b), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    nx, ny = -uy, ux
    out = []
    for i in range(n):
        s = (i - (n - 1) / 2) * gap
        cx, cy = m[0] + s * ux, m[1] + s * uy
        out.append(_poly([(cx - half * nx, cy - half * ny), (cx + half * nx, cy + half * ny)], ", stroke: 0.6pt"))
    return out

def _gapped_arcs(v, p, q, count, r0=0.34, step=0.08, gap=8):
    """Like _angle_arcs, but short of both rays by `gap` degrees, so two equal angles side
    by side (a bisected angle) show as two arcs, not one."""
    a0 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]))
    a1 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0]))
    sweep = (a1 - a0) % 360
    if sweep > 180:
        a0, sweep = a1, 360 - sweep
    g = min(gap, sweep / 4)
    return [_poly([(v[0] + x, v[1] + y) for x, y in _arc(r0 + step * i, a0 + g, a0 + sweep - g, 24)], ", stroke: 0.6pt")
            for i in range(count)]

def marked(pts, chains, ticks=(), arcs=(), rights=(), circles=(), wide=4.4, tall=2.4, unit="1cm"):
    """pts: {name: (x, y)} in any units (scaled here to fit wide by tall); chains: runs of
    names on one straight line, each drawn as one line; ticks: (a, b, count) on segment a-b;
    arcs: (vertex, p, q, count) in the angle at vertex between the rays toward p and q;
    rights: (vertex, p, q), a right-angle box; circles: (a, b), a small circle on the middle
    of segment a-b (the side two triangles share). Each name sits off its point away from
    its own piece of the figure (across the line, for a point inside a chain)."""
    k, x0, y0 = _fit(list(pts.values()), wide, tall)
    P = {n: (k * (x - x0), k * (y - y0)) for n, (x, y) in pts.items()}
    cmds = [_poly([P[n] for n in c], ", stroke: 0.8pt") for c in chains]
    for a, b, n in ticks:
        cmds += _ticks(P[a], P[b], n)
    for v, p, q, n in arcs:
        cmds += _gapped_arcs(P[v], P[p], P[q], n)
    for v, p, q in rights:
        cmds.append(_right_angle(P[v], _unit(P[v], P[p]), _unit(P[v], P[q]), k=0.2))
    for a, b in circles:
        m = ((P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2)
        cmds.append(f"circle({_pt(*m)}, radius: 0.1, stroke: 0.6pt)")
    piece = {n: {n} for n in P}                                  # the connected piece each point is in
    for c in chains:
        joined = set().union(*(piece[n] for n in c))
        for n in joined:
            piece[n] = joined
    for n, p in P.items():
        g = piece[n]
        c = (sum(P[m][0] for m in g) / len(g), sum(P[m][1] for m in g) / len(g))
        d = (p[0] - c[0], p[1] - c[1])
        for ch in chains:
            if n in ch[1:-1]:                                    # inside a line: across it, away from the middle
                ux, uy = _unit(P[ch[0]], P[ch[-1]])
                d = (-uy, ux) if (-uy * d[0] + ux * d[1]) >= 0 else (uy, -ux)
        cmds.append(_name(p, n, _away(d)))
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 11: a circle with segments, marked angles, and labels; the bank
# works out every coordinate (cm), this only draws
# ------------------------------------------------------------------
def circled(center, r, chains, arcs=(), labels=(), leaders=(), unit="1cm"):
    """A circle (center, radius r), chains of points each drawn as one line, arcs: (vertex, p, q),
    one arc in the angle at vertex between the rays toward p and q; labels: (x, y, markup),
    each centered at its point; leaders: (a, b), a thin line from a label to what it names."""
    cmds = [f"circle({_pt(*center)}, radius: {_num(r)}, stroke: 0.8pt)"]
    cmds += [_poly(c, ", stroke: 0.8pt") for c in chains]
    cmds += [_poly([a, b], ", stroke: 0.5pt") for a, b in leaders]
    for v, p, q in arcs:
        cmds += _angle_arcs(v, p, q, 1, r0=0.24)
    cmds += [_label(x, y, text) for x, y, text in labels]
    return _canvas(cmds, unit)

# ------------------------------------------------------------------
# Lesson 12: a convex polygon, split into triangles from one vertex
# ------------------------------------------------------------------
def polygon_points(n, r=1.3):
    """A regular n-gon's vertices, the first at the left, going clockwise."""
    return [(r * math.cos(math.radians(180 - 360 * i / n)), r * math.sin(math.radians(180 - 360 * i / n)))
            for i in range(n)]

def polygon(n, triangulated=False, r=None, unit="1cm"):
    """A regular n-gon (bigger as n grows); triangulated: the diagonals from the first vertex,
    and each triangle numbered, as the deck draws example 12.1's answer. A number sits 4/5 of
    the way from that vertex to the middle of the far side, where even a thin triangle has room."""
    r = r or 1.3 + 0.1 * max(n - 6, 0)
    P = polygon_points(n, r)
    cmds = [_poly(P + [P[0]], ", stroke: 0.9pt")]
    if triangulated:
        cmds += [_poly([P[0], P[i]], ", stroke: 0.6pt") for i in range(2, n - 1)]
        for i in range(1, n - 1):
            mx, my = (P[i][0] + P[i + 1][0]) / 2, (P[i][1] + P[i + 1][1]) / 2
            cx, cy = P[0][0] + 0.8 * (mx - P[0][0]), P[0][1] + 0.8 * (my - P[0][1])
            cmds.append(_label(cx, cy, f"#text(size: 0.8em)[{i}]"))
    return _canvas(cmds, unit)
