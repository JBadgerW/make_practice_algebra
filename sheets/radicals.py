"""Square roots in simplest form, shared by the banks that simplify them.

    simplify(c, n, powers)  c sqrt(n x^a y^b ...) -> (coefficient, outside powers, inside n, inside powers)
    written(c, out, n, inside)   Typst: "6 x^2 sqrt(5 x)", "3 sqrt(2)", "4 a b^3"
    simplest(text)          the answer as written has one radical at most, and nothing
                            left inside it to take out: a square-free number, every
                            letter's exponent 0 or 1

Letters are assumed positive, as the lessons say.
"""
import re
from .check import to_sympy
from .gen import prime_factors

def squarefree(n):
    """n = k^2 m with m square-free -> (k, m)."""
    k, m = 1, 1
    for p in set(prime_factors(n)):
        e = prime_factors(n).count(p)
        k *= p ** (e // 2)
        m *= p ** (e % 2)
    return k, m

def simplify(c, n, powers):
    """c sqrt(n * prod x^e) -> (coefficient, {x: outside exponent}, inside n, {x: inside exponent})."""
    k, m = squarefree(n)
    out = {x: e // 2 for x, e in powers.items() if e // 2}
    inside = {x: e % 2 for x, e in powers.items() if e % 2}
    return c * k, out, m, inside

def monomial(c, powers):
    """"6 x^2 y", "x", "-3": letters in alphabetical order."""
    body = " ".join(x if e == 1 else f"{x}^{e}" for x, e in sorted(powers.items()) if e)
    if not body:
        return str(c)
    return body if c == 1 else "-" + body if c == -1 else f"{c} {body}"

def written(c, out, n, inside):
    """The simplified radical in Typst: coefficient and outside letters, then sqrt(inside)."""
    root = monomial(n, inside) if (n != 1 or inside) else ""
    front = monomial(c, out)
    if not root:
        return front
    front = "" if front == "1" else "-" if front == "-1" else front + " "
    return f"{front}sqrt({root})"

SQRT = re.compile(r"sqrt\(([^()]*)\)")

def simplest(text):
    """One radical at most, with nothing left inside it to take out."""
    roots = SQRT.findall(text)
    if len(roots) > 1:
        return False
    for r in roots:
        e = to_sympy(r)
        num, rest = e.as_coeff_Mul()
        if not num.is_Integer or squarefree(int(num))[0] != 1:
            return False
        for f in rest.as_powers_dict().items():
            if f[0] != 1 and f[1] != 1:
                return False
    return True
