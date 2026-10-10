"""mathsheet: a terminal worksheet editor, driven with vim keys.

    python3 mathsheet.py                       # start empty
    python3 mathsheet.py --mix 3:6 8:4 --seed 12
    python3 mathsheet.py practice/literal_practice.sheet.json   # reopen a sheet

The left pane is a tree of problem banks: the literal-equation generator
(each type's made-up equations and its real formulas: 3 and 3f) and the
fixed banks in banks/ (written problems, such as the lesson's fifty), then
the settings. l adds a problem; o opens a bank or a type. The right pane is the
sheet itself, laid out like the page: Tab into it to move through the
problems, reroll them, change their width and work space, edit them, and
cut, copy, and paste them between sections (v selects several at once,
as in vim); the banks stay beside it, and
^W o widens the sheet to the whole screen and back. :w writes exactly what
it shows.
Press ? inside for the full key list.
"""
import copy, curses, os, random, re, shlex, subprocess, sys, textwrap
from pathlib import Path
import make_practice as mp
from sheets import sheet as sh, edit as E, banks
from sheets.banks.literal import pretty

# ------------------------------------------------------------------
# Rows in the left pane: ("bank", name), ("count", (bank, entry)),
# ("problem", (bank, id)) under an open type of a fixed bank, ("set", key)
# ------------------------------------------------------------------
SETTINGS = ["versions", "title", "class", "instructions", "name", "out"]
SETTING_HINTS = {
    "versions": "How many parallel versions to write (h/l, or i to type one): each drawn problem is redrawn in its slot; edited problems stay. Each version gets its own worksheet, key, and slides.",
    "title": "The worksheet and slide title. i to edit.",
    "class": "The class name in the worksheet and slide header (default Algebra 1). i to edit.",
    "instructions": "The italic line under the header, for the whole sheet. i to edit; empty for none.",
    "name": "File prefix: NAME.sheet.json, NAME_v1.pdf, NAME_v1_key.pdf, NAME_v1_slides.pdf. i to edit.",
    "out": "Folder to write into: ~ is your home folder, and a relative path starts in the folder you ran mathsheet from. i to edit; Tab completes folder names.",
}

HELP = """\
BANKS PANE                          THE SHEET (Tab to it; ^W o widens it)
j k gg G  move   /text n N  search  j k  h l    next/prev; left/right
l + ^A  add to the type's section   ]] [[       next / previous section
L  add at the sheet cursor (3L)     gg G  5G    top, bottom; problem 5
h - ^X  remove the last one         r 3r R      reroll it / 3 / section
x dd  remove all   D  clear sheet   W           half / full width
i a cc  type a count or a setting   + -         work space ±0.25in
r  reroll all of this type          i  A        edit problem / answer
o  open a bank or a type's list     dd yy p P   cut, copy (redraws), paste
EVERYWHERE                          J K         move problem or section
u ^R .   undo, redo, repeat         o O  cS cI  new section; title, instr.
Tab ^W w switch panes               zM zR       fold to sections / unfold
za zs    answers / compact          ✗ an answer fails its check
gt gT    next / previous version    ? an answer can't be checked
^W o     sheet full width / split   v  gv       select (Esc ends); reselect
                                    + - W r     change all selected
                                    d y :group  cut, copy, new section
COMMANDS
:w :wq :x ZZ :q :q! ZQ   :e FILE.sheet.json   :open [sheet|key|slides] [N]
:mix 3:6 3f:2  new sheet   :reroll [section]   :space 1.5in   :width full
:groups 9 8 3+4=Warm-up   :shuffle   :join   :rename TEXT   :N  problem N
:title :class :instructions :versions :name :out  :set [no]compact [no]wide
Types 1-11, A, B: the lesson's sequence. 3f: real formulas. banks/: fixed."""

SHEET = (-1, -1)                       # the sheet cursor on the header (title, instructions)
SHEET_MIN = 60                         # a sheet pane narrower than this takes room from the banks while it has focus
# For the page-break estimate, measured from the refined template in Typst
# (inches): the page body, the header, an instructions line, a section title,
# and a problem's own line (plain, or with a stacked fraction), each with the
# gap that follows it.
PAGE_IN, HEADER_IN, LINE_IN, TITLE_IN, PLAIN_IN, FRAC_IN = 9.5, 0.62, 0.25, 0.30, 0.30, 0.38

