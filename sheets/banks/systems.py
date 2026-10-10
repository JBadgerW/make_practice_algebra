"""Systems of three linear equations in x, y, z, sorted by the first move.

Problems are built backward from the answer: pick an integer solution, then
coefficients, then the constants. The answer in the key is an ordered triple,
or "no solution" / "infinitely many solutions". check() solves the system
again with sympy, independently of how it was built.

A problem: dict(type, prompt, answer, source). prompt holds the three
equations in Typst math, separated by ";": "2x - 3y + z = 13; x + 4y - 2z = -11; ...".
"""
import random, re
from fractions import Fraction
import sympy as sp

NAME = FAMILY = "systems"
FIXED = False
TITLE = "Systems of Three Equations"
INSTRUCTIONS = "Solve each system of equations."
COURSES = ["Algebra 2", "Precalculus"]

TYPES = [
    dict(key="1", title="Back-Substitute",
         look="One equation has a single variable, and another has just two.",
         move="Solve the one-variable equation, substitute into the two-variable one, then into the last."),
    dict(key="2", title="Substitute First",
         look="One equation is already solved for a variable.",
         move="Substitute that expression into the other two equations; solve the two-variable system that is left."),
    dict(key="3", title="One Variable Missing",
         look="One equation has only two of the variables.",
         move="Eliminate that same variable from the other two equations; then solve the two equations in the same two variables."),
    dict(key="4", title="Eliminate",
         look="Every variable in every equation, and some coefficients are 1 or −1.",
         move="Pick the variable with a coefficient of 1 or −1 and eliminate it from two pairs of equations."),
    dict(key="5", title="Eliminate and Scale",
         look="Every variable in every equation, and no coefficient is 1 or −1.",
         move="Multiply one or both equations so a variable's coefficients are opposites, then add; do it for two pairs."),
    dict(key="A", title="No Solution", special=True,
         look="Two equations' left sides combine to make the third's, but the constants don't.",
         move="Eliminate as usual. A false statement such as 0 = 7 means there is no solution."),
    dict(key="B", title="Infinitely Many Solutions", special=True,
         look="One equation is a combination of the other two, constants included.",
         move="Eliminate as usual. A true statement such as 0 = 0 means infinitely many solutions."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]
WIDTH, SPACE = "half", "2.5in"
ENTRIES = [dict(key=k, type=k, kind="letters", title=TYPE[k]["title"], width=WIDTH, space=SPACE) for k in KEYS]
ENTRY = {e["key"]: e for e in ENTRIES}
V = ("x", "y", "z")
NONE, MANY = "no solution", "infinitely many solutions"

def label(t):
    return ("Special Case " if t.get("special") else "Type ") + t["key"]

def entry_key(text):
    t = text.strip()
    return t.upper() if t.upper() in ENTRY else None

def type_of(entry):
    return entry

def heading(typ):
    return f"{label(TYPE[typ])}: {TYPE[typ]['title']}"

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return bool(TYPE[typ].get("special"))

def initial_seen():
    return set()

def seen_key(p):
    return ("systems", p["prompt"])

# ------------------------------------------------------------------
# Writing equations
# ------------------------------------------------------------------
def side(coefs, names=V):
    """[2, -3, 1] -> "2x - 3y + z" (zero terms left out; all zero -> "0")."""
    out = ""
    for c, v in zip(coefs, names):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else str(abs(c))
        if not out:
            out = ("-" if c < 0 else "") + mag + v
        else:
            out += (" - " if c < 0 else " + ") + mag + v
    return out or "0"

def standard(coefs, const):
    return f"{side(coefs)} = {const}"

def solved(var, coefs, const):
    """var = (coefs . others) + const, e.g. x = 2y - z + 3."""
    others = [v for v in V if v != var]
    rhs = side(coefs, others)
    if const:
        rhs = f"{rhs} {'-' if const < 0 else '+'} {abs(const)}" if rhs != "0" else str(const)
    return f"{var} = {rhs}"

# ------------------------------------------------------------------
# Drawing, by type. Each returns a list of equation strings; Redraw retries.
# ------------------------------------------------------------------
class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

def nz(r, lo=1, hi=9):
    return r.choice([-1, 1]) * r.randint(lo, hi)

def solution(r):
    s = [r.randint(-9, 9) for _ in V]
    need(sum(x == 0 for x in s) <= 1)
    return s

def dot(a, s):
    return sum(x * y for x, y in zip(a, s))

def full_row(r, lo=1, hi=6):
    return [nz(r, lo, hi) for _ in V]

def lowest(a):
    """No common factor: otherwise dividing it out could change the type."""
    from math import gcd
    g = 0
    for x in a:
        g = gcd(g, x)
    need(g == 1)
    return a

def eq(r, a, s, c=None):
    """The equation a . (x, y, z) = c (default: a . s), usually leading with a plus."""
    c = dot(a, s) if c is None else c
    lead = next(x for x in a if x)
    if lead < 0 and r.random() < 0.8:
        a, c = [-x for x in a], -c
    return standard(a, c)

def det(rows):
    return sp.Matrix(rows).det()

def proportional(a, b):
    return sp.Matrix([a, b]).rank() < 2

def t1(r):
    s = solution(r)
    order = r.sample(range(3), 3)                    # which variable is alone, which pairs with it
    one, two, three = order[2], order[1], order[0]
    a3 = [0, 0, 0]; a3[one] = r.choice([1, 1, 1, 2, 3])
    a2 = [0, 0, 0]; a2[two] = r.choice([1, 1, 2]); a2[one] = nz(r, 1, 5)
    a1 = lowest(full_row(r, 1, 4))
    lowest(a2)
    return [eq(r, a1, s), eq(r, a2, s), standard(a3, dot(a3, s))], s

def t2(r):
    s = solution(r)
    k = r.randrange(3)
    cs = [nz(r, 1, 4) for _ in range(2)]
    others = [i for i in range(3) if i != k]
    const = s[k] - cs[0] * s[others[0]] - cs[1] * s[others[1]]
    need(abs(const) <= 12)
    rows = [lowest(full_row(r, 1, 4)) for _ in range(2)]
    eqs = [eq(r, a, s) for a in rows]
    eqs.insert(r.randrange(3), solved(V[k], cs, const))
    sub = [0, 0, 0]; sub[k] = 1
    for i, c in zip(others, cs):
        sub[i] = -c
    need(det(rows + [sub]) != 0)
    return eqs, s

def t3(r):
    s = solution(r)
    gone = r.randrange(3)
    short = [nz(r, 1, 6) for _ in V]; short[gone] = 0
    rows = [lowest(a) for a in (full_row(r, 1, 6), full_row(r, 1, 6), short)]
    r.shuffle(rows)
    need(det(rows) != 0)
    return [eq(r, a, s) for a in rows], s

def t4(r):
    s = solution(r)
    rows = [lowest(full_row(r, 1, 7)) for _ in range(3)]
    ones = sum(abs(c) == 1 for a in rows for c in a)
    need(2 <= ones <= 5)
    need(det(rows) != 0)
    return [eq(r, a, s) for a in rows], s

def t5(r):
    s = solution(r)
    rows = [lowest(full_row(r, 2, 7)) for _ in range(3)]
    need(det(rows) != 0)
    need(all(len(set(map(abs, col))) > 1 for col in zip(*rows)))   # no variable with equal sizes everywhere
    return [eq(r, a, s) for a in rows], s

def special_case(r, consistent):
    s = solution(r)
    a1, a2 = lowest(full_row(r, 1, 6)), lowest(full_row(r, 1, 6))
    need(not proportional(a1, a2))
    if r.random() < 0.3:                             # a multiple of one equation
        k = r.choice([2, 3, -1, -2])
        a3, c3 = [k * x for x in a1], k * dot(a1, s)
    else:                                            # a combination of both
        m, n = nz(r, 1, 2), nz(r, 1, 2)
        a3 = [m * x + n * y for x, y in zip(a1, a2)]
        c3 = m * dot(a1, s) + n * dot(a2, s)
    need(all(a3) and max(map(abs, a3)) <= 12)
    if not consistent:
        c3 += nz(r, 1, 9)
    rows = [(a1, dot(a1, s)), (a2, dot(a2, s)), (a3, c3)]
    r.shuffle(rows)
    return [eq(r, a, s, c) for a, c in rows], None

TEMPLATES = {"1": t1, "2": t2, "3": t3, "4": t4, "5": t5,
             "A": lambda r: special_case(r, False), "B": lambda r: special_case(r, True)}

def generate(entry, rng, seen, tries=400):
    for _ in range(tries):
        try:
            eqs, s = TEMPLATES[entry](rng)
        except Redraw:
            continue
        consts = [int(e.rsplit("=", 1)[1]) for e in eqs if re.fullmatch(r"-?\d+", e.rsplit("=", 1)[1].strip())]
        if any(abs(c) > 60 for c in consts):
            continue
        p = dict(type=entry, prompt="; ".join(eqs),
                 answer=triple(s) if s else (NONE if entry == "A" else MANY), source="template")
        if seen_key(p) in seen:
            continue
        if check(p) != "checked":                    # the independent check must agree with the build
            raise AssertionError(f"systems type {entry}: {p}")
        seen.add(seen_key(p))
        return p
    raise RuntimeError(f"could not draw a systems Type {entry} problem; check its template")

# ------------------------------------------------------------------
# Checking: solve the system again with sympy and compare
# ------------------------------------------------------------------
def equations(prompt):
    return [e.strip() for e in prompt.split(";") if e.strip()]

def solve_system(prompt):
    """A tuple of Fractions, NONE, or MANY; raises ValueError if it can't read the system."""
    from ..check import side_diff
    syms = sp.symbols("x y z")
    try:
        exprs = [side_diff(e) for e in equations(prompt)]
    except Exception as e:
        raise ValueError(f"can't read the equations: {e}") from None
    if any(e.free_symbols - set(syms) for e in exprs):
        raise ValueError("use only x, y, and z")
    if not all(sp.Poly(e, *syms).total_degree() <= 1 for e in exprs):
        raise ValueError("these equations aren't linear")
    sol = sp.linsolve(exprs, *syms)
    if sol == sp.EmptySet:
        return NONE
    (t,) = sol
    if any(c.free_symbols for c in t):
        return MANY
    return tuple(Fraction(str(c)) for c in t)

def read_answer(text):
    """An answer as written -> a tuple of Fractions, NONE, or MANY; None if unreadable."""
    t = " ".join(text.lower().replace("−", "-").split())
    if t in (NONE, "none", "no solutions", "∅"):
        return NONE
    if t.startswith("infinite") or t in ("many", "infinitely many"):
        return MANY
    m = re.fullmatch(r"\(?\s*([^,()]+),\s*([^,()]+),\s*([^,()]+?)\s*\)?", t)
    if not m:
        return None
    try:
        return tuple(Fraction(x.replace(" ", "")) for x in m.groups())
    except (ValueError, ZeroDivisionError):
        return None

def check(p):
    try:
        right = solve_system(p["prompt"])
    except ValueError:
        return "unchecked"
    given = read_answer(p["answer"])
    if given is None:
        return "unchecked"
    return "checked" if given == right else "failed"

def triple(s):
    return "(" + ", ".join(str(Fraction(x)) for x in s) + ")"

def answer_of(sol):
    return sol if isinstance(sol, str) else triple(sol)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
TERM = re.compile(r"\s*([+-]?)\s*(\d*)\s*([xyz])")

def cells(eq):
    """'2x - 3y + z = 13' -> the seven cells of an aligned row, or None if it isn't
    in standard form (terms in x, y, z order, a number on the right)."""
    left, _, right = eq.partition("=")
    if not re.fullmatch(r"\s*-?\d+\s*", right):
        return None
    out, pos, last = ["", "", "", "", ""], 0, -1
    for m in TERM.finditer(left):
        if m.start() != pos:
            return None
        sign, num, v = m.groups()
        i = V.index(v)
        if i <= last:
            return None
        if last < 0:                                   # the first term carries its own sign
            out[2 * i] = ("-" if sign == "-" else "") + num + v
        else:
            out[2 * i - 1], out[2 * i] = ("-" if sign == "-" else "+"), num + v
        last, pos = i, m.end()
    if left[pos:].strip():
        return None
    return out + ["=", right.strip()]

def typst(p, gap="0.3em"):
    eqs = equations(p["prompt"])
    rows = [cells(e) for e in eqs]
    if all(rows):
        body = ";\n    ".join(", ".join(c for c in row) for row in rows)
        return (f"$display(mat(delim: #(\"{{\", none), align: #right, column-gap: #0.2em,\n"
                f"    {body}))$")
    return f"$display(cases({', '.join(eqs)}))$"

def answer_typst(p):
    a = p["answer"]
    return f"${a}$" if a.startswith("(") else a

def pretty(s):
    return s.replace(" - ", " − ").replace("-", "−")

def text(p):
    eqs = equations(p["prompt"])
    braces = ["⎧", "⎨", "⎩"] if len(eqs) == 3 else ["{"] * len(eqs)
    return "\n".join(f"{b} {pretty(e)}" for b, e in zip(braces, eqs))

def answer_text(p):
    return pretty(p["answer"])

def height(p):
    """Inches the prompt takes on the page (three stacked rows), for page estimates."""
    return 0.65

# ------------------------------------------------------------------
# Hand editing: "eq1 ; eq2 ; eq3" in Typst math
# ------------------------------------------------------------------
def edit_text(p):
    return " ; ".join(equations(p["prompt"]))

def from_edit(text, old):
    eqs = [" ".join(e.split()) for e in text.split(";") if e.strip()]
    if len(eqs) < 2 or any(e.count("=") != 1 for e in eqs):
        raise ValueError("write the equations separated by ; each with a single =")
    prompt = "; ".join(eqs)
    sol = solve_system(prompt)
    new = dict(old, prompt=prompt, answer=answer_of(sol), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, text):
    a = read_answer(text)
    if a is None:
        raise ValueError("write the answer as (x, y, z), no solution, or infinitely many solutions")
    new = dict(p, answer=answer_of(a))
    return new, check(new)

def selftest(n, seed):
    rng, ok = random.Random(seed), True
    for k in KEYS:
        seen = set()
        for _ in range(n):
            generate(k, rng, seen)
        print(f"systems {label(TYPE[k]):16} {n} drawn, all verified")
    return ok
