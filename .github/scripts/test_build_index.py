import tempfile
import unittest
from pathlib import Path

from build_index import LayoutError, build_sections, rebuild


def make_tech(root, name, frontmatter="domain: languages\nstatus: learning", title="Java"):
    tech = root / "@tech" / name
    tech.mkdir(parents=True)
    (tech / "README.md").write_text(f"---\n{frontmatter}\n---\n\n# {title}\n")
    return tech


class BuildIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_counts_entries_and_renders_between_markers(self):
        tech = make_tech(self.root, "java")
        (tech / "00-notes").mkdir()
        (tech / "00-notes" / "00-cheatsheet.md").write_text("x")
        (tech / "00-notes" / "01-jvm.md").write_text("x")
        (tech / "02-labs" / "00-virtual-threads").mkdir(parents=True)

        readme = rebuild("intro\n<!-- index:start -->\nold\n<!-- index:end -->\nend", build_sections(self.root))

        self.assertIn("### @tech", readme)
        self.assertIn("| languages | [Java](@tech/java/) | learning | 2 | 0 | 1 | 0 |", readme)
        self.assertNotIn("old", readme)
        self.assertTrue(readme.startswith("intro\n") and readme.endswith("\nend"))

    def test_rejects_layout_violations(self):
        cases = {
            "unknown category": lambda tech: (tech / "examples").mkdir(),
            "unnumbered entry": lambda tech: (tech / "01-snippets" / "hello").mkdir(parents=True),
            "duplicate number": lambda tech: [(tech / "01-snippets" / n).mkdir(parents=True) for n in ("00-a", "00-b")],
            "folder in notes": lambda tech: (tech / "00-notes" / "00-jvm").mkdir(parents=True),
        }
        for case, break_layout in cases.items():
            with self.subTest(case), tempfile.TemporaryDirectory() as tmp:
                break_layout(make_tech(Path(tmp), "java"))
                with self.assertRaises(LayoutError):
                    build_sections(Path(tmp))

    def test_rejects_unknown_status(self):
        make_tech(self.root, "java", frontmatter="domain: languages\nstatus: done")
        with self.assertRaises(LayoutError):
            build_sections(self.root)

    def test_rejects_content_outside_an_area(self):
        (self.root / "java").mkdir()
        with self.assertRaises(LayoutError):
            build_sections(self.root)


if __name__ == "__main__":
    unittest.main()
