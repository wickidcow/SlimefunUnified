import copy
import unittest
from scripts.check_platform_matrix import TARGETS, verify


def fixture():
    modules = [{"slug": "legacy-core", "source_sha": "a" * 40}, {"slug": "extraheads", "source_sha": "b" * 40}]
    for row in modules:
        row["targets"] = {target: {"state": "UNTESTED", "evidence": []} for target in TARGETS}
    manifest = {"addons": [
        {"slug": "extraheads", "status": "integrated-compile-verified", "integrated_source_sha": "b" * 40},
        {"slug": "magicexpansion", "status": "excluded-by-owner", "integrated_source_sha": None},
        {"slug": "mobdrops", "status": "pending", "integrated_source_sha": None}
    ]}
    return {"schema_version": 1, "required_targets": list(TARGETS), "stable_ready": False, "modules": modules}, manifest


class PlatformMatrixTest(unittest.TestCase):
    def test_complete_experimental_matrix_valid(self):
        matrix, manifest = fixture()
        verify(matrix, manifest, "a" * 40)

    def test_missing_folia_target_rejected(self):
        matrix, manifest = fixture()
        del matrix["modules"][1]["targets"]["folia-26.3+"]
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)

    def test_untracked_integrated_module_rejected(self):
        matrix, manifest = fixture()
        manifest["addons"].append({"slug": "souljars", "status": "integrated-compile-verified", "integrated_source_sha": "c" * 40})
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)

    def test_excluded_module_must_not_appear(self):
        matrix, manifest = fixture()
        clone = copy.deepcopy(matrix["modules"][1])
        clone["slug"] = "magicexpansion"
        matrix["modules"].append(clone)
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)

    def test_pass_requires_evidence(self):
        matrix, manifest = fixture()
        matrix["modules"][0]["targets"]["folia-1.21.11"]["state"] = "PASSED"
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)

    def test_stable_ready_requires_every_platform(self):
        matrix, manifest = fixture()
        matrix["stable_ready"] = True
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)

    def test_pinned_source_drift_rejected(self):
        matrix, manifest = fixture()
        matrix["modules"][1]["source_sha"] = "z" * 40
        with self.assertRaises(ValueError):
            verify(matrix, manifest, "a" * 40)


if __name__ == "__main__":
    unittest.main()
