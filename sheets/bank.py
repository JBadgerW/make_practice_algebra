"""What every bank is, to the rest of the app: one object with the whole bank
interface (see sheets/banks/__init__.py), whatever the bank left out.

    Bank             the optional parts' defaults, in one place. A new optional
                     part of the interface goes here, with what a bank that
                     doesn't have it should do; the app then just calls it.
    GeneratorBank    a generator module (sheets/banks/*.py) as a Bank: the
                     module's own names first, then the defaults
    missing(mod)     the required names a generator module lacks

The library wraps each generator when it reads it (sheets/library.py), so the
app never asks a bank whether it has something (no getattr, no hasattr): a
bank file with a missing required name is reported once, in :warnings, when
the library is read, not when a key happens to need it.

Fixed banks (sheets/banks/fixed.py) inherit from Bank directly.
"""
import types

# A problem's own line on the page, in inches, with the gap after it: plain, or
# with a stacked fraction (measured from the refined template in Typst). What
# the page-break estimate uses for a bank with no height() of its own.
PLAIN_IN, FRAC_IN = 0.30, 0.38

class Bank:
    """The defaults for the optional parts of the bank interface."""
    FIXED = False           # True: written problems, the same in every version
    MISSING = False         # True: a stand-in for a bank the library doesn't have
    PREAMBLE = ""           # Typst definitions the bank's markup needs, once per file
    COURSES = None          # the courses it belongs to (see sheets/library.py)
    FORMERLY = ()           # names the bank used to have
    WARNINGS = ()           # what the library should report about it
    SOURCE = None           # the file it was read from (a fixed bank); None for a generator
    PROBLEMS = ()           # a fixed bank's problems, and by id
    PROBLEM = types.MappingProxyType({})

    def initial_seen(self):
        """What must never be drawn."""
        return set()

    def type_of(self, entry):
        """The type an entry belongs to."""
        return entry

    def special(self, typ):
        """Is the type a special case?"""
        return False

    def hint(self, typ):
        """(label, title, look, move), or None when the type has no hints."""
        return None

    def type_instructions(self, typ):
        """A type's own instructions (default: the bank's)."""
        return self.INSTRUCTIONS

    def edit_hint(self, p):
        """What to type when editing the problem, if it isn't plain: "equation ; unknown"."""
        return ""

    def height(self, p):
        """The height of the problem's own line on the page, in inches."""
        return FRAC_IN if "/" in p["prompt"] else PLAIN_IN

    def key_typst(self, p, gap="0.3em"):
        """The prompt as the key shows it (a bank may draw on it, as when a graph is the answer)."""
        return self.typst(p, gap)

    def slide_typst(self, p, key=False):
        """The problem's whole slide (its answer too, when key); None to show it as usual."""
        return None

    def slide_parts(self, p, key=False):
        """(text, graph) of a graphed problem's slide, for the board presenter; None for any other."""
        return None

# What a generator module must define; the rest have defaults above.
REQUIRED = ("NAME", "TITLE", "INSTRUCTIONS", "FAMILY", "ENTRIES", "ENTRY",
            "entry_key", "heading", "seen_key", "generate", "check",
            "typst", "answer_typst", "text", "answer_text",
            "edit_text", "from_edit", "answer_edit_text", "with_answer")

def missing(mod):
    """The required names a generator module doesn't define."""
    return [n for n in REQUIRED if not hasattr(mod, n)]

class GeneratorBank:
    """A generator module as a Bank. Every name is the module's own, looked up
    when it's asked for (so the module stays the one place a bank is defined);
    a name the module lacks is Bank's default."""
    def __init__(self, module):
        self.module = module

    def __getattr__(self, name):            # only for names not on this object: everything but module
        if name == "module":                # (not set yet: don't look for it in itself)
            raise AttributeError(name)
        try:
            return getattr(self.module, name)
        except AttributeError:
            pass
        try:
            default = Bank.__dict__[name]
        except KeyError:
            raise AttributeError(f"the bank {getattr(self.module, 'NAME', self.module)!r} has no {name}") from None
        return types.MethodType(default, self) if isinstance(default, types.FunctionType) else default

    def __repr__(self):
        return f"<GeneratorBank {getattr(self.module, 'NAME', self.module)!r}>"
