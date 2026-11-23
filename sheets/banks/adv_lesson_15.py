"""Lesson 15 (Advanced Math): assumptions; proofs: Euclid's postulates, two-column
proofs. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_015/slides/deck_015.typ): examples 15.5 and 15.6
and Problem Set 15, problems 5 and 6.

    1  triangles congruent, the givens marked:    given AC = BC, angle ACD = angle BCD;
                                                  prove triangle ACD = triangle BCD          (problem 5)
    2  triangles congruent, a given turned into   given angle Q = angle S, PQ parallel SR;
       congruent parts first:                     prove triangle PQR = triangle RSP          (15.6)
    3  a part, by CPCTC:                          given BD bisects angle B, AB = CB;
                                                  prove AD = CD                              (15.5)

The answer is a two-column proof, the deck's statements and reasons. The playbook
skipped two-column proofs until this lesson; the teacher brought congruence proofs
in scope here (BANK_PLAYBOOK.md now says so). The theorem proofs, examples
15.1-15.4, stay skipped.

The types split the problem types file's one heading by the move: Type 1's givens are
the congruent parts (problems 5 and 6); Type 2 has a given that isn't a congruence yet,
an angle bisector, a midpoint, or parallel sides, and a row must turn it into one (15.6:
parallel lines cut by a transversal make alternate interior angles congruent); Type 3
proves a pair of parts, the triangles' congruence first and then CPCTC (15.5).

The figures are Lesson 9's split triangle (15.5, problem 5) and kite (problem 6, turned over so A is
at the top, as the book draws it), and a
parallelogram with one diagonal (15.6), its points named by role as the book names
them: split A B C D or A C B D (the base, the apex, the foot), kite A B C D (A and C on
the diagonal), para P Q R S (the diagonal P R; P Q parallel to S R, Q R to P S).
Lesson 9's machinery reads the figure's segments, angles, and triangles from its
points. Parallel sides are marked with arrowheads, as the book draws them; the
key's figure is the same (the proof is the answer).

The key writes the deck's rows, in the deck's order:
    1. the congruences given, each "Given" (in the problem's order), then the
       other givens (a bisector, a midpoint, parallel sides), each "Given";
    2. each of those turned into congruent parts, with its reason;
    3. for AAAS, the third pair of angles ("If two angles of one triangle are
       congruent to two angles of another, the third angles are congruent"),
       unless it is known already: the book's AAAS uses all three angles;
    4. a side both triangles share, "Reflexive axiom", when the postulate uses it;
    5. the triangles' congruence and its postulate (SSS, SAS, AAAS);
    6. for a part, the part and "CPCTC".
The triangles are named in the goal's order, or for a part with the first triangle's
vertices in the figure's role order (15.5: triangle ABD = triangle CBD).

check() is a proof checker: it reads the rows in order and accepts each only if the
givens and the rows above it justify it. A "Given" must be a given. A bisector, a
midpoint, or parallel sides justify only the congruence they make (alternate
interior angles are found from the figure: the transversal joins the parallels,
and the angles lie on opposite sides of it). The third angles need the other two
pairs of the two triangles. A postulate needs its parts (SSS three sides; SAS two
sides and the angle between them; AAAS three angles and a side), a shared side only
if a reflexive row said so, and the triangles really congruent in the drawing in the
row's vertex order. CPCTC needs a proved congruence whose corresponding parts these
are. The last row must be the goal, and every given must be listed.

Skipped sources: examples 15.1-15.4, theorem proofs (a median of an isosceles
triangle bisects the vertex angle; tangent segments are equal; a triangle's angles
sum to 180°; vertical angles are equal, from Euclid's postulates). They prove the
lesson's theorems, not congruences from givens about a figure.

A problem: dict(type, prompt, answer, source).
    prompt  "split A C B D; B D bis angle A B C, A B = C B; show A D = C D"
    answer  "A B = C B | given; B D bis angle A B C | given; angle A B D = angle C B D | bisector;
             B D = B D | reflexive; triangle A B D = triangle C B D | SAS; A D = C D | CPCTC"
A given is "A D = B D", "angle Q = angle S" or "angle A C D = angle B C D",
"B D bis angle A B C" (B D bisects angle A B C), "D mid A C", or "P Q par S R".
"""
import itertools, math, re
from .. import gen
from ..gen import need
from . import lesson_figures as fig
from . import adv_lesson_9 as L9

