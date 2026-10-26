"""Khan Prealgebra: one bank per Khan Academy lesson, ported from the old
app's sets/archive/PreAlg_UU_LL*.py, as khan_alg1 is (see its docstring).
A lesson's NAME is kpa_UU_LL, its TITLE "Lesson U-L: <Khan's title>".
"""
COURSE = "Khan Prealgebra"
UNITS = {
    1: "Unit 1: Factors and multiples",
    3: "Unit 3: Ratios and rates",
    6: "Unit 6: Variables & expressions",
    8: "Unit 8: Percent & rational number word problems",
}

def courses(unit):
    """The COURSES tag for a lesson of this unit."""
    return {COURSE: UNITS[unit]}
