"""Algebra 1, Units 1-2 Cumulative Test: thirty question types, one per
question of the cumulative test for units 1 and 2, each drawn new: real
numbers and sets, equations, literal equations and formulas, inequalities,
absolute value, and lines.

Each type keeps its question's logic and form (multiple choice, select all,
fill in the blanks, parts) but draws its own numbers. Each word problem has
its own stories, set up with the same logic as the original question. Wrong
choices come from real mistakes: a sign not flipped, a reciprocal slope
without its sign change, a fraction not distributed, a tick misread on a
number line. With --mix all:1, every version is a parallel form of the test.

A problem: dict(type, prompt, answer, text, answer_text, mc, letters, d, source).
    prompt   Typst markup: the question with its choices, parts, and figures
    answer   Typst markup for the key
    mc       each multiple-choice group's choices, Typst markup ("$x = 8$")
    letters  each group's right letters ("A", "B, D")
    d        the numbers the question was built from
    key      (type 16 only) the prompt with the graph drawn on it
check() works the question again from d with sympy (solving the equation,
reading each choice back, testing points) and confirms that the right
letters are exactly the choices that are right.
"""
import math, random, re
from fractions import Fraction as F
import sympy as sp
from .. import gen, ineq
from ..gen import need, written, ABC
from ..check import to_sympy, same_value
from ..graphs import Graph, PREAMBLE as CETZ
from ..typmath import text as plain

NAME = FAMILY = "alg1_units_1_2_cumulative"
FIXED = False
TITLE = "Units 1-2 Cumulative Test"
INSTRUCTIONS = "Answer each question. Show your work."
COURSES = {"Algebra 1": "Tests"}
PREAMBLE = CETZ

def _t(key, title, width, space, look, move):
    return dict(key=key, title=title, width=width, space=space, look=look, move=move)

TYPES = [
    _t("1", "Odd or Even Multiples", "half", "0.5in",
       "A set of integers: which are odd (or even) and multiples of a number?",
       "Keep the multiples of the number, then keep the odd (or even) ones. Zero is even and a multiple of every number."),
    _t("2", "Order Real Numbers", "half", "0.5in",
       "A fraction, a decimal, and two square roots to put in order.",
       "Write each as a decimal (simplify the fraction under a root first), then order them."),
    _t("3", "Rational Results", "half", "0.25in",
       "A mixed number combined with a square root of a fraction.",
       "Simplify the root. A rational number with a rational number stays rational; with an irrational root, it doesn't."),
    _t("4", "Multi-Step Equation with Fractions", "half", "1in",
       "A fraction times a sum, subtracted.",
       "Distribute the fraction to both terms (with the minus sign), combine like terms, and solve."),
    _t("5", "Consecutive Odd or Even Integers", "half", "1in",
       "Three consecutive odd (or even) numbers and their sum.",
       "Call them n, n + 2, n + 4; add them, set the sum equal, and solve."),
    _t("6", "Price per Pound", "half", "1.25in",
       "Two items by the pound, the total, and how much less one costs per pound.",
       "Let x be the price of the first; the second is x minus the difference. Write the total, solve, and add the two prices."),
    _t("7", "Model with an Equation", "half", "0.25in",
       "A mix of two items at two prices that averages a third price.",
       "Cost of the first + cost of the second = average price × total amount."),
    _t("8", "Equation with Fractions", "half", "1.25in",
       "Fractions times sums on both sides.",
       "Distribute (or multiply both sides by a common denominator), collect x on one side, and solve."),
    _t("9", "Literal Equation", "half", "0.75in",
       "A formula of the form A = B + C D, solved for one letter of the product.",
       "Subtract the term added, then divide by the other factor."),
    _t("10", "Formula: Square Pyramid", "full", "1in",
       "V = 1/3 s^2 h: solve for h, then use it.",
       "Multiply both sides by 3 and divide by s^2. Then substitute."),
    _t("11", "Linear Inequality", "half", "1.25in",
       "Fractions times sums on both sides of an inequality.",
       "Distribute and collect x. If x drops out, the inequality left is always true or never true."),
    _t("12", "Compound Inequality", "half", "1in",
       "Two inequalities joined by \"or\".",
       "Solve each one. Dividing by a negative flips the sign."),
    _t("13", "Compound Inequality from a Number Line", "half", "0.25in",
       "A segment between two dots on a number line.",
       "Read each endpoint: an open dot is < or >, a closed dot is ≤ or ≥."),
    _t("14", "Absolute Value Equation", "half", "0.75in",
       "A target, a tolerance, and an absolute value equation in a story.",
       "Split it into target − x = tolerance and target − x = −tolerance."),
    _t("15", "Absolute Value Inequality from a Graph", "half", "0.75in",
       "Two rays pointing away from each other on a number line.",
       "Find the center and the distance to each end; isolate each absolute value and compare."),
    _t("16", "Graph a Linear Equation", "half", "0.25in",
       "A line in slope-intercept form in a story.",
       "Plot the y-intercept, then use the slope to find another point."),
    _t("17", "Perpendicular Lines", "half", "0.5in",
       "A line in standard form and five lines in different forms.",
       "Find each slope. Perpendicular slopes are opposite reciprocals."),
    _t("18", "Line Through Two Points", "half", "1in",
       "Two points on a trend line.",
       "Slope = rise over run; then use a point to find the y-intercept."),
    _t("19", "Linear Model in Context", "full", "0.25in",
       "An amount that goes down by the same amount each day or hour.",
       "The starting amount is the y-intercept; the amount used each day is the negative slope."),
    _t("20", "Horizontal or Vertical Line in Standard Form", "half", "0.5in",
       "Ax + By = C as a horizontal (or vertical) line through a point.",
       "A horizontal line is y = (the point's y): A = 0. A vertical line is x = (the point's x): B = 0."),
    _t("21", "Justify the Steps", "half", "0.75in",
       "The steps of solving an equation, and the reasons.",
       "Match each step with what was done to get there."),
    _t("22", "Point-Slope Form", "half", "0.5in",
       "A point and a slope in a story.",
       "y − y1 = m(x − x1): subtract the point's coordinates."),
    _t("23", "Standard Form from Intercept and Slope", "half", "1in",
       "An x-intercept and a slope.",
       "Write point-slope form through (intercept, 0), clear the fraction, and move x and y to one side."),
    _t("24", "Intercepts in Context", "full", "0.75in",
       "A profit equation in standard form.",
       "Set y = 0 for the x-intercept and x = 0 for the y-intercept. A profit needs y > 0."),
    _t("25", "Standard Form in Context", "half", "0.5in",
       "A budget and two prices.",
       "Price × number + price × number = budget."),
    _t("26", "Solutions in Context", "half", "0.5in",
       "A budget, two prices, and ordered pairs.",
       "Substitute each pair: it must use the budget exactly."),
    _t("27", "Parallel, Perpendicular, or Neither", "half", "0.75in",
       "Two lines in different forms.",
       "Write both in slope-intercept form and compare the slopes."),
    _t("28", "Parallel and Perpendicular Lines", "half", "1in",
       "A line perpendicular to one line, then a line parallel to it.",
       "The perpendicular slope is the opposite reciprocal; a parallel line keeps it. Use the point for the intercept."),
    _t("29", "Equivalent Profit Equations", "half", "0.25in",
       "A fixed cost, a cost per item, and a price per item.",
       "Profit = income − costs: s x − c x − fixed cost, in any equivalent form."),
    _t("30", "Formula: Cone", "full", "1in",
       "V = 1/3 π r^2 h: solve for h, then use it.",
       "Multiply both sides by 3 and divide by π r^2. Then substitute."),
]
T = gen.Types(TYPES, INSTRUCTIONS)
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Writing numbers
# ------------------------------------------------------------------
def q(x):
    """A Fraction as Typst math: 3, -2/3."""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def qt(x):
    """A Fraction for the terminal: 3, −2/3."""
    return plain(q(x))

def mixed(x):
    """A positive Fraction as a mixed number in Typst math: 2 1/2, 3, 3/4."""
    w, r = divmod(F(x), 1)
    return q(w) if not r else q(r) if not w else f"{w} {q(r)}"

def usd(x):
    """Dollars with cents: 31.25, 3.00."""
    return f"{F(x):.2f}" if isinstance(x, float) else f"{float(x):.2f}"

def price(x):
    """A price in an equation: 3.50, but 3 for a whole number."""
    return q(x) if F(x).denominator == 1 else usd(x)

def times(x):
    """A price times x: 3.50x, 4x, x."""
    return "x" if x == 1 else f"{price(x)}x"

def line(m, b, v="x"):
    """y = m x + b."""
    return f"y = {written((m, v), (b, ''))}"

def mc(r, right, wrong, shuffle=True):
    """(choices, letters), the choices distinct."""
    return gen.lettered(r, right, wrong, shuffle)

def choices(cs, arrangement="vertical"):
    return gen.choices_typst(cs, arrangement)

def choices_t(cs):
    return gen.choices_text(cs, lambda c: plain(c.replace("$", "")))

def parts(*ps):
    return "#parts(" + ", ".join(f"[{x}]" for x in ps) + ")"

