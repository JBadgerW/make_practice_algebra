"""Shared pieces for the literal-equation scripts in this folder:
the type classification, Typst math -> sympy parsing and numeric checks,
and the worksheet/slide preambles copied into templates/.
"""
import random, re
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication, convert_xor)

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------
# The sequence. Each type: key, short title, what to look for, the move,
# worksheet problems, workspace height on the worksheet (in), and the
# problems worked step by step in the guide.
# ------------------------------------------------------------------

TYPES = [
    dict(key="1", title="One Step",
         look="The unknown is tied to the rest by a single operation: $+$, $-$, $times$, or $div$.",
         move="Undo that one operation on both sides.",
         probs=[1, 2, 3, 4, 5, 6, 7, 8], space=0.95, worked=[1]),
    dict(key="2", title="Add or Subtract, Then Divide",
         look="No fractions. The unknown's term has other terms added to it or subtracted from it.",
         move="Undo the adding or subtracting first, then divide by the unknown's coefficient.",
         probs=[9, 10, 11, 12], space=1.1, worked=[9]),
    dict(key="3", title="Clear One Denominator",
         look="One fraction bar (or a fraction coefficient like $1/3$), and no parentheses to distribute.",
         move="Multiply both sides by the denominator; then add or subtract and divide as usual.",
         probs=[13, 14, 15, 16, 17, 18], space=1.25, worked=[13]),
    dict(key="4", title="Distribute First",
         look="The unknown is inside parentheses, with a number or letter multiplying the group.",
         move="Distribute; then add or subtract like terms and divide.",
         probs=[19, 20, 21, 22, 23, 24], space=1.5, worked=[19]),
    dict(key="5", title="Clear a Denominator, Then Distribute",
         look="A fraction and a set of parentheses.",
         move="Multiply both sides by the denominator first, then distribute and solve.",
         probs=[25, 26, 27], space=1.5, worked=[25]),
    dict(key="6", title="Clear Two Denominators",
         look="Two different fractions in the equation.",
         move="Multiply every term on both sides by both denominators, which clears both fractions at once.",
         probs=[28, 29], space=1.5, worked=[28]),
    dict(key="7", title="Factor Out, Then Divide",
         look="The unknown appears in two terms that are already together on one side.",
         move="Factor the unknown out of those terms, then divide by what is left in the parentheses.",
         probs=[30, 31], space=1.4, worked=[30]),
    dict(key="8", title="Gather, Factor Out, Divide",
         look="The unknown appears on both sides of the equation.",
         move="Add or subtract to get every term with the unknown on one side and everything else on the other; then factor out and divide.",
         probs=[32, 33, 34, 35], space=1.6, worked=[32]),
    dict(key="9", title="Distribute, Gather, Factor Out, Divide",
         look="Parentheses, and the unknown shows up in more than one term.",
         move="Distribute first; then gather, factor out, and divide as in Type 8.",
         probs=[36, 37, 38], space=1.75, worked=[36]),
    dict(key="10", title="Clear Single-Term Denominators, Then Solve",
         look="Fractions whose denominators are single numbers or letters.",
         move="Multiply both sides by every denominator to clear the fractions; what is left is a Type 9 (or easier) equation.",
         probs=[39, 40, 41], space=1.85, worked=[39]),
    dict(key="11", title="Clear a Multi-Term Denominator",
         look="A denominator that is a sum or difference, such as $(x - 1)$.",
         move="Multiply both sides by the whole denominator, keeping its parentheses; then distribute and solve as in Type 9.",
         probs=[42, 43, 44, 45], space=1.85, worked=[42]),
    dict(key="A", title="Watch the Sign", special=True,
         look="The term with the unknown has a minus sign in front of it.",
         move="Add that term to both sides so it is positive on the other side, then solve. (If you leave it where it is, divide by the negative coefficient, not the positive one.)",
         probs=[46, 47], space=1.2, worked=[46, 47]),
    dict(key="B", title="Finish with a Square Root", special=True,
         look="The unknown is squared.",
         move="Solve for the squared term as usual, then take the square root of both sides. These unknowns are lengths, so use the positive root.",
         probs=[48, 49, 50], space=1.5, worked=[48, 49, 50]),
]

def label(t):
    return ("Special Case " if t.get("special") else "Type ") + t["key"]


# ------------------------------------------------------------------
# Typst math -> sympy, and numeric checks
# ------------------------------------------------------------------
TR = standard_transformations + (implicit_multiplication, convert_xor)

def to_sympy(s):
    s = s.replace("ell", "L_")       # keep 'ell' a single symbol
    s = re.sub(r"\b(?!sqrt\b)([A-Za-z]\w*)\s*\(", r"\1*(", s)  # m(x + 2) is a product
    names = {n: sp.Symbol(n) for n in re.findall(r"[A-Za-z]\w*", s)}  # I, E, S are symbols, not sympy constants
    names.update({"pi": sp.pi, "sqrt": sp.sqrt})
    return parse_expr(s, transformations=TR, local_dict=names)

def side_diff(eq):
    l, r = eq.split("=")
    return to_sympy(l) - to_sympy(r)

def syms_of(prompt):
    return {str(v).replace("L_", "ell"): v for v in side_diff(prompt).free_symbols}

def holds(eq, prompt, var, sol, trials=5):
    """eq is true whenever var = sol in prompt (random positive values for the rest)."""
    e, syms = side_diff(eq), syms_of(prompt)
    assert e.free_symbols <= set(syms.values()), (eq, prompt)
    se = to_sympy(sol)
    for _ in range(trials):
        vals = {s: random.uniform(1.5, 9.5) for s in syms.values()}
        vals[syms[var]] = complex(se.subs(vals).evalf())
        assert abs(complex(e.subs(vals).evalf())) < 1e-8, (eq, prompt, var, sol)

# ------------------------------------------------------------------
# Typst preambles
# ------------------------------------------------------------------
MARK = "// ==================================================\n// DOCUMENT VARIABLES"
head = (HERE / "templates/mixed_review_v1.typ").read_text()
head = head[:head.index(MARK)]
slhead = (HERE / "templates/mixed_review_slides.typ").read_text()
slhead = slhead[:slhead.index(MARK)]

def vars_(title, version="1", class_name="Algebra 1"):
    return f'''{MARK}
// ==================================================

#let class-name = "{class_name}"
#let worksheet-title = "{title}"
#let version = "{version}"

'''

