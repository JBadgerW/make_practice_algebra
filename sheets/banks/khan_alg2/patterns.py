"""The factoring patterns of Khan Algebra 2, Unit 3 (3-5 to 3-7): U and V,
and the expressions (U + V)^2, (U - V)^2, U^2 - V^2 written from them.
(Not a bank.)

U and V are what Khan allows: a constant integer or a single-variable
expression, a monomial k x^n or a binomial (x + h)^n.

    Part                 mono(k, v, n) or binomial(v, h, n)
    square_text(U, V, s) U^2 + 2 s U V + V^2 as Khan writes it: (x + 7)^2 + 2 y (x + 7) + y^2
    difference_text(U, V)            U^2 - V^2: 16 x^4 - 25, (x + 1)^2 - 4 y^2
    sum_text(U, V, s)    U + s V, a binomial's parentheses dropped, like terms combined: x - 5 + y^3
    irreducible(text)    no factor over the integers at all: no pattern applies
"""
import sympy as sp
from ... import gen
from ...check import to_sympy

class Part:
    def __init__(self, kind, k=1, v="", n=1, h=0):
        self.kind, self.k, self.v, self.n, self.h = kind, k, v, n, h

    def body(self):
        """The part without its number: "x^3", "y", "", "(x + 7)", "(y - 2)^2"."""
        if self.kind == "bin":
            inner = gen.written((1, self.v), (self.h, ""))
            return f"({inner})" if self.n == 1 else f"({inner})^{self.n}"
        return "" if self.n == 0 or not self.v else self.v if self.n == 1 else f"{self.v}^{self.n}"

    def text(self):
        return gen.written((self.k, self.body())) if self.body() else str(self.k)

    def power(self, p):
        return Part(self.kind, self.k ** p, self.v, self.n * p, self.h)

    def terms(self, sign=1):
        """The part as terms of a sum, a binomial's parentheses dropped when its power is 1."""
        if self.kind == "bin" and self.n == 1:
            return [(sign, self.v), (sign * self.h, "")]
        return [(sign * self.k, self.body())]

    def sym(self):
        return to_sympy(self.text())

def mono(k, v="", n=1):
    return Part("mono", k, v, n if v else 0)

def binomial(v, h, n=1):
    return Part("bin", 1, v, n, h)

def product_body(*parts):
    """The letters of a product, monomials first: "x^3 y", "y (x + 7)"."""
    ps = sorted(parts, key=lambda p: p.kind == "bin")
    return " ".join(b for b in (p.body() for p in ps) if b)

def square_text(U, V, s=1):
    """U^2 + 2 s U V + V^2."""
    U2, V2 = U.power(2), V.power(2)
    return gen.written((U2.k, U2.body()), (2 * s * U.k * V.k, product_body(U, V)), (V2.k, V2.body()))

def difference_text(U, V):
    U2, V2 = U.power(2), V.power(2)
    return gen.written((U2.k, U2.body()), (-V2.k, V2.body()))

def sum_text(U, V, s=1):
    """Like terms combined: (x + 3) + 7 is x + 10."""
    out = {}
    for c, b in U.terms() + V.terms(s):
        out[b] = out.get(b, 0) + c
    return gen.written(*[(c, b) for b, c in out.items()])

def irreducible(text):
    """Nothing to factor out and no factors over the integers."""
    c, fs = sp.factor_list(sp.expand(to_sympy(text)))
    return abs(c) == 1 and len(fs) == 1 and fs[0][1] == 1
