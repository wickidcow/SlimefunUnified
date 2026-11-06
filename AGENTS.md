# SlimefunUnified development instructions

- Develop **exclusively** in wickidcow/SlimefunUnified. Slimefun Legacy is an independently maintained upstream source input, NOT a destination for Unified source changes.
- Never alter Slimefun Legacy master, addon branches, workflows, release assets, or its hourly development cycle for Unified work.
- Use `upstream/legacy-core.sha` as an exact source pin; build in a disposable checkout with fail-closed anchored overlays, not an unpinned branch.
- Goal: one future plugin JAR with individually named and credited modules. Keep the standalone Slimefun Legacy/addon repositories independent and maintained.
- **Owner toggle = player access policy, never unload.** Hide from the Guide and/or deny manual player crafting, independently. Do not remove item registration, machines, worlds, inventories, storage, saved identities or automation when hidden.
- OP permission `slimefununified.admin` defaults to OP; re-check permissions on each menu click and each manual crafting decision. Existing automatic crafting must not be blocked by the Unified policy.
- Enforce Guide filtering in category listings, search, details, recipe usages, bookmarks and JEG before describing it as complete. Flex groups, third-party guide paths and addon custom crafting need explicit validation.
- Preserve historical addon IDs, PDC keys, world/item data, BlockStorage and sources. Detect duplicate registrations with separately installed addon JARs before bundling them.
- Preserve creators, source headers, upstream links, authorship and modification notices. `LICENSE` has been aligned to GPLv3 for the **new repo**; independently audit each addon and bundled resource/license before adding code. No-money distribution is not an exception.
- A successful compile does NOT prove safe multiplayer usage, data migration, item crafting coverage, Folia safety or production readiness.
- No stable release until Paper/Purpur 1.21.11 and 26.3+, world data round-trips, anti-dupe and scheduler-safety validation is complete. Do not re-use Legacy test receipts as Unified release evidence.
- Preserve original author attribution for each module in in-game UI and docs. Addons not yet bundled must not appear toggleable/active.
