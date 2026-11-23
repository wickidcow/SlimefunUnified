# Unified integration checkpoint — 2026-11-21

This is an **experimental planning checkpoint**, not a runtime integration or certification receipt. It records the status observed from the GitHub connector at the main head `5d819b3b8710dbf8f33b6a33044fd8d74371bc26` (2026-11-18).

## Inventory invariant

- Historical roster: **44** addon sources.
- **43 eligible** candidates, subject to licensing and technical review.
- **1 excluded-by-owner**: `wickidcow/SF_MagicExpansion` / MagicExpansion (the "magic plugin"). **Never** copy its source, classes, assets, module registration or feature implementation into Unified. Excluded is neither completed nor outstanding. Magic8Ball is distinct and remains eligible.
- **3 experimental source-integrated prototypes**: ExtraHeads, SoulJars, SlimyTreeTaps. **40 eligible candidates remain**. These three are not production-certified.
- Do not increment the integrated count for audits, test fixtures, snapshots or docs.

## Source provenance and next gate

| Source | Exact pin / status | Gate |
| --- | --- | --- |
| Slimefun Legacy core | `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8` | Pinned experimental core; preserve upstream read-only |
| MobDrops | `8943594f006a443ce8a77113f76709c871d03697` | Audit only; NOT integrated |
| SF_MagicExpansion | excluded-by-owner | Never import or implement |

MobDrops: preserve Daniel Walsh's original 2020 MIT notice verbatim; audit shaded/transitive bStats licensing and duplicate metrics registration; preserve original command aliases, permissions, config defaults and paths; integrate listener enable/disable lifecycle, safe reload snapshots, drop identity and anti-duplication tests. [Draft PR #56](https://github.com/wickidcow/SlimefunUnified/pull/56) is an audit, not executable integration.

## Policy and safety invariants

Guide visibility and ordinary-player manual crafting are **independent OP-controlled toggles**. All integrated modules remain registered and loaded; machine automation, existing items, inventories, drops and world persistence are unaffected. OP bypass is retained. Preserve original item IDs, namespaces, PDC, configuration paths, credits, source headers, licenses and modification notices.

Before declaring any stable compatibility, require actual Paper and Purpur 1.21.11 and 26.3+ server boot/restart/world-data round trips, anti-dupe and scheduler ownership checks; require corresponding Folia tests on available matching builds. A successful compile or experimental JAR assembly is not gameplay validation. No stable release is authorized.

## Execution receipt

At this checkpoint main was `5d819b3`; open [draft PR #56](https://github.com/wickidcow/SlimefunUnified/pull/56) was observed. No new CI verdict or executable MobDrops import was established. The historical 44-row per-module manifest still requires a separate full-row verification; do not fabricate missing names or licenses. All Legacy and standalone SF_* repositories remain read-only.
