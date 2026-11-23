"""Lesson 16 (Advanced Math): complex fractions, abstract equations, division of
polynomials. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_016/slides/deck_016.typ): examples 16.1-16.4
and Problem Set 16, problems 5-10.

    1  a multi-level complex fraction:     x/(a + m/(b + c/d))                    (x (b d + c))/(a b d + a c + d m)
    2  sums of fractions above and below:  (a/x^2 + b/x)/(m/x^2 + k/(x c))         (c (a + b x))/(c m + k x)
    3  an abstract equation:               y = v (a/x + b/(m c)), for c            c = (b v x)/(m x y - a m v)
    4  division by x - a, a remainder:     x^3 - 2 by x - 1                        x^2 + x + 1 - 1/(x - 1)

Each heading of the problem types file is a type. The Additional Practice banks
do this lesson's math, and this bank uses their checks and formatters
(adv_complex_fractions, adv_literal, adv_poly_division) with templates in the
shapes of the lesson's own problems:
  1  n/(a + m/(b + c/d)), all letters (16.1, problem 7), and n/(a + a/(k + b/c)),
     a letter repeated and a number (problem 6: p/(m + m/(1 + b/c))).
  2  (p/v^2 + q/v)/(r/v^2 + s/(v c)), each sign + or -, a numerator 1 or a letter
     (16.2; problem 5: (x/a^2 + b/a)/(1/a^2 - k/(a c))).
  3  L = K (n/x + q/(m c)) for c, K one letter or two, n a letter or 1, K maybe the
     same letter as m (16.3; problem 8: x = p m (1/y + a/(b d)) for d; problem 9,
     where the m's cancel).
  4  x^n + k divided by x - a (or x + a): every inner power missing, a remainder
     (16.4: x^3 - 2 by x - 1; problem 10: x^3 - 1 by x - 2); n is 2, 3, or 4.
The letters are drawn as each source has them, distinct, from the bank's letters.

The key writes what the deck writes, as near as one rule allows:
  1, 2  one fraction in lowest terms; the numerator and the denominator each with
     its common factor taken out, else multiplied out, a positive term first:
     (p (b + c))/(m (b + 2 c)) (problem 6), (a (c p + m))/(c p x + c y + m x)
     (problem 7), (c (a + b x))/(c m + k x) (16.2). Two sources differ from the
     deck in grouping only (the same value and form): 16.1's denominator, which
     the deck writes a(b d + c) + m d, and problem 5, which the deck writes
     (x c + a b c)/(c - a k), here (c (a b + x))/(c - a k).
  3  "c = one fraction", multiplied out, as the deck has it (no factor taken out):
     c = (b v x)/(m x y - a m v); d = (a m p y)/(b x y - b m p).
  4  the quotient, then the remainder over the divisor: x^2 + 2 x + 4 + 7/(x - 2).
The letters in a term are in alphabetical order (the deck's x v b is b v x here).

check() checks what the Additional Practice banks check: Types 1-2 compare values
at random points and require one fraction in lowest terms; Type 3 puts the answer
into the equation at random values, and the unknown must be gone from the right
side; Type 4 (adv_poly_division's own check) compares values, and what's left over
must be a number over the divisor. None of them uses how the problem was built.
Types 1-3 compile each expression once (sympy's lambdify) instead of the shared
helpers' subs and evalf, which take too long here for the 100 ms budget.

No skipped sources: Lesson 16 has no proofs.

A problem: dict(type, prompt, answer, source), and target (Type 3) or divisor (Type 4).
    1  prompt "x/(a + m/(b + c/d))"
    3  prompt "y = v (a/x + b/(m c))", target "c"
    4  prompt "x^3 - 2", divisor "x - 1"
"""
import functools, random
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, simplest_form, denominators, syms_of, side_diff
from ..typmath import tx, fr
from . import adv_literal as AL
from . import adv_poly_division as PD

