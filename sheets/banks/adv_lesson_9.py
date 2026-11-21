"""Lesson 9 (Advanced Math): congruent figures, proof outlines. From the Saxon
lesson and its deck (~/Documents/adv_math/problem_sets/ps_009/slides/deck_009.typ):
examples 9.1-9.3 and Problem Set 9, problems 9-11.

    1  the congruency postulate:     a marked pair, triangle W X Z = triangle Y X Z      SAS
    2  two triangles congruent:      given AB = CB, angle ABD = angle CBD; show triangle ABD = triangle CBD
                                                                     triangle ABD = triangle CBD, SAS
    3  a part, by CPCTC:             given BC = DC, AB = AD; show angle ABC = angle ADC
                                                                     triangle ABC = triangle ADC, SSS;
                                                                     angle ABC = angle ADC, CPCTC
    4  a fact first, then CPCTC:     given angle E = angle H, EF = HG; show DF = DG
                                     (1. DE = DH, sides opposite congruent angles)
                                                                     triangle EDF = triangle HDG, SAS;
                                                                     DF = DG, CPCTC

Problem 9 (name the postulate for four marked pairs) has no worked example; it is
Type 1, one problem a pair, because it practices the lesson's four postulates. The
outlines are three short steps, not two-column proofs, so they are types (as
Lesson 8's "show the following" is): 1 marks the figure, 2 names the triangles'
congruence and its postulate, 3 the part by CPCTC. Type 4 is split from Type 3
because its step 1 needs a fact the givens don't mark: an isosceles triangle
(9.2: base angles E and H make DE = DH) or halves of congruent segments (9.3).

The figures are the book's five shapes, each a "family" with its points named in
a fixed order of roles:
    pair  A B C D E F    two triangles, the second turned half around (problem 9a)
    split A B C D        triangle ABC, D on AB, segment CD (9.1; problems 9b, 10)
    kite  A B C D        quadrilateral ABCD and its diagonal AC (problems 9c, 9d, 11)
    cevians E H D F G    triangle DEH, F and G on EH, segments DF and DG (9.2)
    mids  A B C D E F G  triangle ACE, B on CA, D on CE, G and F on AE, segments BG, DF (9.3)
The letters are a run of the alphabet (no I or O), assigned to the roles as the book
assigns them.

The key writes what the deck writes: the triangles' congruence and its postulate,
then the asked-for part and CPCTC; the key's figure is the marked copy (step 1),
ticks for equal sides, arcs for equal angles, boxes for right angles, a circle on
the side both triangles share; a fact found in step 1 is written as step 1 with
its reason ("sides opposite congruent angles", "base angles of an isosceles
triangle", "halves of congruent segments"). The key's left triangle holds the
asked-for part: an angle's three letters in order (problem 11: triangle ABC =
triangle ADC), or the vertex off a segment, then the segment (9.2: triangle EDF
= triangle HDG; 9.3: triangle ABG = triangle EDF). For 9.1 that gives triangle
DAC = triangle DBC where the deck writes ADC = BDC; the check accepts both.
Type 1's answer is the postulate's name.

check() works from the problem's data, independently of how it was built: the
figure's triangles, angles (by their rays), and segments are read from the
points; the givens are closed under the lesson's step 1 (a perpendicular makes
right angles, a midpoint two equal halves, an isosceles triangle's base angles
and sides opposite congruent angles, halves of congruent segments; a side in
both triangles is equal to itself); the key's two triangles must be triangles
of the figure, really congruent in its drawing in the key's vertex order, the
named postulate's parts (SSS; SAS with the angle between the sides; AAAS, two
angles and any side; HL, right angles, hypotenuses, and a leg) equal in the
closure, and the asked-for part a pair of corresponding parts. Type 1 reads
the marks alone (no step 1): exactly one postulate holds, and it is the answer.

Skipped sources: none (the types file lists no proof beyond these outlines).

A problem: dict(type, prompt, answer, source); the prompt is the problem's data:
  1  "postulate split W Y X Z; W X = Y X, angle W X Z = angle Y X Z; triangle W X Z = triangle Y X Z"
     answer "SAS"
  2-4  "split A C B D; A B = C B, angle A B D = angle C B D; show triangle A B D = triangle C B D"
     answer "triangle A B D = triangle C B D, SAS"
     "kite A B C D; B C = D C, A B = A D; show angle A B C = angle A D C"
     answer "triangle A B C = triangle A D C, SSS; angle A B C = angle A D C, CPCTC"
  A given is "A D = B D" (segments), "angle E = angle H" or "angle A B D = angle C B D",
  "D C perp A B", or "B mid C A" (B is the midpoint of CA).
"""
import itertools, math, re
from functools import lru_cache
from .. import gen
from ..gen import need
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_9"
FIXED = False
TITLE = "Lesson 9: Congruent Figures, Proof Outlines"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

POSTULATES = ("SSS", "SAS", "AAAS", "HL")
OUTLINE = "Outline a proof: mark the figure, show two triangles congruent, and finish with CPCTC when a part is asked for."
TYPES = [
    dict(key="1", title="Naming the Congruency Postulate",
         look="Two triangles marked to show their equal parts, and a statement that they are congruent.",
         move="Read the marks: ticks are equal sides, arcs equal angles, a box a right angle, and a side in both "
              "triangles is equal to itself. Three pairs of sides: SSS. Two sides and the angle between them: SAS. "
              "Two angles and any side: AAAS. Right triangles with equal hypotenuses and a pair of equal legs: HL.",
         instructions="State the congruency postulate (SSS, SAS, AAAS, or HL) that proves the triangles congruent.",
         space="0.5in"),
    dict(key="2", title="Outlining a Proof That Two Triangles Are Congruent",
         look="Givens about a figure, and two triangles to show congruent.",
         move="Copy the figure and mark it: ticks for equal sides, arcs for equal angles, a box for a right angle "
              "($perp$), a circle on the side both triangles share. Then write the congruence with the vertices in "
              "matching order and its postulate: $Delta A B D tilde.equiv Delta C B D$, SAS.",
         instructions=OUTLINE),
    dict(key="3", title="Outlining a Proof by CPCTC",
         look="Givens about a figure, and two segments or two angles to show congruent.",
         move="Find two triangles that hold the parts. Mark the figure, show the triangles congruent by SSS, SAS, "
              "AAAS, or HL, then the parts are congruent by CPCTC: $Delta A B C tilde.equiv Delta A D C$, SSS; "
              "$angle A B C tilde.equiv angle A D C$, CPCTC.",
         instructions=OUTLINE),
    dict(key="4", title="Outlining a Proof: A Fact First, Then CPCTC",
         look="The givens don't mark enough parts until step 1 finds another pair.",
         move="Mark the figure, then look for more. Base angles of an isosceles triangle are congruent, and sides "
              "opposite congruent angles are congruent: $angle E tilde.equiv angle H$ makes "
              "$overline(D E) tilde.equiv overline(D H)$. Halves of congruent segments are congruent. Then show "
              "the triangles congruent and finish with CPCTC.",
         instructions=OUTLINE),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The figures: each family's points in role order, its straight runs, its drawing
# ------------------------------------------------------------------
SIZE = {"pair": 6, "split": 4, "kite": 4, "cevians": 5, "mids": 7}
CHAINS = {
    "pair": ((0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)),
    "split": ((0, 3, 1), (0, 2), (1, 2), (2, 3)),
    "kite": ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2)),
    "cevians": ((0, 3, 4, 1), (2, 0), (2, 3), (2, 4), (2, 1)),
    "mids": ((0, 1, 2), (2, 3, 4), (0, 6, 5, 4), (1, 6), (3, 5)),
}

