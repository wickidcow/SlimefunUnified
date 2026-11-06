# SlimefunUnified development instructions

- Develop this project separately from wickidcow/Slimefun-Legacy. Never alter the working Slimefun Legacy core, standalone addons, their release assets, or their development automation just to build SlimefunUnified.
- Goal: **one future installable JAR**, while retaining distinctly named, individually credited modules and the separately maintained addon repositories.
- **Player access toggle only.** Never unload integrated module code or unregister saved items when an owner hides an addon or denies player crafting. Existing items, worlds, recipes, machines, research, storage and automation must remain intact.
- Maintain independent Guide-visibility and player-crafting flags for each module and item. Administrators/OPs still see and craft the content; machine automation is unaffected.
- Replace the former Coming Soon button in the Guide with an OP-only Server Management entry. Also support the maintained JustEnoughGuide settings entry. Re-check permissions for every action and command. Use slimefununified.admin with default OP.
- Hide from player-facing Guide searches, favorites/bookmarks, recipes, usages and category lists, without breaking underlying item identity or persistence.
- Do not claim hiding is a security boundary: content could still be visible in inventories, through old items, other mods or plugins.
- Preserve all historical addon IDs, PDC keys, BlockStorage and other saved data. Prevent duplicate registration if standalone addon JARs coexist with integrated ones.
- Honor original author credits, headers, source repositories, modification notices and license requirements. Current repo LICENSE is GPLv2; imported GPLv3-only code needs a legally compatible project license decision **before import**. Noncommercial distribution is not an exemption.
- Current source is *policy prototype only*, not a deployable Minecraft plugin. Never market it as complete without server bootstrap, build, and real tests.
- Use small verified changes and keep future release gates: 1.21.11 and 26.3+ Paper/Purpur, saved-world round trips, duplication/persistence and performance; region scheduler validation before Folia/Leaf claims.
