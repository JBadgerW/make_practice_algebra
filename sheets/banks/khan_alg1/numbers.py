"""Numbers for the Khan Algebra 1 banks: decimals that stay short, and
fractions with small denominators. (Not a bank: the library passes over it.)

Decimals are Decimal, so 0.1 + 0.2 is 0.3 and gen.coef writes them as
typed; fractions are Fraction."""
from decimal import Decimal as D
from fractions import Fraction as F
from ...gen import need

def decimal(r, hi, steps=("0.5", "0.25", "0.1"), signed=True, whole=False):
    """A multiple of one of the steps, up to hi, not 0; whole=False: not an integer."""
    step = D(r.choice(steps))
    n = step * r.randint(1, int(D(hi) / step))
    need(whole or n != int(n))
    return n * r.choice((-1, 1)) if signed else n

def places(d):
    """How many decimal places d needs: 2.50 -> 1."""
    d = D(d).normalize()
    return max(0, -d.as_tuple().exponent)

def short(*ds, most=2):
    """Every number has at most `most` decimal places."""
    need(all(places(d) <= most for d in ds))

def fraction(r, hi=9, dens=(2, 3, 4, 5), signed=True, whole=False):
    """n/q with q in dens and |n/q| <= hi, in lowest terms, not 0; whole=False: not an integer."""
    q = r.choice(dens)
    f = F(r.randint(1, hi * q), q)
    need(whole or f.denominator != 1)
    return f * r.choice((-1, 1)) if signed else f

def simple(*fs, most=6):
    """Every fraction's denominator is at most `most`."""
    need(all(F(f).denominator <= most for f in fs))
