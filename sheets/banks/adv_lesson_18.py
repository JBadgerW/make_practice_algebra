"""Lesson 18 (Advanced Math): advanced word problems. From the Saxon lesson
and its deck (~/Documents/adv_math/problem_sets/ps_018/slides/deck_018.typ):
examples 18.1-18.7 and Problem Set 18, problems 1-3 and 5-7.

    1  three colors, three statements:  The number of blues was 4 less than the sum of the whites and the
                                        greens. Also, ... twice as many blues as whites?
                                                                    4 blues, 2 whites, 6 greens
    2  three coins:                     The quarters, nickels, and dimes totaled 20, and their value was
                                        $1.90. ... 4 times as many nickels as quarters?
                                                                    2 quarters, 8 nickels, 10 dimes
    3  direct and inverse variation:    Reds varied directly as blues squared and inversely as greens. ...
                                                                    64 reds
    4  digits reversed:                 The sum of the digits of a two-digit counting number is 5. ...
                                                                    23
    5  mixture, both amounts:           To get 1000 gallons (gal) of a mixture that was 56% alcohol, ...
                                                                    400 gal of 20% alcohol, 600 gal of 80% alcohol
    6  mixture, the amount to add:      How many liters of a 64% glycol solution must be added to 77 liters
                                        of a 23% glycol solution to get a 42% glycol solution?
                                                                    66.5 liters
    7  a compound's total weight:       The weight of the carbon (C) in the container of C3H7Cl was 113
                                        grams. ...                  244.83 grams

The types file's mixture heading (18.5, 18.6, problem 6) is split by its
move: Type 5 has a total and two unknowns (two equations); Type 6 adds an
unknown amount to a known one (one equation). Problem 4 of the set is a line
problem (Lesson 10), not a word problem, so it is not a source here.

Every story is the book's wording; a type's templates are its sources' two
wordings where they differ (18.1 past tense with "Also,", problem 1 present;
18.4 "the number", problem 5 "the new number"; 18.6 "How many liters of ...
must be", problem 6 "How much of ... should be").

The key (the deck's values; the words chosen here, since the deck writes
N_B = 4 and the like):
  1  each color's count, in the order the story first names the colors:
     "4 blues, 2 whites, 6 greens" (18.1), "2 blues, 3 whites, 6 greens"
     (problem 1); "1 blue" when one.
  2  the coins in the order the story lists them: "2 quarters, 8 nickels,
     10 dimes" (18.2, as the deck), "3 quarters, 8 nickels, 9 dimes" (problem 2).
  3  the count asked for, with its color: "64 reds" (18.3), "10 reds" (problem 3).
  4  the original number: "23" (18.4), "49" (problem 5).
  5  both amounts, the weaker first, with the story's unit abbreviation:
     "400 gal of 20% alcohol, 600 gal of 80% alcohol" (18.5).
  6  the amount, with the given amount's unit: "66.5 liters" (18.6),
     "106.8 ounces" (problem 6).
  7  the total weight in grams: "244.83 grams" (18.7), "891.43 grams" (problem 7).
Types 6 and 7 round to two places, half up, and drop trailing zeros
("66.5", "120"), as the deck writes 244.83 and 66.5. Every other answer is a
whole number: Types 1-5 are built backward from whole answers.

check() reads the numbers back out of the story's words and puts the
answer into the lesson's equations, independently of how it was drawn:
  1  N_X + d = N_Y + N_Z (or N_X = ... + d), N_Z = N_X + N_Y + e, N_P = k N_Q:
     solved exactly; the answer's counts and colors must match.
  2  N_1 + N_2 + N_3 = n, the value in cents, N_A = k N_B: solved exactly.
  3  R = k B^p / G^q: k from the first situation, then R; must be the answer.
  4  every two-digit number is tried; exactly one fits, and it is the answer.
  5  L + H = T and (lp) L + (hp) H = (tp) T, solved exactly.
  6  (bp) A + (ap) x = (tp)(A + x), solved exactly, then rounded.
  7  the formula is read from the prompt and weighed with the given atomic
     weights; total = given weight times total over the element's part.

No skipped sources: Lesson 18 has no proofs.

A problem: dict(type, story, prompt, answer, source); prompt and answer are
words (story names the template the words were written from):
    story   "past"
    prompt  "The number of blues was 4 less than the sum of the whites and the greens. Also, the number of
             greens equaled the sum of the blues and the whites. How many of each were there if there
             were twice as many blues as whites?"
    answer  "4 blues, 2 whites, 6 greens"
"""
import math, re
from fractions import Fraction as F
from .. import gen
from ..gen import need
from ..typst import esc
from .adv_lesson_25 import rounded

