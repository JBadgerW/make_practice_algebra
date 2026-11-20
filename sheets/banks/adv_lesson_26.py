"""Lesson 26 (Advanced Math): the logarithmic form of the exponential,
logarithmic equations. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_026/slides/deck_026.typ): examples
26.1-26.7 and Problem Set 26, problems 6-10.

    1  exponential to logarithmic form:     4 = 3^y;  k^p = 7;  b^a = 12               log_3 4 = y
    2  logarithmic to exponential form:     log_x 4 = m;  log_k 7 = p;  log_b 12 = a   x^m = 4
    3  the base, a whole-number log:        log_b 8 = 3;  log_b 27 = 3                 b = 2
    4  the base, a negative or fractional log:
                                            log_b 9 = -1/2                             b = 1/81
    5  the log, the number a power of the base:
                                            log_3 (1/27) = M;  log_2 (1/8) = m         M = -3
    6  the log, both powers of one number:  log_4 8 = x                                x = 3/2
    7  the number:                          log_(1/3) P = -2;  log_(1/2) c = -4        P = 9

The types file's first heading (changing between the forms) is split by
direction, since each has its own answer form; problems 6 and 7 are two
problems each, one a part. Its "solve for the base" heading is split by the
move: a whole-number log takes a root (26.3, problem 8), a negative or
fractional one raises both sides to the reciprocal power (26.4, which has no
Problem Set item). Its "solve for the logarithm" heading is split too: when
the number is a power of the base (26.5, problem 9) the exponents are read
off; when it isn't (26.7, no item), base and number are both rewritten as
powers of one number.

The key writes what the deck writes:
  1  log_b N = L, the base as a subscript: log_3 4 = y, log_k 7 = p.
  2  b^L = N, the power on the left: x^m = 4, k^p = 7, b^a = 12.
  3-7  the letter named, its value a whole number or a fraction in lowest
     terms (the deck bolds the value; Lesson 6's keys name the letter):
     b = 2, b = 1/81, M = -3, x = 3/2, P = 9, c = 16.

check() is independent of how a problem was built. It reads the prompt and
the answer as (base, log, number) triples:
  1-2  the answer is in the other form, with the same base, log, and number;
       when all three are numbers, b^L = N must also hold.
  3-7  the answer names the prompt's one letter; its value put in for the
       letter makes b^L = N exactly (sympy rationals), with the base positive
       and not 1 and the number positive; the value is written in lowest terms.

No skipped sources: Lesson 26 has no proofs.

A problem: dict(type, prompt, answer, source), in Typst math. A fraction is
in parentheses where it is a log's base or number, or an exponent:
    prompt  "log_(1/3) P = -2"           answer  "P = 9"
    prompt  "3^(-2) = 1/9"               answer  "log_3 (1/9) = -2"
On a sheet the prompt is shown in its sentence, the subscript fraction with
a slash and the others full size: Solve: log_(1/3) P = -2.
"""
import re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need

