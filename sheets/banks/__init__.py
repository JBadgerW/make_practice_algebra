"""Problem banks. A bank is a module (or package) here that provides:

    NAME, TITLE, INSTRUCTIONS     its key, display name, default instructions
    ENTRIES, ENTRY                what can be added: dict(key, type, title, width, space, ...)
    entry_key(text)               the user's spelling of an entry -> its key, or None
    type_of(entry)                the type an entry belongs to
    heading(type), hint(type), special(type)
                                  a type's section heading; (label, title, look, move); a special case?
    initial_seen(), seen_key(p)   what must never be drawn; a problem's no-repeat key
    generate(entry, rng, seen)    a new checked problem (adds it to seen); RuntimeError if none
    check(p)                      "checked" | "failed" | "unchecked"
    typst(p), answer_typst(p)     Typst markup for the sheet and the key
    text(p), answer_text(p)       plain text for the terminal
"""
import importlib

NAMES = ("literal",)

def get(name):
    if name not in NAMES:
        raise KeyError(f"no bank named {name!r}")
    return importlib.import_module(f"{__name__}.{name}")
