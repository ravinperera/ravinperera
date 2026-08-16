import tempfile
import unittest
from pathlib import Path

from scripts.validate_profile import validate


class ValidateProfileTests(unittest.TestCase):
    def test_valid_markdown_and_fenced_example_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "# Profile\n\n[Guide](docs/guide.md)\n\n```md\n[Example](missing.md)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(validate(root), [])

    def test_missing_relative_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[Missing](docs/missing.md)\n", encoding="utf-8")

            errors = validate(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("missing local link target 'docs/missing.md'", errors[0])

    def test_relative_link_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "repo"
            root.mkdir()
            (parent / "outside.md").write_text("# Outside\n", encoding="utf-8")
            (root / "README.md").write_text("[Outside](../outside.md)\n", encoding="utf-8")

            errors = validate(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("link target escapes repository '../outside.md'", errors[0])

    def test_text_hygiene_failures_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Profile  ", encoding="utf-8")

            errors = validate(root)

            self.assertTrue(any("trailing whitespace" in error for error in errors))
            self.assertTrue(any("missing final newline" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
