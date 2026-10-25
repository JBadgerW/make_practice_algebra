"""Khan Algebra 1, Lesson 6-6: Combining equations, from the old app's
Alg1_06_06 (sixteen generated slots, two templates).

What is the result of adding the two equations (or subtracting the second
from the first)? Coefficients -10 to 10, not 0; constants -10 to 10.

A problem: dict(type, prompt, answer, source); prompt "eq1 ; eq2".
    prompt  "3 x - 2 y = 5 ; 4 x + 6 y = -2"
    answer  "7 x + 4 y = 3"
check() reads the answer's coefficients and constant (as written, not up to
a multiple) and compares them with the sum (or difference) of the
equations'.
"""
from ... import gen
from ...gen import signed, written
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard, coefficients, equations

NAME = FAMILY = "ka1_06_06"
FIXED = False
TITLE = "Lesson 6-6: Combining equations"
INSTRUCTIONS = ""
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Add the Equations", instructions="What is the result of adding the two equations?",
         look="Two equations in standard form.",
         move="Add the x terms, add the y terms, and add the numbers on the right."),
    dict(key="2", title="Subtract the Equations",
         instructions="What is the result of subtracting the second equation from the first?",
         look="Two equations in standard form.",
         move="Subtract each term of the second from the matching term of the first. Watch the signs."),
]
T = gen.Types(TYPES, "", space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def combined(prompt, typ):
    (a, b, c), (d, e, f) = (coefficients(q) for q in equations(prompt))
    s = 1 if typ == "1" else -1
    return a + s * d, b + s * e, c + s * f

def draw(entry, r, tpl):
    a, b, d, e = (signed(r, 1, 10) for _ in range(4))
    c, f = r.randint(-10, 10), r.randint(-10, 10)
    prompt = f"{standard(a, b, c)} ; {standard(d, e, f)}"
    A, B, C = combined(prompt, entry)
    return dict(prompt=prompt, answer=f"{written((int(A), 'x'), (int(B), 'y'))} = {int(C)}")

def check(p):
    try:
        return "checked" if coefficients(p["answer"]) == combined(p["prompt"], p["type"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return twovar.system_typst(p["prompt"])

def answer_typst(p):
    return f"${p['answer']}$"

text = twovar.text

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.7

def answer_of_type(typ):
    def answer_of(prompt):
        A, B, C = combined(prompt, typ)
        return f"{written((int(A), 'x'), (int(B), 'y'))} = {int(C)}"
    return answer_of

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    return gen.edits(answer_of_type(old["type"]), check, "3 x - 2 y = 5 ; 4 x + 6 y = -2", "7 x + 4 y = 3")[1](t, old)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
