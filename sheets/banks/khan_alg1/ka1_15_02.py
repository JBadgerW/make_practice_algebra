"""Khan Algebra 1, Lesson 15-2: Rational vs. irrational expressions, from the
old app's Alg1_15_02 (twenty-six of Khan's, without answers).

Is it rational, irrational, or can it be either? Type 1: particular
numbers (sqrt(23) + sqrt(77), sqrt(12) · sqrt(3), 3/14 · 7/71,
sqrt(40)/sqrt(5), 36/25 · sqrt(11), sqrt(8) + (-sqrt(8))). Type 2: letters
that stand for rational or irrational numbers ("Let a be a non-zero
rational number and b be an irrational number. Is a/b rational or
irrational?"), with Khan's cases, and two irrationals, which can be either.

A problem: dict(type, prompt, choices, answer, source); Type 2 adds
given ({letter: "rational" | "nonzero" | "irrational"}) and expr.
    Type 1  prompt "sqrt(12) dot sqrt(3)", answer "A"
    Type 2  given {"a": "nonzero", "b": "irrational"}, expr "a/b", answer "B"
check(): Type 1 computes the number exactly; Type 2 tries the expression
on sample values of each letter (rational: 0, 1, -3, 2/7; irrational:
sqrt(2), -sqrt(2), 1 - sqrt(2), 1/sqrt(2), pi) and finds whether the results
are always rational, never, or sometimes.
"""
import itertools
import sympy as sp
from ... import gen
from ...gen import need, signed
from ...check import to_sympy
from ...typst import esc
from ...typmath import display, dfrac, text as plain
from . import courses
from .rationality import rational

NAME = FAMILY = "ka1_15_02"
FIXED = False
TITLE = "Lesson 15-2: Rational vs. irrational expressions"
INSTRUCTIONS = "Is each one rational or irrational?"
COURSES = courses(15)
EITHER = "It can be either rational or irrational"
CHOICES = ["Rational", "Irrational", EITHER]

