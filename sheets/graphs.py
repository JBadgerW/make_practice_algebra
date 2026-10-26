"""Coordinate-plane graphs, drawn with Typst's cetz package. The banks that
draw a graph set PREAMBLE (the import) and build a Graph; Graph.typst() is
the picture, ready to go in a problem.

    g = Graph(x=(-8, 8), y=(-8, 8))            a window, a grid, the axes, labels
    g.line(2, -3)                              y = 2x - 3 across the window
    g.through((0, 1), (3, 7)); g.vertical(4)   a line through two points; x = 4
    g.polyline([(-8, 2), (-7, 3), ...])        straight pieces through the points
    g.smooth([(-6, 0), (-3, 4), (0, 1), ...])  a smooth curve through the points
    g.function(f, -8, 8)                       y = f(x), sampled, cut at the window
    g.point(2, 1); g.point(4, 3, fill=False)   a dot (an open circle); label="A"
    g.label_at(3, 5, "$y = f(x)$")             text at a point
    g.typst()                                  "#cetz.canvas(...)"

Every coordinate is worked out here, in Python: the window maps to
centimeters (x and y each with their own scale, so a 0..90 axis by 10s
fits), and each curve is cut where it leaves the window, with an arrowhead
where it goes on (ends="arrow") or a dot where it stops (ends="closed" or
"open"). cetz only draws. Pieces of a curve that leave the window and come
back are drawn as separate runs.

The window: the grid lines every `step` (x and y may differ: step=(10, 5)),
the numbers every `label` steps, the axes through 0 (or along the edge when
0 is outside the window), arrowheads on both ends of each axis, and the
axis names (xlabel, ylabel) at the arrow ends.
"""
import math

CETZ = "0.5.2"
PREAMBLE = f'#import "@preview/cetz:{CETZ}"\n'
INK = {"blue": "rgb(\"#1f5fbf\")", "red": "rgb(\"#c0392b\")", "green": "rgb(\"#1e8449\")",
       "purple": "rgb(\"#7d3c98\")", "orange": "rgb(\"#d35400\")", "black": "black", "gray": "luma(110)"}

def _num(t):
    """A number for Typst: no trailing zeros, no -0."""
    t = round(t, 4)
    s = f"{t:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def _minus(v):
    """A tick label: the minus sign, not a hyphen."""
    s = _num(v)
    return s.replace("-", "−")

def clip(p, q, box):
    """The part of segment pq inside box (x0, x1, y0, y1), or None (Liang-Barsky)."""
    (x0, y0), (x1, y1) = p, q
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, x0 - box[0]), (dx, box[1] - x0), (-dy, y0 - box[2]), (dy, box[3] - y0)):
        if pk == 0:
            if qk < 0:
                return None
            continue
        t = qk / pk
        if pk < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (x0 + t0 * dx, y0 + t0 * dy), (x0 + t1 * dx, y0 + t1 * dy), t0 > 0, t1 < 1

def runs(points, box):
    """The polyline cut to the box: a list of (points, starts cut?, ends cut?)."""
    out, cur, cut_start = [], [], False
    for p, q in zip(points, points[1:]):
        c = clip(p, q, box)
        if c is None:
            if cur:
                out.append((cur, cut_start, True))
                cur = []
            continue
        a, b, a_cut, b_cut = c
        if not cur:
            cur, cut_start = [a], a_cut
        elif a_cut:                                   # left and came back: a new run
            out.append((cur, cut_start, True))
            cur, cut_start = [a], True
        cur.append(b)
        if b_cut:
            out.append((cur, cut_start, True))
            cur = []
    if cur:
        out.append((cur, cut_start, False))
    return out

