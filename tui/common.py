"""What every part of the app shares: imports, constants, and small helpers."""
import os, re, textwrap, time, traceback
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

HELP = """\
BANKS PANE                          THE SHEET (Tab to it; ^W o widens it)
j k gg G  move   /text n N  search  j k  h l    next/prev; left/right
l + ^A  add to the type's section   ]] [[       next / previous section
  on a bank: any type (20l)         gg G  5G    top, bottom; problem 5
L  add at the sheet cursor (3L)
h - ^X  remove the last one         r 3r R      reroll it / 3 / section
x dd  remove all   D  clear sheet   W           half / full width
i a cc  type a count or a setting   + -         work space ±0.25in
r  reroll all of this type          i  A        edit problem / answer
o O  open one / open or close all   dd yy p P   cut, copy (redraws), paste
EVERYWHERE                          J K         move problem or section
u ^R .   undo, redo, repeat         o O  cS cI  new section; title, instr.
Tab ^W w switch panes               zM zR       fold to sections / unfold
za zs    answers / compact          ✗ an answer fails its check
gt gT    next / previous version    ? an answer can't be checked
^W o     sheet full width / split   v  gv       select (Esc ends); reselect
I        what's here, in a box      + - W r     change all selected
f ^P     find a bank or type        d y :group  cut, copy, new section
                                    gs          shuffle selection / section
                                    :scope bank|type  reroll from bank / type
COMMANDS
:w :w! :wq :x ZZ :q :q! ZQ   :e FILE.sheet.json   :open [sheet|slides]
:new  start a new sheet (asks to write or discard changes; :new! discards)
:pre [sheet|key|slides] [N]  preview the sheet as it stands (writes nothing)
:present [N]  two problems at a time at the board, in the browser
:decoys  a warm-up's new decoys (:pre key marks them)
:w NAME  :saveas NAME  write under a new name (FOLDER/NAME: there; Tab completes)
:add systems/4:3 BANK/any:5  add to this sheet (Tab completes banks and types)
:scale 2  :scale 0.5  :scale 3/2  the sheet that many times as long (each kind keeps one)
:mix 3:6 3f:2  new sheet   :reroll [section]   :space 1.5in   :width full
:draft SEQ 5-6 [x6] [review 1-4|none] [pinned]   a sheet from a sequence's steps
:groups 9 8 3+4=Warm-up   :shuffle   :join (:j)   :ja   :rename TEXT   :N  problem N
:form :title :class :instructions :versions :name :out  :set [no]compact [no]wide
:course NAME|all  (h l on COURSE)   :rescan   :library DIR   :warnings
Types 1-11, A, B: the lesson's sequence. 3f: real formulas. Banks: built in, and your :library."""

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
