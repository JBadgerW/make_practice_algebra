"""Lesson 29 (Advanced Math): the unit circle, very large and very small
fractions, quadrantal angles. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_029/slides/deck_029.typ): examples
29.1-29.3 and Problem Set 29, problems 17-20.

    1  one quadrantal value:            3 tan 180°,  4 sin 270°,  3 tan 270°       0,  -4,  undefined
    2  a sum of quadrantal values:      2 sin 180° - 3 cos 90° + cos 270°          0
    3  quadrantal and triangle values:  sin(-135°) + 3 sqrt(2) cos 180°           -(7 sqrt(2))/2
                                        2 sin 30° cos 30° - sin 60° + cos 90°      0
    4  functions of theta:              If f(θ) = cos θ and g(θ) = sin θ, find 3 f(60°) + g(180°).    3/2
                                        If r(θ) = (sin θ)/(cos θ) and s(θ) = cos θ + sin(θ - 300°),
                                        find (sqrt(3)/2) r(180°) + s(30°).                             (2 + sqrt(3))/2

A quadrantal angle is a multiple of 90°: no triangle, so the value is read
from the endpoint (x, y) of the unit circle's radius: cos θ = x, sin θ = y,
tan θ = y/x, undefined at 90° and 270°. Example 29.2's two parts are one
skill each, so each is its own Type 1 problem; (b) is keyed "undefined", as
the deck says. Only Type 1 draws an undefined value. Types 3 and 4 mix in the
reference-triangle values of Lessons 20 and 27 (any angle with a related
angle of 30°, 45°, or 60°).

Lesson 29.B (very large and very small fractions) is reference only: it has
no example and no Problem Set item, so it has no type.

The key writes the exact value as the deck does, in Lesson 20's form: one
fraction, rationalized, radicands square-free, with typmath.single's signs:
0, -4, 3/2, -(7 sqrt(2))/2, (2 + sqrt(3))/2. Values with two different
radicals go over one denominator: (sqrt(2) + sqrt(3))/2. "undefined" when a
tangent's x is 0.

check() works the prompt out again with sympy (Type 4: each function's rule
is put in, with θ replaced by the angle, from the prompt's text) and
compares values exactly; "undefined" must be the answer exactly when the
value is. The form: Lesson 20's rules (no trig left, no radical below,
square-free, lowest terms), one fraction at most, and no 0 left in a sum.

No skipped sources: Lesson 29 has no proofs.

A problem: dict(type, prompt, answer, source), in Typst math. Type 4's
prompt is its rules and what to find, joined by "; ":
    prompt  "f(theta) = cos(theta); g(theta) = sin(theta); 3 f(60 degree) + g(180 degree)"
    answer  "3/2"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value, parts as written_parts
from ..typmath import single, fr, display, dfrac, text as plain
from .adv_lesson_20 import simplest
from .adv_lesson_27 import POSITIVE as L27_POSITIVE, NEGATIVE as L27_NEGATIVE

NAME = FAMILY = "adv_lesson_29"
FIXED = False
TITLE = "Lesson 29: The Unit Circle, Very Large and Very Small Fractions, Quadrantal Angles"
INSTRUCTIONS = "Draw the necessary reference triangles and evaluate. Do not use a calculator."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="One Quadrantal Value",
         look="sin, cos, or tan of $0 degree$, $90 degree$, $180 degree$, or $270 degree$ (or a negative one), times a "
              "number.",
         move="Draw the unit circle and the radius at the angle. Its endpoint $(x, y)$ gives $cos theta = x$, "
              "$sin theta = y$, $tan theta = y/x$: at $180 degree$ the endpoint is $(-1, 0)$, so $tan 180 degree = "
              "0/(-1) = 0$. At $90 degree$ and $270 degree$, $tan theta = y/0$ is undefined."),
    dict(key="2", title="A Sum of Quadrantal Values",
         look="Several sines and cosines of multiples of $90 degree$.",
         move="Find each endpoint: $90 degree arrow.r (0, 1)$, $180 degree arrow.r (-1, 0)$, $270 degree arrow.r "
              "(0, -1)$. Replace each sine with $y$ and each cosine with $x$, then multiply and add.",
         width="full"),
    dict(key="3", title="Quadrantal and Reference-Triangle Values",
         look="Quadrantal angles mixed with angles like $30 degree$ or $-135 degree$.",
         move="Use the unit circle's endpoint for each multiple of $90 degree$. For the others, find the related "
              "angle and the quadrant's sign: $sin(-135 degree) = -sin 45 degree = -1/sqrt(2)$. Rationalize and "
              "add over one denominator.",
         width="full"),
    dict(key="4", title="Functions of an Angle",
         instructions="Do not use a calculator.",
         look="Functions of $theta$, like $f(theta) = cos theta$, and a sum of their values.",
         move="Put each angle in for $theta$: $s(30 degree) = cos 30 degree + sin(30 degree - 300 degree) = "
              "cos 30 degree + sin(-270 degree)$. Evaluate each value, then multiply and add.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FUNCS = ("sin", "cos", "tan")
QUAD = (0, 90, 180, 270, -90, -180, -270)
OTHER = (30, 45, 60) + L27_POSITIVE + L27_NEGATIVE       # a related angle of 30°, 45°, or 60°
WHOLE = tuple(n for n in range(-6, 7) if n)
RADICANDS = (1, 2, 3)                                    # a coefficient's: 3, 3 sqrt(2), sqrt(3)
NAMES = (("f", "g"), ("r", "s"), ("g", "h"), ("p", "q"))

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def undefined_at(f, a):
    return f == "tan" and a % 180 == 90

# ------------------------------------------------------------------
# Terms: (n, m, d, factors), the coefficient n sqrt(m)/d times sin, cos, tan values
# ------------------------------------------------------------------
def coefficient(n, m, d):
    """The coefficient as the deck writes it: 3, -, 3 sqrt(2), sqrt(3)/2 (a space after, unless empty)."""
    sign = "-" if n < 0 else ""
    n = abs(n)
    rad = f"sqrt({m})" if m > 1 else ""
    top = (rad if n == 1 else f"{n} {rad}".strip()) if rad else ("" if n == 1 and d == 1 else str(n))
    if d > 1:
        top = fr(top or "1", str(d))
    return sign + top + (" " if top else "")

def factor(f, a):
    return f"{f}({a} degree)"

def expression(terms):
    """3 tan(180 degree);  2 sin(30 degree) cos(30 degree) - sin(60 degree) + cos(90 degree)."""
    out = ""
    for i, (n, m, d, factors) in enumerate(terms):
        body = coefficient(abs(n), m, d) + " ".join(factor(f, a) for f, a in factors)
        out += ("-" if n < 0 else "") + body if i == 0 else (" - " if n < 0 else " + ") + body
    return out

def terms_ok(terms, quad_only=False, mixed=False, defined=True):
    angles = [a for *_, fs in terms for _, a in fs]
    return (all(n in WHOLE and m in RADICANDS and d in (1, 2) and 1 <= len(fs) <= 2
                and all(f in FUNCS and a in QUAD + OTHER for f, a in fs) for n, m, d, fs in terms)
            and (not quad_only or all(a in QUAD for a in angles))
            and (not mixed or (any(a in QUAD for a in angles) and any(a in OTHER for a in angles)))
            and (not defined or not any(undefined_at(f, a) for *_, fs in terms for f, a in fs)))

# ------------------------------------------------------------------
# Type 1: one quadrantal value
# ------------------------------------------------------------------
def t1(n, f, a):
    return expression([(n, 1, 1, ((f, a),))])

def t1_ok(n, f, a):
    return n in WHOLE and f in FUNCS and a in QUAD

def t1_pick(undefined):
    def pick(r):
        f = "tan" if undefined else r.choice(FUNCS)
        a = r.choice([a for a in QUAD if undefined_at(f, a) == undefined])
        p = dict(n=r.choice(WHOLE), f=f, a=a)
        need(undefined or to_sympy(t1(**p)) != 0 or r.random() < ZERO)
        return p
    return pick

# ------------------------------------------------------------------
# Types 2 and 3: sums
# ------------------------------------------------------------------
def t23(terms):
    return expression([(n, m, d, tuple(tuple(x) for x in fs)) for n, m, d, fs in terms])

def t2_ok(terms):
    return 2 <= len(terms) <= 3 and terms_ok(terms, quad_only=True) and all(m == 1 and d == 1 for n, m, d, _ in terms)

def t3_ok(terms):
    return 2 <= len(terms) <= 3 and terms_ok(terms, mixed=True)

SMALL = (-4, -3, -2, -1, 1, 2, 3, 4)       # Type 3's whole coefficients

def term(r, angles, radical=False, product=False, whole=WHOLE):
    n = r.choice(whole) if r.random() < 0.6 else r.choice((1, -1))
    m = r.choice(RADICANDS) if radical else 1
    k = 2 if product and r.random() < 0.3 else 1
    fs = []
    for _ in range(k):
        f, a = r.choice(FUNCS), r.choice(angles)
        need(not undefined_at(f, a))
        fs.append((f, a))
    return (n, m, 1, tuple(fs))

ZERO = 0.25                              # the share of drawn sums allowed to come to 0 (problems 17, 18 do)

def varied(r, terms):
    """No factor twice (no cos 0° - cos 0°), and a 0 answer only now and then."""
    fs = [x for *_, f in terms for x in f]
    need(len(set(fs)) == len(fs))
    need(to_sympy(expression(terms)) != 0 or r.random() < ZERO)

def t2_pick(r):
    terms = [term(r, QUAD) for _ in range(r.choice((2, 3, 3)))]
    need(t2_ok(terms))
    varied(r, terms)
    return dict(terms=terms)

def t3_pick(r):
    k = r.choice((2, 3))
    terms = [term(r, QUAD, radical=True, whole=SMALL)] + [term(r, OTHER, product=True, whole=SMALL)
                                                          for _ in range(k - 1)]
    r.shuffle(terms)
    need(t3_ok(terms))
    varied(r, terms)
    return dict(terms=terms)

# ------------------------------------------------------------------
# Type 4: functions of theta
# ------------------------------------------------------------------
SHIFTS = (90, 180, 270, 300, 330, 120)                   # s(θ) = F θ + G(θ - k°)

def rule(kind, f1, f2=None, k=None):
    if kind == "one":
        return f"{f1}(theta)"
    if kind == "ratio":
        return f"({f1}(theta))/({f2}(theta))"
    return f"{f1}(theta) + {f2}(theta - {k} degree)"

def t4(names, rules, asks):
    """rules: (kind, f1, f2, k) per function; asks: (coefficient (n, m, d), angle) per function."""
    defs = [f"{g}(theta) = {rule(*rl)}" for g, rl in zip(names, rules)]
    find = ""
    for i, (g, ((n, m, d), a)) in enumerate(zip(names, asks)):
        body = coefficient(abs(n), m, d) + f"{g}({a} degree)"
        find += ("-" if n < 0 else "") + body if i == 0 else (" - " if n < 0 else " + ") + body
    return "; ".join(defs + [find])

def t4_ok(names, rules, asks):
    return (tuple(names) in NAMES and len(rules) == len(asks) == 2
            and all(kind in ("one", "ratio", "shifted") and f1 in FUNCS and (f2 in FUNCS if kind != "one" else f2 is None)
                    and (k in SHIFTS if kind == "shifted" else k is None) for kind, f1, f2, k in rules)
            and all(n in WHOLE and m in RADICANDS and d in (1, 2) and a in QUAD + OTHER for (n, m, d), a in asks)
            and any(a in QUAD for _, a in asks) and not undefined(worked(t4(names, rules, asks))))

def ask(r, a):
    """The coefficient of one value asked for; sqrt(3)/2 only on a quadrantal one, as problem 20's."""
    plain = ((1, 1, 1), (1, 1, 1), (r.choice(SMALL), 1, 1))
    return r.choice(plain + ((1, r.choice((2, 3)), 2),) if a in QUAD else plain)

