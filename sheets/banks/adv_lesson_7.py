"""Lesson 7 (Advanced Math): inductive and deductive reasoning, logic, the
contrapositive, converse and inverse. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_007/slides/deck_007.typ): examples
7.1-7.4 and Problem Set 7, problems 1-6.

    1  is the syllogism valid?          All boys are good. / That child is a good child. /
                                        Therefore, that child is a boy.
                                            Invalid. The major premise is about the set of boys. ...
    2  write as an if-then statement:   Elephants are large animals.
                                            If an animal is an elephant, then it is a large animal.
    3  write the contrapositive:        If the team won, then the coach is happy.
                                            If the coach is not happy, then the team did not win.
    4  the contrapositive tests it:     If the car is not moving, then the motor is off. /
                                        The motor is on. / Therefore, the car is moving.
                                            Contrapositive of the major premise: If the motor is on,
                                            then the car is moving. ... The argument is valid.
    5  the converse and the inverse:    If the team won, then the coach is happy.
                                            Converse: If the coach is happy, then the team won.
                                            Inverse: If the team did not win, then the coach is not happy.

The types file's order is 1, 4, 2, 3; the bank follows the lesson's order
instead, since Type 4 (example 7.4) uses the if-then form and the
contrapositive that Types 2 and 3 practice. Type 5 (7.D) has no example or
problem in the book; it was added at the teacher's request, from Type 3's
statements.

Type 1's minor premise affirms something: the member (valid, 7.3) or the
property (invalid, 7.1, 7.2, problem 5). Type 4's minor premise denies
something: the then-part (valid, 7.4, problem 6) or the if-part (invalid, the
lesson's "It did not rain" argument, which has no example of its own).

Problems are words, made from a vocabulary: predicates in a domain (animals,
people, students, children, figures), each with its "not" form ("is a
nonathlete", "is not a seal", "does not have four legs") and the set it names
("four-legged animals"), and propositions with their negations ("the motor is
on" / "the motor is off"). A statement pairs a kind (elephant, student) with a
property (large animal, studies at home) in the same domain, so most are
sensible and some are as false as the book's three-legged chickens: the
lesson's point is that validity doesn't depend on truth. Propositions are
paired only as listed (PAIRS).

The key writes what the deck writes:
  1  Valid./Invalid., then why, in the deck's problem 5 wording:
     "Invalid. The major premise is about the set of students. The minor
     premise says Lori is a member of the set of people who study at home, not
     a member of the set of students." A valid one: "Valid. The major premise
     is about the set of chickens, and the minor premise says Henny Penny is a
     member of that set." (The deck's 7.1-7.3 explanations say the same in
     their own words.)
  2  "If an animal is an elephant, then it is a large animal." An animal or a
     figure is "it"; a person is "the person", "the student", "the child"
     (problem 2: "If a student is an advanced math student, then the student is
     intelligent.").
  3  The negated then-part, then the negated if-part, double negatives
     removed: "If an animal is a seal, then it is not green." (problem 3).
  4  "Contrapositive of the major premise: <if-then>. The minor premise says
     the motor is on, so the car is moving. The argument is valid." (problem
     6). An invalid one: "... The minor premise says the car is moving, but
     neither the premise nor its contrapositive starts with that, so the
     conclusion does not follow. The argument is invalid."
  5  "Converse: If the coach is happy, then the team won. Inverse: If the team
     did not win, then the coach is not happy." Q -> P, then not P -> not Q,
     in the lesson's order; the same subject and referent as Type 2.

check() reads the words back into literals (a predicate or proposition and
whether it is negated), independently of how they were built:
  1, 4  validity by truth table: no assignment makes the major premise
        (P -> Q) and the minor premise true and the conclusion false. The
        verdict must agree. The reason must name the right sets and member
        (Type 1), or the contrapositive must be exactly not-Q -> not-P and the
        minor premise and conclusion restated (Type 4). A reason in other
        words is "unchecked"; the verdict alone is "checked".
  2     the answer's if-part and then-part are the statement's subject and
        predicate, in the domain's words.
  3     the answer's if-part is the negated then-part and its then-part the
        negated if-part.
  5     the converse's parts are the statement's, swapped; the inverse's are
        the statement's, each negated, in order.
An edited statement may use phrases outside the vocabulary when they negate
by rule (is/are/was/were/can/will/has/have + not).

No skipped sources: Lesson 7 has no proofs.

A problem: dict(type, prompt, answer, source); prompt and answer are words,
a syllogism's three lines separated by " / ".
    prompt  "All students study at home. / Lori is studying at home. / Therefore, Lori is a student."
    answer  "Invalid. The major premise is about the set of students. ..."
"""
import itertools, re
from .. import gen
from ..gen import need
from ..typst import esc

