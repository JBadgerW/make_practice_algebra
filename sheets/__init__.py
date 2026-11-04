"""The worksheet builder: a small core plus banks of problems.

    sheets.check     Typst math -> sympy, and numeric checks
    sheets.typst     the Typst preambles from templates/, and escaping
    sheets.present   the board presenter: two problems at a time, in a web page
    sheets.banks.*   problem banks; literal is the first
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # the project folder
