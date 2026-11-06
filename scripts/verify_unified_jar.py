#!/usr/bin/env python3
import sys
import zipfile
from pathlib import Path
if len(sys.argv) != 3:
    raise SystemExit("Usage: verify_unified_jar.py <jar> <source-sha>")
jar = Path(sys.argv[1])
sha = sys.argv[2]
with zipfile.ZipFile(jar) as z:
    names = set(z.namelist())
    must = [
        "plugin.yml",
        "unified/legacy-source.sha",
        "unified/COPYING",
        "com/wickidcow/slimefununified/runtime/UnifiedRuntime.class",
        "com/wickidcow/slimefununified/runtime/UnifiedOwnerMenu.class",
        "com/wickidcow/slimefununified/runtime/UnifiedCraftingListener.class",
        "com/wickidcow/slimefununified/policy/PolicyRules.class",
        "io/github/thebusybiscuit/slimefun4/implementation/Slimefun.class",
    ]
    missing = [n for n in must if n not in names]
    if missing:
        raise SystemExit("Missing required JAR entries: " + repr(missing))
    meta = z.read("plugin.yml").decode()
    if "name: Slimefun" not in meta or "slimefununified.admin:" not in meta or "default: op" not in meta:
        raise SystemExit("Plugin metadata incorrect")
    if z.read("unified/legacy-source.sha").decode().strip() != sha:
        raise SystemExit("Pinned source receipt mismatch")
print(f"Validated experimental core JAR ({jar.stat().st_size:,} bytes), exact upstream {sha}")
