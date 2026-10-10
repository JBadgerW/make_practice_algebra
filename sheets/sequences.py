"""Sequences: an ordered path through banks' entries, for teaching a skill one
step at a time, each step changing a single element.

    {
     "format": 1,
     "kind": "sequence",
     "name": "literal_by_move",                    (default: the file name)
     "title": "Literal Equations by First Move",
     "courses": {"Algebra 1": "Equations"},        (as for a bank; see library.py)
     "steps": [
      {"entry": "literal/1", "note": "one operation to undo"},
      {"entry": "literal/3", "title": "A Fraction Bar",
       "note": "a fraction bar appears",
       "examples": ["lesson_1-4#13", "lesson_1-4#14"]},
      ...]
    }

A step is a bank's entry, spelled BANK/ENTRY as in --mix. Its title is the
entry's unless it gives its own; its note says what changes at this step.
Its examples (optional) are problems of a fixed bank, BANK#ID, pinned in
this order: a teaching sequence needs those exact problems, while practice
draws fresh ones of the entry. A step finer than a bank's types is a new
entry in the bank, never something reached for inside a template.

A sequence only points at banks: a problem added from one of its steps is
the bank's own, so a sheet never depends on a sequence. A step whose bank,
entry, or examples the library lacks is reported and kept, marked, so step
numbers never shift.
"""
from pathlib import Path

FORMAT = 1

class Sequence:
    SEQUENCE = True

    def __init__(self, d, path):
        """d: the file's JSON. Raises ValueError if it isn't a sequence file."""
        if not isinstance(d, dict) or d.get("format") != FORMAT or d.get("kind") != "sequence":
            raise ValueError(f'not a sequence file (it needs "format": {FORMAT} and "kind": "sequence")')
        self.path = Path(path)
        self.NAME = d.get("name") or self.path.stem
        self.TITLE = d.get("title") or self.NAME
        self.COURSES = d.get("courses")
        steps = d.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ValueError('"steps" must be a list of steps')
        self.steps = []
        for n, s in enumerate(steps, 1):
            spec = s.get("entry") if isinstance(s, dict) else None
            if not isinstance(spec, str) or "/" not in spec:
                raise ValueError(f'step {n} needs an "entry" like "literal/3"')
            examples = s.get("examples", [])
            if not isinstance(examples, list) or not all(isinstance(x, str) and "#" in x for x in examples):
                raise ValueError(f'step {n}: "examples" must be a list like ["lesson_1-4#13"]')
            for k in ("title", "note"):
                if not isinstance(s.get(k, ""), str):
                    raise ValueError(f'step {n}: "{k}" must be text')
            bank, _, entry = spec.partition("/")
            self.steps.append(dict(n=n, spec=spec, bank=bank.strip(), entry=entry.strip(), type=None,
                                   title=s.get("title") or spec, own_title=bool(s.get("title")),
                                   note=s.get("note", ""), examples=[tuple(x.split("#", 1)) for x in examples],
                                   missing=None))

    def resolve(self, lib):
        """Check every step against the library's banks: spell its entry as the
        bank does, take its title and type, and check its examples. Returns
        warnings; a step that can't be used keeps a "missing" message."""
        from .library import suggest
        out = []
        for st in self.steps:
            where = f"{self.SOURCE}, step {st['n']} ({st['spec']})"
            if not lib.has(st["bank"]):
                near = suggest(st["bank"], lib.names())
                st["missing"] = f"no bank {st['bank']!r}" + (f" (did you mean {near!r}?)" if near else "")
            else:
                b = lib.get(st["bank"])
                key = b.entry_key(st["entry"])
                if key is None:
                    st["missing"] = f"{st['bank']} has no entry {st['entry']!r}"
                else:
                    st["entry"], st["type"] = key, b.type_of(key)
                    if not st["own_title"]:
                        st["title"] = b.ENTRY[key]["title"]
            if st["missing"]:
                out.append(f"{where}: {st['missing']}")
                continue
            for eb, pid in st["examples"]:
                x = lib.get(eb) if lib.has(eb) else None
                if x is None or pid not in getattr(x, "PROBLEM", {}):
                    out.append(f"{where}: no problem {eb}#{pid} (examples come from a fixed bank)")
                elif x.FAMILY != b.FAMILY or x.PROBLEM[pid]["type"] != st["type"]:
                    out.append(f"{where}: example {eb}#{pid} is {x.heading(x.PROBLEM[pid]['type'])}, "
                               f"not {b.heading(st['type'])}")
        return out

    def usable(self):
        """The steps that can draw problems."""
        return [st for st in self.steps if not st["missing"]]
