"""Lesson 6 (Advanced Math): fractional equations, radical equations, systems of
three linear equations. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_006/slides/deck_006.typ): examples
6.1-6.6 and Problem Set 6, problems 5-12.

    1  a fractional equation:              4/7 + 3/(x + 2) = 5/3                  x = 17/23
    2  fraction and decimal coefficients:  3/7 x + 2/5 y = 11;  0.03x - 0.2y = -0.37   (21, 5)
    3  a cube root:                        root(3, x - 5) - 2 = 2                 x = 69
    4  two square roots:                   sqrt(s - 48) + sqrt(s) = 8             s = 49
    5  three equations, a variable missing: 2x + 2y - z = 14;  3x + 3y + z = 16;  x - 2y = 0    (4, 2, -2)
    6  three equations, every variable:    x + 2y + z = 4;  2x - y - z = 0;  2x - 2y + z = 1   (1, 1, 1)

Type 5 holds the systems the deck solves by substituting first: example 6.5
(one equation has two variables, x = 2y) and problem 11 (each equation has
two, a different one missing from each). Type 6 holds the ones it solves by
eliminating one variable twice (example 6.6, problem 12): every variable in
every equation, some coefficients 1 or -1. Type 3 is example 6.3 alone (no
problem has a cube root); Type 4 is example 6.4 and problems 8-9.

The key writes what the deck writes. A one-letter equation: the letter and its
value, x = 17/23, s = 49 (the deck sets the value in bold; the letter is drawn,
so the key names it). A value that is not whole is one fraction in lowest
terms, the minus in front: x = -6/23. A system: the ordered pair or triple of
whole numbers, (21, 5), (4, 2, -2). No source has an excluded root or an
extraneous one, and no draw does: the fractional equation is linear once
cleared, and the radical equations' left sides increase with the letter.

check() is independent of how a problem was built. Type 1 clears the equation
with sympy, drops roots that make a denominator zero, and requires the key's
value to be the one root left, in lowest terms (adv_fractional_equations).
Types 3-4 put the key's value into the original equation and require both
sides equal exactly (adv_radical_equations). Types 2, 5, and 6 solve the
system again with sympy (decimals read as exact fractions) and compare the
key's numbers.

No skipped sources: Lesson 6 has no proofs.

A problem: dict(type, prompt, answer, source), in Typst math; a system's prompt
is its equations separated by ";".
    prompt  "x + 2y + z = 4; 2x - y - z = 0; 2x - 2y + z = 1"
    answer  "(1, 1, 1)"
"""
import math, re
from fractions import Fraction
import sympy as sp
from .. import gen
from ..gen import need
from ..check import side_diff
from ..typmath import tx, fr, display, dfrac, text as plain
from . import adv_fractional_equations as FE
from . import adv_radical_equations as RE
from . import systems as SY

NAME = FAMILY = "adv_lesson_6"
FIXED = False
TITLE = "Lesson 6: Fractional Equations, Radical Equations, Systems of Three Linear Equations"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Lessons"}

SYSTEMS = ("2", "5", "6")

