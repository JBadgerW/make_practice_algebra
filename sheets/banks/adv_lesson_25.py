"""Lesson 25 (Advanced Math): age problems, rate problems. From the Saxon
lesson and its deck (~/Documents/adv_math/problem_sets/ps_025/slides/deck_025.typ):
examples 25.1-25.5 and Problem Set 25, problems 1-4.

    1  ages now, from two statements:   Ten years ago, Thomas was twice as old as Patricia. Five years
                                        from now, Thomas will be 10 years older than Patricia. ...
                                                                    Patricia is 20, Thomas is 30
    2  one works alone, then both:      Joe Frank can wash 3 cars in 5 hours and Myrl can wash 4 cars
                                        in 3 hours. Fifteen cars ... how long ... together ...?
                                                                    207/29 hr ≈ 7.14 hr
    3  an unknown rate from a total:    Mayha could empty 2 bottles in 3 hours. Working together, ...
                                                                    2/3 bottle/hr
    4  workers, RWT = J:                If 5 workers can do 1 job in 8 days, how many workers would it
                                        take to do 3 jobs in 7 days?          17.14 workers
    5  supplies, RTI = G, more added:   Mary had 252 gallons (gal) of milk. This would feed 42 infants
                                        for 12 days. Then 14 more infants ... 48 more gallons ...
                                                                    10.71 days

The types file's last heading (four-variable rate problems) is split by its
story: Type 4 finds the workers (or the days) for more jobs (25.4, problem 4);
Type 5 finds how long supplies last after more eaters and more supplies come
(25.5, which has no Problem Set item).

Stories use names only, no pronouns. The book's wording is kept, with these
changes so that one template writes both of a type's sources:
  25.1     "Ten years ago, Thomas ..." (a comma, as problem 1 has).
  PS 2     written as 25.2 is: "If Emerson works for 1 hour and is then joined by
           Johnna, how long will Johnna and Emerson have to work together ...".
  25.3     "Working with Wilbur, she found they could empty ..." is written
  PS 3     "Working together, Mayha and Wilbur could empty ..." (no pronoun);
           problem 3's "merely" is dropped.

The key writes what the deck writes:
  1  the ages now, the younger first: "Patricia is 20, Thomas is 30" (25.1),
     "Wilbur is 15, Orville is 25" (problem 1).
  2  the time together in hours, a fraction in lowest terms, then its decimal
     to two places: "207/29 hr ≈ 7.14 hr" (25.2), "32/13 hr ≈ 2.46 hr"
     (problem 2); "= 2.5 hr" when the decimal is exact; "3 hr" when whole.
  3  the rate, a fraction in lowest terms (or a whole number) per hour, the
     unit singular when the rate is 1 or less: "2/3 bottle/hr" (25.3),
     "2/5 sandcastle/hr" (problem 3), "7/3 bottles/hr".
  4  the number of workers (or days), as a decimal rounded to two places, or
     whole: "17.14 workers" (25.4), "162 men" (problem 4).
  5  the days, the same way: "10.71 days" (25.5).
Rounding is half up.

check() reads the numbers back out of the story's words and puts the
answer back into the lesson's equation, independently of how it was drawn:
  1  each statement is a linear equation in the ages now (a ratio
     a + t = k(b + t), a difference a - b = d, a sum a + b + 2t = s); the two
     are solved by Cramer's rule, and the answer's names and ages must match.
  2  R1 (t + T) + R2 T = N, exactly, with T the answer's fraction; the
     decimal after it must be T rounded (and "=" only when exact).
  3  R1 d + R d = c, exactly; singular or plural by the rule above.
  4  R = J1/(W1 D1) from the first situation, then R W D2 = J2 (or R W2 D = J2)
     solved and rounded; the answer's number and word must match.
  5  R = G1/(I1 D1), then R (I1 + I2) T = G1 + G2 solved and rounded.

No skipped sources: Lesson 25 has no proofs.

A problem: dict(type, story, prompt, answer, source); prompt and answer are
words (story names the template the words were written from):
    story   "ago:ratio|ahead:diff|0"
    prompt  "Ten years ago, Thomas was twice as old as Patricia. Five years from now, Thomas will be
             10 years older than Patricia. How old are both people now?"
    answer  "Patricia is 20, Thomas is 30"
"""
import math, re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from .. import gen
from ..gen import need
from ..typst import esc

