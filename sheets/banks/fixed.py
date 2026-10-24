"""Fixed banks: written problems, read from a JSON file in banks/.

    {
     "format": 1,
     "name": "lesson_1-4",                        (default: the file name)
     "title": "Lesson 1-4",
     "family": "literal",                         (optional; see below)
     "courses": {"Algebra 1": "Equations"},        (optional; see sheets/library.py)
     "instructions": "Solve each equation for the indicated variable.",
     "formerly": ["lesson_4"],                    (optional: names it used to have)
     "types": [{"key": "3", "title": "Clear One Denominator",
                "id": "3",                         (optional, default the key; see below)
                "width": "half", "space": "1in",   (defaults: half, 1in)
                "look": "...", "move": "...", "special": false,
                "courses": [...]}, ...],          (optional: replaces the bank's for this type)
     "problems": [{"id": "13", "type": "3", ...the family's fields...}, ...]
    }

With a family (a generator bank such as literal), problems carry that
family's fields (literal: prompt, target, answer). The family checks them,
solves them again when they are edited, and shows them; its own problems and
these never repeat each other on a sheet, and a type of both shares one
section. Without a family, a problem is Typst markup: prompt, answer, and
optionally text and answer_text for the terminal. Those answers can't be
checked by machine.

The name is the bank's permanent id: sheets and sequences refer to the bank
by it, so change the title freely but never the name (if you must, list the
old one under "formerly"). Likewise a type's id is what sheets store, and its
key is only the label shown, so a type can be renumbered by changing its key
once it has an id. Problems name their type by id. With a family, a type
whose id is one of the family's types is that type.

Adding a type draws an unused problem of it at random; a reroll swaps in
another. Fixed problems are the same in every version.
"""
import json, re
from pathlib import Path

FORMAT = 1

