# Unified integration ledger and checkpoint

Updated: 2026-11-06 UTC. This ledger tracks **addon modules**, excluding the Slimefun core. Target distribution: 44 addons; this number is a planning target, **not** an assertion that 44 candidates have passed eligibility review.

## Exact pinned inputs

| Component | Repository | Pinned commit | Status | Outstanding validation |
| --- | --- | --- | --- | --- |
| Slimefun core | wickidcow/Slimefun-Legacy | `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8` | Experimental bundled core | Paper/Purpur 1.21.11 and 26.3+ boot/restart/data and scheduler safety |
| ExtraHeads | wickidcow/SF_ExtraHeads | `b1e8a1f11692b44d359eec863f3be5be0f061516` | Prototype integrated (1/44); MIT notice packaged | Old config and item identities, drop behavior, collision and world round-trip |
| SoulJars | wickidcow/SF_SoulJars | `8fbd6befc477bbbf9970afc79e538c6b1f028cd3` | Prototype integrated (2/44); GPLv3 notice packaged | Old IDs, collection/spawner behavior, world round-trip |

**Remaining: 42/44 not integrated.** Candidate status below is **not** an eligibility determination. Do not count an addon as integrated until source, licensing, runtime and data preservation are audited, source pinned and compiled into the one-JAR artifact.

## Named pending candidates (not bundled)

| Candidate | Maintained source | License evidence | Integration blocker / next step |
| --- | --- | --- | --- |
| FluffyMachines | wickidcow/SF_FluffyMachines | GPLv3 verified at source pin `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f` (`LICENSE.txt`); ExtraUtils GPLv3 license verified at `bf89aee6ae`; bStats and any third-party assets still require audit | Maven build; depends on Slimefun; optional mcMMO/NoCheatPlus; bundled bStats and ExtraUtils `bf89aee6ae`. Audit shaded ExtraUtils, item IDs, machine persistence and barrel formatting before import |
| InfinityExpansion2 | wickidcow/SF_InfinityExpansion2 | GPLv3 listed in credits ledger; independently reverify | Audit storage identity and anti-duplication, dependency graph; pin source |
| Networks Expansion | wickidcow/SF_NetworksExp | GPLv3 listed in credits ledger; independently reverify | Audit item movement and conservation, dependencies; pin source |
| Supreme | wickidcow/SF_Supreme | GPLv3 listed in credits ledger; independently reverify | Audit equipment persistence and dependencies; pin source |
| JustEnoughGuide | wickidcow/SF_JustEnoughGuide | GPLv3 listed in credits ledger; independently reverify | Audit all Guide visibility paths before claiming filtering complete; pin source |

The other **37 pending candidate slots** are not individually inventoried in this ledger. Obtain the authoritative 44-addon distribution list and verify each repository, current maintenance status, exact commit, transitive dependencies, resource rights and compatibility before assigning a module row. Do not infer legal eligibility from a repository name or from noncommercial intent.

## FluffyMachines provenance audit — 2026-11-06 (no import)

- **Source:** `wickidcow/SF_FluffyMachines`, default branch `master`, exact inspected commit `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f`. This is an **audit pin**, not yet a Unified build/source import pin. Original author `NCBPFluffyBear`; lineage includes `SlimefunGuguProject/FluffyMachines` per upstream README.
- **License:** `LICENSE.txt` contains GPL version 3; preserve upstream source headers and author credits, provide corresponding source and modification notices. Independently inspect licenses and notices for all shaded resources, particularly `com.github.Slimefun-Addon-Community:ExtraUtils:bf89aee6ae` and bStats, before distribution.
- **Dependency graph:** `plugin.yml` declares required `Slimefun`, optional `mcMMO` and `NoCheatPlus`; Maven `pom.xml` declares Paper API `1.21.11-R0.1-SNAPSHOT` and Gugu Slimefun4 `2025.1` as provided, JSR305 provided, bStats `3.0.2` and ExtraUtils `bf89aee6ae` as compile dependencies. The original Maven shade configuration relocates bStats and ExtraUtils and minimizes the JAR; direct inclusion without adapting dependencies may silently remove classes or conflict with Unified.
- **Data/runtime hazards:** inspect Dolly/backpack persistence, Fluffy Barrel metadata identity, Loader/Unloader transfers and rollback, machine registration, commands, permissions and config paths. Upstream `VALIDATION.md` describes staging tests but does not establish Unified runtime compatibility; some sections are historical and disagree with current `pom.xml` Java 21 target, so use the pinned source as authority.
- **Decision:** import BLOCKED pending transitive license/resource inspection and a source-pinned adaptation plan. Do not claim a third integrated addon or expose FluffyMachines toggles yet. Next feasible step: implement a fail-closed source provenance/license gate or a targeted Guide/crafting regression test inside Unified.

