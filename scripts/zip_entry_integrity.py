"""Fail-closed ZIP entry checks for the experimental single-plugin artifact."""
from collections import Counter

def duplicate_entries(archive):
    """Return sorted duplicate entry names, including repeated plugin descriptors."""
    counts = Counter(info.filename for info in archive.infolist())
    return sorted(name for name, count in counts.items() if count > 1)
