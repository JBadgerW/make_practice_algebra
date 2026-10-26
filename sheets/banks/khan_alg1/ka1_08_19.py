"""Khan Algebra 1, Lesson 8-19: Average rate of change: graphs & tables,
from the old app's Alg1_08_19 (forty of Khan's, the graphs as screenshots,
without answers).

The graph goes through lattice points (walk.py), so f at every whole x is
read off a grid point. Type 1: the average rate of change of f over an
interval, -6 <= x <= 3 or [2, 6], exactly (a fraction if need be, as
Khan's "Give an exact number"). Type 2: over which of four intervals is
the average rate of change positive (negative, zero)? Exactly one. The
function is f, g, or h, its input x or t, as in Khan's.

A problem: dict(type, ys, letter, var, brackets, interval or (ask, choices), answer, source).
    ys  f at -8, ..., 8    interval [-6, 3]    answer "-2/3"
check() reads f at the ends off the graph's points: (f(b) - f(a))/(b - a).
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from ...typmath import display, dfrac
from ...linear import exact
from . import courses
from . import walk

NAME = FAMILY = "ka1_08_19"
FIXED = False
TITLE = "Lesson 8-19: Average rate of change: graphs & tables"
INSTRUCTIONS = ""
COURSES = courses(8)
X0, X1 = -8, 8
SIGN = {"positive": lambda v: v > 0, "negative": lambda v: v < 0, "zero": lambda v: v == 0}

TYPES = [
    dict(key="1", title="Over an Interval", instructions="Give an exact number.",
         look="A graph and an interval of inputs.",
         move="Read f at both ends of the interval. Average rate of change = (f(b) - f(a))/(b - a).", width="full"),
    dict(key="2", title="Which Interval?", instructions="Choose 1 answer.",
         look="A graph and four intervals: on which is the average rate of change positive (negative, zero)?",
         move="Compare f at the two ends of each interval: higher at the right end is positive, lower is negative, "
              "the same is zero.", width="full"),
]
T = gen.Types(TYPES, "", space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p["ys"]), str(p.get("interval") or p.get("choices")))

def rate(ys, a, b):
    return F(walk.value(ys, X0, b) - walk.value(ys, X0, a)) / (b - a)

def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

def interval(r):
    a = r.randint(X0, X1 - 2)
    return [a, r.randint(a + 2, min(X1, a + 10))]

def draw(entry, r, tpl):
    ys = walk.walk(r, X0, X1)
    common = dict(ys=ys, letter=r.choice("fgh"), var=r.choice("xt"), brackets=r.random() < 0.4)
    if entry == "1":
        iv = interval(r)
        return dict(common, interval=iv, answer=frac(rate(ys, *iv)))
    ask = r.choice(list(SIGN))
    pool = [interval(r) for _ in range(80)]
    yes = [iv for iv in pool if SIGN[ask](rate(ys, *iv))]
    no = list(dict.fromkeys(tuple(iv) for iv in pool if not SIGN[ask](rate(ys, *iv))))
    need(yes and len(no) >= 3)
    key = lambda iv: f"{iv[0]},{iv[1]}"                          # strings: lettered() reads a tuple as several
    choices, letter = gen.lettered(r, key(yes[0]), [key(iv) for iv in r.sample(no, 3)])
    return dict(common, ask=ask, choices=[[int(v) for v in c.split(",")] for c in choices], answer=letter)

def check(p):
    try:
        if p["type"] == "1":
            return "checked" if F(str(exact(p["answer"]))) == rate(p["ys"], *p["interval"]) else "failed"
        right = [gen.ABC[i] for i, iv in enumerate(p["choices"]) if SIGN[p["ask"]](rate(p["ys"], *iv))]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def written(iv, p):
    return f"[{iv[0]}, {iv[1]}]" if p["brackets"] else f"{iv[0]} <= {p['var']} <= {iv[1]}"

def graph(p, key=False):
    g = Graph(x=(X0, X1), y=(-8, 8), width=5.2, xlabel=p["var"])
    walk.draw(g, p["ys"], X0)
    g.label_at(X1, p["ys"][-1], f"${p['letter']}$", anchor="west", color="blue", size=9)
    if key and p["type"] == "1":
        for x in p["interval"]:
            g.point(x, p["ys"][x - X0], color="red")
    return g.typst()

def question(p):
    f = p["letter"]
    if p["type"] == "1":
        return f"What is the average rate of change of ${f}$ over the interval ${written(p['interval'], p)}$?"
    words = {"zero": "an average rate of change of zero", "positive": "a positive average rate of change",
             "negative": "a negative average rate of change"}[p["ask"]]
    items = [f"${written(iv, p)}$" for iv in p["choices"]]
    return f"Over which interval does ${f}$ have {words}? #v(0.3em) {gen.choices_typst(items)}"

def typst(p, gap="0.3em", key=False):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{question(p)}], [{graph(p, key)}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    if p["type"] == "1":
        return display(dfrac(p["answer"]))
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. ${written(p['choices'][gen.ABC.index(a)], p)}$"

def text(p):
    head = f"{p['letter']} through {list(zip(range(X0, X1 + 1), p['ys']))}"
    if p["type"] == "1":
        return f"{head}  rate over {p['interval']}?"
    return f"{head}  {p['ask']}?  " + gen.choices_text([str(c) for c in p["choices"]])

def answer_text(p):
    return p["answer"] if p["type"] == "1" else answer_typst(p).replace("$", "").replace("<=", "≤")

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "2":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
