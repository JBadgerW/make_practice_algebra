"""Lesson 24 (Advanced Math): sums of trigonometric functions, combining
functions. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_024/slides/deck_024.typ): examples
24.1-24.6 and Problem Set 24, problems 13-15.

    1  a sum of trig values:            cos 60° + sin 45°;  tan 45° + 2 tan 30°        (1 + sqrt(2))/2;  (3 + 2 sqrt(3))/3
    2  radical coefficients:            sqrt(6) sin 30° + (1/sqrt(2)) tan 60°          sqrt(6)
    3  in function notation:            f(θ) = tan θ;  f(45°) + 2 f(30°)              f(45°) + 2 f(30°) = (3 + 2 sqrt(3))/3
    4  a composition, as a function:    f(x) = log x, g(x) = x^2 + 6;  (g ∘ f)(x)      (g ∘ f)(x) = (log x)^2 + 6
    5  sum, difference, product, quotient at a number:
                                        f(x) = x + 2, g(x) = x^2 + 3;  (f + g)(6)      (f + g)(6) = 47
    6  a composition at a number:       f(x) = x + 3, g(x) = x^2 + 1;  (f ∘ g)(3)      (f ∘ g)(3) = 13

The deck's one heading for the trig sums is split by its move: Type 1's
coefficients are whole numbers; Type 2's are radicals, which multiply into the
trig values before the common denominator (and can leave no radical below, as
24.4's sqrt(6)); Type 3 (problem 15) asks in function notation, f(45°) for
tan 45°. Its combining-functions heading is split too: Type 4's composition is
a new function (24.5), Type 6's is a number (problem 14c), and Type 5 is the
rest of 24.6 and problem 14, one problem a part, since each part is the same
skill: f(6) and g(6), then one operation. 24.6's product and quotient have no
Problem Set item; they're Type 5's two other operations.

The key writes what the deck writes:
  1-3  the exact value as one fraction, the denominator rationalized and
       radicands square-free, in lowest terms; the numerator's terms in the
       order the problem's terms give them, a positive term first:
       (3 + 2 sqrt(3))/3 (tan 45° + 2 tan 30°), (2 sqrt(3) + 3 sqrt(2))/6
       (tan 30° + cos 45°), (1 + sqrt(2))/2 (problem 13), sqrt(6). Example 24.1's
       deck answer, (sqrt(2) + 1)/2, has its terms the other way; the key writes
       (1 + sqrt(2))/2 there too, by the rule (the check accepts both).
  3-6  what's found named, as the adv_* function banks write it:
       f(45°) + 2 f(30°) = (3 + 2 sqrt(3))/3, (f + g)(6) = 47, (f/g)(6) = 8/39.
       A number is a whole number or a fraction in lowest terms. A composition
       of two polynomials is multiplied out, by descending degree; with log x
       or sqrt(x) in it, the inside goes in as written: (log x)^2 + 6,
       log(x^2 + 6), 2 sqrt(x) + 1.

check() is independent of how a problem was built: it reads the prompt again
(the functions with adv_functions.read), works out the value with sympy, and
compares it with the answer's, exactly; then it reads the form from the
answer's text: for 1-3, no trig left, no radical below, square-free
radicands, lowest terms, and one numerator term per radical (like terms
combined); for 3-6, the name on the left matches what was asked; a number in
lowest terms; a composition of polynomials multiplied out.

No skipped sources: Lesson 24 has no proofs.

A problem: dict(type, prompt, answer, source), in Typst math; sin(30 degree)
is shown sin 30°, log(x) is shown log x, and circle.small is ∘.
    prompt  "f(x) = x + 2; g(x) = x^2 + 3; (f/g)(6)"
    answer  "(f/g)(6) = 8/39"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value, simplest_form, parts
from ..typmath import tx, fr, display, dfrac, text as plain_math
from .adv_trig import shown as trig_shown, readable
from .adv_lesson_20 import simplest as rationalized
from .adv_lesson_5 import terms, signed_join, positive_first
from . import adv_functions as AF

NAME = FAMILY = "adv_lesson_24"
FIXED = False
TITLE = "Lesson 24: Sums of Trigonometric Functions, Combining Functions"
INSTRUCTIONS = "Draw the necessary reference triangles and evaluate. Do not use a calculator."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="A Sum of Trig Values",
         look="Sines, cosines, and tangents of 30°, 45°, and 60° added, maybe with whole-number coefficients.",
         move="Find each value from its triangle (cos 60° = 1/2, sin 45° = 1/sqrt(2), tan 30° = 1/sqrt(3)). "
              "Write the terms over a common denominator, add, and rationalize: multiply the top and the bottom "
              "by the radical below."),
    dict(key="2", title="Radical Coefficients",
         look="A coefficient with a radical, like sqrt(6) sin 30° or (1/sqrt(2)) tan 60°.",
         move="Find each trig value and multiply it by its coefficient first: sqrt(6) (1/2) = sqrt(6)/2 and "
              "(1/sqrt(2)) sqrt(3) = sqrt(3)/sqrt(2). Then add over a common denominator, rationalize, and reduce."),
    dict(key="3", title="Trig Values in Function Notation",
         look="f(θ) = tan θ, and f of two angles.",
         move="f(45°) is tan 45°: put each angle into the function. Then evaluate the sum as in Type 1."),
    dict(key="4", title="A Composition of Functions",
         look="(g ∘ f)(x): one function inside another.",
         move="(g ∘ f)(x) = g(f(x)): put f(x) into the g machine. Replace every x in g's rule with f(x), in "
              "parentheses where needed, and multiply out polynomials.", instructions="Solve each problem."),
    dict(key="5", title="Combining Functions at a Number",
         look="(f + g)(6), (f - g)(6), (f g)(6), or (f/g)(6).",
         move="Find f(6) and g(6) first. Then add, subtract, multiply, or divide them: (f - g)(6) = f(6) - g(6).",
         instructions="Solve each problem."),
    dict(key="6", title="A Composition at a Number",
         look="(f ∘ g)(3): one function inside another, at a number.",
         move="Work from the inside out: find g(3), then put that number into f.", instructions="Solve each problem."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X = sp.Symbol("x")
COMPOSE = AF.COMPOSE                                # circle.small: ∘

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The exact sum, as the key writes it
# ------------------------------------------------------------------
FUNCS = ("sin", "cos", "tan")
ANGLES = (30, 45, 60)

def surd(v):
    """A sympy c sqrt(r), c rational -> (c, r), r square-free."""
    v = sp.radsimp(v)
    c, rest = v.as_coeff_Mul()
    if rest == 1:
        return sp.Rational(c), 1
    need(isinstance(rest, sp.Pow) and rest.exp == sp.Rational(1, 2) and rest.base.is_Integer)
    return sp.Rational(c), int(rest.base)

def surd_text(n, r):
    if r == 1:
        return str(n)
    return {1: f"sqrt({r})", -1: f"-sqrt({r})"}.get(n, f"{n} sqrt({r})")

def exact_sum(values):
    """Values c sqrt(r), in the problem's order, as one fraction: the like radicals added where
    each first appears, over the common denominator, reduced; a positive term first, or a minus
    in front when every term is negative."""
    seen = {}
    for v in values:
        c, r = surd(sp.radsimp(v))
        seen[r] = seen.get(r, 0) + c
    items = [(c, r) for r, c in seen.items() if c]
    need(items)
    d = math.lcm(*[c.q for c, _ in items])
    nums = [(int(c * d), r) for c, r in items]
    g = math.gcd(d, *[n for n, _ in nums])
    d, nums = d // g, [(n // g, r) for n, r in nums]
    neg = all(n < 0 for n, _ in nums)
    if neg:
        nums = [(-n, r) for n, r in nums]
    nums = positive_first(nums, lambda it: it[0])
    top = signed_join([surd_text(n, r) for n, r in nums])
    out = top if d == 1 else fr(top, str(d))
    return ("-" + (out if len(nums) == 1 or d != 1 else f"({out})")) if neg else out

def trig_terms(prompt):
    """The prompt's terms, each as a sympy value, in order."""
    return [to_sympy(t) for t in terms(prompt)]