NAME = FAMILY = "adv_lesson_15"
FIXED = False
TITLE = "Lesson 15: Assumptions, Proofs, Euclid's Postulates, Two-Column Proofs"
INSTRUCTIONS = "Write a two-column proof."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Two-Column Proof: Congruent Triangles",
         look="Congruent parts given about a figure, and two triangles to prove congruent.",
         move="List each given with the reason Given. A side both triangles share is congruent to itself: "
              "$overline(C D) tilde.equiv overline(C D)$, Reflexive axiom. Then the triangles, their vertices in "
              "matching order, and the postulate: SSS, SAS (the angle between the two sides), or AAAS."),
    dict(key="2", title="Two-Column Proof: A Given to Turn Into Congruent Parts",
         look="A given that isn't a congruence yet: an angle bisector, a midpoint, or parallel sides.",
         move="After the givens, turn that one into congruent parts, with its reason. Parallel lines cut by a "
              "transversal: alternate interior angles are congruent, $angle Q P R tilde.equiv angle S R P$. An angle "
              "bisector makes two congruent angles; a midpoint, two congruent segments. For AAAS, the third angles "
              "are congruent too. Then the reflexive side and the postulate."),
    dict(key="3", title="Two-Column Proof of a Part, by CPCTC",
         look="Two segments or two angles to prove congruent.",
         move="Find two triangles that hold the parts. Prove the triangles congruent, row by row, then the last "
              "row: $overline(A D) tilde.equiv overline(C D)$, CPCTC (corresponding parts of congruent triangles "
              "are congruent)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="2.6in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

POSTULATES = ("SSS", "SAS", "AAAS")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The figures: Lesson 9's split triangle and kite, and a parallelogram with a diagonal
# ------------------------------------------------------------------
SIZE = {"split": 4, "kite": 4, "para": 4}
CHAINS = {"split": L9.CHAINS["split"], "kite": L9.CHAINS["kite"],
          "para": ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))}

def layout(family):
    if family == "para":
        return [(0.0, 0.0), (0.6, 1.6), (3.2, 1.6), (2.6, 0.0)]     # P Q R S: P Q parallel to S R, Q R to P S
    if family == "kite":                                            # Lesson 9's, turned over: A at the top (problem 6)
        return [(x, 3 - y) for x, y in L9.layout("kite", None)]
    return L9.layout(family, None)

class Figure(L9.Figure):
    """Lesson 9's figure, for this lesson's families (no perpendiculars)."""
    def __init__(self, family, names):
        if family not in SIZE:
            raise ValueError("start with " + ", ".join(SIZE))
        if len(names) != SIZE[family] or len(set(names)) != len(names):
            raise ValueError(f"name the {SIZE[family]} points of the {family} with different letters")
        self.family, self.names = family, tuple(names)
        self.chains = [tuple(names[i] for i in c) for c in CHAINS[family]]
        self.pts = dict(zip(self.names, layout(family)))
        self._rays, self._tris, self._ang = {}, None, {}

    def chain(self, a, b):
        if a == b or a not in self.names or b not in self.names:
            return None
        for c in self.chains:
            if a in c and b in c:
                return c
        return None

# ------------------------------------------------------------------
# Reading facts: Lesson 9's, and a bisector and parallel sides
# ------------------------------------------------------------------
LT = r"([A-Z])"
BIS = re.compile(rf"{LT} {LT} bis angle {LT} {LT} {LT}")
PAR = re.compile(rf"{LT} {LT} par {LT} {LT}")

def parse_fact(s):
    """Lesson 9's facts, and ("bis", (v, e), (p, v, q)) and ("par", (a, b), (c, d))."""
    s = " ".join(s.split())
    m = BIS.fullmatch(s)
    if m:
        g = m.groups()
        return ("bis", g[:2], g[2:])
    m = PAR.fullmatch(s)
    if m:
        g = m.groups()
        return ("par", g[:2], g[2:])
    f = L9.parse_fact(s)
    if f[0] == "perp":
        raise ValueError("this lesson's givens: congruences, a bisector (bis), a midpoint (mid), or parallels (par)")
    return f

def fact_text(f):
    if f[0] == "bis":
        return f"{' '.join(f[1])} bis angle {' '.join(f[2])}"
    if f[0] == "par":
        return f"{' '.join(f[1])} par {' '.join(f[2])}"
    return L9.fact_text(f)

CONGRUENCES = ("seg", "ang")

