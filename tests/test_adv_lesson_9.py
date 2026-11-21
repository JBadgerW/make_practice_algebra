"""Lesson 9 (Advanced Math): congruent figures, proof outlines. Every source is
reachable from in-range parameters and checks with the deck's answer; the
combos table is the enumeration's; wrong answers fail; every type draws, checks,
and keeps its shape; figures compile from the data; edits solve again.

    python3 tests/test_adv_lesson_9.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_9 as B

lib = library.current()
assert "adv_lesson_9" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 9: Congruent Figures, Proof Outlines"
assert B.type_instructions("1") == "State the congruency postulate (SSS, SAS, AAAS, or HL) that proves the triangles congruent."
assert B.type_instructions("2") == B.type_instructions("3") == B.type_instructions("4") == B.OUTLINE

# ---- the combos table is what the enumeration makes
for (k, fam), table in B.COMBOS.items():
    assert table == B.enumerate_combos(k, fam), (k, fam)
for k, tpls in B.TEMPLATES.items():
    for pick, build in tpls:
        assert build in B.RANGES

# ---- every source, and its key
SOURCES = [   # (id, type, prompt, key)
    ("ex 9.1", "3", "split A B C D; A D = B D, D C perp A B; show A C = B C",
     "triangle D A C = triangle D B C, SAS; A C = B C, CPCTC"),
    ("ex 9.2", "4", "cevians E H D F G; angle E = angle H, E F = H G; show D F = D G",
     "triangle E D F = triangle H D G, SAS; D F = D G, CPCTC"),
    ("ex 9.3", "4", "mids A B C D E F G; A G = E F, C A = C E, B mid C A, D mid C E; show B G = D F",
     "triangle A B G = triangle E D F, SAS; B G = D F, CPCTC"),
    ("PS 9a", "1", "postulate pair A B C D E F; A B = D E, angle A = angle D, angle B = angle E; "
                   "triangle A B C = triangle D E F", "AAAS"),
    ("PS 9b", "1", "postulate split W Y X Z; W X = Y X, angle W X Z = angle Y X Z; triangle W X Z = triangle Y X Z",
     "SAS"),
    ("PS 9c", "1", "postulate kite P Q R S; Q R = S R, P Q = P S; triangle P Q R = triangle P S R", "SSS"),
    ("PS 9d", "1", "postulate kite A B C D; A B = A D, A B perp B C, A D perp D C; triangle A B C = triangle A D C",
     "HL"),
    ("PS 10", "2", "split A C B D; A B = C B, angle A B D = angle C B D; show triangle A B D = triangle C B D",
     "triangle A B D = triangle C B D, SAS"),
    ("PS 11", "3", "kite A B C D; B C = D C, A B = A D; show angle A B C = angle A D C",
     "triangle A B C = triangle A D C, SSS; angle A B C = angle A D C, CPCTC"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
src = {s[0]: dict(type=s[1], prompt=s[2], answer=s[3]) for s in SOURCES}
for sid, typ, prompt, key in SOURCES:
    assert B.answer_of(prompt) == key, (sid, B.answer_of(prompt))
    assert B.kind_of(prompt) == typ, sid
    assert B.check(src[sid]) == "checked", sid
# 9.1: the deck's vertex order (ADC = BDC) is a correspondence too, and checks
assert B.check(dict(src["ex 9.1"], answer="triangle A D C = triangle B D C, SAS; A C = B C, CPCTC")) == "checked"
# step 1, as the deck writes it
assert B.answer_text(src["ex 9.2"]).splitlines()[0] == "1. DE ≅ DH   sides opposite congruent angles"
assert B.answer_text(src["ex 9.3"]).splitlines()[:2] == ["1. ∠A ≅ ∠E   base angles of an isosceles triangle",
                                                          "AB ≅ ED   halves of congruent segments"]
assert B.answer_text(src["PS 11"]) == "1. Mark the figure.\n2. △ABC ≅ △ADC   SSS\n3. ∠ABC ≅ ∠ADC   CPCTC"

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 9.1": (B.build_outline, dict(family="split", names=("A", "B", "C", "D"), givens=(0, 2), goal=0)),
    "ex 9.2": (B.build_outline, dict(family="cevians", names=("E", "H", "D", "F", "G"), givens=(0, 2), goal=0)),
    "ex 9.3": (B.build_outline, dict(family="mids", names=tuple("ABCDEFG"), givens=(0, 4, 6, 7), goal=0)),
    "PS 9a": (B.build_name, dict(family="pair", names=tuple("ABCDEF"), givens=(0, 3, 4))),
    "PS 9b": (B.build_name, dict(family="split", names=("W", "Y", "X", "Z"), givens=(3, 4))),
    "PS 9c": (B.build_name, dict(family="kite", names=tuple("PQRS"), givens=(0, 1))),
    "PS 9d": (B.build_name, dict(family="kite", names=tuple("ABCD"), givens=(1, 5))),
    "PS 10": (B.build_outline, dict(family="split", names=("A", "C", "B", "D"), givens=(3, 4), goal=5)),
    "PS 11": (B.build_outline, dict(family="kite", names=tuple("ABCD"), givens=(0, 1), goal=0)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    k = TYPE_OF[sid]
    fam = params["family"]
    assert any(b is build for _, b in B.TEMPLATES[k]), sid
    assert (k, fam) in B.COMBOS and (params["givens"], params.get("goal")) in B.COMBOS[k, fam], sid
assert sorted(set(TYPE_OF.values())) == B.KEYS
# out of range
assert not B.in_range(B.build_outline, dict(REACH["ex 9.1"][1], names=("A", "B", "C", "E")))   # not a run
assert not B.in_range(B.build_outline, dict(REACH["ex 9.1"][1], givens=(0, 2, 3)))            # a given not needed
assert not B.in_range(B.build_outline, dict(REACH["ex 9.1"][1], givens=(0, 4)))               # SSA: nothing proves it
assert not B.in_range(B.build_name, dict(REACH["PS 9b"][1], givens=(0, 3, 4)))                # SAS and SSS both

# ---- wrong answers fail
WRONG = [
    ("ex 9.1", "triangle A D C = triangle D B C, SAS; A C = B C, CPCTC"),     # vertices out of order
    ("ex 9.1", "triangle D A C = triangle D B C, SSS; A C = B C, CPCTC"),     # AC = BC is what's to show
    ("ex 9.1", "triangle D A C = triangle D B C, HL; A C = B C, CPCTC"),      # no hypotenuses known
    ("ex 9.1", "triangle D A C = triangle D B C, SAS"),                       # the part never stated
    ("ex 9.1", "triangle D A C = triangle D B C, SAS; A D = B D, CPCTC"),     # a given, not the goal
    ("ex 9.2", "triangle E D F = triangle H D G, AAAS; D F = D G, CPCTC"),   # one pair of angles
    ("ex 9.2", "triangle E D G = triangle H D F, SAS; D G = D F, CPCTC"),     # EG = HF isn't known
    ("ex 9.3", "triangle A B G = triangle E D F, SSS; B G = D F, CPCTC"),
    ("PS 9a", "SAS"), ("PS 9b", "AAAS"), ("PS 9c", "SAS"), ("PS 9d", "SAS"), ("PS 9d", "SSS"),
    ("PS 10", "triangle A B D = triangle C B D, SAS; A D = C D, CPCTC"),     # Type 2 shows the triangles only
    ("PS 10", "triangle A B D = triangle C B D, SSS"),
    ("PS 10", "triangle B A D = triangle C B D, SAS"),
    ("PS 11", "triangle A B C = triangle A D C, SAS; angle A B C = angle A D C, CPCTC"),
    ("PS 11", "triangle A B C = triangle C D A, SSS; angle A B C = angle A D C, CPCTC"),
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got == "failed", (sid, answer, got)
# a goal the givens already give: no outline
for bad in ("split A B C D; A D = B D, D C perp A B; show A D = B D",
            "split A B C D; A C = B C; show angle A = angle B",          # base angles: step 1, not a proof
            "split A B C D; A D = B D, angle A C D = angle B C D; show A C = B C"):   # SSA
    try:
        B.answer_of(bad); raise AssertionError(bad)
    except ValueError:
        pass
# a type that doesn't match: Type 3's check refuses an outline that needs step 1
assert B.check(dict(src["ex 9.2"], type="3")) == "failed"

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^postulate (pair|split|kite) [A-Z]( [A-Z])+; .+; triangle [A-Z] [A-Z] [A-Z] = triangle [A-Z] [A-Z] [A-Z]$",
    "2": r"^(split|kite) [A-Z]( [A-Z])+; .+; show triangle [A-Z] [A-Z] [A-Z] = triangle [A-Z] [A-Z] [A-Z]$",
    "3": r"^(split|kite) [A-Z]( [A-Z])+; .+; show (angle )?[A-Z]( [A-Z])* = (angle )?[A-Z]( [A-Z])*$",
    "4": r"^(cevians|mids|split) [A-Z]( [A-Z])+; .+; show (angle )?[A-Z]( [A-Z])* = (angle )?[A-Z]( [A-Z])*$",
}
KEY = r"triangle [A-Z] [A-Z] [A-Z] = triangle [A-Z] [A-Z] [A-Z], (SSS|SAS|AAAS|HL)"
ANSWER = {"1": r"^(SSS|SAS|AAAS|HL)$", "2": rf"^{KEY}$", "3": rf"^{KEY}; .+, CPCTC$", "4": rf"^{KEY}; .+, CPCTC$"}
rng = random.Random(9)
answers, families = {k: set() for k in B.KEYS}, {k: set() for k in B.KEYS}
for k in B.KEYS:
    seen = set()
    for i in range(300):
        if i % 50 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(SHAPE[k], p["prompt"]), p
        assert re.search(ANSWER[k], p["answer"]), p
        assert B.answer_of(p["prompt"]) == p["answer"], p
        assert B.kind_of(p["prompt"]) == k, p
        assert "cetz.canvas" in B.typst(p) and "cetz.canvas" in B.key_typst(p), p
        lines = B.answer_text(p).splitlines()
        if k == "3":
            assert lines[0] == "1. Mark the figure.", p                # no step-1 fact needed
        if k == "4":
            assert lines[0] != "1. Mark the figure.", p                # a step-1 fact, with its reason
            assert any(r in lines[0] for r in B.REASONS.values()), p
        answers[k].add(p["answer"].split(", ")[-1] if k != "1" else p["answer"])
        families[k].add(B.read(p["prompt"])[1].family)
        if i < 40:
            B.answer_typst(p), B.slide_typst(p), B.slide_typst(p, key=True)
assert answers["1"] == set(B.POSTULATES), answers["1"]
assert families == {"1": {"pair", "split", "kite"}, "2": {"split", "kite"}, "3": {"split", "kite"},
                    "4": {"cevians", "mids", "split"}}, families

# ---- showing
p = src["ex 9.1"]
assert B.statement(p) == ("Given: $overline(A D) tilde.equiv overline(B D)$ and $overline(D C) perp overline(A B)$. "
                          "Outline a proof that shows $overline(A C) tilde.equiv overline(B C)$.")
assert B.text(p) == "Given: AD ≅ BD and DC ⊥ AB. Outline a proof that shows AC ≅ BC.   [figure]", B.text(p)
assert B.text(src["ex 9.3"]).startswith("Given: AG ≅ EF, CA ≅ CE, B is the midpoint of CA, and D is the midpoint of CE.")
assert B.statement(src["PS 9b"]) == "Name the postulate that proves $Delta W X Z tilde.equiv Delta Y X Z$: SSS, SAS, AAAS, or HL."
assert B.answer_typst(src["PS 9b"]) == "#emph[SAS]"
a = B.answer_typst(src["ex 9.2"])
assert a.startswith("#grid(columns: 3") and "[$overline(D E) tilde.equiv overline(D H)$]" in a \
    and "[#emph[sides opposite congruent angles]]" in a and "[$Delta E D F tilde.equiv Delta H D G$], [#emph[SAS]]" in a, a
# the plain figure has no marks; the key's has the step-1 marks: ticks, arcs, a circle on the shared side
plain, marked = B.figure(src["ex 9.1"]), B.figure(src["ex 9.1"], key=True)
assert "circle(" not in plain and "circle(" in marked
ticks, arcs, boxes, circles = B.mark_list(*(lambda k, F_, g, goal: (F_, B.Closure(F_, g), g))(*B.read(prompt_of["ex 9.1"])),
                                          B.key_parts(*B.read(prompt_of["ex 9.1"])[1:], src["ex 9.1"]["answer"])[3])
assert ticks == [("A", "D", 1), ("B", "D", 1)] and circles == [("C", "D")] and len(boxes) == 2 and not arcs, \
    (ticks, arcs, boxes, circles)
assert "#hide[" in B.slide_typst(src["PS 11"]) and "#text(fill: red)[" in B.slide_typst(src["PS 11"], key=True)

# ---- editing: the data solved again
p, status = B.from_edit("split A B C D; A C = B C, A D = B D; show angle A C D = angle B C D", src["ex 9.1"])
assert status == "checked" and p["answer"] == "triangle A C D = triangle B C D, SSS; angle A C D = angle B C D, CPCTC", p
p, status = B.from_edit("cevians E H D F G; D E = D H, E F = H G; show D F = D G", src["ex 9.2"])
assert status == "checked" and p["answer"] == "triangle E D F = triangle H D G, SAS; D F = D G, CPCTC", p
assert B.answer_text(p).startswith("1. ∠E ≅ ∠H   base angles of an isosceles triangle"), B.answer_text(p)
p, status = B.from_edit("postulate kite A B C D; B C = D C, A B = A D; triangle A B C = triangle A D C", src["PS 9c"])
assert status == "checked" and p["answer"] == "SSS"
for bad, sid in (("split A B C D; A D = B D; show A C = B C", "ex 9.1"),            # not enough
                 ("split A B C D; A D = B D, D C perp A B; show A C = B C", "ex 9.2"),  # a Type 3 for a Type 4
                 ("kite A B C D; A C perp B D; show A B = A D", "PS 11"),           # BD isn't drawn
                 ("postulate kite A B C D; A B = A D; triangle A B C = triangle A D C", "PS 9c"),
                 ("Show that AC = BC", "ex 9.1")):
    try:
        B.from_edit(bad, src[sid]); raise AssertionError(bad)
    except ValueError:
        pass
p, status = B.with_answer(src["PS 9a"], "AAAS")
assert status == "checked"
p, status = B.with_answer(src["PS 9a"], "SAS")
assert status == "failed"

print("adv_lesson_9: ok")
