#!/usr/bin/env python3
import sys
import zipfile
from folia_gate import experimental_mode, validate_unified_descriptor
from zip_entry_integrity import duplicate_entries
from pathlib import Path
if len(sys.argv) != 6:
    raise SystemExit("Usage: verify_unified_jar.py <jar> <core-sha> <extraheads-sha> <souljars-sha> <slimytreetaps-sha>")
jar = Path(sys.argv[1])
sha = sys.argv[2]
extra_sha = sys.argv[3]
soul_sha = sys.argv[4]
taps_sha = sys.argv[5]
with zipfile.ZipFile(jar) as z:
    duplicates = duplicate_entries(z)
    if duplicates:
        raise SystemExit("Duplicate ZIP entries in Unified JAR: " + repr(duplicates[:8]))
    names = set(z.namelist())
    # Owner explicitly excluded MagicExpansion; refuse a JAR containing its classes.
    # These are the exact Java package paths used by SF_MagicExpansion, not generic magic addons.
    forbidden = sorted(n for n in names if n.startswith("io/Yomicer/magicExpansion/"))
    if forbidden:
        raise SystemExit("Owner-excluded MagicExpansion classes found in Unified JAR: " + repr(forbidden[:8]))
    must = [
        "plugin.yml",
        "unified/legacy-source.sha",
        "unified/COPYING",
        "unified/addons/extraheads/COPYING-MIT",
        "unified/addons/extraheads/source.sha",
        "unified/addons/extraheads/config.yml",
        "io/github/thebusybiscuit/extraheads/ExtraHeads.class",
        "io/github/thebusybiscuit/souljars/SoulJars.class",
        "io/github/thebusybiscuit/souljars/JarsListener.class",
        "unified/addons/souljars/config.yml",
        "unified/addons/souljars/source.sha",
        "unified/addons/souljars/COPYING-GPLv3",
        "io/github/thebusybiscuit/slimytreetaps/TreeTaps.class",
        "io/github/thebusybiscuit/slimytreetaps/TreeTool.class",
        "io/github/thebusybiscuit/slimytreetaps/RubberFactory.class",
        "io/github/thebusybiscuit/slimytreetaps/ResinExtractor.class",
        "io/github/thebusybiscuit/slimytreetaps/MagicalMirror.class",
        "unified/addons/slimytreetaps/config.yml",
        "unified/addons/slimytreetaps/source.sha",
        "unified/addons/slimytreetaps/COPYING-MIT",
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
    # The core Folia flag must not silently certify the combined runtime.
    validate_unified_descriptor(meta, test_mode=experimental_mode())
    if z.read("unified/legacy-source.sha").decode().strip() != sha:
        raise SystemExit("Pinned source receipt mismatch")
    if z.read("unified/addons/extraheads/source.sha").decode().strip() != extra_sha:
        raise SystemExit("ExtraHeads source receipt mismatch")
    if "Copyright (c) 2019 TheBusyBiscuit" not in z.read("unified/addons/extraheads/COPYING-MIT").decode():
        raise SystemExit("Missing original ExtraHeads MIT copyright")
    if z.read("unified/addons/souljars/source.sha").decode().strip() != soul_sha:
        raise SystemExit("SoulJars exact-source receipt mismatch")
    if "GNU GENERAL PUBLIC LICENSE" not in z.read("unified/addons/souljars/COPYING-GPLv3").decode():
        raise SystemExit("SoulJars GPLv3 notice missing")
    if b"souljars:soul_jars" not in z.read("io/github/thebusybiscuit/souljars/SoulJars.class"):
        raise SystemExit("SoulJars historical Guide namespace missing")
    if z.read("unified/addons/slimytreetaps/source.sha").decode().strip() != taps_sha:
        raise SystemExit("SlimyTreeTaps exact-source receipt mismatch")
    if "Copyright (c) 2019 TheBusyBiscuit" not in z.read("unified/addons/slimytreetaps/COPYING-MIT").decode():
        raise SystemExit("Original SlimyTreeTaps MIT attribution missing")
    tree_class = z.read("io/github/thebusybiscuit/slimytreetaps/TreeTaps.class")
    mirror_class = z.read("io/github/thebusybiscuit/slimytreetaps/MagicalMirror.class")
    for expected_key in (b"slimytreetaps:tree_taps", b"slimytreetaps:rubber_factory", b"slimytreetaps:magical_mirror"):
        if expected_key not in tree_class:
            raise SystemExit("Historical SlimyTreeTaps key missing: "+repr(expected_key))
    if b"slimytreetaps:mirror_location" not in mirror_class:
        raise SystemExit("Historical MagicalMirror persistent identity missing")
print(f"Validated experimental core JAR ({jar.stat().st_size:,} bytes), exact upstream {sha}")
