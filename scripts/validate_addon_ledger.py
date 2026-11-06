#!/usr/bin/env python3
"""No network: confirm complete, self-consistent 44-addon import provenance."""
from pathlib import Path
import json
data=json.loads((Path(__file__).resolve().parents[1]/"integration"/"addons.json").read_text())
rows=data["addons"]
assert data["scope"]["standalone_repos_read_only"] is True
assert data["scope"]["addons_target_count"]==44
assert len(rows)==44
assert len({x["slug"] for x in rows})==44
assert len({x["repository"] for x in rows})==44
statuses={"pending", "integration-in-progress", "integrated-compile-verified", "runtime-verified", "blocked"}
assert all(x["status"] in statuses for x in rows)
for x in rows:
    assert x["repository"].startswith("wickidcow/"), x
    assert len(x["baseline_source_sha"])==40 and all(c in "0123456789abcdef" for c in x["baseline_source_sha"])
    if x["status"] in {"integrated-compile-verified","runtime-verified"}:
        assert x["integrated_source_sha"] and len(x["integrated_source_sha"])==40, x
        assert x["license_review"]!="pending",x
    else:
        assert x["integrated_source_sha"] is None, x
    if x["status"]=="runtime-verified":
        assert x["runtime_validation"]=="verified", x
included=sum(x["status"] in {"integrated-compile-verified","runtime-verified"} for x in rows)
print(f"SlimefunUnified addon ledger: {included}/44 source-integrated, {44-included} remaining")
