"""Khan Algebra 2, Lesson 3-8: Polynomial identities, from the old app's
Alg2_03_08 (twenty of Khan's, without answers).

Type 1: which of two equations are true identities? Only A, Only B, Both,
Neither (Khan's order), spread evenly over a sheet. Each equation is one
of Khan's shapes with new numbers: n(n + 1)(n + 2) = n^3 + 3 n^2 + 2 n,
(a + 3)^2 - 9 = a^2 + 6 a, (9 k - 8)(9 k + 8) = 81 k^2 - 64,
m^3 - 1 = (m - 1)(m^2 + m + 1), (x - 2 y)^2 = x^2 - 4 x y + 4 y^2, ...; a
false one carries a usual slip (a term dropped, a sign flipped, a number
off).
Type 2: a student checks an identity step by step (Khan's Chun, Mabel,
Alaina). Is the student correct? If not, in which step was the mistake?
At most one step is wrong, with the slip Khan's students make (the number
multiplied into both factors, x^2 + c^2 for (x + c)^2, the minus not
distributed, a sign); the steps after it are right, from the wrong line.
Names only, no pronouns.

A problem: dict(type, ..., choices, answer, source).
    Type 1  equations ["v (v + 1) (v + 2) = v^3 + 3 v^2 + 2 v", ...]  answer "A"
    Type 2  name "Chun", steps ["3 (2 x - 1)^2 + 27", "3 (2 x - 1)(2 x - 1) + 27", ...]
            choices ["Chun is correct.", "Chun is incorrect. Chun made a mistake in step 2.", ...]
check(): Type 1 expands both sides of each equation; Type 2 compares each
step with the one before: the first that differs is the mistake.
"""
import math, re
import sympy as sp
from ... import gen
from ...gen import need, signed, written
from ...check import to_sympy
from ...typmath import tx, text as plain
from . import courses

NAME = FAMILY = "ka2_03_08"
FIXED = False
TITLE = "Lesson 3-8: Polynomial identities"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(3)
WHICH = ["Only A", "Only B", "Both A and B", "Neither A nor B"]

