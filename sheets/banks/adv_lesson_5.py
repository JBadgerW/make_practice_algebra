"""Lesson 5 (Advanced Math): exponents and radicals, complex numbers, areas of
similar geometric figures, diagonals of rectangular solids. From the Saxon
lesson and its deck (~/Documents/adv_math/problem_sets/ps_005/slides/deck_005.typ):
examples 5.1-5.11 and Problem Set 5, problems 6-17 and 19.

    1  radicals as fractional exponents:   sqrt(x^3 y) root(4, x y^3)                    = x^(7/4) y^(5/4)
    2  variable exponents:                 (a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))  = a^((-5 x)/2) y^((2 + 3 x)/2)
    3  negative exponents, complex fraction: (x^(-2) + y^(-2))/(x y)^(-1)               = (x^2 + y^2)/(x y)
    4  adding radicals, rationalized:      3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)        = (25 sqrt(6))/6
    5  multiplying radical binomials:      (sqrt(2) + sqrt(x))(1 - sqrt(x))              = sqrt(2) + (1 - sqrt(2)) sqrt(x) - x
    6  powers of i:                        3 i^3 + 2 i^5 - 3 i + 2 i^2                   = -2 - 4 i
    7  square roots of negative numbers:   sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9)        = -9 sqrt(2) + 2 sqrt(3) i
    8  ratio of areas of similar figures:  the radii are R and (3R)/5; first to second   = 25/9
    9  the diagonal of a rectangular solid: base edges 2 and 3, height m                 = sqrt(13 + m^2)

The key writes what the deck writes:
  1  one power of each letter, alphabetical, the exponent one fraction in lowest
     terms: x^(7/4) y^(5/4), x^(37/12) y^(1/2).
  2  every power in the numerator, as the deck does, so an exponent may be
     negative: a^((-5 x)/2). Each exponent is one fraction in lowest terms. Its
     terms go in the order the problem writes them: the letters in the order they
     first appear in that base's exponents, the number last, unless the base's
     first exponent starts with its number (y^(2 - x) gives (2 + 3 x)/2;
     y^(x + 3) gives (2 x + a + 4)/2), and a positive term first ((4 a - x)/3).
  3  one fraction in lowest terms, positive exponents: (x^2 + y^2)/(x y).
  4  one fraction, denominator rationalized, radicands square-free: (25 sqrt(6))/6, 4 sqrt(6).
  5  three terms: the number, the sqrt(x) term, the x term. When the two middle
     products are like terms they combine (2 sqrt(3 x)); when not, sqrt(x) is
     factored out and its coefficient written as a sum, in the order the
     products arise, a positive term first, or a minus in front when both are
     negative: sqrt(2) + (1 - sqrt(2)) sqrt(x) - x, sqrt(2) - (sqrt(2) + 1) sqrt(x) + x.
  6  a + b i: -2 - 4 i, 1 - i.
  7  the real part, then the imaginary part; a part with two terms in parentheses,
     its terms in the order they arise, a positive term first:
     (4 - 9 sqrt(2)) + (2 sqrt(3) + 4) i, -9 sqrt(2) + 2 sqrt(3) i, (4 + 3 sqrt(2)) i.
  8  a fraction in lowest terms, the areas in the order the question asks
     (25/9, 4/25); for a scale factor alone, "16 to 1, or 1 to 16".
  9  the length alone: sqrt(x^2 + y^2 + z^2), the number first: sqrt(13 + m^2);
     all numbers, simplified: sqrt(29), 3 sqrt(5), 7.

check() is independent of how a problem was built. Types 1-7 read the prompt
and the answer back with sympy (root(n, t) as t^(1/n), i as the imaginary unit
in Types 6-7), compare values (exactly for Types 1-2), and read the answer's
form from its text: one power per letter and reduced exponents (1-2), lowest
terms (3), square-free radicands and no radical below (4), one term per power
of sqrt(x) (5), standard form with like terms combined (6-7). Type 8 reads the
two sizes back out of the problem and squares their ratio. Type 9 reads the
three edges and compares sqrt(w^2 + d^2 + h^2), with the radicand's numbers
combined and each letter squared once.

No skipped sources: Lesson 5 has no proofs.

A problem: dict(type, prompt, answer, source). Types 1-7: Typst math.
Type 8's prompt is the question's data: "scale 4, rectangles", "one circle R,
(3 R)/5; first", "big circle R, 2/5 R, meters; small". Type 9's is the figure's:
"BH; x, y, z" (all eight corners lettered, the book's 5.10), "CA; 2, 3, m"
(A, B, C only, C at the front right, the book's 5.11; "; C left" mirrors it);
the edges are the front bottom, the right side going back, and the height.
    prompt  "sqrt(x^3 y) root(4, x y^3)"
    answer  "x^(7/4) y^(5/4)"
"""

import math, re
from fractions import Fraction
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value, simplest_form
from ..typmath import single, tx, display, dfrac, text as plain_math
from .adv_lesson_20 import simplest as rationalized, squarefree
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_5"
FIXED = False
TITLE = "Lesson 5: Exponents and Radicals, Complex Numbers, Areas of Similar Geometric Figures, Diagonals of Rectangular Solids"
INSTRUCTIONS = "Simplify."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(
        key="1",
        title="Radicals as Fractional Exponents",
        look="Square roots and other roots multiplied together, maybe with fractional powers.",
        move="Write each radical as a fractional exponent: $sqrt(t)$ is $t^(1/2)$, $root(4, t)$ is $t^(1/4)$. "
             "Multiply the exponents inside by the outside one, then add the exponents of like bases.",
    ),
    dict(
        key="2",
        title="Variable Exponents",
        look="Powers whose exponents have letters in them, in a fraction.",
        move="Move every power to the numerator (change the sign of the exponents below). Multiply a power of a "
        "power. Add the exponents of each base over a common denominator.",
        space="1.25in",
    ),
    dict(
        key="3",
        title="Negative Exponents in a Complex Fraction",
        look="A sum of powers with negative exponents over a power of a product.",
        move="Write each negative exponent as a fraction: $x^(-2)$ is $1/x^2$. Add the fractions on top, then "
             "divide by multiplying by the reciprocal of the bottom.",
        space="1.25in",
    ),
    dict(
        key="4",
        title="Adding Radicals with Rationalized Denominators",
        look="Square roots of fractions added to a square root of a whole number.",
        move="Write $sqrt(3/2)$ as $sqrt(3)/sqrt(2)$ and rationalize: $(sqrt(3) sqrt(2))/2 = sqrt(6)/2$. "
             "Simplify the whole radical ($sqrt(24) = 2 sqrt(6)$), write every term over the common "
             "denominator, and add.",
        space="1.25in",
    ),
    dict(
        key="5",
        title="Multiplying Radical Binomials",
        look="Two binomials with $sqrt(x)$ in each, multiplied.",
        move="Multiply each term by each term; $sqrt(a) sqrt(b) = sqrt(a b)$ and $sqrt(x) sqrt(x) = x$. "
             "Combine the two middle terms: add them when they are like terms, or factor $sqrt(x)$ out of "
             "them.",
    ),
    dict(
        key="6",
        title="Powers of i",
        look="A sum of terms with powers of $i$.",
        move="Pair the $i$'s: each $i i$ is $-1$, so $i^2 = -1$, $i^3 = -i$, $i^4 = 1$, $i^5 = i$. Collect the "
             "real terms and the $i$ terms, and write $a + b i$.",
    ),
    dict(
        key="7",
        title="Square Roots of Negative Numbers",
        look="Square roots of negative numbers multiplied together.",
        move="First write each square root of a negative number with $i$: $sqrt(-3) = sqrt(3) i$, $sqrt(-9) = "
             "3 i$. Only then multiply ($i i = -1$). Group the real terms, then the $i$ terms.",
        space="1.25in",
    ),
    dict(
        key="8",
        title="Ratio of Areas of Similar Figures",
        look="Two similar figures, a scale factor or two radii, and the ratio of their areas.",
        move="Write each area with its dimensions ($pi R^2$ and $pi ((3 R)/5)^2$) and divide in the order "
             "asked. The ratio of the areas is the square of the scale factor.",
        instructions="Answer each question.",
    ),
    dict(
        key="9",
        title="Diagonal of a Rectangular Solid",
        look="A rectangular solid with its edges labeled and a diagonal from one corner to the far corner.",
        move="Step 1: the diagonal of the base is the hypotenuse of a right triangle whose legs are two base edges. "
        "Step 2: the solid's diagonal is the hypotenuse of a right triangle whose legs are the base diagonal "
        "and the height.",
        instructions="Find the length of the diagonal. Do a two-step development: the diagonal of the base first.",
    ),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()


