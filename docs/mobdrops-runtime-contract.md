# MobDrops runtime integration checkpoint (2026-11-10)

**Status: pending, NOT compiled, NOT registered, NOT production validated.**
Source: `wickidcow/SF_MobDrops@8943594f006a443ce8a77113f76709c871d03697`.
Original creator: Daniel Walsh (WalshyDev); original MIT copyright/license must be embedded verbatim if imported.
This document is a source audit and implementation contract, not authorization to mark MobDrops integrated.

## Exact-source findings

- `dev.walshy.sfmobdrops.SfMobDrops` extends `JavaPlugin`, implements `Listener`, and stores a static singleton plus a mutable `LinkedHashSet<MobDrop>`.
- `onEnable` calls `saveDefaultConfig`, creates `new Metrics(this, 11950)`, constructs `new Config(this)`, loads drops, registers its own `EntityDeathEvent` listener and `new Guis()` inventory listener, and uses `getCommand("mobdrops")`.
- `MobDropsCommand` uses `SfMobDrops.getInstance().reloadConfig()` and `loadDrops()` for reload; the list GUI uses the singleton's drop set. Both must be adapted together.
- `Config` requires a `JavaPlugin` instance to read `getConfig().getList("drops")` and log warnings. Reusing the Unified core's main config would silently change drop definitions and is forbidden.
- Original plugin metadata defines `/mobdrops` with aliases `sfmobdrops`, `mobdrop`, `sfmd` and OP-default `sfmobdrops.admin`.
- `pom.xml` declares Java 21, Paper API 1.21.11, Slimefun API as provided, and bStats Bukkit 3.2.1 shaded/relocated to `dev.walshy.sfmobdrops.bstats`.
- The death handler selects matching entity type/name/PDC key, rolls each configured chance, resolves `SlimefunItem.getById`, checks world disablement, clones the item, and adds it to `EntityDeathEvent#getDrops()`. Preserve this behavior, including legacy configuration format.

## Required source-pinned implementation gates

1. **Import:** fetch and verify the exact SHA, reject Java/resource collisions and symlinked import paths, copy original Java source and MIT notice into the disposable Unified assembly only. Do not import `plugin.yml` as a second Bukkit plugin descriptor.
2. **Lifecycle:** replace the standalone `JavaPlugin` superclass/singleton assumption with a Unified-owned module facade. Initialize once from Unified enable and unregister/clear on disable; detect separately installed SFMobDrops before registering to avoid duplicate drops.
3. **Configuration:** read/write the historical `plugins/SFMobDrops/config.yml` (verify actual historical data-folder spelling against installed servers) through an isolated YAML facade. Preserve both legacy single-drop and current multi-drop schema. Reload must refresh only this module, never the core config.
4. **Commands:** register the original label, aliases and OP permission with explicit collision detection, preserving console support for reload and player-only list GUI. Avoid relying on `JavaPlugin#getCommand` for a command absent from the one-JAR descriptor.
5. **Listeners:** register exactly one death handler and one GUI click handler, and ensure disable/reload never duplicates either. Preserve original chance, item, world and entity filtering.
6. **Dependencies:** audit bStats 3.2.1's license and transitive classes. Do not start a second metrics instance automatically; decide on a clearly attributed single-plugin metrics strategy before enabling telemetry.
7. **Verification:** require pinned-source compilation, exact JAR class/license/source receipts, manifest consistency and policy regression tests before counting a fourth integrated module. Validate real Paper/Purpur 1.21.11 and 26.3+ boot/restart, config reload, world data, drops, duplicate-plugin detection, inventory GUI and scheduler safety separately.

## Non-negotiable scope

Only `wickidcow/SlimefunUnified` may be modified. Upstream Slimefun Legacy and standalone SF_* sources remain read-only. `wickidcow/SF_MagicExpansion` is **excluded-by-owner**, never imported or counted as pending/completed; Magic8Ball is a distinct eligible addon. The historical inventory remains **44 sources, 43 eligible, 3 compile-verified prototypes, 40 pending** until the actual integration gates pass.

**Checkpoint:** this audit documents specific code changes needed for the next source import; it does not modify runtime behavior, advance the integration count, or constitute CI/gameplay validation.