NAME = FAMILY = "adv_lesson_26"
FIXED = False
TITLE = "Lesson 26: The Logarithmic Form of the Exponential, Logarithmic Equations"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="Exponential to Logarithmic Form",
         instructions="Write each equation in logarithmic form.",
         look="An exponential equation, like $4 = 3^y$ or $k^p = 7$.",
         move="The logarithm is the exponent. Write $log$, the base as its subscript, then the number, and set it "
              "equal to the exponent: $4 = 3^y$ becomes $log_3 4 = y$."),
    dict(key="2", title="Logarithmic to Exponential Form",
         instructions="Write each equation in exponential form.",
         look="A logarithmic equation, like $log_x 4 = m$.",
         move="The subscript is the base and the logarithm is the exponent. Raise the base to the exponent; it "
              "equals the number left over: $log_x 4 = m$ becomes $x^m = 4$."),
    dict(key="3", title="Solve for the Base: A Whole-Number Log",
         look="$log_b N = L$ with the base unknown and $L$ a whole number, like $log_b 8 = 3$.",
         move="Write it in exponential form, $b^3 = 8$. Raise both sides to the $1/3$ power: $b = 8^(1/3) = 2$."),
    dict(key="4", title="Solve for the Base: A Negative or Fractional Log",
         look="The base unknown and the log negative or a fraction, like $log_b 9 = -1/2$.",
         move="Write $b^(-1/2) = 9$. Raise both sides to the reciprocal power, $-2$: $b = 9^(-2) = 1/81$."),
    dict(key="5", title="Solve for the Log: The Number Is a Power of the Base",
         look="The log unknown, and the number a power of the base, like $log_3 1/27 = M$.",
         move="Write $3^M = 1/27$. Write the number as a power of the base, $1/27 = 3^(-3)$, and set the "
              "exponents equal: $M = -3$."),
    dict(key="6", title="Solve for the Log: Powers of One Number",
         look="The log unknown; base and number are powers of the same number, like $log_4 8 = x$.",
         move="Write $4^x = 8$. Write both as powers of 2: $(2^2)^x = 2^3$, so $2x = 3$ and $x = 3/2$."),
    dict(key="7", title="Solve for the Number",
         look="The number unknown, like $log_(1\\/3) P = -2$.",
         move="Write it in exponential form, $P = (1/3)^(-2)$, and simplify: a negative exponent flips the "
              "fraction, so $P = 3^2 = 9$."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
CONVERT = ("1", "2")

# letters for the unknowns: the shared ones and the book's capitals (26.5's M, 26.6's P)
LETTERS = gen.LETTERS + tuple("LMNP")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing and reading the two forms. A part is a letter (str) or a Fraction.
# ------------------------------------------------------------------
def q(s):
    return s if isinstance(s, str) else F(s)

def number(x):
    """A number as the right side or an exponential's number writes it: 9, -3, 1/9, -1/2."""
    return x if isinstance(x, str) else str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def wrapped(x):
    """A log's base or number, or a power's base: 3, (1/3), (1/27); a letter as is."""
    s = number(x)
    return f"({s})" if "/" in s or s.startswith("-") else s

def exponent(x):
    """An exponent: 3, (-2), (1/2), (-1/2); a letter as is."""
    return wrapped(x)

def log_form(b, N, L):
    return f"log_{wrapped(b)} {wrapped(N)} = {number(L)}"

def exp_form(b, L, N, power_first=True):
    power = f"{wrapped(b)}^{exponent(L)}"
    return f"{power} = {number(N)}" if power_first else f"{number(N)} = {power}"

TOKEN = r"(?:[A-Za-z]|\(-?\d+(?:/\d+)?\)|-?\d+(?:/\d+)?)"
LOG = re.compile(rf"log_({TOKEN}) ({TOKEN}) = ({TOKEN})")
EXP_FIRST = re.compile(rf"({TOKEN})\^({TOKEN}) = ({TOKEN})")
EXP_LAST = re.compile(rf"({TOKEN}) = ({TOKEN})\^({TOKEN})")

def part(tok):
    t = tok.strip("()") if tok.startswith("(") else tok
    return t if re.fullmatch(r"[A-Za-z]", t) else F(t)

def clean(t):
    return " ".join(t.replace("−", "-").replace("\\/", "/").split())

def read(t):
    """(form, b, L, N): form is "log", "exp" (power first), or "exp last"; ValueError if neither."""
    t = clean(t)
    m = LOG.fullmatch(t)
    if m:
        return ("log", part(m[1]), part(m[3]), part(m[2]))
    m = EXP_FIRST.fullmatch(t)
    if m:
        return ("exp", part(m[1]), part(m[2]), part(m[3]))
    m = EXP_LAST.fullmatch(t)
    if m:
        return ("exp last", part(m[2]), part(m[3]), part(m[1]))
    raise ValueError("write log_b N = L or b^L = N")

def letters_in(*parts_):
    return [x for x in parts_ if isinstance(x, str)]

# ------------------------------------------------------------------
# Ranges
# ------------------------------------------------------------------
BASES = range(2, 11)                     # whole-number bases
NUMBERS = range(2, 51)                   # a number to convert, with a letter for the log
POWERS = range(-4, 6)                    # whole-number logs (0 and 1 are left out where trivial)
ROOTS = range(2, 11)                     # the one number both are powers of (Types 4, 6, 7)
BIG = 1000                               # no numerator or denominator past this

def small(x):
    return isinstance(x, str) or (abs(x.numerator) <= BIG and x.denominator <= BIG)

def distinct(*xs):
    ls = letters_in(*xs)
    return len(set(ls)) == len(ls)

def is_unit(b):
    """A whole-number base or its reciprocal (26.6's 1/3, problem 10's 1/2)."""
    return (b.denominator == 1 and b.numerator in BASES) or (b.numerator == 1 and b.denominator in BASES)

# ------------------------------------------------------------------
# Types 1 and 2: changing forms
# ------------------------------------------------------------------
def t1(b, L, N, power_first):
    return exp_form(q(b), q(L), q(N), power_first)

def t2(b, N, L):
    return log_form(q(b), q(N), q(L))

def true_triple(b, L, N):
    return (F(b) ** F(L) == F(N)) if F(L).denominator == 1 else sp.Rational(F(b)) ** sp.Rational(F(L)) == \
        sp.Rational(F(N))

def convert_ok(b, L, N):
    b, L, N = q(b), q(L), q(N)
    if not distinct(b, L, N) or not all(small(x) for x in (b, L, N)):
        return False
    if isinstance(L, str):                                       # the sources: the log a letter
        return isinstance(N, F) and N in [F(n) for n in NUMBERS] and \
            (isinstance(b, str) or b in [F(x) for x in BASES]
             and all(b ** k != N for k in range(1, 7)))           # else it's a Type 5 to solve
    if isinstance(b, str) or isinstance(N, str):
        return False
    return is_unit(b) and L != 0 and L != 1 and true_triple(b, L, N)   # all numbers: a true statement

def t1_ok(b, L, N, power_first):
    return power_first in (True, False) and convert_ok(b, L, N)

def t2_ok(b, N, L):
    return convert_ok(b, L, N)

def letters_pick(r):
    """The sources' kind: the log a letter; the base a letter or a whole number; the number whole."""
    x, y = r.sample(LETTERS, 2)
    b = x if r.random() < 0.6 else F(r.choice(BASES))
    return dict(b=b, L=y, N=F(r.choice(NUMBERS)))

def numbers_pick(r):
    """All three numbers: 2^5 = 32, 3^(-2) = 1/9, (1/2)^3 = 1/8, 9^(1/2) = 3."""
    root = r.choice(ROOTS)
    if r.random() < 0.25:                                        # a root: 9^(1/2) = 3, 8^(2/3) = 4
        k, j = r.choice(((2, 1), (3, 1), (3, 2), (2, -1)))
        b, L, N = F(root ** k), F(j, k), F(root) ** j
    else:
        b = F(root) if r.random() < 0.75 else F(1, root)
        L = F(r.choice([e for e in POWERS if e not in (0, 1)]))
        N = b ** L
    return dict(b=b, L=L, N=N)

def t1_pick(kind):
    def pick(r):
        p = dict(kind(r), power_first=r.random() < 0.5)
        need(t1_ok(**p))
        return p
    return pick

def t2_pick(kind):
    def pick(r):
        p = kind(r)
        need(t2_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Types 3 and 4: the base unknown
# ------------------------------------------------------------------
def t3(x, b, L):
    """log_x (b^L) = L, the answer x = b."""
    return log_form(x, F(b) ** L, F(L))

def t3_ok(x, b, L):
    return x in LETTERS and b in BASES and L in range(2, 6) and small(F(b) ** L)

def t3_pick(r):
    p = dict(x=r.choice(LETTERS), b=r.choice(BASES), L=r.choice(range(2, 6)))
    need(t3_ok(**p))
    return p

def t4(x, root, n, m):
    """The number root^n, the base root^m, so the log is n/m: 26.4 is root 3, n 2, m -4."""
    return log_form(x, F(root) ** n, F(n, m))

def t4_ok(x, root, n, m):
    L = F(n, m) if m else F(0)
    return (x in LETTERS and root in ROOTS and n in range(1, 5) and m in range(-4, 5) and m != 0
            and not (L > 0 and L.denominator == 1)                   # that is Type 3
            and abs(L.numerator) <= 4 and small(F(root) ** n) and small(F(root) ** m)
            )

def t4_pick(r):
    p = dict(x=r.choice(LETTERS), root=r.choice((2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10)), n=r.randint(1, 4),
             m=r.choice([-4, -3, -2, -1, 2, 3, 4]))
    need(t4_ok(**p))
    need(F(p["n"], p["m"]) != -1 or r.random() < 0.25)            # mostly a fraction, as 26.4 is
    return p

# ------------------------------------------------------------------
# Types 5 and 6: the log unknown
# ------------------------------------------------------------------
def t5(x, b, k):
    """log_b (b^k) = x, the answer x = k; b whole or a unit fraction."""
    b = F(b)
    return log_form(b, b ** k, x)

def t5_ok(x, b, k):
    b = F(b)
    return x in LETTERS and is_unit(b) and k in POWERS and k not in (0, 1) and small(b ** k)

def t5_pick(r):
    b = F(r.choice(BASES)) if r.random() < 0.8 else F(1, r.choice(BASES))
    k = r.choice((-4, -3, -3, -2, -2, -1, 2, 3, 4, 5))            # the book's are negative
    p = dict(x=r.choice(LETTERS), b=b, k=k)
    need(t5_ok(**p))
    return p

def t6(x, root, m, n):
    """log_(root^m) (root^n) = x, the answer n/m: 26.7 is root 2, m 2, n 3."""
    return log_form(F(root) ** m, F(root) ** n, x)

def t6_ok(x, root, m, n):
    return (x in LETTERS and root in (2, 3, 5, 6, 7, 10) and m in range(2, 5) and n in range(-5, 6) and n != 0
            and F(n, m).denominator != 1 and small(F(root) ** m) and small(F(root) ** n))

def t6_pick(r):
    p = dict(x=r.choice(LETTERS), root=r.choice((2, 2, 2, 3, 3, 5, 6, 7, 10)), m=r.randint(2, 4),
             n=r.choice((-3, -2, -1, 1, 2, 3, 3, 4, 5)))
    need(t6_ok(**p))
    return p

# ------------------------------------------------------------------
# Type 7: the number unknown
# ------------------------------------------------------------------
def t7(x, b, L):
    """log_b x = L, the answer b^L."""
    return log_form(F(b), x, F(L))

def t7_ok(x, b, L):
    b, L = F(b), F(L)
    if not (x in LETTERS and L != 0 and L != 1 and abs(L.numerator) <= 5):
        return False
    if L.denominator == 1:
        return is_unit(b) and small(b ** int(L))
    root = round(float(b) ** (1 / L.denominator)) if b > 1 else 0   # a perfect power: 8 = 2^3, 4 = 2^2
    return (L.denominator in (2, 3) and root in ROOTS and F(root) ** L.denominator == b
            and small(F(root) ** L.numerator))

def t7_whole(r):
    b = F(1, r.choice(BASES)) if r.random() < 0.5 else F(r.choice(BASES))
    L = r.choice((-4, -3, -2, -2, -1, 2, 3)) if b < 1 else r.choice((-3, -2, -1, 2, 3, 4))
    p = dict(x=r.choice(LETTERS), b=b, L=F(L))
    need(t7_ok(**p))
    return p

def t7_root(r):
    """A fractional log: log_8 x = 2/3, x = 4."""
    k = r.choice((2, 3))
    root = r.choice(ROOTS)
    j = r.choice([j for j in range(-4, 5) if j and j % k])
    p = dict(x=r.choice(LETTERS), b=F(root) ** k, L=F(j, k))
    need(t7_ok(**p))
    return p

# ------------------------------------------------------------------
# Templates: (pick, build)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick(letters_pick), t1), (t1_pick(letters_pick), t1), (t1_pick(numbers_pick), t1)],
    "2": [(t2_pick(letters_pick), t2), (t2_pick(letters_pick), t2), (t2_pick(numbers_pick), t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick, t4)],
    "5": [(t5_pick, t5)],
    "6": [(t6_pick, t6)],
    "7": [(t7_whole, t7), (t7_whole, t7), (t7_root, t7)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok, t6: t6_ok, t7: t7_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving and checking, from the text alone
# ------------------------------------------------------------------
def rat(x):
    return sp.Rational(x.numerator, x.denominator)

def holds(b, L, N):
    """b^L = N exactly, with b positive and not 1, and N positive."""
    return b > 0 and b != 1 and N > 0 and rat(b) ** rat(L) == rat(N)

def solve(prompt):
    """(letter, value) for a log equation with one letter; ValueError unless the value is rational."""
    form, b, L, N = read(prompt)
    ls = letters_in(b, L, N)
    if form != "log" or len(ls) != 1:
        raise ValueError("one letter in log_b N = L")
    if isinstance(b, str):
        v = rat(N) ** (1 / rat(L))
    elif isinstance(L, str):                                     # b^(p/q) = N: b^p = N^q, exactly
        fits = [F(a, c) for c in range(1, 13) for a in range(-60, 61) if b ** a == N ** c]
        if not fits:
            raise ValueError("no rational answer")
        return ls[0], fits[0]
    else:
        v = rat(b) ** rat(L)
    if not v.is_Rational:
        raise ValueError("no rational answer")
    return ls[0], F(int(v.p), int(v.q))

def answer_of(prompt, typ):
    form, b, L, N = read(prompt)
    if typ in CONVERT:
        return log_form(b, N, L) if form != "log" else exp_form(b, L, N)
    x, v = solve(prompt)
    return f"{x} = {number(v)}"

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

def check(p):
    try:
        typ = p["type"]
        form, b, L, N = read(p["prompt"])
        ans = clean(p["answer"])
        if typ in CONVERT:
            aform, ab, aL, aN = read(ans)
            want = "log" if typ == "1" else "exp"
            ok = (form != "log") == (typ == "1") and aform == want and (ab, aL, aN) == (b, L, N)
            if ok and not letters_in(b, L, N):
                ok = holds(b, L, N)
        else:
            m = re.fullmatch(r"([A-Za-z]) = (-?\d+(?:/\d+)?)", ans)
            ls = letters_in(b, L, N)
            if form != "log" or len(ls) != 1 or not m or m[1] != ls[0]:
                return "failed"
            v = F(m[2])
            ok = number(v) == m[2]                                           # lowest terms
            b, L, N = (v if x == m[1] else x for x in (b, L, N))
            ok = ok and holds(b, L, N)
    except (ValueError, KeyError, TypeError, ZeroDivisionError):
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: each problem in its own sentence, as the deck writes it
# ------------------------------------------------------------------
def pretty(t):
    """Typst math as the deck sets it: log_(1\\/3) P, log_3 display(1/27), = -display(1/2)."""
    t = re.sub(r"log_\((-?\d+)/(\d+)\)", r"log_(\1\\/\2)", t)
    t = re.sub(r"(log_\S+) \((\d+)/(\d+)\)", r"\1 display(\2/\3)", t)
    t = re.sub(r"(^|= )(-?)(\d+)/(\d+)$", r"\1\2display(\3/\4)", t)
    t = re.sub(r"^(-?)(\d+)/(\d+) =", r"\1display(\2/\3) =", t)
    return t

SENTENCE = {"1": ("Write ", " in logarithmic form."), "2": ("Write ", " in exponential form.")}

def typst(p, gap="0.3em"):
    before, after = SENTENCE.get(p["type"], ("Solve: #h(0.5em) ", ""))
    return f"{before}${pretty(p['prompt'])}${after}"

def answer_typst(p):
    return f"${pretty(p['answer'])}$"

def text(p):
    before, after = SENTENCE.get(p["type"], ("Solve: ", ""))
    return before + p["prompt"] + after

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.55 if "/" in p["prompt"] else 0.35

# ------------------------------------------------------------------
# Editing: an edited prompt is solved again
# ------------------------------------------------------------------
EXAMPLE = {"1": "4 = 3^y", "2": "log_x 4 = m", "3": "log_b 8 = 3", "4": "log_b 9 = -1/2",
           "5": "log_3 (1/27) = M", "6": "log_4 8 = x", "7": "log_(1/3) P = -2"}

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    typ = old.get("type", "1")
    t = clean(t)
    try:
        read(t)
    except ValueError:
        raise ValueError(f"write it in Typst math, like {EXAMPLE[typ]}") from None
    try:
        answer = answer_of(t, typ)
    except (ValueError, ZeroDivisionError, TypeError):
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
