"""Integer polynomials in one letter, shared by the banks that multiply and
factor them: the key's forms, and reading an answer's form from its text.

    expanded(e, ascending)   standard form: "6 x^2 - x - 15" (descending degree),
                             or ascending: "25 - x^2"
    factored(e, reversed_)   the key's factored form: the greatest common factor
                             (with the sign of the leading term) in front, then each
                             factor, a repeated one as a power: "-2 (x - 3) (x + 5)",
                             a power of the letter before the binomials: "3 x^2 (x - 1)",
                             "(2 x + 1)^2"; reversed_ writes the constant first, as a
                             prompt that leads with it does: "(9 + x) (9 - x)"
    standard(text, either)   the text is a sum of terms, no parentheses, every
                             degree once, in descending order (either: or ascending)
    completely_factored(text, prompt)
                             the same polynomial as the prompt, the content pulled
                             out in front, every factor left irreducible over the integers
    terms(text)              the terms as written: "x^2 - 3 x + 1" -> [x^2, -3 x, 1]
"""
import math
import sympy as sp
from .check import to_sympy
from .typmath import Printer, tx

def letter(e):
    syms = sorted(e.free_symbols, key=str)
    return syms[0] if syms else sp.Symbol("x")

def expanded(e, ascending=False):
    """Standard form (descending degree), or ascending: "25 - x^2", "12 - 5 x - 2 x^2"."""
    e = sp.expand(e)
    if not ascending or not e.free_symbols:
        return tx(e)
    v = letter(e)
    ts = sorted(sp.Add.make_args(e), key=lambda t: sp.degree(t, v))
    out = ""
    for i, t in enumerate(ts):
        neg = t.could_extract_minus_sign()
        body = tx(-t if neg else t)
        out += ("-" + body if neg else body) if i == 0 else (" - " if neg else " + ") + body
    return out

def content(p):
    """The greatest common factor of the coefficients (positive), in every letter."""
    syms = sorted(p.free_symbols, key=str)
    return math.gcd(*[int(c) for c in sp.Poly(p, *syms).coeffs()]) if syms else abs(int(p))

def binomial(f, reversed_=False):
    """A factor as the key writes it: "2 x + 1"; reversed_: "1 + 2 x", "9 - x" (constant first)."""
    if not reversed_:
        return tx(f)
    ts = sorted(sp.Add.make_args(f), key=lambda t: sp.degree(t, letter(f)))
    out = ""
    for i, t in enumerate(ts):
        neg = t.could_extract_minus_sign()
        body = tx(-t if neg else t)
        out += ("-" + body if neg else body) if i == 0 else (" - " if neg else " + ") + body
    return out

def factored(e, reversed_=False):
    """The key's factored form of an integer polynomial."""
    e = sp.expand(e)
    c, parts = sp.factor_list(e)
    lead = sp.Poly(e, letter(e)).LC()
    out = []
    for f, m in parts:
        if sp.Poly(f, letter(f)).LC() < 0 and not reversed_:      # each factor leads with a plus
            f, c = -f, c * (-1) ** m
        if reversed_ and f.subs(letter(f), 0) < 0:                  # (9 - x), not (-9 + x)
            f, c = -f, c * (-1) ** m
        out.append((f, m))
    v = letter(e)
    out.sort(key=lambda fm: (fm[0].is_Add, sp.degree(fm[0], v), fm[0].subs(v, 0) * (-1 if reversed_ else 1),
                             str(fm[0])))                   # 3 x^2 (x - 3) (x + 5): a letter before the binomials
    body = " ".join(f"({binomial(f, reversed_)})" + (f"^{m}" if m > 1 else "") if f.is_Add
                    else (tx(f) if m == 1 else f"{tx(f)}^{m}") for f, m in out)
    return body if c == 1 else "-" + body if c == -1 else f"{tx(c)} {body}"

def terms(text):
    """The terms as written, read without combining anything."""
    t = to_sympy(text, evaluate=False)
    return list(t.args) if isinstance(t, sp.Add) else [t]

def standard(text, either=False):
    """A sum of monomials, as written: no parentheses, every degree once, descending
    (either: or ascending, "25 - x^2")."""
    if "(" in text:
        return False
    ts = [sp.sympify(t) for t in terms(text)]
    e = to_sympy(text)
    v = letter(e)
    degs = [sp.degree(t, v) if t.free_symbols else 0 for t in ts]
    return len(set(degs)) == len(degs) and (degs == sorted(degs, reverse=True) or (either and degs == sorted(degs)))

def _evaluated(e):
    return e.func(*[_evaluated(a) for a in e.args]) if e.args else e

def completely_factored(text, prompt):
    """Equal to the prompt, the number in front the content, every factor irreducible."""
    a, p = to_sympy(text), to_sympy(prompt)
    if sp.expand(a - p) != 0:
        return False
    t = to_sympy(text, evaluate=False)
    fs = [_evaluated(f) for f in (t.args if isinstance(t, sp.Mul) else [t])]
    number = sp.Integer(1)
    for f in fs:
        base = f.base if f.is_Pow and f.exp.is_Integer else f
        if not base.free_symbols:
            number *= f
            continue
        if base.is_Symbol:
            continue
        if content(base) != 1:                                     # a number left inside
            return False
        _, parts = sp.factor_list(base)
        if len(parts) != 1 or parts[0][1] != 1:                    # it factors again
            return False
    return abs(number) == content(p)
