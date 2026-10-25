"""Khan Algebra 1, Lesson 8-4: Function inputs & outputs: equation, from the
old app's Alg1_08_04 (thirteen generated slots).

f(t) = 3 t + 5; f( ? ) = 26: find the input. Coefficients -12 to 12 (not
-1 to 1), constants to 30, inputs -12 to 12.

A problem: dict(type, prompt, answer, source).
    prompt  "f(t) = 3 t + 5 ; 26"     (the definition ; the output)
    answer  "t = 7"
check() substitutes the answer into the definition and requires the output.
"""
import re
from ... import gen
from ...gen import signed, written
from ...linear import exact
from ...typmath import display, dfrac, text as plain, tx
from ... import linear
from . import courses

NAME = FAMILY = "ka1_08_04"
FIXED = False
TITLE = "Lesson 8-4: Function inputs & outputs: equation"
INSTRUCTIONS = "Find the input that gives each output."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Input from an Output",
         look="A function and the value it outputs: f( ) = 26.",
         move="Set the function's rule equal to the output, and solve for the letter."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
DEF = re.compile(r"\s*(\w)\((\w)\)\s*=\s*(.+)")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def parts(prompt):
    definition, _, out = prompt.partition(";")
    f, v, body = DEF.match(definition).groups()
    return f, v, body, out.strip()

def answer_of(prompt):
    f, v, body, out = parts(prompt)
    return linear.answer_of(f"{body} = {out}")

def draw(entry, r, tpl):
    f, v = r.choice("fgh"), r.choice("xt")
    x, a, b = signed(r, 1, 12), signed(r, 2, 12), signed(r, 1, 30)
    prompt = f"{f}({v}) = {written((a, v), (b, ''))} ; {a * x + b}"
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        f, v, body, out = parts(p["prompt"])
        return "checked" if linear.solves(f"{body} = {out}", p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    f, v, body, out = parts(p["prompt"])
    return f"{display(dfrac(f'{f}({v}) = {body}'))} \\\n    ${f}($#h(0.5in)$) = {out}$"

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    f, v, body, out = parts(p["prompt"])
    return plain(f"{f}({v}) = {body};  {f}( ? ) = {out}")

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.5

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "f(t) = 3 t + 5 ; 26", "t = 7")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
