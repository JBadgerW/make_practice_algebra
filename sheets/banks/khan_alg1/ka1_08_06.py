"""Khan Algebra 1, Lesson 8-6: Function rules from equations, from the old
app's Alg1_08_06 (twenty generated slots, four templates).

For a given input b, the function f outputs a value a that satisfies an
equation in a and b; write a formula for f(b). The old templates' shapes:
A a + B b = C (Type 1), A b + B a = C b + D a (Type 2), a + B = C (b + E)
(Type 3), A b + B = C a + D (Type 4). The old key for Type 1 always began
"f(x) =", even for g and h; here it names the function.

A problem: dict(type, prompt, answer, source).
    prompt  "3 a + 2 b = 9 ; f ; b ; a"    (equation ; function ; input ; output)
    answer  "f(b) = -2/3 b + 3"     (slope-intercept form, fractions as written)
check() puts the formula in for the output and requires the equation to
hold for every input.
"""
from fractions import Fraction as F
import sympy as sp
from ... import gen
from ...gen import need, signed, signed_except, written
from ...linear import exact
from ...typst import esc
from ...typmath import display, dfrac, text as plain, tx
from . import courses

NAME = FAMILY = "ka1_08_06"
FIXED = False
TITLE = "Lesson 8-6: Function rules from equations"
INSTRUCTIONS = "Write a formula for each function in terms of its input."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Output and Input Terms",
         look="A a + B b = C: one output term and one input term.",
         move="Solve for the output: move the input term across, then divide by the output's coefficient."),
    dict(key="2", title="Both Letters on Both Sides",
         look="A b + B a = C b + D a.",
         move="Gather the output terms on one side and the input terms on the other, then divide."),
    dict(key="3", title="Distribute First",
         look="a + B = C (b + E).",
         move="Distribute, then move the number across to get the output alone."),
    dict(key="4", title="A Number with Each Letter",
         look="A b + B = C a + D.",
         move="Move the number on the output's side across, then divide by the output's coefficient."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in", width="full")     # the sentence and its equation on one line
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
PAIRS = [("b", "a"), ("a", "b"), ("m", "n"), ("x", "y"), ("q", "r"), ("u", "v"), ("t", "s")]

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t1(r, i, o):                              # A o + B i = C
    A, B = signed(r, 1, 10), signed(r, 1, 10)
    return f"{written((A, o), (B, i))} = {signed(r, 1, 10) * A}"

def t2(r, i, o):                              # A i + B o = C i + D o
    n, B = signed(r, 1, 8), signed(r, 1, 12)
    D = signed_except(r, 1, 12, B)
    A = signed_except(r, 1, 12, -n * (B - D))
    C = n * (B - D) + A
    need(C != 0 and abs(A) + abs(B) + abs(C) + abs(D) <= 60)
    return f"{written((A, i), (B, o))} = {written((C, i), (D, o))}"

def t3(r, i, o):                              # o + B = C (i + E)
    B, C, E = signed(r, 1, 12), signed_except(r, 1, 8, 1), signed(r, 1, 12)
    return f"{written((1, o), (B, ''))} = {written((C, '(' + written((1, i), (E, '')) + ')'))}"

def t4(r, i, o):                              # A i + B = C o + D
    A, B, C, D = signed(r, 1, 12), signed(r, 1, 12), signed_except(r, 1, 12, 1), signed(r, 1, 12)
    return f"{written((A, i), (B, ''))} = {written((C, o), (D, ''))}"

TEMPLATES = {"1": [t1], "2": [t2], "3": [t3], "4": [t4]}

def parts(prompt):
    eq, f, i, o = (s.strip() for s in prompt.split(";"))
    return eq, f, i, o

def rule(prompt):
    eq, f, i, o = parts(prompt)
    l, _, r = eq.partition("=")
    sol = sp.solve(exact(l) - exact(r), sp.Symbol(o))
    if len(sol) != 1:
        raise ValueError("the output must be one formula of the input")
    return sol[0]

def slope_intercept(e, v):
    """A linear expression as m v + b, fractions as written: "5/3 q - 10"."""
    e = sp.expand(e)
    m, b = e.coeff(sp.Symbol(v), 1), e.coeff(sp.Symbol(v), 0)
    return written((F(str(m)), v), (F(str(b)), ""))

def answer_of(prompt):
    eq, f, i, o = parts(prompt)
    return f"{f}({i}) = {slope_intercept(rule(prompt), i)}"

def draw(entry, r, tpl):
    i, o = r.choice(PAIRS)
    f = r.choice("fgh")
    prompt = f"{TEMPLATES[entry][tpl](r, i, o)} ; {f} ; {i} ; {o}"
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        eq, f, i, o = parts(p["prompt"])
        lhs, _, rhs = p["answer"].partition("=")
        if " ".join(lhs.split()) != f"{f}({i})":
            return "failed"
        l, _, r = eq.partition("=")
        holds = sp.simplify((exact(l) - exact(r)).subs(sp.Symbol(o), exact(rhs))) == 0
        return "checked" if holds and sp.Symbol(o) not in exact(rhs).free_symbols else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    eq, f, i, o = parts(p["prompt"])
    return (f"For a given input value ${i}$, the function ${f}$ outputs a value ${o}$ that satisfies "
            f"{display(dfrac(eq))}. Write a formula for ${f}({i})$ in terms of ${i}$.")

def answer_typst(p):
    return display(dfrac(p["answer"]))

def text(p):
    eq, f, i, o = parts(p["prompt"])
    return f"{plain(eq)}:  {f}({i}) = ?  (input {i}, output {o})"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.6

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "3 a + 2 b = 9 ; f ; b ; a", "f(b) = -2/3 b + 3")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