def _pair_points(right):
    """A scalene triangle (problem 9a's shape), or a right one with its right angle at
    vertex `right`, then a copy turned half around, to its right."""
    a = {None: (68, 82, 30), 0: (90, 58, 32), 1: (60, 90, 30), 2: (58, 32, 90)}[right]
    base = 2.6
    side = base * math.sin(math.radians(a[2])) / math.sin(math.radians(a[1]))
    tri = [(0.0, 0.0), (side * math.cos(math.radians(a[0])), side * math.sin(math.radians(a[0]))), (base, 0.0)]
    xs, ys = [p[0] for p in tri], [p[1] for p in tri]
    X0, Y0 = 2 * max(xs) + 0.5 - min(xs), max(ys) + min(ys)
    return tri + [(X0 - x, Y0 - y) for x, y in tri]

def layout(family, right):
    """The role points; right: the right angle's role (pair) or True (kite)."""
    if family == "pair":
        return _pair_points(right)
    if family == "split":
        return [(0, 0), (2.4, 0), (1.2, 2.0), (1.2, 0)]
    if family == "kite":
        if right:
            y = 1.5 - math.sqrt(1.5 ** 2 - 1.4 ** 2)                  # on the circle on AC: right angles at B, D
            return [(0, 0), (-1.4, y), (0, 3), (1.4, y)]
        return [(0, 0), (-1.25, 1.2), (0, 3), (1.25, 1.2)]
    if family == "cevians":
        return [(0, 0), (4, 0), (2, 1.8), (0.9, 0), (3.1, 0)]
    return [(0, 0), (1, 1.3), (2, 2.6), (3, 1.3), (4, 0), (3, 0), (1, 0)]

RIGHT = ("right",)

@lru_cache(maxsize=None)
def _chain(family, names, a, b):
    """The straight run of the figure holding points a and b, or None."""
    for c in CHAINS[family]:
        c = tuple(names[i] for i in c)
        if a in c and b in c and a != b:
            return c
    return None

class Figure:
    """A family's figure with its points named: its segments, angles (by vertex and the
    directions of the two rays), and triangles, read from the points."""
    def __init__(self, family, names, perps=()):
        if family not in SIZE:
            raise ValueError("start with " + ", ".join(SIZE))
        if len(names) != SIZE[family] or len(set(names)) != len(names):
            raise ValueError(f"name the {SIZE[family]} points of the {family} with different letters")
        self.family, self.names = family, tuple(names)
        self.chains = [tuple(names[i] for i in c) for c in CHAINS[family]]
        roles = {self.names.index(self.meet(*pq)) for pq in perps}
        right = None
        if family == "pair" and roles:
            if len({r % 3 for r in roles}) > 1:
                raise ValueError("a triangle has one right angle")
            right = roles.pop() % 3
        elif family == "kite" and roles:
            right = True
        self.pts = dict(zip(self.names, layout(family, right)))
        self._rays, self._tris, self._ang = {}, None, {}
        for (a, b), (c, d) in perps:
            O = self.meet((a, b), (c, d))
            u, w = self.vec(a, b), self.vec(c, d)
            if abs(u[0] * w[0] + u[1] * w[1]) > 1e-9 * math.hypot(*u) * math.hypot(*w):
                raise ValueError(f"{a}{b} and {c}{d} aren't perpendicular in this figure")

    def vec(self, a, b):
        (ax, ay), (bx, by) = self.pts[a], self.pts[b]
        return bx - ax, by - ay

    def chain(self, a, b):
        return _chain(self.family, self.names, a, b) if (a in self.names and b in self.names) else None

    def joined(self, a, b):
        return self.chain(a, b) is not None

    def meet(self, s1, s2):
        c1, c2 = self.chain(*s1), self.chain(*s2)
        if c1 is None or c2 is None:
            raise ValueError("a perpendicular joins two segments of the figure")
        common = set(c1) & set(c2)
        if len(common) != 1:
            raise ValueError("perpendicular segments must meet at a point of the figure")
        return common.pop()

    def direction(self, v, p):
        x, y = self.vec(v, p)
        return round(math.degrees(math.atan2(y, x)), 3) + 0.0

    def seg(self, a, b):
        if not self.joined(a, b):
            raise ValueError(f"{a}{b} isn't a segment of the figure")
        return ("s", frozenset((a, b)))

    def ang(self, v, p, q):
        k = (v, p, q)
        if k not in self._ang:
            self._ang[k] = self._ang_new(v, p, q)
        return self._ang[k]

    def _ang_new(self, v, p, q):
        if not (self.joined(v, p) and self.joined(v, q)):
            raise ValueError(f"angle {p}{v}{q} isn't an angle of the figure")
        dp, dq = self.direction(v, p), self.direction(v, q)
        if dp == dq or abs(abs(dp - dq) - 180) < 1e-6:
            raise ValueError(f"angle {p}{v}{q} isn't an angle of the figure")
        return ("a", v, frozenset((dp, dq)))

    def rays(self, v):
        """{direction: the nearest point that way} of the rays from v along the figure's lines."""
        if v in self._rays:
            return self._rays[v]
        out = self._rays[v] = {}
        for p in self.names:
            if p != v and self.joined(v, p):
                d = self.direction(v, p)
                if d not in out or self.length(v, p) < self.length(v, out[d]):
                    out[d] = p
        return out

    def ang1(self, v):
        r = self.rays(v)
        if len(r) != 2:
            raise ValueError(f"name the angle at {v} with three letters")
        p, q = r.values()
        return self.ang(v, p, q)

    def ray_points(self, item):
        """Two points that show an angle item's rays."""
        _, v, dirs = item
        r = self.rays(v)
        return [r[d] for d in sorted(dirs)]

    def length(self, a, b):
        return math.hypot(*self.vec(a, b))

    @property
    def triangles(self):
        if self._tris is not None:
            return self._tris
        out = self._tris = []
        for t in itertools.combinations(self.names, 3):
            if all(self.joined(a, b) for a, b in itertools.combinations(t, 2)):
                (ux, uy), (wx, wy) = self.vec(t[0], t[1]), self.vec(t[0], t[2])
                if abs(ux * wy - uy * wx) > 1e-9:
                    out.append(frozenset(t))
        return out

    def is_triangle(self, t):
        return len(set(t)) == 3 and frozenset(t) in self.triangles

    def tri_angle(self, t, v):
        p, q = [x for x in t if x != v]
        return self.ang(v, p, q)

    def angle_name(self, v, p, q):
        """angle E when E has two rays, else angle D E F."""
        return f"angle {v}" if len(self.rays(v)) == 2 else f"angle {p} {v} {q}"