def form_sum(answer):
    """No trig left, no radical below, square-free radicands, lowest terms; and as many
    numerator terms written as there are radicals (like terms combined)."""
    if not rationalized(answer):
        return False
    m = re.fullmatch(r"-?\((.*)\)/\d+", answer) or re.fullmatch(r"-?(.*)/\d+", answer)
    top = (m.group(1) if m else answer).lstrip("-")
    top = top[1:-1] if top.startswith("(") and top.endswith(")") else top
    n, _ = parts(answer)
    return len(terms(top)) == len(sp.Add.make_args(sp.expand(n)))

# ------------------------------------------------------------------
# Type 1: cos(60 degree) + sin(45 degree), tan(45 degree) + 2 tan(30 degree)
# ------------------------------------------------------------------
COEF1 = range(1, 5)
RATIONAL = {(f, a) for f in FUNCS for a in ANGLES if to_sympy(f"{f}({a} degree)").is_Rational}

def trig(c, f, a):
    """c f(a) as written: "tan(30 degree)", "2 tan(30 degree)", "sqrt(6) sin(30 degree)"."""
    return f"{f}({a} degree)" if c in (1, "1") else f"{c} {f}({a} degree)"

def t1_pick(r):
    (f1, a1), (f2, a2) = r.sample([(f, a) for f in FUNCS for a in ANGLES], 2)
    return dict(k1=1, f1=f1, a1=a1, s=r.choice("++++-"), k2=1, f2=f2, a2=a2)

