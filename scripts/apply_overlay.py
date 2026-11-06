#!/usr/bin/env python3
"""Fail-closed source overlay applied only to a disposable pinned Legacy checkout."""
import argparse
from pathlib import Path
import shutil

p = argparse.ArgumentParser()
p.add_argument("--source", type=Path, required=True)
p.add_argument("--unified", type=Path, required=True)
args = p.parse_args()
root = args.source.resolve()
project = args.unified.resolve()

def patch(relative, old, new):
    f = root / relative
    content = f.read_text(encoding="utf-8")
    count = content.count(old)
    if count != 1:
        raise SystemExit(f"Source pin drift: expected exactly one anchor in {relative}, found {count}: {old[:100]!r}")
    f.write_text(content.replace(old, new), encoding="utf-8")

for f in (project / "src/main/java/com/wickidcow/slimefununified/policy").glob("*.java"):
    target = root / "src/main/java/com/wickidcow/slimefununified/policy" / f.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f, target)

for f in (project / "overlay/src/main/java").rglob("*.java"):
    target = root / "src/main/java" / f.relative_to(project / "overlay/src/main/java")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f, target)

patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/Slimefun.java",
    "        new CraftingRestrictionListener(this);",
    "        new CraftingRestrictionListener(this);\n"
    "        com.wickidcow.slimefununified.runtime.UnifiedRuntime.initialize(this);\n"
    "        new com.wickidcow.slimefununified.runtime.UnifiedCraftingListener(this);",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/core/guide/options/SlimefunGuideSettings.java",
    """        addPlayerResources(p, menu, guide);
        addAdminTools(p, menu, guide);""",
    """        addPlayerResources(p, menu, guide);
        addAdminTools(p, menu, guide);
        // Unified owner controls occupy the formerly unused Settings & Info position.
        if (p.hasPermission("slimefununified.admin")) {
            menu.addItem(49, new CustomItemStack(Material.COMMAND_BLOCK,
                    "&6&lServer Management",
                    "&7Control addon Guide visibility and player crafting.",
                    "&7OP-only. Existing machines and data remain intact.",
                    "&eClick to configure Slimefun Unified"),
                    (pl, slot, stack, action) -> {
                        com.wickidcow.slimefununified.runtime.UnifiedOwnerMenu.open(pl, guide);
                        return false;
                    });
        }""",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/guide/SurvivalSlimefunGuide.java",
    "        int pages = (itemGroup.getItems().size() - 1) / MAX_ITEM_GROUPS + 1;",
    "        List<SlimefunItem> unifiedVisibleItems = itemGroup.getItems().stream()\n"
    "                .filter(candidate -> com.wickidcow.slimefununified.runtime.UnifiedRuntime.isVisible(p, candidate))\n"
    "                .toList();\n"
    "        int pages = Math.max(1, (unifiedVisibleItems.size() - 1) / MAX_ITEM_GROUPS + 1);",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/guide/SurvivalSlimefunGuide.java",
    "            if (target >= itemGroup.getItems().size()) {",
    "            if (target >= unifiedVisibleItems.size()) {",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/guide/SurvivalSlimefunGuide.java",
    "            SlimefunItem sfitem = itemGroup.getItems().get(target);",
    "            SlimefunItem sfitem = unifiedVisibleItems.get(target);",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/guide/SurvivalSlimefunGuide.java",
    "            if (!slimefunItem.isHidden()\n                    && isItemGroupAccessible(p, slimefunItem)",
    "            if (!slimefunItem.isHidden()\n"
    "                    && com.wickidcow.slimefununified.runtime.UnifiedRuntime.isVisible(p, slimefunItem)\n"
    "                    && isItemGroupAccessible(p, slimefunItem)",
)
patch(
    "src/main/java/io/github/thebusybiscuit/slimefun4/implementation/guide/SurvivalSlimefunGuide.java",
    "        ChestMenu menu = create(p);\n        Optional<String> wiki = item.getWikipage();",
    "        if (!com.wickidcow.slimefununified.runtime.UnifiedRuntime.isVisible(p, item)) {\n"
    "            return;\n"
    "        }\n"
    "        ChestMenu menu = create(p);\n        Optional<String> wiki = item.getWikipage();",
)
patch(
    "src/main/resources/plugin.yml",
    "website: https://github.com/wickidcow/Slimefun-Legacy",
    "website: https://github.com/wickidcow/SlimefunUnified",
)
patch(
    "src/main/resources/plugin.yml",
    "# Default permissions\npermissions:",
    "# Default permissions\npermissions:\n"
    "  slimefununified.admin:\n"
    "    description: Allows OP/admins to manage Unified addon player visibility and crafting\n"
    "    default: op",
)
print("Applied verified source overlay without changing any source repository.")
