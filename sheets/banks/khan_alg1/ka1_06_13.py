"""Khan Algebra 1, Lesson 6-13: Age word problems, from the old app's
Alg1_06_13 (forty slots: seven generated kinds, and Khan's own).

The old seven kinds, as four types: (1) one is d years older than the
other, and Y years ago was k times as old (sometimes said the other way,
"years younger", sometimes with a fact that doesn't matter, when they
met); (2) k times as old and also d years older; (3) k times as old now,
and m times as old t years ago; (4) the future: in d years someone will be
k times as old as now, or how many years until one is only k times as old
as the other. Names only, no pronouns (the old type 11 used them).

A problem: dict(type, story, prompt, answer, source); words.
    answer  "Maya is 14." or "6 years"
check() reads the numbers back out of the story and tries every age from 0
to 120 (every wait from 1 to 120): exactly one must fit, and it is the key's.
"""
from ... import gen
from ...gen import need
from . import courses

NAME = FAMILY = "ka1_06_13"
FIXED = False
TITLE = "Lesson 6-13: Age word problems"
INSTRUCTIONS = "Write a system of equations, and solve it."
COURSES = courses(6)
TIMES = {2: "twice", 3: "three times", 4: "four times", 5: "five times", 6: "six times", 7: "seven times",
         8: "eight times", 9: "nine times"}
TIMES_OF = {w: k for k, w in TIMES.items()}
WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
         11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen",
         18: "Eighteen", 19: "Nineteen", 20: "Twenty"}
WORDS_OF = {w: k for k, w in WORDS.items()}

