# Extending This into a General Algebra Worksheet Builder

*A brief for an LLM coding assistant, or a person, picking this project up.*

## For the teacher: how to use this file

Open a session in this folder with a coding assistant and paste:

> Read `literal_sequence/EXTENDING.md`, then `README.md` and `MANUAL.md`, then
> the code they point to. I want to add **[problem family, e.g. "factoring
> trinomials"]**. Follow the phases in EXTENDING.md and stop at each
> checkpoint for my approval. Before you build any types, ask me how I
> classify these problems.

Name one problem family at a time. The checkpoints exist because the
classification and the answer forms are teaching decisions, and those are
yours to make.

---

## 1. What you are building

The goal is one application that makes **algebra worksheets, answer keys,
slide decks, and tests** for many kinds of problems. Every problem is
generated from a template, solved, and **machine-checked**, and it can be
reproduced from a seed. The literal-equation tool in this folder is the
first working instance. Generalize it; don't rewrite it.

The person you're working for is an Algebra 1 teacher. They know exactly
how they want problems classified and how answers should look, and they use
vim. The first job of every new feature is to produce correct materials for
their classroom. Ease of building comes second.

## 2. Read first, in this order

1. `README.md` and `MANUAL.md`: what exists and how it's used.
2. `PLAN.md`: the agreed plan; it overrides this file where they differ.
3. `sheets/check.py`: the Typst-to-sympy parser `to_sympy` and the numeric
   checker `holds`. `sheets/banks/literal/`: `TYPES` (the classification
   data), the templates (`D`, `need`, `t*_*`, `TEMPLATES`), `FORMULAS`,
   `solve`/`fmt`/`poly_tx`/`terms` (the answer formatter), `make` (solve +
   check), and `draw`.
4. `make_practice.py`, read top to bottom:
   - `draw_versions`, `build`: the API;
   - `worksheet`, `slides`: Typst output.
5. `mathsheet.py`: `App` holds all the state and key handling, and has no
   curses in it. `Screen` draws. `run` is the loop.
6. `gen_sequence.py`: the fixed lesson set, with hand-written worked steps
   that are checked step by step.
7. `tests/`: `test_mathsheet.py` and `screen_test.py`.

Then run everything in section 7 to record a baseline before you change
anything.

## 3. Non-negotiables

1. **Every answer is checked by machine before it's written,** and the check
   must not depend on the formatter. The current pattern: format the answer,
   parse the *formatted* text back with `to_sympy`, then substitute it into
   the original problem at random points. A family whose check can only pass
   or fail by re-deriving the answer the same way is not checked.
2. **The teacher owns the classification.** Ask before you invent types.
   When they list problem numbers per type, check programmatically that every
   problem lands in exactly one type, and report gaps and overlaps. (In this
   project four problems were unassigned; asking about them was correct.)
3. **A problem's type comes from how its template is built.** Each template
   must require exactly its type's moves, with `need()` guards against draws
   that drift into another type. The self-test cannot catch a wrong type.
   **Print samples of every type and read them** before you call a family
   done. In this project, one Type 1 template was producing Type 3 problems;
   only reading samples found it.
4. **Answers are written the way the teacher writes them.** Agree on
   conventions with examples, encode them in the family's formatter, and show
   the teacher samples.
5. **Reproducible:** the same arguments and seed must give byte-identical
   output. Draws use a dedicated `random.Random(seed)`; the numeric checks
   use the global `random`, so checking never changes what gets drawn. Each
   output file records the command that recreates it.
6. **No repeats** within a run or across versions, and no reuse of the
   lesson's own problems (`seen` / `original_prompts()`).
7. **Don't break what exists.** The lesson set and the literal-equation
   practice sets must come out byte-identical after any refactor (section 7).
8. **The TUI preview shows exactly what `:w` writes.** Same function, same
   arguments.
9. **The Typst look stays the teacher's:** the preamble comes from
   `templates/` (Name/Date/Ver header, the `question` environment
   with `points`, `choices`, `parts`). Reuse it; don't restyle it.

## 4. Where the code assumes literal equations

| Place | Assumption | Generalize to |
|---|---|---|
| `literal_common.TYPES`, `label()` | One family's types; "Type"/"Special Case" labels | Each family has its own type list |
| `make_practice.solve`, `make` | Answer = solve a linear (or squared) equation for `target` | `family.solve(problem)` and `family.check(problem)` |
| `make_practice.fmt` and helpers | Rational-expression answer formatting | Shared helper, with family-specific rules on top |
| `make` → `answer=f"{target} = {ans}"`; the `target` field | Every problem has an unknown | Family-defined fields; core uses only `prompt`, `answer`, `type`, and a dedupe key |
| `worksheet()`: "Solve each equation for the indicated variable."; `problem_tx` appends `; target` | Instructions and prompt layout | `family.instructions`, `family.prompt_typst(p)`, `family.answer_typst(p)` |
| `TYPE[...]["space"]` | Work space per type | Keep; every type gives a work-space height |
| `original_prompts()` reads `lesson_1-4_literal_seq_bank.json` | One lesson's bank | Per-family exclusion list (optional) |
| `FORMULAS`, `--style mixed/letters/formulas` | A pool of real-world formulas | Optional per-family pools; the family declares its styles |
| `mathsheet.pretty()`, `"for {target}"`, title bar, help text "Types 1-11…" | Literal-equation display | `family.prompt_text(p)`, `answer_text(p)`; help built from the family list |
| `mathsheet` hints: "Look for / The move" | Per-type teaching text | Keep as optional type fields |
| `DEFAULTS["title"]`, `name` | Literal-equation names | Per family, or set by the user |

## 5. Target design

Grow the folder into a package. Keep the existing entry points working
until the teacher agrees to move them.

```
algebra_sheets/
  core/
    draw.py        versions, seeds, the seen-set, mixes across families
    typst.py       worksheet, key, and slides from a list of problems
    check.py       to_sympy, numeric checks, shared answer formatting
    cli.py         make_sheets.py: today's command-line flags, plus families
    tui.py         today's App/Screen, made family-aware
  families/
    literal/       today's templates, formulas, types, solve, format
    linear/        (example new family)
    factoring/     ...
```

A family is a module that exposes:

```python
FAMILY = dict(
    key="factoring",
    title="Factoring",
    instructions="Factor completely.",
    types=[dict(key="1", title="Greatest Common Factor", look=..., move=..., space=1.0), ...],
    styles=("mixed",),                        # optional style choices
)

def draw(type_key, rng, style, seen) -> dict      # returns a problem; raises Redraw to retry
def check(problem) -> None                        # raises if the answer is wrong (independent of formatting)
def prompt_typst(problem) -> str                  # Typst markup for the worksheet
def answer_typst(problem) -> str
def prompt_text(problem) -> str                   # plain/Unicode text for the TUI
def answer_text(problem) -> str
```

A problem is a dict with at least `family`, `type`, `prompt`, `answer`,
`key` (for no-repeat checks), and `source`. Families may add fields (today's
`target`).

**Mixing families on one sheet** (tests need this): extend `--mix` to
`FAMILY/TYPE:COUNT`, for example `--mix literal/3:4 factoring/2:3`. A bare
`TYPE:COUNT` keeps meaning the default family, so old commands still work.
Each family becomes a section with its own instructions line.

**Tests vs. practice:** for quizzes and tests, versions should be
*parallel*: position k uses the same type, and preferably the same
template, in every version. Then versions differ only in letters and
numbers. Add per-problem points (the `question` environment already takes
`points:`) and optionally multiple-choice distractors (`choices`).
Distractors should come from real mistakes (sign errors, dividing by the
wrong coefficient), never random noise. Get the teacher's approval on
distractor rules.

## 6. Phases and checkpoints

Stop for the teacher's approval at every **checkpoint**.

**Phase 0: Baseline.** Run section 7. Save the outputs of these commands in
a scratch folder (not in the project):

```sh
python3 gen_sequence.py                                  # then copy *.typ and *.json
python3 make_practice.py --mix all:2 --versions 2 --seed 12 --no-compile --out /tmp/base_a
python3 make_practice.py --mix all:1 --shuffle --style formulas --seed 7 --no-compile --out /tmp/base_b
```

**Phase 1: Separate core from family, with no behavior change.** Move code
into the design in section 5, with literal equations as the only family.
Done when every baseline is byte-identical (`diff -r`), the self-test
passes, and the TUI tests pass. Commit only after this. → **Checkpoint:**
show the teacher the new layout and confirm the old commands still work.

**Phase 2: Design the new family with the teacher.** Ask:
- Which textbook section or worksheet the problems come from, and whether
  there's a screenshot or a list of problems.
- How they classify them: types, order, and special cases. Offer a proposal
  if they want one, but the decision is theirs.
- What a finished answer looks like, with 3–5 examples. Which forms are
  acceptable, and which is printed in the key.
- Number rules: integer answers only? sizes? negatives allowed? fractions?
- Which courses the family belongs to, and in which unit of each (see
  section 8a). Ask whether any types belong to a different course than the
  rest: a family often starts in Algebra 1 and finishes in Algebra 2.

Write the types down as data. → **Checkpoint:** the teacher approves the
types and the answer conventions.

**Phase 3: Build the family.** For each type, write 3–6 templates that
require its moves (see section 8 for techniques). Write `check` before the
formatter. Add a self-test that draws hundreds per type. Then print 8–10
samples per type, with answers, and read them yourself for type drift,
ugly forms, and degenerate cases. → **Checkpoint:** send the teacher those
samples. Expect to adjust.

**Phase 4: Output and TUI.** Worksheets, keys, and slides through the
shared Typst code. Compile them and look at the PDFs (render pages to PNG
and view them). A generator module in `sheets/banks/` appears in the banks
pane on its own; tag it with its courses (section 8a) so it shows in the
right ones, and check `:warnings` is empty. Make the help text and hints
family-aware where they need to be. Add tests alongside
`tests/test_mathsheet.py`. → **Checkpoint:** a sample set of each output.

**Phase 5: Tests and mixed sets** (when asked): parallel versions, points,
sections per family, multiple choice.

## 7. Checks to run, every time

```sh
python3 make_practice.py --selftest 100     # every type of every family + formula pools
python3 tests/test_mathsheet.py              # TUI state and keys, no terminal
python3 tests/test_library.py                # the library: banks, courses.json, tags
python3 tests/screen_test.py 80 24 ":mix all:1\r" wait3 @ "?" @   # real screen (needs pyte)
TT=vt100 python3 tests/screen_test.py 80 24 wait1 @                # a terminal without color
python3 gen_sequence.py                     # lesson set: answers and worked steps
```

Also compile one set and look at the rendered pages. Don't test `:open`; it
launches a PDF viewer on the teacher's desktop.

## 8. Techniques for building problem families

**Build backward from the answer when answers must be nice.** For a numeric
family (linear equations, systems, factoring), choose the answer first,
then build the problem around it:
- *Linear equation:* pick x = 4, then a = 3, b = −5, giving 3x − 5 = 7.
- *Systems:* pick (x, y), then the coefficients, then compute the constants.
- *Factoring:* pick the factors (2x + 3)(x − 4), then expand them to get the
  prompt.

That guarantees integer answers and controls difficulty. Literal equations
didn't need this, because their answers are expressions.

**Make the check independent of how the answer was produced.**
- *Equation solving:* substitute the parsed answer back into the problem.
- *Factoring:* `expand(answer) == prompt`, **plus** each factor is
  irreducible over the integers and the GCF is pulled out. Equal alone isn't
  enough: `2(x² + 3x + 2)` equals the prompt but isn't factored completely.
- *Simplifying* (exponents, radicals, rational expressions): equivalence
  **plus** a family-specific "simplest form" test (no negative exponents,
  no radical in a denominator, and so on). Agree on the rules with the
  teacher.
- *Inequalities:* compare the solution set at sample points on both sides of
  the boundary, and check the direction of the sign, especially after
  dividing by a negative. That's a natural special case.

**Guard against degenerate draws** with `need()`: zero coefficients, terms
that cancel, a coefficient of 1 printed as `1x`, answers that are
accidentally constant, systems with no solution or infinitely many (unless
that's the type), and duplicate letters.

**Special cases are types.** A move that students miss (a negative
coefficient, an extraneous root, a flipped inequality) gets its own type, so
it can be practiced and shown separately.

**Ideas for families, roughly in order of how easy they are to build:**

| Family | Types (suggested; let the teacher decide) | Check |
|---|---|---|
| One-variable linear | one-step, two-step, distribute, variable on both sides, fractions; special: no solution / identity | substitution; identity cases are special |
| Linear inequalities | as above; special: dividing by a negative | sample points |
| Evaluating expressions and functions | order of operations, substitution, function notation | exact arithmetic |
| Slope and line equations | slope from points; slope-intercept / point-slope / standard form | both points satisfy the line |
| Systems of two | substitution-ready, elimination, elimination with scaling; special: none / infinite | substitution |
| Exponent rules | product, quotient, power, zero and negative | equivalence + form rules |
| Factoring | GCF, x²+bx+c, ax²+bx+c, difference of squares, perfect squares, grouping | expand + irreducible + GCF |
| Quadratics | factoring, square roots, quadratic formula; special: no real roots | substitution |
| Word problems | needs context templates and units | hardest; build last |

The parent folders already have related material: answer-key instructions
(`../../answer_key_instructions.md`), word-problem notes
(`../../savvas_word_problems_1-4.md`), and picker scripts
(`../../modeling_picker.py`, `../../loader_picker.py`). Read them before
designing word-problem or test features, and ask the teacher what they're
for rather than guessing.

## 8a. Tagging a bank with its courses

Courses are tags, not folders (`sheets/library.py` has the details). A
generator module declares them at the top, next to `TITLE`:

```python
COURSES = {"Algebra 1": "Equations", "Algebra 2": None}   # course -> unit, or None
COURSES = ["Algebra 2", "Precalculus"]                    # or: no units
```

A bank file does the same with `"courses"`. A type that belongs elsewhere
carries its own `courses` (in `TYPES` for a generator, in `"types"` for a
bank file), which replaces the bank's for that type only.

- Course titles and unit names must match `courses.json` exactly (the
  built-in one is `banks/courses.json`; the teacher's library may have its
  own). Don't invent a course or unit: ask the teacher, and add it to
  `courses.json` if they agree.
- A bank with no `COURSES` shows only under *All banks*. That's a fine
  state while a family is being built.
- Check with `:rescan` and `:warnings` in the app, or
  `python3 -c "from sheets import library; print(library.current().warnings)"`.
- Generators stay in `sheets/banks/`; the library folder holds only JSON.
  A shared folder must never be able to run code.

## 9. Lessons learned in this project

- **Typst and sympy read fractions differently.** In Typst, `a/b c` means
  (a/b)·c, and `1/3 B h` means (1/3)·B·h. Build every fraction with `fr()`,
  which adds the parentheses.
- **sympy reads `m(x + 2)` as a function call.** `to_sympy` rewrites
  `letter(` as `letter*(`, keeps `ell` as one symbol, and passes symbols
  named `I`, `E`, `S`, `pi` explicitly so they don't become sympy constants.
- **sympy comparisons return sympy booleans,** and those can't be compared
  in a Python sort key; wrap them in `bool()`.
- **Answer forms are teaching decisions.** Pulling numbers out of numerators
  produced `2(2M − 1)` where the teacher writes `4M − 2`. Letter factors
  (`y(b + 8)`) and numbers in denominators (`2(ℓ + w)`) were wanted.
  Constants go where the problem wrote them (`1 + rt`, not `rt + 1`). Expect
  more choices like these in every family.
- **Correct isn't the same as well-classified.** Every check passed while a
  template was making problems of the wrong type.
- **Curses on real terminals:** `curs_set` and colors can fail (`TERM=vt100`);
  wrap both. Test with the `pyte` harness at 80×24 and at a larger size. Set
  `ESCDELAY` so Esc feels instant.
- **Separate the state from the drawing** (`App` vs `Screen`) so the key
  handling can be tested without a terminal.

## 10. Definition of done for a new family

- [ ] Types approved by the teacher; coverage checked by code.
- [ ] 3+ templates per type, each guarded against drifting into another type.
- [ ] `check` passes for hundreds of draws per type and doesn't depend on the formatter.
- [ ] Samples per type read by you and approved by the teacher.
- [ ] Worksheet, key, and slides compile; rendered pages inspected.
- [ ] TUI: family selectable, preview correct, help and hints updated, tests added.
- [ ] Tagged with the teacher's courses and units (types too, where they differ); `:warnings` empty.
- [ ] Byte-identical baselines for everything that existed before.
- [ ] README and MANUAL updated: new family, its types, and its answer conventions.
