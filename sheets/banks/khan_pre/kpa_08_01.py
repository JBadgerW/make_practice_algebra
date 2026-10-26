"""Khan Prealgebra, Lesson 8-1: Equivalent expressions with percent
problems, from the old app's PreAlg_08_01 (ten generated stories). The old
haircut story keyed both 1/3 h and 0.33 h as right for 33%, which aren't
equal, and its decimals came from floating point (1 - 0.7 can print as
0.30000000000000004); the percents here are exact, and 33% is not used.

A quantity goes up by p%, down by p%, or becomes p% of itself: which two
expressions could represent the new amount? Choose 2 of five. The right
ones are Khan's forms: 1.15 v, v + 15/100 v, 115/100 v, v (1 + 0.15)
(and 0.85 v, v - 15/100 v, ... going down; 0.75 h, 3/4 h for 75% of). The
wrong ones are Khan's misreadings: 15 v, v + 15, v + 0.15, 0.15 v,
15 v + v, the other direction. Names only, no pronouns.

A problem: dict(type, story, v, p, change, prompt, choices, answer, source).
    v "f", p 15, change "more"    choices ["$1.15 f$", "$15 f$", ...]    answer "A, D"
check() evaluates every choice against (1 + p/100) v (or 1 - p/100, or
p/100) at random values of v: exactly the answer's are equal.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...check import same_value
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "kpa_08_01"
FIXED = False
TITLE = "Lesson 8-1: Equivalent expressions with percent problems"
INSTRUCTIONS = "Choose 2 answers."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Percent Change Expressions",
         look="A quantity v that goes up or down by a percent (or becomes a percent of itself), and five expressions.",
         move="p% more is v + (p/100) v = (1 + p/100) v; p% less is (1 - p/100) v; p% of v is (p/100) v. "
              "Two of the choices are the same amount written two ways.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

# story: (letter, change, percents, the story with {p} and {name}, the question)
STORIES = {
    "snow": ("f", "more", range(10, 70, 10),
             "In March, {name}'s house had {p}% more snowfall than in February, when it had $f$ centimeters.",
             "Which expressions could represent the snowfall in March?"),
    "hospital": ("m", "more", range(20, 90, 10),
                 "After an outbreak of a mysterious disease, the average wait time at a hospital went up by {p}%. "
                 "Before the outbreak, the average wait was $m$ minutes.",
                 "Which expressions could represent the average wait time after the outbreak?"),
    "beach": ("L", "less", range(5, 50, 5),
              "{name} spent $L$ hours at the beach last weekend. {other} spent {p}% fewer hours at the beach than {name}.",
              "Which expressions could represent how many hours {other} spent at the beach?"),
    "flying": ("m", "less", (25, 75),
               "After learning how to fly, {name} cut a daily commute by {p}%. The commute used to take $m$ minutes.",
               "Which expressions could represent {name}'s commute time, in minutes, now?"),
    "ring": ("H", "more", (10, 20, 30, 40, 60, 70, 80, 90),
             "A magic ring makes {name}'s healing spell {p}% stronger. Without the ring, the spell restores $H$ "
             "health points.", "Which expressions could represent the health points restored with the ring?"),
    "weather": ("T", "more", range(1, 10),
                "Last Sunday's average temperature was {p}% higher than the Sunday before, when it was $T$ degrees Celsius.",
                "Which expressions could represent last Sunday's average temperature?"),
    "soup": ("x", "less", (25, 30, 40, 60, 70, 75),
             "A new soup recipe has {p}% less sodium per serving than the old one, which had $x$ milligrams.",
             "Which expressions could represent the sodium per serving, in milligrams, in the new recipe?"),
    "haircut": ("h", "of", (10, 20, 25, 30, 40, 60, 70, 75, 80, 90),
                "On Monday, {name}'s hair was $h$ centimeters long. After a haircut on Tuesday, it was only {p}% of "
                "that length.", "Which expressions could represent the length of {name}'s hair after the haircut?"),
    "menu": ("D", "more", range(10, 45, 5),
             "Crispy Clover, a vegetarian restaurant, has a new menu with {p}% more dishes than the old menu, which "
             "had $D$ dishes.", "Which expressions could represent the number of dishes on the new menu?"),
    "game": ("B", "less", range(10, 31),
             "A power-up in {name}'s video game costs {p}% less this week. Last week it cost $B$ coins.",
             "Which expressions could represent the cost this week, in coins?"),
}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def dec(q):
    """An exact decimal: 1.15, 0.3, 0.05."""
    s = f"{float(q):.4f}".rstrip("0").rstrip(".")
    assert F(s) == q
    return s

def fr(q):
    return f"{q.numerator}/{q.denominator}"

def forms(v, p, change):
    """(right forms, wrong forms) in Typst math."""
    k = F(p, 100)
    if change == "of":
        right = [f"{dec(k)} {v}", f"{fr(k)} {v}", f"{p}/100 {v}"]
        wrong = [f"{dec(1 - k)} {v}", f"{v} - {dec(k)}", f"{dec(1 + k)} {v}", f"{v} (1 - {dec(k)})", f"{p} {v}"]
        return right, wrong
    s, o = ("+", "-") if change == "more" else ("-", "+")
    m = 1 + k if change == "more" else 1 - k
    right = [f"{dec(m)} {v}", f"{v} {s} {p}/100 {v}", f"{100 + p if change == 'more' else 100 - p}/100 {v}",
             f"{v} (1 {s} {dec(k)})"]
    wrong = [f"{p} {v}", f"{v} {s} {p}", f"{v} {s} {dec(k)}", f"{dec(k)} {v}", f"{dec(1 - k if change == 'more' else 1 + k)} {v}",
             f"{v} {s} 1/{p} {v}"]
    if change == "more":
        wrong.append(f"{p} {v} + {v}")
    return right, wrong

def value_of(v, p, change):
    k = F(p, 100)
    return f"{dec({'more': 1 + k, 'less': 1 - k, 'of': k}[change])} {v}"

def draw(entry, r, tpl):
    story = r.choice(list(STORIES))
    v, change, percents, words, question = STORIES[story]
    p = r.choice(list(percents))
    name, other = r.sample(gen.NAMES, 2)
    right, wrong = forms(v, p, change)
    right = r.sample(right, 2)
    wrong = [w for w in dict.fromkeys(wrong) if not same_value(w, right[0])]
    need(len(wrong) >= 3)
    choices, answer = gen.lettered(r, right, r.sample(wrong, 3))
    fill = lambda t: t.format(p=p, name=name, other=other)
    return dict(story=story, v=v, p=p, change=change, prompt=f"{fill(words)} {fill(question)}",
                choices=[f"${c}$" for c in choices], answer=answer)

def check(p):
    try:
        target = value_of(p["v"], p["p"], p["change"])
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if same_value(c.strip("$"), target)]
        ok = right == gen.letters_of(p["answer"]) and len(right) == 2 and f"{p['p']}%" in p["prompt"]
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    items = [display(dfrac(c.strip("$"))) for c in p["choices"]]
    return f"{p['prompt']} \\\n    {gen.choices_typst(items, 'linear')}"

def answer_typst(p):
    return "; ".join(f"{a}. {display(dfrac(c.strip('$')))}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def text(p):
    return p["prompt"].replace("$", "") + "   " + gen.choices_text(p["choices"], lambda c: plain(c.strip("$")))

def answer_text(p):
    return "; ".join(f"{a}. {plain(c.strip('$'))}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def height(p):
    return 1.1

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
