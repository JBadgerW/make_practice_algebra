"""Trig values and polar form (Advanced Math), from the 2025-26 midterm:
sums of exact trig values, a trig function at an angle past 90°, and
converting between rectangular (x î + y ĵ) and polar (r∠θ) form.

    Type 1   "2 sin(30 degree) + sqrt(2) cos(45 degree) - sqrt(3)/2 tan(60 degree)"   exact, as the midterm
             chose coefficients so the radicals cancel
    Type 2   "f(x) = 3 sin(x); f(135 degree)"          answer "f(135 degree) = (3 sqrt(2))/2"
    Type 3   "3 hat(dotless.i) - 4 hat(dotless.j)"     answer: four polar forms, r to 0.1 and θ to 0.01°,
             "5 angle -53.13 degree, -5 angle 126.87 degree, 5 angle 306.87 degree, -5 angle -233.13 degree"
    Type 4   "6 angle 200 degree"                      answer "-5.64 hat(dotless.i) - 2.05 hat(dotless.j)"

The prompt and answer are Typst math; sin(30 degree) is shown sin 30°, as
the midterm wrote it. check() works the prompt out again: Types 1 and 2
compare exact values at random points; Types 3 and 4 read the answer's
numbers and compare them with the exact conversion, within the rounding.
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need, signed
from ..check import to_sympy, same_value, simplest_form
from ..typmath import tx, single, fr, display, dfrac, text as plain

NAME = FAMILY = "adv_trig"
FIXED = False
TITLE = "Trig Values and Polar Form"
INSTRUCTIONS = ""
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Exact Trig Values", instructions="Find the exact value.",
         look="Sines, cosines, and tangents of 30°, 45°, and 60°, with coefficients.",
         move="Replace each with its exact value from the 30-60-90 and 45-45-90 triangles: sin 30° = 1/2, "
              "cos 45° = sqrt(2)/2, tan 60° = sqrt(3), and so on. Multiply and combine."),
    dict(key="2", title="Angles Past 90°", instructions="Find the exact value.",
         look="A trig function of an angle like 135°, 210°, or 300°.",
         move="Find the reference angle (its distance to the x-axis) and the quadrant. Use the reference "
              "angle's value, with the sign the quadrant gives: All Students Take Calculus."),
    dict(key="3", title="Rectangular to Polar",
         instructions="Convert to polar form. Write four forms: r to 0.1 and θ to 0.01°.",
         look="x î + y ĵ.",
         move="r = sqrt(x^2 + y^2); θ from tan θ = y/x, in the quadrant of (x, y). The other forms: -r at "
              "θ ± 180°, and r and -r with 360° subtracted.", width="full", space="1in"),
    dict(key="4", title="Polar to Rectangular",
         instructions="Convert to rectangular form, to 0.01.",
         look="r∠θ.",
         move="x = r cos θ and y = r sin θ. Write x î + y ĵ."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
FUNCS = ("sin", "cos", "tan")
I, J = "hat(dotless.i)", "hat(dotless.j)"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def term(c, body, first=False):
    """c body as a signed term: term("-sqrt(3)/2", "tan(60 degree)") = " - sqrt(3)/2 tan(60 degree)"."""
    neg = c.startswith("-")
    c = c.lstrip("-")
    t = body if c == "1" else f"{c} {body}"
    return ("-" + t if neg else t) if first else (" - " if neg else " + ") + t

# ------------------------------------------------------------------
# Type 1: coefficients that cancel the radicals (the midterm's choice)
# ------------------------------------------------------------------
def coefficient(r, angle, f):
    """A coefficient for f(angle) so that the product has no radical."""
    s = r.choice(("", "-"))
    if angle == 45:
        k = r.randint(1, 3)
        return s + (str(r.randint(1, 5)) if f == "tan" else ("sqrt(2)" if k == 1 else f"{k} sqrt(2)"))
    plain_ = (angle == 30 and f == "sin") or (angle == 60 and f == "cos")
    if plain_:
        return s + str(2 * r.randint(1, 3))
    return s + r.choice(("sqrt(3)", fr("sqrt(3)", "2"), fr("sqrt(3)", "3")))

def exact_sum(r, n):
    out = ""
    pairs = r.sample([(a, f) for a in (30, 45, 60) for f in FUNCS], n)    # no like terms
    for i, (angle, f) in enumerate(pairs):
        out += term(coefficient(r, angle, f), f"{f}({angle} degree)", first=i == 0)
    return out

def t1_three(r):                              # the midterm
    return exact_sum(r, 3)

def t1_two(r):
    return exact_sum(r, 2)

def t1_four(r):
    return exact_sum(r, 4)

# ------------------------------------------------------------------
# Type 2: f(x) = k trig(x) at 30, 45, or 60 plus 90, 180, or 270
# ------------------------------------------------------------------
def past_90(f):
    def t(r):
        angle = r.choice((30, 45, 60)) + 90 * r.randint(1, 3)
        return f"f(x) = {term(str(signed(r, 1, 8)), f'{f}(x)', True)}; f({angle} degree)"
    return t

# ------------------------------------------------------------------
# Types 3 and 4: the conversions, rounded
# ------------------------------------------------------------------
def rect(x, y):
    return f"{x} {I} {'-' if y < 0 else '+'} {abs(y)} {J}"

def t3_quadrant(xs, ys):
    def t(r):
        return rect(xs * r.randint(2, 12), ys * r.randint(2, 12))
    return t

def polar(r_, theta):
    return f"{r_} angle {theta} degree"

def t4_range(lo, hi):
    def t(r):
        theta = r.randint(lo, hi)
        need(theta % 90)                                  # not on an axis
        return polar(r.randint(2, 12), theta)
    return t

TEMPLATES = {
    "1": [t1_three, t1_two, t1_four],
    "2": [past_90(f) for f in FUNCS],
    "3": [t3_quadrant(1, 1), t3_quadrant(-1, 1), t3_quadrant(-1, -1), t3_quadrant(1, -1)],
    "4": [t4_range(1, 180), t4_range(181, 359), t4_range(-359, -1)],
}

# ------------------------------------------------------------------
# Solving
# ------------------------------------------------------------------
RECT = re.compile(rf"^(-?\d+) {re.escape(I)} ([+-]) (\d+) {re.escape(J)}$")
POLAR = re.compile(r"^(-?\d+(?:\.\d+)?) angle (-?\d+(?:\.\d+)?) degree$")
NUM = r"-?\d+(?:\.\d+)?"

def read_rect(t):
    m = RECT.match(" ".join(t.split()))
    if not m:
        raise ValueError(f"write it like 3 {I} - 4 {J}")
    return int(m.group(1)), int(m.group(3)) * (1 if m.group(2) == "+" else -1)

def read_polar(t):
    m = POLAR.match(" ".join(t.split()))
    if not m:
        raise ValueError("write it like 6 angle 200 degree")
    return float(m.group(1)), float(m.group(2))

def two(v):
    return f"{v:.2f}"

def forms(x, y):
    """The four polar forms of (x, y): r at θ and at θ - 360; -r at θ ± 180 and that - 360."""
    r_ = math.hypot(x, y)
    th = math.degrees(math.atan2(y, x)) % 360
    th2 = th + 180 if th < 180 else th - 180
    return [(r_, th), (-r_, th2), (r_, th - 360), (-r_, th2 - 360)]

def answer_of(typ, prompt):
    if typ in ("1", "2"):
        if typ == "1":
            return single(sp.radsimp(to_sympy(prompt)))
        rule, ask = (s.strip() for s in prompt.split(";"))
        f = to_sympy(rule.split("=", 1)[1])
        arg = re.match(r"^f\((.+)\)$", ask).group(1)
        return f"{ask} = {single(sp.radsimp(f.subs(sp.Symbol('x'), to_sympy(arg))))}"
    if typ == "3":
        return ", ".join(polar(f"{r_:.1f}", two(th)) for r_, th in forms(*read_rect(prompt)))
    r_, th = read_polar(prompt)
    x, y = r_ * math.cos(math.radians(th)), r_ * math.sin(math.radians(th))
    return f"{two(x)} {I} {'-' if round(y, 2) < 0 else '+'} {two(abs(y))} {J}"

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    answer = answer_of(entry, prompt)
    if entry == "1":
        need(answer not in ("0",) and simplest_form(answer))
    return dict(prompt=prompt, answer=answer)

def check(p):
    try:
        typ, prompt, answer = p["type"], p["prompt"], p["answer"]
        if typ == "1":
            ok = same_value(prompt, answer) and simplest_form(answer)
        elif typ == "2":
            ask, _, value = answer.partition("=")
            rule, want_ask = (s.strip() for s in prompt.split(";"))
            arg = re.match(r"^f\((.+)\)$", want_ask).group(1)
            f = to_sympy(rule.split("=", 1)[1]).subs(sp.Symbol("x"), to_sympy(arg))
            ok = " ".join(ask.split()) == want_ask and same_value(value.strip(), tx(f)) \
                and simplest_form(value.strip())
        elif typ == "3":
            x, y = read_rect(prompt)
            got = [read_polar(f) for f in answer.split(",")]
            want = forms(x, y)
            ok = len(got) == 4 and all(abs(a - b) <= 0.051 and abs(c - d) <= 0.0051
                                       for (a, c), (b, d) in zip(got, want))
        else:
            r_, th = read_polar(prompt)
            nums = re.findall(rf"({NUM}) {re.escape(I)} ([+-]) ({NUM}) {re.escape(J)}", answer)
            (x, s, y), = nums
            y = float(y) * (1 if s == "+" else -1)
            ok = abs(float(x) - r_ * math.cos(math.radians(th))) <= 0.0051 and \
                abs(y - r_ * math.sin(math.radians(th))) <= 0.0051
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: sin(30 degree) as sin 30°, and ∠ for angle
# ------------------------------------------------------------------
TRIG_ARG = re.compile(r"\b(sin|cos|tan)\((-?\d+) degree\)")

def shown(t):
    t = TRIG_ARG.sub(r"\1 \2 degree", t).replace("angle -", 'angle class("unary", -)')   # ∠−59.04°, a sign
    return dfrac(t)

def typst(p, gap="0.3em"):
    if p["type"] == "2":
        rule, ask = (s.strip() for s in p["prompt"].split(";"))
        return f"${shown(rule)}$; #h({gap}) ${shown(ask)}$"
    return display(shown(p["prompt"]))

def answer_typst(p):
    if p["type"] == "3":
        return ", #h(0.5em) ".join(f"${shown(f.strip())}$" for f in p["answer"].split(","))
    return display(shown(p["answer"]))

def readable(t):
    return plain(TRIG_ARG.sub(r"\1 \2°", t).replace(" degree", "°").replace(" angle ", "∠")
                 .replace(I, "î").replace(J, "ĵ"))

def text(p):
    return readable(p["prompt"])

def answer_text(p):
    return readable(p["answer"])

def height(p):
    return 0.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        answer = answer_of(old["type"], t)
    except Exception:
        raise ValueError(f"write it like the problem it replaces: {old['prompt']}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
