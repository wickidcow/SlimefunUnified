#!/usr/bin/env python3
"""Keep Unified platform qualification tied to actual integrated, pinned modules."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    "paper-1.21.11", "paper-26.3+",
    "purpur-1.21.11", "purpur-26.3+",
    "folia-1.21.11", "folia-26.3+",
)
STATES = {"UNTESTED", "FAILED", "PASSED", "BLOCKED"}


def verify(matrix, manifest, core_sha):
    if matrix.get("schema_version") != 1 or matrix.get("required_targets") != list(TARGETS):
        raise ValueError("Platform qualification target/schema drift")
    expected = {"legacy-core": core_sha.strip()}
    for addon in manifest["addons"]:
        if addon["status"] == "integrated-compile-verified":
            if not addon["integrated_source_sha"]:
                raise ValueError("Integrated module missing source SHA")
            expected[addon["slug"]] = addon["integrated_source_sha"]
    rows = matrix.get("modules", [])
    if len(rows) != len(expected) or {row["slug"] for row in rows} != set(expected):
        raise ValueError("Qualification ledger must cover core and every compiled addon exactly once")
    for row in rows:
        if row["source_sha"] != expected[row["slug"]]:
            raise ValueError(f"Qualification source pin drift: {row['slug']}")
        checks = row.get("targets", {})
        if set(checks) != set(TARGETS):
            raise ValueError(f"Missing platform/version target: {row['slug']}")
        for target, record in checks.items():
            state = record.get("state")
            links = record.get("evidence", [])
            if state not in STATES or not isinstance(links, list):
                raise ValueError(f"Malformed qualification state: {row['slug']} {target}")
            if state == "PASSED" and not links:
                raise ValueError(f"False passed qualification without evidence: {row['slug']} {target}")
            if state != "PASSED" and links:
                raise ValueError(f"Unverified evidence attached to incomplete target: {row['slug']} {target}")
    if matrix.get("stable_ready"):
        if len(expected) - 1 != manifest.get("scope", {}).get("addons_target_count"):
            raise ValueError("Stable readiness requires every eligible addon to be integrated")
        if any(record["state"] != "PASSED" for row in rows for record in row["targets"].values()):
            raise ValueError("Stable readiness claimed before all required platform gates pass")
        if not matrix.get("world_roundtrip_evidence") or not matrix.get("anti_dupe_evidence"):
            raise ValueError("Stable readiness missing world persistence/anti-dupe evidence")
    if "magicexpansion" in {row["slug"] for row in rows}:
        raise ValueError("Owner-excluded MagicExpansion must never be qualified")


if __name__ == "__main__":
    manifest = json.loads((ROOT / "integration/addons.json").read_text(encoding="utf-8"))
    matrix = json.loads((ROOT / "integration/platform-qualification.json").read_text(encoding="utf-8"))
    verify(matrix, manifest, (ROOT / "upstream/legacy-core.sha").read_text(encoding="utf-8"))
    print("Platform qualification ledger verified (not runtime certification)")
