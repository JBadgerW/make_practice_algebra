"""sympy -> Typst math, the way the key writes it.

    tx(e, order)   an expression as Typst math. A product with a denominator is
                   one fraction, (3 x)/(4 y^2), so exponents are positive;
                   a sum's terms go by descending degree, letters in `order`
                   first (then alphabetical); a product reads
                   coefficient, radicals, pi, letters, i: 3 sqrt(2) x y^2.
    single(e, order)  e as one fraction over a common denominator, multiplied out, minus in front
    fr(n, d)       a fraction from two Typst strings, parenthesized as needed
    display(t)     $display(t)$, so the outermost fraction is full size
    dfrac(t)       every fraction full size, nested ones too, but not in exponents
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
        return f"{base}^{ex}" if x.is_Integer or x.is_Symbol else f"{base}^({ex})"

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
    """e as one fraction over a common denominator, its numerator and
    denominator multiplied out, and any minus sign in front:
    (3 + 2 sqrt(2))/7, (x^3 + x y^4)/y^3, -(x + 1)/(2 x - 3)."""
    n, d = sp.fraction(sp.together(e))
    n, d = sp.expand(n), sp.expand(d)
    p = Printer(order)
    if d == 1:
        return p.expr(n)
    def leads_negative(x):
        return (p.terms(x)[0] if x.is_Add else x).could_extract_minus_sign()
    if leads_negative(d):                             # the denominator leads with a plus
        n, d = -n, -d
    neg = leads_negative(n)                           # -(x + 1)/(2 x), not (-x - 1)/(2 x)
    n = -n if neg else n
    return ("-" if neg else "") + fr(p.expr(n), p.expr(d))

# ------------------------------------------------------------------
# Display style for every fraction, not only the outermost one
# ------------------------------------------------------------------
TOKEN = re.compile(r"\s+|\d+(?:\.\d+)?|[A-Za-z]\w*|.")

def _group(toks, i):
    """The tokens of a parenthesized group starting at toks[i] == "(" -> (inner tokens, index after ")")."""
    depth, j = 0, i
    while True:
        depth += {"(": 1, ")": -1}.get(toks[j], 0)
        if depth == 0:
            return toks[i + 1:j], j + 1
        j += 1

def _items(toks):
    """Typst math tokens -> items: (kind, text), kind "atom" (with any ^ or _ attached), "space", or "op"."""
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t.isspace():
            out.append(("space", t)); i += 1; continue
        if t == "(":
            inner, i = _group(toks, i)
            text = "(" + _dfrac(inner) + ")"
        elif re.match(r"[A-Za-z]", t) and i + 1 < len(toks) and toks[i + 1] == "(":
            inner, i = _group(toks, i + 1)                          # sqrt(...), abs(...): a function's argument
            text = t + "(" + _dfrac(inner) + ")"
        elif re.match(r"\w", t):
            text, i = t, i + 1
        else:
            out.append(("op", t)); i += 1; continue
        while i < len(toks) and toks[i] in "^_":               # an exponent stays as written: no display there
            mark = toks[i]
            if i + 1 < len(toks) and toks[i + 1] == "(":
                inner, i = _group(toks, i + 1)
                text += mark + "(" + "".join(inner) + ")"
            else:
                text += mark + toks[i + 1]; i += 2
        out.append(("atom", text))
    return out

def _dfrac(toks):
    items = _items(toks)
    out = []                                   # items with fractions joined into display(a/b)
    i = 0
    while i < len(items):
        kind, text = items[i]
        if kind == "op" and text == "/" and out:
            j = len(out) - 1
            while j >= 0 and out[j][0] == "space":
                j -= 1
            k = i + 1
            while k < len(items) and items[k][0] == "space":
                k += 1
            if j >= 0 and out[j][0] == "atom" and k < len(items) and items[k][0] == "atom":
                left = out[j][1]
                del out[j:]
                out.append(("atom", f"display({left}/{items[k][1]})"))
                i = k + 1
                continue
        out.append((kind, text))
        i += 1
    return "".join(t for _, t in out)

def dfrac(t):
    """Typst math with every fraction in display style (full size, as \\dfrac),
    nested ones too, except in exponents: "(1/x + 2)/y" ->
    "display((display(1/x) + 2)/y)"; "x^(1/2)" stays as it is."""
    return _dfrac(TOKEN.findall(t))
