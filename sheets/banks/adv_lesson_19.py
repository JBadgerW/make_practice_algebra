"""Lesson 19 (Advanced Math): nonlinear systems, factoring exponentials, and
the sum and difference of two cubes. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_019/slides/deck_019.typ).

    1  a circle and a line:         x^2 + y^2 = 9;  y - x = 1
    2  a circle and a hyperbola:    x^2 + y^2 = 9;  2 x^2 - y^2 = -6
    3  a hyperbola and a line:      x y = -4;  y = -x - 2
    4  factoring exponentials:      3 x^(2 n + 2) + 12 x^(3 n + 3)
    5  simplify by factoring:       (x^(2 a) - y^(2 b))/(x^a + y^b)
    6  a sum or difference of cubes: x^3 y^3 - p^3,  8 m^3 y^6 + x^3

The key writes as the deck does. A system's answer is every real solution,
largest x first (then largest y), each coordinate a rational part and a
radical part, the radical simplified: (-1/2 + sqrt(17)/2, 1/2 + sqrt(17)/2)
"and" (-1/2 - sqrt(17)/2, 1/2 - sqrt(17)/2). A factored exponential takes out
the number and each letter's common power, piece by piece (x^n x^n x^2), so
4 x^(3 n + 2) - 6 x^(4 n + 1) is 2 x^(3 n + 1) (2 x - 3 x^n). A sum or
difference of cubes is (F ± S)(F^2 ∓ F S + S^2), with F S written F first:
(2 m y^2 + x)(4 m^2 y^4 - 2 m y^2 x + x^2).

Every system is built backward and its solutions worked out by the quadratic
formula. check() doesn't use that: it reads the points from the answer's
text, puts each into both equations exactly, and requires as many points as
sympy finds real solutions; each coordinate must be in simplest form (the
radicand has no square factor, fractions are in lowest terms). Types 4-6 are
checked by value at random points (the letters in the exponents too) and by
their form: Type 4's factor in parentheses has nothing common left, Type 5
has no fraction left, and Type 6's factors don't factor again.

A problem: dict(type, prompt, answer, source), in Typst math; a system's
prompt is its two equations separated by ";".
    prompt  "x y = -4; y = -x - 2"
    answer  '(-1 + sqrt(5), -1 - sqrt(5)) "and" (-1 - sqrt(5), -1 + sqrt(5))'
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need, signed, written
from ..check import to_sympy, same_value, simplest_form
from ..typmath import tx, display, dfrac, text as plain
from . import adv_factoring as AF

NAME = FAMILY = "adv_lesson_19"
FIXED = False
TITLE = "Lesson 19: Nonlinear systems, Factoring Exponentials, Sum and Difference of Two Cubes"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Lessons"}

SYSTEMS = ("1", "2", "3")
FRIENDLY = tuple("abcmnpqrstxyz")                               # letters for Types 4 and 6
BASES = (("x", "y"), ("x", "y"), ("p", "q"), ("m", "z"))        # Type 5: x^(2 a) - y^(2 b)
EXPONENTS = (("a", "b"), ("a", "b"), ("m", "n"), ("c", "d"))

TYPES = [
    dict(key="1", title="A Circle and a Line",
         look="x² + y² = r² and a line.",
         move="Solve the line for y and substitute into the circle. Solve the quadratic (often with the "
              "quadratic formula), then use the line to find each y.", space="2in", width="full"),
    dict(key="2", title="A Circle and a Hyperbola",
         look="x² + y² = r² and an equation with x² and y² of opposite signs.",
         move="Eliminate y² (scale an equation if you must) and solve for x². Then x = ± its square root; "
              "use the circle to find y. Up to four points.", space="2in", width="full"),
    dict(key="3", title="A Hyperbola and a Line",
         look="xy = k and a line.",
         move="Substitute the line's y into xy = k. Solve the quadratic, then use the line to find each y.",
         space="2in", width="full"),
    dict(key="4", title="Factoring Exponentials", instructions="Factor.",
         look="Terms with the same letter, its exponents written with another letter, like x²ⁿ⁺².",
         move="Rewrite each power in pieces: x²ⁿ⁺² = xⁿ · xⁿ · x². Take out the largest number and "
              "every piece the terms share."),
    dict(key="5", title="Simplify by Factoring the Numerator", instructions="Simplify.",
         look="A fraction whose top is a difference of two squares, like x²ᵃ − y²ᵇ, and whose "
              "bottom is the sum or the difference of their square roots.",
         move="Factor the top: A² − B² = (A + B)(A − B). Cancel the factor that matches the bottom."),
    dict(key="6", title="A Sum or Difference of Two Cubes", instructions="Factor.",
         look="Two cubes added or subtracted: the numbers are cubes and the exponents multiples of 3.",
         move="Find F and S, the cube roots. F³ + S³ = (F + S)(F² − FS + S²) and "
              "F³ − S³ = (F − S)(F² + FS + S²).", space="1.25in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

X, Y = sp.symbols("x y")

# ------------------------------------------------------------------
# Writing numbers: a rational part and a radical part, -1/2 + sqrt(17)/2
# ------------------------------------------------------------------
def rational(q):
    q = sp.Rational(q)
    return str(q.p) if q.q == 1 else f"{q.p}/{q.q}"

def radical(q, f):
    """|q| sqrt(f), q rational: sqrt(17)/2, (3 sqrt(17))/2, 2 sqrt(2)."""
    q = abs(sp.Rational(q))
    core = f"sqrt({f})" if q.p == 1 else f"{q.p} sqrt({f})"
    return core if q.q == 1 else (f"{core}/{q.q}" if q.p == 1 else f"({core})/{q.q}")

def number(e):
    """An exact p + q sqrt(f) as the key writes it."""
    e = sp.nsimplify(sp.expand(e))
    p, rest = e.as_coeff_Add()
    if rest == 0:
        return rational(p)
    q, root = rest.as_coeff_Mul()
    need(root.is_Pow and root.exp == sp.Rational(1, 2) and root.base.is_Integer)   # one square root
    r = radical(q, root.base)
    if p == 0:
        return ("-" if q < 0 else "") + r
    return f"{rational(p)} {'-' if q < 0 else '+'} {r}"

def nice(e, den=6, rad=60, size=20):
    """A coordinate a student can work out: small denominators, a small radicand."""
    e = sp.expand(e)
    p, rest = e.as_coeff_Add()
    q, root = rest.as_coeff_Mul() if rest != 0 else (sp.Integer(0), sp.Integer(1))
    f = root.base if root.is_Pow else 1
    return p.q <= den and q.q <= den and f <= rad and abs(p.p) <= size and abs(q.p) <= size

def points(sols):
    """The key's answer: largest x first, then largest y."""
    sols = sorted(sols, key=lambda s: (-float(s[0]), -float(s[1])))
    ps = [f"({number(a)}, {number(b)})" for a, b in sols]
    return ' "and" '.join(ps) if len(ps) == 2 else ", ".join(ps)

