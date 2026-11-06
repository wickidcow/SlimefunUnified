# Creator credits and license review

This project is intended to benefit players, not generate revenue. **Not charging money does not remove software license obligations.** Every integrated addon will retain independent in-game credit, historical authorship, source links, copyright notices and any distribution attribution required by its license.

| Intended module | Original credits / lineage identified in maintained README | Maintained source | Initial license identified |
| --- | --- | --- | --- |
| Slimefun core | TheBusyBiscuit and original Slimefun contributors | https://github.com/wickidcow/Slimefun-Legacy | GPL-3.0 |
| FluffyMachines | NCBPFluffyBear; later FluffyMachines and Gugu contributors | https://github.com/wickidcow/SF_FluffyMachines | GPL-3.0 |
| InfinityExpansion2 | Mooy1's InfinityExpansion lineage; GuizhanCraft/InfinityExpansion2 rewrite contributors | https://github.com/wickidcow/SF_InfinityExpansion2 | GPL-3.0 |
| Networks | Sefiraat original project; ytdd9527, balugaq, yitoudaidai, tinalness and NetworksExpansion contributors | https://github.com/wickidcow/SF_NetworksExp | GPL-3.0 |
| Supreme | RelativoBR, Especttra, WilianSantosBR, Mynothauro and Supreme contributors | https://github.com/wickidcow/SF_Supreme | GPL-3.0 |
| JustEnoughGuide | balugaq and JEG contributors | https://github.com/wickidcow/SF_JustEnoughGuide | GPL-3.0 |

These credits are **not exhaustive**; read source headers and history before integration. Additional addon candidates require the same diligence.

## License blocker to resolve

This new repository currently has a **GNU GPL version 2** LICENSE file, while the *current inspected* core and first addon candidates have GPLv3 license files. This is not by itself proof that every source file is GPLv3-only, but a GPLv2-only combined distribution cannot simply absorb GPLv3-only sources. Before migrating source, explicitly review applicable source licenses and select a compatible license (likely GPLv3, subject to all existing rights/versions). Do **not** silently assume free/nonprofit use resolves incompatibilities.

Before code import, inventory source headers, author copyright, license grants, upstream fork lineage, assets (textures/sounds), third-party libraries, modified-source notice, source distribution and corresponding source offer obligations.

Every player-facing creator screen should name the original author and link original and maintained project sources, not imply SlimefunUnified originated their work.
