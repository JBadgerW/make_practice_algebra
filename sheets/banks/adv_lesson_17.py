"""Lesson 17 (Advanced Math): proofs of the Pythagorean theorem, proofs of similarity.
From the Saxon lesson and its deck (~/Documents/adv_math/problem_sets/ps_017/slides/deck_017.typ):
examples 17.1-17.3 and Problem Set 17, problems 4-8.

    1  similarity proof, an angle given:   prove triangle ABC ~ triangle EDC; angle A = angle E marked    (17.1)
    2  similarity proof, parallels given:  prove triangle ABC ~ triangle DEC; AB parallel ED             (17.2, problem 8)
    3  SAS similarity, from numbers:       angle G = angle J = 30°; 12, 15 and 8, 10                     (17.3)
    4  similar? from the sides:            angle B = angle Y, 6, 4 and 3, 2 (SAS); sides 2, 2, 2 and 3, 3, 3 (SSS)
                                                                                                        (problems 4, 5)
    5  similar? from the angles:           two pairs of angles marked (problem 6); 27°, 115° and 38°, 27° (problem 7)

The problem types file has one heading; it is five types here, one per move. Types 1
and 2 are two-column proofs on two triangles that meet at a point (the "bowtie":
segments AD and BE crossing at C), as Lesson 15's are (the playbook brings two-column
proofs in scope); Type 2's given is parallel sides, which a row must turn into
alternate interior angles. Type 3 is 17.3, a proof whose parts are numbers. Types 4
and 5 ask whether two triangles are similar: by their sides (SAS, SSS) or by their
angles (marked, or measured, the third angle found from 180°). A Type 4 or 5 pair is
not similar about one time in four, so the question is a real one; the book's pairs
are all similar.

The figures are drawn from the data, to scale. Types 1-2: the bowtie, its two
triangles really similar in the given correspondence (C A / C E = C B / C D when an
angle is given, C A / C D = C B / C E when the sides are parallel), the given angles
marked with arcs, parallel sides with arrowheads. Types 3-5: the two triangles side
by side at one scale, the second one mirrored (pose 1) as the book draws 17.3; sides
and angles labeled, equal angles marked with matching arcs.

The key writes what the deck writes:
  1, 2  the deck's rows: the given; the vertical angles at the crossing ("Vertical angles
        are congruent"); for Type 2 the alternate interior angles at the first point of
        the given's first segment; the last pair of angles, "AA -> AAA"; the similarity,
        "AAA". Each pair of angles is written the first triangle's angle first.
  3     the deck's rows: the angles, "Both angles measure 30°"; the two ratios, "Given";
        their equality, "12/8 = 3/2 = 15/10"; "SAS similarity postulate".
  4, 5  "Similar by SAS: triangle ABC ~ triangle XYZ, ratio 2 : 1" (the first triangle's
        letters in order, the ratio first triangle to second, in lowest terms); "Similar
        by AA -> AAA: triangle PQR ~ triangle STU" with no ratio (no sides given); for
        measured angles the missing angles first: "angle B = 38°, angle F = 115°; similar
        by AAA: triangle ABC ~ triangle DEF"; or "Not similar".

check() works from the data, not from the build. Types 1-2: a proof checker, as
Lesson 15's: each row must follow from the givens and the rows above it (vertical
angles must be at the crossing with opposite rays; alternate interior angles must come
from a stated parallel; AA -> AAA needs the other two pairs; AAA needs all three and
the triangles really similar in the drawing in the row's order); the last row is the
goal and every given is listed. Type 3: each row read against the data (the angle
measures, the side lengths, the ratios equal, the postulate's angle between the two
sides). Types 4-5: every correspondence of the two triangles is tried against the data;
the answer must name a correspondence that works, by a postulate the data supports, with
the right ratio, or say "not similar" when none works.

Skipped sources: the lesson's proofs of the Pythagorean theorem (theorem proofs; the
types file lists none as an example or problem).

A problem: dict(type, prompt, answer, source).
    1  "bowtie A B C D E; angle A = angle E; show triangle A B C ~ triangle E D C"
    2  "bowtie A B C D E; A B par E D; show triangle A B C ~ triangle D E C"
    3  "sas G H I 30 12 15; J K L 30 8 10; pose 1"     each: the angle's vertex, then two
                                                        sides from it (G H = 12, G I = 15)
    4  "sas B C A 6 4; Y Z X 3 2"                       the angles at B and Y marked equal
       "sss G H I 2 2 2; J K L 3 3 3"                   G H, H I, I G
    5  "marks P Q R S T U; Q T, R U"                    angle Q = angle T, angle R = angle U marked
       "angles A B C D E F; A 27, C 115; E 38, D 27"
"""
import itertools, math, re
from fractions import Fraction as F
from .. import gen
from ..gen import need
from . import lesson_figures as fig
from . import adv_lesson_9 as L9
from . import adv_lesson_15 as L15

NAME = FAMILY = "adv_lesson_17"
FIXED = False
TITLE = "Lesson 17: Proofs of the Pythagorean Theorem, Proofs of Similarity"
INSTRUCTIONS = ""
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

DETERMINE = "Determine whether the triangles are similar, and justify your answer. Write the ratio of corresponding sides when possible."
TYPES = [
    dict(key="1", title="Proving Similarity: An Angle Given", instructions="Write a two-column proof.",
         look="Two triangles that meet at a point (segments crossing), and a pair of angles marked congruent.",
         move="List the given. The angles where the segments cross are vertical angles, so they are congruent. Two "
              "pairs of angles congruent make the third pair congruent ($A A arrow A A A$), and the triangles are "
              "similar by $A A A$.", width="full", space="2.4in"),
    dict(key="2", title="Proving Similarity: Parallel Sides Given", instructions="Write a two-column proof.",
         look="Two triangles that meet at a point, and two of their sides given parallel (arrowheads).",
         move="List the given, then the vertical angles. The crossing segments are transversals of the parallels, "
              "so alternate interior angles are congruent: $angle A tilde.equiv angle D$. Then $A A arrow A A A$ "
              "and $A A A$.", width="full", space="2.6in"),
    dict(key="3", title="Proving Similarity by SAS, from Numbers", instructions="Write a two-column proof.",
         look="Two triangles with an equal angle given in degrees and the two sides that form it.",
         move="The angles are equal (both measure the same). Write the ratios of the sides that form them: "
              "$(G H)/(J K) = 12/8$ and $(G I)/(J L) = 15/10$. They are equal ($3/2$), so the triangles are "
              "similar by the SAS similarity postulate.", width="full", space="2.2in"),
    dict(key="4", title="Similar Triangles? From the Sides", instructions=DETERMINE,
         look="Two triangles with side lengths given: two sides and the angle between them marked equal, or all "
              "three sides.",
         move="Match the sides in order of size and divide. Three equal ratios: SSS. The sides around equal angles "
              "in equal ratios: SAS. The ratio of corresponding sides is the common ratio: $6/3 = 4/2 = 2$, so "
              "$2 : 1$. Unequal ratios: not similar.", width="full", space="1.2in"),
    dict(key="5", title="Similar Triangles? From the Angles", instructions=DETERMINE,
         look="Two triangles with angles marked congruent, or with angles given in degrees.",
         move="Find each missing angle: the angles of a triangle sum to $180 degree$. Two pairs of equal angles "
              "make the third pair equal ($A A arrow A A A$). With no sides given there is no ratio to write.",
         width="full", space="1.2in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

PROOFS = ("1", "2")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], re.sub(r"; pose \d+$", "", p["prompt"]))

