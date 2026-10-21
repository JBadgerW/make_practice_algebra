"""Inequalities on the number line: read a graph, graph an inequality, and
solve an inequality before graphing it.

Every number on a problem, and every number met while solving it, is
between -15 and 15. Solving never ends by dividing by a negative.

A problem: dict(type, prompt, answer, graph, line, source).
    graph   the solution set: [lower, upper], each [value, closed?], or null
            for a ray that end: [[-4, false], [1, true]] is -4 < x <= 1
    line    the integers the number line shows: [lo, hi]
    prompt  the inequality in Typst math ("" for a graph to read)
    answer  the solution as the key writes it: "x <= 1", "-4 < x <= 1"

Types 1 and 2 print the graph and ask for the inequality; types 3-6 print
the inequality and a blank number line, and the key draws the graph on it
in red. check() solves the prompt and the answer again with sympy and
compares both with the graph at every boundary and between them.
"""
import random, re
from fractions import Fraction
import sympy as sp

NAME = FAMILY = "inequalities"
FIXED = False
TITLE = "Lesson 1-5: Solving Inequalities in One Variable"
INSTRUCTIONS = ""                     # each type has its own (type_instructions)
COURSES = ["Algebra 1"]

TYPES = [
    dict(key="1", title="Write the Inequality",
         instructions="Write the inequality shown by each graph.",
         look="A dot and a ray on a number line.",
         move="Write x, then the sign, then the number at the dot. The ray points toward the numbers x can be; a closed dot means ≤ or ≥, an open dot means < or >."),
    dict(key="2", title="Write the Compound Inequality",
         instructions="Write the compound inequality shown by each graph.",
         look="A segment between two dots on a number line.",
         move="Write it smallest to largest: number, sign, x, sign, number. Each dot chooses its own sign: closed is ≤, open is <."),
    dict(key="3", title="Graph the Inequality",
         instructions="Graph each inequality.",
         look="x compared with one number.",
         move="Put a dot at the number: closed for ≤ or ≥, open for < or >. Shade the ray toward the numbers that make it true."),
    dict(key="4", title="Graph the Compound Inequality",
         instructions="Graph each compound inequality.",
         look="x between two numbers.",
         move="Put a dot at each number, closed for ≤ and open for <, and shade the segment between them."),
    dict(key="5", title="Solve, Then Graph",
         instructions="Solve each inequality. Then graph its solution.",
         look="An inequality with x in a two-step or multi-step expression.",
         move="Solve it like an equation, keeping the inequality sign. Then graph x compared with one number."),
    dict(key="6", title="Solve the Compound Inequality, Then Graph",
         instructions="Solve each compound inequality. Then graph its solution.",
         look="x in an expression between two numbers, or two inequalities joined by \"and\".",
         move="Do each step to all three parts (or solve each half). Then graph x between two numbers."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]
SPACE = {"1": "0.5in", "2": "0.5in", "3": "0.35in", "4": "0.35in", "5": "1.5in", "6": "1.5in"}
ENTRIES = [dict(key=k, type=k, kind="numbers", title=TYPE[k]["title"], width="half", space=SPACE[k])
           for k in KEYS]
ENTRY = {e["key"]: e for e in ENTRIES}
GRAPHED = ("1", "2")                  # types whose prompt is a graph
COMPOUND = ("2", "4", "6")
BIG = 15                              # every number stays within -BIG..BIG
SPAN = 10                             # a number line shows SPAN + 1 integers

def label(t):
    return "Type " + t["key"]

def entry_key(text):
    t = text.strip()
    return t if t in ENTRY else None

def type_of(entry):
    return entry

def heading(typ):
    return f"{label(TYPE[typ])}: {TYPE[typ]['title']}"

def type_instructions(typ):
    return TYPE[typ]["instructions"]

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return False

def initial_seen():
    return set()

def seen_key(p):
    return ("inequalities", p["type"], p["prompt"] or repr(p["graph"]))

# ------------------------------------------------------------------
# Writing inequalities
# ------------------------------------------------------------------
def sign(closed, less=True):
    return ("<" if less else ">") + ("=" if closed else "")

def flip(op):
    return {"<": ">", ">": "<", "<=": ">=", ">=": "<="}[op]

def plus(c):
    """7 -> " + 7", -7 -> " - 7", 0 -> ""."""
    return f" + {c}" if c > 0 else f" - {-c}" if c < 0 else ""

def lin(a, c=0):
    """a x + c: lin(2, 7) = "2x + 7", lin(1, -3) = "x - 3"."""
    return ("" if a == 1 else str(a)) + "x" + plus(c)

def canon(graph):
    """The solution as the key writes it, x on the left: "x <= 1", "-4 < x <= 1"."""
    lo, hi = graph
    if lo is None:
        return f"x {sign(hi[1])} {hi[0]}"
    if hi is None:
        return f"x {sign(lo[1], less=False)} {lo[0]}"
    return f"{lo[0]} {sign(lo[1])} x {sign(hi[1])} {hi[0]}"

AND = ' quad "and" quad '

# ------------------------------------------------------------------
# Drawing, by type
# ------------------------------------------------------------------
class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

def small(*ns):
    need(all(abs(n) <= BIG for n in ns))

def nz(r, lo=1, hi=9):
    return r.choice([-1, 1]) * r.randint(lo, hi)

def ray(r):
    """A ray's graph: one boundary, either direction, open or closed."""
    b, closed = r.randint(-BIG + 2, BIG - 2), r.random() < 0.5
    return [None, [b, closed]] if r.random() < 0.5 else [[b, closed], None]

def segment(r):
    lo = r.randint(-BIG + 1, BIG - 3)
    hi = lo + r.randint(2, 8)
    need(hi <= BIG - 1)
    return [[lo, r.random() < 0.5], [hi, r.random() < 0.5]]

def window(r, graph):
    """The number line: SPAN + 1 integers, every boundary inside it. A ray's
    boundary gets two integers of room on each side, so the line doesn't
    give away which way the ray points; a segment's ends get one."""
    ends = [e[0] for e in graph if e]
    room = 1 if all(graph) else 2
    first = r.randint(max(-BIG, max(ends) + room - SPAN), min(BIG - SPAN, min(ends) - room))
    return [first, first + SPAN]

def written(r, graph):
    """Types 3 and 4: the inequality itself, sometimes with x on the right in type 3."""
    lo, hi = graph
    if lo and hi:
        return canon(graph)
    if r.random() < 0.2:
        b, closed = lo or hi
        return f"{b} {sign(closed, less=bool(lo))} x"
    return canon(graph)

# Type 5: x compared with b, hidden in one side. Each template takes the
# answer's operator ("x op b") and returns the prompt.
def t5_two_step(r, op, b):
    a, c = r.randint(2, 5), nz(r, 1, 12)
    d = a * b + c
    small(a * b, d)
    return f"{lin(a, c)} {op} {d}"

def t5_reversed(r, op, b):
    a, c = r.randint(2, 5), nz(r, 1, 12)
    d = a * b + c
    small(a * b, d)
    return f"{d} {flip(op)} {lin(a, c)}"

def t5_distribute(r, op, b):
    a, c = r.randint(2, 4), nz(r, 1, 9)
    d = a * (b + c)
    small(b + c, a * c, a * b, d)
    return f"{a}({lin(1, c)}) {op} {d}"

def t5_both_sides(r, op, b):
    e = r.randint(1, 4)
    a = e + r.randint(1, 4)                            # more x on the left: no negative to divide by
    c = nz(r, 1, 12)
    d = (a - e) * b + c
    small(a, (a - e) * b, d, d - c)
    return f"{lin(a, c)} {op} {lin(e, d)}"

def t5_like_terms(r, op, b):
    a, e, c = r.randint(1, 5), r.randint(1, 4), nz(r, 1, 12)
    need(a + e <= 6)
    d = (a + e) * b + c
    small((a + e) * b, d)
    return f"{lin(a, c)} + {lin(e)} {op} {d}"

def t5_fraction(r, op, b):
    a = r.randint(2, 5)
    need(b % a == 0)
    c = nz(r, 1, 12)
    d = b // a + c
    small(d)
    return f"x/{a}{plus(c)} {op} {d}"

T5 = [t5_two_step, t5_two_step, t5_reversed, t5_distribute, t5_both_sides, t5_like_terms, t5_fraction]

# Type 6: lo < x < hi, hidden in a middle expression a x + c, or split into two
# inequalities joined by "and". Each template takes the two operators and ends.
def middle(r, a, c, form, ops, lo, hi):
    """d1 op1 [form] op2 d2, where form shows a x + c."""
    d1, d2 = a * lo + c, a * hi + c
    small(d1, d2, a * lo, a * hi)
    return f"{d1} {ops[0]} {form} {ops[1]} {d2}"

def t6_one_step(r, ops, lo, hi):
    c = nz(r, 1, 12)
    return middle(r, 1, c, lin(1, c), ops, lo, hi)

def t6_times(r, ops, lo, hi):
    a = r.randint(2, 5)
    return middle(r, a, 0, lin(a), ops, lo, hi)

def t6_two_step(r, ops, lo, hi):
    a, c = r.randint(2, 4), nz(r, 1, 12)
    return middle(r, a, c, lin(a, c), ops, lo, hi)

def t6_distribute(r, ops, lo, hi):
    a, c = r.randint(2, 3), nz(r, 1, 6)
    small(lo + c, hi + c, a * c)
    return middle(r, a, a * c, f"{a}({lin(1, c)})", ops, lo, hi)

def t6_fraction(r, ops, lo, hi):
    a = r.randint(2, 4)
    need(lo % a == 0 and hi % a == 0)
    c = nz(r, 1, 9)
    d1, d2 = lo // a + c, hi // a + c
    small(d1, d2)
    return f"{d1} {ops[0]} x/{a}{plus(c)} {ops[1]} {d2}"

def t6_and(r, ops, lo, hi):
    a, c, e, f = r.randint(1, 4), nz(r, 1, 9), r.randint(1, 4), nz(r, 1, 9)
    need(a > 1 or e > 1)
    d1, d2 = a * lo + c, e * hi + f
    small(a * lo, e * hi, d1, d2)
    halves = [f"{lin(a, c)} {flip(ops[0])} {d1}", f"{lin(e, f)} {ops[1]} {d2}"]
    if r.random() < 0.3:
        halves.reverse()
    return AND.join(halves)

T6 = [t6_one_step, t6_times, t6_two_step, t6_two_step, t6_distribute, t6_fraction, t6_and]

def draw(entry, r, tpl):
    """(prompt, graph) for one problem of the type; tpl picks type 5's or 6's template."""
    if entry in ("1", "3", "5"):
        graph = ray(r)
    else:
        graph = segment(r)
    if entry in GRAPHED:
        return "", graph
    if entry in ("3", "4"):
        return written(r, graph), graph
    if entry == "5":
        lo, hi = graph
        b, closed = lo or hi
        return T5[tpl % len(T5)](r, sign(closed, less=not lo), b), graph
    lo, hi = graph
    return T6[tpl % len(T6)](r, (sign(lo[1]), sign(hi[1])), lo[0], hi[0]), graph

def numbers(prompt):
    return [int(n) for n in re.findall(r"\d+", prompt)]

def generate(entry, rng, seen, tries=400):
    tpl = rng.randrange(len(T5) * len(T6))           # chosen once, so templates that redraw often aren't rarer
    for _ in range(tries):
        try:
            prompt, graph = draw(entry, rng, tpl)
            small(*numbers(prompt))
            line = window(rng, graph)
        except Redraw:
            continue
        p = dict(type=entry, prompt=prompt, answer=canon(graph), graph=graph, line=line, source="template")
        if seen_key(p) in seen:
            continue
        if check(p) != "checked":                    # the independent check must agree with the build
            raise AssertionError(f"inequalities type {entry}: {p}")
        seen.add(seen_key(p))
        return p
    raise RuntimeError(f"could not draw an inequalities Type {entry} problem; check its template")

# ------------------------------------------------------------------
# Checking: solve the inequality again with sympy and compare its solution
# set with the graph at every boundary, between them, and beyond them
# ------------------------------------------------------------------
X = sp.Symbol("x")
OPS = {"<=": sp.Le, ">=": sp.Ge, "<": sp.Lt, ">": sp.Gt}
REL = re.compile(r"\s*(<=|>=|<|>)\s*")
AND_RE = re.compile(r'\s*(?:quad\s*)?"and"(?:\s*quad)?\s*|\s+and\s+')

def normal(text):
    return (text.replace("≤", "<=").replace("≥", ">=").replace("−", "-")
            .replace("⩽", "<=").replace("⩾", ">="))

def solution(text):
    """The set of x that make the inequality true (a sympy set); ValueError if unreadable."""
    from ..check import to_sympy
    s = sp.S.Reals
    try:
        for part in AND_RE.split(normal(text).strip()):
            bits = REL.split(part)
            if len(bits) not in (3, 5):
                raise ValueError("write one or two inequality signs")
            exprs = [to_sympy(e) for e in bits[0::2]]
            if any(e.free_symbols - {X} for e in exprs):
                raise ValueError("use only the variable x")
            for i, op in enumerate(bits[1::2]):
                s = s & sp.solve_univariate_inequality(OPS[op](exprs[i], exprs[i + 1]), X, relational=False)
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"can't read the inequality: {e}") from None
    return s

