# First bundled addon: ExtraHeads (MIT)

## Exact source and scope

The first non-core integration is the independent [ExtraHeads](https://github.com/wickidcow/SF_ExtraHeads) project, source pin `upstream/extraheads.sha`. This is a *small* initial integration to verify the new single-JAR system. It does not change the standalone ExtraHeads repository.

At build time, the original ExtraHeads Java sources are copied from that immutable revision into a disposable, exact-version Slimefun Legacy source checkout. We replace only the original `JavaPlugin` bootstrap with a Unified `SlimefunAddon` facade and adjust three Bukkit registration/namespace call sites. All item IDs, mob head textures, head chances, original `extraheads:extra_heads` category and `extraheads:decapitation` recipe keys remain unchanged.

Original creator: **TheBusyBiscuit**; later maintenance: **ybw0014 / Slimefun Addon Community**; active compatibility fork: **wickidcow/SF_ExtraHeads**. The source LICENSE is MIT with the original 2019 copyright notice, retained in `unified/addons/extraheads/COPYING-MIT` in the prototype JAR.

## Runtime behavior

- Only one real Bukkit plugin named `Slimefun` loads. No second `ExtraHeads` JavaPlugin or nested JAR is loaded.
- Existing `plugins/ExtraHeads/config.yml` is loaded and saved at its original path to preserve head chances and older setups. If absent, the pinned source's original default YAML is installed.
- Its original head listener, drops, and Sword of Beheading multiplier remain active. Guide/crafting toggles should only change *player* discovery and manual creation, not mob drops or existing items.
- The module registers itself with a **distinct SlimefunAddon facade**, so access rules identify ExtraHeads items even though the underlying JavaPlugin is the single Slimefun bootstrap.
- If a separate standalone ExtraHeads plugin is installed, Unified **skips bundled ExtraHeads registration** and warns, instead of registering duplicate Slimefun IDs. This does not yet cover all future addon coexistence checks.

## Constraints and tests required

The source build and JAR-contents checks are **compiler/artifact evidence only**. We must still validate old-world item identity, old ExtraHeads config round-trips, mob drops, permission and Guide behavior, standalone-plugin collision handling and Paper/Purpur restarts before any stable distribution.

This MIT license is permissive for inclusion in a GPLv3-covered aggregate, provided its original copyright/permission notice remains supplied. Evaluate other addons separately before each import.
