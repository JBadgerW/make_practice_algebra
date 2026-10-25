"""Khan Algebra 1, Lesson 2-3: Equations with parentheses, from the old app's
Alg1_02_03 (nineteen of Khan's, answered, every answer right).

Khan's equations have one product to distribute, integer solutions from
-4 to 10, multipliers to 9, and numbers to 90. Some need only the
distributing (-4n - 8 = 4(-3n + 2)), some leave like terms to combine
(10p - 3 = 2(12 + 4p) - 7), and some have a minus sign before the
parentheses (7h = -(2h - 18)).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "3 - 2 (b - 2) = 2 - 7 b"
    answer  "b = -1"
check() substitutes the answer into the prompt and requires exactly one solution.
"""
from ... import gen, linear
from ...gen import need, signed, signed_except, written
from . import courses

NAME = FAMILY = "ka1_02_03"
FIXED = False
TITLE = "Lesson 2-3: Equations with parentheses"
INSTRUCTIONS = "Solve each equation."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Distribute, Then Solve",
         look="A number times a sum on one side, and nothing to combine after distributing.",
         move="Distribute. Then gather the variable terms on one side and the numbers on the other, and divide."),
    dict(key="2", title="Distribute, Then Combine",
         look="A product to distribute, with another term on the same side.",
         move="Distribute, then combine like terms on that side. Then solve."),
    dict(key="3", title="A Minus Sign Before Parentheses",
         look="-( ... ): a minus sign in front of the parentheses.",
         move="The minus sign is -1 times the parentheses: change the sign of every term inside. Then solve."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: the solution x, then the pieces; the last constant makes x the solution
# ------------------------------------------------------------------
def solution(r):
    return gen.except_(r, -5, 10, 0)

def inside(r, v, x):
    """b v + c (or c + b v), and its value at x."""
    b, c = signed(r, 1, 5), signed(r, 1, 12)
    text = written((b, v), (c, "")) if r.random() < 0.6 else written((c, ""), (b, v))
    return f"({text})", b * x + c, b

def side(r, v, x, k, value):
    """k v + e (or e + k v) whose value at x is `value`: the side that fixes the solution."""
    e = value - k * x
    need(abs(e) <= 90)
    return written((k, v), (e, "")) if r.random() < 0.6 else written((e, ""), (k, v))

def t1_left(r, v):                            # 2s + 4 = 5(-4 - 2s), mirrored
    x, a = solution(r), signed(r, 2, 9)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, a * b)
    return f"{written((a, par))} = {side(r, v, x, k, a * val)}"

def t1_right(r, v):                           # -4n - 8 = 4(-3n + 2)
    left, _, right = t1_left(r, v).partition(" = ")
    return f"{right} = {left}"

def t1_no_constant(r, v):                     # 8(10 - k) = 2k, 9g = 3(-4 + 5g)
    x, a = solution(r), signed(r, 2, 9)
    par, val, b = inside(r, v, x)
    need(a * val % x == 0)
    k = a * val // x
    need(k != 0 and k != a * b and abs(k) <= 20)
    eq = [written((a, par)), written((k, v))]
    r.shuffle(eq)
    return " = ".join(eq)

def t2_number_before(r, v):                   # 3 - 2(b - 2) = 2 - 7b
    x, a, q = solution(r), signed(r, 2, 9), signed(r, 1, 12)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, a * b)
    return f"{written((q, ''), (a, par))} = {side(r, v, x, k, q + a * val)}"

def t2_number_after(r, v):                    # 7(2e - 1) - 3 = 6 + 6e
    x, a, q = solution(r), signed(r, 2, 9), signed(r, 1, 12)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, a * b)
    return f"{written((a, par), (q, ''))} = {side(r, v, x, k, a * val + q)}"

def t2_variable_after(r, v):                  # 4(3 + c) + c = c + 4
    x, a, f = solution(r), signed(r, 2, 9), signed(r, 1, 9)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, a * b + f)
    need(a * b + f != 0)
    return f"{written((a, par), (f, v))} = {side(r, v, x, k, a * val + f * x)}"

def t2_on_the_right(r, v):                    # 10p - 3 = 2(12 + 4p) - 7
    left, _, right = t2_number_after(r, v).partition(" = ")
    return f"{right} = {left}"

def t3_alone(r, v):                           # -(4 + h) = 3h, 7h = -(2h - 18)
    x = solution(r)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, -b)
    eq = [written((-1, par)), side(r, v, x, k, -val)]
    r.shuffle(eq)
    return " = ".join(eq)

def t3_plus_number(r, v):                     # m = -(4 + m) + 2
    x, q = solution(r), signed(r, 1, 12)
    par, val, b = inside(r, v, x)
    k = signed_except(r, 1, 12, -b)
    return f"{side(r, v, x, k, q - val)} = {written((-1, par), (q, ''))}"

def t3_both_sides(r, v):                      # 6(-2g - 1) = -(13g + 2)
    x, a = solution(r), signed(r, 2, 9)
    par, val, b = inside(r, v, x)
    c = gen.except_(r, 1, 15, -a * b)              # -(13 g + 2): the inside leads with a plus
    e = -(a * val) - c * x                        # -(c v + e) has the value a * val at x
    need(e != 0 and abs(e) <= 30)
    other = f"({written((c, v), (e, ''))})"
    return f"{written((a, par))} = {written((-1, other))}"

TEMPLATES = {
    "1": [t1_left, t1_right, t1_no_constant],
    "2": [t2_number_before, t2_number_after, t2_variable_after, t2_on_the_right],
    "3": [t3_alone, t3_plus_number, t3_both_sides],
}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    prompt = TEMPLATES[entry][tpl](r, v)
    return dict(prompt=prompt, answer=linear.answer_of(prompt))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if linear.solves(p["prompt"], p["answer"], "fraction") else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    linear.answer_of, check, "3 - 2 (b - 2) = 2 - 7 b", "b = -1")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