def inside(graph, v):
    lo, hi = graph
    return ((lo is None or v > lo[0] or (v == lo[0] and lo[1])) and
            (hi is None or v < hi[0] or (v == hi[0] and hi[1])))

def same(s, graph):
    """Is the sympy set s exactly the graph's set? Both are unions of intervals,
    so they agree everywhere if they agree at every endpoint and between."""
    ends = {Fraction(e[0]) for e in graph if e}
    ends |= {Fraction(str(b)) for b in s.boundary if b.is_finite}
    pts = sorted(ends) or [Fraction(0)]
    probes = pts + [(x + y) / 2 for x, y in zip(pts, pts[1:])] + [pts[0] - 1, pts[-1] + 1]
    return all(bool(s.contains(sp.Rational(v.numerator, v.denominator))) == inside(graph, v) for v in probes)

def fits(p):
    lo, hi = p["line"]
    return all(lo < e[0] < hi for e in p["graph"] if e)

def check(p):
    try:
        ok = same(solution(p["answer"]), p["graph"])
        if p["prompt"]:
            ok = ok and same(solution(p["prompt"]), p["graph"])
    except (ValueError, KeyError, TypeError):
        return "unchecked"
    return "checked" if ok and fits(p) else "failed"

def to_graph(s):
    """A sympy set -> a graph, or ValueError if a number line here can't show it."""
    if not isinstance(s, sp.Interval) or (s.start == -sp.oo and s.end == sp.oo):
        raise ValueError("the solution must be a ray or a segment")
    out = []
    for v, open_ in ((s.start, s.left_open), (s.end, s.right_open)):
        if v.is_infinite:
            out.append(None)
        elif not v.is_integer or abs(v) > BIG:
            raise ValueError(f"the boundary {v} must be a whole number from {-BIG} to {BIG}")
        else:
            out.append([int(v), not open_])
    return out

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
PREAMBLE = r"""// A number line for inequality problems: the integers lo..hi, labeled, with
// arrows at both ends. from/to: none (a ray off that end) or (value, closed?);
// with neither, the line is blank.
#let numline(lo, hi, from: none, to: none, ink: black) = layout(size => {
  let w = size.width
  let step = w / (hi - lo + 2)
  let x(v) = step * (v - lo + 1)
  let lab = calc.min(step * 0.45, 0.75em.to-absolute())
  let r = calc.min(step * 0.2, lab * 0.45)
  let y = r + 2pt
  let tk = r * 0.9
  let head(at, dir, fill, s) = place(top + left, dx: at, dy: y,
    polygon(fill: fill, stroke: none, (0pt, 0pt), (-dir * s, -s * 0.5), (-dir * s, s * 0.5)))
  box(width: w, height: y + tk + lab * 1.5, {
    place(top + left, line(start: (step * 0.3, y), end: (w - step * 0.3, y), stroke: 0.7pt))
    head(step * 0.15, -1, black, r * 1.4)
    head(w - step * 0.15, 1, black, r * 1.4)
    for v in range(lo, hi + 1) {
      place(top + left, line(start: (x(v), y - tk), end: (x(v), y + tk), stroke: 0.7pt))
      place(top + left, dx: x(v) - step, dy: y + tk + lab * 0.25,
        box(width: 2 * step, align(center, text(size: lab, str(v).replace("-", "\u{2212}")))))
    }
    if from != none or to != none {
      // Shading stops at an open dot's edge, so the dot shows the line underneath.
      let a = if from == none { step * 0.3 } else { x(from.at(0)) + if from.at(1) { 0pt } else { r } }
      let b = if to == none { w - step * 0.3 } else { x(to.at(0)) - if to.at(1) { 0pt } else { r } }
      place(top + left, line(start: (a, y), end: (b, y), stroke: r * 0.75 + ink))
      if from == none { head(step * 0.1, -1, ink, r * 2.2) }
      if to == none { head(w - step * 0.1, 1, ink, r * 2.2) }
      for end in (from, to) {
        if end != none {
          place(top + left, dx: x(end.at(0)) - r, dy: y - r,
            circle(radius: r, fill: if end.at(1) { ink } else { none }, stroke: 1.1pt + ink))
        }
      }
    }
  })
})
"""