# ------------------------------------------------------------------
# Writing equations
# ------------------------------------------------------------------
def line(r, a, b, c):
    """a x + b y = c, written one of the ways the lesson writes a line."""
    if b == 1 or (b == -1 and r.random() < 0.5):
        if b == -1:
            a, b, c = -a, 1, -c
        if r.random() < 0.5:                                    # y = -x - 2
            return f"y = {written((-a, 'x'), (c, ''))}"
    if b < 0 or (b > 0 and a < 0 and r.random() < 0.5):
        a, b, c = (-a, -b, -c) if b < 0 else (a, b, c)
    if a < 0 or r.random() < 0.3:                               # y - x = 1
        return f"{written((b, 'y'), (a, 'x'))} = {c}"
    return f"{written((a, 'x'), (b, 'y'))} = {c}"

def circle(R):
    return f"x^2 + y^2 = {R}"

def roots_with_line(conic, a, b, c):
    """The real points of conic = 0 on a x + b y = c (b ≠ 0), by the quadratic formula."""
    yx = (c - a * X) / b
    A, B, C = [sp.Rational(k) for k in sp.Poly(sp.expand(conic.subs(Y, yx)), X).all_coeffs()]
    D = B ** 2 - 4 * A * C
    need(D > 0)                                                 # two points, not tangent, not none
    xs = [(-B + s * sp.sqrt(D)) / (2 * A) for s in (1, -1)]
    return [(sp.expand(x), sp.expand(yx.subs(X, x))) for x in xs]

def with_line(r, conic, prompt, a, b, c):
    need(b != 0 and a != 0 and math.gcd(a, b) == 1)              # no 3 y - 3 x = -2
    sols = roots_with_line(conic, a, b, c)
    need(all(nice(v) for s in sols for v in s))
    return dict(prompt=f"{prompt}; {line(r, a, b, c)}", answer=points(sols))

