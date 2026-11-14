"""What every part of the app shares: imports, constants, and small helpers."""
import functools, os, re, textwrap, time, traceback
from pathlib import Path
from sheets import draft
from sheets import library
from sheets.bank import FRAC_IN, PLAIN_IN  # noqa: F401
from sheets.typmath import pretty

# ------------------------------------------------------------------
# Rows in the left pane: ("course", None) on top; ("seq", name) and its
# ("step", (name, n)), with ("example", (name, n, bank, id)) under an open
# step; ("bank", name), ("count", (bank, entry)), ("problem", (bank, id))
# under an open type of a fixed bank; ("set", key)
# ------------------------------------------------------------------
SETTINGS = ["form", "versions", "title", "class", "instructions", "name", "out"]
COURSE_HINT = ("Which course's banks to show, grouped by unit: h/l step through the courses "
               "(then All banks); i types one (Tab completes). Banks list their courses; :rescan "
               "rereads the library after you change one.")
SETTING_HINTS = {
    "form": "What to print (h/l, or i to type one): a worksheet, or a half-page warm-up: two copies side by side, the answers shuffled and lettered on the back for students to check themselves. An answer that would give itself away gets a look-alike decoy (:pre key marks them, :decoys redraws them). Each version of a warm-up gets its own front and back.",
    "versions": "How many parallel versions to write (h/l, or i to type one): each drawn problem is redrawn in its slot; edited problems stay. Each version gets its own worksheet (key appended) and slides.",
    "title": "The worksheet and slide title. i to edit.",
    "class": "The class name in the worksheet and slide header (default: the course). i to edit.",
    "instructions": "The italic line under the header, for the whole sheet. i to edit; empty for none.",
    "name": "File prefix: NAME.sheet.json, NAME.pdf (every version, each with its key; or the warm-up), NAME_slides.pdf (every version's slides). i to edit.",
    "out": "Folder to write into: ~ is your home folder, and a relative path starts in the folder you ran mathsheet from. i to edit; Tab completes folder names.",
}

# The help pop-up (? or :help): sections of (keys, what they do), in the order shown.
# A new key or command goes in the section it belongs to; a section's title is
# also what :help TOPIC looks for.
HELP = [
    ("Banks pane", [
        ("j k  gg G", "move"),
        ("/text  n N", "search every bank, opening what it finds; next, previous"),
        ("o  O", "open or close this one; open or close all"),
        ("l  +  ^A", "add a problem to the type's section; on a bank, one of any type (20l: twenty)"),
        ("L", "add at the sheet cursor (3L: three)"),
        ("h  -  ^X", "remove the last one"),
        ("x  dd", "remove all of this row's problems"),
        ("D", "clear the sheet"),
        ("r", "reroll all of this type"),
        ("i  a  cc", "type a count or a setting"),
        (":5", "row 5"),
    ]),
    ("The sheet: problems", [
        ("Tab", "to the sheet, and back to the banks"),
        ("j k  h l", "next, previous; left, right"),
        ("gg  G  5G  :5", "top, bottom; problem 5"),
        ("/text  n N", "search the problems; next, previous"),
        ("r  3r  R", "reroll it; three of them; the section"),
        ("W", "half or full width"),
        ("+  -", "work space ±0.25in"),
        ("i  A", "edit the problem; edit its answer"),
        ("dd  yy  p  P", "cut, copy (the copy redraws), paste"),
        ("J  K", "move the problem or section down, up"),
        (":space 1.5in", "set the work space"),
        (":width full", "set the width: half or full"),
        (":scope bank|type", "rerolls draw from the whole bank, or from the type only"),
        (":reroll [section]", "reroll the sheet, or the cursor's section"),
        ("", ":space, :width, and :scope change the selection, or the problem, section, "
             "or sheet the cursor is on."),
    ]),
    ("The sheet: sections and selecting", [
        ("]]  [[", "next, previous section"),
        ("o  O", "new section below, above"),
        ("cS  cI", "change the section's title; its instructions"),
        (":rename TEXT", "retitle the cursor's section"),
        (":join  :j", "merge the section below into this one"),
        (":ja", "merge every section below into this one"),
        ("zM  zR", "fold to section titles; unfold"),
        ("v  gv", "select (Esc ends); select the same again"),
        ("+  -  W  r", "change everything selected"),
        ("d  y", "cut, copy the selection"),
        ("gs", "shuffle the selection, or the section"),
        (":group TITLE", "move the selection into a new section"),
        (":groups 9 8 3+4=Warm-up", "sort the sheet's problems into sections by type"),
        (":shuffle", "every problem in one shuffled section"),
    ]),
    ("Views", [
        ("Tab  ^W w", "switch panes"),
        ("^W o", "the sheet at full width; split again"),
        ("za", "show or hide the answers"),
        ("zs", "compact: show or hide the work space"),
        ("gt  gT", "next, previous version"),
        (":set [no]compact [no]wide [no]answers", "the same, by name (compact! flips it)"),
    ]),
    ("Everywhere", [
        ("u  ^R  .", "undo, redo, repeat"),
        ("I", "what's here, in a box, with the keys that change it"),
        ("f  ^P  :find", "find a bank or type by a few letters"),
        ("?  :help TOPIC", "this help; at a section (:help files)"),
    ]),
    ("Marks on the sheet", [
        ("✗", "the answer fails its check"),
        ("?", "the answer can't be checked"),
        ("!", "the problem's bank is missing"),
    ]),
    ("Files and printing", [
        (":w  :w!", "write the sheet, its worksheets, keys, and slides (! doesn't ask about the name)"),
        (":w NAME  :saveas NAME", "write under a new name (FOLDER/NAME: there; Tab completes)"),
        (":wq  :x  ZZ", "write, then quit"),
        (":q  :q!  ZQ", "quit (! and ZQ discard changes)"),
        (":e FILE.sheet.json", "open a sheet"),
        (":new", "start a new sheet (asks to write or discard changes; :new! discards)"),
        (":pre [sheet|key|slides] [N]", "preview the sheet as it stands (writes nothing)"),
        (":open [sheet|slides]", "open the written PDF"),
        (":present [N]", "two problems at a time at the board, in the browser"),
        (":decoys", "a warm-up's new decoys (:pre key marks them)"),
    ]),
    ("Building a sheet", [
        (":add systems/4:3 BANK/any:5", "add to this sheet (Tab completes banks and types)"),
        (":mix 3:6 3f:2", "a new sheet from these types and counts"),
        (":draft SEQ 5-6 [x6] [review 1-4|none] [pinned]", "a new sheet from a sequence's steps"),
        (":scale 2  :scale 0.5  :scale 3/2", "the sheet that many times as long (each kind keeps one)"),
        (":form  :versions  :title  :class  :instructions  :name  :out",
         "set a setting, as on the banks pane (:title Unit 2 Review)"),
        (":set KEY=VALUE", "the same (:set versions=3)"),
    ]),
    ("Courses and the library", [
        (":course NAME|all", "show a course's banks, or every bank (h l on COURSE)"),
        (":rescan", "read the library again"),
        (":library DIR", "use this library folder from now on"),
        (":warnings", "everything wrong in the library"),
        ("", "Types 1-11, A, B: the lesson's sequence. 3f: real formulas. "
             "Banks: built in, and your :library."),
    ]),
]
HELP_KEYS_W = 22                       # the help box's key column; longer keys get a line of their own

