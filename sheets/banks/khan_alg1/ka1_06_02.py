"""Khan Algebra 1, Lesson 6-2: Systems of equations with graphing, from the
old app's Alg1_06_02 (eighteen generated slots, drawn in TikZ; answers
computed, right).

Find the solution of the system; the two lines are graphed beside it.
Khan's two shapes: equations in standard form, each line through the
solution and its y-intercept (the old slots), or in slope-intercept form
with whole-number slopes (the old system_int_coef_slope_int). The solution
is a lattice point in -7..7, so it can be read off the graph. Type 1:
write x and y. Type 2: choose 1 of four points, the old app's wrong ones:
x and y traded, x one off, and that one traded.

A problem: dict(type, prompt, answer, source) (Type 2 adds choices).
    prompt  "3 x - 4 y = 2 ; x + 2 y = 4"      (twovar's "eq1 ; eq2")
    answer  "x = 2, y = 1"  or "C"
check(): the answer satisfies both equations, the system's one solution
(twovar.solves); for Type 2, exactly the answer's point does. The graph
is drawn from the equations themselves.
"""
import math
from fractions import Fraction as F
from ... import gen
from ...gen import need, signed
from ...graphs import Graph, PREAMBLE
from . import courses
from .twovar import solve, solves, letters, system_typst, answer_text, answer_of, text as system_text, standard, coefficients, equations

NAME = FAMILY = "ka1_06_02"
FIXED = False
TITLE = "Lesson 6-2: Systems of equations with graphing"
INSTRUCTIONS = "Find the solution to each system of equations. You can use the graph to find it."
COURSES = courses(6)
COLORS = ("blue", "red")

TYPES = [
    dict(key="1", title="Read the Solution",
         look="A system of two equations and the graph of its two lines.",
         move="The solution is where the lines cross. Read its x and y, then check it in both equations.",
         width="full"),
    dict(key="2", title="Choose the Solution",
         look="A system, its graph, and four points.",
         move="Find where the lines cross. The order matters: (x, y). Check the point in both equations.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def through(px, py, b):
    """The standard form of the line through (px, py) and (0, b), reduced, x first and positive."""
    A, B, C = b - py, px, px * b
    g = math.gcd(math.gcd(A, B), C)
    A, B, C = A // g, B // g, C // g
    if A < 0 or A == 0 and B < 0:
        A, B, C = -A, -B, -C
    return standard(A, B, C)

def slope_form(m, b):
    return f"y = {gen.written((m, 'x'), (b, ''))}"

def draw_system(r, tpl):
    px, py = signed(r, 1, 7), r.randint(-7, 7)
    if tpl == 0:
        b1, b2 = r.sample([b for b in range(-7, 8) if b and b != py], 2)
        m1, m2 = F(py - b1, px), F(py - b2, px)
        need(abs(m1) <= 4 and abs(m2) <= 4 and abs(m1 - m2) >= F(1, 2))    # readable: not steep, clearly apart
        return f"{through(px, py, b1)} ; {through(px, py, b2)}", (px, py)
    slopes = [m for m in range(-4, 5) if m and abs(py - m * px) <= 7]
    need(len(slopes) >= 2)
    m1, m2 = r.sample(slopes, 2)
    return f"{slope_form(m1, py - m1 * px)} ; {slope_form(m2, py - m2 * px)}", (px, py)

def point(x, y):
    return f"$({x}, {y})$"

def draw(entry, r, tpl):
    prompt, (px, py) = draw_system(r, tpl)
    need(solve(prompt) == (px, py))
    if entry == "1":
        return dict(prompt=prompt, answer=answer_of(prompt))
    swap = (py, px) if px != py else (-px, py)
    off = px - 1 if abs(px) > 3 else px + 1
    off_swap = (py, off) if off != py else (-off, py)
    choices, answer = gen.lettered(r, point(px, py), [point(*swap), point(off, py), point(*off_swap)])
    return dict(prompt=prompt, choices=choices, answer=answer)

def at(c):
    x, y = c.strip("$()").split(",")
    return f"x = {x.strip()}, y = {y.strip()}"

def check(p):
    try:
        if p["type"] == "1":
            return "checked" if solves(p["prompt"], p["answer"]) else "failed"
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if solves(p["prompt"], at(c))]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 2)

def graph(p, key=False):
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    for q, color in zip(equations(p["prompt"]), COLORS):
        a, b, c = coefficients(q)
        if b == 0:
            g.vertical(float(c / a), color=color)
        else:
            g.line(float(-a / b), float(c / b), color=color)
    if key:
        x, y = solve(p["prompt"])
        g.point(float(x), float(y), color="red")
    return g.typst()

def side(p):
    if p["type"] == "1":
        return f"{system_typst(p['prompt'])} #v(1.2em) $x =$ #v(1.2em) $y =$"
    return f"{system_typst(p['prompt'])} #v(0.6em) {gen.choices_typst(p['choices'])}"

def typst(p, gap="0.3em", key=False):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{side(p)}], [{graph(p, key)}])"

def key_typst(p, gap="0.3em"):
    """The key's prompt: the solution marked on the graph."""
    return typst(p, gap, key=True)

def answer_typst(p):
    return f"${p['answer']}$" if p["type"] == "1" else gen.choice_answer_typst(p)

def text(p):
    return system_text(p) + ("" if p["type"] == "1" else "   " + gen.choices_text([c.strip("$") for c in p["choices"]]))

def answer_text(p):
    return p["answer"] if p["type"] == "1" else gen.choice_answer_typst(p).replace("$", "")

def height(p):
    return 2.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new system; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "2":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