def initial_seen():
    return set()


def seen_key(p):
    return (NAME, p["type"], p["prompt"])


# ------------------------------------------------------------------
# Reading Typst math: root(n, t) is t^(1/n); letters are positive
# ------------------------------------------------------------------
ROOT = re.compile(r"root\((\d+),\s*([^()]*(?:\([^()]*\)[^()]*)*)\)")


def unroot(t):
    return ROOT.sub(lambda m: f"(({m.group(2)})^(1/{m.group(1)}))", t)


def positive(e):
    return e.subs({s: sp.Symbol(s.name, positive=True) for s in e.free_symbols})


def sym(t, imaginary=False):
    return positive(to_sympy(unroot(t), imaginary))


def split_top(t, sep=" "):
    """t split at `sep` outside parentheses."""
    out, depth, cur = [], 0, ""
    for ch in t:
        depth += {"(": 1, ")": -1}.get(ch, 0)
        if ch == sep and depth == 0:
            if cur:
                out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def terms(t):
    """The signed terms of a sum, outside parentheses: "a - (b + c) d + e" -> ["a", "-(b + c) d", "+e"]."""
    out, depth, cur = [], 0, ""
    i = 0
    while i < len(t):
        ch = t[i]
        depth += {"(": 1, ")": -1}.get(ch, 0)
        if (
            depth == 0
            and ch in "+-"
            and cur.strip()
            and t[i - 1] == " "
            and t[i + 1 : i + 2] == " "
        ):
            out.append(cur.strip())
            cur = ch
            i += 2
            continue
        cur += ch
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return [s[1:].strip() if s.startswith("+") else s for s in out]


def coef(c):
    """A coefficient as written before a letter or radical: "" for 1, "-" for -1."""
    return {1: "", -1: "-"}.get(c, f"{c} ")


def signed_join(items):
    """["3 x", "-2 y", "4"] -> "3 x - 2 y + 4"."""
    out = items[0]
    for s in items[1:]:
        out += f" - {s[1:]}" if s.startswith("-") else f" + {s}"
    return out


def positive_first(items, value):
    """The items in order, with the first positive one moved to the front when the first is negative."""
    if value(items[0]) < 0:
        for i, it in enumerate(items):
            if value(it) > 0:
                return [it] + items[:i] + items[i + 1 :]
    return items


# ------------------------------------------------------------------
# Type 1: sqrt(x^3 y) root(4, x y^3), x^(1/2) x^(3/4) sqrt(x y) root(3, x^4)
# ------------------------------------------------------------------
LETTERS1 = (("x", "y"), ("x", "y"), ("x", "y"), ("a", "b"), ("m", "n"))
EXP1 = range(1, 6)
ROOTS1 = (3, 4)
FRACS1 = ("1/2", "1/3", "2/3", "1/4", "3/4", "3/2", "5/4")


def pw(base, e):
    """base^e as written: "x", "x^3", "x^(-2)", "x^(1/2)"; "" for 0."""
    if e == 0:
        return ""
    if e == 1:
        return base
    t = str(e)
    return f"{base}^{t}" if t.isalnum() else f"{base}^({t})"


def mono(*powers):
    return " ".join(s for s in (pw(b, e) for b, e in powers) if s)


def t1_two_pick(r):
    u, v = r.choice(LETTERS1)
    return dict(
        u=u,
        v=v,
        a=r.choice(EXP1),
        b=r.choice(EXP1),
        n=r.choice(ROOTS1),
        c=r.choice(EXP1),
        d=r.choice(EXP1),
    )


def t1_two_ok(u, v, a, b, n, c, d):
    return (
        a in EXP1
        and b in EXP1
        and c in EXP1
        and d in EXP1
        and n in ROOTS1
        and (u, v) in LETTERS1
        and (a % 2 or b % 2)
        and (c % n or d % n)
    )


def t1_two(u, v, a, b, n, c, d):
    """Example 5.1, problem 7: a square root times another root, each of a product."""
    need(t1_two_ok(u, v, a, b, n, c, d))
    return f"sqrt({mono((u, a), (v, b))}) root({n}, {mono((u, c), (v, d))})"


def t1_mixed_pick(r):
    u, v = r.choice(LETTERS1)
    return dict(
        u=u,
        v=v,
        f1=r.choice(FRACS1),
        f2=r.choice(FRACS1),
        a=r.randint(1, 3),
        b=r.randint(1, 3),
        n=r.choice(ROOTS1),
        c=r.choice(EXP1),
    )


def t1_mixed_ok(u, v, f1, f2, a, b, n, c):
    return (
        (u, v) in LETTERS1
        and f1 in FRACS1
        and f2 in FRACS1
        and f1 != f2
        and 1 <= a <= 3
        and 1 <= b <= 3
        and n in ROOTS1
        and c in EXP1
        and c % n
        and (a % 2 or b % 2)
    )


def t1_mixed(u, v, f1, f2, a, b, n, c):
    """Problem 8: two fractional powers, a square root of a product, and a root of a power."""
    need(t1_mixed_ok(u, v, f1, f2, a, b, n, c))
    return f"{u}^({f1}) {u}^({f2}) sqrt({mono((u, a), (v, b))}) root({n}, {pw(u, c)})"


def powers(e):
    """{base name: exponent} of a product of powers of letters."""
    e = sp.powsimp(sp.expand_power_base(e, force=True), force=True)
    out = {}
    for f in sp.Mul.make_args(e):
        b, x = f.as_base_exp()
        need(isinstance(b, sp.Symbol))
        out[b.name] = out.get(b.name, 0) + x
    return out


def exp_text(e):
    """A rational exponent as the key writes it: "x", "x^3", "x^(7/4)"."""
    return str(e) if e.q == 1 else f"({e.p}/{e.q})" if e.p > 0 else f"(-{-e.p}/{e.q})"


def answer1(prompt):
    ps = powers(sym(prompt))
    need(all(isinstance(x, sp.Rational) and x != 0 for x in ps.values()))
    need(
        any(x.q > 1 for x in ps.values())
    )  # a fractional exponent left, as in the book's
    return " ".join(
        b if x == 1 else f"{b}^{exp_text(x)}" for b, x in sorted(ps.items())
    )


