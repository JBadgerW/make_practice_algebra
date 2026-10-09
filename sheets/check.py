"""Typst math -> sympy, and numeric checks shared by every bank."""
import random, re
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication, convert_xor)

TR = standard_transformations + (implicit_multiplication, convert_xor)

def to_sympy(s):
    s = s.replace("ell", "L_")       # keep 'ell' a single symbol
    s = re.sub(r"\b(?!sqrt\b)([A-Za-z]\w*)\s*\(", r"\1*(", s)  # m(x + 2) is a product
    names = {n: sp.Symbol(n) for n in re.findall(r"[A-Za-z]\w*", s)}  # I, E, S are symbols, not sympy constants
    names.update({"pi": sp.pi, "sqrt": sp.sqrt})
    return parse_expr(s, transformations=TR, local_dict=names)

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
