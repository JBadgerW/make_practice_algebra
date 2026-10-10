"""Changes to a sheet, with no user interface: the terminal app and tests call these.

Positions are (section index, item index). Every function changes the sheet
in place; those that can fail raise ValueError or RuntimeError with a message
for the teacher, and leave the sheet as it was.
"""
import copy, re
from . import banks
from .sheet import new_item, fixed_item, new_section, items, seen_of, fill_versions, drawn_status, _draw

SPACE_STEP = 0.25                       # inches, for + and -
UNITS = {"in": 1.0, "cm": 1 / 2.54, "mm": 1 / 25.4, "pt": 1 / 72}

def inches(space):
    """'1.25in' / '3cm' / '1.5' -> inches as a float; raises ValueError."""
    m = re.fullmatch(r"\s*(\d*\.?\d+)\s*(in|cm|mm|pt)?\s*", str(space))
    if not m:
        raise ValueError(f"{space!r} isn't a length: use inches like 1.5in (or cm, mm, pt)")
    return float(m.group(1)) * UNITS[m.group(2) or "in"]

def length(x):
    """inches -> '1.25in'."""
    return f"{round(x, 3):g}in"

# ------------------------------------------------------------------
# Adding and removing by entry (the types pane)
# ------------------------------------------------------------------
def auto_tag(bank, entry):
    b = banks.get(bank)
    return f"{b.FAMILY}:{b.type_of(entry)}"

def type_order(bank):
    """The family's types in order, then any of the bank's own."""
    b = banks.get(bank)
    fam = banks.get(b.FAMILY)
    return list(dict.fromkeys([fam.type_of(e["key"]) for e in fam.ENTRIES] + [b.type_of(e["key"]) for e in b.ENTRIES]))

def type_section(sheet, bank, entry):
    """The index of the entry's type section (shared by its family), made in type order if needed."""
    tag = auto_tag(bank, entry)
    for i, sec in enumerate(sheet["sections"]):
        if sec.get("auto") == tag:
            return i
    b = banks.get(bank)
    typ = b.type_of(entry)
    order = type_order(bank)
    at = len(sheet["sections"])
    for i, sec in enumerate(sheet["sections"]):
        fam, _, t = sec.get("auto", "").partition(":")
        if fam == b.FAMILY and t in order and order.index(t) > order.index(typ):
            at = i
            break
    ins = b.INSTRUCTIONS if b.INSTRUCTIONS != sheet["instructions"] else ""
    sheet["sections"].insert(at, new_section(b.heading(typ), ins, auto=tag))
    return at

def add(sheet, si, bank, entry, seed, at=None):
    """Draw a new item into section si (at index at, default the end). Returns it."""
    b = banks.get(bank)
    if not items(sheet) and sheet["instructions"] in [banks.get(n).INSTRUCTIONS for n in banks.names()]:
        sheet["instructions"] = b.INSTRUCTIONS            # an empty sheet takes its first bank's instructions
        for sec in sheet["sections"]:
            if sec.get("auto") and sec["instructions"] == b.INSTRUCTIONS:
                sec["instructions"] = ""
    seen = seen_of(sheet)
    it = new_item(bank, entry, seed, seen)
    its = sheet["sections"][si]["items"]
    its.insert(len(its) if at is None else at, it)
    fill_versions(sheet, seen)
    return it

def count(sheet, bank, entry):
    return sum(1 for it in items(sheet) if it["bank"] == bank and it["entry"] == entry)

def where_problem(sheet, bank, pid):
    """The position of a fixed bank's problem on the sheet, or None."""
    b = banks.get(bank)
    key = b.seen_key(b.problem(pid))
    for si, sec in enumerate(sheet["sections"]):
        for ii, it in enumerate(sec["items"]):
            ib = banks.get(it["bank"])
            if ib.FAMILY == b.FAMILY and not it["edited"] and ib.seen_key(it["problem"]) == key:
                return si, ii
    return None

def add_problem(sheet, bank, pid, si=None, at=None):
    """Add one particular problem of a fixed bank (to its type's section unless si
    is given). Raises ValueError if it's already on the sheet."""
    if where_problem(sheet, bank, pid):
        raise ValueError(f"problem {pid} is already on the sheet")
    it = fixed_item(bank, pid)
    si = type_section(sheet, bank, it["entry"]) if si is None else si
    its = sheet["sections"][si]["items"]
    its.insert(len(its) if at is None else at, it)
    return it

def remove_problem(sheet, bank, pid):
    pos = where_problem(sheet, bank, pid)
    if pos:
        del sheet["sections"][pos[0]]["items"][pos[1]]
        drop_empty_auto(sheet)

def drop_empty_auto(sheet):
    """Type sections that lost their last problem go; sections the teacher made stay."""
    sheet["sections"] = [sec for sec in sheet["sections"] if sec["items"] or not sec.get("auto")]