POW1 = re.compile(r"^([a-z])(?:\^(\d+|\((\d+)/(\d+)\)))?$")


def form1(answer):
    """One power of each letter, each exponent a whole number or a fraction in lowest terms."""
    bases = []
    for f in split_top(answer):
        m = POW1.match(f)
        if not m:
            return False
        if m.group(3) and (
            math.gcd(int(m.group(3)), int(m.group(4))) != 1 or int(m.group(4)) == 1
        ):
            return False
        if m.group(2) and m.group(2) in ("0", "1"):
            return False
        bases.append(m.group(1))
    return len(bases) == len(set(bases))


def exact(prompt, answer):
    """The same power of each letter, exactly: exponents compared term by term."""
    a, b = powers(sym(prompt)), powers(sym(answer))
    return set(a) == set(b) and all(sp.expand(a[k] - b[k]) == 0 for k in a)


def check1(prompt, answer):
    return form1(answer) and exact(prompt, answer)


# ------------------------------------------------------------------
# Type 2: (a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x)),
#         (y^(x + 3) y^(x/2 - 1) z^a)/(y^((x - a)/2) z^((x - a)/3))
# ------------------------------------------------------------------
LETTERS2 = (
    ("a", "y", "x"),
    ("a", "y", "x"),
    ("b", "z", "n"),
    ("m", "y", "k"),
    ("a", "b", "x"),
)
PQ2 = ((1, 2), (1, 3), (2, 3), (3, 2), (1, 4), (3, 4))
LETTERS2B = (
    ("y", "z", "x", "a"),
    ("y", "z", "x", "a"),
    ("a", "b", "x", "n"),
    ("p", "q", "m", "n"),
)


def lin(k, x):
    """k x as written: "x", "-x", "3 x"."""
    return f"{coef(k)}{x}"


def frac_x(p, q, x):
    return f"{x}/{q}" if p == 1 else f"({p} {x})/{q}"


def t2_quot_pick(r):
    a, y, x = r.choice(LETTERS2)
    p, q = r.choice(PQ2)
    return dict(
        a=a,
        y=y,
        x=x,
        p=p,
        q=q,
        m=r.randint(1, 5),
        sx=r.choice("+-"),
        n=r.choice((2, 3)),
        k=r.randint(2, 5),
        j=r.randint(1, 3),
        sj=r.choice("+-"),
    )


def t2_quot_ok(a, y, x, p, q, m, sx, n, k, j, sj):
    return (
        (a, y, x) in LETTERS2
        and (p, q) in PQ2
        and 1 <= m <= 5
        and sx in "+-"
        and n in (2, 3)
        and 2 <= k <= 5
        and 1 <= j <= 3
        and sj in "+-"
    )


def t2_quot(a, y, x, p, q, m, sx, n, k, j, sj):
    """Example 5.2, problem 9: a power of a power on top, a power with a negative exponent below."""
    need(t2_quot_ok(a, y, x, p, q, m, sx, n, k, j, sj))
    bottom = lin(-j if sj == "-" else j, x)
    return f"({a}^({frac_x(p, q, x)}) ({y}^({m} {sx} {x}))^(1/{n}))/({a}^({k} {x}) {y}^({bottom}))"


def t2_three_pick(r):
    y, z, x, a = r.choice(LETTERS2B)
    return dict(
        y=y,
        z=z,
        x=x,
        a=a,
        c1=r.choice((-4, -3, -2, -1, 1, 2, 3, 4)),
        c2=r.choice((-3, -2, -1, 1, 2, 3)),
        h=r.choice((2, 3)),
        d1=r.choice((2, 3)),
        d2=r.choice((2, 3)),
    )


def t2_three_ok(y, z, x, a, c1, c2, h, d1, d2):
    return (
        (y, z, x, a) in LETTERS2B
        and c1
        and -4 <= c1 <= 4
        and c2
        and -3 <= c2 <= 3
        and h in (2, 3)
        and d1 in (2, 3)
        and d2 in (2, 3)
    )


def plus(c):
    return f"+ {c}" if c > 0 else f"- {-c}"


def t2_three(y, z, x, a, c1, c2, h, d1, d2):
    """Problem 10: three powers over two, the exponents sums with two letters."""
    need(t2_three_ok(y, z, x, a, c1, c2, h, d1, d2))
    return (
        f"({y}^({x} {plus(c1)}) {y}^({x}/{h} {plus(c2)}) {z}^{a})/"
        f"({y}^(({x} - {a})/{d1}) {z}^(({x} - {a})/{d2}))"
    )


def exponent_texts(prompt, base):
    """The exponents written on `base` in the prompt, in order."""
    out = []
    for m in re.finditer(rf"(?<![A-Za-z]){base}\^", prompt):
        i = m.end()
        if prompt[i] == "(":
            depth, j = 0, i
            while True:
                depth += {"(": 1, ")": -1}.get(prompt[j], 0)
                if depth == 0:
                    break
                j += 1
            out.append(prompt[i + 1 : j])
        else:
            out.append(re.match(r"\w+", prompt[i:]).group(0))
    return out


def exponent2(e, order, number_first):
    """A letter exponent as the key writes it: "x/2", "(-5 x)/2", "(2 + 3 x)/2", "x + 2", "-3"."""
    e = sp.expand(e)
    syms = sorted(
        e.free_symbols, key=lambda s: order.index(s.name) if s.name in order else 99
    )
    c = {s: e.coeff(s) for s in syms}
    k = e.subs({s: 0 for s in syms})
    den = math.lcm(*[sp.Rational(v).q for v in list(c.values()) + [k]])
    items = [(c[s] * den, s.name) for s in syms if c[s]]
    if k:
        items.insert(0, (k * den, "")) if number_first else items.append((k * den, ""))
    items = positive_first(items, lambda it: it[0])
    words = [str(v) if not s else lin(int(v), s) for v, s in items]
    top = signed_join(words)
    if den == 1:
        return top if re.fullmatch(r"\w+", top) else f"({top})"
    if re.fullmatch(r"\w+", top):
        return f"({top}/{den})"
    return f"(({top})/{den})"


def answer2(prompt):
    ps = powers(sym(prompt))
    letters = re.findall(r"[a-z]", prompt)
    out = []
    for b, x in sorted(ps.items()):
        need(x != 0)
        texts = exponent_texts(prompt, b)
        names = [s for s in re.findall(r"[a-z]", " ".join(texts))]
        order = list(dict.fromkeys(names + letters))
        first = texts[0].lstrip("(") if texts else ""
        lead = bool(re.match(r"-?\d", first))
        out.append(b if x == 1 else f"{b}^{exponent2(x, order, lead)}")
    return " ".join(out)


POW2 = re.compile(r"^([a-z])(?:\^(.+))?$")


