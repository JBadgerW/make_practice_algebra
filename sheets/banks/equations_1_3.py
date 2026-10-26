"""Lesson 1-3: linear equations of four or more steps, from the teacher's
equation banks for Lessons 1-2 and 1-3 (~/Documents/alg1/unit_1, every
problem rated 4 or 5 there): fractions to clear, decimals, distributing on
both sides, and mixtures. The easier ones are equations_1_2.

The types follow the moves, and every equation in those banks rated 4 or 5
is one some template here can draw. Problems are built backward from the
solution, except where the bank's own answers are fractions (12/7, 2/3):
there the numbers come first and the solution is whatever it is, if it's
small.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "1/4 (n - 8) = -5 n + 7"
    answer  "n = 12/7", "y = -10.4" (the prompt has decimals), "x = 18",
            "no solution", or "all real numbers"
check() solves the prompt with sympy and compares (sheets/linear.py: key, keyed).
"""
import math
from fractions import Fraction as F
from .. import gen, linear
from ..gen import need, signed, signed_except, except_, written
from .equations_1_2 import dec, places, over, plus, flip, other, answer_typst

NAME = FAMILY = "equations_1_3"
FIXED = False
TITLE = "Lesson 1-3: Equations with Fractions, Decimals, and Parentheses"
INSTRUCTIONS = "Solve each equation."
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Distribute a Subtraction",
         look="A number minus a product, or large numbers: 11 - 3(4 - 2x) = 41, 300 = 12(4t - 3).",
         move="Distribute, keeping the sign in front of the number with it. Combine, then solve."),
    dict(key="2", title="Decimal Coefficients",
         look="Decimal coefficients to distribute or combine: 4x - 0.5(x + 2) + 3 = 16.",
         move="Distribute and combine like terms (or multiply by 10 or 100 first). Then solve."),
    dict(key="3", title="Clear One Denominator",
         look="One denominator, on a fraction or in front of parentheses.",
         move="Multiply every term on both sides by the denominator. Then distribute and solve."),
    dict(key="4", title="Clear Several Denominators",
         look="Two or more different denominators.",
         move="Multiply every term on both sides by the least common denominator. Then solve.",
         space="1.5in"),
    dict(key="5", title="Distribute on Both Sides",
         look="Parentheses on both sides, or a decimal to distribute with the variable on both sides.",
         move="Distribute on each side and combine. Gather the variable terms on one side, then solve.",
         space="1.5in"),
    dict(key="6", title="Mixtures",
         look="Percents as decimals, times an amount x and the rest of the total (T - x).",
         move="Distribute and combine the x terms (or multiply by 100 first). Then solve.",
         space="1.5in"),
    dict(key="A", title="No Solution or All Real Numbers", special=True,
         look="Parentheses on both sides whose variable terms come out the same.",
         move="Distribute on both sides. When the variable terms cancel, a true statement means all real numbers; "
              "a false one means no solution."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def paren(t):
    return f"({t})"

def small(x, d=20):
    """A solution read off the numbers is short: an integer or a fraction with a small denominator."""
    need(x != 0 and F(x).denominator <= d and abs(x) <= 60)

# ------------------------------------------------------------------
# Type 1: distribute a subtraction, or large numbers
# ------------------------------------------------------------------
def t1_minus(r, v):                        # 11 - 3(4 - 2x) = 41
    q, a, b, c, x = r.randint(5, 25), r.randint(2, 6), r.randint(2, 9), r.randint(2, 5), r.randint(1, 9)
    return f"{q} - {a} ({b} - {c} {v}) = {q - a * (b - c * x)}"

def t1_large(r, v):                        # 1500 - 4(2x + 25) = 600
    n, a, b, c = 100 * r.randint(6, 30), r.randint(2, 8), r.randint(2, 4), 5 * r.randint(2, 6)
    x = 5 * r.randint(2, 20)
    m = n - a * (b * x + c)
    need(m > 0 and m % 100 == 0)
    return f"{n} - {a} ({b} {v} + {c}) = {m}"

def t1_number_first(r, v):                 # 300 = 12(4t - 3)
    a, b, c, x = r.randint(10, 20), r.randint(2, 5), r.randint(2, 6), r.randint(3, 12)
    n = a * (b * x - c)
    need(n % 10 == 0)
    return f"{n} = {a} ({b} {v} - {c})"

# ------------------------------------------------------------------
# Type 2: decimal coefficients
# ------------------------------------------------------------------
def t2_distribute(r, v):                   # 4x - 0.5(x + 2) + 3 = 16
    a, k = r.randint(3, 8), F(r.choice((1, 2, 3)), 4)
    b, c, x = r.choice((2, 4, 8)), r.randint(1, 9), r.randint(1, 10)
    d = a * x - k * (x + b) + c
    need(places(d, 2))
    group = paren(written((1, v), (b, "")))
    return f"{written((a, v), (-dec(k), group), (c, ''))} = {written((dec(d), ''))}"

def t2_combine(r, v):                      # 1.025x + 0.05x + 40 = 61.5
    a = 1 + F(r.choice((20, 25, 40, 50, 60, 75, 80)), 1000)
    b = F(r.choice((1, 2, 3, 4, 5, 6)), 100)
    c, x = 5 * r.randint(1, 10), 10 * r.randint(1, 5)
    d = (a + b) * x + c
    need(places(d, 2))
    return f"{written((dec(a), v), (dec(b), v), (c, ''))} = {written((dec(d), ''))}"

def t2_both(r, v):                         # 20a + 22.5 = 12.5(a + 3)
    c = F(r.randint(5, 15)) + F(1, 2)
    a, d, x = r.randint(int(c) + 2, 25), r.randint(2, 5), r.randint(1, 6)
    b = c * (x + d) - a * x
    need(b > 0)
    return f"{written((a, v), (dec(b), ''))} = {dec(c)} ({v} + {d})"

# ------------------------------------------------------------------
# Type 3: clear one denominator
# ------------------------------------------------------------------
def t3_product_over(r, v):                 # (3(x + 2))/4 - 5 = 10
    c, a, b, x = r.randint(2, 6), r.randint(2, 5), signed(r, 1, 6), r.randint(1, 25)
    need(math.gcd(a, c) == 1 and a * (x + b) % c == 0 and x + b != 0)
    d = r.randint(1, 9)
    top = f"{a} ({written((1, v), (b, ''))})"
    return f"{plus(paren(top) + f'/{c}', -d)} = {a * (x + b) // c - d}"

def t3_number_before(r, v):                # 6 + (2x - 3)/5 = 9
    c, a, b, x = r.randint(2, 6), r.randint(2, 5), signed(r, 1, 9), r.randint(1, 12)
    need(a % c != 0 and (a * x + b) % c == 0)
    d = r.randint(1, 9)
    return f"{d} + {over(written((a, v), (b, '')), c)} = {d + (a * x + b) // c}"

def t3_plus_term(r, v):                    # (x - 6)/3 + 3x = 8
    c, b, a, x = r.randint(2, 6), signed(r, 1, 9), r.randint(2, 4), r.randint(1, 9)
    need((x + b) % c == 0)
    return f"{written((1, over(written((1, v), (b, '')), c)), (a, v))} = {(x + b) // c + a * x}"

def t3_both_sides(r, v):                   # 4y = (10 - 16y)/2 + 3
    a, k, c, b, d = r.randint(2, 8), r.randint(2, 4), r.randint(2, 20), r.randint(1, 20), r.randint(1, 9)
    x = (F(b, k) + d) / (a + F(c, k))
    small(x, 8)
    return f"{a} {v} = {plus(over(written((b, ''), (-c, v)), k), d)}"

def t3_fraction_times(r, v):               # 1/4 (n - 8) = -5n + 7
    k, b, a, d = r.randint(2, 6), r.randint(2, 12), r.randint(2, 6), r.randint(2, 9)
    x = F(k * d + b, 1 + a * k)
    small(x)
    return f"1/{k} ({v} - {b}) = {written((-a, v), (d, ''))}"

def t3_nested(r, v):                       # 1/6 (4(x - 3) + 18) = x
    k = r.randint(4, 10)
    a, b, x = r.randint(2, k - 1), r.randint(1, 5), r.randint(1, 10)
    c = (k - a) * x + a * b
    return f"1/{k} ({a} ({v} - {b}) + {c}) = {v}"

# ------------------------------------------------------------------
# Type 4: clear several denominators
# ------------------------------------------------------------------
def fraction(r, top=9, dens=(2, 3, 4, 5, 6, 8)):
    """p/q in lowest terms, q > 1."""
    q = r.choice(dens)
    p = r.randint(1, top)
    need(math.gcd(p, q) == 1)
    return F(p, q)

def t4_coefficients(r, v):                 # 4/3 x - 1/2 x = 5
    a, b = fraction(r), fraction(r)
    need(a != b and a.denominator != b.denominator)
    x = math.lcm(a.denominator, b.denominator) * signed(r, 1, 3)
    c = (a - b) * x
    need(c.denominator == 1)
    return f"{written((a, v), (-b, v))} = {c}"

def t4_parts(r, v):                        # 960 = h/8 + h/4
    a, b = r.sample((2, 3, 4, 5, 6, 8, 10, 12), 2)
    x = math.lcm(a, b) * r.randint(10, 200)
    n = F(x, a) + F(x, b)
    need(n.denominator == 1 and n % 10 == 0 and x <= 6000)
    return f"{n} = {over(v, a)} + {over(v, b)}"

def t4_fraction_terms(r, v):               # 5/36 = 7/18 w + 11/12
    a, c = fraction(r, 11, (3, 4, 6, 8, 9, 10, 12, 18)), fraction(r, 11, (3, 4, 6, 8, 9, 10, 12))
    x = r.choice((F(signed(r, 1, 4)), F(signed(r, 1, 4), 2)))
    n = a * x + c
    need(n != 0 and n.denominator > 1 and n.denominator <= 60 and len({a.denominator, c.denominator, n.denominator}) == 3)
    return f"{written((n, ''))} = {written((a, v), (c, ''))}"

def t4_letter_over(r, v):                  # (2m)/3 - m/6 = 5/4
    p, q = r.randint(2, 9), r.choice((2, 3, 4, 5, 6, 8))
    s = r.choice((2, 3, 4, 6, 8, 12))
    need(math.gcd(p, q) == 1 and q != s and F(p, q) != F(1, s))
    rhs = fraction(r, 11, (2, 3, 4, 6))
    small(rhs / (F(p, q) - F(1, s)), 12)
    return f"{over(f'{p} {v}', q)} - {over(v, s)} = {rhs}"

def t4_binomials(r, v):                    # (6x + 8)/2 = (4x - 12)/4, (q + 2)/3 = (q - 1)/4
    a, c = r.sample((2, 3, 4, 5, 6), 2)
    k1, k2 = r.choice((1, a, 2 * a, 3 * a)), r.choice((1, c))
    b, d = signed(r, 1, 6) * (a if k1 > 1 else 1), signed(r, 1, 12) * (c if k2 > 1 else 1)
    need(F(k1, a) != F(k2, c))
    x = (F(d, c) - F(b, a)) / (F(k1, a) - F(k2, c))
    small(x, 4)
    return f"{over(written((k1, v), (b, '')), a)} = {over(written((k2, v), (d, '')), c)}"

def t4_fraction_times(r, v):               # 1/4 (k - 2) = 2/3
    a, b = r.randint(2, 6), signed(r, 1, 9)
    c = fraction(r, 7, (2, 3, 4, 5, 6))
    need(c.denominator != a)
    x = a * c - b
    small(x, 12)
    return f"1/{a} ({written((1, v), (-b, ''))}) = {c}"

# ------------------------------------------------------------------
# Type 5: distribute on both sides
# ------------------------------------------------------------------
def t5_fraction(r, v):                     # 3/4 (8d + 16) = 5(d - 2) + 2
    f = fraction(r, 7, (2, 3, 4, 8))
    q = f.denominator
    a, b = q * r.randint(1, 3), q * r.randint(1, 4)
    c, d, e = r.randint(2, 9), r.randint(1, 5), r.randint(1, 9)
    need(f * a != c)
    x = (c * -d + e - f * b) / (f * a - c)
    small(x, 2)
    return f"{f} ({a} {v} + {b}) = {written((c, paren(f'{v} - {d}')), (e, ''))}"

def t5_hundred(r, v):                      # 100(x - 0.3) = -20(4x + 0.6)
    b, k, d = F(r.randint(1, 9), 10), 10 * r.randint(1, 5), r.randint(2, 4)
    e = F(r.randint(1, 9), 10)
    x = (100 * b - k * e) / (100 + k * d)
    need(x != 0 and places(x, 3))
    return f"100 ({v} - {dec(b)}) = -{k} ({d} {v} + {dec(e)})"

def t5_decimals(r, v):                     # 0.25(y - 0.4) = 3 - 0.5(1 - y)
    a, d = (F(r.choice((1, 2, 3, 4, 5, 6, 7, 8, 9)), r.choice((10, 20))) for _ in range(2))
    b, c = F(r.randint(1, 9), 10), r.randint(2, 6)
    need(a != d)
    x = (a * b + c - d) / (a - d)
    need(x != 0 and places(x, 2) and abs(x) <= 60)
    return f"{dec(a)} ({v} - {dec(b)}) = {c} - {dec(d)} (1 - {v})"

# ------------------------------------------------------------------
# Type 6: mixtures
# ------------------------------------------------------------------
def mixture(r):
    """low < mix < high, as percents, a total, and the amount of the low one."""
    low, high = sorted(r.sample(range(5, 60, 5), 2))
    mix, total = r.randrange(low + 5, high, 5) if high - low > 5 else None, 10 * r.randint(2, 10)
    need(mix is not None)
    x = F(total * (high - mix), high - low)
    need(x.denominator == 1 and 0 < x < total)
    return F(low, 100), F(mix, 100), F(high, 100), total

def pct(q):
    return f"{float(q):.2f}"

def t6_total_first(r, v):                  # (0.25)(20) = 0.15x + 0.35(20 - x)
    low, mix, high, total = mixture(r)
    return f"{pct(mix)} ({total}) = {pct(low)} {v} + {pct(high)} ({total} - {v})"

def t6_total_last(r, v):                   # 0.2x + 0.5(40 - x) = 0.35(40)
    low, mix, high, total = mixture(r)
    return f"{pct(low)} {v} + {pct(high)} ({total} - {v}) = {pct(mix)} ({total})"

def t6_high_first(r, v):                   # 0.5x + 0.2(40 - x) = 0.35(40)
    low, mix, high, total = mixture(r)
    return f"{pct(high)} {v} + {pct(low)} ({total} - {v}) = {pct(mix)} ({total})"

# ------------------------------------------------------------------
# Special Case A: no solution or all real numbers
# ------------------------------------------------------------------
def ta_fraction(r, v, all_):               # 12(5 - 2m) = 72(-m/3 + 1), 9(2 - 4m) = 18(-2m + 2)
    a, k, b = r.randint(2, 24), r.randint(2, 6), r.randint(1, 9)
    c = k * r.randint(1, 2) if r.random() < 0.5 else r.randint(1, 5)
    m = F(c, k)                    # a c v = a k (m v): -m v inside
    g = F(a * b, a * k) if all_ else F(other(r, a * b), a * k)
    need(g.denominator == 1 and g != 0)
    inner = written((-m, v), (g, "")) if m.denominator == 1 else plus(f"-({m.numerator} {v})/{m.denominator}" if m.numerator > 1 else f"-{v}/{m.denominator}", g)
    return f"{a} ({written((b, ''), (-c, v))}) = {a * k} ({inner})"

def ta_fraction_front(r, v, all_):         # 3/4 (8d + 16) = 6(d + 2), 3/4 (8d + 16) = 5(d - 2) + d + 20
    f = fraction(r, 7, (2, 3, 4, 8))
    q = f.denominator
    a, b = q * r.randint(1, 3), q * r.randint(1, 4)
    slope, const = f * a, f * b               # integers
    c = r.randint(2, min(int(slope) + 3, 9))
    need(c != slope)
    d = r.randint(1, 5)
    e = const + c * d if all_ else other(r, const + c * d)
    rest = written((slope - c, v), (e, ""))
    return f"{f} ({a} {v} + {b}) = {written((c, paren(f'{v} - {d}')))} + {rest}".replace("+ -", "- ")

TEMPLATES = {
    "1": [t1_minus, t1_large, t1_number_first],
    "2": [t2_distribute, t2_combine, t2_both],
    "3": [t3_product_over, t3_number_before, t3_plus_term, t3_both_sides, t3_fraction_times, t3_nested],
    "4": [t4_coefficients, t4_parts, t4_fraction_terms, t4_letter_over, t4_binomials, t4_fraction_times],
    "5": [t5_fraction, t5_hundred, t5_decimals],
    "6": [t6_total_first, t6_total_last, t6_high_first],
    "A": [ta_fraction, ta_fraction_front],
}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    if entry == "A":
        all_ = r.random() < 0.5
        prompt = TEMPLATES[entry][tpl](r, v, all_)
        need(linear.count(prompt) == ("all" if all_ else "none"))
    else:
        prompt = TEMPLATES[entry][tpl](r, v)
        need(linear.count(prompt) == "one")
    return dict(prompt=prompt, answer=linear.key(prompt))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if linear.keyed(p["prompt"], p["answer"]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, _, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    linear.key, check, "1/4 (n - 8) = -5 n + 7", "n = 12/7")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