NAME = FAMILY = "adv_lesson_25"
FIXED = False
TITLE = "Lesson 25: Age Problems, Rate Problems"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="Age Problems",
         look="Two people's ages compared at two times: years ago, now, or years from now.",
         move="Let $A_N$ and $B_N$ be the ages now. Write every other age from them: $B_N - 10$ ten years ago, "
              "$B_N + 5$ five years from now. Write one equation per statement, like $A_N - 10 = 2(B_N - 10)$, "
              "and solve the system."),
    dict(key="2", title="One Works Alone, Then Both Together",
         look="Two rates, a total job, and one person who starts alone.",
         move="Find each rate as work over time: $(3 \"cars\")/(5 \"hr\") = 3/5 \"car\"/\"hr\"$. Subtract what "
              "the first person does alone. Then $R_1 T + R_2 T = \"what is left\"$; clear the fractions and "
              "solve for $T$."),
    dict(key="3", title="An Unknown Rate from a Joint Total",
         look="One person's rate, and what the two do together in a given time.",
         move="$R_1 T_1 + R_2 T_2 = \"total\"$. Put in the known rate and the times, and solve for the unknown "
              "rate $R_2$."),
    dict(key="4", title="Workers and Jobs, RWT = J",
         look="Workers do some jobs in some days; how many workers (or days) for other jobs?",
         move="$R W T = J$. Find the rate from the first situation: $R(5)(8) = 1$, so $R = 1/40$ job per "
              "worker-day. Then use $R$ in the second situation and solve for what is asked."),
    dict(key="5", title="Supplies That Must Last, RTI = G",
         look="Supplies feed so many for so many days; then more eaters and more supplies come.",
         move="$R T I = G$. Find the rate from the first situation, $R(12)(42) = 252$. Then put in the new "
              "totals, $(42 + 14)$ eaters and $(252 + 48)$ of supplies, and solve for $T$."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

# the book's names, then the shared ones
NAMES = ("Thomas", "Patricia", "Orville", "Wilbur", "Joe Frank", "Myrl", "Mayha", "Emerson", "Johnna",
         "Sandra", "Frederick", "Mary") + gen.NAMES

WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
         "sixteen seventeen eighteen nineteen").split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