TYPES = [
    dict(key="1", title="Which Are Identities?",
         look="Two equations, A and B.",
         move="An identity is true for every value. Multiply out both sides of each: the same polynomial means "
              "an identity.", width="full"),
    dict(key="2", title="Find the Mistake",
         look="A student's steps toward showing an equation is an identity.",
         move="Check each step against the one before it. The first step that isn't equal to the line above "
              "is the mistake; if every step is right, the student is correct.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p.get("equations") or p.get("steps")), p["answer"])

# ------------------------------------------------------------------
# Type 1: an equation's sides, the structured one and the multiplied-out one
# ------------------------------------------------------------------
def b(c, v, h):
    """(c v + h) as written."""
    return f"({written((c, v), (h, ''))})"

def shapes(r):
    v, w = r.sample("abkmnxy", 2)
    a, h = r.randint(1, 5), signed(r, 1, 9)
    p, q = r.randint(2, 9), r.randint(1, 9)
    need(math.gcd(p, q) == 1 and h != -a)
    return r.choice([
        (f"{v} {b(1, v, a)} {b(1, v, a + r.randint(1, 3))}", None),             # n (n + 1)(n + 2)
        (f"{b(1, v, h)}^2 - {h * h}", None),                                     # (a + 3)^2 - 9
        (f"{b(p, v, -q)}^2 + {q * q}", None),                                    # (5 b - 2)^2 + 4
        (f"{b(p, v, -q)} {b(p, v, q)}", None),                                   # (9 k - 8)(9 k + 8)
        (f"({p} {v}^2 + {q} {w}^2) ({p} {v}^2 - {q} {w}^2)", None),              # (2 x^2 + y^2)(2 x^2 - y^2)
        (f"{b(1, v, h)} {b(1, v, -a)} {'+' if h > 0 else '-'} {abs(h * a)}", None),   # (y + 6)(y - 7) + 42
        (f"({written((1, v), (-q, w))})^2", None),                                            # (x - 2 y)^2
        (f"{b(1, v, a)}^2 - {v}^2", None),                                       # (m + 1)^2 - m^2
        (f"{v}^3 - {a ** 3}", f"{b(1, v, -a)} ({written((1, f'{v}^2'), (a, v), (a * a, ''))})"),   # m^3 - 1
    ])

def slip(r, e):
    """e with one usual slip: a term dropped, its sign flipped, or its number off."""
    terms = list(sp.Add.make_args(sp.expand(e)))
    i = r.randrange(len(terms))
    kind = r.choice(("drop", "sign", "number"))
    if kind == "drop" and len(terms) > 1:
        terms.pop(i)
    elif kind == "sign":
        terms[i] = -terms[i]
    else:
        c, rest = terms[i].as_coeff_Mul()
        terms[i] = (c + r.choice((-1, 1)) * r.randint(1, 3)) * rest
    out = sp.Add(*terms)
    need(sp.expand(out - e) != 0)
    return out

def factored_slip(r, text):
    """(m - 1)(m^2 + m + 1) with a slip in the second factor: (m - 1)(m^2 + 1), (m - 1)(m^2 - m + 1)."""
    first, second = re.fullmatch(r"(\(.*?\)) \((.*)\)", text).groups()
    return f"{first} ({tx(slip(r, to_sympy(second)))})"

def equation(r, true):
    lhs, factored = shapes(r)
    e = to_sympy(lhs)
    if factored:                                                 # m^3 - 1 = (m - 1)(m^2 + m + 1)
        rhs = factored if true else factored_slip(r, factored)
    else:
        rhs = tx(sp.expand(e) if true else slip(r, e))
    return f"{lhs} = {rhs}" if r.random() < 0.6 else f"{rhs} = {lhs}"

def identity(eq):
    l, rhs = eq.split("=")
    return sp.expand(to_sympy(l) - to_sympy(rhs)) == 0

# ------------------------------------------------------------------
# Type 2: a student's steps, each a function of the numbers so far; one
# step may carry a slip, and the steps after it follow from it
# ------------------------------------------------------------------
def x_poly(*cs):
    """written(c_n x^n, ..., c_0) from the coefficients, highest first."""
    n = len(cs) - 1
    return written(*[(c, "" if n - i == 0 else "x" if n - i == 1 else f"x^{n - i}") for i, c in enumerate(cs)])

def chun(r, wrong):
    """c (p x + q)^2 + d."""
    c, p, q, d = r.randint(2, 5), r.randint(1, 4), signed(r, 1, 6), r.randint(1, 30)
    steps = [f"{c} ({x_poly(p, q)})^2 + {d}", f"{c} ({x_poly(p, q)}) ({x_poly(p, q)}) + {d}"]
    f1, f2 = (c * p, c * q), (p, q)
    if wrong == 2:
        f2 = f1                                                  # the c into both factors
    steps.append(f"({x_poly(*f1)}) ({x_poly(*f2)}) + {d}")
    cross = [f1[0] * f2[1], f1[1] * f2[0]]
    if wrong == 3:
        cross[1] = -cross[1]
    steps.append(written((f1[0] * f2[0], "x^2"), (cross[0], "x"), (cross[1], "x"), (f1[1] * f2[1], ""), (d, "")))
    k = f1[1] * f2[1] + (-d if wrong == 4 else d)
    steps.append(x_poly(f1[0] * f2[0], cross[0] + cross[1], k))
    return steps

def mabel(r, wrong):
    """(a x + b)(x + c)^2."""
    a, bb, c = r.randint(2, 5), signed(r, 1, 5), signed(r, 1, 4)
    steps = [f"({x_poly(a, bb)}) ({x_poly(1, c)})^2", f"({x_poly(a, bb)}) ({x_poly(1, c)}) ({x_poly(1, c)})"]
    quad = (1, 0, c * c) if wrong == 2 else (1, 2 * c, c * c)              # x^2 + c^2 for (x + c)^2
    if wrong == 2:
        steps.append(f"({x_poly(a, bb)}) ({x_poly(*quad)})")
    else:
        steps.append(f"({x_poly(a, bb)}) ({written((1, 'x^2'), (c, 'x'), (c, 'x'), (c * c, ''))})")
    steps.append(f"({x_poly(a, bb)}) ({x_poly(*quad)})")
    prods = [a * quad[0], a * quad[1], a * quad[2], bb * quad[0], bb * quad[1], bb * quad[2]]
    if wrong == 4:
        prods[5] = -prods[5]
    steps.append(written((prods[0], "x^3"), (prods[1], "x^2"), (prods[2], "x"), (prods[3], "x^2"), (prods[4], "x"),
                         (prods[5], "")))
    steps.append(x_poly(prods[0], prods[1] + prods[3], prods[2] + prods[4], prods[5]))
    if wrong == 2:                                               # the slip and its line are the same step
        steps.pop(3)
    return steps

def alaina(r, wrong):
    """(p x + q)^2 - (s x + t)^2."""
    p, q, s, t = r.randint(2, 5), signed(r, 1, 5), r.randint(1, 4), signed(r, 1, 5)
    need(p != s)
    steps = [f"({x_poly(p, q)})^2 - ({x_poly(s, t)})^2", f"({x_poly(p, q)}) ({x_poly(p, q)}) - ({x_poly(s, t)}) ({x_poly(s, t)})"]
    back = [-s * s, -2 * s * t, -t * t]
    if wrong == 2:
        back = [-s * s, 2 * s * t, t * t]                        # the minus on the first term only
    steps.append(written((p * p, "x^2"), (2 * p * q, "x"), (q * q, ""), (back[0], "x^2"), (back[1], "x"), (back[2], "")))
    k = q * q + back[2]
    if wrong == 3:
        k = q * q - back[2]
    steps.append(x_poly(p * p + back[0], 2 * p * q + back[1], k))
    return steps

STUDENTS = {"chun": (chun, (2, 3, 4)), "mabel": (mabel, (2, 4)), "alaina": (alaina, (2, 3))}

def mistake(steps):
    """The first step not equal to the line before it, or None."""
    for k in range(1, len(steps)):
        if sp.expand(to_sympy(steps[k]) - to_sympy(steps[k - 1])) != 0:
            return k
    return None

def step_choices(name, n, wrong, r):
    """Khan's four: correct, and a mistake in three of the steps (the wrong one among them)."""
    pool = [k for k in range(1, n + 1) if k != wrong]
    ks = sorted(([wrong] if wrong else []) + r.sample(pool, 3 - bool(wrong)))
    return [f"{name} is correct."] + [f"{name} is incorrect. {name} made a mistake in step {k}." for k in ks]

def draw(entry, r, tpl, want=None):
    if entry == "1":
        outcome = want or r.choice("ABCD")
        trues = {"A": (True, False), "B": (False, True), "C": (True, True), "D": (False, False)}[outcome]
        eqs = [equation(r, t) for t in trues]
        need(eqs[0].split("=")[0] != eqs[1].split("=")[0])
        choices, answer = gen.in_order(WHICH, WHICH["ABCD".index(outcome)])
        return dict(equations=eqs, choices=choices, answer=answer)
    student = r.choice(list(STUDENTS))
    make, slips = STUDENTS[student]
    wrong = None if r.random() < 0.3 else r.choice(slips)
    steps = make(r, wrong)
    need(mistake(steps) == wrong and len(steps) >= 3)
    name = r.choice(gen.NAMES)
    choices = step_choices(name, len(steps) - 1, wrong, r)
    right = choices[0] if wrong is None else f"{name} is incorrect. {name} made a mistake in step {wrong}."
    return dict(student=student, name=name, steps=steps, choices=choices, answer=gen.ABC[choices.index(right)])

STEP = re.compile(r"step (\d+)\.$")

def check(p):
    try:
        if p["type"] == "1":
            trues = tuple(identity(eq) for eq in p["equations"])
            outcome = {(True, False): "A", (False, True): "B", (True, True): "C", (False, False): "D"}[trues]
            return "checked" if p["answer"] == outcome else "failed"
        k = mistake(p["steps"])
        said = gen.chosen(p)
        m = STEP.search(said[0]) if len(said) == 1 else None
        ok = len(said) == 1 and (int(m.group(1)) == k if m else k is None and said[0].endswith("correct."))
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("ABCD", lambda k: k[3] if k[0] == NAME and k[1] == "1" else None))

def typst(p, gap="0.3em"):
    if p["type"] == "1":
        eqs = " \\\n    ".join(f"{x}. ${eq}$" for x, eq in zip("AB", p["equations"]))
        return f"Which of the equations are true identities? \\\n    {eqs} \\\n    {gen.choices_typst(p['choices'], 'linear')}"
    s, name = p["steps"], p["name"]
    rows = f"[], [$ {s[0]} $], " + ", ".join(f"[Step {k}:], [$= {t}$]" for k, t in enumerate(s[1:], 1))
    return (f"{name} was asked whether the equation ${s[0]} = {s[-1]}$ is an identity. {name}'s steps: \\\n    "
            f"#pad(left: 1em, grid(columns: 2, column-gutter: 0.8em, row-gutter: 0.6em, {rows})) \\\n    "
            f"So {name} stated that the equation is a true identity. Is {name} correct? If not, in which step "
            f"was the mistake? \\\n    {gen.choices_typst(p['choices'])}")

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    if p["type"] == "1":
        return "   ".join(f"{x}. {plain(eq)}" for x, eq in zip("AB", p["equations"]))
    return f"{p['name']}: " + "  =  ".join(plain(t) for t in p["steps"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.3 if p["type"] == "1" else 1.2 + 0.32 * len(p["steps"])

def edit_text(p):
    return "; ".join(p.get("equations") or p["steps"])

def from_edit(t, old):
    raise ValueError("reroll for a new problem; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
