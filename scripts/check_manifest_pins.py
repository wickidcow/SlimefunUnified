#!/usr/bin/env python3
"""Validate historical addon roster and source-pin invariants without touching upstream."""
import json
import re
import sys
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")
EXCLUDED = "wickidcow/SF_MagicExpansion"
ALLOWED_STATUSES = {"pending", "integrated-compile-verified", "excluded-by-owner"}


def validate(root):
    root = Path(root)
    manifest = json.loads((root / "integration/addons.json").read_text(encoding="utf-8"))
    addons = manifest["addons"]
    scope = manifest["scope"]
    errors = []
    if len(addons) != 44 or scope.get("source_roster_count") != 44:
        errors.append("historical roster must contain exactly 44 entries")
    if scope.get("addons_target_count") != 43:
        errors.append("eligible addon target must be 43")
    if scope.get("excluded_repositories") != [EXCLUDED]:
        errors.append("owner exclusion list must contain only SF_MagicExpansion")
    if scope.get("standalone_repos_read_only") is not True:
        errors.append("upstream repositories must remain read-only")
    repos = [a.get("repository") for a in addons]
    if len(repos) != len(set(repos)):
        errors.append("duplicate addon repositories")
    slugs = [a.get("slug") for a in addons]
    if len(slugs) != len(set(slugs)):
        errors.append("duplicate addon slugs")
    excluded = [a for a in addons if a.get("status") == "excluded-by-owner"]
    if len(excluded) != 1 or excluded[0].get("repository") != EXCLUDED:
        errors.append("exactly MagicExpansion must be excluded-by-owner")
    for addon in addons:
        repo = addon.get("repository", "<missing>")
        baseline = addon.get("baseline_source_sha")
        integrated = addon.get("integrated_source_sha")
        status = addon.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{repo}: unknown integration status {status!r}")
        if not isinstance(baseline, str) or not SHA.fullmatch(baseline):
            errors.append(f"{repo}: invalid baseline SHA")
        if repo == EXCLUDED:
            if status != "excluded-by-owner" or integrated is not None:
                errors.append("MagicExpansion must never have an integrated source SHA")
        elif status == "excluded-by-owner":
            errors.append(f"{repo}: unexpected owner exclusion")
        if status == "pending" and integrated is not None:
            errors.append(f"{repo}: pending module has integrated source")
        if status != "pending" and status != "excluded-by-owner":
            if not isinstance(integrated, str) or not SHA.fullmatch(integrated):
                errors.append(f"{repo}: integrated module missing exact source SHA")
    pins = {"wickidcow/SF_ExtraHeads": "extraheads.sha",
            "wickidcow/SF_SoulJars": "souljars.sha",
            "wickidcow/SF_SlimyTreeTaps": "slimytreetaps.sha"}
    # A manifest entry is not an integration until the one-JAR assembler has a source pin.
    # Reject phantom integrated modules that would inflate progress reporting.
    for addon in addons:
        if addon.get("status") == "integrated-compile-verified" and addon.get("repository") not in pins:
            errors.append(f"{addon.get('repository')}: marked integrated but absent from pinned assembly")
    for repo, filename in pins.items():
        matches = [a for a in addons if a.get("repository") == repo]
        if len(matches) != 1:
            errors.append(f"{repo}: missing from manifest")
            continue
        pin = (root / "upstream" / filename).read_text(encoding="utf-8").strip()
        if not SHA.fullmatch(pin) or matches[0].get("integrated_source_sha") != pin:
            errors.append(f"{repo}: manifest and build source pins disagree")
    core_pin = (root / "upstream/legacy-core.sha").read_text(encoding="utf-8").strip()
    if not SHA.fullmatch(core_pin):
        errors.append("invalid core source pin")
    return errors


if __name__ == "__main__":
    problems = validate(Path(__file__).resolve().parent.parent)
    for problem in problems:
        print("FAIL:", problem, file=sys.stderr)
    if not problems:
        print("PASS: 44 historical / 43 eligible; exclusion and integrated source pins consistent")
    raise SystemExit(bool(problems))
