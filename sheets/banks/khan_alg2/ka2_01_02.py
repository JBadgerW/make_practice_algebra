"""Khan Algebra 2, Lesson 1-2: Average rate of change of polynomials, from the
old app's Alg2_01_02 (sixteen of Khan's, without answers; each "which
interval" has exactly one right choice).

Khan's functions: x^3 - k x, (t + h)^2 + k, -(t - h)^2 + k, x^2 + c,
x^2 - x - c, -x^2/4 + c, x^3/8 - x^2 (each drawn with new numbers). Type 1:
the average rate of change over an interval, written [1, 6] or
-5 <= t <= -1. Type 2: over which of four intervals is it positive
(negative, zero)? Exactly one.

A problem: dict(type, prompt, interval or (ask, choices), answer, source).
    Type 1  prompt "f(x) = x^3 - 9 x", interval [1, 6], answer "34"
    Type 2  ask "positive", choices [[-4, -1], [-3, 3], ...], answer "C"
check() computes (f(b) - f(a))/(b - a) exactly.
"""
import sympy as sp
from ... import gen
from ...gen import need, signed
from ...linear import exact
from ...typmath import display, dfrac, text as plain, tx
from . import courses

NAME = FAMILY = "ka2_01_02"
FIXED = False
TITLE = "Lesson 1-2: Average rate of change of polynomials"
INSTRUCTIONS = ""
COURSES = courses(1)
SIGN = {"positive": lambda v: v > 0, "negative": lambda v: v < 0, "zero": lambda v: v == 0}

TYPES = [
    dict(key="1", title="Over an Interval", instructions="Find each average rate of change.",
         look="A function and an interval [a, b].",
         move="Average rate of change = (f(b) - f(a))/(b - a): the change in output over the change in input."),
    dict(key="2", title="Which Interval?", instructions="Choose 1 answer.",
         look="A function and four intervals: on which is the average rate of change positive (negative, zero)?",
         move="Find f at both ends of each interval. Positive if the output goes up, negative if down, zero if the ends match."),
]
T = gen.Types(TYPES, "", space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], str(p.get("interval") or p.get("choices")))

def function(r):
    f, v = r.choice("fgh"), r.choice("xt")
    k, h, c = r.choice((1, 4, 9, 16)), signed(r, 1, 4), r.randint(1, 10)
    sh = f"({v} {'+' if h > 0 else '-'} {abs(h)})^2"
    body = r.choice([f"{v}^3 - {k} {v}", f"{sh} + {c}", f"-{sh} + {c}", f"{v}^2 + {c}", f"{v}^2 - {v} - {c}",
                     f"-{v}^2/4 + {c}", f"{v}^3/8 - {v}^2"])
    return f"{f}({v}) = {body}"

def rate(prompt, a, b):
    f, _, body = prompt.partition("=")
    v = sp.Symbol(f[f.index("(") + 1])
    e = exact(body)
    return (e.subs(v, b) - e.subs(v, a)) / (b - a)

def interval(r):
    a = r.randint(-6, 4)
    return [a, min(8, a + r.randint(1, 6))]          # Khan's: [1, 6], -5 <= t <= -1

def written_interval(iv, v, brackets):
    a, b = iv
    return f"[{a}, {b}]" if brackets else f"{a} <= {v} <= {b}"

def draw(entry, r, tpl):
    prompt = function(r)
    if entry == "1":
        iv = interval(r)
        return dict(prompt=prompt, interval=iv, brackets=r.random() < 0.5, answer=tx(rate(prompt, *iv)))
    ask = r.choice(list(SIGN))
    pool = [interval(r) for _ in range(60)]
    yes = [iv for iv in pool if SIGN[ask](rate(prompt, *iv))]
    no = [iv for iv in pool if not SIGN[ask](rate(prompt, *iv))]
    need(yes and len({tuple(i) for i in no}) >= 3)
    key = lambda iv: f"{iv[0]},{iv[1]}"                # a choice as a string: lettered() reads a tuple as several
    wrong = list(dict.fromkeys(key(i) for i in no))[:3]
    choices, letter = gen.lettered(r, key(yes[0]), wrong)
    return dict(prompt=prompt, ask=ask, brackets=r.random() < 0.5,
                choices=[[int(x) for x in c.split(",")] for c in choices], answer=letter)

def check(p):
    try:
        if p["type"] == "1":
            return "checked" if exact(p["answer"]) == rate(p["prompt"], *p["interval"]) else "failed"
        right = [gen.ABC[i] for i, iv in enumerate(p["choices"]) if SIGN[p["ask"]](rate(p["prompt"], *iv))]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def letters(p):
    f = p["prompt"].split("(")[0]
    return f, p["prompt"][len(f) + 1]

def typst(p, gap="0.3em"):
    f, v = letters(p)
    if p["type"] == "1":
        return (f"{display(dfrac(p['prompt']))} \\\n    What is the average rate of change of ${f}$ over the interval "
                f"${written_interval(p['interval'], v, p['brackets'])}$?")
    words = {"zero": "an average rate of change of zero", "positive": "a positive average rate of change",
             "negative": "a negative average rate of change"}[p["ask"]]
    items = [f"${written_interval(iv, v, p['brackets'])}$" for iv in p["choices"]]
    return (f"{display(dfrac(p['prompt']))} \\\n    Over which interval does ${f}$ have {words}? \\\n    "
            f"{gen.choices_typst(items, 'grid')}")

def answer_typst(p):
    if p["type"] == "1":
        return display(dfrac(p["answer"]))
    a = gen.letters_of(p["answer"])[0]
    f, v = letters(p)
    return f"{a}. ${written_interval(p['choices'][gen.ABC.index(a)], v, p['brackets'])}$"

def text(p):
    f, v = letters(p)
    if p["type"] == "1":
        return f"{plain(p['prompt'])}  over {written_interval(p['interval'], v, True)}"
    return f"{plain(p['prompt'])}  {p['ask']}?  " + gen.choices_text([str(c) for c in p["choices"]])

def answer_text(p):
    return plain(p["answer"]) if p["type"] == "1" else f"{p['answer']}. {gen.chosen(p)[0]}"

def height(p):
    return 0.6 if p["type"] == "1" else 1.2

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    new = dict(old, prompt=t, source="edited")
    try:
        if old["type"] == "1":
            new["answer"] = tx(rate(t, *old["interval"]))
        else:
            new["answer"] = ", ".join(gen.ABC[i] for i, iv in enumerate(old["choices"]) if SIGN[old["ask"]](rate(t, *iv))) or old["answer"]
    except Exception:
        raise ValueError("write a function like f(x) = x^3 - 9 x") from None
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "2":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
