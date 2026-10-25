"""sympy -> Typst math, the way the key writes it.

    tx(e, order)   an expression as Typst math. A product with a denominator is
                   one fraction, (3 x)/(4 y^2), so exponents are positive;
                   a sum's terms go by descending degree, letters in `order`
                   first (then alphabetical); a product reads
                   coefficient, radicals, pi, letters, i: 3 sqrt(2) x y^2.
    single(e, order)  e as one fraction over a common denominator
    fr(n, d)       a fraction from two Typst strings, parenthesized as needed
    display(t)     $display(t)$, so every fraction is full size
    text(t)        Typst math for the terminal

Typst reads xy as one name, so letters are always separated by spaces, and
to_sympy (sheets/check.py) reads every tx() back as the same expression:
tests/test_typmath.py checks that for each shape the banks use.
"""
import re
import sympy as sp

ATOM = re.compile(r"-?(\w+(\^\w+)?|sqrt\(\w+\))")        # 3, x, x^2: needs no parentheses in a fraction

def paren(t):
    return t if ATOM.fullmatch(t) else f"({t})"

def fr(n, d):
    """n over d: "(x + 1)/(2 y)", "x^2/y"."""
    return f"{paren(n)}/{paren(d)}"

def display(t):
    return f"$display({t})$"

def text(t):
    """Typst math for the terminal: minus signs, and <= as ≤."""
    t = t.replace("<=", "≤").replace(">=", "≥").replace(" - ", " − ")
    return re.sub(r"(^|[\s(])-", r"\1−", t)

class Printer:
    def __init__(self, order=()):
        self.order = [str(s) for s in order]

    def rank(self, sym):
        name = str(sym)
        return (self.order.index(name), "") if name in self.order else (len(self.order), name)

    def letters(self, e):
        return sorted(e.free_symbols, key=self.rank)

    # -- sums ------------------------------------------------------
    def degree(self, term, sym):
        d = term.as_powers_dict().get(sym, 0)
        if d == 0:
            return 0
        return float(d) if d.is_number else 1000.0       # a letter exponent outranks a number

    def terms(self, e):
        """e's terms in the key's order: descending degree, letter by letter; i last."""
        syms = self.letters(e)
        args = list(sp.Add.make_args(e))
        return sorted(args, key=lambda t: (tuple(-self.degree(t, s) for s in syms), t.has(sp.I)))

    def add(self, e):
        out = ""
        for i, t in enumerate(self.terms(e)):
            neg = t.could_extract_minus_sign()
            body = self.expr(-t if neg else t)
            out += ("-" + body if neg else body) if i == 0 else (" - " if neg else " + ") + body
        return out

    # -- products --------------------------------------------------
    def factor_rank(self, f):
        b = f.base if f.is_Pow else f
        if b.is_Integer:                       # sqrt(2)
            return (0, 0, "")
        if b == sp.pi:
            return (1, 0, "")
        if b == sp.I:
            return (4, 0, "")
        if b.is_Symbol:
            return (2,) + self.rank(b)
        return (3, 0, str(f))                  # (x + 1), sin(x)

    def product(self, e):
        """A product with no denominator: "3 sqrt(2) x y^2", "-x (x + 1)"."""
        c, rest = e.as_coeff_Mul()
        fs = sorted(sp.Mul.make_args(rest), key=self.factor_rank) if rest != 1 else []
        body = [paren(self.expr(f)) if f.is_Add else self.expr(f) for f in fs]
        neg = c < 0
        c = abs(c)
        if c != 1 or not body:
            body.insert(0, self.number(c))
        return ("-" if neg else "") + " ".join(body)

    def mul(self, e):
        num, den = sp.fraction(e)
        if den == 1:
            return self.product(e)
        neg = num.could_extract_minus_sign()
        n, d = self.expr(-num if neg else num), self.expr(den)
        return ("-" if neg else "") + fr(n, d)

    # -- the rest --------------------------------------------------
    def number(self, c):
        if c.is_Integer:
            return str(c)
        if c.is_Rational:
            return ("-" if c < 0 else "") + f"{abs(c.p)}/{c.q}"
        return format(float(c), "g")

    def power(self, e):
        b, x = e.as_base_exp()
        if x.is_negative or (x.is_Mul and x.could_extract_minus_sign()):
            return self.mul(e)
        if x == sp.Rational(1, 2):
            return f"sqrt({self.expr(b)})"
        base = self.expr(b)
        if not (b.is_Symbol or (b.is_Integer and b > 0)):
            base = f"({base})"
        ex = self.expr(x)
        return f"{base}^{ex}" if x.is_Integer else f"{base}^({ex})"

    def expr(self, e):
        e = sp.sympify(e)
        if e == sp.I:
            return "i"
        if e == sp.pi:
            return "pi"
        if e.is_Symbol:
            return str(e).replace("L_", "ell")
        if e.is_Number:
            return self.number(e)
        if e.is_Add:
            return self.add(e)
        if e.is_Mul:
            return self.mul(e)
        if e.is_Pow:
            return self.power(e)
        if isinstance(e, sp.Abs):
            return f"abs({self.expr(e.args[0])})"
        if isinstance(e, (sp.sin, sp.cos, sp.tan, sp.log)):
            return f"{type(e).__name__}({self.expr(e.args[0])})"
        raise ValueError(f"tx can't write {e!r}")

def tx(e, order=()):
    return Printer(order).expr(e)

def single(e, order=()):
    """e as one fraction over a common denominator: (3 + 2 sqrt(2))/7."""
    n, d = sp.fraction(sp.together(e))
    p = Printer(order)
    if d == 1:
        return p.expr(n)
    lead = p.terms(n)[0] if n.is_Add else n
    neg = lead.could_extract_minus_sign()             # -(x + 1)/(2 x), not (-x - 1)/(2 x)
    n = sp.expand(-n) if neg else n
    return ("-" if neg else "") + fr(p.expr(n), p.expr(d))
