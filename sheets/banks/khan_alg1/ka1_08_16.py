"""Khan Algebra 1, Lesson 8-16: Positive and negative intervals, from the old
app's Alg1_08_16 (eighteen of Khan's graphs as screenshots, without
answers).

Select the interval where f(x) > 0 (or "f is positive", f(x) < 0, "f is
negative"): three intervals one unit long, a < x < a + 1, in order, as
Khan's; exactly one has the asked sign all the way across. The others have
the other sign or cross zero. The curve is smooth (curves.py), its
crossings exactly known.

A problem: dict(type, ks, letter, ask, wording, choices, answer, source).
    ks  the knots    ask 1 (positive) or -1    choices [[-2, -1], [1, 2], [4, 5]]    answer "B"
check() finds the sign of the curve on each interval (curves.sign_on, which
knows where it crosses zero): exactly the answer's has the asked sign.
"""
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from . import courses
from . import curves

NAME = FAMILY = "ka1_08_16"
FIXED = False
TITLE = "Lesson 8-16: Positive and negative intervals"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Where Is It Positive or Negative?",
         look="The graph of a function and three intervals.",
         move="Positive means above the x-axis; negative, below. The graph must stay on that side for the whole "
              "interval, without crossing.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, str(p["ks"]), p["ask"], str(p["choices"]))

def asked(letter, ask, wording):
    if wording == 0:
        return f"${letter}(x) {'>' if ask > 0 else '<'} 0$"
    return f"${letter}$ is {'positive' if ask > 0 else 'negative'}"

def draw(entry, r, tpl):
    ks = curves.knots(r, -7, 7, -5, 5, gap=(2, 3))
    ask = r.choice((1, -1))
    spans = [(a, a + 1) for a in range(-7, 7)]
    right = [s for s in spans if curves.sign_on(ks, *s) == ask]
    wrong = [s for s in spans if curves.sign_on(ks, *s) != ask]
    need(right and len(wrong) >= 2)
    chosen = sorted([r.choice(right)] + r.sample(wrong, 2))
    choices = [list(s) for s in chosen]
    good = [c for c in choices if curves.sign_on(ks, *c) == ask]
    choices, answer = gen.in_order(choices, good)
    return dict(ks=[list(k) for k in ks], letter=r.choice("fgh"), ask=ask, wording=r.randint(0, 1),
                choices=choices, answer=answer)

def check(p):
    try:
        ks = [tuple(k) for k in p["ks"]]
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if curves.sign_on(ks, *c) == p["ask"]]
        return "checked" if right == gen.letters_of(p["answer"]) and len(right) == 1 else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p):
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    curves.draw(g, [tuple(k) for k in p["ks"]], ends="closed")
    g.label_at(p["ks"][-1][0], p["ks"][-1][1], f"$y = {p['letter']}(x)$", anchor="south-east", color="blue", size=7)
    return g.typst()

def interval(c):
    return f"${c[0]} < x < {c[1]}$"

def typst(p, gap="0.3em"):
    q = f"Select the interval where {asked(p['letter'], p['ask'], p['wording'])}."
    left = f"{q} #v(0.3em) {gen.choices_typst([interval(c) for c in p['choices']])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return "; ".join(f"{a}. {interval(p['choices'][gen.ABC.index(a)])}" for a in gen.letters_of(p["answer"]))

def text(p):
    return (f"{asked(p['letter'], p['ask'], p['wording']).replace('$', '')}: knots {p['ks']}   "
            + gen.choices_text([interval(c).replace("$", "") for c in p["choices"]]))

def answer_text(p):
    return answer_typst(p).replace("$", "")

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
