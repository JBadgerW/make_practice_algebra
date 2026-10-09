"""The worksheet document: what gets saved, edited, and written.

    Sheet   dict(format, title, class_name, instructions, versions, command, sections)
    Section dict(title, instructions, items, auto) an empty title prints no header;
                                                   auto "bank:type" marks a type's own section
    Item    dict(bank, entry, seed, width, space, problem, alts, edited, status)

An item's problem is version 1. For a generated item (it has a seed and was
not edited by hand) alts holds versions 2, 3, ...: the same entry redrawn
from seeds derived from the item's own seed, so versions are parallel.
Edited items, and items with no seed (imported, or from a fixed bank),
print the same problem in every version.
"""
import json, random
from pathlib import Path
from . import banks

FORMAT = 1
WIDTHS = ("half", "full")

def new_sheet(title, class_name="Algebra 1", instructions="", versions=1):
    return dict(format=FORMAT, title=title, class_name=class_name, instructions=instructions,
                versions=versions, command=None, sections=[])

def new_section(title="", instructions="", auto=""):
    return dict(title=title, instructions=instructions, items=[], auto=auto)

def items(sheet):
    return [it for sec in sheet["sections"] for it in sec["items"]]

def _draw(bank, entry, seed, seen):
    random.seed(seed)                       # the numeric checks, so a seed always gives the same problem
    return banks.get(bank).generate(entry, random.Random(seed), seen.setdefault(bank, set()))

def new_item(bank, entry, seed, seen):
    """A freshly drawn item. seen: dict bank -> no-repeat set (see seen_of)."""
    e = banks.get(bank).ENTRY[entry]
    return dict(bank=bank, entry=entry, seed=seed, width=e["width"], space=e["space"],
                problem=_draw(bank, entry, seed, seen), alts=[], edited=False, status="checked")

def seen_of(sheet):
    """dict bank -> the no-repeat keys of every problem on the sheet, plus each bank's exclusions."""
    seen = {}
    for it in items(sheet):
        b = banks.get(it["bank"])
        s = seen.setdefault(it["bank"], set(b.initial_seen()))
        s.update(b.seen_key(p) for p in [it["problem"], *it["alts"]])
    return seen

def fill_versions(sheet, seen=None):
    """Give every generated item exactly versions - 1 alternates (drawing any missing ones)."""
    seen = seen_of(sheet) if seen is None else seen
    n = sheet["versions"] - 1
    for it in items(sheet):
        if it["edited"]:
            it["alts"] = []
        del it["alts"][n:]
    for v in range(2, n + 2):                # version-major, so the draw order never depends on n
        for it in items(sheet):
            if it["seed"] is not None and not it["edited"] and len(it["alts"]) < v - 1:
                try:
                    alt = _draw(it["bank"], it["entry"], f"{it['seed']}:v{v}", seen)
                except RuntimeError:            # nothing new left (a small pool): repeat version 1
                    alt = it["problem"]
                it["alts"].append(alt)
    return sheet

def problem(item, v=0):
    """The item's problem in version v (0-based)."""
    return item["alts"][v - 1] if 0 < v <= len(item["alts"]) else item["problem"]

def rows(section_items):
    """Lay items out in rows: two consecutive half-width items share a row,
    a full-width item gets its own, and a half item left over sits alone."""
    out, half = [], None
    for it in section_items:
        if it["width"] == "full":
            if half:
                out.append([half])
                half = None
            out.append([it])
        elif half:
            out.append([half, it])
            half = None
        else:
            half = it
    if half:
        out.append([half])
    return out

def save(sheet, path):
    Path(path).write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")

def load(path):
    """Read a .sheet.json; raises ValueError if it isn't one."""
    d = json.loads(Path(path).read_text())
    if not isinstance(d, dict) or d.get("format") != FORMAT or "sections" not in d:
        raise ValueError(f"{path} is not a sheet file")
    return d
