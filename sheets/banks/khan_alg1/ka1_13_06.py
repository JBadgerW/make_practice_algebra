"""Khan Algebra 1, Lesson 13-6: Multiply difference of squares, from the old app's Alg1_13_06
(twelve generated slots).

(a + b)(a - b): (x + 7)(x - 7), (5 + x)(5 - x), (3 x - 4)(3 x + 4).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(3 x - 4) (3 x + 4)"
    answer  "9 x^2 - 16"
check() expands the prompt and requires the answer to be the same
polynomial, multiplied out, its degrees in order. When the binomials lead
with their numbers, (5 + x)(5 - x), the key does too: 25 - x^2.
"""
from ... import gen
from . import courses
from .polybank import binomial, checker, expand_edits, expand_answer_of

NAME = FAMILY = "ka1_13_06"
FIXED = False
TITLE = "Lesson 13-6: Multiply difference of squares"
INSTRUCTIONS = "Expand. Combine like terms."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Sum Times Difference",
         look="Two binomials alike but for one sign.",
         move="The middle terms cancel: (a + b)(a - b) = a^2 - b^2. Square the first term, subtract the square of the second."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_x(r, v):                                  # (x + 7)(x - 7)
    e = r.randint(1, 9)
    pair = [binomial(1, e, v), binomial(1, -e, v)]
    r.shuffle(pair)
    return " ".join(pair)

def t_number_first(r, v):                      # (5 + x)(5 - x)
    e = r.randint(1, 9)
    pair = [binomial(1, e, v, True), binomial(-1, e, v, True)]
    r.shuffle(pair)
    return " ".join(pair)

def t_coefficient(r, v):                       # (3x - 4)(3x + 4)
    d, e = r.randint(2, 9), r.randint(1, 9)
    pair = [binomial(d, e, v), binomial(d, -e, v)]
    r.shuffle(pair)
    return " ".join(pair)

def t_coefficient_number_first(r, v):          # (4 - 3x)(4 + 3x)
    d, e = r.randint(2, 9), r.randint(1, 9)
    pair = [binomial(d, e, v, True), binomial(-d, e, v, True)]
    r.shuffle(pair)
    return " ".join(pair)

TEMPLATES = {"1": [t_x, t_number_first, t_coefficient, t_coefficient_number_first]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=expand_answer_of(prompt, follow=True))

check = checker(True)                         # 25 - x^2 for (5 + x)(5 - x)
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(3 x - 4) (3 x + 4)", "9 x^2 - 16", follow=True)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
