"""Make practice worksheets, answer keys, and slide decks of literal equations,
drawn by type (the same Types 1-11 and Special Cases A-B as the lesson).

Each type has a set of templates that build a fresh equation from random
letters and numbers, plus a pool of real formulas sorted by type. Templates
only write the *equation*: the answer is solved by sympy, written out in
classroom form by fmt() below, and checked numerically before it is used.

Examples (run from this folder):
    python3 make_practice.py --mix 3:6 8:4 A:2 --versions 3 --seed 12
    python3 make_practice.py --mix all:2 --shuffle
    python3 make_practice.py --mix 1:10 --style formulas
    python3 make_practice.py --selftest 200        # stress-test every type
    python3 practice_tui.py                        # the same, interactively (vim keys)

--mix TYPE:COUNT ...  types are 1-11, A, B, or "all" (default all:2)
--versions N          N different versions (default 1)
--seed S              same seed -> same problems (default: random, printed)
--style               mixed (default), letters (made-up equations only),
                      or formulas (real formulas where the type has them)
--shuffle             interleave the types instead of grouping them
--out DIR, --name N   output folder (default ./practice) and file prefix
--no-compile          write .typ files only
"""
import argparse, json, math, random, re, shlex, shutil, subprocess, sys
import sympy as sp
from literal_common import HERE, TYPES, label, to_sympy, side_diff, syms_of, holds, \
    head, slhead, vars_

TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]

# ------------------------------------------------------------------
# Random pieces for templates
# ------------------------------------------------------------------
LOWER = list("abcdfghkmnpqrstuvwxyz")     # no e, i, j, l, o
UPPER = list("ABCDFGHKMNPQRSTVW")         # no E, I, L, O
ATOM = re.compile(r"^([A-Za-z]\w*(\^\d+)?|\d+)$")

def w(s):
    """Parenthesize s unless it is a single letter, power, or number."""
    return s if ATOM.match(s) else f"({s})"

def fr(n, d):
    return f"{w(n)}/{w(d)}"

def co(n, v):
    """Numeric coefficient times v, dropping a coefficient of 1."""
    return v if n == 1 else f"{n} {v}"

class D:
    """One problem's worth of random choices; letters never repeat."""
    def __init__(self, rng):
        self.r, self.used = rng, set()
    def _fresh(self, pool):
        c = self.r.choice([c for c in pool if c.lower() not in self.used])
        self.used.add(c.lower())
        return c
    def v(self):                     # a fresh lowercase letter
        return self._fresh(LOWER)
    x = v                            # the unknown
    def S(self):                     # a "subject" like the y in y = ...
        return self._fresh(UPPER if self.r.random() < 0.5 else LOWER)
    def n(self, lo=2, hi=9):
        return self.r.randint(lo, hi)
    def ch(self, p=0.5):
        return self.r.random() < p
    def pm(self):
        return self.r.choice("+-")
    def pick(self, *opts):
        return self.r.choice(opts)
    def const(self, p=0.5):          # number or letter, as a term on its own
        return str(self.n(2, 15)) if self.ch(p) else self.v()
    def coef(self, p=0.4):           # number (>= 2) or letter, multiplying something
        return str(self.n()) if self.ch(p) else self.v()
    def prod(self):                  # a richer coefficient: 2 pi, a b, 3 a, a^2, ...
        return self.pick(lambda: self.coef(), lambda: f"{self.v()} {self.v()}",
                         lambda: f"{self.n()} {self.v()}", lambda: "pi",
                         lambda: f"{self.n(2, 4)} pi", lambda: f"pi {self.v()}",
                         lambda: f"{self.v()}^2")()
    def frac(self):                  # p/q in lowest terms, p != q
        while True:
            p, q = self.n(1, 7), self.n(2, 9)
            if p != q and math.gcd(p, q) == 1:
                return p, q

def lettered(*cs):
    return any(not c.isdigit() for c in cs)

class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

# ------------------------------------------------------------------
# Templates: each takes a D and returns (equation, unknown).
# Every one is built so it needs exactly its type's moves.
# ------------------------------------------------------------------
def T(*fs):
    return list(fs)

