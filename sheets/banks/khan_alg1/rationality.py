"""Rational or irrational, decided by computing: shared by Lessons 15-1 and
15-2. (Not a bank.)

    value(text)     a number written in Typst math as sympy, exactly: decimals,
                    repeating decimals (0.overline(151)), mixed numbers (6 1/2),
                    fractions, square roots, pi
    rational(text)  is it rational? (its exact value is a fraction)
"""
import re
from fractions import Fraction as F
import sympy as sp
from ...check import to_sympy

REPEAT = re.compile(r"(-?)(\d*)\.(\d*)overline\((\d+)\)")
MIXED = re.compile(r"(?<![\w.)])(\d+) (\d+)/(\d+)")

def repeating(sign, whole, fixed, cycle):
    """-0.3overline(2) -> the fraction it equals."""
    q = F(int(whole or 0)) + (F(int(fixed), 10 ** len(fixed)) if fixed else 0) + \
        F(int(cycle), (10 ** len(cycle) - 1) * 10 ** len(fixed))
    return f"({'-' if sign else ''}{q.numerator}/{q.denominator})"

def value(text):
    t = REPEAT.sub(lambda m: repeating(*m.groups()), text)
    t = MIXED.sub(lambda m: f"({m.group(1)} + {m.group(2)}/{m.group(3)})", t)
    return sp.simplify(sp.nsimplify(to_sympy(t.replace("dot", "*")), rational=True))     # decimals exactly

def rational(text):
    return bool(value(text).is_Rational)