class FixedBank:
    FIXED = True

    def __init__(self, path, families):
        """families: the generator banks by name, for "family"."""
        d = json.loads(Path(path).read_text())
        if not isinstance(d, dict) or d.get("format") != FORMAT:
            raise ValueError(f"not a bank file (it needs \"format\": {FORMAT})")
        self.path = Path(path)
        self.NAME = d.get("name") or self.path.stem
        self.TITLE = d.get("title") or self.NAME
        if d.get("family") and d["family"] not in families:
            raise ValueError(f'no generator bank {d["family"]!r} for "family"')
        self.fam = families[d["family"]] if d.get("family") else None
        self.COURSES = d.get("courses")
        self.FAMILY = self.fam.NAME if self.fam else self.NAME
        self.INSTRUCTIONS = d.get("instructions") or (self.fam.INSTRUCTIONS if self.fam else "")
        self.FORMERLY = d.get("formerly", [])
        if not isinstance(self.FORMERLY, list) or not all(isinstance(x, str) for x in self.FORMERLY):
            raise ValueError('"formerly" must be a list of the names the bank used to have')
        self.WARNINGS = [] if d.get("name") else \
            [f'no "name": its id is the file name, so renaming the file breaks sheets that use it '
             f'(add "name": "{self.NAME}")']
        self.types = {}
        for i, t in enumerate(d.get("types", []), 1):
            if "key" not in t or "title" not in t:
                raise ValueError(f'type {i} needs a "key" and a "title"')
            tid = str(t.get("id", t["key"]))
            if tid in self.types:
                raise ValueError(f'two types have the id {tid!r}')
            if any(x["key"] == str(t["key"]) for x in self.types.values()):
                self.WARNINGS.append(f'two types are labeled {str(t["key"])!r}')
            self.types[tid] = dict(t, id=tid, key=str(t["key"]))
        self.PROBLEMS = []
        need = ("prompt", "target", "answer") if self.fam else ("prompt", "answer")
        for i, p in enumerate(d.get("problems", []), 1):
            missing = [k for k in ("type", *need) if k not in p]
            if missing:
                raise ValueError(f"problem {p.get('id', i)} needs " + ", ".join(f'"{k}"' for k in missing))
            p = dict(p, id=str(p.get("id", i)), type=str(p["type"]))
            if p["type"] not in self.types:
                self.types[p["type"]] = dict(id=p["type"], key=p["type"], title=f"Type {p['type']}")
            self.PROBLEMS.append(p)
        self.PROBLEM = {p["id"]: p for p in self.PROBLEMS}
        self.ENTRIES = [dict(key=k, type=k, label=t["key"], kind="fixed", title=t["title"], width=t.get("width", "half"),
                             space=t.get("space", "1in"),
                             count=sum(p["type"] == k for p in self.PROBLEMS)) for k, t in self.types.items()]
        self.ENTRY = {e["key"]: e for e in self.ENTRIES}

    # -- types ---------------------------------------------------------
    def entry_key(self, text):
        """A type's id, from its id or its label (either in any case)."""
        t = text.strip()
        for same in (lambda a, b: a == b, lambda a, b: a.lower() == b.lower()):
            for k, ty in self.types.items():
                if same(k, t) or same(ty["key"], t):
                    return k
        return None

    def type_of(self, entry):
        return entry

    def _family_type(self, typ):
        """Is typ one of the family's own types (so the family's names and hints apply)?"""
        return self.fam is not None and typ in getattr(self.fam, "TYPE", {})

    def hint(self, typ):
        """(label, title, look, move), or None when the type has no hints."""
        if self._family_type(typ):
            return self.fam.hint(typ)
        t = self.types[typ]
        if t.get("look") or t.get("move"):
            return (("Special Case " if t.get("special") else "Type ") + t["key"],
                    t["title"], t.get("look", ""), t.get("move", ""))
        return None

    def heading(self, typ):
        return self.fam.heading(typ) if self._family_type(typ) else self.types[typ]["title"]

    def special(self, typ):
        return self.fam.special(typ) if self._family_type(typ) else bool(self.types[typ].get("special"))

    def fam_of(self, p):
        """The family that checks and shows problem p."""
        return self.fam

    # -- drawing -------------------------------------------------------
    def initial_seen(self):
        return set()

    def seen_key(self, p):
        f = self.fam_of(p)
        return f.seen_key(p) if f else ("fixed", p.get("id"), p.get("prompt"))

    def problem(self, pid):
        """A copy of one problem, as an item stores it."""
        p = dict(self.PROBLEM[pid])
        p["source"] = f"{self.NAME}#{pid}"
        if self.fam:
            p["family"] = self.fam.NAME            # so it still shows if this bank goes missing
        return p

    def generate(self, entry, rng, seen):
        pool = [p for p in self.PROBLEMS if p["type"] == entry and self.seen_key(p) not in seen]
        if not pool:
            raise RuntimeError(f"no unused problems of {self.heading(entry)} left in {self.TITLE}")
        p = self.problem(rng.choice(pool)["id"])
        seen.add(self.seen_key(p))
        return p

    # -- checking, showing, editing -------------------------------------
    def check(self, p):
        f = self.fam_of(p)
        return f.check(p) if f else "unchecked"

    def typst(self, p, gap="0.3em"):
        f = self.fam_of(p)
        return f.typst(p, gap) if f else p["prompt"]

    def answer_typst(self, p):
        f = self.fam_of(p)
        return f.answer_typst(p) if f else p["answer"]

    def text(self, p):
        f = self.fam_of(p)
        return f.text(p) if f else p.get("text") or plain(p["prompt"])

    def answer_text(self, p):
        f = self.fam_of(p)
        return f.answer_text(p) if f else p.get("answer_text") or plain(p["answer"])

    def edit_text(self, p):
        f = self.fam_of(p)
        return f.edit_text(p) if f else p["prompt"]

    def from_edit(self, text, old):
        f = self.fam_of(old)
        if f:
            return f.from_edit(text, old)
        if not text.strip():
            raise ValueError("the problem can't be empty")
        new = dict(old, prompt=text.strip(), source="edited")
        new.pop("text", None)
        return new, "unchecked"

    def answer_edit_text(self, p):
        f = self.fam_of(p)
        return f.answer_edit_text(p) if f else p["answer"]

    def with_answer(self, p, text):
        f = self.fam_of(p)
        if f:
            return f.with_answer(p, text)
        if not text.strip():
            raise ValueError("the answer can't be empty")
        new = dict(p, answer=text.strip())
        new.pop("answer_text", None)
        return new, "unchecked"

def plain(typst):
    """Typst markup -> rough terminal text."""
    s = re.sub(r"#\w+(\([^)]*\))?", "", typst)
    return " ".join(s.replace("$", "").replace("[", "").replace("]", "").split())
