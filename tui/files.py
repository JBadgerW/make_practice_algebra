"""Writing, previewing, opening, and loading sheets."""
import copy, re, shlex, subprocess
from pathlib import Path
from sheets import draft, build, legacy
from sheets import sheet as sh, library, writer, present as presenter
from .common import dir_label, home_path, SHEET

class Files:
    # -- files ---------------------------------------------------------
    def write(self):
        if not self.total():
            return self.say("E: nothing to write: the sheet is empty", True) or False
        out, name = self.s["out"], self.s["name"]
        sheet = copy.deepcopy(self.sheet)
        path = Path(out).expanduser().resolve() / f"{name}.sheet.json"
        sheet["command"] = f"python3 make_practice.py --sheet {shlex.quote(str(path))}"
        try:
            r = build.build(sheet, out, name)
        except (RuntimeError, OSError) as e:
            self.say(f"E: {e}".splitlines()[0], True)
            return False
        self.written, self.last_build = self.snapshot(), r
        self.rev += 1                               # dirty() compares against the new written state
        try:
            library.save_config(out=home_path(r["out"]))   # the next session starts here
        except OSError:
            pass
        where = dir_label(r["out"])
        un, bad = self.statuses()
        warn = (f"  ·  {bad} failing answer{'s' * (bad > 1)} (✗)" if bad else "") + \
               (f"  ·  {un} unchecked" if un else "") + self.graph_warning()
        self.say(f'"{where}/" {len(r["files"])} files written '
                 f'({"PDFs compiled" if r["compiled"] else "typst not found: .typ only"}){warn}', bool(bad))
        return True

    def write_cmd(self, then=None, force=False):
        """:w, :wq: write, then (then="quit") quit or (then="new") start a new sheet.
        While the name is still the default, ask first: the name to write under,
        filled in, so Enter confirms it and typing changes it (Esc writes nothing).
        With ! there's no asking."""
        if self.total() and not force and self.s["name"] == draft.DEFAULTS["name"]:
            return self.start_edit(("write", then), self.s["name"])
        if self.write():
            if then == "quit":
                self.quit = True
            elif then == "new":
                self.new_sheet()

    def write_as(self, target, force=False):
        """:w NAME, :saveas NAME: the sheet goes by this name from now on (as the
        name setting; FOLDER/NAME sets out too), ready to be written under it.
        Without !, a name that would write over another sheet's file is refused.
        False (and an error shown, nothing changed) if it can't be."""
        target = re.sub(r"(\.sheet)?\.json$", "", target.strip())
        folder, slash, name = target.rpartition("/")
        out = self.in_out(folder or "/") if slash else self.s["out"]
        if not re.fullmatch(r"[\w.-]+", name):
            return self.say("E: write as NAME or FOLDER/NAME: a name may use letters, digits, _ . - only", True) or False
        here = lambda o, n: Path(o).expanduser().resolve() / f"{n}.sheet.json"
        new = here(out, name)
        if new != here(self.s["out"], self.s["name"]) and new.exists() and not force:
            return self.say(f"E13: {dir_label(new.parent)}/{new.name} exists (add ! to write over it)", True) or False
        if (out, name) != (self.s["out"], self.s["name"]):
            self.change(lambda: self.s.update(out=dir_label(out) if slash else out, name=name))
        return True

    def new_cmd(self, force=False):
        """:new: start a new sheet. With unsaved changes, ask first: write them
        (then start), discard them, or Esc to keep working. :new! doesn't ask."""
        if self.dirty() and self.total() and not force:
            return self.start_edit(("new", None), "")
        self.new_sheet()

    def new_sheet(self):
        """Close this sheet and start a blank one: the title, name, versions, form,
        and instructions go back to their defaults; the out folder, class, and
        course stay. Undoable, like :clear."""
        keep = {k: self.sheet.get(k) for k in ("class_name", "course")}
        def go():
            self.s.update(sheet=sh.new_sheet(draft.DEFAULTS["title"], keep["class_name"]),
                          name=draft.DEFAULTS["name"])
            self.sheet["course"] = keep["course"]
        self.end_visual()
        if not self.change(go):
            return
        self.cur, self.version, self.last_build = SHEET, 0, None
        self.clamp()
        self.say("new sheet (u to undo)")

    def graph_warning(self):
        """For a warm-up: the problems whose answer is a graph, which can't be lettered
        on the back, and those whose answer gives itself away with no decoy to hide it
        (by version, when there are several)."""
        if not sh.is_warmup(self.sheet):
            return ""
        out = ""
        for v in range(self.sheet["versions"]):
            ver = f"v{v + 1}: " if self.sheet["versions"] > 1 else ""
            k, u = writer.unlettered(self.sheet, v), writer.unmatched(self.sheet, v)
            out += (f"  ·  {ver}{k} graph answer{'s' * (k > 1)} not on the back" if k else "") + \
                   (f"  ·  {ver}{', '.join(f'#{n}' for n in u)} can be matched without solving" if u else "")
        return out

    def redraw_decoys(self):
        """:decoys: new decoys on a warm-up's back (the problems stay)."""
        if not sh.is_warmup(self.sheet):
            return self.say("E: decoys are for a warm-up (:form warmup)", True)
        n = sum(d for v in range(self.sheet["versions"]) for _, _, d in writer.back(self.sheet, v))
        if not n:
            return self.say("no decoys: no answer gives itself away" + self.graph_warning())
        self.change(lambda: self.sheet.__setitem__("decoy_seed", self.sheet.get("decoy_seed", 0) + 1))
        self.say(f"{n} decoy{'s' * (n > 1)} redrawn (:pre key shows them)" + self.graph_warning())

    def open_file(self, args):
        if not self.last_build:
            return self.say("E: nothing written yet (:w first)", True)
        what = "sheet"
        for a in args:
            if a in ("sheet", "slides"):
                what = a
            else:
                return self.say("usage: :open [sheet|slides]  (every version is in one file, each key after its sheet)", True)
        b = self.last_build
        suffix = {"sheet": "", "slides": "_slides"}[what]
        f = b["out"] / f"{self.s['name']}{suffix}.{'pdf' if b['compiled'] else 'typ'}"
        if self.open_path(f):
            self.say(f"opening {f.name}")

    def open_path(self, f):
        """Open f in the desktop's viewer; False (and an error shown) if that can't start."""
        try:
            subprocess.Popen(["xdg-open", str(f)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
            return True
        except OSError as e:
            self.say(f"E: {e}", True)
            return False

    def preview(self, args):
        """:pre [sheet|key|slides] [N]: compile the sheet as it stands (version N,
        else the one showing) to a temporary PDF and open it. Nothing is written
        to the out folder and the sheet isn't marked saved."""
        what, v = "sheet", self.version + 1
        for a in args:
            if a.isdigit():
                v = int(a)
            elif a in ("sheet", "key", "slides"):
                what = a
            else:
                return self.say("usage: :pre [sheet|key|slides] [version]", True)
        if not 1 <= v <= self.sheet["versions"]:
            return self.say(f"E: there are {self.sheet['versions']} versions", True)
        try:
            pdf = build.preview(self.sheet, v - 1, what, self.preview_dir)
        except (RuntimeError, OSError) as e:
            return self.say(f"E: {e}".splitlines()[0], True)
        self.preview_dir = pdf.parent           # the same file every time, so an open viewer reloads it
        if self.open_path(pdf):
            un, bad = self.statuses()
            self.say(f"preview: version {v} {('warm-up' if sh.is_warmup(self.sheet) else 'worksheet') if what == 'sheet' else what} (not saved)"
                     + (f"  ·  {bad} failing answer{'s' * (bad > 1)} (✗)" if bad else "")
                     + (f"  ·  {un} unchecked" if un else "") + self.graph_warning(), bool(bad))

    def present(self, args):
        """:present [N]: the board presenter for version N (else the one showing),
        the sheet as it stands: <name>.present.html in the out folder, opened
        in the browser. The sheet isn't marked saved."""
        v = self.version + 1
        for a in args:
            if not a.isdigit():
                return self.say("usage: :present [version]", True)
            v = int(a)
        if not 1 <= v <= self.sheet["versions"]:
            return self.say(f"E: there are {self.sheet['versions']} versions", True)
        if not self.total():
            return self.say("E: nothing to present: the sheet is empty", True)
        many = self.sheet["versions"] > 1 and v > 1
        f = Path(self.s["out"]).expanduser().resolve() / f"{self.s['name']}{f'_v{v}' * many}.present.html"
        try:
            f.parent.mkdir(parents=True, exist_ok=True)
            presenter.build(self.sheet, f, v - 1)
        except (RuntimeError, OSError) as e:
            return self.say(f"E: {e}".splitlines()[0], True)
        if self.open_path(f):
            self.say(f"presenting version {v}: {dir_label(f.parent)}/{f.name} (click a half: answer, then next)")

    def in_out(self, path):
        """A path as :e and :w FOLDER/NAME read it: relative to the out folder."""
        return Path(self.s["out"]).expanduser() / Path(path).expanduser()

    def load(self, path):
        """Open a .sheet.json (or convert an older practice .json) to edit,
        a relative path starting in the out folder."""
        p = self.in_out(path)
        try:
            sheet = legacy.read_sheet(p)
        except (OSError, ValueError, KeyError, TypeError, SystemExit) as e:
            return self.say(f"E: can't open {path}: {e}", True)
        name = re.sub(r"(\.sheet\.json|_v\d+\.json|\.json)$", "", p.name)
        out = dir_label(p.resolve().parent)
        sheet.setdefault("course", self.sheet.get("course"))
        def go():
            self.s.update(sheet=sheet, out=out, name=name)
        self.change(go)
        self.cur, self.version = SHEET, 0
        self.clamp()
        older = not str(p).endswith(".sheet.json")
        if not older:
            self.written = self.snapshot()
            self.rev += 1
        gone = self.missing()
        self.say(f'"{path}" opened: {self.total()} problems' +
                 (" (an older set, converted: :w saves it as a sheet)" if older else "") +
                 (f"  ·  not in the library: {', '.join(gone)} (marked !; :library or :rescan)" if gone else ""),
                 bool(gone))
