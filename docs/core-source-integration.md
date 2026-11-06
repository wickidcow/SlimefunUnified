# Slimefun Legacy source integration

This repository stays **independent**. It builds from a precise public `wickidcow/Slimefun-Legacy` source revision instead of rewriting or pushing changes into its `master` branch.

- The trusted source commit is recorded in `upstream/legacy-core.sha`. Never use an unpinned branch in an executable build.
- `scripts/assemble_unified.sh` checks out that revision into a disposable build directory, copies Unified-owned Java policy classes, applies strictly anchored Unified-only source overlays, and invokes **the upstream Gradle wrapper** with Java 25.
- The resulting JAR is **one plugin** with the upstream Slimefun internal/plugin name retained for data and addon API compatibility; its release-file name is different. This **prototype only includes the Slimefun core**, NOT the maintained addons yet.
- The overlay does **not** modify the source Slimefun Legacy repository or any maintained addon repository.
- GPLv3 was adopted in this project because Slimefun Legacy and selected addons contain GPLv3-covered code; license headers, contributors and original history remain attributed. Every future addon, asset and dependency requires its own compatibility review.
- An independent CI lane compiles the exact pinned core. This compilation by itself does **not** prove server boot, persistent-world compatibility, item access coverage or safety of a real deployment.

## Current prototype capabilities

- Owner-only shortcut in the classic Guide **Settings & Info** screen, in slot 49 (an otherwise empty slot in the maintained Legacy edition).
- Per-module Guide visibility and player-manual-crafting controls stored in `plugins/Slimefun/UnifiedModules.yml`. The only bundled module currently supported by the server UI is **Slimefun Core**. Addon candidates appear as future modules and cannot be toggled as though present.
- All items remain registered, machines persist and OPs bypass player-only restrictions.
- Native guide category lists, item pages, search and direct item details have initial filtering. Native multiblock, altar and crafting-table output events have initial player-only crafting denial.
- No automatic crafter listener: the policy does not block automation by design.

## Known gaps, blocking any production release

- **JEG and all addon code are not integrated yet**, so a maintained JEG Guide, FlexItemGroup implementations and third-party/inventory UI paths may bypass these initial filters.
- Addon-specific custom machine/manual crafting listeners, anvils, production interfaces and guide integrations require auditing one by one. Do not claim player craft prevention is comprehensive.
- Individual item policy is supported by the underlying engine and YAML schema but doesn't yet have the final owner UI browser.
- No real-world upgrade/rollback, world persistence, anti-dupe or full Paper/Purpur/Folia/Leaf validation.
- The server JAR is a **development artifact only**; do not publish a stable release or install on a production world.

## Using this branch

```bash
# Java 25 and network access to the public source/Maven dependencies required
bash scripts/test.sh
bash scripts/assemble_unified.sh
```

Check `.github/workflows/unified-core-prototype.yml` for CI validation and experimental artifact handling.
