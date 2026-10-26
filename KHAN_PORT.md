# Plan: porting the Khan Academy banks

Proposed 2026-10-25 on the `portKhan` branch. The teacher approved, the same day:
copied Khan items become **generators** (they aren't ported word for word);
**multiple choice stays** where Khan uses it; the **screenshot graphs get
generated graphs** in the last phase; and **review is per unit**, after a pilot.
`EXTENDING.md` and `PLAN.md` still hold. Where they disagree with this file,
this file wins for the Khan banks.

Source: `khan_algebra_worksheets/sets/archive/`, the `PreAlg_*`, `Alg1_*`, and
`Alg2_*` files: 115 lessons with about 2,000 problem slots. The `ExamUnit*` and
`Leah_exam_*` files are tests assembled from these lessons. They are left out,
since a sequence or a saved sheet can rebuild them.

## 1. What's in the old banks

Each file is one Khan exercise (its `index`, such as `2-6`, is unit-lesson).
Each `Problem` is one slot. Most lessons repeat one template 12–30 times,
so a lesson has only a few distinct shapes.

| Kind | Lessons | What it is | Port as |
|---|---|---|---|
| **Generator** | ~45 | `random` draws, answers computed | a generator bank; the old code is the spec |
| **Fixed, answered** | 5 | Khan items with answers typed in (2-2, 2-3, 2-4, 11-4, 11-6) | a generator modeled on them |
| **Fixed, no answer** | ~50 | Khan items copied in, `ANSWER TO nn GOES HERE` | a generator modeled on them |
| **Multiple choice** | ~30 (overlaps) | `randomizechoices` / "Choose all that apply" | `#choices`, distractors from real mistakes |
| **Screenshot graphs** | 11 | Khan PNGs, no answers (unit 8: 8-8, 8-12, 8-14 … 8-21; Alg2 3-1) | generated graphs (Phase 5) |
| **TikZ graphs** | 7 | drawn graphs (6-2, 6-4, 6-11, 8-2, 8-3, 8-5; Alg2 2-5) | cetz graphs (Phase 5) |
| **Area models / tables** | 6 | `class_poly_mult_box`, factor-pair tables, hundred charts | Typst `table`/`grid` |

By course:

- **Khan Prealgebra** (7): 1-1, 1-2, 1-3 factors and multiples; 3-9 equivalent ratio
  word problems; 6-2 evaluating expressions; 8-1, 8-2 percent problems.
- **Khan Algebra 1** (76): unit 0 (intro), 1 (evaluating), 2 (equations and
  inequalities, 11 lessons), 6 (systems, 15), 8 (functions, 22), 11 (exponents and
  radicals, 9), 13 (quadratics: multiplying and factoring, 15), 15 (irrational numbers, 2).
- **Khan Algebra 2** (32): unit 1 (polynomial arithmetic, 12), 2 (complex numbers, 9),
  3 (polynomial factorization, 9; 3-3 is missing from the archive, though its images exist).

## 2. Decisions proposed

### Courses and units
Three new courses in `library/courses.json`. Their units are Khan's, numbered as
Khan numbers them, listing only the units that have banks:

```
Khan Prealgebra: Unit 1: Factors and multiples, Unit 3: Ratios and rates,
                 Unit 6: Variables & expressions, Unit 8: Percent & rational number word problems
Khan Algebra 1:  Unit 1: Algebra foundations, Unit 2: Solving equations & inequalities,
                 Unit 6: Systems of equations, Unit 8: Functions, Unit 11: Exponents & radicals,
                 Unit 13: Quadratics: Multiplying & factoring, Unit 15: Irrational numbers
Khan Algebra 2:  Unit 1: Polynomial arithmetic, Unit 2: Complex numbers,
                 Unit 3: Polynomial factorization
```
(Alg1 0-1, "First introduction to algebra", goes in Unit 1.)

### One bank per Khan lesson
- `NAME` (the permanent id) is `ka1_02_06`, `ka2_03_07`, or `kpa_08_02`. `TITLE` is
  `Lesson 2-6: Number of solutions to equations`, so lessons sort in order within a unit.
- The code goes in three subpackages, `sheets/banks/khan_prealg/`, `khan_alg1/`, and
  `khan_alg2/`, with one module per lesson. Library discovery learns to look one level
  into a package that has no `NAME` of its own. (`literal/` still counts as a single
  bank.) This keeps 115 files out of `sheets/banks/`.
- **Types:** the lesson's distinct shapes, in Khan's order. For example, 2-6 has
  three: *one solution*, *no solution*, *infinitely many*. Or it has one type when
  every slot is the same template. For each lesson I propose the types, taken from
  its slots, and you approve them (see the checkpoints).

### Port the math, not the code
As with the Advanced Math banks: the old functions and the copied Khan items are the
**spec** (shapes, number ranges, niceness), not code to translate. No LaTeX survives.
Prompts and answers are plain Typst math built with `typmath.tx`, `fr`, and
`dfrac` at render time, and each bank has an independent `check` (substitution,
`same_value`, `simplest_form`, or reading a story back with `gen.read`). Copied Khan
items become generators drawn like them. They aren't ported word for word, and every
new problem has a checked answer.

### Old helpers → shared code
| Old (`LaTeXutils` etc.) | New |
|---|---|
| `random_signed`, `random_exclude`, `random_signed_exc` | `gen.signed`, `gen.except_`, `gen.signed_except` |
| `algterm`, `wrap_latex_math`, `dfrac`, `format_fraction` | `typmath.tx` / `fr` / `display` (sympy in, Typst out) |
| `get_*_names`, `Person` (pronouns) | `gen.NAMES`; stories use names, no pronouns (as in `adv_word`) |
| `make_cases`, `aligned` systems | a `system(eqs)` helper in Typst (aligned columns, as `systems.py` does) |
| `create_multiple_choice`, `randomizechoices` | a `gen.choices(...)` helper: shuffled with the bank's rng, letters A–D, key gives the letter **and** the choice |
| `Quadratic`, `class_poly_mult_box` | sympy and a Typst `table` area model |
| `reduce_sqrt`, `prime_factors`, `is_perfect_square` | `gen.prime_factors`, plus a small `radical` helper |
| `class_linear`, `class_graphs`, `school_graph`, TikZ | `sheets/graphs.py`: cetz grids, lines, points, piecewise graphs (Phase 5) |

### Sizes
Old `width` 0.5/1 → `half`/`full`. Old `height` (a fraction of a page, prompt
included) → work space, calibrated to what the Advanced Math port used:

| old height | 0.16–0.2 | 0.24 | 0.3–0.33 | 0.45–0.49 | 0.6+ |
|---|---|---|---|---|---|
| space | 0.75in | 1in | 1.25in | 1.75in | 2.25in |

Multiple-choice types need less work space, since the choices are the room. They
get 0.5in plus the choices.

### Multiple choice
`#choices` from the template, letters A–D, with the order shuffled by the bank's rng
so it's reproducible. Distractors are real mistakes, never noise (sign errors,
adding exponents instead of multiplying, and so on). The key prints `B. x = −4`.
`check` verifies that exactly one choice is right (or, for "choose all", the set
of right ones).

