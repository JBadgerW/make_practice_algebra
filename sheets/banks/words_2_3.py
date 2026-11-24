"""Lesson 2-3's word problems, Types 5 to 12: not a bank of its own (no NAME), but the
part of forms_2_3 that writes, checks, and shows them. Each type is one of the teacher's
word problems (~/Documents/alg1/unit_2/lesson_2-3_Standard_Form/2-3_word_problems.md),
with the same logic in four stories ("a" is the source's own setting; Type 5's "b" is
problem 3's) and new numbers and names every draw. Type 11 is bare math, one setting.

    Type  source  the logic                                         the key
    5     1, 3    two prices and a total to spend                    25 x + 10 y = 150
    6     2       a total, two prices, about the same amount of each 10 x + 12 y = 30; x = y = 15/11, about 1.36 lb
    7     4       only one item, only the other, a mix of both       10 lb; 6 lb; 5 lb and 3 lb; 3 x + 5 y = 30
    8     5       the space each animal needs in a pen; is every     100 x + 20 y = 2500; no, whole numbers only;
                  solution possible; about k times as many           15 goats and 45 chickens, validated
    9     6       a budget for two items; is every point viable      20 x + 12 y = 300; no: the whole-number points
    10    7       prices with cents: choose the standard form        5 x + 8 y = 100, among the source's three
                                                                     shufflings of its numbers (one letter)
    11    8       a fractional equation: choose the standard form    9 x + 16 y = 120, among slope-intercept,
                                                                     point-slope, the given, half-cleared (a letter)
    12    9       three items, a budget, use two: each mixture's     2 x + 3 y = 32 for each pair; each pair's
                  equation, its range of amounts, which reach T      range of cups; the pairs with the cheapest item

The model equation: x and y are the story's two amounts (it says which), and the key writes
a x + b y = c with the story's own numbers when they are whole (25 x + 10 y = 150, not
reduced, so the prices stay visible) and cleared of decimals by the smallest whole number
that does it when they aren't (2.50 and 4, 50: 5 x + 8 y = 100), as source 7's answer does.
An edited answer may be any whole-number multiple of the line (5 x + 2 y = 30). No pronouns:
a name is repeated.

A problem: dict(type, story, prompt, answer[, choices], source), as in words_2_2: the prompt
is the story's words (Type 11: the equation alone); the answer its parts, "; " between
(Types 10, 11: a letter). check() reads the numbers back out of the words with the story's
own template, solves forward from them, and compares each equation by its line and form,
each sentence word for word, and (Types 10, 11) each choice by reading it strictly as
standard form: exactly one may be the story's line.
"""
import math
import re
from fractions import Fraction as F
from .. import gen
from ..gen import need, written
from .words_2_1 import num, cents, number, mixed, math_letters
from .words_2_2 import money, table

TYPES_ = ("5", "6", "7", "8", "9", "10", "11", "12")
STORIES = "abcd"
WORDS = ("who",)
CHOICE = ("10", "11")                      # multiple choice, one letter
PART = re.compile(r"(?<=[.?]) (?=[A-D]\. )")   # a new line before each part, A. to D.

TYPES = [
    dict(key="5", title="Word Problems: Two Prices and a Total",
         instructions="Write a linear equation in standard form for each situation.",
         look="Two prices and a total amount to spend: reserved seats at 25 dollars, general admission at 10 "
              "dollars, 150 dollars in all.",
         move="Cost of the first item plus cost of the second is the total: price times $x$ plus price times $y$. "
              "$25 x + 10 y = 150$.",
         width="full", space="1in"),
    dict(key="6", title="Word Problems: About the Same Amount of Each",
         instructions="Answer each part. Write each equation in standard form.",
         look="A total to spend on a mix of two items, their prices, and about the same amount of each.",
         move="Write the model, $10 x + 12 y = 30$. The same amount of each means $y = x$: $10 x + 12 x = 30$, "
              "so $22 x = 30$ and $x = 15/11 approx 1.36$.",
         width="full", space="1.4in"),
    dict(key="7", title="Word Problems: Only One, Only the Other, or a Mix",
         instructions="Answer each part. Write each equation in standard form.",
         look="A total to spend on a mix of two items, and questions about buying only one, only the other, or "
              "some of both.",
         move="Only the first item means $y = 0$: $3 x = 30$, $x = 10$, the $x$-intercept. Only the second means "
              "$x = 0$: $5 y = 30$, $y = 6$. A mix is any point between: $3(5) + 5(3) = 30$. The model is "
              "$3 x + 5 y = 30$.",
         width="full", space="1.8in"),
    dict(key="8", title="Word Problems: Sharing a Space",
         instructions="Answer each part. Write each equation in standard form.",
         look="A pen of a given size, the space each kind of animal needs, and about how many times as many of "
              "one kind as the other.",
         move="Area of the pen: $50 dot 50 = 2500$. Space used: $100 x + 20 y = 2500$. Animals come in whole "
              "numbers, 0 or more. With $y = 3 x$: $160 x = 2500$, $x = 15.625$, so 15 goats and 45 chickens, "
              "and $100(15) + 20(45) = 2400 <= 2500$.",
         width="full", space="2in"),
    dict(key="9", title="Word Problems: Which Points Are Viable?",
         instructions="Answer each part. Write each equation in standard form.",
         look="A budget for two items sold one at a time, and whether every point on the graph makes sense.",
         move="The model: $20 x + 12 y = 300$. Only whole numbers of items, 0 or more, can be bought, so only "
              "the line's points with whole-number coordinates are viable: $(0, 25)$, $(3, 20)$, ..., $(15, 0)$.",
         width="full", space="1.6in"),
    dict(key="10", title="Word Problems: Choosing the Equation in Standard Form",
         instructions="Choose the equation in standard form for each situation.",
         look="Prices with cents, like 2.50 dollars and 4 dollars a pound, and 50 dollars to spend.",
         move="Write $2.5 x + 4 y = 50$, then multiply by the smallest number that clears the decimals ($2$): "
              "$5 x + 8 y = 100$. Standard form has whole-number $A$, $B$, $C$ and $x$ and $y$ on the left.",
         width="full", space="0.5in"),
    dict(key="11", title="Fractions to Standard Form",
         instructions="Choose the equation written in standard form.",
         look="An equation like $3/8 x + 2/3 y = 5$, with fractions for coefficients.",
         move="Multiply every term by the least common denominator, $24$: $9 x + 16 y = 120$. Clearing only "
              "one fraction ($3 x + 16/3 y = 40$) isn't enough.",
         width="full", space="0.5in"),
    dict(key="12", title="Word Problems: Three Items, Two at a Time",
         instructions="Answer each part. Write each equation in standard form.",
         look="A table of three items' prices, a budget, a mix of two of them, and an amount needed.",
         move="Each pair of items is a mixture with its own equation: $0.50 x + 0.75 y = 8$, or $2 x + 3 y = "
              "32$. Its amounts run from all of the dearer item ($8 / 0.75 = 10 2/3$ cups) to all of the "
              "cheaper ($8 / 0.50 = 16$). Only a pair that can reach the amount needed works.",
         width="full", space="2.4in"),
]

