"""Khan Algebra 1, Lesson 8-9: Identifying values in the domain, from the old
app's Alg1_08_09 (twelve of Khan's, without answers).

For each of three x-values, is it in the domain of f? Khan's functions are
rational (excluding a number), square roots (from a boundary on), and
polynomials (every number); the three values always include the special
number, one more on each side where there is one. One type, the kinds
mixed: a header naming the kind would give the answer away.

A problem: dict(type, prompt, answer, source).
    prompt  "f(x) = (x - 3)/(x + 2) ; -2, 0, 3"
    answer  "in the domain: 0, 3; not in the domain: -2"
check() computes the domain with sympy and tests each value.
"""
import re
from ... import gen
from ...gen import need
from ...linear import exact
from ...typst import esc
from ...typmath import display, dfrac, text as plain, tx
from . import courses
from .domains import function, domain

NAME = FAMILY = "ka1_08_09"
FIXED = False
TITLE = "Lesson 8-9: Identifying values in the domain"
INSTRUCTIONS = "Determine for each x-value whether it is in the domain of the function or not."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="In the Domain or Not?",
         look="A function and three x-values.",
         move="Put each value in. If it makes a denominator 0, or the inside of a square root negative, it isn't in the domain."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def parts(prompt):
    definition, _, xs = prompt.partition(";")
    f, _, body = definition.partition("=")
    return f.strip(), body.strip(), [x.strip() for x in xs.split(",")]

def answer_of(prompt):
    f, body, xs = parts(prompt)
    d = domain(body)
    ins = [x for x in xs if d.contains(exact(x))]
    outs = [x for x in xs if not d.contains(exact(x))]
    return f"in the domain: {', '.join(ins) or 'none'}; not in the domain: {', '.join(outs) or 'none'}"

def draw(entry, r, tpl):
    body, s, kind = function(r)
    need(s.is_integer)
    xs = sorted({int(s), int(s) - r.randint(1, 6), int(s) + r.randint(1, 6), r.randint(-10, 10)})
    xs = sorted(r.sample(xs[1:-1] + [xs[0], xs[-1]], 3)) if len(xs) > 3 else xs
    need(len(xs) == 3 and int(s) in xs)
    prompt = f"{r.choice('fgh')}(x) = {body} ; {', '.join(map(str, xs))}"
    return dict(prompt=prompt, answer=answer_of(prompt))

ANSWER = re.compile(r"in the domain: (.*); not in the domain: (.*)")

def check(p):
    try:
        f, body, xs = parts(p["prompt"])
        m = ANSWER.fullmatch(" ".join(p["answer"].replace("−", "-").split()))
        ins, outs = ([x.strip() for x in g.split(",") if x.strip() not in ("", "none")] for g in m.groups())
        d = domain(body)
        ok = sorted(ins + outs) == sorted(xs) and all(d.contains(exact(x)) for x in ins) and \
            not any(d.contains(exact(x)) for x in outs)
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    f, body, xs = parts(p["prompt"])
    rows = ", ".join(f"[${x}$], [], []" for x in xs)
    return (f"{display(dfrac(f'{f} = {body}'))} \\\n    #table(columns: 3, inset: 5pt, align: center, "
            f"[], [In domain], [Not in domain], {rows})")

def answer_typst(p):
    return esc(p["answer"]).replace("-", "−")

def text(p):
    f, body, xs = parts(p["prompt"])
    return f"{plain(f + ' = ' + body)}:  {', '.join(plain(x) for x in xs)}?"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 1.4

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "f(x) = (x - 3)/(x + 2) ; -2, 0, 3", "in the domain: 0, 3; not in the domain: -2")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
