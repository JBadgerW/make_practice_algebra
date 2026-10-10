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

    COURSES                       optional: the courses it belongs to (see sheets/library.py);
                                  a type may carry its own "courses"

Generator banks are modules in this package, found automatically. Fixed
banks are JSON files: the built-in ones in the project's banks/ folder, and
your own in the library folder (see fixed.py and sheets/library.py).
"""
from .. import library

def errors():
    """What went wrong reading the library: unreadable files, unknown courses."""
    return list(library.current().warnings)

def names():
    """Every bank: the generators, then the fixed banks by name."""
    return library.current().names()

def has(name):
    """Is there a bank by this name?"""
    return library.current().has(name)

def get(name):
    """A bank by name (a stand-in, marked MISSING, for one that's gone)."""
    return library.current().get(name)

def problems(name):
    """A fixed bank's problems (empty for a generator)."""
    return getattr(get(name), "PROBLEMS", [])
