"""Khan Algebra 2, Lesson 3-1: Factor monomials, from the old app's
Alg2_03_01 (eighteen of Khan's, without answers; the rectangles were
pictures).

Type 1: the missing factor, 12 x^5 = (4 x^2)(C), the unknown on either
side, signs as Khan's (-15 y^4 = (D)(3 y^2)). Type 2: a rectangle's area
and one side; the other side (drawn here, not a picture). Type 3: two
students factor a monomial; which of them did it correctly? A wrong one
has the wrong product of numbers (3 x^2 times 4 x^4 for 7 x^6) or adds the
exponents wrong (7 x^2 times x^3 for 7 x^6). Only, Only, Both, Neither
are spread evenly over a sheet.

A problem: dict(type, prompt, answer, source, ...).
    Type 1  prompt "12 x^5 = (4 x^2)(C)", answer "3 x^3"
    Type 2  area "18 x^3", side "2 x^2", ask "width", answer "9 x"  (shape "rectangle")
    Type 3  monomial "12 x^7", names ["Ibuki", "Melodie"], ways ["(4 x^3)(3 x^4)", "(2 x^6)(6 x)"],
            choices [...], answer "A"
check() multiplies back: the factor times the known one is the product,
the side times the side is the area, and each student's factors multiply
to the monomial (or don't) as the key says.
"""
import re
import sympy as sp
from ... import gen
from ...gen import need, signed
from ...check import to_sympy
from ...typmath import display, text as plain
from . import courses
from ..khan_alg1.figures import PREAMBLE
from ..khan_alg1.polybank import side_check, side_typst, side_text

NAME = FAMILY = "ka2_03_01"
FIXED = False
TITLE = "Lesson 3-1: Factor monomials"
INSTRUCTIONS = ""
COURSES = courses(3)

TYPES = [
    dict(key="1", title="The Missing Factor", instructions="Find the missing factor that makes each equality true.",
         look="A monomial equal to a product of two, one of them unknown.",
         move="Divide: the numbers divide, and the exponents subtract. Check by multiplying back."),
    dict(key="2", title="A Missing Side", instructions="Answer each question.",
         look="A rectangle's area, a monomial, and one of its sides.",
         move="Area = length × width, so divide the area by the side you know.", width="full"),
    dict(key="3", title="Who Factored It Correctly?", instructions="Choose 1 answer.",
         look="Two students' factorizations of the same monomial.",
         move="Multiply each pair back: multiply the numbers and add the exponents. Does it give the monomial?",
         width="full"),
]
T = gen.Types(TYPES, "", space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p.get("prompt") or p.get("monomial"), str(p.get("side") or p.get("ways")), p["answer"])

def mono(c, v, n):
    """"12 x^5", "x", "-x^2", "7"."""
    body = "" if n == 0 else v if n == 1 else f"{v}^{n}"
    if not body:
        return str(c)
    return body if c == 1 else f"-{body}" if c == -1 else f"{c} {body}"

def t_factor(r):
    v = r.choice("xy")
    a, b = signed(r, 1, 9), signed(r, 1, 9)
    need(abs(a * b) > 1 and abs(a) * abs(b) <= 81 and (a > 0 or b > 0))
    m, n = r.randint(1, 5), r.randint(1, 5)
    letter_ = r.choice("BCD")
    known, unknown = mono(a, v, m), mono(b, v, n)
    product = mono(a * b, v, m + n)
    prompt = f"{product} = ({known})({letter_})" if r.random() < 0.5 else f"{product} = ({letter_})({known})"
    return dict(prompt=prompt, answer=unknown)

def t_side(r):
    a, b = r.randint(2, 15), r.randint(2, 12)
    m, n = r.randint(1, 4), r.randint(1, 4)
    need(a * b <= 150)
    v = r.choice("xy")
    area = mono(a * b, v, m + n)
    return dict(prompt=area, shape="rectangle", area=area, side=mono(a, v, m), ask=r.choice(("length", "width")),
                answer=mono(b, v, n))

OUTCOMES = "ABCD"

def way(r, c, v, n, right):
    """A factorization of c v^n: right, or one of the two mistakes."""
    for _ in range(50):
        ds = [d for d in range(1, c + 1) if c % d == 0]
        a = r.choice(ds)
        k = r.randint(1, n - 1) if n > 1 else 1
        b, j = c // a, n - k
        if not right:
            if r.random() < 0.5:
                b = b + r.choice((-1, 1)) * r.randint(1, 3)          # the numbers don't multiply to c
                if b < 1 or a * b == c:
                    continue
            else:
                j = n // k if k > 1 and n % k == 0 and n // k != n - k else n - k + r.choice((-1, 1))   # exponents
                if j < 1 or k + j == n:
                    continue
        if j == 0:
            continue
        return f"({mono(a, v, k)})({mono(b, v, j)})"
    need(False)

