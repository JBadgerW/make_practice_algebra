"""Khan Algebra 1, Lesson 8-5: Function inputs & outputs: graph, from the
old app's Alg1_08_05 (sixteen generated slots, drawn in TikZ).

The graph of g goes from x = -10 to 10 through lattice points (walk.py).
Type 1: the input for which g(x) = k. Type 2: the input other than a given
one for which g(x) = k. Type 3: select all the inputs, from three whole
numbers and "None of the above". The old app counted only the grid points,
but the graph is straight between them, so g(x) = k can also hold between
two of them; here every solution of g(x) = k on the whole graph is
counted, and k is chosen so the question has the answer it claims: one
input (Type 1), two (Type 2), and for Type 3, whole numbers only.

A problem: dict(type, ys, k, given (Type 2), choices (Type 3), answer, source).
    ys  g at -10, ..., 10    k -3    answer "x = 4" (Types 1, 2) or "B, C" (Type 3)
check() finds every x with g(x) = k on the graph (walk.solutions).
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from . import courses
from . import walk

NAME = FAMILY = "ka1_08_05"
FIXED = False
TITLE = "Lesson 8-5: Function inputs & outputs: graph"
INSTRUCTIONS = "Use the graph of g to answer each question."
COURSES = courses(8)
X0, X1 = -10, 10
NONE = "None of the above"

TYPES = [
    dict(key="1", title="The One Input",
         look="An output of g, reached at one input.",
         move="Find the output on the y-axis, go across to the graph, then down or up to the x-axis.", width="full"),
    dict(key="2", title="The Other Input",
         look="An output of g reached at two inputs, one of them given.",
         move="Go across from the output: the graph meets that height twice. The answer is the other crossing.",
         width="full"),
    dict(key="3", title="Select All the Inputs",
         look="An output of g and three inputs to test.",
         move="Check each input: go up or down to the graph and read its output. If none gives the output, choose "
              "None of the above.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p["ys"]), p["k"])

def whole(xs):
    return xs != "many" and all(x.denominator == 1 for x in xs)

def draw(entry, r, tpl):
    ys = walk.walk(r, X0, X1, -10, 10)
    levels = range(min(ys), max(ys) + 1)
    if entry == "1":
        ks = [k for k in levels if walk.solutions(ys, X0, k) != "many" and len(walk.solutions(ys, X0, k)) == 1
              and whole(walk.solutions(ys, X0, k))]                # Khan: "the integer input"
        need(ks)
        k = r.choice(ks)
        return dict(ys=ys, k=k, answer=f"x = {walk.solutions(ys, X0, k)[0]}")
    if entry == "2":
        ks = [k for k in levels if walk.solutions(ys, X0, k) != "many" and len(walk.solutions(ys, X0, k)) == 2
              and whole(walk.solutions(ys, X0, k))]
        need(ks)
        k = r.choice(ks)
        given, other = r.sample(walk.solutions(ys, X0, k), 2)
        return dict(ys=ys, k=k, given=int(given), answer=f"x = {other}")
    some = r.random() < 0.65                                      # one or two inputs work, or none does
    ks = [k for k in range(-9, 10) if whole(walk.solutions(ys, X0, k))
          and (1 <= len(walk.solutions(ys, X0, k)) <= 2 if some else not walk.solutions(ys, X0, k))]
    need(ks)
    k = r.choice(ks)
    right = [int(x) for x in walk.solutions(ys, X0, k)]
    wrong = [x for x in range(X0, X1 + 1) if x not in right]
    shown = sorted(right + r.sample(wrong, 3 - len(right)))     # every input that works is offered
    choices = [f"$x = {x}$" for x in shown] + [NONE]
    picks = [c for c, x in zip(choices, shown) if x in right] or [NONE]
    choices, answer = gen.in_order(choices, picks)
    return dict(ys=ys, k=k, choices=choices, answer=answer)

def check(p):
    try:
        xs = walk.solutions(p["ys"], X0, p["k"])
        if xs == "many":
            return "failed"
        if p["type"] == "1":
            ok = len(xs) == 1 and p["answer"] == f"x = {xs[0]}"
        elif p["type"] == "2":
            ok = len(xs) == 2 and p["given"] in xs and p["answer"] == f"x = {[x for x in xs if x != p['given']][0]}"
        else:
            right = [gen.ABC[i] for i, c in enumerate(p["choices"])
                     if c != NONE and F(c.strip("$").split("=")[1]) in xs]
            listed = {F(c.strip("$").split("=")[1]) for c in p["choices"] if c != NONE}
            ok = set(xs) <= listed and gen.letters_of(p["answer"]) == (right or [gen.ABC[p["choices"].index(NONE)]])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p, key=False):
    g = Graph(x=(X0, X1), y=(-10, 10), width=6.4)
    walk.draw(g, p["ys"], X0)
    g.label_at(X1, p["ys"][-1], "$g$", anchor="west", color="blue", size=9)
    if key:
        for x in walk.solutions(p["ys"], X0, p["k"]):
            g.point(float(x), p["k"], color="red")
    return g.typst()

def question(p):
    k = p["k"]
    if p["type"] == "1":
        return f"What is the input value for which $g(x) = {k}$? #v(0.6em) $x =$"
    if p["type"] == "2":
        return f"What is the input value other than $x = {p['given']}$ for which $g(x) = {k}$? #v(0.6em) $x =$"
    return f"Select all input values for which $g(x) = {k}$. #v(0.3em) {gen.choices_typst(p['choices'])}"

def typst(p, gap="0.3em", key=False):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{question(p)}], [{graph(p, key)}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    return f"${p['answer']}$" if p["type"] != "3" else gen.choice_answer_typst(p)

def text(p):
    q = {"1": f"g(x) = {p['k']}: x?", "2": f"g(x) = {p['k']}, other than x = {p.get('given')}: x?",
         "3": f"g(x) = {p['k']}: " + gen.choices_text([c.strip("$") for c in p.get("choices", [])])}[p["type"]]
    return f"{q}   g through {list(zip(range(X0, X1 + 1), p['ys']))}"

def answer_text(p):
    return p["answer"] if p["type"] != "3" else gen.choice_answer_typst(p).replace("$", "")

def height(p):
    return 2.8

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "3":
        return gen.with_letters(p, t, check)
    t = t.strip().replace("−", "-")
    new = dict(p, answer=t if t.startswith("x") else f"x = {t}")
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
