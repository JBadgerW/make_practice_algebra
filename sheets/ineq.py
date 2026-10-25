"""One-variable linear inequalities, shared by the banks that solve them:
the solution set read from Typst text, the key's way of writing a set, and
comparing two sets.

    solution(text)   the set of values that make it true: "4 x + 4 <= 9 x + 8",
                     "2 x + 3 >= 7 or 2 x + 9 > 11", "-3 <= x < 7", "x = -3",
                     "no solution", "all real numbers" (and Khan's wordings of those two)
    written(s, v)    a set as the key writes it: "x > 5/6", "-3 <= x < 7",
                     "x <= -3 or x > 7", "x = -3", NONE, ALL
    same(a, b)       two sets are equal (probed at every boundary and between)
    typst(text)      Typst math for the page: "or" and "and" as words

Decimals are read exactly, so nothing is rounded.
"""
import re
from fractions import Fraction
import sympy as sp
from .linear import exact
from .typmath import tx

NONE, ALL = "no solution", "all real numbers"
WORDS = {"no solution": sp.S.EmptySet, "no solutions": sp.S.EmptySet, "there are no solutions": sp.S.EmptySet,
         "all real numbers": sp.S.Reals, "all values of x are solutions": sp.S.Reals}
REL = re.compile(r"\s*(<=|>=|<|>|=)\s*")
JOIN = re.compile(r"\s+(and|or)\s+", re.I)
OPS = {"<": sp.Lt, ">": sp.Gt, "<=": sp.Le, ">=": sp.Ge, "=": sp.Eq}

def normal(text):
    return (text.replace("≤", "<=").replace("≥", ">=").replace("−", "-")
            .replace("$", "").replace('"', "").strip())

def letter_of(text):
    syms = set()
    for bit in REL.split(JOIN.sub(" ; ", normal(text)).replace(";", " < ")):
        if bit.strip() and bit.strip() not in OPS:
            syms |= exact(bit).free_symbols
    if len(syms) != 1:
        raise ValueError("an inequality needs exactly one letter")
    return syms.pop()

def chain(part, v):
    """The set for one inequality, or a chain like -3 <= x < 7."""
    bits = REL.split(part.strip())
    if len(bits) not in (3, 5):
        raise ValueError("write one or two signs")
    exprs = [exact(e) for e in bits[0::2]]
    s = sp.S.Reals
    for i, op in enumerate(bits[1::2]):
        s &= linear_set(exprs[i] - exprs[i + 1], op, v)
    return s

def linear_set(e, op, v):
    """Where e op 0, for e = a v + b (directly: solveset is slow); any other e by solveset."""
    e = sp.expand(e)
    a, b = e.coeff(v, 1), e.coeff(v, 0)
    if sp.expand(e - a * v - b) != 0 or not (a.is_number and b.is_number):
        return sp.solveset(OPS[op](e, 0), v, sp.S.Reals)
    if a == 0:
        return sp.S.Reals if OPS[op](b, 0) == sp.true else sp.S.EmptySet
    root = -b / a
    if op == "=":
        return sp.FiniteSet(root)
    if a < 0:
        op = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}[op]
    return (sp.Interval(-sp.oo, root, right_open=op == "<") if op in ("<", "<=")
            else sp.Interval(root, sp.oo, left_open=op == ">"))

def solution(text, v=None):
    """The set of values of the text's letter that make it true; ValueError if unreadable."""
    t = normal(text)
    if t.lower() in WORDS:
        return WORDS[t.lower()]
    v = v or letter_of(t)
    parts = JOIN.split(t)
    s = chain(parts[0], v)
    for join, part in zip(parts[1::2], parts[2::2]):
        s = s | chain(part, v) if join.lower() == "or" else s & chain(part, v)
    return s

# ------------------------------------------------------------------
# Writing a set
# ------------------------------------------------------------------
def ray(i, v):
    """An interval with one infinite end: "x > 5/6", "x <= -3"."""
    if i.start == -sp.oo:
        return f"{v} {'<' if i.right_open else '<='} {tx(i.end)}"
    return f"{v} {'>' if i.left_open else '>='} {tx(i.start)}"

def piece(i, v):
    if isinstance(i, sp.FiniteSet):
        return " or ".join(f"{v} = {tx(a)}" for a in i)
    if i.start == -sp.oo or i.end == sp.oo:
        return ray(i, v)
    return f"{tx(i.start)} {'<' if i.left_open else '<='} {v} {'<' if i.right_open else '<='} {tx(i.end)}"

def written(s, v):
    """A set as the key writes it."""
    if s == sp.S.EmptySet:
        return NONE
    if s == sp.S.Reals:
        return ALL
    if isinstance(s, sp.Complement):                            # x != a: Khan writes x < a or x > a
        a = next(iter(s.args[1]))
        return f"{v} < {tx(a)} or {v} > {tx(a)}"
    pieces = sorted(s.args, key=lambda i: i.inf) if isinstance(s, sp.Union) else [s]
    return " or ".join(piece(i, v) for i in pieces)

# ------------------------------------------------------------------
# Comparing
# ------------------------------------------------------------------
def same(a, b):
    """Sets a and b (unions of intervals and points) are equal: they agree at
    every boundary of either, between them, and beyond them."""
    ends = sorted({Fraction(str(x)) for s in (a, b) for x in s.boundary if x.is_finite})
    if not ends:
        ends = [Fraction(0)]
    probes = ends + [(x + y) / 2 for x, y in zip(ends, ends[1:])] + [ends[0] - 1, ends[-1] + 1]
    at = lambda s, q: bool(s.contains(sp.Rational(q.numerator, q.denominator)))
    return all(at(a, q) == at(b, q) for q in probes)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def typst(text, upper=False):
    """Typst math for an inequality or answer: "or"/"and" as upright words."""
    t = text
    for w in ("or", "and"):
        word = w.upper() if upper else w
        t = re.sub(rf"\s+{w}\s+", f' quad "{word}" quad ' if upper else f' " {word} " ', t)
    return t
