"""Combine the nine review answers into one import-free homework submission.

This development tool is not part of the submitted solution. It uses Python's
syntax parser to extract function definitions, keeping their original comments.
Question headers become comments, and study-only imports are omitted because all
nine functions live in the same file. Run it again after changing an answer.
"""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "submission" / "HW1.py"
SOURCE_PATHS = (
    "part_1/question_a_ticket_price.py",
    "part_1/question_b_direct_route.py",
    "part_1/question_c_travel_time.py",
    "part_2/question_a_initialize_station.py",
    "part_2/question_b_split_schedule.py",
    "part_2/question_c_find_conflicts.py",
    "part_2/question_d_delay_train.py",
    "part_2/question_e_resolve_conflicts.py",
    "part_3/question_a_find_direct_trains.py",
)
HEADER = '''"""Homework 1: all nine answers from the supplied 15-page PDF.

Generated from the explained scripts in part_1, part_2, and part_3.
Each section keeps its approach explanation and implementation comments.
No imports, external libraries, or demonstration code are needed here.
Edit the review scripts and run python tools/build_submission.py to rebuild.
"""'''


def render_question(relative_path):
    """Keep a question's explanation and function source, but omit its imports."""
    source = (ROOT / relative_path).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=relative_path)
    lines = source.splitlines()
    explanation = ast.get_docstring(tree, clean=False)
    if explanation is None:
        raise ValueError(f"Question header missing: {relative_path}")

    header_lines = [f"# Source: {relative_path}"]
    header_lines.extend("# " + line if line else "#" for line in explanation.splitlines())
    functions = []
    for node in tree.body[1:]:
        if isinstance(node, ast.ImportFrom):
            if not node.module or not node.module.startswith(("part_1.", "part_2.")):
                raise ValueError(f"Unexpected import in {relative_path}")
        elif isinstance(node, ast.FunctionDef):
            functions.append("\n".join(lines[node.lineno - 1 : node.end_lineno]))
        else:
            raise ValueError(f"Unexpected top-level statement in {relative_path}")

    if not functions:
        raise ValueError(f"No answer function in {relative_path}")
    return "\n".join(header_lines) + "\n\n\n" + "\n\n\n".join(functions)


def build_submission_text():
    """Return the complete import-free solution in dependency order."""
    sections = [HEADER]
    sections.extend(render_question(path) for path in SOURCE_PATHS)
    return "\n\n\n".join(sections) + "\n"


def main():
    """Check the generated syntax and write the combined submission file."""
    text = build_submission_text()
    compile(text, str(OUTPUT), "exec")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as output_file:
        output_file.write(text)
    print(f"Built {OUTPUT.relative_to(ROOT)} from {len(SOURCE_PATHS)} question scripts.")


if __name__ == "__main__":
    main()