def t1_add(d):
    x, S, k = d.x(), d.S(), d.const()
    return d.pick(f"{S} = {x} {d.pm()} {k}", f"{S} = {k} + {x}"), x
def t1_mul(d):
    x, S, c = d.x(), d.S(), d.prod()
    return d.pick(f"{S} = {c} {x}", f"{S} = {x} {c}" if ATOM.match(c) else f"{S} = {c} {x}"), x
def t1_div(d):
    x, S, c = d.x(), d.S(), d.coef()
    return f"{S} = {fr(x, c)}", x
def t2_a(d):
    x, S, c, k = d.x(), d.S(), d.coef(), d.const()
    return d.pick(f"{S} = {c} {x} {d.pm()} {k}", f"{S} = {k} + {c} {x}"), x
def t2_b(d):
    x, c, k, k2 = d.x(), d.coef(), d.const(), d.const()
    need(lettered(c, k, k2))
    return f"{c} {x} {d.pm()} {k} = {k2}", x
def t2_c(d):
    x, S, a, b, c = d.x(), d.S(), d.v(), d.v(), d.coef()
    return d.pick(f"{a} {b} + {c} {x} = {S}", f"{c} {x} + {a} {b} = {S}"), x
def t2_d(d):
    x, S, c, k1, k2 = d.x(), d.S(), d.coef(), d.const(), d.v()
    return f"{S} = {c} {x} + {k1} {d.pm()} {k2}", x

def t3_frac_coef(d):
    x, S, n = d.x(), d.S(), d.n(2, 5)
    return f"{S} = 1/{n} {d.v() + ' ' if d.ch(0.7) else ''}{x}", x
def t3_over(d):
    x, S, c, k = d.x(), d.S(), d.coef(), d.const()
    return f"{S} = {fr(f'{x} {d.pm()} {k}', c)}", x
def t3_in_denom(d):
    x, S = d.x(), d.S()
    top = d.pick(f"{d.v()} {d.v()}", d.v(), f"{d.n()} {d.v()}")
    return f"{S} = {fr(top, x)}", x
def t3_pq(d):
    x, S, k = d.x(), d.S(), d.const()
    p, q = d.frac()
    return f"{S} = {p}/{q} {x} {d.pm()} {k}", x
def t3_linear_over(d):
    x, S, c, k, dd = d.x(), d.S(), d.coef(), d.const(), d.coef()
    return f"{S} = {fr(f'{c} {x} {d.pm()} {k}', dd)}", x
def t3_part_over(d):
    x, S, c, k = d.x(), d.S(), d.coef(), d.const()
    return f"{fr(x, c)} {d.pm()} {k} = {S}", x

def t4_a(d):
    x, S, c, k = d.x(), d.S(), d.coef(), d.const()
    return d.pick(f"{S} = {c}({x} {d.pm()} {k})", f"{S} = {c}({k} + {x})"), x
def t4_b(d):
    x, S, k, c, k2 = d.x(), d.S(), d.const(), d.coef(), d.const()
    return f"{S} {d.pm()} {k} = {c}({x} {d.pm()} {k2})", x
def t4_c(d):
    x, S, k, c, n = d.x(), d.S(), d.v(), d.v(), d.n(1, 3)
    return f"{S} = {k} + ({x} {d.pm()} {n}) {c}", x
def t4_d(d):
    x, k, c, m, u = d.x(), d.const(), d.coef(), d.n(2, 9), d.v()
    return f"{c}({k} {d.pm()} {co(d.n(2, 5), x)}) = {m} {u}", x
def t4_both(d):
    x, u, n1, n2, p, q = d.x(), d.v(), d.n(2, 9), d.n(2, 9), d.n(1, 4), d.n(1, 4)
    need(n1 != n2)
    return d.pick(f"{n1}({x} + {co(p, u)}) = {n2}({co(q, u)} - {x})",
                  f"{n1}({x} - {co(p, u)}) = {n2}({x} + {co(q, u)})",
                  f"{n1}({co(p, u)} + {x}) = {n2}({x} - {co(q, u)})"), x

