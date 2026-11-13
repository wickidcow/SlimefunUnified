"""Regression tests for canonical paths in the experimental JAR."""
import io
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from zip_entry_integrity import duplicate_entries


class ZipPathSafetyTest(unittest.TestCase):
    def inspect(self, names):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            for name in names:
                archive.writestr(name, b"content")
        output.seek(0)
        with zipfile.ZipFile(output) as archive:
            return duplicate_entries(archive)

    def test_normal_classes_and_directories(self):
        self.assertEqual([], self.inspect(["META-INF/", "plugin.yml", "a/b/C.class"]))

    def test_parent_traversal(self):
        self.assertEqual(["a/../plugin.yml"], self.inspect(["a/../plugin.yml"]))

    def test_dot_component(self):
        self.assertEqual(["a/./B.class"], self.inspect(["a/./B.class"]))

    def test_empty_component(self):
        self.assertEqual(["a//B.class"], self.inspect(["a//B.class"]))

    def test_absolute_path(self):
        self.assertEqual(["/plugin.yml"], self.inspect(["/plugin.yml"]))

    def test_backslash_alias(self):
        self.assertEqual(["a\\B.class"], self.inspect(["a\\B.class"]))

    def test_windows_drive_path(self):
        self.assertEqual(["C:/plugin.yml"], self.inspect(["C:/plugin.yml"]))


if __name__ == "__main__":
    unittest.main()
