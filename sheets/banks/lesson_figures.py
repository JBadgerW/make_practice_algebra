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
