"""One-variable linear equations, shared by the banks that solve them: the
solution read from the prompt with sympy, and the key's form, "x = 3"."""
import sympy as sp
from .check import to_sympy, side_diff
from .typmath import tx

def letter(prompt):
    """The equation's one letter (read from both sides: in an identity it cancels)."""
    l, r = prompt.split("=")
    syms = to_sympy(l).free_symbols | to_sympy(r).free_symbols
    if len(syms) != 1:
        raise ValueError("the equation needs exactly one letter")
    return syms.pop()

def solutions(prompt):
    """The real solutions of a linear equation: a FiniteSet, EmptySet, or Reals."""
    return sp.solveset(side_diff(prompt), letter(prompt), sp.S.Reals)

def count(prompt):
    """"none", "one", or "all"."""
    s = solutions(prompt)
    return "none" if s == sp.S.EmptySet else "all" if s == sp.S.Reals else "one"

def answer_of(prompt):
    """The key's answer, "x = 3", for an equation with one solution; ValueError otherwise."""
    s = solutions(prompt)
    if not isinstance(s, sp.FiniteSet) or len(s) != 1:
        raise ValueError("the equation doesn't have exactly one solution")
    return f"{letter(prompt)} = {tx(next(iter(s)))}"

def solves(prompt, answer):
    """The answer, "x = 3", is the equation's one solution: substituted, both sides agree."""
    lhs, _, rhs = answer.partition("=")
    v = letter(prompt)
    if lhs.strip() != str(v) or count(prompt) != "one":
        return False
    return sp.simplify(side_diff(prompt).subs(v, to_sympy(rhs))) == 0
