"""One-variable linear equations, shared by the banks that solve them: the
solution read from the prompt with sympy, and the key's form, "x = 3",
"x = -1.5" (decimals: the prompt's numbers are decimals), or "x = -1/2".

Decimals in a prompt are read exactly (0.1 is 1/10), so a check never
rounds."""
import re
from decimal import Decimal
from fractions import Fraction as F
import sympy as sp
from .check import to_sympy
from .typmath import tx

def exact(t):
    """Typst math -> sympy, decimals as exact fractions."""
    return sp.nsimplify(to_sympy(t), rational=True)

def sides(prompt):
    l, r = prompt.split("=")
    return exact(l), exact(r)

def letter(prompt):
    """The equation's one letter (read from both sides: in an identity it cancels)."""
    l, r = sides(prompt)
    syms = l.free_symbols | r.free_symbols
    if len(syms) != 1:
        raise ValueError("the equation needs exactly one letter")
    return syms.pop()

def solutions(prompt):
    """The real solutions of a linear equation: a FiniteSet, EmptySet, or Reals."""
    l, r = sides(prompt)
    return sp.solveset(l - r, letter(prompt), sp.S.Reals)

def count(prompt):
    """"none", "one", or "all"."""
    s = solutions(prompt)
    return "none" if s == sp.S.EmptySet else "all" if s == sp.S.Reals else "one"

def as_decimal(q, places=3):
    """A rational as a terminating decimal, "-1.5", "12"; ValueError if it doesn't terminate within places."""
    q = F(int(q.p), int(q.q)) if isinstance(q, sp.Rational) else F(q)
    d = Decimal(q.numerator) / Decimal(q.denominator)
    if d != round(d, places) or F(str(round(d, places))) != q:
        raise ValueError(f"{q} isn't a short decimal")
    s = format(round(d, places), "f")
    return s.rstrip("0").rstrip(".") if "." in s else s

def answer_of(prompt, decimals=False):
    """The key's answer, "x = 3", for an equation with one solution; ValueError otherwise.
    decimals: written as a decimal ("x = -1.5"), else as a fraction ("x = -3/2")."""
    s = solutions(prompt)
    if not isinstance(s, sp.FiniteSet) or len(s) != 1:
        raise ValueError("the equation doesn't have exactly one solution")
    v = next(iter(s))
    return f"{letter(prompt)} = {as_decimal(v) if decimals else tx(v)}"

DECIMAL = re.compile(r"-?\d+(\.\d+)?")
FRACTION = re.compile(r"-?\d+(/\d+)?")

def solves(prompt, answer, form=None):
    """The answer, "x = 3", is the equation's one solution: substituted, both sides agree.
    form: "decimal" (an integer or a decimal) or "fraction" (an integer or a fraction in lowest terms)."""
    lhs, _, rhs = answer.partition("=")
    v, rhs = letter(prompt), rhs.strip()
    if lhs.strip() != str(v) or count(prompt) != "one":
        return False
    if form == "decimal" and not DECIMAL.fullmatch(rhs.replace(" ", "")):
        return False
    if form == "fraction":
        t = rhs.replace(" ", "")
        if not FRACTION.fullmatch(t) or ("/" in t and sp.Rational(t).q != int(t.split("/")[1])):
            return False
    l, r = sides(prompt)
    return sp.simplify((l - r).subs(v, exact(rhs))) == 0