def t_who(r, want):
    v = r.choice("xy")
    c, n = r.choice([6, 7, 8, 10, 12, 14, 15, 18, 20, 24, 28, 30, 36, 45]), r.randint(2, 8)
    names = r.sample(gen.NAMES, 2)
    outcome = want or r.choice(OUTCOMES)
    rights = {"A": (True, False), "B": (False, True), "C": (True, True), "D": (False, False)}[outcome]
    ways = [way(r, c, v, n, ok) for ok in rights]
    need(ways[0] != ways[1])
    monomial = mono(c, v, n)
    choices, answer = gen.in_order(choices_for(names), choices_for(names)[OUTCOMES.index(outcome)])
    return dict(monomial=monomial, names=names, ways=ways, choices=choices, answer=answer)

def choices_for(names):
    a, b = names
    return [f"Only {a}", f"Only {b}", f"Both {a} and {b}", f"Neither {a} nor {b}"]

def draw(entry, r, tpl, want=None):
    if entry == "1":
        return t_factor(r)
    if entry == "2":
        return t_side(r)
    return t_who(r, want)

def correct(monomial, w):
    return sp.expand(to_sympy(w) - to_sympy(monomial)) == 0

def is_monomial(t):
    e = to_sympy(t)
    return "(" not in t and len(sp.Add.make_args(sp.expand(e))) == 1

def check(p):
    try:
        if p["type"] == "1":
            product, rhs = p["prompt"].split("=")
            known = re.sub(r"\(([BCD])\)", "", rhs).strip()
            ok = is_monomial(p["answer"]) and sp.expand(to_sympy(known) * to_sympy(p["answer"]) - to_sympy(product)) == 0
            return "checked" if ok else "failed"
        if p["type"] == "2":
            return side_check(p)
        rights = tuple(correct(p["monomial"], w) for w in p["ways"])
        outcome = {(True, False): "A", (False, True): "B", (True, True): "C", (False, False): "D"}[rights]
        return "checked" if p["answer"] == outcome else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=(OUTCOMES, lambda k: k[4] if k[0] == NAME and k[1] == "3" else None))

def typst(p, gap="0.3em"):
    if p["type"] == "1":
        unknown = re.search(r"\(([BCD])\)", p["prompt"]).group(1)
        return f"{display(p['prompt'])} \\\n    ${unknown} =$"
    if p["type"] == "2":
        return side_typst(p)
    (a, b), (u, w), m = p["names"], p["ways"], p["monomial"]
    return (f"{a} factored ${m}$ as ${u}$. {b} factored ${m}$ as ${w}$. Which of them factored ${m}$ correctly? "
            f"\\\n    {gen.choices_typst(p['choices'], 'linear')}")

def answer_typst(p):
    if p["type"] == "1":
        unknown = re.search(r"\(([BCD])\)", p["prompt"]).group(1)
        return f"${unknown} = {p['answer']}$"
    if p["type"] == "2":
        return f"${p['answer']}$"
    return gen.choice_answer_typst(p)

def text(p):
    if p["type"] == "1":
        return plain(p["prompt"])
    if p["type"] == "2":
        return side_text(p)
    return f"{p['monomial']}: {p['names'][0]} {p['ways'][0]}, {p['names'][1]} {p['ways'][1]}"

def answer_text(p):
    return plain(p["answer"]) if p["type"] != "3" else gen.choice_answer_typst(p)

def height(p):
    return {"1": 0.6, "2": 1.4, "3": 0.9}[p["type"]]

def edit_text(p):
    return p.get("prompt") or p["monomial"]

def from_edit(t, old):
    if old["type"] != "1":
        raise ValueError("reroll for a new problem; you can edit the answer")
    t = " ".join(t.replace("−", "-").split())
    m = re.fullmatch(r"(.+)=\s*(?:\((.+)\)\s*\(([BCD])\)|\(([BCD])\)\s*\((.+)\))", t)
    if not m:
        raise ValueError("write it like 12 x^5 = (4 x^2)(C)")
    product, known = m.group(1), m.group(2) or m.group(5)
    q = sp.simplify(to_sympy(product) / to_sympy(known))
    from ...typmath import tx
    new = dict(old, prompt=t, answer=tx(q), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "3":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