# ------------------------------------------------------------------
# Reading the data
# ------------------------------------------------------------------
L = r"([A-Z])"
SEG = rf"{L} {L}"
ANG = rf"angle {L}(?: {L} {L})?"
TRI = rf"triangle {L} {L} {L}"
FORMS = [("seg", re.compile(rf"{SEG} = {SEG}")), ("ang", re.compile(rf"{ANG} = {ANG}")),
         ("perp", re.compile(rf"{SEG} perp {SEG}")), ("mid", re.compile(rf"{L} mid {SEG}")),
         ("tri", re.compile(rf"{TRI} = {TRI}"))]

def parse_fact(s):
    """A given, a goal, or a statement: ("seg", (a, b), (c, d)), ("ang", (v,) or (p, v, q), ...),
    ("perp", (a, b), (c, d)), ("mid", m, (x, y)), ("tri", (a, b, c), (d, e, f))."""
    s = " ".join(s.split())
    for kind, rx in FORMS:
        m = rx.fullmatch(s)
        if not m:
            continue
        g = m.groups()
        if kind in ("seg", "perp"):
            return (kind, g[:2], g[2:])
        if kind == "mid":
            return (kind, g[0], g[1:])
        if kind == "tri":
            return (kind, g[:3], g[3:])
        a, b = g[:3], g[3:]
        return (kind, tuple(x for x in a if x), tuple(x for x in b if x))
    raise ValueError(f"can't read {s!r}: write A D = B D, angle E = angle H, D C perp A B, or B mid C A")

def fact_text(f):
    """The data's spelling of a parsed fact."""
    kind = f[0]
    if kind == "seg":
        return f"{' '.join(f[1])} = {' '.join(f[2])}"
    if kind == "ang":
        return f"angle {' '.join(f[1])} = angle {' '.join(f[2])}"
    if kind == "perp":
        return f"{' '.join(f[1])} perp {' '.join(f[2])}"
    if kind == "mid":
        return f"{f[1]} mid {' '.join(f[2])}"
    return f"triangle {' '.join(f[1])} = triangle {' '.join(f[2])}"

def split_facts(s):
    return [x for x in (y.strip() for y in s.split(",")) if x]

def read(prompt):
    """(kind, figure, givens, goal): kind "postulate" (Type 1, the goal is the statement) or "outline"."""
    s = " ".join(prompt.split())
    kind = "outline"
    if s.startswith("postulate "):
        kind, s = "postulate", s[len("postulate "):]
    parts = [x.strip() for x in s.split(";")]
    if len(parts) != 3:
        raise ValueError("write it like: split A B C D; A D = B D, D C perp A B; show A C = B C")
    head = parts[0].split()
    givens = [parse_fact(x) for x in split_facts(parts[1])]
    if not givens:
        raise ValueError("give at least one fact")
    goal_s = parts[2]
    if kind == "outline":
        if not goal_s.startswith("show "):
            raise ValueError("end with: show A C = B C")
        goal_s = goal_s[5:]
    goal = parse_fact(goal_s)
    if goal[0] in ("perp", "mid") or (kind == "postulate" and goal[0] != "tri"):
        raise ValueError("show two segments, two angles, or two triangles congruent")
    if any(g[0] == "tri" for g in givens):
        raise ValueError("a given is about segments or angles")
    F_ = Figure(head[0], head[1:], [(g[1], g[2]) for g in givens if g[0] == "perp"])
    return kind, F_, givens, goal

def item(F_, part, kind):
    """The segment or angle a fact's side names."""
    if kind == "seg":
        return F_.seg(*part)
    if len(part) == 1:
        return F_.ang1(part[0])
    p, v, q = part
    return F_.ang(v, p, q)

# ------------------------------------------------------------------
# Step 1: what the givens make equal
# ------------------------------------------------------------------
REASONS = {"base": "base angles of an isosceles triangle", "opposite": "sides opposite congruent angles",
           "halves": "halves of congruent segments"}

