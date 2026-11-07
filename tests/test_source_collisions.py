import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_source_collisions.py"
spec = importlib.util.spec_from_file_location("source_collision_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class SourceCollisionTests(unittest.TestCase):
    def test_distinct_sources_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "core", Path(tmp) / "addon"
            for root, name in ((a, "Core.java"), (b, "Addon.java")):
                file = root / "src/main/java/example" / name
                file.parent.mkdir(parents=True)
                file.write_text("class Example {}")
            self.assertEqual([], gate.collisions(a, b))

    def test_identical_paths_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "core", Path(tmp) / "addon"
            for root in (a, b):
                file = root / "src/main/java/example/Shared.java"
                file.parent.mkdir(parents=True)
                file.write_text("class Shared {}")
            self.assertEqual(1, len(gate.collisions(a, b)))

    def test_case_insensitive_paths_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "core", Path(tmp) / "addon"
            for root, name in ((a, "Shared.java"), (b, "shared.java")):
                file = root / "src/main/java/example" / name
                file.parent.mkdir(parents=True)
                file.write_text("class Shared {}")
            self.assertEqual(1, len(gate.collisions(a, b)))

    def test_addon_to_addon_collision_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            core, first, second = (Path(tmp) / name for name in ("core", "first", "second"))
            for root, name in ((core, "Core.java"), (first, "Shared.java"), (second, "Shared.java")):
                file = root / "src/main/java/example" / name
                file.parent.mkdir(parents=True)
                file.write_text("class Example {}")
            self.assertEqual([], gate.collisions(core, first))
            self.assertEqual([], gate.collisions(core, second))
            self.assertEqual(1, len(gate.collisions(core, first, second)))

    def test_assembly_checks_all_three_sources_before_soul_copy(self):
        assembly = (SCRIPT.parent / "assemble_unified.sh").read_text()
        combined = 'check_source_collisions.py" "$WORK" "$EXTRA_WORK" "$SOUL_WORK"'
        self.assertIn(combined, assembly)
        self.assertLess(assembly.index(combined), assembly.index('cp -R "$SOUL_WORK/src/main/java/."'))

    def test_missing_source_tree_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                gate.collisions(Path(tmp) / "missing")


if __name__ == "__main__":
    unittest.main()
