#!/usr/bin/env python3
"""Fail-closed owner-exclusion check for experimental Unified JARs.

Usage: python3 scripts/check_owner_exclusion.py path/to/SlimefunUnified.jar
This checks archive paths and embedded class/package names; it is not a
substitute for source review of copied or renamed feature implementations.
"""
import argparse
import sys
import stat
import zipfile

FORBIDDEN = ("magicexpansion", "sf_magicexpansion")
# Avoid scanning arbitrary textual credits or license notices: references to
# the excluded historical addon are permitted in documentation.


def check_jar(path):
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            # ZIP permits duplicate entries and ambiguous separators; refuse
            # archives whose contents cannot be audited unambiguously.
            normalized = [name.replace("\\", "/").lower() for name in names]
            if len(set(normalized)) != len(normalized):
                raise ValueError("duplicate or case-colliding ZIP entries")
            if any(\n                name.startswith("/")\n                or ".." in name.split("/")\n                or (len(name) >= 2 and name[0].isalpha() and name[1] == ":")\n                or any(part == "" for part in name.rstrip("/").split("/"))\n                for name in normalized\n            ):
                raise ValueError("unsafe archive entry path")
            # A ZIP symlink may point outside the archive or to excluded content.
            # Never accept filesystem links in a compiled plugin artifact.
            links = [
                info.filename for info in archive.infolist()
                if stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK
            ]
            if links:
                raise ValueError("symlink ZIP entries forbidden: " + ", ".join(links[:10]))
            if archive.testzip() is not None:
                raise ValueError("corrupt ZIP entry")
            hits = [
                name for name, canonical in zip(names, normalized)
                if not (canonical.startswith("meta-inf/credits/") and canonical.endswith((".txt", ".md")))
                and any(token in canonical.replace("-", "_") for token in FORBIDDEN)
            ]
            # Nested JARs cannot be inspected safely by entry-name matching;
            # reject them until a separate dependency/source audit approves them.
            nested = [name for name, canonical in zip(names, normalized) if canonical.endswith(".jar")]
            if nested:
                raise ValueError("nested JARs require manual review: " + ", ".join(nested[:10]))
            if hits:
                raise ValueError("excluded MagicExpansion archive paths: " + ", ".join(hits[:20]))
            if not any(name.endswith(".class") for name in normalized):
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
