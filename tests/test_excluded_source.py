"""Regression tests for the precompile owner-exclusion gate."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_excluded_source.py"
spec = importlib.util.spec_from_file_location("check_excluded_source", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceExclusionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.java = self.root / "src/main/java"
        self.resources = self.root / "src/main/resources"
        self.java.mkdir(parents=True)
        self.resources.mkdir(parents=True)

    def write(self, base, name):
        target = base / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture", encoding="utf-8")

    def test_normal_sources_and_distinct_magic8ball_allowed(self):
        self.write(self.java, "example/Magic8Ball.java")
        self.write(self.resources, "unified/addons/magic8ball/config.yml")
        self.assertEqual([], module.inspect(self.root))

    def test_excluded_java_package_rejected(self):
        self.write(self.java, "io/yomicer/magicexpansion/Forbidden.java")
        self.assertTrue(module.inspect(self.root))

    def test_excluded_resource_rejected_case_insensitive(self):
        self.write(self.resources, "unified/addons/SF_MagicExpansion/config.yml")
        self.assertTrue(module.inspect(self.root))

    def test_missing_source_directory_fails_closed(self):
        self.resources.rmdir()
        with self.assertRaises(ValueError):
            module.inspect(self.root)


if __name__ == "__main__":
    unittest.main()
