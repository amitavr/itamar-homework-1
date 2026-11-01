"""Check that the combined submission is current, restricted, and behaviorally correct."""

import ast
import unittest
from unittest.mock import patch

import test_homework
from submission import HW1 as submission
from tools.build_submission import OUTPUT, ROOT, SOURCE_PATHS, build_submission_text


FUNCTION_NAMES = (
    "calculate_ticket_price",
    "is_direct_route",
    "calculate_travel_time",
    "initialize_station",
    "split_schedule",
    "find_conflicts",
    "delay_train",
    "resolve_conflicts",
    "find_direct_trains",
)


class SubmissionTests(unittest.TestCase):
    """Validate the actual file intended for submission, not only the review modules."""

    def test_generated_file_is_current(self):
        """A changed review answer must be followed by rebuilding the submission."""
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), build_submission_text())

    def test_exactly_nine_functions_with_docstrings(self):
        """Expose the requested API and keep a docstring on every function."""
        tree = ast.parse(OUTPUT.read_text(encoding="utf-8"))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.assertEqual([node.name for node in functions], list(FUNCTION_NAMES))
        for function in functions:
            with self.subTest(function=function.name):
                self.assertTrue(ast.get_docstring(function))
        self.assertTrue(ast.get_docstring(tree))
        self.assertEqual(len(tree.body), len(FUNCTION_NAMES) + 1)

    def test_function_implementations_match_review_scripts(self):
        """The combined copy must contain the same implementations as the review files."""
        tree = ast.parse(OUTPUT.read_text(encoding="utf-8"))
        combined = {
            node.name: ast.dump(node)
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }
        for path in SOURCE_PATHS:
            source_tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
            for node in source_tree.body:
                if isinstance(node, ast.FunctionDef):
                    with self.subTest(function=node.name):
                        self.assertEqual(combined[node.name], ast.dump(node))

    def test_only_permitted_python_constructs(self):
        """Reject imports, classes, sets, comprehensions, and unapproved calls."""
        allowed_nodes = (
            ast.Module, ast.Expr, ast.Constant, ast.FunctionDef, ast.arguments,
            ast.arg, ast.Assign, ast.AugAssign, ast.Name, ast.Load, ast.Store,
            ast.If, ast.Return, ast.For, ast.While, ast.Continue, ast.Break,
            ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.Add, ast.Sub,
            ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub, ast.UAdd,
            ast.And, ast.Or, ast.Not, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
            ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.Subscript, ast.List, ast.Tuple,
            ast.Dict, ast.Call, ast.Attribute, ast.keyword,
        )
        allowed_calls = set(FUNCTION_NAMES) | {
            "len", "chr", "str", "ord", "int", "bool", "float", "list", "dict",
            "pow", "type", "range", "min", "max", "print", "sum", "enumerate", "round",
        }
        allowed_methods = {"pop", "insert", "index", "append", "get", "keys", "values", "items", "update"}
        tree = ast.parse(OUTPUT.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            with self.subTest(node=type(node).__name__, line=getattr(node, "lineno", 0)):
                self.assertIsInstance(node, allowed_nodes)
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertIn(node.func.id, allowed_calls)
                    else:
                        self.assertIsInstance(node.func, ast.Attribute)
                        self.assertIn(node.func.attr, allowed_methods)

    def test_all_behavior_cases_against_combined_script(self):
        """Run the same behavioral suite again with all nine combined functions."""
        functions = {name: getattr(submission, name) for name in FUNCTION_NAMES}
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_homework)
        expected_count = suite.countTestCases()
        result = unittest.TestResult()
        with patch.multiple(test_homework, **functions):
            suite.run(result)
        self.assertGreater(expected_count, 0)
        self.assertEqual(result.testsRun, expected_count)
        self.assertEqual(result.errors, [], str(result.errors))
        self.assertEqual(result.failures, [], str(result.failures))


if __name__ == "__main__":
    unittest.main()