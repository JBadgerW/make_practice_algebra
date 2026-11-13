"""The banks pane: its rows, what each shows, and the changes made from it (counts, settings, the course)."""
import re
from sheets import draft
from sheets import sheet as sh, edit as E, banks, library
from .common import dir_label, SETTINGS

class Tree:
    def rows(self, everything=False):
        """The left pane's rows, as shown (or with every bank and type open).
        Built once for each library, course, and set of open rows; don't change the list."""
        lib = library.current()
        key = (lib, self.course, everything) + ((None, None) if everything else
                                                    (frozenset(self.open), frozenset(self.open_types)))
        if getattr(self, "_rows", (None,))[0] != key:
            self._rows = (key, self._build_rows(lib, everything))
        return self._rows[1]

    def _build_rows(self, lib, everything):
        out = [("course", None)]
        for name in [n for _, ns in lib.view(self.course, sequences=True) for n in ns]:
            if name in lib.sequences:
                out.append(("seq", name))
                if everything or name in self.open:
                    for st in lib.sequences[name].steps:
                        out.append(("step", (name, st["n"])))
                        if everything or (name, st["n"]) in self.open_types:
                            out += [("example", (name, st["n"], b, pid)) for b, pid in self.examples(st)]
                continue
            out.append(("bank", name))
            if everything or name in self.open:
                b, keep = banks.get(name), lib.types_in(name, self.course)
                for e in b.ENTRIES:
                    if e["type"] not in keep:
                        continue
                    out.append(("count", (name, e["key"])))
                    if b.FIXED and (everything or (name, e["key"]) in self.open_types):
                        out += [("problem", (name, p["id"])) for p in b.PROBLEMS if p["type"] == e["key"]]
        return out + [("set", k) for k in SETTINGS]

    def examples(self, st):
        """A step's pinned examples that the library has, as (bank, id)."""
        lib = library.current()
        return [] if st["missing"] else \
            [(b, pid) for b, pid in st["examples"] if lib.has(b) and pid in lib.get(b).PROBLEM]

    def step(self, key):
        """The step a ("step", (sequence, n)) row is."""
        return library.current().sequence(key[0]).steps[key[1] - 1]

    def act(self, row=None):
        """A row as the bank row it stands for: a sequence's step acts as its
        entry's row, a pinned example as its problem's, and a step that can't
        draw is ("missing", why)."""
        kind, key = self.rid(row)
        if kind == "step":
            st = self.step(key)
            return ("missing", f"step {st['n']}: {st['missing']}") if st["missing"] else ("count", (st["bank"], st["entry"]))
        if kind == "example":
            return "problem", key[2:]
        return kind, key

    def step_items(self, st):
        """Is a sheet item this step's: of its entry, or one of its pinned examples
        (found as where_problem finds a fixed problem)?"""
        if st["missing"]:
            return lambda it: False
        pinned = set()
        for b, pid in self.examples(st):
            x = banks.get(b)
            pinned.add((x.FAMILY, x.seen_key(x.problem(pid))))
        def mine(it):
            if (it["bank"], it["entry"]) == (st["bank"], st["entry"]):
                return True
            ib = banks.get(it["bank"])
            return not it["edited"] and (ib.FAMILY, ib.seen_key(it["problem"])) in pinned
        return mine

    def seq_items(self, name):
        """Is a sheet item one of this sequence's (see step_items)?"""
        steps = [self.step_items(st) for st in library.current().sequence(name).steps]
        return lambda it: any(f(it) for f in steps)

    def rid(self, row=None):
        """The id of a row (default: the cursor's); a row id passes through."""
        if isinstance(row, tuple):
            return row
        rows = self.rows()
        return rows[min(self.row if row is None else row, len(rows) - 1)]

    def value(self, row):
        """What a row shows (a count, a setting); row is an index or a row id."""
        rid = self.rid(row)
        return self.memo(("value", rid), lambda: self._value(rid))

    def _value(self, row):
        if self.rid(row)[0] == "step":
            return sum(map(self.step_items(self.step(self.rid(row)[1])), sh.items(self.sheet)))
        kind, key = self.act(row)
        if kind == "missing":
            return 0
        if kind == "seq":
            return sum(map(self.seq_items(key), sh.items(self.sheet)))
        if kind == "course":
            return self.course or "All banks"
        if kind == "bank":
            return sum(1 for it in sh.items(self.sheet) if it["bank"] == key)
        if kind == "count":
            return E.count(self.sheet, *key)
        if kind == "problem":
            return E.where_problem(self.sheet, *key) is not None
        return {"form": "warm-up" if sh.is_warmup(self.sheet) else "worksheet", "versions": self.sheet["versions"], "title": self.sheet["title"], "class": self.sheet["class_name"],
                "instructions": self.sheet["instructions"]}.get(key, self.s.get(key))

    def toggle_open(self, rid=None):
        """o: open or close the bank, or the fixed bank's type, under the cursor."""
        kind, key = rid or self.rid()
        if kind in ("bank", "seq"):
            self.open ^= {key}
        elif kind in ("step", "example"):
            st = self.step(key)
            if not self.examples(st):
                return self.say(f"step {st['n']} has no pinned examples: l draws one of {st['spec']}", True)
            self.open_types ^= {key[:2]}
            rid = ("step", key[:2])
        elif kind in ("count", "problem"):
            bank = key[0]
            b = banks.get(bank)
            if not b.FIXED:
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
        self.open = set() if close else set(banks.names()) | set(library.current().sequences)
        if close:
            self.open_types = set()
        rows = self.rows()
        parent = self.parent(here)
        self.row = rows.index(here) if here in rows else rows.index(parent) if parent in rows else 0

    def parent(self, rid):
        """The bank or sequence row a row belongs to (itself, for one), or None."""
        kind, key = rid
        if kind in ("bank", "seq"):
            return rid
        if kind in ("count", "problem"):
            return ("bank", key[0])
        if kind in ("step", "example"):
            return ("seq", key[0])
        return None

    # -- the types pane --------------------------------------------------
    def bump(self, n, row=None):
        kind, key = self.act(row)
        if kind == "missing":
            return self.say(key, True)
        if kind == "course":
            titles = [c["title"] for c in library.current().courses] + [None]
            self.set_course(titles[(titles.index(self.course) + n) % len(titles)])
        elif kind == "count":
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
            if n > 0:
                if self.change(lambda: E.add_from_bank(self.sheet, key, n, self.seeds())):
                    self.say(f"{n} from all of {banks.get(key).TITLE}")
            else:
                self.change(lambda: E.remove_last_from_bank(self.sheet, key, -n))
        elif kind == "seq":
            return self.say("o opens the sequence; l on a step adds a problem of it", True)
        elif key == "versions":
            self.set_versions(self.sheet["versions"] + n)
        elif key == "form":
            self.set_form(not sh.is_warmup(self.sheet))
        else:
            return self.say(f"{key} is text: press i to edit it", True)
        self.last_change = lambda: self.bump(n)

    # -- the library ------------------------------------------------------
    def set_course(self, title):
        """Show this course's banks (None, "" or "all": every bank). The class name
        follows while the sheet has no problems and the class is the default or
        the last course's title. Returns an error message, or None."""
        lib, title = library.current(), (title or "").strip()
        new = None
        if title.lower() not in ("", "all", "all banks"):
            c = lib.course(title)
            if not c:
                near = library.suggest(title, [x["title"] for x in lib.courses])
                return f"no course {title!r}" + (f" (did you mean {near}?)" if near else "") + "; :course all shows every bank"
            new = c["title"]
        old, here = self.course, self.rid()
        def go():
            self.sheet["course"] = new
            if new and not self.total() and self.sheet["class_name"] in (draft.DEFAULTS["class_name"], old):
                self.sheet["class_name"] = new
        self.change(go)
        try:
            library.save_config(course=new)         # a new sheet starts here next time
        except OSError:
            pass
        rows = self.rows()
        self.row = rows.index(here) if here in rows else min(self.row, len(rows) - 1)
        n = sum(len(ns) for _, ns in lib.view(new))
        self.say(f"{new or 'All banks'}: {n} bank{'s' * (n != 1)}" +
                 ("" if n or not new else " (tag a bank with this course, then :rescan)"))
        return None

    def rescan(self):
        """:rescan: read the library again (banks, courses, tags)."""
        lib = library.rescan()
        self.row = min(self.row, len(self.rows()) - 1)
        gone = self.missing()
        where = dir_label(lib.folder) + ("" if lib.folder.is_dir() else " (no such folder: built-in banks only)")
        msg = f"{where}: {lib.summary()}" + (f"  ·  missing: {', '.join(gone)}" if gone else "")
        if lib.warnings:
            msg += f"  ·  {lib.warnings[0]}" + (f" (+{len(lib.warnings) - 1} more: :warnings)" if len(lib.warnings) > 1 else "")
        self.say(msg, bool(lib.warnings or gone))

    def set_library(self, text):
        """:library DIR: use this library folder from now on."""
        if not text:
            return self.rescan()
        try:
            library.save_config(library=text)
        except OSError as e:
            return self.say(f"E: can't save the config: {e}", True)
        self.rescan()

    def set_form(self, warmup):
        """A warm-up or a worksheet; the versions stay."""
        self.change(lambda: self.sheet.__setitem__("form", "warmup" if warmup else "worksheet"))

    def set_versions(self, n):
        n = min(26, max(1, n))
        def go():
            self.sheet["versions"] = n
            sh.fill_versions(self.sheet)
        self.change(go)
        self.version = min(self.version, n - 1)

    def zero(self, row=None):
        kind, key = self.act(row)
        if kind == "missing":
            return self.say(key, True)
        if kind == "seq":
            mine = self.seq_items(key)
            def go():
                for sec in self.sheet["sections"]:
                    sec["items"] = [it for it in sec["items"] if not mine(it)]
                E.drop_empty_auto(self.sheet)
            self.change(go)
        elif kind == "count":
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
        kind, key = self.act(row)
        text = text.strip()
        if kind == "missing":
            return key
        if kind == "course":
            return self.set_course(text)
        if kind in ("seq", "problem"):
            return "type a count on a type's or a bank's row"
        if key == "form":
            f = text.lower().replace("-", "")
            if f not in ("warmup", "worksheet", "sheet"):
                return "form is worksheet or warmup"
            self.set_form(f == "warmup")
            self.last_change = lambda: self.set_value(text)
            return None
        if kind in ("count", "bank") or key == "versions":
            if not text.isdigit():
                return f"{'count' if kind in ('count', 'bank') else key} must be a whole number"
            n = int(text)
            if key == "versions":
                if not 1 <= n <= 26:
                    return "versions must be 1-26"
                self.set_versions(n)
            elif kind == "bank":
                self.change(lambda: E.set_bank_count(self.sheet, key, n, self.seeds()))
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
        kind, key = self.act()
        if kind == "missing":
            return self.say(key, True)
        if kind not in ("count", "problem", "bank"):
            return self.say("L adds the bank, type, or problem under the cursor where the sheet cursor is", True)
        def go():
            si, ii = self.cur
            if si < 0 and not self.sheet["sections"]:
                self.sheet["sections"].append(sh.new_section())
            si = max(si, 0)
            at = ii + 1 if ii >= 0 else None
            if kind == "problem":
                return E.add_problem(self.sheet, *key, si, at)
            if kind == "bank":
                return E.add_from_bank(self.sheet, key, n, self.seeds(), si, at)
            for k in range(n):
                E.add(self.sheet, si, *key, next(self.seeds()), None if at is None else at + k)
        if self.change(go):
            self.say(f"added to “{self.sheet['sections'][max(0, self.cur[0])]['title'] or 'untitled'}”")
        self.last_change = lambda: self.add_here(n)

    def reroll_entry(self):
        kind, key = self.act()
        if kind == "missing":
            return self.say(key, True)
        if kind not in ("count", "bank", "seq"):
            return
        mine = self.seq_items(key) if kind == "seq" else \
            (lambda it: it["bank"] == key) if kind == "bank" else (lambda it: (it["bank"], it["entry"]) == key)
        ps = [p for p in E.positions(self.sheet) if mine(self.sheet["sections"][p[0]]["items"][p[1]])]
        if self.change(lambda: E.reroll(self.sheet, ps, self.seeds())):
            self.say(f"{len(ps)} rerolled")
