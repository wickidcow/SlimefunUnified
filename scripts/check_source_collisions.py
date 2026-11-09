#!/usr/bin/env python3
"""Reject Java source overwrites and case-folding collisions in pinned modules."""
import argparse
from pathlib import Path


def collisions(*roots: Path) -> list[tuple[str, str, str]]:
    seen: dict[str, tuple[str, str]] = {}
    found: list[tuple[str, str, str]] = []
    for root in roots:
        source = root / "src/main/java"
        if not source.is_dir():
            raise ValueError(f"Missing Java source directory: {source}")
        for file in sorted(source.rglob("*.java")):
            relative = file.relative_to(source).as_posix()
            key = relative.casefold()
            if key in seen:
                found.append((relative, seen[key][0] + "/" + seen[key][1], str(root)))
            else:
                seen[key] = (str(root), relative)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        duplicates = collisions(*args.roots)
    except ValueError as error:
        parser.error(str(error))
    if duplicates:
        for path, first, second in duplicates:
            print(f"Source collision: {path}: {first} vs {second}", file=__import__("sys").stderr)
        return 1
    print("Source-pinned Java trees have no overlapping relative class paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
