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

    def test_case_insensitive_collision_within_single_addon_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            for name in ("Shared.java", "shared.java"):
                file = root / "src/main/java/example" / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("class Shared {}")
            self.assertEqual(1, len(gate.collisions(root)))

    def test_case_insensitive_package_collision_within_single_addon_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            for package in ("Example", "example"):
                file = root / "src/main/java" / package / "Shared.java"
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("class Shared {}")
            self.assertEqual(1, len(gate.collisions(root)))

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
        combined = 'check_source_collisions.py" "$WORK" "$SOUL_WORK"'
        self.assertIn(combined, assembly)
        self.assertIn('cp -R "$EXTRA_WORK/src/main/java/." "$WORK/src/main/java/"', assembly)
        self.assertLess(assembly.index('cp -R "$EXTRA_WORK/src/main/java/." "$WORK/src/main/java/"'), assembly.index(combined))
        self.assertLess(assembly.index(combined), assembly.index('cp -R "$SOUL_WORK/src/main/java/."'))

    def test_symlinked_java_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            source = root / "src/main/java/example"
            source.mkdir(parents=True)
            outside = Path(tmp) / "external.java"
            outside.write_text("class External {}")
            (source / "External.java").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "Symlink"):
                gate.collisions(root)

    def test_symlinked_package_directory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            source = root / "src/main/java"
            source.mkdir(parents=True)
            outside = Path(tmp) / "external"
            outside.mkdir()
            (outside / "External.java").write_text("class External {}")
            (source / "example").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlink"):
                gate.collisions(root)

    def test_regular_import_assets_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            config = root / "src/main/resources/config.yml"
            config.parent.mkdir(parents=True)
            config.write_text("enabled: true")
            (root / "LICENSE").write_text("MIT")
            gate.validate_import_assets(root)

    def test_symlinked_config_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            config = root / "src/main/resources/config.yml"
            config.parent.mkdir(parents=True)
            outside = Path(tmp) / "external.yml"
            outside.write_text("unsafe: true")
            config.symlink_to(outside)
            (root / "LICENSE").write_text("MIT")
            with self.assertRaisesRegex(ValueError, "Symlink"):
                gate.validate_import_assets(root)

    def test_symlinked_resource_parent_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            resources = root / "src/main/resources"
            resources.parent.mkdir(parents=True)
            outside = Path(tmp) / "external"
            outside.mkdir()
            (outside / "config.yml").write_text("unsafe: true")
            resources.symlink_to(outside, target_is_directory=True)
            (root / "LICENSE").write_text("MIT")
            with self.assertRaisesRegex(ValueError, "Symlink"):
                gate.validate_import_assets(root)

    def test_missing_license_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "addon"
            config = root / "src/main/resources/config.yml"
            config.parent.mkdir(parents=True)
            config.write_text("enabled: true")
            with self.assertRaisesRegex(ValueError, "Missing regular"):
                gate.validate_import_assets(root)

    def test_assembly_checks_assets_before_each_copy(self):
        assembly = (SCRIPT.parent / "assemble_unified.sh").read_text()
        for variable in ("EXTRA_WORK", "SOUL_WORK", "TAPS_WORK"):
            check = 'check_source_collisions.py" --check-assets "$' + variable + '"'
            copy = 'cp -R "$' + variable + '/src/main/java/."'
            self.assertIn(check, assembly)
            self.assertIn(copy, assembly)
            self.assertLess(assembly.index(check), assembly.index(copy))

    def test_missing_source_tree_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                gate.collisions(Path(tmp) / "missing")


if __name__ == "__main__":
    unittest.main()
