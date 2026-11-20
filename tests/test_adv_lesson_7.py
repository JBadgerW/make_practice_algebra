"""Lesson 7 (Advanced Math): logic, the contrapositive. Every source is
reachable from in-range parameters and checks; wrong answers fail; every type
draws, checks, and keeps its shape; edits are read back and solved again.

    python3 tests/test_adv_lesson_7.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_7 as B

lib = library.current()
assert "adv_lesson_7" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 7: Inductive and Deductive Reasoning, Logic, The Contrapositive, Converse and Inverse"
assert B.type_instructions("2") == "Write each statement as an if-then statement."
assert B.type_instructions("3") == "Write the contrapositive of each statement."
assert B.type_instructions("5") == "Write the converse and the inverse of each statement."
assert B.type_instructions("4").startswith("Write the contrapositive of the major premise")

# ---- every source, and its key (Types 1 and 4 in the deck's problem 5 and 6 wording)
SOURCES = [   # (id, type, prompt, key)
    ("ex 7.1", "1", "All normal dogs have four legs. / That dog has four legs. / Therefore, that dog is a normal dog.",
     "Invalid. The major premise is about the set of normal dogs. The minor premise says that dog is a member of "
     "the set of four-legged animals, not a member of the set of normal dogs."),
    ("ex 7.2", "1", "All boys are good. / That child is a good child. / Therefore, that child is a boy.",
     "Invalid. The major premise is about the set of boys. The minor premise says that child is a member of the "
     "set of good children, not a member of the set of boys."),
    ("ex 7.3", "1", "All chickens have three legs. / Henny Penny is a chicken. / Therefore, Henny Penny has three legs.",
     "Valid. The major premise is about the set of chickens, and the minor premise says Henny Penny is a member of "
     "that set."),
    ("PS 5", "1", "All students study at home. / Lori is studying at home. / Therefore, Lori is a student.",
     "Invalid. The major premise is about the set of students. The minor premise says Lori is a member of the set "
     "of people who study at home, not a member of the set of students."),                 # the deck's words
    ("PS 1", "2", "Elephants are large animals.", "If an animal is an elephant, then it is a large animal."),
    ("PS 2", "2", "Advanced math students are intelligent.",
     "If a student is an advanced math student, then the student is intelligent."),
    ("PS 3", "3", "If an animal is green, then it is not a seal.", "If an animal is a seal, then it is not green."),
    ("PS 4", "3", "If the team won, then the coach is happy.", "If the coach is not happy, then the team did not win."),
    ("ex 7.4", "4", "All nonathletes are vegetarians. / Jim is a nonvegetarian. / Therefore, Jim is an athlete.",
     "Contrapositive of the major premise: If a person is a nonvegetarian, then the person is an athlete. The minor "
     "premise says Jim is a nonvegetarian, so Jim is an athlete. The argument is valid."),
    ("PS 6", "4", "If the car is not moving, then the motor is off. / The motor is on. / Therefore, the car is moving.",
     "Contrapositive of the major premise: If the motor is on, then the car is moving. The minor premise says the "
     "motor is on, so the car is moving. The argument is valid."),                          # the deck's words
]
prompt_of = {s[0]: s[2] for s in SOURCES}
src = {s[0]: dict(type=s[1], prompt=s[2], answer=s[3]) for s in SOURCES}
for sid, typ, prompt, key in SOURCES:
    assert B.answer_of(typ, prompt) == key, (sid, B.answer_of(typ, prompt))
    assert B.check(src[sid]) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 7.1": (B.t1, dict(S="dog", Q="legs4", ind="That dog", shape="property")),
    "ex 7.2": (B.t1, dict(S="boy", Q="good", ind="That child", shape="property")),
    "ex 7.3": (B.t1, dict(S="chicken", Q="legs3", ind="Henny Penny", shape="member")),
    "PS 5": (B.t1, dict(S="student", Q="home", ind="Lori", shape="property")),
    "PS 1": (B.t2, dict(S="elephant", Spol=True, Q="large", Qpol=True)),
    "PS 2": (B.t2, dict(S="advanced", Spol=True, Q="intelligent", Qpol=True)),
    "PS 3": (B.t3_dom, dict(P="green", Ppol=True, Q="seal", Qpol=False)),
    "PS 4": (B.t3_prop, dict(pair=0)),
    "ex 7.4": (B.t4_cat, dict(S="athlete", Spol=False, Q="vegetarian", ind="Jim", shape="then")),
    "PS 6": (B.t4_prop, dict(pair=1, shape="then")),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid  # the type's own template
assert sorted(set(TYPE_OF.values())) == ["1", "2", "3", "4"]            # Type 5 has no source (7.D, added)
assert B.KEYS == ["1", "2", "3", "4", "5"]
# out of range
assert not B.in_range(B.t1, dict(REACH["ex 7.3"][1], ind="Lori"))       # Lori is no chicken
assert not B.in_range(B.t1, dict(REACH["ex 7.3"][1], Q="student"))      # another domain, and a kind
assert not B.in_range(B.t2, dict(REACH["PS 1"][1], Spol=False))         # no "nonelephants"
assert not B.in_range(B.t3_dom, dict(REACH["PS 3"][1], P="frog"))       # two kinds
assert not B.in_range(B.t4_cat, dict(REACH["ex 7.4"][1], shape="member"))
assert not B.in_range(B.t3_prop, dict(pair=len(B.PAIRS)))

# ---- the vocabulary: no phrase means two things; no individual repeats its kind's noun
for k in B.kinds():
    word = B.PRED[k]["forms"][True]["sg"].split(" ", 2)[2]
    assert all(i.split()[-1] != word for i in B.PRED[k]["inds"]), k

assert B.form(("honor", True), "sg") == "is an honor student"

# ---- validity by truth table
A, Q = ("a", True), ("q", True)
assert B.valid(A, Q, A, Q) and B.valid(A, Q, B.neg(Q), B.neg(A))       # affirm the if-part, deny the then-part
assert not B.valid(A, Q, Q, A) and not B.valid(A, Q, B.neg(A), B.neg(Q))

# ---- wrong answers fail
WRONG = [
    ("ex 7.1", "Valid. The major premise is about the set of normal dogs, and the minor premise says that dog is a "
               "member of that set."),                                  # the converse assumed
    ("ex 7.3", "Invalid."),                                             # a false premise, a valid argument
    ("ex 7.2", "Invalid. The major premise is about the set of good children. The minor premise says that child is "
               "a member of the set of boys, not a member of the set of good children."),   # sets swapped
    ("PS 5", "Invalid. The major premise is about the set of students. The minor premise says Lori is a member of "
             "the set of people who study at home, not a member of the set of people."),
    ("PS 1", "If an animal is a large animal, then it is an elephant."),  # the converse
    ("PS 1", "If an animal is an elephant, then the animal is a large animal."),   # the deck says it
    ("PS 2", "If a student is an advanced math student, then it is intelligent."),
    ("PS 2", "If a person is an advanced math student, then the person is intelligent."),
    ("PS 3", "If an animal is not a seal, then it is not green."),      # the inverse
    ("PS 3", "If an animal is not green, then it is a seal."),          # P and Q negated, not swapped
    ("PS 3", "If an animal is not not a seal, then it is not green."),
    ("PS 4", "If the coach is happy, then the team won."),              # the converse
    ("PS 4", "If the team did not win, then the coach is not happy."),  # the inverse
    ("ex 7.4", "Contrapositive of the major premise: If a person is a vegetarian, then the person is a nonathlete. "
               "The minor premise says Jim is a nonvegetarian, so Jim is an athlete. The argument is valid."),
    ("ex 7.4", "Contrapositive of the major premise: If a person is a nonvegetarian, then the person is an athlete. "
               "The minor premise says Jim is a nonvegetarian, so Jim is an athlete. The argument is invalid."),
    ("PS 6", "Contrapositive of the major premise: If the motor is off, then the car is not moving. The minor "
             "premise says the motor is on, so the car is moving. The argument is valid."),   # the premise again
    ("PS 6", "Contrapositive of the major premise: If the motor is on, then the car is moving. The minor premise "
             "says the car is moving, so the car is moving. The argument is valid."),
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got == "failed", (sid, answer, got)
# ---- Type 5: the converse and the inverse, from PS 3 and PS 4's statements
T5 = {
    "PS 4": "Converse: If the coach is happy, then the team won. Inverse: If the team did not win, then the coach "
            "is not happy.",
    "PS 3": "Converse: If an animal is not a seal, then it is green. Inverse: If an animal is not green, then it is "
            "a seal.",
}
for sid, key in T5.items():
    p5 = dict(type="5", prompt=prompt_of[sid], answer=key)
    assert B.answer_of("5", p5["prompt"]) == key, B.answer_of("5", p5["prompt"])
    assert B.check(p5) == "checked", sid
for answer in [
    "Converse: If the team did not win, then the coach is not happy. Inverse: If the coach is happy, then the team won.",
    "Converse: If the coach is not happy, then the team did not win. Inverse: If the team did not win, then the "
    "coach is not happy.",                                              # the contrapositive for the converse
    "Converse: If the coach is happy, then the team won. Inverse: If the coach is not happy, then the team did not win.",
    "Converse: If the coach is happy, then the team won.",              # no inverse
]:
    assert B.check(dict(type="5", prompt=prompt_of["PS 4"], answer=answer)) == "failed", answer
assert B.check(dict(type="5", prompt=prompt_of["PS 3"], answer=T5["PS 3"].replace("then it is green",
                                                                                "then the animal is green"))) == "failed"   # "it", as Types 2-3
assert B.check(dict(type="5", prompt=prompt_of["PS 3"], answer=T5["PS 3"].replace("If an animal is not a seal",
                                                                                "If a person is not a seal"))) == "failed"
p5 = dict(type="5", prompt=prompt_of["PS 4"], answer=T5["PS 4"])
assert B.answer_typst(p5) == ("#block(width: 96%)[#align(left)[Converse: _If the coach is happy, then the team won._ \\\n"
                              "Inverse: _If the team did not win, then the coach is not happy._]]"), B.answer_typst(p5)
assert B.answer_text(p5).splitlines()[1] == "Inverse: If the team did not win, then the coach is not happy."
assert B.typst(p5) == ("Write the converse and the inverse of the statement: #h(0.5em) "
                       "If the team won, then the coach is happy.")

# a verdict alone is enough; a reason in other words can't be read
assert B.check(dict(src["PS 5"], answer="Invalid.")) == "checked"
assert B.check(dict(src["PS 5"], answer="Invalid. Lori might be a teacher.")) == "unchecked"

# ---- the invalid Type 4 shape: the minor premise denies the if-part
p = dict(type="4", prompt=B.t4_prop(pair=1, shape="if"))
assert p["prompt"] == "If the car is not moving, then the motor is off. / The car is moving. / Therefore, the motor is on."
p["answer"] = B.answer_of("4", p["prompt"])
assert p["answer"] == ("Contrapositive of the major premise: If the motor is on, then the car is moving. The minor "
                       "premise says the car is moving, but neither the premise nor its contrapositive starts with "
                       "that, so the conclusion does not follow. The argument is invalid."), p["answer"]
assert B.check(p) == "checked"
assert B.check(dict(p, answer=p["answer"].replace("invalid.", "valid."))) == "failed"

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^All [a-z ]+ [a-z ]+\. / [A-Z][\w ]+ (is|has|can|takes|likes|eats|gets|pays|stays|practices|rides) "
         r"[\w -]+\. / Therefore, [\w ]+\.$",
    "2": r"^[A-Z][a-z ]+ (are|have|can|cannot|do|eat|take|study|practice|get|pay|stay|like|ride)\b[\w -]*\.$",
    "3": r"^If .+, then .+\.$",
    "5": r"^If .+, then .+\.$",
    "4": r"^(All non[a-z ]+|All [a-z ]+|If .+, then .+\.) .*/ .+ / Therefore, .+\.$",
}
ANSWER = {
    "1": r"^(Valid\. The major premise is about the set of .+, and the minor premise says .+ is a member of that set\."
         r"|Invalid\. The major premise is about the set of (.+)\. The minor premise says .+ is a member of the set "
         r"of .+, not a member of the set of \2\.)$",
    "2": r"^If (an animal|a figure) .+, then it .+\.$|^If a (person|student|child) .+, then the \2 .+\.$",
    "3": r"^If .+, then .+\.$",
    "5": r"^Converse: If .+?, then .+?\. Inverse: If .+?, then .+?\.$",
    "4": r"^Contrapositive of the major premise: If .+?, then .+?\. The minor premise says .+ The argument is "
         r"(valid|invalid)\.$",
}
rng = random.Random(7)
shapes = {k: set() for k in B.KEYS}
for k in B.KEYS:
    seen = set()
    for i in range(300):
        if i % 50 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(SHAPE[k], p["prompt"]), p
        assert re.search(ANSWER[k], p["answer"]), p
        assert B.answer_of(k, p["prompt"]) == p["answer"], p
        assert not re.search(r"\bnot not\b|\bnon ?non|\bnot (a|an) non", p["prompt"] + p["answer"]), p
        assert not re.search(r"\b(he|she|his|her|him|they|their)\b", p["prompt"] + p["answer"], re.I), p
        if k == "1":
            shapes[k].add(p["answer"].split(".")[0])
            dom, a, b, ind, m, c = B.read_syllogism(p["prompt"])
            assert m in (a, b) and c in (a, b) and m != c, p        # Type 1 affirms; it never denies
        if k == "4":
            shapes[k].add(p["answer"].rsplit(" ", 1)[1] + (" if" if p["prompt"].startswith("If") else " all"))
            dom, a, b, ind, m, c = B.read_syllogism(p["prompt"])
            assert m in (B.neg(a), B.neg(b)), p                     # Type 4 denies
        if k == "5":
            shapes[k].add(p["prompt"].split()[1] in ("a", "an"))
        if k in ("3", "5"):
            dom, a, b = B.read_if_then(p["prompt"])
            assert dom is None or not ("kind" in B.PRED[b[0]]["roles"] and "prop" not in B.PRED[b[0]]["roles"]
                                       and "kind" in B.PRED[a[0]]["roles"]), p    # never kind -> kind
        if k == "3":
            shapes[k].add(p["prompt"].split()[1] in ("a", "an"))
assert shapes["1"] == {"Valid", "Invalid"}, shapes
assert shapes["4"] == {"valid. if", "valid. all", "invalid. if", "invalid. all"}, shapes
assert shapes["3"] == shapes["5"] == {True, False}, shapes

# ---- showing: the syllogism's minor premise underlined, the verdict in bold
t = B.typst(src["PS 5"])
assert t.startswith("Is the following argument a valid argument? Why or why not?") and "#underline" in t, t
assert "#underline(offset: 3pt)[Lori is studying at home.]" in t, t
assert B.answer_typst(src["PS 5"]).startswith("#block(width: 96%)[#align(left)[*Invalid.*")
assert B.answer_typst(src["PS 6"]).endswith("*The argument is valid.*]]")
assert B.answer_typst(dict(src["PS 5"], answer="Invalid.")) == "*Invalid.*"
assert "_If the motor is on, then the car is moving._" in B.answer_typst(src["PS 6"])
assert B.typst(src["PS 1"]) == "Write as an if-then statement: #h(0.5em) Elephants are large animals."
assert B.answer_typst(src["PS 4"]) == "_If the coach is not happy, then the team did not win._"
assert B.text(src["PS 3"]) == "Write the contrapositive of the statement: If an animal is green, then it is not a seal."
assert B.text(src["ex 7.3"]).splitlines()[2].strip() == "Henny Penny is a chicken."

# ---- editing: the words are read back and solved again
for bad in ("If the team lost, then the coach is not happy.",   # "lost" doesn't negate by rule
            "The team lost the game"):
    try:
        B.from_edit(bad, src["PS 4"]); raise AssertionError("unreadable")
    except ValueError as e:
        assert "If the team won, then the coach is happy." in str(e), e
p, status = B.from_edit("If the bus is late, then the class has a quiz.", src["PS 4"])
assert status == "checked" and p["answer"] == "If the class does not have a quiz, then the bus is not late.", p
p, status = B.from_edit("If a number is even, then it is divisible by 2.", src["PS 3"])
assert status == "checked" and p["answer"] == "If a number is not divisible by 2, then it is not even.", p
p, status = B.from_edit("All horses eat grass. / Dobbin eats grass. / Therefore, Dobbin is a horse.", src["ex 7.1"])
assert status == "checked" and p["answer"].startswith("Invalid. The major premise is about the set of horses."), p
p, status = B.from_edit("Spiders are green.", src["PS 1"])
assert status == "checked" and p["answer"] == "If an animal is a spider, then it is green.", p
try:
    B.from_edit("All chickens have three legs. Henny Penny is a chicken.", src["ex 7.3"]); raise AssertionError
except ValueError:
    pass
p, status = B.with_answer(src["PS 4"], "If the coach is not happy, then the team did not win.")
assert status == "checked", p
p, status = B.with_answer(src["PS 4"], "If the coach is happy, then the team won.")
assert status == "failed", p

print("adv_lesson_7: ok")