class Closure:
    """The givens' equal parts (union-find over segments, angles, and RIGHT). deduce: also
    the lesson's step-1 facts (isosceles triangles both ways, halves of congruent
    segments), each kept as a record: dict(pair, text, reason, premises)."""
    def __init__(self, F_, givens, deduce=True):
        self.F, self.parent, self.records = F_, {}, []
        self.base = None if not deduce else Closure(F_, givens, deduce=False)
        mids = []
        for g in givens:
            kind = g[0]
            if kind in ("seg", "ang"):
                self.union(item(F_, g[1], kind), item(F_, g[2], kind))
            elif kind == "perp":
                O = F_.meet(g[1], g[2])
                c1, c2 = F_.chain(*g[1]), F_.chain(*g[2])
                for p in c1:
                    for q in c2:
                        if O not in (p, q):
                            self.union(F_.ang(O, p, q), RIGHT)
            elif kind == "mid":
                m, (x, y) = g[1], g[2]
                c = F_.chain(x, y)
                if c is None or m not in c or not (min(c.index(x), c.index(y)) < c.index(m) < max(c.index(x), c.index(y))):
                    raise ValueError(f"{m} must lie between {x} and {y}")
                self.union(F_.seg(x, m), F_.seg(m, y))
                mids.append((m, x, y))
        if deduce:
            self._deduce(mids)

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        return True

    def eq(self, a, b):
        return a == b or self.find(a) == self.find(b)

    def right(self, a):
        return self.find(a) == self.find(RIGHT)

    def _premise(self, a, b):
        """The record that made a and b equal, when the givens alone don't."""
        if self.base.eq(a, b):
            return []
        for i, r in enumerate(self.records):
            x, y = r["pair"]
            if {self.base.find(x), self.base.find(y)} == {self.base.find(a), self.base.find(b)}:
                return [i]
        return [i for i in range(len(self.records))]

    def _record(self, pairs, reason, premise):
        """pairs: [((a, b), text)], made equal for one reason; recorded if any was news."""
        new = [self.union(a, b) for (a, b), _ in pairs]
        if any(new):
            self.records.append(dict(pairs=pairs, pair=pairs[0][0], text=pairs[0][1], reason=reason,
                                     premises=premise))
            return True
        return False

    def _deduce(self, mids):
        F_ = self.F
        changed = True
        while changed:
            changed = False
            for t in F_.triangles:
                for a in sorted(t):
                    b, c = sorted(t - {a})
                    sb, sc = F_.seg(a, b), F_.seg(a, c)              # sides at a, opposite c and b
                    ab, ac = F_.tri_angle(t, b), F_.tri_angle(t, c)
                    if self.eq(sb, sc) and not self.eq(ab, ac):
                        names = (F_.angle_name(b, a, c), F_.angle_name(c, a, b))
                        changed |= self._record([((ab, ac), f"{names[0]} = {names[1]}")], "base", self._premise(sb, sc))
                    if self.eq(ab, ac) and not self.eq(sb, sc):
                        changed |= self._record([((sb, sc), f"{a} {b} = {a} {c}")], "opposite", self._premise(ab, ac))
            for (m, x, y), (n, u, v) in itertools.combinations(mids, 2):
                whole1, whole2 = F_.seg(x, y), F_.seg(u, v)
                if self.eq(whole1, whole2):
                    pairs = [((F_.seg(p, q), F_.seg(r, s)), f"{p} {q} = {r} {s}")
                             for (p, q), (r, s) in (((x, m), (u, n)), ((y, m), (v, n)))]
                    changed |= self._record(pairs, "halves", self._premise(whole1, whole2))

# ------------------------------------------------------------------
# The postulates
# ------------------------------------------------------------------
def parts(F_, t1, t2):
    """Corresponding sides (side i joins vertices i and i+1) and angles (at vertex i)."""
    S = [(F_.seg(t1[i], t1[(i + 1) % 3]), F_.seg(t2[i], t2[(i + 1) % 3])) for i in range(3)]
    A = [(F_.tri_angle(t1, t1[i]), F_.tri_angle(t2, t2[i])) for i in range(3)]
    return S, A

def support(F_, C, t1, t2):
    """{postulate: the three pairs of parts it uses} for the correspondence t1 -> t2."""
    S, A = parts(F_, t1, t2)
    se, ae = [C.eq(*s) for s in S], [C.eq(*a) for a in A]
    out = {}
    if all(se):
        out["SSS"] = S
    for i in range(3):                                          # the angle at i lies between sides i-1 and i
        if ae[i] and se[i] and se[i - 1]:
            out.setdefault("SAS", [S[i - 1], A[i], S[i]])
    angs, sides = [i for i in range(3) if ae[i]], [i for i in range(3) if se[i]]
    if len(angs) >= 2 and sides:
        out["AAAS"] = [A[angs[0]], A[angs[1]], S[sides[0]]]
    for i in range(3):
        hyp, legs = S[(i + 1) % 3], (S[i], S[i - 1])
        if C.right(A[i][0]) and C.right(A[i][1]) and C.eq(*hyp):
            for leg in legs:
                if C.eq(*leg):
                    out.setdefault("HL", [A[i], hyp, leg])
    return out

def congruent_drawn(F_, t1, t2):
    """The correspondence is a congruence in the figure as drawn."""
    return all(abs(F_.length(t1[i], t1[j]) - F_.length(t2[i], t2[j])) < 1e-9 for i, j in ((0, 1), (1, 2), (0, 2)))

def mapping(t1, t2):
    return frozenset(zip(t1, t2))

def corresponds(F_, goal, t1, t2):
    """Is the goal (two segments or two angles) a pair of corresponding parts?"""
    kind, g1, g2 = goal
    i1, i2 = item(F_, g1, kind), item(F_, g2, kind)
    S, A = parts(F_, t1, t2)
    return any({i1, i2} == set(pq) for pq in (S if kind == "seg" else A))

def candidates(F_, goal):
    """(t1, t2) correspondences that could prove the goal, the left triangle in the key's
    order: an angle's three letters; else the vertex off a segment (or the angle's other
    two points in the figure's order), then the part."""
    kind, g1, g2 = goal
    if kind == "tri":
        return [(tuple(g1), tuple(g2))]
    i1, i2 = item(F_, g1, kind), item(F_, g2, kind)
    out = []
    for T1 in F_.triangles:
        if kind == "seg":
            if not set(g1) <= T1:
                continue
            (z,) = T1 - set(g1)
            t1 = (z,) + tuple(g1)
        else:
            v = i1[1]
            if v not in T1 or F_.tri_angle(T1, v) != i1:
                continue
            if len(g1) == 3 and set(g1) == T1:
                t1 = tuple(g1)
            else:
                o = [n for n in F_.names if n in T1 and n != v]
                t1 = (v, o[0], o[1])
        for T2 in F_.triangles:
            if T2 == T1 or (kind == "seg" and not set(g2) <= T2) or (kind == "ang" and i2[1] not in T2):
                continue
            for perm in itertools.permutations(sorted(T2)):
                t2 = dict(zip(sorted(T1), perm))
                t2 = tuple(t2[n] for n in t1)
                if (t1, t2) not in out and corresponds(F_, goal, t1, t2):
                    out.append((t1, t2))
    return out

def known(F_, C, goal):
    kind, g1, g2 = goal
    return kind != "tri" and C.eq(item(F_, g1, kind), item(F_, g2, kind))

def solve(F_, givens, goal):
    """(t1, t2, postulate, direct): the key's congruence. direct: the givens prove it with
    no step-1 fact. Prefers a direct proof, then SSS, SAS, AAAS, HL. None if there's none."""
    full = Closure(F_, givens)
    if known(F_, full, goal):
        return None
    best = None
    for t1, t2 in candidates(F_, goal):
        if not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
            continue
        if not congruent_drawn(F_, t1, t2):
            continue
        sf, sd = support(F_, full, t1, t2), support(F_, full.base, t1, t2)
        for post in POSTULATES:
            if post in sf:
                rank = (post not in sd, POSTULATES.index(post))
                if best is None or rank < best[0]:
                    best = (rank, t1, t2, post)
    if best is None:
        return None
    (indirect, _), t1, t2, post = best
    return t1, t2, post, not indirect

