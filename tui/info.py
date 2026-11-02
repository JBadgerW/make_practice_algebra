"""The info box (I): what the cursor is on, each line with the keys that change it."""
import os
from sheets import ROOT, sheet as sh, edit as E, banks, library, writer
from .common import dir_label, prose, tags_text

class Info:
    def info(self):
        """What I's box shows for the cursor: (title, [(label, value, keys)], footer)."""
        if self.focus != "preview":
            return self.info_row()
        si, ii = self.cur
        if self.anchor is not None:
            ps = self.selection()
            return (f"{len(ps)} selected", self.info_items([self.item(q) for q in ps]),
                    "b scope · W + - width, space · r reroll · Esc")
        if si < 0:
            sheet = self.sheet
            rows = [("Title", sheet["title"], ":title"), ("Class", sheet["class_name"], ":class"),
                    ("Form", "warm-up" if sh.is_warmup(sheet) else "worksheet", ":form"),
                    *([("Decoys", str(sum(d for _, _, d in writer.back(sheet))), ":decoys")]
                      if sh.is_warmup(sheet) else []),
                    ("Versions", str(sheet["versions"]), ":versions"),
                    ("Sections", str(len(sheet["sections"])), "")]
            return "The sheet", rows + self.info_items(sh.items(sheet)), "b scope · W + - · R reroll all · Esc"
        if ii < 0:
            sec = self.sheet["sections"][si]
            bk, _, typ = sec.get("auto", "").partition(":")
            kind = ("a section you made (or :group, :mix)" if not bk else
                    f"the bank's own: l on {banks.get(bk).TITLE} adds here" if typ == "*" else
                    f"its type's own: l on {banks.get(bk).heading(typ)} adds here")
            rows = [("Title", sec["title"] or "(none: no header prints)", "cS"),
                    ("Instr.", sec["instructions"] or "(none)", "cI"), ("Kind", kind, "")]
            return (f"Section {si + 1}", rows + self.info_items(sec["items"]),
                    "b scope · W + - · R reroll · gs shuffle · Esc")
        return f"Problem {E.positions(self.sheet).index(self.cur) + 1}", self.info_item(self.item()), \
            "r reroll · i edit · A answer · Esc"

    def info_item(self, it):
        b, p = banks.get(it["bank"]), sh.problem(it, self.version)
        e = b.ENTRY.get(it["entry"])
        src = p.get("source", "")
        what = "written problems" if getattr(b, "FIXED", False) else "draws new problems"
        rows = [("Bank", b.TITLE, ""),
                ("", f"{it['bank']}, {what}" + (f"; the bank's #{src.split('#')[1]}" if "#" in src else "")
                 + (" (missing from the library: :rescan once it's back)" if getattr(b, "MISSING", False) else ""), "")]
        if e:
            rows.append(("Type", f"{banks.label(b, it['entry'])}  {e['title']}"
                         + (" (real formulas)" if e.get("kind") == "formulas" else ""), ""))
        if sh.from_bank(it):
            keep = sh.bank_types(it["bank"], self.sheet.get("course"))
            left = E.unused(self.sheet, it["bank"], keep)
            how = "from the whole bank, any type" + ("" if left is None else f": {left} unused left")
        else:
            left = E.unused(self.sheet, it["bank"], [b.type_of(it["entry"])]) if e else None
            how = "from its type only" + ("" if left is None else f": {left} unused left")
        if it["edited"]:
            how += "; edited by hand, so r draws a fresh one"
        rows.append(("Rerolls", how, "b"))
        for k, keys in (("width", "W"), ("space", "+ -")):
            dflt = e and e[k]
            note = "" if not e else " (the type's)" if it[k] == dflt else f" (by hand; the type's is {dflt})"
            rows.append((k.title(), it[k] + note, keys))
        status = {"checked": "checked", "unchecked": "can't be checked by machine",
                  "failed": "FAILS its check"}.get(it["status"], it["status"])
        rows.append(("Answer", f"{b.answer_text(p)}  ({status})", "A"))
        fixed = getattr(b, "FIXED", False) or it["edited"] or it["seed"] is None
        n = self.sheet["versions"]
        rows.append(("Versions", "one" if n == 1 else
                     f"the same in all {n} ({'edited' if it['edited'] else 'written'})" if fixed else
                     f"redrawn in each of {n}, same type; showing {self.version + 1} (gt gT)", ""))
        return rows

    def info_row(self):
        """The box for the banks pane's row: a bank, a type (or a step, which acts as
        its type), or a fixed bank's problem; for anything else, how to get one."""
        kind, key = self.act()
        its = sh.items(self.sheet)
        if kind == "bank":
            return self.info_bank(key, its)
        if kind == "seq":
            return self.info_seq(key, its)
        if kind == "count":
            title, rows, foot = self.info_type(*key, its)
            if self.rid()[0] == "step":
                st = self.step(self.rid()[1])
                rows.insert(0, ("Step", f"{st['n']} of {self.rid()[1][0]}: {st['title']}"
                                + (f". What changes: {st['note']}" if st["note"] else ""), ""))
            return title, rows, foot
        if kind == "problem":
            return self.info_problem(*key)
        return "Banks", [("", "I shows a bank, a sequence, a type, or a problem: move to one", "")], "Esc"

    def info_bank(self, name, its):
        b, lib = banks.get(name), library.current()
        fixed = getattr(b, "FIXED", False)
        shown = sh.bank_types(name, self.course)              # what l here draws from
        every = library.types(b)
        mine = [it for it in its if it["bank"] == name]
        whole = sum(map(sh.from_bank, mine))
        rows = [("Title", b.TITLE, ""),
                ("Id", name + "  (permanent: sheets and sequences use it)"
                 + (f"; formerly {', '.join(b.FORMERLY)}" if getattr(b, "FORMERLY", None) else ""), ""),
                ("Kind", (f"{len(b.PROBLEMS)} written problem{'s' * (len(b.PROBLEMS) != 1)}"
                          + (f", checked as {b.fam.TITLE}" if b.fam else "; their answers can't be checked by machine (?)"))
                 if fixed else "draws new problems, each checked", ""),
                ("File", self.bank_file(b), ""),
                ("Courses", tags_text(library.bank_tags(b)), ""),
                ("Types", f"{len(every)}" + (f", {len(shown)} of them in {self.course}" if self.course and
                                             len(shown) != len(every) else ""), "o")]
        if fixed:
            rows.append(("Unused", f"{E.unused(self.sheet, name, shown)} of the "
                         f"{sum(p['type'] in shown for p in b.PROBLEMS)} that l here can draw", ""))
        rows += [("On sheet", f"{len(mine)}" + ("" if not whole else ", all from the whole bank" if whole == len(mine)
                                                else f", {whole} from the whole bank"), "l h x"),
                 ("Instr.", b.INSTRUCTIONS or "(none)", "")]
        return (f"Bank: {b.TITLE}", rows,
                "l 20l any type · h remove · i count · r reroll · x remove all · Esc")

    def info_seq(self, name, its):
        q = library.current().sequence(name)
        usable, pinned = q.usable(), sum(len(self.examples(st)) for st in q.steps)
        rows = [("Title", q.TITLE, ""),
                ("Id", f"{name}  (:draft {name} … uses it)", ""),
                ("File", q.SOURCE if q.SOURCE.startswith("library/") else
                 f"{q.SOURCE} in your library ({dir_label(library.current().folder)})", ""),
                ("Courses", tags_text(library.bank_tags(q)), ""),
                ("Steps", f"{len(q.steps)}" + (f", {len(q.steps) - len(usable)} of them can't draw (shown in red)"
                                               if len(usable) < len(q.steps) else "")
                 + (f"; {pinned} pinned examples" if pinned else ""), "o"),
                ("On sheet", str(sum(map(self.seq_items(name), its))), "x"),
                ("Draft", f":draft {name} STEPS [xN] [review STEPS|none] [pinned]", "")]
        for st in q.steps:
            n = sum(map(self.step_items(st), its))
            k = len(self.examples(st))
            rows.append((f"  {st['n']}", st["title"] + (f"  ({st['spec']})" if st["title"] != st["spec"] else "")
                         + (f"  MISSING: {st['missing']}" if st["missing"] else "")
                         + "".join(f" · {x}" for x in (f"{k} pinned" if k else "", f"{n} on sheet" if n else "") if x), ""))
        return f"Sequence: {q.TITLE}", rows, "o steps · r reroll · x remove all · Esc"

    def info_type(self, name, entry, its):
        b = banks.get(name)
        e, typ = b.ENTRY[entry], b.type_of(entry)
        fixed = getattr(b, "FIXED", False)
        rows = [("Bank", f"{b.TITLE}  ({name})", ""),
                ("Type", f"{banks.label(b, entry)}  {e['title']}"
                 + (" (real formulas)" if e.get("kind") == "formulas" else ""), ""),
                ("Id", entry + ("  (shown as " + banks.label(b, entry) + ")" if banks.label(b, entry) != entry else "")
                 + "  (permanent: sheets store it)", "")]
        t = library.type_table(b).get(typ)
        own = isinstance(t, dict) and t.get("courses") is not None
        rows.append(("Courses", tags_text(library.bank_tags(b, typ)) + ("  (its own)" if own else ""), ""))
        rows.append(("Layout", f"{e['width']} width, {e['space']} work space", ""))
        h = b.hint(typ)
        if h:
            rows += [("Look for", prose(h[2]), ""), ("The move", prose(h[3]), "")]
        if fixed:
            rows.append(("Problems", f"{e['count']} written, {E.unused(self.sheet, name, [typ])} unused", "o"))
        else:
            rows.append(("Problems", "drawn new each time", ""))
        n, whole = E.count(self.sheet, name, entry), sum(1 for it in its if it["bank"] == name
                                                          and it["entry"] == entry and sh.from_bank(it))
        rows.append(("On sheet", f"{n}" + (f", {whole} of them from the whole bank" if whole else ""), "l h x"))
        rows.append(("Instr.", banks.instructions(b, typ) or "(none)", ""))
        return (f"Type {banks.label(b, entry)}: {e['title']}", rows,
                "l add · h remove · i count · L at cursor · r reroll · Esc")

    def info_problem(self, name, pid):
        b = banks.get(name)
        p = b.problem(pid)
        rows = [("Bank", f"{b.TITLE}  ({name})", ""),
                ("Problem", f"#{pid}  ({name}#{pid}, as sequences pin it)", ""),
                ("Type", f"{banks.label(b, p['type'])}  {b.ENTRY[p['type']]['title']}", ""),
                ("Prompt", b.text(p), ""),
                ("Answer", f"{b.answer_text(p)}  ({b.check(p)})", ""),
                ("On sheet", "yes" if E.where_problem(self.sheet, name, pid) else "no", "l h")]
        return f"Problem {name}#{pid}", rows, "l add · h remove · L at cursor · Esc"

    def bank_file(self, b):
        if getattr(b, "MISSING", False):
            return "none: it's missing from the library"
        src = getattr(b, "SOURCE", None)
        if src:
            return src if src.startswith("library/") else f"{src} in your library ({dir_label(library.current().folder)})"
        return os.path.relpath(b.__file__, ROOT) + " (a generator)"

    def info_items(self, its):
        """Rows summing up several problems."""
        if not its:
            return [("Problems", "none", "")]
        by = {}                                         # bank -> entry -> how many, in the bank's order
        for it in its:
            by.setdefault(it["bank"], {}).setdefault(it["entry"], 0)
            by[it["bank"]][it["entry"]] += 1
        def kinds(bank, es):
            b = banks.get(bank)
            order = [e["key"] for e in b.ENTRIES]
            return ", ".join((banks.label(b, e) if e in b.ENTRY else e) + (f" ×{es[e]}" if es[e] > 1 else "")
                             for e in sorted(es, key=lambda e: order.index(e) if e in order else len(order)))
        mix = "; ".join(f"{banks.get(bk).TITLE}: {kinds(bk, es)}" for bk, es in by.items())
        nb = sum(map(sh.from_bank, its))
        scope = ("all from their whole bank" if nb == len(its) else "all from their own type" if not nb else
                 f"{nb} from their whole bank, {len(its) - nb} from their type")
        widths = [it["width"] for it in its]
        spaces = sorted({it["space"] for it in its}, key=E.inches)
        un = sum(it["status"] == "unchecked" for it in its)
        bad = sum(it["status"] == "failed" for it in its)
        checks = ", ".join(x for x in (f"{bad} FAIL" if bad else "", f"{un} can't be checked" if un else "") if x)
        return [("Problems", f"{len(its)}  ({mix})", ""),
                ("Rerolls", scope, "b"),
                ("Width", ", ".join(f"{widths.count(w)} {w}" for w in sh.WIDTHS if w in widths), "W"),
                ("Space", spaces[0] if len(spaces) == 1 else f"{spaces[0]} to {spaces[-1]}", "+ -"),
                ("Answers", checks or "all checked", "")]