def blank(w="2.5em"):
    return f"#box(width: {w}, stroke: (bottom: 0.5pt))"

def P(prompt, answer, text, answer_text, d, mcs=(), **extra):
    """A problem's fields; mcs: (choices, letters) per multiple-choice group."""
    return dict(prompt=prompt, answer=answer, text=text, answer_text=answer_text, d=d,
                mc=[list(c) for c, _ in mcs], letters=[l for _, l in mcs], **extra)

def math_of(c):
    """A choice's Typst math, for sympy: "$x = 8$" -> "x = 8"; |a| -> abs(a)."""
    s = c.replace("$", "").replace("plus.minus", "+-").replace("times", "*").replace("div", "/")
    return re.sub(r"\|([^|]*)\|", r"abs(\1)", s)

def right_letters(group, ok):
    """The letters of the choices in group that ok() says are right."""
    return ", ".join(ABC[i] for i, c in enumerate(group) if ok(c))

def slope_of(eq):
    """The slope of a line written any way, in x and y."""
    x, y = sp.symbols("x y")
    l, r = eq.split("=")
    e = to_sympy(l) - to_sympy(r)
    e = e.subs({s: {"x": x, "y": y}.get(str(s), s) for s in e.free_symbols})
    sol = sp.solve(e, y)
    need(len(sol) == 1)
    return sp.diff(sol[0], x)

def on_line(eq, pt):
    x, y = sp.symbols("x y")
    l, r = eq.split("=")
    e = to_sympy(l) - to_sympy(r)
    return sp.simplify(e.subs({s: {"x": pt[0], "y": pt[1]}[str(s)] for s in e.free_symbols})) == 0

def solve_x(eq):
    """The one solution of a linear equation in x, or None."""
    l, r = eq.split("=")
    e = sp.expand(to_sympy(l) - to_sympy(r))
    x = sp.Symbol("x")
    sol = sp.solve(e, x)
    return sol[0] if len(sol) == 1 else None

def name(r):
    return r.choice(gen.NAMES)

# ------------------------------------------------------------------
# A number line, drawn with cetz: pieces are (a, b, a closed?, b closed?),
# a or b None for a ray off that end.
# ------------------------------------------------------------------
def numline(lo, hi, pieces=(), ink="black", k=0.55):
    X = lambda v: f"{v * k:g}"
    out = [f"line(({(lo - 0.8) * k:g}, 0), ({(hi + 0.8) * k:g}, 0), mark: (start: \">\", end: \">\"), stroke: 0.6pt)"]
    for v in range(lo, hi + 1):
        out.append(f"line(({X(v)}, -0.1), ({X(v)}, 0.1), stroke: 0.6pt)")
        out.append(f"content(({X(v)}, -0.35), text(size: 8pt)[${v}$])")
    for a, b, ac, bc in pieces:
        a0 = lo - 0.8 if a is None else a
        b0 = hi + 0.8 if b is None else b
        if a is None:
            out.append(f"line(({X(b0)}, 0), ({a0 * k:g}, 0), stroke: 2pt + {ink}, mark: (end: \">\", fill: {ink}))")
        elif b is None:
            out.append(f"line(({X(a0)}, 0), ({b0 * k:g}, 0), stroke: 2pt + {ink}, mark: (end: \">\", fill: {ink}))")
        else:
            out.append(f"line(({X(a0)}, 0), ({X(b0)}, 0), stroke: 2pt + {ink})")
        for v, closed in ((a, ac), (b, bc)):
            if v is not None:
                out.append(f"circle(({X(v)}, 0), radius: 0.1, fill: {ink if closed else 'white'}, stroke: 0.8pt + {ink})")
    body = "\n    ".join(out)
    return f"#align(center)[#cetz.canvas(length: 1cm, {{\n    import cetz.draw: *\n    {body}\n  }})]"

# ------------------------------------------------------------------
# 1. Which elements are odd (or even) and multiples of k?
# ------------------------------------------------------------------
def setm(xs):
    return "${" + ", ".join(str(x) for x in sorted(xs)) + "}$"

def t1(r):
    k, par = r.choice((3, 5, 7)), r.choice(("odd", "even"))
    mult = [i * k for i in range(-3, 4)]
    a = r.choice([n for n in range(2, 3 * k) if n % 2 and n % k])
    b = r.choice([n for n in range(2, 3 * k) if n % 2 == 0 and n % k])
    s = sorted(mult + [a, -a, b, -b])
    odd_m = [x for x in mult if x % 2]
    even_m = [x for x in mult if x % 2 == 0]
    if par == "odd":
        right, wrong = odd_m, [[3 * k, -3 * k], even_m, [x for x in mult if x < 0]]
    else:
        right, wrong = even_m, [[x for x in even_m if x], odd_m, [x for x in s if x % 2 == 0]]
    cs, let = mc(r, setm(right), [setm(w) for w in wrong])
    prompt = (f"Which elements of Set $A$ are both {par} and multiples of {k}?\n\n$A = {{{', '.join(map(str, s))}}}$\n\n"
              + choices(cs))
    return P(prompt, f"{let}: {setm(right)}", f"Which elements of A = {{{', '.join(map(str, s))}}} are {par} multiples of {k}?  "
             + choices_t(cs), f"{let}: {{{', '.join(map(str, sorted(right)))}}}", dict(k=k, par=par, set=s), [(cs, let)])

def c1(p):
    d = p["d"]
    want = sorted(x for x in d["set"] if x % d["k"] == 0 and (x % 2 == 1) == (d["par"] == "odd"))
    as_set = lambda c: sorted(int(x) for x in c.strip("${}").split(", "))
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: as_set(c) == want)

# ------------------------------------------------------------------
# 2. Order a fraction, a decimal, and two square roots
# ------------------------------------------------------------------
def t2(r):
    fr = F(r.randint(10, 40), r.choice((3, 4, 6)))
    need(fr.denominator > 1 and 3 < fr < 9)
    dec = F(r.randint(31, 89), 10)
    need(dec.denominator > 1)
    squares = {n * n for n in range(10)}
    n1 = r.choice([n for n in range(10, 80) if n not in squares])
    n2 = r.choice([n for n in range(10, 80) if n not in squares and n != n1])
    den = r.randint(2, 4)
    items = [(q(fr), float(fr)), (f"{float(dec):g}", float(dec)),
             (f"sqrt({n1})", math.sqrt(n1)), (f"sqrt({n2 * den}/{den})", math.sqrt(n2))]
    vals = sorted(v for _, v in items)
    need(all(b - a >= 0.15 for a, b in zip(vals, vals[1:])))
    r.shuffle(items)
    shown = [t for t, _ in items]
    order = [t for t, _ in sorted(items, key=lambda i: i[1])]
    j = lambda ts: ", quad ".join(ts)
    return P(f"Order the numbers from least to greatest.\n\n${j(shown)}$", f"${j(order)}$",
             "Order from least to greatest: " + ", ".join(plain(t) for t in shown),
             ", ".join(plain(t) for t in order), dict(shown=shown, order=order))

def c2(p):
    v = [float(to_sympy(t)) for t in p["d"]["order"]]
    return sorted(p["d"]["order"]) == sorted(p["d"]["shown"]) and all(a < b for a, b in zip(v, v[1:]))

# ------------------------------------------------------------------
# 3. Which give a rational number? A mixed number with a square root
# ------------------------------------------------------------------
OPS3 = {"+": "+", "-": "-", "*": "times", "/": "div"}

def t3(r):
    w, b = r.randint(1, 5), r.randint(2, 5)
    a = r.choice([n for n in range(1, b) if math.gcd(n, b) == 1])
    t, R = r.randint(2, 4), r.randint(2, 5)
    rat = (R * R * t, t)
    c = r.choice([n for n in range(2, R * R * t) if n != R * R * t and not sp.sqrt(sp.Rational(n, t)).is_rational])
    irr = (c, t)
    n_rat = r.choice((2, 3))
    pool = [(op, rat) for op in OPS3]
    picks = r.sample(pool, n_rat) + r.sample([(op, irr) for op in OPS3], 5 - n_rat)
    r.shuffle(picks)
    mixed_n = f"{w} {a}/{b}"
    cs = [f"${mixed_n} {OPS3[op]} sqrt({x}/{y})$" for op, (x, y) in picks]
    let = ", ".join(ABC[i] for i, (_, rt) in enumerate(picks) if rt == rat)
    return P("Select all the expressions that will result in a rational number.\n\n" + choices(cs), let,
             "Select all that result in a rational number:  " + choices_t(cs), let,
             dict(w=w, a=a, b=b, picks=[[op, list(rt)] for op, rt in picks]), [(cs, let)])

def c3(p):
    d = p["d"]
    m = sp.Integer(d["w"]) + sp.Rational(d["a"], d["b"])
    def val(op, x, y):
        s = sp.sqrt(sp.Rational(x, y))
        return {"+": m + s, "-": m - s, "*": m * s, "/": m / s}[op]
    ok = [bool(sp.nsimplify(val(op, *rt)).is_rational) for op, rt in d["picks"]]
    shown = [f"${d['w']} {d['a']}/{d['b']} {OPS3[op]} sqrt({x}/{y})$" for op, (x, y) in d["picks"]]
    return shown == p["mc"][0] and p["letters"][0] == ", ".join(ABC[i] for i, o in enumerate(ok) if o)