def t4_pick(shape):
    def pick(r):
        names = r.choice(NAMES)
        if shape == "plain":                                  # problem 19
            rules = [("one", f, None, None) for f in r.sample(FUNCS, 2)]
        else:                                                 # problem 20
            f1, f2 = r.sample(FUNCS[:2], 2)
            rules = [("ratio", f1, f2, None), ("shifted", r.choice(FUNCS[:2]), r.choice(FUNCS[:2]), r.choice(SHIFTS))]
        angles = [r.choice(QUAD), r.choice(OTHER + QUAD)]
        r.shuffle(angles)
        p = dict(names=names, rules=rules, asks=[(ask(r, a), a) for a in angles])
        need(t4_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick(False), t1), (t1_pick(False), t1), (t1_pick(False), t1), (t1_pick(True), t1)],
    "2": [(t2_pick, t23)],
    "3": [(t3_pick, t23)],
    "4": [(t4_pick("plain"), t4), (t4_pick("shifted"), t4)],
}
RANGES = {t1: t1_ok, t4: t4_ok}

def in_range(build, params, typ=None):
    """Every parameter inside its named range: the random draw can pick these. Types 2 and 3
    share their build, so name the type."""
    if build is t23:
        return bool((t2_ok if typ == "2" else t3_ok)(**params))
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def worked(prompt):
    """What to evaluate, in Typst math: each function's rule put in, θ replaced by the angle."""
    if ";" not in prompt:
        return prompt
    *defs, find = (s.strip() for s in prompt.split(";"))
    rules = {}
    for d in defs:
        m = re.fullmatch(r"(\w)\(theta\) = (.+)", d)
        rules[m.group(1)] = m.group(2)
    def put(m):
        return "(" + re.sub(r"\btheta\b", f"({m.group(2)})", rules[m.group(1)]) + ")"
    out = re.sub(r"\b(\w)\(([^()]+)\)", lambda m: put(m) if m.group(1) in rules else m.group(0), find)
    if re.search(r"\b(\w)\(", out) and any(re.search(rf"\b{g}\(", out) for g in rules):
        raise ValueError("a function left")
    return out

