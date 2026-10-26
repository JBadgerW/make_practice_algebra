"""Khan Algebra 1, Lesson 6-11: Number of solutions to a system of equations
graphically, from the old app's Alg1_06_11 (twelve generated slots, drawn
in TikZ; answers computed, right).

A system in standard form, its two lines graphed: exactly one solution
(the lines cross), no solutions (parallel), or infinitely many (the same
line, the second equation a multiple of the first; it's drawn dashed over
the first so both show). Slopes are dy/dx with dy up to 5 and dx up to 4,
as the old app drew them. Khan's three choices in Khan's order; the three
answers are spread evenly over a sheet.

A problem: dict(type, prompt, choices, answer, source).
    prompt  "-2 x + 3 y = 6 ; -4 x + 6 y = 12"   (twovar's "eq1 ; eq2")
check() solves the system (twovar.solve): one solution, none, or many.
"""
import math
from ... import gen
from ...gen import need, signed
from ...graphs import Graph, PREAMBLE
from . import courses
from .twovar import solve, system_typst, coefficients, equations, standard, text as system_text

NAME = FAMILY = "ka1_06_11"
FIXED = False
TITLE = "Lesson 6-11: Number of solutions to a system of equations graphically"
INSTRUCTIONS = "How many solutions does each system have? You can use the graph to decide."
COURSES = courses(6)
CHOICES = ["Exactly one solution", "No solutions", "Infinitely many solutions"]
KIND = {"one": "A", "none": "B", "many": "C"}

TYPES = [
    dict(key="1", title="How Many Solutions?",
         look="A system of two equations and the graph of its lines.",
         move="Lines that cross: one solution. Parallel lines (the same slope, different intercepts): none. The same "
              "line twice: infinitely many.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def line(dy, dx, b):
    """y = (dy/dx) x + b in standard form: -dy x + dx y = b dx, reduced, x positive."""
    A, B, C = -dy, dx, b * dx
    g = math.gcd(math.gcd(A, B), C)
    A, B, C = A // g, B // g, C // g
    if A < 0:
        A, B, C = -A, -B, -C
    return A, B, C

def draw(entry, r, tpl, want=None):
    kind = {"A": "one", "B": "none", "C": "many"}[want] if want else r.choice(list(KIND))
    dy, dx, b1 = signed(r, 1, 5), r.randint(1, 4), signed(r, 1, 7)
    need(math.gcd(abs(dy), dx) == 1)
    A, B, C = line(dy, dx, b1)
    first = standard(A, B, C)
    if kind == "many":
        k = r.choice((2, 3, -1, -2))
        second = standard(k * A, k * B, k * C)
    elif kind == "none":
        b2 = r.choice([b for b in range(max(b1 - 5, -7), min(b1 + 5, 7) + 1) if b not in (b1, 0)])
        second = standard(*line(dy, dx, b2))
    else:
        dy2, dx2 = signed(r, 1, 5), r.randint(1, 4)
        need(dy2 * dx != dy * dx2 and math.gcd(abs(dy2), dx2) == 1)
        b2 = r.choice([b for b in range(max(b1 - 5, -7), min(b1 + 5, 7) + 1) if b])
        second = standard(*line(dy2, dx2, b2))
        x, y = solve(f"{first} ; {second}")
        need(abs(x) <= 7 and abs(y) <= 7)                          # the crossing shows on the graph
    prompt = f"{first} ; {second}" if r.random() < 0.5 else f"{second} ; {first}"
    choices, answer = gen.in_order(CHOICES, CHOICES["ABC".index(KIND[kind])])
    return dict(prompt=prompt, choices=choices, answer=answer)

def check(p):
    try:
        s = solve(p["prompt"])
        kind = "one" if isinstance(s, tuple) else s
        return "checked" if gen.letters_of(p["answer"]) == [KIND[kind]] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("ABC", lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def graph(p):
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    for q, color, dash in zip(equations(p["prompt"]), ("blue", "red"), (None, "dashed")):
        a, b, c = coefficients(q)
        g.line(float(-a / b), float(c / b), color=color, dash=dash)
    return g.typst()

def typst(p, gap="0.3em"):
    left = f"{system_typst(p['prompt'])} #v(0.6em) {gen.choices_typst(p['choices'])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return system_text(p) + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 2.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new system; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