# ------------------------------------------------------------------
# 4. a x + b - f (c + d x) = e, multiple choice
# ------------------------------------------------------------------
def t4(r):
    f = F(r.randint(1, 4), r.randint(2, 4))
    need(f.denominator > 1)
    n1, n2 = r.randint(1, 6), r.randint(1, 6)
    c, dd = n1 / f, n2 / f
    need(c.denominator > 1 or dd.denominator > 1)
    a, b, x = r.randint(2, 7), r.randint(1, 9), r.randint(2, 9)
    need(a != n2)
    e = a * x + b - n1 - n2 * x
    eq = f"{a}x + {b} - {q(f)} ({q(c)} + {q(dd)} x) = {e}"
    wrongs = []
    for num, den in ((e - b + n1, a - dd), (e - b + n1, a + n2), (e - b + c, a - dd)):
        need(den != 0)
        wrongs.append(F(num) / den)
    vals = [F(x)] + wrongs
    need(len(set(vals)) == 4 and all(abs(v) < 40 for v in vals))
    cs, let = mc(r, f"${x}$", [f"${q(v)}$" for v in wrongs])
    return P(f"What is the value of $x$ in the equation?\n\n${eq}$\n\n" + choices(cs, "grid"),
             f"{let}: $x = {x}$", f"What is x?  {plain(eq)}   " + choices_t(cs), f"{let}: x = {x}",
             dict(eq=eq), [(cs, let)])

def c4(p):
    x = solve_x(p["d"]["eq"])
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: to_sympy(math_of(c)) == x)

# ------------------------------------------------------------------
# 5. Three consecutive odd (or even) numbers and their sum
# ------------------------------------------------------------------
STORIES5 = [
    (None, 11, 95, "The house numbers of three houses side by side on {name}'s street are consecutive {par} numbers. "
                   "The house numbers add up to {S}. What are the three house numbers?"),
    (None, 3, 40, "Three players on a soccer team wear consecutive {par} jersey numbers. The sum of their jersey "
                  "numbers is {S}. What are the three jersey numbers?"),
    (None, 101, 297, "{name} and two classmates have lockers with consecutive {par} numbers. The locker numbers add "
                     "up to {S}. What are the three locker numbers?"),
    ("odd", 21, 301, "The right-hand pages of a book have odd page numbers. {name} reads three right-hand pages in a "
                     "row, and their page numbers add up to {S}. What are the three page numbers?"),
]

def t5(r):
    fixed, lo, hi, story = r.choice(STORIES5)
    par = fixed or r.choice(("odd", "even"))
    n = r.randint(lo, hi)
    need((n % 2 == 1) == (par == "odd"))
    S = 3 * n + 6
    prompt = story.format(name=name(r), par=par, S=S)
    ans = f"{n}, {n + 2}, {n + 4}"
    return P(prompt, ans, prompt, ans, dict(par=par, S=S, n=[n, n + 2, n + 4]))

def c5(p):
    d = p["d"]
    a, b, c = d["n"]
    return (b - a == c - b == 2 and a + b + c == d["S"] and (a % 2 == 1) == (d["par"] == "odd")
            and f"{d['S']}" in p["prompt"] and p["answer"] == f"{a}, {b}, {c}")

# ------------------------------------------------------------------
# 6. Two prices per pound, the total, and the difference
# ------------------------------------------------------------------
GOODS6 = [("cashews", "almonds"), ("cheddar cheese", "Swiss cheese"), ("ground beef", "ground turkey"),
          ("dark-roast coffee beans", "light-roast coffee beans"), ("shrimp", "scallops")]
WEIGHTS6 = [F(5, 4), F(3, 2), F(7, 4), F(2), F(9, 4), F(5, 2), F(3), F(7, 2)]

def t6(r):
    A, B = r.choice(GOODS6)
    w1, w2 = r.sample(WEIGHTS6, 2)
    pa = F(r.randint(30, 140), 10)
    diff = F(r.randint(1, 8), 10)
    pb = pa - diff
    need(pb >= 2)
    total = w1 * pa + w2 * pb
    need((total * 100).denominator == 1)
    right = pa + pb
    x2 = (total - w2 * diff) / (w1 + w2)                 # read "less" as "more"
    vals = [right, 2 * pa, 2 * pb, F(round(2 * x2 + diff, 2)).limit_denominator(100)]
    need(len(set(vals)) == 4)
    cs, let = mc(r, rf"\${usd(right)}", [rf"\${usd(v)}" for v in vals[1:]])
    nm = name(r)
    prompt = (f"{nm} buys ${mixed(w1)}$ pounds of {A} and ${mixed(w2)}$ pounds of {B} and pays a total of "
              rf"\${usd(total)}. A pound of {B} costs \${usd(diff)} less than a pound of {A}. What would be the "
              f"combined cost of 1 pound of {A} and 1 pound of {B}?\n\n" + choices(cs, "grid"))
    return P(prompt, rf"{let}: \${usd(right)} ({A} \${usd(pa)}, {B} \${usd(pb)})",
             f"{nm}: {plain(mixed(w1))} lb {A}, {plain(mixed(w2))} lb {B}, ${usd(total)} in all; {B} ${usd(diff)}/lb "
             f"less. Cost of 1 lb of each?  " + choices_t(cs).replace("\\", ""), f"{let}: ${usd(right)}",
             dict(w1=str(w1), w2=str(w2), total=str(total), diff=str(diff)), [(cs, let)])

def c6(p):
    d = {k: F(v) for k, v in p["d"].items()}
    x = sp.Symbol("x")
    pa = sp.solve(sp.Rational(str(d["w1"])) * x + sp.Rational(str(d["w2"])) * (x - sp.Rational(str(d["diff"])))
                  - sp.Rational(str(d["total"])), x)[0]
    want = F(str(2 * pa - sp.Rational(str(d["diff"]))))
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: F(c.replace("\\$", "")) == want)

# ------------------------------------------------------------------
# 7. A mix of two items that averages a price: choose the equation
# ------------------------------------------------------------------
STORIES7 = [
    ("{name} mixes $x$ pounds of walnuts at \\${p1} per pound with {n} pounds of raisins at \\${p2} per pound. "
     "The trail mix costs \\${p3} per pound."),
    ("A coffee shop blends $x$ pounds of Kona beans at \\${p1} per pound with {n} pounds of house beans at "
     "\\${p2} per pound. The blend is worth \\${p3} per pound."),
    ("{name} fills party bags with $x$ toy cars at \\${p1} each and {n} yo-yos at \\${p2} each. The toys in the "
     "bags cost an average of \\${p3} per toy."),
]

def t7(r):
    n = r.randint(4, 16)
    p2 = F(r.randint(4, 16), 4)
    p3 = p2 + F(r.randint(1, 6), 4)
    p1 = p3 + F(r.randint(1, 8), 4)
    x = n * (p3 - p2) / (p1 - p3)
    need(x.denominator == 1 and 2 <= x <= 30)
    P1, P2, P3 = price(p1), price(p2), price(p3)
    X1 = times(p1)
    right = f"${X1} + {P2}({n}) = {P3}(x + {n})$"
    wrong = [f"${X1} + {P2} = {times(p3 - p2)}$", f"${X1} + {P3} = {price(p2 * n)}(x + {n})$",
             f"${X1} + {P2}({n}) = {times(p3)} + {n}$"]
    cs, let = mc(r, right, wrong)
    story = r.choice(STORIES7).format(name=name(r), n=n, p1=usd(p1), p2=usd(p2), p3=usd(p3))
    return P(f"{story} Select the equation that models the situation.\n\n" + choices(cs), f"{let}: {right}",
             story.replace("\\", "").replace("$x$", "x") + " Which equation models it?  " + choices_t(cs),
             f"{let}: {plain(right.strip('$'))}", dict(x=int(x)), [(cs, let)])

def c7(p):
    x = p["d"]["x"]
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: solve_x(math_of(c)) == x)

# ------------------------------------------------------------------
# 8. f1 (a x + b) + c = f2 (d + e x)
# ------------------------------------------------------------------
def t8(r):
    f1, f2 = F(r.randint(1, 3), r.randint(2, 4)), F(1, r.randint(2, 3)) * r.randint(1, 2)
    need(f1.denominator > 1 and f2.denominator > 1)
    a, b, d, e = r.randint(2, 9), gen.signed(r, 1, 9), r.randint(1, 9), gen.signed(r, 1, 6)
    x = r.randint(-4, 6)
    need(f1 * a != f2 * e)
    c = f2 * (d + e * x) - f1 * (a * x + b)
    need(c.denominator == 1 and c != 0 and abs(c) <= 15)
    eq = f"{q(f1)} ({written((a, 'x'), (b, ''))}) {'+' if c > 0 else '-'} {abs(c)} = {q(f2)} ({written((d, ''), (e, 'x'))})"
    return P(f"Find the value of $x$ in the equation.\n\n${eq}$", f"$x = {x}$", f"Find x:  {plain(eq)}",
             f"x = {x}", dict(eq=eq, x=x))