def t5_pq(d):
    x, S, k = d.x(), d.S(), d.const()
    p, q = d.frac()
    return f"{S} = {p}/{q} ({x} {d.pm()} {k})", x
def t5_half(d):
    x, S, h, b, n = d.x(), d.S(), d.v(), d.const(), d.n(2, 4)
    return f"{S} = 1/{n} {h}({x} + {b})", x
def t5_over(d):
    x, S, c, k, dd = d.x(), d.S(), d.coef(), d.const(), d.coef()
    return f"{S} = {fr(f'{c}({x} {d.pm()} {k})', dd)}", x

def t6_prop(d):
    a, b, c, dd = d.v(), d.v(), d.v(), d.v()
    if d.ch(0.4):                      # one slot a number
        i = d.n(0, 3); s = [a, b, c, dd]; s[i] = str(d.n(2, 9)); a, b, c, dd = s
    x = d.pick(*[s for s in (a, b, c, dd) if not s.isdigit()])
    return f"{fr(a, b)} = {fr(c, dd)}", x
def t6_sum(d):
    x, u, a, b, k = d.x(), d.v(), d.coef(), d.coef(), d.const()
    need(lettered(a, b, k))
    return d.pick(f"{fr(x, a)} + {fr(u, b)} = {k}", f"{fr(u, a)} + {fr(x, b)} = {k}",
                  f"{fr(x, a)} - {fr(u, b)} = {k}"), x
def t6_sum2(d):
    x, u, a, b, k = d.x(), d.v(), d.v(), d.coef(), d.const()
    return f"{fr(u, a)} = {fr(x, b)} + {k}", x

def t7_two(d):
    x, S, a, b = d.x(), d.S(), d.coef(), d.coef()
    need(lettered(a, b) and a != b)
    return f"{a} {x} {d.pm()} {b} {x} = {S}", x
def t7_interest(d):
    x, S, c, dd = d.x(), d.S(), d.v(), d.v()
    return d.pick(f"{S} = {x} + {x} {c} {dd}", f"{S} = {x} + {c} {x}", f"{S} = {x} - {c} {x}"), x
def t7_three(d):
    x, S, a, b, c = d.x(), d.S(), d.v(), d.v(), d.coef()
    return f"{S} = {a} {x} + {b} {x} + {c} {x}", x

def t8_a(d):
    x, c1, c2, k = d.x(), d.coef(), d.coef(), d.const()
    need(lettered(c1, c2) and c1 != c2)
    return f"{c1} {x} = {c2} {x} {d.pm()} {k}", x
def t8_b(d):
    x, a, b, c, dd = d.x(), d.coef(), d.const(), d.coef(), d.const()
    need(lettered(a, c) and a != c)
    return f"{a} {x} {d.pm()} {b} = {c} {x} {d.pm()} {dd}", x
def t8_c(d):
    x, k, n1, n2 = d.x(), d.v(), d.n(2, 7), d.n(2, 5)
    n3 = d.n(n1 + 1, 12)
    return f"{n1} {x} + {n2} {k} = {n3} {x} - {k} {x}", x
def t8_d(d):
    x, a, n1, n2, k = d.x(), d.v(), d.n(2, 9), d.n(2, 9), d.const()
    return f"{n1} {x} - {n2} {a} = {a} {x} + {k}", x
def t8_e(d):
    x, S, a, b, c = d.x(), d.S(), d.coef(), d.const(), d.coef()
    need(lettered(a, c))
    return f"{a} {x} + {b} = {S} - {c} {x}", x

def t9_a(d):
    x, a, k, n, b = d.x(), d.v(), d.const(), d.coef(), d.const()
    return f"{a}({x} {d.pm()} {k}) = {n} {x} {d.pm()} {b}", x
def t9_b(d):
    x, n, a, k, b, j = d.x(), d.n(2, 6), d.v(), d.const(), d.v(), d.const()
    return f"{n}({a} {x} {d.pm()} {k}) = {b} {x} {d.pm()} {j}", x
def t9_box(d):
    x, S, u, v, n = d.x(), d.S(), d.v(), d.v(), d.n(2, 4)
    return f"{S} = {n}({u} {v} + {v} {x} + {u} {x})", x
