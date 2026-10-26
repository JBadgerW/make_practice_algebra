"""Lesson 1-2: linear equations of one to three steps, from the teacher's
equation banks for Lessons 1-2 and 1-3 (~/Documents/alg1/unit_1, every
problem rated 1 to 3 there). The harder ones, rated 4 and 5, are
equations_1_3.

The types follow the moves, and every equation in those banks is one some
template here can draw: integer, decimal, and fraction coefficients alike.
Problems are built backward from the solution; the last number written makes
it the solution.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "-3 = -7 t + 9 + 3 t"
    answer  "t = 3", "r = 17.5" (the prompt has decimals), "x = 40/11",
            "no solution", or "all real numbers"
check() solves the prompt with sympy and compares (sheets/linear.py: key, keyed).
"""
from decimal import Decimal
from fractions import Fraction as F
from .. import gen, linear
from ..gen import need, signed, signed_except, except_, written

NAME = FAMILY = "equations_1_2"
FIXED = False
TITLE = "Lesson 1-2: Solving Linear Equations"
INSTRUCTIONS = "Solve each equation."
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Two Steps",
         look="One variable term and one number on a side: 5x + 12 = 37, x/4 + 7 = 12, 0.2r - 3 = 0.5.",
         move="Undo the adding or subtracting, then undo the multiplying or dividing."),
    dict(key="2", title="Combine Like Terms First",
         look="Two variable terms, or two numbers, on the same side.",
         move="Combine the like terms on that side. Then solve in two steps."),
    dict(key="3", title="Distribute First",
         look="A number times parentheses, and nothing else on that side: 6(p - 12) = 90.",
         move="Distribute (or divide both sides by the number). Then solve in two steps.",
         space="1.25in"),
    dict(key="4", title="Distribute, Then Combine",
         look="A product to distribute, with another term on the same side; -( ... ) is -1 times the parentheses.",
         move="Distribute, combine like terms on that side, then solve.",
         space="1.25in"),
    dict(key="5", title="A Binomial over a Number",
         look="(x - 7)/4 with a number added or subtracted outside the fraction.",
         move="Undo the number outside, multiply by the denominator, then undo the number inside.",
         space="1.25in"),
    dict(key="6", title="Variable on Both Sides",
         look="A variable term on each side, nothing to distribute.",
         move="Gather the variable terms on one side and the numbers on the other. Then divide.",
         space="1.25in"),
    dict(key="7", title="Distribute, Then Variable on Both Sides",
         look="Parentheses, and the variable on both sides.",
         move="Distribute and combine on each side. Then gather the variable terms on one side and solve.",
         space="1.5in"),
    dict(key="A", title="No Solution or All Real Numbers", special=True,
         look="The variable terms are (or become) the same on both sides.",
         move="Simplify both sides. When the variable terms cancel, a true statement means all real numbers; "
              "a false one means no solution.",
         space="1.25in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Writing numbers and terms
# ------------------------------------------------------------------
def dec(q):
    """A Fraction with a terminating decimal, as a Decimal (written as one)."""
    q = F(q)
    d = Decimal(q.numerator) / Decimal(q.denominator)
    need(F(d) == q)
    return d

def places(q, n):
    """q has at most n decimal places."""
    return (F(q) * 10 ** n).denominator == 1

def over(top, a):
    """top/a, as Typst: "x/4", "(x - 7)/4"."""
    return f"{top}/{a}" if top.isalpha() else f"({top})/{a}"

def plus(text, n):
    """text + n with the sign written: plus("x/4", -3) is "x/4 - 3"."""
    return written((1, text), (n, ""))

def flip(r, left, right, chance=0.5):
    """left = right, or the sides swapped."""
    return f"{right} = {left}" if r.random() < chance else f"{left} = {right}"

def solution(r, lo=-10, hi=12):
    return except_(r, lo, hi, 0)

# ------------------------------------------------------------------
# Type 1: two steps
# ------------------------------------------------------------------
def t1_integers(r, v):                     # 5x + 12 = 37
    x, a, b = solution(r), signed(r, 2, 9), signed(r, 1, 20)
    return flip(r, written((a, v), (b, "")), a * x + b, 0.25)

def t1_divide(r, v):                       # x/4 + 7 = 12
    a, q, b = r.randint(2, 9), signed(r, 1, 10), signed(r, 1, 15)
    return flip(r, plus(over(v, a), b), q + b, 0.25)

def t1_fraction(r, v):                     # 1/3 x + 5 = 3
    a, q, b = r.randint(2, 6), signed(r, 1, 6), signed(r, 1, 12)
    k = r.choice((1, 1, 1, 2, 3))
    need(k < a and F(k, a).denominator == a)
    return flip(r, written((F(k, a), v), (b, "")), k * q + b, 0.25)

def t1_decimal(r, v):                      # 0.2r - 3 = 0.5
    a = F(r.choice((2, 4, 5, 6, 8, 12, 15, 25, 75)), r.choice((10, 100)))
    need(places(a, 2) and a != 1)
    x = F(signed(r, 1, 40), 2) if places(a, 1) else F(signed(r, 1, 20))
    b = signed(r, 1, 9)
    c = a * x + b
    need(places(c, 2) and c != 0)
    return f"{written((dec(a), v), (b, ''))} = {written((dec(c), ''))}"

# ------------------------------------------------------------------
# Type 2: combine like terms first
# ------------------------------------------------------------------
def t2_numbers(r, v):                      # 0.25 + t + 0.4 = 2
    c = F(r.randint(4, 20), 4)
    p, q = F(r.randint(1, 19), 20), F(r.randint(1, 19), 20)
    x = c - p - q
    need(x > 0)
    return f"{written((dec(p), ''), (1, v), (dec(q), ''))} = {written((dec(c), ''))}"

def t2_times(r, v):                        # 6x + 3(2x) = 48
    x, a, b, k = solution(r, -6, 10), r.randint(2, 9), r.randint(2, 6), r.randint(2, 3)
    return f"{written((a, v), (b, f'({k} {v})'))} = {(a + b * k) * x}"

def t2_split(r, v):                        # -3 = -7t + 9 + 3t
    x, a, b = solution(r, -8, 8), signed(r, 2, 12), signed(r, 1, 20)
    c = -r.choice((1, -1)) * (a // abs(a)) * r.randint(1, 9)
    need(a + c != 0 and abs(a + c) != 1)
    return flip(r, written((a, v), (b, ""), (c, v)), (a + c) * x + b, 0.6)

def t2_twice(r, v):                        # -0.75t - 0.75t - 2.4 = -6.9
    a = r.choice((-1, 1)) * F(r.choice((25, 35, 45, 55, 65, 75)), 100)
    b, x = F(signed(r, 1, 50), 10), solution(r, -6, 8)
    c = 2 * a * x + b
    need(c != 0)
    return f"{written((dec(a), v), (dec(a), v), (dec(b), ''))} = {written((dec(c), ''))}"

def t2_consecutive(r, v):                  # x + (x + 1) + (x + 2) = 96
    s, n, x = r.choice((1, 1, 2)), r.choice((3, 3, 4)), r.randint(-20, 60)
    terms = [v] + [f"({v} + {s * i})" for i in range(1, n)]
    return f"{' + '.join(terms)} = {n * x + s * n * (n - 1) // 2}"

def t2_grouped(r, v):                      # 3.5 = 4.5x + (9.5 - 7.5x)
    a, b, c = (F(r.randint(1, 9)) + F(1, 2) for _ in range(3))
    need(a != c)
    x = r.choice((F(signed(r, 1, 5)), F(signed(r, 1, 5), 2)))
    d = (a - c) * x + b
    need(places(d, 1) and d != 0)
    group = "(" + written((dec(b), ""), (-dec(c), v)) + ")"
    return f"{written((dec(d), ''))} = {written((dec(a), v), (1, group))}"

# ------------------------------------------------------------------
# Type 3: distribute first
# ------------------------------------------------------------------
def t3_integers(r, v):                     # 6(p - 12) = 90
    a, b, x = r.randint(3, 9), signed(r, 4, 25), r.randint(-10, 50)
    need(x - b != 0)
    return f"{a} ({written((1, v), (-b, ''))}) = {a * (x - b)}"

def t3_number_first(r, v):                 # 84 = -3(2r - 6)
    a, b, d, x = signed(r, 2, 9), r.randint(2, 4), signed(r, 2, 9), solution(r)
    need(b * x + d != 0 and abs(a * (b * x + d)) <= 150)
    return f"{a * (b * x + d)} = {a} ({written((b, v), (d, ''))})"

def t3_fraction(r, v):                     # 1/3 (2x + 1) = 15
    a, b, d, x = r.randint(2, 5), r.randint(2, 5), signed(r, 1, 9), solution(r, -5, 25)
    need(b % a != 0 and (b * x + d) % a == 0 and b * x + d != 0)
    return f"1/{a} ({written((b, v), (d, ''))}) = {(b * x + d) // a}"

def t3_decimal(r, v):                      # 0.5(4x - 6) = 17
    a = F(r.choice((1, 1, 3)), r.choice((2, 4)))
    k = a.denominator
    b, d, x = k * r.randint(1, 3), k * signed(r, 1, 3), solution(r)
    need(a * (b * x + d) != 0)
    return f"{dec(a)} ({written((b, v), (d, ''))}) = {a * (b * x + d)}"

def t3_small(r, v):                        # 0.045(q + 3) = 2.34
    a, d, x = F(r.choice((15, 25, 35, 45, 55, 65)), 1000), r.randint(2, 9), r.randint(10, 99)
    c = a * (x + d)
    need(places(c, 2))
    return f"{dec(a)} ({v} + {d}) = {dec(c)}"

TEMPLATES_3 = [t3_integers, t3_number_first, t3_fraction, t3_decimal, t3_small]

# ------------------------------------------------------------------
# Type 4: distribute, then combine
# ------------------------------------------------------------------
def t4_plus(r, v):                         # -5x + 4(3x + 2) = 50
    a, b, c, d, x = signed(r, 2, 7), r.randint(2, 7), r.randint(2, 4), r.randint(1, 5), solution(r, -5, 9)
    need(a + b * c not in (0, 1, -1))
    group = "(" + written((c, v), (d, "")) + ")"
    return f"{written((a, v), (b, group))} = {(a + b * c) * x + b * d}"

def t4_minus(r, v):                        # -(9 - 3x) + 5 = -10
    d, c, b, x = r.randint(2, 9), r.randint(2, 5), signed(r, 1, 9), solution(r, -5, 5)
    group = "(" + written((d, ""), (-c, v)) + ")"
    return f"{written((-1, group), (b, ''))} = {c * x - d + b}"

def t4_eighths(r, v):                      # 0.875(x + 4) - 7 = 0
    a, m, x = F(r.choice((1, 3, 5, 7)), 8), r.randint(1, 4), r.randint(1, 24)
    d = 8 * m - x
    need(d > 0)
    return f"{written((dec(a), f'({v} + {d})'), (-a * 8 * m, ''))} = 0"

# ------------------------------------------------------------------
# Type 5: a binomial over a number
# ------------------------------------------------------------------
def binomial(r, v):
    """(v + b)/a, and its value q at the solution."""
    a, q, b = r.randint(2, 9), r.randint(1, 10), signed(r, 2, 30)
    need(a * q - b != 0)
    return over(written((1, v), (b, "")), a), q

def t5_after(r, v):                        # (x - 7)/4 - 3 = 5
    f, q = binomial(r, v)
    c = signed(r, 1, 9)
    return f"{plus(f, c)} = {q + c}"

def t5_before(r, v):                       # 6 + (x - 7)/4 = 9
    f, q = binomial(r, v)
    c = signed(r, 1, 9)
    return f"{written((c, ''), (1, f))} = {q + c}"

def t5_right(r, v):                        # 5 = (x - 7)/4 - 3
    left, _, right = t5_after(r, v).partition(" = ")
    return f"{right} = {left}"

# ------------------------------------------------------------------
# Type 6: variable on both sides
# ------------------------------------------------------------------
def t6_both(r, v):                         # 7n - 23 = 3n + 5
    a, c, x, b = r.randint(2, 9), r.randint(1, 9), solution(r, -6, 12), signed(r, 1, 40)
    need(a != c)
    d = (a - c) * x + b
    need(d != 0 and abs(d) <= 40)
    return f"{written((a, v), (b, ''))} = {written((c, v), (d, ''))}"

def t6_one_number(r, v):                   # 6x - 5 = 5x, 9x = 10x + 15, -x = 9x - 60, 40 - 3x = 8x
    a, c = signed(r, 1, 12), signed(r, 1, 12)
    need(a != c)
    x = F(signed(r, 1, 20)) if r.random() < 0.8 else F(signed(r, 10, 60), c - a)
    b = (c - a) * x
    need(b.denominator == 1 and b != 0 and abs(b) <= 90 and x.denominator <= 15)
    shape = r.randrange(3)
    if shape == 0:
        return f"{written((a, v), (b, ''))} = {written((c, v))}"
    if shape == 1:
        return f"{written((c, v))} = {written((a, v), (b, ''))}"
    return f"{written((b, ''), (a, v))} = {written((c, v))}"

def t6_negatives(r, v):                    # -4k + 5 = -3 - 8k
    a, c, x, b = -r.randint(1, 9), -r.randint(1, 12), solution(r), signed(r, 1, 15)
    need(a != c)
    d = (a - c) * x + b
    need(d != 0 and abs(d) <= 30)
    return f"{written((a, v), (b, ''))} = {written((d, ''), (c, v))}"

def t6_same_number(r, v):                  # 42 - 5x = 5x + 42
    a, c, b = signed(r, 2, 9), signed(r, 2, 9), r.randint(10, 60)
    need(a != c)
    return f"{written((b, ''), (a, v))} = {written((c, v), (b, ''))}"

def t6_decimals(r, v):                     # 0.79s + 15 = 0.85s, 5x + 3 = 4.75x + 5, 60 - 3p = 45 - 2.5p
    step = F(1, r.choice((100, 10, 4, 2)))
    a = F(r.randint(1, 9)) if r.random() < 0.4 else step * r.randint(1, 99 if step == F(1, 100) else int(10 / step))
    diff = step * signed(r, 1, 9) if step < F(1, 4) else F(signed(r, 1, 9), r.choice((10, 4, 2)))
    c = a + diff
    need(a > 0 and c > 0 and (a.denominator > 1 or c.denominator > 1))
    if r.random() < 0.3:                   # both negative
        a, c = -a, -c
    x = r.randint(1, 10) * 50 if diff.denominator in (25, 50, 100) else r.randint(1, 20)
    b = r.choice((0, signed(r, 1, 60)))
    d = (a - c) * x + b
    need(places(d, 2))
    left = written((dec(a), v), (b, "")) if r.random() < 0.5 else written((b, ""), (dec(a), v))
    right = written((dec(c), v), (dec(d), "")) if r.random() < 0.5 else written((dec(d), ""), (dec(c), v))
    return f"{left} = {right}"

def t6_decimal_answer(r, v):               # 0.75t = 0.75 - 0.5t
    a, c = (F(r.choice((1, 2, 3, 4, 5, 6, 8, 10, 12, 15)), r.choice((4, 10))) for _ in range(2))
    b = F(r.randint(1, 100), 20)
    x = b / (a + c)
    need(places(x, 1) and places(a, 2) and places(c, 2) and x.denominator > 1 and (a.denominator > 1 or c.denominator > 1))
    return f"{written((dec(a), v))} = {written((dec(b), ''), (-dec(c), v))}"

# ------------------------------------------------------------------
# Type 7: distribute, then the variable on both sides
# ------------------------------------------------------------------
def inside(r, v, b, d):
    """(b v + d) or (d + b v)."""
    return f"({written((b, v), (d, '')) if d < 0 or r.random() < 0.7 else written((d, ''), (b, v))})"

def t7_one_side(r, v):                     # 4(3x + 7) = 9x + 55, -4(6 + 2h) = 3h + 9, 5(x + 6) = x + 6
    a, b, d, x = signed(r, 2, 7), r.randint(1, 3), signed(r, 1, 9), solution(r, -8, 10)
    c = signed_except(r, 1, 12, a * b)
    e = a * (b * x + d) - c * x
    need(abs(e) <= 70)
    return flip(r, written((a, inside(r, v, b, d))), written((c, v), (e, "")), 0.2)

def t7_no_number(r, v):                    # 3x = 5(x - 6), 4(x - 3) = 10x, 5(h - 0.4) = 4h
    a, c = r.randint(2, 9), signed(r, 1, 15)
    need(a != c)
    if r.random() < 0.25:                  # a decimal inside: the solution is a decimal too
        d = r.choice((-1, 1)) * F(r.choice((1, 2, 4, 5, 6, 8)), r.choice((4, 10)))
        need(places(d, 2))
        x = a * d / (c - a)
        need(places(x, 2))
        d = dec(d)
    else:
        x = solution(r, -25, 25)
        d = F((c - a) * x, a)
        need(d.denominator == 1)
    return flip(r, written((a, f"({written((1, v), (d, ''))})")), written((c, v)))

def t7_two_products(r, v):                 # 4(n - 9) = 3(n + 4)
    a, c, b, x = r.randint(2, 9), r.randint(2, 9), signed(r, 1, 9), solution(r, -10, 50)
    need(a != c and (a * b - c * x + a * x) % c == 0)
    d = (a * (x + b) - c * x) // c
    need(d not in (0, b) and abs(d) <= 12)
    return f"{a} ({written((1, v), (b, ''))}) = {c} ({written((1, v), (d, ''))})"

def t7_combine(r, v):                      # 3(x + 4) = 4x + 2 + x
    a, b, x = r.randint(2, 9), signed(r, 1, 9), solution(r)
    c, e = r.randint(1, 9), signed(r, 1, 9)
    need(c + e != a and c + e != 0)
    d = a * (x + b) - (c + e) * x
    need(d != 0 and abs(d) <= 40)
    return f"{a} ({written((1, v), (b, ''))}) = {written((c, v), (d, ''), (e, v))}"

def t7_right(r, v):                        # 9w - 40 = 5(3w - 8), -5(4 + 3h) = 4h + 18
    a, b, e, x = r.randint(2, 9), r.randint(2, 6), signed(r, 2, 9), solution(r, -6, 6)
    c = except_(r, 2, 12, a * b)
    d = a * (b * x - e) - c * x
    need(d != 0 and abs(d) <= 60)
    return f"{written((c, v), (d, ''))} = {a} ({written((b, v), (-e, ''))})"

def t7_opposite(r, v):                     # x - 5 = -(x - 5)
    b = r.randint(2, 40) * r.choice((1, 1, 1, -1))
    side = written((1, v), (-b, ""))
    return f"{side} = -({side})"

# ------------------------------------------------------------------
# Special Case A: no solution or all real numbers
# ------------------------------------------------------------------
def other(r, n):
    """A number that isn't n, the way a slip would change it: its opposite, or off by a little."""
    return r.choice([m for m in (-n, n + signed(r, 1, 9), n + signed(r, 1, 9)) if m != n])

def ta_same(r, v, all_):                   # 5c - 2 = 5c - 2, 9b + 4 = 9b + 7
    a, b = signed(r, 2, 20), signed(r, 1, 9)
    return f"{written((a, v), (b, ''))} = {written((a, v), (b if all_ else other(r, b), ''))}"

def ta_split(r, v, all_):                  # 5x = 3x + 2x
    a, c = r.randint(2, 9), signed(r, 1, 9)
    need(a != c and a - c not in (0, 1))
    return f"{written((a, v))} = {written((c, v), (a - c, v), (0 if all_ else signed(r, 1, 12), ''))}"

def ta_distribute(r, v, all_):             # 6x + 9 = 3(2x + 3), 8x - 3 = 4(2x + 5)
    a, b, d = r.randint(2, 6), r.randint(2, 5), signed(r, 1, 9)
    e = a * d if all_ else other(r, a * d)
    return flip(r, written((a * b, v), (e, "")), f"{a} ({written((b, v), (d, ''))})", 0.2)

def ta_minus(r, v, all_):                  # t - 14 = -(14 - t)
    b = r.randint(2, 60)
    c = b if all_ else other(r, b)
    need(c > 0)
    return f"{written((1, v), (-b, ''))} = -({written((c, ''), (-1, v))})"

def ta_two_products(r, v, all_):           # 3(y - 4) = 4(y - 3) - y
    a, c = r.choice([(a, c) for a in range(2, 7) for c in range(2, 7) if a != c])
    k = r.choice((1, 1, 2))
    b, d = c * k, a * k                    # a b = c d
    rest = a - c
    out = written((c, f"({written((1, v), (-d if all_ else -other(r, d), ''))})"), (rest, v))
    return f"{a} ({written((1, v), (-b, ''))}) = {out}"

def ta_fraction(r, v, all_):               # (8x + 10)/2 - 5 = 4x
    a, b, d = r.randint(2, 4), r.randint(2, 6), r.randint(1, 9)
    e = d if all_ else other(r, d)
    need(e > 0)
    return f"{plus(over(written((a * b, v), (a * d, '')), a), -e)} = {written((b, v))}"

TEMPLATES = {
    "1": [t1_integers, t1_divide, t1_fraction, t1_decimal],
    "2": [t2_numbers, t2_times, t2_split, t2_twice, t2_consecutive, t2_grouped],
    "3": TEMPLATES_3,
    "4": [t4_plus, t4_minus, t4_eighths],
    "5": [t5_after, t5_before, t5_right],
    "6": [t6_both, t6_one_number, t6_negatives, t6_same_number, t6_decimals, t6_decimal_answer],
    "7": [t7_one_side, t7_no_number, t7_two_products, t7_combine, t7_right, t7_opposite],
    "A": [ta_same, ta_split, ta_distribute, ta_minus, ta_two_products, ta_fraction],
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
typst, _answer_typst, text, answer_text, height = gen.shown()

def answer_typst(p):
    return p["answer"] if p["answer"] in (linear.NONE, linear.ALL) else _answer_typst(p)

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    linear.key, check, "-3 = -7 t + 9 + 3 t", "t = 3")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