TYPES = [
    dict(key="1", title="A Fractional Equation",
         look="Number fractions and one fraction with the unknown below: $4/7 + 3/(x + 2) = 5/3$.",
         move="Write the value the unknown can't be ($x != -2$). Multiply every term by the least common "
              "multiple of the denominators, $21(x + 2)$, cancel, and solve.", space="1.25in"),
    dict(key="2", title="Fraction and Decimal Coefficients",
         look="Two equations in $x$ and $y$: one with fractions for coefficients, one with decimals.",
         move="Multiply the fraction equation by the $\"LCD\"$ and the decimal equation by a power of $10$ "
              "($35$ and $100$). Then eliminate a variable from the whole-number system.", space="2.25in"),
    dict(key="3", title="A Cube Root",
         look="A cube root of an expression with the unknown, and numbers: $root(3, x - 5) - 2 = 2$.",
         move="Get the cube root alone: $root(3, x - 5) = 4$. Cube both sides, $x - 5 = 64$, solve, and check."),
    dict(key="4", title="Two Square Roots",
         look="Two radicals, one of them the unknown alone: $sqrt(s - 48) + sqrt(s) = 8$.",
         move="Get $sqrt(s - 48)$ alone and square; the $s$ terms cancel. Get $sqrt(s)$ alone and square "
              "again. Check in the original equation.", space="1.75in"),
    dict(key="5", title="Three Equations, a Variable Missing",
         look="Three equations in $x$, $y$, $z$; one or more of them has only two variables.",
         move="Solve a two-variable equation for one variable ($x = 2 y$) and substitute it into the "
              "others. Solve the smaller system, then substitute back for the rest.", space="2.5in"),
    dict(key="6", title="Three Equations, Every Variable",
         look="Three equations, each with $x$, $y$, and $z$; some coefficients are $1$ or $-1$.",
         move="Eliminate the same variable twice: add (a) and (b), then (b) and (c), scaling if needed. "
              "Solve the two equations left, then substitute back to find the third variable.", space="2.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def P(e):
    return tx(sp.expand(e))

def rational(q):
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

# ------------------------------------------------------------------
# Type 1: p/q + k/(x + c) = s/t (example 6.1, problems 5-7)
# ------------------------------------------------------------------
DEN1 = range(2, 10)                  # q, t: the number fractions' denominators
TOP1 = range(1, 5)                   # k: the unknown fraction's numerator
SHIFT1 = range(-9, 10)               # c in x + c, not 0
ORDERS1 = ("number first", "unknown first")

def proper(q):
    """The tops p for p/q: lowest terms, not whole, under 2."""
    return [p for p in range(1, 2 * q) if math.gcd(p, q) == 1 and p % q]

def solve1(order, p, q, sign, k, c, s, t):
    """p/q +- k/(x + c) = s/t gives x = +-k/(s/t - p/q) - c; k/(x + c) +- p/q = s/t
    gives x = k/(s/t -+ p/q) - c."""
    if order == "number first":
        d, top = Fraction(s, t) - Fraction(p, q), sign * k
    else:
        d, top = Fraction(s, t) - sign * Fraction(p, q), k
    need(d != 0)
    return Fraction(top) / d - c

def t1_ok(x, order, p, q, sign, k, c, s, t):
    return (x in gen.LETTERS and order in ORDERS1 and sign in (1, -1) and q in DEN1 and t in DEN1
            and q != t and p in proper(q) and s in proper(t) and k in TOP1 and c in SHIFT1 and c != 0)

def t1_pick(r):
    q, t = r.sample(list(DEN1), 2)
    return dict(x=r.choice(gen.LETTERS), order=r.choice(ORDERS1), p=r.choice(proper(q)), q=q,
                sign=r.choice((1, 1, -1)), k=r.choice(TOP1), c=r.choice([n for n in SHIFT1 if n]),
                s=r.choice(proper(t)), t=t)

def t1(x, order, p, q, sign, k, c, s, t):
    need(t1_ok(x, order, p, q, sign, k, c, s, t))
    v = solve1(order, p, q, sign, k, c, s, t)
    need(v != 0 and v.denominator <= 30 and abs(v.numerator) <= 90)
    unknown = fr(str(k), P(sp.Symbol(x) + c))
    op = "+" if sign > 0 else "-"
    left = (f"{p}/{q} {op} {unknown}" if order == "number first"
            else f"{unknown} {op} {p}/{q}")
    return f"{left} = {s}/{t}"

# ------------------------------------------------------------------
# Type 2: a/b x + c/d y = n; e x + f y = m in decimals (example 6.2, problem 10)
# ------------------------------------------------------------------
DEN2 = range(2, 10)
TOP2 = range(1, 6)
DECIMALS = tuple(Fraction(k, 100) for k in range(1, 10)) + tuple(Fraction(k, 10) for k in range(1, 10))
SOLUTION2 = range(-36, 37)

def t2_ok(a, b, c, d, e, f, x, y):
    fa, fc = Fraction(a, b), Fraction(c, d)
    return (b in DEN2 and d in DEN2 and b != d and abs(a) in TOP2 and abs(c) in TOP2 and a > 0
            and math.gcd(a, b) == 1 and math.gcd(abs(c), d) == 1 and abs(fa) < 1 and abs(fc) < 1
            and e > 0 and abs(e) in DECIMALS and abs(f) in DECIMALS and e != abs(f)
            and x in SOLUTION2 and y in SOLUTION2 and x and y
            and (fa * x + fc * y).denominator == 1 and fa * f - fc * e != 0)

def t2_pick(r):
    b, d = r.sample(list(DEN2), 2)
    a = r.choice([n for n in TOP2 if math.gcd(n, b) == 1 and n < b])
    c = r.choice([-1, 1]) * r.choice([n for n in TOP2 if math.gcd(n, d) == 1 and n < d])
    hundredths = DECIMALS[:9]
    e, f = r.choice(hundredths), r.choice([-1, 1]) * r.choice(DECIMALS[9:])
    if r.random() < 0.5:
        e, f = r.choice(DECIMALS[9:]), r.choice([-1, 1]) * r.choice(hundredths)
    return dict(a=a, b=b, c=c, d=d, e=e, f=f,
                x=b * gen.signed(r, 1, 3), y=d * gen.signed(r, 1, 3))

def decimal(q):
    """A Fraction with a power-of-ten denominator as a decimal: 0.03, -0.37, 2."""
    return SY.decimal(Fraction(q))

def t2(a, b, c, d, e, f, x, y):
    need(t2_ok(a, b, c, d, e, f, x, y))
    n = Fraction(a, b) * x + Fraction(c, d) * y
    m = e * x + f * y
    need(abs(n) <= 40 and m != 0 and abs(m) < 10 and math.lcm(b, d) <= 45)   # the deck's 11, -0.37, LCD 35
    top = f"{a}/{b} x {'-' if c < 0 else '+'} {abs(c)}/{d} y = {rational(n)}"
    bottom = f"{decimal(e)}x {'-' if f < 0 else '+'} {decimal(abs(f))}y = {decimal(m)}"
    return f"{top}; {bottom}"

# ------------------------------------------------------------------
# Type 3: root(3, k x + b) +- c = n (example 6.3)
# ------------------------------------------------------------------
CUBE = tuple(v for v in range(-4, 6) if v not in (0, 1))   # the cube root's value
SHIFT3 = range(-9, 10)               # b, not 0
OUT3 = range(1, 10)                  # c
COEF3 = (1, 1, 1, 2, 3)              # k: mostly the deck's x alone

def t3_ok(x, k, b, sign, c, v):
    return (x in gen.LETTERS and k in COEF3 and b in SHIFT3 and b != 0 and sign in (1, -1)
            and c in OUT3 and v in CUBE and (v ** 3 - b) % k == 0)

def t3_pick(r):
    k = r.choice(COEF3)
    return dict(x=r.choice(gen.LETTERS), k=k, b=r.choice([n for n in SHIFT3 if n]),
                sign=r.choice((1, -1)), c=r.choice(OUT3), v=r.choice(CUBE))

def t3(x, k, b, sign, c, v):
    need(t3_ok(x, k, b, sign, c, v))
    n = v + sign * c
    need(n != 0 and (v ** 3 - b) // k != 0)
    return f"root(3, {P(k * sp.Symbol(x) + b)}) {'+' if sign > 0 else '-'} {c} = {n}"

# ------------------------------------------------------------------
# Type 4: sqrt(s - k) + sqrt(s) = n with sqrt(s) = m, sqrt(s - k) = j (example 6.4, problems 8-9)
# ------------------------------------------------------------------
ROOT4 = range(1, 10)                 # m and j
ORDERS4 = ("bare last", "bare first")

def t4_ok(x, m, j, order):
    return x in gen.LETTERS and m in ROOT4 and j in ROOT4 and m != j and m >= 2 and order in ORDERS4

def t4_pick(r):
    m = r.choice([n for n in ROOT4 if n >= 2])
    below, above = [n for n in ROOT4 if n < m], [n for n in ROOT4 if n > m]
    j = r.choice(below) if not above or r.random() < 0.8 else r.choice(above)   # mostly the deck's s - k
    return dict(x=r.choice(gen.LETTERS), m=m, j=j, order=r.choice(("bare last",) * 3 + ("bare first",)))

def t4(x, m, j, order):
    need(t4_ok(x, m, j, order))
    s = sp.Symbol(x)
    other, bare = f"sqrt({P(s + j * j - m * m)})", f"sqrt({x})"
    left = f"{other} + {bare}" if order == "bare last" else f"{bare} + {other}"
    return f"{left} = {m + j}"

# ------------------------------------------------------------------
# Types 5 and 6: three equations in x, y, z, built backward from a whole-number triple
# ------------------------------------------------------------------
COEF3D = range(-4, 5)
SOLUTION3 = range(-6, 7)

def shape(rows):
    """Which variable each row is missing (None: it has all three)."""
    out = []
    for a in rows:
        zeros = [i for i, c in enumerate(a) if c == 0]
        out.append(None if not zeros else zeros[0] if len(zeros) == 1 else "short")
    return out

def rows_ok(rows, sol):
    return (len(rows) == 3 and all(len(a) == 3 and all(c in COEF3D for c in a) for a in rows)
            and all(next(c for c in a if c) > 0 for a in rows if any(a))
            and all(math.gcd(*a) == 1 for a in rows)
            and len(sol) == 3 and all(v in SOLUTION3 for v in sol) and sum(v == 0 for v in sol) <= 1
            and sp.Matrix(rows).det() != 0)

def t5_ok(rows, sol):
    """Example 6.5: one row with two variables; problem 11: each row missing a different one."""
    if not rows_ok(rows, sol):
        return False
    s = shape(rows)
    one = sum(v is None for v in s) == 2 and sum(isinstance(v, int) for v in s) == 1
    each = sorted(v for v in s if isinstance(v, int)) == [0, 1, 2]
    return one or each

def t6_ok(rows, sol):
    """Examples 6.6, problem 12: every coefficient there, at least two of them 1 or -1."""
    return (rows_ok(rows, sol) and all(shape(rows)[i] is None for i in range(3))
            and sum(abs(c) == 1 for a in rows for c in a) >= 2)

def full_row(r):
    a = [r.choice([n for n in COEF3D if n]) for _ in range(3)]
    if a[0] < 0:
        a = [-c for c in a]
    return tuple(a)

def short_row(r, gone):
    a = [0 if i == gone else r.choice([n for n in COEF3D if n]) for i in range(3)]
    first = next(c for c in a if c)
    return tuple(-c for c in a) if first < 0 else tuple(a)

def solution(r):
    return tuple(r.choice(SOLUTION3) for _ in range(3))

def t5_one_pick(r):                  # example 6.5: x - 2y = 0 beside two full rows
    rows = [full_row(r), full_row(r), short_row(r, r.randrange(3))]
    r.shuffle(rows)
    return dict(rows=tuple(rows), sol=solution(r))

def t5_each_pick(r):                 # problem 11: 2x + 3y = -1; x - 2z = -3; 2y - z = -4
    gone = [2, 1, 0]
    r.shuffle(gone)
    return dict(rows=tuple(short_row(r, g) for g in gone), sol=solution(r))

def t6_pick(r):
    return dict(rows=tuple(full_row(r) for _ in range(3)), sol=solution(r))

def system3(rows, sol):
    return "; ".join(SY.standard(list(a), sum(c * v for c, v in zip(a, sol))) for a in rows)

def t5(rows, sol):
    need(t5_ok(rows, sol))
    return system3(rows, sol)

def t6(rows, sol):
    need(t6_ok(rows, sol))
    need(sum(abs(c) == 1 for a in rows for c in a) <= 6)     # some elimination still to do
    return system3(rows, sol)

TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick, t4)],
    "5": [(t5_one_pick, t5), (t5_each_pick, t5)],
    "6": [(t6_pick, t6)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok, t6: t6_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving and checking, independently of the build
# ------------------------------------------------------------------
def equations(prompt):
    return [e.strip() for e in prompt.split(";") if e.strip()]

XY = sp.symbols("x y")

def solve2(prompt):
    """The pair (x, y) as Fractions; raises ValueError unless there is exactly one."""
    eqs = equations(prompt)
    if len(eqs) != 2 or any(e.count("=") != 1 for e in eqs):
        raise ValueError("two equations, separated by ;")
    exprs = [sp.nsimplify(side_diff(e), rational=True) for e in eqs]      # 0.03 -> 3/100
    if any(e.free_symbols - set(XY) for e in exprs) or not all(sp.Poly(e, *XY).total_degree() <= 1 for e in exprs):
        raise ValueError("two linear equations in x and y")
    sol = sp.linsolve(exprs, *XY)
    if sol == sp.EmptySet or any(c.free_symbols for c in next(iter(sol))):
        raise ValueError("not exactly one solution")
    return tuple(Fraction(str(c)) for c in next(iter(sol)))

def read_tuple(text, n):
    t = " ".join(text.replace("−", "-").split())
    m = re.fullmatch(r"\(\s*" + r"\s*,\s*".join([r"(-?\d+(?:\s*/\s*\d+)?)"] * n) + r"\s*\)", t)
    if not m:
        raise ValueError(f"write the answer as ({', '.join('xyz'[:n])})")
    return tuple(Fraction(g.replace(" ", "")) for g in m.groups())

def pair(s):
    return "(" + ", ".join(rational(v) for v in s) + ")"

def answer_of(prompt, typ=None):
    typ = typ or guess(prompt)
    if typ == "1":
        return FE.answer_of(prompt)
    if typ in ("3", "4"):
        return RE.answer_of(prompt)
    if typ == "2":
        return pair(solve2(prompt))
    sol = SY.solve_system(prompt)
    if isinstance(sol, str):
        raise ValueError(sol)
    return pair(sol)

def guess(prompt):
    n = len(equations(prompt))
    return "2" if n == 2 else "6" if n == 3 else "3" if "root(3" in prompt else "4" if "sqrt" in prompt else "1"

def check(p):
    t = p["type"]
    try:
        if t == "1":
            return FE.check(p)
        if t in ("3", "4"):
            return RE.check(p)
        if t == "2":
            ok = read_tuple(p["answer"], 2) == solve2(p["prompt"])
        else:
            right = SY.solve_system(p["prompt"])
            ok = not isinstance(right, str) and read_tuple(p["answer"], 3) == right
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

# The radical types' keys come from the draw (sympy's radical solve is slow); check() still puts
# them back into the equation. An edited prompt is solved by answer_of.
KEY = {
    t3: lambda x, k, b, sign, c, v: f"{x} = {rational(Fraction(v ** 3 - b, k))}",
    t4: lambda x, m, j, order: f"{x} = {m * m}",
}

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    params = pick(r)
    prompt = build(**params)
    if build in KEY:
        return dict(prompt=prompt, answer=KEY[build](**params))
    try:
        answer = answer_of(prompt, entry)
    except ValueError:
        raise gen.Redraw
    return dict(prompt=prompt, answer=answer)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: three equations aligned in columns under one brace; two (Type 2) left-aligned
# ------------------------------------------------------------------
def is_system(p):
    return ";" in p["prompt"]

def aligned(eqs):
    rows = [SY.cells(e) for e in eqs]
    if not all(rows):
        return f"$display(cases({', '.join(dfrac(e) for e in eqs)}))$"
    keep = [i for i in range(7) if any(row[i] for row in rows)]    # drop z's columns from a pair
    body = ";\n    ".join(", ".join(row[i] for i in keep) for row in rows)
    gap = ""
    if "/" in body:
        body, gap = re.sub(r"(\d+)/(\d+)", r"display(\1/\2)", body), " row-gap: #0.6em,"
    return (f"$display(mat(delim: #(\"{{\", none), align: #right, column-gap: #0.2em,{gap}\n"
            f"    {body}))$")

def braced(eqs):
    """Type 2 as the deck sets it: one brace, each equation left-aligned (a fraction row and a decimal
    row have no columns in common), the fractions full size."""
    rows = ", ".join(re.sub(r"(\d+)/(\d+)", r"display(\1/\2)", e) for e in eqs)
    return f"$display(cases(gap: #0.8em, {rows}))$"

def typst(p, gap="0.3em"):
    if not is_system(p):
        return "Solve: #h(0.5em) " + display(dfrac(p["prompt"]))
    eqs = equations(p["prompt"])
    return "Solve the system: #h(0.5em) " + (braced(eqs) if len(eqs) == 2 else aligned(eqs))

def answer_typst(p):
    return f"${p['answer']}$" if is_system(p) else display(dfrac(p["answer"]))

def text(p):
    if is_system(p):
        eqs = equations(p["prompt"])
        braces = ["⎧", "⎨", "⎩"] if len(eqs) == 3 else ["⎰", "⎱"]
        return "Solve the system:\n" + "\n".join(f"{b} {SY.pretty(e)}" for b, e in zip(braces, eqs))
    return "Solve: " + plain(p["prompt"])

def answer_text(p):
    return SY.pretty(p["answer"]) if is_system(p) else plain(p["answer"])

def height(p):
    if is_system(p):
        n = len(equations(p["prompt"]))
        return (0.85 if "/" in p["prompt"] else 0.65) * n / 3
    return 0.55 if "/" in p["prompt"] else 0.4

# ------------------------------------------------------------------
# Editing: a system is its equations separated by ";"
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "4/7 + 3/(x + 2) = 5/3",
    "2": "3/7 x + 2/5 y = 11 ; 0.03x - 0.2y = -0.37",
    "3": "root(3, x - 5) - 2 = 2",
    "4": "sqrt(s - 48) + sqrt(s) = 8",
    "5": "2x + 2y - z = 14 ; 3x + 3y + z = 16 ; x - 2y = 0",
    "6": "x + 2y + z = 4 ; 2x - y - z = 0 ; 2x - 2y + z = 1",
}

def clean(t):
    return " ".join(t.replace("−", "-").replace("√", "sqrt").split())

def edit_text(p):
    return " ; ".join(equations(p["prompt"])) if is_system(p) else p["prompt"]

def from_edit(t, old):
    typ = old.get("type", "1")
    t = clean(t)
    if typ in SYSTEMS:
        t = "; ".join(equations(t))
    else:
        t = re.sub(r"(\d)([a-z])", r"\1 \2", t)               # 2x as 2 x, the way the prompts write it
    try:
        answer = answer_of(t, typ)
    except Exception:
        raise ValueError(f"write it in Typst math, like {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