def form2(answer):
    """One power of each letter, none below a fraction bar; each exponent one fraction in lowest
    terms, its like terms combined."""
    bases = []
    for f in split_top(answer):
        m = POW2.match(f)
        if not m:
            return False
        bases.append(m.group(1))
        x = m.group(2)
        if x is None:
            continue
        x = (
            x[1:-1]
            if x.startswith("(")
            and x.endswith(")")
            and len(split_top(x[1:-1], "/")) <= 2
            else x
        )
        parts = split_top(x, "/")
        if len(parts) > 2:
            return False
        top = parts[0][1:-1] if parts[0].startswith("(") else parts[0]
        if "/" in top:
            return False
        n = sp.expand(to_sympy(top))
        if len(terms(top)) != len(sp.Add.make_args(n)):
            return False
        if len(parts) == 2:
            d = int(parts[1])
            content = sp.Poly(n, *n.free_symbols).content() if n.free_symbols else n
            if d <= 1 or math.gcd(int(content), d) != 1:
                return False
    return len(bases) == len(set(bases))


def check2(prompt, answer):
    return form2(answer) and exact(prompt, answer)


# ------------------------------------------------------------------
# Type 3: (x^(-2) + y^(-2))/(x y)^(-1)
# ------------------------------------------------------------------
LETTERS3 = (("x", "y"), ("x", "y"), ("a", "b"), ("m", "n"), ("p", "q"))
COEF3 = (1, 1, 1, 2, 3)


def t3_power_pick(r):
    x, y = r.choice(LETTERS3)
    return dict(
        x=x,
        y=y,
        a=r.choice(COEF3),
        m=r.randint(1, 3),
        s=r.choice("+-"),
        b=r.choice(COEF3),
        n=r.randint(1, 3),
        k=r.choice((1, 1, 2)),
    )


def t3_power_ok(x, y, a, m, s, b, n, k):
    return (
        (x, y) in LETTERS3
        and a in COEF3
        and b in COEF3
        and 1 <= m <= 3
        and 1 <= n <= 3
        and s in "+-"
        and k in (1, 2)
    )


def t3_power(x, y, a, m, s, b, n, k):
    """Example 5.3, problem 14: over a power of a product."""
    need(t3_power_ok(x, y, a, m, s, b, n, k))
    return f"({coef(a)}{x}^(-{m}) {s} {coef(b)}{y}^(-{n}))/({x} {y})^(-{k})"


def t3_mono_pick(r):
    x, y = r.choice(LETTERS3)
    return dict(
        x=x,
        y=y,
        m=r.randint(1, 3),
        s=r.choice("+-"),
        n=r.randint(1, 3),
        p=r.randint(1, 3),
        q=r.randint(1, 3),
    )


def t3_mono_ok(x, y, m, s, n, p, q):
    return (x, y) in LETTERS3 and all(1 <= v <= 3 for v in (m, n, p, q)) and s in "+-"


def t3_mono(x, y, m, s, n, p, q):
    """The same move over a product of powers with negative exponents."""
    need(t3_mono_ok(x, y, m, s, n, p, q))
    return f"({x}^(-{m}) {s} {y}^(-{n}))/({pw(x, -p)} {pw(y, -q)})"


def answer3(prompt):
    a = single(sp.together(sym(prompt)))
    need(
        "/" in a and not a.startswith("-") and not re.search(r"\d{3}", a)
    )  # a fraction, led by a plus; small numbers
    return a


def check3(prompt, answer):
    return (
        simplest_form(answer)
        and answer.count("/") <= 1
        and "sqrt" not in answer
        and same_value(prompt, answer)
    )


# ------------------------------------------------------------------
# Type 4: 3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)
# ------------------------------------------------------------------
PAIRS4 = ((3, 2), (2, 3), (5, 2), (2, 5), (5, 3), (3, 5), (7, 2), (2, 7))
COEF4 = range(1, 6)
SQ4 = (2, 3)
MAX4 = 60  # the whole radical's radicand


def t4_pick(r):
    p, q = r.choice(PAIRS4)
    return dict(
        a=r.choice(COEF4),
        p=p,
        q=q,
        s1=r.choice("+-"),
        b=r.choice(COEF4),
        s2=r.choice("+-"),
        c=r.choice(COEF4),
        k=r.choice(SQ4),
    )


def t4_ok(a, p, q, s1, b, s2, c, k):
    return (
        (p, q) in PAIRS4
        and a in COEF4
        and b in COEF4
        and c in COEF4
        and s1 in "+-"
        and s2 in "+-"
        and k in SQ4
        and k * k * p * q <= MAX4
    )


def t4(a, p, q, s1, b, s2, c, k):
    """Example 5.4, problem 11: sqrt(p/q), sqrt(q/p), and a whole radical, all multiples of sqrt(p q)."""
    need(t4_ok(a, p, q, s1, b, s2, c, k))
    return f"{coef(a)}sqrt({p}/{q}) {s1} {coef(b)}sqrt({q}/{p}) {s2} {coef(c)}sqrt({k * k * p * q})"


def answer4(prompt):
    v = sp.radsimp(sym(prompt))
    need(v != 0)
    return single(v)


def check4(prompt, answer):
    return rationalized(answer) and same_value(prompt, answer)


# ------------------------------------------------------------------
# Type 5: (sqrt(2) + sqrt(x))(1 - sqrt(x)), (sqrt(3) + sqrt(x))(sqrt(3) + sqrt(x))
# ------------------------------------------------------------------
RAD5 = (2, 3, 5, 6, 7, 10, 11)
WHOLE5 = range(1, 6)
VAR5 = ("x", "x", "x", "y", "a", "t", "n")


def t5_mixed_pick(r):
    return dict(
        p=r.choice(RAD5),
        s1=r.choice("+-"),
        n=r.choice(WHOLE5),
        s2=r.choice("+-"),
        x=r.choice(VAR5),
    )


def t5_mixed_ok(p, s1, n, s2, x):
    return p in RAD5 and n in WHOLE5 and s1 in "+-" and s2 in "+-" and x in VAR5


def t5_mixed(p, s1, n, s2, x):
    """Example 5.5, problem 13: (sqrt(p) ± sqrt(x))(n ± sqrt(x)); the middle terms aren't like terms."""
    need(t5_mixed_ok(p, s1, n, s2, x))
    return f"(sqrt({p}) {s1} sqrt({x}))({n} {s2} sqrt({x}))"


def t5_square_pick(r):
    return dict(p=r.choice(RAD5), s=r.choice("+-"), x=r.choice(VAR5))


def t5_square_ok(p, s, x):
    return p in RAD5 and s in "+-" and x in VAR5


def t5_square(p, s, x):
    """Problem 12: a binomial times itself; the middle terms are like terms."""
    need(t5_square_ok(p, s, x))
    return f"(sqrt({p}) {s} sqrt({x}))(sqrt({p}) {s} sqrt({x}))"


def surd(c, r):
    """c sqrt(r), simplified: (c k, r / k^2)."""
    k = max(k for k in range(1, math.isqrt(r) + 1) if r % (k * k) == 0)
    return c * k, r // (k * k)


def surd_text(c, r):
    """c sqrt(r) as written: "3", "sqrt(2)", "-2 sqrt(3)"."""
    return str(c) if r == 1 else f"{coef(c)}sqrt({r})"


def combine(items):
    """[(c, r)] with like radicals added, each where it first appears, zeros dropped."""
    out = {}
    for c, r in items:
        c, r = surd(c, r)
        out[r] = out.get(r, 0) + c
    return [(c, r) for r, c in out.items() if c]


def surd_value(it):
    return it[0] * math.sqrt(it[1])


