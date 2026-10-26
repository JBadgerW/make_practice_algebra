"""Khan Algebra 1, Lesson 8-2: Evaluate functions from their graph, from the
old app's Alg1_08_02 (eighteen generated slots, drawn in TikZ; answers
computed, right).

f(3) = ? The graph of f goes from x = -8 to 8 through lattice points, a
step up or down from each integer to the next (walk.py, the old app's
steps); the input is a whole number, so the output is read off a grid
point.

A problem: dict(type, ys, x, prompt, answer, source).
    ys  [2, 3, 3, 4, ...]  (f at -8, -7, ..., 8)    x 3    answer "-1"
check() reads f(x) off the points the graph is drawn through.
"""
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from . import courses
from . import walk

NAME = FAMILY = "ka1_08_02"
FIXED = False
TITLE = "Lesson 8-2: Evaluate functions from their graph"
INSTRUCTIONS = "Use the graph to find each value."
COURSES = courses(8)
X0, X1 = -8, 8

TYPES = [
    dict(key="1", title="Read f(a) off the Graph",
         look="The graph of f and an input.",
         move="Go to the input on the x-axis, straight up or down to the graph, then across to the y-axis: that's "
              "the output.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, str(p["ys"]), p["x"])

def draw(entry, r, tpl):
    ys = walk.walk(r, X0, X1)
    x = r.randint(X0, X1)
    return dict(ys=ys, x=x, prompt=f"f({x})", answer=str(ys[x - X0]))

def check(p):
    try:
        return "checked" if int(p["answer"]) == walk.value(p["ys"], X0, p["x"]) and p["prompt"] == f"f({p['x']})" else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p, key=False):
    g = Graph(x=(X0, X1), y=(-8, 8), width=5.2)
    walk.draw(g, p["ys"], X0)
    g.label_at(X1, p["ys"][-1], "$f$", anchor="west", color="blue", size=9)
    if key:
        g.point(p["x"], p["ys"][p["x"] - X0], color="red")
    return g.typst()

def typst(p, gap="0.3em", key=False):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [${p['prompt']} =$], [{graph(p, key)}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    return f"${p['prompt']} = {p['answer']}$"

def text(p):
    return f"{p['prompt']} = ?   f through {list(zip(range(X0, X1 + 1), p['ys']))}"

def answer_text(p):
    return p["answer"]

def height(p):
    return 2.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=t.strip().replace("−", "-"))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
