"""Typst math -> sympy, and numeric checks shared by every bank."""
import random, re
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication, convert_xor)

TR = standard_transformations + (implicit_multiplication, convert_xor)
FUNCTIONS = {"sqrt": sp.sqrt, "abs": sp.Abs, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "log": sp.log}

def to_sympy(s, imaginary=False, evaluate=True):
    """Typst math -> sympy. imaginary: i is the imaginary unit, not a letter.
    evaluate=False keeps the tree as written (a/b is a * b^-1), for checking an answer's form."""
    s = s.replace("ell", "L_")       # keep 'ell' a single symbol
    s = re.sub(r"\b(?!(?:sqrt|abs|sin|cos|tan|log)\b)([A-Za-z]\w*)\s*\(", r"\1*(", s)  # m(x + 2) is a product
    names = {n: sp.Symbol(n) for n in re.findall(r"[A-Za-z]\w*", s)}  # I, E, S are symbols, not sympy constants
    names.update(FUNCTIONS, pi=sp.pi, degree=sp.pi / 180)
    if imaginary:
        names["i"] = sp.I
    return parse_expr(s, transformations=TR, local_dict=names, evaluate=evaluate)

def side_diff(eq):
    l, r = eq.split("=")
    return to_sympy(l) - to_sympy(r)

def syms_of(prompt):
    return {str(v).replace("L_", "ell"): v for v in side_diff(prompt).free_symbols}

def holds(eq, prompt, var, sol, trials=5):
    """eq is true whenever var = sol in prompt (random positive values for the rest)."""
    e, syms = side_diff(eq), syms_of(prompt)
    assert e.free_symbols <= set(syms.values()), (eq, prompt)
    se = to_sympy(sol)
    for _ in range(trials):
        vals = {s: random.uniform(1.5, 9.5) for s in syms.values()}
        vals[syms[var]] = complex(se.subs(vals).evalf())
        assert abs(complex(e.subs(vals).evalf())) < 1e-8, (eq, prompt, var, sol)

def same_value(a, b, trials=6, imaginary=False):
    """Typst expressions a and b are equal: at random values of their letters
    (1.2 to 2.8, so exponents that are letters stay tame), relative error under 1e-9."""
    ea, eb = to_sympy(a, imaginary), to_sympy(b, imaginary)
    syms = sorted(ea.free_symbols | eb.free_symbols, key=str)
    for _ in range(trials):
        vals = {s: random.uniform(1.2, 2.8) for s in syms}
        try:
            va, vb = complex(ea.subs(vals).evalf()), complex(eb.subs(vals).evalf())
        except (TypeError, ZeroDivisionError):      # zoo: a point where one side is undefined
            continue
        if not abs(va - vb) <= 1e-9 * max(1, abs(va)):
            return False
    return True

NEGATIVE_EXPONENT = re.compile(r"\^\s*\(?\s*-")

def denominators(text, imaginary=False):
    """What the Typst expression divides by, as written."""
    out = []
    def walk(e):
        if isinstance(e, sp.Pow) and e.exp.is_number and e.exp.is_negative:
            out.append(e.base)
        for a in e.args:
            walk(a)
    walk(to_sympy(text, imaginary, evaluate=False))
    return out

def simplest_form(text, imaginary=False):
    """The answer follows the key's conventions, read from the text as written:
    no negative exponents, no radical in a denominator, and (imaginary) no i in one."""
    if NEGATIVE_EXPONENT.search(text):
        return False
    for d in denominators(text, imaginary):
        if any(isinstance(p, sp.Pow) and p.exp.is_Rational and not p.exp.is_Integer for p in sp.preorder_traversal(d)):
            return False
        if imaginary and d.has(sp.I):
            return False
    return True