def numline(p, graphed=False, ink=None):
    lo, hi = p["line"]
    args = [str(lo), str(hi)]
    if graphed:
        for name, e in zip(("from", "to"), p["graph"]):
            if e:
                args.append(f"{name}: ({e[0]}, {'true' if e[1] else 'false'})")
        if ink:
            args.append(f"ink: {ink}")
    return f"#numline({', '.join(args)})"

def typst(p, gap="0.3em"):
    if p["type"] in GRAPHED:
        return numline(p, graphed=True)
    return f"${p['prompt']}$ \\\n    {numline(p)}"

def key_typst(p, gap="0.3em"):
    """The key's prompt: types 3-6 have the graph drawn on the number line."""
    if p["type"] in GRAPHED:
        return typst(p, gap)
    return f"${p['prompt']}$ \\\n    {numline(p, graphed=True, ink='red')}"

def answer_typst(p):
    """What the key writes beside the problem: the inequality, or nothing when the graph is the answer."""
    return "" if p["type"] in ("3", "4") else f"${p['answer']}$"

def pretty(s):
    s = s.replace(AND, " and ").replace("<=", "≤").replace(">=", "≥")
    return s.replace(" - ", " − ").replace("-", "−")

def glyph(graph):
    """A small picture of the graph for the terminal: "−4 ○━━━● 1"."""
    lo, hi = graph
    def dot(e):
        return "●" if e[1] else "○"
    n = lambda e: pretty(str(e[0]))
    if lo is None:
        return f"◀━━━{dot(hi)} {n(hi)}"
    if hi is None:
        return f"{n(lo)} {dot(lo)}━━━▶"
    return f"{n(lo)} {dot(lo)}━━━{dot(hi)} {n(hi)}"

