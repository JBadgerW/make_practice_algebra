"""Make practice worksheets, answer keys, and slide decks from the command line.

    python3 make_practice.py --help

The command itself is sheets/cli.py (its usage is there). The code lives in
the sheets package:

    sheets/draft.py     a sheet from a recipe: --mix, --groups, --draft
    sheets/build.py     writing and compiling it; previews
    sheets/legacy.py    reading an older practice .json
    sheets/cli.py       the flags, and main

Their names are here too, as they were when this file held them all (the
tests, and anything of yours that imports make_practice, still find them).
"""
from sheets.draft import *                                   # noqa: F401,F403
from sheets.draft import L, E, sh, banks, library            # noqa: F401
from sheets.build import build, preview                      # noqa: F401
from sheets.legacy import from_practice_json, read_sheet     # noqa: F401
from sheets.cli import parser, main, __doc__ as USAGE        # noqa: F401

if __name__ == "__main__":
    main()
