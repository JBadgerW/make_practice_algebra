# Plan: from practice generator to a general worksheet editor

Agreed with the teacher on 2026-10-09. Read this alongside `EXTENDING.md`,
which still holds for the non-negotiables (section 3) and the checks to run
(section 7). Where the two disagree, this file wins.

## Goals

1. Reroll one problem, one section, or the whole sheet. A sheet-wide seed
   matters less than that.
2. A preview that looks like the page: one or two columns, bold section
   headers, italic instructions, and room to scroll, edit, and reroll there.
3. Groups become **sections**: a section can hold any kind of problem.
4. Each problem carries its **width** (`half` or `full`) and its **work
   space** as an absolute length (`0.75in`, `1.5in`, `2in`).
5. Typst output follows `templates/refined_template.typ`: a header, a
   sheet-wide instructions block, `section-head(instructions: ...)`, and one
   `#grid` per row (two half-width problems, or one full-width problem).
   Problems of a section are not blocked together.
6. **Banks** of problems and problem types, browsed in the left pane and
   imported into the sheet.

## The central change: store the sheet, not the recipe

Today a worksheet is `mix + seed + groups -> draw`. From now on the
**worksheet document** is what gets saved; generators only fill or refill
its slots.

```python
Sheet = dict(class_="Algebra 1", title=..., instructions="Solve each equation for ...",
             versions=1, sections=[Section, ...])

Section = dict(title="Type 1: One Step",     # empty -> no header
               instructions=None,            # italic block under the header
               items=[Item, ...])

Item = dict(
    source=dict(bank="literal", type="3"),   # or dict(bank="lesson_1-4", id="17")
    seed=482913,          # this problem's own seed; rerolling gives it a new one
    width="half",         # "half" | "full"; default from the type
    space="1.5in",        # absolute work space; default from the type
    prompt=..., answer=..., target=...,      # the concrete problem, cached
    edited=False,         # set when the teacher edits it by hand
    status="checked",     # checked | unchecked | failed (see below)
)
```

- Reopening a sheet gives exactly the same problems, even after templates
  change, because the concrete problems are stored.
- The command line can still draft a first sheet from `--mix` and a seed.

## Decisions

1. **Versions are parallel.** Version k rerolls every *generated* problem
   in its slot (same bank, same type). Hand-edited problems and fixed-bank
   problems are the same in every version.
2. **Unchecked answers are allowed but visible.** Each item has a status:

   | Status | Meaning | Preview | `:w` |
   |---|---|---|---|
   | checked | a checker ran and the answer is right | nothing | writes |
   | unchecked | no checker could run | dim `?` | writes, reports the count |
   | failed | a checker ran and the answer is wrong | red `✗` | writes, warns loudly |

   Editing a prompt that the family can solve re-solves and re-checks it.
   Editing an answer by hand checks it by substitution. Something the
   family can't solve keeps the teacher's answer, marked unchecked. Fixed
   banks that name a checker family are checked. Nothing is ever marked on
   the PDF.
3. **Files are JSON** for now (sheets and fixed banks).
4. **Literal "style" goes away.** Each literal type has separate *letters*
   and *formulas* entries. A formulas entry draws from the fixed formula
   pool, so it behaves like a fixed bank: a reroll picks another unused
   formula, and the pool can run out. Types without formulas get only a
   letters entry.

## Typst layout

- `first-page-header`, then the sheet's `instructions-block`.
- Per section: `#section-head(instructions: ...)[title]` when it has a title.
- Items flow in order. Two consecutive `half` items share
  `#grid(columns: (1fr, 1fr), column-gutter: 1em)`; a `full` item gets its own
  `#grid`. Each item is `question(space-below: <space>)`, numbered through
  the whole sheet.
- A half item followed by a full item, or ending a section, sits alone with
  an empty right cell. Order never changes silently; a `:pack` command may
  pull the next half item up.
- The key is the same layout with answers in red. Slides: a slide per
  section header, then problem and answer slides. Type hint slides
  (Look for / The move) only when a section is all one type.

## Banks

