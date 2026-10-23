"""Absolute value equations and inequalities, in the order they're taught:
|x| alone, one step outside the bars, one or two steps inside, steps on
both sides of the bars, equations with no solution, and then inequalities.

Every number on a problem, and every number met while solving it, is
between -20 and 20, and every solution is an integer.

Problems are built backward. Pick k, the value the absolute value must
equal (or be compared with), then the expression inside the bars, so that
both solutions are integers, then the steps outside. Types 1-5 and 7-8 have
k > 0; type 6 has k < 0, so it has no solution.

A problem: dict(type, prompt, answer, source).
    prompt  the equation or inequality in Typst math: "3 abs(x - 2) + 1 = 13"
    answer  the solution as the key writes it: "x = -2 or x = 6",
            "-2 < x < 6", "x <= -2 or x >= 6", or "no solution"

check() solves the prompt and reads the answer again with sympy, and
compares the two sets.
"""
import random, re
from fractions import Fraction as F
import sympy as sp

NAME = FAMILY = "absolute"
FIXED = False
TITLE = "Lesson 1-7: Absolute Value Equations and Inequalities"
INSTRUCTIONS = ""                     # each type has its own (type_instructions)
COURSES = {"Algebra 1": "Lessons"}

SOLVE_EQ, SOLVE_INEQ = "Solve each equation.", "Solve each inequality."
TYPES = [
    dict(key="1", title="Absolute Value of x", instructions=SOLVE_EQ,
         look="|x| equals a number.",
         move="x is that far from 0 in either direction: x equals the number or its opposite."),
    dict(key="2", title="One Step Outside", instructions=SOLVE_EQ,
         look="|x| with a number added, subtracted, multiplied, or divided outside the bars.",
         move="Undo that step to get |x| alone. Then x equals the number or its opposite."),
    dict(key="3", title="One Step Inside", instructions=SOLVE_EQ,
         look="The bars are alone, with one step on x inside them.",
         move="Split into two equations: the inside equals the number, or the inside equals its opposite. Solve each with one step."),
    dict(key="4", title="Two Steps Inside", instructions=SOLVE_EQ,
         look="The bars are alone, with two steps on x inside them.",
         move="Split into two equations, the inside equal to the number and to its opposite. Solve each with two steps."),
    dict(key="5", title="Steps Inside and Outside", instructions=SOLVE_EQ,
         look="Steps outside the bars and inside them.",
         move="First undo the steps outside to get the absolute value alone. Then split into two equations and solve each."),
    dict(key="6", title="No Solution", instructions=SOLVE_EQ,
         look="Any of types 1-5, but getting the absolute value alone leaves it equal to a negative number.",
         move="Get the absolute value alone. An absolute value is never negative, so there is no solution. Stop there."),
    dict(key="7", title="Inequalities with |x|", instructions=SOLVE_INEQ,
         look="|x| compared with a number.",
         move="|x| < 5 means x is within 5 of 0: -5 < x < 5. |x| > 5 means x is farther than 5 from 0: x < -5 or x > 5. ≤ and ≥ include the ends."),
    dict(key="8", title="Solving Absolute Value Inequalities", instructions=SOLVE_INEQ,
         look="Steps outside the bars and inside them, with <, >, ≤, or ≥.",
         move="Get the absolute value alone, flipping the sign if you multiply or divide by a negative. Less than: write one compound inequality, -k < inside < k. Greater than: write two, inside < -k or inside > k. Solve."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]
SPACE = {"1": "0.5in", "2": "1in", "3": "1in", "4": "1.25in", "5": "1.75in", "6": "1.25in", "7": "0.75in", "8": "1.75in"}
ENTRIES = [dict(key=k, type=k, kind="numbers", title=TYPE[k]["title"], width="half", space=SPACE[k])
           for k in KEYS]
ENTRY = {e["key"]: e for e in ENTRIES}
INEQUALITY = ("7", "8")
BIG = 20                              # every number stays within -BIG..BIG
NONE, ALL = "no solution", "all real numbers"

def label(t):
    return "Type " + t["key"]

def entry_key(text):
    t = text.strip()
    return t if t in ENTRY else None

def type_of(entry):
    return entry

def heading(typ):
    return f"{label(TYPE[typ])}: {TYPE[typ]['title']}"

def type_instructions(typ):
    return TYPE[typ]["instructions"]

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return False

def initial_seen():
    return set()

def seen_key(p):
    return ("absolute", p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------
def flip(op):
    return {"<": ">", ">": "<", "<=": ">=", ">=": "<=", "=": "="}[op]

def plus(c):
    """7 -> " + 7", -7 -> " - 7", 0 -> ""."""
    return f" + {c}" if c > 0 else f" - {-c}" if c < 0 else ""

def lin(a, c=0):
    """a x + c: lin(2, 7) = "2x + 7", lin(1, -3) = "x - 3"."""
    return ("" if a == 1 else "-" if a == -1 else str(a)) + "x" + plus(c)

def times(a, s):
    """a times the absolute value s: "3 abs(x)", or s when a is 1."""
    return s if a == 1 else f"{a} {s}"

def answer_of_roots(op, lo, hi):
    """The key's answer when |inside| op k and the inside equals ±k at lo and hi."""
    if op == "=":
        return f"x = {lo} or x = {hi}"
    if op in ("<", "<="):
        return f"{lo} {op} x {op} {hi}"
    return f"x {flip(op)} {lo} or x {op} {hi}"

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

def small(*ns):
    need(all(abs(n) <= BIG for n in ns))

def nz(r, lo=1, hi=9):
    return r.choice([-1, 1]) * r.randint(lo, hi)

# The inside of the bars: u = p x + q. Each returns (text, p, q, mid), where
# mid(v) lists the numbers met solving u = v.
def i_x(r):
    return "x", F(1), F(0), lambda v: []

def i_plus(r):
    a = r.randint(1, 12)
    return f"x + {a}", F(1), F(a), lambda v: []

def i_minus(r):
    a = r.randint(1, 12)
    return f"x - {a}", F(1), F(-a), lambda v: []

def i_times(r):
    a = r.randint(2, 9)
    return f"{a}x", F(a), F(0), lambda v: []

def i_over(r):
    a = r.randint(2, 5)
    return f"x/{a}", F(1, a), F(0), lambda v: []

def i_lin(r):
    a, b = r.randint(2, 5), nz(r)
    return lin(a, b), F(a), F(b), lambda v: [v - b]

def i_over_plus(r):
    a, b = r.randint(2, 5), nz(r)
    return f"x/{a}{plus(b)}", F(1, a), F(b), lambda v: [v - b]

def i_group(r):
    a, b = r.randint(2, 5), nz(r)
    return f"(x{plus(b)})/{a}", F(1, a), F(b, a), lambda v: [a * v]

def i_back(r):
    a, b = r.randint(1, 5), r.randint(1, 12)
    return f"{b} - {lin(a)}", F(-a), F(b), lambda v: [v - b]

INNER1 = [i_plus, i_minus, i_times, i_over]
INNER2 = [i_lin, i_lin, i_over_plus, i_group, i_back]

# Outside the bars, around the absolute value s. Each takes the relation
# |u| op k and returns (left side, its relation, right side, numbers met).
def o_none(r, s, op, k):
    return s, op, k, []

def o_plus(r, s, op, k):
    a = r.randint(1, 12)
    return f"{s} + {a}", op, k + a, []

def o_minus(r, s, op, k):
    a = r.randint(1, 12)
    return f"{s} - {a}", op, k - a, []

def o_times(r, s, op, k):
    a = r.randint(2, 9)
    return times(a, s), op, a * k, []

def o_over(r, s, op, k):
    a = r.randint(2, 5)
    need(k % a == 0)
    return f"{s}/{a}", op, k // a, []

def o_lin(r, s, op, k):
    a, b = r.randint(2, 5), nz(r)
    return f"{times(a, s)}{plus(b)}", op, a * k + b, [a * k]

def o_over_plus(r, s, op, k):
    a, b = r.randint(2, 5), nz(r)
    need(k % a == 0)
    return f"{s}/{a}{plus(b)}", op, k // a + b, [k // a]

def o_back(r, s, op, k):
    """b - a|u|: undoing it divides by a negative, so an inequality's sign flips."""
    a, b = r.randint(1, 4), r.randint(1, 15)
    return f"{b} - {times(a, s)}", flip(op), b - a * k, [a * k, -a * k]

OUTER1 = [o_plus, o_minus, o_times, o_over]
OUTER2 = [o_lin, o_lin, o_over_plus, o_back]

# The stages: (insides, outsides, values of k, relations, chance the sides are swapped)
POS, NEG = range(1, 13), range(-9, 0)
EQ, INEQ = ("=",), ("<", ">", "<=", ">=")
STAGES = {
    "1": ([i_x], [o_none], range(1, BIG + 1), EQ, 0.2),
    "2": ([i_x], OUTER1, POS, EQ, 0),
    "3": (INNER1, [o_none], POS, EQ, 0),
    "4": (INNER2, [o_none], POS, EQ, 0),
    "5": (INNER1 + INNER2, OUTER1 + OUTER2, POS, EQ, 0),
    "6": ([i_x] + INNER1 + INNER2, [o_none] + OUTER1 + OUTER2, NEG, EQ, 0),
    "7": ([i_x], [o_none], POS, INEQ, 0.2),
    "8": (INNER1 + INNER2, OUTER1 + OUTER2, POS, INEQ, 0.15),
}

FRACTION = (i_over, i_over_plus, i_group, o_over, o_over_plus)
PAIRS = {k: [(i, o) for o in outer for i in inner if not (i in FRACTION and o in FRACTION)]   # no fraction inside a fraction
         for k, (inner, outer, *_) in STAGES.items()}

def draw(entry, r, tpl):
    """(prompt, answer) for one problem of the type; tpl picks the inside and outside."""
    _, _, ks, ops, swap = STAGES[entry]
    pairs = PAIRS[entry]
    inside, outside = pairs[tpl % len(pairs)]
    text, p, q, mid = inside(r)
    k, op = r.choice(ks), r.choice(ops)
    left, shown, right, met = outside(r, f"abs({text})", op, k)
    prompt = f"{right} {flip(shown)} {left}" if r.random() < swap else f"{left} {shown} {right}"
    small(k, right, *met)
    if k < 0:
        return prompt, NONE
    roots = sorted(((k - q) / p, (-k - q) / p))
    need(all(x.denominator == 1 for x in roots))
    small(*roots, *mid(k), *mid(-k))
    return prompt, answer_of_roots(op, int(roots[0]), int(roots[1]))

def numbers(prompt):
    return [int(n) for n in re.findall(r"\d+", prompt)]

def generate(entry, rng, seen, tries=400):
    tpl = rng.randrange(len(PAIRS[entry]))                       # chosen once, so templates that redraw often aren't rarer
    for _ in range(tries):
        try:
            prompt, answer = draw(entry, rng, tpl)
            small(*numbers(prompt))
        except Redraw:
            continue
        p = dict(type=entry, prompt=prompt, answer=answer, source="template")
        if seen_key(p) in seen:
            continue
        if check(p) != "checked":                    # the independent check must agree with the build
            raise AssertionError(f"absolute type {entry}: {p}")
        seen.add(seen_key(p))
        return p
    raise RuntimeError(f"could not draw an absolute value Type {entry} problem; check its template")

# ------------------------------------------------------------------
# Checking: solve the prompt again with sympy and compare its solution set
# with the answer's
# ------------------------------------------------------------------
X = sp.Symbol("x")
OPS = {"<=": sp.Le, ">=": sp.Ge, "<": sp.Lt, ">": sp.Gt, "=": sp.Eq}
REL = re.compile(r"\s*(<=|>=|<|>|=)\s*")
OR = re.compile(r'\s*(?:quad\s*)?"or"(?:\s*quad)?\s*|\s+or\s+')

def normal(text):
    """Unicode signs to ASCII, and |u| to abs(u)."""
    t = (text.replace("≤", "<=").replace("≥", ">=").replace("−", "-")
         .replace("⩽", "<=").replace("⩾", ">="))
    t = re.sub(r"\|([^|]+)\|", r"abs(\1)", t)
    return re.sub(r"(\d)\s*abs\(", r"\1 abs(", t)          # 2|x| -> "2 abs(x)", which Typst and sympy both read

def relations(text):
    """The set of x that make a chain like "-2 < x <= 6" or "abs(x) = 3" true."""
    from ..check import to_sympy
    bits = REL.split(text.strip())
    if len(bits) not in (3, 5):
        raise ValueError("write one or two signs")
    exprs = [to_sympy(e) for e in bits[0::2]]
    if any(e.free_symbols - {X} for e in exprs):
        raise ValueError("use only the variable x")
    s = sp.S.Reals
    for i, op in enumerate(bits[1::2]):
        s = s & sp.solveset(OPS[op](exprs[i], exprs[i + 1]), X, sp.S.Reals)
    return s

def solution(text):
    """The set of x an equation, inequality, or answer describes (a sympy set);
    ValueError if unreadable. Parts joined by "or" are unioned."""
    t = " ".join(normal(text).split())
    if t.lower() in (NONE, "no solutions", "none", "∅"):
        return sp.S.EmptySet
    if t.lower() in (ALL, "all reals"):
        return sp.S.Reals
    try:
        return sp.Union(*[relations(part) for part in OR.split(t)])
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"can't read it: {e}") from None

def same(a, b):
    return a.symmetric_difference(b) == sp.S.EmptySet

def check(p):
    try:
        ok = same(solution(p["prompt"]), solution(p["answer"]))
    except (ValueError, KeyError, TypeError):
        return "unchecked"
    return "checked" if ok else "failed"

def answer_of(s):
    """A sympy set -> the answer as the key writes it; ValueError if it isn't one of the shapes here."""
    def num(v):
        if not v.is_rational:
            raise ValueError(f"the solution {v} isn't a rational number")
        return str(v)
    def piece(i):
        if isinstance(i, sp.FiniteSet):
            return " or ".join(f"x = {num(v)}" for v in sorted(i))
        if not isinstance(i, sp.Interval):
            raise ValueError("the solution must be numbers, a segment, or rays")
        lo = "" if i.start.is_infinite else f"{num(i.start)} {'<' if i.left_open else '<='} "
        hi = "" if i.end.is_infinite else f" {'<' if i.right_open else '<='} {num(i.end)}"
        if lo and not hi:
            return f"x {'>' if i.left_open else '>='} {num(i.start)}"
        return f"{lo}x{hi}"
    if s == sp.S.EmptySet:
        return NONE
    if s == sp.S.Reals:
        return ALL
    return " or ".join(piece(i) for i in (s.args if isinstance(s, sp.Union) else [s]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def bars(s):
    """abs(u) -> |u|, matching parentheses: "abs((x + 2)/3)" -> "|(x + 2)/3|"."""
    out, i = "", 0
    while (j := s.find("abs(", i)) >= 0:
        depth, n = 0, j + 3
        while True:
            depth += {"(": 1, ")": -1}.get(s[n], 0)
            if depth == 0:
                break
            n += 1
        out += s[i:j] + "|" + bars(s[j + 4:n]) + "|"
        i = n + 1
    return out + s[i:]

def pretty(s):
    s = bars(s).replace("<=", "≤").replace(">=", "≥")
    return s.replace(" - ", " − ").replace("-", "−")

def typst(p, gap="0.3em"):
    """Display style, so every fraction is full size."""
    return f"$display({p['prompt']})$"

def answer_typst(p):
    a = p["answer"]
    return a if a in (NONE, ALL) else "$display(" + a.replace(" or ", ' quad "or" quad ') + ")$"

def text(p):
    return pretty(p["prompt"])

def answer_text(p):
    return pretty(p["answer"])

def height(p):
    """Inches the prompt takes on the page, for page estimates."""
    return 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Hand editing: the prompt, with |u| or abs(u)
# ------------------------------------------------------------------
def edit_text(p):
    return bars(p["prompt"])

def from_edit(text, old):
    t = " ".join(normal(text).split())
    if not t:
        raise ValueError("write an equation or inequality, like |x + 2| = 5")
    if old["type"] in INEQUALITY and not re.search(r"<|>", t):
        raise ValueError(f"Type {old['type']} is an inequality: use <, >, <=, or >=")
    if old["type"] not in INEQUALITY and t.count("=") != 1:
        raise ValueError(f"Type {old['type']} is an equation: use a single =")
    new = dict(old, prompt=t, answer=answer_of(solution(t)), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, text):
    t = " ".join(normal(text).split())
    try:
        solution(t)
    except ValueError:
        raise ValueError("write the answer like x = -2 or x = 6, -2 < x < 6, x < -2 or x > 6, or no solution") from None
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    rng = random.Random(seed)
    for k in KEYS:
        seen = set()
        for i in range(n):
            if i % 25 == 0:                          # type 1 has only forty problems
                seen = set()
            p = generate(k, rng, seen)
            assert all(abs(v) <= BIG for v in numbers(p["prompt"] + " " + p["answer"])), p
        print(f"absolute {label(TYPE[k]):8} {n} drawn, all verified")
    return True
