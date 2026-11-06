# Roadmap

## Phase 0: isolated policy foundation — completed
- [x] Independent SlimefunUnified repository; no changes to Slimefun Legacy or maintained addons.
- [x] Single future JAR, independent creator credits and guide/crafting player-access controls specified.
- [x] Strict pure-Java module/item policy engine with regression self-tests.
- [x] Initial CI policy tests passing.
- [x] Align the new repository license to GPLv3 before core import.

## Phase 1: pinned upstream source and first server hooks — experimental
- [x] Pin Slimefun Legacy source SHA and create deterministic, fail-closed overlay assembly.
- [x] Add an OP-only classic Guide Server Management button and owner menu source.
- [x] Add initial YAML persistence, policy and player-only crafting/Guide source hooks.
- [ ] Confirm pinned-core build CI passes and inspect experimental JAR contents.
- [ ] Complete OP item-specific rule browser and safe confirmation/audit log.
- [ ] Cover all native guide discovery routes and all manual player crafting, including non-event custom workflows.
- [ ] JEG and FlexItemGroup discovery and alternate Guide implementations.
- [ ] Real test server launch and Paper/Purpur persistence/crafting integration tests.

## Phase 2: addon source integration (not yet started)
- [ ] Comprehensive per-addon licensing and creator credit verification.
- [ ] First real addon merged as an internal module without renaming its item IDs or dropping gameplay.
- [ ] Explicit module-to-item ownership registration (one JavaPlugin bootstrap for all).
- [ ] Duplicate standalone JAR detection and safe refusal/warning.
- [ ] Repeat integration and tests across maintained modules, preserving standalone repositories.

## Phase 3: release quality
- [ ] Old-world storage, inventory, BlockStorage, ItemStack and API tests on Paper/Purpur 1.21.11 and 26.3+.
- [ ] Anti-duplication and storage conservation across machine, cargo, Networks and addons.
- [ ] Repeatable same-factory performance A/B comparison.
- [ ] Folia/Leaf region safety and official source-pinned single-JAR release.

**Experimental core prototype is NOT production ready.**
