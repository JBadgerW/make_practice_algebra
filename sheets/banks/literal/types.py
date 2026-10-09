"""The literal-equation classification: eleven types and two special cases."""

# ------------------------------------------------------------------
# The sequence. Each type: key, short title, what to look for, the move,
# worksheet problems, workspace height on the lesson worksheet (in), the
# work space below a practice problem (work), and the
# problems worked step by step in the guide.
# ------------------------------------------------------------------

TYPES = [
    dict(key="1", title="One Step",
         look="The unknown is tied to the rest by a single operation: $+$, $-$, $times$, or $div$.",
         move="Undo that one operation on both sides.",
         probs=[1, 2, 3, 4, 5, 6, 7, 8], space=0.95, work="0.75in", worked=[1]),
    dict(key="2", title="Add or Subtract, Then Divide",
         look="No fractions. The unknown's term has other terms added to it or subtracted from it.",
         move="Undo the adding or subtracting first, then divide by the unknown's coefficient.",
         probs=[9, 10, 11, 12], space=1.1, work="0.75in", worked=[9]),
    dict(key="3", title="Clear One Denominator",
         look="One fraction bar (or a fraction coefficient like $1/3$), and no parentheses to distribute.",
         move="Multiply both sides by the denominator; then add or subtract and divide as usual.",
         probs=[13, 14, 15, 16, 17, 18], space=1.25, work="1in", worked=[13]),
    dict(key="4", title="Distribute First",
         look="The unknown is inside parentheses, with a number or letter multiplying the group.",
         move="Distribute; then add or subtract like terms and divide.",
         probs=[19, 20, 21, 22, 23, 24], space=1.5, work="1.25in", worked=[19]),
    dict(key="5", title="Clear a Denominator, Then Distribute",
         look="A fraction and a set of parentheses.",
         move="Multiply both sides by the denominator first, then distribute and solve.",
         probs=[25, 26, 27], space=1.5, work="1.25in", worked=[25]),
    dict(key="6", title="Clear Two Denominators",
         look="Two different fractions in the equation.",
         move="Multiply every term on both sides by both denominators, which clears both fractions at once.",
         probs=[28, 29], space=1.5, work="1.25in", worked=[28]),
    dict(key="7", title="Factor Out, Then Divide",
         look="The unknown appears in two terms that are already together on one side.",
         move="Factor the unknown out of those terms, then divide by what is left in the parentheses.",
         probs=[30, 31], space=1.4, work="1.25in", worked=[30]),
    dict(key="8", title="Gather, Factor Out, Divide",
         look="The unknown appears on both sides of the equation.",
         move="Add or subtract to get every term with the unknown on one side and everything else on the other; then factor out and divide.",
         probs=[32, 33, 34, 35], space=1.6, work="1.25in", worked=[32]),
    dict(key="9", title="Distribute, Gather, Factor Out, Divide",
         look="Parentheses, and the unknown shows up in more than one term.",
         move="Distribute first; then gather, factor out, and divide as in Type 8.",
         probs=[36, 37, 38], space=1.75, work="1.5in", worked=[36]),
    dict(key="10", title="Clear Single-Term Denominators, Then Solve",
         look="Fractions whose denominators are single numbers or letters.",
         move="Multiply both sides by every denominator to clear the fractions; what is left is a Type 9 (or easier) equation.",
         probs=[39, 40, 41], space=1.85, work="1.5in", worked=[39]),
    dict(key="11", title="Clear a Multi-Term Denominator",
         look="A denominator that is a sum or difference, such as $(x - 1)$.",
         move="Multiply both sides by the whole denominator, keeping its parentheses; then distribute and solve as in Type 9.",
         probs=[42, 43, 44, 45], space=1.85, work="1.5in", worked=[42]),
    dict(key="A", title="Watch the Sign", special=True,
         look="The term with the unknown has a minus sign in front of it.",
         move="Add that term to both sides so it is positive on the other side, then solve. (If you leave it where it is, divide by the negative coefficient, not the positive one.)",
         probs=[46, 47], space=1.2, work="1in", worked=[46, 47]),
    dict(key="B", title="Finish with a Square Root", special=True,
         look="The unknown is squared.",
         move="Solve for the squared term as usual, then take the square root of both sides. These unknowns are lengths, so use the positive root.",
         probs=[48, 49, 50], space=1.5, work="1.25in", worked=[48, 49, 50]),
]

def label(t):
    return ("Special Case " if t.get("special") else "Type ") + t["key"]

TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]