@functools.lru_cache(maxsize=8)
def help_lines(width):
    """The help for a box `width` columns wide inside: (lines, starts). Each line
    is (kind, keys, text): "head" (a section's title), "row" (keys and what they
    do; no keys on a wrapped line), "long" (keys too wide for their column, alone
    on the line), "note" (text from the left edge), or "blank". starts[k] is the
    line of section k's title."""
    lines, starts = [], []
    room = max(20, width - HELP_KEYS_W)
    for title, rows in HELP:
        if lines:
            lines.append(("blank", "", ""))
        starts.append(len(lines))
        lines.append(("head", "", title.upper()))
        for keys, text in rows:
            if not keys:
                lines += [("note", "", l) for l in textwrap.wrap(text, max(20, width))]
                continue
            if len(keys) > HELP_KEYS_W - 2:
                lines.append(("long", keys, ""))
                keys = ""
            for i, l in enumerate(textwrap.wrap(text, room)):
                lines.append(("row", keys if i == 0 else "", l))
    return lines, starts

def help_section(starts, top):
    """Which section the line `top` is in."""
    return max(0, sum(s <= top for s in starts) - 1)

SHEET = (-1, -1)                       # the sheet cursor on the header (title, instructions)
SHEET_MIN = 60                         # a sheet pane narrower than this takes room from the banks while it has focus
# For the page-break estimate, measured from the refined template in Typst
# (inches): the page body, the header, an instructions line, a section title,
# and a problem's own line (plain, or with a stacked fraction), each with the
# gap that follows it.
PAGE_IN, HEADER_IN, LINE_IN, TITLE_IN = 9.5, 0.62, 0.25, 0.30


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
def home_path(p):
    """A folder in full, with your home folder as ~, so it means the same from anywhere."""
    p = Path(p).expanduser().resolve()
    try:
        return str(Path("~") / p.relative_to(Path.home()))
    except ValueError:
        return str(p)

def start_out():
    """The out folder a session starts in: the folder mathsheet was started from,
    unless that's your home folder; then the folder written to last, else practice."""
    if Path.cwd() != Path.home().resolve():
        return home_path(Path.cwd())
    return library.config().get("out") or draft.DEFAULTS["out"]

def error_log():
    """Where unexpected errors are recorded: errors.log, beside the config file."""
    return library.config_path().parent / "errors.log"