NAME = FAMILY = "adv_lesson_16"
FIXED = False
TITLE = "Lesson 16: Complex Fractions, Abstract Equations, Division of Polynomials"
INSTRUCTIONS = ""              # each type has its own
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="Multi-Level Complex Fractions", instructions="Simplify.",
         look="A fraction inside a fraction inside a fraction.",
         move="Start at the bottom: write $b + c/d$ as one fraction, $(b d + c)/d$. Then $m$ over it is "
              "$(m d)/(b d + c)$; add $a$ as one fraction, and divide $x$ by the result.", space="1.6in"),
    dict(key="2", title="Sums of Fractions Above and Below", instructions="Simplify.",
         look="Fractions added or subtracted on top, and on the bottom.",
         move="Multiply above and below by the LCM of all the denominators, here $x^2 c$: "
              "$(a c + b x c)/(m c + k x)$. Take out a common factor if there is one.", space="1.4in"),
    dict(key="3", title="Abstract Equations", instructions="Solve for the indicated variable.",
         look="An equation in letters only, with fractions, and a letter to solve for.",
         move="Distribute, then multiply every term by the LCM of the denominators. Put the terms with the "
              "unknown on one side, factor it out, and divide: $c = (x v b)/(x m y - m v a)$.", space="1.6in"),
    dict(key="4", title="Division of Polynomials", instructions="Divide, and check the result.",
         look="A polynomial with missing powers, divided by $x - a$.",
         move="Write $0 x^2$ and $0 x$ for the missing powers and divide. The answer is the quotient plus the "
              "remainder over the divisor. Check: multiply the quotient by $(x - a)/(x - a)$ and add the "
              "remainder fraction.", space="1.6in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

LETTERS = gen.LETTERS
X = sp.Symbol("x")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], p.get("target"), p.get("divisor"))

def distinct(*ls):
    return all(l in LETTERS for l in ls) and len(set(ls)) == len(ls)

def pick_letters(r, n):
    return tuple(r.sample(LETTERS, n))

# ------------------------------------------------------------------
# Type 1: a multi-level complex fraction (16.1, problems 6 and 7)
# ------------------------------------------------------------------
def t1_letters_ok(n, a, m, b, c, d):
    return distinct(n, a, m, b, c, d)

def t1_letters_pick(r):
    n, a, m, b, c, d = pick_letters(r, 6)
    return dict(n=n, a=a, m=m, b=b, c=c, d=d)

def t1_letters(n, a, m, b, c, d):            # 16.1: x/(a + m/(b + c/d)); problem 7: a/(x + y/(p + m/c))
    need(t1_letters_ok(n, a, m, b, c, d))
    return fr(n, f"{a} + {fr(m, f'{b} + {fr(c, d)}')}")

K1 = range(1, 4)

def t1_repeat_ok(n, a, k, b, c):
    return distinct(n, a, b, c) and k in K1

def t1_repeat_pick(r):
    n, a, b, c = pick_letters(r, 4)
    return dict(n=n, a=a, k=r.choice(K1), b=b, c=c)

def t1_repeat(n, a, k, b, c):                # problem 6: p/(m + m/(1 + b/c))
    need(t1_repeat_ok(n, a, k, b, c))
    return fr(n, f"{a} + {fr(a, f'{k} + {fr(b, c)}')}")

# ------------------------------------------------------------------
# Type 2: sums of fractions above and below (16.2, problem 5)
# ------------------------------------------------------------------
SIGNS = ("+", "-")

def t2_ok(p1, p2, q1, q2, v, c, s1, s2):
    tops = [t for t in (p1, p2, q1, q2) if t != "1"]
    return (distinct(*tops, v, c) and s1 in SIGNS and s2 in SIGNS
            and [p1, p2, q1, q2].count("1") <= 1 and p2 != "1" and q2 != "1")

def t2_pick(r):
    p1, p2, q1, q2, v, c = pick_letters(r, 6)
    one = r.choice((None, None, "p1", "q1"))
    if one == "p1":
        p1 = "1"
    elif one == "q1":
        q1 = "1"
    return dict(p1=p1, p2=p2, q1=q1, q2=q2, v=v, c=c, s1=r.choice(SIGNS), s2=r.choice(SIGNS))

def t2(p1, p2, q1, q2, v, c, s1, s2):        # 16.2: (a/x^2 + b/x)/(m/x^2 + k/(x c)); problem 5
    need(t2_ok(p1, p2, q1, q2, v, c, s1, s2))
    top = f"{fr(p1, f'{v}^2')} {s1} {fr(p2, v)}"
    bottom = f"{fr(q1, f'{v}^2')} {s2} {fr(q2, f'{v} {c}')}"
    return fr(top, bottom)

# ------------------------------------------------------------------
# Type 3: an abstract equation (16.3, problems 8 and 9)
# ------------------------------------------------------------------
def t3_ok(L, K, n, x, q, m, c, s):
    ks = K.split()
    return (1 <= len(ks) <= 2 and s in SIGNS and distinct(L, *[k for k in ks if k != m], *([n] if n != "1" else []),
                                                            x, q, m, c)
            and all(k in LETTERS for k in ks) and len(set(ks)) == len(ks))

def t3_pick(r):
    L, k1, k2, n, x, q, m, c = pick_letters(r, 8)
    shape = r.choice(("one", "one", "two", "same"))
    K = k1 if shape == "one" else f"{k1} {k2}" if shape == "two" else m
    return dict(L=L, K=K, n=r.choice((n, n, "1")), x=x, q=q, m=m, c=c, s=r.choice(("+", "+", "-")))