def made(F_, g):
    """The congruent pairs (items) a bisector, a midpoint, or parallel sides make, with the
    statement for each: [((a, b), fact)]. Raises if the given isn't true of the figure."""
    if g[0] == "bis":
        (v, e), (p, w, q) = g[1], g[2]
        if w != v:
            raise ValueError(f"{v}{e} must start at the angle's vertex")
        a, b = F_.ang(v, p, e), F_.ang(v, q, e)
        if abs(abs_angle(F_, v, p, e) - abs_angle(F_, v, q, e)) > 1e-6:
            raise ValueError(f"{v}{e} doesn't bisect angle {p}{v}{q} in this figure")
        return [((a, b), ("ang", (p, v, e), (q, v, e)))]
    if g[0] == "mid":
        m, (x, y) = g[1], g[2]
        c = F_.chain(x, y)
        if c is None or m not in c or not (min(c.index(x), c.index(y)) < c.index(m) < max(c.index(x), c.index(y))):
            raise ValueError(f"{m} must lie between {x} and {y}")
        if abs(F_.length(x, m) - F_.length(m, y)) > 1e-9:
            raise ValueError(f"{m} isn't the midpoint of {x}{y} in this figure")
        return [((F_.seg(x, m), F_.seg(y, m)), ("seg", (x, m), (y, m)))]
    if g[0] == "par":
        out = alternate(F_, g)
        if not out:
            raise ValueError("no transversal joins those parallels")
        return out
    return []

def abs_angle(F_, v, p, q):
    (ax, ay), (bx, by) = F_.vec(v, p), F_.vec(v, q)
    return abs(math.degrees(math.atan2(ax * by - ay * bx, ax * bx + ay * by)))

def cross(F_, o, a, b):
    (ax, ay), (bx, by) = F_.vec(o, a), F_.vec(o, b)
    return ax * by - ay * bx

def alternate(F_, g):
    """The alternate interior angles of parallels a b and c d: a transversal is a segment of
    the figure from an end of one to an end of the other, and the two angles it makes with
    them lie on opposite sides of it. [((item, item), fact)]."""
    (a, b), (c, d) = g[1], g[2]
    if not (F_.joined(a, b) and F_.joined(c, d)):
        raise ValueError(f"{a}{b} and {c}{d} must be segments of the figure")
    u1, u2 = F_.vec(a, b), F_.vec(c, d)
    if abs(u1[0] * u2[1] - u1[1] * u2[0]) > 1e-9:
        raise ValueError(f"{a}{b} and {c}{d} aren't parallel in this figure")
    out = []
    for u, ou in ((a, b), (b, a)):
        for w, ow in ((c, d), (d, c)):
            if u == w or not F_.joined(u, w) or F_.chain(u, w) in (F_.chain(a, b), F_.chain(c, d)):
                continue
            if cross(F_, u, w, ou) * cross(F_, u, w, ow) < 0:          # opposite sides of the transversal
                out.append(((F_.ang(u, ou, w), F_.ang(w, ow, u)), ("ang", (ou, u, w), (ow, w, u))))
    return out

def read(prompt):
    """(figure, givens, goal) from "split A C B D; B D bis angle A B C, A B = C B; show A D = C D"."""
    s = " ".join(prompt.split())
    parts = [x.strip() for x in s.split(";")]
    if len(parts) != 3 or not parts[2].startswith("show "):
        raise ValueError("write it like: split A C B D; B D bis angle A B C, A B = C B; show A D = C D")
    head = parts[0].split()
    F_ = Figure(head[0], head[1:])
    givens = [parse_fact(x) for x in L9.split_facts(parts[1])]
    if not givens or any(g[0] == "tri" for g in givens):
        raise ValueError("give facts about segments and angles")
    goal = parse_fact(parts[2][5:])
    if goal[0] not in ("seg", "ang", "tri"):
        raise ValueError("prove two segments, two angles, or two triangles congruent")
    for g in givens:                                     # every given names parts of the figure
        if g[0] in CONGRUENCES:
            L9.item(F_, g[1], g[0]), L9.item(F_, g[2], g[0])
        else:
            made(F_, g)
    return F_, givens, goal

# ------------------------------------------------------------------
# Solving: what the givens make congruent, and the triangles that prove the goal
# ------------------------------------------------------------------
class Equal:
    """Union-find over the figure's items; right() is never true (no right angles here)."""
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)

    def eq(self, a, b):
        return a == b or self.find(a) == self.find(b)

    def right(self, a):
        return False

def closure(F_, givens):
    C = Equal()
    for g in givens:
        if g[0] in CONGRUENCES:
            C.union(L9.item(F_, g[1], g[0]), L9.item(F_, g[2], g[0]))
        else:
            for (a, b), _ in made(F_, g):
                C.union(a, b)
    return C

