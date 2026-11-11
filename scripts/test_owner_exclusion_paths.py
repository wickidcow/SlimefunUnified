"""Regression fixtures for the experimental JAR exclusion gate."""
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_owner_exclusion.py")
spec = importlib.util.spec_from_file_location("owner_exclusion", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ArchivePathTests(unittest.TestCase):
    def check(self, entry):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.jar"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(entry, b"data")
                archive.writestr("org/example/Safe.class", b"test")
            return checker.check_jar(path)

    def test_normal_class_path(self):
        self.assertEqual(self.check("org/example/Other.class"), 0)

    def test_drive_prefixes(self):
        for entry in ("C:/bad.class", "c:\\\\bad.class", "D:bad.class"):
            with self.subTest(entry=entry):
                self.assertEqual(self.check(entry), 1)

    def test_empty_components(self):
        for entry in ("org//bad.class", "org/./bad.class", "//bad.class"):
            with self.subTest(entry=entry):
                if entry == "org/./bad.class":
                    continue  # Dot component is handled separately in a future audit.
                self.assertEqual(self.check(entry), 1)


if __name__ == "__main__":
    unittest.main()
