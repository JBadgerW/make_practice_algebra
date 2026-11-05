"""Adding and subtracting rational expressions (Advanced Math), from the
50-problem practice set "Adding & Subtracting Rational Expressions Practice"
(~/Documents/adv_math/adding_rational_expressions/).

The set's 50 problems are 16 types, each a step past the one before:

    1  (1-2)    like denominators, a number             (x - 4)/3 + (5 x)/3
    2  (3-5)    like denominators, a monomial; two of three reduce to a number
    3  (6,7,11) like binomial denominators, subtraction: the minus reaches every term
    4  (8-10)   like denominators k (x + a), number numerators: the k cancels
    5  (12-18)  like quadratic denominators: the new numerator is one of its factors
    6  (19-22)  unlike monomials, one is the LCD:   6/x + 7/(5 x^2)
    7  (26-27)  unlike monomials, both rewritten:   (5 x - 3)/(4 x) - 1/(6 x)
    8  (23-24)  monomials in two letters:           6/(5 x^3 y) - 1/(2 x^2 y^3)
    9  (25,28,29) a whole term and a fraction:      7 - 4/(x - 9)
    10 (30-32)  a binomial and a trinomial denominator, subtracted; it reduces to 1/(x + c)
    11 (33-40)  two quadratics sharing a factor (the second a difference of squares)
    12 (41-42)  two quadratics sharing none, numbers c and -c on top: four factors
    13 (43-44)  a whole number, a binomial, and a difference of squares
    14 (45-46)  three fractions, the third already over the LCD; the x^2 terms cancel
    15 (47-48)  three fractions, one denominator the opposite of a factor: 1 - x
    16 (49-50)  three trinomials in a chain, numerators k, -2 k, k: four factors

The set's choices are kept: like denominators come before unlike ones; the
like-denominator types are built to reduce (2, 4, 5, 10) or to test the
minus sign (3); the numbers stay small; the three-fraction types are built
so the x^2 terms cancel, leaving a short numerator. Answers never reduce in
Types 11-16, as in the set's key.

The key writes one fraction: the numerator multiplied out, the denominator
factored, its factors in the order the problem first shows them, a repeated
factor as a power, (x + 3)^2 (x - 3). A monomial denominator stays one
monomial, 10 x^3 y^3. A leading minus goes in front of the fraction, as in
the other Advanced Math banks (the set writes -2x^2 + 9x - 8 on top).

check() reads the prompt and the answer back with to_sympy, compares their
values at random points, and reads the answer's form from its text: lowest
terms, the numerator multiplied out, and the denominator a product of
numbers, letters, and first-degree factors.

A problem: dict(type, prompt, answer, source), both in Typst math.
    prompt  "(x - 4)/(x^2 + 5 x + 6) + (x - 1)/(x^2 - 4)"
    answer  "(2 x^2 - 4 x + 5)/((x + 2) (x + 3) (x - 2))"
"""
import random, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, simplest_form, parts, _evaluated
from ..typmath import Printer, tx, fr