## 3. Phases and checkpoints

**Phase 0: Infrastructure.** Run the EXTENDING §7 baseline. Add the three courses,
package discovery, `gen.choices`, and the `system` display, with tests. Commit.

**Phase 1: Pilot, one lesson end to end.** Alg1 **2-6 Number of solutions** (multiple
choice, three types) and **2-1 Variables on both sides** (free response). Samples,
worksheet, key, and slides compiled and inspected. → **Checkpoint:** you approve the
conventions (types, answer forms, MC look, sizes) before I repeat them 100 times.

**Phase 2: Khan Algebra 1, no graphs**, a unit at a time (2, 1/0, 11, 13, 15, 6, then
the non-graph lessons of 8). Each lesson gets its own commit. → **Checkpoint per
unit:** proposed types plus 8–10 samples per type, with a list of errors found in
the old math.

**Phase 3: Khan Algebra 2** (units 1, 2, 3), the same way.

**Phase 4: Khan Prealgebra** (7 lessons; the hundred chart and factor-pair tables in Typst).

**Phase 5: Graphs.** `sheets/graphs.py` on cetz, then the TikZ lessons, then the
screenshot lessons as generated graphs: domain and range, functions or not,
extrema, positive/negative and increasing/decreasing intervals, average rate of
change, and inverses. The answers are checked from the function that drew the
graph.

**Phase 6: Docs and tests.** README/MANUAL sections per course, `:warnings` empty,
selftest over every Khan type, and byte-identical baselines for the existing banks.

## 4. Status
- Phase 0: three courses in `library/courses.json`; the library finds banks one
  level into a package (`sheets/banks/khan_alg1/`); `gen.written` (terms as written);
  `gen.lettered`/`in_order`/`choices_typst`/`with_letters` (multiple choice);
  `sheets/linear.py` (count, solve, and check one-variable linear equations);
  `tests/test_khan.py`. The existing tests pass, and the baselines are byte-identical.
- Phase 1: `ka1_02_01` (2 types, 4 templates each) and `ka1_02_06` (2 types by form,
  each drawing none/one/infinitely many equally; MC in a fixed natural order).
  300 draws per type, all verified. The worksheet, key, and slides compiled and
  were inspected. Approved 2026-10-25: the answers stay random (not
  balanced), the work-space sizes stand, and choices are stacked with the
  key reading "A. No solutions". Changed 2026-10-26: answers are balanced
  over a sheet (2-6, 6-12, 6-15), through gen.generator's balance.