# ------------------------------------------------------------------
# Types 1-2: the bowtie, and its proofs
# ------------------------------------------------------------------
BOW_CHAINS = ((0, 2, 3), (1, 2, 4), (0, 1), (3, 4))      # A C D and B C E straight, sides A B and D E
CA, CB, K = 1.6, 1.15, 1.3

def bow_layout(kind):
    """A (0) lower left, B (1) upper left, C (2) the crossing, D (3) upper right, E (4) lower right.
    kind "anti": triangle ABC ~ triangle EDC (angle A = angle E); "par": A B parallel to D E."""
    u1 = (math.cos(math.radians(24)), math.sin(math.radians(24)))      # A to D
    u2 = (math.cos(math.radians(-36)), math.sin(math.radians(-36)))    # B to E
    d, e = (K * CB, K * CA) if kind == "anti" else (K * CA, K * CB)
    return [(-CA * u1[0], -CA * u1[1]), (-CB * u2[0], -CB * u2[1]), (0.0, 0.0),
            (d * u1[0], d * u1[1]), (e * u2[0], e * u2[1])]

class Bowtie(L9.Figure):
    def __init__(self, names, kind):
        if len(names) != 5 or len(set(names)) != 5:
            raise ValueError("name the bowtie's 5 points with different letters")
        self.family, self.names = "bowtie", tuple(names)
        self.chains = [tuple(names[i] for i in c) for c in BOW_CHAINS]
        self.pts = dict(zip(self.names, bow_layout(kind)))
        self._rays, self._tris, self._ang = {}, None, {}

    def chain(self, a, b):
        if a == b or a not in self.names or b not in self.names:
            return None
        for c in self.chains:
            if a in c and b in c:
                return c
        return None

