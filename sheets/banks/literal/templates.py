"""Templates that build fresh literal equations from random letters and numbers."""
import math, re

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