def group(items):
    """Two or more terms as one coefficient: ("(1 - sqrt(2))", +1) or ("(sqrt(2) + 1)", -1)."""
    if all(surd_value(it) < 0 for it in items):
        return f"({signed_join([surd_text(-c, r) for c, r in items])})", -1
    return (
        f"({signed_join([surd_text(c, r) for c, r in positive_first(items, surd_value)])})",
        1,
    )


BINOMIAL = re.compile(
    r"^\((sqrt\(\d+\)|\d+) ([+-]) sqrt\(([a-z])\)\)\((sqrt\(\d+\)|\d+) ([+-]) sqrt\(([a-z])\)\)$"
)


def number5(t):
    m = re.fullmatch(r"sqrt\((\d+)\)", t)
    return (1, int(m.group(1))) if m else (int(t), 1)


def answer5(prompt):
    m = BINOMIAL.match(prompt)
    if not m or m.group(3) != m.group(6):
        raise ValueError("not two binomials like (sqrt(2) + sqrt(x))(1 - sqrt(x))")
    (c1, r1), s1, x = number5(m.group(1)), (1 if m.group(2) == "+" else -1), m.group(3)
    (c2, r2), s2 = number5(m.group(4)), (1 if m.group(5) == "+" else -1)
    const = surd(c1 * c2, r1 * r2)
    middle = combine(
        [(c1 * s2, r1), (s1 * c2, r2)]
    )  # first times last, then inner times first
    out = [surd_text(*const)]
    if len(middle) == 1:
        c, r = middle[0]
        out.append(f"{coef(c)}sqrt({x})" if r == 1 else f"{coef(c)}sqrt({r} {x})")
    elif middle:
        g, sign = group(middle)
        out.append(f"{'-' if sign < 0 else ''}{g} sqrt({x})")
    out.append(x if s1 * s2 > 0 else f"-{x}")
    return signed_join(out)


def form5(prompt, answer):
    """One term for each power of sqrt(x), radicands square-free, no radicals multiplied."""
    x = BINOMIAL.match(prompt).group(3)
    t = sp.Symbol("t", positive=True)
    degrees = []
    for term in terms(answer):
        if re.search(r"sqrt\([^()]*\)\s+sqrt\(", term):  # radicals left unmultiplied
            return False
        for rad in re.findall(r"sqrt\((\d+)(?: [a-z])?\)", term):
            if not squarefree(int(rad)):
                return False
        e = sp.expand(to_sympy(term).subs(sp.Symbol(x), t**2))
        poly = sp.Poly(e, t)
        if len(poly.terms()) != 1:
            return False
        degrees.append(poly.degree())
    return len(degrees) == len(set(degrees))


def check5(prompt, answer):
    return form5(prompt, answer) and same_value(prompt, answer)


# ------------------------------------------------------------------
# Type 6: 3 i^3 + 2 i^5 - 3 i + 2 i^2
# ------------------------------------------------------------------
COEF6 = range(1, 6)
POW6 = range(1, 9)


def t6_pick(r):
    n = r.choice((3, 4, 4))
    es = r.sample(list(POW6), n)
    return dict(
        terms=tuple(
            (r.choice("+-") if i else "+", r.choice(COEF6), e) for i, e in enumerate(es)
        )
    )


def t6_ok(terms):
    es = [e for _, _, e in terms]
    return (
        3 <= len(terms) <= 4
        and len(set(es)) == len(es)
        and terms[0][0] == "+"
        and all(s in "+-" and c in COEF6 and e in POW6 for s, c, e in terms)
    )


def t6(terms):
    """Example 5.6, problem 15: three or four powers of i with coefficients."""
    need(t6_ok(terms))
    words = [f"{coef(c)}{'i' if e == 1 else f'i^{e}'}" for _, c, e in terms]
    out = words[0]
    for (s, _, _), w in zip(terms[1:], words[1:]):
        out += f" {s} {w}"
    return out


def reim(v):
    """The real and imaginary parts of a sympy number, each expanded."""
    return [sp.expand(x) for x in sp.expand(v).as_real_imag()]


def complex_text(a, b):
    """a + b i: "-2 - 4 i", "1 - i"."""
    bi = "i" if abs(b) == 1 else f"{abs(b)} i"
    return f"{a} {'+' if b > 0 else '-'} {bi}"


def answer6(prompt):
    v = sp.expand(to_sympy(prompt, imaginary=True))
    a, b = reim(v)
    need(a != 0 and b != 0 and a.is_Integer and b.is_Integer)
    return complex_text(int(a), int(b))


FORM6 = re.compile(r"^-?[1-9]\d* [+-] (?:[2-9]|\d{2,}) ?i$|^-?[1-9]\d* [+-] i$")


def check6(prompt, answer):
    return bool(FORM6.match(answer)) and same_value(prompt, answer, imaginary=True)


# ------------------------------------------------------------------
# Type 7: sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9) + sqrt(-16) + sqrt(16), 2 sqrt(-2) sqrt(2) + 3 i sqrt(2)
# ------------------------------------------------------------------
# A term is (sign, kind, c, u, s): c times
#   K1 sqrt(-u) sqrt(s^2)    K2 sqrt(-u) sqrt(-s^2)    K3 sqrt(-s^2)
#   K4 sqrt(s^2)             K5 sqrt(-u) sqrt(u)       K6 i sqrt(u)
KINDS7 = ("K1", "K2", "K3", "K4", "K5", "K6")
COEF7 = range(1, 5)
RAD7 = (2, 3, 5, 6, 7)
ROOT7 = range(2, 6)


def term7(kind, c, u, s):
    k = coef(c)
    return {
        "K1": f"{k}sqrt(-{u}) sqrt({s * s})",
        "K2": f"{k}sqrt(-{u}) sqrt(-{s * s})",
        "K3": f"{k}sqrt(-{s * s})",
        "K4": f"{k}sqrt({s * s})",
        "K5": f"{k}sqrt(-{u}) sqrt({u})",
        "K6": f"{k}i sqrt({u})",
    }[kind]


def t7_term(r, kind, sign):
    return (sign, kind, r.choice(COEF7), r.choice(RAD7), r.choice(ROOT7))


def t7_four_pick(r):
    return dict(
        terms=tuple(
            t7_term(r, k, r.choice("+-") if i else "+")
            for i, k in enumerate(("K1", "K2", "K3", "K4"))
        )
    )


def t7_two_pick(r):
    return dict(
        terms=tuple(
            t7_term(r, k, r.choice("+-") if i else "+")
            for i, k in enumerate(("K1", "K2"))
        )
    )


def t7_pair_pick(r):
    return dict(
        terms=tuple(
            t7_term(r, k, r.choice("+-") if i else "+")
            for i, k in enumerate(("K5", "K6"))
        )
    )


def t7_any_pick(r):
    kinds = r.sample(KINDS7, 3)
    return dict(
        terms=tuple(
            t7_term(r, k, r.choice("+-") if i else "+") for i, k in enumerate(kinds)
        )
    )


def t7_ok(terms):
    return (
        2 <= len(terms) <= 4
        and terms[0][0] == "+"
        and len({t[1] for t in terms}) == len(terms)
        and all(
            s in "+-" and k in KINDS7 and c in COEF7 and u in RAD7 and v in ROOT7
            for s, k, c, u, v in terms
        )
    )


def t7(terms):
    """Examples 5.7, problems 16-17: products of square roots of negatives, and i times a radical."""
    need(t7_ok(terms))
    out = term7(*terms[0][1:])
    for s, *t in terms[1:]:
        out += f" {s} {term7(*t)}"
    return out


