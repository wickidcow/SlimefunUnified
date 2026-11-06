# Source-pinned SoulJars prototype module

This is the **second embedded addon source**, following ExtraHeads, in a **single** SlimefunUnified plugin JAR. It is not a nested Jar-in-Jar addon loader.

- Original project: SoulJars by **TheBusyBiscuit**, original contributors and subsequent compatibility maintainers.
- Maintained source: https://github.com/wickidcow/SF_SoulJars
- Source commit: `8fbd6befc477bbbf9970afc79e538c6b1f028cd3` from the r153 Slimefun Legacy addon matrix.
- Source license: GPLv3. Copy of original license in JAR at `unified/addons/souljars/COPYING-GPLv3`.

## Compatibility contract

Original collectible jars, broken-spawner recipes, item IDs, `souljars:soul_jars` category and `souljars:mob_killing` recipe namespace are kept. The config reads/writes the original `plugins/SoulJars/config.yml` location, copying the exact pinned upstream defaults **only if absent**. Owner Guide visibility and player manual-crafting controls are independent; SoulJars remains initialized, and automated crafting and natural mob interactions remain enabled.

To bridge new Paper versions, Unified's **local build-only facade** uses the runtime Bukkit entity key rather than requiring `EntityType` to be an enum. It preserves the historical `MUSHROOM_COW` identifier when newer Paper exposes `MOOSHROOM`. The standalone SoulJars repository remains untouched.

## Validation still required

Compilation / license packaging / class presence are only early gates. Before stable release, test: an existing server's soul jar items (partial and filled), empty jar and BrokenSpawner recipes, collection after mob kills, ancient altar craft and admin bypass, disabled-player Guide/crafting, config read/save, server restart and rollback, modded mob types, version aliases, and interaction with ExtraHeads. Check both Paper/Purpur 1.21.11 and 26.3+ and anti-dupe/inventory conservation.

No release or claim of gameplay verification until those tests are evidenced.
