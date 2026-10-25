"""Number, coin, and average problems (Advanced Math), from the 2025-26
midterm (digit reversal; nickels, dimes, and quarters) and Test 4, no. 20
(the score needed on the last test).

Stories use names only, no pronouns (the old Person class guessed them from
the name). Every answer is a whole number; a needed test score is 0 to 100
(the old Test 4 problem could ask for 115).

A problem: dict(type, story, prompt, answer, source); prompt and answer are
words. check() reads the numbers back out of the story and searches every
possibility (every two-digit number, every count of coins up to the total,
every score 0 to 100) for the ones that fit; there must be exactly one, and
it must be the answer's.
"""
from fractions import Fraction as F
from .. import gen
from ..gen import need

NAME = FAMILY = "adv_word"
FIXED = False
TITLE = "Number, Coin, and Average Problems"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Digit Problems",
         look="A two-digit number and the number with its digits reversed.",
         move="Let t be the tens digit and u the units digit. The number is 10t + u, and reversed it is "
              "10u + t. Write two equations from the facts and solve the system."),
    dict(key="2", title="Coin Problems",
         look="A number of coins, their total value, and how the kinds compare.",
         move="Let a letter stand for each kind of coin. Write one equation for the number of coins, one for "
              "their value in cents (5, 10, 25), and one for each comparison. Solve the system."),
    dict(key="3", title="Averages",
         look="Scores and an average, with one score missing.",
         move="average × number of scores = sum of the scores. Write that sum with x for the missing score and solve."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
TIMES = {1: "the same as", 2: "twice", 3: "three times", 4: "four times", 5: "five times"}
TIMES_OF = {w: k for k, w in TIMES.items()}
VALUE = {"nickels": 5, "dimes": 10, "quarters": 25}

STORIES = {
    "1": [
        dict(key="a",                          # the midterm
             text="The sum of the digits of a two-digit counting number is {s}. When the digits are reversed, "
                  "the new number is {d} {cmp} than the original number. What are the two numbers?",
             answer="{N}, {M}"),
        dict(key="b",
             text="The tens digit of a two-digit number is {k} more than the units digit. The sum of the number "
                  "and the number with its digits reversed is {S}. What are the two numbers?",
             answer="{N}, {M}"),
        dict(key="c",
             text="The units digit of a two-digit number is {m} the tens digit. When the digits are reversed, "
                  "the new number is {d} greater than the original number. What are the two numbers?",
             answer="{N}, {M}"),
    ],
    "2": [
        dict(key="a",                          # the midterm
             text="{name} has a total of {n} coins worth ${v}. All of the coins are nickels, dimes, or quarters. "
                  "If the number of {c2} is {f} the number of {c3}, how many of each kind of coin does {name} have?",
             answer="{a} nickels, {b} dimes, {c} quarters"),
        dict(key="b",
             text="{name} has {n} coins, all dimes and quarters, worth ${v}. How many of each does {name} have?",
             answer="{b} dimes, {c} quarters"),
        dict(key="c",
             text="{name} has {k} more dimes than nickels and {j} fewer quarters than dimes. The coins are worth "
                  "${v} in all. How many of each kind of coin does {name} have?",
             answer="{a} nickels, {b} dimes, {c} quarters"),
    ],
    "3": [
        dict(key="a",                          # Test 4, no. 20
             text="{name}'s test scores are {s1}, {s2}, {s3}, and {s4}. What does {name} need on the last test "
                  "to average {avg} on all five tests?",
             answer="{x}"),
        dict(key="b",
             text="{name}'s first {n} quiz scores average {a1}. What score on the next quiz would make the "
                  "average {a2}?",
             answer="{x}"),
        dict(key="c",
             text="The average of four test scores is {avg}. Three of them are {s1}, {s2}, and {s3}. What is the "
                  "fourth score?",
             answer="{x}"),
    ],
}
STORY = {(t, s["key"]): s for t, ss in STORIES.items() for s in ss}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def cents(c):
    return f"{c // 100}.{c % 100:02d}"

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def digits(r, st):
    t, u = r.sample(range(1, 10), 2)
    N, M = 10 * t + u, 10 * u + t
    if st["key"] == "a":
        return dict(s=t + u, d=abs(M - N), cmp="greater" if M > N else "less", N=N, M=M)
    if st["key"] == "b":
        need(t > u)
        return dict(k=t - u, S=N + M, N=N, M=M)
    need(u % t == 0 and 2 <= u // t <= 4)
    return dict(m=TIMES[u // t], d=M - N, N=N, M=M)

def coins(r, st):
    v = dict(name=r.choice(gen.NAMES))
    if st["key"] == "a":
        first, second, third = r.sample(list(VALUE), 3)
        f = r.randint(1, 5)
        count = {first: r.randint(1, 10), third: r.randint(1, 10)}
        count[second] = f * count[third]
        v.update(c2=second, c3=third, f=TIMES[f])
    elif st["key"] == "b":
        count = {"nickels": 0, "dimes": r.randint(1, 20), "quarters": r.randint(1, 20)}
    else:
        a, k, j = r.randint(1, 10), r.randint(1, 6), r.randint(1, 6)
        count = {"nickels": a, "dimes": a + k, "quarters": a + k - j}
        need(count["quarters"] >= 1)
        v.update(k=k, j=j)
    v.update(n=sum(count.values()), v=cents(sum(VALUE[c] * n for c, n in count.items())),
             a=count["nickels"], b=count["dimes"], c=count["quarters"])
    return v

def averages(r, st):
    v = dict(name=r.choice(gen.NAMES))
    if st["key"] == "a":
        s = [r.randint(80, 89), r.randint(70, 79), r.randint(90, 99), r.randint(90, 99)]
        avg = r.randint(80, 89)
        x = 5 * avg - sum(s)
        v.update(s1=s[0], s2=s[1], s3=s[2], s4=s[3], avg=avg)
    elif st["key"] == "b":
        n, a1 = r.randint(3, 6), r.randint(70, 90)
        a2 = a1 + r.choice((-2, -1, 1, 2, 3))
        x = a2 * (n + 1) - a1 * n
        v.update(n=n, a1=a1, a2=a2)
    else:
        s = [r.randint(60, 100) for _ in range(3)]
        avg = r.randint(70, 95)
        x = 4 * avg - sum(s)
        v.update(s1=s[0], s2=s[1], s3=s[2], avg=avg)
    need(0 <= x <= 100)
    v["x"] = x
    return v

DRAW = {"1": digits, "2": coins, "3": averages}

def draw(entry, r, tpl):
    st = STORIES[entry][tpl]
    v = DRAW[entry](r, st)
    p = dict(story=st["key"], prompt=gen.fill(st["text"], **v), answer=gen.fill(st["answer"], **v))
    need(len(solutions(entry, st, gen.read(st["text"], p["prompt"]))) == 1)       # one answer, no more
    return p

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(STORIES[e]))

# ------------------------------------------------------------------
# Checking: every possibility that fits the story's numbers
# ------------------------------------------------------------------
def solutions(typ, st, v):
    """Every answer that fits: a list of dicts of the answer's numbers."""
    n = {k: gen.number(x) for k, x in v.items() if k not in ("name", "cmp", "c2", "c3", "f", "m")}
    key = st["key"]
    if typ == "1":
        out = []
        for t in range(1, 10):
            for u in range(1, 10):
                N, M = 10 * t + u, 10 * u + t
                if key == "a":
                    ok = t + u == n["s"] and M - N == (n["d"] if v["cmp"] == "greater" else -n["d"])
                elif key == "b":
                    ok = t - u == n["k"] and N + M == n["S"]
                else:
                    ok = u == TIMES_OF[v["m"]] * t and M - N == n["d"]
                if ok:
                    out.append(dict(N=N, M=M))
        return out
    if typ == "2":                                       # a nickels, b dimes; the value fixes the quarters
        out, cents_ = [], int(100 * n["v"])
        for a in range(0, cents_ // 5 + 1):
            for b in range(0, (cents_ - 5 * a) // 10 + 1):
                c, left = divmod(cents_ - 5 * a - 10 * b, 25)
                count = {"nickels": a, "dimes": b, "quarters": c}
                if left or ("n" in n and a + b + c != n["n"]):
                    continue
                if key == "a" and count[v["c2"]] != TIMES_OF[v["f"]] * count[v["c3"]]:
                    continue
                if key == "b" and a != 0:
                    continue
                if key == "c" and not (b == a + n["k"] and c == b - n["j"]):
                    continue
                out.append(dict(a=a, b=b, c=c) if key != "b" else dict(b=b, c=c))
        return out
    total = {"a": 5 * n.get("avg", 0), "b": (n.get("n", 0) + 1) * n.get("a2", 0), "c": 4 * n.get("avg", 0)}[key]
    known = {"a": lambda: n["s1"] + n["s2"] + n["s3"] + n["s4"], "b": lambda: n["n"] * n["a1"],
             "c": lambda: n["s1"] + n["s2"] + n["s3"]}[key]()
    return [dict(x=x) for x in range(0, 101) if known + x == total]

def check(p):
    try:
        st = STORY[(p["type"], p["story"])]
        sols = solutions(p["type"], st, gen.read(st["text"], p["prompt"]))
        got = gen.read(st["answer"], p["answer"])
        ok = len(sols) == 1 and all(gen.number(got[k]) == x for k, x in sols[0].items())
    except (ValueError, KeyError):
        return "unchecked"
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing and editing: change the numbers and names; keep the words
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.text_shown()

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    st = STORY[(old["type"], old["story"])]
    sols = solutions(old["type"], st, gen.read(st["text"], t))
    answer = gen.fill(st["answer"], **sols[0]) if len(sols) == 1 else old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=8)   # story 1c has only 9 numbers
