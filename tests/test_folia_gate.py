import unittest
from scripts.folia_gate import experimental_mode, rewrite_pinned_descriptor, validate_unified_descriptor

DESCRIPTOR = "name: Slimefun\nfolia-supported: true\ncommands:\n  slimefun:\n    description: normal\n"


class FoliaGateTest(unittest.TestCase):
    def test_prototype_disables_inherited_folia_claim(self):
        result = rewrite_pinned_descriptor(DESCRIPTOR)
        self.assertIn("folia-supported: false\n", result)
        self.assertIn("commands:\n", result)
        validate_unified_descriptor(result)

    def test_explicit_experimental_opt_in_enables_boot_testing(self):
        result = rewrite_pinned_descriptor(DESCRIPTOR, test_mode=True)
        self.assertEqual(result, DESCRIPTOR)
        validate_unified_descriptor(result, test_mode=True)

    def test_folia_flag_is_verified_in_output(self):
        with self.assertRaises(ValueError):
            validate_unified_descriptor(DESCRIPTOR)
        with self.assertRaises(ValueError):
            validate_unified_descriptor(rewrite_pinned_descriptor(DESCRIPTOR), test_mode=True)

    def test_duplicate_folia_keys_fail_closed(self):
        with self.assertRaises(ValueError):
            rewrite_pinned_descriptor(DESCRIPTOR + "folia-supported: false\n")
        with self.assertRaises(ValueError):
            validate_unified_descriptor(DESCRIPTOR + " folia-supported: false\n")

    def test_missing_or_mutated_pinned_anchor_fails(self):
        for descriptor in ("name: Slimefun\n", "name: Slimefun\nfolia-supported: false\n", "name: Slimefun\nfolia-supported: YES\n"):
            with self.subTest(descriptor=descriptor), self.assertRaises(ValueError):
                rewrite_pinned_descriptor(descriptor)

    def test_invalid_environment_is_rejected(self):
        self.assertFalse(experimental_mode({}))
        self.assertFalse(experimental_mode({"UNIFIED_FOLIA_EXPERIMENTAL": "0"}))
        self.assertTrue(experimental_mode({"UNIFIED_FOLIA_EXPERIMENTAL": "1"}))
        for bad in ("true", "yes", "2", ""):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                experimental_mode({"UNIFIED_FOLIA_EXPERIMENTAL": bad})


if __name__ == "__main__":
    unittest.main()
