# MobDrops integration checkpoint (experimental; not bundled)

Source: [wickidcow/SF_MobDrops](https://github.com/wickidcow/SF_MobDrops), pinned at `8943594f006a443ce8a77113f76709c871d03697` (`upstream/mobdrops.sha`). Original author: Daniel Walsh / WalshyDev. License: MIT; retain the complete original LICENSE and headers in the assembled JAR. Status: **source audited, runtime NOT imported, NOT registered, NOT counted integrated**.

## Source-derived runtime dependencies and compatibility blockers

| Pinned source | Current behavior | Unified adapter requirement |
| --- | --- | --- |
| `SfMobDrops.java` | Extends `JavaPlugin`, owns static singleton, invokes `saveDefaultConfig`, `new Metrics(this, 11950)`, registers two listeners and command, disables plugin on missing command | Do not construct/enable a second `JavaPlugin` or register a second bStats instance. Use a module lifecycle owned by Unified, with a single listener registration and explicit disable cleanup. |
| `Config.java` | Reads `instance.getConfig().getList("drops")`, logs through plugin, supports legacy single-drop entries | Preserve historical `plugins/SFMobDrops/config.yml` if present and its complete schema, including `drops`, `settings`, `entity`, `name`, `nbtTag`, `slimefunItem`, `chance`, `amount`. Do not redirect into core Slimefun config or overwrite existing data. |
| `MobDropsCommand.java` | Uses `SfMobDrops.getInstance()`; registers `/mobdrops` with aliases `sfmobdrops`, `mobdrop`, `sfmd`, permission `sfmobdrops.admin` | Route command and tab completion through Unified plugin.yml and a module service; retain aliases, permission and reload/list behavior. |
| `Guis.java` | Static GUI accesses singleton; listens to inventory clicks | Inject module service or equivalent without a second plugin instance. Ensure listener registration once and avoid cancelling unrelated inventories. |
| `SfMobDrops.onMobDeath` | Appends Slimefun item clones to `EntityDeathEvent#getDrops()` | Preserve item IDs, configured chance and amount, world-disabled item checks. Prevent duplicate listeners when standalone SFMobDrops is installed; reject/disable module safely rather than doubling drops. |

## Required implementation order

1. Add source-pinned import and explicit source/license/asset collision checks. Keep `SF_MagicExpansion` excluded-by-owner; it is not a dependency of MobDrops.
2. Replace the plugin singleton/lifecycle with a module service without changing the original drop-selection algorithm. Preserve existing historical config before writing defaults; test old single-drop and new nested `drops` formats.
3. Register `/mobdrops` and aliases, permission and listener exactly once through the Unified plugin, with restart-safe teardown. Ensure standalone addon detection prevents duplicate death drops.
4. Maintain separate OP-controlled Guide visibility and manual player crafting policies. Neither policy may disable MobDrops death-drop processing, existing items or automation.
5. Test compile and artifact contents, then Paper/Purpur 1.21.11 and 26.3+ boot, restart, world persistence, command/reload, named/PDC-filtered drops, duplicate-install protection, anti-dupe and scheduler safety. **No gameplay validation or production compatibility is claimed before these tests.**

## Inventory and gate checkpoint

Historical roster: 44. Owner-excluded `SF_MagicExpansion`: 1 (neither integrated nor outstanding). Eligible: 43. Experimentally source-integrated: 3 (ExtraHeads, SoulJars, SlimyTreeTaps). Remaining eligible: 40, **including MobDrops**. Magic8Ball is a distinct eligible addon.

This document is a source-derived integration contract, **not an implementation or a passed test**. No upstream repository modifications are authorized.
