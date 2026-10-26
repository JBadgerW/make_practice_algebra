"""Khan Algebra 1, Lesson 8-21: Evaluate inverse functions, from the old app's
Alg1_08_21 (twenty-four of Khan's, the graphs as screenshots, without
answers).

Type 1: a table of some inputs and outputs of an invertible function f;
find two values, Khan's kinds: f^(-1)(a) + f(b), f^(-1)(a), and
f^(-1)(f(c)) for a c not in the table (it's c). Type 2: the graph of an
invertible f (strictly rising or falling through lattice points); find
f^(-1)(k). Type 3: the graph of y = h(x) is a segment; graph its inverse.
The student draws; the key draws the inverse segment in red, with y = x
dashed, and names its ends.

A problem: dict(type, ..., answer, source).
    Type 1  table [[-14, 3], [-2, 7], ...] (x, f(x)), parts ["finv(1) + f(-14)", "finv(f(93))"], answer "(a) 5; (b) 93"
    Type 2  pts [[-6, -5], [-5, -3], ...], k -3, answer "-5"
    Type 3  seg [[-4, 1], [3, 6]], answer "from (1, -4) to (6, 3)"
check() works each value out from the table or the points (f^(-1)(a) is
the x with f(x) = a); Type 3, the answer's ends are the segment's with x
and y traded.
"""
import re
from ... import gen
from ...gen import need, signed
from ...graphs import Graph, PREAMBLE
from . import courses

NAME = FAMILY = "ka1_08_21"
FIXED = False
TITLE = "Lesson 8-21: Evaluate inverse functions"
INSTRUCTIONS = ""
COURSES = courses(8)

TYPES = [
    dict(key="1", title="From a Table", instructions="Find each value.",
         look="A table of inputs and outputs of f, and expressions with f and f^(-1).",
         move="f^(-1)(a) is the input that gives the output a: find a in the outputs column. f^(-1)(f(c)) undoes f: "
              "it's c.", width="full"),
    dict(key="2", title="From a Graph", instructions="Find each value.",
         look="The graph of f and a value of its inverse to find.",
         move="f^(-1)(k) is the x where f(x) = k: find k on the y-axis, go across to the graph, read its x.",
         width="full"),
    dict(key="3", title="Graph the Inverse", instructions="Graph each inverse on the grid.",
         look="The graph of y = h(x), a line segment.",
         move="Trade x and y in each endpoint: (a, b) becomes (b, a). Connect the new endpoints; it's the mirror "
              "image across y = x.", width="full"),
]
T = gen.Types(TYPES, "", space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p.get("table") or p.get("pts") or p.get("seg")), str(p.get("parts") or p.get("k")))

EXPR = re.compile(r"(finv|f)\((-?\d+|f\(-?\d+\))\)")

def evaluate(expr, pairs):
    """finv(1) + f(-14), finv(f(93)), finv(5): from the table's pairs."""
    fwd = {x: y for x, y in pairs}
    inv = {y: x for x, y in pairs}
    total = 0
    for term in expr.split("+"):
        term = term.strip()
        m = re.fullmatch(r"finv\(f\((-?\d+)\)\)", term)
        if m:
            total += int(m.group(1))                              # f^(-1)(f(c)) = c, in the table or not
            continue
        m = re.fullmatch(r"(finv|f)\((-?\d+)\)", term)
        total += (inv if m.group(1) == "finv" else fwd)[int(m.group(2))]
    return total

def table_problem(r):
    xs = r.sample(range(-15, 16), 5)
    ys = r.sample(range(-15, 16), 5)
    pairs = [[x, y] for x, y in zip(xs, ys)]
    (x1, y1), (x2, _), (x3, y3) = r.sample(pairs, 3)
    c = r.choice([v for v in range(-99, 100) if v not in xs and abs(v) > 20])
    parts = r.sample([f"finv({y1}) + f({x2})", f"finv({y3})", f"finv(f({c}))"], 2)
    return dict(table=pairs, parts=parts,
                answer="; ".join(f"({l}) {evaluate(e, pairs)}" for l, e in zip("ab", parts)))