def t1_coef_pick(r):
    return dict(t1_pick(r), k1=r.choice((1, 1, 2, 3)), k2=r.choice((2, 2, 3, 4)))

def t1_ok(k1, f1, a1, s, k2, f2, a2):
    return (k1 in COEF1 and k2 in COEF1 and f1 in FUNCS and f2 in FUNCS and a1 in ANGLES and a2 in ANGLES
            and s in "+-" and (f1, a1) != (f2, a2) and not {(f1, a1), (f2, a2)} <= RATIONAL)

def t1(k1, f1, a1, s, k2, f2, a2):
    """Examples 24.1-24.3: two trig values, a whole-number coefficient on either."""
    need(t1_ok(k1, f1, a1, s, k2, f2, a2))
    return f"{trig(k1, f1, a1)} {s} {trig(k2, f2, a2)}"

# ------------------------------------------------------------------
# Type 2: sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree), sqrt(3)/2 tan(30 degree) + sqrt(2) cos(60 degree)
# ------------------------------------------------------------------
COEF2 = ("sqrt(2)", "sqrt(3)", "sqrt(6)", "2 sqrt(2)", "2 sqrt(3)", "1/sqrt(2)", "1/sqrt(3)",
         "sqrt(2)/2", "sqrt(3)/2", "sqrt(3)/3", "sqrt(6)/2")

def t2_pick(r):
    (f1, a1), (f2, a2) = r.sample([(f, a) for f in FUNCS for a in ANGLES], 2)
    return dict(c1=r.choice(COEF2), f1=f1, a1=a1, s=r.choice("+++-"), c2=r.choice(COEF2), f2=f2, a2=a2)

def t2_ok(c1, f1, a1, s, c2, f2, a2):
    return (c1 in COEF2 and c2 in COEF2 and f1 in FUNCS and f2 in FUNCS and a1 in ANGLES and a2 in ANGLES
            and s in "+-" and (f1, a1) != (f2, a2))

def t2(c1, f1, a1, s, c2, f2, a2):
    """Example 24.4, problem 13: a radical coefficient on each trig value."""
    need(t2_ok(c1, f1, a1, s, c2, f2, a2))
    return f"{trig(c1, f1, a1)} {s} {trig(c2, f2, a2)}"

# ------------------------------------------------------------------
# Type 3: f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)
# ------------------------------------------------------------------
NAMES = ("f", "g", "h")
COEF3 = range(1, 5)
RULE3 = re.compile(r"^([a-z])\(theta\) = (sin|cos|tan)\(theta\)$")
CALL3 = re.compile(r"\b([a-z])\((-?\d+) degree\)")

