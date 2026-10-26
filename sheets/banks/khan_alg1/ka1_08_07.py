"""Khan Algebra 1, Lesson 8-7: Function notation word problems, from the old
app's Alg1_08_07 (twelve generated stories). The old no. 9 drew the height
difference equal to the month difference, muddling two of its choices.

What does the statement mean? A function models a situation (P(t): people
at a beach t hours past midnight; H(t): a baby's height at t months), and a
statement uses it: P(7) = N, H(13) > H(11), T(40) = T(20) + 15. The wrong
choices are the usual misreadings: input and output traded, the two inputs
traded, or "the same" for a comparison. Names only, no pronouns.

The meaning of a sentence can't be computed, so this check is weaker than
the others: it reads the statement back out of the problem and requires
the key to be the right reading of those numbers, so a key or a statement
edited out of step is caught.

A problem: dict(type, context, name, statement, prompt, choices, answer, source).
    statement  "H(13) = 82"     (F(a) = b, F(a) > F(b), or F(a) = F(b) + d)
"""
import re
from ... import gen
from ...gen import need
from ...typst import esc
from . import courses

NAME = FAMILY = "ka1_08_07"
FIXED = False
TITLE = "Lesson 8-7: Function notation word problems"
INSTRUCTIONS = "What does each statement mean?"
COURSES = courses(8)

TYPES = [
    dict(key="1", title="An Input and Its Output",
         look="A statement like H(13) = 82: the function at one input.",
         move="The number in the parentheses is the input; the number after = is the output. Say each in the story's words."),
    dict(key="2", title="Comparing Outputs",
         look="A statement comparing the function at two inputs: H(13) > H(11), T(40) = T(20) + 15.",
         move="Each F( ) is an output at its input. Say which output is greater (or by how much), at which input.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"

# key: (F, intro, at(x), amount(y), noun, inputs, outputs, more(d) or None, differences)
CONTEXTS = {
    "beach": ("P", "P(t) models the number of people at a beach t hours past midnight on a certain day.",
              lambda x: f"at {x}:00 a.m.", lambda y: f"there were {y} people at the beach",
              "the number of people at the beach", (5, 11), (100, 900),
              lambda d: f"there were {d} more people at the beach", (20, 200)),
    "baby": ("H", "Baby {name}'s parents measure {name}'s height every month. H(t) models {name}'s height (in "
             "centimeters) at t months old.", lambda x: f"at {x} months old", lambda y: f"{{name}}'s height was {y} centimeters",
             "{name}'s height", (10, 30), (60, 95), lambda d: f"{{name}} was {d} centimeters taller", (2, 9)),
    "throw": ("H", "{name} is taking a free throw. H(d) models the ball's height (in meters) at a horizontal "
              "distance of d meters from {name}.", lambda x: f"at a horizontal distance of {x} meters",
              lambda y: f"the ball's height was {y} meters", "the ball's height", (2, 6), (2, 5), None, None),
    "taxi": ("M", "{name} drives a taxi. M(n) models {name}'s fee (in dollars) for the n-th drive of a certain day.",
             lambda x: f"for the {ordinal(x)} drive", lambda y: f"{{name}}'s fee was ${y}",
             "{name}'s fee", (2, 12), (8, 40), lambda d: f"{{name}}'s fee was ${d} more", (2, 15)),
    "tower": ("T", "Princess Tower in Dubai has 101 floors. T(n) models the number of tenants living on floor n.",
              lambda x: f"on floor {x}", lambda y: f"there were {y} tenants", "the number of tenants",
              (10, 100), (20, 90), lambda d: f"there were {d} more tenants", (2, 15)),
    "valley": ("V", "{name} walked down a trail into a valley. V(d) models {name}'s distance below the top of the "
               "valley (in kilometers) after walking d kilometers along the trail.",
               lambda x: f"after walking {x} km along the trail", lambda y: f"{{name}} was {y} km below the top",
               "{name}'s distance below the top", (2, 8), (1, 3), None, None),
}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

STATEMENT = {"equal": re.compile(r"(\w)\((\d+)\) = (\d+)"),
             "compare": re.compile(r"(\w)\((\d+)\) > \w\((\d+)\)"),
             "more": re.compile(r"(\w)\((\d+)\) = \w\((\d+)\) \+ (\d+)")}

def readings(ctx, statement, name):
    """(the right reading, two wrong ones) of a statement, in the story's words."""
    return [t.replace("a.m..", "a.m.") for t in _readings(ctx, statement, name)]   # one period after a.m.

def _readings(ctx, statement, name):
    F, intro, at, amount, noun, xs, ys, more, ds = CONTEXTS[ctx]
    fill = lambda s: s.replace("{name}", name)
    cap = lambda s: s[0].upper() + s[1:]
    m = STATEMENT["equal"].fullmatch(statement)
    if m:
        a, b = int(m.group(2)), int(m.group(3))
        return [fill(f"{cap(at(a))}, {amount(b)}."), fill(f"{cap(at(b))}, {amount(a)}."),
                fill(f"{cap(noun)} was the same {at(a)} and {at(b)}.")]
    m = STATEMENT["more"].fullmatch(statement)
    if m:
        a, b, d = int(m.group(2)), int(m.group(3)), int(m.group(4))
        return [fill(f"{cap(at(a))}, {more(d)} than {at(b)}."),
                fill(f"{cap(at(b))}, {more(d)} than {at(a)}."),
                fill(f"{cap(noun)} was the same {at(a)} and {at(b)}.")]
    m = STATEMENT["compare"].fullmatch(statement)
    a, b = int(m.group(2)), int(m.group(3))
    return [fill(f"{cap(noun)} was greater {at(a)} than {at(b)}."),
            fill(f"{cap(noun)} was greater {at(b)} than {at(a)}."),
            fill(f"{cap(noun)} was the same {at(a)} and {at(b)}.")]

def draw(entry, r, tpl):
    ctx = r.choice(list(CONTEXTS))
    F, intro, at, amount, noun, xs, ys, more, ds = CONTEXTS[ctx]
    name = r.choice(gen.NAMES)
    a, b = r.sample(range(xs[0], xs[1] + 1), 2)
    if entry == "1":
        y = r.randint(*ys)
        need(y != a)
        statement = f"{F}({a}) = {y}"
    elif more is None or r.random() < 0.5:
        statement = f"{F}({a}) > {F}({b})"
    else:
        d = r.randint(*ds)
        need(d not in (a, b, abs(a - b)))                 # no number does double duty (the old no. 9)
        statement = f"{F}({a}) = {F}({b}) + {d}"
    right, *wrong = readings(ctx, statement, name)
    choices, letter = gen.lettered(r, right, wrong)
    prompt = f"{intro.replace('{name}', name)} What does the statement {statement} mean?"
    return dict(context=ctx, name=name, statement=statement, prompt=prompt, choices=choices, answer=letter)

def check(p):
    try:
        right = readings(p["context"], p["statement"], p["name"])[0]
        ok = p["statement"] in p["prompt"] and p["choices"].count(right) == 1 and gen.chosen(p) == [right]
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    F = CONTEXTS[p["context"]][0]
    prompt = esc(p["prompt"]).replace(esc(p["statement"]), f"${p['statement']}$")
    prompt = re.sub(rf"\b{F}\((\w)\)", rf"${F}(\1)$", prompt, count=1)       # the model's name, as math
    return f"{prompt} \\\n    {gen.choices_typst([esc(c) for c in p['choices']])}"

def answer_typst(p):
    return esc(gen.choice_answer_typst(p))

def text(p):
    return p["prompt"] + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.6

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new statement; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
