# MobDrops pinned dependency and packaging audit — 2026-11-16

**Audit only; no runtime module import or integration-count change.** This file supplements the MobDrops source-contract audit in draft PR #56.

## Source provenance

- Read-only upstream: `wickidcow/SF_MobDrops@8943594f006a443ce8a77113f76709c871d03697`
- Audited descriptor: `pom.xml` at that exact commit, Maven project `dev.walshy:SFMobDrops:1.0.4`
- Java target: 21. Paper API: `1.21.11-R0.1-SNAPSHOT`; Slimefun API: `com.github.SlimefunGuguProject:Slimefun4:2025.1` (both `provided`).
- `org.bstats:bstats-bukkit:3.2.1` is a runtime dependency; the standalone shade relocates `org.bstats` to `dev.walshy.sfmobdrops.bstats`. An embedded Unified module **must not** copy standalone metrics startup or duplicate the relocated service.
- `com.google.code.findbugs:jsr305:3.0.2` is `provided`.
- Test-only: `org.junit.jupiter:junit-jupiter:6.0.3` and `org.mockbukkit.mockbukkit:mockbukkit-v26.2:4.116.1`.
- Maven repositories declared: PaperMC and JitPack. The descriptor uses resource filtering on top-level resources and the Maven shade plugin; never blindly merge `plugin.yml` or `META-INF` from the standalone jar into Unified.
- Upstream MIT license and original Daniel Walsh copyright notice require preservation verbatim in the eventual combined JAR. This descriptor audit **does not** establish licenses of every transitive dependency or resource.

## Integration blockers and acceptance criteria

1. Verify exact pinned Java sources, LICENSE, config and all transitive dependency licenses before any source import. Preserve source headers, historical command aliases and `plugins/SFMobDrops/config.yml`.
2. Adapt `JavaPlugin` lifecycle to a host-owned module facade; register one death listener, one GUI listener and one command executor only, with no standalone metrics instance. Reject a simultaneously installed standalone `SFMobDrops` before enabling embedded handlers.
3. Convert the complete configuration into an immutable validated snapshot and publish atomically; invalid reloads must preserve the prior working snapshot. Entity death events must execute on the entity-owning region on Folia.
4. Assert drop amount/chance, item metadata, world-disabled behavior, custom-name/PDC filters and no duplicate rewards. Independent Guide and manual-crafting policies must not suppress mob drops.
5. Check combined-JAR class/resource collisions, retained original MIT license, and the exact source SHA. Execute tests and collect CI evidence, then Paper/Purpur/Folia boot/restart and world-data round-trips. Compile success alone is not certification.

Historical inventory remains 44 sources / **43 eligible**, with 3 experimental modules staged and **40 outstanding**. `SF_MagicExpansion` is **excluded-by-owner** and must not be imported, registered, reimplemented or counted; distinct Magic8Ball remains eligible.