def support(F_, C, t1, t2):
    """Lesson 9's postulates, without HL: {postulate: the parts it uses}."""
    s = L9.support(F_, C, t1, t2)
    return {k: v for k, v in s.items() if k in POSTULATES}

def role_order(F_, t1, t2):
    """The correspondence with the first triangle's vertices in the figure's role order."""
    m = dict(zip(t1, t2))
    a = tuple(sorted(t1, key=F_.names.index))
    return a, tuple(m[x] for x in a)

def solve(F_, givens, goal):
    """(t1, t2, postulate, parts) of the proof, or None: SSS first, then SAS, then AAAS."""
    C = closure(F_, givens)
    if goal[0] != "tri" and C.eq(L9.item(F_, goal[1], goal[0]), L9.item(F_, goal[2], goal[0])):
        return None                                      # nothing to prove
    best = None
    for t1, t2 in L9.candidates(F_, goal):
        if not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
            continue
        if not L9.congruent_drawn(F_, t1, t2):
            continue
        s = support(F_, C, t1, t2)
        for post in POSTULATES:
            if post in s and (best is None or POSTULATES.index(post) < POSTULATES.index(best[2])):
                best = (t1, t2, post, s[post])
    if best is None:
        return None
    t1, t2, post, used = best
    if goal[0] != "tri":
        t1, t2 = role_order(F_, t1, t2)
    return t1, t2, post, used

def angle_text(t, i):
    """The angle at vertex i of triangle t, by three letters: the vertex before, it, the one after."""
    return (t[i - 1], t[i], t[(i + 1) % 3])

def proof_rows(F_, givens, goal):
    """[(fact, reason code)]: the key's two-column proof, in the deck's order."""
    found = solve(F_, givens, goal)
    if found is None:
        raise ValueError("SSS, SAS, or AAAS doesn't prove it from these givens")
    t1, t2, post, _ = found
    C = closure(F_, givens)
    rows = [(g, "given") for g in givens if g[0] in CONGRUENCES]
    rows += [(g, "given") for g in givens if g[0] not in CONGRUENCES]
    for g in givens:
        if g[0] not in CONGRUENCES:
            rows += [(f, REASON_CODE[g[0]]) for _, f in made(F_, g)]
    S, A = L9.parts(F_, t1, t2)
    if post == "AAAS":
        third = [i for i in range(3) if not C.eq(*A[i])]
        for i in third[:1]:
            rows.append((("ang", angle_text(t1, i), angle_text(t2, i)), "third"))
    used = support(F_, C, t1, t2)[post] if post != "AAAS" else None
    if post == "AAAS":                                   # the side: a given one, else the shared one
        sides = [i for i in range(3) if C.eq(*S[i])]
        given_sides = [i for i in sides if S[i][0] != S[i][1]]
        side = (given_sides or sides)[0]
        used = [S[side]]
    for a, b in used:
        if a == b and a[0] == "s":
            i = next(j for j in range(3) if S[j][0] == a)
            x, y = sorted((i, (i + 1) % 3))
            rows.append((("seg", (t1[x], t1[y]), (t1[x], t1[y])), "reflexive"))
    rows.append((("tri", tuple(t1), tuple(t2)), post))
    if goal[0] != "tri":
        if any(same_fact(F_, f, goal) for f, _ in rows):
            raise ValueError("the goal follows before the triangles are congruent")   # third angles gave it
        rows.append((goal, "CPCTC"))
    return rows

REASON_CODE = {"bis": "bisector", "mid": "midpoint", "par": "parallel"}

def answer_text_of(rows):
    return "; ".join(f"{fact_text(f)} | {code}" for f, code in rows)

def answer_of(prompt):
    F_, givens, goal = read(prompt)
    return answer_text_of(proof_rows(F_, givens, goal))

def kind_of(prompt):
    """1: triangles from congruences given; 2: triangles, a given to turn first; 3: a part."""
    _, givens, goal = read(prompt)
    if goal[0] != "tri":
        return "3"
    return "1" if all(g[0] in CONGRUENCES for g in givens) else "2"

