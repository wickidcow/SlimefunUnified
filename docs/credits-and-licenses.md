# Creator credits and license review

SlimefunUnified is intended for players, not for profit. However, **noncommercial use does not waive license obligations**. Every integrated source preserves its original authorship, attribution, copyright notices, modification history and required Corresponding Source access.

This repository is licensed under **GNU GPLv3** (see `LICENSE`), aligned with the inspected Slimefun Legacy core license.

| Module | Original creators / project lineage | Current maintained repository | Source license | Current bundling |
| --- | --- | --- | --- | --- |
| Slimefun core | TheBusyBiscuit and original Slimefun contributors | https://github.com/wickidcow/Slimefun-Legacy | GPLv3 | Prototype core |
| SoulJars | **TheBusyBiscuit**, original SoulJars community contributors | https://github.com/wickidcow/SF_SoulJars | GPLv3 | Second prototype module |
| ExtraHeads | **TheBusyBiscuit**, ybw0014 and Slimefun Addon Community contributors | https://github.com/wickidcow/SF_ExtraHeads | **MIT**; original © 2019 notice preserved | First pilot addon |
| SlimyTreeTaps | **TheBusyBiscuit** and original SlimyTreeTaps contributors; maintained by wickidcow | https://github.com/wickidcow/SF_SlimyTreeTaps | MIT original notice plus GPLv3 maintenance; original © 2019 notice preserved | Third prototype module |
| FluffyMachines | NCBPFluffyBear; FluffyMachines and Gugu contributors | https://github.com/wickidcow/SF_FluffyMachines | GPLv3 | Not bundled |
| InfinityExpansion2 | Mooy1; GuizhanCraft/IE2 contributors | https://github.com/wickidcow/SF_InfinityExpansion2 | GPLv3 | Not bundled |
| Networks | Sefiraat; ytdd9527, balugaq, yitoudaidai, tinalness and contributors | https://github.com/wickidcow/SF_NetworksExp | GPLv3 | Not bundled |
| Supreme | RelativoBR, Especttra, WilianSantosBR, Mynothauro and contributors | https://github.com/wickidcow/SF_Supreme | GPLv3 | Not bundled |
| JustEnoughGuide | balugaq and JEG contributors | https://github.com/wickidcow/SF_JustEnoughGuide | GPLv3 | Not bundled |
| MobDrops | **Daniel Walsh** (© 2020), original MobDrops contributors | https://github.com/wickidcow/SF_MobDrops | **MIT**, verified at pinned source `8943594f006a443ce8a77113f76709c871d03697` | **Not bundled**; lifecycle/configuration/command/listener adapter and bStats dependency audit outstanding |

Credits above are not exhaustive. Each subsequent addon requires its own review of source headers, source/asset licenses, fork history, modified-file notices, bundled dependency compatibility and source distribution obligations.

The ExtraHeads prototype includes the **verbatim original ExtraHeads MIT license** as `unified/addons/extraheads/COPYING-MIT` in the prototype JAR and retains the original addon repository unchanged. The new facade is clearly labeled as a Unified modification. For any distributed GPL-covered combined binary, corresponding build scripts and source must remain available under the applicable licenses.

**MobDrops staged-source audit (not an integration claim):** The exact pinned `LICENSE` includes the 2020 Daniel Walsh MIT notice, which must be copied verbatim into `unified/addons/mobdrops/COPYING-MIT` if MobDrops is ever bundled. Preserve original source headers and document Unified modifications. Review bStats transitive/shaded dependency licensing and prevent duplicate metrics registration. Do not mark MobDrops integrated or count it toward the three compiled modules until source import, JAR checks and runtime gates are actually satisfied.
