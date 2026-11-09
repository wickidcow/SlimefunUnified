import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.check_manifest_pins import validate

ROOT = Path(__file__).resolve().parents[1]


class ManifestPinsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "integration").mkdir()
        (self.root / "upstream").mkdir()
        shutil.copy(ROOT / "integration/addons.json", self.root / "integration/addons.json")
        for name in ("legacy-core.sha", "extraheads.sha", "souljars.sha", "slimytreetaps.sha", "mobdrops.sha"):
            shutil.copy(ROOT / "upstream" / name, self.root / "upstream" / name)

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, fn):
        path = self.root / "integration/addons.json"
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data))

    def test_baseline_passes(self):
        self.assertEqual(validate(self.root), [])

    def test_owner_exclusion_cannot_be_integrated(self):
        self.mutate(lambda d: next(a for a in d["addons"] if a["slug"] == "magicexpansion").update(
            status="integrated-compile-verified", integrated_source_sha="a" * 40))
        self.assertTrue(validate(self.root))

    def test_duplicate_repository_rejected(self):
        self.mutate(lambda d: d["addons"][1].update(repository=d["addons"][0]["repository"]))
        self.assertTrue(any("duplicate" in e for e in validate(self.root)))

    def test_duplicate_slug_rejected(self):
        self.mutate(lambda d: d["addons"][1].update(slug=d["addons"][0]["slug"]))
        self.assertTrue(any("duplicate addon slugs" in e for e in validate(self.root)))

    def test_unknown_status_rejected(self):
        self.mutate(lambda d: d["addons"][1].update(status="integrated-untested", integrated_source_sha="a" * 40))
        self.assertTrue(any("unknown integration status" in e for e in validate(self.root)))

    def test_unassembled_module_cannot_claim_integration(self):
        self.mutate(lambda d: next(a for a in d["addons"] if a["slug"] == "mobdrops").update(
            status="integrated-compile-verified", integrated_source_sha="a" * 40))
        self.assertTrue(any("absent from pinned assembly" in e for e in validate(self.root)))

    def test_source_pin_mismatch_rejected(self):
        (self.root / "upstream/extraheads.sha").write_text("b" * 40)
        self.assertTrue(any("disagree" in e for e in validate(self.root)))

    def test_slimytreetaps_source_pin_mismatch_rejected(self):
        (self.root / "upstream/slimytreetaps.sha").write_text("a" * 40)
        self.assertTrue(any("SlimyTreeTaps" in e and "disagree" in e for e in validate(self.root)))

    def test_staged_mobdrops_pin_mismatch_rejected(self):
        (self.root / "upstream/mobdrops.sha").write_text("a" * 40)
        self.assertTrue(any("MobDrops: staged source pin disagrees" in e for e in validate(self.root)))

    def test_missing_staged_mobdrops_pin_rejected(self):
        (self.root / "upstream/mobdrops.sha").unlink()
        self.assertTrue(any("MobDrops: missing historical entry" in e for e in validate(self.root)))

    def test_missing_historical_entry_rejected(self):
        self.mutate(lambda d: d["addons"].pop())
        self.assertTrue(any("44" in e for e in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
