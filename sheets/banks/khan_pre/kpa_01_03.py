"""Khan Prealgebra, Lesson 1-3: Relate factors and multiples, from the old
app's PreAlg_01_03 (twenty-one of Khan's, without answers; the old hundred
charts lost the numbers in their choices).

Type 1: we know 9 × 2 = 18; which statements are also true? Choose 2 of
Khan's three: "18 is a multiple of 2", "9 is a factor of 18", and one
false ("18 is a factor of 9", "5 is a multiple of 8"). Type 2: what set is
shaded on the hundred chart, the factors of n or the multiples of k?
Choose 1 of four. Type 3: a student tried to shade the multiples of k (or
the factors of n) and made Khan's mistakes: the multiples of 9 for 3, the
factors instead of the multiples, k left out, only the factors of 25 for
50. Which mistake? One choice states a false rule ("multiples are always
greater than the number"), as Khan's do. Names only, no pronouns.

A problem: dict(type, ..., choices, answer, source).
    Type 1  a 9, b 2
    Types 2, 3  shaded [7, 14, ...]; Type 3 adds name, goal ("multiples", 3)
check(): Type 1 tests each statement by dividing; Types 2 and 3 read the
set each choice describes and compare it with the shaded numbers: exactly
the answer's matches.
"""
import re
from ... import gen
from ...gen import need
from . import courses
from .numbers import factors, multiples, PREAMBLE, hundred_chart

NAME = FAMILY = "kpa_01_03"
FIXED = False
TITLE = "Lesson 1-3: Relate factors and multiples"
INSTRUCTIONS = ""
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Factors and Multiples from a Product", instructions="Choose 2 answers.",
         look="A multiplication fact and three statements.",
         move="In a × b = n, a and b are factors of n, and n is a multiple of a and of b."),
    dict(key="2", title="What Is Shaded?", instructions="Choose 1 answer.",
         look="A hundred chart with some numbers shaded.",
         move="Factors of n divide n: few, all at most n. Multiples of k are k, 2k, 3k, ...: they go on to 100.",
         width="full"),
    dict(key="3", title="Find the Mistake", instructions="Choose 1 answer.",
         look="A student's hundred chart, meant to show the multiples of k or the factors of n.",
         move="Work out what should be shaded, compare, and name the difference.", width="full"),
]
T = gen.Types(TYPES, "", space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p.get("a"), p.get("b"), str(p.get("shaded")), str(p.get("goal")))

# ------------------------------------------------------------------
# Type 1
# ------------------------------------------------------------------
STATEMENT = re.compile(r"(\d+) is a (multiple|factor) of (\d+)\.")

def true_statement(s):
    x, kind, y = STATEMENT.fullmatch(s).groups()
    x, y = int(x), int(y)
    return x % y == 0 if kind == "multiple" else y % x == 0

def products(r):
    a, b = r.sample(range(2, 10), 2)
    n = a * b
    true = [f"{n} is a multiple of {a}.", f"{n} is a multiple of {b}.", f"{a} is a factor of {n}.", f"{b} is a factor of {n}."]
    false = [s for s in (f"{n} is a factor of {a}.", f"{a} is a multiple of {n}.", f"{b} is a multiple of {a}.",
                         f"{a} is a factor of {b}.") if not true_statement(s)]
    choices, answer = gen.lettered(r, r.sample(true, 2), [r.choice(false)])
    return dict(a=a, b=b, choices=choices, answer=answer)

# ------------------------------------------------------------------
# Types 2 and 3: a choice names a set; read it back from the words
# ------------------------------------------------------------------
def only(kind, x):
    return f"Only the {kind} of {x}"

SETS = [
    (re.compile(r"Only the factors of (\d+)$"), lambda m: factors(int(m[0]))),
    (re.compile(r"Only the multiples of (\d+)$"), lambda m: multiples(int(m[0]))),
    (re.compile(r"shaded the multiples of (\d+) instead of the multiples of \d+\.$"), lambda m: multiples(int(m[0]))),
    (re.compile(r"shaded the factors instead of the multiples of (\d+)\.$"), lambda m: factors(int(m[0]))),
    (re.compile(r"didn't shade (\d+)\.$"), lambda m: multiples(int(m[0])) - {int(m[0])}),
    (re.compile(r"shaded the multiples instead of the factors of (\d+)\.$"), lambda m: multiples(int(m[0]))),
    (re.compile(r"shaded only the factors of (\d+) instead of all the factors of \d+\.$"), lambda m: factors(int(m[0]))),
]