def outline_answer(F_, givens, goal):
    found = solve(F_, givens, goal)
    if found is None:
        raise ValueError("the lesson's postulates don't prove it from these givens")
    t1, t2, post, _ = found
    a = f"triangle {' '.join(t1)} = triangle {' '.join(t2)}, {post}"
    return a if goal[0] == "tri" else f"{a}; {fact_text(goal)}, CPCTC"

def marks_support(F_, givens, statement):
    """Type 1: the postulates the marks alone prove (no step 1)."""
    C = Closure(F_, givens, deduce=False)
    _, t1, t2 = statement
    if not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
        raise ValueError("name two triangles of the figure")
    return support(F_, C, tuple(t1), tuple(t2))

def answer_of(prompt):
    kind, F_, givens, goal = read(prompt)
    if kind == "postulate":
        if not congruent_drawn(F_, goal[1], goal[2]):
            raise ValueError("those triangles don't match in this order")
        s = marks_support(F_, givens, goal)
        if len(s) != 1:
            raise ValueError("the marks must prove the triangles congruent by exactly one postulate")
        return next(iter(s))
    if any(g[0] == "tri" for g in givens):
        raise ValueError("a given is about segments or angles")
    return outline_answer(F_, givens, goal)

# ------------------------------------------------------------------
# The candidate givens and goals of each family, in role letters
# ------------------------------------------------------------------
CANDS = {
    "pair": ["{0} {1} = {3} {4}", "{1} {2} = {4} {5}", "{2} {0} = {5} {3}",
             "angle {0} = angle {3}", "angle {1} = angle {4}", "angle {2} = angle {5}",
             "{1} {0} perp {0} {2}, {4} {3} perp {3} {5}", "{0} {1} perp {1} {2}, {3} {4} perp {4} {5}",
             "{1} {2} perp {2} {0}, {4} {5} perp {5} {3}"],
    "split": ["{0} {3} = {1} {3}", "{3} mid {0} {1}", "{3} {2} perp {0} {1}", "{0} {2} = {1} {2}",
              "angle {0} {2} {3} = angle {1} {2} {3}", "angle {0} = angle {1}"],
    "kite": ["{1} {2} = {3} {2}", "{0} {1} = {0} {3}", "angle {1} {0} {2} = angle {3} {0} {2}",
             "angle {1} {2} {0} = angle {3} {2} {0}", "angle {1} = angle {3}",
             "{0} {1} perp {1} {2}, {0} {3} perp {3} {2}"],
    "cevians": ["angle {0} = angle {1}", "{2} {0} = {2} {1}", "{0} {3} = {1} {4}",
                "angle {0} {2} {3} = angle {1} {2} {4}", "{2} {3} = {2} {4}"],
    "mids": ["{0} {6} = {4} {5}", "{1} {6} perp {0} {4}, {3} {5} perp {0} {4}",
             "angle {0} {1} {6} = angle {4} {3} {5}", "{1} {6} = {3} {5}", "{2} {0} = {2} {4}",
             "angle {0} = angle {4}", "{1} mid {2} {0}", "{3} mid {2} {4}"],
}
GOALS = {
    "split": ["{0} {2} = {1} {2}", "{0} {3} = {1} {3}", "angle {0} = angle {1}",
              "angle {0} {2} {3} = angle {1} {2} {3}", "angle {0} {3} {2} = angle {1} {3} {2}",
              "triangle {0} {2} {3} = triangle {1} {2} {3}"],
    "kite": ["angle {0} {1} {2} = angle {0} {3} {2}", "{1} {2} = {3} {2}", "{0} {1} = {0} {3}",
             "angle {1} {0} {2} = angle {3} {0} {2}", "angle {1} {2} {0} = angle {3} {2} {0}",
             "triangle {0} {1} {2} = triangle {0} {3} {2}"],
    "cevians": ["{2} {3} = {2} {4}", "angle {0} {2} {3} = angle {1} {2} {4}",
                "angle {2} {3} {0} = angle {2} {4} {1}", "{0} {3} = {1} {4}"],
    "mids": ["{1} {6} = {3} {5}", "{0} {6} = {4} {5}", "angle {0} {1} {6} = angle {4} {3} {5}",
             "angle {1} {6} {0} = angle {3} {5} {4}"],
}
STATEMENT = {"pair": "triangle {0} {1} {2} = triangle {3} {4} {5}", "split": "triangle {0} {2} {3} = triangle {1} {2} {3}",
             "kite": "triangle {0} {1} {2} = triangle {0} {3} {2}"}
MOST = {"pair": 4, "split": 3, "kite": 3, "cevians": 3, "mids": 5}   # the most givens a problem has

def givens_text(family, names, givens):
    return ", ".join(CANDS[family][i].format(*names) for i in givens)

def build_name(family, names, givens):
    """Type 1: the marks and the congruence to name the postulate of."""
    return f"postulate {family} {' '.join(names)}; {givens_text(family, names, givens)}; {STATEMENT[family].format(*names)}"

def build_outline(family, names, givens, goal):
    """Types 2-4: the givens and what to show."""
    return f"{family} {' '.join(names)}; {givens_text(family, names, givens)}; show {GOALS[family][goal].format(*names)}"

def _subsets(family):
    n = len(CANDS[family])
    for size in range(1, MOST[family] + 1):
        yield from itertools.combinations(range(n), size)

def enumerate_combos(kind, family):
    """Every (givens, goal) a type draws in the family (goal None for Type 1): proved, by
    givens that are all needed. Type 1: the marks prove the statement by exactly one
    postulate. Type 2: a triangle goal, proved with no step-1 fact; Type 3: a part, the
    same; Type 4: a part that needs a step-1 fact."""
    names = tuple("ABCDEFGHJ"[:SIZE[family]])
    out = []
    if kind == "1":
        proves = {}
        for sub in _subsets(family):
            if family != "kite" and sum("perp" in CANDS[family][i] for i in sub) > 1:
                continue
            if any("mid" in CANDS[family][i] for i in sub):
                continue
            try:
                _, F_, givens, goal = read(build_name(family, names, sub))
                proves[sub] = set(marks_support(F_, givens, goal))
            except ValueError:
                continue
        for sub, s in proves.items():
            if len(s) == 1 and all(not proves.get(tuple(x for x in sub if x != i), set()) for i in sub):
                out.append((sub, None))
        return tuple(out)
    status = {}
    for sub in _subsets(family):
        for g in range(len(GOALS[family])):
            try:
                _, F_, givens, goal = read(build_outline(family, names, sub, g))
                found = solve(F_, givens, goal)
            except ValueError:
                found = None
            status[sub, g] = found and (goal[0], found[3])
    for (sub, g), st in status.items():
        if not st or any(status.get((tuple(x for x in sub if x != i), g)) for i in sub):
            continue
        tri, direct = st[0] == "tri", st[1]
        k = "2" if tri and direct else "3" if direct else "4" if not tri else None
        if k == kind:
            out.append((sub, g))
    return tuple(out)