TYPES = [
    dict(key="1", title="Older By, and Years Ago",
         look="How much older one person is, and a multiple some years ago.",
         move="Let a letter stand for each age now. One equation: the difference. The other: subtract the years "
              "from both ages, then one is k times the other.", width="full"),
    dict(key="2", title="Times as Old, and Older By",
         look="One person is k times as old as the other and also d years older.",
         move="Two equations, both about ages now: a = k b and a = b + d.", width="full"),
    dict(key="3", title="Times as Old, Now and Years Ago",
         look="A multiple now, and a different multiple some years ago.",
         move="a = k b now; (a - t) = m (b - t) years ago. Substitute the first into the second.", width="full"),
    dict(key="4", title="Into the Future",
         look="What will be true some years from now.",
         move="Add the years to every age that changes. Write the equation, then solve.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def two(r):
    return r.sample(gen.NAMES, 2)

# ------------------------------------------------------------------
# Stories: draw(r) -> the words; fits(n, a, b) -> do ages a, b now fit the story?
# ------------------------------------------------------------------
def d_then(r):                                # a = b + d; a - y = k (b - y)
    a_, b_ = two(r)
    b0, k = r.randint(1, 5), r.randint(2, 6)
    y = r.randint(5, 20)
    q = r.choice((a_, b_))
    return dict(a=a_, b=b_, d=b0 * k - b0, y=WORDS[y], k=TIMES[k], q=q, met=WORDS[r.randint(2, 4)].lower())

def f_then(n, a, b):
    y = WORDS_OF[n["y"]]
    return a == b + int(n["d"]) and a - y >= 0 and b - y >= 0 and a - y == TIMES_OF[n["k"]] * (b - y)

def d_times_older(r):                         # a = k b; a = b + d
    a_, b_ = two(r)
    b, k = r.randint(1, 12), r.randint(2, 6)
    return dict(a=a_, b=b_, k=TIMES[k], d=k * b - b, q=r.choice((a_, b_)))

def f_times_older(n, a, b):
    return a == TIMES_OF[n["k"]] * b and a == b + int(n["d"])

def d_now_then(r):                            # a = j b now; a - t = k (b - t)
    a_, b_ = two(r)
    for _ in range(50):
        k, delta = r.randint(4, 9), r.randint(1, 6)
        j, b = k - delta, r.randint(2, 12)
        if j >= 2 and (b * delta) % (j - 1) == 0:
            t = b * delta // (j - 1)
            if 1 <= t <= 20 and b * k + t <= 100:
                return dict(a=a_, b=b_, j=TIMES[j], t=WORDS[t] if t in WORDS else None, k=TIMES[k], q=r.choice((a_, b_)))
    raise gen.Redraw

def f_now_then(n, a, b):
    t = WORDS_OF[n["t"]]
    return a == TIMES_OF[n["j"]] * b and b - t > 0 and a - t == TIMES_OF[n["k"]] * (b - t)

def d_future_self(r):                         # a + d = k a
    a_ = r.choice(gen.NAMES)
    age, k = r.randint(1, 12), r.randint(2, 6)
    return dict(a=a_, d=age * k - age, k=TIMES[k], q=a_)

def f_future_self(n, a, b):
    return a + int(n["d"]) == TIMES_OF[n["k"]] * a

def d_until(r):                               # (a + t) = k (b + t)
    a_, b_ = two(r)
    k, young = r.randint(2, 6), r.randint(6, 16)
    t = r.randint(2, young - 2)                   # the younger is 2 or older now
    return dict(a=a_, b=b_, an=young * k - t, bn=young - t, k=TIMES[k])

STORIES = [
    dict(key="a", type="1", draw=d_then, fits=f_then,
         text="{a} is {d} years older than {b}. {y} years ago, {a} was {k} as old as {b}.",
         ask="How old is {q} now?"),
    dict(key="b", type="1", draw=d_then, fits=f_then,
         text="{b} is {d} years younger than {a}. {a} and {b} met {met} years ago. {y} years ago, {a} was {k} as "
              "old as {b}.",
         ask="How old is {q} now?"),
    dict(key="c", type="2", draw=d_times_older, fits=f_times_older,
         text="{a} is {k} as old as {b} and is also {d} years older than {b}.",
         ask="How old is {q}?"),
    dict(key="d", type="3", draw=d_now_then, fits=f_now_then,
         text="{a} is {j} as old as {b}. {t} years ago, {a} was {k} as old as {b}.",
         ask="How old is {q} now?"),
    dict(key="e", type="4", draw=d_future_self, fits=f_future_self,
         text="In {d} years, {a} will be {k} as old as {a} is now.",
         ask="How old is {q} now?"),
    dict(key="f", type="4", draw=d_until, fits=None,
         text="{a} is {an} years old, and {b} is {bn} years old.",
         ask="How many years will it take until {a} is only {k} as old as {b}?"),
]
STORY = {s["key"]: s for s in STORIES}
BY_TYPE = {k: [s for s in STORIES if s["type"] == k] for k in KEYS}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def words_of(st, prompt):
    return gen.read(st["text"] + " " + st["ask"], prompt)

def key(st, prompt):
    """The answer, from the story's words: every age (or wait) tried; exactly one must fit."""
    n = words_of(st, prompt)
    if st["fits"] is None:                    # how many years until
        an, bn, k = int(n["an"]), int(n["bn"]), TIMES_OF[n["k"]]
        found = [t for t in range(1, 121) if an + t == k * (bn + t)]
        if len(found) != 1:
            raise ValueError(f"{len(found)} answers")
        return f"{found[0]} years"
    ages = [(a, b) for a in range(0, 121) for b in range(0, 121) if st["fits"](n, a, b)] if "b" in n else \
        [(a, None) for a in range(0, 121) if st["fits"](n, a, None)]
    if len(ages) != 1:
        raise ValueError(f"{len(ages)} answers")
    a, b = ages[0]
    return f"{n['q']} is {a if n['q'] == n['a'] else b}."

def draw(entry, r, tpl):
    st = BY_TYPE[entry][tpl]
    w = st["draw"](r)
    need(all(x is not None for x in w.values()))
    prompt = gen.fill(st["text"] + " " + st["ask"], **w)
    return dict(story=st["key"], prompt=prompt, answer=key(st, prompt))

def check(p):
    try:
        return "checked" if " ".join(p["answer"].split()) == key(STORY[p["story"]], p["prompt"]) else "failed"
    except (ValueError, KeyError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(BY_TYPE[e]))
typst, answer_typst, text, answer_text, height = gen.text_shown()

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    try:
        answer = key(STORY[old["story"]], t)
    except ValueError as e:
        raise ValueError(f"keep the story's words; change only its numbers and names ({e})") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