def undefined(text):
    v = to_sympy(text)
    return v.has(sp.zoo, sp.nan, sp.oo, -sp.oo)

def written(v):
    """The exact value as the key writes it: one fraction (see the docstring)."""
    v = sp.expand(sp.radsimp(sp.S(v)))
    out = single(v)
    if out.count("/") <= 1:
        return out
    D = math.lcm(*(int(sp.fraction(t)[1]) for t in sp.Add.make_args(sp.expand(v))))
    N = sp.expand(v * D)
    top = single(N)
    if top.startswith("-"):
        return f"-({single(-N)})/{D}"
    return f"({top})/{D}"

def answer_of(prompt):
    w = worked(prompt)
    return "undefined" if undefined(w) else written(to_sympy(w))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        w, ans = worked(p["prompt"]), " ".join(p["answer"].split())
        if undefined(w) or ans == "undefined":
            ok = undefined(w) and ans == "undefined"
        else:
            lone_zero = ans != "0" and re.search(r"(?<![\d.])0(?![\d.])", ans)      # 3/2 + 0: unfinished
            one_fraction = "/" not in ans or (ans.count("/") == 1 and written_parts(ans)[1] != 1)   # not 1 + sqrt(3)/2
            ok = same_value(w, ans) and simplest(ans) and one_fraction and not lone_zero
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: sin 180°, sin(-135°), cos θ, sin(θ - 300°)
# ------------------------------------------------------------------
TRIG = re.compile(r"\b(sin|cos|tan)\(((-?)(\d+) degree|theta)\)")

