# Literal Equations by Type

Algebra 1 materials for solving literal equations (formulas) for a given
variable. The equations are sorted into eleven **types** by the first move
each one needs, plus two **special cases**. There are two parts:

1. **The lesson set:** 50 equations in sequence, with a worksheet, an answer
   key, a slide deck, a worked-examples guide, and a reference sheet that
   solves every equation for every variable.
2. **A practice generator:** new problems of whatever types you choose, as
   many versions as you like. It writes a worksheet, an answer key, and a
   slide deck for each version. You can run it from the command line or from
   a terminal app with vim keys.

Every answer, and every line of every worked example, is checked
numerically with sympy before anything is written.

## Quick start

```sh
# Rebuild the lesson set
python3 gen_sequence.py [--class NAME] [--groups G ...] && (cd lesson_1-4 && for f in *.typ; do typst compile "$f"; done)

# Practice sets from the command line (3f = real formulas of Type 3)
python3 make_practice.py --mix 3:6 3f:2 8:4 A:2 --versions 3 --seed 12

# Systems of three equations (another bank: name it before the entry)
python3 make_practice.py --mix systems/1:2 systems/4:4 systems/A:1 --versions 2

# Build and edit a sheet interactively: add by type, then Tab to the sheet to
# reroll, resize, edit, and move problems (press ? inside for keys)
python3 practice_tui.py
```

The practice files go into `practice/`. See [MANUAL.md](MANUAL.md) for the
details.

## The types

| Key | Type | Lesson problems |
|---|---|---|
| 1 | One Step | 1–8 |
| 2 | Add or Subtract, Then Divide | 9–12 |
| 3 | Clear One Denominator | 13–18 |
| 4 | Distribute First | 19–24 |
| 5 | Clear a Denominator, Then Distribute | 25–27 |
| 6 | Clear Two Denominators | 28–29 |
| 7 | Factor Out, Then Divide | 30–31 |
| 8 | Gather, Factor Out, Divide | 32–35 |
| 9 | Distribute, Gather, Factor Out, Divide | 36–38 |
| 10 | Clear Single-Term Denominators, Then Solve | 39–41 |
| 11 | Clear a Multi-Term Denominator | 42–45 |
| A | Special Case: Watch the Sign | 46–47 |
| B | Special Case: Finish with a Square Root | 48–50 |

### Systems of three equations

A second family, in the `systems` bank, sorted the same way: by the first move.

| Key | Type | Look for |
|---|---|---|
| 1 | Back-Substitute | One equation has a single variable, another just two |
| 2 | Substitute First | One equation is already solved for a variable |
| 3 | One Variable Missing | One equation has only two of the variables |
| 4 | Eliminate | Every variable everywhere; some coefficients are 1 or −1 |
| 5 | Eliminate and Scale | Every variable everywhere; no coefficient is 1 or −1 |
| A | Special Case: No Solution | Left sides combine; constants don't |
| B | Special Case: Infinitely Many Solutions | One equation is a combination of the other two |

Solutions are integers from −9 to 9, coefficients at most 7 (or 12 in a
combined equation), constants at most 60, and no equation has a common
factor. Answers are ordered triples, `(2, −1, 3)`, or the words *no solution*
or *infinitely many solutions*. Each system is half width with 2.5in of work
space, its terms lined up in columns.

## Files

| File | What it is |
|---|---|
| `sheets/` | The shared package: `sheet.py` (the worksheet document), `edit.py` (changes to a sheet), `writer.py` (worksheet, key, and slide Typst), `check.py` (Typst-to-sympy parsing and numeric checks), `typst.py` (the Typst preambles), `banks/` (the bank interface, the literal-equation generator, and fixed banks) |
| `sheets/banks/systems.py` | The systems-of-three-equations bank: types, templates, the sympy check, and the aligned Typst layout |
| `sheets/banks/literal/` | The literal-equation bank: `types.py`, `templates.py`, `formulas.py`, `answers.py` (solver and answer formatter), and drawing in `__init__.py` |
| `gen_sequence.py` | Builds the lesson set (`lesson_1-4_literal_seq_*`) |
| `make_practice.py` | Practice generator: drafts a sheet from `--mix`/`--groups`/`--seed`, writes it, and the command line |
| `practice_tui.py` | Terminal worksheet editor (vim keys) |
| `tests/` | `test_tui_keys.py` (no terminal needed) and `screen_test.py` (draws the real screen; needs `pyte`) |
| `banks/` | Fixed banks: written problems as JSON, browsed and added in the terminal app (`lesson_1-4.json` is the lesson's fifty, written by `gen_sequence.py`) |
| `lesson_1-4/` | Output of `gen_sequence.py`: the lesson set: worksheet, key, slides, guide, all-solutions reference, JSON bank |
| `templates/` | Typst style headers shared by every worksheet and slide deck |
| `practice/` | Default output folder for practice sets |
| `PLAN.md` | The agreed plan for turning this into a general worksheet editor |
| `EXTENDING.md` | A brief for an LLM (or a person) turning this into a general worksheet builder |

## Requirements

- Python 3.10+ with **sympy** (tested with 1.13).
- **Typst** 0.15 to compile PDFs. Without it, the `.typ` files are still written.
- The styles live in `templates/` and are read at run time: practice
  worksheets use `refined_template.typ`; slides use `mixed_review_slides.typ`;
  the lesson set still uses `mixed_review_v1.typ`.
- Optional: `pyte`, only for `tests/screen_test.py`.

## Reproducibility

Each practice set is saved as `NAME.sheet.json`, which holds every problem
of every version; `python3 make_practice.py --sheet NAME.sheet.json` prints
it again exactly. The same settings and seed also always draft the same
sheet: each file begins with the command that does it, for example
`// Generated by: python3 make_practice.py --mix 3:6 8:4 A:2 --versions 2 --seed 12`,
and `practice_tui.py` opens the sheet to edit it.
