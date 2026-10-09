"""Solving literal equations and writing answers in classroom form."""
import re
import sympy as sp
from ...check import to_sympy, side_diff, syms_of, holds
from .templates import Redraw, need, fr

def tname(sym):
    return str(sym).replace("L_", "ell")

def fmt_num(c):
    assert c.is_Integer, c
    return str(abs(int(c)))

def terms(poly, appear, rotate=True):
    """Split an expanded polynomial into (negative?, typst) terms: letters in the
    order they appear in the problem (new constants last), a positive term first."""
    out = []
    for t in sp.Add.make_args(sp.expand(poly)):
        c, rest = t.as_coeff_Mul()
        fs = [] if rest == 1 else sorted(rest.as_powers_dict().items(),
                                         key=lambda be: -1 if be[0] == sp.pi else appear.get(tname(be[0]), 99))
        body = [tname(b) if b != sp.pi else "pi" for b, _ in fs]
        body = [s if e == 1 else f"{s}^{e}" for s, (_, e) in zip(body, fs)]
        if abs(c) != 1 or not body:
            body.insert(0, fmt_num(c))
        first = min([appear.get(tname(b), 99) for b, _ in fs if b != sp.pi] or
                    [appear.get(fmt_num(c), 99)])           # a constant goes where it was written
        out.append((not fs, first, bool(c < 0), " ".join(body)))
    out.sort(key=lambda z: z[1])                    # stable: ties keep sympy order
    out = [(neg, s) for _, _, neg, s in out]
    pos = [i for i, (neg, _) in enumerate(out) if not neg]
    if rotate and out[0][0] and pos:                   # 5 - m, not -m + 5
        out.insert(0, out.pop(pos[0]))
    return out

def joined(ts):
    s = ""
    for i, (neg, body) in enumerate(ts):
        s += ("-" if neg else "") + body if i == 0 else (" - " if neg else " + ") + body
    return s

def poly_tx(p, appear, numeric=False):
    """(negative?, typst) for a polynomial, with a common letter factor pulled
    out: y (b + 8) rather than b y + 8 y. With numeric=True a plain number is
    pulled out too, 2 (ell + w); numerators keep 4 M - 2 rather than 2 (2 M - 1)."""
    rest = sp.factor_terms(p)
    c, rest = rest.as_coeff_Mul()
    parts = sp.Mul.make_args(rest)
    adds = [f for f in parts if f.is_Add]
    if len(sp.Add.make_args(p)) > 1 and len(adds) == 1 and (len(parts) > 1 or (numeric and abs(c) != 1)):
        (neg, mono), = terms(c * sp.Mul(*[f for f in parts if f is not adds[0]]), appear)
        return neg, f"{mono} ({joined(terms(adds[0], appear))})"
    ts = terms(p, appear)
    return ts[0] if len(ts) == 1 else (False, joined(ts))

def fmt(expr, appear):
    """sympy expression -> Typst, as a single fraction with tidy signs."""
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    num, den = sp.expand(num), sp.expand(den)
    # clear any leftover rational coefficients
    cs = [t.as_coeff_Mul()[0] for q in (num, den) for t in sp.Add.make_args(q)]
    l = sp.ilcm(1, 1, *[sp.Rational(c).q for c in cs])
    num, den = sp.expand(num * l), sp.expand(den * l)
    # fewest minus signs; on a tie, the denominator leads with a plus
    negs = lambda p: sum(1 for t in sp.Add.make_args(p) if t.as_coeff_Mul()[0] < 0)
    a, b = negs(num) + negs(den), negs(-num) + negs(-den)
    if b < a or (a == b and terms(den, appear, rotate=False)[0][0]):
        num, den = -num, -den
    nneg, ns = poly_tx(num, appear)
    if den == 1:
        return ("-" if nneg else "") + ns
    dneg, ds = poly_tx(den, appear, numeric=True)
    return ("-" if nneg != dneg else "") + fr(ns, ds)

def solve(prompt, target, root=False):
    """Answer (Typst) for target in prompt; root=True solves for target^2 first."""
    syms = syms_of(prompt)
    t = syms[target]
    e = side_diff(prompt)
    if root:
        W = sp.Symbol("W_")
        e = e.subs(t**2, W)
        need(t not in e.free_symbols)
        u = W
    else:
        u = t
    num = sp.expand(sp.numer(sp.together(e)))
    need(u in num.free_symbols)
    P = sp.Poly(num, u)
    need(P.degree() == 1)
    a, b = P.coeff_monomial(u), P.coeff_monomial(1)
    need(a != 0)
    appear = {}
    for m in re.finditer(r"[A-Za-z]\w*|\b\d+\b", prompt):
        appear.setdefault(m.group(), m.start())
    ans = fmt(-b / a, appear)
    if root:
        ans = f"sqrt({ans})"
    return ans

def make(prompt, target, typ):
    """Solve, check, and package one problem (raises Redraw if unusable)."""
    try:
        ans = solve(prompt, target, root=(typ == "B"))
        sol = to_sympy(ans)
        need(sol.free_symbols)                       # a literal answer, not a number
        need(syms_of(prompt)[target] not in sol.free_symbols)
        need(len(ans) <= 60)
        holds(prompt, prompt, target, ans, trials=4)
    except (Redraw, ZeroDivisionError, TypeError, ValueError, AssertionError, sp.PolynomialError):
        raise Redraw
    return dict(type=typ, prompt=prompt, target=target, answer=f"{target} = {ans}")
