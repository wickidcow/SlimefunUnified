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
- **Platform parity is a release requirement:** complete Paper, Purpur, and Folia support for the combined core and every eligible integrated addon. One shared JAR does not make region-threaded code safe. Audit entity/region/global/async scheduler ownership, concurrency, cargo/machine/world saves and restart safety on all three platforms.
- The inherited Legacy `folia-supported: true` flag is NOT evidence for Unified. Normal Unified experimental artifacts must have `folia-supported: false`; the explicit `UNIFIED_FOLIA_EXPERIMENTAL=1` override is restricted to isolated Folia test runs and must never be labeled production compatible.
- A successful compile does NOT prove safe multiplayer usage, data migration, item crafting coverage, Folia safety or production readiness.
- No stable release until Paper, Purpur, and available matching Folia 1.21.11 / 26.3+ targets pass their own boot/restart/world round-trips, anti-dupe and scheduler-safety validation for the combined plugin and each integrated addon. Record unavailable Folia builds explicitly rather than claiming tests passed. Do not re-use Legacy test receipts as Unified release evidence.
- Preserve original author attribution for each module in in-game UI and docs. Addons not yet bundled must not appear toggleable/active.

- **Explicit owner exclusion:** Do NOT import, embed, register, or reimplement `wickidcow/SF_MagicExpansion` (`MagicExpansion`, also referred to as "magic plugin") in SlimefunUnified. Keep its original repository untouched. Mark it `excluded-by-owner` in the 44-row historical source manifest, targeting **43 eligible addons**. Do not count the excluded addon as unfinished, or mistake it for another addon such as Magic8Ball.
