"""Ensure duplicate ZIP names cannot bypass the experimental JAR gate."""
import io
import sys
import unittest
import warnings
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from zip_entry_integrity import duplicate_entries

class ZipEntryIntegrityTest(unittest.TestCase):
    def test_unique_entries_pass(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as z:
            z.writestr("plugin.yml", "name: Slimefun")
            z.writestr("com/example/Example.class", b"bytecode")
        data.seek(0)
        with zipfile.ZipFile(data) as z:
            self.assertEqual([], duplicate_entries(z))

    def test_repeated_class_and_descriptor_fail(self):
        data = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(data, "w") as z:
                for name in ("plugin.yml", "com/example/Example.class"):
                    z.writestr(name, b"old")
                    z.writestr(name, b"new")
        data.seek(0)
        with zipfile.ZipFile(data) as z:
            self.assertEqual(["com/example/Example.class", "plugin.yml"], duplicate_entries(z))

if __name__ == "__main__":
    unittest.main()