NAME = FAMILY = "adv_rational_add"
FIXED = False
TITLE = "Adding and Subtracting Rational Expressions"
INSTRUCTIONS = "Add or subtract. Simplify if possible."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Like Denominators: A Number",
         look="Two fractions over the same number.",
         move="Add or subtract the numerators. Keep the denominator."),
    dict(key="2", title="Like Denominators: A Monomial",
         look="Two fractions over the same monomial, like 4x.",
         move="Add or subtract the numerators and keep the denominator. If the letter is left on top alone, "
              "it cancels with the one below."),
    dict(key="3", title="Like Binomial Denominators: Subtracting",
         look="One fraction minus another, over the same binomial.",
         move="Put the second numerator in parentheses. The minus changes the sign of every term in it."),
    dict(key="4", title="Like Denominators with a Number Factor",
         look="Number numerators over the same k(x + a).",
         move="Add the numerators. The number on top divides by k, leaving a number over (x + a)."),
    dict(key="5", title="Like Quadratic Denominators",
         look="Two fractions over the same quadratic.",
         move="Combine the numerators. Factor the denominator; the new numerator is one of its factors, "
              "so it cancels.", space="1.5in"),
    dict(key="6", title="Unlike Monomials: One Is the LCD",
         look="Monomial denominators, one dividing the other: x and 5x².",
         move="The larger denominator is the LCD. Multiply the other fraction, top and bottom, by what it lacks."),
    dict(key="7", title="Unlike Monomials: Both Rewritten",
         look="Monomial denominators like 4x and 6x, or 3x and 5x², neither dividing the other.",
         move="The LCD takes the least common multiple of the numbers and the highest power of the letter. "
              "Rewrite both fractions over it.", space="1.25in"),
    dict(key="8", title="Monomials in Two Letters",
         look="Denominators like 5x³y and 2x²y³.",
         move="The LCD takes the least common multiple of the numbers and the highest power of each letter. "
              "Rewrite both fractions over it.", space="1.25in"),
    dict(key="9", title="A Whole Term and a Fraction",
         look="A number or a monomial added to a fraction: 5/x + 8, 7 - 4/(x - 9).",
         move="Write the whole term over 1, then over the fraction's denominator, and combine."),
    dict(key="10", title="A Binomial and a Trinomial", width="full",
         look="A fraction over x - b, minus one over a trinomial that has x - b as a factor.",
         move="Factor the trinomial: it is the LCD. Multiply the first fraction by the factor it lacks, subtract "
              "(the minus reaches every term), and cancel the factor left on top.", space="1.75in"),
    dict(key="11", title="Two Quadratics with a Common Factor", width="full",
         look="Two fractions over quadratics, the second a difference of squares.",
         move="Factor both denominators. The LCD has the common factor once and each other factor. "
              "Multiply each fraction by the factor it lacks and combine.", space="2in"),
    dict(key="12", title="Two Quadratics with No Common Factor", width="full",
         look="Number numerators, c and -c, over two quadratics that share no factor.",
         move="Factor both. The LCD is all four factors. Multiply each fraction by the other's two factors and "
              "combine; the x² terms cancel.", space="2in"),
    dict(key="13", title="A Number and Two Fractions", width="full",
         look="A whole number plus x/(x + a), minus a fraction over x² − a².",
         move="The LCD is (x + a)(x - a). Write the whole number over it, rewrite the binomial fraction, "
              "and combine all three numerators.", space="2in"),
    dict(key="14", title="Three Fractions, One over the LCD", width="full",
         look="Two binomial denominators and a third that is their product.",
         move="The third denominator is the LCD. Rewrite the first two over it and combine; the x² terms "
              "cancel.", space="2in"),
    dict(key="15", title="Opposite Denominators", width="full",
         look="Three fractions, one over a denominator like 1 − x where another has x - 1.",
         move="Multiply the fraction over 1 − x by -1/-1 so it is over x - 1. Then the LCD is the difference "
              "of squares; combine the three.", space="2in"),
    dict(key="16", title="Three Trinomial Denominators", width="full",
         look="Three fractions over trinomials, each sharing a factor with the next.",
         move="Factor all three. The LCD is the four different factors. Multiply each fraction by the factors "
              "it lacks and combine; the x² terms cancel.", space="2.25in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The key's form
# ------------------------------------------------------------------
def _key(f):
    """A factor, up to its sign, for matching."""
    f = sp.expand(f)
    return sp.expand(-f) if f.could_extract_minus_sign() else f

def read(prompt):
    """The prompt's value; its fractions as written, (numerator, denominator); and
    its first-degree factors, in the order its denominators show them."""
    fractions = []
    def walk(e):
        if isinstance(e, sp.Mul):
            over = [a for a in e.args if isinstance(a, sp.Pow) and a.exp == -1]
            if over:
                top = sp.Mul(*[_evaluated(a) for a in e.args if not any(a is o for o in over)])
                fractions.append((top, sp.expand(sp.Mul(*[_evaluated(o.base) for o in over]))))
                return
        for a in e.args:
            walk(a)
    written_tree = to_sympy(prompt, evaluate=False)
    walk(written_tree)
    order = []
    for _, d in fractions:
        for f, _ in sp.factor_list(d)[1]:
            if not f.is_Symbol and _key(f) not in order:
                order.append(_key(f))
    letters = list(dict.fromkeys(re.findall(r"\b[a-z]\b", prompt)))    # in the order the prompt shows them
    return _evaluated(written_tree), fractions, order, letters

def combined(e):
    """A sum of fractions as one, in lowest terms: (numerator, denominator),
    worked as polynomials over the least common denominator."""
    xs = sorted(e.free_symbols, key=str)
    if not xs:
        return sp.fraction(sp.nsimplify(e))
    terms = [t.as_numer_denom() for t in sp.Add.make_args(e)]
    tops = [sp.Poly(n, *xs) for n, _ in terms]
    bottoms = [sp.Poly(d, *xs) for _, d in terms]
    lcd = bottoms[0]
    for b in bottoms[1:]:
        lcd = lcd.lcm(b)
    top = sum((t * lcd.exquo(b) for t, b in zip(tops, bottoms)), sp.Poly(0, *xs))
    if top.is_zero:
        return sp.Integer(0), sp.Integer(1)
    g = top.gcd(lcd)
    n, d = top.exquo(g), lcd.exquo(g)
    if d.LC() < 0:
        n, d = -n, -d
    return n.as_expr(), d.as_expr()

def written(n, d, order=(), letters=()):
    """n/d as the key writes it: one fraction, its numerator multiplied out, its
    denominator factored, the factors in `order` first, the letters in `letters` first."""
    if n == 0:
        return "0"
    c, fs = sp.factor_list(d)
    mono, rest = sp.Integer(c), []
    for f, m in fs:
        if f.is_Symbol:
            mono *= f ** m
        else:
            if f.could_extract_minus_sign():
                f, mono = -f, -mono
            rest.append((f, m))
    if mono.could_extract_minus_sign():
        n, mono = -n, -mono
    n = sp.expand(n)
    rest.sort(key=lambda fm: order.index(_key(fm[0])) if _key(fm[0]) in order else len(order))
    p = Printer(letters)
    two_letters = n.is_Add and len(n.free_symbols) > 1
    neg = (p.terms(n)[0] if n.is_Add else n).could_extract_minus_sign()
    if two_letters and any(not t.could_extract_minus_sign() for t in sp.Add.make_args(n)):
        neg = False                                   # (12 y^2 - 5 x): a plus term leads
    if neg:
        n = -n
    top = p.add(n, positive_first=True) if n.is_Add else p.expr(n)
    if d == 1 or (not rest and mono == 1):
        return ("-" if neg else "") + top
    pieces = [] if mono == 1 else [p.expr(mono)]
    pieces += [f"({p.expr(f)})" + (f"^{m}" if m > 1 else "") for f, m in rest]
    bottom = " ".join(pieces)
    if len(rest) == 1 and rest[0][1] == 1 and mono == 1:
        bottom = p.expr(rest[0][0])                   # x + 5: fr() adds the parentheses
    return ("-" if neg else "") + fr(top, bottom)

def answer_of(prompt):
    e, _, order, letters = read(prompt)
    need(not e.has(sp.zoo, sp.nan))
    return written(*combined(e), order, letters)

def key_form(a):
    """The answer's form, read from its text: in lowest terms, the numerator
    multiplied out, the denominator numbers, letters, and first-degree factors."""
    if not simplest_form(a):
        return False
    n, d = parts(a)
    if sp.expand(n) != n:
        return False
    for f in sp.Mul.make_args(d):
        b = f.base if f.is_Pow else f
        if b.is_Number or b.is_Symbol:
            continue
        if not (b.is_Add and sp.Poly(b).total_degree() == 1 and b == sp.expand(b)):
            return False
    return True

# ------------------------------------------------------------------
# Writing the pieces of a prompt
# ------------------------------------------------------------------
def P(e):
    """A polynomial, descending degree: x^2 - 5 x + 4."""
    return tx(sp.expand(e))

def const_first(c, a, x):
    """c + a x written number first, as the set writes 3 - 2x."""
    s = f"{c}"
    return s + (" + " if a > 0 else " - ") + tx(abs(a) * x)

def over(n, d):
    return fr(n if isinstance(n, str) else P(n), d if isinstance(d, str) else P(d))

def op(r, plus=0.5):
    return " + " if r.random() < plus else " - "

def combine(*pieces):
    return "".join(pieces)

def ints(r, lo, hi, n, *out):
    """n different nonzero integers in [-hi, -lo] or [lo, hi], none in out."""
    pool = [k for k in range(-hi, hi + 1) if abs(k) >= lo and k not in out]
    return r.sample(pool, n)

def letter(r):
    return sp.Symbol(r.choice(gen.LETTERS))

# ------------------------------------------------------------------
# Type 1 (1-2): like number denominators
# ------------------------------------------------------------------
def t1_two_binomials(r):                      # (2x + 5)/7 - x/7 ... with constants on both
    x = letter(r)
    d = r.randint(3, 9)
    a, c = r.randint(1, 6), r.randint(1, 6)
    b, e = gen.signed(r, 1, 9), gen.signed(r, 1, 9)
    s = op(r)
    return combine(over(a * x + b, str(d)), s, over(c * x + e, str(d)))

def t1_monomial(r):                           # (x - 4)/3 + (5 x)/3, (2x + 5)/7 - x/7
    x = letter(r)
    d = r.randint(3, 9)
    a, b, c = r.randint(1, 5), gen.signed(r, 1, 9), r.randint(1, 6)
    s = op(r)
    need((s == " + " or a != c) and sp.gcd(c, d) == 1)
    return combine(over(a * x + b, str(d)), s, over(c * x, str(d)))

# ------------------------------------------------------------------
# Type 2 (3-5): like monomial denominators
# ------------------------------------------------------------------
def t2_number_and_binomial(r):                # 8/x + (x + 9)/x
    x = letter(r)
    k = r.choice((1, 1, 2, 3, 4))
    a, b = r.randint(2, 9), r.randint(1, 9)
    c = r.randint(1, 3)
    need(sp.gcd(a, k) == 1 and sp.gcd(sp.gcd(c, a + b), k) == 1)     # the k x stays below
    return combine(over(str(a), tx(k * x)), " + ", over(c * x + b, tx(k * x)))

def answer_number(r):
    """(t, k): t x over k x is u/v in lowest terms, reduced by m = 2 to 4: 2/4, 6/24."""
    v = r.randint(2, 6)
    u = r.choice([n for n in range(1, v) if sp.gcd(n, v) == 1])
    m = r.choice([n for n in (2, 3, 4) if v * n <= 24] or [2])
    return u * m, v * m

def t2_to_a_number(r):                        # (3x - 8)/(4x) + (-x + 8)/(4x) = 1/2
    x = letter(r)
    tot, k = answer_number(r)
    a = r.randint(1, 6)
    b = gen.signed(r, 1, 9)
    c = tot - a                               # the x terms add to tot x, the numbers cancel
    need(c != 0)
    return combine(over(a * x + b, tx(k * x)), " + ", over(c * x - b, tx(k * x)))

def t2_subtract_to_a_number(r):               # (5x + 2)/(6x) - (2x + 2)/(6x) = 1/2
    x = letter(r)
    tot, k = answer_number(r)
    b = gen.signed(r, 1, 9)
    c = r.randint(1, 6)
    a = c + tot
    return combine(over(a * x + b, tx(k * x)), " - ", over(c * x + b, tx(k * x)))

# ------------------------------------------------------------------
# Type 3 (6, 7, 11): like binomial denominators, subtracting
# ------------------------------------------------------------------
def t3_subtract(r):                           # (2x + 3)/(x + 5) - (x - 3)/(x + 5)
    x = letter(r)
    p = gen.signed(r, 1, 9)
    a, c = r.randint(2, 5), r.randint(1, 4)
    need(a > c)
    b, e = gen.signed(r, 1, 9), gen.signed(r, 1, 9)
    return combine(over(a * x + b, x + p), " - ", over(c * x + e, x + p))

def t3_negative_constant(r):                  # the second numerator's minus becomes a plus
    x = letter(r)
    p = gen.signed(r, 1, 9)
    a, c = r.randint(2, 5), r.randint(1, 4)
    need(a > c)
    b, e = r.randint(1, 9), -r.randint(1, 9)
    return combine(over(a * x + b, x + p), " - ", over(c * x + e, x + p))

# ------------------------------------------------------------------
# Type 4 (8-10): number numerators over k (x + a)
# ------------------------------------------------------------------
def t4_sum(r, minus=False):                   # 8/(3 (x + 8)) + 4/(3 (x + 8)) = 4/(x + 8)
    x = letter(r)
    k = r.randint(2, 5)
    a = gen.signed(r, 1, 9)
    q = r.randint(2, 6)
    total = k * q
    m = r.randint(1, total - 1) if not minus else r.randint(total + 1, total + 9)
    n = total - m if not minus else m - total
    need(n > 0 and sp.gcd(m, k) == 1 and sp.gcd(n, k) == 1)
    d = f"{k} ({P(x + a)})"
    return combine(over(str(m), d), " - " if minus else " + ", over(str(n), d))

def t4_add(r):
    return t4_sum(r)

def t4_subtract(r):
    return t4_sum(r, minus=True)

# ------------------------------------------------------------------
# Type 5 (12-18): like quadratic denominators, reducing to 1/(x + q)
# ------------------------------------------------------------------
def quad(r, square=False):
    """(p, q) for (x + p)(x + q): a difference of squares, or a trinomial."""
    if square:
        a = r.randint(1, 9)
        return a, -a
    p, q = ints(r, 1, 7, 2)
    need(p != -q)
    return p, q

def t5_parts(r, square):
    x = letter(r)
    p, q = quad(r, square)
    if r.random() < 0.5:
        p, q = q, p                           # the numerator is x + p; the answer 1/(x + q)
    return x, p, q, sp.expand((x + p) * (x + q))

def t5_difference(r):                         # (5x + 1)/(x^2 - 64) - (4x - 7)/(x^2 - 64)
    x, p, q, D = t5_parts(r, square=r.random() < 0.6)
    c = r.randint(1, 5)
    e = gen.signed(r, 1, 9)
    a, b = c + 1, e + p
    need(b != 0)
    return combine(over(a * x + b, D), " - ", over(c * x + e, D))

def t5_sum_written_backward(r):               # (3x - 4)/(x^2 - 5x + 4) + (3 - 2x)/(x^2 - 5x + 4)
    x, p, q, D = t5_parts(r, square=r.random() < 0.3)
    a = r.randint(2, 6)
    b = gen.signed(r, 1, 9)
    c, e = 1 - a, p - b
    need(e != 0)
    second = const_first(e, c, x) if e > 0 else c * x + e
    return combine(over(a * x + b, D), " + ", over(second, D))

def t5_negative_leads(r):                     # (-2x + 1)/(x^2 - 4) - (-3x - 1)/(x^2 - 4)
    x, p, q, D = t5_parts(r, square=r.random() < 0.6)
    a = -r.randint(1, 4)
    c = a - 1
    b = gen.signed(r, 1, 9)
    e = b - p
    need(e != 0)
    return combine(over(a * x + b, D), " - ", over(c * x + e, D))

def t5_quadratic_tops(r):                     # (2x^2 + 7x - 3)/(x^2 + 4x - 12) - (2x^2 + 6x - 1)/(...)
    x, p, q, D = t5_parts(r, square=False)
    k = r.randint(2, 3)
    b, c = gen.signed(r, 1, 9), gen.signed(r, 1, 9)
    first = k * x ** 2 + b * x + c
    second = k * x ** 2 + (b - 1) * x + (c - p)
    need(b - 1 != 0 and c - p != 0)
    return combine(over(first, D), " - ", over(second, D))

# ------------------------------------------------------------------
# Type 6 (19-22): unlike monomials, one the LCD
# ------------------------------------------------------------------
def t6_x_and_kx2(r):                          # 6/x + 7/(5x^2)
    x = letter(r)
    k = r.randint(2, 9)
    a, b = r.randint(2, 9), r.randint(2, 9)
    need(sp.gcd(b, k) == 1)
    return combine(over(str(a), tx(x)), " + ", over(str(b), tx(k * x ** 2)))

def t6_kx_and_x(r):                           # 2/(3x) + 4/x
    x = letter(r)
    k = r.randint(2, 9)
    a, b = r.randint(1, 9), r.randint(1, 9)
    need(sp.gcd(a + k * b, k) == 1 and sp.gcd(a, k) == 1)
    return combine(over(str(a), tx(k * x)), " + ", over(str(b), tx(x)))

def t6_x2_and_kx(r):                          # 3/(4x^2) + 5/x
    x = letter(r)
    k = r.randint(2, 9)
    a, b = r.randint(1, 9), r.randint(2, 9)
    need(sp.gcd(a, k) == 1)
    return combine(over(str(b), tx(x)), op(r, 0.7), over(str(a), tx(k * x ** 2)))

# ------------------------------------------------------------------
# Type 7 (26-27): unlike monomials, both rewritten
# ------------------------------------------------------------------
def t7_shared_number(r):                      # (5x - 3)/(4x) - 1/(6x)
    x = letter(r)
    m, n = r.choice(((4, 6), (6, 4), (6, 8), (8, 6), (4, 10), (10, 4), (6, 9), (9, 6), (10, 15), (6, 10)))
    a, b, c = r.randint(2, 7), gen.signed(r, 1, 9), r.randint(1, 7)
    need(sp.gcd(c, n) == 1 and sp.gcd(sp.gcd(a, b), m) == 1)
    return combine(over(a * x + b, tx(m * x)), op(r, 0.4), over(str(c), tx(n * x)))

def t7_coprime_powers(r):                     # 7/(3x) - 4/(5x^2)
    x = letter(r)
    m, n = r.sample((2, 3, 4, 5, 7), 2)
    need(sp.gcd(m, n) == 1)
    a, c = r.randint(1, 9), r.randint(1, 9)
    need(sp.gcd(a, m) == 1 and sp.gcd(c, n) == 1)
    return combine(over(str(a), tx(m * x)), op(r, 0.4), over(str(c), tx(n * x ** 2)))

def t7_binomial_powers(r):                    # (x + 2)/(6x^2) - 3/(4x)
    x = letter(r)
    m, n = r.choice(((6, 4), (4, 6), (9, 6), (6, 9), (10, 4), (4, 10), (3, 2), (2, 3)))
    b, c = gen.signed(r, 1, 9), r.randint(1, 9)
    need(sp.gcd(c, n) == 1 and sp.gcd(b, m) == 1)
    return combine(over(x + b, tx(m * x ** 2)), op(r, 0.4), over(str(c), tx(n * x)))

# ------------------------------------------------------------------
# Type 8 (23-24): monomials in two letters
# ------------------------------------------------------------------
def t8_powers(r):                             # 6/(5x^3 y) - 1/(2x^2 y^3)
    x, y = (sp.Symbol(s) for s in gen.letters(r, 2))
    m, n = r.sample((2, 3, 4, 5, 7), 2)
    i, j = r.sample((1, 2), 2)
    a, c = r.randint(1, 9), r.randint(1, 9)
    need(sp.gcd(a, m) == 1 and sp.gcd(c, n) == 1)
    return combine(over(str(a), tx(m * x ** 3 * y ** i)), op(r, 0.4), over(str(c), tx(n * x ** j * y ** 3)))

def t8_product_and_power(r):                  # 5/(x y) + 7/(2x^2)
    x, y = (sp.Symbol(s) for s in gen.letters(r, 2))
    k = r.randint(2, 5)
    a, c = r.randint(2, 9), r.randint(2, 9)
    need(sp.gcd(c, k) == 1)
    return combine(over(str(a), tx(x * y)), op(r, 0.6), over(str(c), tx(k * x ** 2)))

def t8_numbers_and_letters(r):                # 3/(4 x y^2) + 5/(6 x^2 y)
    x, y = (sp.Symbol(s) for s in gen.letters(r, 2))
    m, n = r.choice(((4, 6), (6, 4), (2, 3), (3, 2), (6, 9), (4, 10)))
    a, c = r.randint(1, 9), r.randint(1, 9)
    need(sp.gcd(a, m) == 1 and sp.gcd(c, n) == 1)
    return combine(over(str(a), tx(m * x * y ** 2)), op(r, 0.5), over(str(c), tx(n * x ** 2 * y)))

# ------------------------------------------------------------------
# Type 9 (25, 28, 29): a whole term and a fraction
# ------------------------------------------------------------------
def t9_monomial_plus(r):                      # 2x + x/y
    x, y = (sp.Symbol(s) for s in gen.letters(r, 2))
    if r.random() < 0.5:
        x, y = y, x
    k, c = r.randint(2, 6), r.randint(1, 5)
    return combine(tx(k * x), op(r, 0.6), over(tx(c * x), tx(y)))

def t9_fraction_plus_number(r):               # 5/x + 8
    x = letter(r)
    k = r.choice((1, 1, 1, 2, 3))
    a, n = r.randint(1, 9), r.randint(2, 9)
    need(sp.gcd(a, k) == 1)
    return combine(over(str(a), tx(k * x)), op(r, 0.6), str(n))

def t9_number_minus_binomial(r):              # 7 - 4/(x - 9)
    x = letter(r)
    n, a, p = r.randint(2, 9), r.randint(1, 9), gen.signed(r, 1, 9)
    return combine(str(n), op(r, 0.4), over(str(a), x + p))

# ------------------------------------------------------------------
# Type 10 (30-32): (x + a)/(x - b) - N/((x - b)(x + c)) = 1/(x + c)
# ------------------------------------------------------------------
def t10_reduces(r):
    x = letter(r)
    b, c = ints(r, 1, 7, 2)
    a = gen.signed_except(r, 1, 9, b)
    N = sp.expand((x + a) * (x + c) - (x + b))
    need(N.coeff(x, 1) != 0 and N.coeff(x, 0) != 0)
    need(sp.gcd(N, (x + b) * (x + c)) == 1)   # the second fraction doesn't reduce first
    return combine(over(x + a, x + b), " - ", over(N, (x + b) * (x + c)))

def t10_coefficient(r):                       # (2x + a)/(x - b) - N/(...) = 1/(x + c)
    x = letter(r)
    b, c = ints(r, 1, 6, 2)
    a = gen.signed(r, 1, 7)
    N = sp.expand((2 * x + a) * (x + c) - (x + b))
    need(N.coeff(x, 1) != 0 and N.coeff(x, 0) != 0 and sp.gcd(N, (x + b) * (x + c)) == 1)
    need(sp.gcd(2 * x + a, x + b) == 1)
    return combine(over(2 * x + a, x + b), " - ", over(N, (x + b) * (x + c)))

def t10_square(r):                            # the trinomial is a difference of squares
    x = letter(r)
    b = gen.signed(r, 1, 8)
    c = -b
    a = gen.signed_except(r, 1, 9, b, c)
    N = sp.expand((x + a) * (x + c) - (x + b))
    need(N.coeff(x, 1) != 0 and N.coeff(x, 0) != 0 and sp.gcd(N, (x + b) * (x + c)) == 1)
    return combine(over(x + a, x + b), " - ", over(N, (x + b) * (x + c)))

# ------------------------------------------------------------------
# Type 11 (33-40): two quadratics sharing a factor, the second x^2 - s^2
# ------------------------------------------------------------------
def t11_parts(r):
    x = letter(r)
    s = r.randint(1, 6)
    shared = r.choice((s, -s))
    other = gen.signed_except(r, 1, 7, s, -s)
    return x, shared, other, sp.expand((x + shared) * (x + other)), x ** 2 - s ** 2

def t11_sum(r, minus=False):                  # (x - 4)/(x^2 + 5x + 6) + (x - 1)/(x^2 - 4)
    x, sh, ot, Q1, Q2 = t11_parts(r)
    a, b = gen.signed(r, 1, 6), gen.signed(r, 1, 6)
    return combine(over(x + a, Q1), " - " if minus else " + ", over(x + b, Q2))

def t11_add(r):
    return t11_sum(r)

def t11_subtract(r):
    return t11_sum(r, minus=True)

def t11_negative_first(r):                    # -(x - 2)/(x^2 - 2x - 8) - (x - 1)/(x^2 - 4)
    x, sh, ot, Q1, Q2 = t11_parts(r)
    a, b = gen.signed(r, 1, 6), gen.signed(r, 1, 6)
    return combine("-", over(x + a, Q1), op(r, 0.4), over(x + b, Q2))

def t11_coefficient(r):                       # (3x - 1)/(x^2 + 2x - 3) - (x + 4)/(x^2 - 9)
    x, sh, ot, Q1, Q2 = t11_parts(r)
    k = r.randint(2, 3)
    a, b = gen.signed(r, 1, 6), gen.signed(r, 1, 6)
    return combine(over(k * x + a, Q1), op(r, 0.4), over(x + b, Q2))

def t11_perfect_square(r):                    # (x + 1)/(x^2 + 6x + 9) + (x - 4)/(x^2 - 9)
    x = letter(r)
    s = r.randint(1, 6)
    sh = r.choice((s, -s))
    a, b = gen.signed(r, 1, 6), gen.signed(r, 1, 6)
    return combine(over(x + a, sp.expand((x + sh) ** 2)), op(r), over(x + b, x ** 2 - s ** 2))

# ------------------------------------------------------------------
# Type 12 (41-42): c/((x - m)(x - n)) + (-c)/(x^2 - s^2), four factors
# ------------------------------------------------------------------
def t12_parts(r):
    x = letter(r)
    m, n = r.sample(range(1, 7), 2)
    s = r.choice([k for k in range(1, 5) if k not in (m, n)])
    c = r.randint(2, 4)
    need(c * (m * n + s * s) <= 60)           # c ((m + n) x - m n - s^2) on top
    return x, sp.expand((x - m) * (x - n)), x ** 2 - s ** 2, c

def t12_plus_negative(r):                     # 2/(x^2 - 5x + 4) + (-2)/(x^2 - 4)
    x, Q1, Q2, c = t12_parts(r)
    return combine(over(str(c), Q1), " + ", f"(-{c})/({P(Q2)})")

def t12_minus(r):                             # 3/(x^2 - 7x + 6) - 3/(x^2 - 9)
    x, Q1, Q2, c = t12_parts(r)
    return combine(over(str(c), Q1), " - ", over(str(c), Q2))

def t12_squares_first(r):                     # 2/(x^2 - 9) + (-2)/(x^2 - 3x + 2)
    x, Q1, Q2, c = t12_parts(r)
    return combine(over(str(c), Q2), " + ", f"(-{c})/({P(Q1)})")

# ------------------------------------------------------------------
# Type 13 (43-44): n + x/(x + a) - c/(x^2 - a^2)
# ------------------------------------------------------------------
def t13_parts(r):
    x = letter(r)
    a = r.randint(1, 6)
    return x, r.choice((a, -a)), x ** 2 - a ** 2

def t13_standard(r):                          # 3 + x/(x + 2) - 2/(x^2 - 4)
    x, p, Q = t13_parts(r)
    n, c = r.randint(2, 5), r.randint(1, 9)
    return combine(str(n), " + ", over(tx(x), x + p), " - ", over(str(c), Q))

def t13_plus(r):                              # 2 - x/(x - 3) + 4/(x^2 - 9)
    x, p, Q = t13_parts(r)
    n, c = r.randint(2, 5), r.randint(1, 9)
    return combine(str(n), " - ", over(tx(x), x + p), " + ", over(str(c), Q))

def t13_coefficient(r):                       # 4 + (2x)/(x + 1) - 3/(x^2 - 1)
    x, p, Q = t13_parts(r)
    n, k, c = r.randint(2, 5), r.randint(2, 3), r.randint(1, 9)
    return combine(str(n), " + ", over(tx(k * x), x + p), op(r, 0.4), over(str(c), Q))

# ------------------------------------------------------------------
# Type 14 (45-46): a/(x + p) - x/(x + q) + (x^2 + c)/((x + p)(x + q))
# ------------------------------------------------------------------
def t14_to_zero(r):                           # 1/(x + 1) - x/(x - 2) + (x^2 + 2)/(x^2 - x - 2) = 0
    x = letter(r)
    a = r.randint(1, 5)
    p = a
    q = gen.signed_except(r, 1, 6, p, -p)
    c = -a * q
    return combine(over(str(a), x + p), " - ", over(tx(x), x + q), " + ", over(x ** 2 + c, (x + p) * (x + q)))

def t14_to_monomial(r):                       # 2/(x + 3) - x/(x - 1) + (x^2 + 2)/(x^2 + 2x - 3) = -x/(...)
    x = letter(r)
    a = r.randint(1, 5)
    p = a + r.choice([k for k in range(-3, 4) if k])
    q = gen.signed_except(r, 1, 6, p, -p)
    need(p != 0)
    c = -a * q
    need(c != 0)
    return combine(over(str(a), x + p), " - ", over(tx(x), x + q), " + ", over(x ** 2 + c, (x + p) * (x + q)))

def t14_to_number(r):                         # the x terms cancel instead: a number over the LCD
    x = letter(r)
    a = r.randint(1, 5)
    p = a
    q = gen.signed_except(r, 1, 6, p, -p)
    c = -a * q + gen.signed(r, 1, 6)
    need(c != 0)
    return combine(over(str(a), x + p), " - ", over(tx(x), x + q), " + ", over(x ** 2 + c, (x + p) * (x + q)))

# ------------------------------------------------------------------
# Type 15 (47-48): opposite denominators
# ------------------------------------------------------------------
def t15_parts(r):
    x = letter(r)
    k = r.choice((1, 2))
    b = r.choice([n for n in range(1, 6) if sp.gcd(n, k) == 1])
    return x, k, b, sp.expand((k * x) ** 2 - b ** 2)

def t15_square_first(r):                      # 4x/(x^2 - 1) + 3x/(1 - x) - 4/(x - 1)
    x, k, b, Q = t15_parts(r)
    opp = const_first(b, -k, x)
    third = k * x - b
    m, n, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    return combine(over(tx(m * x), Q), " + ", over(tx(n * x), opp), " - ", over(str(c), third))

def t15_opposite_first(r):                    # 5x/(1 - 2x) - 2x/(2x + 1) + 3/(4x^2 - 1)
    x, k, b, Q = t15_parts(r)
    opp = const_first(b, -k, x)
    m, n, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    return combine(over(tx(m * x), opp), " - ", over(tx(n * x), k * x + b), " + ", over(str(c), Q))

def t15_number_tops(r):                       # 3/(x^2 - 4) - 2/(2 - x) + 1/(x + 2)
    x, k, b, Q = t15_parts(r)
    opp = const_first(b, -k, x)
    m, n, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    return combine(over(str(m), Q), " - ", over(tx(n * x), opp), op(r), over(str(c), k * x + b))

# ------------------------------------------------------------------
# Type 16 (49-50): three trinomials in a chain, numerators k, -2k, k
# ------------------------------------------------------------------
def t16_chain(r):                             # 1/(x^2 + 5x + 6) - 2/(x^2 + 3x + 2) + 1/(x^2 - 3x - 4)
    x = letter(r)
    a, b, c, d = ints(r, 1, 5, 4)
    need(b + c != a + d)                      # else the x terms cancel too, leaving a number
    k = r.choice((1, 1, 2, 3))
    need(k * abs(c * d - 2 * a * d + a * b) <= 60 and k * abs(b + c - a - d) <= 60)
    Q1, Q2, Q3 = (sp.expand((x + u) * (x + v)) for u, v in ((a, b), (b, c), (c, d)))
    return combine(over(str(k), Q1), " - ", over(str(2 * k), Q2), " + ", over(str(k), Q3))

def t16_chain_squares(r):                     # the middle one a difference of squares
    x = letter(r)
    s = r.randint(1, 5)
    b, c = r.choice(((s, -s), (-s, s)))
    a, d = ints(r, 1, 6, 2, s, -s)
    need(b + c != a + d)                      # else the x terms cancel too, leaving a number
    k = r.choice((1, 1, 2, 3))
    need(k * abs(c * d - 2 * a * d + a * b) <= 60 and k * abs(b + c - a - d) <= 60)
    Q1, Q2, Q3 = (sp.expand((x + u) * (x + v)) for u, v in ((a, b), (b, c), (c, d)))
    return combine(over(str(k), Q1), " - ", over(str(2 * k), Q2), " + ", over(str(k), Q3))

def t16_reversed(r):                          # k/... + k/... - 2k/...: the -2k last
    x = letter(r)
    a, b, c, d = ints(r, 1, 5, 4)
    need(b + c != a + d)                      # else the x terms cancel too, leaving a number
    k = r.choice((1, 1, 2, 3))
    need(k * abs(c * d - 2 * a * d + a * b) <= 60 and k * abs(b + c - a - d) <= 60)
    Q1, Q2, Q3 = (sp.expand((x + u) * (x + v)) for u, v in ((a, b), (b, c), (c, d)))
    return combine(over(str(k), Q1), " + ", over(str(k), Q3), " - ", over(str(2 * k), Q2))

TEMPLATES = {
    "1": [t1_two_binomials, t1_monomial],
    "2": [t2_number_and_binomial, t2_to_a_number, t2_subtract_to_a_number],
    "3": [t3_subtract, t3_negative_constant],
    "4": [t4_add, t4_add, t4_subtract],
    "5": [t5_difference, t5_sum_written_backward, t5_negative_leads, t5_quadratic_tops],
    "6": [t6_x_and_kx2, t6_kx_and_x, t6_x2_and_kx],
    "7": [t7_shared_number, t7_coprime_powers, t7_binomial_powers],
    "8": [t8_powers, t8_product_and_power, t8_numbers_and_letters],
    "9": [t9_monomial_plus, t9_fraction_plus_number, t9_number_minus_binomial],
    "10": [t10_reduces, t10_coefficient, t10_square],
    "11": [t11_add, t11_subtract, t11_negative_first, t11_coefficient, t11_perfect_square],
    "12": [t12_plus_negative, t12_minus, t12_squares_first],
    "13": [t13_standard, t13_plus, t13_coefficient],
    "14": [t14_to_zero, t14_to_monomial, t14_to_number],
    "15": [t15_square_first, t15_opposite_first, t15_number_tops],
    "16": [t16_chain, t16_chain_squares, t16_reversed],
}

# ------------------------------------------------------------------
# What each type's answer must look like, so a draw stays in its type
# ------------------------------------------------------------------
def shape(entry, tpl, n, d, dens, xs):
    """Redraw unless the sum n/d (of fractions over dens, in the letters xs) is what its type makes."""
    e = n / d
    deg = lambda f: sp.Poly(f, *xs).total_degree()
    terms = lambda f: len(sp.Add.make_args(sp.expand(f)))
    factors = [f for f, m in sp.factor_list(d)[1] if not f.is_Symbol for _ in range(m)]   # not monomials
    if n != 0:
        need(max(abs(c) for c in sp.Poly(n, *xs).coeffs()) <= 60)
    if entry == "1":
        need(d.is_Integer and d != 1 and deg(n) == 1 and terms(n) == 2)
    elif entry == "2":
        if tpl == 0:
            need(deg(n) == 1 and terms(n) == 2 and deg(d) == 1 and not factors)
        else:
            need(e.is_Rational and not e.is_Integer)
    elif entry == "3":
        need(deg(d) == 1 and deg(n) == 1 and terms(n) == 2)
    elif entry == "4":
        need(n.is_Integer and n > 1 and deg(d) == 1 and d.is_Add)
    elif entry in ("5", "10"):
        need(n == 1 and deg(d) == 1)
    elif entry in ("6", "7", "8"):
        need(not factors and (n.is_Add or entry == "6") and len(xs) == (2 if entry == "8" else 1))
        one_is_lcd = any(sp.expand(d - b) == 0 for b in dens)
        need(one_is_lcd if entry == "6" else not one_is_lcd)
    elif entry == "9":
        need(n.is_Add and d.is_Add == (tpl == 2))
    elif entry == "11":
        need(len(factors) == 3 and deg(n) in (1, 2))
    elif entry == "12":
        need(len(factors) == 4 and deg(n) == 1)
    elif entry == "13":
        need(len(factors) == 2 and deg(n) == 2)
    elif entry == "14":
        need(e == 0 if tpl == 0 else (len(factors) == 2 and n != 0 and (n.is_Integer if tpl == 2 else n.is_Mul or n.is_Symbol)))
    elif entry == "15":
        need(len(factors) == 2 and deg(n) in (1, 2))
    elif entry == "16":
        need(len(factors) == 4 and n != 0 and deg(n) <= 1)

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    e, fractions, order, letters = read(prompt)
    for top, bottom in fractions:             # no fraction in the prompt reduces by a factor with a letter
        need(sp.gcd(top, bottom).is_Number)
    n, d = combined(e)
    shape(entry, tpl, n, d, [d for _, d in fractions], [sp.Symbol(v) for v in letters])
    return dict(prompt=prompt, answer=written(n, d, order, letters))

def same(a, b, trials=5):
    """Typst expressions a and b have the same value, exactly, at random
    rational points (a point where either is undefined is skipped)."""
    ea, eb = to_sympy(a), to_sympy(b)
    xs = sorted(ea.free_symbols | eb.free_symbols, key=str)
    rng = random.Random(f"{a}|{b}")           # not the drawing generator
    tried = 0
    for _ in range(4 * trials):
        at = {x: sp.Rational(rng.randint(-97, 97), rng.randint(2, 13)) for x in xs}
        va, vb = ea.xreplace(at), eb.xreplace(at)
        if va.has(sp.zoo, sp.nan) or vb.has(sp.zoo, sp.nan):
            continue
        if va != vb:
            return False
        tried += 1
        if tried == trials:
            return True
    return False

def check(p):
    try:
        a = p["answer"]
        ok = same(p["prompt"], a) and (a == "0" or key_form(a))
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "(x - 4)/(x^2 + 5 x + 6) + (x - 1)/(x^2 - 4)", "(2 x^2 - 4 x + 5)/((x + 2) (x + 3) (x - 2))")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