# ------------------------------------------------------------------
# Type 1: a circle and a line
# ------------------------------------------------------------------
def t1_slope_one(r):                                            # the deck: x^2 + y^2 = 9; y - x = 1
    R = r.randint(2, 30)
    a, b = r.choice((1, -1)), 1
    return with_line(r, X ** 2 + Y ** 2 - R, circle(R), a, b, signed(r, 1, 5))

def t1_lattice(r):                                              # two whole-number points
    R = r.choice((5, 10, 13, 17, 25, 26, 29, 34, 37, 41, 50, 53, 58, 65, 85))
    pts = [(i, j) for i in range(-10, 11) for j in range(-10, 11) if i * i + j * j == R]
    (x1, y1), (x2, y2) = r.sample(pts, 2)
    a, b = y2 - y1, x1 - x2                                     # the line through them
    c = a * x1 + b * y1
    g = math.gcd(a, b, c)
    a, b, c = a // g, b // g, c // g
    need(abs(a) <= 4 and abs(b) <= 4)
    return with_line(r, X ** 2 + Y ** 2 - R, circle(R), a, b, c)

def t1_general(r):
    R = r.randint(2, 30)
    a, b = signed(r, 1, 3), signed(r, 1, 3)
    need(abs(a) != 1 or abs(b) != 1)
    return with_line(r, X ** 2 + Y ** 2 - R, circle(R), a, b, signed(r, 1, 8))

# ------------------------------------------------------------------
# Type 2: a circle and a hyperbola, built from x^2 and y^2
# ------------------------------------------------------------------
def t2(r, a, b, flip=False):
    """x^2 + y^2 = P + Q and a x^2 - b y^2 = a P - b Q (or b y^2 - a x^2 = ...)."""
    P, Q = r.randint(1, 16), r.randint(1, 16)
    need(math.gcd(a, b) == 1 and a * P != b * Q)
    hx, hy = (f"{a} x^2" if a != 1 else "x^2"), (f"{b} y^2" if b != 1 else "y^2")
    hyper = f"{hy} - {hx} = {b * Q - a * P}" if flip else f"{hx} - {hy} = {a * P - b * Q}"
    sols = [(sx * sp.sqrt(P), sy * sp.sqrt(Q)) for sx in (1, -1) for sy in (1, -1)]
    need(all(nice(v, rad=50) for s in sols for v in s))
    return dict(prompt=f"{circle(P + Q)}; {hyper}", answer=points(sols))

def t2_add(r):                                                  # the deck: 2 x^2 - y^2 = -6; add
    return t2(r, r.randint(1, 4), 1)

def t2_scale(r):                                                # scale the circle first
    return t2(r, r.randint(1, 4), r.randint(2, 4))

def t2_y_first(r):                                              # y^2 - 3 x^2 = ...
    return t2(r, r.randint(1, 4), r.randint(1, 3), flip=True)

# ------------------------------------------------------------------
# Type 3: x y = k and a line
# ------------------------------------------------------------------
def t3_slope_one(r):                                            # the deck: x y = -4; y = -x - 2
    k = signed(r, 1, 12)
    return with_line(r, X * Y - k, f"x y = {k}", r.choice((1, -1)), 1, signed(r, 1, 6))

def t3_whole(r):                                                # two whole-number points
    x1, x2 = r.sample([v for v in range(-6, 7) if v], 2)
    m = signed(r, 1, 3)                                         # m x^2 + c x - k = m (x - x1)(x - x2)
    c, k = -m * (x1 + x2), -m * x1 * x2
    need(c != 0)
    return with_line(r, X * Y - k, f"x y = {k}", -m, 1, c)

def t3_general(r):
    k = signed(r, 1, 12)
    a, b = signed(r, 1, 3), signed(r, 1, 3)
    need(abs(a) != 1 or abs(b) != 1)
    return with_line(r, X * Y - k, f"x y = {k}", a, b, signed(r, 1, 8))

# ------------------------------------------------------------------
# Type 4: factoring exponentials, the common factor taken piece by piece
# ------------------------------------------------------------------
def exponent(n, k):
    """(c, d) as c n + d."""
    return k[0] * n + k[1]

