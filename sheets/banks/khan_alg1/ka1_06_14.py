"""Khan Algebra 1, Lesson 6-14: Systems of equations word problems, from the
old app's Alg1_06_14 (fifteen generated stories).

Khan's fifteen stories, retold with names and no pronouns. Type 1 has two
totals (prices of chickens and ducks from two sales, a stone's time in air
and water from its total time and distance, doses of two vaccines). Type 2
has a total and a comparison (twice as many babies as adults, three fir
trees taller than a pine, a ratio of seats). Every answer is a whole number,
or money, or hours in quarters, built backward from the answer.

A problem: dict(type, story, prompt, answer, source); prompt and answer are words.
check() reads the numbers back out of the story, builds the story's system,
solves it, and requires the key's values (stories.key).
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...typst import esc
from . import courses
from .stories import money, show, fill_story, key, solve_story

NAME = FAMILY = "ka1_06_14"
FIXED = False
TITLE = "Lesson 6-14: Systems of equations word problems"
INSTRUCTIONS = "Write a system of equations, and solve it."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Two Totals",
         look="Two totals, each made of the same two unknowns: two sales, a total time and a total distance.",
         move="Let a letter stand for each unknown. Write one equation for each total, then solve the system.",
         width="full"),
    dict(key="2", title="A Total and a Comparison",
         look="One total, and a sentence comparing the two unknowns: twice as many, 6 meters taller, a ratio.",
         move="Write one equation for the total and one for the comparison. Substitution is often quickest.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="2in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
TIMES = {2: "twice", 3: "three times", 4: "four times", 5: "five times"}
TIMES_OF = {w: k for k, w in TIMES.items()}

def name(r):
    return r.choice(gen.NAMES)

def two_names(r):
    a, b = r.sample(gen.NAMES, 2)
    return a, b

# ------------------------------------------------------------------
# Type 1: two totals
# ------------------------------------------------------------------
def d_chickens(r):
    C, D = r.randint(4, 10), r.randint(4, 10)
    need(C != D)
    c1, d1, c2, d2 = r.randint(30, 60), r.randint(20, 40), r.randint(30, 60), r.randint(20, 40)
    need(c1 * d2 != c2 * d1)
    return dict(name=name(r), c1=c1, d1=d1, r1=c1 * C + d1 * D, c2=c2, d2=d2, r2=c2 * C + d2 * D)

def d_stone(r):
    sa, sw = r.randint(15, 30), r.randint(2, 6)
    ta, tw = r.randint(2, 6), r.randint(2, 8)
    return dict(sa=sa, sw=sw, dist=sa * ta + sw * tw, time=ta + tw)

def d_sushi(r):
    chefs, cust = r.randint(3, 8), r.randint(10, 30)
    pr, pv, er, ev = r.randint(20, 40), r.randint(10, 25), r.randint(1, 3), r.randint(1, 2)
    lr, lv = pr * chefs - er * cust, pv * chefs - ev * cust
    need(lr > 0 and lv > 0 and pr * ev != pv * er)
    return dict(pr=pr, pv=pv, er=er, ev=ev, lr=lr, lv=lv)

def d_milk(r):
    m, b = F(r.randrange(100, 300, 5), 100), F(r.randrange(150, 450, 5), 100)
    m1, b1, m2, b2 = r.randint(2, 6), r.randint(2, 5), r.randint(2, 6), r.randint(2, 5)
    need(m1 * b2 != m2 * b1)
    return dict(name=name(r), m1=m1, b1=b1, t1=money(m1 * m + b1 * b), m2=m2, b2=b2, t2=money(m2 * m + b2 * b))

def d_jetpack(r):
    rs, js = r.randint(6, 12), r.randint(40, 90)
    tr, tj = F(r.choice((1, 2, 3, 5, 6)), 4), F(r.choice((1, 2, 3, 5, 6)), 4)     # never 1 hour ("1 hours")
    return dict(name=name(r), rs=rs, js=js, dist=show(rs * tr + js * tj), time=show(tr + tj))

def d_vaccines(r):
    dp, dm = r.randint(2, 4), r.randint(1, 3)
    need(dp != dm)
    P, M = r.randint(50, 300), r.randint(50, 300)
    return dict(name=name(r), dp=dp, dm=dm, vac=P + M, doses=dp * P + dm * M)

def d_portugal(r):
    wp, wb = r.randint(40, 90), r.randint(40, 90)
    need(wp != wb)
    tp, tb = r.randint(2, 12), r.randint(2, 12)
    return dict(name=name(r), months=tp + tb, wp=wp, wb=wb, words=wp * tp + wb * tb)

def d_jobs(r):
    rc, rb = r.randint(15, 35), r.randint(15, 35)
    need(rc != rb)
    hc, hb = r.randint(5, 25), r.randint(5, 25)
    return dict(name=name(r), rc=rc, rb=rb, hours=hc + hb, earned=rc * hc + rb * hb)

# ------------------------------------------------------------------
# Type 2: a total and a comparison
# ------------------------------------------------------------------
def d_dinosaurs(r):
    adults, k = r.randint(2, 6), r.randint(2, 5)
    pb, pa = r.randint(12, 20), r.randint(5, 10)
    return dict(pb=pb, pa=pa, total=pb * k * adults + pa * adults, times=TIMES[k])

def d_trees(r):
    f, p, k = r.randint(5, 20), r.randint(10, 40), r.randint(2, 4)
    need(k * f > p)
    return dict(name=name(r), sum=f + p, k=k, taller=k * f - p)

def d_race(r):
    a, b = two_names(r)
    s1, s2 = r.randint(20, 60), r.randint(20, 60)
    need((s1 + s2) % 2 == 0 and 2 * s1 > s2)
    return dict(a=a, b=b, average=(s1 + s2) // 2, more=2 * s1 - s2)

def d_languages(r):
    h, p = r.randint(90, 150), r.randint(90, 150)
    th, tp = r.randint(2, 12), r.randint(2, 12)
    diff = p * tp - h * th
    need(diff != 0 and h != p)
    return dict(name=name(r), h=h, p=p, time=th + tp, diff=abs(diff), cmp="more" if diff > 0 else "fewer")

def d_okapi(r):
    o, l, n = r.randint(200, 300), r.randint(100, 180), r.randint(2, 3)
    diff = n * l - o
    need(diff != 0)
    return dict(sum=o + l, n=n, diff=abs(diff), cmp="more" if diff > 0 else "less")

def d_seats(r):
    e, b = r.randint(3, 9), r.randint(1, 3)
    need(e % b and e > b)
    k = r.randint(5, 20)
    return dict(total=(e + b) * k, e=e, b=b)

def d_walk(r):
    ws, bs = r.randint(3, 6), r.randint(30, 60)
    tw, tb = F(r.randint(1, 3), 4), F(r.choice((1, 2, 3, 5)), 4)
    return dict(name=name(r), ws=ws, bs=bs, dist=show(ws * tw + bs * tb), time=show(tw + tb))

STORIES = [
    dict(key="a", type="1", text="{name} breeds chickens and ducks. Last month, {name} sold {c1} chickens and {d1} ducks for "
         "${r1}. This month, {name} sold {c2} chickens and {d2} ducks for ${r2}, at the same prices.",
         ask="How much does a chicken cost, and how much does a duck cost?",
         answer="A chicken costs ${u} and a duck costs ${v}.", draw=d_chickens, fmt=money,
         model=lambda n: ((n["c1"], n["d1"], n["r1"]), (n["c2"], n["d2"], n["r2"]))),
    dict(key="b", type="1", text="A stone fell from the top of a cliff into the ocean. In the air, it had an average speed of "
         "{sa} m/s. In the water, it had an average speed of {sw} m/s before hitting the seabed. The total distance from "
         "the top of the cliff to the seabed is {dist} meters, and the stone's entire fall took {time} seconds.",
         ask="How long did the stone fall in the air, and how long did it fall in the water?",
         answer="The stone fell in the air for {u} seconds and in the water for {v} seconds.", draw=d_stone,
         model=lambda n: ((1, 1, n["time"]), (n["sa"], n["sw"], n["dist"]))),
    dict(key="c", type="1", text="Each chef at Sushi Emperor prepares {pr} regular rolls and {pv} vegetarian rolls daily. On "
         "Tuesday, each customer ate {er} regular rolls and {ev} vegetarian rolls. By the end of the day, {lr} regular "
         "rolls and {lv} vegetarian rolls were left uneaten.",
         ask="How many chefs and how many customers were at Sushi Emperor on Tuesday?",
         answer="There were {u} chefs and {v} customers.", draw=d_sushi,
         model=lambda n: ((n["pr"], -n["er"], n["lr"]), (n["pv"], -n["ev"], n["lv"]))),
    dict(key="d", type="1", text="{name} bought {m1} liters of milk and {b1} loaves of bread for a total of ${t1}. A month "
         "later, {name} bought {m2} liters of milk and {b2} loaves of bread at the same prices, for a total of ${t2}.",
         ask="How much does a liter of milk cost, and how much does a loaf of bread cost?",
         answer="A liter of milk costs ${u} and a loaf of bread costs ${v}.", draw=d_milk, fmt=money,
         model=lambda n: ((n["m1"], n["b1"], n["t1"]), (n["m2"], n["b2"], n["t2"]))),
    dict(key="e", type="1", text="{name} ran from home to a secret laboratory at an average speed of {rs} km/h, then flew a "
         "jetpack to school at an average speed of {js} km/h. {name} traveled {dist} kilometers in all, and the whole "
         "trip took {time} hours.",
         ask="How long did {name} spend running, and how long flying?",
         answer="{name} ran for {u} hours and flew for {v} hours.", draw=d_jetpack,
         model=lambda n: ((1, 1, n["time"]), (n["rs"], n["js"], n["dist"]))),
    dict(key="f", type="1", text="Dr. {name} gives vaccinations against polio and measles. Each polio vaccination is {dp} "
         "doses, and each measles vaccination is {dm} doses. Last year, Dr. {name} gave {vac} vaccinations, {doses} "
         "doses in all.",
         ask="How many polio vaccinations and how many measles vaccinations did Dr. {name} give last year?",
         answer="Dr. {name} gave {u} polio vaccinations and {v} measles vaccinations.", draw=d_vaccines,
         model=lambda n: ((1, 1, n["vac"]), (n["dp"], n["dm"], n["doses"]))),
    dict(key="g", type="1", text="{name} lived in Portugal and Brazil for {months} months in all to learn Portuguese, "
         "learning an average of {wp} new words a month in Portugal and {wb} in Brazil: {words} new words in all.",
         ask="How long did {name} live in Portugal, and how long in Brazil?",
         answer="{name} lived in Portugal for {u} months and in Brazil for {v} months.", draw=d_portugal,
         model=lambda n: ((1, 1, n["months"]), (n["wp"], n["wb"], n["words"]))),
    dict(key="h", type="1", text="{name} works as a carpenter and as a blacksmith, earning ${rc} an hour as a carpenter and "
         "${rb} an hour as a blacksmith. Last week, {name} worked {hours} hours at the two jobs and earned ${earned}.",
         ask="How many hours did {name} work as a carpenter last week, and how many as a blacksmith?",
         answer="{name} worked {u} hours as a carpenter and {v} hours as a blacksmith.", draw=d_jobs,
         model=lambda n: ((1, 1, n["hours"]), (n["rc"], n["rb"], n["earned"]))),
    dict(key="i", type="1", text="{name} walked from home to the bus stop at an average speed of {ws} km/h, then rode the "
         "school bus at an average speed of {bs} km/h. The trip from home to school is {dist} kilometers, and it took "
         "{time} hours.",
         ask="How many hours did {name} walk, and how many did {name} ride the bus?",
         answer="{name} walked for {u} hours and rode the bus for {v} hours.", draw=d_walk,
         model=lambda n: ((1, 1, n["time"]), (n["ws"], n["bs"], n["dist"]))),
    dict(key="j", type="2", text="A herd of dinosaurs made paintings in the sand with their claws. Each baby dinosaur made "
         "{pb} paintings and each adult made {pa}. The herd made {total} paintings in all, and there were {times} as "
         "many babies as adults.",
         ask="How many baby dinosaurs and how many adult dinosaurs were there?",
         answer="There were {u} babies and {v} adults.", draw=d_dinosaurs,
         model=lambda n: ((n["pb"], n["pa"], n["total"]), (1, -TIMES_OF[n["times"]], 0))),
    dict(key="k", type="2", text="{name} engineered a new kind of fir tree and a new kind of pine tree. One fir tree and one "
         "pine tree together are {sum} meters tall. Stacked on top of each other, {k} fir trees are {taller} "
         "meters taller than one pine tree.",
         ask="How tall is each kind of tree?",
         answer="A fir tree is {u} meters tall and a pine tree is {v} meters tall.", draw=d_trees,
         model=lambda n: ((1, 1, n["sum"]), (n["k"], -1, n["taller"]))),
    dict(key="l", type="2", text="{a} and {b} raced each other. The average of their top speeds was {average} km/h. "
         "Doubled, {a}'s top speed would be {more} km/h more than {b}'s.",
         ask="What were {a}'s and {b}'s top speeds?",
         answer="{a}'s top speed was {u} km/h and {b}'s was {v} km/h.", draw=d_race,
         model=lambda n: ((1, 1, 2 * n["average"]), (2, -1, n["more"]))),
    dict(key="m", type="2", text="{name} speaks {h} words a minute in Hungarian and {p} words a minute in Polish. {name} "
         "gave cooking instructions in Hungarian and then cleaning instructions in Polish, {time} minutes in all, "
         "and spoke {diff} {cmp} words in Polish than in Hungarian.",
         ask="How many minutes did {name} speak in Hungarian, and how many in Polish?",
         answer="{name} spoke for {u} minutes in Hungarian and {v} minutes in Polish.", draw=d_languages,
         model=lambda n: ((1, 1, n["time"]), (-n["h"], n["p"], n["diff"] if n["cmp"] == "more" else -n["diff"]))),
    dict(key="n", type="2", text="An okapi and a llama together weigh {sum} kilograms, on average. The average weight of "
         "{n} llamas is {diff} kilograms {cmp} than the average weight of one okapi.",
         ask="On average, how much does an okapi weigh, and how much does a llama weigh?",
         answer="An okapi weighs {u} kilograms and a llama {v} kilograms.", draw=d_okapi,
         model=lambda n: ((1, 1, n["sum"]), (-1, n["n"], n["diff"] if n["cmp"] == "more" else -n["diff"]))),
    dict(key="o", type="2", text="A plane has {total} seats, in economy class and business class. For every {e} seats in "
         "economy class, there are {b} in business class.",
         ask="How many seats are in each class?",
         answer="There are {u} economy seats and {v} business seats.", draw=d_seats,
         model=lambda n: ((1, 1, n["total"]), (n["b"], -n["e"], 0))),
]
STORY = {s["key"]: s for s in STORIES}
BY_TYPE = {k: [s for s in STORIES if s["type"] == k] for k in KEYS}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    st = BY_TYPE[entry][tpl]
    prompt = fill_story(st, st["draw"](r))
    return dict(story=st["key"], prompt=prompt, answer=key(st, prompt))

def check(p):
    try:
        st = STORY[p["story"]]
        return "checked" if " ".join(p["answer"].split()) == key(st, p["prompt"]) else "failed"
    except (ValueError, KeyError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(BY_TYPE[e]))
typst, answer_typst, text, answer_text, height = gen.text_shown()

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    st = STORY[old["story"]]
    try:
        answer = key(st, t)
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