def surd_of(v):
    """A sympy c sqrt(r) -> (c, r)."""
    c, rest = v.as_coeff_Mul()
    if rest == 1:
        need(c.is_Integer)
        return int(c), 1
    need(
        c.is_Integer
        and isinstance(rest, sp.Pow)
        and rest.exp == sp.Rational(1, 2)
        and rest.base.is_Integer
    )
    return int(c), int(rest.base)


def answer7(prompt):
    real, imag = [], []
    for t in terms(prompt):
        v = sp.expand(to_sympy(t, imaginary=True))
        a, b = reim(v)
        if a:
            real.append(surd_of(a))
        if b:
            imag.append(surd_of(b))
    real, imag = combine(real), combine(imag)
    need(imag)
    out = ""
    if len(real) == 1:
        out = surd_text(*real[0])
    elif real:
        g, sign = group(real)
        out = ("-" if sign < 0 else "") + g
    if len(imag) == 1:
        c, r = imag[0]
        im = "i" if (abs(c), r) == (1, 1) else f"{surd_text(abs(c), r)} i"
        neg = c < 0
    else:
        g, sign = group(imag)
        im, neg = f"{g} i", sign < 0
    if not out:
        return ("-" if neg else "") + im
    return f"{out} {'-' if neg else '+'} {im}"


def form7(answer):
    """Standard form, real part first: no square root of a negative, no power of i, i once and last,
    radicands square-free, and like terms combined (as many terms written as sympy finds)."""
    if (
        "sqrt(-" in answer
        or "i^" in answer
        or len(re.findall(r"\bi\b", answer)) != 1
        or not answer.endswith("i")
    ):
        return False
    if not all(squarefree(int(r)) for r in re.findall(r"sqrt\((\d+)\)", answer)):
        return False
    v = sp.expand(to_sympy(answer, imaginary=True))
    a, b = reim(v)
    want = len(sp.Add.make_args(a)) * (a != 0) + len(sp.Add.make_args(b))
    flat = re.sub(r"\bi\b", "1", answer).replace("(", " ").replace(")", " ")   # a lone i is a term: 5 + i
    flat = " ".join(flat.split())
    return len(terms(flat.lstrip("-").strip())) == want


def check7(prompt, answer):
    return form7(answer) and same_value(prompt, answer, imaginary=True)


# ------------------------------------------------------------------
# Type 8: the ratio of the areas of similar figures
# ------------------------------------------------------------------
SHAPES8 = (
    "rectangles",
    "triangles",
    "squares",
    "parallelograms",
    "trapezoids",
    "pentagons",
    "hexagons",
)
SCALE8 = range(2, 11)
SIZE8 = range(2, 10)
LETTER8 = {"circle": ("R", "r"), "square": ("s", "x")}
UNITS8 = ("meters", "feet", "inches", "centimeters")


def t8_scale_pick(r):
    return dict(k=r.choice(SCALE8), shapes=r.choice(SHAPES8))


def t8_scale_ok(k, shapes):
    return k in SCALE8 and shapes in SHAPES8


def t8_scale(k, shapes):
    """Example 5.8: only the scale factor."""
    need(t8_scale_ok(k, shapes))
    return f"scale {k}, {shapes}"


def t8_one_pick(r):
    shape = r.choice(("circle", "circle", "square"))
    return dict(
        shape=shape,
        L=r.choice(LETTER8[shape]),
        a=r.choice(SIZE8),
        b=r.choice(SIZE8),
        first=r.choice(("first", "second")),
    )


def t8_one_ok(shape, L, a, b, first):
    return (
        shape in LETTER8
        and L in LETTER8[shape]
        and a in SIZE8
        and b in SIZE8
        and a != b
        and math.gcd(a, b) == 1
        and first in ("first", "second")
    )


def t8_one(shape, L, a, b, first):
    """Example 5.9: one figure's size R, the other's (a R)/b."""
    need(t8_one_ok(shape, L, a, b, first))
    return f"one {shape} {L}, ({a} {L})/{b}; {first}"


def t8_big_pick(r):
    shape = r.choice(("circle", "circle", "square"))
    a, b = sorted(r.sample(list(SIZE8), 2))
    return dict(
        shape=shape,
        L=r.choice(LETTER8[shape]),
        a=a,
        b=b,
        unit=r.choice(UNITS8),
        small=r.choice(("small", "large")),
    )


def t8_big_ok(shape, L, a, b, unit, small):
    return (
        shape in LETTER8
        and L in LETTER8[shape]
        and a in SIZE8
        and b in SIZE8
        and a < b
        and math.gcd(a, b) == 1
        and unit in UNITS8
        and small in ("small", "large")
    )


def t8_big(shape, L, a, b, unit, small):
    """Problem 6: the big figure's size R, the small one's (a/b) R, with units."""
    need(t8_big_ok(shape, L, a, b, unit, small))
    return f"big {shape} {L}, {a}/{b} {L}, {unit}; {small}"


SCALE_RE = re.compile(r"^scale (\d+), ([a-z]+)$")
ONE_RE = re.compile(
    r"^one (circle|square) ([A-Za-z]), \((\d+) \2\)/(\d+); (first|second)$"
)
BIG_RE = re.compile(
    r"^big (circle|square) ([A-Za-z]), (\d+)/(\d+) \2, ([a-z]+); (small|large)$"
)


def read8(prompt):
    """("scale", k) or ("ratio", the second size over the first as a Fraction, which over which)."""
    if m := SCALE_RE.match(prompt):
        return "scale", int(m.group(1))
    if m := ONE_RE.match(prompt):
        f = Fraction(int(m.group(3)), int(m.group(4)))
        return "ratio", (1 / f) ** 2 if m.group(5) == "first" else f**2
    if m := BIG_RE.match(prompt):
        f = Fraction(int(m.group(3)), int(m.group(4)))
        return "ratio", f**2 if m.group(6) == "small" else (1 / f) ** 2
    raise ValueError("not a Type 8 problem")


def answer8(prompt):
    kind, v = read8(prompt)
    if kind == "scale":
        return f"{v * v} to 1, or 1 to {v * v}"
    need(v.denominator != 1 and v.numerator != 1)
    return f"{v.numerator}/{v.denominator}"


def check8(prompt, answer):
    kind, v = read8(prompt)
    if kind == "scale":
        m = re.fullmatch(r"(\d+) to 1, or 1 to (\d+)", answer)
        return bool(m) and int(m.group(1)) == int(m.group(2)) == v * v
    m = re.fullmatch(r"(\d+)/(\d+)", answer)
    return (
        bool(m)
        and math.gcd(int(m.group(1)), int(m.group(2))) == 1
        and Fraction(int(m.group(1)), int(m.group(2))) == v
    )


def statement8(prompt):
    if m := SCALE_RE.match(prompt):
        return f"The scale factor between two {m.group(2)} is {m.group(1)}. What is the ratio of the areas?"
    if m := ONE_RE.match(prompt):
        shape, L, a, b, first = m.groups()
        size = "radius" if shape == "circle" else "side"
        other = "second" if first == "first" else "first"
        return (
            f"The {size} of one {shape} is ${L}$, and the {size} of a second {shape} is $({a} {L})/{b}$. "
            f"What is the ratio of the area of the {first} {shape} to the area of the {other} {shape}?"
        )
    m = BIG_RE.match(prompt)
    shape, L, a, b, unit, small = m.groups()
    size = "radius" if shape == "circle" else "side"
    other = "large" if small == "small" else "small"
    return (
        f"The {size} of the big {shape} is ${L}$ {unit} and the {size} of the small {shape} is "
        f"$display({a}/{b}) {L}$ {unit}. What is the ratio of the area of the {small} {shape} to the area "
        f"of the {other} {shape}?"
    )