COMBOS = {   # (type, family): (givens, goal) -- enumerate_combos() made it; tests/test_adv_lesson_9.py remakes it
    ('1', 'pair'): (((0, 1, 2), None), ((0, 1, 4), None), ((0, 1, 6), None), ((0, 1, 7), None), ((0, 1, 8), None),
        ((0, 2, 3), None), ((0, 2, 6), None), ((0, 2, 7), None), ((0, 2, 8), None), ((0, 3, 4), None),
        ((0, 3, 5), None), ((0, 3, 7), None), ((0, 3, 8), None), ((0, 4, 5), None), ((0, 4, 6), None),
        ((0, 4, 8), None), ((0, 5, 6), None), ((0, 5, 7), None), ((1, 2, 5), None), ((1, 2, 6), None),
        ((1, 2, 7), None), ((1, 2, 8), None), ((1, 3, 4), None), ((1, 3, 5), None), ((1, 3, 7), None),
        ((1, 3, 8), None), ((1, 4, 5), None), ((1, 4, 6), None), ((1, 4, 8), None), ((1, 5, 6), None),
        ((1, 5, 7), None), ((2, 3, 4), None), ((2, 3, 5), None), ((2, 3, 7), None), ((2, 3, 8), None),
        ((2, 4, 5), None), ((2, 4, 6), None), ((2, 4, 8), None), ((2, 5, 6), None), ((2, 5, 7), None),),
    ('1', 'split'): (((0, 2), None), ((0, 3), None), ((2, 3), None), ((2, 4), None), ((2, 5), None),
        ((3, 4), None), ((4, 5), None),),
    ('1', 'kite'): (((0, 1), None), ((0, 3), None), ((0, 5), None), ((1, 2), None), ((1, 5), None), ((2, 3), None),
        ((2, 4), None), ((2, 5), None), ((3, 4), None), ((3, 5), None),),
    ('2', 'split'): (((0, 2), 5), ((0, 3), 5), ((1, 2), 5), ((1, 3), 5), ((2, 3), 5), ((2, 4), 5), ((2, 5), 5),
        ((3, 4), 5), ((4, 5), 5),),
    ('2', 'kite'): (((0, 1), 5), ((0, 3), 5), ((0, 5), 5), ((1, 2), 5), ((1, 5), 5), ((2, 3), 5), ((2, 4), 5),
        ((2, 5), 5), ((3, 4), 5), ((3, 5), 5),),
    ('3', 'split'): (((0, 2), 0), ((0, 2), 2), ((0, 2), 3), ((0, 3), 3), ((0, 3), 4), ((1, 2), 0), ((1, 2), 2),
        ((1, 2), 3), ((1, 3), 3), ((1, 3), 4), ((2, 3), 1), ((2, 3), 3), ((2, 4), 0), ((2, 4), 1), ((2, 4), 2),
        ((2, 5), 1), ((2, 5), 3), ((3, 4), 1), ((3, 4), 4), ((4, 5), 1), ((4, 5), 4),),
    ('3', 'kite'): (((0, 1), 0), ((0, 1), 3), ((0, 1), 4), ((0, 3), 0), ((0, 3), 2), ((0, 3), 3), ((0, 5), 2),
        ((0, 5), 3), ((0, 5), 4), ((1, 2), 0), ((1, 2), 1), ((1, 2), 4), ((1, 5), 1), ((1, 5), 3), ((1, 5), 4),
        ((2, 3), 0), ((2, 3), 1), ((2, 3), 2), ((2, 4), 1), ((2, 4), 2), ((2, 4), 4), ((2, 5), 1), ((2, 5), 2),
        ((2, 5), 4), ((3, 4), 1), ((3, 4), 2), ((3, 4), 3), ((3, 5), 1), ((3, 5), 2), ((3, 5), 3),),
    ('4', 'cevians'): (((0, 2), 0), ((0, 2), 1), ((0, 2), 2), ((0, 3), 0), ((0, 3), 2), ((0, 3), 3), ((1, 2), 0),
        ((1, 2), 1), ((1, 2), 2), ((1, 3), 0), ((1, 3), 2), ((1, 3), 3),),
    ('4', 'mids'): (((0, 1, 4), 0), ((0, 1, 4), 2), ((0, 2, 4), 0), ((0, 2, 4), 3), ((1, 3, 4), 1), ((1, 3, 4), 2),
        ((2, 3, 4), 1), ((2, 3, 4), 3), ((0, 4, 6, 7), 0), ((0, 4, 6, 7), 2), ((0, 4, 6, 7), 3), ((0, 5, 6, 7), 0),
        ((0, 5, 6, 7), 2), ((0, 5, 6, 7), 3), ((1, 4, 6, 7), 0), ((1, 4, 6, 7), 1), ((1, 4, 6, 7), 2),
        ((1, 5, 6, 7), 0), ((1, 5, 6, 7), 1), ((1, 5, 6, 7), 2), ((2, 4, 6, 7), 0), ((2, 4, 6, 7), 1),
        ((2, 4, 6, 7), 3), ((2, 5, 6, 7), 0), ((2, 5, 6, 7), 1), ((2, 5, 6, 7), 3),),
    ('4', 'split'): (((0, 5), 3), ((0, 5), 4), ((1, 5), 3), ((1, 5), 4),),
}

def combos(kind, family):
    return COMBOS.get((kind, family), ())

# ------------------------------------------------------------------
# Letters: a run of the alphabet, given to the roles as the book gives them
# ------------------------------------------------------------------
ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ"

def lettered(family, run, swap=False):
    """split: A B C D or (swap) A C B D, the foot last (9.1; problems 9b, 10); cevians: the
    apex first, then the base left to right (9.2: D, then E F G H); the rest in order."""
    r = tuple(run)
    if family == "split":
        return (r[0], r[2], r[1], r[3]) if swap else r
    if family == "cevians":
        return (r[1], r[4], r[0], r[2], r[3])
    return r

def names_ok(family, names):
    n = SIZE[family]
    runs = [ALPHA[i:i + n] for i in range(len(ALPHA) - n + 1)]
    return any(tuple(names) == lettered(family, run, s) for run in runs for s in (False, True))