- Khan Algebra 1, Unit 2: all eleven lessons (2-1 to 2-11, with 2-7a)
  built and committed; awaiting the unit checkpoint. New shared pieces:
  `sheets/ineq.py` (inequality and compound-inequality sets),
  `khan_alg1/numbers.py` (short decimals, simple fractions).

## 5. Unit 2 checkpoint (2026-10-25)
Approved: the types as built; 2-8 keeps the Advanced Math answer form,
y = -(u - 58)/(r + 17); 2-7a's key gives only the letters ("A, C").
Changed: 2-10's stories draw their letter at random instead of Khan's.

## 5b. Units 1 and 11 (approved 2026-10-25)
Unit 1: 0-1, 1-1. Unit 11: 11-1 to 11-9. New shared pieces: `sheets/radicals.py`
(simplest-form square roots), `check.same_power` (exact comparison of powers,
since 7^(-17) and 7^(-20) both look like 0 at random points).
Approved: 11-1 keeps Khan's form (7^2); 11-3's equivalents have one to three
right ("choose all that apply"); square roots to 400 and cube roots to 1728.

## 5c. Unit 13 (approved 2026-10-25)
All fifteen lessons. New shared pieces: `sheets/poly.py` (expanded and
factored forms, read back from the text), `khan_alg1/figures.py` (area
models and labeled rectangles in Typst), `khan_alg1/polybank.py`.
13-1 also serves Khan Algebra 2's 1-1 (the same set).
Approved: the factored key ((x + 3)^2; binomials by constant; (9 - x) (9 + x)
when the prompt leads with its number). Changed: an expansion whose binomials
lead with their numbers is keyed in ascending order, 25 - x^2 (13-6, 13-7;
13-4 and 13-5 ask for standard form); no negative lengths: 13-2's widths
are positive.

## 5d. Unit 15 (approved 2026-10-25)
15-1 and 15-2: rational or irrational, decided by computing the number
exactly (`khan_alg1/rationality.py`); statements about letters (15-2 Type 2)
are checked by trying sample rational and irrational values. Approved: a
rational letter may be zero (a · b can be either), as a deliberate trap.

## 5e. Unit 6 without graphs (approved 2026-10-25)
Twelve lessons (6-1, 6-3, 6-5 to 6-10, 6-12 to 6-15); 6-2, 6-4, and 6-11 draw
graphs and wait for Phase 5. New shared pieces: `khan_alg1/twovar.py`
(two-letter systems), `khan_alg1/stories.py` (stories whose model is a
system, checked from the words). Approved: answers "x = 2, y = -5" (the old
key's form); word problems keyed with the sentence only. Changed: 6-3 shows
a product unmultiplied, 0.5 s = 2 · 0.3 h, as the old key did.

## 5f. Unit 8 without graphs (approved 2026-10-26)
8-1, 8-4, 8-6, 8-7, 8-9, 8-10, 8-11, 8-13, 8-22. 8-2, 8-3, 8-5, 8-8, 8-12, and
8-14 to 8-21 draw graphs and wait for Phase 5. 8-6 and 8-22 key linear
answers in slope-intercept form (5/3 q - 10), as the teacher wants. 8-7 and 8-11 are
interpretation questions: their checks only confirm the key matches the
story. New: `khan_alg1/domains.py` (8-9, 8-10).

## 5g. Khan Algebra 2, Unit 1 (approved 2026-10-26)
All twelve lessons (`sheets/banks/khan_alg2/`). 1-1 is Algebra 1's 13-1. The
area models (1-7, 1-9) have positive lengths only; 1-11 and 1-12 key a
product that leads with its number in ascending order, as 13-6 does.
Approved: 1-2's rates as exact fractions (-9/4), not decimals.

## 5h. Khan Algebra 2, Unit 2 (approved 2026-10-26)
Eight lessons, 2-1 to 2-9 without 2-5 (the complex plane, a graph: Phase 5).
Shared helpers in `khan_alg2/cx.py` (a + bi written and read back, the form
check). 2-4's choices are Real, Purely imaginary, Complex: the standard
term, not Khan's bare "Imaginary" (the teacher's call). 3.75i + 7 is only
Complex, 7 is Real and Complex, -91i is Purely imaginary and Complex.
2-7 and 2-8 keep Khan's dot between the factors. Approved: 2-9 writes ±
where Khan wrote ∓ (a < 0): the same two numbers. All thirty of the old
2-9 items were checked: each has exactly one right choice.

