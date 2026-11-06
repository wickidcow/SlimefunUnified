# Roadmap

## Phase 0: isolated access-policy foundation
- [x] Separate SlimefunUnified GitHub repo, no core/addon changes.
- [x] State target: single JAR, separately credited loaded addons, two independent player-access controls.
- [x] Implement pure-Java parsing, access-policy evaluation and self-tests.
- [ ] Validate the initial CI job on the committed revision.
- [ ] Resolve project license compatibility before importing any GPLv3-only code.

## Phase 1: server and Guide integration
- [ ] Paper bootstrap that emits a single test plugin JAR.
- [ ] Map integrated item IDs to originating modules.
- [ ] OP-only server settings replacing the Guide Coming Soon slot and corresponding JEG integration.
- [ ] Verified permission checks on all UI actions; persistence and audit trail.
- [ ] Player Guide filtering across category, search, bookmarks, recipes, usages and cheat entry points.
- [ ] Player crafting enforcement for every applicable manual Slimefun crafting path and admin bypass.
- [ ] Prove automated machine recipes and preexisting items are unaffected.

## Phase 2: addon source integration
- [ ] License and attribution review per addon, asset and dependency.
- [ ] Begin with one test addon only; preserve its item IDs, machines and gameplay.
- [ ] Expand through individually tested addon modules while preserving maintained standalone repositories.
- [ ] Detect conflict with standalone addon JAR and report safe resolution instructions.

## Phase 3: release quality
- [ ] Two-way world persistence tests on 1.21.11 and 26.3+ Paper/Purpur.
- [ ] Anti-duplication, inventory and storage regressions.
- [ ] Actual same-factory performance A/B comparison versus separate plugins.
- [ ] Folia/Leaf safety checks and reproducible one-JAR release build.

**Current build is NOT a Minecraft plugin.**