def t4(r, letters, terms, split=False):
    """g v^E (c1 v^d1 + c2 v^d2 + ...): for each letter the d's share no n and no number.
    split: no term keeps the common power alone, like 2 x - 3 x^n (the deck's problem 11)."""
    n = sp.Symbol(r.choice([v for v in ("n", "a", "m", "k") if v not in letters]))
    g = r.randint(1, 6)
    E = {v: (r.randint(1, 3), r.randint(0, 3)) for v in letters}
    while True:
        cs = [signed(r, 1, 6) if i else r.randint(1, 6) for i in range(terms)]
        if math.gcd(*cs) == 1:
            break
    need(g > 1 or any(abs(c) > 1 for c in cs))
    ds = [{v: (r.randint(0, 2), r.randint(0, 3)) for v in letters} for _ in range(terms)]
    for v in letters:                                           # each piece's smallest power is 0
        for part in (0, 1):
            if all(d[v][part] for d in ds):
                i = r.randrange(terms)
                ds[i][v] = (0, ds[i][v][1]) if part == 0 else (ds[i][v][0], 0)
    need(len({tuple(d.values()) for d in ds}) == terms)
    if split:
        need(all(any(d[v] != (0, 0) for v in letters) for d in ds))
    else:
        need(any(all(d[v] == (0, 0) for v in letters) for d in ds))
    full = lambda d: [(v, exponent(n, (E[v][0] + d[v][0], E[v][1] + d[v][1]))) for v in letters]
    prompt = AF.joined(*[(1 if c > 0 else -1, AF.mono(abs(c) * g, *full(d))) for c, d in zip(cs, ds)])
    inner = AF.joined(*[(1 if c > 0 else -1, AF.mono(abs(c), *[(v, exponent(n, d[v])) for v in letters]))
                        for c, d in zip(cs, ds)])
    return dict(prompt=prompt, answer=f"{AF.mono(g, *[(v, exponent(n, E[v])) for v in letters])} ({inner})")

def t4_two_terms(r):                                            # the deck: 3 x^(2 n + 2) + 12 x^(3 n + 3)
    return t4(r, ["x"], 2)

def t4_split(r):                                                # the deck: 4 x^(3 n + 2) - 6 x^(4 n + 1)
    return t4(r, ["x"], 2, split=True)

def t4_three_terms(r):
    return t4(r, [r.choice(("x", "y", "a", "p", "z"))], 3)

def t4_two_letters(r):
    return t4(r, ["x", "y"], 2)

# ------------------------------------------------------------------
# Type 5 (adv_factoring's Type 1) and Type 6
# ------------------------------------------------------------------
def t5(r, coefficients, sign, double=False):
    """(A^2 - B^2)/(A ± B), A = k x^(i a), B = j y^(h b): the deck's letters."""
    (x, y) = r.choice(BASES)
    (m, n) = r.choice([e for e in EXPONENTS if not set(e) & {x, y}])
    k, j = (r.randint(2, 5), r.randint(2, 5)) if coefficients else (1, 1)
    need(math.gcd(k, j) == 1)                                   # else a common number comes out first
    i, h = (2, 2) if double else (r.randint(1, 3), r.randint(1, 3))
    A, B = (k, ((x, i * sp.Symbol(m)),)), (j, ((y, h * sp.Symbol(n)),))
    sq = lambda M: AF.mono(M[0] ** 2, *[(v, 2 * e) for v, e in M[1]])
    one = lambda M: AF.mono(M[0], *M[1])
    prompt = f"({AF.joined((1, sq(A)), (-1, sq(B)))})/({AF.joined((1, one(A)), (sign, one(B)))})"
    return dict(prompt=prompt, answer=AF.joined((1, one(A)), (-sign, one(B))))

def t5_over_sum(r):                                             # the deck: (x^(2 a) - y^(2 b))/(x^a + y^b)
    return t5(r, False, 1, double=r.random() < 0.3)            # (x^(4 a) - y^(4 b))/(x^(2 a) + y^(2 b))

def t5_over_difference(r):
    return t5(r, False, -1)

def t5_with_numbers(r):
    return t5(r, True, r.choice((-1, 1)))

def t6(r, a_range, b_range, f_letters, s_letters):
    """F = a (letters), S = b (letters): F^3 ± S^3."""
    vs = r.sample(FRIENDLY, f_letters + s_letters)
    fv, sv = sorted(vs[:f_letters]), sorted(vs[f_letters:])
    a, b = r.randint(*a_range), r.randint(*b_range)
    need(math.gcd(a, b) == 1)
    A = a * sp.Mul(*[sp.Symbol(v) ** r.randint(1, 4) for v in fv])
    B = b * sp.Mul(*[sp.Symbol(v) ** r.randint(1, 3) for v in sv])
    sign = r.choice((-1, 1))
    order = [sp.Symbol(v) for v in fv + sv]
    return dict(prompt=AF.joined((1, tx(A ** 3, order)), (sign, tx(B ** 3, order))), answer=AF.cubes(A, B, sign))