def t3_pick(r):
    a1, a2 = r.sample(ANGLES, 2)
    return dict(name=r.choice(("f", "f", "g", "h")), func=r.choice(FUNCS), k1=r.choice((1, 1, 1, 2)), a1=a1,
                s=r.choice("+++-"), k2=r.choice((1, 2, 2, 3)), a2=a2)

def t3_ok(name, func, k1, a1, s, k2, a2):
    return (name in NAMES and func in FUNCS and k1 in COEF3 and k2 in COEF3 and a1 in ANGLES and a2 in ANGLES
            and a1 != a2 and s in "+-" and not {(func, a1), (func, a2)} <= RATIONAL)

def t3(name, func, k1, a1, s, k2, a2):
    """Problem 15: f(θ) = tan θ, and f at two angles."""
    need(t3_ok(name, func, k1, a1, s, k2, a2))
    call = lambda k, a: f"{name}({a} degree)" if k == 1 else f"{k} {name}({a} degree)"
    return f"{name}(theta) = {func}(theta); {call(k1, a1)} {s} {call(k2, a2)}"

def read3(prompt):
    rule, ask = [s.strip() for s in prompt.split(";")]
    m = RULE3.match(rule)
    if not m:
        raise ValueError("write it like: f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)")
    name, func = m.groups()
    if {n for n, _ in CALL3.findall(ask)} != {name}:
        raise ValueError(f"evaluate {name} only")
    return ask, CALL3.sub(lambda c: f"{func}({c.group(2)} degree)", ask)

# ------------------------------------------------------------------
# Types 4-6: the functions, and what to find
# ------------------------------------------------------------------
LIN = tuple(f"x + {c}" for c in range(1, 10)) + tuple(f"x - {c}" for c in range(1, 6)) + \
      tuple(f"{a} x" for a in range(2, 6)) + tuple(f"{a} x {s} {b}" for a in range(2, 5) for s in "+-" for b in range(1, 6))
QUAD = tuple(f"x^2 + {c}" for c in range(1, 10)) + tuple(f"x^2 - {c}" for c in range(1, 6)) + \
       tuple(f"2 x^2 + {c}" for c in range(1, 6))
NONPOLY = ("log(x)", "sqrt(x)")
ASK = re.compile(rf"^\(([a-z])\s*(\+|-|/|{re.escape(COMPOSE)}|)\s*([a-z])\)\((.+)\)$")
OPS5 = ("+", "+", "-", "-", " ", "/")
ARG5 = (1, 2, 3, 4, 5, 6, -1, -2, -3)
ARG6 = (-2, -1, 1, 2, 3, 4, 5)

def combo(f, op, g):
    return {"+": f"({f} + {g})", "-": f"({f} - {g})", " ": f"({f} {g})", "/": f"({f}/{g})",
            COMPOSE: f"({f} {COMPOSE} {g})"}[op]

def t4_log_pick(r):
    return dict(f=r.choice(NONPOLY), g=r.choice(QUAD + LIN), outer=r.choice("fg"))

def t4_poly_pick(r):
    return dict(f=r.choice(LIN), g=r.choice(QUAD), outer=r.choice("fg"))

def t4_ok(f, g, outer):
    return f in LIN + NONPOLY and g in QUAD + LIN and outer in "fg" and f != g

def t4(f, g, outer):
    """Example 24.5: (g ∘ f)(x) with f(x) = log x; or two polynomials, multiplied out."""
    need(t4_ok(f, g, outer))
    inner = "g" if outer == "f" else "f"
    return f"f(x) = {f}; g(x) = {g}; {combo(outer, COMPOSE, inner)}(x)"

def t5_pick(r):
    return dict(f=r.choice(LIN), g=r.choice(QUAD), op=r.choice(OPS5), n=r.choice(ARG5))

def t5_ok(f, g, op, n):
    return f in LIN and g in QUAD + LIN and op in OPS5 and n in ARG5

def t5(f, g, op, n):
    """Example 24.6, problem 14 (a)-(b): f and g at a number, then one operation."""
    need(t5_ok(f, g, op, n))
    return f"f(x) = {f}; g(x) = {g}; {combo('f', op, 'g')}({n})"

def t6_pick(r):
    return dict(f=r.choice(LIN), g=r.choice(QUAD), outer=r.choice("ffg"), n=r.choice(ARG6))

