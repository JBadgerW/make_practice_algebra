# Manual

1. [The lesson set](#1-the-lesson-set)
2. [Making practice sets from the command line](#2-making-practice-sets-from-the-command-line)
3. [mathsheet, the terminal app](#3-mathsheet-the-terminal-app)
4. [What gets written](#4-what-gets-written)
5. [Adding problems](#5-adding-problems)
6. [Checking your changes](#6-checking-your-changes)
7. [Troubleshooting](#7-troubleshooting)

## 1. The lesson set

`gen_sequence.py` holds the 50 lesson equations, the worked steps for the
guide, and the rules about which problems get worked out. Run it, then
compile:

```sh
python3 gen_sequence.py [--class NAME] [--groups G ...] && (cd lesson_1-4 && for f in *.typ; do typst compile "$f"; done)
```

`--groups` reorders, mixes, and renames the sections of the worksheet, key,
and slides, with the same syntax as `make_practice.py` (see section 2):
`python3 gen_sequence.py --groups 9 8 3+4="Warm-up" 1 2`. Problems are numbered
in print order, so with a custom layout the numbers differ from the lesson
numbers. A mixed group is shuffled; `--seed N` (default 0) picks the shuffle.
The guide and all-solutions reference always stay in lesson order and lesson
numbers. Without `--groups`, the output is the same as before.

| Output | Contents |
|---|---|
| `lesson_1-4_literal_seq_worksheet` | Problems 1–50 under type headings, each with a one-line hint |
| `lesson_1-4_literal_seq_key` | The same, with answers in red |
| `lesson_1-4_literal_seq_slides` | A title slide per type, then a problem slide and an answer slide; the worked examples get step-by-step answer slides |
| `lesson_1-4_literal_seq_guide` | For each type: Look for, The move, and a worked example; the special cases are worked in full, with a "Watch out" note |
| `lesson_1-4_literal_seq_all_solutions` | The textbook equations and the 50 lesson equations, each solved for every variable |
| `lesson_1-4_literal_seq_bank.json` | Everything above as data |
| `../banks/lesson_1-4.json` | The fifty as a fixed bank for the terminal app (section 5) |

The script stops with an error if an answer or a worked step fails its
numeric check. It also stops if the types don't cover problems 1–50 exactly
once, in order.

**Editing the lesson.** The type names, hints, problem ranges, and worksheet
spacing are in `TYPES` in `sheets/banks/literal/types.py`. The equations are in `EQ`,
and the worked steps are in `STEPS`, `ALT`, `NOTICE`, and `PITFALL`, all in
`gen_sequence.py`. A worked step is `("equation", "note")`. The first
equation must be the problem itself, and the last must be `target = answer`.

## 2. Making practice sets from the command line

```sh
python3 make_practice.py [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--mix ENTRY:COUNT ...` | How many problems of each entry. `1`–`11`, `A`, `B` are made-up equations of that type; `1f`, `3f`, `Bf`, ... are real formulas of that type. `all` means every made-up entry and `allf` every formulas entry. Repeated entries add up: `all:1 3:2` gives three of Type 3 and one of everything else. | `all:2` |
| `--versions N` | Number of parallel versions: each problem is redrawn in its own slot, so version 2's problem 5 is the same type as version 1's | 1 |
| `--seed S` | Same seed → same sheet | random (printed) |
| `--shuffle` | One section with every problem shuffled, no headings | grouped |
| `--groups G ...` | Order and combine the headed sections (see below) | sequence order |
| `--title TEXT` | Title on the worksheet and slides | Literal Equations Practice |
| `--class NAME` | Class name in the worksheet and slide header | Algebra 1 |
| `--out DIR` | Output folder: `~` is home; a relative path starts in the current folder | `practice` |
| `--name NAME` | File prefix | `literal_practice` |
| `--sheet FILE` | Print a saved `.sheet.json` again, or convert an older `NAME_v1.json` set (with its other versions) and print it in the current style | |
| `--no-compile` | Write `.typ` files only | compile |
| `--selftest N` | Draw N problems of every type, check them all, then check every formula | |

Examples:

```sh
# Three equal-difficulty quiz versions
python3 make_practice.py --mix 2:2 3:2 4:2 8:2 A:1 --versions 3 --title "Quiz 1-4" --name quiz_1-4

# Mixed review, interleaved
python3 make_practice.py --mix all:1 --shuffle

# Warm-up from real formulas
python3 make_practice.py --mix 1f:4 3f:4 Bf:2
```

### Ordering and combining groups

Each headed section of a worksheet is a *group*. By default every type with
problems is its own group, in the lesson's sequence. `--groups` sets the print
order, and joins types into one mixed group with `+`:

```sh
# Hardest first, so the class works those together; easier ones for home
python3 make_practice.py --mix 3:3 4:3 8:3 9:3 --groups 9 8 3 4

# Types 3 and 4 mixed together under a heading you choose
python3 make_practice.py --mix 3:3 4:3 8:3 --groups 3+4="Warm-up" 8
```

- A mixed group's problems are shuffled together, and numbering carries on
  from group to group. Its default heading is *Mixed Practice (3, 4)*.
- `=Name` replaces the heading of any group, mixed or not.
- Types you leave out of `--groups` follow at the end in sequence order, and
  types with no problems are ignored. A type can appear only once.
- `--shuffle` ignores groups: everything is one mixed list.
- A type's made-up and formulas entries (`3` and `3f`) share its group.
- On the slides, a single-type group gets its usual title slide. A mixed group
  gets one title slide listing every type's *Look for* and *The move*.
- The same seed draws the same problems whatever the group order, apart from
  the shuffling inside mixed groups. Adding versions never changes version 1.

**Guarantees:**
- Problems never repeat within a run, across versions, or with the 50 lesson
  problems. The one exception: a formulas entry with a small pool (Type 9 has
  one formula the lesson doesn't use) repeats its formula in later versions
  rather than fail. Type 7's only formula is a lesson problem, so there is no `7f`.
- Every answer is solved by sympy, written out in classroom form, and checked
  numerically.
- **Answer forms:**
  - Answers come as a single fraction, with as few minus signs as possible.
  - Terms are listed in the order they appear in the problem.
  - Common letter factors are pulled out: `y(b + 8)`.
  - Numbers are pulled out only in denominators: `2(ℓ + w)`.
  - A student's correct answer may still be in a different but equivalent
    form.

### Systems of three equations

`--mix systems/4:3` draws from the `systems` bank (`systems/all:1` is one of
each type); it mixes with literal entries on one sheet, each family in its own
sections with its own instructions. Problems are built backward from an
integer solution, then solved again by sympy to check the key. Every type is
guarded so it needs its own move: a Type 5 never has a coefficient of 1 or −1,
and no equation has a common factor that would turn it into a Type 4. In the
terminal app, `i` edits a system as `eq1 ; eq2 ; eq3` (solved again), and `A`
takes `(x, y, z)`, `no solution`, or `infinitely many solutions`.

## 3. mathsheet, the terminal app

```sh
python3 mathsheet.py                                      # start empty
python3 mathsheet.py --mix 3:6 8:4 --seed 12              # start from a draft
python3 mathsheet.py practice/literal_practice.sheet.json # open a sheet
```

It takes the same drafting options as `make_practice.py` (`--mix`,
`--versions`, `--seed`, `--shuffle`, `--groups`, `--title`, `--class`,
`--out`, `--name`). An older `NAME_v1.json` opens too: it is converted, and
`:w` saves it as a sheet.

**Two panes.** On the left are the **banks** of one **course** (the COURSE
row on top; see *Courses and the library* below), as a tree under their
units: each bank, its types with how many of each are on the sheet (`·`
means none), and, for a fixed bank, the problems of a type you open (`●`
marks one on the sheet). Then the settings, and a hint for the row under the
cursor. On the right is **the sheet**, laid out like the page:
the header, the instructions in italics, bold section titles, problems in
one or two columns with their work space as blank lines, and a dashed line
where a new page probably starts. `Tab` moves between the panes, and the
label of the one you are in (BANKS or SHEET, at the top) is highlighted. Both
stay on screen: you can add problems from the banks and arrange them on the
sheet without losing either. `^W o` widens the sheet to the whole screen (for
a closer look at two-column rows) and splits it again; `:set wide` and
`:set nowide` do the same. In a narrow terminal (where the sheet would
get fewer than 60 columns), the banks pane slims down while you are on the
sheet, and comes back to full width when you Tab to it. `:w` writes exactly what the sheet shows.

The status line shows the totals, how many answers fail their check or
can't be checked, `[+]` when there are unwritten changes, and, on the sheet,
what the cursor is on (`#5 3f half 1in`: problem 5, entry 3f, half width,
1in of work space).

### The banks pane

| Keys | Action |
|---|---|
| `j` `k` `gg` `G` `7G` | Move. `/text`, `n`, `N` search the course's banks (type names, and the text of fixed problems), opening what they find, and the settings. |
| `h` `l` on COURSE | The previous / next course, then *All banks*. `i` types one (`Tab` completes). |
| `o` | Open or close a bank; on a fixed bank's type, list its problems. `zM` `zR` close or open every bank. |
| `l` `+` `→` `Ctrl-A` | On a type: add one problem to the type's own section (made, in sequence order, if needed); `3l` adds three. From a fixed bank, it is an unused problem picked at random. On a problem: add that problem. On *versions*: add a version. |
| `L` | Add one (or that problem) where the sheet cursor is: after the problem under it, or at the end of its section (`3L`) |
| `h` `-` `←` `Ctrl-X` | Remove the last problem of that type, or that problem. A type's own section disappears when it's empty. |
| `x` `dd` | Remove every problem of that type (or bank) (on *versions*, back to 1) |
| `i` `a` `Enter`, `cc` `s` | Type a count or a setting (starting from the current value, or blank) |
| `r` | Reroll every problem of that type (or bank) |
| `D` | Clear the whole sheet |

A bank's types share sections with its family: Type 3 problems from the
lesson bank and from the generator go into the same *Type 3* section, and
the sheet never holds the same problem twice.

### Sequences

A **sequence** is an ordered path through a skill, one step at a time, each
step changing a single thing (Engelmann's minimal differences). It doesn't
hold problems itself: each step points at a bank's type, so the same
problems can sit in several sequences (a first teaching sequence, a review,
a set that sets two look-alike types side by side).

In the banks pane, a course's sequences come first under their unit, marked
`≡`, with their steps in order:

```
Equations
▾ ≡ Literal Equations by First Move       3
     1  One Step                          1
     2  Add or Subtract, Then Divide      ·
  ▾  3  Clear One Denominator             2
       13. V = (1/3)Bh;  B                ●
       14. A = (1/2)d₁d₂;  d₁             ·
▸ Literal Equations
```

- A step works like its type's row in the bank: `l` adds a problem (drawn
  fresh), `h` removes one, `L` adds at the sheet cursor, `r` rerolls, `i`
  types a count. The number is how many of the step's problems are on the
  sheet.
- A step may have **pinned examples**, the exact problems the sequence
  teaches with. `o` on the step lists them (`▸`); `l` on one adds that
  problem.
- On the sequence's own row, `o` opens or closes it, `r` rerolls all its
  problems on the sheet, and `x` removes them.
- The hint under the tree shows what changes at the step under the cursor.
- A step whose bank or type the library doesn't have is shown in red,
  marked *(missing)*, and `:warnings` says why. It keeps its number, so the
  steps after it don't renumber.
- As with courses, a problem added from a sequence is just its bank's
  problem: the sheet doesn't depend on the sequence.

### Courses and the library

The **library** is every bank the app knows: the generators, the built-in
banks in the app's `banks/` folder, and **your own banks**, in a library
folder outside the app (`~/Documents/mathsheet-library` unless you choose
another with `:library DIR`). Keep your banks there: they survive updates to
the app, and the folder can be synced or shared with colleagues. Inside it,
organize bank files in any subfolders you like. A bank of yours with the same
name as a built-in one replaces it, so to change a built-in bank, copy it
into your library and edit the copy.

A **course** (Algebra 1, Geometry, ...) is a tag on a bank, not a folder, so
one bank can belong to several courses. The COURSE row at the top of the
banks pane picks which course's banks you see, grouped under the course's
units in order (banks without a unit come last, under *Other*); *All banks*
shows everything. A bank may tag some of its types for other courses, and
then a course shows only its own types.

- `h` `l` on the COURSE row, or `:course Algebra 2` (`Tab` completes,
  `:course all` for every bank), changes the course. `:course` alone says
  which one you're in.
- The **class name** on the worksheet follows the course (choosing
  Algebra 2 makes it *Algebra 2*) until you type a class name of your own,
  which then stays.
- The sheet remembers its course, so reopening it shows that course; a new
  sheet starts in the course you used last. `u` undoes a course change.
- Courses only change what the banks pane shows. A sheet can mix problems
  from any courses, and changing a bank's tags never changes a sheet.

The app reads the library each time it starts (it takes a few
milliseconds). After you add or change a bank or `courses.json` while it's
running, `:rescan` reads it again. Mistakes, such as a tag for a course
that doesn't exist, a misspelled unit, or a file that isn't a bank, never
stop the app: `:rescan` reports the first (with a guess at what you meant:
*did you mean 'Algebra 1'?*), and `:warnings` lists them all.

**When a bank goes missing.** If a sheet uses a bank the library no longer
has (renamed, moved, or deleted), the sheet still opens, shows, edits, and
prints, since it stores its own problems. Those problems are marked with a red
`!`, and the status line counts the missing banks. Nothing new can be drawn
from a missing bank, so rerolling those problems explains why. Restore the
bank, or point `:library` at the right folder, and they're ordinary again.

### The sheet pane

| Keys | Action |
|---|---|
| `j` `k` | Next / previous stop: the header, each section title, each problem |
| `h` `l` | The other problem in the same row |
| `]]` `[[` | Next / previous section title |
| `gg` `G`, `5G` or `:5` | Top, bottom, problem 5 |
| `r` `3r` | Reroll the problem (or the next three) |
| `R` | Reroll its whole section. `:reroll` rerolls the sheet. |
| `W` | Half / full width |
| `+` `-` | Work space up or down a quarter inch (`3+`). `:space 2in` sets it (cm, mm, pt work too). |
| `i` `a` `Enter` | Edit the problem: `equation ; unknown`, in Typst math as stored. The answer is solved again. |
| `A` | Edit the answer (`m = ...`, or just the right side). It is checked at once. |
| `dd` `x` | Cut the problem (`3dd`: three), or the whole section on its title |
| `yy` | Copy the problem or section |
| `p` `P` | Paste below / above. A cut pastes exactly what was cut; a copy (or pasting a second time) draws **new** problems of the same entries, width, and space, so nothing repeats. |
| `J` `K` | Move the problem down / up (it crosses into the next section at an edge), or the section on its title |
| `o` `O` | New section below / above, then type its title (empty: no header) |
| `cS` `cI` | Edit the section's title / instructions. On the header: the sheet's title / instructions. |
| `zM` `zR` | Fold to just the section titles (with counts) / unfold |

On a section title, `W`, `+`, `-`, `:space`, and `:width` change every problem
in the section; on the header, every problem on the sheet.

**Selecting.** `v` starts a selection at the cursor; move with any of the
keys above and every problem between the start and the cursor is
highlighted, across sections (when a section title ends the selection, its
whole section is in it). The status line shows `VISUAL` and how many are
selected. Then:

| Keys | On every selected problem |
|---|---|
| `+` `-` (`3+`), `:space 1.5in` | Work space up or down, or set |
| `W`, `:width full` | Half / full width: all of them the same way (the first one's toggled) |
| `r` | Reroll them |
| `d` `x` / `y` | Cut / copy them all; `p` pastes them as one block, so this moves them |
| `:group TITLE` | Move them into a new section, just after the section of the first one. Sections this empties go; with no title, the section prints no header. |
| `Esc` or `v` | End the selection. `gv` brings the last one back. |

`+`, `-`, `W`, `r`, `:space`, and `:width` keep the selection, so you can press
`+` again or reroll until you like what you get; `d`, `y`, and `:group` end it,
as does anything that moves problems around (`J`, `p`, undo). One `u` undoes
a whole change to a selection. Without a selection, `:group` works on what
the cursor is on.

**Checking.** Drawn problems are checked when they are drawn. An edited
problem is solved again and checked. An answer you write is checked by
substituting it into the problem. The sheet marks an answer that fails with
a red `✗` and one that can't be checked with `?`; `:w` still writes them and
reports how many. Nothing is marked on the PDF. Rerolling an edited problem
makes it a drawn one again.

**Versions.** Version 2, 3, ... redraw every drawn problem in its own slot;
edited problems are the same in every version. `gt` `gT` show the versions.

### Everywhere

| Keys | Action |
|---|---|
| `u` `Ctrl-R` `.` | Undo, redo, repeat the last change (`3u`, `3.`) |
| `Tab`, `Ctrl-W w` `h` `l` | Switch panes |
| `Ctrl-W o` | The sheet full width, or beside the banks again (`:set [no]wide`) |
| `za` `zs` | Answers on / off; compact (no work space) on / off |
| `gt` `gT` | Next / previous version |
| `?` | The keys |

While typing a value: `Enter` accepts, `Esc` cancels, `Ctrl-U` erases the
line, and `Ctrl-W` erases a word.

**The output folder** (*out*, `:out DIR`, `--out DIR`) works as a path does
in Neovim: `~` is your home folder (`~/Desktop`), and a relative path starts
in the folder you ran mathsheet from (the default, `practice`, is a
`practice/` folder there). The folder is made if it doesn't exist. While
typing it, `Tab` completes a folder name: `~/Docu` becomes `~/Documents/`.
When several match, the first fills in, the rest show on the status line,
and each `Tab` moves to the next (`Shift-Tab` back; past the last, you're
back to what you typed). `:e` completes the same way, files included. Names
starting with a dot show only when you type the dot. Opening a sheet sets
*out* to the sheet's folder.

**Commands.** Type `:` and the command, then press Enter. `↑` and `↓` scroll
through earlier commands.

| Command | Action |
|---|---|
| `:w` | Write the sheet and every version's worksheet, key, and slides |
| `:wq` `:x` `ZZ` | Write, then quit |
| `:q` | Quit. If there are unwritten changes, it refuses with *E37*. |
| `:q!` `ZQ` | Quit and discard |
| `:mix 3:6 3f:2 A:1` | Draft a new sheet (`all:N`, `allf:N` work). The title and settings stay. |
| `:groups 9 8 3+4=Warm-up 1` | Sort the problems already on the sheet into sections by type, as with `--groups`. `:groups` alone: one section per type, in sequence order. |
| `:shuffle` | Every problem in one shuffled section with no title |
| `:reroll`, `:reroll section` | Reroll the sheet / the cursor's section |
| `:space 1.5in`, `:width full` | Set work space or width (the selection, or problem, section, or sheet, by where the cursor is) |
| `:join` | Merge the section below into the cursor's section |
| `:course NAME`, `:course all` | Show a course's banks, or every bank (`Tab` completes); `:course` says which |
| `:rescan` | Read the library again (after you add or change a bank or `courses.json`) |
| `:library DIR` | Use this library folder from now on (`Tab` completes); `:library` alone rescans |
| `:warnings` | Everything wrong in the library: unknown courses or units, unreadable files |
| `:group TITLE` | Move the selected problems (or the cursor's) into a new section |
| `:rename TEXT` | Retitle the cursor's section |
| `:clear` | Clear the sheet |
| `:versions N` `:title TEXT` `:class NAME` `:instructions TEXT` `:name N` `:out DIR` | Set a setting (`Tab` completes the folder in `:out`) |
| `:set answers` `noanswers` `answers!`, `compact` ... | Toggles; `:set key=value` sets settings |
| `:e FILE.sheet.json` | Open a sheet |
| `:open [sheet\|key\|slides] [N]` | Open version N's PDF (default: worksheet, version 1) |
| `:N` | On the sheet: problem N. On the types pane: row N. |
| `:help` or `?` | Show the keys |

`Ctrl-C` doesn't quit (same as vim); use `:q!` instead. The app needs a
terminal of at least 72×14. It works without color; italics show where the
terminal supports them.

## 4. What gets written

In the output folder:

| File | Contents |
|---|---|
| `NAME.sheet.json` | The sheet: every section and problem of every version (see below) |
| `NAME_vN.typ` / `.pdf` | Version N's worksheet, in the style of `templates/refined_template.typ` |
| `NAME_vN_key.typ` / `.pdf` | The same, with answers in red. The answers float in the work space, so the key breaks pages exactly where the worksheet does. |
| `NAME_vN_slides.typ` / `.pdf` | Title slide, a title slide per section (grouped only), then a problem slide and an answer slide for each problem |

**The worksheet.** The header, the instructions block, then each section:
its bold heading (with italic instructions, if it has any), then its problems
in rows. Two half-width problems share a row; a full-width problem gets a row
of its own; a half-width problem with no partner sits alone. Each problem has
its own work space below it. Problems are numbered through the whole sheet.

**The sheet file.** `NAME.sheet.json` is the document itself: a title, class,
instructions, number of versions, the command that drafted it, and a list of
sections. Each section has a `title`, `instructions`, and `items`. Each item
has:

| Field | Meaning |
|---|---|
| `bank`, `entry` | Where it came from: `literal`, `3f` |
| `seed` | Its own seed. Versions 2, 3, ... are redrawn from it. |
| `width` | `half` or `full` |
| `space` | Work space below it, such as `1.25in` |
| `problem` | Version 1: `type`, `prompt`, `target`, `answer`, `source` |
| `alts` | Versions 2, 3, ... |
| `edited`, `status` | `edited` is set when you edit it by hand; `status` is `checked`, `unchecked`, or `failed` |

The terminal app edits all of this. You can also edit the file by hand and
print it again with `python3 make_practice.py --sheet FILE`.

Prompts and answers are stored as Typst math. Paste one into a Typst file
as `$display(...)$`.

## 5. Adding problems

**A fixed bank.** Put a JSON file in your library folder (any subfolder
will do), then `:rescan` or restart; the terminal app lists it under its
title in each of its courses. Problems you write are fixed: they print the
same in every version, and rerolling one swaps in another unused problem of
its type.

```json
{
 "format": 1,
 "name": "quiz_bank",
 "title": "Quiz Bank",
 "family": "literal",
 "courses": {"Algebra 1": "Equations", "Algebra 2": null},
 "types": [{"key": "3", "title": "Clear One Denominator", "space": "1in"}],
 "problems": [{"id": "q1", "type": "3", "prompt": "A = 1/2 b h", "target": "b",
               "answer": "b = (2 A)/h"}]
}
```

- `family` (optional) names a generator bank. With `literal`, problems give
  `prompt` and `target` in Typst math and an `answer` like `b = ...`. Each
  answer is checked, an edited problem is solved again, types `1`-`11`, `A`,
  `B` take the lesson's names and hints, and the problems share sections with
  (and never repeat) the generator's.
- Without a family, `prompt` and `answer` are any Typst markup (text, `$math$`,
  `#parts`, ...), with optional plain `text` and `answer_text` for the terminal.
  These answers can't be checked, so they show `?`.
- A type may set `width` (`half` or `full`, default `half`), `space` (default
  `1in`), `look` and `move` (hints on the slides), and `special`.
- `courses` (optional) names the courses the bank belongs to, each with its
  unit, or `null` for none. A plain list, `["Algebra 1", "Geometry"]`, means
  no units. A bank with no `courses` shows only under *All banks*.
- A type may have its own `courses`, which replace the bank's for that type:
  `{"key": "9", "title": "...", "courses": ["Algebra 2"]}`.
- A file that can't be read, or a tag for a course or unit `courses.json`
  doesn't have, is reported when the app starts (and by `:rescan`).

**A course, or a unit.** The courses and their units live in
`courses.json`. The app comes with one in `banks/` (Prealgebra, Algebra 1,
Geometry, Algebra 2, Precalculus, Calculus); a `courses.json` in your library
folder adds courses to it, or replaces one with the same title:

```json
{
 "format": 1,
 "courses": [
  {"title": "Algebra 1", "units": ["Foundations", "Equations", "Linear Functions"]},
  {"title": "Statistics", "units": ["Data", "Probability"]}
 ]
}
```

Courses appear in this order (the built-in ones first), and each course's
banks under its units in this order. Rename a unit here and in the banks
that use it; until both match, those banks show under *Other* and
`:warnings` says why.

**A sequence.** A JSON file with `"kind": "sequence"`, in your library like a
bank, tagged with `courses` the same way:

```json
{
 "format": 1,
 "kind": "sequence",
 "name": "literal_by_move",
 "title": "Literal Equations by First Move",
 "courses": {"Algebra 1": "Equations"},
 "steps": [
  {"entry": "literal/1", "note": "one operation to undo"},
  {"entry": "literal/2", "note": "two operations: add or subtract, then divide"},
  {"entry": "literal/3", "note": "a fraction bar appears",
   "examples": ["lesson_1-4#13", "lesson_1-4#14"]}
 ]
}
```

- `entry` names a bank's type as `--mix` does: `literal/3`, `literal/3f`
  (real formulas), `systems/A`, `lesson_1-4/9`.
- `note` says what changes at this step; it shows in the hint. `title`
  (optional) replaces the type's title.
- `examples` (optional) pins problems of a fixed bank, `BANK#ID`, in order.
  Each should be of the step's type; `:warnings` says when one isn't.
- A step finer than a bank's types (Type 3 with a number denominator, then
  with a letter) needs its own entry in the bank first.
- Banks and sequences share names: a sequence can't have a bank's name.

`gen_sequence.py` writes the lesson's fifty as `banks/lesson_1-4.json`.

**A real formula.** Add a line to `FORMULAS` in `sheets/banks/literal/formulas.py`:

```python
("I = p r t", "p", "1"),        # equation, variable to solve for, type
```

You only give the equation; the script works out and checks the answer. Run
`--selftest 1` to confirm it passes. Before you assign a type, think through
the steps a student would take. The same formula can be a different type for
a different variable.

**A template.** A template is a function that takes a `D` (a source of random
letters and numbers that never repeats a letter within a problem). It
returns `(equation, unknown)`:

```python
def t8_f(d):
    x, a, b, k = d.x(), d.v(), d.coef(), d.const()
    need(lettered(a, b) and a != b)          # reject draws that change the type
    return f"{a} {x} + {k} = {b} {x}", x
```

Add it to that type's list in `TEMPLATES` (`sheets/banks/literal/templates.py`). The helpers:

| Helper | Gives you |
|---|---|
| `d.x()`, `d.v()` | A fresh lowercase letter |
| `d.S()` | A fresh "subject" letter, upper- or lowercase |
| `d.n(lo, hi)` | An integer |
| `d.coef()` | A coefficient: a number from 2 to 9, or a letter |
| `d.const()` | A term on its own: a number from 2 to 15, or a letter |
| `d.prod()` | A richer coefficient: `2 pi`, `a b`, `3 a`, `a^2`, ... |
| `d.frac()` | `p, q` in lowest terms |
| `d.pm()`, `d.pick(...)`, `d.ch(p)` | Random sign, choice, or coin flip |
| `fr(n, d)` | A Typst fraction with the right parentheses |
| `co(n, v)` | `n v`, or just `v` when n is 1 |
| `need(cond)` | Throws the draw away and tries again |

Rules that keep templates honest:

- **Write Typst math with spaces between factors:** `a x`, `3 x`, `2 pi r`.
  Always use `fr()` for fractions; `a/b c` means (a/b)·c.
- **Build each type's move into the template's shape.** For example, Type 8
  needs the unknown on both sides, and at least one coefficient must be a
  letter (otherwise it's just Type 2). Use `need()` to throw out draws that
  turn into another type.
- **Keep the unknown's term positive,** except in Special Case A.
- After adding a template, **read a sample** as well as running the self-test.
  The self-test proves the answers are right; only reading proves the
  problems are the right type.

## 6. Checking your changes

```sh
python3 make_practice.py --selftest 100     # every type of both families and every formula
python3 tests/test_mathsheet.py              # TUI key handling
python3 tests/screen_test.py 80 24 ":mix all:1\r" wait3 @    # the real screen (needs pyte)
python3 gen_sequence.py                     # lesson set: answers and worked steps
```

To confirm a refactor changed nothing, write a set with a fixed seed and
`--no-compile`, before and after, and compare the folders with `diff -r`.

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `could not draw a Type N problem` | Its templates reject almost every draw; loosen the `need()` conditions |
| `typst failed on ...` | Usually Typst syntax in a template or formula. Check the `.typ` file it names; the full error is in the message. |
| `FileNotFoundError: ... mixed_review` | The style preambles are missing; see Requirements in the README |
| The TUI shows `typst not found: .typ only` | Install Typst, or compile the `.typ` files somewhere else |
| `:open` does nothing | It uses `xdg-open`; open the PDF from the output folder instead |
| A bank you added doesn't show | `:rescan`; check `:warnings`; check it's tagged with the course you're in (or `:course all`); check `:library` names the folder it's in |
| Problems marked `!` | Their bank isn't in the library any more; see *When a bank goes missing* |
