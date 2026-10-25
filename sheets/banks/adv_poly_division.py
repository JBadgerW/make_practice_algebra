"""Polynomial division (Advanced Math), from the old app's set
AdvMath_00_04_polynomial_division and Test 5, no. 5 (a missing term).

Problems are built backward, as the old set did: pick the quotient, the
divisor, and the remainder, and multiply out the dividend. The key writes
the quotient, then the remainder over the divisor:
2 x^2 - 3 x + 5 + 7/(2 x + 3).

A problem: dict(type, prompt, divisor, answer, source), all Typst math.
    prompt   the dividend: "4 x^3 + 7 x - 8"
    divisor  "2 x + 3"
check() doesn't use how the problem was built: the answer must equal the
dividend over the divisor at random points, its polynomial part must be a
polynomial, and what's left over must be a number over the divisor.
"""
import sympy as sp
from .. import gen
from ..gen import need, signed
from ..check import to_sympy, same_value
from ..typmath import tx, fr, display, dfrac, text as plain

NAME = FAMILY = "adv_poly_division"
FIXED = False
TITLE = "Polynomial Division"
INSTRUCTIONS = ""                                # the prompt says it: "Divide ... by ..."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Dividing by x + a, No Remainder",
         look="A divisor x + a or x - a that divides evenly.",
         move="Long or synthetic division. Write a 0 for each missing power in the dividend. "
              "The remainder is 0, so the quotient is the answer."),
    dict(key="2", title="Dividing by x + a, with a Remainder",
         look="A divisor x + a or x - a, and a remainder.",
         move="Divide as usual. Write the answer as quotient + remainder/divisor."),
    dict(key="3", title="Dividing by a x + b",
         look="A divisor whose first coefficient isn't 1, like 2 x + 3.",
         move="Long division: divide each leading term by a x. Write the answer as quotient + "
              "remainder/divisor.", space="1.75in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")     # one line: "Divide ... by ...", the answer clear of it
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X = sp.Symbol("x")
BIG = 150                                        # the dividend's coefficients stay within this

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], p["divisor"])

def quotient(r, degree, missing=False):
    """A quotient of that degree: leading coefficient 1..4; with missing, one inner power is 0."""
    cs = [r.randint(1, 4)] + [r.randint(-8, 8) for _ in range(degree)]
    if missing and degree >= 2:
        cs[r.randint(1, degree - 1)] = 0
    return sum(c * X ** (degree - i) for i, c in enumerate(cs))

def build(r, q, a, b, rem):
    """(prompt, divisor, answer) for (a x + b) q + rem divided by a x + b."""
    need(len(sp.Add.make_args(q)) >= 2)                       # not x - 8 dividing x^2 - 8 x
    d = a * X + b
    dividend = sp.expand(d * q + rem)
    need(all(abs(c) <= BIG for c in sp.Poly(dividend, X).coeffs()))
    answer = tx(q, "x")
    if rem:
        answer += (" + " if rem > 0 else " - ") + fr(str(abs(rem)), tx(d))
    return tx(dividend, "x"), tx(d), answer

def t_even(degree, missing=False):
    def t(r):
        return build(r, quotient(r, degree, missing), 1, signed(r, 1, 9), 0)
    return t

def t_remainder(degree, missing=False):
    def t(r):
        return build(r, quotient(r, degree, missing), 1, signed(r, 1, 9), signed(r, 1, 12))
    return t

def t_leading(degree, missing=False):            # AdvMath_00_04: divisor f x + g, f = 2..4
    def t(r):
        a, b = r.randint(2, 4), signed(r, 1, 9)
        need(sp.gcd(a, b) == 1)
        return build(r, quotient(r, degree, missing), a, b, signed(r, 1, 12))
    return t

def t_missing_dividend(r):                       # Test 5, no. 5: x^3 - 5 x^2 + 9 divided by x - 4
    b, rem = signed(r, 1, 6), signed(r, 1, 12)
    q = quotient(r, 2)
    dividend = sp.expand((X + b) * q + rem)
    need(sp.Poly(dividend, X).coeff_monomial(X) == 0)        # the dividend has no x term
    return build(r, q, 1, b, rem)

TEMPLATES = {
    "1": [t_even(1), t_even(2), t_even(3, missing=True)],
    "2": [t_remainder(2), t_remainder(3, missing=True), t_missing_dividend],
    "3": [t_leading(1), t_leading(2), t_leading(2, missing=True)],
}

def draw(entry, r, tpl):
    prompt, divisor, answer = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, divisor=divisor, answer=answer)

def check(p):
    try:
        d = to_sympy(p["divisor"])
        if not same_value(fr(p["prompt"], p["divisor"]), p["answer"]):
            return "failed"
        rest = [t for t in sp.Add.make_args(to_sympy(p["answer"])) if not t.is_polynomial(X)]
        if len(rest) > 1 or any(sp.cancel(t * d).free_symbols for t in rest):
            return "failed"                                   # the remainder is a number over the divisor
        return "checked"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing: "dividend ; divisor"
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return f"Divide ${p['prompt']}$ by ${p['divisor']}$."

def answer_typst(p):
    return display(dfrac(p["answer"]))

def text(p):
    return f"Divide {plain(p['prompt'])} by {plain(p['divisor'])}."

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.3

def edit_text(p):
    return f"{p['prompt']} ; {p['divisor']}"

def from_edit(t, old):
    top, _, bottom = t.replace("−", "-").partition(";")
    top, bottom = " ".join(top.split()), " ".join(bottom.split()) or old["divisor"]
    try:
        q, rem = sp.div(sp.Poly(to_sympy(top), X), sp.Poly(to_sympy(bottom), X))
    except Exception:
        raise ValueError("write the dividend, then ; and the divisor: x^3 - 5 x^2 + 9 ; x - 4") from None
    answer = tx(q.as_expr(), "x")
    r = rem.as_expr()
    if r != 0:
        answer += " + " + fr(tx(r), bottom) if not r.could_extract_minus_sign() else " - " + fr(tx(-r), bottom)
    new = dict(old, prompt=top, divisor=bottom, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
