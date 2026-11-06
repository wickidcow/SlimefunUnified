#!/usr/bin/env python3
import sys
import zipfile
from pathlib import Path
if len(sys.argv) != 4:
    raise SystemExit("Usage: verify_unified_jar.py <jar> <core-sha> <extraheads-sha>")
jar = Path(sys.argv[1])
sha = sys.argv[2]
extra_sha = sys.argv[3]
with zipfile.ZipFile(jar) as z:
    names = set(z.namelist())
    must = [
        "plugin.yml",
        "unified/legacy-source.sha",
        "unified/COPYING",
        "unified/addons/extraheads/COPYING-MIT",
        "unified/addons/extraheads/source.sha",
        "unified/addons/extraheads/config.yml",
        "io/github/thebusybiscuit/extraheads/ExtraHeads.class",
        "io/github/thebusybiscuit/extraheads/items/MobHead.class",
        "com/wickidcow/slimefununified/runtime/UnifiedRuntime.class",
        "com/wickidcow/slimefununified/runtime/UnifiedOwnerMenu.class",
        "com/wickidcow/slimefununified/runtime/UnifiedCraftingListener.class",
        "com/wickidcow/slimefununified/policy/PolicyRules.class",
        "io/github/thebusybiscuit/slimefun4/implementation/Slimefun.class",
    ]
    missing = [n for n in must if n not in names]
    if missing:
        raise SystemExit("Missing required JAR entries: " + repr(missing))
    if z.namelist().count("plugin.yml") != 1:
        raise SystemExit("Unified must expose exactly one root Bukkit plugin descriptor")
    if b"extraheads:extra_heads" not in z.read(
            "io/github/thebusybiscuit/extraheads/setup/ItemGroups.class"):
        raise SystemExit("Historical ExtraHeads category namespace not retained")
    if b"extraheads:decapitation" not in z.read(
            "io/github/thebusybiscuit/extraheads/setup/RecipeTypes.class"):
        raise SystemExit("Historical ExtraHeads recipe namespace not retained")
    meta = z.read("plugin.yml").decode()
    if "name: Slimefun" not in meta or "slimefununified.admin:" not in meta or "default: op" not in meta:
        raise SystemExit("Plugin metadata incorrect")
    if z.read("unified/legacy-source.sha").decode().strip() != sha:
        raise SystemExit("Pinned source receipt mismatch")
    if z.read("unified/addons/extraheads/source.sha").decode().strip() != extra_sha:
        raise SystemExit("ExtraHeads source receipt mismatch")
    if "Copyright (c) 2019 TheBusyBiscuit" not in z.read("unified/addons/extraheads/COPYING-MIT").decode():
        raise SystemExit("Missing original ExtraHeads MIT copyright")
print(f"Validated experimental core JAR ({jar.stat().st_size:,} bytes), exact upstream {sha}")
