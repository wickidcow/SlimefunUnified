"""Regression tests for MobDrops pinned-source preflight (no Bukkit dependency)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from subprocess import CompletedProcess, CalledProcessError

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
        (self.root / "LICENSE").write_text(
            'MIT License\\nCopyright (c) 2020 Daniel Walsh\\n'
            'Permission is hereby granted, free of charge\\n'
            'The above copyright notice and this permission notice\\n'
            'THE SOFTWARE IS PROVIDED "AS IS"\\n'
        )

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

    def test_replaced_license_notice_rejected(self):
        (self.root / "LICENSE").write_text("MIT")
        self.assertIn(
            "MobDrops MIT attribution or license terms changed",
            module.check(self.root, PIN),
        )

    def test_removed_author_credit_rejected(self):
        license_path = self.root / "LICENSE"
        license_path.write_text(license_path.read_text().replace("Daniel Walsh", "Unknown"))
        self.assertIn(
            "MobDrops MIT attribution or license terms changed",
            module.check(self.root, PIN),
        )

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

    def test_checkout_head_matches_pin(self):
        responses = [
            CompletedProcess([], 0, stdout=PIN + "\n"),
            CompletedProcess([], 0, stdout=str(self.root) + "\n"),
            CompletedProcess([], 0, stdout=""),
        ]
        with patch.object(module.subprocess, "run", side_effect=responses) as git_run:
            self.assertEqual([], module.verify_checkout_head(self.root, PIN))
            self.assertIn("status", git_run.call_args.args[0])
            self.assertIn("--untracked-files=all", git_run.call_args.args[0])
            self.assertIn("--ignored=matching", git_run.call_args.args[0])

    def test_dirty_checkout_rejected(self):
        for status in (" M src/main/java/Test.java\\n", "?? injected.java\\n", "A  staged.java\\n", "!! src/main/java/Injected.java\\n"):
            with self.subTest(status=status):
                responses = [
                    CompletedProcess([], 0, stdout=PIN + "\n"),
                    CompletedProcess([], 0, stdout=str(self.root) + "\n"),
                    CompletedProcess([], 0, stdout=status),
                ]
                with patch.object(module.subprocess, "run", side_effect=responses):
                    self.assertIn(
                        "MobDrops checkout has modified or untracked source files",
                        module.verify_checkout_head(self.root, PIN),
                    )

    def test_git_status_failure_fails_closed(self):
        responses = [
            CompletedProcess([], 0, stdout=PIN + "\n"),
            CompletedProcess([], 0, stdout=str(self.root) + "\n"),
            CalledProcessError(128, "git status"),
        ]
        with patch.object(module.subprocess, "run", side_effect=responses):
            self.assertIn(
                "Cannot verify MobDrops checkout working tree",
                module.verify_checkout_head(self.root, PIN),
            )

    def test_checkout_head_mismatch(self):
        responses = [
            CompletedProcess([], 0, stdout="0" * 40 + "\n"),
            CompletedProcess([], 0, stdout=str(self.root) + "\n"),
        ]
        with patch.object(module.subprocess, "run", side_effect=responses):
            self.assertTrue(module.verify_checkout_head(self.root, PIN))

    def test_nested_git_directory_rejected(self):
        responses = [
            CompletedProcess([], 0, stdout=PIN + "\n"),
            CompletedProcess([], 0, stdout=str(self.root.parent) + "\n"),
        ]
        with patch.object(module.subprocess, "run", side_effect=responses):
            self.assertTrue(module.verify_checkout_head(self.root, PIN))

    def test_git_failure_fails_closed(self):
        with patch.object(module.subprocess, "run", side_effect=CalledProcessError(128, "git")):
            self.assertTrue(module.verify_checkout_head(self.root, PIN))

    def test_unreadable_utf8_source(self):
        self.java.write_bytes(bytes([0xff, 0xfe]))
        self.assertTrue(any("Unreadable MobDrops source file" in error for error in module.check(self.root, PIN)))

if __name__ == "__main__":
    unittest.main()