# ------------------------------------------------------------------
# The givens and goals each family draws from, in role letters
# ------------------------------------------------------------------
CANDS = {
    "split": ["{2} {3} bis angle {0} {2} {1}", "{0} {2} = {1} {2}", "angle {0} {2} {3} = angle {1} {2} {3}",
              "{0} {3} = {1} {3}", "{3} mid {0} {1}", "angle {0} = angle {1}",
              "angle {0} {3} {2} = angle {1} {3} {2}"],
    "kite": ["{0} {1} = {0} {3}", "{1} {2} = {3} {2}", "angle {1} {0} {2} = angle {3} {0} {2}",
             "angle {1} {2} {0} = angle {3} {2} {0}", "angle {1} = angle {3}", "{0} {2} bis angle {1} {0} {3}",
             "{2} {0} bis angle {1} {2} {3}"],
    "para": ["angle {1} = angle {3}", "{0} {1} par {3} {2}", "{1} {2} par {0} {3}", "{0} {1} = {2} {3}",
             "{1} {2} = {3} {0}"],
}
GOALS = {
    "split": ["triangle {0} {2} {3} = triangle {1} {2} {3}", "{0} {3} = {1} {3}", "{0} {2} = {1} {2}",
              "angle {0} = angle {1}", "angle {0} {2} {3} = angle {1} {2} {3}",
              "angle {0} {3} {2} = angle {1} {3} {2}"],
    "kite": ["triangle {0} {1} {2} = triangle {0} {3} {2}", "{1} {2} = {3} {2}", "{0} {1} = {0} {3}",
             "angle {0} {1} {2} = angle {0} {3} {2}", "angle {1} {0} {2} = angle {3} {0} {2}",
             "angle {1} {2} {0} = angle {3} {2} {0}"],
    "para": ["triangle {0} {1} {2} = triangle {2} {3} {0}", "{0} {1} = {2} {3}", "{1} {2} = {3} {0}",
             "angle {1} = angle {3}", "angle {1} {0} {2} = angle {3} {2} {0}",
             "angle {1} {2} {0} = angle {3} {0} {2}"],
}
MOST = 3                                                 # the most givens a problem has
FAMILIES = tuple(CANDS)

def build(family, names, givens, goal):
    return (f"{family} {' '.join(names)}; {', '.join(CANDS[family][i].format(*names) for i in givens)}; "
            f"show {GOALS[family][goal].format(*names)}")

def enumerate_combos(kind, family):
    """Every (givens, goal) of the type in the family: proved by SSS, SAS, or AAAS, with
    every given needed (none can be dropped), and a part's goal not reached before its
    triangles are (a third pair of angles can be the goal itself)."""
    names = tuple("ABCD")
    proved = {}
    n = len(CANDS[family])
    for size in range(1, MOST + 1):
        for sub in itertools.combinations(range(n), size):
            for g in range(len(GOALS[family])):
                try:
                    F_, givens, goal = read(build(family, names, sub, g))
                    proved[sub, g] = bool(proof_rows(F_, givens, goal))
                except ValueError:
                    proved[sub, g] = False
    out = []
    for (sub, g), ok in proved.items():
        if not ok or any(proved.get((tuple(x for x in sub if x != i), g)) for i in sub):
            continue
        if kind_of(build(family, names, sub, g)) == kind:
            out.append((sub, g))
    return tuple(out)

