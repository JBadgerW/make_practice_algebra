"""Writing a sheet: its .sheet.json, its Typst files, and (when typst is
installed) their PDFs; and a one-document preview.

    build(sheet, out, name)        NAME.sheet.json, NAME.typ, NAME_slides.typ, compiled
    preview(sheet, v, what)        one document of one version, compiled into a temp folder
"""
import shutil, subprocess, tempfile
from pathlib import Path
from . import sheet as sh, writer
from .draft import DEFAULTS

def build(sheet, out=DEFAULTS["out"], name=DEFAULTS["name"], compile=True):
    """Write NAME.sheet.json, NAME.typ (every version's worksheet, each with its
    key after it; or a warm-up, each version's front and back) and NAME_slides.typ (every
    version's slides), compiled when typst is found.
    Returns dict(out, files, compiled, sheet); raises RuntimeError."""
    if not sh.items(sheet):
        raise RuntimeError("no problems: the sheet is empty")
    outp = Path(out).expanduser().resolve()   # ~ is home; a relative out starts in the current folder
    outp.mkdir(parents=True, exist_ok=True)
    typst = shutil.which("typst") if compile else None
    sh.save(sheet, outp / f"{name}.sheet.json")
    written = [f"{name}.sheet.json"]
    page = writer.warmup(sheet) if sh.is_warmup(sheet) else writer.worksheets(sheet)
    for fname, text in ((f"{name}.typ", page), (f"{name}_slides.typ", writer.slides(sheet))):
        (outp / fname).write_text(text)
        if typst:
            r = subprocess.run([typst, "compile", fname], cwd=outp, capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError(f"typst failed on {fname}:\n{r.stderr}")
        written.append(fname)
    return dict(out=outp, files=written, compiled=bool(typst), sheet=sheet)

def preview(sheet, v=0, what="sheet", folder=None):
    """Compile one document of version v (0-based), the worksheet (a warm-up's
    front and back), key, or slides, into folder (a new temp folder by default), always under the same
    name so an open viewer reloads it. Returns the PDF's path; raises RuntimeError."""
    if not sh.items(sheet):
        raise RuntimeError("no problems: the sheet is empty")
    typst = shutil.which("typst")
    if not typst:
        raise RuntimeError("typst not found: can't preview")
    text = {"sheet": lambda: writer.warmup(sheet, v) if sh.is_warmup(sheet) else writer.worksheet(sheet, v),
            "key": lambda: writer.warmup_key(sheet, v) if sh.is_warmup(sheet) else writer.worksheet(sheet, v, key=True),
            "slides": lambda: writer.slides(sheet, v)}[what]()
    outp = Path(folder or tempfile.mkdtemp(prefix="mathsheet-"))
    fname = "preview" + {"sheet": "", "key": "_key", "slides": "_slides"}[what] + ".typ"
    (outp / fname).write_text(text)
    r = subprocess.run([typst, "compile", fname], cwd=outp, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"typst failed on {fname}:\n{r.stderr}")
    return outp / fname.replace(".typ", ".pdf")
