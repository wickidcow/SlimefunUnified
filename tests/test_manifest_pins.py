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
        for name in ("legacy-core.sha", "extraheads.sha", "souljars.sha"):
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

    def test_source_pin_mismatch_rejected(self):
        (self.root / "upstream/extraheads.sha").write_text("b" * 40)
        self.assertTrue(any("disagree" in e for e in validate(self.root)))

    def test_missing_historical_entry_rejected(self):
        self.mutate(lambda d: d["addons"].pop())
        self.assertTrue(any("44" in e for e in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
