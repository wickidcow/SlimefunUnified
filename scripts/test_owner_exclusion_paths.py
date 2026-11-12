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
    def check_entries(self, *entries):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.jar"
            with zipfile.ZipFile(path, "w") as archive:
                for entry in entries:
                    archive.writestr(entry, b"data")
                archive.writestr("org/example/Safe.class", b"test")
            return checker.check_jar(path)

    def check(self, entry):
        return self.check_entries(entry)

    def test_normal_class_path(self):
        self.assertEqual(self.check("org/example/Other.class"), 0)

    def test_distinct_magic8ball_remains_eligible(self):
        self.assertEqual(self.check("dev/example/magic8ball/Magic8Ball.class"), 0)

    def test_excluded_owner_module_paths(self):
        for entry in (
            "dev/example/MagicExpansion/Listener.class",
            "dev/example/SF_MagicExpansion/Plugin.class",
            "unified/addons/magicexpansion/source.sha",
            "unified/addons/sf_magicexpansion/config.yml",
            "DEV/EXAMPLE/MAGICEXPANSION/Listener.class",
        ):
            with self.subTest(entry=entry):
                self.assertEqual(self.check(entry), 1)

    def test_drive_prefixes(self):
        for entry in ("C:/bad.class", "c:\\\\bad.class", "D:bad.class"):
            with self.subTest(entry=entry):
                self.assertEqual(self.check(entry), 1)

    def test_empty_components(self):
        for entry in ("org//bad.class", "org/./bad.class", "//bad.class"):
            with self.subTest(entry=entry):
                self.assertEqual(self.check(entry), 1)

    def test_parent_directory_escape(self):
        for entry in ("../bad.class", "org/../bad.class", "org/./bad.class"):
            with self.subTest(entry=entry):
                self.assertEqual(self.check(entry), 1)

    def test_nested_jar_rejected(self):
        self.assertEqual(self.check("lib/other-addon.jar"), 1)

    def test_case_colliding_entries_rejected(self):
        self.assertEqual(
            self.check_entries("dev/example/Item.class", "dev/example/item.class"), 1
        )

    def test_backslash_alias_collision_rejected(self):
        self.assertEqual(
            self.check_entries("dev/example/Item.class", "dev\\example\\Item.class"), 1
        )


if __name__ == "__main__":
    unittest.main()
