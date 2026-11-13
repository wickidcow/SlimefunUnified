"""Fail-closed ZIP entry checks for the experimental single-plugin artifact."""
from collections import Counter


def duplicate_entries(archive):
    """Return sorted duplicate or unsafe entry names.

    Reject path aliases that may be interpreted differently by ZIP extractors,
    classloaders, or artifact inspection tools. Directory entries ending in '/'
    are permitted, but must have otherwise canonical relative paths.
    """
    counts = Counter()
    unsafe = set()
    for info in archive.infolist():
        name = info.filename
        parts = name.rstrip("/").split("/")
        if (
            not name
            or name.startswith("/")
            or "\\" in name
            or "\x00" in name
            or any(part in ("", ".", "..") for part in parts)
            or (parts and ":" in parts[0])
        ):
            unsafe.add(name)
        counts[name] += 1
    return sorted(unsafe | {name for name, count in counts.items() if count > 1})
