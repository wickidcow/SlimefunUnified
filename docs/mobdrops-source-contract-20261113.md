# MobDrops source-pinned plugin contract — 2026-11-13

Status: **AUDITED PARTIALLY; NOT IMPORTED**. This document does not change the 3/43 integration count or certify runtime behavior.

## Immutable upstream evidence

- Repository: https://github.com/wickidcow/SF_MobDrops
- Source commit: `8943594f006a443ce8a77113f76709c871d03697`
- `src/main/resources/plugin.yml` at that commit declares `name: SFMobDrops`, `main: dev.walshy.sfmobdrops.SfMobDrops`, `depend: [Slimefun]`, `author: WalshyDev`.
- Commands: `mobdrops` with aliases `sfmobdrops`, `mobdrop`, `sfmd`; permission `sfmobdrops.admin` (default OP).
- README documents config reload, list GUI, global and entity-specific item drops, chance/amount, custom-name and PDC/tag filters, and backward-compatible single-drop definitions.
- Source is identified as MIT licensed with © 2020 Daniel Walsh; retain the **verbatim** pinned LICENSE and source headers, not a reconstructed notice. Review third-party dependencies/assets separately.

## Fail-closed integration gates

1. Fetch and verify the exact commit and MIT LICENSE, build descriptor, Java sources, default config, command/listener registrations and all dependency declarations. No floating refs.
2. Map the existing JavaPlugin lifecycle to a distinct SlimefunAddon facade. Preserve the historical `plugins/SFMobDrops/` data/config location, reload semantics and default command aliases/permission; do not silently replace the configuration format.
3. Ensure the Unified plugin registers commands/listeners exactly once and rejects a concurrently installed standalone SFMobDrops JAR before duplicate handlers or drops can occur. Audit bStats: do not duplicate metrics services or accidentally shade incompatible classes.
4. Ensure the mob death event executes on the entity's owning region on Folia. No unsafe global mutable configuration or cross-region world/inventory access. Reload must publish a complete immutable validated snapshot; never expose partially parsed drops to concurrent events.
5. Verify each eligible mob death rolls each configured drop only once, preserves item metadata/amounts, and handles invalid IDs, chance, amount, custom names, PDC/tag filters, and multiple matching rules without unintended duplication.
6. Ensure **Guide visibility** and **ordinary-player manual crafting** flags remain independent. Neither may suppress MobDrops' existing automated mob-death drops or remove item registrations. Preserve OP bypass.
7. Test configuration and existing item/world state across stop/restart, upgrade and rollback on disposable Paper/Purpur 1.21.11 and 26.3+; perform Folia entity/region safety and concurrency tests where matching builds are available.
8. Verify exact JAR class/resource inventory, credits, LICENSE, original item IDs/namespaces, duplicate standalone detection, source pin and CI before marking MobDrops experimentally integrated. Compilation alone is insufficient.

## Explicit exclusions and counts

The historical inventory contains 44 source entries, including `SF_MagicExpansion` marked **excluded-by-owner**. Eligible target: **43**. Currently experimentally staged: **3** (ExtraHeads, SoulJars, SlimyTreeTaps). **40 remain**, including MobDrops. MagicExpansion must not be imported, reimplemented, registered, bundled or counted as unfinished; this does not exclude unrelated Magic8Ball.

This audit does not modify any upstream repository and does not authorize stable release.