def t6_letters(r):                                              # the deck: x^3 y^3 - p^3
    return t6(r, (1, 1), (1, 1), 2, 1)

def t6_numbers(r):                                              # the deck: 8 m^3 y^6 + x^3, 27 x^12 y^6 - z^9
    return t6(r, (2, 5), (1, 3), 2, 1)

def t6_number(r):                                               # 8 y^6 - 125
    return t6(r, (1, 4), (2, 6), 1, 0)

TEMPLATES = {
    "1": [t1_slope_one, t1_lattice, t1_general],
    "2": [t2_add, t2_scale, t2_y_first],
    "3": [t3_slope_one, t3_whole, t3_general],
    "4": [t4_two_terms, t4_split, t4_three_terms, t4_two_letters],
    "5": [t5_over_sum, t5_over_difference, t5_with_numbers],
    "6": [t6_letters, t6_numbers, t6_number],
}

def draw(entry, r, tpl):
    p = TEMPLATES[entry][tpl](r)
    if entry not in SYSTEMS:
        need(finished(entry, p["answer"]))                     # x^12 + 27 y^6: its trinomial factors again
    return p

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def equations(prompt):
    return [e.strip() for e in prompt.split(";") if e.strip()]

def system(prompt):
    eqs = equations(prompt)
    if len(eqs) != 2 or any(e.count("=") != 1 for e in eqs):
        raise ValueError("two equations, separated by ;")
    out = []
    for e in eqs:
        left, right = e.split("=")
        out.append(sp.expand(to_sympy(left) - to_sympy(right)))
    if not set().union(*[e.free_symbols for e in out]) <= {X, Y}:
        raise ValueError("equations in x and y")
    return out

def _groups(s):
    """The text inside each top-level pair of parentheses, and the text outside them."""
    depth, start, groups, outside = 0, 0, [], ""
    for i, ch in enumerate(s):
        if ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced parentheses")
            if depth == 0:
                groups.append(s[start:i])
        elif depth == 0:
            outside += ch
    if depth:
        raise ValueError("unbalanced parentheses")
    return groups, outside

def _split(s):
    depth, parts, cur = 0, [], ""
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]

def read_points(answer):
    """The points written in an answer, as text: [("-1 + sqrt(5)", "-1 - sqrt(5)"), ...]."""
    groups, outside = _groups(answer)
    if not groups or outside.replace('"and"', "").strip(" ,"):
        raise ValueError("write the answer as points: (x, y), (x, y)")
    out = []
    for g in groups:
        cs = [c.strip() for c in _split(g)]
        if len(cs) != 2 or not all(cs):
            raise ValueError("each point is (x, y)")
        out.append(tuple(cs))
    return out

def squarefree(n):
    return all(n % (p * p) for p in range(2, math.isqrt(n) + 1))

def simplest_number(t):
    """A coordinate as the key writes it: radicands without square factors, fractions in lowest terms."""
    if not all(squarefree(int(f)) and int(f) > 1 for f in re.findall(r"sqrt\((\d+)\)", t)):
        return False
    if re.search(r"sqrt\([^)]*[^\d)][^)]*\)", t) or re.search(r"/\s*\(?\s*sqrt", t):
        return False                                            # a radicand that isn't a number, a radical below
    fractions = re.findall(r"(?<![\w(])(\d+)\s*/\s*(\d+)", t) + re.findall(r"\((\d+) sqrt\(\d+\)\)\s*/\s*(\d+)", t)
    for n, d in fractions:
        if math.gcd(int(n), int(d)) != 1 or int(d) == 1:
            return False
    return simplest_form(t)

def check_system(p):
    eqs = system(p["prompt"])
    pts = read_points(p["answer"])
    if not all(simplest_number(c) for pt in pts for c in pt):
        return False
    vals = [(to_sympy(a), to_sympy(b)) for a, b in pts]
    if any(not (v.is_number and v.is_real) for pt in vals for v in pt):
        return False
    if len({(sp.nsimplify(a), sp.nsimplify(b)) for a, b in vals}) != len(vals):
        return False                                            # a point written twice
    for a, b in vals:
        if any(sp.expand(e.subs({X: a, Y: b})) != 0 for e in eqs):
            return False
    real = [s for s in sp.solve(eqs, [X, Y], dict=True) if all(v.is_real for v in s.values())]
    return len(real) == len(vals)