def t3(L, K, n, x, q, m, c, s):              # 16.3: y = v (a/x + b/(m c)) for c
    """(the equation, the letter to solve for)."""
    need(t3_ok(L, K, n, x, q, m, c, s))
    return f"{L} = {K} ({fr(n, x)} {s} {fr(q, f'{m} {c}')})", c

# ------------------------------------------------------------------
# Type 4: division with missing powers and a remainder (16.4, problem 10)
# ------------------------------------------------------------------
DEGREE4 = (2, 3, 3, 4)
K4 = range(1, 10)
A4 = range(1, 5)

def t4_ok(n, k, a):
    rem = a ** n + k
    return n in DEGREE4 and abs(k) in K4 and abs(a) in A4 and rem != 0 and abs(a) ** n <= 64   # hand-sized: x^4 by x - 4 leaves 254

def t4_pick(r):
    return dict(n=r.choice(DEGREE4), k=gen.signed(r, 1, 9), a=r.choice((1, 1, -1)) * r.choice(A4))

def t4(n, k, a):                             # 16.4: x^3 - 2 by x - 1; problem 10: x^3 - 1 by x - 2
    need(t4_ok(n, k, a))
    return tx(X ** n + k, "x"), tx(X - a, "x")

TEMPLATES = {
    "1": [(t1_letters_pick, t1_letters), (t1_letters_pick, t1_letters), (t1_repeat_pick, t1_repeat)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick, t4)],
}
RANGES = {t1_letters: t1_letters_ok, t1_repeat: t1_repeat_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# The key
# ------------------------------------------------------------------
def positive_first(e):
    """e as Typst math, a positive term first when there is one: c - a k, not -a k + c."""
    terms = [tx(t) for t in sp.Add.make_args(sp.expand(e))]
    if len(terms) == 1:
        return terms[0]
    order = sp.expand(e).as_ordered_terms()
    terms = [tx(t) for t in order]
    pos = [t for t in terms if not t.startswith("-")]
    neg = [t for t in terms if t.startswith("-")]
    out = (pos + neg)
    s = out[0]
    for t in out[1:]:
        s += f" - {t[1:]}" if t.startswith("-") else f" + {t}"
    return s

def monomial_gcd(e):
    """The common factor of an expanded polynomial's terms: a number times letters."""
    terms = sp.Add.make_args(sp.expand(e))
    g = functools.reduce(sp.gcd, terms)
    return sp.Abs(g) if g.is_number else g

def gcf_form(e):
    """e with its common factor taken out, else multiplied out: c (a b + x); c p x + c y + m x."""
    e = sp.expand(e)
    if len(sp.Add.make_args(e)) == 1:
        return tx(e)
    g = monomial_gcd(e)
    if g == 1:
        return positive_first(e)
    rest = sp.expand(e / g)
    gt = tx(g)
    return f"{gt} ({positive_first(rest)})"

def negatives(e):
    return sum(t.could_extract_minus_sign() for t in sp.Add.make_args(sp.expand(e)))

def fraction_answer(prompt):
    e = sp.cancel(sp.together(to_sympy(prompt)))
    need(e != 0 and not e.has(sp.zoo, sp.nan))
    n, d = sp.fraction(e)
    if negatives(-n) + negatives(-d) < negatives(n) + negatives(d):
        n, d = -n, -d                                   # the signs that leave the fewest negative terms
    if d == 1:
        return gcf_form(n)
    return fr(gcf_form(n), gcf_form(d))

def answer_of(p):
    typ = p["type"]
    if typ in ("1", "2"):
        return fraction_answer(p["prompt"])
    if typ == "3":
        return AL.solve(p["prompt"], p["target"])
    q, rem = sp.div(sp.Poly(to_sympy(p["prompt"]), X), sp.Poly(to_sympy(p["divisor"]), X))
    answer = tx(q.as_expr(), "x")
    r_ = rem.as_expr()
    if r_ != 0:
        answer += (" + " if r_ > 0 else " - ") + fr(tx(abs(r_)), p["divisor"])
    return answer

def problem(typ, built):
    if typ == "3":
        return dict(prompt=built[0], target=built[1])
    if typ == "4":
        return dict(prompt=built[0], divisor=built[1])
    return dict(prompt=built)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    p = dict(type=entry, **problem(entry, build(**pick(r))))
    p["answer"] = answer_of(p)
    p.pop("type")
    return p

# ------------------------------------------------------------------
# Checking: what the Additional Practice banks check (their value at random points,
# their forms), with each expression compiled once (lambdify) to keep in budget
# ------------------------------------------------------------------
def at_points(e, syms, trials=6, lo=1.2, hi=2.8, rng=random.Random(0)):
    """e's values (complex) at random points of syms; a point where it's undefined is skipped."""
    f = sp.lambdify(syms, e, "math")
    out = []
    for _ in range(trials):
        vals = [rng.uniform(lo, hi) for _ in syms]
        try:
            out.append((vals, complex(f(*vals))))
        except (ZeroDivisionError, OverflowError, ValueError):
            continue
    return f, out

def same_value(a, b):
    ea, eb = to_sympy(a), to_sympy(b)
    syms = sorted(ea.free_symbols | eb.free_symbols, key=str)
    fb = sp.lambdify(syms, eb, "math")
    _, pts = at_points(ea, syms)
    for vals, va in pts:
        try:
            vb = complex(fb(*vals))
        except (ZeroDivisionError, OverflowError, ValueError):
            continue
        if not abs(va - vb) <= 1e-9 * max(1, abs(va)):
            return False
    return bool(pts)

def check_fraction(p):
    """Types 1-2 (adv_complex_fractions' check): the prompt's value, one fraction in lowest terms."""
    a = p["answer"]
    return same_value(p["prompt"], a) and simplest_form(a) and len(denominators(a)) <= 1

def check_solved(p):
    """Type 3 (adv_literal's check): "target = ...", the unknown gone from the right side, the
    equation true with it at random values, the right side in simplest form."""
    lhs, sep, rhs = p["answer"].partition("=")
    if not sep or lhs.strip() != p["target"]:
        return False
    syms = syms_of(p["prompt"])
    v = syms[p["target"]]
    rhs_e = to_sympy(rhs.strip())
    if v in rhs_e.free_symbols or not rhs_e.free_symbols <= set(syms.values()):
        return False
    rest = sorted(set(syms.values()) - {v}, key=str)
    e = side_diff(p["prompt"]).subs(v, rhs_e)
    _, pts = at_points(e, rest, trials=5, lo=1.5, hi=9.5)
    return bool(pts) and all(abs(val) < 1e-8 for _, val in pts) and simplest_form(rhs.strip())

def check(p):
    try:
        if p["type"] == "4":
            return PD.check(p)
        ok = check_fraction(p) if p["type"] in ("1", "2") else check_solved(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing: each type as its Additional Practice bank shows it
# ------------------------------------------------------------------
CF_SHOWN = gen.shown(lead="Simplify:")                 # as adv_complex_fractions shows them

def typst(p, gap="0.3em"):
    if p["type"] == "3":
        return AL.typst(p, gap)
    if p["type"] == "4":
        return f"Divide ${p['prompt']}$ by ${p['divisor']}$ and check the result by adding the quotient and the remainder fraction."
    return CF_SHOWN[0](p, gap)

def answer_typst(p):
    if p["type"] == "3":
        return AL.answer_typst(p)
    if p["type"] == "4":
        return PD.answer_typst(p)
    return CF_SHOWN[1](p)

def text(p):
    if p["type"] == "3":
        return AL.text(p)
    if p["type"] == "4":
        return PD.text(p)[:-1] + " and check the result by adding the quotient and the remainder fraction."
    return CF_SHOWN[2](p)

def answer_text(p):
    if p["type"] == "3":
        return AL.answer_text(p)
    if p["type"] == "4":
        return PD.answer_text(p)
    return CF_SHOWN[3](p)

def height(p):
    return 0.55

EXAMPLE = {"1": "x/(a + m/(b + c/d))", "2": "(a/x^2 + b/x)/(m/x^2 + k/(x c))",
           "3": "y = v (a/x + b/(m c)) ; c", "4": "x^3 - 2 ; x - 1"}

def edit_text(p):
    if p["type"] == "3":
        return AL.edit_text(p)
    if p["type"] == "4":
        return PD.edit_text(p)
    return p["prompt"]

def from_edit(t, old):
    typ = old.get("type", "1")
    t = " ".join(t.replace("−", "-").split())
    try:
        if typ == "3":
            eq, _, target = t.partition(";")
            new = dict(old, prompt=" ".join(eq.split()), target=target.strip() or old.get("target", ""))
        elif typ == "4":
            top, _, bottom = t.partition(";")
            new = dict(old, prompt=" ".join(top.split()), divisor=" ".join(bottom.split()) or old.get("divisor", ""))
        else:
            new = dict(old, prompt=t)
        new["answer"] = answer_of(new)
    except Exception:
        raise ValueError(f"write it like {EXAMPLE[typ]}") from None
    new["source"] = "edited"
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