def t9_both(d):
    x, a, b, c, dd = d.x(), d.v(), d.const(), d.v(), d.const()
    return f"{a}({x} + {b}) = {c}({x} - {dd})", x
def t9_mixed(d):
    x, S, a, b, c = d.x(), d.S(), d.v(), d.v(), d.const()
    return f"{S} = {a} {x} + {b}({x} {d.pm()} {c})", x

def t10_cross(d):
    x, a, b, c, dd = d.x(), d.const(), d.coef(), d.const(), d.coef()
    need(lettered(b, dd) and b != dd)
    return f"{fr(f'{x} {d.pm()} {a}', b)} = {fr(f'{x} {d.pm()} {c}', dd)}", x
def t10_harmonic(d):
    a, b, c = d.v(), d.v(), d.v()
    return f"1/{a} + 1/{b} = 1/{c}", d.pick(a, b, c)
def t10_split(d):
    x, S, a, b = d.x(), d.S(), d.coef(), d.coef()
    need(lettered(a, b) and a != b)
    return f"{S} = {fr(x, a)} + {fr(x, b)}", x
def t10_sides(d):
    x, a, b, c = d.x(), d.coef(), d.const(), d.coef()
    need(lettered(a, c) and a != c)
    return f"{fr(x, a)} + {b} = {fr(x, c)}", x
def t10_energy(d):
    x, S, a, b, c, n = d.x(), d.S(), d.v(), d.v(), d.v(), d.n(2, 3)
    return f"{S} = 1/{n} {x} {a}^2 + {x} {b} {c}", x

def t11_a(d):
    x, S, a, b = d.x(), d.S(), d.const(), d.const()
    need(lettered(a, b))
    return f"{S} = {fr(a, d.pick(f'{x} + {b}', f'{b} + {x}', f'{x} - {b}'))}", x
def t11_b(d):
    x, S, n1, n2, n3 = d.x(), d.S(), d.coef(0.8), d.const(0.8), d.const(0.8)
    return f"{S} = {fr(f'{n1} {x} {d.pm()} {n2}', f'{x} {d.pm()} {n3}')}", x
def t11_c(d):
    x, S, c = d.x(), d.S(), d.v()
    return f"{S} = {fr(f'{x} + {c}', f'{x} - {c}')}", x
def t11_d(d):
    x, S, a, b = d.x(), d.S(), d.coef(), d.const()
    return f"{S} = {fr(f'{a} {x}', f'{x} + {b}')}", x
def t11_e(d):
    x, S, a, b, c = d.x(), d.S(), d.const(), d.const(), d.coef()
    return f"{S} = {fr(a, f'{b} + {c} {x}')}", x

def tA_a(d):
    x, S, k = d.x(), d.S(), d.const()
    return d.pick(f"{k} - {x} = {S}", f"{S} = {k} - {x}"), x
def tA_b(d):
    x, u, c1, c2, k = d.x(), d.v(), d.coef(), d.coef(), d.const()
    return f"{c1} {u} - {c2} {x} = {k}", x
def tA_c(d):
    x, S, k, c = d.x(), d.S(), d.const(), d.coef()
    return f"{S} = {k} - {c} {x}", x

def tB_a(d):
    x, S = d.x(), d.S()
    c = d.pick(lambda: d.prod(), lambda: f"1/{d.n(2, 4)} {d.v()}", lambda: f"1/{d.n(2, 4)} pi {d.v()}")()
    return f"{S} = {c} {x}^2", x
def tB_b(d):
    x, S = d.x(), d.S()
    return f"{S} = {fr(d.pick(f'{d.v()} {d.v()}', f'{d.v()} {d.v()} {d.v()}', d.v()), f'{x}^2')}", x
def tB_c(d):
    x, S, k = d.x(), d.S(), d.const()
    return f"{S} = {x}^2 {d.pm()} {k}", x