def text(p):
    if p["type"] in GRAPHED:
        return "graph: " + glyph(p["graph"])
    return pretty(p["prompt"])

def answer_text(p):
    if p["type"] in ("3", "4"):
        return glyph(p["graph"])
    return f"{pretty(p['answer'])}  {glyph(p['graph'])}" if p["type"] in ("5", "6") else pretty(p["answer"])

def height(p):
    """Inches the prompt takes on the page, for page estimates."""
    return 0.4 if p["type"] in GRAPHED else 0.65

# ------------------------------------------------------------------
# Hand editing. Types 1-2: the inequality the graph shows. Types 3-6: the prompt.
# ------------------------------------------------------------------
def edit_text(p):
    return p["answer"] if p["type"] in GRAPHED else p["prompt"].replace(AND, " and ")

def from_edit(text, old):
    t = " ".join(normal(text).split())
    if not t:
        raise ValueError("write an inequality, like x <= 1 or -4 < x <= 1")
    graph = to_graph(solution(t))
    if old["type"] in COMPOUND and not all(graph):
        raise ValueError(f"Type {old['type']} is a compound inequality: its solution is a segment, like -4 < x <= 1")
    if old["type"] not in COMPOUND and all(graph):
        raise ValueError(f"Type {old['type']} has one boundary: its solution is a ray, like x <= 1")
    prompt = "" if old["type"] in GRAPHED else re.sub(r"\s+and\s+", AND, t)
    new = dict(old, prompt=prompt, answer=canon(graph), graph=graph, source="edited")
    if not fits(new):                                # center the line on the new graph
        ends = [e[0] for e in graph if e]
        first = max(-BIG, min(BIG - SPAN, (min(ends) + max(ends)) // 2 - SPAN // 2))
        new["line"] = [first, first + SPAN]
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, text):
    t = " ".join(normal(text).split())
    try:
        s = solution(t)
    except ValueError:
        raise ValueError("write the answer as an inequality, like x <= 1 or -4 < x <= 1") from None
    new = dict(p, answer=t)
    return new, ("checked" if same(s, p["graph"]) else "failed")

def selftest(n, seed):
    rng = random.Random(seed)
    for k in KEYS:
        seen = set()
        for i in range(n):
            if i % 40 == 0:                          # types 1-4 have fewer than 100 graphs each
                seen = set()
            p = generate(k, rng, seen)
            assert all(abs(v) <= BIG for v in numbers(p["prompt"]) + p["line"]), p
        print(f"inequalities {label(TYPE[k]):8} {n} drawn, all verified")
    return True
