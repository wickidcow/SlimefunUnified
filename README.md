# SlimefunUnified

**Experimental single-JAR Slimefun edition built independently from [Slimefun Legacy](https://github.com/wickidcow/Slimefun-Legacy).**

Slimefun Legacy remains actively developed in its own repository. This project **reads a pinned Legacy source commit** and applies Unified-specific overlays in a disposable build workspace. It never pushes to or changes the Legacy repository. Standalone addon repositories remain separately maintained.

## Target design

One `SlimefunUnified.jar` will eventually include the Slimefun core and multiple separately credited, individually configurable addon modules. **All bundled addon code stays loaded and operational.** An owner can separately hide addon content from regular players in the Guide and deny ordinary players manual crafting. OPs retain Guide and crafting privileges; automatic machines and existing items/storage continue working.

The OP-only **Server Management** menu replaces a previously unused Guide Settings & Info slot. It includes independent Guide and player-crafting flags, project credits and source links. The maintained JustEnoughGuide UI will receive equivalent integration when JEG is bundled.

This is a player UI and manual crafting policy; hiding an item does *not* prevent someone from finding an old item, seeing it in an inventory or learning about it through external plugins.

## What has actually been implemented

- Pure Java policy engine with module and item flags and executable regression self-tests.
- Source-pinned experimental build lane which fetches Legacy at `upstream/legacy-core.sha`, overlays Unified sources and attempts one **core-only** Paper plugin JAR.
- OP-only Server Management entry in the **classic** Guide's Settings & Info screen; candidate modules are listed with credits but cannot be toggled before being integrated.
- Initial filter hooks for classic Guide item pages, search and direct item details; initial manual-crafting denial for native multiblock, altar and workbench event paths.
- Persistent `plugins/Slimefun/UnifiedModules.yml` with atomic saves; owner bypass and fail-closed behavior on malformed policy files.

**Important: No addon code has been integrated yet. JEG, flexible guide categories and custom addon crafting pathways are NOT covered. No real server smoke tests or world migration tests have been completed. The experimental artifact must NOT be installed on a production server.** The plugin keeps the internal name `Slimefun` to preserve historical identity; do not install it beside Slimefun Legacy.

## Building and testing

Java 21+ is sufficient for the standalone access-policy self-test:

```bash
bash scripts/test.sh
```

The experimental pinned-core build requires Java 25, network access and the original Gradle wrapper:

```bash
bash scripts/assemble_unified.sh
```

The GitHub Actions experimental JAR is uploaded as a *prototype* artifact **only if compilation and artifact checks pass**. See [source integration](docs/core-source-integration.md), [roadmap](docs/roadmap.md), and [credits and licenses](docs/credits-and-licenses.md).

## Attribution and licensing

All original creator names and project lineage are preserved. SlimefunUnified is licensed under GPLv3 (see [LICENSE](LICENSE)), and individual source/asset licenses must be reviewed before each addon is imported. Not charging money does not waive obligations to preserve notices and make corresponding source available upon distribution.
