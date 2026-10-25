"""Khan Algebra 1, Lesson 11-2: Powers of products & quotients (integer
exponents), from the old app's Alg1_11_02 (nineteen of Khan's, without
answers; each has exactly one right choice).

Select the expression equivalent to (3^(-8) · 7^3)^(-2) or (b^7/4^5)^(-3).
Bases are 2 to 9 or letters; inner exponents -10 to 10, outer -9 to 9 (not
-1 to 1). The right choice is written with negative exponents
(3^16 · 7^(-6)) or as a fraction with positive ones (3^16/7^6). The wrong
ones are Khan's mistakes: exponents added instead of multiplied
(8^9 for (a^(-2) · 8^7)^2's 8^14), the outer power on the first factor
only, and every sign flipped (the reciprocal).

A problem: dict(type, prompt, choices, answer, source), Typst math with
* for a product (shown as a dot).
    prompt   "(3^(-8) * 7^3)^(-2)"
    choices  ["7^6/3^16", "3^16 * 7^(-6)", "3^(-6) * 7^1"]
    answer   "B"
check() compares every choice with the prompt exactly (their ratio
simplifies to 1): exactly one is equal, and it's the answer's.
"""
from ... import gen
from ...gen import need, signed, signed_except
from ...check import same_power
from ...typmath import display, dfrac, fr, text as plain
from ..adv_exponents import pw, raised
from . import courses

NAME = FAMILY = "ka1_11_02"
FIXED = False
TITLE = "Lesson 11-2: Powers of products & quotients (integer exponents)"
INSTRUCTIONS = "Select the equivalent expression."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Power of a Product",
         look="A product of powers, raised to a power: (a^m · b^n)^k.",
         move="Raise each factor to the outside power by multiplying exponents: a^(m k) · b^(n k). "
              "A negative exponent means the factor belongs on the other side of a fraction bar."),
    dict(key="2", title="Power of a Quotient",
         look="A quotient of powers, raised to a power: (a^m / b^n)^k.",
         move="Raise the top and the bottom to the outside power by multiplying exponents. "
              "Then move any factor with a negative exponent across the fraction bar."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Writing a product of powers, {base: exponent}, two ways
# ------------------------------------------------------------------
def product(powers):
    """With negative exponents: "3^16 * 7^(-6)"."""
    return " * ".join(pw(b, e) for b, e in powers if e)

def fraction(powers):
    """Positive exponents only: "3^16/7^6", "1/(3^9 * 6^18)", "a^63 * b^18"."""
    top = " * ".join(pw(b, e) for b, e in powers if e > 0)
    bottom = " * ".join(pw(b, -e) for b, e in powers if e < 0)
    if not bottom:
        return top
    return fr(top or "1", bottom)

def write(r, powers):
    return r.choice((product, fraction))(powers)

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def bases(r):
    pool = [str(n) for n in range(2, 10)] + list(gen.LETTERS)
    a, b = r.sample(pool, 2)
    need(not (a.isdigit() and b.isdigit() and (int(a) % int(b) == 0 or int(b) % int(a) == 0)))   # 2 and 4: one base in disguise
    return a, b

def draw(entry, r, tpl):
    a, b = bases(r)
    p, q, k = signed(r, 2, 10), signed(r, 2, 10), signed_except(r, 2, 9)
    if entry == "1":
        prompt = raised(f"{pw(a, p)} * {pw(b, q)}", k)
        q_ = q                                     # b's exponent as a factor of the product
    else:
        prompt = raised(fr(pw(a, p), pw(b, q)), k)
        q_ = -q
    right = [(a, p * k), (b, q_ * k)]
    wrong = [[(a, p + k), (b, q_ + k)],             # added instead of multiplied
             [(a, p * k), (b, q_)],                  # the outer power on the first factor only
             [(a, -p * k), (b, -q_ * k)]]            # every sign flipped
    r.shuffle(wrong)
    need(all(any(e for _, e in w) for w in wrong[:2]))        # (s^(-2) q^(-2))^2 "added" is s^0 q^0: nothing to write
    choices, letter = gen.lettered(r, write(r, right), [write(r, w) for w in wrong[:2]])
    return dict(prompt=prompt, choices=choices, answer=letter)

def equal(a, b):
    """Exactly (at random points, 9^(-40) is too close to 0 to tell from anything else)."""
    return same_power(a.replace("*", ""), b.replace("*", ""))

def check(p):
    try:
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if equal(p["prompt"], c)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def math(t):
    return display(dfrac(t.replace("*", "dot")))

def typst(p, gap="0.3em"):
    return f"{math(p['prompt'])} \\\n    {gen.choices_typst([math(c) for c in p['choices']])}"

def answer_typst(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {math(p['choices'][gen.ABC.index(a)])}"

def text(p):
    star = lambda t: plain(t.replace("*", "·"))
    return star(p["prompt"]) + "      " + gen.choices_text(p["choices"], star)

def answer_text(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {plain(p['choices'][gen.ABC.index(a)].replace('*', '·'))}"

def height(p):
    return 1.2

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").replace("·", "*").split())
    new = dict(old, prompt=t, source="edited")
    right = [gen.ABC[i] for i, c in enumerate(old["choices"]) if equal(t, c)]
    new["answer"] = ", ".join(right) or old["answer"]
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
