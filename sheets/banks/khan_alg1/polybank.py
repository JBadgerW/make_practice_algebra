"""What the Khan Algebra 1 polynomial lessons share (Unit 13): binomials as
written, and the checks and edits for "expand" and "factor" problems.
(Not a bank: the library passes over it.)

    binomial(d, e, v, constant_first)   "(3 x - 5)", "(9 - x)"
    expand_check, expand_answer_of      the same polynomial, written in standard form;
    checker(either), constants_first    or, where the prompt leads with numbers, ascending
    factor_check, factor_answer_of      the same polynomial, factored completely
"""
import re
import sympy as sp
from ... import gen, poly
from ...gen import written
from ...check import to_sympy
from ...typmath import tx, text as plain
from .figures import labeled_box

def binomial(d, e, v, constant_first=False):
    """(d v + e), or (e + d v)."""
    return f"({written((e, ''), (d, v)) if constant_first else written((d, v), (e, ''))})"

BINOMIAL = re.compile(r"\(([^()]*)\)")

def constants_first(prompt):
    """Does every binomial in the prompt lead with its number, (5 + x)(5 - x)?"""
    bs = BINOMIAL.findall(prompt)
    return bool(bs) and all(re.match(r"\s*-?\d+\s*[-+]", b) for b in bs)

def expand_answer_of(prompt, follow=False):
    """The product multiplied out: standard form, or (follow) ascending when the
    prompt's binomials lead with their numbers: (5 + x)(5 - x) = 25 - x^2."""
    return poly.expanded(to_sympy(prompt), follow and constants_first(prompt))

def checker(either):
    """check() for an expand problem: the same polynomial, in standard form (either:
    or in ascending order)."""
    def check(p):
        try:
            ok = poly.standard(p["answer"], either) and sp.expand(to_sympy(p["prompt"]) - to_sympy(p["answer"])) == 0
            return "checked" if ok else "failed"
        except Exception:
            return "unchecked"
    return check

expand_check = checker(False)

def leads_with_number(prompt):
    """Does the prompt start with its constant (81 - x^2), so the key writes (9 - x) (9 + x)?"""
    return bool(re.match(r"-?\d+\s*[-+]", prompt.strip())) and "(" not in prompt

def factor_answer_of(prompt):
    return poly.factored(to_sympy(prompt), leads_with_number(prompt))

def factor_check(p):
    try:
        return "checked" if poly.completely_factored(p["answer"], p["prompt"]) else "failed"
    except Exception:
        return "unchecked"

def expand_edits(example, example_answer, follow=False):
    return gen.edits(lambda t: expand_answer_of(t, follow), checker(follow), example, example_answer)

def factor_edits(example, example_answer):
    return gen.edits(factor_answer_of, factor_check, example, example_answer)

# ------------------------------------------------------------------
# Area models: a product shown as a rectangle (13-2, 13-3)
# ------------------------------------------------------------------
def term_list(text):
    """The terms of a polynomial as (Typst, coefficient), as written: "x^2 - 2 x + 5"."""
    return [(tx(sp.expand(t)), sp.expand(t).as_coeff_Mul()[0]) for t in poly.terms(text)]

# ------------------------------------------------------------------
# A missing side: a rectangle (or square) with its area and one side given
# ------------------------------------------------------------------
def side_check(p):
    """The answer times the given side (or squared, for a square) is the area, and
    the answer is multiplied out (a side of 9 - 6 x + x^2 is x - 3 or 3 - x)."""
    try:
        a = to_sympy(p["answer"])
        given = a if p["shape"] == "square" else to_sympy(p["side"])
        ok = "(" not in p["answer"] and sp.expand(a * given - to_sympy(p["area"])) == 0
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

def side_typst(p):
    if p["shape"] == "square":
        return (f"The square below has an area of ${p['area']}$ square meters. What expression represents "
                f"the length of one side of the square? \\\n    "
                f"{labeled_box('Side length', '', '$' + p['area'] + '$')}")
    known, ask = ("width", "length") if p["ask"] == "length" else ("length", "width")
    top, left = (ask.capitalize(), f"${p['side']}$") if p["ask"] == "length" else (f"${p['side']}$", ask.capitalize())
    return (f"The rectangle below has an area of ${p['area']}$ square meters and a {known} of ${p['side']}$ "
            f"meters. What expression represents the {ask} of the rectangle? \\\n    "
            f"{labeled_box(top, left, '$' + p['area'] + '$')}")

def side_text(p):
    if p["shape"] == "square":
        return f"square of area {plain(p['area'])}: side?"
    return f"area {plain(p['area'])}, {'width' if p['ask'] == 'length' else 'length'} {plain(p['side'])}: {p['ask']}?"
