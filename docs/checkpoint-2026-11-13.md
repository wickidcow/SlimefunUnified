# Unified integration checkpoint — 2026-11-13 UTC

This checkpoint is a **documentation-only, non-release audit** of the current main-branch README, AGENTS.md, roadmap, credits and exact core pin. It does not assert that source imports or runtime tests passed.

## Scope and accounting

- Historical roster: **44** source entries.
- Explicit owner exclusion: **SF_MagicExpansion / MagicExpansion**, status **excluded-by-owner**. Never import its source, classes, assets, registration or feature implementation. This is not a pending or completed module.
- Eligible target: **43**.
- Source-pinned experimental prototype modules reported by the current roadmap: **3** — ExtraHeads, SoulJars, SlimyTreeTaps. Their runtime validation is outstanding.
- Remaining eligible candidates not yet reported integrated: **40**. Licensing and technical gates may further block individual candidates; do not silently reduce the historical roster.
- Distinct candidates such as Magic8Ball are **not** excluded by the MagicExpansion instruction.

## Provenance and audit evidence

- Core exact pin: `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8` from `upstream/legacy-core.sha`.
- See `docs/credits-and-licenses.md` for currently reviewed attribution and license provenance. MobDrops is **audit-only**, pinned at `8943594f006a443ce8a77113f76709c871d03697`; **not integrated**.
- Verify the complete 44-row historical source manifest, exact addon pins, headers, license files, transitive dependencies and binary resource notices before the next source import. This checkpoint is not a substitute for that per-module manifest.
- Standalone Slimefun Legacy and SF_* repositories are strictly read-only upstreams for Unified.

## Next development gate

1. Inspect the full source inventory and current CI; select one non-excluded, license-cleared, source-pinned addon candidate. MobDrops needs lifecycle/configuration/command/listener facade and bStats audit before any import.
2. Implement a fail-closed source overlay with original namespaces, item IDs, configuration, authorship and persistence intact; detect duplicate standalone plugin installation.
3. Run policy tests, full Java 25 compilation, JAR-content and license verification and PR-head CI. Record exact workflow URLs and results; do not infer CI success from documentation changes.
4. Validate Paper and Purpur 1.21.11 and 26.3+ server boot/restart/world round-trips, anti-dupe and scheduler safety, plus matching Folia targets where available, before claiming production compatibility.

**Release state:** experimental only; compile success is not gameplay certification. No stable release authorized.