## 5i. Khan Algebra 2, Unit 3 (approved 2026-10-26)
All nine lessons (3-1, 3-2, 3-4 to 3-10; the old app has no 3-3). 3-1's
rectangles are drawn (Algebra 1's labeled box), not pictures. `patterns.py`
builds U and V for 3-5 to 3-7; `poly.factored` now writes a power of the
letter before the binomials (3 x (x - 4) (x - 1)^2), and `poly.content`
works in several letters, so 3-6 and 3-7 are checked as completely
factored. 3-5's "none" expressions are checked to have no factor at all.
3-8 Type 2 builds a student's steps with at most one slip; the check finds
the first step not equal to the one before. 3-10's monkey is "it"; people
are named, no pronouns (approved). 3-10 keeps Khan's dot in its expressions.

## 5j. Khan Prealgebra (built 2026-10-26; awaiting its checkpoint)
All seven lessons (`sheets/banks/khan_pre/`, NAME kpa_UU_LL). 6-2 is
Algebra 1's 1-1 under this course. 1-3's hundred chart is drawn in Typst
(`khan_pre/numbers.py`); its choices are read back as sets and compared
with the shaded numbers. 1-1's tables are Typst tables with blank cells.
The 3-9, 8-1 and 8-2 stories use names, no pronouns; every percent in 8-1
and 8-2 is exact.

**To revisit:** random letters in word problems (2-10). The teacher wants
to look at this again later: Khan's letters (S for stops, F for flour)
name the thing counted.

**To revisit:** Khan's dot. 2-7 and 2-8 write 5i · (3 − 2i), against the
textbook's 5i(3 − 2i); 3-10 writes 24 · (1 − (1/3)^n)/(1 − 1/3). Kept for
now (2026-10-26).

## 6. Errors found in the old banks so far
- Prealgebra 8-1 (haircut): for 33% it keyed both 1/3 h and 0.33 h as right; they differ.
  Its decimals came from floating point (1 - 0.7 can print 0.30000000000000004).
- Prealgebra 8-2 no. 8 (iris blooms): asked "how many more" and keyed the total.
- Prealgebra 8-2 nos. 4, 5, 10, 12, 14-16: took 33% (67%) as exactly 1/3 (2/3), so the
  numbers didn't fit; no. 4 (hiking) could key 2 km as "33% less" than 2 km.
- Prealgebra 8-2 nos. 3, 9, 13: rounded the percent change to a tenth without saying so.
- Prealgebra 1-3: the hundred-chart choices lost their numbers ("Only the factors of").
- Alg1 2-2 no. 18: `2 − ½n = 3n + 16` has key `n = 4`. The solution is `n = −4`.
- Alg1 2-10 no. 9 (plumber): the key's part (a) was 65 + 28H >= 250; "no more than $250" is <=.
- Alg1 2-10 no. 10 (Sergei's flour) and others: no answers; part (b) now computed and checked.
- Alg1 2-2 no. 10: "15.3 + 1h = 1.3 - 1h" writes a coefficient of 1 (cosmetic).
- Alg1 1-1 no. 12 (a - x/b): the answer was drawn at random, apart from the expression; its key was always wrong.
- Alg1 11-1 no. 6: no exponent excluded, so b^m/b^m (b^0) could be drawn.
- Alg1 11-7, 11-8: the "not perfect squares" list held 8 and 12, so keys like 3 sqrt(8) weren't simplified.
- Alg1 13-8 (area-model templates): the stated GCF divided out only gcd(a, b, c), so 6 x^2 + 12 was said to have GCF 3, and the "GCF" could become 1.
- Alg1 13-15: (d x + e)^2 with d and e not reduced, so (2 x + 4)^2 was keyed as factored completely (it's 4 (x + 2)^2).
- Alg1 13-12 no. 8: asks for the width, labels the blank "Length =".
- Alg1 13-2: allowed a negative height (-6) for a rectangle; heights are positive now.
- Alg1 6-7: templates 4, 8, and 12 could make a choice keyed wrong eliminate a variable too (d = -a; q = -p; e = b d or a e = -b), so "choose 2" had three right.
- Alg1 6-10 no. 12: printed "(b) No" (right) but marked "Yes" as the correct choice.
- Alg1 6-15 no. 6: marked two choices correct (many solutions, right, and no solution).
- Alg1 8-6 templates 1, 5, 9, 13, 17: the key began "f(x) =" even for g and h.
- Alg1 8-7 no. 9: the height difference equals the month difference, muddling two choices.
- Alg1 2-6: the one generated slot (no. 30) was always "infinitely many".
- About 1,000 slots have no answer at all (`ANSWER TO nn GOES HERE`). The generators
  will supply checked answers for all of them.

(More will turn up as each answer is checked. I'll list them at each checkpoint.)
