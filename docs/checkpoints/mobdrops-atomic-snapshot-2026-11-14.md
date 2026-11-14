# Unified checkpoint — 2026-11-14

Status: **experimental source foundation only; not a MobDrops integration**.

- Base main: `d4da898a89af2d0785b449e861faa6b4f050f98e`.
- Historical source inventory: **44**. `SF_MagicExpansion`: **excluded-by-owner**, not imported, completed, or outstanding. Eligible: **43**. Experimentally integrated: **3** (ExtraHeads, SoulJars, SlimyTreeTaps). Outstanding: **40**, including MobDrops. Magic8Ball remains eligible.
- Pinned Legacy core: `f04d8077f496b5cc5e9f76bda4f8d47b5040a7c8`. Pinned MobDrops: `8943594f006a443ce8a77113f76709c871d03697`.
- MobDrops provenance: `wickidcow/SF_MobDrops`, original author Daniel Walsh / WalshyDev, MIT license; full original license must be preserved when imported. Source and runtime integration blockers documented in `docs/mobdrops-runtime-integration-checkpoint.md`.
- This branch adds `DropSnapshotStore`, a Java 21 immutable atomic publication primitive, and a concurrency regression test. It is deliberately not wired to live MobDrops events. It cannot be counted as an integrated module.
- Local standalone Java 21 compilation and assertion self-test passed. Full repository CI and experimental assembly are separate gates; check the PR's current workflow status before merging.
- Remaining MobDrops work: source-pinned host lifecycle adapter, historical config path and parser, one-time command/listener registration, standalone collision rejection, bStats review, original drop algorithm, Guide/crafting policy isolation, restart/persistence, Paper/Purpur/Folia scheduler and anti-dupe validation.
- No stable release or production compatibility assertion is authorized. Standalone SF_* and Slimefun Legacy repositories remain read-only.