TEMPLATES = {
    "1": T(t1_add, t1_mul, t1_div),
    "2": T(t2_a, t2_b, t2_c, t2_d),
    "3": T(t3_frac_coef, t3_over, t3_in_denom, t3_pq, t3_linear_over, t3_part_over),
    "4": T(t4_a, t4_b, t4_c, t4_d, t4_both),
    "5": T(t5_pq, t5_half, t5_over),
    "6": T(t6_prop, t6_sum, t6_sum2),
    "7": T(t7_two, t7_interest, t7_three),
    "8": T(t8_a, t8_b, t8_c, t8_d, t8_e),
    "9": T(t9_a, t9_b, t9_box, t9_both, t9_mixed),
    "10": T(t10_cross, t10_harmonic, t10_split, t10_sides, t10_energy),
    "11": T(t11_a, t11_b, t11_c, t11_d, t11_e),
    "A": T(tA_a, tA_b, tA_c),
    "B": T(tB_a, tB_b, tB_c),
}

# Real formulas: (equation, unknown, type). Add more freely; each is solved
# and checked like a generated problem.
FORMULAS = [
    ("d = r t", "r", "1"), ("d = r t", "t", "1"), ("I = p r t", "p", "1"), ("I = p r t", "r", "1"),
    ("V = ell w h", "w", "1"), ("C = 2 pi r", "r", "1"), ("F = m a", "m", "1"), ("W = F d", "d", "1"),
    ("P = W/t", "W", "1"), ("D = m/V", "m", "1"), ("p = m v", "v", "1"), ("V = I R", "R", "1"),
    ("P = I^2 R", "R", "1"), ("P_1 V_1 = P_2 V_2", "V_2", "1"), ("V = pi r^2 h", "h", "1"),
    ("y = m x + b", "b", "1"), ("A = P(1 + r t)", "P", "1"),
    ("y - y_1 = m(x - x_1)", "m", "1"),
    ("P = 2 ell + 2 w", "ell", "2"), ("y = m x + b", "x", "2"),
    ("y = m x + b", "m", "2"), ("v = u + a t", "t", "2"), ("A x + B y = C", "y", "2"),
    ("A x + B y = C", "x", "2"), ("A = P + P r t", "r", "2"), ("v^2 = u^2 + 2 a s", "a", "2"),
    ("a_n = a_1 + (n - 1) d", "d", "2"), ("S = 2 pi r^2 + 2 pi r h", "h", "2"),
    ("A = 1/2 b h", "b", "3"), ("V = 1/3 B h", "h", "3"), ("F = 9/5 C + 32", "C", "3"),
    ("P = W/t", "t", "3"), ("D = m/V", "V", "3"), ("M = (a + b)/2", "a", "3"),
    ("K = 1/2 m v^2", "m", "3"), ("F = (G m_1 m_2)/r^2", "m_1", "3"),
    ("m = (y_2 - y_1)/(x_2 - x_1)", "y_2", "3"), ("d = v t + 1/2 a t^2", "a", "3"),
    ("V = 1/3 pi r^2 h", "h", "3"), ("A = 1/2 h(b_1 + b_2)", "h", "3"),
    ("E = 1/2 m v^2 + m g h", "h", "3"), ("P = F/A", "A", "3"),
    ("A = P(1 + r t)", "r", "4"), ("A = P(1 + r t)", "t", "4"), ("S = 180(n - 2)", "n", "4"),
    ("a_n = a_1 + (n - 1) d", "n", "4"), ("y - y_1 = m(x - x_1)", "x", "4"),
    ("q = m c(T_f - T_i)", "T_f", "4"),
    ("C = 5/9 (F - 32)", "F", "5"), ("A = 1/2 h(b_1 + b_2)", "b_1", "5"),
    ("S = (n(a + ell))/2", "ell", "5"), ("S = (n(a + ell))/2", "a", "5"),
    ("x/a + y/b = 1", "y", "6"), ("x/a + y/b = 1", "x", "6"),
    ("(P_1 V_1)/T_1 = (P_2 V_2)/T_2", "V_2", "6"), ("(P_1 V_1)/T_1 = (P_2 V_2)/T_2", "T_2", "6"),
    ("A = P + P r t", "P", "7"),
    ("S = 2 ell w + 2 ell h + 2 w h", "ell", "8"), ("S = 2 ell w + 2 ell h + 2 w h", "h", "8"),
    ("T = 2(ell w + w h + ell h)", "h", "9"), ("T = 2(ell w + w h + ell h)", "ell", "9"),
    ("1/f = 1/d_o + 1/d_i", "f", "10"), ("1/f = 1/d_o + 1/d_i", "d_o", "10"),
    ("1/R = 1/R_1 + 1/R_2", "R_1", "10"), ("1/R = 1/R_1 + 1/R_2", "R", "10"),
    ("E = 1/2 m v^2 + m g h", "m", "10"),
    ("R = (R_1 R_2)/(R_1 + R_2)", "R_1", "11"), ("I = E/(R + r)", "R", "11"),
    ("I = E/(R + r)", "r", "11"), ("m = (y_2 - y_1)/(x_2 - x_1)", "x_2", "11"),
    ("f = (d_o d_i)/(d_o + d_i)", "d_o", "11"),
    ("P = R - C", "C", "A"), ("a t = v - u", "u", "A"), ("A x - B y = C", "y", "A"),
    ("A = pi r^2", "r", "B"), ("V = pi r^2 h", "r", "B"), ("E = m c^2", "c", "B"),
    ("K = 1/2 m v^2", "v", "B"), ("F = (G m_1 m_2)/r^2", "r", "B"), ("P = I^2 R", "I", "B"),
    ("a^2 + b^2 = c^2", "a", "B"), ("a^2 + b^2 = c^2", "c", "B"), ("V = 1/3 pi r^2 h", "r", "B"),
    ("A = 4 pi r^2", "r", "B"), ("v^2 = u^2 + 2 a s", "v", "B"),
]

