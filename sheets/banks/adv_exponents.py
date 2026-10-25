"""Simplifying with exponents (Advanced Math), from the old app's sets
AdvMath_20_20 (powers of products and quotients), AdvMath_12_21 (a sum over
a monomial, or over a power of a product), and the 2025-26 midterm (letters
in the exponents).

The key's answer has positive exponents only, and it is one fraction with
its numerator multiplied out: (x^3 + x y^4)/y^3. In Type 4 every exponent
is a letter term with a positive coefficient, x^(2n + 3) y^(n - 4).

Each problem draws its own letters (gen.LETTERS), as the old sets did.
Problems are drawn at random within each template, and rejected when they
drift: every problem has a negative exponent to clear (Types 1-3), and
the numbers in the answer stay small. check() doesn't use how the problem
was built: it reads the prompt and the answer back with to_sympy, compares
their values at random points, and reads the answer's form from its text.

A problem: dict(type, prompt, answer, source), both in Typst math.
    prompt  "(3 x^2 y^(-1))^(-2) ((2 x^3 y)/(x^(-1) y^4))^3"
    answer  "(8 x^8)/(9 y^7)"
"""
import sympy as sp
from .. import gen
from ..gen import need, signed, signed_except
from ..check import to_sympy, same_value, simplest_form
from ..typmath import tx, single, fr

