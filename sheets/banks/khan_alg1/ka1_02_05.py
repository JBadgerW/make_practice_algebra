"""Khan Algebra 1, Lesson 2-5: Reasoning with linear equations, from the old
app's Alg1_02_05 (four generated slots and eight of Khan's, answered, every
answer right).

Two equations, A and B. (a) Which move turns A into B? (b) Are they
equivalent? The moves are Khan's seven: add/subtract the same quantity on
both sides (yes) or on one side only (no); multiply/divide both sides by
the same nonzero constant (yes), one side only (no), or both sides by a
variable expression (no: dividing 5x = 2x by x loses x = 0); rewrite a side
by combining like terms or by distributing (yes). One type: the move is
the question, so a header naming it would give it away. The wrong choices
are the right move's partner (the same move on one side only, say) and a
pair of other moves, as in Khan's.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "4 x + 2 = 6 - x ; 5 x + 2 = 6"     (A ; B)
    choices  four moves
    answer   "B; Yes"                              (part a's letter; part b)
check() works out the move from the equations alone: the same quantity
added to both sides, both sides in the same constant (or variable) ratio,
one side unchanged, or both sides rewritten as equal expressions; and
solves both equations for part (b).
"""
import sympy as sp
from ... import gen, linear
from ...gen import need, signed, signed_except, written
from ...typmath import text as plain
from . import courses

NAME = FAMILY = "ka1_02_05"
FIXED = False
TITLE = "Lesson 2-5: Reasoning with linear equations"
INSTRUCTIONS = "Answer two questions about Equations A and B."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Which Move?",
         look="Two equations, A and B, where B comes from A by one move.",
         move="Compare the sides. Did both sides change the same way (equivalent), or only one side (not)? "
              "Multiplying or dividing by a variable can lose or add a solution.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

ADD_BOTH = "Add/subtract the same quantity to/from both sides"
ADD_ONE = "Add/subtract a quantity to/from only one side"
MUL_BOTH = "Multiply/divide both sides by the same non-zero constant"
MUL_ONE = "Multiply/divide only one side by a non-zero constant"
MUL_VAR = "Multiply/divide both sides by the same variable expression"
COMBINE = "Rewrite one side (or both) by combining like terms"
DISTRIBUTE = "Rewrite one side (or both) using the distributive property"
EQUIVALENT = {ADD_BOTH: True, ADD_ONE: False, MUL_BOTH: True, MUL_ONE: False, MUL_VAR: False,
              COMBINE: True, DISTRIBUTE: True}
PARTNER = {ADD_BOTH: ADD_ONE, ADD_ONE: ADD_BOTH, MUL_BOTH: MUL_ONE, MUL_ONE: MUL_BOTH, MUL_VAR: MUL_BOTH,
           COMBINE: DISTRIBUTE, DISTRIBUTE: COMBINE}
PAIRS = [(ADD_BOTH, ADD_ONE), (MUL_BOTH, MUL_ONE), (COMBINE, DISTRIBUTE), (MUL_BOTH, MUL_VAR)]
QUESTION_A = "How can we get Equation B from Equation A?"
QUESTION_B = "Based on the previous answer, are the equations equivalent? In other words, do they have the same solution?"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: each template is one move, (A, B)
# ------------------------------------------------------------------
def eq(left, right):
    return f"{left} = {right}"

def add_both_variable(r):                     # a x - 1 = c x  ->  -1 = b x
    a, b, q = r.randint(2, 8), signed(r, 2, 8), signed(r, 1, 9)
    return eq(written((a, "x"), (q, "")), written((a + b, "x"))), eq(str(q), written((b, "x")))

def add_both_opposite(r):                     # 4x + 2 = 6 - x  ->  5x + 2 = 6
    a, c, q, s = r.randint(2, 8), r.randint(1, 6), signed(r, 1, 9), signed(r, 1, 12)
    return eq(written((a, "x"), (q, "")), written((s, ""), (-c, "x"))), eq(written((a + c, "x"), (q, "")), str(s))

def add_both_number(r):                       # 3x - 1 = 7  ->  3x = 8
    a, q, s = signed_except(r, 1, 9, 1, -1), signed(r, 1, 9), signed(r, 1, 20)
    need(s - q != 0)
    return eq(written((a, "x"), (q, "")), str(s)), eq(written((a, "x")), str(s - q))

def add_one_number(r):                        # 5x - 2 + x = x - 4  ->  5x + x = x - 4
    a, b, q, c, s = r.randint(2, 8), r.randint(1, 5), signed(r, 1, 9), r.randint(1, 4), signed(r, 1, 9)
    return (eq(written((a, "x"), (q, ""), (b, "x")), written((c, "x"), (s, ""))),
            eq(written((a, "x"), (b, "x")), written((c, "x"), (s, ""))))