def c8(p):
    return solve_x(p["d"]["eq"]) == p["d"]["x"] and p["answer"] == f"$x = {p['d']['x']}$"

# ------------------------------------------------------------------
# 9. A = B + C D, solved for C or D
# ------------------------------------------------------------------
FORMULAS9 = [("v", "u", "a", "t"), ("y", "b", "m", "x"), ("C", "F", "c", "n"), ("E", "v", "I", "r"),
             ("A", "P", "k", "h"), ("d", "s", "r", "t")]

def t9(r):
    X, Y, Z0, W0 = r.choice(FORMULAS9)
    Z, W = (Z0, W0) if r.random() < 0.5 else (W0, Z0)    # solve for either factor
    right = f"${W} = ({X} - {Y})/{Z}$"
    wrong = [f"${W} = {Z}({X} - {Y})$", f"${W} = ({Y} + {Z})/{X}$", f"${W} = {X} - {Y} - {Z}$"]
    cs, let = mc(r, right, wrong)
    f = f"{X} = {Y} + {Z0} {W0}"
    return P(f"Solve the equation ${f}$ for ${W}$.\n\n" + choices(cs, "grid"), f"{let}: {right}",
             f"Solve {f} for {W}.  " + choices_t(cs), f"{let}: {plain(right.strip('$'))}",
             dict(f=f, W=W), [(cs, let)])

def c9(p):
    W = p["d"]["W"]
    l, rr = p["d"]["f"].split("=")
    e = to_sympy(l) - to_sympy(rr)
    w = sp.Symbol(W)
    sol = sp.solve(e, w)[0]
    def ok(c):
        got = to_sympy(math_of(c).split("=")[1])
        return sp.simplify(got - sol) == 0
    return p["letters"][0] == right_letters(p["mc"][0], ok)

# ------------------------------------------------------------------
# 10 and 30. V = 1/3 s^2 h (a square pyramid), V = 1/3 pi r^2 h (a cone)
# ------------------------------------------------------------------
UNITS = ("cm", "mm", "m", "ft")

def t10(r):
    s, h = r.randint(3, 12), r.randint(3, 20)
    V = F(s * s * h, 3)
    need(V.denominator == 1)
    u = r.choice(UNITS)
    right = "$h = (3V)/s^2$"
    cs, let = mc(r, right, ["$h = (3s)/V^2$", "$h = s^2/(3V)$", "$h = 3/(V s^2)$"])
    uu = u.rstrip(".")
    prompt = ("The formula for the volume of a square pyramid is $V = 1/3 s^2 h$.\n\n" + parts(
        "Which formula gives the height $h$ of the square pyramid in terms of $s$ and $V$?\n\n" + choices(cs, "grid"),
        f'What is the height of a square pyramid with $V = {V} thin "{uu}"^3$ and side length $s = {s}$ {u}?'))
    return P(prompt, f"(a) {let}: {right} #h(1em) (b) {h} {u}",
             f"V = 1/3 s² h. (a) Solve for h.  {choices_t(cs)}  (b) h when V = {V} {uu}³, s = {s} {u}",
             f"(a) {let}: h = 3V/s²  (b) {h} {u}", dict(V=int(V), s=s, h=h, solid="pyramid"), [(cs, let)])

def t30(r):
    rad, h = r.randint(2, 7), r.randint(2, 15)
    V = F(rad * rad * h, 3)
    need(V.denominator == 1)
    u = r.choice(UNITS)
    uu = u.rstrip(".")
    right = "$h = (3V)/(pi r^2)$"
    cs, let = mc(r, right, ["$h = 3V pi r^2$", "$h = (1/3 V pi)/r^2$", "$h = (3V r^2)/pi$"])
    prompt = ("The formula for the volume $V$ of a cone is $V = 1/3 pi r^2 h$, where $r$ is the radius of the base "
              "and $h$ is the height of the cone.\n\n" + parts(
                  "Solve the formula for $h$. Choose the correct formula.\n\n" + choices(cs, "grid"),
                  f'Find the height of a cone with a volume of ${V} pi thin "{uu}"^3$ and a base with a radius of '
                  f"{rad} {u}."))
    return P(prompt, f"(a) {let}: {right} #h(1em) (b) $h = {h}$ {u}",
             f"V = 1/3 π r² h. (a) Solve for h.  {choices_t(cs)}  (b) h when V = {V}π {uu}³, r = {rad} {u}",
             f"(a) {let}: h = 3V/(πr²)  (b) {h} {u}", dict(V=int(V), s=rad, h=h, solid="cone"), [(cs, let)])

def c_formula(p):
    d = p["d"]
    V, s, h = sp.symbols("V s h")
    k = sp.pi if d["solid"] == "cone" else 1
    sol = sp.solve(sp.Eq(V, sp.Rational(1, 3) * k * s ** 2 * h), h)[0]
    def ok(c):
        got = to_sympy(math_of(c).split("=")[1])
        got = got.subs({x: {"V": V, "s": s, "r": s}.get(str(x), x) for x in got.free_symbols})
        return sp.simplify(got - sol) == 0
    vol = d["V"] * k
    return (p["letters"][0] == right_letters(p["mc"][0], ok) and sol.subs({V: vol, s: d["s"]}) == d["h"]
            and re.search(rf"\b{d['h']}\b", p["answer"].split("(b)")[1]) is not None)

# ------------------------------------------------------------------
# 11. An inequality whose x terms cancel: no solution or all real numbers
# ------------------------------------------------------------------
REL = {">=": "<=", "<=": ">=", ">": "<", "<": ">"}

def boundary(coef, const, op):
    """coef x op const, solved: "x >= 3/2"."""
    need(coef != 0)
    b = F(const) / coef
    return f"x {op if coef > 0 else REL[op]} {q(b)}"

def t11(r):
    f = F(r.randint(1, 5), r.choice((2, 3)))
    need(f.denominator > 1)
    a, b, c = r.randint(1, 4), r.randint(1, 5), gen.signed(r, 1, 10)
    Fx = f * a
    g, dco = r.randint(2, 3), r.randint(1, 3)
    h = (Fx - dco) / g
    need(h > 0 and h.denominator > 1)
    k = r.randint(1, 5)
    L, R = f * b + c, g * k
    need(L != R)
    op = r.choice((">=", "<="))
    always = (L >= R) if op == ">=" else (L <= R)
    left = f"{q(f)} ({written((a, 'x'), (b, ''))}) {'+' if c > 0 else '-'} {abs(c)}"
    right = f"{dco if dco != 1 else ''}x + {g}({q(h)} x + {k})"
    m1 = boundary(Fx - dco - h, R - L, op)                     # g left off h x
    m2 = boundary(a - dco - g * h, g * k - f * b - c, op)      # f left off a x
    need(m1 != m2)
    cs, let = gen.in_order([f"${m1}$", f"${m2}$", "no solution", "all real numbers"],
                           "all real numbers" if always else "no solution")
    ineq_s = f"{left} {op} {right}"
    return P(f"Solve the inequality.\n\n${ineq_s}$\n\n" + choices(cs, "grid"),
             f"{let}: {cs[ABC.index(let)]} (${written((Fx, 'x'), (L, ''))} {op} {written((Fx, 'x'), (R, ''))}$ is "
             f"{'always' if always else 'never'} true)", f"Solve: {plain(ineq_s)}   " + choices_t(cs),
             f"{let}: {cs[ABC.index(let)]}", dict(ineq=ineq_s), [(cs, let)])

def c11(p):
    s = ineq.solution(p["d"]["ineq"])
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: ineq.same(ineq.solution(math_of(c), sp.Symbol("x")), s))

# ------------------------------------------------------------------
# 12. c - a x >= d or a2 (b + x) + c2 >= d2
# ------------------------------------------------------------------
def t12(r):
    p_, q_ = r.randint(-4, 3), None
    need(p_ != 0)
    q_ = p_ + r.randint(1, 5)
    a1, c1_ = r.randint(2, 6), r.randint(1, 12)
    d1 = c1_ - a1 * p_
    a2, b2, c2 = r.randint(2, 5), gen.signed(r, 1, 5), gen.signed(r, 1, 8)
    d2 = a2 * (b2 + q_) + c2
    first = f"{c1_} - {a1}x >= {d1}"
    second = f"{a2}({written((b2, ''), (1, 'x'))}) {'+' if c2 > 0 else '-'} {abs(c2)} >= {d2}"
    both = f"{first} or {second}"
    right = f"x <= {p_} or x >= {q_}"
    wrong = [f"x >= {p_} or x >= {q_}", f"x <= {-p_} or x <= {q_}", f"x >= {-p_} or x >= {q_}"]
    cs, let = mc(r, f"${ineq.typst(right)}$", [f"${ineq.typst(w)}$" for w in wrong])
    return P(f"Solve the compound inequality.\n\n${ineq.typst(both)}$\n\n" + choices(cs), f"{let}: {cs[ABC.index(let)]}",
             f"Solve: {plain(both)}   " + choices_t(cs).replace('"', ""), f"{let}: {plain(right)}",
             dict(ineq=both), [(cs, let)])