# ------------------------------------------------------------------
# Solving and writing answers in classroom form
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# Drawing a set of problems
# ------------------------------------------------------------------
def original_prompts():
    try:
        bank = json.loads((HERE / "lesson_1-4" / "lesson_1-4_literal_seq_bank.json").read_text())
        return {(p["prompt"], p["target"]) for p in bank["problems"]}
    except (OSError, ValueError, KeyError):
        return set()

def draw(typ, rng, style, seen, tries=400):
    pool = [f for f in FORMULAS if f[2] == typ and (f[0], f[1]) not in seen]
    use_formula = pool and (style == "formulas" or (style == "mixed" and rng.random() < 0.3))
    if use_formula:
        p, t, _ = rng.choice(pool)
        prob = make(p, t, typ)
    else:
        for _ in range(tries):
            d = D(rng)
            try:
                p, t = rng.choice(TEMPLATES[typ])(d)
                if rng.random() < 0.35:              # write the sides the other way round
                    l, r = p.split(" = ")
                    p = f"{r} = {l}"
                if (p, t) in seen:
                    continue
                prob = make(p, t, typ)
                break
            except Redraw:
                continue
        else:
            raise RuntimeError(f"could not draw a Type {typ} problem; check its templates")
    seen.add((prob["prompt"], prob["target"]))
    prob["source"] = "formula" if use_formula else "template"
    return prob

# ------------------------------------------------------------------
# Typst output
# ------------------------------------------------------------------
def problem_tx(p):
    return f"$display({p['prompt']})$; #h(0.3em) ${p['target']}$"

def worksheet(probs, version, key, grouped, title, cmd, class_name="Algebra 1"):
    s = f"// Generated by: {cmd}\n" + head + vars_(title + (" — Answer Key" if key else ""), version, class_name)
    s += """#let type-head(lbl, title) = block(sticky: true, above: 1.1em, below: 0.6em,
  text(weight: "bold", size: 12.5pt)[#lbl: #title])

#first-page-header(class-name, worksheet-title, version: version)
#v(-2.2em)
Solve each equation for the indicated variable.
#v(0.2em)

"""
    groups = [[p for p in probs if p["type"] == k] for k in KEYS] if grouped else [probs]
    n = 0
    for g in groups:
        if not g:
            continue
        if grouped:
            ty = TYPE[g[0]["type"]]
            s += f'#type-head([{label(ty)}], [{ty["title"]}])\n'
        s += "#grid(\n  columns: (1fr, 1fr),\n  column-gutter: 1em,\n"
        for p in g:
            n += 1
            a = f"\n    #v(0.3em) #h(1fr) #text(fill: red)[$display({p['answer']})$] #h(0.4em)" if key else ""
            s += (f"  block(height: {TYPE[p['type']]['space']}in, question(renum: {n}, space-below: 0em)[\n"
                  f"    {problem_tx(p)}{a}\n  ]),\n")
        s += ")\n\n"
    return s

