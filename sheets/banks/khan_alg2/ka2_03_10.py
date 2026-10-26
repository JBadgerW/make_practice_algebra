"""Khan Algebra 2, Lesson 3-10: Finite geometric series word problems, from
the old app's Alg2_03_10 (sixteen of Khan's, without answers).

Khan's four stories, with new numbers: a monkey's swings (each arc 9/10,
4/5, 3/4, 2/3, or half the one before, or 75%), a hiking trip (90%, 2/3),
a new mall's shoppers (10% to 20% more each day), and a salary (a 2% to 5%
raise each year). Names, no pronouns (the monkey is "it").
Type 1: the total after n swings, days, or years, rounded as Khan asks (to
the meter, kilometer, shopper, or thousand dollars). Type 2: the total and
the ratio; the first term, rounded (Khan's monkey: 175 m over 4 swings at
75%, so 64 m). Type 3: which expression gives the total for the first n?
Khan's wrong choices: the first term and the ratio traded, the ratio's
complement (0.85 for 15% more, 2/3 for a third), the rate as the ratio
(0.04^n for a 4% raise), or the ratio plus 1 (4/3 for a third).

A problem: dict(type, story, name, a, r, n, prompt, answer, source); Type 2
adds shown (the total in the prompt), Type 3 choices.
    a 10   r "9/10"   n 25   answer "93"
check() recomputes from the story's numbers: Type 1, a (1 - r^n)/(1 - r)
rounded; Type 2, the shown total solved for a, rounded; Type 3, each
choice at n = 1 to 5 against the terms added up: exactly the answer's matches.
"""
import re
from fractions import Fraction as F
import sympy as sp
from ... import gen
from ...gen import need
from ...check import to_sympy
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka2_03_10"
FIXED = False
TITLE = "Lesson 3-10: Finite geometric series word problems"
INSTRUCTIONS = "Answer each question."
COURSES = courses(3)

