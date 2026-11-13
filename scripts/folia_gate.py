#!/usr/bin/env python3
"""Fail-closed Folia opt-in for Unified's source-pinned plugin descriptor.

The standalone Legacy core may advertise Folia support, but its declaration
must not certify the combined core+addon runtime before live validation.
"""
import os
import re

FOLIA_KEY = re.compile(r"^\s*folia-supported\s*:", re.IGNORECASE)


def experimental_mode(environ=None):
    env = os.environ if environ is None else environ
    value = env.get("UNIFIED_FOLIA_EXPERIMENTAL", "0")
    if value not in ("0", "1"):
        raise ValueError("UNIFIED_FOLIA_EXPERIMENTAL must be 0 or 1")
    return value == "1"


def _descriptor_line(text):
    lines = text.splitlines(keepends=True)
    positions = [i for i, line in enumerate(lines) if FOLIA_KEY.match(line)]
    if len(positions) != 1:
        raise ValueError("plugin.yml must have exactly one folia-supported field")
    i = positions[0]
    value = lines[i].rstrip("\r\n")
    if value not in ("folia-supported: true", "folia-supported: false"):
        raise ValueError("Unexpected folia-supported field in plugin.yml")
    return lines, i, value


def rewrite_pinned_descriptor(text, *, test_mode=False):
    """Replace ONLY the pinned upstream true flag; preserve other YAML verbatim."""
    lines, index, value = _descriptor_line(text)
    if value != "folia-supported: true":
        raise ValueError("Pinned Legacy Folia descriptor anchor drift")
    original_ending = "\r\n" if lines[index].endswith("\r\n") else "\n" if lines[index].endswith("\n") else ""
    lines[index] = "folia-supported: " + ("true" if test_mode else "false") + original_ending
    return "".join(lines)


def validate_unified_descriptor(text, *, test_mode=False):
    """Reject accidental Folia support claims in the final experimental JAR."""
    _, _, found = _descriptor_line(text)
    expected = "folia-supported: " + ("true" if test_mode else "false")
    if found != expected:
        raise ValueError(f"Unified descriptor Folia flag {found!r}, expected {expected!r}")
