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
| FluffyMachines | wickidcow/SF_FluffyMachines | GPLv3 listed in credits ledger; independently reverify source and assets | Audit runtime dependencies, machines, config and item formatting; pin source |
| InfinityExpansion2 | wickidcow/SF_InfinityExpansion2 | GPLv3 listed in credits ledger; independently reverify | Audit storage identity and anti-duplication, dependency graph; pin source |
| Networks Expansion | wickidcow/SF_NetworksExp | GPLv3 listed in credits ledger; independently reverify | Audit item movement and conservation, dependencies; pin source |
| Supreme | wickidcow/SF_Supreme | GPLv3 listed in credits ledger; independently reverify | Audit equipment persistence and dependencies; pin source |
| JustEnoughGuide | wickidcow/SF_JustEnoughGuide | GPLv3 listed in credits ledger; independently reverify | Audit all Guide visibility paths before claiming filtering complete; pin source |

The other **37 pending candidate slots** are not individually inventoried in this ledger. Obtain the authoritative 44-addon distribution list and verify each repository, current maintenance status, exact commit, transitive dependencies, resource rights and compatibility before assigning a module row. Do not infer legal eligibility from a repository name or from noncommercial intent.

## Invariants and gates

- All source repository writes are forbidden for this project; only `wickidcow/SlimefunUnified` is writable.
- Preserve addon identities, source credits, copyright/license notices, namespaces, item IDs, YAML paths, persistent data and machine behavior.
- Guide visibility and ordinary-player manual crafting are independent controls; hidden modules remain registered, automation works and OP access bypasses restrictions.
- Test category/search/detail/usage/bookmark/JEG/flex/custom guide routes, and all crafting routes including custom addon recipes.
- CI compile and static JAR checks are **not** proof of gameplay compatibility. No stable release until backed-up Paper/Purpur 1.21.11 and 26.3+ boot, restart, world/data round-trip, anti-duplication, and scheduler/region-safety tests pass.

## Checkpoint — 2026-11-06

Reviewed main `AGENTS.md`, README, roadmap, credits, pinned-source assembly script and all three exact source-pin files. No open Unified PRs returned by the GitHub PR search at checkpoint. This change adds a durable audit ledger only: **no addon import, gameplay fix, new compatibility claim or release**. Next work: verify a compact next addon and its license/dependency graph, or close an existing Guide/manual-crafting coverage gap with a focused regression test. Recheck main and CI before any merge.