def pick_names(r, family):
    n = SIZE[family]
    i = r.randrange(len(ALPHA) - n + 1)
    return lettered(family, ALPHA[i:i + n], r.random() < 0.5)

@lru_cache(maxsize=None)
def by_postulate(family):
    """Type 1's combos grouped by their answer, so each postulate comes up as often."""
    out = {}
    for sub, _ in combos("1", family):
        out.setdefault(answer_of(build_name(family, tuple("ABCDEFG"[:SIZE[family]]), sub)), []).append(sub)
    return [out[k] for k in POSTULATES if k in out]

def name_pick(family):
    def pick(r):
        sub = r.choice(r.choice(by_postulate(family)))
        return dict(family=family, names=pick_names(r, family), givens=sub)
    return pick

def outline_pick(kind, family):
    def pick(r):
        sub, g = r.choice(combos(kind, family))
        return dict(family=family, names=pick_names(r, family), givens=sub, goal=g)
    return pick

def name_ok(family, names, givens):
    return names_ok(family, names) and (tuple(givens), None) in combos("1", family)

def outline_ok(family, names, givens, goal, kind=None):
    if not names_ok(family, names):
        return False
    return any((tuple(givens), goal) in combos(k, family) for k in ([kind] if kind else ("2", "3", "4")))

