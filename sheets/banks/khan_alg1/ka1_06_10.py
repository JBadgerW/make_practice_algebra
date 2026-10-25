"""Khan Algebra 1, Lesson 6-10: Reasoning with systems of equations, from the
old app's Alg1_06_10 (twelve generated slots).

Two systems, A and B. (a) How can we get System B from System A? (b) Are
they equivalent? Khan's ten moves: replace one equation with the sum or
difference of both (yes), or only its left side, or only its right side, with
the sum or difference of the sides (no); replace one equation with a
multiple of itself (yes) or of the other equation (no); swap the equations
(yes), or only their left sides, or only their right sides (no); add the same
quantity to both sides of one equation (yes) or to only one side (no). The
wrong choices are the right move's partner and two others, as Khan's.
(The old no. 12 printed "(b) No", right, but marked "Yes" in its choices.)

A problem: dict(type, prompt, choices, answer, source).
    prompt   "eqA1 ; eqA2 | eqB1 ; eqB2"
    answer   "B; Yes"     (part a's letter; part b)
check() works out the move from the two systems' sides alone, and solves
both systems for part (b).
"""
import sympy as sp
from ... import gen
from ...gen import need, signed, signed_except, written
from ...linear import exact
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard

NAME = FAMILY = "ka1_06_10"
FIXED = False
TITLE = "Lesson 6-10: Reasoning with systems of equations"
INSTRUCTIONS = "Answer two questions about Systems A and B."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Which Move?",
         look="Two systems, A and B, where B comes from A by one move.",
         move="Find what changed. Adding equations, multiplying one by a number, swapping them, or doing the "
              "same to both sides keeps the solution; changing only one side, or replacing an equation with a "
              "multiple of the other, does not.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

SUM = "Replace one equation with the sum/difference of both equations."
LHS_SUM = "Replace only the left-hand side of one equation with the sum/difference of the left-hand sides of both equations."
RHS_SUM = "Replace only the right-hand side of one equation with the sum/difference of the right-hand sides of both equations."
SELF = "Replace one equation with a multiple of itself."
OTHER = "Replace one equation with a multiple of the other equation."
SWAP = "Swap the order of the equations."
SWAP_LHS = "Swap only the left-hand sides of both equations."
SWAP_RHS = "Swap only the right-hand sides of both equations."
BOTH = "Replace one equation with itself where the same quantity is added to both sides."
ONE = "Replace one equation with itself where a quantity is added to only one side."
YES = {SUM, SELF, SWAP, BOTH}
PARTNER = {SUM: LHS_SUM, LHS_SUM: SUM, RHS_SUM: SUM, SELF: OTHER, OTHER: SELF, SWAP: SWAP_LHS,
           SWAP_LHS: SWAP, SWAP_RHS: SWAP, BOTH: ONE, ONE: BOTH}
MOVES = [SUM, LHS_SUM, RHS_SUM, SELF, OTHER, SWAP, SWAP_LHS, SWAP_RHS, BOTH, ONE]
QUESTION_A = "How can we get System B from System A?"
QUESTION_B = "Based on the previous answer, are the systems equivalent? In other words, do they have the same solution?"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: System A, then B by one move; an equation is (left, right) in Typst
# ------------------------------------------------------------------
def lin(a, b, c=0):
    return written((a, "x"), (b, "y"), (c, ""))

def draw(entry, r, tpl):
    move = MOVES[tpl]
    x, y = r.randint(-10, 10), r.randint(-10, 10)
    a, b, d, e = signed(r, 1, 9), signed(r, 1, 9), signed(r, 1, 9), signed(r, 1, 9)
    need(a * e != b * d)
    A = [(lin(a, b), str(a * x + b * y)), (lin(d, e), str(d * x + e * y))]
    (L1, R1), (L2, R2) = A
    i = r.randrange(2)                                       # the equation that changes
    k = signed_except(r, 2, 4, 1)
    s = r.choice((1, -1))                                     # sum or difference
    (ai, bi, ci), (aj, bj, cj) = [(a, b, a * x + b * y), (d, e, d * x + e * y)][::1 if i == 0 else -1]
    B = list(A)
    if move == SUM:
        B[i] = (lin(ai + s * aj, bi + s * bj), str(ci + s * cj))
        need(ai + s * aj or bi + s * bj)
    elif move == LHS_SUM:
        B[i] = (lin(ai + s * aj, bi + s * bj), str(ci))
        need((ai + s * aj or bi + s * bj) and cj)
    elif move == RHS_SUM:
        B[i] = (lin(ai, bi), str(ci + s * cj))
        need(cj)
    elif move == SELF:
        B[i] = (lin(k * ai, k * bi), str(k * ci))
    elif move == OTHER:
        B[i] = (lin(k * aj, k * bj), str(k * cj))
    elif move == SWAP:
        B = [A[1], A[0]]
    elif move == SWAP_LHS:
        B = [(L2, R1), (L1, R2)]
        need(R1 != R2)
    elif move == SWAP_RHS:
        B = [(L1, R2), (L2, R1)]
        need(R1 != R2)
    elif move == BOTH:                                        # move the y term across: a x = c - b y
        B[i] = (written((ai, "x")), written((ci, ""), (-bi, "y")))
    else:                                                     # a number added to one side only
        q = signed(r, 1, 9)
        B[i] = (lin(ai, bi, q), str(ci)) if r.random() < 0.5 else (lin(ai, bi), str(ci + q))
    prompt = " ; ".join(f"{l} = {rt}" for l, rt in A) + " | " + " ; ".join(f"{l} = {rt}" for l, rt in B)
    others = [m for m in MOVES if m not in (move, PARTNER[move])]
    r.shuffle(others)
    choices, letter = gen.lettered(r, move, [PARTNER[move]] + others[:2])
    need(classify(prompt) == move)                             # the move is the only reading of the change
    return dict(prompt=prompt, choices=choices, answer=f"{letter}; {'Yes' if move in YES else 'No'}")

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(MOVES))

