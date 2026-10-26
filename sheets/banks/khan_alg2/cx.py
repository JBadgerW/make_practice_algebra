"""Complex numbers for Khan Algebra 2, Unit 2: a + b i written, read back.

    number(r, lo, hi, places)   a nonzero real, as a Decimal: 12, -3.75
    written(a, b, imaginary_first=False)
                     Typst: "6 - 3 i", "-4 i", "i", "7", "14 i + 12.1"
    value(text)      the number, exact (decimals as fractions), i the imaginary unit
    parts(text)      (real part, imaginary part), exact
    standard(text)   written a + b i: the real part first, no zero part, no 1 before i
    answer_of(prompt), check(p)   for a bank whose answer is the prompt worked out,
                     as a + b i (2-6 to 2-8); a product may be written with dot
"""
import re
from decimal import Decimal
import sympy as sp
from ...check import to_sympy

def number(r, lo, hi, places=0):
    """A nonzero number from lo to hi, with up to `places` decimal places."""
    scale = 10 ** places
    while True:
        n = r.randint(lo * scale, hi * scale)
        if n:
            return (Decimal(n) / scale).normalize() + 0

def num(x):
    """A number as written: 12, -3.75 (no exponent, no trailing zeros)."""
    return format(Decimal(str(x)).normalize(), "f")

def imaginary(b):
    return "i" if b == 1 else "-i" if b == -1 else f"{num(b)} i"

def written(a, b, imaginary_first=False):
    """a + b i in Typst, as the key writes it."""
    if not b:
        return num(a)
    if not a:
        return imaginary(b)
    if imaginary_first:
        return f"{imaginary(b)} {'-' if a < 0 else '+'} {num(abs(a))}"
    return f"{num(a)} {'-' if b < 0 else '+'} {imaginary(abs(b))}"

def value(text):
    return sp.nsimplify(sp.expand(to_sympy(text.replace("dot", "*"), imaginary=True)), rational=True)

def parts(text):
    v = value(text)
    return sp.re(v), sp.im(v)

N = r"\d+(?:\.\d+)?"
STANDARD = re.compile(rf"-?({N})|-?(?:({N}) )?i|-?({N}) [+-] (?:({N}) )?i")

def standard(text):
    """a + b i as the key writes it: the real part first, a part only if it isn't zero,
    a plain i for 1 i."""
    m = STANDARD.fullmatch(text.strip())
    if not m:
        return False
    real, coef, real2, coef2 = m.groups()
    if any(c is not None and Decimal(c) in (0, 1) for c in (coef, coef2)):
        return False                                   # 0 i or 1 i
    return all(Decimal(a) != 0 for a in (real, real2) if a is not None) or text.strip() == "0"

def answer_of(prompt):
    return written(*parts(prompt))

def check(p):
    try:
        ok = value(p["answer"]) == value(p["prompt"]) and standard(p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

def plain(t):
    """For the terminal: minus signs, and dot as a centered dot."""
    from ...typmath import text
    return text(t).replace(" dot ", " · ")
