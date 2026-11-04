#!/usr/bin/env python3
"""Present a saved sheet at the board, two problems at a time.

    python3 present.py lesson.sheet.json [--version N] [--out DIR] [--no-open]

Writes lesson.present.html next to the sheet (or in --out) and opens it in
the browser (F11 for full screen). The screen splits in half, one problem in
each. Click a half to show its answer; click again for the next problem.
The numbers down the left move the queue to any problem. Keys: a / Left and
l / Right click the left and right halves, u undoes a click.
"""
import argparse, re, subprocess, sys
from pathlib import Path
from sheets import sheet as sh, present

def out_path(src, out=None, v=0, versions=1):
    name = re.sub(r"(\.sheet)?\.json$", "", Path(src).name)
    suffix = f"_v{v + 1}" if versions > 1 and v else ""
    return Path(out or Path(src).resolve().parent) / f"{name}{suffix}.present.html"

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", help="a .sheet.json saved by mathsheet")
    ap.add_argument("--version", type=int, default=1, help="which version's problems (default 1)")
    ap.add_argument("--out", help="the folder for the page (default: the sheet's folder)")
    ap.add_argument("--no-open", action="store_true", help="write the page but don't open it")
    a = ap.parse_args(argv)
    try:
        s = sh.load(Path(a.sheet).expanduser())
    except (OSError, ValueError) as e:
        sys.exit(f"present: can't open {a.sheet}: {e}")
    if not 1 <= a.version <= s["versions"]:
        sys.exit(f"present: the sheet has {s['versions']} version{'s' * (s['versions'] > 1)}")
    v = a.version - 1
    try:
        path = present.build(s, out_path(a.sheet, a.out, v, s["versions"]), v)
    except RuntimeError as e:
        sys.exit(f"present: {e}")
    print(f"wrote {path} ({len(sh.items(s))} problems)")
    if not a.no_open:
        subprocess.Popen(["xdg-open", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)

if __name__ == "__main__":
    main()
