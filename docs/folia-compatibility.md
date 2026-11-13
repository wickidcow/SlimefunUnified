# Paper, Purpur, and Folia qualification gates

**Release goal:** one source-pinned, individually credited Unified plugin JAR that works correctly on **Paper, Purpur, and Folia**, including the core and every eligible integrated addon. Folia compatibility is mandatory, not optional.

## Current status: unqualified experimental prototype

The pinned Legacy core declares `folia-supported: true`, but that cannot certify the combined runtime. The Unified overlay changes this to `folia-supported: false` by default in experimental builds so an unvalidated combined JAR does not advertise Folia support.

To create a **disposable Folia evaluation JAR**, explicitly run:

```bash
UNIFIED_FOLIA_EXPERIMENTAL=1 bash scripts/assemble_unified.sh
```

This only sets the loader declaration for isolated backed-up Folia testing. **It is not a proof of compatibility and must not be used in production.** The final JAR verifier checks whether the declaration matches the selected mode.

The source-pinned qualification ledger at `integration/platform-qualification.json` records the core and every currently compiled addon, with per-platform and per-version status. `UNTESTED`, `BLOCKED` (unavailable build or environment), or `FAILED` are not compatibility claims. `PASSED` requires linked, dated live-test evidence.

## Scheduler ownership and shared-state audit

- **Region scheduler:** Machines, blocks, cargo, chunk operations, persistent block data and world changes must execute in their owning region. Do not touch another region directly, even when accessing nearby storage.
- **Entity scheduler:** Player/mob inventories, GUI effects, custom drops and teleport-related changes must follow the entity, including when it moves between regions.
- **Global scheduler:** Use only for global ownership, never as a workaround to access region-owned blocks or entities. **Async scheduler:** Use for independent I/O/computation; marshal results back to the correct region/entity scheduler before Bukkit access.
- **Concurrency:** Audit shared addon caches, registries, mutable config, inventories, storage transactions and shutdown/save order for lost updates, races, deadlocks, and duplication. A concurrent collection by itself does not establish ownership correctness.
- **Policy preservation:** Independent OP-controlled Guide visibility and ordinary-player manual crafting restrictions must not unload modules or interfere with existing machines, items, data, or automation.

## Required live validation before stable release

1. Build from exact source pins, verify one plugin descriptor, source receipts, original copyright/license notices and the owner-excluded MagicExpansion absence. Keep the distinct Magic8Ball addon eligible.
2. Boot, disable, restart and restore on actual matching Paper, Purpur, and Folia 1.21.11 / 26.3+ server builds where available. Record the exact build, Java version and plugin dependencies; mark an unavailable target `BLOCKED`, not `PASSED`.
3. For the core **and each integrated addon**, test command and listener registration; ordinary-player and OP Guide/crafting behavior; entity drops; machine and cargo outputs; original IDs/PDC keys; historical configuration paths; saved-world and item round-trips; and backed-up rollback.
4. Exercise multiple distant active Folia regions concurrently, including storage/cargo, machine ticking, entity movement, GUI interactions, chunk unload, cancellations and restart. Inspect region-thread exceptions, deadlocks, item-count conservation and duplication.
5. Retest on Purpur including nondefault gameplay settings, and compare scheduler/performance behavior against Paper. Record reproducible evidence separately for each ledger cell.

**Never set `stable_ready` until every mandatory module/platform target has evidence-backed success and world persistence/anti-duplication evidence is recorded.** Java compilation and CI tests are not gameplay qualification.

References: [PaperMC Folia support](https://docs.papermc.io/paper/dev/folia-support/) and [Folia region concurrency](https://github.com/PaperMC/Folia/blob/ver/26.3.x/README.md).
