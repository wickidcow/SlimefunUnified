#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/scripts" "$TMP/upstream" "$TMP/build/output"
cp "$ROOT/scripts/assemble_unified.sh" "$TMP/scripts/assemble_unified.sh"
OUTPUT="$TMP/build/output/SlimefunUnified-0.4.0-prototype.jar"

# The preflight must discard a previous build even when the source pin is invalid.
printf '%s\n' 'invalid-pin' > "$TMP/upstream/legacy-core.sha"
printf '%s\n' 'stale artifact' > "$OUTPUT"
if bash "$TMP/scripts/assemble_unified.sh" > "$TMP/log" 2>&1; then
  echo "Expected invalid source pin to fail" >&2
  exit 1
fi
if [[ -e "$OUTPUT" ]]; then
  echo "Stale artifact survived invalid source pin" >&2
  exit 1
fi
grep -q 'invalid Slimefun Legacy source SHA' "$TMP/log"

# Missing pin file must also fail without leaving a stale JAR.
rm "$TMP/upstream/legacy-core.sha"
printf '%s\n' 'stale artifact' > "$OUTPUT"
if bash "$TMP/scripts/assemble_unified.sh" > "$TMP/log" 2>&1; then
  echo "Expected missing source pin to fail" >&2
  exit 1
fi
if [[ -e "$OUTPUT" ]]; then
  echo "Stale artifact survived missing source pin" >&2
  exit 1
fi

echo "Preflight stale-artifact regression checks passed"