def c12(p):
    s = ineq.solution(p["d"]["ineq"])
    x = sp.Symbol("x")
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: ineq.same(ineq.solution(math_of(c).replace('"', ""), x), s))

# ------------------------------------------------------------------
# 13. A compound inequality from a number line
# ------------------------------------------------------------------
STORIES13 = ["a pharmacy stores a vaccine", "a grocery store keeps fresh fish", "a farm keeps apples in cold storage",
             "a florist keeps cut tulips", "a lab stores a blood sample"]

def chain(lo, hi, lc, hc):
    return f"{lo} {'<=' if lc else '<'} x {'<=' if hc else '<'} {hi}"

def t13(r):
    lo = r.randint(-4, 1)
    hi = r.randint(lo + 2, 4)
    lc, hc = r.random() < 0.5, r.random() < 0.5
    right = chain(lo, hi, lc, hc)
    wrong = [chain(lo, hi, not lc, not hc), chain(lo - 1, hi - 1, lc, hc), chain(lo - 1, hi - 1, not lc, not hc)]
    cs, let = mc(r, f"${right}$", [f"${w}$" for w in wrong])
    story = r.choice(STORIES13)
    pic = numline(-5, 5, [(lo, hi, lc, hc)])
    prompt = (f"The number line shows the temperatures, in degrees Celsius, at which {story}. Write a compound "
              f"inequality that shows the same range.\n\n{pic}\n\n" + choices(cs, "grid"))
    dot = lambda c: "●" if c else "○"
    return P(prompt, f"{let}: ${right}$", f"Number line: {dot(lc)} at {lo}, {dot(hc)} at {hi}, shaded between ({story}).  "
             + choices_t(cs), f"{let}: {plain(right)}", dict(lo=lo, hi=hi, lc=lc, hc=hc), [(cs, let)])

def c13(p):
    d = p["d"]
    s = sp.Interval(d["lo"], d["hi"], not d["lc"], not d["hc"])
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: ineq.same(ineq.solution(math_of(c)), s))

# ------------------------------------------------------------------
# 14. tolerance = |target - x| in a story
# ------------------------------------------------------------------
STORIES14 = [
    (20, 60, 3, 9, "{name} plans to spend \\${b} on a birthday gift, give or take \\${c}. {name} uses the equation "
                   "${c} = |{b} - x|$ to find the most and the least the gift could cost."),
    (25, 60, 3, 10, "A recipe says to bake bread for {b} minutes, give or take {c} minutes. {name} uses the equation "
                    "${c} = |{b} - x|$ to find the longest and the shortest baking times."),
    (45, 90, 5, 15, "A coach wants practice to last {b} minutes, within {c} minutes either way. The coach uses the "
                    "equation ${c} = |{b} - x|$ to find the longest and the shortest practices."),
    (6, 15, 2, 5, "{name} wants to run {b} miles this week, within {c} miles either way, and uses the equation "
                  "${c} = |{b} - x|$ to find the most and the fewest miles."),
]

def t14(r):
    blo, bhi, clo, chi, story = r.choice(STORIES14)
    b, c = r.randint(blo, bhi), r.randint(clo, chi)
    need(b - c > 0 and b - c != c)
    lo, hi = b - c, b + c
    right = f"$x = {lo}, {hi}$"
    wrong = [f"$x = plus.minus {lo}$", f"$x = plus.minus {hi}$", f"$x = -{lo}, {hi}$"]
    cs, let = mc(r, right, wrong)
    s = story.format(name=name(r), b=b, c=c)
    return P(f"{s} What are the solutions to the equation?\n\n" + choices(cs, "grid"), f"{let}: {right}",
             s.replace("\\", "").replace("$", "") + " Solutions?  " + choices_t(cs).replace("plus.minus ", "±"),
             f"{let}: x = {lo}, {hi}", dict(b=b, c=c), [(cs, let)])

def c14(p):
    b, c = p["d"]["b"], p["d"]["c"]
    sols = set(sp.solve(sp.Abs(b - sp.Symbol("x", real=True)) - c))
    def vals(choice):
        t = choice.strip("$").split("=")[1].strip()
        if t.startswith("plus.minus"):
            n = int(t.split()[1])
            return {n, -n}
        return {int(v) for v in t.split(", ")}
    return p["letters"][0] == right_letters(p["mc"][0], lambda ch: vals(ch) == sols)

# ------------------------------------------------------------------
# 15. An absolute value inequality from a graph of two rays
# ------------------------------------------------------------------
STORIES15 = ["the readings that will set off the alarm on a machine's sensor",
             "the values that will count as outliers for a data set",
             "the scores that a spreadsheet will flag as unusual",
             "the changes in water level, in feet, that will trigger a warning at a dam"]

def absx(a, m):
    """|a x - a m| as Typst: |2x - 3|, |x + 2|."""
    return f"|{written((a, 'x'), (-a * m, ''))}|"

def t15(r):
    lo = r.randint(-4, 2)
    hi = r.randint(lo + 2, 4)
    closed = r.random() < 0.3
    op = ">=" if closed else ">"
    mid = F(lo + hi, 2)
    a = 1 if mid.denominator == 1 and r.random() < 0.5 else 2
    rad = a * F(hi - lo, 2)
    c = gen.signed(r, 1, 3)
    need(rad + c > 0)
    right = f"{absx(a, mid)} {'+' if c > 0 else '-'} {abs(c)} {op} {rad + c}"
    neg = -r.randint(1, 4)
    j = gen.signed(r, 1, 3)
    w1 = f"{neg} > {absx(1, j)}"
    w2 = f"{r.randint(1, 3)} > {absx(1, j)} + {r.randint(4, 6)}"
    need(mid != 0)
    wc = r.randint(1, 3)
    w3 = f"{a * F(hi - lo, 2) + wc} < {absx(a, -mid)} + {wc}" if a * mid == int(a * mid) else None
    need(w3 is not None)
    cs, let = mc(r, f"${right}$", [f"${w}$" for w in (w1, w2, w3)])
    story = r.choice(STORIES15)
    pic = numline(-5, 5, [(None, lo, False, closed), (hi, None, closed, False)])
    prompt = (f"The graph shows {story}. Which inequality represents the same set of values as the graph?\n\n"
              f"{pic}\n\n" + choices(cs))
    dot = "●" if closed else "○"
    return P(prompt, f"{let}: ${right}$", f"Graph: shaded left from {dot} {lo} and right from {dot} {hi} ({story}).  "
             + choices_t(cs), f"{let}: {plain(right)}", dict(lo=lo, hi=hi, closed=closed), [(cs, let)])

def c15(p):
    d = p["d"]
    lo, hi, closed = d["lo"], d["hi"], d["closed"]
    def graph(v):
        return v < lo or v > hi or (closed and v in (lo, hi))
    probes = [F(v, 2) for v in range(2 * lo - 6, 2 * hi + 7)]
    x = sp.Symbol("x")
    def ok(c):
        e = math_of(c)
        rel = next(o for o in (">=", "<=", ">", "<") if o in e)
        L, R = (to_sympy(s) for s in e.split(rel))
        L, R = (t.subs({s: x for s in t.free_symbols}) for t in (L, R))
        test = {">": lambda t: t > 0, "<": lambda t: t < 0, ">=": lambda t: t >= 0, "<=": lambda t: t <= 0}[rel]
        return all(bool(test((L - R).subs(x, sp.Rational(v.numerator, v.denominator)))) == graph(v) for v in probes)
    return p["letters"][0] == right_letters(p["mc"][0], ok)

# ------------------------------------------------------------------
# 16. Graph y = m x + b
# ------------------------------------------------------------------
SLOPES16 = [F(1), F(2), F(3), F(1, 2), F(3, 2)]

def t16(r):
    m = r.choice(SLOPES16) * r.choice((1, -1))
    b = gen.signed(r, 1, 3)
    run = m.denominator
    p2 = (run, b + m * run)
    need(-5 <= p2[1] <= 5)
    eq = line(m, b)
    if m > 0:
        story = (f"The equation ${eq}$ gives the temperature, in degrees Celsius, of a liquid $x$ minutes after it is "
                 "taken out of a freezer.")
    else:
        story = (f"The equation ${eq}$ gives the temperature, in degrees Celsius, of a liquid $x$ minutes after it is "
                 "put into a freezer.")
    pts = f"$(0, {b})$ and $({p2[0]}, {q(p2[1])})$"
    return P(f"{story} Graph the equation.\n\n#align(center)[{grid16()}]", f"The line through {pts}",
             plain(story.replace("$", "")) + " Graph the equation.", plain(f"the line through {pts}".replace("$", "")),
             dict(eq=eq, m=str(m), b=b, pts=[[0, b], [p2[0], str(p2[1])]]),
             key=f"{story} Graph the equation.\n\n#align(center)[{grid16(m, b)}]")

def grid16(m=None, b=None):
    g = Graph(x=(-5, 5), y=(-5, 5), width=4.0)
    if m is not None:
        g.line(float(m), b)
    return g.typst()

