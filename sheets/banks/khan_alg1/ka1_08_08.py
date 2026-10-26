"""Khan Algebra 1, Lesson 8-8: Domain and range from graph, from the old
app's Alg1_08_08 (twenty-four of Khan's, the graphs as screenshots, without
answers).

What is the domain (Type 1) or the range (Type 2) of f? The graph is a
curve with closed ends (curves.py) or a set of separate points, as Khan's
are. Choose 1 of four, in Khan's two forms: an interval, -6 <= x <= 2 (or
-6 <= f(x) <= 2), or a list, "The x-values -6, -5, 2, 3, and 4". The
wrong ones are Khan's: the other axis's values, an end misread, the list
for a curve or the interval for points.

A problem: dict(type, kind, graph, choices, answer, source).
    kind   "curve" (graph: knots, the ends closed) or "points" (graph: the points)
    choices  [["int", -6, 2], ["vals", [-6, -5, 2]], ...]   (written with x or f(x) by type)
check() works the domain or range out from the graph and finds it among
the choices: exactly the answer's.
"""
import ast
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from . import courses
from . import curves

NAME = FAMILY = "ka1_08_08"
FIXED = False
TITLE = "Lesson 8-8: Domain and range from graph"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="The Domain",
         look="The whole graph of f: a curve or separate points.",
         move="The domain is every x the graph covers: read left to right. A curve covers an interval; separate "
              "points cover just their x-values.", width="full"),
    dict(key="2", title="The Range",
         look="The whole graph of f: a curve or separate points.",
         move="The range is every output the graph reaches: read bottom to top, from the lowest point to the highest.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p["graph"]))

def truth(p):
    """The domain (Type 1) or range (Type 2), as choice data."""
    pts = [tuple(q) for q in p["graph"]]
    i = 0 if p["type"] == "1" else 1
    vals = sorted({q[i] for q in pts})
    if p["kind"] == "points":
        return ["vals", vals]
    return ["int", vals[0], vals[-1]]                                # a curve: its knots hold its ends and extremes

def draw(entry, r, tpl):
    kind = r.choice(("curve", "curve", "points"))
    if kind == "curve":
        a = r.randint(-7, -2)                                       # the ends inside the grid
        b = r.randint(a + 5, 7)
        graph = [list(k) for k in curves.knots(r, a, b, -7, 7, gap=(2, 4))]
    else:
        xs = sorted(r.sample(range(-7, 8), r.randint(4, 5)))
        graph = [[x, r.randint(-7, 7)] for x in xs]
    p = dict(type=entry, kind=kind, graph=graph)
    right = truth(p)
    other = truth(dict(p, type="2" if entry == "1" else "1"))
    vals = sorted({q[0 if entry == "1" else 1] for q in graph})
    wrong = [other]
    if right[0] == "int":
        lo, hi = right[1], right[2]
        wrong += [["int", lo, hi + r.choice((-2, -1, 1, 2))], ["int", lo + r.choice((-2, -1, 1, 2)), hi],
                  ["vals", vals[:5]]]
    else:
        wrong += [["int", vals[0], vals[-1]], ["vals", sorted(set(vals[:-1] + [vals[-1] + r.choice((1, 2))]))]]
    wrong = [w for w in wrong if w != right and not (w[0] == "int" and w[1] >= w[2])]
    wrong = [w for i, w in enumerate(wrong) if w not in wrong[:i]]
    need(len(wrong) >= 3)
    choices, answer = gen.lettered(r, str(right), [str(w) for w in r.sample(wrong, 3)])
    return dict(kind=kind, graph=graph, choices=[ast.literal_eval(c) for c in choices], answer=answer)

def check(p):
    try:
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if list(c) == truth(p)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def words(c, var):
    if c[0] == "int":
        return f"${c[1]} <= {var} <= {c[2]}$"
    *first, last = [f"${v}$" for v in c[1]]
    return f"The ${var}$-values {', '.join(first)}, and {last}"

def var(p):
    return "x" if p["type"] == "1" else "f(x)"

def graph(p):
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    if p["kind"] == "curve":
        curves.draw(g, [tuple(k) for k in p["graph"]], ends="closed")
    else:
        for x, y in p["graph"]:
            g.point(x, y, color="blue")
    return g.typst()

def typst(p, gap="0.3em"):
    q = f"The graph shows all of $f$. What is the {'domain' if p['type'] == '1' else 'range'} of $f$?"
    left = f"{q} #v(0.3em) {gen.choices_typst([words(c, var(p)) for c in p['choices']])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return "; ".join(f"{a}. {words(p['choices'][gen.ABC.index(a)], var(p))}" for a in gen.letters_of(p["answer"]))

def text(p):
    return f"{p['kind']} {p['graph']}   " + gen.choices_text([words(c, var(p)).replace("$", "") for c in p["choices"]])

def answer_text(p):
    return answer_typst(p).replace("$", "").replace("<=", "≤")

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