| Kind | What | Reroll |
|---|---|---|
| Generator bank | a Python module (today's literal templates) | new seed, same type |
| Fixed bank | a JSON list of written problems (lesson 1-4, textbook sets) | another unused problem of the same type |

A bank declares its types (`title`, default `width`, default `space`,
default section `instructions`, optional `look`/`move`) and provides
`check(problem)`, `typst(problem)`, and `text(problem)`. A fixed bank may
name a checker family. The lesson's `lesson_1-4_literal_seq_bank.json`
becomes the first fixed bank.

## Library and courses

Decided with the teacher on 2026-10-10. A **course** (Algebra 1, Algebra 2,
Precalculus, ...) is a tag on a bank, not a folder, since one bank fits
several courses. Courses only decide what the banks pane shows; sheets never
depend on them, and a sheet may mix courses.

- **Where:** generators in `sheets/banks/` (found automatically, never from
  the library: a shared folder mustn't run code); the built-in fixed banks
  and starter `courses.json` in `banks/`; the teacher's own banks (any
  `*.json`, any subfolder) and `courses.json` in a library folder set in
  `~/.config/mathsheet/config.json` (default `~/Documents/mathsheet-library`).
  A library bank replaces a built-in one of the same name.
- **courses.json** lists the courses in order, each with its units in order.
  The library's adds courses or replaces one of the same title.
- **Tags:** `"courses": {"Algebra 1": "Equations", "Algebra 2": null}` (or a
  list) on a bank (`COURSES` in a generator); a type's own `"courses"`
  replaces the bank's for that type. Unknown courses and units are warnings
  with a suggestion, never errors.
- **Scanning:** every start, and `:rescan`. It takes under a millisecond
  past loading sympy, so there is no cache to go stale.
- **The app:** a course row atop the banks pane (`h`/`l`, ending in All
  banks), `:course NAME` with Tab completion, banks under unit headings in
  the course's order (no unit: Other, last), `:library DIR`, `/` searches
  the course. The sheet stores its course; a new sheet starts in the last
  one used. The class name follows the course while it is the default or
  the previous course's title. A sheet whose bank is gone still opens and
  prints, its problems marked.

## TUI

**Left pane, the bank browser:** a tree `Bank > Type > (items)`. `l` or
Enter adds a problem of that type to the section under the preview cursor;
`5l` adds five. Each type shows how many of its problems are on the sheet.
`/` searches every bank.

**Right pane, the sheet:** stays beside the bank browser; `^W o` widens it
to the whole screen and back. Header block, bold section
headers, italic instructions (dim where italics aren't supported), one or
two columns, work space as blank rows (about one row per 1/4 in; `zs`
toggles compact), and estimated page breaks.

| Keys | Action |
|---|---|
| `j k` / `h l` | next/previous problem; left/right column |
| `]] [[` | next/previous section |
| `r` / `R` / `:reroll` | reroll problem (`3r`) / section / sheet |
| `W` | half/full width |
| `+ -` | work space +/-0.25in (`:space 2in`) |
| `i` | edit the prompt inline; re-solved and re-checked |
| `dd yy p P` | cut, copy, paste problems (across sections) |
| `J K` | move a problem down/up |
| `o O` | new section below/above |
| `cS` `cI` | rename section / edit its instructions |
| `zM zR` | fold to a section outline / unfold |
| `za`, `gt gT` | answers on/off, versions |
| `u ^R .` | undo, redo, repeat |

`:w` writes the sheet JSON and the PDFs; `:e` reopens a sheet. The preview
and `:w` still use the same data and the same functions.

## Phases (stop for the teacher at each checkpoint)

0. ✅ **Baseline.** Save today's outputs (`EXTENDING.md` section 6).
1. ✅ **Package split, no behavior change.** A core package plus
   `banks/literal`; old commands give byte-identical output.
2. ✅ **Document model and new writer.** `Sheet`/`Section`/`Item`,
   `.sheet.json`, a reader for old practice JSON, the refined-template
   writer, statuses. `make_practice.py --mix ...` drafts a sheet. Output
   changes on purpose here: compile and inspect the PDFs.
   Done as: `sheets/sheet.py`, `sheets/writer.py`, the bank interface in
   `sheets/banks/__init__.py`. Key answers float in the work space so key and
   sheet break pages alike. Lesson 1-4 output is still byte-identical (it
   keeps the old template until it becomes a fixed bank in phase 4).
3. ✅ **Preview becomes the editor.** Rendering, cursor, rerolls, width and
   space, sections, inline editing, tests.
   Done as: `sheets/edit.py` (every change, no UI) and a rewritten
   `mathsheet.py`. Departures from the plan above: `l` adds to the type's
   own section and `L` adds at the sheet cursor; `yy` + `p` draws new
   problems rather than duplicating; the groups pane is gone (`:groups`,
   `:join`, `J`/`K` on titles, and `zM` cover it).
4. ✅ **Bank browser.** Tree, import, fixed banks, lesson 1-4 as a bank.
   Done as: `sheets/banks/fixed.py` (JSON banks in `banks/`, with an
   optional checker family), a registry in `sheets/banks/__init__.py`, and a
   tree in the left pane. Banks share sections and the no-repeat rule by
   family. Not yet: fixed banks on the `make_practice.py` command line.
5. ✅ **A second family**: systems of three equations (`sheets/banks/systems.py`).
   Decided with the teacher on 2026-10-09: types by first move (1
   Back-Substitute, 2 Substitute First, 3 One Variable Missing, 4 Eliminate,
   5 Eliminate and Scale; specials A No Solution, B Infinitely Many);
   answers as `(x, y, z)` or words; integer solutions −9..9 with
   coefficients to 7 and constants to 60; half width, 2.5in. Checked by
   solving again with sympy; 1400 samples checked for their type's structure.
   Also: `--mix BANK/ENTRY:N` on the command line.
6. **Library and courses** (see above).
   1. ✅ Library core: `sheets/library.py` (config, scan, courses.json, tags,
      warnings), generators found automatically, tags on the three banks,
      `tests/test_library.py`. No change on screen yet.
   2. ✅ The app: course row, units, `:course`, `:rescan`, `:library`, class
      name, the sheet's course, missing banks (a stand-in shows, edits, and
      prints their problems from the sheet, through the family the problem
      records; `!` marks them), `:warnings`.
   3. ✅ Docs: MANUAL (*Courses and the library*, bank and courses.json
      formats, commands, troubleshooting), tagging in EXTENDING.md (8a),
      README; `gen_sequence.py` writes Lesson 1-4's course tag.
