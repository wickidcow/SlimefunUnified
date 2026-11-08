# SlimyTreeTaps — third embedded addon candidate

Source: `wickidcow/SF_SlimyTreeTaps` pinned to `ac1680260503ae7ba8070797069923f983d080c6` (the historical r153 Slimefun Legacy distribution matrix revision).

**Original author:** TheBusyBiscuit and contributors. Modern maintenance: wickidcow. The original MIT copyright and permission notice (© 2019 TheBusyBiscuit) is preserved at `unified/addons/slimytreetaps/COPYING-MIT` in the experimental JAR; maintained GPLv3 modifications remain subject to the new project's GPLv3 license. No change is made to SF_SlimyTreeTaps or Slimefun Legacy upstream.

## Source integration

All eight original Java classes are copied from the exact source commit to the disposable Unified build checkout; the single standalone `TreeTaps` JavaPlugin entry point is replaced by a Unified-only `SlimefunAddon` facade. It uses the single core Slimefun JavaPlugin as its Bukkit event owner. It is **not a nested JAR** and retains separate module credits, item-registration identity, and owner Guide/crafting settings.

Historical keys are explicitly preserved by using original namespace `slimytreetaps` for `tree_taps`, `tree_tap`, `rubber_factory`, `rubber_automation`, `amber`, `magical_mirror`, and persistent key `mirror_location`. The original config location `plugins/SlimyTreeTaps/config.yml` is reused; exact pinned defaults are copied **only when absent**. Existing items, machines, research and bound magical mirrors must not be unregistered or overwritten by owner Guide/crafting switches.

The prototype attempts duplicate-standalone-addon detection and skips in-JAR item registration if an installed `SlimyTreeTaps` plugin is already present. The present policy engine uses the separate `SlimefunAddon` facade to resolve module provenance, despite a single JavaPlugin bootstrap.

## Safety/compatibility blockers

Successful CI compilation and ZIP/class provenance verification are **not** runtime verification. Before any stable release: test previous world state, existing bound mirrors' PDC locations, tree taps, vanilla resin forms, resin extractors/factories, recipe and research IDs, login/teleport, world unload, normal and OP Guide paths, allowed/denied player crafts, old config preservation, standalone module co-install behavior and interaction with other addons. Test Paper/Purpur 1.21.11 and 26.3+, dupes, downgrade/restart and regional scheduler safety. No production-world deployment is approved.

MagicExpansion remains explicitly excluded and its original code is never imported as part of this module.
