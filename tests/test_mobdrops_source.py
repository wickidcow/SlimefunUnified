"""Regression tests for MobDrops pinned-source preflight (no Bukkit dependency)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_mobdrops_source.py"
spec = importlib.util.spec_from_file_location("check_mobdrops_source", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

JAVA = '''public class SfMobDrops extends JavaPlugin {
  void onEnable() {
    new Metrics(this, 11950);
    registerEvents(this, this);
    getCommand("mobdrops");
  }
}'''
PLUGIN = "name: SFMobDrops\ncommands:\n  mobdrops:\n"
PIN = module.EXPECTED_PIN

class MobDropsPreflightTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.java = self.root / "src/main/java/dev/walshy/sfmobdrops/SfMobDrops.java"
        self.java.parent.mkdir(parents=True)
        self.java.write_text(JAVA)
        self.plugin = self.root / "src/main/resources/plugin.yml"
        self.plugin.parent.mkdir(parents=True)
        self.plugin.write_text(PLUGIN)
        (self.root / "LICENSE").write_text("MIT")

    def test_valid_fixture(self):
        self.assertEqual([], module.check(self.root, PIN))

    def test_wrong_pin(self):
        self.assertTrue(module.check(self.root, "0" * 40))

    def test_missing_command(self):
        self.java.write_text(JAVA.replace('getCommand("mobdrops");', ""))
        self.assertTrue(module.check(self.root, PIN))

    def test_missing_license(self):
        (self.root / "LICENSE").unlink()
        self.assertTrue(module.check(self.root, PIN))

    def test_symlinked_license(self):
        (self.root / "LICENSE").unlink()
        (self.root / "LICENSE").symlink_to(self.java)
        self.assertTrue(module.check(self.root, PIN))

    def test_symlinked_checkout_ancestor(self):
        alias = self.root / "alias"
        actual = self.root / "actual"
        actual.mkdir()
        alias.symlink_to(actual, target_is_directory=True)
        nested = alias / "nested"
        nested.mkdir()
        self.assertIn("Invalid or symlinked MobDrops checkout", module.check(nested, PIN))

    def test_unreadable_utf8_source(self):
        self.java.write_bytes(b"\\xff\\xfe")
        self.assertTrue(any("Unreadable MobDrops source file" in error for error in module.check(self.root, PIN)))

if __name__ == "__main__":
    unittest.main()