# ------------------------------------------------------------------
# Type 9: the diagonal of a rectangular solid
# ------------------------------------------------------------------
# The book's 5.10 letters every corner; its 5.11 and problem 19 letter only C, B, A:
# C a front bottom corner, B the bottom corner across the base from it, A above B.
FULL9 = {
    "ftl": "A",
    "ftr": "D",
    "btr": "H",
    "btl": "E",
    "fbl": "B",
    "fbr": "C",
    "bbr": "G",
    "bbl": "F",
}
DIAG9 = {
    "BH": ("fbl", "bbr", "btr"),
    "CE": ("fbr", "bbl", "btl"),
}  # start, under the end, end
THREE9 = {"right": ("fbr", "bbl", "btl"), "left": ("fbl", "bbr", "btr")}  # C, B, A
LETTER9 = tuple("abcdhkmnpqrstuvwxyz")
NUM9 = range(1, 7)  # the base edges drawn at random, hand-sized as the book's
HEIGHT9 = ("m", "n", "h", "k", "z")
WHOLE9 = (
    (2, 3, 6),
    (1, 2, 2),
    (2, 6, 9),
    (4, 4, 7),
    (1, 4, 8),
    (6, 6, 7),
    (3, 4, 12),
    (2, 2, 1),
    (4, 8, 1),
    (2, 5, 14),
)


def t9_build(diag, w, d, h, side="right"):
    tail = "; C left" if side == "left" else ""
    return f"{diag}; {w}, {d}, {h}{tail}"


def edge_ok(e):
    return (
        (isinstance(e, str) and re.fullmatch(r"[a-z]", e))
        or e in NUM9
        or isinstance(e, int)
        and 1 <= e <= 14
    )


def t9_ok(diag, w, d, h, side="right"):
    letters = [e for e in (w, d, h) if isinstance(e, str)]
    return (
        (diag in DIAG9 and side == "right" or diag == "CA" and side in THREE9)
        and all(edge_ok(e) for e in (w, d, h))
        and len(set(letters)) == len(letters)
    )


def t9(diag, w, d, h, side="right"):
    need(t9_ok(diag, w, d, h, side))
    return t9_build(diag, w, d, h, side)


def t9_letters_pick(r):
    """Example 5.10: every corner lettered, every edge a letter."""
    w, d, h = ("x", "y", "z") if r.random() < 0.3 else r.sample(LETTER9, 3)
    return dict(diag=r.choice(("BH", "BH", "CE")), w=w, d=d, h=h)


def t9_mixed_pick(r):
    """Example 5.11, problem 19: two base edges numbers, the height a letter."""
    w, d = r.sample(list(NUM9), 2)
    return dict(
        diag="CA",
        w=w,
        d=d,
        h=r.choice(HEIGHT9),
        side=r.choice(("right", "right", "left")),
    )


def t9_whole_pick(r):
    """Every edge a number; often three that make a whole-number diagonal."""
    if r.random() < 0.6:
        es = list(r.choice(WHOLE9))
        r.shuffle(es)
    else:
        es = [r.choice(NUM9) for _ in range(3)]
    diag = r.choice(("CA", "CA", "BH"))
    return dict(
        diag=diag,
        w=es[0],
        d=es[1],
        h=es[2],
        side=r.choice(("right", "left")) if diag == "CA" else "right",
    )


READ9 = re.compile(r"^(BH|CE|CA); (\w+), (\w+), (\w+)(; C left)?$")


def read9(prompt):
    m = READ9.match(prompt)
    if not m:
        raise ValueError("not a Type 9 problem")
    diag, *es, left = m.groups()
    es = [int(e) if e.isdigit() else e for e in es]
    if diag != "CA" and left:
        raise ValueError("only CA mirrors")
    return diag, es, "left" if left else "right"


def corners9(diag, side):
    """({corner: name} to label, (start, under, end) corners)."""
    if diag == "CA":
        c, b, a = THREE9[side]
        return {c: "C", b: "B", a: "A"}, (c, b, a)
    return dict(FULL9), DIAG9[diag]


def radicand9(es):
    """The squares' sum as the key writes it: its number first, then each letter squared."""
    n = sum(e * e for e in es if isinstance(e, int))
    return ([str(n)] if n else []) + [f"{e}^2" for e in es if isinstance(e, str)]


def answer9(prompt):
    diag, es, side = read9(prompt)
    rad = radicand9(es)
    if all(isinstance(e, int) for e in es):
        return single(sp.sqrt(sum(e * e for e in es)))
    return f"sqrt({' + '.join(rad)})"


def check9(prompt, answer):
    diag, es, side = read9(prompt)
    names, (s, u, e) = corners9(diag, side)
    P = fig.solid_corners(*[2.0 if isinstance(v, str) else v for v in es])
    if not all(P[s][i] != P[e][i] for i in (0, 1)) or s[1] != "b" or e[1] != "t":
        return False  # the far corner, across the solid
    letters = {v for v in es if isinstance(v, str)}
    want = sp.sqrt(
        sum(
            sp.Symbol(v, positive=True) ** 2 if isinstance(v, str) else v * v
            for v in es
        )
    )
    try:
        got = sym(answer)
    except Exception:
        return False
    if sp.simplify(got - want) != 0:
        return False
    if not letters:
        return rationalized(answer)
    m = re.fullmatch(r"sqrt\((.*)\)", answer)
    if not m:
        return False
    parts = m.group(1).split(" + ")
    nums = [p for p in parts if p.isdigit()]
    sq = [p for p in parts if re.fullmatch(r"[a-z]\^2", p)]
    return (
        len(nums) <= 1
        and len(nums) + len(sq) == len(parts)
        and {p[0] for p in sq} == letters
        and len(sq) == len(letters)
    )


