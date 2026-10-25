"""Khan Algebra 1, Lesson 6-7: Elimination strategies, from the old app's
Alg1_06_07 (twelve generated slots, twelve templates).

Which of these strategies would eliminate a variable? A strategy multiplies
the top equation by s and the bottom by t, then adds them or subtracts one
from the other: "Add the equations", "Multiply the top equation by -3, then
add the equations", "Multiply the top equation by 4, multiply the bottom
equation by -5, then add the equations". The wrong choices are the same
strategies with a sign wrong. In the old templates a "wrong" choice could
also eliminate a variable (no. 4 when d = -a, no. 8 when q = -p, no. 12 when
e = b d), so the key was wrong; here every choice is tried, and the right
ones are exactly those that eliminate. Choose all that apply.

A problem: dict(type, prompt, strategies, choices, answer, source).
    prompt      "2 x + 3 y = 7 ; 4 x - 5 y = 3"
    strategies  [["-2", "1", "add"], ...]  (top multiplier, bottom multiplier,
                "add", "sub" (top - bottom), or "rsub" (bottom - top))
    choices     the strategies in words
    answer      "A, C"
check() applies every strategy to the equations and sees which leave no x
or no y.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need, signed, signed_except
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard, coefficients, equations

NAME = FAMILY = "ka1_06_07"
FIXED = False
TITLE = "Lesson 6-7: Elimination strategies"
INSTRUCTIONS = "Which of these strategies would eliminate a variable? Choose all that apply."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Which Strategies Work?",
         look="A system, and strategies that multiply the equations and add or subtract them.",
         move="For each strategy, work out just the x terms and just the y terms. It works if either comes to 0.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], tuple(p["choices"]))

# ------------------------------------------------------------------
# Strategies: (s, t, op)
# ------------------------------------------------------------------
def eliminates(prompt, s, t, op):
    (a, b, _), (d, e, _) = (coefficients(q) for q in equations(prompt))
    s, t = F(s), F(t)
    sign = {"add": (1, 1), "sub": (1, -1), "rsub": (-1, 1)}[op]
    x = sign[0] * s * a + sign[1] * t * d
    y = sign[0] * s * b + sign[1] * t * e
    return x == 0 or y == 0

def num(q):
    q = F(q)
    return f"${q.numerator}/{q.denominator}$" if q.denominator != 1 else f"${q.numerator}$"

def words(s, t, op):
    """The strategy as Khan words it."""
    s, t = F(s), F(t)
    last = {"add": "add the equations", "sub": "subtract the bottom equation from the top equation",
            "rsub": "subtract the top equation from the bottom equation"}[op]
    steps = []
    if s != 1:
        steps.append(f"multiply the top equation by {num(s)}")
    if t != 1:
        steps.append(f"multiply the bottom equation by {num(t)}")
    text = ", ".join(steps + [("then " if steps else "") + last]) + "."
    return text[0].upper() + text[1:]

def candidates(a, b, d, e):
    """Strategies for the system a x + b y = c, d x + e y = f, and their wrong-sign twins."""
    out = [(1, 1, "add"), (1, 1, "sub"), (1, 1, "rsub")]
    for p, q in ((a, d), (b, e)):                  # the x coefficients, then the y coefficients
        if q % p == 0 and abs(q // p) > 1:          # top times k matches the bottom
            k = q // p
            out += [(-k, 1, "add"), (k, 1, "sub"), (k, 1, "add"), (-k, 1, "sub")]
        if p % q == 0 and abs(p // q) > 1:          # bottom times k matches the top
            k = p // q
            out += [(1, -k, "add"), (1, k, "sub"), (1, k, "add"), (1, -k, "sub")]
        if abs(q) > 1 and F(p, q).denominator != 1:  # bottom times a fraction
            out += [(1, -F(p, q), "add"), (1, F(p, q), "add")]
        out += [(q, -p, "add"), (q, p, "sub"), (-q, p, "add"), (q, p, "add")]
    return out

def system(r, kind):
    x, y = r.randint(-9, 9), r.randint(-9, 9)
    a, b = signed(r, 2, 10), signed(r, 2, 10)
    if kind == "same":                             # a letter's coefficients equal or opposite
        d, e = (r.choice((a, -a)), signed_except(r, 2, 10, b, -b)) if r.random() < 0.5 else \
            (signed_except(r, 2, 10, a, -a), r.choice((b, -b)))
    elif kind == "multiple":                       # one is a multiple of the other
        k = signed_except(r, 2, 4, 1, -1)
        d, e = (k * a, signed_except(r, 2, 10, b, -b)) if r.random() < 0.5 else (signed_except(r, 2, 10, a, -a), k * b)
        if r.random() < 0.5:
            a, b, d, e = d, e, a, b
    else:                                          # neither: multiply both
        d, e = signed_except(r, 2, 10, a, -a), signed_except(r, 2, 10, b, -b)
    need(a * e != b * d)
    return standard(a, b, a * x + b * y) + " ; " + standard(d, e, d * x + e * y), (a, b, d, e)

TEMPLATES = {"1": [lambda r, k=k: system(r, k) for k in ("same", "multiple", "both")]}

def draw(entry, r, tpl):
    prompt, (a, b, d, e) = TEMPLATES[entry][tpl](r)
    pool = list(dict.fromkeys(candidates(a, b, d, e)))
    right = [c for c in pool if eliminates(prompt, *c)]
    wrong = [c for c in pool if not eliminates(prompt, *c)]
    r.shuffle(right), r.shuffle(wrong)
    n = r.choice([k for k in (1, 2, 3) if k <= len(right) and 3 - k <= len(wrong)] or [0])
    need(n)
    picked = right[:n] + wrong[:3 - n]
    r.shuffle(picked)
    strategies = [[str(F(s)), str(F(t)), op] for s, t, op in picked]
    return dict(prompt=prompt, strategies=strategies, choices=[words(*s) for s in strategies],
                answer=", ".join(gen.ABC[i] for i, s in enumerate(strategies) if eliminates(prompt, *s)))

def check(p):
    try:
        right = [gen.ABC[i] for i, s in enumerate(p["strategies"]) if eliminates(p["prompt"], *s)]
        return "checked" if right and right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    return f"{twovar.system_typst(p['prompt'])} \\\n    {gen.choices_typst(p['choices'])}"

def answer_typst(p):
    return p["answer"]

def text(p):
    return twovar.text(p) + "      " + gen.choices_text(p["choices"], lambda c: c.replace("$", ""))

def answer_text(p):
    return p["answer"]

def height(p):
    return 1.3

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        answer = ", ".join(gen.ABC[i] for i, s in enumerate(old["strategies"]) if eliminates(t, *s))
    except Exception:
        raise ValueError("write the two equations, separated by ;  2 x + 3 y = 7 ; 4 x - 5 y = 3") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