# ------------------------------------------------------------------
# The model equation: a x + b y = c, whole numbers
# ------------------------------------------------------------------
def cleared(*qs):
    """The numbers times the smallest whole number that makes them all whole."""
    n = math.lcm(*(F(q).denominator for q in qs))
    return tuple(int(F(q) * n) for q in qs)

def model(a, b, c):
    """"25 x + 10 y = 150"; "5 x + 8 y = 100" for 2.50, 4, 50; a coefficient of 1 left off."""
    A, B, C = cleared(a, b, c)
    return f"{written((A, 'x'), (B, 'y'))} = {C}"

COEF = r"(?:[1-9]\d* )?"
MODEL = re.compile(rf"(?P<a>{COEF})x \+ (?P<b>{COEF})y = (?P<c>[1-9]\d*)")

def read_model(t):
    """(a, b, c) of A x + B y = C with positive whole numbers, 1 left off; None if not."""
    g = MODEL.fullmatch(" ".join(t.replace("−", "-").split()))
    if not g:
        return None
    a, b = (F(1) if not s.strip() else F(int(s)) for s in (g["a"], g["b"]))
    return a, b, F(int(g["c"]))

def same_line(got, want):
    """Two (a, b, c)s are one line: a positive multiple."""
    return got is not None and got[0] * want[1] == got[1] * want[0] and got[0] * want[2] == got[2] * want[0]

def hundredths(q):
    """Rounded half up: 1.36."""
    return cents(F(math.floor(q * 100 + F(1, 2)), 100)).rstrip("0").rstrip(".")

def exact_or_about(q, places=3):
    """("1.5", True) when q ends within `places` decimal places; else ("15/11 ≈ 1.36", False)."""
    if (q * 10 ** places).denominator == 1:
        return num(q), True
    return f"{q.numerator}/{q.denominator} ≈ {hundredths(q)}", False

