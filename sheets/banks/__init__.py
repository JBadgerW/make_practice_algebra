"""Problem banks. A bank provides:

    NAME, TITLE, INSTRUCTIONS     its key, display name, default instructions
    FAMILY                        whose problems these are: a sheet never repeats a problem
                                  within a family, and a type's section is shared by the family
    FIXED                         True for written problems (the same in every version)
    ENTRIES, ENTRY                what can be added: dict(key, type, title, width, space, kind, ...);
                                  key is the entry's permanent id, which sheets store; an
                                  optional label is shown instead (so a type can be renumbered)
    entry_key(text)               the user's spelling of an entry -> its key, or None
    type_of(entry)                the type an entry belongs to
    heading(type), hint(type), special(type)
    type_instructions(type)       optional: a type's own instructions (default INSTRUCTIONS)
                                  a type's section heading; (label, title, look, move) or None;
                                  a special case?
    initial_seen(), seen_key(p)   what must never be drawn; a problem's no-repeat key
    generate(entry, rng, seen)    a new checked problem (adds it to seen); RuntimeError if none
    check(p)                      "checked" | "failed" | "unchecked"
    typst(p, gap), answer_typst(p)  Typst markup for the sheet and the key ("" answer: none printed)
    key_typst(p, gap), PREAMBLE   optional: the prompt as the key shows it; Typst definitions
                                  the markup needs, printed once per file
    text(p), answer_text(p)       plain text for the terminal
    edit_text(p), from_edit(text, p), answer_edit_text(p), with_answer(p, text)
                                  hand editing; the last two return (problem, status)

    COURSES                       optional: the courses it belongs to (see sheets/library.py);
                                  a type may carry its own "courses"
    FORMERLY                      optional: names the bank used to have (NAME is permanent)

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

def canonical(name):
    """A bank's name now, from any name it has had ("formerly")."""
    return library.current().canonical(name)

def label(b, entry):
    """What the banks pane shows for an entry: its label, else its key (its id)."""
    return b.ENTRY[entry].get("label") or entry

def get(name):
    """A bank by name (a stand-in, marked MISSING, for one that's gone)."""
    return library.current().get(name)

def instructions(b, typ):
    """The instructions for a section of one type of bank b."""
    f = getattr(b, "type_instructions", None)
    return f(typ) if f else b.INSTRUCTIONS

def problems(name):
    """A fixed bank's problems (empty for a generator)."""
    return getattr(get(name), "PROBLEMS", [])
