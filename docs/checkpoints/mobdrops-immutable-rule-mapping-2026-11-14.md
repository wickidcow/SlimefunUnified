# MobDrops immutable rule mapping — 2026-11-14

- Base Unified main: `68b15a078ef3ffa1534c4974df5cfbf239b9a60f`.
- Pinned MobDrops source: `8943594f006a443ce8a77113f76709c871d03697`; pinned Legacy core: `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8`.
- This change extends `DropSnapshotStore` with `publishMapped`, permitting an adapter to convert mutable parsed rules into immutable DTOs *before* atomic publication. Mapper errors and null output leave the previous snapshot untouched. `publish` remains source-compatible.
- The mapper contract requires **deeply immutable output**; neither `List.copyOf` nor the mapper API itself guarantees that a caller-provided rule is immutable.
- Standalone Java 21 compilation and `-ea` snapshot regression tests passed in an isolated local scratch workspace. Full CI and Minecraft gameplay gates are separate.
- No MobDrops listener, command, parser, drop rules, or source classes imported; no additional addon counted. No change to standalone or Legacy repositories.
- Historical inventory: 44 entries, 1 excluded-by-owner `SF_MagicExpansion`, 43 eligible; 3 experimentally staged, 40 outstanding. Magic8Ball remains eligible.
- Next: source-pinned MobDrops parser to immutable DTO mapping, host lifecycle and single-listener registration, exact config/permission/command parity, and Paper/Purpur/Folia server validation. No stable release claim.
