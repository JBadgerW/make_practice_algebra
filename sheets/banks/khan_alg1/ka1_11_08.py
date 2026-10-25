"""Khan Algebra 1, Lesson 11-8: Simplify square roots (variables), from the
old app's Alg1_11_08: as Lesson 11-7 (ka1_11_07), with a variable to a
power 1 to 9 under the root: sqrt(72 x^5) = 6 x^2 sqrt(2 x).
"""
from ... import gen
from . import courses
from .ka1_11_07 import radicand, draw_with, check, answer_of, initial_seen

NAME = FAMILY = "ka1_11_08"
FIXED = False
TITLE = "Lesson 11-8: Simplify square roots (variables)"
INSTRUCTIONS = "Simplify. Remove all perfect squares from inside the square root. Assume each variable is positive."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Numbers and a Variable",
         look="The square root of a number times a power of a variable.",
         move="Take out the largest perfect square from the number. For the variable, half the exponent comes "
              "out front; an odd exponent leaves one factor inside."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def seen_key(p):
    return (NAME, p["prompt"])

draw = draw_with(lambda r: {r.choice("abxyz"): r.randint(1, 9)})
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "sqrt(72 x^5)", "6 x^2 sqrt(2 x)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
