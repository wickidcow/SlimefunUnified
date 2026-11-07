# SlimefunUnified — 44-addon source roster / 43 eligible integrations

This ledger tracks all **44 addons** in the canonical Slimefun Legacy r153 release matrix. Snapshot source: `wickidcow/Slimefun-Legacy/compatibility/sfl-addon-release-matrix.json` at `726d7449c38a9829872b7585439b9a1c4cd6518e`. The source matrix and original addon repos are **read-only inputs** to this project.

**Current status:** **2/43 eligible addon sources** have been included in compiled Unified prototype JARs (**ExtraHeads** and **SoulJars**); **41 eligible addons remain**. The Slimefun core is also bundled. **MagicExpansion (`wickidcow/SF_MagicExpansion`) is excluded by explicit owner request** and must never be imported into Unified. It remains a historical entry in the 44-addon upstream source roster for provenance only. No actual gameplay validation is claimed.

The machine-readable [integration manifest](../integration/addons.json) records exact baseline upstream commits, implementation status, source pin and review gates for every addon. When importing another addon, update its `status`, source SHA, license review and safety tests. Don't silently mark a module integrated until the class files and single-JAR build have been verified. Distinguish `integrated-compile-verified` from `runtime-verified`.

## Per-module acceptance requirements

1. Verify the repository/commit/headers, all license grants and any non-code assets. Preserve original author credit and required notices.
2. Integrate source into the **Unified repository build only**, never push modifications to Slimefun Legacy or the standalone addon project. Do not embed nested plugin JARs.
3. Preserve Bukkit/Slimefun item IDs, recipes, persistent namespaces, world/config paths, resource keys, gameplay behavior and item output. Implement one core JavaPlugin plus distinct per-addon `SlimefunAddon` identity.
4. Duplicate-addon protection should avoid registering the same historical items twice; owners must be informed of conflicts.
5. Complete OP-only Guide visibility and manual crafting toggle coverage while keeping all module runtime behavior loaded for both players and OPs.
6. Compile/build, assert provenance and license packaging, and test actual Paper/Purpur startup, Guide visibility, manual crafting, items, machines, storage persistence, restart, downgrade safety, anti-duplication and cross-addon dependencies as applicable.
7. Only mark `runtime-verified` with explicit saved-world/gameplay receipts. Keep stable releases gated until full-system validation.

### Progress reporting

The ledger counts exact included addon source, **not** every recognized candidate. Check branch PRs and CI for actual verification. Source pins are historical baseline values from r153 and may be deliberately updated after compatibility review; never silently substitute an unreviewed HEAD.

Pylon, Rebar, BuildingStaff and archived addons are not implicitly in the 44-addon target. Existing standalone repos and the hourly Slimefun Legacy development cycle continue independently.

## Explicit owner exclusion — MagicExpansion

The historical 44-addon source matrix includes `SF_MagicExpansion`, but **SlimefunUnified must exclude it completely**, not merely hide it in the player Guide. Do not copy its source, dependencies/assets as a module, namespaced items, or runtime code into the combined JAR. The manifest's `excluded-by-owner` status and separate 43-addon eligible target are deliberate. This exclusion does not imply exclusion of separately identified addons such as Magic8Ball.