def c16(p):
    d = p["d"]
    return all(on_line(d["eq"], (F(x), F(y))) for x, y in d["pts"]) and d["pts"][0] != d["pts"][1]

# ------------------------------------------------------------------
# 17. Select every line perpendicular to a line in standard form
# ------------------------------------------------------------------
def std(A, B, C):
    """A x + B y = C, with A > 0."""
    if A < 0 or A == 0 and B < 0:
        A, B, C = -A, -B, -C
    return f"{written((A, 'x'), (B, 'y'))} = {C}"

def t17(r):
    m = gen.signed(r, 2, 5)
    C = gen.signed(r, 1, 12)
    given = std(m, -1, C)
    k = lambda: gen.signed(r, 1, 20)
    perp = F(-1, m)
    j, J = r.randint(1, 9), r.randint(1, 40)
    right = [f"${line(perp, k())}$", f"${std(1, m, k())}$"]
    wrong = [f"${line(m, k())}$", f"$y - {j} = {q(F(1, abs(m)))} ({abs(m)}x + {J})$", f"${line(-perp, k())}$"]
    cs, let = mc(r, right, wrong)
    return P(f"Select all the lines that are perpendicular to ${given}$.\n\n" + choices(cs), let,
             f"Lines perpendicular to {plain(given)}?  " + choices_t(cs), let, dict(given=given), [(cs, let)])

def c17(p):
    m = slope_of(p["d"]["given"])
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: slope_of(math_of(c)) * m == -1)

# ------------------------------------------------------------------
# 18. The equation of a trend line through two points
# ------------------------------------------------------------------
STORIES18 = ["The trend line on {name}'s scatter plot of plant growth goes through the points {P} and {Q}.",
             "The line of best fit for {name}'s science fair data passes through the points {P} and {Q}.",
             "On a graph of a store's weekly sales, {name} draws a trend line through the points {P} and {Q}."]

def t18(r):
    m = gen.signed(r, 2, 4)
    x1 = r.randint(1, 6)
    y1 = r.randint(0, 6)
    dx = r.choice((1, 2))
    x2, y2 = x1 - dx, y1 - m * dx
    b = y1 - m * x1
    need(abs(b) <= 20 and y2 >= -10)
    fits = lambda s: line(s, F(y1) - s * x1)
    right = f"${line(m, b)}$"
    wrong = [f"${fits(F(-m))}$", f"${fits(F(1, m))}$", f"${fits(F(-1, m))}$"]
    cs, let = mc(r, right, wrong)
    Pp, Qp = f"$({x1}, {y1})$", f"$({x2}, {y2})$"
    s = r.choice(STORIES18).format(name=name(r), P=Pp, Q=Qp)
    return P(f"{s} What is the equation of the line?\n\n" + choices(cs, "grid"), f"{let}: {right}",
             plain(s.replace("$", "")) + " Equation?  " + choices_t(cs), f"{let}: {plain(right.strip('$'))}",
             dict(pts=[[x1, y1], [x2, y2]]), [(cs, let)])

def c18(p):
    pts = p["d"]["pts"]
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: all(on_line(math_of(c), pt) for pt in pts))

# ------------------------------------------------------------------
# 19. An amount used up at a steady rate: the model, and the y-intercept
# ------------------------------------------------------------------
STORIES19 = [
    dict(text="{name} has to read a {T}-page book for class and reads {d} pages each day.",
         ask="the number of pages {name} still has to read after $x$ days",
         means=["number of days of reading", "number of pages read each day", "number of chapters in the book",
                "number of pages in the book"], T=(120, 400), d=(10, 40)),
    dict(text="A water tank holds {T} gallons. A pump drains {d} gallons from it each hour.",
         ask="the number of gallons left in the tank after $x$ hours",
         means=["number of hours the pump runs", "number of gallons drained each hour", "number of quarts in the tank",
                "number of gallons in the tank at the start"], T=(200, 900), d=(20, 75)),
    dict(text="{name} has a gift card worth \\${T} and spends \\${d} on lunch with it each school day.",
         ask="the number of dollars left on the card after $x$ school days",
         means=["number of lunches the card pays for", "number of dollars spent on each lunch",
                "number of school days in a week", "number of dollars on the card at the start"], T=(40, 150), d=(5, 12)),
]

def t19(r):
    st = r.choice(STORIES19)
    d = r.randint(*st["d"])
    n = r.randint(4, 12)
    T = d * n
    need(st["T"][0] <= T <= st["T"][1])
    nm = name(r)
    right = f"$y = -{d}x + {T}$"
    cs, let = mc(r, right, [f"$y = -{T}x - {d}$", f"$y = {T}x - {d}$", f"$y = -{T}x + {d}$"])
    ms, mlet = gen.in_order(st["means"], st["means"][3])
    text = st["text"].format(name=nm, T=T, d=d)
    prompt = text + "\n\n" + parts(
        f"Write a linear equation to represent {st['ask'].format(name=nm)}.\n\n" + choices(cs, "grid"),
        "For the graph of the equation, what does the $y$-intercept represent?\n\n" + choices(ms))
    return P(prompt, f"(a) {let}: {right} #h(1em) (b) {mlet}: {ms[ABC.index(mlet)]}",
             text.replace("\\", "") + f" (a) Equation?  {choices_t(cs)}  (b) The y-intercept?  {choices_t(ms)}",
             f"(a) {let}: y = −{d}x + {T}  (b) {mlet}", dict(T=T, d=d, means=st["means"][3]), [(cs, let), (ms, mlet)])

def c19(p):
    d = p["d"]
    def ok(c):
        e = math_of(c).split("=")[1]
        return to_sympy(e).subs(sp.Symbol("x"), 0) == d["T"] and slope_of(math_of(c)) == -d["d"]
    return (p["letters"][0] == right_letters(p["mc"][0], ok)
            and p["letters"][1] == right_letters(p["mc"][1], lambda c: c == d["means"]))

# ------------------------------------------------------------------
# 20. A x + B y = C as a horizontal (or vertical) line through a point
# ------------------------------------------------------------------
def t20(r):
    x0, y0 = gen.signed(r, 1, 8), gen.signed(r, 1, 8)
    kind = r.choice(("horizontal", "horizontal", "vertical"))
    A, B, C = (0, 1, y0) if kind == "horizontal" else (1, 0, x0)
    pt = f"$({x0}, {y0})$"
    prompt = (f"For which values of $A$, $B$, and $C$ will $A x + B y = C$ be a {kind} line through the point {pt}?\n\n"
              f"$A = $ {blank('3em')}, #h(0.5em) $B = $ {blank('3em')}, #h(0.5em) $C = $ {blank('3em')}")
    other = f"$B = k$, $C = {y0}k$" if kind == "horizontal" else f"$A = k$, $C = {x0}k$"
    return P(prompt, f"$A = {A}$, $B = {B}$, $C = {C}$ (or any multiple: {other})",
             f"For which A, B, C is Ax + By = C a {kind} line through ({x0}, {y0})?", f"A = {A}, B = {B}, C = {C}",
             dict(kind=kind, pt=[x0, y0], ABC=[A, B, C]))

def c20(p):
    d = p["d"]
    A, B, C = d["ABC"]
    x0, y0 = d["pt"]
    flat = (A == 0) if d["kind"] == "horizontal" else (B == 0)
    return flat and (A, B) != (0, 0) and A * x0 + B * y0 == C

# ------------------------------------------------------------------
# 21. Justify the steps of a(x - b) = c(x - d), a = c + 1
# ------------------------------------------------------------------
REASONS21 = ["Distributive Property", "Multiply", "Addition and Subtraction Properties of Equality", "Add and subtract"]

def t21(r):
    c = r.randint(2, 8)
    a = c + 1
    b, d = gen.signed(r, 1, 9), gen.signed(r, 1, 9)
    need(a * b != c * d)
    x = a * b - c * d
    sx = lambda k, n: f"{k}(x {'-' if n > 0 else '+'} {abs(n)})"
    eq0 = f"{sx(a, b)} = {sx(c, d)}"
    steps = [f"{a}(x) + {a}({-b}) = {c}(x) + {c}({-d})",
             f"{written((a, 'x'), (-a * b, ''))} = {written((c, 'x'), (-c * d, ''))}",
             f"{a}x - {c}x = {written((-c * d, ''), (a * b, ''))}",
             f"x = {x}"]
    order = REASONS21[:]
    r.shuffle(order)
    rows = ", ".join(f"[${s}$], [{i}]" for i, s in enumerate(steps, 1))
    prompt = (f"The steps below show the solution to the equation ${eq0}$. Write the number of the step each reason "
              f"justifies.\n\n#align(center)[#table(columns: 2, stroke: none, align: (center, left), [${eq0}$], [], "
              f"{rows})]\n\n" + " \\\n".join(f"{blank('2em')} {w}" for w in order))
    ans = "; ".join(f"{w}: {REASONS21.index(w) + 1}" for w in order)
    return P(prompt, ans, f"Steps of {plain(eq0)}: " + ", ".join(f"({i}) {plain(s)}" for i, s in enumerate(steps, 1))
             + ". Match: " + "; ".join(order), ans, dict(eq=eq0, steps=steps, order=order))

