"""Special products with letter exponents (Advanced Math), from the old app's
set AdvMath_05_17 (simplify by the difference of two squares) and the
2025-26 midterm (factor a difference of squares, a sum or difference of
cubes, and a greatest common factor with letter exponents).

The key writes terms in the order the problem does, and exponents with a
coefficient of 1 as the letter alone: y^m, not y^(1 m) (the old set printed
^{1 m}). Type 2 factors completely: x^(4 n) - y^(4 m) is three factors.

Problems are built from their answers. check() doesn't use that: it
compares the prompt's value with the answer's at random points (letters in
the exponents too), and reads from the answer's text that it is finished:
Type 1 has no fraction left; in Types 2 and 3 no factor is a difference of
two squares, and in Type 3 sympy can't split any factor further when the
exponents are numbers; in Type 4 the factor left in parentheses has no
common factor.

A problem: dict(type, prompt, answer, source), both in Typst math.
    prompt  "3 y^(2 n + 1) + 12 y^(3 n + 2)"
    answer  "3 y^(2 n + 1) (1 + 4 y^(n + 1))"
"""
import math
import sympy as sp
from .. import gen
from ..gen import need, signed
from ..check import to_sympy, same_value, simplest_form
from ..typmath import tx, single, fr

NAME = FAMILY = "adv_factoring"
FIXED = False
TITLE = "Special Products with Letter Exponents"
INSTRUCTIONS = "Factor completely."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Simplify by the Difference of Two Squares", instructions="Simplify.",
         look="A fraction whose top is a difference of two squares, like y^(4 m) - x^(2 n), and whose "
              "bottom is the sum or the difference of their square roots.",
         move="Factor the top: A^2 - B^2 = (A + B)(A - B). Cancel the factor that matches the bottom."),
    dict(key="2", title="A Difference of Two Squares",
         look="Two squares subtracted; the exponents are even multiples of a letter.",
         move="A^2 - B^2 = (A + B)(A - B), with A and B the square roots: the square root of x^(6 n) "
              "is x^(3 n). If a factor is still a difference of squares, factor it again."),
    dict(key="3", title="A Sum or Difference of Cubes",
         look="Two cubes added or subtracted: the numbers are cubes and the exponents multiples of 3.",
         move="A^3 + B^3 = (A + B)(A^2 - A B + B^2) and A^3 - B^3 = (A - B)(A^2 + A B + B^2). "
              "Find A and B by taking cube roots.", space="1.25in"),
    dict(key="4", title="A Greatest Common Factor with Letter Exponents",
         look="Terms with the same letter, its exponents written with another letter, like y^(2 n + 1).",
         move="Take out the largest number that divides every coefficient and each letter to its smallest "
              "power. Subtract exponents to find what is left: y^(3 n + 2) ÷ y^(2 n + 1) = y^(n + 1)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing: monomials as written, k x^e y^f, exponents numbers or letter terms
# ------------------------------------------------------------------
def pw(base, e):
    if e == 0:
        return ""
    if e == 1:
        return base
    t = tx(e)
    return f"{base}^{t}" if t.isalnum() else f"{base}^({t})"

def mono(k, *powers):
    """mono(9, ("x", 2 * n)) = "9 x^(2 n)"; k may be 1."""
    body = [s for s in (pw(b, e) for b, e in powers) if s]
    if k != 1 or not body:
        body.insert(0, str(k))
    return " ".join(body)

def joined(*terms):
    """Signed terms (sign, text) as a sum: joined((1, "a"), (-1, "b")) = "a - b"."""
    out = ""
    for i, (s, t) in enumerate(terms):
        out += (("-" if s < 0 else "") + t) if i == 0 else ((" - " if s < 0 else " + ") + t)
    return out

def square_part(r, lo=1, hi=6):
    """A monomial A for a difference of squares: (coefficient k, exponent coefficient a)."""
    return r.randint(lo, hi), r.randint(1, 6)

# ------------------------------------------------------------------
# Type 1 (AdvMath_05_17): (A^2 - B^2)/(A ± B)
# ------------------------------------------------------------------
def t1(r, coefficients, sign):
    y, x, m, n = r.sample(gen.LETTERS, 4)
    k, j = (r.randint(2, 5), r.randint(2, 5)) if coefficients else (1, 1)
    need(math.gcd(k, j) == 1)                  # else a common number comes out first
    a, b = r.randint(1, 6), r.randint(1, 6)
    A, B = (k, ((y, a * sp.Symbol(m)),)), (j, ((x, b * sp.Symbol(n)),))
    sq = lambda M: mono(M[0] ** 2, *[(v, 2 * e) for v, e in M[1]])
    one = lambda M: mono(M[0], *M[1])
    prompt = fr(joined((1, sq(A)), (-1, sq(B))), joined((1, one(A)), (sign, one(B))))
    return prompt, joined((1, one(A)), (-sign, one(B)))

def t1_over_sum(r):
    return t1(r, False, 1)

def t1_over_difference(r):
    return t1(r, False, -1)

def t1_with_numbers(r):
    return t1(r, True, r.choice((-1, 1)))

# ------------------------------------------------------------------
# Type 2 (the midterm): A^2 - B^2, factored completely
# ------------------------------------------------------------------
def complete(A, B):
    """The factors of A^2 - B^2, where A = (k, a) means k v^(a m): sums first."""
    (k, a), (j, b) = A, B
    if k ** 0.5 % 1 == 0 and j ** 0.5 % 1 == 0 and a % 2 == 0 and b % 2 == 0:
        return [(1, A, B)] + complete((math.isqrt(k), a // 2), (math.isqrt(j), b // 2))
    return [(1, A, B), (-1, A, B)]

def t2(r, A, B, number=False):
    need(math.gcd(A[0], B[0]) == 1)            # else a common number comes out first
    x, y, m, n = r.sample(gen.LETTERS, 4)
    M, N = sp.Symbol(m), sp.Symbol(n)
    def term(P, v, L, power=1):
        k, a = P
        return mono(k ** power, (v, a * power * L)) if not (number and v == y) else str(k ** power)
    prompt = joined((1, term(A, x, M, 2)), (-1, term(B, y, N, 2)))
    factors = complete(A, B)
    answer = " ".join(f"({joined((1, term(P, x, M)), (s, term(Q, y, N)))})" for s, P, Q in factors)
    return prompt, answer

def t2_letters(r):                            # the midterm: x^(2 k b) - y^(2 j c)
    return t2(r, (1, r.randint(1, 6)), (1, r.randint(1, 6)))

def t2_numbers(r):
    return t2(r, square_part(r, 1, 7), square_part(r, 2, 7))

def t2_fourth_powers(r):                      # x^(4 n) - 16, three factors
    return t2(r, (r.choice((1, 4)), 2 * r.randint(1, 3)), (r.choice((4, 9)), 2), number=True)

# ------------------------------------------------------------------
# Type 3 (the midterm): A^3 ± B^3
# ------------------------------------------------------------------
def cubes(A, B, s):
    """(A ± B)(A^2 ∓ A B + B^2) for sympy monomials A, B; A B keeps A's letters first."""
    order = sorted(A.free_symbols, key=str) + sorted(B.free_symbols, key=str)
    return (f"({joined((1, tx(A)), (s, tx(B)))}) "
            f"({joined((1, tx(A ** 2)), (-s, tx(A * B, order)), (1, tx(B ** 2)))})")

def t3_three_letters(r):                      # the midterm: a^3 q^(3i) r^(3j) - b^3 s^(3k)
    q, rr, s = (sp.Symbol(v) for v in gen.letters(r, 3))
    a, b = r.randint(1, 6), r.randint(1, 6)
    need(math.gcd(a, b) == 1)
    A, B = a * q ** r.randint(1, 4) * rr ** r.randint(1, 4), b * s ** r.randint(1, 4)
    sign = r.choice((-1, 1))
    return joined((1, tx(A ** 3)), (sign, tx(B ** 3))), cubes(A, B, sign)

def t3_number(r):
    x = sp.Symbol(gen.letters(r, 1)[0])
    a, b = r.randint(1, 5), r.randint(1, 6)
    need(math.gcd(a, b) == 1)
    A, B, sign = a * x ** r.randint(1, 3), sp.Integer(b), r.choice((-1, 1))
    return joined((1, tx(A ** 3)), (sign, tx(B ** 3))), cubes(A, B, sign)

def t3_letter_exponents(r):
    x, y, m, n = (sp.Symbol(v) for v in r.sample(gen.LETTERS, 4))
    a, b = r.randint(1, 4), r.randint(1, 4)
    need(math.gcd(a, b) == 1)
    A, B, sign = a * x ** m, b * y ** n, r.choice((-1, 1))       # A B is never a square, so A^2 ± A B + B^2 is finished
    return joined((1, tx(A ** 3)), (sign, tx(B ** 3))), cubes(A, B, sign)

# ------------------------------------------------------------------
# Type 4 (the midterm, no. 31: 3 y^(2 n + 1) + 12 y^(3 n + 2))
# ------------------------------------------------------------------
def gcf(r, letters, terms):
    """A greatest common factor g v^E for each letter, and terms c_i v^(E + d_i): some d_i = 0 for each letter."""
    n = sp.Symbol(r.choice([v for v in gen.LETTERS if v not in letters]))
    g = r.randint(2, 6)
    E = {v: r.randint(1, 3) * n + r.randint(0, 4) for v in letters}
    while True:
        cs = [signed(r, 1, 6) if i else r.randint(1, 6) for i in range(terms)]
        if math.gcd(*cs) == 1:
            break
    ds = [{v: r.randint(0, 2) * n + r.randint(0, 3) for v in letters} for _ in range(terms)]
    for v in letters:                           # the smallest power of each letter is the common one
        ds[r.randrange(terms)][v] = 0
    need(all(any(d[v] != 0 for d in ds) for v in letters) and len({tuple(d.values()) for d in ds}) == terms)
    prompt = joined(*[(1 if c > 0 else -1, mono(abs(c) * g, *[(v, E[v] + d[v]) for v in letters]))
                      for c, d in zip(cs, ds)])
    inner = joined(*[(1 if c > 0 else -1, mono(abs(c), *[(v, d[v]) for v in letters])) for c, d in zip(cs, ds)])
    return prompt, f"{mono(g, *[(v, E[v]) for v in letters])} ({inner})"

def t4_two_terms(r):
    return gcf(r, gen.letters(r, 1), 2)

def t4_three_terms(r):
    return gcf(r, gen.letters(r, 1), 3)

def t4_two_letters(r):
    return gcf(r, gen.letters(r, 2), 2)

TEMPLATES = {
    "1": [t1_over_sum, t1_over_difference, t1_with_numbers],
    "2": [t2_letters, t2_numbers, t2_fourth_powers],
    "3": [t3_three_letters, t3_number, t3_letter_exponents],
    "4": [t4_two_terms, t4_three_terms, t4_two_letters],
}

def draw(entry, r, tpl):
    prompt, answer = TEMPLATES[entry][tpl](r)
    need(finished(entry, answer))             # x^12 + 27 y^6: its trinomial factors again
    return dict(prompt=prompt, answer=answer)

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def factors(answer):
    """The factors of an answer, as written."""
    t = to_sympy(answer, evaluate=False)
    return [_ev(a) for a in (t.args if isinstance(t, sp.Mul) else [t])]

def _ev(e):
    return e.func(*[_ev(a) for a in e.args]) if e.args else e

def is_square(term):
    """k v^e ... with k a perfect square and every exponent an even multiple."""
    c, rest = term.as_coeff_Mul()
    if c < 0 or not (c.is_Integer and math.isqrt(int(c)) ** 2 == c):
        return False
    for f in (sp.Mul.make_args(rest) if rest != 1 else ()):
        e = f.exp if f.is_Pow else sp.Integer(1)
        if e.as_coeff_Mul()[0] % 2:
            return False
    return True

def difference_of_squares(f):
    ts = sp.Add.make_args(f)
    return len(ts) == 2 and ts[0].could_extract_minus_sign() != ts[1].could_extract_minus_sign() and \
        all(is_square(-t if t.could_extract_minus_sign() else t) for t in ts)

def numeric_exponents(e):
    return all(t.exp.is_number for t in sp.preorder_traversal(e) if t.is_Pow)

def content(f):
    """The greatest common factor of a sum's coefficients."""
    return math.gcd(*[int(t.as_coeff_Mul()[0]) for t in sp.Add.make_args(f)])

def finished(typ, answer):
    if typ == "1":
        return "/" not in answer and content(to_sympy(answer)) == 1
    fs = factors(answer)
    adds = [f for f in fs if f.is_Add]
    if any(content(f) != 1 for f in adds):
        return False
    if typ in ("2", "3"):
        if any(difference_of_squares(f) for f in adds) or len(adds) < 2:
            return False
        e = to_sympy(answer)
        if typ == "3" and numeric_exponents(e):
            _, parts = sp.factor_list(e)
            return sum(m for _, m in parts) == len(adds)
        return True
    if len(adds) != 1:                                  # Type 4: one factor left in parentheses,
        return False
    inner = adds[0]
    cs = [t.as_coeff_Mul()[0] for t in sp.Add.make_args(inner)]
    letters = {b for t in sp.Add.make_args(inner) for b in t.free_symbols if any(
        p.is_Pow and p.base == b for p in sp.Mul.make_args(t)) or b in sp.Mul.make_args(t)}
    return math.gcd(*[int(c) for c in cs]) == 1 and all(       # with no number and no letter common to its terms
        any(not t.has(v) for t in sp.Add.make_args(inner)) for v in letters)

def check(p):
    try:
        ok = same_value(p["prompt"], p["answer"]) and simplest_form(p["answer"]) and finished(p["type"], p["answer"])
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing: an edited prompt is solved again only when its
# exponents are numbers (sympy can't factor with letters in exponents)
# ------------------------------------------------------------------
def answer_of(prompt):
    e = to_sympy(prompt)
    if not numeric_exponents(e):
        raise ValueError("letters in the exponents")
    return single(sp.cancel(e)) if sp.fraction(sp.together(e))[1] != 1 else " ".join(
        f"({tx(f)})" if f.is_Add else tx(f) for f in sp.Mul.make_args(sp.factor(e)))

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "3 y^(2 n + 1) + 12 y^(3 n + 2)", "3 y^(2 n + 1) (1 + 4 y^(n + 1))")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