COMBOS = {   # (type, family): (givens, goal) -- enumerate_combos() made it; tests/test_adv_lesson_15.py remakes it
    ('1', 'split'): (((1, 2), 0), ((1, 3), 0), ((2, 5), 0), ((2, 6), 0), ((3, 6), 0), ((5, 6), 0),),
    ('1', 'kite'): (((0, 1), 0), ((0, 2), 0), ((1, 3), 0), ((2, 3), 0), ((2, 4), 0), ((3, 4), 0),),
    ('1', 'para'): (((3, 4), 0),),
    ('2', 'split'): (((0, 1), 0), ((0, 5), 0), ((0, 6), 0), ((1, 4), 0), ((4, 6), 0),),
    ('2', 'kite'): (((0, 5), 0), ((1, 6), 0), ((2, 6), 0), ((3, 5), 0), ((4, 5), 0), ((4, 6), 0), ((5, 6), 0),),
    ('2', 'para'): (((0, 1), 0), ((0, 2), 0), ((1, 2), 0), ((1, 3), 0), ((2, 4), 0),),
    ('3', 'split'): (((0, 1), 1), ((0, 1), 3), ((0, 1), 5), ((0, 5), 1), ((0, 5), 2), ((0, 6), 1), ((0, 6), 2),
        ((1, 2), 1), ((1, 2), 3), ((1, 2), 5), ((1, 3), 3), ((1, 3), 4), ((1, 3), 5), ((1, 4), 3), ((1, 4), 4),
        ((1, 4), 5), ((2, 5), 1), ((2, 5), 2), ((2, 6), 1), ((2, 6), 2), ((3, 6), 2), ((3, 6), 3), ((3, 6), 4),
        ((4, 6), 2), ((4, 6), 3), ((4, 6), 4), ((5, 6), 1), ((5, 6), 2),),
    ('3', 'kite'): (((0, 1), 3), ((0, 1), 4), ((0, 1), 5), ((0, 2), 1), ((0, 2), 3), ((0, 2), 5), ((0, 5), 1),
        ((0, 5), 3), ((0, 5), 5), ((1, 3), 2), ((1, 3), 3), ((1, 3), 4), ((1, 6), 2), ((1, 6), 3), ((1, 6), 4),
        ((2, 3), 1), ((2, 3), 2), ((2, 4), 1), ((2, 4), 2), ((2, 6), 1), ((2, 6), 2), ((3, 4), 1), ((3, 4), 2),
        ((3, 5), 1), ((3, 5), 2), ((4, 5), 1), ((4, 5), 2), ((4, 6), 1), ((4, 6), 2), ((5, 6), 1), ((5, 6), 2),),
    ('3', 'para'): (((0, 1), 1), ((0, 1), 2), ((0, 2), 1), ((0, 2), 2), ((1, 2), 1), ((1, 2), 2), ((1, 3), 2),
        ((1, 3), 3), ((1, 3), 5), ((2, 4), 1), ((2, 4), 3), ((2, 4), 4), ((3, 4), 3), ((3, 4), 4), ((3, 4), 5),),
}

def combos(kind, family):
    return COMBOS.get((kind, family), ())

ALPHA = L9.ALPHA

def lettered(family, run, swap=False):
    return L9.lettered("split", run, swap) if family == "split" else tuple(run)

def names_ok(family, names):
    runs = [ALPHA[i:i + 4] for i in range(len(ALPHA) - 3)]
    return any(tuple(names) == lettered(family, run, s) for run in runs for s in (False, True))

def pick_names(r, family):
    i = r.randrange(len(ALPHA) - 3)
    return lettered(family, ALPHA[i:i + 4], r.random() < 0.5)

def proof_pick(kind, family):
    def pick(r):
        sub, g = r.choice(combos(kind, family))
        return dict(family=family, names=pick_names(r, family), givens=sub, goal=g)
    return pick

def proof_ok(family, names, givens, goal):
    return (family in FAMILIES and names_ok(family, names)
            and any((tuple(givens), goal) in combos(k, family) for k in KEYS))

TEMPLATES = {
    "1": [(proof_pick("1", "split"), build), (proof_pick("1", "kite"), build), (proof_pick("1", "para"), build)],
    "2": [(proof_pick("2", "split"), build), (proof_pick("2", "kite"), build), (proof_pick("2", "para"), build),
          (proof_pick("2", "para"), build)],
    "3": [(proof_pick("3", "split"), build), (proof_pick("3", "kite"), build), (proof_pick("3", "para"), build)],
}
RANGES = {build: proof_ok}

def in_range(build_, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build_](**params))

def draw(entry, r, tpl):
    pick, build_ = TEMPLATES[entry][tpl]
    prompt = build_(**pick(r))
    need(kind_of(prompt) == entry)
    return dict(prompt=prompt, answer=answer_of(prompt))

# ------------------------------------------------------------------
# The check: a proof checker, row by row, from the givens alone
# ------------------------------------------------------------------
ROW = re.compile(r"(.+?) \| (given|bisector|midpoint|parallel|third|reflexive|SSS|SAS|AAAS|CPCTC)")

def same_fact(F_, f, g):
    """Do two facts say the same thing about the figure?"""
    if f[0] != g[0]:
        return False
    if f[0] in CONGRUENCES:
        return ({L9.item(F_, f[1], f[0]), L9.item(F_, f[2], f[0])}
                == {L9.item(F_, g[1], g[0]), L9.item(F_, g[2], g[0])})
    if f[0] == "tri":
        return L9.mapping(f[1], f[2]) in (L9.mapping(g[1], g[2]), L9.mapping(g[2], g[1]))
    if f[0] == "par":
        return {frozenset(f[1]), frozenset(f[2])} == {frozenset(g[1]), frozenset(g[2])}
    if f[0] == "bis":
        return f[1][0] == g[1][0] and f[1][1] == g[1][1] and f[2][1] == g[2][1] and {f[2][0], f[2][2]} == {g[2][0], g[2][2]}
    return f[1] == g[1] and set(f[2]) == set(g[2])