def slides(probs, version, grouped, title, cmd, class_name="Algebra 1"):
    s = f"// Generated by: {cmd}\n" + slhead + vars_(title, version, class_name) + f"""
#let slide(n, prob, answer: none) = {{
  align(left)[#text(size: 30pt, weight: "bold")[Problem #n]]
  v(1.5em)
  align(center)[
    #text(size: 34pt)[#prob]
    #if answer != none [
      #v(0.8em)
      #text(fill: red, size: 34pt)[#answer]
    ]
  ]
}}

#let type-slide(lbl, title, look, move) = align(horizon)[
  #text(size: 24pt, fill: luma(90))[#lbl]
  #v(-0.3em)
  #text(size: 40pt, weight: "bold")[#title]
  #v(0.6em)
  #text(size: 24pt)[*Look for:* #look]
  #v(0.2em)
  #text(size: 24pt)[*The move:* #move]
]

#align(center + horizon)[
  #text(size: 44pt, weight: "bold")[{title}]
  #v(0.4em)
  #text(size: 28pt)[Version {version}]
  #v(0.2em)
  #text(size: 24pt)[Solve each equation for the indicated variable.]
]
"""
    last = None
    for n, p in enumerate(probs, 1):
        if grouped and p["type"] != last:
            ty = TYPE[p["type"]]
            s += f'#pagebreak()\n#type-slide([{label(ty)}], [{ty["title"]}], [{ty["look"]}], [{ty["move"]}])\n'
            last = p["type"]
        pr = f"$display({p['prompt']})$; #h(0.5em) ${p['target']}$"
        s += f"#pagebreak()\n#slide({n}, [{pr}])\n"
        s += f"#pagebreak()\n#slide({n}, [{pr}], answer: [$display({p['answer']})$])\n"
    return s

# ------------------------------------------------------------------
# API (used by the command line below and by practice_tui.py)
# ------------------------------------------------------------------
DEFAULTS = dict(versions=1, style="mixed", shuffle=False, title="Literal Equations Practice",
                class_name="Algebra 1",
                out="practice", name="literal_practice")
STYLES = ("mixed", "letters", "formulas")

def parse_mix(tokens):
    """["3:6", "A:2", "all:1"] -> {"3": 7, "A": 3, ...}; raises ValueError."""
    mix = {}
    for tok in tokens:
        k, _, c = tok.partition(":")
        k = k.upper() if k.lower() in ("a", "b") else k.lower()
        if not c.isdigit() or (k not in KEYS and k != "all"):
            raise ValueError(f"bad mix entry {tok!r}: use TYPE:COUNT with TYPE in {', '.join(KEYS)} or all")
        for key in (KEYS if k == "all" else [k]):
            mix[key] = mix.get(key, 0) + int(c)
    return mix

def command_for(mix, versions, seed, style="mixed", shuffle=False, title=DEFAULTS["title"],
                out=DEFAULTS["out"], name=DEFAULTS["name"], class_name=DEFAULTS["class_name"]):
    """The make_practice.py command line that reproduces a set exactly."""
    c = ["python3 make_practice.py", "--mix", *[f"{k}:{n}" for k, n in mix.items() if n],
         "--versions", str(versions), "--seed", str(seed)]
    if style != "mixed":
        c += ["--style", style]
    if shuffle:
        c.append("--shuffle")
    for opt, val in (("title", title), ("out", out), ("name", name), ("class_name", class_name)):
        if val != DEFAULTS[opt]:
            c += [f"--{'class' if opt == 'class_name' else opt}", shlex.quote(val)]
    return " ".join(c)

