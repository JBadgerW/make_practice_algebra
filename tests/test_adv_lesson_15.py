"""Lesson 15 (Advanced Math): two-column proofs. Every source is reachable and its key is
the deck's proof; the proof checker rejects broken proofs; every type draws, checks, and
keeps its rules; edits solve again.

    python3 tests/test_adv_lesson_15.py
"""
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_15 as B

lib = library.current()
assert "adv_lesson_15" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 15: Assumptions, Proofs, Euclid's Postulates, Two-Column Proofs"
assert all(B.type_instructions(k) == "Write a two-column proof." for k in B.KEYS)

# ---- every source: the deck's proof, row for row, and checked
SOURCES = [   # (id, type, prompt, the deck's rows)
    ("ex 15.5", "3", "split A C B D; B D bis angle A B C, A B = C B; show A D = C D",
     "A B = C B | given; B D bis angle A B C | given; angle A B D = angle C B D | bisector; B D = B D | reflexive; "
     "triangle A B D = triangle C B D | SAS; A D = C D | CPCTC"),
    ("ex 15.6", "2", "para P Q R S; angle Q = angle S, P Q par S R; show triangle P Q R = triangle R S P",
     "angle Q = angle S | given; P Q par S R | given; angle Q P R = angle S R P | parallel; "
     "angle Q R P = angle S P R | third; P R = P R | reflexive; triangle P Q R = triangle R S P | AAAS"),
    ("PS 5", "1", "split A B C D; A C = B C, angle A C D = angle B C D; show triangle A C D = triangle B C D",
     "A C = B C | given; angle A C D = angle B C D | given; C D = C D | reflexive; "
     "triangle A C D = triangle B C D | SAS"),
    ("PS 6", "1", "kite A B C D; A B = A D, B C = D C; show triangle A B C = triangle A D C",
     "A B = A D | given; B C = D C | given; A C = A C | reflexive; triangle A B C = triangle A D C | SSS"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt))
    assert B.kind_of(prompt) == typ, sid
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# the key's reasons as the deck words them
p = dict(type="2", prompt=SOURCES[1][2], answer=SOURCES[1][3])
assert "Parallel lines cut by a transversal: alternate interior angles are congruent" in B.answer_typst(p)
assert "the third angles are congruent" in B.answer_typst(p)
assert "#emph[AAAS] congruency postulate" in B.answer_typst(p)

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 15.5": dict(family="split", names=("A", "C", "B", "D"), givens=(0, 1), goal=1),
    "ex 15.6": dict(family="para", names=("P", "Q", "R", "S"), givens=(0, 1), goal=0),
    "PS 5": dict(family="split", names=("A", "B", "C", "D"), givens=(1, 2), goal=0),
    "PS 6": dict(family="kite", names=("A", "B", "C", "D"), givens=(0, 1), goal=0),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)
for sid, params in REACH.items():
    assert B.build(**params) == prompt_of[sid], (sid, B.build(**params))
    assert B.in_range(B.build, params), sid
    assert (params["givens"], params["goal"]) in B.combos(type_of[sid], params["family"]), sid
assert set(type_of.values()) == set(B.KEYS)
for k in B.KEYS:                                                     # the stored table is what enumeration makes
    for f in B.FAMILIES:
        assert B.combos(k, f) == B.enumerate_combos(k, f), (k, f)
assert not B.in_range(B.build, dict(family="split", names=("A", "C", "B", "D"), givens=(0, 1, 3), goal=1))  # a given not needed
assert not B.in_range(B.build, dict(family="split", names=("A", "B", "D", "C"), givens=(0, 1), goal=1))     # letters out of order
assert not B.in_range(B.build, dict(family="kite", names=("A", "B", "C", "D"), givens=(0,), goal=0))        # not proved