TYPES = [
    dict(key="1", title="Numbers",
         look="Sums, products, and quotients of particular numbers: fractions and square roots.",
         move="Simplify first: sqrt(12) · sqrt(3) = sqrt(36) = 6. Rational if it's a fraction of integers in the end."),
    dict(key="2", title="Rational and Irrational Letters",
         look="Letters that stand for rational or irrational numbers.",
         move="Rational with rational stays rational. Rational (not zero) with irrational, by +, -, ·, or ÷, is "
              "irrational. Two irrationals can give either: sqrt(2) · sqrt(2) = 2.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

NONSQUARE = [n for n in range(2, 100) if int(n ** 0.5) ** 2 != n]

# ------------------------------------------------------------------
# Type 1: particular numbers
# ------------------------------------------------------------------
def t1_root_sum(r):                           # sqrt(23) + sqrt(77)
    a, b = r.sample(NONSQUARE, 2)
    return f"sqrt({a}) + sqrt({b})"

def t1_root_product(r):                       # sqrt(12) dot sqrt(3), sqrt(2) dot sqrt(3)
    m = r.choice((2, 3, 5, 6, 7))
    k = r.choice((r.randint(2, 6) ** 2, r.choice(NONSQUARE)))
    return f"sqrt({k * m}) dot sqrt({m})"

def t1_root_quotient(r):                      # sqrt(40)/sqrt(5), sqrt(20)/sqrt(5)
    m = r.choice((2, 3, 5, 6, 7))
    k = r.choice((r.randint(2, 6) ** 2, r.choice(NONSQUARE)))
    return f"(sqrt({k * m}))/(sqrt({m}))"

def t1_fractions(r):                          # 3/14 dot 7/71, -59/3 + 4/63
    b, c, d = r.randint(2, 20), r.randint(1, 20), r.randint(2, 80)
    return f"{signed(r, 1, 60)}/{b} {r.choice(('dot', '+', '-'))} {c}/{d}"

def t1_fraction_root(r):                      # 36/25 dot sqrt(11)
    a, b = r.randint(2, 9) ** 2, r.randint(2, 9) ** 2
    return f"{a}/{b} dot sqrt({r.choice(NONSQUARE + [r.randint(2, 9) ** 2])})"

def t1_opposites(r):                          # sqrt(8) + (-sqrt(8))
    n = r.choice(NONSQUARE)
    return f"sqrt({n}) + (-sqrt({n}))"

def t1_root_plus(r):                          # sqrt(12) + 4
    return f"sqrt({r.choice(NONSQUARE)}) + {r.randint(1, 20)}"

# ------------------------------------------------------------------
# Type 2: letters
# ------------------------------------------------------------------
WORDS = {"rational": "a rational number", "nonzero": "a non-zero rational number", "irrational": "an irrational number"}
PLURAL = {"rational": "rational numbers", "nonzero": "non-zero rational numbers", "irrational": "irrational numbers"}

def statement(given):
    """"Let a be a non-zero rational number and b be an irrational number." (or both alike)"""
    items = list(given.items())
    if len(items) == 2 and items[0][1] == items[1][1]:
        return f"Let ${items[0][0]}$ and ${items[1][0]}$ be {PLURAL[items[0][1]]}."
    return "Let " + " and ".join(f"${x}$ be {WORDS[k]}" for x, k in items) + "."

CASES = [  # (given, expressions)
    ({"a": "rational", "b": "rational"}, ["a dot b", "a + b", "a - b"]),
    ({"a": "rational", "b": "nonzero"}, ["a/b"]),
    ({"a": "rational", "b": "irrational"}, ["a + b", "a - b", "b - a", "a dot b"]),
    ({"a": "nonzero", "b": "irrational"}, ["a dot b", "a/b", "b/a"]),
    ({"a": "irrational"}, ["a dot {k}", "{k} + a", "-{k} + a", "1/a", "{k}/a"]),
    ({"a": "nonzero"}, ["a dot sqrt({n})", "(sqrt({n}))/a", "-sqrt({n}) + a", "1/a"]),
    ({"a": "irrational", "b": "irrational"}, ["a + b", "a dot b"]),
]

RATIONAL = [sp.Integer(0), sp.Integer(1), sp.Integer(-3), sp.Rational(2, 7)]
IRRATIONAL = [sp.sqrt(2), -sp.sqrt(2), 1 - sp.sqrt(2), 1 / sp.sqrt(2), sp.pi]

def kind(given, expr):
    """Rational, Irrational, or EITHER: the expression tried at every sample value."""
    pools = [[v for v in (IRRATIONAL if k == "irrational" else RATIONAL) if not (k == "nonzero" and v == 0)]
             for k in given.values()]
    syms = [sp.Symbol(x) for x in given]
    e = to_sympy(expr.replace("dot", "*"))
    seen = set()
    for vals in itertools.product(*pools):
        try:
            v = sp.nsimplify(sp.simplify(e.subs(dict(zip(syms, vals)))))
        except ZeroDivisionError:
            continue
        if v.has(sp.zoo, sp.nan):
            continue
        seen.add(bool(v.is_Rational))
    return "Rational" if seen == {True} else "Irrational" if seen == {False} else EITHER

def t2(r):
    given, exprs = r.choice(CASES)
    expr = r.choice(exprs).format(k=r.randint(2, 30), n=r.choice(NONSQUARE))
    return given, expr

TEMPLATES = {"1": [t1_root_sum, t1_root_product, t1_root_quotient, t1_fractions, t1_fraction_root,
                   t1_opposites, t1_root_plus],
             "2": [t2]}

def draw(entry, r, tpl):
    if entry == "1":
        prompt = TEMPLATES[entry][tpl](r)
        right = "Rational" if rational(prompt) else "Irrational"
        return dict(prompt=prompt, choices=CHOICES, answer=gen.in_order(CHOICES, right)[1])
    given, expr = t2(r)
    prompt = f"{statement(given)} Is ${expr}$ rational or irrational?"
    return dict(prompt=prompt, given=given, expr=expr, choices=CHOICES,
                answer=gen.in_order(CHOICES, kind(given, expr))[1])

def check(p):
    try:
        right = ("Rational" if rational(p["prompt"]) else "Irrational") if p["type"] == "1" else kind(p["given"], p["expr"])
        return "checked" if gen.chosen(p) == [right] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def question(p):
    if p["type"] == "1":
        return f"Is {display(dfrac(p['prompt']))} rational or irrational?"
    return p["prompt"].replace(f"${p['expr']}$", display(dfrac(p["expr"])))

def typst(p, gap="0.3em"):
    return f"{question(p)} \\\n    {gen.choices_typst(p['choices'])}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    words = p["prompt"].replace("$", "") if p["type"] == "2" else f"Is {plain(p['prompt'])} rational?"
    return plain(words.replace("dot", "·"))

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.0

def edit_text(p):
    return p["prompt"] if p["type"] == "1" else p["expr"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        if old["type"] == "1":
            new = dict(old, prompt=t, answer=gen.in_order(CHOICES, "Rational" if rational(t) else "Irrational")[1])
        else:
            new = dict(old, expr=t, prompt=f"{statement(old['given'])} Is ${t}$ rational or irrational?",
                       answer=gen.in_order(CHOICES, kind(old["given"], t))[1])
    except Exception:
        raise ValueError("write it in Typst math, like sqrt(12) dot sqrt(3), or a dot b") from None
    new["source"] = "edited"
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
