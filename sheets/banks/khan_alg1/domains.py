"""Functions for the Khan Algebra 1 domain lessons (8-9, 8-10), and their
domains. (Not a bank.)

    function(r)    (Typst, the special number, the domain's kind): Khan's kinds,
                   rational (excludes a number), square root (from a boundary on),
                   and polynomial (every number)
    domain(body)   the domain, computed by sympy (adv_functions.domain_of)
"""
import sympy as sp
from ...gen import need, signed, written
from ...linear import exact
from ..adv_functions import domain_of

def lin(a, c):
    return written((a, "x"), (c, ""))

def function(r):
    body, s, kind = _function(r)
    return body, sp.sympify(s), kind

def _function(r):
    kind = r.choice(("rational", "root", "polynomial"))
    if kind == "rational":
        p = signed(r, 1, 9)
        form = r.randrange(3)
        top = lin(1, -signed(r, 1, 9)) if form == 0 else "x" if form == 1 else str(signed(r, 1, 9))
        body = f"({top})/({lin(1, -p)})" if form == 0 else f"{top}/({lin(1, -p)})"     # x/(x - 7), 4/(x - 5)
        return body, p, kind
    if kind == "root":
        k = r.choice((1, 1, 2, 8, -1, -2))
        c = signed(r, 1, 10) if abs(k) == 1 else 0
        return f"sqrt({lin(k, c)})", exact(f"{-c}/{k}"), kind
    form = r.randrange(4)
    a = signed(r, 1, 9)
    body = [f"(x {'+' if a > 0 else '-'} {abs(a)})^2", f"({lin(1, a)})/{r.randint(2, 5)}",
            lin(-r.randint(2, 5), r.randint(1, 9)), lin(1, a)][form]
    return body, -a, kind

def domain(body):
    return domain_of(exact(body))