def listed(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + (", and " if len(items) > 2 else " and ") + items[-1]

def steps(lo, hi, by):
    return [F(n, 100) for n in range(int(lo * 100), int(hi * 100) + 1, int(by * 100))]

# ------------------------------------------------------------------
# The stories. text has {placeholders} for names and numbers; the rest of a
# story's fields are its fixed words.
# ------------------------------------------------------------------
S5 = {
    "a": dict(a=(15, 40, 5), b=(5, 20, 5), c=(100, 400, 10), count=True,
              text="{who} will spend ${c} on music festival tickets. Reserved seat tickets cost ${a} and general "
                   "admission tickets cost ${b}.",
              ask=" Let x be the number of reserved seat tickets and y the number of general admission tickets. "
                  "How can you represent the situation with a linear equation in standard form?"),
    "b": dict(a=(2, 6, 1), b=(2, 6, 1), c=(10, 30, 1), count=False,
              text="{who} has ${c} to spend on a mixture of green and red grapes. Green grapes cost ${a} per pound "
                   "and red grapes cost ${b} per pound.",
              ask=" Let x be the pounds of green grapes and y the pounds of red grapes. What equation in standard "
                  "form can {who} use to graph a line showing the different amounts of each grape {who} can buy "
                  "for ${c}?"),
    "c": dict(a=(8, 20, 1), b=(2, 6, 1), c=(60, 200, 10), count=True,
              text="{who} has ${c} to spend on plants for a school garden. Flats of flowers cost ${a} each and "
                   "tomato plants cost ${b} each.",
              ask=" Let x be the number of flats of flowers and y the number of tomato plants. How can you "
                  "represent the situation with a linear equation in standard form?"),
    "d": dict(a=(3, 9, 1), b=(2, 6, 1), c=(15, 50, 1), count=False,
              text="{who} has ${c} to spend on a mixture of peanuts and pretzels for a party. Peanuts cost ${a} per "
                   "pound and pretzels cost ${b} per pound.",
              ask=" Let x be the pounds of peanuts and y the pounds of pretzels. What equation in standard form can "
                  "{who} use to graph a line showing the different amounts of each {who} can buy for ${c}?"),
}

ASK_6 = (" Let x be the pounds of {xn} and y the pounds of {yn}. A. Write a linear equation in standard form for the "
         "amounts {{who}} can buy. B. How can {{who}} determine how many pounds of each kind of {kind} to buy? How "
         "many pounds of each should {{who}} buy?")
S6 = {
    "a": dict(xn="almonds", yn="cashews", kind="nut",
              text="{who} is making trail mix. {who} has ${c} to spend on a mixture of almonds and cashews and wants "
                   "about the same amount of almonds as cashews. Almonds cost ${a} per pound and cashews cost ${b} "
                   "per pound."),
    "b": dict(xn="strawberries", yn="blueberries", kind="berry",
              text="{who} is making a fruit salad. {who} has ${c} to spend on a mixture of strawberries and "
                   "blueberries and wants about the same amount of strawberries as blueberries. Strawberries cost "
                   "${a} per pound and blueberries cost ${b} per pound."),
    "c": dict(xn="gummy bears", yn="chocolate drops", kind="candy",
              text="{who} is filling party bags. {who} has ${c} to spend on a mixture of gummy bears and chocolate "
                   "drops and wants about the same amount of gummy bears as chocolate drops. Gummy bears cost ${a} "
                   "per pound and chocolate drops cost ${b} per pound."),
    "d": dict(xn="Colombian beans", yn="Kenyan beans", kind="coffee bean",
              text="{who} is blending coffee for a café. {who} has ${c} to spend on a mixture of Colombian beans and "
                   "Kenyan beans and wants about the same amount of Colombian beans as Kenyan beans. Colombian beans "
                   "cost ${a} per pound and Kenyan beans cost ${b} per pound."),
}
for _s in S6.values():
    _s["ask"] = ASK_6.format(**_s)

ASK_7 = (" Let x be the pounds of {xn} and y the pounds of {yn}. A. How many pounds of {kind} can {{who}} buy if "
         "{{who}} buys only {xn}? B. How many pounds if {{who}} buys only {yn}? C. What is one mixture of both that "
         "{{who}} can buy? D. What linear equation in standard form can {{who}} use to model the situation?")
S7 = {
    "a": dict(xn="Cheddar cheese", yn="Swiss cheese", xs="Cheddar", ys="Swiss", kind="cheese",
              text="{who} is catering a luncheon. {who} has ${c} to spend on a mixture of Cheddar cheese and Swiss "
                   "cheese. Cheddar cheese costs ${a} per pound and Swiss cheese costs ${b} per pound."),
    "b": dict(xn="turkey", yn="ham", xs="turkey", ys="ham", kind="meat",
              text="{who} is making sandwich trays for a meeting. {who} has ${c} to spend on a mixture of sliced "
                   "turkey and sliced ham. Turkey costs ${a} per pound and ham costs ${b} per pound."),
    "c": dict(xn="sunflower seed", yn="millet", xs="sunflower seed", ys="millet", kind="seed",
              text="{who} is filling the bird feeders at a nature center. {who} has ${c} to spend on a mixture of "
                   "sunflower seed and millet. Sunflower seed costs ${a} per pound and millet costs ${b} per pound."),
    "d": dict(xn="fudge", yn="taffy", xs="fudge", ys="taffy", kind="candy",
              text="{who} is making gift boxes for a fundraiser. {who} has ${c} to spend on a mixture of fudge and "
                   "taffy. Fudge costs ${a} per pound and taffy costs ${b} per pound."),
}
for _s in S7.values():
    _s["ask"] = ASK_7.format(**_s)

ASK_8 = (" Let x be the number of {xs} and y the number of {ys}. A. Write an equation in standard form to model the "
         "situation. B. Is every solution of the equation a solution of the situation? Explain. C. {{who}} wants "
         "about {{k}} times as many {ys} as {xs}. How many of each {kind} could {{who}} have? Validate your "
         "solution.")
S8 = {
    "a": dict(xs="goats", ys="chickens", kind="animal", place="pen", square=True, side=(30, 70, 5),
              g=(60, 150, 10), h=(10, 30, 5), k=(2, 4),
              text="{who} has a {l} ft by {l} ft square pen in the yard to raise goats and chickens. The goats need "
                   "{g} ft² each and the chickens need {h} ft² each."),
    "b": dict(xs="tomato plants", ys="pepper plants", kind="plant", place="garden", square=False, side=(10, 30, 2),
              g=(6, 12, 1), h=(2, 5, 1), k=(2, 4),
              text="{who} is planting a {l} ft by {w} ft garden with tomato plants and pepper plants. Each tomato "
                   "plant needs {g} ft² and each pepper plant needs {h} ft²."),
    "c": dict(xs="large booths", ys="small booths", kind="booth", place="floor", square=False, side=(50, 120, 10),
              g=(100, 200, 10), h=(40, 80, 5), k=(2, 4),
              text="{who} is planning a craft fair on a {l} ft by {w} ft gym floor with large booths and small "
                   "booths. Each large booth needs {g} ft² and each small booth needs {h} ft²."),
    "d": dict(xs="bus spaces", ys="car spaces", kind="space", place="lot", square=False, side=(100, 200, 10),
              g=(400, 600, 20), h=(150, 200, 10), k=(4, 8),
              text="{who} is laying out a {l} ft by {w} ft parking lot at a fairground with bus spaces and car "
                   "spaces. Each bus space needs {g} ft² and each car space needs {h} ft²."),
}
for _s in S8.values():
    _s["ask"] = ASK_8.format(**_s)

ASK_9 = (" Let x be the number of {xs} and y the number of {ys}. A. What equation in standard form can {{who}} use to "
         "determine the number of {ys} and {xs} {{who}} can order for ${{c}}? B. If {{who}} sketched a graph of the "
         "linear equation, would every point on the graph represent a viable solution? Explain.")
S9 = {
    "a": dict(xs="T-shirts", ys="caps", a=(15, 30), b=(6, 15), c=(150, 400, 10),
              text="{who}, a summer camp counselor, has a budget of ${c} to spend on caps and T-shirts for a summer "
                   "camp. T-shirts cost ${a} each and caps cost ${b} each."),
    "b": dict(xs="basketballs", ys="jump ropes", a=(18, 35), b=(4, 12), c=(120, 300, 10),
              text="{who}, a basketball coach, has a budget of ${c} to spend on jump ropes and basketballs for the "
                   "team. Basketballs cost ${a} each and jump ropes cost ${b} each."),
    "c": dict(xs="hardcover books", ys="paperback books", a=(15, 30), b=(5, 12), c=(150, 360, 10),
              text="{who}, a school librarian, has a budget of ${c} to spend on paperback books and hardcover books. "
                   "Hardcover books cost ${a} each and paperback books cost ${b} each."),
    "d": dict(xs="hoodies", ys="water bottles", a=(20, 40), b=(6, 15), c=(200, 500, 10),
              text="{who}, the band boosters' treasurer, has a budget of ${c} to spend on water bottles and hoodies "
                   "for the band. Hoodies cost ${a} each and water bottles cost ${b} each."),
}
for _s in S9.values():
    _s["ask"] = ASK_9.format(**_s)

ASK_10 = (" Let x be the pounds of {xn} and y the pounds of {yn}. Select the equation in standard form that "
          "represents how many pounds of each {kind} {{who}} can buy.")
S10 = {
    "a": dict(xn="oranges", yn="pineapple", kind="kind of fruit", a=(1, 4), b=(2, 6), c=(20, 80),
              text="{who} has ${c} to spend on a fruit salad for a party. Oranges cost ${a} per pound and pineapple "
                   "costs ${b} per pound."),
    "b": dict(xn="rice", yn="beans", kind="food", a=(1, 3), b=(1, 4), c=(20, 60),
              text="{who} has ${c} to spend on rice and dried beans for a food drive. Rice costs ${a} per pound and "
                   "dried beans cost ${b} per pound."),
    "c": dict(xn="ground beef", yn="chicken", kind="meat", a=(3, 7), b=(2, 6), c=(40, 100),
              text="{who} has ${c} to spend on ground beef and chicken for a cookout. Ground beef costs ${a} per "
                   "pound and chicken costs ${b} per pound."),
    "d": dict(xn="apples", yn="pears", kind="kind of fruit", a=(1, 3), b=(1, 4), c=(15, 50),
              text="{who} has ${c} to spend on apples and pears for baking pies. Apples cost ${a} per pound and "
                   "pears cost ${b} per pound."),
}
for _s in S10.values():
    _s["ask"] = ASK_10.format(**_s)

S11 = {"a": dict(text="{eq}", ask="")}

ASK_12 = (" A. What are the possible combinations of {kinds} that {{who}} can buy? Write a linear equation to model "
          "how many {units} of {kind} {{who}} can buy for each possible mixture, with x the {units} of the first "
          "{one} named and y the {units} of the second. B. What are the possible amounts of {kind}, in {units}, that "
          "{{who}} can buy for each mixture in part A? C. {{who}} wants to use at least {{T}} {units} of {kind} to "
          "{goal}. Which mixtures will allow {{who}} to have enough and still stay within the budget? Explain your "
          "reasoning.")
S12 = {
    "a": dict(items=("mango", "pineapple", "strawberry"), kind="fruit", one="fruit", kinds="fruit", unit="cup", units="cups",
              price=(0.25, 2, 0.25), c=(6, 16), goal="make the batch of smoothies",
              text="{who} has a total of ${c} to spend to make fruit smoothies. {who} will use two types of fruit. "
                   "The cost of each type of fruit per cup: mango, ${p1}; pineapple, ${p2}; strawberry, ${p3}."),
    "b": dict(items=("apple", "cranberry", "grape"), kind="juice", one="juice", kinds="juice", unit="quart", units="quarts",
              price=(1, 4, 0.25), c=(12, 30), goal="make the punch",
              text="{who} has a total of ${c} to spend to make punch for a party. {who} will use two types of juice. "
                   "The cost of each type of juice per quart: apple, ${p1}; cranberry, ${p2}; grape, ${p3}."),
    "c": dict(items=("peanuts", "raisins", "walnuts"), kind="trail mix", one="ingredient", kinds="ingredients", unit="pound",
              units="pounds", price=(2, 8, 0.5), c=(20, 48), goal="fill the hiking club's bags",
              text="{who} has a total of ${c} to spend to make trail mix for a hiking club. {who} will use two of "
                   "the ingredients. The cost of each ingredient per pound: peanuts, ${p1}; raisins, ${p2}; "
                   "walnuts, ${p3}."),
    "d": dict(items=("topsoil", "compost", "peat moss"), kind="soil", one="soil", kinds="soil", unit="cubic foot",
              units="cubic feet", price=(1, 5, 0.25), c=(20, 60), goal="fill the bed",
              text="{who} has a total of ${c} to spend on soil for a raised garden bed. {who} will use two types of "
                   "soil. The cost of each type of soil per cubic foot: topsoil, ${p1}; compost, ${p2}; peat moss, "
                   "${p3}."),
}
for _s in S12.values():
    _s["ask"] = ASK_12.format(**_s)
    _s["intro"], _, _ = _s["text"].rpartition(" The cost of each")

STORY = {"5": S5, "6": S6, "7": S7, "8": S8, "9": S9, "10": S10, "11": S11, "12": S12}

def stories(typ):
    return len(STORY[typ])

def template(typ, story):
    st = STORY[typ][story]
    return st["text"] + st["ask"]

# ------------------------------------------------------------------
# Drawing: built backward from the answer
# ------------------------------------------------------------------
def rng_step(r, lo, hi, by):
    return F(r.randrange(lo, hi + 1, by))

def draw_5(r, st):
    a, b = rng_step(r, *st["a"]), rng_step(r, *st["b"])
    c = rng_step(r, *st["c"])
    need(a != b and c > a + b)
    if st["count"]:
        need(any((c - a * x) % b == 0 for x in range(1, int(c / a))))      # some whole mix of both
    return dict(who=r.choice(gen.NAMES), a=a, b=b, c=c), dict(abc=(a, b, c))

def draw_6(r, st):
    a, b = F(r.randint(4, 15)), F(r.randint(4, 15))
    c = F(r.randrange(20, 81, 5))
    need(a != b and c >= 2 * (a + b) / 3)
    return dict(who=r.choice(gen.NAMES), a=a, b=b, c=c), dict(each=c / (a + b))

def draw_7(r, st):
    a, b = F(r.randint(2, 12)), F(r.randint(2, 12))
    need(a != b)
    L = math.lcm(int(a), int(b))
    c = F(L * r.randint(1, 6))
    need(20 <= c <= 90 and mixture(a, b, c))
    return dict(who=r.choice(gen.NAMES), a=a, b=b, c=c), dict(only=(c / a, c / b))

def draw_8(r, st):
    l = rng_step(r, *st["side"])
    w = l if st["square"] else rng_step(r, *st["side"])
    need(st["square"] or l != w)
    g, h = rng_step(r, *st["g"]), rng_step(r, *st["h"])
    k = F(r.randint(*st["k"]))
    need(h < g and l * w / (g + k * h) >= 3)
    v = dict(who=r.choice(gen.NAMES), l=l, g=g, h=h, k=k)
    if not st["square"]:
        v["w"] = w
    return v, dict(area=l * w)

def draw_9(r, st):
    a, b = F(r.randint(*st["a"])), F(r.randint(*st["b"]))
    c = rng_step(r, *st["c"])
    need(a > b and 3 <= len(viable(a, b, c)) <= 7)
    return dict(who=r.choice(gen.NAMES), a=a, b=b, c=c), dict(abc=(a, b, c))

def draw_10(r, st):
    a, b = r.choice(steps(*st["a"], 0.25)), r.choice(steps(*st["b"], 0.25))
    c = F(r.randrange(st["c"][0], st["c"][1] + 1, 5))
    A, B, C = cleared(a, b, c)
    need(a.denominator != 1 or b.denominator != 1)
    need(a != b and math.gcd(A, B, C) == 1 and len({A, B, C}) == 3)
    return dict(who=r.choice(gen.NAMES), a=a, b=b, c=c), dict(abc=(a, b, c))

def draw_11(r, st):
    q, s = r.sample(range(2, 10), 2)
    p = r.choice([n for n in range(1, 2 * q) if math.gcd(n, q) == 1])
    t = r.choice([n for n in range(1, 2 * s) if math.gcd(n, s) == 1])
    c = F(r.randint(1, 12))
    a, b = F(p, q), F(t, s)
    need(a.denominator != 1 and b.denominator != 1 and (b * q).denominator != 1)
    m, k = -a / b, c / b
    need(k.denominator <= 4 and m.denominator <= 20)                  # as the source's -9/16 and 15/2
    from . import forms_2_3 as B
    A, Bc, C = B.coefficients(m, k)
    need(max(A, abs(Bc)) <= 30 and abs(C) <= 200)                   # 9 x + 16 y = 120
    return dict(eq=given(a, b, c)), dict(abc=(a, b, c))

def draw_12(r, st):
    ps_ = r.sample(steps(*st["price"]), 3)
    c = F(r.randint(*st["c"]))
    lo, mid = sorted(ps_)[:2]
    Ts = [T for T in range(1, int(c / lo) + 1) if F(T) > c / mid and F(T) <= c / lo]
    need(Ts and all((c / p).denominator <= 4 for p in ps_))          # amounts like 16 and 10 2/3
    return dict(who=r.choice(gen.NAMES), c=c, p1=ps_[0], p2=ps_[1], p3=ps_[2], T=F(r.choice(Ts))), {}

DRAW = {"5": draw_5, "6": draw_6, "7": draw_7, "8": draw_8, "9": draw_9, "10": draw_10, "11": draw_11, "12": draw_12}
CASH = ("a", "b", "c", "p1", "p2", "p3")

def words(typ, v):
    out = {}
    for k, x in v.items():
        if isinstance(x, str):
            out[k] = x
        elif k in ("p1", "p2", "p3"):
            out[k] = cents(x)
        elif k in CASH:
            out[k] = money(x)
        else:
            out[k] = f"{x.numerator:,}" if x.denominator == 1 else num(x)
    return out

def draw(typ, r, tpl):
    story = STORIES[tpl]
    st = STORY[typ][story]
    v, built = DRAW[typ](r, st)
    prompt = gen.fill(template(typ, story), **words(typ, v))
    try:
        v = read(typ, story, prompt)
        f = facts(typ, story, v)                     # forward, from the words
        for k, x in built.items():
            need(f.get(k) == x)                      # the forward solve agrees with the build
        p = dict(story=story, prompt=prompt)
        if typ == "10":
            p["choices"], p["answer"] = choices_10(r, f)
        elif typ == "11":
            p["choices"], p["answer"] = choices_11(r, f)
        else:
            p["answer"] = "; ".join(t for _, _, t in parts(typ, story, v, f))
    except ValueError:                               # the words don't make a problem: draw again
        raise gen.Redraw
    return p

# ------------------------------------------------------------------
# Reading the words back, and solving forward
# ------------------------------------------------------------------
def read(typ, story, prompt):
    got = gen.read(template(typ, story), prompt)
    out = {}
    for k, s in got.items():
        if k in WORDS:
            if not s.strip() or len(s.split()) > 2:
                raise ValueError("a name is one or two words")
            out[k] = s
        elif k == "eq":
            out[k] = " ".join(s.split())
        else:
            out[k] = number(s.replace(",", ""))
            if out[k] <= 0:
                raise ValueError("the numbers must be positive")
    return out

def mixture(a, b, c):
    """The mix of both with whole amounts nearest half and half, or None."""
    pts = [(F(x), (c - a * x) / b) for x in range(1, int(c / a) + 1)]
    pts = [(x, y) for x, y in pts if y > 0 and y.denominator == 1]
    return min(pts, key=lambda p: (abs(p[0] - c / (2 * a)), p[0])) if pts else None

def viable(a, b, c):
    """The line's points with whole-number coordinates, 0 or more."""
    return [(F(x), (c - a * x) / b) for x in range(0, int(c / a) + 1) if ((c - a * x) / b).denominator == 1]

def given(a, b, c):
    """"3/8 x + 2/3 y = 5"."""
    return f"{written((a, 'x'), (b, 'y'))} = {num(c) if c.denominator == 1 else c}"

def facts(typ, story, v):
    """What the words say, solved forward: the model's (a, b, c) and the type's own answers."""
    st = STORY[typ][story]
    if typ == "8":
        area = v["l"] * v.get("w", v["l"])
        g, h, k = v["g"], v["h"], v["k"]
        if g <= h or k.denominator != 1:
            raise ValueError("the first kind needs more space, and k is whole")
        x = area / (g + k * h)
        X = math.floor(x)
        if X < 1:
            raise ValueError("not even one of each fits")
        return dict(abc=(g, h, area), area=area, x=x, X=F(X), Y=k * X)
    if typ == "11":
        from . import forms_2_3 as B
        from . import slope_intercept_2_1 as si
        m, b = si.solved(v["eq"])
        if B.read("std", v["eq"]) is not None or m == 0 or b == 0:
            raise ValueError("already in standard form, or not a slanted line off the origin")
        g = re.fullmatch(r"(\d+/\d+) x \+ (\d+/\d+) y = (\d+)", v["eq"])
        if not g:
            raise ValueError("write it like 3/8 x + 2/3 y = 5")
        a, bb, c = F(g[1]), F(g[2]), F(g[3])
        return dict(abc=(a, bb, c), m=m, b=b)
    if typ == "12":
        ps_ = (v["p1"], v["p2"], v["p3"])
        if len(set(ps_)) != 3:
            raise ValueError("three different prices")
        pairs = [(i, j) for i in range(3) for j in range(i + 1, 3)]
        reach = {pr: v["c"] / min(ps_[pr[0]], ps_[pr[1]]) for pr in pairs}
        if all(reach[pr] >= v["T"] for pr in pairs) or not any(reach[pr] >= v["T"] for pr in pairs):
            raise ValueError("some mixtures reach the amount and some don't")
        return dict(prices=ps_, pairs=pairs, reach=reach)
    a, b, c = v["a"], v["b"], v["c"]
    if a == b:
        raise ValueError("two different prices")
    f = dict(abc=(a, b, c))
    if typ == "6":
        f["each"] = c / (a + b)
    if typ == "7":
        if (c / a).denominator != 1 or (c / b).denominator != 1 or mixture(a, b, c) is None:
            raise ValueError("whole intercepts and a whole mix of both")
        f["only"], f["mix"] = (c / a, c / b), mixture(a, b, c)
    if typ == "9":
        f["viable"] = viable(a, b, c)
        off = [(F(x), (c - a * x) / b) for x in range(1, int(c / a)) if ((c - a * x) / b).denominator != 1]
        if not off:
            raise ValueError("every whole x gives a whole y")
        f["off"] = off[0]
    return f

def nice(q):
    """A coordinate: 12.5 when it ends, else a mixed number, 23 1/3."""
    return num(q) if "/" not in num(q) else mixed(q)

def point(x, y):
    return f"({nice(x)}, {nice(y)})"

def half_example(g, h, area):
    """x = n + 1/2 nearest the middle of the line, y positive and ending within 3 places, or None."""
    pts = [(x, (area - g * x) / h) for x in (F(2 * n + 1, 2) for n in range(int(area / g)))]
    pts = [(x, y) for x, y in pts if y > 0 and (y * 1000).denominator == 1]
    return min(pts, key=lambda p: (abs(p[0] - area / (2 * g)), p[0])) if pts else None

def pairs_named(names):
    """"Mango and pineapple, and mango and strawberry"."""
    names = [t if i == 0 else t[0].lower() + t[1:] for i, t in enumerate(names)]
    return ", and ".join(names)

def parts(typ, story, v, f):
    """[(label, kind, text)]: kind "eq" (a model equation), "named" (an item pair: its equation), "text"."""
    st = STORY[typ][story]
    who = v.get("who")
    eq = model(*f["abc"]) if "abc" in f else None
    if typ == "5":
        return [("", "eq", eq)]
    if typ == "6":
        a, b, c = f["abc"]
        x, exact = exact_or_about(f["each"])
        amt = (num(f["each"]) if exact else f"about {hundredths(f['each'])}")
        return [("A.", "eq", eq),
                ("B.", "text", f"Put y = x into the equation: {num(a)} x + {num(b)} x = {num(c)}, so {num(a + b)} x = "
                               f"{num(c)} and x = {x}. Buy {amt} lb of {st['xn']} and {amt} lb of {st['yn']}.")]
    if typ == "7":
        a, b, c = f["abc"]
        (xi, yi), (mx, my) = f["only"], f["mix"]
        return [("A.", "text", f"{num(xi)} lb: only {st['xs']} means y = 0, so {num(a)} x = {num(c)} and x = {num(xi)}."),
                ("B.", "text", f"{num(yi)} lb: only {st['ys']} means x = 0, so {num(b)} y = {num(c)} and y = {num(yi)}."),
                ("C.", "text", f"For example, {num(mx)} lb of {st['xs']} and {num(my)} lb of {st['ys']}: "
                               f"{num(a)}({num(mx)}) + {num(b)}({num(my)}) = {num(c)}."),
                ("D.", "eq", eq)]
    if typ == "8":
        g, h, area = f["abc"]
        k, X, Y = v["k"], f["X"], f["Y"]
        half = half_example(g, h, area)
        if half is None:
            raise ValueError("no half-number solution to show")
        neg_x = math.floor(area / g) + 1
        neg = (F(neg_x), (area - g * neg_x) / h)
        xs, ys = st["xs"], st["ys"]
        x_eq, exact = exact_or_about(f["x"])
        start = (f"{num(X)} {xs} and {num(Y)} {ys}: put y = {num(k)} x into the equation: {num(g)} x + "
                 f"{num(h)}({num(k)} x) = {num(area)}, so {num(g + k * h)} x = {num(area)} and x = {x_eq}.")
        used = g * X + h * Y
        if f["x"] == X:
            end = f" Check: {num(g)}({num(X)}) + {num(h)}({num(Y)}) = {num(used)} ft², the whole {st['place']}."
        else:
            end = (f" Round down to {num(X)} {xs}, and {num(k)}({num(X)}) = {num(Y)} {ys}. Check: {num(g)}({num(X)}) + "
                   f"{num(h)}({num(Y)}) = {num(used)} ft², which fits in the {num(area)} ft² {st['place']}.")
        return [("A.", "eq", eq),
                ("B.", "text", f"No: x and y count {xs} and {ys}, so only whole numbers, 0 or more, make sense. A "
                               f"solution like {point(*half)} or {point(*neg)} is on the "
                               f"line but isn't possible."),
                ("C.", "text", start + end)]
    if typ == "9":
        pts = [point(x, y) for x, y in f["viable"]]
        return [("A.", "eq", eq),
                ("B.", "text", f"No: x and y count {st['xs']} and {st['ys']}, so only points whose coordinates are whole "
                               f"numbers, 0 or more, are viable: {listed(pts)}. A point like {point(*f['off'])} is on "
                               f"the graph but isn't viable.")]
    if typ == "12":
        items, prices, c = st["items"], f["prices"], v["c"]
        name = lambda i: items[i]
        pair = lambda pr: f"{name(pr[0]).capitalize()} and {name(pr[1])}"
        out = [("A.", "named", f"{pair(pr)}: {model(prices[pr[0]], prices[pr[1]], c)}") for pr in f["pairs"]]
        for pr in f["pairs"]:
            (i, j) = pr
            lo, hi = sorted(pr, key=lambda n: -prices[n])     # lo: the dearer item, fewer units
            out.append(("B.", "text", f"{pair(pr)}: from {mixed(c / prices[lo])} {st['units']} (all {name(lo)}) to "
                                      f"{mixed(c / prices[hi])} {st['units']} (all {name(hi)})."))
        T = v["T"]
        yes = [pr for pr in f["pairs"] if f["reach"][pr] >= T]
        no = [pr for pr in f["pairs"] if f["reach"][pr] < T]
        cheap = min(range(3), key=lambda n: prices[n])
        top = mixed(c / prices[cheap])
        yes_t = pairs_named([pair(pr) for pr in yes])
        no_t = " ".join(f"{pair(pr)} can make at most {mixed(f['reach'][pr])} {st['units']}, less than {num(T)}."
                        for pr in no)
        out.append(("C.", "text", f"{yes_t}: with enough {name(cheap)}, {'each' if len(yes) > 1 else 'it'} can make up "
                                  f"to {top} {st['units']}, at least {num(T)}. {no_t}"))
        return out
    raise KeyError(typ)

def kinds(typ, story, v, f):
    return [k for _, k, _ in parts(typ, story, v, f)]

# Types 10 and 11: choices, each read strictly as standard form
def choices_10(r, f):
    A, B, C = cleared(*f["abc"])
    right = f"{written((A, 'x'), (B, 'y'))} = {C}"
    wrong = [f"y - {A} = {C} (x - {B})", f"{C} y = {written((B, 'x'))} + {A}", f"{written((C, 'x'), (A, 'y'))} = {B}"]
    return gen.lettered(r, right, wrong)

def choices_11(r, f):
    from . import forms_2_3 as B
    a, b, c = f["abc"]
    m, k = f["m"], f["b"]
    q = a.denominator
    xs = [x for x in range(m.denominator, 25, m.denominator) if m * x + k != 0]   # m x1 whole, as (16, -3/2)
    need(xs)
    x1 = min(xs, key=lambda x: (abs(m * x + k), x))
    wrong = [B.slope_intercept(m, k), B.point_slope(m, x1, m * x1 + k), given(a, b, c),
             f"{written((a * q, 'x'), (b * q, 'y'))} = {num(c * q)}"]
    return gen.lettered(r, B.standard(m, k), wrong)

def line_of(abc):
    a, b, c = abc
    return -a / b, c / b

def true_choice(f, text):
    from . import forms_2_3 as B
    return B.read("std", text) == line_of(f["abc"])

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def split(p):
    return [s.strip() for s in p["answer"].split(";")]

def check(p):
    try:
        typ, story = p["type"], p["story"]
        v = read(typ, story, p["prompt"])
        f = facts(typ, story, v)
        if typ in CHOICE:
            truth = [gen.ABC[i] for i, c in enumerate(p["choices"]) if true_choice(f, c)]
            return "checked" if len(truth) == 1 and truth[0] == p["answer"] else "failed"
        got = split(p)
        want = parts(typ, story, v, f)
        if len(got) != len(want):
            return "failed"
        for g, (_, kind, w) in zip(got, want):
            if kind == "eq":
                if not same_line(read_model(g), f["abc"]):
                    return "failed"
            elif kind == "named":
                name, _, eq = w.partition(": ")
                gn, _, ge = g.partition(": ")
                pr = f["pairs"][[t for _, k, t in want if k == "named"].index(w)]
                abc = (f["prices"][pr[0]], f["prices"][pr[1]], v["c"])
                if gn != name or not same_line(read_model(ge), abc):
                    return "failed"
            elif g != w:
                return "failed"
        if typ == "7":                                # the mix is on the line, both amounts positive
            a, b, c = f["abc"]
            mx, my = f["mix"]
            if a * mx + b * my != c or mx <= 0 or my <= 0:
                return "failed"
        if typ == "8":                                # the animals fit, about k to 1
            g, h, area = f["abc"]
            if g * f["X"] + h * f["Y"] > area or g * (f["X"] + 1) + h * (f["Y"] + v["k"]) <= area:
                return "failed"
        if typ == "9":
            a, b, c = f["abc"]
            if any(a * x + b * y != c or x < 0 or y < 0 for x, y in f["viable"]):
                return "failed"
        return "checked"
    except Exception:
        return "unchecked"

def seen_key(p):
    try:
        v = read(p["type"], p["story"], p["prompt"])
        return (p["story"],) + tuple((k, str(x)) for k, x in sorted(v.items()) if k not in WORDS)
    except (ValueError, KeyError):
        return (p.get("story"), p["prompt"])

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def eq_typst(t):
    from ..typmath import display, dfrac
    return display(dfrac(t))

def typst(p):
    from ..typst import esc
    typ, story = p["type"], p["story"]
    if typ == "11":
        try:
            eq = read(typ, story, p["prompt"])["eq"]
        except ValueError:
            eq = p["prompt"]
        return (f"What is {eq_typst(eq)} written in standard form? " +
                gen.choices_typst([eq_typst(c) for c in p.get("choices", ())]))
    try:
        v = read(typ, story, p["prompt"])
    except ValueError:
        v = None
    if typ == "10":
        return math_letters(esc(p["prompt"])) + " " + gen.choices_typst([eq_typst(c) for c in p.get("choices", ())])
    if typ == "12" and v:
        st = S12[story]
        w = words(typ, v)
        rows = [[it.capitalize(), "$" + cents(v[f"p{i + 1}"])] for i, it in enumerate(st["items"])]
        ask = PART.sub(" \\\n", esc(gen.fill(st["ask"], **w).strip()))
        return math_letters(f"{esc(gen.fill(st['intro'], **w))} #v(0.2em) " +
                            table([st["kind"].capitalize() if st["kind"] != "trail mix" else "Ingredient",
                                   f"Cost per {st['unit']}"], rows) + f" #v(0.2em) {ask}")
    return math_letters(PART.sub(" \\\n", esc(p["prompt"])))

def labeled(p):
    """[(label, kind, text)] for the key; plain labels when the prompt can't be read."""
    typ, story = p["type"], p["story"]
    try:
        v = read(typ, story, p["prompt"])
        want = parts(typ, story, v, facts(typ, story, v))
    except Exception:
        want = []
    got = split(p)
    out = [(want[i][0], want[i][1], g) if i < len(want) else ("", "text", g) for i, g in enumerate(got)]
    return [("" if i and l == out[i - 1][0] else l, k, g) for i, (l, k, g) in enumerate(out)]   # A. once

def answer_typst(p):
    from ..typst import esc
    if p["type"] in CHOICE:
        return " \\\n".join(f"{a}. {eq_typst(c)}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    out = []
    for label, kind, t in labeled(p):
        if kind == "eq":
            shown = eq_typst(t)
        elif kind == "named":
            name, _, eq = t.partition(": ")
            shown = f"{esc(name)}: {eq_typst(eq)}"
        else:
            shown = math_letters(esc(t))
        out.append(f"{label} {shown}".strip())
    return " \\\n".join(out)

def text(p):
    if p["type"] == "11":
        return f"What is {p['prompt']} written in standard form?   " + gen.choices_text(p.get("choices", ()))
    if p["type"] == "10":
        return p["prompt"] + "   " + gen.choices_text(p.get("choices", ()))
    return p["prompt"]

def answer_text(p):
    if p["type"] in CHOICE:
        return "   ".join(f"{a}. {c}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    return "  |  ".join(f"{label} {t}".strip() for label, _, t in labeled(p))

def height(p):
    if p["type"] == "11":
        return 1.4
    extra = {"10": 1.0, "12": 1.1}.get(p["type"], 0)
    return 0.2 * (1 + len(p["prompt"]) // 95) + extra

# ------------------------------------------------------------------
# Editing: the story's own words, with new names or numbers
# ------------------------------------------------------------------
def from_edit(t, old):
    import random
    t = " ".join(t.split())
    typ, story = old["type"], old["story"]
    if typ == "11":
        from . import forms_2_3 as B
        t = B.tidy(t)
    v = read(typ, story, t)
    f = facts(typ, story, v)
    new = dict(old, prompt=t, source="edited")
    if typ in CHOICE:
        r = random.Random(t)                         # the same edit gives the same choices
        for _ in range(50):
            try:
                new["choices"], new["answer"] = (choices_10 if typ == "10" else choices_11)(r, f)
                break
            except gen.Redraw:
                continue
    else:
        new["answer"] = "; ".join(x for _, _, x in parts(typ, story, v, f))
    return new, check(new)

def with_answer(p, t, check):
    if p["type"] in CHOICE:
        return gen.with_letters(p, t, check)
    t = " ".join(t.replace("−", "-").replace("|", ";").split())
    new = dict(p, answer=t.replace(" ;", ";"))
    return new, check(new)

def answer_of(typ, story, prompt):
    v = read(typ, story, prompt)
    return "; ".join(x for _, _, x in parts(typ, story, v, facts(typ, story, v)))
