"""Khan Algebra 1, Lesson 11-3: Properties of exponents challenge (integer
exponents), from the old app's Alg1_11_03 (twelve of Khan's, without
answers; each "choose 2" has exactly two right, and the three mistakes are
in step 3, nowhere, and step 2).

Type 1: which two of four expressions equal 7 · 7 · 7 · 7 · 7 · 7, or
4^(-3)/4^(-1), or 4^(-2) · 7^(-2)? The right ones rewrite it by a rule
(7^8/7^2, (7^2)^3, 1/28^2); the wrong ones break a rule the way students do
(exponents added for a power of a power, multiplied for a product, the
bases multiplied, an exponent off by one).

Type 2: a three-step rewrite, with at most one step wrong; which step?
After a wrong step, the later steps follow correctly from it, as Khan's do.

A problem: dict(type, prompt, choices, answer, source); Type 2 adds name
and steps. Typst math with * for a product.
    Type 1  prompt "7 * 7 * 7 * 7 * 7 * 7", choices four expressions, answer "A, C"
    Type 2  prompt "(4^(-3) * 2^(-3))^0", steps ["(8^(-3))^0", "8^0", "0"],
            choices the four statements, answer "D"
check() compares values exactly (check.same_power): Type 1, the choices
equal to the prompt; Type 2, the first step that isn't equal to the one before.
"""
from ... import gen
from ...gen import need, signed, signed_except
from ...check import same_power
from ...typst import esc
from ...typmath import display, dfrac, fr, text as plain
from ..adv_exponents import pw, raised
from . import courses

NAME = FAMILY = "ka1_11_03"
FIXED = False
TITLE = "Lesson 11-3: Properties of exponents challenge (integer exponents)"
INSTRUCTIONS = ""                       # each type has its own
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Equivalent Expressions", instructions="Which expressions are equivalent? Choose 2.",
         look="One expression, and four rewritings of it.",
         move="Write the expression as one power of one base. Do the same with each choice, using the rules: "
              "add exponents to multiply, subtract to divide, multiply for a power of a power."),
    dict(key="2", title="Find the Mistake", instructions="Did the student make a mistake? If so, in which step?",
         look="A rewrite in three steps.",
         move="Check each step against the one before. The first step that changes the value is the mistake."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], tuple(p.get("steps", ())))

def equal(a, b):
    return same_power(a, b)

