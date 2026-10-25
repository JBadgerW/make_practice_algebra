"""Khan Algebra 1, Lesson 13-1: Polynomials intro, from the old app's
Alg1_13_01 (twelve of Khan's, without answers; Khan Algebra 2's 1-1 is the
same set).

Type 1: pick the expression that matches a description ("A polynomial of the
5th degree with a leading coefficient of 7 and a constant term of 6", "A
trinomial with a leading coefficient of 3 and a constant term of -5", "A 3rd
degree binomial with a constant term of 8"). Each wrong choice breaks
exactly one part of the description, as Khan's do: the degree and the
leading coefficient traded, the constant and a coefficient traded, a term
too many or too few. Type 2: which polynomials are in standard form?
(choose all that apply, or none of the above). Type 3: the degree.

A problem: dict(type, prompt, ..., answer, source).
    Type 1  describe {terms, degree, lead, constant} (the parts given), choices, answer "C"
    Type 2  choices three polynomials and "None of the above", answer "A, C" or "D"
    Type 3  prompt "5 z^3 - 2 z^4 - 9 z^2 + z", answer "4"
check() reads every choice's terms, degree, and coefficients from its text.
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, written
from ...check import to_sympy
from ...typmath import text as plain
from . import courses

NAME = FAMILY = "ka1_13_01"
FIXED = False
TITLE = "Lesson 13-1: Polynomials intro"
INSTRUCTIONS = ""
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Describe a Polynomial", instructions="Pick the expression that matches each description.",
         look="A description: the number of terms, the degree, the leading coefficient, the constant term.",
         move="Check each part of the description against each choice. Write a choice in standard form first if it isn't."),
    dict(key="2", title="Standard Form", instructions="Which polynomials are in standard form? Choose all that apply.",
         look="Polynomials whose terms may be in any order.",
         move="Standard form lists the terms from the highest exponent down to the constant."),
    dict(key="3", title="Degree", instructions="What is the degree of each polynomial?",
         look="A polynomial, its terms in any order.",
         move="The degree is the highest exponent of the variable, wherever that term is.", space="0.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
KINDS = {1: "monomial", 2: "binomial", 3: "trinomial"}
NONE = "None of the above"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], tuple(p.get("choices", ())))

def ordinal(n):
    return f"{n}^\"{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n, 'th') }\""

def poly_of(r, v, degree, lead, constant, n):
    """A polynomial in standard form with n terms, this degree, leading coefficient,
    and constant term (None: no constant term), its other terms drawn at random."""
    exps = [degree]
    middle = list(range(1, degree))
    k = n - 1 - (constant is not None)
    need(0 <= k <= len(middle))
    exps += sorted(r.sample(middle, k), reverse=True)
    terms = [(lead, f"{v}^{degree}" if degree > 1 else v)] + \
        [(signed(r, 1, 9), f"{v}^{e}" if e > 1 else v) for e in exps[1:]]
    if constant is not None:
        terms.append((constant, ""))
    return written(*terms)

def parts(text):
    """(terms, degree, leading coefficient, constant) of a polynomial, as written."""
    e = to_sympy(text)
    v = poly.letter(e)
    p = sp.Poly(e, v)
    return len(sp.Add.make_args(e)), p.degree(), p.LC(), e.subs(v, 0)

def fits(text, d):
    n, deg, lead, const = parts(text)
    return ((d.get("terms") is None or n == d["terms"]) and (d.get("degree") is None or deg == d["degree"]) and
            (d.get("lead") is None or lead == d["lead"]) and (d.get("constant") is None or const == d["constant"]))

def describe(d):
    """The description in words, Typst math for the numbers."""
    kind = KINDS.get(d.get("terms"), "polynomial")
    out = "A "
    if d.get("degree") is not None:
        out += f"${ordinal(d['degree'])}$ degree {kind}" if d.get("lead") is None else f"{kind} of the ${ordinal(d['degree'])}$ degree"
    else:
        out += kind
    bits = []
    if d.get("lead") is not None:
        bits.append(f"a leading coefficient of ${d['lead']}$")
    if d.get("constant") is not None:
        bits.append(f"a constant term of ${d['constant']}$")
    return out + (" with " + " and ".join(bits) if bits else "")

def t1(r):
    v = r.choice(gen.LETTERS)
    deg, lead, const = r.randint(2, 7), signed(r, 2, 9), signed(r, 1, 9)
    shape = r.choice(("degree-lead-constant", "kind-lead-constant", "kind-degree-lead", "degree-kind-constant"))
    if shape == "degree-lead-constant":       # a polynomial of the 5th degree with ... and ...
        d = dict(degree=deg, lead=lead, constant=const)
        n = r.randint(3, 4)
    elif shape == "kind-lead-constant":        # a trinomial with a leading coefficient of 3 and a constant of -5
        n = r.choice((2, 3))
        d = dict(terms=n, lead=lead, constant=const)
    elif shape == "kind-degree-lead":          # a monomial of the 2nd degree with a leading coefficient of 3
        n = 1
        d = dict(terms=1, degree=deg, lead=lead)
        const = None
    else:                                      # a 3rd degree binomial with a constant term of 8
        n = 2
        d = dict(terms=2, degree=deg, constant=const)
    need(deg >= n - 1 + (const is None) and abs(lead) != deg and abs(const or 0) != abs(lead))
    right = poly_of(r, v, deg, lead, const, n)
    wrong = [poly_of(r, v, abs(lead), deg, const, n) if abs(lead) <= 9 else None,          # degree and coefficient traded
             poly_of(r, v, deg, const or lead, lead if const is not None else None, n),     # constant and coefficient traded
             poly_of(r, v, deg, lead, const, n + 1) if n < deg + 1 else None,               # a term too many
             poly_of(r, v, deg, lead, const, n - 1) if n > 1 + (const is not None) else None,
             poly_of(r, v, deg + 1, lead, const, n)]
    wrong = [w for w in dict.fromkeys(wrong) if w and not fits(w, d)]
    need(len(wrong) >= 3)
    r.shuffle(wrong)
    choices, letter = gen.lettered(r, right, wrong[:3])
    return dict(describe=d, prompt=describe(d), choices=choices, answer=letter)

def shuffled(r, v):
    """A polynomial of 2 to 4 terms, standard or not."""
    n = r.randint(2, 4)
    exps = sorted(r.sample(range(0, 6), n), reverse=True)
    terms = [(signed(r, 1, 9), "" if e == 0 else v if e == 1 else f"{v}^{e}") for e in exps]
    if r.random() < 0.5:                       # out of order, half the time
        for _ in range(6):
            r.shuffle(terms)
            if not poly.standard(written(*terms)):
                break
    return written(*terms)

def t2(r):
    polys = [shuffled(r, r.choice(gen.LETTERS)) for _ in range(3)]
    need(len(set(polys)) == 3)
    right = [p for p in polys if poly.standard(p)]
    choices = polys + [NONE]
    return dict(prompt="", choices=choices,
                answer=", ".join(gen.ABC[i] for i, c in enumerate(choices) if c in right) or "D")

def t3(r):
    v = r.choice(gen.LETTERS)
    n = r.randint(3, 4)
    exps = r.sample(range(0, 8), n)
    need(exps != sorted(exps, reverse=True))   # the degree isn't simply the first exponent
    terms = [(signed(r, 1, 9), "" if e == 0 else v if e == 1 else f"{v}^{e}") for e in exps]
    prompt = written(*terms)
    return dict(prompt=prompt, answer=str(max(exps)))

TEMPLATES = {"1": [t1], "2": [t2], "3": [t3]}

def draw(entry, r, tpl):
    return TEMPLATES[entry][tpl](r)

def check(p):
    try:
        if p["type"] == "1":
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if fits(c, p["describe"])]
            return "checked" if right == gen.letters_of(p["answer"]) else "failed"
        if p["type"] == "2":
            right = [gen.ABC[i] for i, c in enumerate(p["choices"][:-1]) if poly.standard(c)]
            return "checked" if gen.letters_of(p["answer"]) == (right or ["D"]) else "failed"
        return "checked" if parts(p["prompt"])[1] == int(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def math(c):
    return c if c == NONE else f"${c}$"

def typst(p, gap="0.3em"):
    if p["type"] == "3":
        return f"${p['prompt']}$"
    head = f"{p['prompt']} \\\n    " if p["prompt"] else ""
    return head + gen.choices_typst([math(c) for c in p["choices"]], "grid" if p["type"] == "1" else "vertical")

def answer_typst(p):
    if p["type"] == "3":
        return f"${p['answer']}$"
    return gen.choice_answer_typst(dict(p, choices=[math(c) for c in p["choices"]])) if p["type"] == "1" else p["answer"]

def text(p):
    if p["type"] == "3":
        return plain(p["prompt"]) + ": degree?"
    words = p["prompt"].replace("$", "").replace('^"', "").replace('"', "")
    return (words + "   " if words else "") + gen.choices_text(p["choices"], plain)

def answer_text(p):
    return p["answer"] if p["type"] != "1" else f"{p['answer']}. {plain(gen.chosen(p)[0])}"

def height(p):
    return 0.3 if p["type"] == "3" else 1.0

def edit_text(p):
    return p["prompt"] if p["type"] == "3" else "; ".join(p["choices"])

def from_edit(t, old):
    if old["type"] == "3":
        t = " ".join(t.replace("−", "-").split())
        new = dict(old, prompt=t, answer=str(parts(t)[1]), source="edited")
        return new, check(new)
    raise ValueError("reroll for new choices; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "3":
        new = dict(p, answer=t.strip())
        return new, check(new)
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
