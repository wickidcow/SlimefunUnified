# Unified integration ledger and checkpoint

Updated: 2026-11-06 UTC. This ledger tracks **addon modules**, excluding the Slimefun core. Historical distribution: **44 addon sources**, of which **SF_MagicExpansion is excluded by explicit owner instruction**. The target is **43 potentially eligible addons**, subject to licensing and technical review; this is not a claim that all 43 are legally eligible.

## Exact pinned inputs

| Component | Repository | Pinned commit | Status | Outstanding validation |
| --- | --- | --- | --- | --- |
| Slimefun core | wickidcow/Slimefun-Legacy | `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8` | Experimental bundled core | Paper/Purpur 1.21.11 and 26.3+ boot/restart/data and scheduler safety |
| ExtraHeads | wickidcow/SF_ExtraHeads | `b1e8a1f11692b44d359eec863f3be5be0f061516` | Prototype integrated (1/43 eligible); MIT notice packaged | Old config and item identities, drop behavior, collision and world round-trip |
| SoulJars | wickidcow/SF_SoulJars | `8fbd6befc477bbbf9970afc79e538c6b1f028cd3` | Prototype integrated (2/43 eligible); GPLv3 notice packaged | Old IDs, collection/spawner behavior, world round-trip |

**Current accounting: 2 experimentally integrated / 43 potentially eligible; 41 eligible candidate slots not integrated; 1 historical source excluded by owner (SF_MagicExpansion).** Candidate status below is **not** an eligibility determination. Do not count an addon as integrated until source, licensing, runtime and data preservation are audited, source pinned and compiled into the one-JAR artifact.

## Owner-excluded historical source (never bundled)

| Historical source | Status | Enforcement |
| --- | --- | --- |
| `wickidcow/SF_MagicExpansion` (MagicExpansion / magic plugin) | **excluded-by-owner** (1 of historical 44) | Do not fetch for integration, import sources, copy compiled classes/assets, register a module, expose toggles or reimplement its features. Not counted in the 43 eligible target, completed modules or outstanding modules. This exclusion does not apply to the distinct Magic8Ball addon. |

## Named pending candidates (not bundled)

| Candidate | Maintained source | License evidence | Integration blocker / next step |
| --- | --- | --- | --- |
| FluffyMachines | wickidcow/SF_FluffyMachines | GPLv3 verified at source pin `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f` (`LICENSE.txt`); ExtraUtils GPLv3 license verified at `bf89aee6ae`; bStats upstream MIT notice identified on default branch (not yet verified against 3.0.2 artifact); bundled resource rights still require audit | Maven build; depends on Slimefun; optional mcMMO/NoCheatPlus; bundled bStats and ExtraUtils `bf89aee6ae`. Audit shaded ExtraUtils, item IDs, machine persistence and barrel formatting before import |
| InfinityExpansion2 | wickidcow/SF_InfinityExpansion2 | GPLv3 listed in credits ledger; independently reverify | Audit storage identity and anti-duplication, dependency graph; pin source |
| Networks Expansion | wickidcow/SF_NetworksExp | GPLv3 listed in credits ledger; independently reverify | Audit item movement and conservation, dependencies; pin source |
| Supreme | wickidcow/SF_Supreme | GPLv3 listed in credits ledger; independently reverify | Audit equipment persistence and dependencies; pin source |
| JustEnoughGuide | wickidcow/SF_JustEnoughGuide | GPLv3 listed in credits ledger; independently reverify | Audit all Guide visibility paths before claiming filtering complete; pin source |

The other **36 pending eligible candidate slots** are not individually inventoried in this ledger. Obtain the authoritative 44-addon distribution list and verify each repository, current maintenance status, exact commit, transitive dependencies, resource rights and compatibility before assigning a module row. Do not infer legal eligibility from a repository name or from noncommercial intent.

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

## FluffyMachines bStats licensing checkpoint — 2026-11-07 (no import)

