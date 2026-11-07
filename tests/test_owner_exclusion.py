"""Regression tests for the experimental owner-exclusion archive gate.

Run: python3 -m unittest discover -s tests -p 'test_owner_exclusion.py'
"""
import importlib.util
import pathlib
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("owner_exclusion", ROOT / "scripts" / "check_owner_exclusion.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class OwnerExclusionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.jar = pathlib.Path(self.temp.name) / "unified.jar"

    def write(self, entries):
        with zipfile.ZipFile(self.jar, "w") as archive:
            for name, data in entries.items():
                archive.writestr(name, data)

    def test_safe_class_and_historical_credit_allowed(self):
        self.write({"org/example/Unified.class": b"bytecode",
                    "META-INF/credits/MagicExpansion.txt": b"excluded by owner"})
        self.assertEqual(guard.check_jar(self.jar), 0)

    def test_clean_jar_passes(self):
        self.write({"org/example/Unified.class": b"bytecode",
                    "META-INF/credits.txt": b"MagicExpansion excluded by owner"})
        self.assertEqual(guard.check_jar(self.jar), 0)

    def test_magic_expansion_class_rejected(self):
        self.write({"org/example/Unified.class": b"x",
                    "me/example/MagicExpansionFeature.class": b"x"})
        self.assertEqual(guard.check_jar(self.jar), 1)

    def test_nested_jar_rejected(self):
        self.write({"org/example/Unified.class": b"x", "lib/extra.jar": b"x"})
        self.assertEqual(guard.check_jar(self.jar), 1)

    def test_classless_archive_rejected(self):
        self.write({"README.txt": b"hello"})
        self.assertEqual(guard.check_jar(self.jar), 1)

    def test_corrupt_archive_rejected(self):
        self.jar.write_bytes(b"not a zip")
        self.assertEqual(guard.check_jar(self.jar), 1)


if __name__ == "__main__":
    unittest.main()
