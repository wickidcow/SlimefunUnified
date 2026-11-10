#!/usr/bin/env python3
"""Fail-closed preflight for the pinned MobDrops source before Unified integration.

This is a staging gate, not a source rewrite or evidence of a compiled module.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_PIN = "8943594f006a443ce8a77113f76709c871d03697"
REQUIRED = {
    "src/main/java/dev/walshy/sfmobdrops/SfMobDrops.java": (
        r"class\s+SfMobDrops\s+extends\s+JavaPlugin",
        r"new\s+Metrics\s*\(",
        r"registerEvents\s*\(",
        r'getCommand\s*\(\s*"mobdrops"',
    ),
    "src/main/resources/plugin.yml": (
        r"(?m)^name:\s*SFMobDrops\s*$",
        r"(?m)^\s+mobdrops:\s*$",
    ),
    "LICENSE": (),
}

def check(root: Path, pin: str) -> list[str]:
    errors = []
    if not re.fullmatch(r"[0-9a-f]{40}", pin) or pin != EXPECTED_PIN:
        errors.append("MobDrops source pin mismatch")
    if any(path.is_symlink() for path in (root, *root.parents)) or not root.is_dir():
        return errors + ["Invalid or symlinked MobDrops checkout"]
    for relative, patterns in REQUIRED.items():
        target = root
        for component in Path(relative).parts:
            target = target / component
            if target.is_symlink():
                errors.append(f"Symlink in MobDrops source path: {relative}")
                break
        else:
            if not target.is_file():
                errors.append(f"Missing MobDrops source file: {relative}")
                continue
            try:
                data = target.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"Unreadable MobDrops source file: {relative}: {type(exc).__name__}")
                continue
            for pattern in patterns:
                if re.search(pattern, data) is None:
                    errors.append(f"MobDrops source changed: {relative}: {pattern}")
    return errors

def verify_checkout_head(root: Path, pin: str) -> list[str]:
    """Verify the checkout itself, not just the caller-supplied --pin string."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", "HEAD"],
            check=True, capture_output=True, text=True, timeout=10,
        )
        top = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ["Cannot verify MobDrops checkout Git HEAD"]
    if Path(top.stdout.strip()).absolute() != root.absolute():
        return ["MobDrops checkout must be a Git repository root"]
    if result.stdout.strip().lower() != pin:
        return ["MobDrops checkout Git HEAD does not match pinned source"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--pin", required=True)
    args = parser.parse_args()
    errors = check(args.checkout, args.pin)
    if not errors:
        errors.extend(verify_checkout_head(args.checkout, args.pin))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("MobDrops pinned source preflight passed; runtime adapter still required")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
