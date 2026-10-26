"""Khan Algebra 1, Lesson 8-3: Evaluate function expressions, from the old
app's Alg1_08_03 (twelve generated slots, drawn in TikZ; answers computed,
right).

-3 f(4) + 5 g(-6) = ? The graphs of f (solid blue) and g (dashed red) go
from x = -10 to 10 through lattice points (walk.py); a and c are 2 to 10
in size, either sign, as the old app drew them.

A problem: dict(type, f, g, a, b, c, d, prompt, answer, source).
    f, g  their y's at -10, ..., 10    prompt "-3 dot f(4) + 5 dot g(-6)"    answer "13"
check() reads f(b) and g(d) off the points and computes a f(b) + c g(d).
"""
from ... import gen
from ...gen import need, signed
from ...graphs import Graph, PREAMBLE
from . import courses
from . import walk

NAME = FAMILY = "ka1_08_03"
FIXED = False
TITLE = "Lesson 8-3: Evaluate function expressions"
INSTRUCTIONS = "Use the graphs to evaluate each expression."
COURSES = courses(8)
X0, X1 = -10, 10

TYPES = [
    dict(key="1", title="Combine Two Functions' Values",
         look="An expression like a f(b) + c g(d), and the graphs of f and g.",
         move="Read f(b) off f's graph and g(d) off g's. Then multiply and add, minding the signs.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], str(p["f"]), str(p["g"]))

def expression(a, b, c, d):
    return f"{a} dot f({b}) {'+' if c > 0 else '-'} {abs(c)} dot g({d})"

def draw(entry, r, tpl):
    f, g = walk.walk(r, X0, X1, -10, 10), walk.walk(r, X0, X1, -10, 10)
    need(sum(x != y for x, y in zip(f, g)) > 12)                 # two graphs you can tell apart
    a, c = signed(r, 2, 10), signed(r, 2, 10)
    b, d = r.randint(X0, X1), r.randint(X0, X1)
    return dict(f=f, g=g, a=a, b=b, c=c, d=d, prompt=expression(a, b, c, d),
                answer=str(a * f[b - X0] + c * g[d - X0]))

def check(p):
    try:
        v = p["a"] * walk.value(p["f"], X0, p["b"]) + p["c"] * walk.value(p["g"], X0, p["d"])
        ok = int(p["answer"]) == v and p["prompt"] == expression(p["a"], p["b"], p["c"], p["d"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p, key=False):
    gr = Graph(x=(X0, X1), y=(-10, 10), width=6.4)
    walk.draw(gr, p["f"], X0, color="blue")
    walk.draw(gr, p["g"], X0, color="red", dash="dashed")
    gr.label_at(X1, p["f"][-1], "$f$", anchor="west", color="blue", size=9)
    gr.label_at(X1, p["g"][-1], "$g$", anchor="west", color="red", size=9)
    if key:
        gr.point(p["b"], p["f"][p["b"] - X0], color="blue")
        gr.point(p["d"], p["g"][p["d"] - X0], color="red")
    return gr.typst()

def typst(p, gap="0.3em", key=False):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [${p['prompt']} =$], [{graph(p, key)}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    fb, gd = p["f"][p["b"] - X0], p["g"][p["d"] - X0]
    return f"${p['answer']}$ ($f({p['b']}) = {fb}$, $g({p['d']}) = {gd}$)"

def text(p):
    return p["prompt"].replace(" dot ", " · ") + " = ?"

def answer_text(p):
    return p["answer"]

def height(p):
    return 2.8

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for new graphs; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=t.strip().replace("−", "-"))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