NAME = FAMILY = "adv_exponents"
FIXED = False
TITLE = "Simplifying with Exponents"
INSTRUCTIONS = "Simplify. Write each answer with positive exponents only."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Powers of Products and Quotients",
         look="A product or quotient raised to a power, with negative exponents.",
         move="Raise each factor to the outside power by multiplying exponents. Combine like bases: add "
              "exponents to multiply, subtract to divide. A factor with a negative exponent moves across the fraction bar."),
    dict(key="2", title="A Sum over a Monomial",
         look="Two terms over one term, with negative exponents.",
         move="Multiply the top and the bottom by the powers that clear every negative exponent. "
              "Simplify to one fraction."),
    dict(key="3", title="A Sum over a Power of a Product",
         look="Two terms over a product raised to a power, like (x y)^(-2).",
         move="Rewrite the power of the product first: (x y)^(-2) is x^(-2) y^(-2). Then clear the "
              "negative exponents as in Type 2."),
    dict(key="4", title="Letters in the Exponents",
         look="Exponents with letters in them, like x^(2n + 1).",
         move="The same rules: add exponents to multiply, subtract to divide, multiply for a power of a "
              "power. Combine like terms in each exponent.", space="1in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
BIG, BIG_EXP = 1000, 20               # the answer's numbers and exponents stay within these

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing the prompt: exponents as written, negative ones included
# ------------------------------------------------------------------
def pw(base, e):
    """base^e as written: "x", "x^3", "x^(-2)", "x^(2 n + 1)"; "" for e = 0."""
    if e == 0:
        return ""
    if e == 1:
        return base
    t = tx(e)
    return f"{base}^{t}" if t.isalnum() else f"{base}^({t})"

def mono(k, *powers):
    """A monomial as written: mono(3, ("x", 2), ("y", -1)) = "3 x^2 y^(-1)"."""
    body = [s for s in (pw(b, e) for b, e in powers) if s]
    if k != 1 or not body:
        body.insert(0, str(k))
    return " ".join(body)

def raised(inner, e):
    """(inner)^e, or inner alone when e is 1."""
    return inner if e == 1 else f"({inner})" + (f"^{e}" if e > 0 else f"^({e})")

def answer_of(prompt):
    """The key's answer for a prompt: one fraction, positive exponents."""
    e = sp.powsimp(to_sympy(prompt))
    if not letter_exponents(e):
        e = sp.cancel(e)
    return single(e)

def letter_exponents(e):
    """The powers in e whose exponents have letters: x^(2 n + 1)."""
    return [t for t in sp.preorder_traversal(e) if t.is_Pow and not t.exp.is_number]

def small(answer):
    e = to_sympy(answer)
    need(all(abs(a) <= BIG for a in sp.preorder_traversal(e) if a.is_Rational))
    need(all(abs(t.exp) <= BIG_EXP for t in sp.preorder_traversal(e) if t.is_Pow and t.exp.is_number))

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def e5(r):
    return signed(r, 1, 5)

def outer(r):
    """An outside power: -3..-1, 2, or 3."""
    return signed_except(r, 1, 3, 1)

def t1_product_times_quotient(r, x, y, n):            # AdvMath_20_20
    k1, k2 = r.randint(2, 5), r.randint(2, 5)
    a, b, c, d, f, g, h = (e5(r) for _ in range(7))
    p, q = outer(r), outer(r)
    return raised(mono(k1, (x, a), (y, b)), p) + " " + \
        raised(fr(mono(k2, (x, c), (y, d)), mono(1, (x, f), (y, g))), q)

def t1_quotient(r, x, y, n):
    k1, k2 = gen.reduced(r.randint(1, 9), r.randint(2, 9))
    need(k2 != 1)
    a, b, c, d = (e5(r) for _ in range(4))
    return raised(fr(mono(k1, (x, a), (y, b)), mono(k2, (x, c), (y, d))), outer(r))

def t1_power_over_power(r, x, y, n):
    k1, k2 = r.randint(2, 5), r.randint(2, 5)
    a, b, c, d = (e5(r) for _ in range(4))
    return fr(raised(mono(k1, (x, a), (y, b)), outer(r)), raised(mono(k2, (x, c), (y, d)), outer(r)))

def t2_two_letters_over(r, x, y, n):                  # AdvMath_12_21 no. 1
    a, b, c, d, f = (e5(r) for _ in range(5))
    return fr(f"{mono(1, (x, a), (y, b))} + {pw(y, c)}", mono(1, (x, d), (y, f)))

def t2_powers_over(r, x, y, n):                       # AdvMath_12_21 nos. 2-5
    a, c, d, f = (e5(r) for _ in range(4))
    return fr(f"{pw(x, a)} + {pw(y, c)}", mono(1, (x, d), (y, f)))

def t2_two_terms_over(r, x, y, n):
    a, b, c, d, f, g = (e5(r) for _ in range(6))
    return fr(f"{mono(1, (x, a), (y, b))} + {mono(1, (x, c), (y, d))}", mono(1, (x, f), (y, g)))

def t3_powers_over_xy(r, x, y, n):                    # AdvMath_12_21 nos. 6-7
    a, c = e5(r), e5(r)
    return fr(f"{pw(x, a)} + {pw(y, c)}", raised(f"{x} {y}", outer(r)))

def t3_two_letters_over_xy(r, x, y, n):
    a, b, c = e5(r), e5(r), e5(r)
    return fr(f"{mono(1, (x, a), (y, b))} + {pw(y, c)}", raised(f"{x} {y}", outer(r)))

def t3_powers_over_x2y(r, x, y, n):
    a, c = e5(r), e5(r)
    return fr(f"{pw(x, a)} + {pw(y, c)}", raised(mono(1, (x, 2), (y, 1)), outer(r)))

def lin(r, n, lo=1, hi=3):
    """A letter exponent p n + q, with p > 0."""
    return r.randint(lo, hi) * n + signed(r, 1, 6)

def t4_product(r, x, y, n):                           # the 2025-26 midterm, no. 32
    return f'({mono(1, (x, lin(r, n)), (y, lin(r, n)))}) ({mono(1, (x, lin(r, n)), (y, lin(r, n)))})'

def t4_quotient(r, x, y, n):
    return fr(mono(1, (x, lin(r, n, 2, 4)), (y, lin(r, n, 2, 4))), mono(1, (x, lin(r, n)), (y, lin(r, n))))

def t4_power_of_power(r, x, y, n):
    return fr(raised(mono(1, (x, lin(r, n, 1, 2)), (y, lin(r, n, 1, 2))), r.randint(2, 3)),
              mono(1, (x, lin(r, n)), (y, lin(r, n))))

TEMPLATES = {
    "1": [t1_product_times_quotient, t1_quotient, t1_power_over_power],
    "2": [t2_two_letters_over, t2_powers_over, t2_two_terms_over],
    "3": [t3_powers_over_xy, t3_two_letters_over_xy, t3_powers_over_x2y],
    "4": [t4_product, t4_quotient, t4_power_of_power],
}

def draw(entry, r, tpl):
    x, y, n = r.sample(gen.LETTERS, 3)                 # two bases, in order, and Type 4's exponent letter
    x, y = sorted((x, y))
    prompt = TEMPLATES[entry][tpl](r, x, y, sp.Symbol(n))
    if entry != "4":
        need("^(-" in prompt)                          # something to clear
    answer = answer_of(prompt)
    need(to_sympy(answer).free_symbols and simplest_form(answer))
    if entry == "4":
        need(len(letter_exponents(to_sympy(answer))) == 2 and "/" not in answer)   # both bases keep a letter exponent
    small(answer)
    return dict(prompt=prompt, answer=answer)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key,
                         lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Checking: the same value at random points, and the key's form
# ------------------------------------------------------------------
def check(p):
    try:
        ok = same_value(p["prompt"], p["answer"]) and simplest_form(p["answer"])
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "(3 x^2 y^(-1))^(-2)", "(8 x^8)/(9 y^7)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
