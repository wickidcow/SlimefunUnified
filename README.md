# SlimefunUnified

**An experimental single-JAR edition of Slimefun Legacy, with independently configurable addon modules.**

This project is separate from [Slimefun Legacy](https://github.com/wickidcow/Slimefun-Legacy). Existing Slimefun Legacy and SF_* addon repositories remain available and continue their established development and release workflows.

## Intended design

One future SlimefunUnified.jar contains the Slimefun core and integrated addon code as *distinct modules*. **All integrated modules remain loaded and preserve their items, machines and data.** An addon set to "off for players" is *not* unloaded: only its discoverability in the Guide and/or ordinary-player crafting are restricted.

The former **Coming Soon** button in the Slimefun Guide should become an **OP-only Server Management** entry, with equivalent integration in the maintained JustEnoughGuide implementation.

Within it, owners can configure each addon independently:

- **Show in player Guide:** yes/no (all registered items remain visible to OPs)
- **Allow player crafting:** yes/no (OP crafting remains allowed)
- **Item-specific exceptions:** hide individual items from the player Guide or block their player-initiated crafting
- **Creators and licenses:** original authorship, original and maintained repository links, licensing notices
- **Optional presets:** one click to hide from ordinary players *and* block player crafting, without modifying machine operation

Owner changes are intended to be persistent. Future production code must ensure filter coverage of Guide categories, search, recipe usages, bookmarks and other discovery paths; *existing items in the world are never removed*. This is a **player access and visibility policy**, not a guarantee that players can never learn an item's ID or acquire an existing item.

Automatic machine crafting, inventory transactions, storage, item drops and existing machines are **not disabled** by these player crafting controls.

## Current state

**Foundation only. NOT an installable Minecraft plugin.** This repository does not yet embed the Slimefun core, contain migrated addon code, render a Guide button or produce a Paper/Purpur server JAR.

The initial pure-Java prototype includes a strict module/item policy parser, an evaluation engine, a candidate addon catalog and executable self-tests. It intentionally has no Bukkit dependencies until we implement integration safely.

To test on Java 21 or later:

    bash scripts/test.sh

See [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), and [credits & license review](docs/credits-and-licenses.md).