def bare(t):
    def one(m):
        if m.group(2) == "theta":
            return f"{m.group(1)} theta"
        return f"{m.group(1)}({m.group(2)})" if m.group(3) else f"{m.group(1)} {m.group(2)}"
    return TRIG.sub(one, t)

def shown(t):
    return dfrac(bare(t))

def readable(t):
    """Plain text; a coefficient fraction in parentheses, (sqrt(3)/2) r(180°), as the types file writes it."""
    t = re.sub(r"(?<![\w(])(sqrt\(\d+\)/\d+) (?=\w\()", r"(\1) ", bare(t))
    return plain(t.replace(" degree", "°").replace("theta", "θ"))

def parts(prompt):
    *defs, find = (s.strip() for s in prompt.split(";"))
    return defs, find

def typst(p, gap="0.3em"):
    if p["type"] == "4":
        defs, find = parts(p["prompt"])
        listed = " and ".join(f"${shown(d)}$" for d in defs)
        return f"If {listed}, find ${shown(find)}$."
    return "Evaluate: #h(0.5em) " + display(shown(p["prompt"]))

def answer_typst(p):
    return "undefined" if p["answer"] == "undefined" else display(shown(p["answer"]))

def text(p):
    if p["type"] == "4":
        defs, find = parts(p["prompt"])
        return f"If {' and '.join(readable(d) for d in defs)}, find {readable(find)}."
    return "Evaluate: " + readable(p["prompt"])

def answer_text(p):
    return p["answer"] if p["answer"] == "undefined" else readable(p["answer"])

def height(p):
    return 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
def clean(t):
    return " ".join(t.replace("−", "-").replace("°", " degree").replace("θ", "theta").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        answer = answer_of(t)
    except Exception:
        raise ValueError("write it in Typst math, like 3 tan(180 degree), or f(theta) = cos(theta); "
                         "g(theta) = sin(theta); 3 f(60 degree) + g(180 degree)") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