- FluffyMachines Maven pin `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f` declares `org.bstats:bstats-bukkit:3.0.2` and shades/relocates `org.bstats`; its build also pulls `bstats-base` transitively. No binary has been imported into Unified.
- Read-only upstream `Bastian/bStats` default-branch `LICENSE` identifies **MIT**, copyright (c) 2022 Bastian Oppermann; retain copyright and full MIT notice with any redistributed substantial bStats portion. The attempted tag `v3.0.2` returned 404, so this **does not prove the precise 3.0.2 Maven artifact's license or contents**. Verify version-specific published POM/JAR license metadata and bundled notice before distribution.
- ExtraUtils at `bf89aee6ae` explicitly includes its GPLv3 `LICENSE` in Maven resources. The pinned ExtraUtils POM marks Spigot 1.17.1, Slimefun RC-27, JSR305 and Lombok as provided; no other shaded dependencies are declared there. This does not resolve source-header or runtime compatibility checks.
- **Decision:** keep FluffyMachines blocked pending version-specific bStats notice/artifact verification, ExtraUtils file-level source/resource review, and old-world data/machine compatibility tests. Do not expose a FluffyMachines module toggle or increment integrated count.
- **Checkpoint:** refreshed Unified main AGENTS.md, open PR queue (none), ledger, core/ExtraHeads/SoulJars source pins, and pinned FluffyMachines/ExtraUtils Maven inputs. This is documentation-only. No stable release or gameplay validation. Next single task: verify exact bStats 3.0.2 published license metadata and enumerate ExtraUtils source/resource notices.


## FluffyMachines shade and resource packaging gate — 2026-11-07 (no import)

- Re-read the exact FluffyMachines source POM at `e923ad18724f690ca287a1dd2e6abd1ec4f58f2f` (blob `1c02e05bd6cd196c293da3bb623797709ff417f7`) and ExtraUtils POM at `bf89aee6ae` (blob `890ee131f97b736183de5b62fba82342717611c8`). The source pins in Unified remain unchanged: core `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8`, ExtraHeads `b1e8a1f11692b44d359eec863f3be5be0f061516`, SoulJars `8fbd6befc477bbbf9970afc79e538c6b1f028cd3`.
- **Concrete packaging hazard:** FluffyMachines' shade plugin version 3.6.2 enables `minimizeJar=true`, relocates both `org.bstats` and `com.github.Slimefun-Addon-Community.extrautils`, and filters `META-INF/*.MF` for three dependency artifacts. Its own resources configuration includes only immediate children (`<include>*</include>`), not nested resource trees. ExtraUtils' own Maven build explicitly includes root `LICENSE` as a resource; that alone does **not** prove the final minimized FluffyMachines binary retains all applicable dependency notices or resources.
- **Fail-closed import checklist:** before any import, obtain the exact published `org.bstats:bstats-bukkit:3.0.2` and transitive `bstats-base:3.0.2` POM/JAR metadata and inspect embedded LICENSE/NOTICE; inventory ExtraUtils source headers and resources at `bf89aee6ae`; record original author and modification notices; audit which shaded classes/resources are actually used; verify no dependency class collision, no missing reflective classes after minimization, and no change to persistent item IDs. Preserve all required corresponding source and build instructions. An upstream default-branch MIT license alone is insufficient version-specific evidence.
- **Verification limitation:** direct Maven Central retrieval was unavailable in this execution environment. Do not label bStats artifact notices verified or package either dependency until independently inspected. This is a source-POM-only finding, not an artifact audit, build test, or gameplay validation.
- **Checkpoint:** refreshed Unified `main` at `bce99482a111525a0be07b5aec43e4804fff50e8`, `AGENTS.md`, open PR queue (none), exact three Unified source pins, and both dependency POMs. **2/43** modules remain experimentally integrated; **41** potentially eligible candidates remain, with **SF_MagicExpansion excluded-by-owner** outside those counts. Next single task: obtain bStats 3.0.2 binary/POM notices and inspect ExtraUtils file-level notices; if unavailable, switch to an independent Guide/manual-crafting regression improvement. No release or runtime compatibility claim.


## Checkpoint — 2026-11-07 (owner exclusion archive gate)

- Refreshed Unified main at `da43f00c723047b1f63c86d7e9427a54d002769f`, `AGENTS.md`, open PRs (none), and the exact core, ExtraHeads and SoulJars pins. No upstream repository writes.
- Added `scripts/check_owner_exclusion.py` as an executable, **fail-closed archive-path check** for experimental Unified JARs. It rejects MagicExpansion-named archive entries, nested JARs requiring manual audit, corrupt archives and artifacts without compiled classes. It intentionally permits historical documentation/credits mentioning the excluded source.
- **Limitations:** this does not detect renamed/copy-pasted feature implementations, does not establish legal compliance, and does not validate runtime behavior. It must be invoked against the actual built JAR before artifact publication; adding the script alone is not a CI gate. Do not claim complete owner-exclusion enforcement until wired into packaging CI and source-level review.
- **Accounting:** 44 historical; 1 owner-excluded (`SF_MagicExpansion`); 43 potentially eligible; 2 experimentally integrated; 41 outstanding candidates. FluffyMachines remains blocked by dependency artifact notices and runtime/persistence validation.
- **Next:** wire this check into the pinned-source artifact workflow and exercise positive/negative fixture tests; then resume next feasible module. No stable release or gameplay validation.

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

