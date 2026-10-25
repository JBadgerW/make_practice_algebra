"""Khan Algebra 1, Lesson 6-1: Solutions of systems of equations, from the
old app's Alg1_06_01 (twenty-two generated slots, four templates).

Is (x, y) a solution to both equations? Half the time it is; otherwise one
equation's constant is off by 1 to 5, so the point fits one equation and
not the other, as the old templates did. x and y are -12 to 12,
coefficients -6 to 6, not 0; equations in standard form or solved for y.

A problem: dict(type, prompt, point, choices, answer, source).
    prompt  "3 x - 2 y = 13 ; 2 y = -4 x + 6"     point  "(3, -2)"
    choices ["Yes", "No"]                         answer "A"
check() substitutes the point into both equations.
"""
from ... import gen
from ...gen import need, signed, written
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard, coefficients, equations

NAME = FAMILY = "ka1_06_01"
FIXED = False
TITLE = "Lesson 6-1: Solutions of systems of equations"
INSTRUCTIONS = ""                       # each problem asks its own question
COURSES = courses(6)
CHOICES = ["Yes", "No"]

TYPES = [
    dict(key="1", title="Check a Point",
         look="A system and a point (x, y).",
         move="Put x and y into each equation. The point is a solution only if both equations come out true."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["point"])

def solved(a, b, c):
    """b y = -a x + c: the equation a x + b y = c with the x term moved over."""
    return f"{written((b, 'y'))} = {written((-a, 'x'), (c, ''))}"

def draw(entry, r, tpl):
    x, y = r.randint(-12, 12), r.randint(-12, 12)
    off = [0, 0]
    if r.random() < 0.5:
        off[r.randrange(2)] = signed(r, 1, 5)        # the point misses one equation
    eqs = []
    for k in range(2):
        a, b = signed(r, 1, 6), signed(r, 1, 6)
        form = standard if r.random() < 0.6 else solved
        eqs.append(form(a, b, a * x + b * y + off[k]))
    choices, answer = gen.in_order(CHOICES, "Yes" if off == [0, 0] else "No")
    return dict(prompt=" ; ".join(eqs), point=f"({x}, {y})", choices=choices, answer=answer)

def fits(p):
    x, y = (int(t) for t in p["point"].strip("()").split(","))
    return all(a * x + b * y == c for a, b, c in (coefficients(q) for q in equations(p["prompt"])))

def check(p):
    try:
        return "checked" if gen.chosen(p) == ["Yes" if fits(p) else "No"] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return (f"{twovar.system_typst(p['prompt'])} \\\n    Is ${p['point']}$ a solution to both equations? "
            f"#h(1em) {gen.choices_typst(p['choices'], 'linear')}")

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return twovar.text(p) + f"   {plain(p['point'])}?"

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 0.9

def edit_text(p):
    return f"{p['prompt']} ; {p['point']}"

def from_edit(t, old):
    *eqs, point = [s.strip() for s in t.replace("−", "-").split(";")]
    new = dict(old, prompt=" ; ".join(eqs), point=point, source="edited")
    try:
        new["answer"] = gen.in_order(CHOICES, "Yes" if fits(new) else "No")[1]
    except Exception:
        raise ValueError("write the two equations and the point: 3 x - 2 y = 13 ; y = -2 x + 4 ; (3, -2)") from None
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