def graph_problem(r):
    a = r.randint(-8, -4)
    b = r.randint(a + 5, 8)
    up = r.choice((1, -1))
    y = r.randint(-7, 7)
    pts = [[a, y]]
    for x in range(a + 1, b + 1):
        y += up * r.choice((1, 1, 2))
        need(-8 < y < 8)
        pts.append([x, y])
    x, k = r.choice(pts)
    return dict(pts=pts, k=k, answer=str(x))

def segment_problem(r):
    p = [r.randint(-7, 7), r.randint(-7, 7)]
    q = [r.randint(-7, 7), r.randint(-7, 7)]
    need(p[0] != q[0] and p[1] != q[1] and abs(p[0] - q[0]) + abs(p[1] - q[1]) >= 5 and p != p[::-1])
    return dict(seg=[p, q], answer=f"from ({p[1]}, {p[0]}) to ({q[1]}, {q[0]})")

def draw(entry, r, tpl):
    return {"1": table_problem, "2": graph_problem, "3": segment_problem}[entry](r)

PART = re.compile(r"\(([ab])\)\s*(-?\d+)")
END = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")

def check(p):
    try:
        if p["type"] == "1":
            got = dict(PART.findall(p["answer"]))
            ok = len(got) == 2 and all(int(got[l]) == evaluate(e, p["table"]) for l, e in zip("ab", p["parts"]))
        elif p["type"] == "2":
            xs = [x for x, y in p["pts"] if y == p["k"]]
            ok = len(xs) == 1 and int(p["answer"]) == xs[0]
        else:
            ends = sorted([int(a), int(b)] for a, b in END.findall(p["answer"]))
            ok = ends == sorted([q[1], q[0]] for q in p["seg"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def math(expr):
    return expr.replace("finv", "f^(-1)")

def typst(p, gap="0.3em", key=False):
    if p["type"] == "1":
        cells = ", ".join(f"[${x}$], [${y}$]" for x, y in p["table"])
        table = (f"#table(columns: 2, inset: 5pt, align: center, fill: (_, row) => if row == 0 {{ luma(230) }}, "
                 f"[$x$], [$f(x)$], {cells})")
        parts = ", ".join(f"[${math(e)} =$]" for e in p["parts"])
        return (f"The table shows some inputs and outputs of the invertible function $f$, whose domain is all real "
                f"numbers. \\\n    #grid(columns: (auto, 1fr), column-gutter: 2em, [{table}], [#parts({parts})])")
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    if p["type"] == "2":
        g.polyline(p["pts"], ends="closed")
        if key:
            g.point(int(p["answer"]), p["k"], color="red")
        q = f"The graph of the invertible function $f$ is shown. What is the value of $f^(-1)({p['k']})$?"
    else:
        (a, b), (c, d) = p["seg"]
        g.segment((a, b), (c, d), dash="dashed")
        if key:
            g.line(1, 0, color="gray", dash="dotted", width=0.8)
            g.segment((b, a), (d, c), color="red")
        q = "The graph of $y = h(x)$ is the dashed segment. Graph its inverse, $y = h^(-1)(x)$."
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{q}], [{g.typst()}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    if p["type"] == "1":
        return "; ".join(f"({l}) ${v}$" for l, v in PART.findall(p["answer"]))
    if p["type"] == "2":
        return f"$f^(-1)({p['k']}) = {p['answer']}$"
    return "The segment " + END.sub(lambda m: f"$({m.group(1)}, {m.group(2)})$", p["answer"])

def text(p):
    if p["type"] == "1":
        return f"table {p['table']}: " + "; ".join(math(e) for e in p["parts"])
    if p["type"] == "2":
        return f"f through {p['pts']}: f^(-1)({p['k']})?"
    return f"inverse of the segment {p['seg']}"

def answer_text(p):
    return p["answer"]

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new problem; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
