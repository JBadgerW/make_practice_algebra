"""Khan Algebra 2: one bank per Khan Academy lesson, ported from the old
app's sets/archive/Alg2_UU_LL.py, as khan_alg1 is (see its docstring).
A lesson's NAME is ka2_UU_LL, its TITLE "Lesson U-L: <Khan's title>".
"""
COURSE = "Khan Algebra 2"
UNITS = {
    1: "Unit 1: Polynomial arithmetic",
    2: "Unit 2: Complex numbers",
    3: "Unit 3: Polynomial factorization",
}

def courses(unit):
    """The COURSES tag for a lesson of this unit."""
    return {COURSE: UNITS[unit]}