class Graph:
    def __init__(self, x=(-10, 10), y=(-10, 10), width=5.0, height=None, step=1, label=None,
                 xlabel="x", ylabel="y", grid=True, numbers=True, origin=False):
        """width (and height) in cm; step: grid spacing, one number or (x, y); label: the numbers
        every so many grid lines (default: every one if they fit, else every 2 or 5)."""
        self.x0, self.x1 = x
        self.y0, self.y1 = y
        self.sx_step, self.sy_step = step if isinstance(step, tuple) else (step, step)
        self.width = width
        self.height = height or width * (self.y1 - self.y0) / (self.x1 - self.x0)
        self.kx = self.width / (self.x1 - self.x0)
        self.ky = self.height / (self.y1 - self.y0)
        self.xlabel, self.ylabel, self.grid, self.numbers, self.origin = xlabel, ylabel, grid, numbers, origin
        self.label = label
        self.cmds = []

    # ---- coordinates
    def c(self, x, y):
        """A data point in cm, as a cetz coordinate."""
        return f"({_num((x - self.x0) * self.kx)}, {_num((y - self.y0) * self.ky)})"

    def box(self, pad=0.0):
        """The window, a little wider, but not past an axis at its edge (a first-quadrant graph)."""
        px, py = pad / self.kx, pad / self.ky
        return (self.x0 - px if self.x0 < 0 else self.x0, self.x1 + px,
                self.y0 - py if self.y0 < 0 else self.y0, self.y1 + py)

    def _every(self, steps, k):
        if self.label:
            return self.label
        size = k * steps                            # cm between grid lines
        return next(n for n in (1, 2, 5, 10, 20) if size * n >= 0.42)

    # ---- the window
    def _frame(self):
        out = []
        xs = [self.x0 + i * self.sx_step for i in range(int(round((self.x1 - self.x0) / self.sx_step)) + 1)]
        ys = [self.y0 + i * self.sy_step for i in range(int(round((self.y1 - self.y0) / self.sy_step)) + 1)]
        if self.grid:
            for gx in xs:
                out.append(f"line({self.c(gx, self.y0)}, {self.c(gx, self.y1)}, stroke: 0.3pt + luma(200))")
            for gy in ys:
                out.append(f"line({self.c(self.x0, gy)}, {self.c(self.x1, gy)}, stroke: 0.3pt + luma(200))")
        ax = 0 if self.y0 <= 0 <= self.y1 else self.y0          # the x-axis: at y = 0, or along the bottom
        ay = 0 if self.x0 <= 0 <= self.x1 else self.x0
        over_x, over_y = 0.35 / self.kx, 0.35 / self.ky
        def arrow(neg):                                         # no arrow back past an axis at the edge
            start = 'start: ">", ' if neg else ""
            return f'mark: ({start}end: ">", fill: black, scale: 0.6)'
        lo_x = self.x0 - over_x if self.x0 < 0 else self.x0
        lo_y = self.y0 - over_y if self.y0 < 0 else self.y0
        out.append(f"line({self.c(lo_x, ax)}, {self.c(self.x1 + over_x, ax)}, {arrow(self.x0 < 0)}, stroke: 0.7pt)")
        out.append(f"line({self.c(ay, lo_y)}, {self.c(ay, self.y1 + over_y)}, {arrow(self.y0 < 0)}, stroke: 0.7pt)")
        if self.xlabel:
            out.append(f"content({self.c(self.x1 + over_x, ax)}, anchor: \"west\", padding: 3pt, "
                       f"text(size: 8pt)[{self._math(self.xlabel)}])")
        if self.ylabel:
            out.append(f"content({self.c(ay, self.y1 + over_y)}, anchor: \"south\", padding: 3pt, "
                       f"text(size: 8pt)[{self._math(self.ylabel)}])")
        if self.numbers:
            ex, ey = self._every(self.sx_step, self.kx), self._every(self.sy_step, self.ky)
            for i, gx in enumerate(xs):
                if i % ex == 0 and (gx != ay or self.origin) and gx not in (self.x0, self.x1):
                    out.append(f"content({self.c(gx, ax)}, anchor: \"north\", padding: 2pt, "
                               f"text(size: 6pt)[{_minus(gx)}])")
            for i, gy in enumerate(ys):
                if i % ey == 0 and gy != ax and gy not in (self.y0, self.y1):
                    out.append(f"content({self.c(ay, gy)}, anchor: \"east\", padding: 2pt, "
                               f"text(size: 6pt)[{_minus(gy)}])")
        return out

    @staticmethod
    def _math(t):
        """Axis names and labels: a bare letter in math, anything else as given."""
        return f"${t}$" if len(t) == 1 and t.isalpha() else t

    # ---- what goes on it
    def _stroke(self, color, width, dash):
        s = f"{width}pt + {INK.get(color, color)}"
        return f"(paint: {INK.get(color, color)}, thickness: {width}pt, dash: \"{dash}\")" if dash else s

    def _dot(self, x, y, fill, color, r=0.09):
        ink = INK.get(color, color)
        return f"circle({self.c(x, y)}, radius: {r}, fill: {ink if fill else 'white'}, stroke: 0.9pt + {ink})"

    def polyline(self, points, color="blue", width=1.3, dash=None, ends="arrow"):
        """Straight pieces through the points, cut at the window. ends: what each end of the
        curve shows when it's inside the window: "arrow" (it goes on), "closed" or "open" (it
        stops there, at a dot), None (it stops, nothing drawn); one value or (start, end)."""
        start_end, end_end = ends if isinstance(ends, tuple) else (ends, ends)
        pts = [(float(a), float(b)) for a, b in points]
        for run, cut_a, cut_b in runs(pts, self.box(0.18)):
            if len(run) < 2:
                continue
            first = run[0] == pts[0] and not cut_a
            last = run[-1] == pts[-1] and not cut_b
            marks = []
            if cut_a or first and start_end == "arrow":
                marks.append('start: ">"')
            if cut_b or last and end_end == "arrow":
                marks.append('end: ">"')
            mark = f", mark: ({', '.join(marks)}, fill: {INK.get(color, color)}, scale: 0.7)" if marks else ""
            body = ", ".join(self.c(*p) for p in run)
            self.cmds.append(f"line({body}, stroke: {self._stroke(color, width, dash)}{mark})")
            if first and start_end in ("closed", "open"):
                self.cmds.append(self._dot(*run[0], start_end == "closed", color))
            if last and end_end in ("closed", "open"):
                self.cmds.append(self._dot(*run[-1], end_end == "closed", color))
        return self

    def smooth(self, points, color="blue", width=1.3, dash=None, ends="arrow", per=12):
        """A smooth curve through the points (Catmull-Rom, sampled), so it passes through
        each one exactly: a maximum drawn at a point is a maximum of the curve if its
        neighbors are lower."""
        pts = [(float(a), float(b)) for a, b in points]
        out = []
        for i in range(len(pts) - 1):
            p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
            for k in range(per):
                t = k / per
                out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                        + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
        out.append(pts[-1])
        return self.polyline(out, color, width, dash, ends)

    def function(self, f, a=None, b=None, color="blue", width=1.3, dash=None, ends="arrow", n=240):
        """y = f(x) from a to b (default: across the window), sampled; a point where f fails
        (a hole, an asymptote) breaks the curve."""
        a = self.x0 if a is None else a
        b = self.x1 if b is None else b
        pieces, cur = [], []
        jump = 3 * (self.y1 - self.y0)
        for i in range(n + 1):
            x = a + (b - a) * i / n
            try:
                y = float(f(x))
                if math.isnan(y) or abs(y) > 1e6:
                    raise ValueError
                if cur and abs(y - cur[-1][1]) > jump:          # across an asymptote: a new piece
                    pieces.append(cur)
                    cur = []
                cur.append((x, y))
            except (ValueError, ZeroDivisionError, TypeError, OverflowError):
                if cur:
                    pieces.append(cur)
                cur = []
        if cur:
            pieces.append(cur)
        for piece in pieces:
            self.polyline(piece, color, width, dash, ends)
        return self

    def line(self, m, b, **kw):
        """y = m x + b, across the window, arrows at both ends."""
        span = (self.x1 - self.x0) * 2
        return self.polyline([(self.x0 - span, m * (self.x0 - span) + b), (self.x1 + span, m * (self.x1 + span) + b)], **kw)

    def through(self, p, q, **kw):
        if p[0] == q[0]:
            return self.vertical(p[0], **kw)
        m = (q[1] - p[1]) / (q[0] - p[0])
        return self.line(m, p[1] - m * p[0], **kw)

    def vertical(self, x, **kw):
        span = (self.y1 - self.y0) * 2
        return self.polyline([(x, self.y0 - span), (x, self.y1 + span)], **kw)

    def segment(self, p, q, ends=("closed", "closed"), **kw):
        return self.polyline([p, q], ends=ends, **kw)

    def point(self, x, y, fill=True, color="black", label=None, anchor="south-west"):
        self.cmds.append(self._dot(x, y, fill, color, 0.1))
        if label:
            self.label_at(x, y, label, anchor)
        return self

    def label_at(self, x, y, text, anchor="south-west", color="black", size=8):
        self.cmds.append(f"content({self.c(x, y)}, anchor: \"{anchor}\", padding: 3pt, "
                         f"text(size: {size}pt, fill: {INK.get(color, color)})[{text}])")
        return self

    def typst(self):
        body = "\n    ".join(self._frame() + self.cmds)
        return f"#cetz.canvas(length: 1cm, {{\n    import cetz.draw: *\n    {body}\n  }})"