def word(n):
    """A number spelled, capitalized, to start a sentence: Fifteen, Twenty-four."""
    w = WORDS[n] if n < 20 else TENS[n // 10] + ("-" + WORDS[n % 10] if n % 10 else "")
    return w.capitalize()

NUMBER_OF = {word(n): n for n in range(1, 100)}

def whole(s):
    """A number read from the story: digits or a spelled word."""
    s = s.strip()
    return F(NUMBER_OF[s]) if s in NUMBER_OF else gen.number(s)

def plural(n, one, many):
    return one if n == 1 else many

def rounded(q):
    """q to two places, half up: 17.14, 5.30; exact ones without trailing zeros: 12.5, 162."""
    d = (Decimal(q.numerator) / Decimal(q.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    return s.rstrip("0").rstrip(".") if (q * 100).denominator == 1 else s

def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Type 1: ages
# ------------------------------------------------------------------
MULTS = {F(2): "twice", F(3): "three times", F(4): "four times", F(3, 2): "1 1/2 times",
         F(5, 2): "2 1/2 times", F(4, 3): "1 1/3 times"}
MULT_OF = {w: k for k, w in MULTS.items()}
TIMES = range(2, 21)                     # years ago or from now
AGES = range(2, 81)                      # every age the story mentions
NOW = range(6, 61)                       # the younger one's age now
WHENS = ("ago", "now", "ahead")
RELS = ("ratio", "diff", "sum")
ASKS = ("How old are both people now?", "How old are both now?")

def clause(when, rel, i):
    """One statement's words; i (1 or 2) numbers its placeholders."""
    lead = {"ago": f"{{t{i}}} years ago, ", "now": "", "ahead": f"{{t{i}}} years from now, "}[when]
    verb = {"ago": "was", "now": "is now", "ahead": "will be"}[when]
    body = {"ratio": f"{{A}} {verb} {{k{i}}} as old as {{B}}.",
            "diff": f"{{A}} {verb} {{d{i}}} years older than {{B}}.",
            "sum": f"the sum of the ages of {{A}} and {{B}} {verb} {{s{i}}}."}[rel]
    return lead + (body if lead else body[0].upper() + body[1:])

def age_template(story):
    s1, s2, q = story.split("|")
    (w1, r1), (w2, r2) = s1.split(":"), s2.split(":")
    return clause(w1, r1, 1) + " " + clause(w2, r2, 2) + " " + ASKS[int(q)]

AGE_ANSWER = "{B} is {b}, {A} is {a}"

def offset(when, t):
    return {"ago": -t, "now": 0, "ahead": t}[when]

def t1(A, B, a, b, w1, r1, t1, w2, r2, t2, q):
    """A (older, a now) and B (younger, b now); statement i is (when, relation, years)."""
    v = dict(A=A, B=B)
    for i, (w, rel, t) in ((1, (w1, r1, t1)), (2, (w2, r2, t2))):
        o = offset(w, t)
        if w != "now":
            v[f"t{i}"] = word(t)
        if rel == "ratio":
            v[f"k{i}"] = MULTS[F(a + o, b + o)]
        elif rel == "diff":
            v[f"d{i}"] = a - b
        else:
            v[f"s{i}"] = a + b + 2 * o
    story = f"{w1}:{r1}|{w2}:{r2}|{q}"
    return story, gen.fill(age_template(story), **v), gen.fill(AGE_ANSWER, A=A, B=B, a=a, b=b)

def t1_ok(A, B, a, b, w1, r1, t1, w2, r2, t2, q):
    o1, o2 = offset(w1, t1), offset(w2, t2)
    return (A in NAMES and B in NAMES and A != B and a - b >= 2 and b in NOW and q in (0, 1)
            and w1 in WHENS and w2 in WHENS and r1 in RELS and r2 in RELS
            and "ratio" in (r1, r2) and o1 < o2
            and all(t in TIMES for w, t in ((w1, t1), (w2, t2)) if w != "now")
            and all(t == 0 for w, t in ((w1, t1), (w2, t2)) if w == "now")
            and all(x in AGES for x in (a + o1, b + o1, a + o2, b + o2))
            and all(F(a + o, b + o) in MULTS for r, o in ((r1, o1), (r2, o2)) if r == "ratio")
            and not (r1 == r2 == "diff"))

def age_pick(r, shapes):
    """The shape and the years first; then every younger age now and multiplier that the
    first ratio statement allows, kept if the whole story is in range."""
    (w1, r1), (w2, r2) = r.choice(shapes)
    A, B = r.sample(NAMES, 2)
    t1_ = r.choice(TIMES) if w1 != "now" else 0
    t2_ = r.choice(TIMES) if w2 != "now" else 0
    o = offset(w1, t1_) if r1 == "ratio" else offset(w2, t2_)
    base = dict(A=A, B=B, w1=w1, r1=r1, t1=t1_, w2=w2, r2=r2, t2=t2_, q=r.randrange(2))
    fits = []
    for b in NOW:
        for k in MULTS:
            a = k * (b + o) - o                              # a + o = k (b + o)
            if a.denominator == 1 and t1_ok(**base, a=int(a), b=b):
                fits.append(dict(base, a=int(a), b=b))
    need(fits)
    return r.choice(fits)

BOOK_SHAPES = [(("ago", "ratio"), ("ahead", "diff"))]                  # 25.1
RATIO_SHAPES = [(("ago", "ratio"), ("ahead", "ratio"))]                # problem 1
OTHER_SHAPES = [((w1, r1), (w2, r2)) for i, w1 in enumerate(WHENS) for w2 in WHENS[i + 1:]
                for r1 in RELS for r2 in RELS if "ratio" in (r1, r2)]
OTHER_SHAPES = [s for s in OTHER_SHAPES if s not in BOOK_SHAPES + RATIO_SHAPES]

def t1_book(r):
    return age_pick(r, BOOK_SHAPES)

def t1_ratios(r):
    return age_pick(r, RATIO_SHAPES)

def t1_other(r):
    return age_pick(r, OTHER_SHAPES)

def age_equation(when, rel, t, value):
    """(ca, cb, rhs): ca a + cb b = rhs, in the ages now."""
    o = offset(when, t)
    if rel == "ratio":                   # a + o = k (b + o)
        return 1, -value, value * o - o
    if rel == "diff":
        return 1, -1, value
    return 1, 1, value - 2 * o

def solve_ages(story, v):
    s1, s2, _ = story.split("|")
    rows = []
    for i, s in ((1, s1), (2, s2)):
        w, rel = s.split(":")
        t = int(whole(v[f"t{i}"])) if w != "now" else 0
        value = MULT_OF[v[f"k{i}"]] if rel == "ratio" else whole(v[f"d{i}" if rel == "diff" else f"s{i}"])
        rows.append(age_equation(w, rel, t, value))
    (p, q, e), (r, s, f) = rows
    det = p * s - q * r
    if det == 0:
        raise ValueError("no single answer")
    return F(e * s - q * f, det), F(p * f - e * r, det)

# ------------------------------------------------------------------
# Types 2 and 3: work at a rate
# ------------------------------------------------------------------
# (one, many, verb, past participle, -ing)
JOBS = [("car", "cars", "wash", "washed", "washing"), ("hole", "holes", "dig", "dug", "digging"),
        ("bottle", "bottles", "empty", "emptied", "emptying"),
        ("sandcastle", "sandcastles", "build", "built", "building"),
        ("fence", "fences", "paint", "painted", "painting"), ("box", "boxes", "pack", "packed", "packing"),
        ("pie", "pies", "bake", "baked", "baking"), ("room", "rooms", "clean", "cleaned", "cleaning"),
        ("quilt", "quilts", "sew", "sewn", "sewing")]
JOB = {j[1]: j for j in JOBS}
COUNTS = range(1, 7)                     # Type 2: items and hours in each rate
START = range(1, 5)                      # hours alone
TOTALS = range(4, 31)

T2_TEXT = ("{P} can {verb} {a} {ia} in {b} {hb} and {Q} can {verb} {c} {ic} in {d} {hd}. {Nw} {items} need "
           "to be {pp}. If {P} works for {t} {ht} and is then joined by {Q}, how long will {Q} and {P} have to "
           "work together to finish {ing} the {N} {items}?")

def hours(T):
    """207/29 hr ≈ 7.14 hr; 5/2 hr = 2.5 hr; 3 hr."""
    if T.denominator == 1:
        return f"{T} hr"
    exact = (T * 100).denominator == 1
    return f"{frac(T)} hr {'=' if exact else '≈'} {rounded(T)} hr"

def t2(P, Q, job, a, b, c, d, N, t):
    one, many, verb, pp, ing = JOB[job]
    v = dict(P=P, Q=Q, verb=verb, a=a, ia=plural(a, one, many), b=b, hb=plural(b, "hour", "hours"), c=c,
             ic=plural(c, one, many), d=d, hd=plural(d, "hour", "hours"), Nw=word(N), items=many, pp=pp, t=t,
             ht=plural(t, "hour", "hours"), ing=ing, N=N)
    T_ = (N - F(a, b) * t) / (F(a, b) + F(c, d))
    return "together", gen.fill(T2_TEXT, **v), hours(T_)

def t2_ok(P, Q, job, a, b, c, d, N, t):
    return (P in NAMES and Q in NAMES and P != Q and job in JOB
            and all(x in COUNTS for x in (a, b, c, d)) and N in TOTALS and t in START
            and F(a, b) != F(c, d) and N - F(a, b) * t >= 2
            and ((N - F(a, b) * t) / (F(a, b) + F(c, d))).denominator <= 60)

def t2_pick(r):
    P, Q = r.sample(NAMES, 2)
    p = dict(P=P, Q=Q, job=r.choice(JOBS)[1], a=r.choice(COUNTS), b=r.choice(COUNTS), c=r.choice(COUNTS),
             d=r.choice(COUNTS), N=r.choice(TOTALS), t=r.choice(START))
    need(t2_ok(**p))
    return p

T3_TEXT = ("{P} could {verb} {a} {ia} in {b} {hb}. Working together, {P} and {Q} could {verb} {c} {ic} in {d} "
           "{hd}. What was {Q}'s rate of {ing} {items}?")
ALONE = range(1, 9)                      # Type 3: the known rate's items and hours, the joint hours
JOINT = range(1, 13)                     # the joint items

def rate_answer(R, job):
    one, many = JOB[job][:2]
    return f"{frac(R)} {one if R <= 1 else many}/hr"

def t3(P, Q, job, a, b, c, d):
    one, many, verb, pp, ing = JOB[job]
    v = dict(P=P, Q=Q, verb=verb, a=a, ia=plural(a, one, many), b=b, hb=plural(b, "hour", "hours"), c=c,
             ic=plural(c, one, many), d=d, hd=plural(d, "hour", "hours"), items=many, ing=ing)
    return "joint", gen.fill(T3_TEXT, **v), rate_answer(F(c, d) - F(a, b), job)

def t3_ok(P, Q, job, a, b, c, d):
    return (P in NAMES and Q in NAMES and P != Q and job in JOB and a in ALONE and b in ALONE
            and d in ALONE and c in JOINT and F(c, d) > F(a, b)
            and (F(c, d) - F(a, b)).denominator <= 15 and F(c, d) - F(a, b) <= 3)

def t3_pick(r):
    P, Q = r.sample(NAMES, 2)
    p = dict(P=P, Q=Q, job=r.choice(JOBS)[1], a=r.choice(ALONE), b=r.choice(ALONE), c=r.choice(JOINT),
             d=r.choice(ALONE))
    need(t3_ok(**p))
    return p

# ------------------------------------------------------------------
# Type 4: R W T = J
# ------------------------------------------------------------------
CREWS = ("workers", "men", "women", "painters", "carpenters", "machines")
CREW = range(2, 13)
JOBS1 = range(1, 5)
DAYS = range(2, 16)
JOBS2 = range(1, 21)
T4_TEXT = {
    "if": "If {W1} {crew} can do {J1} {j1} in {D1} days, how many {crew} would it take to do {J2} {j2} in {D2} "
          "days?",
    "then": "{W1w} {crew} can do {J1} {j1} in {D1} days. How many {crew} would it take to do {J2} {j2} in {D2} "
            "days?",
    "days": "{W1w} {crew} can do {J1} {j1} in {D1} days. How many days would it take {W2} {crew} to do {J2} "
            "{j2}?",
}
T4_ANSWER = {"if": "{x} {crew}", "then": "{x} {crew}", "days": "{x} days"}

def t4_value(story, W1, J1, D1, J2, D2=None, W2=None):
    R = F(J1, W1 * D1)                   # jobs per worker-day
    return F(J2) / (R * D2) if story != "days" else F(J2) / (R * W2)

def t4(story, crew, W1, J1, D1, J2, D2=None, W2=None):
    v = dict(crew=crew, W1=W1, W1w=word(W1), J1=J1, j1=plural(J1, "job", "jobs"), D1=D1, J2=J2,
             j2=plural(J2, "job", "jobs"), D2=D2, W2=W2)
    x = t4_value(story, W1, J1, D1, J2, D2, W2)
    return story, gen.fill(T4_TEXT[story], **v), gen.fill(T4_ANSWER[story], x=rounded(x), crew=crew)

def t4_ok(story, crew, W1, J1, D1, J2, D2=None, W2=None):
    if story not in T4_TEXT or crew not in CREWS or W1 not in CREW or J1 not in JOBS1 or D1 not in DAYS \
            or J2 not in JOBS2 or (D2 not in DAYS if story != "days" else W2 not in CREW or W2 == W1):
        return False
    x = t4_value(story, W1, J1, D1, J2, D2, W2)
    return 2 <= x <= 500 and J2 != J1 and (story == "days" or D2 != D1)

def t4_pick(story):
    def pick(r):
        p = dict(story=story, crew=r.choice(CREWS), W1=r.choice(CREW), J1=r.choice(JOBS1), D1=r.choice(DAYS),
                 J2=r.choice(JOBS2))
        p.update(dict(W2=r.choice(CREW)) if story == "days" else dict(D2=r.choice(DAYS)))
        need(t4_ok(**p))
        return p
    return pick

# ------------------------------------------------------------------
# Type 5: R T I = G, with more eaters and more supplies
# ------------------------------------------------------------------
# (supply, unit as first named, unit, eaters, how they came, how the supplies came)
SUPPLIES = [("milk", "gallons (gal)", "gallons", "infants", "were placed in the nursery", "were provided"),
            ("hay", "bales", "bales", "horses", "were brought to the ranch", "were delivered"),
            ("dog food", "pounds (lb)", "pounds", "dogs", "were taken in at the shelter", "were donated"),
            ("rice", "kilograms (kg)", "kilograms", "campers", "arrived at the camp", "were brought")]
SUPPLY = {s[0]: s for s in SUPPLIES}
T5_TEXT = ("{P} had {G1} {unit1} of {supply}. This would feed {I1} {eaters} for {D1} days. Then {I2} more {eaters} "
           "{came} and {G2} more {unit} {given}. How long would the {supply} last now?")
RATES = (F(1, 4), F(1, 3), F(1, 2), F(1), F(2), F(3))      # supplies per eater-day
EATERS = range(5, 61)
FEED_DAYS = range(5, 31)
MORE_EATERS = range(2, 41)
MORE_SUPPLY = range(2, 1001)

def t5(P, supply, G1, I1, D1, I2, G2):
    _, unit1, unit, eaters, came, given = SUPPLY[supply]
    v = dict(P=P, G1=G1, unit1=unit1, supply=supply, I1=I1, eaters=eaters, D1=D1, I2=I2, came=came, G2=G2,
             unit=unit, given=given)
    R = F(G1, I1 * D1)
    return "supplies", gen.fill(T5_TEXT, **v), f"{rounded(F(G1 + G2) / (R * (I1 + I2)))} days"

def t5_ok(P, supply, G1, I1, D1, I2, G2):
    return (P in NAMES and supply in SUPPLY and I1 in EATERS and D1 in FEED_DAYS and I2 in MORE_EATERS
            and I2 <= I1 and G2 in MORE_SUPPLY and G2 <= G1 and F(G1, I1 * D1) in RATES and G1 <= 2000
            and F(G1 + G2) / (F(G1, I1 * D1) * (I1 + I2)) != D1)

def t5_pick(r):
    rate, I1, D1 = r.choice(RATES), r.choice(EATERS), r.choice(FEED_DAYS)
    G1 = rate * I1 * D1
    need(G1.denominator == 1)
    G1 = int(G1)
    step = r.choice((1, 2, 5, 10))
    p = dict(P=r.choice(NAMES), supply=r.choice(SUPPLIES)[0], G1=G1, I1=I1, D1=D1, I2=r.randint(2, I1 // 2 + 2),
             G2=step * r.randint(1, max(1, G1 // (2 * step))))
    need(t5_ok(**p))
    return p

# ------------------------------------------------------------------
# Templates: (pick, build); the build writes (story, prompt, answer)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_book, t1), (t1_ratios, t1), (t1_other, t1)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick("if"), t4), (t4_pick("then"), t4), (t4_pick("days"), t4)],
    "5": [(t5_pick, t5)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    story, prompt, answer = build(**pick(r))
    return dict(story=story, prompt=prompt, answer=answer)

# ------------------------------------------------------------------
# Checking: read the story's numbers, put the answer back in
# ------------------------------------------------------------------
def template(typ, story):
    return {"1": lambda: age_template(story), "2": lambda: T2_TEXT, "3": lambda: T3_TEXT,
            "4": lambda: T4_TEXT[story], "5": lambda: T5_TEXT}[typ]()

def solve(typ, story, v):
    """The answer's words, from the story's numbers (as read); ValueError if there is none."""
    if typ == "1":
        a, b = solve_ages(story, v)
        if a.denominator != 1 or b.denominator != 1 or not (0 < b < a):
            raise ValueError("no answer in whole ages")
        return gen.fill(AGE_ANSWER, A=v["A"], B=v["B"], a=int(a), b=int(b))
    n = {k: whole(x) for k, x in v.items() if k in ("a", "b", "c", "d", "N", "t", "W1", "W1w", "J1", "D1",
                                                       "J2", "D2", "W2", "G1", "I1", "I2", "G2")}
    if typ == "2":
        R1, R2 = n["a"] / n["b"], n["c"] / n["d"]
        if whole(v["Nw"]) != n["N"]:
            raise ValueError("the two totals differ")
        return hours((n["N"] - R1 * n["t"]) / (R1 + R2))
    if typ == "3":
        return rate_answer(n["c"] / n["d"] - n["a"] / n["b"], v["items"])
    if typ == "4":
        W1 = n.get("W1", n.get("W1w"))
        R = n["J1"] / (W1 * n["D1"])
        x = n["J2"] / (R * n["D2"]) if story != "days" else n["J2"] / (R * n["W2"])
        return gen.fill(T4_ANSWER[story], x=rounded(x), crew=v["crew"])
    R = n["G1"] / (n["I1"] * n["D1"])
    return f"{rounded((n['G1'] + n['G2']) / (R * (n['I1'] + n['I2'])))} days"

def check(p):
    """The answer put back into the lesson's equation (see the docstring)."""
    try:
        typ, story = p["type"], p["story"]
        v = gen.read(template(typ, story), p["prompt"])
        ans = " ".join(p["answer"].split())
        if typ == "1":
            got = gen.read(AGE_ANSWER, ans)
            a, b = F(int(got["a"])), F(int(got["b"]))
            ok = got["A"] == v["A"] and got["B"] == v["B"] and solve_ages(story, v) == (a, b) and 0 < b < a
        elif typ == "2":
            m = re.fullmatch(r"(\d+(?:/\d+)?) hr(?: (=|≈) (\d+(?:\.\d+)?) hr)?", ans)
            Tf = F(m.group(1))
            R1, R2 = whole(v["a"]) / whole(v["b"]), whole(v["c"]) / whole(v["d"])
            ok = (R1 * (whole(v["t"]) + Tf) + R2 * Tf == whole(v["N"]) == whole(v["Nw"])
                  and m.group(1) == frac(Tf)                           # lowest terms
                  and (m.group(2) is None) == (Tf.denominator == 1)
                  and (Tf.denominator == 1 or (m.group(2) == "=") == ((Tf * 100).denominator == 1)
                       and m.group(3) == rounded(Tf)))
        elif typ == "3":
            m = re.fullmatch(r"(\d+(?:/\d+)?) (\w+)/hr", ans)
            R = F(m.group(1))
            one, many = JOB[v["items"]][:2]
            d = whole(v["d"])
            ok = (whole(v["a"]) / whole(v["b"]) * d + R * d == whole(v["c"]) and m.group(1) == frac(R)
                  and m.group(2) == (one if R <= 1 else many))
        elif typ == "4":
            got = gen.read(T4_ANSWER[story], ans) if story == "days" else gen.read("{x} {crew}", ans)
            W1 = whole(v["W1"] if "W1" in v else v["W1w"])
            R = whole(v["J1"]) / (W1 * whole(v["D1"]))
            if story == "days":                                        # R W2 T = J2
                x = whole(v["J2"]) / (R * whole(v["W2"]))
            else:                                                      # R W D2 = J2
                x = whole(v["J2"]) / (R * whole(v["D2"]))
                ok_word = got["crew"] == v["crew"]
            ok = got["x"] == rounded(x) and (story == "days" or ok_word)
        else:
            m = re.fullmatch(r"(\d+(?:\.\d+)?) days", ans)
            R = whole(v["G1"]) / (whole(v["I1"]) * whole(v["D1"]))     # R T I = G
            x = (whole(v["G1"]) + whole(v["G2"])) / (R * (whole(v["I1"]) + whole(v["I2"])))
            ok = m.group(1) == rounded(x)
    except (ValueError, KeyError, AttributeError, ZeroDivisionError, TypeError):
        return "unchecked"
    return "checked" if ok else "failed"

def answer_of(typ, story, prompt):
    return solve(typ, story, gen.read(template(typ, story), prompt))

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: words, with fractions set as math
# ------------------------------------------------------------------
FRACTION = re.compile(r"(?<![\w/.])(\d+ )?(\d+/\d+)(?![\w/])")

def marked(s):
    """Escaped words, each fraction or mixed number in Typst math, full size:
    1 1/2 is $1 display(1/2)$, 207/29 is $display(207/29)$."""
    return FRACTION.sub(lambda m: f"${m.group(1) or ''}display({m.group(2)})$", esc(s))

def typst(p, gap="0.3em"):
    return marked(p["prompt"])

def answer_typst(p):
    return marked(p["answer"])

def text(p):
    return p["prompt"]

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.2 * (1 + len(p["prompt"]) // 90)

# ------------------------------------------------------------------
# Editing: change the numbers and names; keep the words
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    gen.read(template(old["type"], old["story"]), t)      # ValueError: keep the story's words
    try:
        answer = answer_of(old["type"], old["story"], t)
    except (ValueError, KeyError, ZeroDivisionError):
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