def remove_last(sheet, bank, entry, n=1):
    """Remove the last n items of an entry (last in print order)."""
    for _ in range(n):
        spots = [(si, ii) for si, sec in enumerate(sheet["sections"]) for ii, it in enumerate(sec["items"])
                 if it["bank"] == bank and it["entry"] == entry]
        if not spots:
            break
        si, ii = spots[-1]
        del sheet["sections"][si]["items"][ii]
    drop_empty_auto(sheet)

def set_count(sheet, bank, entry, n, seeds):
    """Add (to the type's section) or remove items until the entry has n. seeds: an iterator of seeds."""
    have = count(sheet, bank, entry)
    if n < have:
        remove_last(sheet, bank, entry, have - n)
    for _ in range(n - have):
        add(sheet, type_section(sheet, bank, entry), bank, entry, next(seeds))

# ------------------------------------------------------------------
# Rerolling
# ------------------------------------------------------------------
def reroll(sheet, positions, seeds):
    """Redraw the items at these positions, each from a new seed. Edited items
    become drawn ones again. Raises RuntimeError (changing nothing) if any can't."""
    before = copy.deepcopy(sheet["sections"])
    seen = seen_of(sheet)                  # includes the old problems, so none comes back
    try:
        for si, ii in positions:
            it = sheet["sections"][si]["items"][ii]
            seed = next(seeds)
            p = _draw(it["bank"], it["entry"], seed, seen)
            it.update(seed=seed, problem=p, alts=[], edited=False, status=drawn_status(it["bank"], p))
        fill_versions(sheet, seen)
    except RuntimeError:
        sheet["sections"] = before
        raise

def positions(sheet, si=None):
    """Every item position, or those of section si."""
    return [(i, j) for i, sec in enumerate(sheet["sections"]) if si is None or i == si
            for j in range(len(sec["items"]))]

# ------------------------------------------------------------------
# Hand edits
# ------------------------------------------------------------------
def edit_problem(sheet, pos, text):
    """Replace an item's problem from edited text; returns its status. Raises ValueError."""
    it = sheet["sections"][pos[0]]["items"][pos[1]]
    p, status = banks.get(it["bank"]).from_edit(text, it["problem"])
    it.update(problem=p, alts=[], edited=True, status=status)
    return status

def edit_answer(sheet, pos, text):
    it = sheet["sections"][pos[0]]["items"][pos[1]]
    p, status = banks.get(it["bank"]).with_answer(it["problem"], text)
    it.update(problem=p, alts=[], edited=True, status=status)
    return status

def set_width(it, width=None):
    it["width"] = width or ("full" if it["width"] == "half" else "half")

def bump_space(it, steps):
    it["space"] = length(max(0.0, inches(it["space"]) + steps * SPACE_STEP))

# ------------------------------------------------------------------
# Moving things
# ------------------------------------------------------------------
def move_item(sheet, pos, d):
    """Move an item d places (-1 up, +1 down), crossing into the next or previous
    section at an edge. Returns its new position."""
    si, ii = pos
    secs = sheet["sections"]
    for _ in range(abs(d)):
        step = 1 if d > 0 else -1
        its = secs[si]["items"]
        if 0 <= ii + step < len(its):
            its.insert(ii + step, its.pop(ii))
            ii += step
            continue
        nsi = si + step
        if not 0 <= nsi < len(secs):
            break
        it = its.pop(ii)
        if step > 0:
            secs[nsi]["items"].insert(0, it)
            si, ii = nsi, 0
        else:
            secs[nsi]["items"].append(it)
            si, ii = nsi, len(secs[nsi]["items"]) - 1
    return si, ii

def move_section(sheet, si, d):
    secs = sheet["sections"]
    j = min(max(0, si + d), len(secs) - 1)
    secs.insert(j, secs.pop(si))
    return j

def join(sheet, si):
    """Merge the section below into si; it keeps si's title."""
    secs = sheet["sections"]
    if si + 1 >= len(secs):
        raise ValueError("no section below to join")
    nxt = secs.pop(si + 1)
    secs[si]["items"] += nxt["items"]
    if nxt.get("auto") != secs[si].get("auto"):
        secs[si]["auto"] = ""               # a mix is no longer one type's own section

def group(sheet, positions, title=""):
    """Move the items at these positions (in reading order) into a new section
    with this title, just after the section of the first of them (or in its
    place, if that empties it). Sections the move empties go. Returns the new
    section's index."""
    secs = sheet["sections"]
    if not positions:
        raise ValueError("no problems to group")
    sources = [secs[si] for si in sorted({si for si, _ in positions})]
    first = secs[positions[0][0]]
    moved = [secs[si]["items"][ii] for si, ii in positions]
    for si, ii in reversed(positions):
        del secs[si]["items"][ii]
    sec = new_section(title)
    sec["items"] = moved
    secs.insert(secs.index(first) + 1, sec)
    secs[:] = [x for x in secs if x["items"] or not any(x is y for y in sources)]
    return next(i for i, x in enumerate(secs) if x is sec)

def fresh_copy(sheet, it, seed):
    """A new item like it (same entry, width, space) with a newly drawn problem."""
    seen = seen_of(sheet)
    new = new_item(it["bank"], it["entry"], seed, seen)
    new.update(width=it["width"], space=it["space"])
    return new
