"""Typst preambles (read from templates/ at import) and text escaping."""
import re
from . import ROOT

MARK = "// ==================================================\n// DOCUMENT VARIABLES"
head = (ROOT / "templates/mixed_review_v1.typ").read_text()
head = head[:head.index(MARK)]
slhead = (ROOT / "templates/mixed_review_slides.typ").read_text()
slhead = slhead[:slhead.index(MARK)]

def vars_(title, version="1", class_name="Algebra 1"):
    return f'''{MARK}
// ==================================================

#let class-name = "{class_name}"
#let worksheet-title = "{title}"
#let version = "{version}"

'''

def esc(text):
    """Make plain text safe inside a Typst [content block]."""
    return re.sub(r"([\\#$\[\]*_@<>`~])", r"\\\1", text)