def check_proof(F_, givens, goal, answer):
    rows = [ROW.fullmatch(" ".join(x.split())) for x in answer.split(";")]
    if not rows or not all(rows):
        return False
    E = Equal()
    reflexive, stated, proved = set(), [], []

    def known(a, b):
        return a in reflexive if a == b else E.eq(a, b)

    def pair(f):
        return L9.item(F_, f[1], f[0]), L9.item(F_, f[2], f[0])

    last = None
    for m in rows:
        f, code = parse_fact(m.group(1)), m.group(2)
        if code == "given":
            if not any(same_fact(F_, f, g) for g in givens):
                return False
            stated.append(f)
            if f[0] in CONGRUENCES:
                E.union(*pair(f))
        elif code in ("bisector", "midpoint", "parallel"):
            src = {"bisector": "bis", "midpoint": "mid", "parallel": "par"}[code]
            if f[0] not in CONGRUENCES:
                return False
            ok = any(set(pq) == set(pair(f)) for g in stated if g[0] == src for pq, _ in made(F_, g))
            if not ok:
                return False
            E.union(*pair(f))
        elif code == "third":
            if f[0] != "ang" or not third_ok(F_, pair(f), known):
                return False
            E.union(*pair(f))
        elif code == "reflexive":
            if f[0] != "seg" or set(f[1]) != set(f[2]):
                return False
            reflexive.add(F_.seg(*f[1]))
        elif code in POSTULATES:
            if f[0] != "tri" or not postulate_ok(F_, code, f[1], f[2], known):
                return False
            proved.append((f[1], f[2]))
        else:                                            # CPCTC
            if f[0] not in CONGRUENCES:
                return False
            if not any(L9.corresponds(F_, f, t1, t2) for t1, t2 in proved):
                return False
            E.union(*pair(f))
        last = f
    every_given = all(any(same_fact(F_, g, s) for s in stated) for g in givens)
    return every_given and last is not None and same_fact(F_, last, goal)

def postulate_ok(F_, post, t1, t2, known):
    if not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
        return False
    if not L9.congruent_drawn(F_, t1, t2):
        return False                                     # the vertices don't correspond
    S, A = L9.parts(F_, t1, t2)
    s, a = [known(*x) for x in S], [known(*x) for x in A]
    if post == "SSS":
        return all(s)
    if post == "SAS":
        return any(a[i] and s[i] and s[i - 1] for i in range(3))
    return all(a) and any(s)                            # AAAS: all three angles, and a side

def third_ok(F_, pq, known):
    """Two triangles hold the two angles, at corresponding vertices, and their other two
    pairs of angles are known."""
    x, y = pq
    for T1 in F_.triangles:
        for T2 in F_.triangles:
            if T1 == T2 or x[1] not in T1 or y[1] not in T2:
                continue
            if F_.tri_angle(T1, x[1]) != x or F_.tri_angle(T2, y[1]) != y:
                continue
            o1, o2 = sorted(T1 - {x[1]}), sorted(T2 - {y[1]})
            for p in (o2, o2[::-1]):
                if all(known(F_.tri_angle(T1, a), F_.tri_angle(T2, b)) for a, b in zip(o1, p)):
                    return True
    return False

