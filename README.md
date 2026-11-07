# SlimefunUnified

**Experimental single-JAR Slimefun edition built independently from [Slimefun Legacy](https://github.com/wickidcow/Slimefun-Legacy).**

Slimefun Legacy remains actively developed in its own repository. This project **reads pinned source commits** and applies Unified-specific overlays in disposable build workspaces. It never pushes to or changes Legacy or the standalone addon repositories.

## Goal: one JAR, individually credited modules

One `SlimefunUnified.jar` will eventually contain Slimefun and the maintained addon modules. **All bundled code stays loaded and functional.** Server owners can separately hide an addon's items from regular players in the Guide and deny non-OPs manual crafting. OPs retain access; existing machines, inventories, storage, drops and automation are unaffected.

The OP-only **Server Management** screen appears in the classic Slimefun Guide's Settings & Info menu. Each addon retains its name, credits and separate original/maintained source links. The maintained JustEnoughGuide UI requires later integration.

**Scope exception:** Per the server owner's request, **MagicExpansion (`SF_MagicExpansion`) will not be bundled**. The historical addon matrix has 44 entries, but Unified's eligible target is **43**. All other eligible addon candidates remain in scope.

## Current experimental content

| Component | Status |
| --- | --- |
| Slimefun Legacy core | Source-pinned, bundled into one JAR |
| ExtraHeads | Source-pinned integrated addon prototype (MIT, original credits retained) |
| SoulJars | **Second source-pinned integrated addon prototype** (GPLv3, original credits retained) |
| FluffyMachines, InfinityExpansion2, Networks, Supreme, JEG and other addons | Not yet integrated; listed as unavailable candidates |

- Java access policy engine with module and individual-item flags and executable self-tests.
- Slimefun classic Guide OP Settings entry and source-pinned source overlays.
- Atomic `plugins/Slimefun/UnifiedModules.yml` with independent Guide-visible / player-crafting toggles and OP bypass.
- Initial classic Guide item list, search, detail filtering and manual crafting interceptors for multiblock, altar and workbench event paths.
- ExtraHeads historical item IDs, mob textures, `extraheads` namespace and prior `plugins/ExtraHeads/config.yml` preserved through a single-plugin facade; separate standalone ExtraHeads JAR detection.
- SoulJars original soul-collection and spawner recipes, `souljars` recipe/category namespaces, historical config path and preexisting entity item-ID aliases preserved by a separate addon facade.
- GPLv3 for Unified source and original MIT copyright/license notice carried inside the JAR for ExtraHeads.

## Major limitations

**This is a prototype, NOT production-ready.** Live Minecraft server start, saved-world migration/rollback, drops/crafting permissions and anti-duplication still need validation. ExtraHeads and SoulJars are the first addon sources integrated, and JEG, custom Flex item categories and other addon-specific crafting/guide pathways have not been audited. Hidden item discovery through alternative plugins and existing inventories remains possible; this toggle is not an item security boundary.

The plugin retains the internal Bukkit name `Slimefun` for legacy compatibility. Never install it next to the original Slimefun Legacy plugin. Only test it on a **backed-up, disposable server copy**.

## Building / testing

```bash
# Pure Java policy tests: Java 21+
bash scripts/test.sh

# Single JAR from pinned core and addon source: Java 25 / Gradle / network required
bash scripts/assemble_unified.sh
```

CI uploads a time-limited **experimental artifact only after compilation and validation**; no stable release is authorized without live safety evidence. See [pinned source integration](docs/core-source-integration.md), [first addon](docs/first-addon-extraheads.md), [roadmap](docs/roadmap.md), [creator credits](docs/credits-and-licenses.md).

This community project is not an official Minecraft/Slimefun release and is not approved or affiliated with Mojang or Microsoft.