def t6_ok(f, g, outer, n):
    return f in LIN and g in QUAD + LIN and outer in "fg" and n in ARG6

def t6(f, g, outer, n):
    """Problem 14 (c): (f ∘ g)(3), the inside first."""
    need(t6_ok(f, g, outer, n))
    return f"f(x) = {f}; g(x) = {g}; {combo(outer, COMPOSE, 'g' if outer == 'f' else 'f')}({n})"

def read_ask(prompt):
    """({name: sympy}, {name: rule as written}, ask, (outer, op, inner, argument))."""
    defs, asks = AF.read(prompt)
    rules = {s.split("(", 1)[0]: s.split("=", 1)[1].strip() for s in AF.split_top(prompt, ";")[:-1]}
    if len(asks) != 1:
        raise ValueError("ask for one thing")
    m = ASK.match(asks[0])
    if not m or m.group(1) not in defs or m.group(3) not in defs:
        raise ValueError(f"write it like: f(x) = x + 2; g(x) = x^2 + 3; (f + g)(6)")
    a, op, b, arg = m.groups()
    return defs, rules, asks[0], (a, op or " ", b, arg)

def combined(defs, a, op, b, arg):
    fa, fb = defs[a], defs[b]
    if op == COMPOSE:
        return fa.subs(X, fb.subs(X, to_sympy(arg)))
    va, vb = fa.subs(X, to_sympy(arg)), fb.subs(X, to_sympy(arg))
    if op == "/":
        if vb == 0:
            raise ValueError("the bottom function is 0 there")
        return va / vb
    return {"+": va + vb, "-": va - vb, " ": va * vb}[op]

def polynomial(e):
    return e.is_polynomial(X)

def put_in(outer, inner):
    """outer's rule with inner's put in for x, as written: (log(x))^2 + 6, log(x^2 + 6), 2 sqrt(x) + 1."""
    return re.sub(r"\bx\b(\^)?", lambda m: f"({inner})^" if m.group(1) else inner,
                  outer.replace("log(x)", "log(@)").replace("sqrt(x)", "sqrt(@)")).replace("@", inner)

def answer_fn(prompt):
    defs, rules, ask, (a, op, b, arg) = read_ask(prompt)
    v = combined(defs, a, op, b, arg)
    if v.free_symbols:
        need(op == COMPOSE)
        if polynomial(defs[a]) and polynomial(defs[b]):
            return f"{ask} = {tx(sp.expand(v), 'x')}"
        return f"{ask} = {put_in(rules[a], rules[b])}"
    need(v.is_Rational)
    return f"{ask} = {v.p}/{v.q}" if v.q != 1 else f"{ask} = {v.p}"

def check_fn(prompt, answer):
    defs, rules, ask, (a, op, b, arg) = read_ask(prompt)
    lhs, eq, rhs = answer.partition("=")
    if not eq or " ".join(lhs.split()) != " ".join(ask.split()):
        return False
    want, got = combined(defs, a, op, b, arg), to_sympy(rhs.strip())
    if want.free_symbols:
        if polynomial(defs[a]) and polynomial(defs[b]) and "(" in rhs:
            return False                                   # polynomials multiplied out
        return not re.search(r"\b[fgh]\(", rhs) and same_value(tx(want) if polynomial(want) else str_typst(want),
                                                          rhs.strip())
    return got.is_Rational and sp.simplify(got - want) == 0 and simplest_form(rhs.strip()) and rhs.count("/") <= 1

def str_typst(e):
    """A sympy expression as Typst math same_value can read: log(x)**2 -> (log(x))^2."""
    return str(e).replace("**", "^")

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def answer_of(prompt, typ):
    if typ in ("1", "2"):
        return exact_sum(trig_terms(prompt))
    if typ == "3":
        ask, values = read3(prompt)
        return f"{ask} = {exact_sum(trig_terms(values))}"
    return answer_fn(prompt)

def check_trig(prompt, answer):
    return same_value(prompt, answer) and form_sum(answer)