## Checkpoint — 2026-11-07 (owner exclusion accounting)

Re-read Unified main `AGENTS.md`, `README.md`, the core/ExtraHeads/SoulJars source pins and the open PR queue. Owner's MagicExpansion exclusion already appears in main AGENTS.md and README; this checkpoint makes the durable integration ledger consistent with the 43-target policy. This is **manifest-only**: no new import, runtime changes, or production claims. PR #9 (ExtraUtils audit) is open separately; its three CI workflows passed at inspected commit `0b3faa0094fcc0e5650bf2a0b9d3a61bc083ff79`, but its mergeability was reported false and it was not merged in this checkpoint. Next: reconcile PR #9 against the updated ledger, then proceed with the remaining dependency audit. Paper/Purpur boot, persistence, anti-dupe and scheduler gates remain unverified.

## Checkpoint — 2026-11-07 (owner exclusion regression fixtures)

- Refreshed Unified `AGENTS.md`, open PR #14, and pinned core/ExtraHeads/SoulJars source SHA files; no upstream writes or source-pin changes.
- Added `tests/test_owner_exclusion.py` with six archive fixtures: clean class JAR, permitted historical credits, excluded class, nested JAR, classless archive and invalid ZIP. Corrected the guard to allow only historical plain-text credits under `META-INF/credits/` while rejecting excluded runtime paths.
- These tests are committed but are **not yet confirmed to run in CI**, and the guard is **not yet connected to artifact publication**. PR #14 must not be merged as a complete packaging guarantee until those checks are wired and pass.
- Accounting unchanged: 44 historical, MagicExpansion excluded by owner, 43 potentially eligible, 2 experimental integrations, 41 remaining. No runtime validation or stable release.

## Checkpoint — 2026-11-07 (owner-exclusion packaging gate)

- Refreshed Unified `main`, `AGENTS.md`, open PR #14, its exact CI status and the three unchanged core/ExtraHeads/SoulJars pins. Changes are confined to Unified PR #14.
- Wired `check_owner_exclusion.py` into `scripts/assemble_unified.sh` **after** the existing artifact verifier and **before** the script reports success; `set -e` fails the build on an excluded entry, nested JAR, corrupt JAR or missing classes. The existing pinned-source artifact workflow must use this assembly script for this gate to protect its uploaded output.
- Wired the six Python archive regression fixtures into `scripts/test.sh`, alongside the existing Java policy self-test. Await exact-head CI results before merge. Archive-path matching is not a source-level copied-feature audit.
- Counts unchanged: 44 historical; MagicExpansion excluded-by-owner; 43 candidate eligible slots; 2 experimentally integrated; 41 remaining. No new addon import or Paper/Purpur runtime validation. Next: inspect exact-head CI and merge only if all required workflows pass; then resume feasible module work.

## Checkpoint — 2026-11-07 (experimental artifact fail-closed publication)

- Refreshed main `AGENTS.md`, open PR search (none), ledger and exact core/ExtraHeads/SoulJars pins; the source pins remain unchanged.
- The experimental assembly script previously copied the built JAR to its final artifact path **before** verification. A failed verifier could leave an unverified JAR at the path later uploaded by CI. The script now removes any previous final output, stages a new JAR in the same output directory, runs both the pinned-source verifier and owner-exclusion checker against the staged file, then atomically renames it into place only after both pass. A shell EXIT trap removes failed staging files.
- This is a packaging safety improvement only, **not** a new addon integration or a runtime compatibility test. The MagicExpansion source/feature exclusion still requires source review in addition to archive-path checks. No stable release permitted.
- Counts: 44 historical; 1 excluded-by-owner (MagicExpansion); 43 potentially eligible; 2 experimental integrations (ExtraHeads, SoulJars); 41 remaining. Next: verify exact-head CI and then resume source-pinned eligible addon imports, prioritizing a legally auditable low-dependency candidate.
