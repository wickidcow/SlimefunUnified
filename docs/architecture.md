# Architecture: one JAR, discrete modules, player-access policies

## What addon OFF means

**An addon is always loaded if built into the Unified distribution.** Module toggle OFF for players *only* hides its content from the ordinary-player Slimefun Guide and/or denies ordinary-player crafting. An OP can still see, obtain and craft its items. Machines, automatic crafting, storage, item identity, existing inventories, world blocks and reward systems continue functioning.

There are two **independent** controls, with a combined "Hide from players" preset:
1. Guide-visible: when false, hide registered module/items from player item groups, searching, discovery, recipes, usages, bookmarks/favorites, guide previews, and relevant JEG surfaces.
2. Player-crafting: when false, block player-initiated crafting of module/items from all audited Slimefun manual crafting paths. Do not block automation or OP crafting.

If a module denies guide visibility/crafting, an item-level ALLOW does not bypass the parent module denial. Otherwise item-specific rules can restrict particular item IDs. OP bypass is evaluated at each access, never inferred from whether a menu was once opened.

## OP Guide flow (future)

    Slimefun Guide -> former Coming Soon slot -> Server Management [OP ONLY]
        Addon Visibility: [FluffyMachines SHOW/HIDE] [IE2 SHOW/HIDE] ...
        Addon Player Crafting: [FluffyMachines ON/OFF] ...
        Individual Item Rules: [look up by registered item ID]
        Creator Credits & Licenses
        Confirm / Save / Audit Log

All changes must persist and report success or failure; authorization must be checked at rendering, click, crafting enforcement and command boundaries.

## Implementation boundary

One Paper plugin bootstrap, with integrated modules registering their own Slimefun categories and items through shared services. **Not** a nested plugin-loader, multi-plugin JAR or hot-unloader. Keep names, provenance, item namespaces, persistent keys and recipe behavior unchanged.

The prototype in src/main/java is deliberately standalone Java 21. It tests access policy only; it does not enforce player craft events or the Bukkit/Slimefun Guide API yet. Integration will add a single registration/ownership index, hooks across Guide and JEG entry points, and recipe-type-specific player-crafting checks. Server owners should be able to use both functions without loss of data.

## Compatibility safeguards

- "Hidden" does not remove a registered SlimefunItem, recipes, references or serialized block metadata.
- Servers upgrading existing worlds retain all addon data; rollback and migration must be tested.
- Standalone addons remain maintained independently, but the unified distribution must prevent colliding standalone JARs from double-registering items.
- Give creator credit in UI and repository, and preserve copyright/attribution/licenses in source and packaged distribution.