# ---- broken proofs fail
P55, A55 = SOURCES[0][2], SOURCES[0][3]
P56, A56 = SOURCES[1][2], SOURCES[1][3]
P6, A6 = SOURCES[3][2], SOURCES[3][3]
WRONG = [
    ("3", P55, A55.replace("B D = B D | reflexive; ", "")),                           # the shared side unstated
    ("3", P55, A55.replace("| SAS", "| SSS")),                                         # the wrong postulate
    ("3", P55, A55.replace("triangle A B D = triangle C B D", "triangle A B D = triangle B C D")),   # vertices crossed
    ("3", P55, A55.replace("angle A B D = angle C B D | bisector; ", "")),             # the bisector not used
    ("3", P55, A55.replace("A B = C B | given; ", "")),                                # a given left out
    ("3", P55, "A D = C D | CPCTC"),                                                    # CPCTC before any congruence
    ("3", P55, A55.replace("B D bis angle A B C | given", "A D = C D | given")),       # not a given
    ("2", P56, A56.replace("angle Q P R = angle S R P", "angle Q P R = angle R S P")), # not alternate interior
    ("2", P56, A56.replace("angle Q R P = angle S P R | third; ", "")),                # AAAS on two angles
    ("2", P56, A56.replace("| AAAS", "| SAS")),
    ("1", P6, A6.replace("| SSS", "| SAS")),
    ("1", P6, A6 + "; A B = A D | CPCTC"),                                              # the last row isn't the goal
    ("1", P6, "A B = A D, Given; B C = D C, Given"),                                    # not rows
    ("3", P6, A6),                                                                     # the wrong type
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (answer, got)

# ---- every type: drawn, checked, and in its rules
rng = random.Random(15)
for k in B.KEYS:
    for i in range(60):
        if i % 10 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        rows = B.rows_of(p["answer"])
        codes = [c for _, c in rows]
        assert codes[0] == "given" and codes.count("given") == len(B.read(p["prompt"])[1]), p
        if k == "1":
            assert set(codes) <= {"given", "reflexive", "SSS", "SAS", "AAAS", "third"} and codes[-1] in B.POSTULATES, p
        if k == "2":
            assert {"bisector", "midpoint", "parallel"} & set(codes) and codes[-1] in B.POSTULATES, p
        if k == "3":
            assert codes[-1] == "CPCTC" and codes[-2] in B.POSTULATES, p
            F_, _, goal = B.read(p["prompt"])
            assert not any(B.same_fact(F_, f, goal) for f, _ in rows[:-1]), p   # the goal comes last only
        assert "cetz.canvas" in B.typst(p) and B.slide_typst(p) is not None, p

# ---- showing
s = dict(type="3", prompt=P55, answer=A55)
assert B.typst(s).startswith("Given: $overline(B D)$ is the angle bisector of angle $B$ and "
                             "$overline(A B) tilde.equiv overline(C B)$. Write a two-column proof to prove: "
                             "$overline(A D) tilde.equiv overline(C D)$."), B.typst(s)
assert B.text(s).startswith("Given: BD is the angle bisector of angle B and AB ≅ CB."), B.text(s)
assert B.answer_text(s).splitlines()[4] == "5. △ABD ≅ △CBD   SAS congruency postulate", B.answer_text(s)
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)
assert "arrows" not in B.typst(s)
assert B.figure(dict(type="2", prompt=P56)).count("line(") > B.figure(dict(type="1", prompt=P6)).count("line(")   # the arrowheads

# ---- editing: a new prompt is solved again; a typed proof is checked
p, status = B.from_edit("kite E F G H; F G = H G, G E bis angle F G H; show triangle E F G = triangle E H G",
                        dict(type="2", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"].endswith("triangle E F G = triangle E H G | SAS"), p
p, status = B.with_answer(p, p["answer"].replace("| SAS", "| SSS"))
assert status != "checked", p
for typ, bad in (("1", "kite A B C D; A B = A D"), ("3", "split A B C D; A C = B C; show A D = B D"),
                 ("2", "kite A B C D; A B = A D, B C = D C; show triangle A B C = triangle A D C")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_15: ok")