# ------------------------------------------------------------------
# Type 1: one base b to the n, written several ways
# ------------------------------------------------------------------
def factors(n):
    """Pairs (s, t), s t = n, neither 1 nor -1."""
    return [(s, n // s) for s in range(-abs(n), abs(n) + 1) if s not in (0, 1, -1) and n % s == 0 and abs(n // s) != 1]

def rights(r, b, n):
    out = []
    s = signed_except(r, 1, 9, n)
    out.append(fr(pw(b, s), pw(b, s - n)))                     # 7^8/7^2
    s = signed_except(r, 1, 9, n)
    out.append(f"{pw(b, s)} * {pw(b, n - s)}")                  # 7^4 * 7^2
    if factors(n):
        s, t = r.choice(factors(n))
        out.append(raised(pw(b, s), t))                         # (7^2)^3
    if n < 0:
        out.append(fr("1", pw(b, -n)))                          # 1/5^6
    return [o for o in out if "^0" not in o]

def wrongs(r, b, n):
    out = []
    s = signed_except(r, 1, 9, n, 0)
    out.append(fr(pw(b, s), pw(b, n - s)))                      # subtracted where it adds: 7^4/7^2
    s = signed_except(r, 2, 8, n)
    if n - s not in (0, 1, -1):
        out.append(raised(pw(b, s), n - s))                     # (7^4)^2: exponents added for a power
    if factors(n):
        s, t = r.choice(factors(n))
        out.append(f"{pw(b, s)} * {pw(b, t)}")                  # 7^2 * 7^3: multiplied for a product
    out.append(f"{pw(b, n)} * {b}")                             # 7^6 * 7^1: one too many
    if b.isdigit() and int(b) <= 6:
        out.append(pw(str(int(b) ** 2), n))                     # 49^6: the bases multiplied
    if factors(-n):
        s, t = r.choice(factors(-n))
        out.append(raised(pw(b, s), t))                         # the sign lost
    return out

def t1_repeated(r):                           # 7 * 7 * 7 * 7 * 7 * 7, or 1/5 * 1/5 * 1/5
    b, n = str(r.randint(2, 9)), r.randint(3, 6)
    if r.random() < 0.3:
        return " * ".join(["1/" + b] * min(n, 5)), b, -min(n, 5)
    return " * ".join([b] * n), b, n

def t1_quotient(r):                           # 4^(-3)/4^(-1), 5^2/5^8
    b, m, k = str(r.randint(2, 9)), signed(r, 1, 9), signed(r, 1, 9)
    return fr(pw(b, m), pw(b, k)), b, m - k

def t1_product(r):                            # 5^12 * 5^8, 7^(-2) * 7^6
    b, m, k = str(r.randint(2, 9)), signed(r, 1, 12), signed(r, 1, 12)
    return f"{pw(b, m)} * {pw(b, k)}", b, m + k

def t1_two_bases(r):                          # 4^(-2) * 7^(-2), 2^5/6^5
    a, c = r.sample(range(2, 8), 2)
    e = signed(r, 2, 5)
    if r.random() < 0.5:
        prompt = f"{pw(str(a), e)} * {pw(str(c), e)}"
        right = [raised(f"{a} * {c}", e), pw(str(a * c), e)] + ([fr("1", pw(str(a * c), -e))] if e < 0 else [])
        wrong = [raised(f"{a} * {c}", 2 * e), pw(str(a * c), 2 * e), pw(str(a + c), e), fr(pw(str(a), e), pw(str(c), -e))]
    else:
        need(a % c and c % a)
        prompt = fr(pw(str(a), e), pw(str(c), e))
        right = [raised(fr(str(a), str(c)), e), f"{pw(str(a), e)} * {pw(str(c), -e)}"]
        wrong = [pw(str(a - c) if a > c else f"({a - c})", e), fr("1", str(c)), raised(fr(str(a), str(c)), 2 * e),
                 f"{pw(str(a), e)} * {pw(str(c), e)}"]
    return prompt, right, wrong

def t1(r, make):
    if make is t1_two_bases:
        prompt, right, wrong = make(r)
    else:
        prompt, b, n = make(r)
        need(abs(n) >= 2)
        right, wrong = rights(r, b, n), wrongs(r, b, n)
    right = list(dict.fromkeys(c for c in right if c != prompt))
    wrong = list(dict.fromkeys(c for c in wrong if not equal(c, prompt)))
    need(len(right) >= 2 and len(wrong) >= 2)
    r.shuffle(right), r.shuffle(wrong)
    choices, letters = gen.lettered(r, right[:2], wrong[:2])
    return dict(prompt=prompt, choices=choices, answer=letters)

# ------------------------------------------------------------------
# Type 2: three steps, at most one wrong
# ------------------------------------------------------------------
def power(b, e):
    """b^e as a step writes it, 0 and 1 included: "8^0", "4^1", "5^(-2)"."""
    return f"{b}^{e}" if e >= 0 else f"{b}^({e})"

def outer(inner, k):
    """(inner)^k, k = 0 included: "(8^(-3))^0"."""
    return f"({inner})^{k}" if k >= 0 else f"({inner})^({k})"

def last(b, n):
    """The last step: 1 for b^0, 1/b^n for a negative exponent, the number for a positive one."""
    if n > 0:
        need(int(b) ** n <= 10000)
        return str(int(b) ** n)
    return "1" if n == 0 else fr("1", power(b, -n))

def t2_same_exponent(r, wrong):               # (4^(-3) * 2^(-3))^0 = (8^(-3))^0 = 8^0 = 1
    a, c = r.sample(range(2, 7), 2)
    e, k = signed(r, 2, 5), r.choice((0, 0, 2, 3, -2))
    need(e * k <= 0)
    m = a * c if wrong != 1 else a + c                       # 1: the bases added
    n = e * k if wrong != 2 else e + k                       # 2: exponents added
    s3 = last(str(m), n) if wrong != 3 else ("0" if n == 0 else power(str(m), -n))   # 3: b^0 = 0, or the sign
    start = outer(f"{power(a, e)} * {power(c, e)}", k)
    return start, [outer(power(m, e), k), power(m, n), s3]

def t2_quotient(r, wrong):                    # 5^(-6)/5^(-4) = 5^(-6-(-4)) = 5^(-2) = 1/5^2
    b, p, q = str(r.randint(2, 9)), signed(r, 2, 9), signed(r, 2, 9)
    need(p - q < 0)
    d = p - q if wrong != 1 else p + q                       # 1: the exponents added
    s1 = f"{b}^({p} - ({q}))" if wrong != 1 else f"{b}^({p} + {q})"
    n = d if wrong != 2 else -d                              # 2: the subtraction's sign
    s3 = last(b, n) if wrong != 3 else fr("1", power(b, n)) if n != 0 else "0"
    return fr(power(b, p), power(b, q)), [s1, power(b, n), s3]

def t2_product_power(r, wrong):               # (4^(-2) * 4^(-3))^3 = (4^(-5))^3 = 4^(-15) = 1/4^15
    b, p, q, k = str(r.randint(2, 9)), signed(r, 2, 6), signed(r, 2, 6), signed(r, 2, 3)
    need((p + q) * k <= 0 and p + q != 0)
    s = p + q if wrong != 1 else p * q                       # 1: multiplied for a product
    n = s * k if wrong != 2 else s + k                       # 2: added for a power
    s3 = last(b, n) if wrong != 3 else fr("1", power(b, n)) if n != 0 else "0"
    return outer(f"{power(b, p)} * {power(b, q)}", k), [outer(power(b, s), k), power(b, n), s3]

T2 = [t2_same_exponent, t2_quotient, t2_product_power]
STATEMENTS = ["{name} did not make a mistake.", "{name} made a mistake in Step 1.",
              "{name} made a mistake in Step 2.", "{name} made a mistake in Step 3."]

def t2(r, make):
    wrong = r.randint(0, 3)
    start, steps = make(r, wrong)
    need(first_wrong(start, steps) == wrong)                 # a "mistake" that kept the value isn't one
    name = r.choice(gen.NAMES)
    return dict(prompt=start, steps=steps, name=name,
                choices=[s.format(name=name) for s in STATEMENTS], answer=gen.ABC[wrong])

def first_wrong(start, steps):
    """0 if every step equals the one before, else the number of the first that doesn't."""
    prev = start
    for i, s in enumerate(steps, 1):
        if not equal(prev, s):
            return i
        prev = s
    return 0

TEMPLATES = {"1": [lambda r, m=m: t1(r, m) for m in (t1_repeated, t1_quotient, t1_product, t1_two_bases)],
             "2": [lambda r, m=m: t2(r, m) for m in T2]}

def draw(entry, r, tpl):
    return TEMPLATES[entry][tpl](r)

def check(p):
    try:
        if p["type"] == "2":
            return "checked" if gen.ABC[first_wrong(p["prompt"], p["steps"])] == p["answer"] else "failed"
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if equal(p["prompt"], c)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def math(t):
    return display(dfrac(t.replace("*", "dot")))

def steps_typst(p):
    rows = [f"[{math(p['prompt'])}]", "[]"]
    for i, s in enumerate(p["steps"], 1):
        rows += [f"[$= {dfrac(s.replace('*', 'dot'))}$]", f"[Step {i}]"]
    return f"#grid(columns: 2, column-gutter: 2em, row-gutter: 0.8em, {', '.join(rows)})"

def typst(p, gap="0.3em"):
    if p["type"] == "2":
        return (f"{esc(p['name'])} tried to rewrite {math(p['prompt'])}. \\\n    {steps_typst(p)}\n    "
                f"{gen.choices_typst([esc(c) for c in p['choices']])}")
    return f"{math(p['prompt'])} \\\n    {gen.choices_typst([math(c) for c in p['choices']], 'grid')}"

def answer_typst(p):
    if p["type"] == "2":
        return f"{p['answer']}. {esc(p['choices'][gen.ABC.index(p['answer'])])}"
    return p["answer"]

def text(p):
    star = lambda t: plain(t.replace("*", "·"))
    if p["type"] == "2":
        return f"{p['name']}: {star(p['prompt'])} = " + " = ".join(star(s) for s in p["steps"])
    return star(p["prompt"]) + "      " + gen.choices_text(p["choices"], star)

def answer_text(p):
    if p["type"] == "2":
        return f"{p['answer']}. {p['choices'][gen.ABC.index(p['answer'])]}"
    return p["answer"]

def height(p):
    return 1.6 if p["type"] == "2" else 1.0

def edit_text(p):
    return p["prompt"] + ("" if p["type"] == "1" else " = " + " = ".join(p["steps"]))

def from_edit(t, old):
    parts = [" ".join(x.replace("−", "-").replace("·", "*").split()) for x in t.split("=")]
    if old["type"] == "2":
        if len(parts) != 4:
            raise ValueError("write the start and its three steps, separated by =")
        new = dict(old, prompt=parts[0], steps=parts[1:], answer=gen.ABC[first_wrong(parts[0], parts[1:])], source="edited")
    else:
        new = dict(old, prompt=parts[0], source="edited")
        new["answer"] = ", ".join(gen.ABC[i] for i, c in enumerate(old["choices"]) if equal(parts[0], c)) or old["answer"]
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
