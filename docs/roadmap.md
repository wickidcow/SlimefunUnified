# Roadmap

## Phase 0 — completed
- [x] Separate SlimefunUnified GitHub repository and independent development policy.
- [x] Two independent owner-facing rules: hide in player Guide; deny ordinary-player manual crafting.
- [x] Pure Java module/item policy engine, tests and GPLv3 license alignment.

## Phase 1 — source-pinned core & classic Guide prototype
- [x] Exact-source Slimefun Legacy core build, reproducible provenance.
- [x] First OP-only classic Guide Server Management menu.
- [x] Persistent YAML flags, atomic save, owner bypass, initial Guide and crafting hooks.
- [x] Core-only prototype compiled and JAR entries verified.
- [ ] Comprehensive Guide/JEG, Flex groups, bookmarks, usages, crafting-path controls.
- [ ] Item-by-item owner menu, confirmations and audit logs.
- [ ] Live server smoke tests, old data round-trips and anti-duplication.

## Phase 2 — individually credited embedded addons
- [x] Identify compact MIT-licensed ExtraHeads as first proof-of-concept.
- [x] Source-pin ExtraHeads; implement shared JavaPlugin / distinct SlimefunAddon adapter.
- [x] Verify exact-source core+ExtraHeads compilation, JAR contents, original MIT notice and Java policy tests (CI only).
- [ ] Test old ExtraHeads config, item namespace, head drops and existing world upgrade/rollback.
- [ ] Verify external standalone plugin collision handling and multi-world/region safety.
- [x] Compile second addon SoulJars from exact source while retaining historical jar IDs and separate creator/license records (prototype only).
- [x] Integrate SlimyTreeTaps source-pinned module prototype, preserving original MIT notice and historical namespaces (compile-only, requires passing PR-head CI).
- [ ] Integrate additional maintainable modules one by one with license and data audits.
- [ ] Finish JEG integration and shared runtime/performance services before publishing stable binaries.

## Phase 3 — release quality
- [ ] Real Paper/Purpur 1.21.11 and 26.3+ server startup/restart tests with existing data.
- [ ] Storage conservation, duplication prevention, old-item compatibility.
- [ ] Same-factory TPS A/B comparison vs independent addons.
- [ ] Folia/Leaf region safety and verified one-JAR reproducibility.

**3/43 eligible addon sources staged for experimental single-JAR compilation (ExtraHeads, SoulJars, SlimyTreeTaps); 40 eligible remain after verification. MagicExpansion remains excluded by owner. NO runtime validation or production-ready release.**
