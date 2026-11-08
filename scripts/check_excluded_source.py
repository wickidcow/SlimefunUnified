#!/usr/bin/env python3
"""Reject owner-excluded MagicExpansion source/assets before compilation.

This path-level check complements the compiled-JAR gate; it does not establish
feature-equivalence or license compliance for renamed implementations.
"""
import sys
from pathlib import Path

FORBIDDEN = ("magicexpansion", "sf_magicexpansion", "io/yomicer/magicexpansion/")


def inspect(root: Path) -> list[str]:
    if not root.is_dir():
        raise ValueError(f"source tree missing: {root}")
    hits = []
    for subdir in ("src/main/java", "src/main/resources"):
        tree = root / subdir
        if not tree.is_dir():
            raise ValueError(f"source directory missing: {tree}")
        for path in tree.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(tree).as_posix().lower().replace("-", "_")
            if any(token in relative for token in FORBIDDEN):
                hits.append(f"{subdir}/{relative}")
    return hits


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_excluded_source.py <assembled-source-root>", file=sys.stderr)
        return 2
    try:
        hits = inspect(Path(sys.argv[1]))
    except (OSError, ValueError) as exc:
        print(f"FAIL source exclusion: {exc}", file=sys.stderr)
        return 1
    if hits:
        print("FAIL owner-excluded MagicExpansion source/assets: " + ", ".join(hits[:20]), file=sys.stderr)
        return 1
    print("PASS source-path owner exclusion (not feature-equivalence verification)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
