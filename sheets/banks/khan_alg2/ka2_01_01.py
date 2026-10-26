"""Khan Algebra 2, Lesson 1-1: Polynomials intro, from the old app's
Alg2_01_01: the same twelve items as Khan Algebra 1's 13-1 (one answered,
right), so the same bank (khan_alg1/ka1_13_01) under this course.
"""
from ... import gen
from . import courses
from ..khan_alg1 import ka1_13_01 as base

NAME = FAMILY = "ka2_01_01"
FIXED = False
TITLE = "Lesson 1-1: Polynomials intro"
INSTRUCTIONS = base.INSTRUCTIONS
COURSES = courses(1)
TYPES, T = base.TYPES, base.T
TYPE, KEYS, ENTRIES, ENTRY = base.TYPE, base.KEYS, base.ENTRIES, base.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
initial_seen, check, typst, answer_typst, text, answer_text, height = (
    base.initial_seen, base.check, base.typst, base.answer_typst, base.text, base.answer_text, base.height)
edit_text, from_edit, answer_edit_text, with_answer = base.edit_text, base.from_edit, base.answer_edit_text, base.with_answer

def seen_key(p):
    return (NAME,) + base.seen_key(p)[1:]

generate = gen.generator(NAME, base.draw, check, seen_key, lambda e: 1)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
