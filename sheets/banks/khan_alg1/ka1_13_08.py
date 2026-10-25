"""Khan Algebra 1, Lesson 13-8: GCF factoring introduction, from the old
app's Alg1_13_08 (twelve generated slots).

Type 1, Khan's area model: someone factoring 6 x^2 + 9 found the greatest
common factor of its terms, 3, and drew an area model; what is its width?
The old templates divided out only the common factor of the GCF and the
inner coefficients, so the inner ones could still share a factor
(3 for 6 x^2 + 12, whose GCF is 6), and the "GCF" could even become 1;
here the GCF is the greatest. Type 2: which expression is the result of
taking out the GCF? The wrong choices are Khan's: a common factor that
isn't the greatest (equal, but not finished), an x that isn't common, and
the factor left inside.

A problem: dict(type, prompt, ..., answer, source), Typst math.
    Type 1  prompt "6 x^2 + 9", gcf "3", name, answer "2 x^2 + 3"
    Type 2  prompt "12 x^2 + 8 x + 4", choices four, answer "C"
check(): Type 1, the GCF is the greatest common factor of the terms and the
width times it is the polynomial, in standard form; Type 2, exactly one
choice is equal with nothing common left inside, and it's the answer.
"""
import math
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, written
from ...check import to_sympy
from ...typst import esc
from ...typmath import display, dfrac, text as plain
from . import courses
from .figures import PREAMBLE, gcf_model

NAME = FAMILY = "ka1_13_08"
FIXED = False
TITLE = "Lesson 13-8: GCF factoring introduction"
INSTRUCTIONS = ""
COURSES = courses(13)

TYPES = [
    dict(key="1", title="The Width of an Area Model", instructions="Answer each question.",
         look="An area model with the greatest common factor on its side.",
         move="Divide each term (each box) by the common factor. The quotients, added, are the width.",
         width="full", space="0.75in"),
    dict(key="2", title="Factor Out the GCF", instructions="Which expression is the result of factoring out the greatest common factor?",
         look="A polynomial whose terms share a factor.",
         move="Find the greatest number (and the highest power of x) that divides every term. Write it in front, "
              "and each term divided by it inside the parentheses.", space="0.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def gcf(e):
    """The greatest common factor of a polynomial's terms: number and power of x, as sympy."""
    v = poly.letter(e)
    ts = sp.Add.make_args(sp.expand(e))
    k = math.gcd(*[int(abs(t.as_coeff_Mul()[0])) for t in ts])
    m = min(sp.degree(t, v) for t in ts)
    return k * v ** m

def inner(r, n):
    """n coefficients with no common factor, the first positive: the polynomial in parentheses."""
    cs = [r.randint(1, 12)] + [signed(r, 1, 12) for _ in range(n - 1)]
    need(math.gcd(*cs) == 1)
    return cs

def draw(entry, r, tpl):
    x = sp.Symbol("x")
    shape = r.choice(("two", "three", "x"))
    if shape == "two":                        # 6 x^2 + 9
        a, b = inner(r, 2)
        inside, k = a * x**2 + b, sp.Integer(r.randint(2, 6))
    elif shape == "three":                    # 6 x^2 + 3 x + 9
        a, b, c = inner(r, 3)
        inside, k = a * x**2 + b * x + c, sp.Integer(r.randint(2, 4))
    else:                                     # 6 x^2 + 9 x: the factor 3 x
        a, b = inner(r, 2)
        inside, k = a * x + b, r.randint(2, 6) * x
    e = sp.expand(k * inside)
    if entry == "1":
        return dict(prompt=poly.expanded(e), gcf=poly.expanded(k), name=r.choice(gen.NAMES),
                    answer=poly.expanded(inside))
    part = k / x if shape == "x" else r.choice([d for d in sp.divisors(k) if 1 < d < k] or [1])
    wrong = []
    if part != 1:
        wrong.append(f"{poly.expanded(part)} ({poly.expanded(sp.expand(e / part))})")         # not the greatest
    wrong.append(f"{poly.expanded(k * x)} ({poly.expanded(inside)})")                         # an x that isn't common
    wrong.append(f"{poly.expanded(k)} ({poly.expanded(sp.expand(inside * x))})")
    wrong.append(f"{poly.expanded(x)} ({poly.expanded(e)})" if shape != "x" else f"x ({poly.expanded(sp.expand(e))})")
    right = f"{poly.expanded(k)} ({poly.expanded(inside)})"
    wrong = [w for w in dict.fromkeys(wrong) if w != right]
    need(len(wrong) >= 3)
    r.shuffle(wrong)
    choices, letter = gen.lettered(r, right, wrong[:3])
    return dict(prompt=poly.expanded(e), choices=choices, answer=letter)

def gcf_out(text, prompt):
    """The text equals the prompt, with the greatest common factor in front: nothing common left inside."""
    if sp.expand(to_sympy(text) - to_sympy(prompt)) != 0:
        return False
    t = to_sympy(text, evaluate=False)                      # as written: 6 (7 x^2 - 2) isn't 42 x^2 - 12
    adds = [poly._evaluated(f) for f in sp.Mul.make_args(t) if isinstance(f, sp.Add)]
    return len(adds) == 1 and sp.simplify(gcf(adds[0])) == 1

def check(p):
    try:
        if p["type"] == "1":
            e, g = to_sympy(p["prompt"]), to_sympy(p["gcf"])
            ok = sp.simplify(g - gcf(e)) == 0 and poly.standard(p["answer"]) and \
                sp.expand(to_sympy(p["answer"]) * g - e) == 0
            return "checked" if ok else "failed"
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if gcf_out(c, p["prompt"])]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    if p["type"] == "1":
        terms = [poly.expanded(t) for t in sp.Add.make_args(to_sympy(p["prompt"]))]
        terms.sort(key=lambda t: -sp.degree(to_sympy(t), sp.Symbol("x")))
        n = esc(p["name"])
        return (f"{n} was trying to factor ${p['prompt']}$. {n} found that the greatest common factor of these "
                f"terms was ${p['gcf']}$ and made an area model: \\\n    {gcf_model(p['gcf'], terms)} \\\n    "
                f"What is the width of {n}'s area model?")
    return f"${p['prompt']}$ \\\n    {gen.choices_typst([f'${c}$' for c in p['choices']], 'grid')}"

def answer_typst(p):
    if p["type"] == "1":
        return f"${p['answer']}$"
    return gen.choice_answer_typst(dict(p, choices=[f"${c}$" for c in p["choices"]]))

def text(p):
    if p["type"] == "1":
        return f"{p['name']}: {plain(p['prompt'])}, GCF {plain(p['gcf'])}: width?"
    return plain(p["prompt"]) + "      " + gen.choices_text(p["choices"], plain)

def answer_text(p):
    if p["type"] == "1":
        return plain(p["answer"])
    return "; ".join(f"{a}. {plain(c)}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def height(p):
    return 1.6 if p["type"] == "1" else 0.9

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new polynomial; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "2":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
