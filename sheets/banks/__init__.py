"""Problem banks. A bank provides:

    NAME, TITLE, INSTRUCTIONS     its key, display name, default instructions
    FAMILY                        whose problems these are: a sheet never repeats a problem
                                  within a family, and a type's section is shared by the family
    FIXED                         True for written problems (the same in every version)
    ENTRIES, ENTRY                what can be added: dict(key, type, title, width, space, kind, ...)
    entry_key(text)               the user's spelling of an entry -> its key, or None
    type_of(entry)                the type an entry belongs to
    heading(type), hint(type), special(type)
                                  a type's section heading; (label, title, look, move) or None;
                                  a special case?
    initial_seen(), seen_key(p)   what must never be drawn; a problem's no-repeat key
    generate(entry, rng, seen)    a new checked problem (adds it to seen); RuntimeError if none
    check(p)                      "checked" | "failed" | "unchecked"
    typst(p, gap), answer_typst(p)  Typst markup for the sheet and the key
    text(p), answer_text(p)       plain text for the terminal
    edit_text(p), from_edit(text, p), answer_edit_text(p), with_answer(p, text)
                                  hand editing; the last two return (problem, status)

Generator banks are modules in this package (NAMES). Fixed banks are JSON
files in the project's banks/ folder (see fixed.py).
"""
import importlib
from .. import ROOT

NAMES = ("literal",)
FIXED_DIR = ROOT / "banks"
_fixed, _errors = {}, {}

def _scan():
    from .fixed import FixedBank
    for f in sorted(FIXED_DIR.glob("*.json")) if FIXED_DIR.is_dir() else []:
        if not any(b.path == f for b in _fixed.values()) and f not in _errors:
            try:
                b = FixedBank(f)
            except (ValueError, KeyError, TypeError, OSError) as e:
                _errors[f] = f"{f.name}: {e}"
                continue
            if b.NAME in NAMES or b.NAME in _fixed:
                _errors[f] = f"{f.name}: a bank named {b.NAME!r} already exists"
                continue
            _fixed[b.NAME] = b

def errors():
    """Messages for bank files in banks/ that couldn't be read."""
    _scan()
    return list(_errors.values())

def names():
    """Every bank: the generators, then the fixed banks by name."""
    _scan()
    return list(NAMES) + sorted(_fixed)

def get(name):
    if name in NAMES:
        return importlib.import_module(f"{__name__}.{name}")
    if name not in _fixed:
        _scan()
    if name not in _fixed:
        raise KeyError(f"no bank named {name!r}")
    return _fixed[name]

def problems(name):
    """A fixed bank's problems (empty for a generator)."""
    return getattr(get(name), "PROBLEMS", [])