def add_one_simple(r):                        # 3x - 1 = 7  ->  3x = 7
    a, q, s = signed_except(r, 1, 9, 1, -1), signed(r, 1, 9), signed(r, 1, 20)
    return eq(written((a, "x"), (q, "")), str(s)), eq(written((a, "x")), str(s))

def mul_both_product(r):                      # 2(x + 2) = 10  ->  x + 2 = 5
    a, b, k = r.randint(2, 6), signed(r, 1, 9), signed(r, 2, 9)
    return eq(written((a, f"(x {'+' if b > 0 else '-'} {abs(b)})")), str(a * k)), eq(written((1, "x"), (b, "")), str(k))

def mul_both_fraction(r):                     # x/4 + 1 = -3  ->  x + 4 = -12
    a, b, k = r.randint(2, 6), signed(r, 1, 9), signed(r, 1, 9)
    return eq(f"x/{a}" + (f" + {b}" if b > 0 else f" - {-b}"), str(k)), eq(written((1, "x"), (a * b, "")), str(a * k))

def mul_both_divide(r):                       # 5x = 20  ->  x = 4
    a, k = signed_except(r, 2, 9), signed(r, 1, 9)
    return eq(written((a, "x")), str(a * k)), eq("x", str(k))

def mul_one_product(r):                       # 3(x + 2) = 18  ->  x + 2 = 18
    a, b, c = r.randint(2, 6), signed(r, 1, 9), signed(r, 2, 30)
    return eq(written((a, f"(x {'+' if b > 0 else '-'} {abs(b)})")), str(c)), eq(written((1, "x"), (b, "")), str(c))

def mul_one_divide(r):                        # 5x = 20  ->  x = 20
    a, k = r.randint(2, 9), signed(r, 1, 9)
    return eq(written((a, "x")), str(a * k)), eq("x", str(a * k))

def mul_var_terms(r):                         # 7x = 3x  ->  7 = 3
    a, b = r.sample(range(2, 10), 2)
    return eq(written((a, "x")), written((b, "x"))), eq(str(a), str(b))

def mul_var_factor(r):                        # 2(x + 3) = 5(x + 3)  ->  2 = 5
    a, b = r.sample(range(2, 10), 2)
    c = signed(r, 1, 9)
    f = f"(x {'+' if c > 0 else '-'} {abs(c)})"
    return eq(written((a, f)), written((b, f))), eq(str(a), str(b))

def combine_left(r):                          # 2x - 1 + 3x = 0  ->  5x - 1 = 0
    a, b, q, s = r.randint(1, 8), signed(r, 1, 8), signed(r, 1, 9), signed(r, 0, 12)
    need(a + b != 0)
    return eq(written((a, "x"), (q, ""), (b, "x")), str(s)), eq(written((a + b, "x"), (q, "")), str(s))

def combine_numbers(r):                       # 4x + 3 - 7 = 9  ->  4x - 4 = 9
    a, q, t, s = signed(r, 2, 8), signed(r, 1, 9), signed(r, 1, 9), signed(r, 1, 12)
    need(q + t != 0)
    return eq(written((a, "x"), (q, ""), (t, "")), str(s)), eq(written((a, "x"), (q + t, "")), str(s))

def distribute_left(r):                       # 4(x + 3) = 18  ->  4x + 12 = 18
    a, b, c = signed(r, 2, 6), signed(r, 1, 9), signed(r, 1, 30)
    return eq(written((a, f"(x {'+' if b > 0 else '-'} {abs(b)})")), str(c)), eq(written((a, "x"), (a * b, "")), str(c))

def distribute_right(r):                      # 5 = -2(x - 1)  ->  5 = -2x + 2
    a, b, c = signed(r, 2, 6), signed(r, 1, 9), signed(r, 1, 30)
    return eq(str(c), written((a, f"(x {'+' if b > 0 else '-'} {abs(b)})"))), eq(str(c), written((a, "x"), (a * b, "")))

TEMPLATES = {"1": [(ADD_BOTH, add_both_variable), (ADD_BOTH, add_both_opposite), (ADD_BOTH, add_both_number),
                   (ADD_ONE, add_one_number), (ADD_ONE, add_one_simple),
                   (MUL_BOTH, mul_both_product), (MUL_BOTH, mul_both_fraction), (MUL_BOTH, mul_both_divide),
                   (MUL_ONE, mul_one_product), (MUL_ONE, mul_one_divide),
                   (MUL_VAR, mul_var_terms), (MUL_VAR, mul_var_factor),
                   (COMBINE, combine_left), (COMBINE, combine_numbers),
                   (DISTRIBUTE, distribute_left), (DISTRIBUTE, distribute_right)]}