def log_error(e):
    """Append an unexpected error's traceback to the error log. Returns the log's
    path as you'd type it, or None if it couldn't be written."""
    path = error_log()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(f"---- {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    + "".join(traceback.format_exception(type(e), e, e.__traceback__)) + "\n")
    except OSError:
        return None
    return home_path(path)

INFO_LABEL, INFO_KEYS_W = 10, 6         # the info box's columns: label, then the keys at the right

MATH_WORDS = {"times": "×", "div": "÷", "dot": "·", "plus.minus": "±", "minus": "−", "eq.not": "≠"}

def prose(t):
    """Hint text for the terminal: its $math$ readable, without the dollar signs."""
    def math(m):
        x = re.sub(r"[a-z]+(?:\.[a-z]+)?", lambda w: MATH_WORDS.get(w.group(0), w.group(0)), m.group(1))
        return pretty(x + " ").strip() if len(x) > 1 else x
    return re.sub(r"\$([^$]*)\$", math, t)

def tags_text(tags):
    """{course: unit or None} -> "Algebra 1 › Lessons; Algebra 2", or "none"."""
    return "; ".join(f"{c} › {u}" if u else c for c, u in tags.items()) or "none: it shows only under All banks"

def info_lines(rows, width):
    """The info box's rows wrapped to a box this wide: [(label, text, keys)], keys on the first line."""
    out = []
    for label, value, keys in rows:
        for i, l in enumerate(textwrap.wrap(value, max(10, width - 4 - INFO_LABEL - INFO_KEYS_W)) or [""]):
            out.append((label if i == 0 else "", l, keys if i == 0 else ""))
    return out

def dir_label(p):
    """A folder as you'd type it: from the folder mathsheet started in if it's
    inside it, else from ~ if it's in your home folder, else in full."""
    p = Path(p).expanduser().resolve()
    for base, pre in ((Path.cwd(), ""), (Path.home(), "~")):
        try:
            rel = str(p.relative_to(base))
        except ValueError:
            continue
        return (pre or ".") if rel == "." else f"{pre}/{rel}" if pre else rel
    return str(p)

def complete_course(text):
    """The course titles (and all) that start with text, ignoring case."""
    t = text.strip().lower()
    return [c for c in [x["title"] for x in library.current().courses] + ["all"] if c.lower().startswith(t)]

def complete_sequence(text):
    """The sequence names that start with text."""
    return [n for n in sorted(library.current().sequences) if n.startswith(text.strip())]

def complete_entry(text, course=None):
    """What a partly typed :add or :mix entry could become: [(text, label)].
    Before the slash, the banks whose name starts with it, or if none does,
    those whose title has it in it (the course's banks first), each ending in /; after it,
    the bank's entries, then any and all. The label says what each is."""
    lib = library.current()
    bank, slash, frag = text.partition("/")
    if not slash:
        t = bank.lower()
        names = lib.names()
        shown = {n for _, ns in lib.view(course) for n in ns} if course else set()
        found = [n for n in names if n.lower().startswith(t)] or \
            [n for n in names if t and t in lib.get(n).TITLE.lower()]      # by title only when no name starts so
        order = sorted(found, key=lambda n: n not in shown)
        return [(f"{n}/", f"{n}: {lib.get(n).TITLE}") for n in order]
    if not lib.has(bank):
        return []
    b = lib.get(bank)
    out = [(f"{bank}/{e['key']}", f"{e.get('label') or e['key']}: {e['title']}") for e in b.ENTRIES
           if e["key"].lower().startswith(frag.lower()) or (e.get("label") or "").lower().startswith(frag.lower())]
    return out + [(f"{bank}/{w}", f"{w}: {what}") for w, what in (("any", "any type, in one section"), ("all", "every type"))
                  if w.startswith(frag.lower())]

def openable(name):
    """Can :e open a file by this name? A sheet, or an older set's first version."""
    return name.endswith(".sheet.json") or re.search(r"_v1\.json$", name) is not None

def complete_path(text, dirs_only=False, keep=None, base="."):
    """The names a partly typed path could become, as Neovim completes them:
    ~ is home, a relative path starts in base (default: the current folder),
    folders end in /, and hidden names show only when the part typed starts
    with a dot. keep(name) picks the files to offer (default: every file)."""
    if text == "~":
        return ["~/"]
    head, sep, frag = text.rpartition("/")
    folder = Path(base).expanduser() / os.path.expanduser(head + sep) if sep else Path(base).expanduser()
    try:
        entries = sorted(os.scandir(folder), key=lambda e: e.name)
    except OSError:
        return []
    out = []
    for e in entries:
        if not e.name.startswith(frag) or (e.name.startswith(".") and not frag.startswith(".")):
            continue
        try:
            is_dir = e.is_dir()
        except OSError:
            continue
        if is_dir:
            out.append(head + sep + e.name + "/")
        elif not dirs_only and (keep is None or keep(e.name)):
            out.append(head + sep + e.name)
    return out

# ------------------------------------------------------------------
