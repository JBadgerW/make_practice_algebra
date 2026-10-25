"""Khan Algebra 1, Lesson 6-12: Number of solutions to a system of equations
algebraically, from the old app's Alg1_06_12 (eighteen generated slots,
seven templates).

How many solutions does the system have? Both equations in slope-intercept
form (Type 1), or one of them a multiple of that form, k y = k m x + k b
(Type 2). Each problem is equally likely to have exactly one solution, none,
or infinitely many; the types follow the form, not the answer. Slopes and
intercepts -12 to 12, not 0.

A problem: dict(type, prompt, choices, answer, source); prompt "eq1 ; eq2".
    choices ["Exactly one solution", "No solutions", "Infinitely many solutions"]
check() solves the system exactly.
"""
from ... import gen
from ...gen import need, signed, signed_except, written
from ...typmath import text as plain
from . import courses, twovar

NAME = FAMILY = "ka1_06_12"
FIXED = False
TITLE = "Lesson 6-12: Number of solutions to a system of equations algebraically"
INSTRUCTIONS = "How many solutions does each system have?"
COURSES = courses(6)
CHOICES = ["Exactly one solution", "No solutions", "Infinitely many solutions"]
COUNT = {"one": CHOICES[0], "none": CHOICES[1], "many": CHOICES[2]}

TYPES = [
    dict(key="1", title="Slope-Intercept Form",
         look="Both equations are y = m x + b.",
         move="Different slopes: one solution. The same slope: no solution if the intercepts differ, "
              "infinitely many if they match."),
    dict(key="2", title="A Multiple of an Equation",
         look="One equation is like 3 y = 6 x + 9: a multiple of y = m x + b.",
         move="Divide that equation by its number to get y = m x + b. Then compare slopes and intercepts."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def line(m, b, k=1, intercept_first=False):
    """k y = k m x + k b (k = 1: y = m x + b), or with the intercept first."""
    terms = [(k * b, ""), (k * m, "x")] if intercept_first else [(k * m, "x"), (k * b, "")]
    return f"{written((k, 'y'))} = {written(*terms)}"

def draw(entry, r, tpl):
    outcome = r.choice(("one", "none", "many"))
    m1, b1 = signed(r, 1, 12), signed(r, 1, 12)
    m2 = m1 if outcome != "one" else signed_except(r, 1, 12, m1)
    b2 = b1 if outcome == "many" else signed_except(r, 1, 12, b1) if outcome == "none" else signed(r, 1, 12)
    k = signed_except(r, 2, 5, 1) if entry == "2" else 1
    first = r.random() < 0.3
    second = not first if outcome == "many" and k == 1 else r.random() < 0.3    # never the same equation twice
    eqs = [line(m1, b1, intercept_first=first), line(m2, b2, k, second)]
    r.shuffle(eqs)
    prompt = " ; ".join(eqs)
    choices, answer = gen.in_order(CHOICES, COUNT[outcome if outcome != "one" else "one"])
    return dict(prompt=prompt, choices=choices, answer=answer)

def count(prompt):
    s = twovar.solve(prompt)
    return "one" if isinstance(s, tuple) else s

def check(p):
    try:
        return "checked" if gen.chosen(p) == [COUNT[count(p["prompt"])]] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return f"{twovar.system_typst(p['prompt'])} \\\n    {gen.choices_typst(p['choices'])}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return twovar.text(p) + "      " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.2

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        answer = gen.in_order(CHOICES, COUNT[count(t)])[1]
    except Exception:
        raise ValueError("write two equations separated by ;  y = 2 x + 3 ; 2 y = 4 x - 1") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