def c21(p):
    d = p["d"]
    x0 = solve_x(d["eq"])
    same = all(solve_x(s) == x0 for s in d["steps"])
    ans = "; ".join(f"{w}: {REASONS21.index(w) + 1}" for w in d["order"])
    return same and d["steps"][-1] == f"x = {x0}" and p["answer"] == ans

# ------------------------------------------------------------------
# 22. Point-slope form from a point and a slope, in a story
# ------------------------------------------------------------------
STORIES22 = ["{name} studies how the hours of sunlight a plant gets each day relate to how much it grows.",
             "{name} collects data on the outside temperature and the number of customers at an ice cream stand.",
             "{name} compares the hours students study with their quiz scores."]

def t22(r):
    h, k = r.randint(1, 9), r.randint(1, 9)
    need(h != k)
    m = r.choice([F(n) for n in range(1, 6)] + [F(1, 2), F(3, 2), F(2, 3)])
    M = q(m)
    Mx = M if m.denominator == 1 else f"{M} "            # 2/3 (x - 4): the fraction stays apart
    right = f"$y - {k} = {Mx}(x - {h})$"
    wrong = [f"$y + {k} = {Mx}(x + {h})$", f"$y - {k} = {Mx}(x + {h})$", f"$y + {k} = {Mx}(x - {h})$"]
    cs, let = mc(r, right, wrong)
    s = r.choice(STORIES22).format(name=name(r))
    s += f" The line of best fit on the scatter plot passes through the point $({h}, {k})$ and has a slope of ${M}$."
    return P(f"{s} What is an equation for this line in point-slope form?\n\n" + choices(cs, "grid"), f"{let}: {right}",
             plain(s.replace("$", "")) + "  " + choices_t(cs), f"{let}: {plain(right.strip('$'))}",
             dict(pt=[h, k], m=str(m)), [(cs, let)])

def c22(p):
    d = p["d"]
    m = sp.Rational(d["m"])
    return p["letters"][0] == right_letters(p["mc"][0],
                                            lambda c: on_line(math_of(c), d["pt"]) and slope_of(math_of(c)) == m)

# ------------------------------------------------------------------
# 23. Standard form from an x-intercept and a slope
# ------------------------------------------------------------------
STORIES23 = ["The relationship between the number of weeks, $x$, since {name} planted a tree and the tree's height, $y$, "
             "in feet,",
             "The relationship between the number of years, $x$, since a town's library opened and the number of books "
             "it has, $y$, in thousands,",
             "The relationship between the number of months, $x$, since {name} opened a savings account and its balance, "
             "$y$, in hundreds of dollars,"]

def t23(r):
    x0 = -r.randint(1, 8)
    m = F(r.randint(1, 5), r.randint(2, 5))
    need(m.denominator > 1)
    A, B = m.numerator, m.denominator
    C = A * x0
    s = r.choice(STORIES23).format(name=name(r)) + f" has an $x$-intercept of ${x0}$ and a slope of ${q(m)}$."
    prompt = (f"{s} Write an equation for this relationship in standard form.\n\n"
              f"{blank()}$x - $ {blank()}$y = $ {blank()}")
    return P(prompt, f"${A}x - {B}y = {C}$", plain(s.replace("$", "")) + " Standard form: _x − _y = _",
             plain(f"{A}x - {B}y = {C}"), dict(x0=x0, m=str(m), eq=f"{A}x - {B}y = {C}"))

def c23(p):
    d = p["d"]
    return on_line(d["eq"], (d["x0"], 0)) and slope_of(d["eq"]) == sp.Rational(d["m"])

# ------------------------------------------------------------------
# 24. The intercepts of a profit equation, and the least sale for a profit
# ------------------------------------------------------------------
STORIES24 = [("A school club sells T-shirts at a fundraiser.", "the club's profit", "shirts it sells",
              "What is the fewest shirts the club must sell to make a profit?"),
             ("{name} runs a car wash on Saturdays.", "{name}'s profit", "cars washed",
              "What is the fewest cars {name} must wash to make a profit?"),
             ("A bakery sells pies at a farmers' market.", "the bakery's profit", "pies it sells",
              "What is the fewest pies the bakery must sell to make a profit?")]

def t24(r):
    b, k = r.randint(2, 6), r.randint(2, 5)
    a = b * k
    c = a * r.randint(2, 9)
    need(c % b == 0)
    xi, yi = c // a, -(c // b)
    need(xi != k)
    least = xi + 1
    story, who, what, ask = r.choice(STORIES24)
    nm = name(r)
    eq = f"{a}x - {b}y = {c}"
    fmt = lambda x, y: f"$x$-intercept: ${x}$; $y$-intercept: ${y}$"
    right = fmt(xi, yi)
    cs, let = mc(r, right, [fmt(k, yi), fmt(xi, -yi), fmt(k, -yi)])
    s = (story + f" The equation that relates {who}, $y$, in dollars, to the number of {what}, $x$, is ${eq}$.").format(name=nm)
    prompt = s + "\n\n" + parts("What are the $x$- and $y$-intercepts of the graph of the equation?\n\n" + choices(cs, "grid"),
                                ask.format(name=nm))
    return P(prompt, f"(a) {let}: {right} #h(1em) (b) {least} (a profit needs $x > {xi}$)",
             plain(s.replace("$", "")) + f" (a) Intercepts?  {choices_t(cs)}  (b) {ask.format(name=nm)}",
             f"(a) {let}  (b) {least}", dict(eq=eq, least=least), [(cs, let)])

def c24(p):
    d = p["d"]
    x, y = sp.symbols("x y")
    l, rr = d["eq"].split("=")
    e = to_sympy(l) - to_sympy(rr)
    e = e.subs({s: {"x": x, "y": y}[str(s)] for s in e.free_symbols})
    xi, yi = sp.solve(e.subs(y, 0), x)[0], sp.solve(e.subs(x, 0), y)[0]
    want = f"$x$-intercept: ${xi}$; $y$-intercept: ${yi}$"
    profit = sp.solve(e, y)[0]
    least = next(n for n in range(1, 1000) if profit.subs(x, n) > 0)
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: c == want) and least == d["least"]

# ------------------------------------------------------------------
# 25 and 26. A budget and two prices: standard form, and its solutions
# ------------------------------------------------------------------
STORIES25 = [("{name} will spend \\${T} on plants for a garden. Herbs cost \\${p} each, and flowering plants cost \\${q} each.",
              "herbs", "flowering plants", (2, 6)),
             ("A youth group will spend \\${T} on museum tickets. Student tickets cost \\${p} each, and adult tickets "
              "cost \\${q} each.", "student tickets", "adult tickets", (4, 12)),
             ("{name} will spend a \\${T} gift card at a bookstore. Paperback books cost \\${p} each, and hardcover "
              "books cost \\${q} each.", "paperbacks", "hardcovers", (6, 15))]