TEMPLATES = {
    "1": [(name_pick("pair"), build_name), (name_pick("pair"), build_name), (name_pick("split"), build_name),
          (name_pick("kite"), build_name)],
    "2": [(outline_pick("2", "split"), build_outline), (outline_pick("2", "kite"), build_outline)],
    "3": [(outline_pick("3", "split"), build_outline), (outline_pick("3", "kite"), build_outline)],
    "4": [(outline_pick("4", "cevians"), build_outline), (outline_pick("4", "mids"), build_outline),
          (outline_pick("4", "split"), build_outline)],
}
RANGES = {build_name: name_ok, build_outline: outline_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def kind_of(prompt):
    """The type a prompt's data is: 1 a postulate to name, 2 triangles, 3 a part needing no
    step-1 fact, 4 a part that needs one."""
    kind, F_, givens, goal = read(prompt)
    if kind == "postulate":
        return "1"
    if goal[0] == "tri":
        return "2"
    found = solve(F_, givens, goal)
    return "3" if found and found[3] else "4"

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

# ------------------------------------------------------------------
# The check: from the data, not from the build
# ------------------------------------------------------------------
KEY_LINE = re.compile(rf"{TRI} = {TRI}, (SSS|SAS|AAAS|HL)")

def check_outline(p):
    kind, F_, givens, goal = read(p["prompt"])
    lines = [x.strip() for x in p["answer"].split(";")]
    m = KEY_LINE.fullmatch(" ".join(lines[0].split()))
    if kind != "outline" or not m:
        return "failed"
    t1, t2, post = m.groups()[:3], m.groups()[3:6], m.group(7)
    if not (F_.is_triangle(t1) and F_.is_triangle(t2)) or set(t1) == set(t2):
        return "failed"
    if not congruent_drawn(F_, t1, t2):
        return "failed"                                            # the vertices don't match
    C = Closure(F_, givens)
    if known(F_, C, goal) or post not in support(F_, C, t1, t2):
        return "failed"
    if goal[0] == "tri":
        ok = len(lines) == 1 and mapping(t1, t2) in (mapping(goal[1], goal[2]), mapping(goal[2], goal[1]))
        return "checked" if ok and p["type"] == "2" else "failed"
    if len(lines) != 2 or not lines[1].endswith(", CPCTC"):
        return "failed"
    said = parse_fact(lines[1][:-len(", CPCTC")])
    if said[0] != goal[0]:
        return "failed"
    same = {item(F_, said[1], said[0]), item(F_, said[2], said[0])} == {item(F_, goal[1], goal[0]),
                                                                       item(F_, goal[2], goal[0])}
    return "checked" if same and corresponds(F_, goal, t1, t2) and p["type"] in ("3", "4") else "failed"

def check_name(p):
    kind, F_, givens, goal = read(p["prompt"])
    if kind != "postulate" or not congruent_drawn(F_, goal[1], goal[2]):
        return "failed"
    s = marks_support(F_, givens, goal)
    return "checked" if len(s) == 1 and p["answer"].strip() in s else "failed"

def check(p):
    try:
        if p["type"] == "1":
            return check_name(p)
        if p["type"] in ("3", "4") and kind_of(p["prompt"]) != p["type"]:
            return "failed"
        return check_outline(p)
    except (ValueError, KeyError, AttributeError, TypeError, IndexError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Step 1 for the key: the marks, and the facts found
# ------------------------------------------------------------------
def key_parts(F_, givens, goal, answer):
    """(closure, t1, t2, the postulate's three pairs of parts) of an outline's key."""
    m = KEY_LINE.fullmatch(" ".join(answer.split(";")[0].split()))
    t1, t2, post = m.groups()[:3], m.groups()[3:6], m.group(7)
    C = Closure(F_, givens)
    direct = support(F_, C.base, t1, t2)                          # the givens alone, when they're enough
    return C, t1, t2, (direct if post in direct else support(F_, C, t1, t2))[post]

def notes(F_, C, used):
    """The step-1 facts the congruence uses, and the facts they came from: [(text, reason)]."""
    want = {}
    for a, b in used:
        if C.base.eq(a, b):
            continue
        hits = [(i, t) for i, r in enumerate(C.records) for pq, t in r["pairs"] if set(pq) == {a, b}]
        if not hits:
            hits = [(i, t) for i, r in enumerate(C.records) for pq, t in r["pairs"]
                    if {C.base.find(x) for x in pq} == {C.base.find(a), C.base.find(b)}]
        if hits:
            want[hits[0][0]] = hits[0][1]
    stack = list(want)
    while stack:
        for j in C.records[stack.pop()]["premises"]:
            if j not in want:
                want[j] = C.records[j]["text"]
                stack.append(j)
    return [(want[i], REASONS[C.records[i]["reason"]]) for i in sorted(want)]

def mark_list(F_, C, givens, used=()):
    """The figure's marks: ticks, arcs, right-angle boxes, circles (lesson_figures.marked)
    for the givens and the parts a key uses, numbered by class in order."""
    items = []
    for g in givens:
        if g[0] in ("seg", "ang"):
            items += [item(F_, g[1], g[0]), item(F_, g[2], g[0])]
        elif g[0] == "mid":
            m, (x, y) = g[1], g[2]
            items += [F_.seg(x, m), F_.seg(m, y)]
    shared = []
    for a, b in used:
        if a == b:
            shared.append(a)
        else:
            items += [a, b]
    rights = [x for x in list(C.parent) if x != RIGHT and x[0] == "a" and C.right(x)]
    seg_class, ang_class = {}, {}
    ticks, arcs = [], []
    seen = set()
    for x in items:
        if x in seen or (x[0] == "a" and C.right(x)):
            continue
        seen.add(x)
        if x[0] == "s":
            a, b = sorted(x[1])
            c = F_.chain(a, b)
            if abs(c.index(a) - c.index(b)) > 1:
                continue                                               # a segment with a point inside: its pieces carry the marks
            n = seg_class.setdefault(C.find(x), len(seg_class) + 1)
            ticks.append((a, b, n))
        else:
            n = ang_class.setdefault(C.find(x), len(ang_class) + 1)
            p, q = F_.ray_points(x)
            arcs.append((x[1], p, q, n))
    boxes = []
    for x in sorted(rights, key=str):
        p, q = F_.ray_points(x)
        boxes.append((x[1], p, q))
    circles = [tuple(sorted(x[1])) for x in shared]
    return ticks, arcs, boxes, circles

def figure(p, key=False, unit="1cm"):
    kind, F_, givens, goal = read(p["prompt"])
    if kind == "postulate":
        C = Closure(F_, givens, deduce=False)
        ticks, arcs, boxes, circles = mark_list(F_, C, givens)
    elif key:
        C, _, _, used = key_parts(F_, givens, goal, p["answer"])
        ticks, arcs, boxes, circles = mark_list(F_, C, givens, used)
    else:
        ticks = arcs = boxes = circles = ()
    wide, tall = (5.6, 1.6) if F_.family == "pair" else (3.2, 2.2) if F_.family in ("split", "kite") else (4.2, 2.2)
    return fig.marked(F_.pts, F_.chains, ticks, arcs, boxes, circles, wide=wide, tall=tall, unit=unit)

# ------------------------------------------------------------------
# Words
# ------------------------------------------------------------------
def fact_typst(f):
    kind = f[0]
    seg = lambda s: f"overline({' '.join(s)})"
    if kind == "seg":
        return f"${seg(f[1])} tilde.equiv {seg(f[2])}$"
    if kind == "ang":
        return f"$angle {' '.join(f[1])} tilde.equiv angle {' '.join(f[2])}$"
    if kind == "perp":
        return f"${seg(f[1])} perp {seg(f[2])}$"
    if kind == "mid":
        return f"${f[1]}$ is the midpoint of ${seg(f[2])}$"
    return f"$Delta {' '.join(f[1])} tilde.equiv Delta {' '.join(f[2])}$"

def fact_plain(f):
    kind = f[0]
    if kind == "seg":
        return f"{''.join(f[1])} ≅ {''.join(f[2])}"
    if kind == "ang":
        return f"∠{''.join(f[1])} ≅ ∠{''.join(f[2])}"
    if kind == "perp":
        return f"{''.join(f[1])} ⊥ {''.join(f[2])}"
    if kind == "mid":
        return f"{f[1]} is the midpoint of {''.join(f[2])}"
    return f"△{''.join(f[1])} ≅ △{''.join(f[2])}"

def listed(xs):
    return xs[0] if len(xs) == 1 else f"{xs[0]} and {xs[1]}" if len(xs) == 2 else ", ".join(xs[:-1]) + ", and " + xs[-1]

def statement(p, show=fact_typst):
    kind, F_, givens, goal = read(p["prompt"])
    if kind == "postulate":
        return f"Name the postulate that proves {show(goal)}: SSS, SAS, AAAS, or HL."
    return f"Given: {listed([show(g) for g in givens])}. Outline a proof that shows {show(goal)}."

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    return f"{s} #v(0.4em) #align(center)[{f}]"

def key_typst(p, gap="0.3em"):
    """The key's prompt: the figure marked (step 1)."""
    try:
        s, f = statement(p), figure(p, key=True)
    except (ValueError, AttributeError, KeyError):
        return typst(p, gap)
    return f"{s} #v(0.4em) #align(center)[{f}]"

def steps(p):
    """[(number, statement, reason)] of an outline's key, as parsed facts and words."""
    _, F_, givens, goal = read(p["prompt"])
    C, t1, t2, used = key_parts(F_, givens, goal, p["answer"])
    rows = [("1." if i == 0 else "", parse_fact(t), r) for i, (t, r) in enumerate(notes(F_, C, used))]
    if not rows:
        rows = [("1.", None, "Mark the figure.")]
    post = p["answer"].split(";")[0].rsplit(",", 1)[1].strip()
    rows.append(("2.", ("tri", t1, t2), post))
    if goal[0] != "tri":
        rows.append(("3.", goal, "CPCTC"))
    return rows

def answer_typst(p):
    if p["type"] == "1":
        return f"#emph[{p['answer']}]"
    try:
        rows = steps(p)
    except (ValueError, AttributeError, KeyError, IndexError):
        return f"${p['answer']}$"
    cells = []
    for n, f, r in rows:
        cells += [f"[{n}]", f"[{fact_typst(f)}]" if f else f"[{r}]", f"[#emph[{r}]]" if f else "[]"]
    return f"#grid(columns: 3, column-gutter: 0.8em, row-gutter: 0.5em, align: left, {', '.join(cells)})"

SLIDE_UNIT = "1.8cm"

def slide_typst(p, key=False):
    """The words (and the answer, hidden on the question slide) beside the figure drawn
    larger; the figure stays put, and its marks appear on the answer slide."""
    try:
        f, s = figure(p, key, SLIDE_UNIT), statement(p)
    except (ValueError, AttributeError, KeyError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def text(p):
    try:
        return statement(p, fact_plain) + "   [figure]"
    except ValueError:
        return p["prompt"]

def answer_text(p):
    if p["type"] == "1":
        return p["answer"]
    try:
        rows = steps(p)
    except (ValueError, AttributeError, KeyError, IndexError):
        return p["answer"]
    return "\n".join(f"{n} {fact_plain(f) + '   ' + r if f else r}".strip() for n, f, r in rows)

def height(p):
    return 2.9

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data
# ------------------------------------------------------------------
EXAMPLE = {"1": "postulate split W Y X Z; W X = Y X, angle W X Z = angle Y X Z; triangle W X Z = triangle Y X Z",
           "2": "split A C B D; A B = C B, angle A B D = angle C B D; show triangle A B D = triangle C B D",
           "3": "kite A B C D; B C = D C, A B = A D; show angle A B C = angle A D C",
           "4": "cevians E H D F G; angle E = angle H, E F = H G; show D F = D G"}

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