def drawn9(es):
    """The edges as drawn: a number as it is, a letter the middle of the numbers given (2 with none)."""
    nums = [e for e in es if isinstance(e, int)]
    dflt = sorted(nums)[len(nums) // 2] if nums else None
    out = []
    for i, e in enumerate(es):
        out.append(float(e) if isinstance(e, int) else (dflt or (3.4, 2.4, 2.0)[i]))
    lo = max(out) / 3  # nothing drawn thinner than a third
    return [max(v, lo) for v in out]


def figure9(prompt, key=False, unit="1cm"):
    diag, es, side = read9(prompt)
    names, (s, u, e) = corners9(diag, side)
    labels = {c: f"${n}$" for c, n in names.items()}
    edges = dict(zip(("width", "depth", "height"), (f"${v}$" for v in es)))
    lines = [(s, u), (u, e), (s, e)] if key else []
    return fig.solid(*drawn9(es), labels, edges, key_lines=lines, unit=unit)


def statement9(prompt):
    diag, _, _ = read9(prompt)
    if diag == "CA":
        return "Find the length of diagonal $A C$ in the rectangular solid shown."
    a, b = diag
    return f"Find the length of the diagonal that connects corners ${a}$ and ${b}$ in the rectangular solid shown."


def steps9(prompt):
    diag, es, side = read9(prompt)
    names, (s, u, e) = corners9(diag, side)
    S, U, E = names[s], names[u], names[e]
    w, d, h = es
    base = radicand9([w, d])
    if all(isinstance(v, int) for v in (w, d)):
        bd = single(sp.sqrt(w * w + d * d))
        base_eq = f"({S} {U})^2 = {w}^2 + {d}^2 = {w * w + d * d}"
    else:
        bd = f"sqrt({' + '.join(base)})"
        base_eq = f"({S} {U})^2 = {w}^2 + {d}^2"
    ans = answer9(prompt)
    return (
        f"*Step 1.* The base diagonal ${S} {U}$ is the hypotenuse of a right triangle with legs ${w}$ and ${d}$: "
        f"$ {base_eq}, quad {S} {U} = {bd}$.\n\n"
        f"*Step 2.* ${S} {E}$ is the hypotenuse of a right triangle with legs ${S} {U}$ and ${U} {E} = {h}$: "
        f"$({S} {E})^2 = ({S} {U})^2 + ({U} {E})^2, quad {S} {E} = {ans}$."
    )


# ------------------------------------------------------------------
# Templates, ranges, and the type each answer function belongs to
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_two_pick, t1_two), (t1_two_pick, t1_two), (t1_mixed_pick, t1_mixed)],
    "2": [(t2_quot_pick, t2_quot), (t2_quot_pick, t2_quot), (t2_three_pick, t2_three)],
    "3": [
        (t3_power_pick, t3_power),
        (t3_power_pick, t3_power),
        (t3_mono_pick, t3_mono),
    ],
    "4": [(t4_pick, t4)],
    "5": [
        (t5_mixed_pick, t5_mixed),
        (t5_mixed_pick, t5_mixed),
        (t5_square_pick, t5_square),
    ],
    "6": [(t6_pick, t6)],
    "7": [(t7_four_pick, t7), (t7_two_pick, t7), (t7_pair_pick, t7), (t7_any_pick, t7)],
    "8": [(t8_scale_pick, t8_scale), (t8_one_pick, t8_one), (t8_big_pick, t8_big)],
    "9": [
        (t9_letters_pick, t9),
        (t9_mixed_pick, t9),
        (t9_mixed_pick, t9),
        (t9_whole_pick, t9),
    ],
}
RANGES = {
    t1_two: t1_two_ok,
    t1_mixed: t1_mixed_ok,
    t2_quot: t2_quot_ok,
    t2_three: t2_three_ok,
    t3_power: t3_power_ok,
    t3_mono: t3_mono_ok,
    t4: t4_ok,
    t5_mixed: t5_mixed_ok,
    t5_square: t5_square_ok,
    t6: t6_ok,
    t7: t7_ok,
    t8_scale: t8_scale_ok,
    t8_one: t8_one_ok,
    t8_big: t8_big_ok,
    t9: t9_ok,
}


def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))


ANSWER = {
    "1": answer1,
    "2": answer2,
    "3": answer3,
    "4": answer4,
    "5": answer5,
    "6": answer6,
    "7": answer7,
    "8": answer8,
    "9": answer9,
}
CHECK = {
    "1": check1,
    "2": check2,
    "3": check3,
    "4": check4,
    "5": check5,
    "6": check6,
    "7": check7,
    "8": check8,
    "9": check9,
}


def answer_of(prompt, typ):
    return ANSWER[typ](prompt)


def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    answer = answer_of(prompt, entry)
    if entry == "7":  # at most two terms in either part, as the book's
        need(
            all(
                len(terms(g)) <= 2
                for g in re.findall(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)", answer)
                if "sqrt" in g or " " in g
            )
        )
    return dict(prompt=prompt, answer=answer)


def check(p):
    try:
        ok = CHECK[p["type"]](p["prompt"], p["answer"])
    except gen.Redraw:
        return "failed"
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"


generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
WORDS = ("8", "9")
SLIDE_UNIT = "2.3cm"


def statement(p):
    return statement8(p["prompt"]) if p["type"] == "8" else statement9(p["prompt"])


def _prompt(p, key):
    t = p["type"]
    try:
        if t == "8":
            return statement8(p["prompt"])
        if t == "9":
            return f"{statement9(p['prompt'])} #v(0.3em) #align(center)[{figure9(p['prompt'], key)}]"
    except (ValueError, KeyError, gen.Redraw):
        return p["prompt"]
    return "Simplify: #h(0.5em) " + display(dfrac(p["prompt"]))     # its own task (EXTENDING.md 3.10)


def typst(p, gap="0.3em"):
    return _prompt(p, False)


def key_typst(p, gap="0.3em"):
    """Type 9's key draws the base diagonal and the solid's diagonal in red."""
    return _prompt(p, True)


def answer_typst(p):
    if p["type"] == "8" and " to " in p["answer"]:
        return p["answer"]
    return display(dfrac(p["answer"]))


def slide_typst(p, key=False):
    """Type 9: the words and the two steps (hidden on the question slide) beside the solid, drawn
    larger; the same figure on both slides (the key's red lines lie inside it), so nothing moves."""
    if p["type"] != "9":
        return None
    try:
        f, s, st = (
            figure9(p["prompt"], key, SLIDE_UNIT),
            statement9(p["prompt"]),
            steps9(p["prompt"]),
        )
    except (ValueError, KeyError, gen.Redraw):
        return None
    ans = f"#text(size: 0.85em)[{st}]"
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"


SUP = {"2": "", "3": "³", "4": "⁴", "5": "⁵"}


def plain(t):
    """Typst math for the terminal: sqrt(x) as √(x), root(4, x) as ⁴√(x)."""
    t = ROOT.sub(lambda m: f"{SUP.get(m.group(1), m.group(1))}√({m.group(2)})", t)
    return plain_math(t.replace("sqrt(", "√("))


def text(p):
    t = p["type"]
    if t in WORDS:
        try:
            s = statement(p)
        except (ValueError, KeyError):
            return p["prompt"]
        s = s.replace("$display(", "$(").replace("$A C$", "$AC$")
        s = re.sub(r"\$([^$]*)\$", lambda m: m.group(1), s)
        return s + ("   [figure]" if t == "9" else "")
    return "Simplify: " + plain(p["prompt"])


def answer_text(p):
    return plain(p["answer"])


def height(p):
    t = p["type"]
    if t == "9":
        return 0.35 + 3.6 / 2.54
    if t == "8":
        return 0.6
    return 0.55 if "/" in p["prompt"] else 0.35


# ------------------------------------------------------------------
# Editing: Types 1-7 are Typst math; 8 and 9 are the question's data
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "sqrt(x^3 y) root(4, x y^3)",
    "2": "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))",
    "3": "(x^(-2) + y^(-2))/(x y)^(-1)",
    "4": "3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)",
    "5": "(sqrt(2) + sqrt(x))(1 - sqrt(x))",
    "6": "3 i^3 + 2 i^5 - 3 i + 2 i^2",
    "7": "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9)",
    "8": "one circle R, (3 R)/5; first",
    "9": "CA; 2, 3, m",
}


def clean(t):
    t = t.replace("−", "-").replace("√", "sqrt").replace("·", " ")
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
    return gen.selftest(
        NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10
    )