def similar_drawn(F_, t1, t2):
    """The correspondence is a similarity in the figure as drawn."""
    pairs = [(F_.length(t1[i], t1[j]), F_.length(t2[i], t2[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
    r = pairs[0][0] / pairs[0][1]
    return all(abs(a / b - r) < 1e-9 for a, b in pairs)

def parse_fact(s):
    """Lesson 15's facts; "triangle A B C ~ triangle E D C" is a similarity ("tri")."""
    return L15.parse_fact(" ".join(s.split()).replace(" ~ ", " = "))

def fact_text(f):
    return L15.fact_text(f).replace(" = triangle", " ~ triangle") if f[0] == "tri" else L15.fact_text(f)

def read_bow(prompt):
    s = " ".join(prompt.split())
    parts = [x.strip() for x in s.split(";")]
    if len(parts) != 3 or not parts[2].startswith("show "):
        raise ValueError("write it like: bowtie A B C D E; angle A = angle E; show triangle A B C ~ triangle E D C")
    head = parts[0].split()
    if head[0] != "bowtie":
        raise ValueError("start with bowtie")
    givens = [parse_fact(x) for x in L9.split_facts(parts[1])]
    if len(givens) != 1 or givens[0][0] not in ("ang", "par"):
        raise ValueError("one given: a pair of angles or two parallel sides")
    F_ = Bowtie(head[1:], "par" if givens[0][0] == "par" else "anti")
    g = givens[0]
    if g[0] == "par":
        L15.alternate(F_, g)                                # raises if not parallel in the drawing
    else:
        a, b = L9.item(F_, g[1], "ang"), L9.item(F_, g[2], "ang")
        if abs(L15.abs_angle(F_, a[1], *F_.ray_points(a)) - L15.abs_angle(F_, b[1], *F_.ray_points(b))) > 1e-6:
            raise ValueError("those angles aren't equal in this figure")
    goal = parse_fact(parts[2][5:])
    if goal[0] != "tri" or not (F_.is_triangle(goal[1]) and F_.is_triangle(goal[2])):
        raise ValueError("show two triangles of the figure similar")
    if not similar_drawn(F_, goal[1], goal[2]):
        raise ValueError("those triangles aren't similar in that order")
    return F_, givens, goal

def crossing(F_):
    return F_.names[2]

def angle_at(F_, t, v):
    """An angle of triangle t at v, as the deck names it: one letter where v has two rays,
    else the other two vertices in the triangle's order around v."""
    if len(F_.rays(v)) == 2:
        return (v,)
    o = [x for x in t if x != v]
    return (o[0], v, o[1])

def bow_rows(F_, givens, goal):
    """The deck's rows: [(fact, code)]."""
    g = givens[0]
    t1, t2 = tuple(goal[1]), tuple(goal[2])
    m = dict(zip(t1, t2))
    x = crossing(F_)
    rows = [(g, "given"), (("ang", angle_at(F_, t1, x), angle_at(F_, t2, x)), "vertical")]
    done = {x}
    if g[0] == "par":
        first = g[1][0]                                    # the alternate interior angles at the given's first point
        v1 = first if first in t1 else next(k for k, v in m.items() if v == first)
        rows.append((("ang", angle_at(F_, t1, v1), angle_at(F_, t2, m[v1])), "parallel"))
        done.add(v1)
    else:
        a = g[1][-1] if len(g[1]) == 3 else g[1][0]
        done.add(a if a in t1 else next(k for k, v in m.items() if v == a))
    (v,) = [y for y in t1 if y not in done]
    rows.append((("ang", angle_at(F_, t1, v), angle_at(F_, t2, m[v])), "third"))
    rows.append((goal, "AAA"))
    return rows

def rows_text(rows):
    return "; ".join(f"{fact_text(f)} | {c}" for f, c in rows)

BOW_ROW = re.compile(r"(.+?) \| (given|vertical|parallel|third|AAA)")

def check_bow(prompt, answer):
    F_, givens, goal = read_bow(prompt)
    rows = [BOW_ROW.fullmatch(" ".join(x.split())) for x in answer.split(";")]
    if not rows or not all(rows):
        return False
    E = L15.Equal()
    stated, last = [], None
    known = lambda a, b: E.eq(a, b)
    pair = lambda f: (L9.item(F_, f[1], f[0]), L9.item(F_, f[2], f[0]))
    for m in rows:
        f, code = parse_fact(m.group(1)), m.group(2)
        if code == "given":
            if not any(L15.same_fact(F_, f, g) for g in givens):
                return False
            stated.append(f)
            if f[0] == "ang":
                E.union(*pair(f))
        elif code == "vertical":
            if f[0] != "ang" or not vertical(F_, *pair(f)):
                return False
            E.union(*pair(f))
        elif code == "parallel":
            if f[0] != "ang" or not any(set(pq) == set(pair(f)) for g in stated if g[0] == "par"
                                        for pq, _ in L15.alternate(F_, g)):
                return False
            E.union(*pair(f))
        elif code == "third":
            if f[0] != "ang" or not L15.third_ok(F_, pair(f), known):
                return False
            E.union(*pair(f))
        else:                                              # AAA
            t1, t2 = f[1], f[2]
            if f[0] != "tri" or not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
                return False
            if not similar_drawn(F_, t1, t2):
                return False
            _, A = L9.parts(F_, t1, t2)
            if not all(known(*a) for a in A):
                return False
        last = f
    every = all(any(L15.same_fact(F_, g, s) for s in stated) for g in givens)
    return every and last is not None and L15.same_fact(F_, last, goal)

def vertical(F_, a, b):
    """Two angles at the same point whose rays point opposite ways."""
    if a == b or a[1] != b[1]:
        return False
    da, db = sorted(a[2]), sorted(b[2])
    opp = lambda u, w: abs(abs(u - w) - 180) < 1e-6
    return (opp(da[0], db[0]) and opp(da[1], db[1])) or (opp(da[0], db[1]) and opp(da[1], db[0]))

# the givens and goals in role letters; the letters: a run in order, or problem 8's (A E D C B)
BOW_GIVENS = {"1": ["angle {0} = angle {4}", "angle {1} = angle {3}"],
              "2": ["{0} {1} par {4} {3}", "{4} {3} par {0} {1}"]}
BOW_GOALS = {"1": ["triangle {0} {1} {2} ~ triangle {4} {3} {2}", "triangle {0} {2} {1} ~ triangle {4} {2} {3}"],
             "2": ["triangle {0} {1} {2} ~ triangle {3} {4} {2}", "triangle {0} {2} {1} ~ triangle {3} {2} {4}"]}
ALPHA = L9.ALPHA
LETTERINGS = ("run", "problem 8")

def bow_names(start, lettering):
    r = ALPHA[start:start + 5]
    return tuple(r) if lettering == "run" else (r[0], r[4], r[3], r[2], r[1])

def bow_ok(kind, start, lettering, given, goal):
    return (kind in PROOFS and start in range(len(ALPHA) - 4) and lettering in LETTERINGS
            and given in range(2) and goal in range(2))

def bow_pick(kind):
    def pick(r):
        return dict(kind=kind, start=r.randrange(len(ALPHA) - 4), lettering=r.choice(LETTERINGS),
                    given=r.randrange(2), goal=r.randrange(2))
    return pick

def bow_build(kind, start, lettering, given, goal):     # 17.1, 17.2, problem 8
    need(bow_ok(kind, start, lettering, given, goal))
    n = bow_names(start, lettering)
    return f"bowtie {' '.join(n)}; {BOW_GIVENS[kind][given].format(*n)}; show {BOW_GOALS[kind][goal].format(*n)}"

# ------------------------------------------------------------------
# Types 3-5: two triangles side by side
# ------------------------------------------------------------------
TRI = re.compile(r"([A-Z]) ([A-Z]) ([A-Z])((?: \d+)*)")

def read_pair(prompt):
    """(kind, t1, t2, data1, data2, pose): kind sas, sss, marks, or angles."""
    s = " ".join(prompt.split())
    pose = 0
    m = re.search(r";\s*pose\s+(\d)$", s)
    if m:
        pose, s = int(m.group(1)), s[:m.start()]
    kind, _, rest = s.partition(" ")
    if kind == "marks":
        m = re.fullmatch(r"([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]); ([A-Z]) ([A-Z]), ([A-Z]) ([A-Z])", rest)
        if not m:
            raise ValueError("write it like: marks P Q R S T U; Q T, R U")
        g = m.groups()
        t1, t2 = g[:3], g[3:6]
        pairs = [(g[6], g[7]), (g[8], g[9])]
        if not all(a in t1 and b in t2 for a, b in pairs) or pairs[0][0] == pairs[1][0] or pairs[0][1] == pairs[1][1]:
            raise ValueError("each pair: an angle of the first triangle, then one of the second")
        if len(set(t1 + t2)) != 6:
            raise ValueError("six different letters")
        return kind, t1, t2, pairs, None, pose
    if kind == "angles":
        m = re.fullmatch(r"([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]) ([A-Z]); ([A-Z]) (\d+), ([A-Z]) (\d+); "
                         r"([A-Z]) (\d+), ([A-Z]) (\d+)", rest)
        if not m:
            raise ValueError("write it like: angles A B C D E F; A 27, C 115; E 38, D 27")
        g = m.groups()
        t1, t2 = g[:3], g[3:6]
        a1, a2 = {g[6]: int(g[7]), g[8]: int(g[9])}, {g[10]: int(g[11]), g[12]: int(g[13])}
        if len(a1) != 2 or len(a2) != 2 or not set(a1) <= set(t1) or not set(a2) <= set(t2) or len(set(t1 + t2)) != 6:
            raise ValueError("two angles of each triangle")
        for t, a in ((t1, a1), (t2, a2)):
            if sum(a.values()) >= 180 or min(a.values()) <= 0:
                raise ValueError("a triangle's angles sum to 180")
            (v,) = [x for x in t if x not in a]
            a[v] = 180 - sum(a.values())
        return kind, t1, t2, a1, a2, pose
    if kind not in ("sas", "sss"):
        raise ValueError("start with sas, sss, marks, or angles")
    halves = [TRI.fullmatch(h.strip()) for h in rest.split(";")]
    if len(halves) != 2 or not all(halves):
        raise ValueError("write it like: sas B C A 6 4; Y Z X 3 2")
    t1, t2 = halves[0].groups()[:3], halves[1].groups()[:3]
    d1, d2 = ([int(x) for x in h.group(4).split()] for h in halves)
    want = {"sas": (2, 3), "sss": (3,)}[kind]
    if len(d1) not in want or len(d1) != len(d2) or len(set(t1 + t2)) != 6 or min(d1 + d2) <= 0:
        raise ValueError("the sides of each triangle")
    if kind == "sss":
        for d in (d1, d2):
            if 2 * max(d) >= sum(d):
                raise ValueError("those sides don't make a triangle")
    if kind == "sas" and len(d1) == 3:                     # with the angle in degrees (Type 3)
        if d1[0] != d2[0] or not 0 < d1[0] < 180:
            raise ValueError("the same angle in both")
    return kind, t1, t2, d1, d2, pose

def sides_of(kind, t, d):
    """{frozenset(pair): length} the data gives."""
    if kind == "sss":
        return {frozenset((t[0], t[1])): d[0], frozenset((t[1], t[2])): d[1], frozenset((t[2], t[0])): d[2]}
    s = d[-2:]
    return {frozenset((t[0], t[1])): s[0], frozenset((t[0], t[2])): s[1]}

def angles_of(kind, t, d):
    """{vertex: degrees} the data gives (None: marked equal, no measure)."""
    if kind == "angles":
        return dict(d)
    if kind == "sas" and len(d) == 3:
        return {t[0]: d[0]}
    return {}

def correspondences(t1, t2):
    for p in itertools.permutations(t2):
        yield dict(zip(t1, p))

def similarity(prompt):
    """(postulate, mapping, ratio) of the data's similarity, or None: tried over every
    correspondence (SSS, then SAS, then AA -> AAA, then AAA)."""
    kind, t1, t2, d1, d2, _ = read_pair(prompt)
    for m in correspondences(t1, t2):
        if kind == "sss":
            s1, s2 = sides_of(kind, t1, d1), sides_of(kind, t2, d2)
            ratios = {F(s1[k], s2[frozenset(m[x] for x in k)]) for k in s1}
            if len(ratios) == 1:
                return "SSS", m, ratios.pop()
        elif kind == "sas":
            if m[t1[0]] != t2[0]:
                continue                                    # the marked (or measured) angles correspond
            s1, s2 = sides_of(kind, t1, d1), sides_of(kind, t2, d2)
            ratios = {F(s1[k], s2[frozenset(m[x] for x in k)]) for k in s1}
            if len(ratios) == 1:
                return "SAS", m, ratios.pop()
        elif kind == "marks":
            if all(m[a] == b for a, b in d1):
                return "AA", m, None
        else:
            if all(d1[v] == d2[m[v]] for v in t1):
                return "AAA", m, None
    return None

def ordered(t1, m):
    a = tuple(sorted(t1))
    return a, tuple(m[x] for x in a)

def ratio_text(r):
    return f"{r.numerator} : {r.denominator}"

def missing(prompt):
    """Type 5's measured angles: the angle found in each triangle, "angle B = 38, angle F = 115"."""
    kind, t1, t2, a1, a2, _ = read_pair(prompt)
    if kind != "angles":
        return ""
    found = []
    for t, a, given in ((t1, a1, prompt.split(";")[1]), (t2, a2, prompt.split(";")[2])):
        (v,) = [x for x in t if f"{x} " not in given + " "]
        found.append(f"angle {v} = {a[v]}")
    return ", ".join(found)

def pair_answer(prompt):
    found = similarity(prompt)
    lead = missing(prompt)
    if found is None:
        return f"{lead}; not similar" if lead else "not similar"
    post, m, r = found
    a, b = ordered(next(iter([read_pair(prompt)[1]])), m)
    out = f"similar; {post}; triangle {' '.join(a)} ~ triangle {' '.join(b)}"
    if r is not None:
        out += f"; {ratio_text(r)}"
    return f"{lead}; {out}" if lead else out

def check_pair(prompt, answer):
    """The answer's claim against every correspondence of the data."""
    kind, t1, t2, d1, d2, _ = read_pair(prompt)
    parts = [x.strip() for x in " ".join(answer.split()).split(";")]
    lead = missing(prompt)
    if lead:
        if not parts or parts[0] != lead:
            return False
        parts = parts[1:]
    found = similarity(prompt)
    if parts == ["not similar"]:
        return found is None
    if found is None or len(parts) < 3 or parts[0] != "similar":
        return False
    post = parts[1]
    m = re.fullmatch(r"triangle ([A-Z]) ([A-Z]) ([A-Z]) ~ triangle ([A-Z]) ([A-Z]) ([A-Z])", parts[2])
    if not m or post not in ("SSS", "SAS", "AA", "AAA"):
        return False
    a, b = m.groups()[:3], m.groups()[3:]
    if set(a) != set(t1) or set(b) != set(t2):
        return False
    corr = dict(zip(a, b))
    ok = {"SSS": kind == "sss", "SAS": kind == "sas", "AA": kind == "marks", "AAA": kind == "angles"}[post]
    if not ok:
        return False
    if kind in ("sss", "sas"):
        s1, s2 = sides_of(kind, t1, d1), sides_of(kind, t2, d2)
        if kind == "sas" and corr[t1[0]] != t2[0]:
            return False
        ratios = {F(s1[k], s2[frozenset(corr[x] for x in k)]) for k in s1}
        if len(ratios) != 1 or len(parts) != 4:
            return False
        r = ratios.pop()
        return parts[3] == ratio_text(r)
    if len(parts) != 3:
        return False
    if kind == "marks":
        return all(corr[x] == y for x, y in d1)
    return all(d1[v] == d2[corr[v]] for v in t1)

# Type 3's rows: the SAS similarity proof
def sas_rows(prompt):
    kind, t1, t2, d1, d2, _ = read_pair(prompt)
    if kind != "sas" or len(d1) != 3:
        raise ValueError("an angle and two sides of each triangle")
    found = similarity(prompt)
    if found is None:
        raise ValueError("these triangles aren't similar")
    _, m, r = found
    v1, p1, q1 = t1
    v2, p2, q2 = t2
    s1, s2 = sides_of(kind, t1, d1), sides_of(kind, t2, d2)
    rp = (f"{v1} {p1}/{m[v1]} {m[p1]}", s1[frozenset((v1, p1))], s2[frozenset((m[v1], m[p1]))])
    rq = (f"{v1} {q1}/{m[v1]} {m[q1]}", s1[frozenset((v1, q1))], s2[frozenset((m[v1], m[q1]))])
    a, b = ordered(t1, m)
    return [f"angle {v1} = angle {m[v1]} | measure {d1[0]}",
            f"{rp[0]} = {rp[1]}/{rp[2]} | given",
            f"{rq[0]} = {rq[1]}/{rq[2]} | given",
            f"{rp[0]} = {rq[0]} | {rp[1]}/{rp[2]} = {r.numerator}/{r.denominator} = {rq[1]}/{rq[2]}",
            f"triangle {' '.join(a)} ~ triangle {' '.join(b)} | SAS"]

SAS_ROWS = [re.compile(r"angle ([A-Z]) = angle ([A-Z]) \| measure (\d+)"),
            re.compile(r"([A-Z]) ([A-Z])/([A-Z]) ([A-Z]) = (\d+)/(\d+) \| given"),
            re.compile(r"([A-Z]) ([A-Z])/([A-Z]) ([A-Z]) = (\d+)/(\d+) \| given"),
            re.compile(r"([A-Z]) ([A-Z])/([A-Z]) ([A-Z]) = ([A-Z]) ([A-Z])/([A-Z]) ([A-Z]) \| (\d+)/(\d+) = (\d+)/(\d+) = (\d+)/(\d+)"),
            re.compile(r"triangle ([A-Z]) ([A-Z]) ([A-Z]) ~ triangle ([A-Z]) ([A-Z]) ([A-Z]) \| SAS")]

def check_sas(prompt, answer):
    kind, t1, t2, d1, d2, _ = read_pair(prompt)
    if kind != "sas" or len(d1) != 3:
        return False
    rows = [x.strip() for x in " ".join(answer.split()).split(";")]
    if len(rows) != 5:
        return False
    ms = [rx.fullmatch(r) for rx, r in zip(SAS_ROWS, rows)]
    if not all(ms):
        return False
    s1, s2 = sides_of(kind, t1, d1), sides_of(kind, t2, d2)
    v1, v2, deg = ms[0].group(1), ms[0].group(2), int(ms[0].group(3))
    if not (v1 == t1[0] and v2 == t2[0] and deg == d1[0] == d2[0]):
        return False                                       # the angles the data measures
    ratios = []
    for mm in ms[1:3]:
        a, b, c, d, n, k = mm.groups()
        if {a, b} not in ({t1[0], t1[1]}, {t1[0], t1[2]}) or a != v1 or c != v2 or {c, d} not in (
                {t2[0], t2[1]}, {t2[0], t2[2]}):
            return False                                   # sides that form the angle
        if s1[frozenset((a, b))] != int(n) or s2[frozenset((c, d))] != int(k):
            return False
        ratios.append(((a, b, c, d), F(int(n), int(k))))
    if ratios[0][0][1] == ratios[1][0][1] or ratios[0][1] != ratios[1][1]:
        return False                                       # two different sides, in equal ratios
    g = ms[3].groups()
    if (g[:4], g[4:8]) != (ratios[0][0], ratios[1][0]):
        return False
    r = ratios[0][1]
    if F(int(g[8]), int(g[9])) != r or (int(g[10]), int(g[11])) != (r.numerator, r.denominator) \
            or F(int(g[12]), int(g[13])) != r:
        return False
    corr = {v1: v2, ratios[0][0][1]: ratios[0][0][3], ratios[1][0][1]: ratios[1][0][3]}
    a, b = ms[4].groups()[:3], ms[4].groups()[3:]
    return set(a) == set(t1) and set(b) == set(t2) and all(corr[x] == y for x, y in zip(a, b))

# --- the templates of Types 3-5
POSES = range(2)
ANGLE3 = range(25, 80, 5)                                 # a labeled angle has room for its label
SIDE = range(2, 13)                                        # the smaller triangle's sides

def shapely(*sides):
    """No sliver: the given sides within a factor of 2 of each other."""
    return max(sides) <= 2 * min(sides)
RATIOS = (F(3, 2), F(2), F(4, 3), F(5, 2), F(5, 3), F(2, 3), F(1, 2), F(3, 4))
BIGGEST = 20

ALPHA3 = "ABCDEFGHIJKLMNPQRSTUVWXYZ"                       # the side-by-side triangles' letters: G H I (17.3), no O
STARTS = range(len(ALPHA3) - 2)

def trio(start):
    return tuple(ALPHA3[start:start + 3])

def t3_ok(n1, n2, deg, p2, q2, r, pose):
    if not (n1 in STARTS and n2 in STARTS and abs(n1 - n2) >= 3 and deg in ANGLE3
            and p2 in SIDE and q2 in SIDE and p2 != q2 and shapely(p2, q2) and r in RATIOS and pose in POSES):
        return False
    p1, q1 = r * p2, r * q2
    return p1.denominator == 1 and q1.denominator == 1 and max(p1, q1) <= BIGGEST and min(p1, q1) >= 2

def t3_pick(r):
    return dict(n1=r.choice(STARTS), n2=r.choice(STARTS), deg=r.choice(ANGLE3), p2=r.choice(SIDE), q2=r.choice(SIDE),
                r=r.choice(RATIOS), pose=r.choice(POSES))

def t3(n1, n2, deg, p2, q2, r, pose):                     # 17.3: sas G H I 30 12 15; J K L 30 8 10; pose 1
    need(t3_ok(n1, n2, deg, p2, q2, r, pose))
    a, b = trio(n1), trio(n2)
    return f"sas {' '.join(a)} {deg} {r * p2} {r * q2}; {' '.join(b)} {deg} {p2} {q2}; pose {pose}"

def roll(t, k):
    """The letters with a different one first: (A B C, 1) -> B C A, the angle's vertex first."""
    return t[k:] + t[:k]

def t4_sas_ok(n1, n2, k1, k2, p2, q2, r, similar, pose):
    if not (n1 in STARTS and n2 in STARTS and abs(n1 - n2) >= 3 and k1 in range(3)
            and k2 in range(3) and p2 in SIDE and q2 in SIDE and p2 != q2 and shapely(p2, q2) and r in RATIOS
            and similar in (0, 1) and pose in POSES):
        return False
    p1, q1 = r * p2, (r * q2 if similar else r * q2 + 1)
    return (p1.denominator == 1 and q1.denominator == 1 and max(p1, q1) <= BIGGEST and min(p1, q1) >= 2
            and shapely(p1, q1))

def t4_sas_pick(r):
    return dict(n1=r.choice(STARTS), n2=r.choice(STARTS), k1=r.randrange(3), k2=r.randrange(3),
                p2=r.choice(SIDE), q2=r.choice(SIDE), r=r.choice(RATIOS), similar=int(r.random() < 0.75),
                pose=r.choice(POSES))

def t4_sas(n1, n2, k1, k2, p2, q2, r, similar, pose):    # problem 4: sas B C A 6 4; Y Z X 3 2
    need(t4_sas_ok(n1, n2, k1, k2, p2, q2, r, similar, pose))
    a, b = roll(trio(n1), k1), roll(trio(n2), k2)
    q1 = r * q2 if similar else r * q2 + 1
    return f"sas {' '.join(a)} {r * p2} {q1}; {' '.join(b)} {p2} {q2}; pose {pose}"

def t4_sss_ok(n1, n2, s, r, similar, pose):
    if not (n1 in STARTS and n2 in STARTS and abs(n1 - n2) >= 3 and len(s) == 3
            and all(x in SIDE for x in s) and 2 * max(s) < sum(s) and r in RATIOS and similar in (0, 1)
            and pose in POSES):
        return False
    big = [r * x for x in s]
    if not similar:
        big[2] += 1
    return all(x.denominator == 1 for x in big) and max(big) <= BIGGEST and 2 * max(big) < sum(big)

def t4_sss_pick(r):
    return dict(n1=r.choice(STARTS), n2=r.choice(STARTS),
                s=tuple(r.choice(SIDE) for _ in range(3)) if r.random() < 0.8 else (r.choice(SIDE),) * 3,
                r=r.choice(RATIOS), similar=int(r.random() < 0.75), pose=r.choice(POSES))

def t4_sss(n1, n2, s, r, similar, pose):                 # problem 5: sss G H I 2 2 2; J K L 3 3 3
    need(t4_sss_ok(n1, n2, s, r, similar, pose))
    big = [r * x for x in s]
    if not similar:
        big[2] += 1
    return f"sss {' '.join(trio(n1))} {' '.join(str(x) for x in big)}; {' '.join(trio(n2))} {' '.join(map(str, s))}; pose {pose}"

def t5_marks_ok(n1, n2, i, j, pose):
    return (n1 in STARTS and n2 in STARTS and abs(n1 - n2) >= 3 and i in range(3)
            and j in range(3) and i != j and pose in POSES)

def t5_marks_pick(r):
    i, j = r.sample(range(3), 2)
    return dict(n1=r.choice(STARTS), n2=r.choice(STARTS), i=i, j=j, pose=r.choice(POSES))

def t5_marks(n1, n2, i, j, pose):                         # problem 6: marks P Q R S T U; Q T, R U
    need(t5_marks_ok(n1, n2, i, j, pose))
    a, b = trio(n1), trio(n2)
    return f"marks {' '.join(a)} {' '.join(b)}; {a[i]} {b[i]}, {a[j]} {b[j]}; pose {pose}"

ANGLE5 = range(25, 126)

def t5_angles_ok(n1, n2, A, B, i1, j1, i2, j2, shift, pose):
    C = 180 - A - B
    if not (n1 in STARTS and n2 in STARTS and abs(n1 - n2) >= 3 and A in ANGLE5
            and B in ANGLE5 and C in ANGLE5 and len({A, B, C}) == 3 and i1 != j1 and i2 != j2
            and {i1, j1, i2, j2} <= {0, 1, 2} and shift in (0, 5, 10, -5, -10) and pose in POSES):
        return False
    if shift:
        b2 = shifted(A, B, shift)
        return b2 is not None and i2 != j2
    return True

def shifted(A, B, shift):
    """The second triangle's angles, not similar: B moved by shift, C taking the rest."""
    angs = [A, B + shift, 180 - A - B - shift]
    return angs if all(a in ANGLE5 for a in angs) and len(set(angs)) == 3 else None

def t5_angles_pick(r):
    i1, j1 = r.sample(range(3), 2)
    i2, j2 = r.sample(range(3), 2)
    return dict(n1=r.choice(STARTS), n2=r.choice(STARTS), A=r.choice(ANGLE5), B=r.choice(ANGLE5),
                i1=i1, j1=j1, i2=i2, j2=j2, shift=0 if r.random() < 0.75 else r.choice((5, 10, -5, -10)),
                pose=r.choice(POSES))

def t5_angles(n1, n2, A, B, i1, j1, i2, j2, shift, pose):   # problem 7: angles A B C D E F; A 27, C 115; E 38, D 27
    """The first triangle's angles A, B, 180 - A - B at its vertices in order; the second's the same
    (shift 0) or not; each lists two of its angles (i, j)."""
    need(t5_angles_ok(n1, n2, A, B, i1, j1, i2, j2, shift, pose))
    a, b = trio(n1), trio(n2)
    first = [A, B, 180 - A - B]
    second = shifted(A, B, shift) if shift else first
    return (f"angles {' '.join(a)} {' '.join(b)}; {a[i1]} {first[i1]}, {a[j1]} {first[j1]}; "
            f"{b[i2]} {second[i2]}, {b[j2]} {second[j2]}; pose {pose}")

# ------------------------------------------------------------------
# All the templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(bow_pick("1"), bow_build)],
    "2": [(bow_pick("2"), bow_build)],
    "3": [(t3_pick, t3)],
    "4": [(t4_sas_pick, t4_sas), (t4_sss_pick, t4_sss)],
    "5": [(t5_marks_pick, t5_marks), (t5_angles_pick, t5_angles), (t5_angles_pick, t5_angles)],
}
RANGES = {bow_build: bow_ok, t3: t3_ok, t4_sas: t4_sas_ok, t4_sss: t4_sss_ok, t5_marks: t5_marks_ok,
          t5_angles: t5_angles_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def kind_of(prompt):
    k = " ".join(prompt.split()).split(" ", 1)[0]
    if k == "bowtie":
        return "2" if " par " in prompt else "1"
    if k == "sas" and len(read_pair(prompt)[3]) == 3:
        return "3"
    return {"sas": "4", "sss": "4", "marks": "5", "angles": "5"}.get(k)

def answer_of(prompt):
    typ = kind_of(prompt)
    if typ in PROOFS:
        return rows_text(bow_rows(*read_bow(prompt)))
    if typ == "3":
        return "; ".join(sas_rows(prompt))
    if typ is None:
        raise ValueError("start with bowtie, sas, sss, marks, or angles")
    return pair_answer(prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    need(kind_of(prompt) == entry)
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        if kind_of(p["prompt"]) != p["type"]:
            return "failed"
        if p["type"] in PROOFS:
            ok = check_bow(p["prompt"], p["answer"])
        elif p["type"] == "3":
            ok = check_sas(p["prompt"], p["answer"])
        else:
            ok = check_pair(p["prompt"], p["answer"])
    except (ValueError, KeyError, AttributeError, TypeError, IndexError, ZeroDivisionError):
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures
# ------------------------------------------------------------------
MARK_SHAPE = (112, 24)                                     # the drawn angles at a marks pair's first two vertices
SAS_ANGLE = 58                                             # a marked angle with no measure

def tri_points(kind, t, d):
    """The triangle's points {name: (x, y)}, its first vertex at the origin, its second along +x."""
    if kind == "sss":
        a, b, c = d                                        # t0 t1, t1 t2, t2 t0
        x = (a * a + c * c - b * b) / (2 * a)
        return {t[0]: (0.0, 0.0), t[1]: (float(a), 0.0), t[2]: (x, math.sqrt(max(c * c - x * x, 0.0)))}
    if kind == "sas":
        deg = d[0] if len(d) == 3 else SAS_ANGLE
        p, q = d[-2:]
        th = math.radians(deg)
        return {t[0]: (0.0, 0.0), t[1]: (float(p), 0.0), t[2]: (q * math.cos(th), q * math.sin(th))}
    angs = d                                               # {vertex: degrees}, all three
    A, B = math.radians(angs[t[0]]), math.radians(angs[t[1]])
    c = 1.0                                                # side t0 t1
    b = c * math.sin(B) / math.sin(A + B)                  # side t0 t2, across from t1
    return {t[0]: (0.0, 0.0), t[1]: (c, 0.0), t[2]: (b * math.cos(A), b * math.sin(A))}

def based(t, angs):
    """The vertices with the smallest angle and the largest along the base, as the book draws
    problem 7 (A and C, 27° and 115°), so an obtuse angle sits at a base corner."""
    lo, hi = min(t, key=lambda v: angs[v]), max(t, key=lambda v: angs[v])
    return (lo, hi, next(v for v in t if v not in (lo, hi)))

def pair_figure(prompt, unit="1cm"):
    kind, t1, t2, d1, d2, pose = read_pair(prompt)
    if kind == "marks":
        (a, b), (c, e) = d1
        third1 = next(x for x in t1 if x not in (a, c))
        angs = {a: MARK_SHAPE[0], c: MARK_SHAPE[1], third1: 180 - sum(MARK_SHAPE)}
        m = {a: b, c: e, third1: next(x for x in t2 if x not in (b, e))}
        p1 = tri_points("angles", based(t1, angs), angs)
        p2 = tri_points("angles", tuple(m[v] for v in based(t1, angs)), {m[v]: angs[v] for v in t1})
        p2 = {k: (1.15 * x, 1.15 * y) for k, (x, y) in p2.items()}
    elif kind == "angles":
        p1, p2 = tri_points(kind, based(t1, d1), d1), tri_points(kind, based(t2, d2), d2)
        p2 = {k: (1.25 * x, 1.25 * y) for k, (x, y) in p2.items()}
    else:
        p1, p2 = tri_points(kind, t1, d1), tri_points(kind, t2, d2)
    if pose:
        p2 = {k: (-x, y) for k, (x, y) in p2.items()}
    x1 = max(x for x, _ in p1.values())
    x2 = min(x for x, _ in p2.values())
    span = max(x for x, _ in p1.values()) - min(x for x, _ in p1.values())
    span2 = max(x for x, _ in p2.values()) - x2
    gap = x1 + 0.5 * max(span, span2) - x2                    # apart by half the wider one: no names touching
    pts = dict(p1)
    pts.update({k: (x + gap, y) for k, (x, y) in p2.items()})
    chains = [(t[i], t[(i + 1) % 3]) for t in (t1, t2) for i in range(3)]        # each side its own line
    sides, labels, arcs = [], [], []
    if kind in ("sas", "sss"):
        for t, d in ((t1, d1), (t2, d2)):
            for k, v in sides_of(kind, t, d).items():
                a, b = sorted(k)
                sides.append((a, b, f"${v}$"))
        if kind == "sas":
            for t, d in ((t1, d1), (t2, d2)):
                if len(d) == 3:
                    labels.append((t[0], t[1], t[2], f"${d[0]} degree$"))
                else:
                    arcs.append((t[0], t[1], t[2], 1))
    elif kind == "marks":
        for n, (a, b) in enumerate(d1):
            for v, t in ((a, t1), (b, t2)):
                o = [x for x in t if x != v]
                arcs.append((v, o[0], o[1], 2 - n))
    else:
        given1 = prompt.split(";")[1]
        given2 = prompt.split(";")[2]
        for t, d, given in ((t1, d1, given1), (t2, d2, given2)):
            for v in t:
                if f"{v} " in given:
                    o = [x for x in t if x != v]
                    labels.append((v, o[0], o[1], f"${d[v]} degree$"))
                    arcs.append((v, o[0], o[1], 1))
    return fig.marked(pts, chains, arcs=arcs, wide=9.5, tall=2.8, unit=unit, side_labels=sides, angle_labels=labels)

def bow_figure(prompt, unit="1cm"):
    F_, givens, _ = read_bow(prompt)
    g = givens[0]
    arcs, arrows = [], []
    if g[0] == "ang":
        for part in (g[1], g[2]):
            it = L9.item(F_, part, "ang")
            p, q = F_.ray_points(it)
            arcs.append((it[1], p, q, 1))
    else:
        for seg in (g[1], g[2]):
            a, b = seg
            if F_.vec(a, b)[1] < 0:
                a, b = b, a
            arrows.append((a, b, 1))
    return fig.marked(F_.pts, F_.chains, arcs=arcs, wide=4.0, tall=1.9, unit=unit, arrows=arrows)

def figure(p, unit="1cm"):
    return bow_figure(p["prompt"], unit) if p["type"] in PROOFS else pair_figure(p["prompt"], unit)

# ------------------------------------------------------------------
# Words
# ------------------------------------------------------------------
REASONS = {"given": "Given", "vertical": "Vertical angles are congruent",
           "parallel": "If two parallel lines are cut by a transversal, then each pair of alternate interior angles "
                       "is congruent",
           "third": "#emph[AA] → #emph[AAA]", "AAA": "#emph[AAA]"}

def tri_m(t):
    return f"triangle {' '.join(t)}"

def fact_typst(f):
    if f[0] == "tri":
        return f"${tri_m(f[1])} tilde {tri_m(f[2])}$"
    return L15.fact_typst(f)

def fact_plain(f):
    if f[0] == "tri":
        return f"△{''.join(f[1])} ~ △{''.join(f[2])}"
    return L15.fact_plain(f)

def statement(p, plain=False):
    typ = p["type"]
    if typ in PROOFS:
        _, givens, goal = read_bow(p["prompt"])
        show = fact_plain if plain else fact_typst
        return f"Given: {show(givens[0])}. Write a two-column proof to prove: {show(goal)}."
    kind, t1, t2, *_ = read_pair(p["prompt"])
    if typ == "3":
        a1 = tuple(sorted(t1))
        corr = similarity(p["prompt"])[1]
        b1 = tuple(corr[x] for x in a1)
        if plain:
            return f"Prove △{''.join(a1)} ~ △{''.join(b1)}."
        return f"Prove ${tri_m(a1)} tilde {tri_m(b1)}$."
    if kind == "angles":
        x, y = tuple(sorted(t1)), tuple(sorted(t2))
        if plain:
            return f"Determine if △{''.join(x)} ~ △{''.join(y)} and justify your answer."
        return f"Determine if ${tri_m(x)} tilde {tri_m(y)}$ and justify your answer."
    return ("Determine whether the pair of triangles shown is similar and justify your answer. Write the ratio "
            "of corresponding sides when possible.")

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except (ValueError, KeyError, TypeError):
        return p["prompt"]
    return f"{s} #v(0.4em) #align(center)[{f}]"

def proof_table(rows):
    cells = ["[#smallcaps[Statements]]", "[#smallcaps[Reasons]]"]
    for i, (st, rs) in enumerate(rows, 1):
        cells += [f"[{i}. {st}]", f"[{i}. {rs}]"]
    return ("#table(columns: (auto, 1fr), inset: (x: 0.5em, y: 0.3em), align: left, "
            "stroke: (x, y) => (left: if x == 1 { 0.6pt } else { none }, "
            f"bottom: if y == 0 or y == {len(rows)} {{ 0.6pt }} else {{ none }}), " + ", ".join(cells) + ")")

def sas_display(answer, plain=False):
    out = []
    for i, row in enumerate(answer.split(";")):
        st, _, rs = row.strip().partition(" | ")
        if i == 0:
            m = re.fullmatch(r"angle ([A-Z]) = angle ([A-Z])", st)
            deg = rs.split()[1]
            out.append((f"∠{m.group(1)} ≅ ∠{m.group(2)}" if plain else f"$angle {m.group(1)} tilde.equiv angle {m.group(2)}$",
                        f"Both angles measure {deg}°" if plain else f"Both angles measure ${deg} degree$"))
        elif i in (1, 2, 3):
            l, r = st.split(" = ")
            frac = lambda x: x.replace(" ", "") if plain else "(" + x.split("/")[0] + ")/(" + x.split("/")[1] + ")"
            why = "Given" if rs == "given" else (rs.replace(" ", "") if plain else "$" + rs.replace(" = ", " = ") + "$")
            out.append((f"{frac(l)} = {frac(r)}" if plain else f"${frac(l)} = {frac(r) if '/' in r else r}$", why))
        else:
            m = re.fullmatch(r"triangle (.+) ~ triangle (.+)", st)
            out.append((f"△{m.group(1).replace(' ', '')} ~ △{m.group(2).replace(' ', '')}" if plain
                        else f"$triangle {m.group(1)} tilde triangle {m.group(2)}$",
                        "SAS similarity postulate" if plain else "#emph[SAS] similarity postulate"))
    return out

def pair_display(answer, plain=False):
    parts = [x.strip() for x in answer.split(";")]
    lead = ""
    if parts[0].startswith("angle "):
        ang = [re.fullmatch(r"angle ([A-Z]) = (\d+)", x.strip()).groups() for x in parts[0].split(",")]
        lead = ", ".join(f"m∠{v} = {d}°" if plain else f"$m angle {v} = {d} degree$" for v, d in ang) + "; "
        parts = parts[1:]
    if parts == ["not similar"]:
        return lead + ("Not similar" if plain else "*Not similar*")
    post = {"AA": "AA → AAA"}.get(parts[1], parts[1])
    t = re.fullmatch(r"triangle (.+) ~ triangle (.+)", parts[2]).groups()
    tri = f"△{t[0].replace(' ', '')} ~ △{t[1].replace(' ', '')}" if plain else f"$triangle {t[0]} tilde triangle {t[1]}$"
    out = f"Similar by {post}: {tri}" if plain else f"*Similar* by #emph[{post}]: {tri}"
    if len(parts) == 4:
        out += f", ratio {parts[3]}" if plain else f", ratio ${parts[3].replace(':', 'colon')}$"
    elif parts[1] == "AA":
        out += " (no sides are given, so no ratio)"
    return lead + out

def answer_typst(p):
    try:
        if p["type"] in PROOFS:
            rows = [(fact_typst(parse_fact(st)), REASONS[c]) for st, c in
                    (r.strip().split(" | ") for r in p["answer"].split(";"))]
            return proof_table(rows)
        if p["type"] == "3":
            return proof_table(sas_display(p["answer"]))
        return pair_display(p["answer"])
    except (ValueError, AttributeError, KeyError, IndexError):
        return p["answer"]

SLIDE_UNIT = "1.6cm"

def slide_typst(p, key=False):
    try:
        f, s = figure(p, SLIDE_UNIT), statement(p)
    except (ValueError, KeyError, TypeError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    if p["type"] in ("3", "4", "5"):                       # the figure is wide: the words above it, the answer below
        return f"{s} #v(0.5em) #align(center)[{f}] #v(0.5em) #text(size: 0.8em)[{shown}]"
    return (f"#grid(columns: (1fr, auto), column-gutter: 1.2em, align: horizon, "
            f"[{s} #v(0.6em) #text(size: 0.8em)[{shown}]], [{f}])")

def text(p):
    try:
        return statement(p, plain=True) + "   [figure: " + p["prompt"] + "]"
    except (ValueError, KeyError, TypeError):
        return p["prompt"]

def answer_text(p):
    try:
        if p["type"] in PROOFS:
            plain_r = {k: re.sub(r"#emph\[(\w+)\]", r"\1", v) for k, v in REASONS.items()}
            return "\n".join(f"{i}. {fact_plain(parse_fact(st))}   {plain_r[c]}" for i, (st, c) in
                             enumerate((r.strip().split(" | ") for r in p["answer"].split(";")), 1))
        if p["type"] == "3":
            return "\n".join(f"{i}. {a}   {b}" for i, (a, b) in enumerate(sas_display(p["answer"], True), 1))
        return pair_display(p["answer"], True)
    except (ValueError, AttributeError, KeyError, IndexError):
        return p["answer"]

def height(p):
    return 2.4

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {"1": "bowtie A B C D E; angle A = angle E; show triangle A B C ~ triangle E D C",
           "2": "bowtie A B C D E; A B par E D; show triangle A B C ~ triangle D E C",
           "3": "sas G H I 30 12 15; J K L 30 8 10; pose 1", "4": "sas B C A 6 4; Y Z X 3 2",
           "5": "angles A B C D E F; A 27, C 115; E 38, D 27"}

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
        figure(dict(old, prompt=t))
    except (ValueError, KeyError, TypeError, IndexError, StopIteration):
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