def finished(typ, answer):
    if typ in ("5", "6"):
        return AF.finished({"5": "1", "6": "3"}[typ], answer)
    fs = AF.factors(answer)                                     # Type 4
    adds = [f for f in fs if f.is_Add]
    if len(adds) != 1 or AF.content(adds[0]) != 1:
        return False
    terms = sp.Add.make_args(adds[0])
    if re.search(r"\(\s*-", answer):                              # as written: the factor starts with a plus
        return False
    bases = {b for t in terms for f in sp.Mul.make_args(t) for b in [f.base if f.is_Pow else f] if b.is_Symbol}
    letters = sorted(to_sympy(answer).free_symbols - bases, key=str)
    for v in bases:                                             # the pieces of v's exponents share nothing:
        pieces = []                                             # each letter's and the number's smallest is 0
        for t in terms:
            e = sum((f.exp if f.is_Pow else sp.Integer(1)) for f in sp.Mul.make_args(t)
                    if f == v or (f.is_Pow and f.base == v))
            e = sp.expand(e)
            ps = [e.coeff(L) for L in letters] + [e.subs({L: 0 for L in letters})]
            if any(not (c.is_Integer and c >= 0) for c in ps) or sp.expand(e - sum(c * L for c, L in zip(ps, letters)) - ps[-1]) != 0:
                return False
            pieces.append(ps)
        if any(min(col) != 0 for col in zip(*pieces)):
            return False
    return True

def check(p):
    try:
        if p["type"] in SYSTEMS:
            ok = check_system(p)
        else:
            ok = same_value(p["prompt"], p["answer"]) and simplest_form(p["answer"]) and finished(p["type"], p["answer"])
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def is_system(p):
    return ";" in p["prompt"]

def typst(p, gap="0.3em"):
    if is_system(p):
        return f"$display(cases({', '.join(equations(p['prompt']))}))$"
    return display(dfrac(p["prompt"]))

def answer_typst(p):
    if is_system(p):                                            # points: commas at the top, so no display(...)
        return f"${dfrac(p['answer'])}$"
    return display(dfrac(p["answer"]))

def text(p):
    if is_system(p):
        return "\n".join(f"{{ {plain(e)}" for e in equations(p["prompt"]))
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"]).replace('"and"', "and")

def height(p):
    return 0.6 if is_system(p) else 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Editing: an edited system is solved again with sympy; an edited
# exponential only when its exponents are numbers
# ------------------------------------------------------------------
def answer_of(prompt):
    if ";" in prompt:
        eqs = system(prompt)
        sols = [(s[X], s[Y]) for s in sp.solve(eqs, [X, Y], dict=True)
                if X in s and Y in s and all(v.is_real for v in s.values())]
        if not sols:
            raise ValueError("no real solutions")
        return points(sols)
    return AF.answer_of(prompt)

def edit_text(p):
    return " ; ".join(equations(p["prompt"])) if is_system(p) else p["prompt"]

def clean(t):
    return " ".join(t.replace("−", "-").split())

def from_edit(t, old):
    t = clean(t)
    try:
        system(t) if old["type"] in SYSTEMS else to_sympy(t)
    except Exception:
        raise ValueError("write it in Typst math, like " + (
            "x y = -4 ; y = -x - 2" if old["type"] in SYSTEMS else "3 x^(2 n + 2) + 12 x^(3 n + 3)")) from None
    if old["type"] in SYSTEMS:
        t = "; ".join(equations(t))
    try:
        answer = answer_of(t)
    except (ValueError, gen.Redraw, NotImplementedError):
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    t = clean(t).replace(" and ", ' "and" ')
    try:
        read_points(t) if p["type"] in SYSTEMS else to_sympy(t)
    except Exception:
        raise ValueError("write the answer in Typst math, like " + (
            "(-1 + sqrt(5), -1 - sqrt(5)) and (-1 - sqrt(5), -1 + sqrt(5))" if p["type"] in SYSTEMS
            else "3 x^(2 n + 2) (1 + 4 x^(n + 1))")) from None
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
