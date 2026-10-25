"""Systems of two linear equations in two letters, shared by the Khan
Algebra 1 Unit 6 banks. (Not a bank.)

A system is stored as its two equations in Typst math, "eq1 ; eq2".

    equations(prompt)        the two equations
    coefficients(eq, u, v)   (a, b, c) with a u + b v = c, exactly (decimals as fractions)
    solve(prompt, u, v)      (u, v) as Fractions, or "none", or "many"
    system_typst(prompt)     the system with a brace, aligned at the equals signs
    answer_text(u, v, sol)   the key: "x = 3, y = -2"
    solves(prompt, answer)   the answer, "x = 3, y = -2", satisfies both equations
"""
import re
from fractions import Fraction as F
import sympy as sp
from ...gen import written
from ...linear import exact
from ...typmath import dfrac, tx, text as plain

def equations(prompt):
    return [e.strip() for e in prompt.split(";")]

def coefficients(eq, u="x", v="y"):
    l, _, r = eq.partition("=")
    e = sp.expand(exact(l) - exact(r))
    U, V = sp.Symbol(u), sp.Symbol(v)
    a, b = e.coeff(U, 1), e.coeff(V, 1)
    c = -e.subs({U: 0, V: 0})
    if sp.expand(e - a * U - b * V + c) != 0:
        raise ValueError("not linear in the two letters")
    return F(str(a)), F(str(b)), F(str(c))

def solve(prompt, u="x", v="y"):
    """The solution: (u, v), "none", or "many"."""
    (a, b, c), (d, e, f) = (coefficients(q, u, v) for q in equations(prompt))
    det = a * e - b * d
    if det != 0:
        return ((c * e - b * f) / det, (a * f - c * d) / det)
    # parallel: the same line if every 2x2 minor with the constants vanishes too
    if a * f - c * d == 0 and b * f - c * e == 0:
        return "many"
    return "none"

def letters(prompt):
    """The system's two letters, in alphabetical order (x before y)."""
    syms = set()
    for q in equations(prompt):
        l, _, r = q.partition("=")
        syms |= exact(l).free_symbols | exact(r).free_symbols
    names = sorted(str(s) for s in syms)
    if len(names) != 2:
        raise ValueError("a system in two letters")
    return names

def system_typst(prompt):
    rows = [q.replace("=", "&=", 1).replace("*", "dot") for q in equations(prompt)]     # 2 * 0.3 h: shown 2 · 0.3 h
    return f"$display(cases({dfrac(rows[0])}, {dfrac(rows[1])}))$"

def number(q):
    return tx(sp.Rational(q.numerator, q.denominator))

def answer_text(u, v, sol):
    return f"{u} = {number(sol[0])}, {v} = {number(sol[1])}"

ANSWER = re.compile(r"\s*(\w+)\s*=\s*([^,]+),\s*(\w+)\s*=\s*([^,]+)\s*")

def read_answer(answer):
    """"x = 3, y = -2" -> {"x": 3, "y": -2} (Fractions)."""
    m = ANSWER.fullmatch(answer.replace("−", "-"))
    if not m:
        raise ValueError("write the answer like x = 3, y = -2")
    return {m.group(1): F(str(exact(m.group(2)))), m.group(3): F(str(exact(m.group(4))))}

def solves(prompt, answer):
    """The answer is the system's one solution: it satisfies both equations, and there is no other."""
    vals = read_answer(answer)
    u, v = letters(prompt)
    if set(vals) != {u, v} or not isinstance(solve(prompt, u, v), tuple):
        return False
    for q in equations(prompt):
        a, b, c = coefficients(q, u, v)
        if a * vals[u] + b * vals[v] != c:
            return False
    return True

# ------------------------------------------------------------------
# What the Unit 6 banks share: writing an equation, and the bank functions
# for "solve the system" problems
# ------------------------------------------------------------------
def standard(a, b, c, u="x", v="y", v_first=False):
    """a u + b v = c, or b v + a u = c."""
    left = written((b, v), (a, u)) if v_first else written((a, u), (b, v))
    return f"{left} = {c}"

def answer_of(prompt):
    u, v = letters(prompt)
    sol = solve(prompt, u, v)
    if not isinstance(sol, tuple):
        raise ValueError(f"the system has {sol} solutions")
    return answer_text(u, v, sol)

def check(p):
    try:
        return "checked" if solves(p["prompt"], p["answer"]) else "failed"
    except Exception:
        return "unchecked"

def text(p):
    return "   ".join("{ " + plain(q.replace("*", "·")) for q in equations(p["prompt"]))