def draw_versions(mix, versions, seed, style="mixed", shuffle=False):
    """The problem lists for each version. Depends only on these arguments."""
    random.seed(seed)                     # the numeric checks
    rng = random.Random(seed)
    seen = original_prompts()             # don't repeat the lesson's own 50
    sets = []
    for _ in range(versions):
        probs = [draw(k, rng, style, seen) for k in KEYS for _ in range(mix.get(k, 0))]
        if shuffle:
            rng.shuffle(probs)
        sets.append(probs)
    return sets

def build(mix, versions=1, seed=None, style="mixed", shuffle=False, title=DEFAULTS["title"],
          out=DEFAULTS["out"], name=DEFAULTS["name"], class_name=DEFAULTS["class_name"],
          compile=True, sets=None):
    """Write (and compile) worksheet, key, slides, and JSON for every version.
    Pass sets from draw_versions() with the same arguments to skip redrawing.
    Returns dict(seed, out, files, compiled, sets, command); raises RuntimeError."""
    if seed is None:
        seed = random.randrange(10**6)
    if not any(mix.values()):
        raise RuntimeError("no problems: every type has a count of 0")
    sets = sets or draw_versions(mix, versions, seed, style, shuffle)
    cmd = command_for(mix, versions, seed, style, shuffle, title, out, name, class_name)
    outp = HERE / out                     # an absolute out stays absolute
    outp.mkdir(parents=True, exist_ok=True)
    typst = shutil.which("typst") if compile else None
    written = []
    for v, probs in enumerate(sets, 1):
        base = f"{name}_v{v}"
        files = {f"{base}.typ": worksheet(probs, str(v), False, not shuffle, title, cmd, class_name),
                 f"{base}_key.typ": worksheet(probs, str(v), True, not shuffle, title, cmd, class_name),
                 f"{base}_slides.typ": slides(probs, str(v), not shuffle, title, cmd, class_name)}
        (outp / f"{base}.json").write_text(json.dumps(
            {"command": cmd, "seed": seed, "version": v, "problems": probs}, indent=1))
        for fname, text in files.items():
            (outp / fname).write_text(text)
            if typst:
                r = subprocess.run([typst, "compile", fname], cwd=outp, capture_output=True, text=True)
                if r.returncode:
                    raise RuntimeError(f"typst failed on {fname}:\n{r.stderr}")
            written.append(fname)
    return dict(seed=seed, out=outp, files=written, compiled=bool(typst), sets=sets, command=cmd)

def selftest(n, seed):
    random.seed(seed)
    rng, bad = random.Random(seed), 0
    for typ in KEYS:
        seen = set()
        for _ in range(n):
            draw(typ, rng, "letters", seen)
        print(f"{label(TYPE[typ]):16} {n} drawn, all verified")
    for p, t, typ in FORMULAS:
        try:
            make(p, t, typ)
        except Redraw:
            bad += 1
            print("formula failed:", p, t, typ)
    print(f"{len(FORMULAS) - bad}/{len(FORMULAS)} formulas verified")
    return bad == 0

# ------------------------------------------------------------------
# Command line
# ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mix", nargs="+", default=["all:2"], metavar="TYPE:COUNT")
    ap.add_argument("--versions", type=int, default=DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--style", choices=STYLES, default=DEFAULTS["style"])
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--title", default=DEFAULTS["title"])
    ap.add_argument("--out", default=DEFAULTS["out"])
    ap.add_argument("--name", default=DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", default=DEFAULTS["class_name"], metavar="NAME")
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--selftest", type=int, metavar="N")
    a = ap.parse_args()

    seed = a.seed if a.seed is not None else random.randrange(10**6)
    if a.selftest:
        sys.exit(0 if selftest(a.selftest, seed) else 1)
    try:
        r = build(parse_mix(a.mix), a.versions, seed, a.style, a.shuffle, a.title, a.out, a.name,
                  a.class_name, compile=not a.no_compile)
    except (ValueError, RuntimeError) as e:
        sys.exit(str(e))
    print(f"seed {seed}: {sum(len(s) for s in r['sets'][:1])} problems x {a.versions} version(s) -> {r['out']}")
    print("  " + "\n  ".join(r["files"]) + ("" if r["compiled"] else "\n  (not compiled)"))

if __name__ == "__main__":
    main()
