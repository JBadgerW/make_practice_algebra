"""mathsheet: a terminal worksheet editor, driven with vim keys.

    python3 mathsheet.py                       # start empty
    python3 mathsheet.py --mix 3:6 8:4 --seed 12
    python3 mathsheet.py --draft by_move 5-6       # from a sequence's steps, with review
    python3 mathsheet.py practice/literal_practice.sheet.json   # reopen a sheet

The left pane is a tree of problem banks: the literal-equation generator
(each type's made-up equations and its real formulas: 3 and 3f) and the
fixed banks in library/ (written problems, such as the lesson's fifty), then
the settings. l adds a problem; o opens a bank or a type. The right pane is the
sheet itself, laid out like the page: Tab into it to move through the
problems, reroll them, change their width and work space, edit them, and
cut, copy, and paste them between sections (v selects several at once,
as in vim); the banks stay beside it, and
^W o widens the sheet to the whole screen and back. :w writes exactly what
it shows.
Press ? inside for the full key list.
"""
import curses, os, random, sys
import make_practice as mp
from sheets import sheet as sh
from tui.app import App
from tui.screen import run
# The app lives in tui/ (see tui/__init__.py). These are here too, for the tests:
from sheets.banks.literal import pretty  # noqa: F401
from tui.common import SETTINGS, SHEET, complete_path, dir_label, home_path  # noqa: F401
from tui.screen import Screen, cursor, handle, left_width  # noqa: F401

def parse_args(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="a .sheet.json to open (or an older practice .json to convert)")
    ap.add_argument("--mix", nargs="+", default=[], metavar="ENTRY:COUNT")
    ap.add_argument("--draft", nargs="+", default=[], metavar="TOKEN",
                    help="start from a sequence: SEQ STEPS [xN] [review STEPS|none] [pinned]")
    ap.add_argument("--versions", type=int, default=mp.DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP")
    ap.add_argument("--title", default=mp.DEFAULTS["title"])
    ap.add_argument("--out", help="default: the current folder; started from ~, the folder written to last, else practice")
    ap.add_argument("--name", default=mp.DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", metavar="NAME", help="default: the course, else Algebra 1")
    return ap.parse_args(argv)

def main():
    a = parse_args(sys.argv[1:])
    try:
        mix, groups = mp.parse_mix(a.mix), mp.parse_groups(a.groups)
    except ValueError as e:
        sys.exit(str(e))
    seed = a.seed if a.seed is not None else random.randrange(10**6)
    try:
        plan = mp.parse_draft(a.draft) if a.draft else None
    except ValueError as e:
        sys.exit(str(e))
    sheet = mp.draft_sequence(plan, a.versions, seed, a.title, a.class_name) if plan else \
        mp.draft(mix, a.versions, seed, a.shuffle, groups, a.title, a.class_name) if mix else \
        sh.new_sheet(a.title, a.class_name, versions=a.versions)
    app = App(seed, sheet, a.out, a.name)
    if a.file:
        app.load(a.file)
        app.undo.clear()
    os.environ.setdefault("ESCDELAY", "25")      # Esc should feel instant
    curses.wrapper(run, app)
    if app.last_build:
        print(f"last written: {app.last_build['out']}")
        print(f"print it again with: {app.last_build['sheet']['command']}")

if __name__ == "__main__":
    main()
