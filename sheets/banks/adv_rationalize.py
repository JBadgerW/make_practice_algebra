"""Rationalizing denominators (Advanced Math), from the old app's set
AdvMath_10_04 (a-d) and the 2025-26 midterm (square roots of negatives).

The key's answer is one fraction in lowest terms with no radical and no i
in its denominator: (3 sqrt(2))/2, (3 - i)/5, -(2 + sqrt(3))/3. Powers of i
are reduced, and a square root of a negative is written with i.

check() doesn't use how the problem was built: it reads the prompt and the
answer back with to_sympy (i as the imaginary unit), compares their values,
and reads the answer's form from its text.

A problem: dict(type, prompt, answer, source), both in Typst math.
    prompt  "(4 + sqrt(3))/(2 - sqrt(3))"
    answer  "11 + 6 sqrt(3)"
"""
import sympy as sp
from .. import gen
from ..gen import need, signed, except_
from ..check import to_sympy, same_value, simplest_form
from ..typmath import tx, single, fr

NAME = FAMILY = "adv_rationalize"
FIXED = False
TITLE = "Rationalizing Denominators"
INSTRUCTIONS = "Simplify. Leave no radical and no i in a denominator."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="A Square Root in the Denominator",
         look="One term in the denominator, with a square root.",
         move="Multiply the top and the bottom by that square root. Then simplify the fraction."),
    dict(key="2", title="i in the Denominator",
         look="One term in the denominator, with i or a power of i.",
         move="Reduce the powers of i. Multiply the top and the bottom by i, and use i^2 = -1."),
    dict(key="3", title="A Binomial with a Square Root",
         look="Two terms in the denominator, one of them a square root.",
         move="Multiply the top and the bottom by the conjugate: a + b sqrt(c) becomes a - b sqrt(c). "
              "The denominator is a^2 - b^2 c. Multiply out the top and reduce.", space="1.5in"),
    dict(key="4", title="A Complex Denominator",
         look="A complex number a + b i in the denominator; maybe powers of i or square roots of negatives.",
         move="Write each square root of a negative with i and reduce the powers of i. Multiply the top "
              "and the bottom by the conjugate a - b i; the denominator is a^2 + b^2.", space="1.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
RADICANDS = (2, 3, 5, 6, 7, 10, 11)           # square-free, so sqrt(c) doesn't simplify
BIG = 200                                     # the answer's numbers stay within this

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------
def term(k, body="", first=False):
    """k body as a term of a sum: term(3, "sqrt(2)") = " + 3 sqrt(2)", term(-1, "i") = " - i"."""
    if k == 0:
        return ""
    mag = body if abs(k) == 1 and body else f"{abs(k)} {body}".strip()
    if first:
        return ("-" if k < 0 else "") + mag
    return (" - " if k < 0 else " + ") + mag

def ipow(k):
    return "i" if k == 1 else f"i^{k}"

def answer_of(prompt):
    """The key's answer: rationalized, as one fraction in lowest terms."""
    e = sp.expand(sp.radsimp(to_sympy(prompt, imaginary=True)))
    need(e != 0 and not e.has(sp.zoo, sp.nan))
    return single(e)

# ------------------------------------------------------------------
# Drawing (AdvMath_10_04 a-d, with its coinflip bug fixed: its b and e
# were always ±1)
# ------------------------------------------------------------------
def t1_over_root(r):                          # 10_04 a
    return fr(str(signed(r, 1, 12)), f"sqrt({r.choice(RADICANDS)})")

def t1_over_k_root(r):
    return fr(str(signed(r, 1, 12)), f"{r.randint(2, 6)} sqrt({r.choice(RADICANDS)})")

def t1_root_over_root(r):
    a, b = r.sample(RADICANDS, 2)
    return fr(term(signed(r, 1, 5), f"sqrt({a})", True), f"sqrt({b})")

def t2_over_i(r):                             # 10_04 b
    a = r.randint(1, 12)
    return fr(term(r.choice((-1, 1)) * a, "", True), f"{except_(r, 2, 12, a)} i")

def t2_binomial_over_i(r):
    return fr(term(signed(r, 1, 9), "", True) + term(signed(r, 1, 9), "i"), f"{r.randint(2, 9)} i")

def t2_over_power(r):
    return fr(str(signed(r, 1, 12)), f"{r.randint(2, 9)} {ipow(r.choice((3, 5, 7)))}")

def coef(r):
    """A radical's coefficient: ±1 half the time, else ±2..12."""
    return r.choice((-1, 1)) if r.random() < 0.5 else signed(r, 2, 12)

def t3_number_over(r):
    c = r.choice(RADICANDS)
    return fr(str(signed(r, 1, 12)), term(signed(r, 1, 12), "", True) + term(coef(r), f"sqrt({c})"))

def t3_binomial_over(r):                      # 10_04 c
    c = r.choice(RADICANDS)
    top = term(signed(r, 1, 12), "", True) + term(coef(r), f"sqrt({c})")
    return fr(top, term(signed(r, 1, 12), "", True) + term(coef(r), f"sqrt({c})"))

def t3_root_over(r):
    c = r.choice(RADICANDS)
    return fr(term(signed(r, 1, 6), f"sqrt({c})", True), term(signed(r, 1, 12), "", True) + term(coef(r), f"sqrt({c})"))

def complex_bottom(r):
    return term(signed(r, 1, 8), "", True) + term(signed(r, 1, 8), "i")

def t4_number_over(r):
    return fr(str(signed(r, 1, 12)), complex_bottom(r))

def t4_powers_of_i(r):                        # 10_04 d
    c, e = r.sample(range(2, 9), 2)
    top = term(signed(r, 1, 8), "", True) + term(signed(r, 1, 3), ipow(c)) + term(signed(r, 1, 3), ipow(e))
    return fr(top, complex_bottom(r))

def t4_roots_of_negatives(r):                 # the 2025-26 midterm
    a, b = r.choice((4, 9, 16, 25)), r.choice((4, 9))
    top = f"sqrt({-a}){term(signed(r, 1, 8))}"
    return fr(top, term(signed(r, 1, 6), "", True) + f" + {ipow(r.choice((4, 8)))} sqrt({-b})")

TEMPLATES = {
    "1": [t1_over_root, t1_over_k_root, t1_root_over_root],
    "2": [t2_over_i, t2_binomial_over_i, t2_over_power],
    "3": [t3_number_over, t3_binomial_over, t3_root_over],
    "4": [t4_number_over, t4_powers_of_i, t4_roots_of_negatives],
}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    answer = answer_of(prompt)
    need(simplest_form(answer, imaginary=True))
    e = to_sympy(answer, imaginary=True)
    need(all(abs(a) <= BIG for a in sp.preorder_traversal(e) if a.is_Rational))
    if entry in ("3", "4"):
        need(not e.is_Integer)                          # the conjugate doesn't cancel everything
    return dict(prompt=prompt, answer=answer)

def check(p):
    try:
        ok = same_value(p["prompt"], p["answer"], imaginary=True) and simplest_form(p["answer"], imaginary=True)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "(4 + sqrt(3))/(2 - sqrt(3))", "11 + 6 sqrt(3)", imaginary=True)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