# ------------------------------------------------------------------
# Checking: the move from the sides alone; part (b) by solving
# ------------------------------------------------------------------
def systems(prompt):
    a, _, b = prompt.partition("|")
    return [[tuple(exact(t) for t in q.split("=")) for q in s.split(";")] for s in (a, b)]

def same(u, v):
    return sp.expand(u - v) == 0

def classify(prompt):
    (A1, A2), (B1, B2) = systems(prompt)
    eq = lambda P, Q: same(P[0], Q[0]) and same(P[1], Q[1])
    if eq(B1, A2) and eq(B2, A1):
        return SWAP
    if same(B1[0], A2[0]) and same(B1[1], A1[1]) and same(B2[0], A1[0]) and same(B2[1], A2[1]):
        return SWAP_LHS
    if same(B1[0], A1[0]) and same(B1[1], A2[1]) and same(B2[0], A2[0]) and same(B2[1], A1[1]):
        return SWAP_RHS
    if eq(B1, A1):
        (Li, Ri), (Lj, Rj), (P, Q) = A2, A1, B2
    elif eq(B2, A2):
        (Li, Ri), (Lj, Rj), (P, Q) = A1, A2, B1
    else:
        raise ValueError("both equations changed")
    D, Di, Dj = P - Q, Li - Ri, Lj - Rj
    sums = [Di + Dj, Di - Dj, Dj - Di]
    if same(Q, Ri) and any(same(P, Li + s * Lj) for s in (1, -1)) and not same(P, Li):
        return LHS_SUM
    if same(P, Li) and any(same(Q, Ri + s * Rj) for s in (1, -1)) and not same(Q, Ri):
        return RHS_SUM
    if same(D, Di):
        return BOTH
    if same(P, Li) != same(Q, Ri):
        return ONE
    if any(same(D, s) for s in sums):
        return SUM
    k = sp.simplify(D / Di)
    if k.is_number:
        return SELF
    if sp.simplify(D / Dj).is_number:
        return OTHER
    raise ValueError("no one move")

def equivalent(prompt):
    a, _, b = prompt.partition("|")
    sa, sb = twovar.solve(a), twovar.solve(b)
    return sa == sb and sa != "many"

def parts_of(p):
    letter, _, yes = p["answer"].partition(";")
    return letter.strip(), yes.strip()

def check(p):
    try:
        letter, yes = parts_of(p)
        ok = gen.chosen(dict(p, answer=letter)) == [classify(p["prompt"])] and \
            yes == ("Yes" if equivalent(p["prompt"]) else "No")
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    a, _, b = p["prompt"].partition("|")
    pair = (f"#grid(columns: 2, column-gutter: 3em, row-gutter: 0.5em, [System A], [System B], "
            f"[{twovar.system_typst(a.strip())}], [{twovar.system_typst(b.strip())}])")
    return (f"{pair}\n    #parts([{QUESTION_A} #pad(left: 1em, top: 0.4em, {gen.choices_typst(p['choices'])[1:]})], "
            f"[{QUESTION_B} #h(1em) Yes #h(1em) No])")

def answer_typst(p):
    letter, yes = parts_of(p)
    return f"(a) {letter} (b) {yes}"

def text(p):
    a, _, b = p["prompt"].partition("|")
    return f"A: {plain(a.strip())}   B: {plain(b.strip())}"

def answer_text(p):
    letter, yes = parts_of(p)
    return f"(a) {letter}. {gen.chosen(dict(p, answer=letter))[0]}  (b) {yes}"

def height(p):
    return 2.2

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for new systems; you can edit the answer")

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
