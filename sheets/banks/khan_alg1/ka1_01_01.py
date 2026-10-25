"""Khan Algebra 1, Lesson 1-1: Evaluating expressions with one variable,
from the old app's Alg1_01_01 (twenty generated slots, nineteen templates;
Khan Prealgebra 6-2 is the same set).

Evaluate an expression at a whole number: x + 5 at x = 3, x/4 - 2 at
x = 24, 12/x + 3 at x = 4. Built backward, as the old templates were: the
answer, a whole number, first. The old no. 12 (a - x/b) drew its answer at
random, apart from the expression, so its key was wrong, and x/b wasn't
always whole; here x is a multiple of b.

A problem: dict(type, prompt, answer, source).
    prompt  "x/4 - 2 ; x = 24"      (the expression ; the value)
    answer  "4"
check() substitutes the value into the expression with sympy.
"""
import sympy as sp
from ... import gen
from ...gen import need, written
from ...check import to_sympy
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka1_01_01"
FIXED = False
TITLE = "Lesson 1-1: Evaluating expressions with one variable"
INSTRUCTIONS = "Evaluate each expression for the given value."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Add or Subtract",
         look="The variable plus or minus a number.",
         move="Put the number in for the variable, then add or subtract."),
    dict(key="2", title="Multiply or Divide",
         look="A number times the variable, or a fraction with the variable on top or bottom.",
         move="Put the number in for the variable, then multiply or divide."),
    dict(key="3", title="Two Operations",
         look="A product or quotient, and a number added or subtracted.",
         move="Put the number in for the variable. Multiply or divide first, then add or subtract."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: each template returns (expression, value)
# ------------------------------------------------------------------
d = lambda r, lo=1, hi=9: r.randint(lo, hi)

def t1_number_plus(r, v):                     # 5 + x
    return written((d(r), ""), (1, v)), d(r)

def t1_minus_number(r, v):                    # x - 5, x >= 5
    a = d(r)
    return written((1, v), (-a, "")), a + d(r)

def t1_number_minus(r, v):                    # 12 - x
    x = d(r)
    return written((x + d(r), ""), (-1, v)), x

def t2_times(r, v):                           # 7 x
    return written((d(r, 2), v)), d(r)

def t2_over_number(r, v):                     # x/4, x = 4 k
    a = d(r, 2)
    return f"{v}/{a}", a * d(r, 2)

def t2_number_over(r, v):                     # 24/x, x divides it
    x = d(r)
    return f"{x * d(r)}/{v}", x

def t3_times_plus(r, v):                      # 3 x + 2
    return written((d(r), v), (d(r), "")), d(r, 2)

def t3_times_minus(r, v):                     # 3 x - 2, at least 0
    a, x = d(r, 2), d(r, 2)
    return written((a, v), (-r.randint(1, a * x), "")), x

def t3_number_minus_times(r, v):              # 20 - 3 x
    b, x = d(r, 2, 5), d(r, 1, 5)
    return written((d(r) + b * x, ""), (-b, v)), x

def t3_number_plus_times(r, v):               # 4 + 3 x
    return written((d(r), ""), (d(r), v)), d(r)

def t3_over_minus(r, v):                      # x/4 - 2
    a, b = d(r, 2), d(r, 1, 5)
    return written((1, f"{v}/{a}"), (-b, "")), a * (d(r) + b)

def t3_over_plus(r, v):                       # x/4 + 2
    a = d(r, 2)
    return written((1, f"{v}/{a}"), (d(r), "")), a * d(r)

def t3_number_plus_over(r, v):                # 5 + x/3
    b = d(r, 2, 6)
    return written((d(r), ""), (1, f"{v}/{b}")), b * d(r)

def t3_number_minus_over(r, v):               # 9 - x/3 (the old no. 12, fixed)
    b, q = d(r, 2, 5), d(r)
    return written((q + d(r), ""), (-1, f"{v}/{b}")), b * q

def t3_number_over_plus(r, v):                # 24/x + 3
    x = d(r)
    return written((1, f"{x * d(r)}/{v}"), (d(r), "")), x

def t3_number_over_minus(r, v):               # 24/x - 3
    x, b = d(r, 2, 6), d(r)
    return written((1, f"{x * (d(r) + b)}/{v}"), (-b, "")), x

def t3_number_minus_number_over(r, v):        # 9 - 12/x
    x, q = d(r, 2, 5), d(r)
    return written((q + d(r), ""), (-1, f"{x * q}/{v}")), x

TEMPLATES = {
    "1": [t1_number_plus, t1_minus_number, t1_number_minus],
    "2": [t2_times, t2_over_number, t2_number_over],
    "3": [t3_times_plus, t3_times_minus, t3_number_minus_times, t3_number_plus_times, t3_over_minus,
          t3_over_plus, t3_number_plus_over, t3_number_minus_over, t3_number_over_plus,
          t3_number_over_minus, t3_number_minus_number_over],
}

def value_of(prompt):
    expr, _, at = prompt.partition(";")
    v, _, x = at.partition("=")
    return to_sympy(expr).subs(sp.Symbol(v.strip()), to_sympy(x))

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    expr, x = TEMPLATES[entry][tpl](r, v)
    prompt = f"{expr} ; {v} = {x}"
    ans = value_of(prompt)
    need(ans.is_integer and ans >= 0)
    return dict(prompt=prompt, answer=str(ans))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if value_of(p["prompt"]) == to_sympy(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing: "expression ; x = 4"
# ------------------------------------------------------------------
def parts(p):
    expr, _, at = p["prompt"].partition(";")
    return expr.strip(), at.strip()

def typst(p, gap="0.3em"):
    expr, at = parts(p)
    return f"{display(dfrac(expr))} when ${at}$"

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    expr, at = parts(p)
    return f"{plain(expr)}  when {at}"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.5 if "/" in p["prompt"] else 0.3

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        ans = value_of(t)
    except Exception:
        raise ValueError("write the expression, then ; and the value: x/4 - 2 ; x = 24") from None
    new = dict(old, prompt=t, answer=str(sp.nsimplify(ans)), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