def described(c):
    """The set of numbers a choice says was shaded, or None (a false rule)."""
    for pattern, make in SETS:
        m = pattern.search(c)
        if m:
            return make(m.groups())
    return None

def which_set(r):
    if r.random() < 0.5:
        k = r.randint(3, 12)
        shaded = multiples(k)
        options = [only("factors", k), only("factors", k * r.randint(2, 4)), only("multiples", k * 2),
                   only("multiples", max(d for d in factors(k) if d < k) if len(factors(k)) > 2 else k + 1)]
        right = only("multiples", k)
    else:
        n = r.choice([m for m in range(12, 100) if len(factors(m)) >= 4])
        shaded = factors(n)
        options = [only("multiples", n), only("factors", 2 * n if 2 * n <= 100 else n // 2),
                   only("multiples", min(factors(n) - {1})), only("factors", n + r.choice((-1, 1)))]
        right = only("factors", n)
    wrong = [o for o in dict.fromkeys(options) if described(o) != shaded and o != right]
    need(len(wrong) >= 3)
    choices, answer = gen.lettered(r, right, r.sample(wrong, 3))
    return dict(shaded=sorted(shaded), choices=choices, answer=answer)

def mistake(r):
    name = r.choice(gen.NAMES)
    if r.random() < 0.5:
        k = r.randint(3, 9)
        goal = ["multiples", k]
        m = k * r.randint(2, 3)
        kinds = {f"{name} shaded the multiples of {m} instead of the multiples of {k}.": multiples(m),
                 f"{name} shaded the factors instead of the multiples of {k}.": factors(k),
                 f"{name} didn't shade {k}.": multiples(k) - {k}}
        rule = f"{name} shaded {k}, but multiples are always greater than the number."
    else:
        n = r.choice([m for m in range(12, 34) if len(factors(m)) >= 4])      # its multiples fill a few rows
        goal = ["factors", n]
        d = r.choice(sorted(factors(n) - {1, n}))
        need(len(factors(d)) >= 2)
        kinds = {f"{name} shaded the multiples instead of the factors of {n}.": multiples(n),
                 f"{name} shaded only the factors of {d} instead of all the factors of {n}.": factors(d)}
        rule = f"{name} shaded {n}, but factors are always less than the number."
    right = r.choice(list(kinds))
    shaded = kinds[right]
    wrong = [c for c in kinds if c != right and kinds[c] != shaded] + [rule]
    need(len(wrong) >= 2)
    choices, answer = gen.lettered(r, right, r.sample(wrong, 2))
    return dict(name=name, goal=goal, shaded=sorted(shaded), choices=choices, answer=answer)

def draw(entry, r, tpl):
    return {"1": products, "2": which_set, "3": mistake}[entry](r)

def check(p):
    try:
        if p["type"] == "1":
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if true_statement(c)]
            ok = right == gen.letters_of(p["answer"]) and f"{p['a'] * p['b']}" in " ".join(p["choices"])
            return "checked" if ok else "failed"
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if described(c) == set(p["shaded"])]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def math(t):
    return re.sub(r"\d+", lambda m: f"${m[0]}$", t)

def typst(p, gap="0.3em"):
    if p["type"] == "1":
        a, b = p["a"], p["b"]
        return (f"We know ${a} times {b} = {a * b}$. Which of the following statements are also true? \\\n    "
                f"{gen.choices_typst([math(c) for c in p['choices']])}")
    if p["type"] == "2":
        q = "What set of numbers is shaded on the hundred chart?"
    else:
        kind, x = p["goal"]
        q = (f"{p['name']} tried to shade all the {kind} of ${x}$ on the hundred chart, but made a mistake. "
             f"What mistake did {p['name']} make?")
    return (f"#grid(columns: (auto, 1fr), column-gutter: 1.2em, [{hundred_chart(p['shaded'])}], "
            f"[{q} #v(0.3em) {gen.choices_typst([math(c) for c in p['choices']])}])")

def answer_typst(p):
    return math(gen.choice_answer_typst(p))

def text(p):
    head = f"{p['a']} × {p['b']} = {p['a'] * p['b']}" if p["type"] == "1" else f"shaded {p['shaded']}"
    return head + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.3 if p["type"] == "1" else 2.9

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new problem; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