NAME = FAMILY = "adv_lesson_7"
FIXED = False
TITLE = "Lesson 7: Inductive and Deductive Reasoning, Logic, The Contrapositive, Converse and Inverse"
INSTRUCTIONS = "Answer each question."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="Is the Syllogism Valid?",
         look="A major premise about all members of a set, a minor premise about one individual, and a "
              "conclusion.",
         move="The major premise gives a property of every member of a set. The argument is valid only when the "
              "minor premise names a member of that set. If it names a member of the property's set instead, "
              "the argument is invalid: the premise is one way. Validity is about the argument, not about "
              "whether the premises are true.",
         instructions="Is each argument valid or invalid? Tell why.", space="1.25in", width="full"),
    dict(key="2", title="Writing an If-Then Statement",
         look="A statement about a kind of thing, like Elephants are large animals.",
         move="The subject goes in the if-part and the predicate in the then-part: If an animal is an elephant, "
              "then it is a large animal. That is $P -> Q$.",
         instructions="Write each statement as an if-then statement.", space="0.6in", width="full"),
    dict(key="3", title="Writing the Contrapositive",
         look="An if-then statement, $P -> Q$.",
         move="Replace the if-part with the negative of the then-part, and the then-part with the negative of "
              "the if-part: if not $Q$, then not $P$. Two negatives cancel: not not a seal is a seal.",
         instructions="Write the contrapositive of each statement.", space="0.6in", width="full"),
    dict(key="4", title="Using the Contrapositive to Test Validity",
         look="A syllogism whose minor premise says something is not so.",
         move="Write the major premise in if-then form, then write its contrapositive: if not $Q$, then not $P$. "
              "It has the same truth as the premise. If the minor premise matches the contrapositive's if-part, "
              "the argument is valid. If it matches neither if-part, the conclusion does not follow.",
         instructions="Write the contrapositive of the major premise of each syllogism to help determine whether "
                      "the argument is valid or invalid.", space="1.4in", width="full"),
    dict(key="5", title="Writing the Converse and the Inverse",
         look="An if-then statement, $P -> Q$, and a request for its converse and inverse.",
         move="The converse goes the other way: $Q -> P$. The inverse negates both parts in place: if not $P$, "
              "then not $Q$. Neither has to be true when the statement is; the contrapositive is the one that "
              "does.",
         instructions="Write the converse and the inverse of each statement.", space="0.8in", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in", width="full", kind="words")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The vocabulary
# ------------------------------------------------------------------
# domain: (indefinite, referent, plural)
DOMAINS = {
    "animal": ("an animal", "it", "animals"),
    "figure": ("a figure", "it", "figures"),
    "person": ("a person", "the person", "people"),
    "student": ("a student", "the student", "students"),
    "child": ("a child", "the child", "children"),
}
PEOPLE = ("Lori", "Jim") + gen.NAMES
CHILDREN = ("That child", "This child", "The youngest child")
FIGURES = ("That figure", "This figure")
# An individual never repeats its kind's noun ("That bird is a bird"); 7.1's "That dog" names a normal dog.

PRED = {}           # id -> dict(id, dom, roles, forms={True: {...}, False: {...}}, inds)

def art(word):
    return "an" if word[0] in "aeiou" or word.startswith("honor") else "a"

def _add(id_, dom, roles, pos, neg, inds=()):
    assert id_ not in PRED, id_
    PRED[id_] = dict(id=id_, dom=dom, roles=set(roles), forms={True: pos, False: neg}, inds=tuple(inds))

def noun(id_, dom, word, plural=None, roles=("kind",), non=False, inds=()):
    """A noun: is an elephant / are elephants; with non: is a nonathlete / are nonathletes."""
    plural = plural or word + "s"
    a = art(word)
    pos = dict(sg=f"is {a} {word}", pl=f"are {plural}", noun=plural, set=plural)
    if non:
        neg = dict(sg=f"is a non{word}", pl=f"are non{plural}", noun=f"non{plural}", set=f"non{plural}")
    else:
        neg = dict(sg=f"is not {a} {word}", pl=f"are not {plural}", noun=None, set=None)
    _add(id_, dom, roles, pos, neg, inds)

def adj(id_, dom, word, child=None):
    """An adjective: is green / are green (the set: green animals); with a noun for one
    member: is a good child / are good (the set: good children)."""
    dpl = DOMAINS[dom][2]
    one = f"{art(word)} {word} {child}" if child else word
    pos = dict(sg=f"is {one}", pl=f"are {word}", noun=f"{word} {dpl}", set=f"{word} {dpl}")
    neg = dict(sg=f"is not {one}", pl=f"are not {word}", noun=None, set=None)
    _add(id_, dom, ("prop",), pos, neg)

def verb(id_, dom, sg, pl, nsg, npl, set_):
    """A verb phrase: has four legs / have four legs / does not have four legs / ..."""
    _add(id_, dom, ("prop",), dict(sg=sg, pl=pl, noun=set_, set=set_), dict(sg=nsg, pl=npl, noun=None, set=None))

def has(id_, dom, what, set_):
    verb(id_, dom, f"has {what}", f"have {what}", f"does not have {what}", f"do not have {what}", set_)

def does(id_, dom, s, p, set_):
    """s: the singular verb phrase (gets up early), p: the plural (get up early)."""
    verb(id_, dom, s, p, f"does not {p}", f"do not {p}", set_)

def can(id_, dom, what, set_):
    verb(id_, dom, f"can {what}", f"can {what}", f"cannot {what}", f"cannot {what}", set_)

# animals (7.1, 7.3, problems 1 and 3; the lesson's rabbits and frogs)
noun("elephant", "animal", "elephant", inds=("Jumbo", "That animal"))
noun("rabbit", "animal", "rabbit", inds=("Flopsy", "That animal"))
noun("dog", "animal", "normal dog", inds=("That dog", "Rex"))
noun("chicken", "animal", "chicken", inds=("Henny Penny", "That hen"))
noun("frog", "animal", "frog", inds=("Henry", "That animal"))
noun("seal", "animal", "seal", inds=("Sammy", "That animal"))
noun("bird", "animal", "bird", inds=("Polly", "That animal"))
noun("fish", "animal", "fish", plural="fish", inds=("Goldie", "That animal"))
noun("cat", "animal", "cat", inds=("Mittens", "That pet"))
noun("spider", "animal", "spider", inds=("Charlotte", "That animal"))
noun("horse", "animal", "horse", inds=("Dobbin", "That animal"))
noun("whale", "animal", "whale", inds=("Humphrey", "That animal"))
noun("large", "animal", "large animal", roles=("prop",))
noun("runner", "animal", "fast runner", roles=("prop",))
noun("mammal", "animal", "mammal", roles=("prop",))
adj("green", "animal", "green")
has("legs4", "animal", "four legs", "four-legged animals")
has("legs3", "animal", "three legs", "three-legged animals")
has("feathers", "animal", "feathers", "animals with feathers")
can("fly", "animal", "fly", "animals that can fly")
can("swim", "animal", "swim", "animals that can swim")
does("grass", "animal", "eats grass", "eat grass", "animals that eat grass")

# figures
noun("square", "figure", "square", roles=("kind",), inds=FIGURES)
noun("rectangle", "figure", "rectangle", roles=("kind", "prop"), inds=FIGURES)
noun("rhombus", "figure", "rhombus", plural="rhombuses", inds=FIGURES)
noun("triangle", "figure", "triangle", inds=FIGURES)
noun("pentagon", "figure", "pentagon", inds=FIGURES)
noun("polygon", "figure", "polygon", roles=("prop",))
noun("parallelogram", "figure", "parallelogram", roles=("prop",))
adj("convex", "figure", "convex")
has("sides3", "figure", "three sides", "figures with three sides")
has("sides4", "figure", "four sides", "figures with four sides")
has("sides5", "figure", "five sides", "figures with five sides")
has("right", "figure", "four right angles", "figures with four right angles")

# people (7.4, problem 5)
noun("student", "person", "student", inds=PEOPLE)
noun("athlete", "person", "athlete", non=True, inds=PEOPLE)
noun("swimmer", "person", "swimmer", non=True, inds=PEOPLE)
noun("resident", "person", "resident", non=True, inds=PEOPLE)
noun("voter", "person", "voter", non=True, inds=PEOPLE)
noun("farmer", "person", "farmer", inds=PEOPLE)
noun("musician", "person", "musician", inds=PEOPLE)
noun("pilot", "person", "pilot", inds=PEOPLE)
noun("vegetarian", "person", "vegetarian", roles=("prop",), non=True)
does("home", "person", "studies at home", "study at home", "people who study at home")
# an individual "is studying at home" (problem 5); a statement about every person "studies at home"
PRED["home"]["forms"][True]["member"] = "is studying at home"
PRED["home"]["forms"][False]["member"] = "is not studying at home"
does("practice", "person", "practices every day", "practice every day", "people who practice every day")
does("early", "person", "gets up early", "get up early", "people who get up early")
does("fee", "person", "pays a fee", "pay a fee", "people who pay a fee")
does("shallow", "person", "stays in the shallow end", "stay in the shallow end", "people who stay in the shallow end")
can("plane", "person", "fly a plane", "people who can fly a plane")
adj("happy", "person", "happy")

# students (problem 2)
noun("advanced", "student", "advanced math student", inds=PEOPLE)
noun("honor", "student", "honor student", inds=PEOPLE)
noun("senior", "student", "senior", inds=PEOPLE)
noun("freshman", "student", "freshman", plural="freshmen", inds=PEOPLE)
adj("intelligent", "student", "intelligent")
adj("hardworking", "student", "hardworking")
has("locker", "student", "a locker", "students who have a locker")
does("chemistry", "student", "takes chemistry", "take chemistry", "students who take chemistry")
does("bus", "student", "rides the bus", "ride the bus", "students who ride the bus")

# children (7.2)
noun("boy", "child", "boy", inds=CHILDREN)
noun("girl", "child", "girl", inds=CHILDREN)
noun("toddler", "child", "toddler", inds=CHILDREN)
adj("good", "child", "good", child="child")
adj("polite", "child", "polite", child="child")
does("nap", "child", "takes a nap", "take a nap", "children who take a nap")
does("icecream", "child", "likes ice cream", "like ice cream", "children who like ice cream")

# propositions: id -> (true, false)
PROP = {
    "won": ("the team won", "the team did not win"),
    "happy_coach": ("the coach is happy", "the coach is not happy"),
    "moving": ("the car is moving", "the car is not moving"),
    "motor": ("the motor is on", "the motor is off"),
    "raining": ("it is raining", "it is not raining"),
    "canceled": ("the game is canceled", "the game is not canceled"),
    "light": ("the light is on", "the light is off"),
    "dark": ("the room is dark", "the room is not dark"),
    "barking": ("the dog is barking", "the dog is not barking"),
    "door": ("someone is at the door", "no one is at the door"),
    "store": ("the store is open", "the store is closed"),
    "lights": ("the lights are on", "the lights are off"),
    "boiling": ("the water is boiling", "the water is not boiling"),
    "pasta": ("the pasta is ready", "the pasta is not ready"),
    "bridge": ("the bridge is up", "the bridge is down"),
    "boats": ("the boats can pass", "the boats cannot pass"),
    "battery": ("the battery is dead", "the battery is not dead"),
    "phone": ("the phone is on", "the phone is off"),
    "wet": ("the field is wet", "the field is not wet"),
    "indoors": ("practice is held indoors", "practice is not held indoors"),
    "tied": ("the score is tied", "the score is not tied"),
    "overtime": ("the game goes to overtime", "the game does not go to overtime"),
    "scored": ("the team scored", "the team did not score"),
    "snow": ("it is snowing", "it is not snowing"),
    "school": ("school is closed", "school is open"),
    "plugged": ("the lamp is plugged in", "the lamp is not plugged in"),
    "lamp": ("the lamp can light", "the lamp cannot light"),
    "frozen": ("the pond is frozen", "the pond is not frozen"),
    "skating": ("the skaters are on the ice", "the skaters are not on the ice"),
    "sunny": ("the sun is shining", "the sun is not shining"),
    "pool": ("the pool is crowded", "the pool is not crowded"),
    "test": ("the test is today", "the test is not today"),
    "studying": ("the students are studying", "the students are not studying"),
}
# (if-part, then-part) as literals (id, truth)
PAIRS = [
    (("won", True), ("happy_coach", True)),           # problem 4
    (("moving", False), ("motor", False)),            # problem 6
    (("raining", True), ("canceled", True)),
    (("light", False), ("dark", True)),
    (("barking", True), ("door", True)),
    (("store", False), ("lights", False)),
    (("boiling", False), ("pasta", False)),
    (("bridge", True), ("boats", True)),
    (("battery", True), ("phone", False)),
    (("wet", True), ("indoors", True)),
    (("tied", True), ("overtime", True)),
    (("scored", False), ("won", False)),
    (("snow", True), ("school", True)),
    (("plugged", False), ("lamp", False)),
    (("frozen", True), ("skating", True)),
    (("sunny", True), ("pool", True)),
    (("test", True), ("studying", True)),
]

def pair_of(i, flip=False):
    """PAIRS[i], or with both parts negated (flip): If the team did not win, then the coach is not happy."""
    a, b = PAIRS[i]
    return (neg(a), neg(b)) if flip else (a, b)

# reading words back: phrase -> literal
def _index(field):
    out = {}
    for p in PRED.values():
        for pol, f in p["forms"].items():
            if f.get(field):
                assert f[field] not in out, f[field]
                out[f[field]] = (p["id"], pol)
    return out

SG, PL, NOUN, SET = _index("sg"), _index("pl"), _index("noun"), _index("set")
for _ph, _lit in _index("member").items():
    assert _ph not in SG
    SG[_ph] = _lit
CLAUSE = {}
for _id, _forms in PROP.items():
    for _pol, _t in zip((True, False), _forms):
        assert _t not in CLAUSE
        CLAUSE[_t] = (_id, _pol)
INDEF = {d[0]: k for k, d in DOMAINS.items()}

def neg(lit):
    return (lit[0], not lit[1])

def kinds(dom=None):
    return [p["id"] for p in PRED.values() if "kind" in p["roles"] and dom in (None, p["dom"])]

def props(dom):
    return [p["id"] for p in PRED.values() if "prop" in p["roles"] and p["dom"] == dom]

def dom_of(id_):
    return PRED[id_]["dom"]

def form(lit, field):
    return PRED[lit[0]]["forms"][lit[1]][field]

def member(lit):
    """What one individual is or does: Lori is studying at home."""
    f = PRED[lit[0]]["forms"][lit[1]]
    return f.get("member", f["sg"])

def cap(s):
    return s[0].upper() + s[1:]

def low(ind):
    """An individual inside a sentence: that dog, Henny Penny."""
    return ind[0].lower() + ind[1:] if ind.split()[0] in ("That", "This", "The") else ind

# ------------------------------------------------------------------
# Rule-based negation, for edited statements outside the vocabulary
# ------------------------------------------------------------------
AUX = r"is|are|was|were|will|can|could|should|would"

def generic(c):
    """A clause outside the vocabulary as a literal (("~", its positive words), truth)."""
    c = " ".join(c.split())
    m = re.fullmatch(rf"(.*?)\b({AUX}) not (.+)", c)
    if m:
        return ("~", f"{m.group(1)}{m.group(2)} {m.group(3)}"), False
    m = re.fullmatch(r"(.*?)\bcannot (.+)", c)
    if m:
        return ("~", f"{m.group(1)}can {m.group(2)}"), False
    m = re.fullmatch(r"(.*?)\b(does|do|did) not have (.+)", c)
    if m:
        return ("~", m.group(1) + {"does": "has", "do": "have", "did": "had"}[m.group(2)] + " " + m.group(3)), False
    if re.fullmatch(rf"(.*?)\b({AUX}|has|have|had) (.+)", c):
        return ("~", c), True
    raise ValueError(f"I can't tell what negates: {c}")

def generic_words(lit):
    (_, c), pol = lit
    if pol:
        return c
    m = re.fullmatch(rf"(.*?)\b({AUX}) (.+)", c)
    if m and m.group(2) == "can":
        return f"{m.group(1)}cannot {m.group(3)}"
    if m:
        return f"{m.group(1)}{m.group(2)} not {m.group(3)}"
    m = re.fullmatch(r"(.*?)\b(has|have|had) (.+)", c)
    return m.group(1) + {"has": "does", "have": "do", "had": "did"}[m.group(2)] + " not have " + m.group(3)

def say_sg(lit):
    return generic_words(lit) if lit[0][0] == "~" else form(lit, "sg")

def say_clause(lit):
    return generic_words(lit) if lit[0][0] == "~" else PROP[lit[0]][0 if lit[1] else 1]

def read_sg(dom, s):
    if s in SG:
        lit = SG[s]
        if dom_of(lit[0]) != dom:
            raise ValueError(f"{s} is not about {dom}s")
        return lit
    return generic(s)

def read_clause(s):
    return CLAUSE[s] if s in CLAUSE else generic(s)

# ------------------------------------------------------------------
# Statements
# ------------------------------------------------------------------
def if_then(dom, a, b):
    """dom: a domain (subject and referent) or None (propositions)."""
    if dom is None:
        return f"If {say_clause(a)}, then {say_clause(b)}."
    indef, ref = (DOMAINS[dom][:2] if dom in DOMAINS else dom)
    return f"If {indef} {say_sg(a)}, then {ref} {say_sg(b)}."

def read_if_then(s):
    """(dom, A, B): dom is a domain key, (indef, ref) for one outside the vocabulary, or None."""
    m = re.fullmatch(r"If (.+?), then (.+)\.", " ".join(s.split()))
    if not m:
        raise ValueError("write it as If ..., then ....")
    x, y = m.groups()
    if x in CLAUSE or y in CLAUSE:
        return None, read_clause(x), read_clause(y)
    d = re.fullmatch(r"(an? \w+) (.+)", x)
    r = re.fullmatch(r"(it|the \w+) (.+)", y)
    if d and r:
        indef, rest = d.groups()
        ref, rest2 = r.groups()
        if indef in INDEF:
            dom = INDEF[indef]
            if ref not in ("it", "the " + indef.split()[1]):
                raise ValueError(f"after {indef}, write it or the {indef.split()[1]}")
            return dom, read_sg(dom, rest), read_sg(dom, rest2)
        return (indef, ref), generic(rest), generic(rest2)
    return None, read_clause(x), read_clause(y)

def categorical(a, b):
    return f"All {form(a, 'noun')} {form(b, 'pl')}."

def read_categorical(s):
    m = re.fullmatch(r"All (.+)\.", s)
    if not m:
        raise ValueError("a major premise starts with All")
    body = m.group(1)
    for n, a in NOUN.items():
        if body.startswith(n + " ") and body[len(n) + 1:] in PL:
            b = PL[body[len(n) + 1:]]
            if dom_of(a[0]) == dom_of(b[0]) and a[0] != b[0]:
                return dom_of(a[0]), a, b
    raise ValueError("use the bank's words: All chickens have three legs.")

def statement(a, b):
    """A bare statement (Type 2): Elephants are large animals."""
    return f"{cap(form(a, 'noun'))} {form(b, 'pl')}."

def read_statement(s):
    m = re.fullmatch(r"(.+)\.", " ".join(s.split()))
    if not m:
        raise ValueError("end the statement with a period")
    return read_categorical("All " + m.group(1)[0].lower() + m.group(1)[1:] + ".")

# ------------------------------------------------------------------
# Syllogisms: major / minor / conclusion
# ------------------------------------------------------------------
def syllogism(dom, a, b, ind, minor, concl):
    """dom None: an if-then of propositions; otherwise All ... about ind."""
    if dom is None:
        return " / ".join((if_then(None, a, b), cap(say_clause(minor)) + ".",
                           f"Therefore, {say_clause(concl)}."))
    return " / ".join((categorical(a, b), f"{ind} {member(minor)}.", f"Therefore, {low(ind)} {member(concl)}."))

def read_member(s):
    """(individual, literal) from 'Lori is studying at home.'"""
    for ph in sorted(SG, key=len, reverse=True):
        if s.endswith(" " + ph + "."):
            return s[:-len(ph) - 2], SG[ph]
    raise ValueError("use the bank's words: Henny Penny is a chicken.")

def read_syllogism(prompt):
    """(dom, A, B, ind, minor, concl): the major premise is A -> B."""
    lines = [" ".join(x.split()) for x in prompt.split("/")]
    if len(lines) != 3 or not lines[2].startswith("Therefore, "):
        raise ValueError("three lines, split by /, the last starting Therefore,")
    major, minor, concl = lines[0], lines[1], lines[2][len("Therefore, "):]
    if major.startswith("All "):
        dom, a, b = read_categorical(major)
        ind, m = read_member(minor)
        ind2, c = read_member(cap(concl))
        if low(ind) != low(ind2):
            raise ValueError("the minor premise and the conclusion name different individuals")
        if any(dom_of(x[0]) != dom for x in (m, c)):
            raise ValueError("keep one domain")
        return dom, a, b, ind, m, c
    dom, a, b = read_if_then(major)
    if dom is not None:
        raise ValueError("an if-then major premise here is about things, like the car or the motor")
    if not minor.endswith(".") or not concl.endswith("."):
        raise ValueError("end each line with a period")
    return None, a, b, None, read_clause(minor[0].lower() + minor[1:-1]), read_clause(concl[:-1])

def valid(a, b, minor, concl):
    """By truth table: no assignment makes a -> b and the minor premise true and the conclusion false."""
    names = sorted({x[0] for x in (a, b, minor, concl)}, key=str)
    for vals in itertools.product((True, False), repeat=len(names)):
        v = dict(zip(names, vals))
        t = lambda lit: v[lit[0]] == lit[1]
        if ((not t(a)) or t(b)) and t(minor) and not t(concl):
            return False
    return True

# ------------------------------------------------------------------
# Type 1: is the syllogism valid?
# ------------------------------------------------------------------
T1_VALID = "Valid. The major premise is about the set of {S}, and the minor premise says {ind} is a member of that set."
T1_INVALID = ("Invalid. The major premise is about the set of {S}. The minor premise says {ind} is a member of the "
              "set of {Q}, not a member of the set of {S2}.")
FORMS1 = ("member", "property")             # the minor premise names a member (valid) or the property (invalid)

def t1(S, Q, ind, shape):
    a, b = (S, True), (Q, True)
    minor, concl = (a, b) if shape == "member" else (b, a)
    return syllogism(dom_of(S), a, b, ind, minor, concl)

def t1_ok(S, Q, ind, shape):
    return (S in PRED and Q in PRED and "kind" in PRED[S]["roles"] and "prop" in PRED[Q]["roles"] and S != Q
            and dom_of(S) == dom_of(Q) and ind in PRED[S]["inds"] and shape in FORMS1)

def t1_pick(shape):
    def pick(r):
        S = r.choice(kinds())
        p = dict(S=S, Q=r.choice(props(dom_of(S))), ind=r.choice(PRED[S]["inds"]), shape=shape)
        need(t1_ok(**p))
        return p
    return pick

def answer1(prompt):
    dom, a, b, ind, m, c = read_syllogism(prompt)
    if dom is None:
        raise ValueError("Type 1's major premise starts with All")
    ok = valid(a, b, m, c)
    if m == a and c == b:
        return gen.fill(T1_VALID, S=form(a, "set"), ind=low(ind))
    if m == b and c == a:
        return gen.fill(T1_INVALID, S=form(a, "set"), ind=low(ind), Q=form(b, "set"), S2=form(a, "set"))
    return "Valid." if ok else "Invalid."

def check1(p):
    dom, a, b, ind, m, c = read_syllogism(p["prompt"])
    ans = " ".join(p["answer"].split())
    verdict = valid(a, b, m, c)
    if not re.match(r"(Valid|Invalid)\.( |$)", ans) or ans.startswith("Valid") != verdict:
        return "failed"
    if ans in ("Valid.", "Invalid."):
        return "checked"
    try:
        v = gen.read(T1_VALID, ans)
        ok = SET.get(v["S"]) == a == m and v["ind"] == low(ind)
    except ValueError:
        try:
            v = gen.read(T1_INVALID, ans)
        except ValueError:
            return "unchecked"                            # a reason in other words
        ok = (SET.get(v["S"]) == a and v["S2"] == v["S"] and SET.get(v["Q"]) == m and m != a
              and v["ind"] == low(ind))
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Type 2: write as an if-then statement
# ------------------------------------------------------------------
def t2(S, Spol, Q, Qpol):
    return statement((S, Spol), (Q, Qpol))

def subject_ok(S, Spol):
    return S in PRED and "kind" in PRED[S]["roles"] and PRED[S]["forms"][Spol]["noun"] is not None

def t2_ok(S, Spol, Q, Qpol):
    return (subject_ok(S, Spol) and Q in PRED and "prop" in PRED[Q]["roles"] and S != Q
            and dom_of(S) == dom_of(Q) and Qpol in (True, False))

def subject(r, non):
    """A kind, or (non) a kind's non- form: nonathletes."""
    if non:
        S = r.choice([k for k in kinds() if PRED[k]["forms"][False]["noun"]])
        return S, False
    return r.choice(kinds()), True

def t2_pick(non=False, negated=False):
    def pick(r):
        S, Spol = subject(r, non)
        p = dict(S=S, Spol=Spol, Q=r.choice(props(dom_of(S))), Qpol=not negated)
        need(t2_ok(**p))
        return p
    return pick

def answer2(prompt):
    dom, a, b = read_statement(prompt)
    return if_then(dom, a, b)

def check2(p):
    dom, a, b = read_statement(p["prompt"])
    try:
        d2, x, y = read_if_then(p["answer"])
    except ValueError:
        return "failed"                                   # the prompt reads; the answer doesn't
    if d2 != dom or (x, y) != (a, b):
        return "failed"
    return "checked" if re.match(rf"If {DOMAINS[dom][0]} .+, then {DOMAINS[dom][1]} ", p["answer"]) else "failed"

# ------------------------------------------------------------------
# Type 3: write the contrapositive
# ------------------------------------------------------------------
def t3_dom(P, Ppol, Q, Qpol):
    return if_then(dom_of(P), (P, Ppol), (Q, Qpol))

def t3_dom_ok(P, Ppol, Q, Qpol):
    return (P in PRED and Q in PRED and P != Q and dom_of(P) == dom_of(Q)
            and ("kind" in PRED[P]["roles"] and "prop" in PRED[Q]["roles"]
                 or "prop" in PRED[P]["roles"] and "kind" in PRED[Q]["roles"])
            and Ppol in (True, False) and Qpol in (True, False))

def t3_dom_pick(r):
    K = r.choice(kinds())
    Pr = r.choice(props(dom_of(K)))
    first = r.random() < 0.6 or "kind" in PRED[Pr]["roles"]    # the kind in the if-part (always, before rectangle)
    P, Q = (K, Pr) if first else (Pr, K)
    p = dict(P=P, Ppol=r.random() < 0.75, Q=Q, Qpol=r.random() < 0.6)
    need(t3_dom_ok(**p))
    return p

def t3_prop(pair, flip=False):
    return if_then(None, *pair_of(pair, flip))

def t3_prop_ok(pair, flip=False):
    return pair in range(len(PAIRS)) and flip in (True, False)

def t3_prop_pick(r):
    return dict(pair=r.randrange(len(PAIRS)), flip=r.random() < 0.3)

def answer3(prompt):
    dom, a, b = read_if_then(prompt)
    return if_then(dom, neg(b), neg(a))

def check3(p):
    dom, a, b = read_if_then(p["prompt"])
    try:
        d2, x, y = read_if_then(p["answer"])
    except ValueError:
        return "failed"
    if d2 != dom or x != neg(b) or y != neg(a):
        return "failed"
    if dom in DOMAINS and not re.match(rf"If {DOMAINS[dom][0]} .+, then {DOMAINS[dom][1]} ", p["answer"]):
        return "failed"
    return "checked"

# ------------------------------------------------------------------
# Type 4: the contrapositive tests a syllogism
# ------------------------------------------------------------------
CONTRA = "Contrapositive of the major premise: "
T4_VALID_TAIL = "The minor premise says {minor}, so {concl}. The argument is valid."
T4_INVALID_TAIL = ("The minor premise says {minor}, but neither the premise nor its contrapositive starts with "
                   "that, so the conclusion does not follow. The argument is invalid.")
FORMS4 = ("then", "if")                     # the minor premise denies the then-part (valid) or the if-part (invalid)

def denied(a, b, shape):
    return (neg(b), neg(a)) if shape == "then" else (neg(a), neg(b))

def t4_cat(S, Spol, Q, ind, shape):
    a, b = (S, Spol), (Q, True)
    return syllogism(dom_of(S), a, b, ind, *denied(a, b, shape))

def t4_cat_ok(S, Spol, Q, ind, shape):
    return (subject_ok(S, Spol) and Q in PRED and "prop" in PRED[Q]["roles"] and S != Q
            and dom_of(S) == dom_of(Q) and ind in PRED[S]["inds"] and shape in FORMS4)

def t4_cat_pick(shape):
    def pick(r):
        S, Spol = subject(r, r.random() < 0.5)
        p = dict(S=S, Spol=Spol, Q=r.choice(props(dom_of(S))), ind=r.choice(PRED[S]["inds"]), shape=shape)
        need(t4_cat_ok(**p))
        return p
    return pick

def t4_prop(pair, shape, flip=False):
    a, b = pair_of(pair, flip)
    return syllogism(None, a, b, None, *denied(a, b, shape))

def t4_prop_ok(pair, shape, flip=False):
    return pair in range(len(PAIRS)) and shape in FORMS4 and flip in (True, False)

def t4_prop_pick(shape):
    return lambda r: dict(pair=r.randrange(len(PAIRS)), shape=shape, flip=r.random() < 0.3)

def said(dom, ind, lit):
    return say_clause(lit) if dom is None else f"{low(ind)} {member(lit)}"

def answer4(prompt):
    dom, a, b, ind, m, c = read_syllogism(prompt)
    contra = if_then(dom, neg(b), neg(a))
    if valid(a, b, m, c):
        return CONTRA + contra + " " + gen.fill(T4_VALID_TAIL, minor=said(dom, ind, m), concl=said(dom, ind, c))
    return CONTRA + contra + " " + gen.fill(T4_INVALID_TAIL, minor=said(dom, ind, m))

def read_said(dom, ind, s):
    if dom is None:
        return read_clause(s)
    if not s.startswith(low(ind) + " "):
        raise ValueError("name the same individual")
    return read_sg(dom, s[len(low(ind)) + 1:])

def check4(p):
    dom, a, b, ind, m, c = read_syllogism(p["prompt"])
    ans = " ".join(p["answer"].split())
    verdict = valid(a, b, m, c)
    tail = re.search(r"The argument is (valid|invalid)\.$", ans)
    if not tail or (tail.group(1) == "valid") != verdict:
        return "failed"
    mm = re.match(re.escape(CONTRA) + r"(If .+?, then .+?\.) ", ans)
    if not mm:
        return "unchecked"
    d2, x, y = read_if_then(mm.group(1))
    if d2 != dom or x != neg(b) or y != neg(a):
        return "failed"                                   # not the contrapositive
    rest = ans[mm.end():]
    try:
        v = gen.read(T4_VALID_TAIL, rest)
        ok = verdict and read_said(dom, ind, v["minor"]) == m and read_said(dom, ind, v["concl"]) == c
    except ValueError:
        try:
            v = gen.read(T4_INVALID_TAIL, rest)
        except ValueError:
            return "unchecked"                            # a reason in other words
        ok = not verdict and read_said(dom, ind, v["minor"]) == m and m not in (a, neg(b))   # starts neither
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Type 5: the converse and the inverse (built from Type 3's statements)
# ------------------------------------------------------------------
T5 = "Converse: {converse} Inverse: {inverse}"

def answer5(prompt):
    dom, a, b = read_if_then(prompt)
    return gen.fill(T5, converse=if_then(dom, b, a), inverse=if_then(dom, neg(a), neg(b)))

def check5(p):
    dom, a, b = read_if_then(p["prompt"])
    m = re.fullmatch(r"Converse: (If .+?, then .+?\.) Inverse: (If .+?, then .+?\.)", " ".join(p["answer"].split()))
    if not m:
        return "failed"
    try:
        (d1, x1, y1), (d2, x2, y2) = read_if_then(m.group(1)), read_if_then(m.group(2))
    except ValueError:
        return "failed"
    if d1 != dom or d2 != dom or (x1, y1) != (b, a) or (x2, y2) != (neg(a), neg(b)):
        return "failed"
    if dom in DOMAINS and not all(re.match(rf"If {DOMAINS[dom][0]} .+, then {DOMAINS[dom][1]} ", g)
                                  for g in m.groups()):
        return "failed"
    return "checked"

# ------------------------------------------------------------------
# Templates: (pick, build)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick("member"), t1), (t1_pick("property"), t1), (t1_pick("property"), t1)],
    "2": [(t2_pick(), t2), (t2_pick(), t2), (t2_pick(non=True), t2), (t2_pick(negated=True), t2)],
    "3": [(t3_dom_pick, t3_dom), (t3_dom_pick, t3_dom), (t3_prop_pick, t3_prop)],
    "4": [(t4_cat_pick("then"), t4_cat), (t4_cat_pick("then"), t4_cat), (t4_prop_pick("then"), t4_prop),
          (t4_prop_pick("then"), t4_prop), (t4_cat_pick("if"), t4_cat), (t4_prop_pick("if"), t4_prop)],
    "5": [(t3_dom_pick, t3_dom), (t3_dom_pick, t3_dom), (t3_prop_pick, t3_prop)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3_dom: t3_dom_ok, t3_prop: t3_prop_ok, t4_cat: t4_cat_ok, t4_prop: t4_prop_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

ANSWER = {"1": answer1, "2": answer2, "3": answer3, "4": answer4, "5": answer5}
CHECK = {"1": check1, "2": check2, "3": check3, "4": check4, "5": check5}

def answer_of(typ, prompt):
    return ANSWER[typ](prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(entry, prompt))

def check(p):
    try:
        return CHECK[p["type"]](p)
    except (ValueError, KeyError, AttributeError, TypeError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
LEAD = {
    "1": "Is the following argument a valid argument? Why or why not?",
    "2": "Write as an if-then statement:",
    "3": "Write the contrapositive of the statement:",
    "4": "Write the contrapositive of the major premise of this syllogism to help determine whether the "
         "following argument is valid or invalid:",
    "5": "Write the converse and the inverse of the statement:",
}

def lines(p):
    return [x.strip() for x in p["prompt"].split(" / ")]

def is_syllogism(p):
    return p["type"] in ("1", "4")

def typst(p, gap="0.3em"):
    if is_syllogism(p):
        major, minor, concl = (esc(x) for x in lines(p))
        return (f"{LEAD[p['type']]} \\\n#pad(left: 1.5em, top: 0.2em)[{major} \\\n"
                f"#underline(offset: 3pt)[{minor}] \\\n{concl}]")
    return f"{LEAD[p['type']]} #h(0.5em) {esc(p['prompt'])}"

def paragraph(a):
    """A reason that runs to several lines: the key sets answers at the right, so the
    lines would end flush right; this keeps them flush left across the width."""
    return f"#block(width: 96%)[#align(left)[{a}]]"

def answer_typst(p):
    a = esc(p["answer"])
    if p["type"] == "1":
        a = re.sub(r"^(Valid|Invalid)\.", r"*\1.*", a)
        return paragraph(a) if len(p["answer"]) > len("Invalid.") else a
    if p["type"] == "4":
        m = re.match(r"(Contrapositive of the major premise: )(If .+?, then .+?\.)( .*)", a)
        if m:
            a = f"{m.group(1)}_{m.group(2)}_{m.group(3)}"
        return paragraph(re.sub(r"(The argument is (?:valid|invalid)\.)$", r"*\1*", a))
    if p["type"] == "5":
        m = re.fullmatch(r"Converse: (.+?\.) Inverse: (.+)", a)
        if m:
            return paragraph(f"Converse: _{m.group(1)}_ \\\nInverse: _{m.group(2)}_")
        return paragraph(a)
    return f"_{a}_"

def text(p):
    if is_syllogism(p):
        return LEAD[p["type"]] + "\n" + "\n".join("    " + x for x in lines(p))
    return f"{LEAD[p['type']]} {p['prompt']}"

def answer_text(p):
    return p["answer"].replace(" Inverse: ", "\nInverse: ") if p["type"] == "5" else p["answer"]

def height(p):
    if is_syllogism(p):
        return 0.2 * (1 + len(LEAD[p["type"]]) // 90) + 0.65
    return 0.2 * (1 + len(text(p)) // 90)

# ------------------------------------------------------------------
# Editing: the words are read back; new words must negate by rule
# ------------------------------------------------------------------
HINT = {
    "1": "keep three lines split by /: All chickens have three legs. / Henny Penny is a chicken. / Therefore, ...",
    "2": "write a statement like Elephants are large animals.",
    "3": "write an if-then statement like If the team won, then the coach is happy.",
    "4": "keep three lines split by /: If the car is not moving, then the motor is off. / The motor is on. / "
         "Therefore, ...",
    "5": "write an if-then statement like If the team won, then the coach is happy.",
}
READ = {"1": read_syllogism, "2": read_statement, "3": read_if_then, "4": read_syllogism, "5": read_if_then}

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    if old["type"] in ("1", "4"):
        t = " / ".join(x.strip() for x in t.split("/"))
    try:
        READ[old["type"]](t)
    except ValueError as e:
        raise ValueError(f"{e}; {HINT[old['type']]}") from None
    try:
        answer = answer_of(old["type"], t)
    except ValueError:
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
