"""Khan Prealgebra, Lesson 6-2: Evaluating expressions with one variable,
from the old app's PreAlg_06_02: the same templates as Khan Algebra 1's 1-1
(only the index differs), so the same bank (khan_alg1/ka1_01_01) under
this course.
"""
from ... import gen
from . import courses
from ..khan_alg1 import ka1_01_01 as base

NAME = FAMILY = "kpa_06_02"
FIXED = False
TITLE = "Lesson 6-2: Evaluating expressions with one variable"
INSTRUCTIONS = base.INSTRUCTIONS
COURSES = courses(6)
TYPES, T = base.TYPES, base.T
TYPE, KEYS, ENTRIES, ENTRY = base.TYPE, base.KEYS, base.ENTRIES, base.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
initial_seen, check, typst, answer_typst, text, answer_text, height = (
    base.initial_seen, base.check, base.typst, base.answer_typst, base.text, base.answer_text, base.height)
edit_text, from_edit, answer_edit_text, with_answer = base.edit_text, base.from_edit, base.answer_edit_text, base.with_answer

def seen_key(p):
    return (NAME,) + base.seen_key(p)[1:]

generate = gen.generator(NAME, base.draw, check, seen_key, lambda e: len(base.TEMPLATES[e]))

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