# ------------------------------------------------------------------
# State and editing (no curses here, so it can be driven by tests)
# ------------------------------------------------------------------
class App:
    def __init__(self, seed=None, sheet=None, out=None, name=None):
        self.rng = random.Random(seed)
        self.s = dict(sheet=sheet or sh.new_sheet(mp.DEFAULTS["title"], mp.DEFAULTS["class_name"], mp.L.INSTRUCTIONS),
                      out=out or mp.DEFAULTS["out"], name=name or mp.DEFAULTS["name"])
        self.undo, self.redo = [], []
        self.row, self.focus, self.version = 1, "left", 0
        self.open = {mp.BANK}           # banks open in the tree
        self.open_types = set()         # (bank, type) of fixed banks showing their problems
        self.cur = SHEET
        self.anchor = None              # where v was pressed: a selection runs from here to the cursor
        self.last_sel = None            # (anchor, cursor) of the last selection, for gv
        self.answers = self.compact = self.folded = False
        self.wide = False               # the sheet fills the screen while it has focus
        self.pv_top = 0
        self.mode = "normal"            # normal, insert, command, search, help
        self.buf, self.editing = "", None
        self.count, self.pending = "", ""
        self.msg, self.err = "Press ? for help.  l adds a problem; Tab moves to the sheet.", False
        self.last_change = None         # a function that repeats the last change (for .)
        self.search_q = ""
        self.cmd_hist, self.hist_i = [], 0
        self.comp = None                # Tab completion in progress: dict(start, options, i, buf)
        self.written = None             # the state at the last :w (or when a file was opened)
        self.reg = None                 # dict(kind="items"|"section", what=..., cut=bool)
        self.last_build = None
        self.quit = False
        self.clamp()
        if banks.errors():
            self.say("E: " + "; ".join(banks.errors()), True)

    @property
    def sheet(self):
        return self.s["sheet"]

    def seeds(self):
        return iter(lambda: self.rng.randrange(2**31), None)

    # -- values --------------------------------------------------------
    def total(self):
        return len(sh.items(self.sheet))

    def rows(self, everything=False):
        """The left pane's rows, as shown (or with every bank and type open)."""
        out = []
        for name in banks.names():
            out.append(("bank", name))
            if everything or name in self.open:
                b = banks.get(name)
                for e in b.ENTRIES:
                    out.append(("count", (name, e["key"])))
                    if getattr(b, "FIXED", False) and (everything or (name, e["key"]) in self.open_types):
                        out += [("problem", (name, p["id"])) for p in b.PROBLEMS if p["type"] == e["key"]]
        return out + [("set", k) for k in SETTINGS]

    def rid(self, row=None):
        """The id of a row (default: the cursor's)."""
        rows = self.rows()
        return rows[min(self.row if row is None else row, len(rows) - 1)]

    def value(self, row):
        kind, key = self.rid(row)
        if kind == "bank":
            return sum(1 for it in sh.items(self.sheet) if it["bank"] == key)
        if kind == "count":
            return E.count(self.sheet, *key)
        if kind == "problem":
            return E.where_problem(self.sheet, *key) is not None
        return {"versions": self.sheet["versions"], "title": self.sheet["title"], "class": self.sheet["class_name"],
                "instructions": self.sheet["instructions"]}.get(key, self.s.get(key))

    def toggle_open(self, rid=None):
        """o: open or close the bank, or the fixed bank's type, under the cursor."""
        kind, key = rid or self.rid()
        if kind == "bank":
            self.open ^= {key}
        elif kind in ("count", "problem"):
            bank = key[0]
            b = banks.get(bank)
            if not getattr(b, "FIXED", False):
                return self.say("o lists the problems of a fixed bank's type; this bank draws new ones", True)
            typ = key[1] if kind == "count" else b.PROBLEM[key[1]]["type"]
            self.open_types ^= {(bank, typ)}
            rid = ("count", (bank, typ))
        else:
            return
        rows = self.rows()
        self.row = rows.index(rid) if rid in rows else min(self.row, len(rows) - 1)

    def fold_banks(self, close):
        here = self.rid()
        self.open = set() if close else set(banks.names())
        if close:
            self.open_types = set()
        rows = self.rows()
        bank = here[1] if here[0] == "bank" else here[1][0] if here[0] != "set" else None
        self.row = rows.index(here) if here in rows else rows.index(("bank", bank)) if bank else len(rows) - 1

    def dirty(self):
        return self.written != self.snapshot()

    def snapshot(self):
        return copy.deepcopy(self.s)

    def change(self, fn):
        """Run fn, which edits self.s; undoable. A ValueError or RuntimeError
        undoes it and becomes the message. Returns True if it worked."""
        before, layout = self.snapshot(), self.layout()
        try:
            fn()
        except (ValueError, RuntimeError) as e:
            self.s = before
            self.say(f"E: {e}".splitlines()[0], True)
            return False
        if self.anchor is not None and self.layout() != layout:
            self.end_visual()                  # its positions no longer mean the same problems
        if self.s != before:
            self.undo.append(before)
            self.redo.clear()
        self.clamp()
        return True

    def layout(self):
        """Which problem is where (by identity), to tell a change that moves them."""
        return [[id(it) for it in sec["items"]] for sec in self.sheet["sections"]]

    def say(self, msg, err=False):
        self.msg, self.err = msg, err

    def statuses(self):
        its = sh.items(self.sheet)
        return (sum(it["status"] == "unchecked" for it in its), sum(it["status"] == "failed" for it in its))

    # -- the types pane --------------------------------------------------
    def bump(self, n, row=None):
        kind, key = self.rid(row)
        if kind == "count":
            if n > 0:
                self.change(lambda: E.set_count(self.sheet, *key, E.count(self.sheet, *key) + n, self.seeds()))
            else:
                self.change(lambda: E.remove_last(self.sheet, *key, -n))
        elif kind == "problem":
            if n > 0:
                self.change(lambda: E.add_problem(self.sheet, *key))
            else:
                self.change(lambda: E.remove_problem(self.sheet, *key))
        elif kind == "bank":
            return self.say("o opens the bank; l on a type adds a problem", True)
        elif key == "versions":
            self.set_versions(self.sheet["versions"] + n)
        else:
            return self.say(f"{key} is text: press i to edit it", True)
        self.last_change = lambda: self.bump(n)

    def set_versions(self, n):
        n = min(26, max(1, n))
        def go():
            self.sheet["versions"] = n
            sh.fill_versions(self.sheet)
        self.change(go)
        self.version = min(self.version, n - 1)

    def zero(self, row=None):
        kind, key = self.rid(row)
        if kind == "count":
            self.change(lambda: E.remove_last(self.sheet, *key, 10**6))
        elif kind == "problem":
            self.change(lambda: E.remove_problem(self.sheet, *key))
        elif kind == "bank":
            b = key
            self.change(lambda: [E.remove_last(self.sheet, b, e["key"], 10**6) for e in banks.get(b).ENTRIES])
        elif key == "versions":
            self.set_versions(1)
        else:
            return self.say("x and dd only remove problems and reset versions", True)
        self.last_change = lambda: self.zero()

    def set_value(self, text, row=None):
        """Apply typed text to a row; returns an error string or None."""
        kind, key = self.rid(row)
        text = text.strip()
        if kind in ("bank", "problem"):
            return "type a count on a type's row"
        if kind == "count" or key == "versions":
            if not text.isdigit():
                return f"{'count' if kind == 'count' else key} must be a whole number"
            n = int(text)
            if key == "versions":
                if not 1 <= n <= 26:
                    return "versions must be 1-26"
                self.set_versions(n)
            else:
                self.change(lambda: E.set_count(self.sheet, *key, n, self.seeds()))
        elif key in ("title", "class", "instructions"):
            if not text and key != "instructions":
                return f"{key} can't be empty"
            field = {"class": "class_name"}.get(key, key)
            self.change(lambda: self.sheet.__setitem__(field, text))
        else:
            if not text:
                return f"{key} can't be empty"
            if key == "name" and not re.fullmatch(r"[\w.-]+", text):
                return "name may use letters, digits, _ . - only"
            self.change(lambda: self.s.__setitem__(key, text))
        self.last_change = lambda: self.set_value(text)
        return None

    def add_here(self, n):
        """L: add n of the type (or the one problem) under the tree cursor where the sheet cursor is."""
        kind, key = self.rid()
        if kind not in ("count", "problem"):
            return self.say("L adds the type or problem under the cursor where the sheet cursor is", True)
        def go():
            si, ii = self.cur
            if si < 0 and not self.sheet["sections"]:
                self.sheet["sections"].append(sh.new_section())
            si = max(si, 0)
            at = ii + 1 if ii >= 0 else None
            if kind == "problem":
                return E.add_problem(self.sheet, *key, si, at)
            for k in range(n):
                E.add(self.sheet, si, *key, next(self.seeds()), None if at is None else at + k)
        if self.change(go):
            self.say(f"added to “{self.sheet['sections'][max(0, self.cur[0])]['title'] or 'untitled'}”")
        self.last_change = lambda: self.add_here(n)

    def reroll_entry(self):
        kind, key = self.rid()
        if kind not in ("count", "bank"):
            return
        mine = lambda it: it["bank"] == key if kind == "bank" else (it["bank"], it["entry"]) == key
        ps = [p for p in E.positions(self.sheet) if mine(self.sheet["sections"][p[0]]["items"][p[1]])]
        if self.change(lambda: E.reroll(self.sheet, ps, self.seeds())):
            self.say(f"{len(ps)} rerolled")

    def clear(self):
        self.change(lambda: self.sheet.__setitem__("sections", []))
        self.say("sheet cleared (u to undo)")

    # -- undo ----------------------------------------------------------
    def do_undo(self, n=1):
        for _ in range(n):
            if not self.undo:
                return self.say("Already at oldest change")
            self.redo.append(self.snapshot())
            self.s = self.undo.pop()
            self.end_visual()
        self.clamp()
        self.say(f"{n} change{'s' * (n > 1)} undone")

    def do_redo(self, n=1):
        for _ in range(n):
            if not self.redo:
                return self.say("Already at newest change")
            self.undo.append(self.snapshot())
            self.s = self.redo.pop()
            self.end_visual()
        self.clamp()
        self.say(f"{n} change{'s' * (n > 1)} redone")

    def repeat(self, n=1):
        if self.last_change:
            for _ in range(n):
                self.last_change()

    # -- the sheet cursor -------------------------------------------------
    def targets(self):
        """Every place the sheet cursor can stop, in reading order."""
        out = [SHEET]
        for si, sec in enumerate(self.sheet["sections"]):
            out.append((si, -1))
            if not self.folded:
                out += [(si, ii) for ii in range(len(sec["items"]))]
        return out

    def clamp(self):
        secs = self.sheet["sections"]
        si, ii = self.cur
        if si >= len(secs):
            si, ii = len(secs) - 1, (len(secs[-1]["items"]) - 1 if secs else -1)
        if si >= 0:
            ii = min(ii, len(secs[si]["items"]) - 1)
            if self.folded:
                ii = -1
        self.cur = (si, ii) if si >= 0 else SHEET
        if self.cur == SHEET and not self.folded and sh.items(self.sheet) and self.focus == "left":
            self.cur = next(t for t in self.targets() if t[1] >= 0)        # start on the first problem

    def item(self, pos=None):
        si, ii = pos or self.cur
        return self.sheet["sections"][si]["items"][ii] if si >= 0 and ii >= 0 else None

    def go(self, n):
        ts = self.targets()
        i = ts.index(self.cur) if self.cur in ts else 0
        self.cur = ts[min(max(0, i + n), len(ts) - 1)]

    def go_problem(self, n):
        """The sheet cursor to problem n (1-based, print order)."""
        ps = E.positions(self.sheet)
        if ps:
            self.folded = False
            self.cur = ps[min(max(1, n), len(ps)) - 1]

    def column(self, d):
        """h/l: the other problem in the same row, if there is one."""
        it = self.item()
        if not it:
            return
        si, ii = self.cur
        for row in sh.rows(self.sheet["sections"][si]["items"]):
            if any(x is it for x in row) and len(row) == 2:
                j = 0 if row[0] is it else 1
                if 0 <= j + d < 2:
                    self.go(d)
                return

    def section_jump(self, d):
        heads = [t for t in self.targets() if t[1] == -1 and t != SHEET]
        if not heads:
            return
        si = self.cur[0]
        if d > 0:
            nxt = [t for t in heads if t[0] > si]
            self.cur = nxt[0] if nxt else heads[-1]
        else:
            prv = [t for t in heads if t[0] < si or (t[0] == si and self.cur[1] >= 0)]
            self.cur = prv[-1] if prv else SHEET

    # -- selecting (v) ---------------------------------------------------
    def span(self):
        """The stops from the anchor to the cursor, in reading order."""
        ts = self.targets()
        a, b = sorted((ts.index(self.anchor), ts.index(self.cur)))
        return ts[a:b + 1]

    def selection(self):
        """The problems selected, in reading order: those between the anchor and the
        cursor, and every problem of a section whose title ends the selection."""
        span = self.span()
        si, ii = span[-1]
        ps = {t for t in span if t[1] >= 0}
        if ii < 0:
            ps |= set(E.positions(self.sheet, None if si < 0 else si))
        return sorted(ps)

    def selected(self):
        """What the sheet pane highlights: the selection and the titles inside it."""
        if self.anchor is None:
            return set()
        return set(self.span()) | set(self.selection())

    def start_visual(self):
        if self.folded:
            return self.say("v selects problems: zR to unfold first", True)
        self.anchor = self.cur
        self.say("-- VISUAL --  + - W r :space :width change them; d y cut or copy; :group TITLE; Esc ends")

    def end_visual(self):
        if self.anchor is not None:
            self.last_sel = (self.anchor, self.cur)
        self.anchor = None

    def reselect(self):
        """gv: the last selection again."""
        ts = self.targets()
        if not self.last_sel or self.folded or not all(t in ts for t in self.last_sel):
            return self.say("no selection to bring back", True)
        self.anchor, self.cur = self.last_sel

    def cut_selection(self, keep=False):
        """d / y on a selection: cut or copy every problem in it (across sections)."""
        ps = self.selection()
        self.end_visual()
        self.cur = min(ps + [self.cur]) if ps else self.cur
        if not ps:
            return self.say("no problems selected", True)
        secs = self.sheet["sections"]
        self.reg = dict(kind="items", what=copy.deepcopy([self.item(p) for p in ps]), cut=not keep)
        if not keep:
            def go():
                for si, ii in reversed(ps):
                    del secs[si]["items"][ii]
            self.change(go)
        what = f"{len(ps)} problem{'s' * (len(ps) > 1)}"
        self.say(f"{what} copied: p pastes new ones like them" if keep else f"{what} cut: p pastes them")

    def group(self, title):
        """:group TITLE: the selection (or what the cursor is on) into a new section."""
        ps = self.scope()
        self.end_visual()
        def go():
            self.cur = (E.group(self.sheet, ps, title), -1)
        if self.change(go):
            self.say(f"{len(ps)} problem{'s' * (len(ps) > 1)} grouped" + (f" under {title}" if title else ""))

    # -- changes on the sheet ---------------------------------------------
    def scope(self):
        """The items a change applies to: the selection, the problem under the
        cursor, every problem of a section on its header, or every problem on the
        sheet header."""
        if self.anchor is not None:
            return self.selection()
        si, ii = self.cur
        if ii >= 0:
            return [self.cur]
        return E.positions(self.sheet, None if si < 0 else si)

    def reroll(self, n=1, section=False, everything=False):
        si, ii = self.cur
        if everything:
            ps = E.positions(self.sheet)
        elif self.anchor is not None and not section:
            ps = self.selection()
        elif section or ii < 0:
            ps = E.positions(self.sheet, None if si < 0 else si)
        else:
            ps = E.positions(self.sheet)
            k = ps.index(self.cur)
            ps = ps[k:k + n]
        if not ps:
            return self.say("nothing to reroll here", True)
        if self.change(lambda: E.reroll(self.sheet, ps, self.seeds())):
            self.say(f"{len(ps)} rerolled" if len(ps) > 1 else "rerolled")
        self.last_change = lambda: self.reroll(n, section, everything)

    def toggle_width(self):
        ps = self.scope()
        if not ps:
            return
        to = "full" if self.item(ps[0])["width"] == "half" else "half"
        self.change(lambda: [E.set_width(self.item(p), to) for p in ps])
        self.say(f"{'all ' + str(len(ps)) + ' ' if len(ps) > 1 else ''}{to} width")
        self.last_change = self.toggle_width

    def space(self, steps):
        ps = self.scope()
        if ps:
            self.change(lambda: [E.bump_space(self.item(p), steps) for p in ps])
            self.say(f"work space {self.item(ps[0])['space']}" + (f" (and {len(ps) - 1} more)" if len(ps) > 1 else ""))
        self.last_change = lambda: self.space(steps)

    def set_space(self, text):
        x = E.inches(text)
        ps = self.scope()
        self.change(lambda: [self.item(p).__setitem__("space", E.length(x)) for p in ps])

    def set_width(self, text):
        w = text.strip().lower()
        if w not in sh.WIDTHS:
            return self.say("usage: :width half|full", True)
        ps = self.scope()
        self.change(lambda: [E.set_width(self.item(p), w) for p in ps])

    def move(self, n):
        si, ii = self.cur
        if si < 0:
            return
        def go():
            if ii >= 0:
                self.cur = E.move_item(self.sheet, self.cur, n)
            else:
                self.cur = (E.move_section(self.sheet, si, n), -1)
        self.change(go)
        self.last_change = lambda: self.move(n)

    def cut(self, n=1, keep=False):
        """dd / yy: cut (or copy) n problems, or the section on its header."""
        si, ii = self.cur
        if si < 0:
            return self.say("dd and yy work on a problem or a section header", True)
        secs = self.sheet["sections"]
        if ii < 0:
            self.reg = dict(kind="section", what=copy.deepcopy(secs[si]), cut=not keep)
            if not keep:
                self.change(lambda: secs.pop(si))
            return self.say("section " + ("copied: p pastes it with new problems" if keep else "cut: p pastes it"))
        its = secs[si]["items"][ii:ii + n]
        self.reg = dict(kind="items", what=copy.deepcopy(its), cut=not keep)
        if not keep:
            self.change(lambda: secs[si]["items"].__delitem__(slice(ii, ii + n)))
        what = f"{len(its)} problem{'s' * (len(its) > 1)}"
        self.say(f"{what} copied: p pastes new ones like {'them' if len(its) > 1 else 'it'}" if keep
                 else f"{what} cut: p pastes {'them' if len(its) > 1 else 'it'}")

    def paste(self, below=True, n=1):
        """p / P. A cut pastes exactly what was cut (once); a copy pastes newly drawn problems."""
        if not self.reg:
            return self.say("nothing to paste: dd or yy first", True)
        reg = self.reg
        si, ii = self.cur
        secs = self.sheet["sections"]
        def fresh(it):
            return E.fresh_copy(self.sheet, it, next(self.seeds())) if it["seed"] is not None and not it["edited"] \
                else copy.deepcopy(it)
        def go():
            for _ in range(n):
                if reg["kind"] == "section":
                    sec = copy.deepcopy(reg["what"])
                    if not reg["cut"]:
                        sec["auto"] = ""
                        sec["items"] = []
                    at = 0 if si < 0 else si + (1 if below else 0)
                    secs.insert(at, sec)
                    if not reg["cut"]:
                        for it in reg["what"]["items"]:
                            sec["items"].append(fresh(it))
                    self.cur = (at, -1)
                else:
                    if not secs:
                        secs.append(sh.new_section())
                    tsi = max(si, 0)
                    at = (ii + 1 if below else ii) if ii >= 0 else 0
                    for k, it in enumerate(reg["what"]):
                        secs[tsi]["items"].insert(at + k, copy.deepcopy(it) if reg["cut"] else fresh(it))
                    self.cur = (tsi, at)
                sh.fill_versions(self.sheet)
                reg["cut"] = False                     # pasting again makes new ones, never duplicates
        self.change(go)
        self.last_change = lambda: self.paste(below, n)

    def new_section(self, below=True):
        si = self.cur[0]
        at = 0 if si < 0 else si + (1 if below else 0)
        def go():
            self.sheet["sections"].insert(at, sh.new_section())
            self.cur = (at, -1)
        self.change(go)
        self.start_edit(("title", at), "")

    def join(self):
        si = self.cur[0]
        if si < 0:
            return self.say("move to a section first", True)
        if self.change(lambda: E.join(self.sheet, si)):
            self.say("joined (u to undo)")

    def rename(self, text, si=None):
        si = self.cur[0] if si is None else si
        text = text.strip()
        if si < 0:
            if not text:
                return self.say("the title can't be empty", True)
            return self.change(lambda: self.sheet.__setitem__("title", text))
        self.change(lambda: self.sheet["sections"][si].__setitem__("title", text))

    def set_instructions(self, text, si=None):
        si = self.cur[0] if si is None else si
        target = self.sheet if si < 0 else self.sheet["sections"][si]
        self.change(lambda: target.__setitem__("instructions", text.strip()))

    def edit_problem(self, text, pos):
        status = None
        def go():
            nonlocal status
            status = E.edit_problem(self.sheet, pos, text)
        if self.change(go):
            self.say({"checked": "edited; the answer was solved again and checks",
                      "failed": "edited, but the answer FAILS its check: A edits the answer",
                      "unchecked": "edited; the answer can't be checked"}[status], status == "failed")

    def edit_answer(self, text, pos):
        status = None
        def go():
            nonlocal status
            status = E.edit_answer(self.sheet, pos, text)
        if self.change(go):
            self.say({"checked": "answer checks", "failed": "that answer FAILS its check",
                      "unchecked": "answer kept; it can't be checked"}[status], status == "failed")

    def regroup(self, tokens):
        try:
            groups = mp.parse_groups(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        self.change(lambda: mp.regroup(self.sheet, groups, self.rng))
        self.cur = SHEET
        self.go(1)

    def redraft(self, tokens):
        try:
            mix = mp.parse_mix(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        def go():
            new = mp.draft(mix, self.sheet["versions"], self.rng.randrange(2**31))
            self.sheet["sections"] = new["sections"]
            defaults = [banks.get(n) for n in banks.names()]
            if self.sheet["instructions"] in [b.INSTRUCTIONS for b in defaults]:   # still a bank's default
                self.sheet["instructions"] = new["instructions"]
            if self.sheet["title"] in [mp.DEFAULTS["title"]] + [f"{b.TITLE} Practice" for b in defaults]:
                self.sheet["title"] = new["title"]
        if self.change(go):
            self.cur = SHEET
            self.clamp()
            self.say(f"new sheet: {self.total()} problems (u to undo)")

    # -- the sheet, drawn ----------------------------------------------------
    def render(self, width):
        """The sheet as the page shows it, for a pane `width` columns wide.
        Returns (lines, span): each line is [(x, text, style, target)], and
        span is the (first, last) line of the cursor's target."""
        sheet, v, width = self.sheet, self.version, max(30, width)
        lines, span = [], [None, None]
        def emit(*segs):
            segs = [sg for sg in segs if sg[1]]
            if any(sg[3] == self.cur for sg in segs):
                span[0] = len(lines) if span[0] is None else span[0]
                span[1] = len(lines)
            lines.append(segs)
        un, bad = self.statuses()
        info = [f"Version {v + 1}/{sheet['versions']}", f"answers {'on' if self.answers else 'off'} (za)",
                f"{'compact' if self.compact else 'work space shown'} (zs)"]
        emit((0, " · ".join(info), "dim", None))
        emit()
        r1, r2 = "Name ______________", f"Date ________  Ver: {v + 1}"
        emit((0, sheet["class_name"], "plain", SHEET), (max(len(sheet["class_name"]) + 2, width - len(r1)), r1, "plain", SHEET))
        emit((0, sheet["title"], "title", SHEET), (max(len(sheet["title"]) + 2, width - len(r2)), r2, "plain", SHEET))
        for l in textwrap.wrap(sheet["instructions"], width):
            emit((0, l, "ital", SHEET))
        if not sheet["sections"]:
            emit()
            emit((0, "No problems yet. On the types pane, l adds one;", "dim", None))
            emit((0, ":mix all:2 drafts two of every type.", "dim", None))
            return lines, tuple(span)

        used, page, n = HEADER_IN + LINE_IN * len(textwrap.wrap(sheet["instructions"], 90)), 1, 0
        def page_break():
            nonlocal used, page
            page += 1
            used = 0.0
            emit((0, f"{'─' * 6} page {page} (about here) {'─' * max(0, width - 30)}", "page", None))
        def prompt_h(it):
            b, p = banks.get(it["bank"]), sh.problem(it, v)
            if hasattr(b, "height"):
                return b.height(p)
            return FRAC_IN if "/" in p["prompt"] else PLAIN_IN
        def fits(h):                                  # the last gap may hang off the page
            return used + h - (FRAC_IN - PLAIN_IN) - 0.05 <= PAGE_IN

        for si, sec in enumerate(sheet["sections"]):
            H = (si, -1)
            rows = sh.rows(sec["items"])
            ins = textwrap.wrap(sec["instructions"], width) if sec["instructions"] else []
            head_h = (TITLE_IN if sec["title"] else 0) + LINE_IN * len(ins)
            first_h = (max(map(prompt_h, rows[0])) + max(E.inches(it["space"]) for it in rows[0])) if rows else 0
            if not self.folded and not fits(head_h + first_h) and used > HEADER_IN:
                page_break()
            used += head_h
            if not self.folded or si == 0:
                emit()
            bk, _, typ = sec.get("auto", "").partition(":")
            style = "special" if bk and typ and banks.get(bk).special(typ) else "head"
            title = (0, sec["title"], style, H) if sec["title"] else (0, "(untitled section: no header)", "dim", H)
            extra = (len(title[1]) + 2, f"{len(sec['items'])} problem{'s' * (len(sec['items']) != 1)}", "dim", H) \
                if self.folded else (0, "", "dim", H)
            emit(title, extra)
            for l in ins:
                emit((0, l, "ital", H))
            if self.folded:
                continue
            if not rows:
                emit((2, "(empty: p pastes here, or L on the types pane)", "dim", H))
            index = {id(it): ii for ii, it in enumerate(sec["items"])}
            for ri, row in enumerate(rows):
                row_h = max(map(prompt_h, row)) + max(E.inches(it["space"]) for it in row)
                if ri and not fits(row_h):
                    page_break()
                used += row_h
                colw = (width - 3) // 2 if row[0]["width"] == "half" else width
                cells = []
                for k, it in enumerate(row):
                    n += 1
                    x0, tgt = k * (colw + 3), (si, index[id(it)])
                    b, p = banks.get(it["bank"]), sh.problem(it, v)
                    mark = {"failed": "✗", "unchecked": "?"}.get(it["status"], "")
                    num = f"{mark}{n}."
                    body = [w for part in b.text(p).split("\n")
                            for w in textwrap.wrap(part, max(8, colw - len(num) - 1)) or [""]]
                    nstyle = {"failed": "err", "unchecked": "dim"}.get(it["status"], "plain")
                    cell = [[(x0, num, nstyle, tgt), (x0 + len(num) + 1, body[0], "plain", tgt)]]
                    cell += [[(x0 + len(num) + 1, l, "plain", tgt)] for l in body[1:]]
                    if self.answers:
                        a = b.answer_text(p)[:colw - 2]
                        cell.append([(x0 + max(len(num) + 1, colw - len(a)), a, "ans", tgt)])
                    cells.append(cell)
                tall = max(map(len, cells))
                for i in range(tall):
                    emit(*[sg for cell in cells if i < len(cell) for sg in cell[i]])
                if not self.compact:
                    blank = round(max(E.inches(it["space"]) for it in row) * 4) - (tall - 1)
                    for _ in range(max(0, blank)):
                        emit()
        if not self.folded:
            emit()
            emit((0, f"about {page} page{'s' * (page > 1)}" + (f" · {bad} failing" if bad else "")
                  + (f" · {un} unchecked" if un else ""), "dim", None))
        return lines, tuple(span)

    def where(self):
        """A short description of what the sheet cursor is on, for the status line."""
        si, ii = self.cur
        if si < 0:
            return "sheet header"
        it = self.item()
        if not it:
            return f"section {si + 1}"
        n = E.positions(self.sheet).index(self.cur) + 1
        src = it["entry"] if it["bank"] == mp.BANK else f"{it['bank']}:{it['entry']}"
        return f"#{n} {src} {it['width']} {it['space']}" + ("" if it["status"] == "checked" else f" {it['status']}")

    # -- files ---------------------------------------------------------
    def write(self):
        if not self.total():
            return self.say("E: nothing to write: the sheet is empty", True) or False
        out, name = self.s["out"], self.s["name"]
        sheet = copy.deepcopy(self.sheet)
        path = Path(out).expanduser().resolve() / f"{name}.sheet.json"
        sheet["command"] = f"python3 make_practice.py --sheet {shlex.quote(str(path))}"
        try:
            r = mp.build(sheet, out, name)
        except (RuntimeError, OSError) as e:
            self.say(f"E: {e}".splitlines()[0], True)
            return False
        self.written, self.last_build = self.snapshot(), r
        where = dir_label(r["out"])
        un, bad = self.statuses()
        warn = (f"  ·  {bad} failing answer{'s' * (bad > 1)} (✗)" if bad else "") + \
               (f"  ·  {un} unchecked" if un else "")
        self.say(f'"{where}/" {len(r["files"])} files written '
                 f'({"PDFs compiled" if r["compiled"] else "typst not found: .typ only"}){warn}', bool(bad))
        return True

    def open_file(self, args):
        if not self.last_build:
            return self.say("E: nothing written yet (:w first)", True)
        what, v = "sheet", 1
        for a in args:
            if a.isdigit():
                v = int(a)
            elif a in ("sheet", "key", "slides"):
                what = a
            else:
                return self.say("usage: :open [sheet|key|slides] [version]", True)
        b = self.last_build
        if not 1 <= v <= b["sheet"]["versions"]:
            return self.say(f"E: there are {b['sheet']['versions']} versions", True)
        suffix = {"sheet": "", "key": "_key", "slides": "_slides"}[what]
        f = b["out"] / f"{self.s['name']}_v{v}{suffix}.{'pdf' if b['compiled'] else 'typ'}"
        try:
            subprocess.Popen(["xdg-open", str(f)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
            self.say(f"opening {f.name}")
        except OSError as e:
            self.say(f"E: {e}", True)

    def load(self, path):
        """Open a .sheet.json (or convert an older practice .json) to edit."""
        p = Path(path).expanduser()
        try:
            sheet = mp.read_sheet(p)
        except (OSError, ValueError, KeyError, TypeError, SystemExit) as e:
            return self.say(f"E: can't open {path}: {e}", True)
        name = re.sub(r"(\.sheet\.json|_v\d+\.json|\.json)$", "", p.name)
        out = dir_label(p.resolve().parent)
        def go():
            self.s.update(sheet=sheet, out=out, name=name)
        self.change(go)
        self.cur, self.version = SHEET, 0
        self.clamp()
        older = not str(p).endswith(".sheet.json")
        if not older:
            self.written = self.snapshot()
        self.say(f'"{path}" opened: {self.total()} problems' +
                 (" (an older set, converted: :w saves it as a sheet)" if older else ""))

    # -- ex commands -----------------------------------------------------
    def ex(self, line):
        line = line.strip()
        if not line:
            return
        if line.isdigit():
            if self.focus == "preview":
                return self.go_problem(int(line))
            self.row = min(len(self.rows()), max(1, int(line))) - 1
            return
        cmd, _, rest = line.partition(" ")
        rest = rest.strip()
        bang = cmd.endswith("!")
        cmd = cmd.rstrip("!")
        if cmd in ("w", "write"):
            self.write()
        elif cmd in ("wq", "x", "xit"):
            if self.write():
                self.quit = True
        elif cmd in ("q", "quit", "qa", "qall"):
            if self.dirty() and self.total() and not bang:
                self.say("E37: No write since last change (add ! to override)", True)
            else:
                self.quit = True
        elif cmd == "mix":
            self.redraft(rest.split())
        elif cmd == "groups":
            try:
                self.regroup(shlex.split(rest))
            except ValueError as e:
                self.say(f"E: {e}", True)
        elif cmd == "shuffle":
            self.change(lambda: mp.shuffle_all(self.sheet, self.rng))
            self.cur = SHEET
            self.go(1)
        elif cmd == "reroll":
            if rest in ("", "all"):
                self.reroll(everything=True)
            elif rest == "section":
                self.reroll(section=True)
            else:
                self.say("usage: :reroll [all|section]", True)
        elif cmd == "space":
            try:
                self.set_space(rest)
            except ValueError as e:
                self.say(f"E: {e}", True)
        elif cmd == "width":
            self.set_width(rest)
        elif cmd == "join":
            self.join()
        elif cmd in ("group", "gr"):
            self.group(rest)
        elif cmd == "rename":
            self.rename(rest) if rest else self.say("usage: :rename NEW TITLE (empty title: cS, then Enter)", True)
        elif cmd == "clear":
            self.clear()
        elif cmd in ("versions", "title", "class", "instructions", "name", "out"):
            err = self.set_value(rest, self.rows().index(("set", cmd)))
            if err:
                self.say(f"E: {err}", True)
        elif cmd in ("set", "se"):
            self.ex_set(rest)
        elif cmd in ("e", "edit"):
            self.load(rest) if rest else self.say("usage: :e FILE.sheet.json", True)
        elif cmd == "open":
            self.open_file(rest.split())
        elif cmd in ("h", "help"):
            self.mode = "help"
        else:
            self.say(f"E492: Not an editor command: {line}", True)

    def ex_set(self, rest):
        opts = rest.split()
        for i, o in enumerate(opts):            # text values keep their spaces
            if o.startswith(("title=", "class=", "instructions=")):
                opts = opts[:i] + [" ".join(opts[i:])]
                break
        for opt in opts:
            flag = opt.rstrip("!").removeprefix("no")
            if flag in ("answers", "compact", "wide"):
                val = (not getattr(self, flag)) if opt.endswith("!") else not opt.startswith("no")
                setattr(self, flag, val)
            elif "=" in opt:
                k, _, v = opt.partition("=")
                k = k.strip()
                if k not in SETTINGS:
                    return self.say(f"E518: Unknown option: {k}", True)
                err = self.set_value(v, self.rows().index(("set", k)))
                if err:
                    return self.say(f"E: {err}", True)
            else:
                return self.say(f"E518: Unknown option: {opt}", True)

    def search(self, q, step=1):
        if not q:
            return
        ql = q.lower()
        if self.focus == "preview":
            ts = self.targets()
            i = ts.index(self.cur) if self.cur in ts else 0
            for k in range(1, len(ts) + 1):
                t = ts[(i + step * k) % len(ts)]
                if ql in self.target_text(t).lower():
                    self.cur = t
                    return self.say(f"/{q}")
        else:                                   # every row of every bank, opening what it finds
            rows, here = self.rows(everything=True), self.rid()
            i = rows.index(here) if here in rows else 0
            for k in range(1, len(rows) + 1):
                rid = rows[(i + step * k) % len(rows)]
                if ql in self.row_text(rid).lower():
                    kind, key = rid
                    if kind != "set":
                        self.open.add(key if kind == "bank" else key[0])
                    if kind == "problem":
                        self.open_types.add((key[0], banks.get(key[0]).PROBLEM[key[1]]["type"]))
                    self.row = self.rows().index(rid)
                    return self.say(f"/{q}")
        self.say(f"E486: Pattern not found: {q}", True)

    def row_text(self, rid):
        """What / searches on a left-pane row."""
        kind, key = rid
        if kind == "bank":
            return f"{key} {banks.get(key).TITLE}"
        if kind == "count":
            b, e = banks.get(key[0]), banks.get(key[0]).ENTRY[key[1]]
            hint = b.hint(b.type_of(key[1])) if hasattr(b, "hint") else None
            return f"{key[1]} {e['title']} {hint[0] if hint else ''}"
        if kind == "problem":
            b = banks.get(key[0])
            return f"{key[1]} {b.text(b.problem(key[1]))}"
        return key

    def target_text(self, t):
        si, ii = t
        if si < 0:
            return f"{self.sheet['title']} {self.sheet['instructions']}"
        sec = self.sheet["sections"][si]
        if ii < 0:
            return f"{sec['title']} {sec['instructions']}"
        it = sec["items"][ii]
        b, p = banks.get(it["bank"]), sh.problem(it, self.version)
        return f"{b.text(p)} {b.answer_text(p)} {p['prompt']} {it['entry']}"

    # -- keys ------------------------------------------------------------
    def key(self, ch, page=10):
        """Handle one key (an int as from curses getch, or a 1-char str)."""
        if isinstance(ch, str):
            ch = ord(ch)
        if self.mode == "help":
            self.mode = "normal"
            return
        if self.mode in ("insert", "command", "search"):
            return self.key_line(ch)
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        self.msg, self.err = "", False
        sheet = self.focus == "preview"

        if self.pending:
            p, self.pending = self.pending, ""
            n = int(self.count) if self.count else None
            self.count = ""
            combo = p + c
            if combo == "gg":
                if sheet:
                    self.go_problem(n) if n else self.go(-10**6)
                else:
                    self.row = min((n or 1) - 1, len(self.rows()) - 1)
            elif combo == "gt":
                self.version = min(n, self.sheet["versions"]) - 1 if n else (self.version + 1) % self.sheet["versions"]
            elif combo == "gv":
                self.reselect() if sheet else self.say("gv selects on the sheet (Tab to it)", True)
            elif combo == "gT":
                self.version = (self.version - (n or 1)) % self.sheet["versions"]
            elif combo == "dd":
                self.cut(n or 1) if sheet else self.zero()
            elif combo == "yy":
                self.cut(n or 1, keep=True) if sheet else self.say("yy copies on the sheet (Tab to it)", True)
            elif combo == "cc":
                self.start_insert(clear=True)
            elif combo == "cS":
                self.start_edit(("title", self.cur[0]))
            elif combo == "cI":
                self.start_edit(("instructions", self.cur[0]))
            elif combo == "ZZ":
                self.ex("x")
            elif combo == "ZQ":
                self.quit = True
            elif combo == "za":
                self.answers = not self.answers
            elif combo == "zs":
                self.compact = not self.compact
            elif combo in ("zM", "zR") and not sheet:
                self.fold_banks(combo == "zM")
            elif combo in ("zM", "zR"):
                self.folded = combo == "zM"
                if self.folded:
                    self.end_visual()
                if self.folded and self.cur[1] >= 0:
                    self.cur = (self.cur[0], -1)
                self.clamp()
            elif combo in ("]]", "[["):
                for _ in range(n or 1):
                    self.section_jump(1 if c == "]" else -1)
            elif p == "\x17" and c in ("w", "\x17", "h", "l"):
                self.set_focus({"h": "left", "l": "preview"}.get(c) or self.other_focus())
            elif p == "\x17" and c == "o":
                self.wide = not self.wide
                if self.wide:
                    self.set_focus("preview")
                self.say("the sheet full width (^W o splits)" if self.wide else "the sheet beside the banks")
            return

        if c.isdigit() and (c != "0" or self.count):
            self.count += c
            return
        n = int(self.count) if self.count else 1
        had_count = bool(self.count)
        self.count = ""

        if sheet and self.anchor is not None and c in ("d", "x", "y"):
            self.cut_selection(keep=(c == "y"))
        elif c == "\x1b":
            self.end_visual()
        elif c == "v":
            self.end_visual() if self.anchor is not None else \
                self.start_visual() if sheet else self.say("v selects on the sheet (Tab to it)", True)
        elif c and c in "gdcZz\x17y][":
            if c == "y" and not sheet:
                return
            self.pending = c
            if had_count:
                self.count = str(n)
        elif c == "j" or ch == curses.KEY_DOWN:
            self.go(n) if sheet else self.move_row(n)
        elif c == "k" or ch == curses.KEY_UP:
            self.go(-n) if sheet else self.move_row(-n)
        elif c == "G":
            if sheet:
                self.go_problem(n) if had_count else self.go(10**6)
            else:
                self.row = min(n, len(self.rows())) - 1 if had_count else len(self.rows()) - 1
        elif c in ("\x04", "\x15", "\x06", "\x02") or ch in (curses.KEY_NPAGE, curses.KEY_PPAGE):
            big = c in ("\x06", "\x02") or ch in (curses.KEY_NPAGE, curses.KEY_PPAGE)
            d = (1 if c in ("\x04", "\x06") or ch == curses.KEY_NPAGE else -1) * n * (10 if big else 5)
            self.go(d) if sheet else self.move_row(d)
        elif sheet and self.key_sheet(c, ch, n):
            pass
        elif c in ("l", "+", "\x01") or ch == curses.KEY_RIGHT:
            self.bump(n)
        elif c in ("h", "-", "\x18") or ch == curses.KEY_LEFT:
            self.bump(-n)
        elif c == "L":
            self.add_here(n)
        elif c == "o":
            self.toggle_open()
        elif c == "x":
            self.zero()
        elif c == "D":
            self.clear()
        elif c in ("i", "a", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert()
        elif c == "s":
            self.start_insert(clear=True)
        elif c == "r":
            self.reroll_entry()
        elif c == "u":
            self.do_undo(n)
        elif c == "\x12":
            self.do_redo(n)
        elif c == ".":
            self.repeat(n)
        elif c == ":":
            self.mode, self.buf = "command", ""
            self.hist_i = len(self.cmd_hist)
        elif c == "/":
            self.mode, self.buf = "search", ""
        elif c == "n":
            self.search(self.search_q, 1)
        elif c == "N":
            self.search(self.search_q, -1)
        elif c == "?":
            self.mode = "help"
        elif c == "\t":
            self.set_focus(self.other_focus())
        elif c == "\x03":
            self.say("Type  :q!  and press Enter to quit")

    def key_sheet(self, c, ch, n):
        """Keys that mean something else on the sheet. True if handled here."""
        if c == "l" or ch == curses.KEY_RIGHT:
            self.column(1)
        elif c == "h" or ch == curses.KEY_LEFT:
            self.column(-1)
        elif c == "r":
            self.reroll(n)
        elif c == "R":
            self.reroll(section=True)
        elif c == "W":
            self.toggle_width()
        elif c in ("+", "\x01"):
            self.space(n)
        elif c in ("-", "\x18"):
            self.space(-n)
        elif c in ("i", "a", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert()
        elif c in ("A", "s"):
            if c == "A" and not self.item():
                self.say("A edits a problem's answer: move to a problem", True)
            else:
                self.start_insert(clear=(c == "s"), answer=(c == "A"))
        elif c == "x":
            self.cut(n)
        elif c in ("p", "P"):
            self.paste(c == "p", n)
        elif c == "J":
            self.move(n)
        elif c == "K":
            self.move(-n)
        elif c in ("o", "O"):
            self.new_section(c == "o")
        elif c in ("L", "D"):
            self.say(f"{c} works on the types pane (Tab back to it)", True)
        else:
            return False
        return True

    def other_focus(self):
        return "left" if self.focus == "preview" else "preview"

    def set_focus(self, f):
        if f != "preview":
            self.end_visual()
        self.focus = f
        if f == "preview" and self.cur == SHEET and sh.items(self.sheet) and not self.folded:
            self.cur = next(t for t in self.targets() if t[1] >= 0)

    def move_row(self, n):
        self.row = min(len(self.rows()) - 1, max(0, self.row + n))

    # -- typing a value ------------------------------------------------
    def start_edit(self, what, buf=None):
        """Type a new value for what: ("row", r), ("title", si), ("instructions", si),
        ("problem", pos), ("answer", pos). buf starts as the current text."""
        kind, ref = what
        if buf is None:
            if kind == "row":
                v = self.value(ref)
                buf = "" if isinstance(v, bool) else str(v)
            elif kind in ("title", "instructions"):
                obj = self.sheet if ref < 0 else self.sheet["sections"][ref]
                buf = obj[kind]
            else:
                it = self.item(ref)
                b = banks.get(it["bank"])
                buf = b.edit_text(it["problem"]) if kind == "problem" else b.answer_edit_text(it["problem"])
        self.mode, self.editing, self.buf = "insert", what, buf

    def start_insert(self, clear=False, answer=False):
        if self.focus != "preview":
            return self.start_edit(("row", self.row), "" if clear else None)
        si, ii = self.cur
        if ii >= 0:
            return self.start_edit(("answer" if answer else "problem", self.cur), "" if clear else None)
        self.start_edit(("title", si), "" if clear else None)

    def finish_edit(self, buf):
        kind, ref = self.editing
        self.editing = None
        if kind == "row":
            err = self.set_value(buf, ref)
            if err:
                self.say(f"E: {err}", True)
        elif kind == "title":
            self.rename(buf, ref)
        elif kind == "instructions":
            self.set_instructions(buf, ref)
        elif kind == "problem":
            self.edit_problem(buf, ref)
        elif kind == "answer":
            self.edit_answer(buf, ref)

    def edit_label(self):
        kind, ref = self.editing
        if kind == "row":
            k, key = self.rid(ref)
            return f"{'count of ' + key[1] if k == 'count' else key}: "
        if kind in ("title", "instructions"):
            return f"{'sheet' if ref < 0 else 'section'} {kind}: "
        return {"problem": "problem (equation ; unknown): ", "answer": "answer: "}[kind]

    def completing(self):
        """What Tab completes in the line being typed: (start, dirs_only), or None.
        The out setting and :out complete folders; :e completes files too."""
        if self.mode == "insert" and self.editing and self.editing[0] == "row":
            return (0, True) if self.rid(self.editing[1]) == ("set", "out") else None
        if self.mode == "command":
            m = re.match(r"\s*(?:(out|e|edit)\s+|set\s+out=)", self.buf)
            if m:
                return m.end(), m.group(1) not in ("e", "edit")
        return None

    def complete(self, step):
        """Tab / Shift-Tab: the next or previous name the path could become, as in
        Neovim: the first match at once, then each in turn, then what was typed."""
        c = self.comp
        if not (c and c["buf"] == self.buf):
            where = self.completing()
            if not where:
                return
            start, dirs_only = where
            word = self.buf[start:]
            matches = complete_path(word, dirs_only)
            if not matches:
                self.comp = None
                return
            if len(matches) == 1:               # done: the next Tab looks inside it
                self.buf, self.comp = self.buf[:start] + matches[0], None
                return
            c = self.comp = dict(start=start, options=matches + [word], i=-1 if step > 0 else len(matches))
        c["i"] = (c["i"] + step) % len(c["options"])
        self.buf = c["buf"] = self.buf[:c["start"]] + c["options"][c["i"]]

    def key_line(self, ch):
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        if c == "\t" or ch == curses.KEY_BTAB:
            return self.complete(-1 if ch == curses.KEY_BTAB else 1)
        self.comp = None
        if c == "\x1b" or (c == "\x03"):
            self.mode, self.buf, self.editing = "normal", "", None
        elif c in ("\n", "\r") or ch == curses.KEY_ENTER:
            mode, buf = self.mode, self.buf
            self.mode, self.buf = "normal", ""
            if mode == "insert":
                self.finish_edit(buf)
            elif mode == "command":
                if buf.strip():
                    self.cmd_hist.append(buf)
                self.ex(buf)
            else:
                self.search_q = buf or self.search_q
                self.search(self.search_q)
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if not self.buf and self.mode != "insert":
                self.mode = "normal"
            self.buf = self.buf[:-1]
        elif c == "\x15":
            self.buf = ""
        elif c == "\x17":
            self.buf = re.sub(r"\S*\s*$", "", self.buf.rstrip()) if self.buf.strip() else ""
        elif self.mode == "command" and ch in (curses.KEY_UP, curses.KEY_DOWN) and self.cmd_hist:
            self.hist_i = max(0, min(len(self.cmd_hist), self.hist_i + (-1 if ch == curses.KEY_UP else 1)))
            self.buf = self.cmd_hist[self.hist_i] if self.hist_i < len(self.cmd_hist) else ""
        elif c.isprintable() and c:
            self.buf += c

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
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

def complete_path(text, dirs_only=False):
    """The names a partly typed path could become, as Neovim completes them:
    ~ is home, a relative path starts in the current folder, folders end in /,
    and hidden names show only when the part typed starts with a dot."""
    if text == "~":
        return ["~/"]
    head, sep, frag = text.rpartition("/")
    folder = Path(os.path.expanduser(head + sep) if sep else ".")
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
        elif not dirs_only:
            out.append(head + sep + e.name)
    return out

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------

def cursor(visible):
    try:                                # some terminals can't hide the cursor
        curses.curs_set(visible)
    except curses.error:
        pass

def left_width(app, w):
    """How wide the banks pane is in a terminal `w` columns wide (0: hidden)."""
    full = max(40, min(55, w - 50))
    if app.focus != "preview":
        return full
    if app.wide:
        return 0
    return 30 if w - full - 3 < SHEET_MIN else full    # a narrow terminal: give the sheet room

class Screen:
    def __init__(self, scr):
        self.scr = scr
        cursor(0)
        P = lambda i: 0                                # monochrome fallback
        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
                bg = -1
            except curses.error:
                bg = curses.COLOR_BLACK
            for i, (fg, b) in enumerate([(curses.COLOR_CYAN, bg), (curses.COLOR_RED, bg),
                                         (curses.COLOR_YELLOW, bg), (curses.COLOR_GREEN, bg),
                                         (curses.COLOR_BLACK, curses.COLOR_BLUE),
                                         (curses.COLOR_BLACK, curses.COLOR_GREEN),
                                         (curses.COLOR_BLACK, curses.COLOR_YELLOW),
                                         (curses.COLOR_BLACK, curses.COLOR_MAGENTA),
                                         (curses.COLOR_BLACK, curses.COLOR_CYAN)], 1):
                curses.init_pair(i, fg, b)
            P = curses.color_pair
        italic = getattr(curses, "A_ITALIC", curses.A_DIM)
        self.st = dict(plain=0, head=P(1) | curses.A_BOLD, ans=P(2), special=P(3) | curses.A_BOLD,
                       dim=curses.A_DIM, count=P(4) | curses.A_BOLD, err=P(2) | curses.A_BOLD,
                       title=curses.A_BOLD, ital=italic, page=P(3) | curses.A_DIM,
                       normal=P(5) | curses.A_BOLD, insert=P(6) | curses.A_BOLD,
                       command=P(7) | curses.A_BOLD, search=P(7) | curses.A_BOLD,
                       visual=P(8) | curses.A_BOLD,
                       sel=P(9) if curses.has_colors() else curses.A_UNDERLINE)   # the cursor is reversed

    def put(self, y, x, text, attr=0, width=None):
        h, w = self.scr.getmaxyx()
        if y < 0 or y >= h or x >= w or x < 0:
            return
        width = min(width if width is not None else w - x, w - x)
        if width <= 0:
            return
        if len(text) > width:
            text = text[:max(0, width - 1)] + "…"
        try:
            self.scr.addstr(y, x, text, attr)
        except curses.error:            # writing the bottom-right cell
            pass

    def draw(self, app):
        scr, st = self.scr, self.st
        scr.erase()
        h, w = scr.getmaxyx()
        if h < 14 or w < 72:
            self.put(0, 0, f"Make the terminal at least 72x14 (now {w}x{h}).  :q! quits.")
            return self.cmdline(app, h, w)
        body = h - 3                                   # title, status, command lines
        on_sheet = app.focus == "preview"
        LEFT_W = left_width(app, w)
        tab = lambda on: st["normal"] if on else st["dim"]      # the focused pane's label stands out
        if LEFT_W:
            self.put(0, 1, " BANKS ", tab(not on_sheet))
        self.put(0, LEFT_W + 1, " SHEET · " + app.sheet["title"] + " ", tab(on_sheet), w - LEFT_W - 14)
        self.put(0, w - 12, "? for help", st["dim"])
        if LEFT_W:
            self.types_view(app, body, LEFT_W)
            for y in range(1, body + 1):
                self.put(y, LEFT_W, "│", st["dim"])

        px = LEFT_W + 2 if LEFT_W else 1
        pw = w - px - 1
        lines, (first, last) = app.render(pw)
        if first is not None:                         # keep the sheet cursor in view
            if first < app.pv_top:
                app.pv_top = max(0, first - 2)
            elif last >= app.pv_top + body:
                app.pv_top = min(first - 2, last - body + 1)
        app.pv_top = max(0, min(app.pv_top, len(lines) - body))
        sel = app.selected()
        for y, segs in enumerate(lines[app.pv_top:app.pv_top + body], 1):
            for x, text, style, tgt in segs:
                attr = st[style]
                if tgt is not None and tgt == app.cur:
                    attr |= curses.A_REVERSE if on_sheet else curses.A_UNDERLINE
                elif tgt in sel:
                    attr = st["sel"]
                self.put(y, px + x, text, attr, pw - x)
        where = ""
        if len(lines) > body:
            where = "Top" if app.pv_top == 0 else "Bot" if app.pv_top >= len(lines) - body else \
                f"{100 * app.pv_top // (len(lines) - body)}%"
        self.status(app, h, w, where)

    def types_view(self, app, body, LEFT_W):
        st = self.st
        rows = app.rows()
        nset = len(SETTINGS)
        lines = [(None, i) for i in range(len(rows) - nset)] + \
                [("", None), ("SETTINGS", None)] + [(None, i) for i in range(len(rows) - nset, len(rows))]
        app.row = min(app.row, len(rows) - 1)
        cur = next(j for j, (_, i) in enumerate(lines) if i == app.row)
        top = max(0, min(cur - body // 2, len(lines) - body))
        room = LEFT_W - 3
        for y, (hdr, i) in enumerate(lines[top:top + body], 1):
            if hdr is not None:
                self.put(y, 1, hdr, st["dim"] | curses.A_BOLD)
                continue
            kind, key = rows[i]
            attr_t = 0
            if kind == "bank":
                b = banks.get(key)
                size = f" ({len(b.PROBLEMS)})" if getattr(b, "FIXED", False) else ""
                text = f"{'▾' if key in app.open else '▸'} {b.TITLE}{size}"
                n = app.value(i)
                val, attr_v, attr_t = (str(n) if n else "·"), (st["count"] if n else st["dim"]), curses.A_BOLD
            elif kind == "count":
                b, e = banks.get(key[0]), banks.get(key[0]).ENTRY[key[1]]
                if getattr(b, "FIXED", False):
                    arrow = "▾" if key in app.open_types else "▸"
                    text = f"  {arrow}{key[1]:>3}  {e['title']} ({e['count']})"
                elif e.get("kind") == "formulas":
                    text = f"   {key[1]:>3}    real formulas"
                else:
                    text = f"   {key[1]:>3}  {e['title']}"
                n = app.value(i)
                val, attr_v = (str(n) if n else "·"), (st["count"] if n else st["dim"])
                attr_t = st["special"] if b.special(b.type_of(key[1])) else 0
            elif kind == "problem":
                b = banks.get(key[0])
                on = app.value(i)
                text = f"       {key[1]:>3}. {b.text(b.problem(key[1]))}"
                val, attr_v = ("●" if on else "·"), (st["count"] if on else st["dim"])
            else:
                text, val = f" {key}", str(app.value(i)) or "(none)"
                attr_v = st["count"]
            val = val if len(val) <= room - 14 else val[:room - 15] + "…"
            space = room - len(val) - 1                # always a gap before the value
            text = text if len(text) <= space else text[:space - 1] + "…"
            row = text.ljust(space + 1) + val + " "
            if i == app.row:
                self.put(y, 1, row, curses.A_REVERSE | (curses.A_BOLD if app.focus == "left" else 0))
            else:
                self.put(y, 1, text, attr_t)
                self.put(y, 1 + space + 1, val, attr_v)
        free = body - min(len(lines), body) - 1
        if free >= 3:
            self.hint(app, rows[app.row], len(lines) + 2, free, LEFT_W)

    def hint(self, app, rid, y0, free, LEFT_W):
        """Under the tree, if there's room: what the row under the cursor is."""
        kind, key = rid
        if kind == "bank":
            b = banks.get(key)
            hint = (f"{b.TITLE}: written problems. o opens it; o on a type lists its problems. l on a type adds one "
                    f"at random; l on a problem adds that one." if getattr(b, "FIXED", False) else
                    f"{b.TITLE}: draws new problems. o opens or closes it. l on a type adds one.")
        elif kind == "count":
            b = banks.get(key[0])
            h = b.hint(b.type_of(key[1]))
            hint = f"Look for: {h[2]}  The move: {h[3]}" if h else b.ENTRY[key[1]]["title"]
        elif kind == "problem":
            b = banks.get(key[0])
            p = b.problem(key[1])
            hint = f"Answer: {b.answer_text(p)}.  l adds it, h removes it, L puts it at the sheet cursor."
        else:
            hint = SETTING_HINTS[key]
        hint = re.sub(r"\$([^$]*)\$", lambda m: pretty(m.group(1)), hint)
        for y, line in enumerate(textwrap.wrap(hint, LEFT_W - 3)[:free], y0):
            self.put(y, 1, line, self.st["dim"])

    def status(self, app, h, w, where):
        st = self.st
        look = "visual" if app.mode == "normal" and app.anchor is not None else app.mode
        mode = {"normal": "NORMAL", "insert": "INSERT", "command": "COMMAND",
                "search": "SEARCH", "help": "HELP", "visual": "VISUAL"}[look]
        self.put(h - 2, 0, " " * (w - 1), curses.A_REVERSE)
        self.put(h - 2, 0, f" {mode} ", st[look if look in st else "normal"])
        un, bad = app.statuses()
        v = app.sheet["versions"]
        info = (f" {app.total()} problem{'s' * (app.total() != 1)} × {v} version{'s' * (v != 1)}"
                + (f"  ·  {bad} failing" if bad else "") + (f"  ·  {un} unchecked" if un else "")
                + ("  ·  [+]" if app.dirty() else "")
                + (f"  ·  {len(app.selection())} selected" if app.anchor is not None else ""))
        self.put(h - 2, len(mode) + 2, info, curses.A_REVERSE)
        right = (f"{app.count}{app.pending.replace(chr(23), '^W')}  "
                 + (f"{app.where()}  sheet {where}" if app.focus == "preview" else "types") + " ")
        self.put(h - 2, w - len(right) - 1, right, curses.A_REVERSE)
        if app.comp:
            self.wildmenu(app, h, w)
        if app.mode == "help":
            self.help(h, w)
        self.cmdline(app, h, w)

    def wildmenu(self, app, h, w):
        """Over the status line while Tab cycles: the matches, the current one lit."""
        names = [m.rstrip("/").rsplit("/", 1)[-1] + ("/" if m.endswith("/") else "")
                 for m in app.comp["options"][:-1]]
        i, x = app.comp["i"], 1
        first = 0                                        # scroll so the current one shows
        while i < len(names) and sum(len(n) + 2 for n in names[first:i + 1]) > w - 6:
            first += 1
        self.put(h - 2, 0, " " * (w - 1), curses.A_REVERSE)
        if first:
            self.put(h - 2, 0, "<", curses.A_REVERSE)
        for k, n in enumerate(names[first:], first):
            if x + len(n) > w - 3:
                self.put(h - 2, w - 3, ">", curses.A_REVERSE)
                break
            self.put(h - 2, x, n, self.st["search"] if k == i else curses.A_REVERSE)
            x += len(n) + 2

    def help(self, h, w):
        lines = HELP.splitlines()
        bw = min(w - 2, max(map(len, lines)) + 4)
        bh = min(h - 2, len(lines) + 2)
        y0, x0 = max(0, (h - bh) // 2), max(0, (w - bw) // 2)
        for y in range(bh):
            self.put(y0 + y, x0, " " * bw, curses.A_REVERSE)
        for y, line in enumerate(lines[:bh - 2], 1):
            self.put(y0 + y, x0 + 2, line, curses.A_REVERSE, bw - 4)

    def cmdline(self, app, h, w):
        st = self.st
        if app.mode in ("command", "search", "insert"):
            prompt = app.edit_label() if app.mode == "insert" else ":" if app.mode == "command" else "/"
            text = prompt + app.buf
            self.put(h - 1, 0, text[-(w - 1):])
            cursor(1)
            try:
                self.scr.move(h - 1, min(len(text), w - 1))
            except curses.error:
                pass
        else:
            cursor(0)
            self.put(h - 1, 0, app.msg, st["err"] if app.err else 0)

def slow(app, ch):
    """Will this key take a moment (writing, or drawing many problems)?"""
    line = app.buf.strip()
    return ((app.mode == "command" and ch in ("\n", "\r") and re.match(r"(w|write|wq|x|xit|mix|reroll|versions)\b", line))
            or (app.mode == "normal" and app.pending == "Z" and ch == "Z"))

def run(scr, app):
    screen = Screen(scr)
    while not app.quit:
        h, _ = scr.getmaxyx()
        screen.draw(app)
        scr.refresh()
        try:
            ch = scr.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            ch = "\x03"
        if ch == curses.KEY_RESIZE:
            continue
        if slow(app, ch):                    # say so before the wait
            saved = app.mode, app.msg, app.err
            app.mode, app.msg, app.err = "normal", "working…", False
            screen.draw(app)
            scr.refresh()
            app.mode, app.msg, app.err = saved
        app.key(ch, page=max(2, h - 3))

def parse_args(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="a .sheet.json to open (or an older practice .json to convert)")
    ap.add_argument("--mix", nargs="+", default=[], metavar="ENTRY:COUNT")
    ap.add_argument("--versions", type=int, default=mp.DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP")
    ap.add_argument("--title", default=mp.DEFAULTS["title"])
    ap.add_argument("--out", default=mp.DEFAULTS["out"])
    ap.add_argument("--name", default=mp.DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", default=mp.DEFAULTS["class_name"], metavar="NAME")
    return ap.parse_args(argv)

def main():
    a = parse_args(sys.argv[1:])
    try:
        mix, groups = mp.parse_mix(a.mix), mp.parse_groups(a.groups)
    except ValueError as e:
        sys.exit(str(e))
    seed = a.seed if a.seed is not None else random.randrange(10**6)
    sheet = mp.draft(mix, a.versions, seed, a.shuffle, groups, a.title, a.class_name) if mix else \
        sh.new_sheet(a.title, a.class_name, mp.L.INSTRUCTIONS, a.versions)
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
