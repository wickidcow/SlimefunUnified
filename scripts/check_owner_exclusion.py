#!/usr/bin/env python3
"""Fail-closed owner-exclusion check for experimental Unified JARs.

Usage: python3 scripts/check_owner_exclusion.py path/to/SlimefunUnified.jar
This checks archive paths and embedded class/package names; it is not a
substitute for source review of copied or renamed feature implementations.
"""
import argparse
import sys
import zipfile

FORBIDDEN = ("magicexpansion", "sf_magicexpansion")
# Avoid scanning arbitrary textual credits or license notices: references to
# the excluded historical addon are permitted in documentation.


def check_jar(path):
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if archive.testzip() is not None:
                raise ValueError("corrupt ZIP entry")
            hits = [
                name for name in names
                if not (name.lower().startswith("meta-inf/credits/") and name.lower().endswith((".txt", ".md")))\n                and any(token in name.lower().replace("-", "_") for token in FORBIDDEN)
            ]
            # Nested JARs cannot be inspected safely by entry-name matching;
            # reject them until a separate dependency/source audit approves them.
            nested = [name for name in names if name.lower().endswith(".jar")]
            if nested:
                raise ValueError("nested JARs require manual review: " + ", ".join(nested[:10]))
            if hits:
                raise ValueError("excluded MagicExpansion archive paths: " + ", ".join(hits[:20]))
            if not any(name.endswith(".class") for name in names):
                raise ValueError("no compiled classes found")
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        print(f"FAIL owner exclusion: {exc}", file=sys.stderr)
        return 1
    print("PASS archive-path exclusion gate (not source/feature equivalence verification)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jar", help="experimental Unified plugin JAR")
    return check_jar(parser.parse_args().jar)


if __name__ == "__main__":
    raise SystemExit(main())