def budget(r):
    story, X, Y, (lo, hi) = r.choice(STORIES25)
    p = r.randint(lo, hi)
    qq = p * r.randint(2, 3) if r.random() < 0.6 else r.randint(p + 1, 2 * hi)
    T = qq * r.randint(3, 6)
    sols = [(x, (T - p * x) // qq) for x in range(T // p + 1) if (T - p * x) % qq == 0]
    return story.format(name=name(r), T=T, p=p, q=qq), X, Y, p, qq, T, sols

def t25(r):
    s, X, Y, p, qq, T, _ = budget(r)
    prompt = (f"{s} What equation in standard form determines the number $x$ of {X} and the number $y$ of {Y} that "
              f"can be bought?\n\n{blank()}$x + $ {blank()}$y = $ {blank()}")
    return P(prompt, f"${p}x + {qq}y = {T}$", s.replace("\\", "") + " Standard form: _x + _y = _",
             f"{p}x + {qq}y = {T}", dict(p=p, q=qq, T=T, eq=f"{p}x + {qq}y = {T}"))

def c25(p):
    d = p["d"]
    return (f"{d['T']}" in p["prompt"] and f"{d['p']} each" in p["prompt"] and f"{d['q']} each" in p["prompt"]
            and on_line(d["eq"], (0, F(d["T"], d["q"]))) and slope_of(d["eq"]) == sp.Rational(-d["p"], d["q"]))

def t26(r):
    s, X, Y, p, qq, T, sols = budget(r)
    need(len(sols) >= 2)
    n_right = r.choice((2, 3)) if len(sols) >= 3 else 2
    right = r.sample(sols, n_right)
    near = set()
    for x, y in sols:
        near |= {(x, y + 1), (x + 1, y), (y, x), (x + 2, y - 1), (max(x - 1, 0), y + 1)}
    near = sorted(pt for pt in near if pt[0] >= 0 and pt[1] >= 0 and p * pt[0] + qq * pt[1] != T)
    need(len(near) >= 5 - n_right)
    wrong = r.sample(near, 5 - n_right)
    pair = lambda pt: f"$({pt[0]}, {pt[1]})$"
    cs, let = mc(r, [pair(x) for x in right], [pair(x) for x in wrong])
    prompt = (f"{s} Select all of the ordered pairs ({X}, {Y}) that are possible combinations that use the "
              f"whole \\${T}.\n\n" + choices(cs, "grid"))
    return P(prompt, let, s.replace("\\", "") + f" Pairs ({X}, {Y}) that use all ${T}?  " + choices_t(cs), let,
             dict(p=p, q=qq, T=T), [(cs, let)])

def c26(p):
    d = p["d"]
    def ok(c):
        x, y = (int(v) for v in c.strip("$()").split(", "))
        return x >= 0 and y >= 0 and d["p"] * x + d["q"] * y == d["T"]
    return p["letters"][0] == right_letters(p["mc"][0], ok)

# ------------------------------------------------------------------
# 27. Parallel, perpendicular, or neither
# ------------------------------------------------------------------
REL27 = ["parallel.", "perpendicular.", "neither."]

def t27(r):
    A, B = r.randint(1, 5), gen.signed(r, 2, 6)
    need(math.gcd(A, abs(B)) == 1 or r.random() < 0.3)
    k = r.randint(1, 4)
    A, B = A * k, B * k
    m1 = F(-A, B)
    C = B * r.randint(-8, 8)
    rel = r.choice(REL27)
    if rel == "parallel.":
        m2, b2 = m1, F(C, B) + gen.signed(r, 1, 6)
    elif rel == "perpendicular.":
        m2, b2 = -1 / m1, r.randint(-10, 10)
    else:
        m2, b2 = r.choice((1 / m1, -m1)), r.randint(-10, 10)
        need(m2 != m1 and m2 * m1 != -1)
    first = std(A, B, C)
    second = line(m2, b2)
    cs, let = gen.in_order(REL27, rel)
    return P(f"Complete the sentence.\n\nThe lines ${first}$ and ${second}$ are\n\n" + choices(cs),
             f"{let}: {rel.rstrip('.')} (slopes ${q(m1)}$ and ${q(m2)}$)",
             f"The lines {plain(first)} and {plain(second)} are  " + choices_t(cs), f"{let}: {rel.rstrip('.')}",
             dict(first=first, second=second), [(cs, let)])

def c27(p):
    d = p["d"]
    a, b = slope_of(d["first"]), slope_of(d["second"])
    if a == b:                                       # parallel, unless they're one line
        y0 = to_sympy(d["second"].split("=")[1]).subs(sp.Symbol("x"), 0)
        rel = "same" if on_line(d["first"], (0, y0)) else "parallel."
    else:
        rel = "perpendicular." if a * b == -1 else "neither."
    return p["letters"][0] == right_letters(p["mc"][0], lambda c: c == rel)

# ------------------------------------------------------------------
# 28. Perpendicular through one point, then parallel through another
# ------------------------------------------------------------------
def t28(r):
    m0 = F(gen.signed(r, 1, 5), r.randint(2, 5))
    need(m0.denominator > 1 and abs(m0.numerator) > 1)
    b0 = gen.signed(r, 1, 9)
    s = -1 / m0
    P1 = (gen.signed(r, 1, 6), gen.signed(r, 1, 6))
    Qx = s.denominator * gen.signed(r, 1, 2)
    Qy = gen.signed(r, 1, 9)
    bn = Qy - s * Qx
    need(bn.denominator == 1 and bn != 0)
    right = f"${line(s, bn)}$"
    cs, let = mc(r, right, [f"${line(v, bn)}$" for v in (-s, 1 / s, -1 / s)])
    prompt = (f"Line $m$ passes through the point $({P1[0]}, {P1[1]})$ and is perpendicular to the graph of "
              f"${line(m0, b0)}$. Line $n$ is parallel to line $m$ and passes through the point $({Qx}, {Qy})$. "
              "What is the equation, in slope-intercept form, of line $n$?\n\n" + choices(cs, "grid"))
    return P(prompt, f"{let}: {right}", plain(prompt.split("\n\n")[0].replace("$", "")) + "  " + choices_t(cs),
             f"{let}: {plain(right.strip('$'))}", dict(given=line(m0, b0), Q=[Qx, Qy]), [(cs, let)])

def c28(p):
    d = p["d"]
    m0 = slope_of(d["given"])
    return p["letters"][0] == right_letters(p["mc"][0],
                                            lambda c: slope_of(math_of(c)) * m0 == -1 and on_line(math_of(c), d["Q"]))

# ------------------------------------------------------------------
# 29. Which equations could give the profit?
# ------------------------------------------------------------------
STORIES29 = [("{name} pays \\${F} for a booth at a craft fair and spends \\${c} on materials for each bracelet. "
              "Each bracelet sells for \\${s}.", "bracelets"),
             ("A food truck owner pays \\${F} for a permit and spends \\${c} on ingredients for each burrito. "
              "Each burrito sells for \\${s}.", "burritos"),
             ("{name} buys a supply of seeds and soil for \\${F}, and pots for \\${c} each. Each potted plant sells "
              "for \\${s}.", "potted plants")]

def t29(r):
    story, things = r.choice(STORIES29)
    Fc, c = r.randint(20, 150), r.randint(1, 6)
    s = c + r.randint(3, 15)
    k = s - c
    right = [f"$y = {s}x - {c}x - {Fc}$", f"$y = ({s} - {c})x - {Fc}$", f"$y = {k}x - {Fc}$", f"$y = -{Fc} + {k}x$"]
    wrong = [f"$y = {k}x + {Fc}$", f"$y = {s}x - {c}x + {Fc}$", f"$y = {s}x - {Fc}$", f"$y = ({s} + {c})x - {Fc}$"]
    n = r.choice((2, 3))
    cs, let = mc(r, r.sample(right, n), r.sample(wrong, 5 - n))
    st = story.format(name=name(r), F=Fc, c=c, s=s)
    return P(f"{st} Select all the equations that could represent the profit $y$ from selling $x$ {things}.\n\n"
             + choices(cs), let, st.replace("\\", "") + f" Profit y from x {things}?  " + choices_t(cs), let,
             dict(F=Fc, c=c, s=s), [(cs, let)])

def c29(p):
    d = p["d"]
    truth = f"{d['s']} x - {d['c']} x - {d['F']}"
    return p["letters"][0] == right_letters(p["mc"][0], lambda ch: same_value(math_of(ch).split("=")[1], truth))

# ------------------------------------------------------------------
# Drawing and checking
# ------------------------------------------------------------------
DRAW = {"1": t1, "2": t2, "3": t3, "4": t4, "5": t5, "6": t6, "7": t7, "8": t8, "9": t9, "10": t10,
        "11": t11, "12": t12, "13": t13, "14": t14, "15": t15, "16": t16, "17": t17, "18": t18, "19": t19,
        "20": t20, "21": t21, "22": t22, "23": t23, "24": t24, "25": t25, "26": t26, "27": t27, "28": t28,
        "29": t29, "30": t30}
CHECK = {"1": c1, "2": c2, "3": c3, "4": c4, "5": c5, "6": c6, "7": c7, "8": c8, "9": c9, "10": c_formula,
         "11": c11, "12": c12, "13": c13, "14": c14, "15": c15, "16": c16, "17": c17, "18": c18, "19": c19,
         "20": c20, "21": c21, "22": c22, "23": c23, "24": c24, "25": c25, "26": c26, "27": c27, "28": c28,
         "29": c29, "30": c_formula}

def draw(entry, r, tpl):
    p = DRAW[entry](r)
    need(CHECK[entry](dict(p, type=entry)))       # a wrong choice that happens to be right too: draw again
    return p

def check(p):
    if p.get("answer_edited"):
        return "unchecked"
    try:
        return "checked" if CHECK[p["type"]](p) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return p["prompt"]

def key_typst(p, gap="0.3em"):
    return p.get("key", p["prompt"])

def answer_typst(p):
    return p["answer"]

def text(p):
    return p["text"]

def answer_text(p):
    return p["answer_text"]

def height(p):
    """Inches the prompt takes, roughly: the words, the choices, and any figure."""
    h = 0.2 * (1 + len(p["text"]) // 90) + 0.3 * sum(len(g) for g in p["mc"])
    return h + (1.6 if "cetz" in p["prompt"] else 0)

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new problem; you can edit the answer")

def answer_edit_text(p):
    return ", ".join(p["letters"]) if len(p["mc"]) == 1 and len(p["mc"][0]) and "(b)" not in p["answer"] else p["answer"]

def with_answer(p, t):
    """A single multiple-choice question takes letters; anything else takes the key's text, unchecked."""
    if not t.strip():
        raise ValueError("the answer can't be empty")
    if len(p["mc"]) == 1 and "(b)" not in p["answer"]:
        got = [a.upper() for a in gen.letters_of(t.replace(" ", ",").replace(",,", ","))]
        if not got or any(a not in ABC[:len(p["mc"][0])] for a in got):
            raise ValueError(f"answer with letters, A to {ABC[len(p['mc'][0]) - 1]}")
        letters = ", ".join(sorted(set(got)))
        new = dict(p, letters=[letters], answer=letters, answer_text=letters)
        return new, check(new)
    new = dict(p, answer=t.strip(), answer_text=t.strip(), answer_edited=True)
    return new, "unchecked"

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
