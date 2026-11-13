"""Make practice worksheets, answer keys, and slide decks of literal equations,
drawn by type (the same Types 1-11 and Special Cases A-B as the lesson).

Each type has two entries: 3 draws made-up equations from templates, and 3f
draws real formulas of that type. Every answer is solved by sympy, written
in classroom form, and checked numerically before it is used.

A run first drafts a *sheet* (sheets/sheet.py): sections of problems, each
problem with its own seed, width, and work space. The sheet is saved as
NAME.sheet.json beside the PDFs, and the worksheet, key, and slides of every
version are printed from it.

Examples (run from this folder):
    python3 make_practice.py --mix 3:6 8:4 A:2 --versions 3 --seed 12
    python3 make_practice.py --mix all:2 --shuffle
    python3 make_practice.py --mix 1f:6 3f:4         # real formulas
    python3 make_practice.py --mix lesson_1-4/any:20  # twenty from every type of a bank
    python3 make_practice.py --draft by_move 5-6 review 1-4   # a sheet from a sequence's steps
    python3 make_practice.py --sheet practice/literal_practice.sheet.json   # print a saved sheet again
    python3 make_practice.py --selftest 200        # stress-test every type
    python3 mathsheet.py                        # the same, interactively (vim keys)

--mix ENTRY:COUNT ... entries are 1-11, A, B (made-up equations), 1f-11f, Af, Bf
                      (real formulas), all (every made-up entry), allf (every
                      formulas entry). Default all:2. Another bank's entries
                      take its name: systems/4:3, systems/all:1. BANK/any:N
                      (or 'BANK/*:N', quoted for the shell) draws N from all
                      of a bank's types, in one section with the bank's title;
                      their rerolls draw from the whole bank too.
--versions N          N parallel versions: every drawn problem is redrawn in its slot
--seed S              same seed -> same sheet (default: random, printed)
--shuffle             one section with every problem shuffled, no headings
--groups G ...        section order and mixed sections: 9 8 3+4=Warm-up 1
--draft SEQ STEPS [xN] [review STEPS|none] [pinned]
                      a sheet from a sequence (sheets/sequences.py): N problems
                      (default 6) of each new step in its own section, then a
                      shuffled review of about one problem per two new ones,
                      spread over the review steps (default: every earlier
                      step). pinned starts each step with its pinned examples.
--sheet FILE          print a saved .sheet.json (or an older practice .json) again
--warmup              a half-page warm-up: two copies side by side, the answers
                      shuffled and lettered on the back, with decoys; each
                      version gets its own front and back
--out DIR, --name N   output folder (default ./practice) and file prefix
--no-compile          write .typ files only
"""
import argparse, random, sys
from . import sheet as sh, writer, library
from .build import build
from .draft import (DEFAULTS, apply_style, command_for, draft, draft_command, draft_sequence,
                    parse_draft, parse_groups, parse_mix)
from .legacy import read_sheet

def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mix", nargs="+", default=["all:2"], metavar="ENTRY:COUNT")
    ap.add_argument("--versions", type=int, default=DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--style", choices=("mixed", "letters", "formulas"), default="mixed",
                    help=argparse.SUPPRESS)           # old commands: formulas means the 3f entries
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP",
                    help="print sections in this order; join types with +, rename with =: 9 8 3+4=Warm-up 1")
    ap.add_argument("--title", default=DEFAULTS["title"])
    ap.add_argument("--out", default=DEFAULTS["out"])
    ap.add_argument("--name", default=DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", default=DEFAULTS["class_name"], metavar="NAME")
    ap.add_argument("--draft", nargs="+", metavar="TOKEN",
                    help="a sheet from a sequence: SEQ STEPS [xN] [review STEPS|none] [pinned]")
    ap.add_argument("--sheet", metavar="FILE", help="print a saved .sheet.json (or older practice .json) again")
    ap.add_argument("--warmup", action="store_true", help="a half-page warm-up (each version a front and back)")
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--selftest", type=int, metavar="N")
    return ap

def main():
    a = parser().parse_args()
    seed = a.seed if a.seed is not None else random.randrange(10**6)
    if a.selftest:
        first = ["literal", "systems", "inequalities", "modeling", "absolute", "absolute_words"]
        gens = library.current().generators
        order = first + sorted(n for n in gens if n not in first)
        sys.exit(0 if all(gens[n].selftest(a.selftest, seed) for n in order if hasattr(gens[n], "selftest")) else 1)
    try:
        if a.sheet:
            sheet = read_sheet(a.sheet)
        elif a.draft:
            plan = parse_draft(a.draft)
            sheet = draft_sequence(plan, a.versions, seed, a.title, a.class_name)
            sheet["command"] = draft_command(plan, a.versions, seed, a.title, a.out, a.name, a.class_name)
        else:
            mix, groups = apply_style(parse_mix(a.mix), a.style), parse_groups(a.groups)
            sheet = draft(mix, a.versions, seed, a.shuffle, groups, a.title, a.class_name)
            sheet["command"] = command_for(mix, a.versions, seed, a.shuffle, a.title, a.out, a.name,
                                           a.class_name, groups)
        if a.warmup:
            sheet["form"] = "warmup"
            if sheet.get("command"):
                sheet["command"] += " --warmup"
        r = build(sheet, a.out, a.name, compile=not a.no_compile)
    except (ValueError, RuntimeError, OSError) as e:
        sys.exit(str(e))
    n = len(sh.items(sheet))
    print(("" if a.sheet else f"seed {seed}: ") + f"{n} problems x {sheet['versions']} version(s) -> {r['out']}")
    print("  " + "\n  ".join(r["files"]) + ("" if r["compiled"] else "\n  (not compiled)"))
    if sh.is_warmup(sheet):
        for v in range(sheet["versions"]):
            ver = f"version {v + 1}: " if sheet["versions"] > 1 else ""
            if k := writer.unlettered(sheet, v):
                print(f"  warning: {ver}{k} problem{'s' * (k > 1)} with a graph for an answer, left off the back")
            if u := writer.unmatched(sheet, v):
                print(f"  warning: {ver}{', '.join(f'#{n}' for n in u)} can be matched without solving (no decoy fits)")

if __name__ == "__main__":
    main()
