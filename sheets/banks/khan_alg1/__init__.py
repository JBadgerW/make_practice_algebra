"""Khan Algebra 1: one bank per Khan Academy lesson, ported from the old
app's sets/archive/Alg1_UU_LL.py. The library finds each module here (this
package isn't a bank itself; see sheets/library.py).

A lesson's NAME is ka1_UU_LL (permanent), its TITLE "Lesson U-L: <Khan's
title>", so lessons sort in order within their unit. The old sets were the
spec, problems copied from Khan included: their shapes and number ranges.
Every problem here is drawn new and its answer checked.
"""
COURSE = "Khan Algebra 1"
UNITS = {
    1: "Unit 1: Algebra foundations",
    2: "Unit 2: Solving equations & inequalities",
    6: "Unit 6: Systems of equations",
    8: "Unit 8: Functions",
    11: "Unit 11: Exponents & radicals",
    13: "Unit 13: Quadratics: Multiplying & factoring",
    15: "Unit 15: Irrational numbers",
}

def courses(unit):
    """The COURSES tag for a lesson of this unit."""
    return {COURSE: UNITS[unit]}