TYPES = [
    dict(key="1", title="The Total",
         look="A first amount and a constant ratio (a fraction, or a percent more or less); the total over n.",
         move="It's a geometric series: a is the first amount, r the ratio (1.15 for 15% more, 0.9 for 90%). "
              "S_n = a (1 - r^n)/(1 - r), then round as asked.", width="full"),
    dict(key="2", title="The First Amount",
         look="The total over n and the ratio; the first amount is unknown.",
         move="Put the total, r, and n into S_n = a (1 - r^n)/(1 - r) and solve for a.", width="full"),
    dict(key="3", title="Which Expression?",
         look="A story and four expressions for the total over the first n.",
         move="The total is a (1 - r^n)/(1 - r): a the first amount, r the ratio. Check which is a and which is r.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

ORD = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"

# story: (ratios as (Typst words, ratio), first amounts, n range, rounding (places dropped), unit word)
STORIES = {
    "monkey": ([("$9/10$ the length of", "9/10"), ("$4/5$ the length of", "4/5"), ("$3/4$ the length of", "3/4"),
                ("$2/3$ the length of", "2/3"), ("half as long as", "1/2"), ("75% as long as", "0.75")],
               (8, 30), (4, 25), 0, "meter"),
    "hiking": ([("90% of", "0.9"), ("80% of", "0.8"), ("$2/3$ of", "2/3"), ("$3/4$ of", "3/4"), ("a third of", "1/3")],
               (12, 30), (3, 10), 0, "kilometer"),
    "mall": ([(f"{k}% more than", str(1 + k / 100)) for k in (5, 10, 15, 20)], (100, 200), (4, 10), 0, "whole number"),
    "salary": ([(f"a {k}% raise", f"1.0{k}") for k in (2, 3, 4, 5)], (30, 45), (5, 12), 3, "thousand dollars"),
}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def total(a, r, n):
    return a * (1 - r ** n) / (1 - r)

def rounded(x, drop):
    """x to the nearest 10^drop, half up, as a whole number."""
    unit = 10 ** drop
    return int(F(x) / unit + F(1, 2)) * unit

def money(x):
    return f"\\${x:,}"

def story_text(story, name, words, a, n, ask):
    """The story, and the question by `ask`: "total", "first", or "expression"."""
    if story == "monkey":
        first = f"On the first swing, it passes through an arc of {a} m. " if ask != "first" else ""
        intro = f"A monkey is swinging from a tree. {first}With each swing, it passes through an arc {words} the previous swing's arc."
        q = {"total": f"What is the total distance the monkey has traveled when it completes its {ORD(n)} swing?",
             "first": f"How long was the monkey's first swing?",
             "expression": "Which expression gives the total length the monkey swings in its first $n$ swings?"}
    elif story == "hiking":
        first = f"On the first day, {name} walked {a} kilometers. " if ask != "first" else ""
        after = "after that" if ask != "first" else "after the first"
        intro = f"{name} went on a hiking trip. {first}Each day {after}, {name} walked {words} the distance of the day before."
        q = {"total": f"What is the total distance {name} walked by the end of the {ORD(n)} day?",
             "first": f"How far did {name} walk on the first day?",
             "expression": f"Which expression gives the total distance {name} walked in the first $n$ days?"}
    elif story == "mall":
        if ask != "first":
            intro = (f"A new shopping mall records {a} shoppers on its first day of business. Each day after that, "
                     f"the number of shoppers is {words} the day before.")
        else:
            intro = (f"A new shopping mall is gaining in popularity. Every day since it opened, the number of "
                     f"shoppers is {words} the day before.")
        q = {"total": f"What is the total number of shoppers in the first {n} days?",
             "first": "How many shoppers were at the mall on the first day?",
             "expression": "Which expression gives the total number of shoppers in the first $n$ days?"}
    else:
        first = f"{name} earns a {money(a)} salary in the first year of a new job" if ask != "first" else \
            f"{name} has a new job"
        intro = f"{first}, with {words} each year."
        q = {"total": f"How much does {name} earn in total in the first {n} years?",
             "first": f"What was {name}'s salary in the first year?",
             "expression": f"Which expression gives the total {name} earns in the first $n$ years?"}
    return intro, q[ask]

def round_words(story):
    return f"Round your answer to the nearest {STORIES[story][4]}."

def formula(a, r):
    """a dot (1 - r^n)/(1 - r) in Typst, as Khan writes it, a fraction in parentheses."""
    A, R = [f"({t})" if "/" in str(t) else str(t) for t in (a, r)]
    return f"{A} dot (1 - {R}^n)/(1 - {R})"

def wrong_formulas(a, r, story):
    q = F(r)
    out = [formula(r, str(a))]                                     # a and r traded
    if story in ("mall", "salary"):
        p = q - 1
        out += [formula(a, str(float(1 - p))), formula(a, str(float(p)))]   # 0.85 for 1.15; 0.04 for 1.04
    else:
        c = 1 - q
        out += [formula(a, str(c) if "/" in r else str(float(c))), formula(a, str(1 + q) if "/" in r else str(float(1 + q)))]
    return out

def draw(entry, r, tpl):
    story = r.choice(list(STORIES))
    ratios, (lo, hi), (n_lo, n_hi), drop, _ = STORIES[story]
    words, rt = r.choice(ratios)
    q = F(rt)
    a = r.randint(lo, hi) * (1000 if story == "salary" else 1)
    n = r.randint(n_lo, n_hi)
    name = r.choice(gen.NAMES)
    p = dict(story=story, name=name, a=a, r=rt, n=n)
    if entry == "1":
        intro, ask = story_text(story, name, words, a, n, "total")
        return dict(p, prompt=f"{intro} {ask} {round_words(story)}", answer=f"{rounded(total(a, q, n), drop):,}")
    if entry == "2":
        n = r.randint(3, min(n_hi, 6))
        s = total(a, q, n)
        shown = rounded(s, 0) if story in ("salary", "mall") else (int(s) if s.denominator == 1 else round(float(s), 2))
        need(rounded(F(str(shown)) * (1 - q) / (1 - q ** n), drop) == a)
        intro, ask = story_text(story, name, words, a, n, "first")
        over = {"monkey": f"The total length of the arcs from its first {n} swings is {shown} m.",
                "hiking": f"{name} walked {shown} kilometers in all over {n} days.",
                "mall": f"The total number of shoppers over the first {n} days is {shown:,}.",
                "salary": f"In the first {n} years, {name} earned a total of {money(shown)}."}[story]
        return dict(p, n=n, shown=str(shown), prompt=f"{intro} {over} {ask} {round_words(story)}", answer=f"{a:,}")
    intro, ask = story_text(story, name, words, a, n, "expression")
    wrong = wrong_formulas(a, rt, story)
    choices, answer = gen.lettered(r, formula(a, rt), r.sample(wrong, 3))
    return dict(p, prompt=f"{intro} {ask}", choices=choices, answer=answer)

def matches(c, a, q):
    n = sp.Symbol("n")
    e = to_sympy(c.replace("dot", "*").replace("^n", "^(n)"))
    return all(abs(float(e.subs(n, k)) - float(total(a, q, k))) < 1e-6 * max(1, float(total(a, q, k))) for k in range(1, 6))

def check(p):
    try:
        a, q, n = p["a"], F(p["r"]), p["n"]
        drop = STORIES[p["story"]][3]
        if p["type"] == "1":
            ok = int(p["answer"].replace(",", "")) == rounded(total(a, q, n), drop)
        elif p["type"] == "2":
            got = rounded(F(p["shown"]) * (1 - q) / (1 - q ** n), drop)
            ok = int(p["answer"].replace(",", "")) == got and f"{n}" in p["prompt"]
        else:
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if matches(c, a, q)]
            ok = right == gen.letters_of(p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def commas(t):
    """Typst math: 35000 as "35,000"."""
    return re.sub(r"\b(\d{4,})\b", lambda m: f'"{int(m.group(1)):,}"', t)

def typst(p, gap="0.3em"):
    if p["type"] != "3":
        return p["prompt"]
    return f"{p['prompt']} \\\n    {gen.choices_typst([display(dfrac(commas(c))) for c in p['choices']], 'grid')}"

def answer_typst(p):
    if p["type"] == "3":
        return "; ".join(f"{x}. {display(dfrac(commas(c)))}" for x, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    return f"\\${p['answer']}" if p["story"] == "salary" else p["answer"]

def text(p):
    t = p["prompt"].replace("$", "").replace("\\", "$")
    return t if p["type"] != "3" else t + "   " + gen.choices_text(p["choices"], lambda c: plain(c).replace(" dot ", " · "))

def answer_text(p):
    return gen.choice_answer_typst(p) if p["type"] == "3" else p["answer"]

def height(p):
    return 1.0 if p["type"] != "3" else 2.0

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "3":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=t.strip().lstrip("$"))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