## ExtraUtils transitive license audit — 2026-11-07 (no import)

- **Dependency source:** `Slimefun-Addon-Community/ExtraUtils` at FluffyMachines' declared dependency revision `bf89aee6ae`; `LICENSE` contains GNU GPL version 3. The dependency's Maven `pom.xml` identifies `dev.j3fftw:ExtraUtils:1.0-SNAPSHOT`, with Spigot API 1.17.1, Slimefun4 RC-27, JSR305 and Lombok marked provided. It does not declare additional bundled runtime libraries in that POM.
- **Scope:** GPLv3 license evidence is sufficient to continue source-level adaptation planning, **not** a complete asset/source-header audit or confirmation of binary redistribution compliance. Preserve license, copyright/source headers, modification notices, corresponding source and build scripts. Inspect individual ExtraUtils source files/resources and FluffyMachines' shaded bStats 3.0.2 notice before importing or distributing adapted classes.
- **Compatibility:** The dependency targets older Spigot/Slimefun APIs; FluffyMachines shades and relocates it. Do not assume the old dependency can be copied into Unified unchanged. Audit referenced classes and minimize duplicate classes without altering behavior or persistent IDs.
- **Checkpoint:** Unified main `2fecc91c3ba9be3d54ae7d39dd2426d313a2c6a6`, `AGENTS.md`, open PRs (none), and the three core/ExtraHeads/SoulJars source pins were refreshed. This is a one-dependency license audit only. No runtime code, module count, release, or production compatibility claim changes. Next focused step: inspect bStats 3.0.2 distribution notices and ExtraUtils file-level headers/resources, then plan an isolated adaptation.

## Invariants and gates

- All source repository writes are forbidden for this project; only `wickidcow/SlimefunUnified` is writable.
- Preserve addon identities, source credits, copyright/license notices, namespaces, item IDs, YAML paths, persistent data and machine behavior.
- Guide visibility and ordinary-player manual crafting are independent controls; hidden modules remain registered, automation works and OP access bypasses restrictions.
- Test category/search/detail/usage/bookmark/JEG/flex/custom guide routes, and all crafting routes including custom addon recipes.
- CI compile and static JAR checks are **not** proof of gameplay compatibility. No stable release until backed-up Paper/Purpur 1.21.11 and 26.3+ boot, restart, world/data round-trip, anti-duplication, and scheduler/region-safety tests pass.

## Checkpoint — 2026-11-06 (FluffyMachines audit)

Refreshed Unified `main`, `AGENTS.md`, open PR search (none), and inspected FluffyMachines source commit `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f`, `LICENSE.txt`, `pom.xml`, `plugin.yml`, README and validation notes. Corrected prior lookup error: this addon uses **Maven** and `LICENSE.txt`, not root Gradle files or `LICENSE`. This is a source/licensing/dependency audit only, with no import, behavior changes or release. CI on this branch must pass before merge; gameplay validation remains pending.

## Earlier checkpoint — 2026-11-06

Reviewed main `AGENTS.md`, README, roadmap, credits, pinned-source assembly script and all three exact source-pin files. No open Unified PRs returned by the GitHub PR search at checkpoint. This change adds a durable audit ledger only: **no addon import, gameplay fix, new compatibility claim or release**. Next work: verify a compact next addon and its license/dependency graph, or close an existing Guide/manual-crafting coverage gap with a focused regression test. Recheck main and CI before any merge.