def draw(entry, r, tpl):
    right, make = TEMPLATES[entry][tpl]
    a, b = make(r)
    pairs = [p for p in PAIRS if right not in p and PARTNER[right] not in p]
    wrong = [PARTNER[right], *r.choice(pairs)]
    choices, letter = gen.lettered(r, right, wrong)
    yes = "Yes" if EQUIVALENT[right] else "No"
    need(same_solutions(a, b) == EQUIVALENT[right])
    return dict(prompt=f"{a} ; {b}", choices=choices, answer=f"{letter}; {yes}")

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Checking: the move, read from the two equations
# ------------------------------------------------------------------
def same_solutions(a, b):
    """Do equations a and b (Typst) have the same solutions, in x?"""
    x = sp.Symbol("x")
    def sols(e):
        l, r = linear.sides(e)
        return sp.solveset(l - r, x, sp.S.Reals)
    return sols(a) == sols(b)

def move(a, b):
    """The move that turns equation a into b, from the equations alone."""
    (la, ra), (lb, rb) = linear.sides(a), linear.sides(b)
    zero = lambda e: sp.simplify(e) == 0
    if zero(la - lb) and zero(ra - rb):                       # both sides rewritten as equal expressions
        return DISTRIBUTE if a.count("(") > b.count("(") else COMBINE
    if zero(la - lb) or zero(ra - rb):                        # one side unchanged
        new, old = (rb, ra) if zero(la - lb) else (lb, la)
        k = sp.simplify(new / old) if old != 0 else None
        return MUL_ONE if k is not None and k.is_number and k != 1 else ADD_ONE
    if zero((la - lb) - (ra - rb)):
        return ADD_BOTH
    if zero(la * rb - lb * ra):                               # la/lb = ra/rb
        k = sp.simplify(la / lb)
        return MUL_BOTH if k.is_number else MUL_VAR
    raise ValueError("B doesn't come from A by one move")

def parts_of(p):
    a, _, b = p["prompt"].partition(";")
    letter, _, yes = p["answer"].partition(";")
    return a.strip(), b.strip(), letter.strip(), yes.strip()

def check(p):
    try:
        a, b, letter, yes = parts_of(p)
        right = gen.chosen(dict(p, answer=letter)) == [move(a, b)]
        return "checked" if right and yes == ("Yes" if same_solutions(a, b) else "No") else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def equations(a, b):
    rows = []
    for name, e in (("A.", a), ("B.", b)):
        l, _, r = e.partition("=")
        rows += [f"[{name}]", f"align(right)[${l.strip()}$]", f"[$= {r.strip()}$]"]
    return f"#grid(columns: 3, column-gutter: 0.4em, row-gutter: 0.65em, {', '.join(rows)})"

def typst(p, gap="0.3em"):
    a, b, _, _ = parts_of(p)
    return (f"{equations(a, b)}\n    #v(0.3em)\n"
            f"    #parts([{QUESTION_A} #pad(left: 1em, top: 0.4em, {gen.choices_typst(p['choices'])[1:]})], "
            f"[{QUESTION_B} #h(1em) Yes #h(1em) No])")

def answer_typst(p):
    _, _, letter, yes = parts_of(p)
    return f"(a) {gen.choice_answer_typst(dict(p, answer=letter))} (b) {yes}"

def text(p):
    a, b, _, _ = parts_of(p)
    return f"A: {plain(a)}   B: {plain(b)}      " + gen.choices_text(p["choices"])

def answer_text(p):
    _, _, letter, yes = parts_of(p)
    return f"(a) {letter}. {gen.chosen(dict(p, answer=letter))[0]}  (b) {yes}"

def height(p):
    return 1.6

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    a, sep, b = t.replace("−", "-").partition(";")
    a, b = " ".join(a.split()), " ".join(b.split())
    try:
        right = move(a, b)
    except Exception:
        raise ValueError("write the two equations, A ; B, where B comes from A by one move: 3 x - 1 = 7 ; 3 x = 8") from None
    choices = old["choices"] if right in old["choices"] else [right] + [c for c in old["choices"] if c != PARTNER[right]][:3]
    yes = "Yes" if same_solutions(a, b) else "No"
    new = dict(old, prompt=f"{a} ; {b}", choices=choices, answer=f"{gen.ABC[choices.index(right)]}; {yes}", source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    letter, _, yes = t.partition(";")
    letter, yes = letter.strip().upper(), yes.strip().capitalize()
    if letter not in gen.ABC[:len(p["choices"])] or yes not in ("Yes", "No"):
        raise ValueError("write the letter, then ; and Yes or No: B; Yes")
    new = dict(p, answer=f"{letter}; {yes}")
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