def check(p):
    typ, prompt, answer = p["type"], p["prompt"], p["answer"]
    try:
        if typ in ("1", "2"):
            ok = check_trig(prompt, answer)
        elif typ == "3":
            ask, values = read3(prompt)
            lhs, _, rhs = answer.partition("=")
            ok = " ".join(lhs.split()) == ask and check_trig(values, rhs.strip())
        else:
            ok = check_fn(prompt, answer)
    except gen.Redraw:
        return "failed"
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

TEMPLATES = {
    "1": [(t1_pick, t1), (t1_pick, t1), (t1_coef_pick, t1)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_log_pick, t4), (t4_log_pick, t4), (t4_poly_pick, t4)],
    "5": [(t5_pick, t5)],
    "6": [(t6_pick, t6)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok, t6: t6_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    try:
        answer = answer_of(prompt, entry)
    except ValueError:                                     # (f/g) where g is 0
        raise gen.Redraw() from None
    value = answer.split("=")[-1].strip()
    if entry in "123":
        need(value != "0" and "sqrt" in value)             # a radical in the answer, as in every source
        need(not re.search(r"\d{3}", value))
    if entry in "56":
        need(not re.search(r"\d{4}", value))               # hand-sized
    return dict(prompt=prompt, answer=answer)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def shown(t):
    """Typst math as the deck shows it: sin 30°, log x, f/g with a slash."""
    t = re.sub(r"\blog\(x\)", "log x", t)
    t = re.sub(r"\(([a-z])/([a-z])\)", r"(\1\\/\2)", t)
    return trig_shown(t)

def statement(p):
    t, pr = p["type"], p["prompt"]
    if t in ("1", "2"):
        return display(shown(pr))
    if t == "3":
        rule, ask = [s.strip() for s in pr.split(";")]
        return f"If ${shown(rule.replace('(theta)', ' theta').replace(' theta =', '(theta) =', 1))}$, evaluate ${shown(ask)}$."
    parts_ = AF.split_top(pr, ";")
    defs = [f"${shown(d)}$" for d in parts_[:-1]]
    return f"If {' and '.join(defs)}, find ${shown(parts_[-1])}$."

def typst(p, gap="0.3em"):
    try:
        return statement(p)
    except (ValueError, IndexError):
        return f"${p['prompt']}$"

def answer_typst(p):
    return display(shown(p["answer"]))

def plain(t):
    t = re.sub(r"\blog\(x\)", "log x", t).replace(COMPOSE, "∘").replace("theta", "θ")
    return readable(t.replace("sqrt(", "√("))

def text(p):
    t = p["type"]
    if t in ("1", "2"):
        return plain(p["prompt"])
    try:
        s = statement(p)
    except (ValueError, IndexError):
        return p["prompt"]
    s = re.sub(r"\$([^$]*)\$", lambda m: m.group(1), s).replace("\\/", "/").replace("display(", "(")
    return plain(s)

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.55 if p["type"] in "12" else 0.4

# ------------------------------------------------------------------
# Editing: Typst math, or the functions and what to find, separated by ";"
# ------------------------------------------------------------------
EXAMPLE = {"1": "tan(45 degree) + 2 tan(30 degree)", "2": "sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)",
           "3": "f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)", "4": "f(x) = log(x); g(x) = x^2 + 6; (g circle.small f)(x)",
           "5": "f(x) = x + 2; g(x) = x^2 + 3; (f + g)(6)", "6": "f(x) = x + 3; g(x) = x^2 + 1; (f circle.small g)(3)"}

def clean(t):
    t = t.replace("−", "-").replace("∘", COMPOSE).replace("°", " degree").replace("θ", "theta").replace("√", "sqrt")
    t = re.sub(r"\blog x\b", "log(x)", t)
    t = re.sub(r"\b(sin|cos|tan) theta\b", r"\1(theta)", t)
    t = re.sub(r"\b(sin|cos|tan) (-?\d+) *degree", r"\1(\2 degree)", t)
    t = re.sub(r"\(\s*(-?\d+) +degree\)", r"(\1 degree)", t)
    return " ".join(t.split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t, typ = clean(t), old.get("type", "1")
    try:
        answer = answer_of(t, typ)
    except Exception:
        raise ValueError(f"write it like: {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
