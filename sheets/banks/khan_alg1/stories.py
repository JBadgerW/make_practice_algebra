"""Word problems whose model is a system of two linear equations, shared by the
Khan Algebra 1 Unit 6 story banks. (Not a bank.)

A story: dict(key, type, text, ask, answer, draw, model).
    text, ask      the story and its question, with {placeholders} for its numbers and names
    answer         the key, with {u} and {v} for the two unknowns' values
    draw(r)        the story's numbers (as written) and names: a dict for text
    fmt            optional: how the answer writes its values (money: $2.20)
    model(n)       from the numbers read back (Fractions, by placeholder): the two
                   equations ((a, b, c), (d, e, f)), a u + b v = c and d u + e v = f

    fill_story(st, w)         the prompt: the text and the question
    solve_story(st, prompt)   read the numbers out of the words, and solve: (u, v), "none", or "many"
    key(st, prompt)           the answer as the key writes it
"""
from fractions import Fraction as F
from ... import gen

def money(x):
    """$ amounts as written: 55, 2.75, 11.50."""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{float(x):.2f}"

def show(x):
    """A number as written: 12, 2.5, 0.75 (at most two decimal places)."""
    return gen.decimal(F(x), 2)

def fill_story(st, w):
    return gen.fill(st["text"] + " " + st["ask"], **w)

def numbers(st, prompt):
    """The story's placeholders read back: numbers as Fractions, words as they are."""
    v = gen.read(st["text"] + " " + st["ask"], prompt)
    out = {}
    for k, s in v.items():
        try:
            out[k] = gen.number(s)
        except (ValueError, ZeroDivisionError):
            out[k] = s
    return out

def solve_system(eqs):
    (a, b, c), (d, e, f) = eqs
    det = a * e - b * d
    if det:
        return (c * e - b * f) / det, (a * f - c * d) / det
    return "many" if a * f - c * d == 0 and b * f - c * e == 0 else "none"

def solve_story(st, prompt):
    return solve_system(st["model"](numbers(st, prompt)))

def key(st, prompt):
    """The key, its values written as the story's "fmt" says (default show; money keeps its cents)."""
    fmt = st.get("fmt", show)
    s = solve_story(st, prompt)
    if not isinstance(s, tuple):
        raise ValueError(f"the story's system has {s} solutions")
    w = numbers(st, prompt)
    return gen.fill(st["answer"], **{k: x for k, x in w.items() if isinstance(x, str)}, u=fmt(s[0]), v=fmt(s[1]))