NAME = FAMILY = "adv_lesson_18"
FIXED = False
TITLE = "Lesson 18: Advanced Word Problems"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="Three-Variable Color Problems",
         look="Three colors, two statements about sums, and one \"times as many\".",
         move="Use $N_B$, $N_W$, $N_G$. Write one equation per statement: \"4 less than\" means add 4 to the "
              "smaller side, $N_B + 4 = N_W + N_G$. Substitute the \"times as many\" equation, $N_B = 2 N_W$, "
              "into the other two and solve the system.",
         space="2in"),
    dict(key="2", title="Three-Coin Problems",
         look="Quarters, nickels, and dimes: how many in all, their value, and a \"times as many\".",
         move="Write $N_Q + N_N + N_D = 20$ and the value in cents, $25 N_Q + 5 N_N + 10 N_D = 190$. Substitute "
              "the \"times as many\" equation into both, then eliminate one variable.",
         space="2in"),
    dict(key="3", title="Direct and Inverse Variation",
         look="\"... varied directly as ... and inversely as ...\", with two situations.",
         move="Write the equation, like $R = (k B^2)/G$. Put in the first situation to find $k$, then put $k$ "
              "and the second situation in to find $R$."),
    dict(key="4", title="Digit Problems",
         look="A two-digit number, the sum of its digits, and the number with its digits reversed.",
         move="Use $U$ for the units digit and $T$ for the tens digit. The number is $10 T + U$, reversed it is "
              "$10 U + T$. Write $U + T = \"sum\"$ and the reversed equation, and solve the system."),
    dict(key="5", title="Mixtures: Both Amounts from the Total",
         look="Two solutions of different strengths mixed to make a given total.",
         move="Write the total, $P_N + D_N = 1000$, and the ingredient, $0.2 P_N + 0.8 D_N = 0.56(1000)$. "
              "Substitute $1000 - D_N$ for $P_N$ and solve."),
    dict(key="6", title="Mixtures: The Amount to Add",
         look="An unknown amount of one solution added to a known amount of another.",
         move="Make the statement about the ingredient: $\"before\" + \"added\" = \"final\"$, "
              "$0.23(77) + 0.64 P_N = 0.42(77 + P_N)$. Solve for $P_N$."),
    dict(key="7", title="Chemical Compound Weights",
         look="The weight of one element in a compound; the total weight is asked for.",
         move="Weigh the compound: each element's atomic weight times its count, then the total. The element "
              "is to the total as its weight is to the total weight: $113/T = 36/78$."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

MULTS = {2: "twice", 3: "3 times", 4: "4 times", 5: "5 times"}
MULT_OF = {w: k for k, w in MULTS.items()}

def plural(n, many):
    """1 blue, 2 blues; 1 box, 2 boxes is not needed here: every word is a plain -s plural."""
    return f"{n} {many[:-1] if n == 1 else many}"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def solve3(rows):
    """The one solution of three linear equations (a, b, c, rhs), exactly; None if there isn't one."""
    m = [[F(x) for x in row] for row in rows]
    for c in range(3):
        piv = next((r for r in range(c, 3) if m[r][c] != 0), None)
        if piv is None:
            return None
        m[c], m[piv] = m[piv], m[c]
        for r in range(3):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return tuple(m[i][3] / m[i][i] for i in range(3))

# ------------------------------------------------------------------
# Type 1: colors
# ------------------------------------------------------------------
COLORS = ("blues", "whites", "greens", "reds", "yellows", "purples", "oranges", "browns", "pinks", "grays")
COUNTS1 = range(1, 31)
OFFSETS = range(-15, 16)                 # the two statements' "... less / greater than"
T1_TEXT = {
    "past": "The number of {X} {r1} the sum of the {Y} and the {Z}. Also, the number of {Z} {r2} the sum of the "
            "{X} and the {Y}. How many of each were there if there were {k} as many {P} as {Q}?",
    "present": "The number of {X} {r1} the sum of the {Y} and the {Z}. The number of {Z} {r2} the sum of the {X} "
               "and the {Y}. How many of each kind are there if there are {k} as many {P} as {Q}?",
}
T1_ANSWER = "{a}, {b}, {c}"

def compare(d, tense):
    """The words for "this is (the sum) - d": d > 0 is "d less than", d < 0 "-d greater than"."""
    be, equal = ("was", "equaled") if tense == "past" else ("is", "equals")
    return equal if d == 0 else f"{be} {abs(d)} {'less' if d > 0 else 'greater'} than"

def compared(words):
    """compare() read back: the d with this = sum - d."""
    if words in ("equaled", "equals"):
        return 0
    m = re.fullmatch(r"(?:was|is) (\d+) (less|greater) than", words)
    if not m:
        raise ValueError("a statement's comparison")
    return int(m.group(1)) * (1 if m.group(2) == "less" else -1)

def t1(tense, X, Y, Z, P, Q, k, x, y, z):
    """X, Y, Z: the colors in the order named, with x, y, z of each; P is k times Q."""
    v = dict(X=X, Y=Y, Z=Z, P=P, Q=Q, k=MULTS[k], r1=compare(y + z - x, tense), r2=compare(x + y - z, tense))
    answer = gen.fill(T1_ANSWER, a=plural(x, X), b=plural(y, Y), c=plural(z, Z))
    return tense, gen.fill(T1_TEXT[tense], **v), answer

def t1_ok(tense, X, Y, Z, P, Q, k, x, y, z):
    n = {X: x, Y: y, Z: z}
    return (tense in T1_TEXT and all(c in COLORS for c in (X, Y, Z)) and len({X, Y, Z}) == 3
            and P in n and Q in n and P != Q and k in MULTS and n[P] == k * n[Q]
            and all(c in COUNTS1 for c in (x, y, z)) and y + z - x in OFFSETS and x + y - z in OFFSETS
            and color_solution(X, Y, Z, P, Q, k, y + z - x, z - x - y) == (x, y, z))

def color_solution(X, Y, Z, P, Q, k, d1, e):
    """N_X + d1 = N_Y + N_Z; N_Z = N_X + N_Y + e; N_P = k N_Q."""
    third = [0, 0, 0, 0]
    names = [X, Y, Z]
    third[names.index(P)] += 1
    third[names.index(Q)] -= k
    return solve3([(1, -1, -1, -d1), (-1, -1, 1, e), third])

BOOK_PAIRS = ((0, 1), (2, 0))            # 18.1: blues twice whites; problem 1: greens 3 times blues
ALL_PAIRS = tuple((i, j) for i in range(3) for j in range(3) if i != j)

def t1_pick(pairs):
    def pick(r):
        X, Y, Z = r.sample(COLORS, 3)
        i, j = r.choice(pairs)
        k = r.choice(list(MULTS))
        n = [None, None, None]
        n[j] = r.randint(1, 8)
        n[i] = k * n[j]
        third = 3 - i - j
        n[third] = r.randint(1, 20)
        names = (X, Y, Z)
        p = dict(tense=r.choice(list(T1_TEXT)), X=X, Y=Y, Z=Z, P=names[i], Q=names[j], k=k,
                 x=n[0], y=n[1], z=n[2])
        need(t1_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Type 2: coins
# ------------------------------------------------------------------
CENTS = {"quarters": 25, "nickels": 5, "dimes": 10}
BOOK_ORDER = ("quarters", "nickels", "dimes")
COUNTS2 = range(1, 31)
TOTALS2 = range(6, 41)
T2_TEXT = ("The {c1}, {c2}, and {c3} totaled {n}, and their value was ${v}. How many of each kind were there if "
           "there were {k} as many {A} as {B}?")
T2_ANSWER = "{a}, {b}, {c}"

def dollars(cents):
    return f"{cents // 100}.{cents % 100:02d}"

def t2(c1, c2, c3, A, B, k, n1, n2, n3):
    """The coins in the order listed, n1, n2, n3 of each; A is k times B."""
    v = dict(c1=c1, c2=c2, c3=c3, n=n1 + n2 + n3, v=dollars(n1 * CENTS[c1] + n2 * CENTS[c2] + n3 * CENTS[c3]),
             k=MULTS[k], A=A, B=B)
    return "coins", gen.fill(T2_TEXT, **v), gen.fill(T2_ANSWER, a=plural(n1, c1), b=plural(n2, c2),
                                                    c=plural(n3, c3))

def coin_solution(c1, c2, c3, A, B, k, n, cents):
    order = [c1, c2, c3]
    third = [0, 0, 0, 0]
    third[order.index(A)] += 1
    third[order.index(B)] -= k
    return solve3([(1, 1, 1, n), (CENTS[c1], CENTS[c2], CENTS[c3], cents), third])

def t2_ok(c1, c2, c3, A, B, k, n1, n2, n3):
    order = (c1, c2, c3)
    m = dict(zip(order, (n1, n2, n3)))
    return (sorted(order) == sorted(CENTS) and A in m and B in m and A != B and k in MULTS and m[A] == k * m[B]
            and all(c in COUNTS2 for c in (n1, n2, n3)) and n1 + n2 + n3 in TOTALS2
            and coin_solution(c1, c2, c3, A, B, k, n1 + n2 + n3,
                              sum(CENTS[c] * m[c] for c in order)) == (n1, n2, n3))

def t2_pick(shuffle):
    def pick(r):
        order = r.sample(BOOK_ORDER, 3) if shuffle else list(BOOK_ORDER)
        A, B = r.sample(BOOK_ORDER, 2)
        k = r.choice(list(MULTS))
        m = {B: r.randint(1, 8)}
        m[A] = k * m[B]
        third = next(c for c in BOOK_ORDER if c not in m)
        m[third] = r.choice(COUNTS2)
        p = dict(c1=order[0], c2=order[1], c3=order[2], A=A, B=B, k=k, n1=m[order[0]], n2=m[order[1]],
                 n3=m[order[2]])
        need(t2_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Type 3: R = k B^p / G^q
# ------------------------------------------------------------------
POWERS = {"2,1": (2, 1), "1,2": (1, 2), "1,1": (1, 1), "2,2": (2, 2)}
WORD_POWER = {1: "", 2: " squared"}
T3_TEXT = {key: "{Rc} varied directly as {B}" + WORD_POWER[p] + " and inversely as {G}" + WORD_POWER[q]
           + ". When there were {r1} {R}, there were {b1} {B} and {g1} {G}. How many {R} were there when there "
           "were {b2} {B} and {g2} {G}?" for key, (p, q) in POWERS.items()}
T3_ANSWER = "{r2} {R}"
SIZES3 = range(2, 13)                    # the blues and greens in each situation
KS = range(1, 61)                        # the constant of variation, a whole number
REDS = range(2, 2001)

def t3_value(key, k, b, g):
    p, q = POWERS[key]
    return F(k * b ** p, g ** q)

def t3(key, R, B, G, k, b1, g1, b2, g2):
    v = dict(Rc=R.capitalize(), R=R, B=B, G=G, r1=t3_value(key, k, b1, g1), b1=b1, g1=g1, b2=b2, g2=g2)
    return key, gen.fill(T3_TEXT[key], **v), gen.fill(T3_ANSWER, r2=t3_value(key, k, b2, g2), R=R)

def t3_ok(key, R, B, G, k, b1, g1, b2, g2):
    r1, r2 = t3_value(key, k, b1, g1), t3_value(key, k, b2, g2)
    return (key in POWERS and all(c in COLORS for c in (R, B, G)) and len({R, B, G}) == 3 and k in KS
            and all(s in SIZES3 for s in (b1, g1, b2, g2)) and (b1, g1) != (b2, g2)
            and r1.denominator == 1 and r2.denominator == 1 and r1 in REDS and r2 in REDS and r1 != r2)

def t3_pick(keys):
    def pick(r):
        key = r.choice(keys)
        p, q = POWERS[key]
        b1, g1 = r.choice(SIZES3), r.choice(SIZES3)
        base = g1 ** q // math.gcd(b1 ** p, g1 ** q)        # the least k that makes r1 whole
        need(base <= KS[-1])
        k = base * r.randint(1, KS[-1] // base)
        seconds = [(b, g) for b in SIZES3 for g in SIZES3 if (k * b ** p) % g ** q == 0 and (b, g) != (b1, g1)]
        need(seconds)
        b2, g2 = r.choice(seconds)
        R, B, G = r.sample(COLORS, 3)
        prm = dict(key=key, R=R, B=B, G=G, k=k, b1=b1, g1=g1, b2=b2, g2=g2)
        need(t3_ok(**prm))
        return prm
    return pick

# ------------------------------------------------------------------
# Type 4: digits
# ------------------------------------------------------------------
T4_TEXT = {
    "number": "The sum of the digits of a two-digit counting number is {s}. When the digits are reversed, the number "
              "is {d} {cmp} than the original number. What was the original number?",
    "new": "The sum of the digits of a two-digit counting number is {s}. When the digits are reversed, the new "
           "number is {d} {cmp} than the original number. What was the original number?",
}

def t4(story, t, u):
    """The original number has tens digit t and units digit u."""
    v = dict(s=t + u, d=9 * abs(u - t), cmp="greater" if u > t else "less")
    return story, gen.fill(T4_TEXT[story], **v), str(10 * t + u)

def t4_ok(story, t, u):
    return story in T4_TEXT and t in range(1, 10) and u in range(1, 10) and t != u

def t4_pick(story):
    def pick(r):
        p = dict(story=story, t=r.randint(1, 9), u=r.randint(1, 9))
        need(t4_ok(**p))
        return p
    return pick

def digit_solutions(s, d, cmp):
    """Every two-digit number that fits the story."""
    sign = 1 if cmp == "greater" else -1 if cmp == "less" else None
    if sign is None:
        raise ValueError("greater or less")
    return [n for n in range(10, 100) if n // 10 + n % 10 == s and (n % 10) * 10 + n // 10 - n == sign * d]

# ------------------------------------------------------------------
# Type 5: mixtures, both amounts from the total
# ------------------------------------------------------------------
UNITS5 = {"gallons (gal)": "gal", "liters (L)": "L", "milliliters (mL)": "mL", "ounces (oz)": "oz",
          "quarts (qt)": "qt"}
INGREDIENTS = ("alcohol", "glycol", "iodine", "acid", "antifreeze", "peroxide")
PERCENTS5 = range(5, 100, 5)             # the two solutions' strengths
TOTALS5 = tuple(range(20, 200, 10)) + tuple(range(200, 2001, 50))
T5_TEXT = ("To get {T} {unit1} of a mixture that was {tp}% {ing}, it was necessary to mix a quantity of {lp}% "
           "{ing} solution with a quantity of {hp}% {ing} solution. How much of each was required?")
T5_ANSWER = "{L} {u} of {lp}% {ing}, {H} {u} of {hp}% {ing}"

def t5(unit1, ing, lp, hp, L, H):
    """L of the weaker lp% and H of the stronger hp% make L + H of the target strength."""
    tp = F(lp * L + hp * H, L + H)
    v = dict(T=L + H, unit1=unit1, tp=tp, ing=ing, lp=lp, hp=hp)
    return "total", gen.fill(T5_TEXT, **v), gen.fill(T5_ANSWER, L=L, H=H, u=UNITS5[unit1], lp=lp, hp=hp, ing=ing)

def t5_ok(unit1, ing, lp, hp, L, H):
    tp = F(lp * L + hp * H, L + H) if L + H else F(0)
    return (unit1 in UNITS5 and ing in INGREDIENTS and lp in PERCENTS5 and hp in PERCENTS5 and lp < hp
            and L >= 1 and H >= 1 and L + H in TOTALS5 and tp.denominator == 1)

def t5_pick(r):
    lp, hp = sorted(r.sample(PERCENTS5, 2))
    T_ = r.choice(TOTALS5)
    step = 10 if T_ < 200 else 50 if T_ < 1000 else 100
    fits = [L for L in range(step, T_, step) if (lp * L + hp * (T_ - L)) % T_ == 0]
    need(fits)
    L = r.choice(fits)
    p = dict(unit1=r.choice(list(UNITS5)), ing=r.choice(INGREDIENTS), lp=lp, hp=hp, L=L, H=T_ - L)
    need(t5_ok(**p))
    return p

# ------------------------------------------------------------------
# Type 6: mixtures, the amount to add
# ------------------------------------------------------------------
UNITS6 = ("liters", "ounces", "gallons", "milliliters", "quarts")
T6_TEXT = {
    "many": "How many {unit} of {a1} {ap}% {ing} solution must be added to {A} {unit} of {a2} {bp}% {ing} solution "
            "to get {a3} {tp}% {ing} solution?",
    "much": "How much of {a1} {ap}% {ing} solution should be added to {A} {unit} of {a2} {bp}% {ing} solution to "
            "get {a3} {tp}% solution?",
}
T6_ANSWER = "{x} {unit}"
PERCENTS6 = range(5, 96)
AMOUNTS6 = range(10, 201)
ADDED = (F(1, 4), F(3))                  # the amount added, as a part of the amount given: at least, at most

def article(n):
    """a 64%, an 82%, an 18%, an 8%."""
    return "an" if n in (8, 11, 18) or 80 <= n <= 89 else "a"

def t6_value(A, ap, bp, tp):
    return F(A * (tp - bp), ap - tp)

def t6(story, unit, ing, ap, A, bp, tp):
    """x of the ap% solution added to A of the bp% one makes tp%."""
    v = dict(unit=unit, ap=ap, ing=ing, A=A, bp=bp, tp=tp, a1=article(ap), a2=article(bp), a3=article(tp))
    return story, gen.fill(T6_TEXT[story], **v), gen.fill(T6_ANSWER, x=rounded(t6_value(A, ap, bp, tp)), unit=unit)

def t6_ok(story, unit, ing, ap, A, bp, tp):
    return (story in T6_TEXT and unit in UNITS6 and ing in INGREDIENTS and all(c in PERCENTS6 for c in (ap, bp, tp))
            and A in AMOUNTS6 and min(ap, bp) < tp < max(ap, bp) and abs(ap - bp) >= 10
            and ADDED[0] * A <= t6_value(A, ap, bp, tp) <= ADDED[1] * A)

def t6_pick(story):
    def pick(r):
        ap, bp = r.sample(PERCENTS6, 2)
        lo, hi = sorted((ap, bp))
        need(hi - lo >= 10)
        p = dict(story=story, unit=r.choice(UNITS6), ing=r.choice(INGREDIENTS), ap=ap, A=r.choice(AMOUNTS6), bp=bp,
                 tp=r.randint(lo + 1, hi - 1))
        need(t6_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Type 7: a compound's weight
# ------------------------------------------------------------------
ELEMENTS = {"C": ("carbon", 12), "H": ("hydrogen", 1), "Cl": ("chlorine", 35), "O": ("oxygen", 16),
            "N": ("nitrogen", 14), "Na": ("sodium", 23), "S": ("sulfur", 32), "Ca": ("calcium", 40),
            "Fe": ("iron", 56), "Mg": ("magnesium", 24), "K": ("potassium", 39), "Al": ("aluminum", 27)}
SYMBOL_OF = {name: s for s, (name, _) in ELEMENTS.items()}
COMPOUNDS = ("C3H7Cl", "H2O", "CO2", "NaCl", "C6H12O6", "NH3", "H2SO4", "CaCO3", "CH4", "Fe2O3", "C3H8", "NaOH",
             "MgO", "KCl", "Al2O3", "CaCl2", "HNO3", "NaHCO3", "C2H5Cl", "MgCl2", "KNO3", "C2H6O", "Na2SO4")
GRAMS = range(5, 1001)
SHARE = F(1, 5)                          # the given element is at least this part of the compound's weight
T7_TEXT = ("The weight of the {el} ({sym}) in the container of {formula} was {w} grams. What was the total weight "
           "of the compound? ({weights})")
T7_ANSWER = "{T} grams"

def parts(formula):
    """[(symbol, count)] in the formula's order: C3H7Cl is [(C, 3), (H, 7), (Cl, 1)]."""
    found = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    if "".join(s + c for s, c in found) != formula:
        raise ValueError("a formula")
    return [(s, int(c) if c else 1) for s, c in found]

def t7_value(formula, sym, w, weight=lambda s: ELEMENTS[s][1]):
    ps = parts(formula)
    total = sum(weight(s) * c for s, c in ps)
    part = sum(weight(s) * c for s, c in ps if s == sym)
    return F(w * total, part)

def t7(formula, sym, w):
    weights = "; ".join(f"{s} = {ELEMENTS[s][1]}" for s, _ in parts(formula))
    v = dict(el=ELEMENTS[sym][0], sym=sym, formula=formula, w=w, weights=weights)
    return "compound", gen.fill(T7_TEXT, **v), gen.fill(T7_ANSWER, T=rounded(t7_value(formula, sym, w)))

def t7_ok(formula, sym, w):
    return (formula in COMPOUNDS and sym in dict(parts(formula)) and w in GRAMS
            and F(w) / t7_value(formula, sym, w) >= SHARE)

def t7_pick(r):
    formula = r.choice(COMPOUNDS)
    p = dict(formula=formula, sym=r.choice(parts(formula))[0], w=r.choice(GRAMS))
    need(t7_ok(**p))
    return p

# ------------------------------------------------------------------
# Templates: (pick, build); the build writes (story, prompt, answer)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick(BOOK_PAIRS), t1), (t1_pick(ALL_PAIRS), t1)],
    "2": [(t2_pick(False), t2), (t2_pick(False), t2), (t2_pick(True), t2)],
    "3": [(t3_pick(["2,1"]), t3), (t3_pick(["1,2"]), t3), (t3_pick(["1,1", "2,2"]), t3)],
    "4": [(t4_pick("number"), t4), (t4_pick("new"), t4)],
    "5": [(t5_pick, t5)],
    "6": [(t6_pick("many"), t6), (t6_pick("much"), t6)],
    "7": [(t7_pick, t7)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok, t6: t6_ok, t7: t7_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    story, prompt, answer = build(**pick(r))
    return dict(story=story, prompt=prompt, answer=answer)

# ------------------------------------------------------------------
# Checking: read the story's numbers, put the answer back in
# ------------------------------------------------------------------
def template(typ, story):
    return {"1": lambda: T1_TEXT[story], "2": lambda: T2_TEXT, "3": lambda: T3_TEXT[story],
            "4": lambda: T4_TEXT[story], "5": lambda: T5_TEXT, "6": lambda: T6_TEXT[story],
            "7": lambda: T7_TEXT}[typ]()

def whole(s):
    n = gen.number(s)
    if n.denominator != 1:
        raise ValueError("a whole number")
    return int(n)

def counted(answer, names):
    """ "4 blues, 2 whites, 6 greens" read back in the given names' order, singular or plural."""
    got = answer.split(", ")
    if len(got) != len(names):
        raise ValueError("one count per kind")
    out = []
    for g, name in zip(got, names):
        m = re.fullmatch(r"(\d+) (\w+)", g)
        n = int(m.group(1))
        if m.group(2) != (name[:-1] if n == 1 else name):
            raise ValueError("the kinds in the story's order")
        out.append(n)
    return tuple(out)

def solve(typ, story, v):
    """The answer's words, from the story's numbers (as read); ValueError if there is none."""
    if typ == "1":
        X, Y, Z = v["X"], v["Y"], v["Z"]
        sol = color_solution(X, Y, Z, v["P"], v["Q"], MULT_OF[v["k"]], compared(v["r1"]), -compared(v["r2"]))
        if sol is None or any(s.denominator != 1 or s < 1 for s in sol):
            raise ValueError("no answer in whole counts")
        return gen.fill(T1_ANSWER, a=plural(int(sol[0]), X), b=plural(int(sol[1]), Y), c=plural(int(sol[2]), Z))
    if typ == "2":
        cs = (v["c1"], v["c2"], v["c3"])
        if sorted(cs) != sorted(CENTS):
            raise ValueError("quarters, nickels, and dimes")
        sol = coin_solution(*cs, v["A"], v["B"], MULT_OF[v["k"]], whole(v["n"]), int(gen.number(v["v"]) * 100))
        if sol is None or any(s.denominator != 1 or s < 1 for s in sol):
            raise ValueError("no answer in whole coins")
        return gen.fill(T2_ANSWER, a=plural(int(sol[0]), cs[0]), b=plural(int(sol[1]), cs[1]),
                        c=plural(int(sol[2]), cs[2]))
    if typ == "3":
        p, q = POWERS[story]
        k = F(whole(v["r1"]) * whole(v["g1"]) ** q, whole(v["b1"]) ** p)
        r2 = k * whole(v["b2"]) ** p / whole(v["g2"]) ** q
        if r2.denominator != 1:
            raise ValueError("no answer in whole counts")
        return gen.fill(T3_ANSWER, r2=r2, R=v["R"])
    if typ == "4":
        sols = digit_solutions(whole(v["s"]), whole(v["d"]), v["cmp"])
        if len(sols) != 1:
            raise ValueError("no single answer")
        return str(sols[0])
    if typ == "5":
        T_, tp, lp, hp = (whole(v[x]) for x in ("T", "tp", "lp", "hp"))
        if not lp < tp < hp:
            raise ValueError("the target between the two")
        H = F((tp - lp) * T_, hp - lp)
        L = T_ - H
        if H.denominator != 1:
            raise ValueError("whole amounts")
        return gen.fill(T5_ANSWER, L=L, H=H, u=UNITS5[v["unit1"]], lp=lp, hp=hp, ing=v["ing"])
    if typ == "6":
        A, ap, bp, tp = (whole(v[x]) for x in ("A", "ap", "bp", "tp"))
        if not min(ap, bp) < tp < max(ap, bp):
            raise ValueError("the target between the two")
        return gen.fill(T6_ANSWER, x=rounded(F(A * (tp - bp), ap - tp)), unit=v["unit"])
    return gen.fill(T7_ANSWER, T=rounded(compound_total(v)))

def compound_total(v):
    """The given weight times the compound's weight over the element's, with the story's atomic weights."""
    given = {}
    for item in v["weights"].split("; "):
        s, w = item.split(" = ")
        given[s] = whole(w)
    ps = parts(v["formula"])
    if set(given) != {s for s, _ in ps} or SYMBOL_OF.get(v["el"]) != v["sym"]:
        raise ValueError("the formula's elements")
    total = sum(given[s] * c for s, c in ps)
    part = sum(given[s] * c for s, c in ps if s == v["sym"])
    return F(whole(v["w"]) * total, part)

def check(p):
    """The answer put back into the lesson's equations (see the docstring)."""
    try:
        typ, story = p["type"], p["story"]
        v = gen.read(template(typ, story), p["prompt"])
        ans = " ".join(p["answer"].split())
        if typ == "1":
            x, y, z = counted(ans, (v["X"], v["Y"], v["Z"]))
            n = {v["X"]: x, v["Y"]: y, v["Z"]: z}
            ok = (x + compared(v["r1"]) == y + z and z == x + y - compared(v["r2"])
                  and n[v["P"]] == MULT_OF[v["k"]] * n[v["Q"]]
                  and color_solution(v["X"], v["Y"], v["Z"], v["P"], v["Q"], MULT_OF[v["k"]],
                                     compared(v["r1"]), -compared(v["r2"])) is not None)
        elif typ == "2":
            cs = (v["c1"], v["c2"], v["c3"])
            got = counted(ans, cs)
            n = dict(zip(cs, got))
            cents = gen.number(v["v"]) * 100
            ok = (sorted(cs) == sorted(CENTS) and sum(got) == whole(v["n"])
                  and sum(CENTS[c] * n[c] for c in cs) == cents and n[v["A"]] == MULT_OF[v["k"]] * n[v["B"]]
                  and coin_solution(*cs, v["A"], v["B"], MULT_OF[v["k"]], whole(v["n"]), cents) is not None)
        elif typ == "3":
            m = re.fullmatch(r"(\d+) (\w+)", ans)
            p_, q = POWERS[story]
            r1, b1, g1, b2, g2 = (whole(v[x]) for x in ("r1", "b1", "g1", "b2", "g2"))
            r2 = int(m.group(1))
            # R G^q / B^p is the same in both situations: r1 g1^q b2^p = r2 g2^q b1^p
            ok = (r1 * g1 ** q * b2 ** p_ == r2 * g2 ** q * b1 ** p_ and m.group(2) == v["R"]
                  and v["Rc"] == v["R"].capitalize())
        elif typ == "4":
            n = int(ans) if re.fullmatch(r"[1-9]\d", ans) else None
            ok = n is not None and digit_solutions(whole(v["s"]), whole(v["d"]), v["cmp"]) == [n]
        elif typ == "5":
            got = gen.read(T5_ANSWER, ans)
            L, H, T_ = whole(got["L"]), whole(got["H"]), whole(v["T"])
            lp, hp, tp = whole(v["lp"]), whole(v["hp"]), whole(v["tp"])
            ok = (L + H == T_ and lp * L + hp * H == tp * T_ and L > 0 and H > 0
                  and (got["lp"], got["hp"]) == (v["lp"], v["hp"]) and lp < hp
                  and got["u"] == UNITS5[v["unit1"]] and got["ing"] == v["ing"])
        elif typ == "6":
            got = gen.read(T6_ANSWER, ans)
            A, ap, bp, tp = (whole(v[x]) for x in ("A", "ap", "bp", "tp"))
            # the ingredient: bp A + ap x = tp (A + x), so x = A (tp - bp)/(ap - tp)
            x = F(A * (tp - bp), ap - tp)
            ok = (x > 0 and got["x"] == rounded(x) and got["unit"] == v["unit"]
                  and all(v[a] == article(whole(v[n])) for a, n in (("a1", "ap"), ("a2", "bp"), ("a3", "tp"))))
        else:
            got = gen.read(T7_ANSWER, ans)
            ok = got["T"] == rounded(compound_total(v))
    except (ValueError, KeyError, AttributeError, ZeroDivisionError, TypeError):
        return "unchecked"
    return "checked" if ok else "failed"

def answer_of(typ, story, prompt):
    return solve(typ, story, gen.read(template(typ, story), prompt))

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: words, with chemical formulas set as math
# ------------------------------------------------------------------
FORMULA = re.compile(r"\b(?:[A-Z][a-z]?\d*){2,}\b|\b[A-Z][a-z]?\d+\b")

def formula_math(f):
    """C3H7Cl as $"C"_3"H"_7"Cl"$, as the deck sets it; NaHCO3 as $"NaHCO"_3$."""
    out, run = "", ""
    for s, c in re.findall(r"([A-Z][a-z]?)(\d*)", f):
        run += s
        if c:
            out, run = out + f'"{run}"_{c}', ""
    return "$" + out + (f'"{run}"' if run else "") + "$"

def marked(s):
    """The formula as math, and each atomic weight kept on one line: (C~=~12; ...)."""
    return FORMULA.sub(lambda m: formula_math(m.group(0)), esc(s)).replace(" = ", "~=~")

def typst(p, gap="0.3em"):
    return marked(p["prompt"]) if p["type"] == "7" else esc(p["prompt"])

def answer_typst(p):
    return esc(p["answer"])

def text(p):
    return p["prompt"]

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.2 * (1 + len(p["prompt"]) // 90)

# ------------------------------------------------------------------
# Editing: change the numbers and names; keep the words
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    gen.read(template(old["type"], old["story"]), t)      # ValueError: keep the story's words
    try:
        answer = answer_of(old["type"], old["story"], t)
    except (ValueError, KeyError, ZeroDivisionError, TypeError):
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