def check(p):
    try:
        F_, givens, goal = read(p["prompt"])
        if kind_of(p["prompt"]) != p["type"]:
            return "failed"
        return "checked" if check_proof(F_, givens, goal, p["answer"]) else "failed"
    except (ValueError, KeyError, AttributeError, TypeError, IndexError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
REASONS = {
    "given": "Given",
    "bisector": "An angle bisector divides an angle into two congruent angles",
    "midpoint": "A midpoint divides a segment into two congruent segments",
    "parallel": "Parallel lines cut by a transversal: alternate interior angles are congruent",
    "third": "If two angles of one triangle are congruent to two angles of another, the third angles are congruent",
    "reflexive": "Reflexive axiom",
    "SSS": "#emph[SSS] congruency postulate", "SAS": "#emph[SAS] congruency postulate",
    "AAAS": "#emph[AAAS] congruency postulate", "CPCTC": "#emph[CPCTC]",
}

def seg_m(s):
    return f"overline({' '.join(s)})"

def fact_typst(f):
    kind = f[0]
    if kind == "seg":
        return f"${seg_m(f[1])} tilde.equiv {seg_m(f[2])}$"
    if kind == "ang":
        return f"$angle {' '.join(f[1])} tilde.equiv angle {' '.join(f[2])}$"
    if kind == "tri":
        return f"$triangle {' '.join(f[1])} tilde.equiv triangle {' '.join(f[2])}$"
    if kind == "bis":
        return f"${seg_m(f[1])}$ is the angle bisector of angle ${f[2][1]}$"
    if kind == "par":
        return f"${seg_m(f[1])} parallel {seg_m(f[2])}$"
    return f"${f[1]}$ is the midpoint of ${seg_m(f[2])}$"

def fact_plain(f):
    kind = f[0]
    if kind == "bis":
        return f"{''.join(f[1])} is the angle bisector of angle {f[2][1]}"
    if kind == "par":
        return f"{''.join(f[1])} ∥ {''.join(f[2])}"
    if kind == "tri":
        return f"△{''.join(f[1])} ≅ △{''.join(f[2])}"
    return L9.fact_plain(f)

def statement(p, show=fact_typst):
    F_, givens, goal = read(p["prompt"])
    return f"Given: {L9.listed([show(g) for g in givens])}. Write a two-column proof to prove: {show(goal)}."

def figure(p, unit="1cm"):
    F_, givens, _ = read(p["prompt"])
    arrows = [(g[1][0], g[1][1], n + 1) if F_.vec(*g[1])[1] >= 0 else (g[1][1], g[1][0], n + 1)
              for n, g in enumerate(x for x in givens if x[0] == "par")]
    arrows += [(g[2][0], g[2][1], n + 1) if F_.vec(*g[2])[1] >= 0 else (g[2][1], g[2][0], n + 1)
               for n, g in enumerate(x for x in givens if x[0] == "par")]
    wide, tall = (4.2, 2.3) if F_.family == "para" else (3.8, 2.8)
    return fig.marked(F_.pts, F_.chains, wide=wide, tall=tall, unit=unit, arrows=arrows)

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    return f"{s} #v(0.4em) #align(center)[{f}]"

def rows_of(answer):
    out = []
    for x in answer.split(";"):
        m = ROW.fullmatch(" ".join(x.split()))
        out.append((parse_fact(m.group(1)), m.group(2)))
    return out

def answer_typst(p):
    try:
        rows = rows_of(p["answer"])
    except (ValueError, AttributeError):
        return p["answer"]
    cells = ["[#smallcaps[Statements]]", "[#smallcaps[Reasons]]"]
    for i, (f, code) in enumerate(rows, 1):
        cells += [f"[{i}. {fact_typst(f)}]", f"[{i}. {REASONS[code]}]"]
    n = len(rows)
    return ("#table(columns: (auto, 1fr), inset: (x: 0.5em, y: 0.3em), align: left, "
            "stroke: (x, y) => (left: if x == 1 { 0.6pt } else { none }, "
            f"bottom: if y == 0 or y == {n} {{ 0.6pt }} else {{ none }}), " + ", ".join(cells) + ")")

SLIDE_UNIT = "1.6cm"

def slide_typst(p, key=False):
    """The words, and the proof (hidden on the question slide), beside the figure; the
    figure stays put."""
    try:
        f, s = figure(p, SLIDE_UNIT), statement(p)
    except (ValueError, AttributeError, KeyError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return (f"#grid(columns: (1fr, auto), column-gutter: 1.2em, align: horizon, "
            f"[{s} #v(0.6em) #text(size: 0.8em)[{shown}]], [{f}])")

def text(p):
    try:
        return statement(p, fact_plain) + "   [figure]"
    except ValueError:
        return p["prompt"]

def answer_text(p):
    try:
        rows = rows_of(p["answer"])
    except (ValueError, AttributeError):
        return p["answer"]
    plain = lambda c: re.sub(r"#emph\[(\w+)\]", r"\1", REASONS[c])
    return "\n".join(f"{i}. {fact_plain(f)}   {plain(c)}" for i, (f, c) in enumerate(rows, 1))

def height(p):
    return 2.9

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data
# ------------------------------------------------------------------
EXAMPLE = {"1": "kite A B C D; A B = A D, B C = D C; show triangle A B C = triangle A D C",
           "2": "para P Q R S; angle Q = angle S, P Q par S R; show triangle P Q R = triangle R S P",
           "3": "split A C B D; B D bis angle A B C, A B = C B; show A D = C D"}

def clean(t):
    return " ".join(t.replace("−", "-").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if kind_of(t) != old["type"]:
            raise ValueError
        answer = answer_of(t)
    except ValueError:
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
