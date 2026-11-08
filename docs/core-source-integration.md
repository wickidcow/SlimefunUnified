# Independent pinned-source integration

SlimefunUnified **never alters** `wickidcow/Slimefun-Legacy` or any maintained addon repositories. It fetches the exact source revisions listed under `upstream/`, copies code to a disposable checkout and applies strictly anchored, explicit Unified-only integration changes.

## Pins

- `upstream/legacy-core.sha`: original maintained Slimefun Legacy Java sources, Gradle wrapper and game assets.
- `upstream/extraheads.sha`: original maintained ExtraHeads addon code and MIT license, imported as the first module.
- `upstream/souljars.sha`: original maintained SoulJars addon code and GPLv3 license, imported as the second module.
- `upstream/slimytreetaps.sha`: original maintained SlimyTreeTaps addon code and original MIT notice, imported as the third source module.

`scripts/assemble_unified.sh` verifies both exact SHAs, copies the addon sources into the same Java compilation as the core and uses the original Gradle wrapper under Java 25. The result is **one server plugin JAR**, not a JAR containing separate plugin JARs.

SoulJars uses an analogous separate `SlimefunAddon` facade, while its soul jar IDs, mob capture behavior, YAML path and historical namespace are preserved. The original GPLv3 notice and source revision are also packaged.

The original main plugin descriptor/name remains `Slimefun` for compatibility. ExtraHeads' original JavaPlugin entrypoint is replaced **only inside Unified** by a SlimefunAddon facade using the shared Slimefun bootstrap, with a retained separate addon identity. Standalone ExtraHeads remains unchanged and is detected to avoid duplicate item registration.

Original ExtraHeads YAML, item IDs and namespace keys are retained. Source pin and original MIT notice are packed in `unified/addons/extraheads/`. The license and core source pin are also packed. Original author: TheBusyBiscuit; community maintenance by ybw0014 and others. See [ExtraHeads details](first-addon-extraheads.md).

## What works in source / is still unproven

- OP-only classic Guide management screen, per-addon visibility and player-crafting flags, atomic policy YAML.
- First classic Guide filters and three manual crafting event paths.
- Distinct addon registration without requiring another Bukkit JavaPlugin classloader.

**Still unproven on a real server:** JEG/flexible categories, all custom crafting, player drops, old ExtraHeads config and item world round trips, plugin collision detection under real loading order, and runtime safety on Paper/Purpur 1.21.11 and 26.3+. The CI compiler cannot certify those.

No stable release until gameplay tests and source/attribution audit gates pass.
