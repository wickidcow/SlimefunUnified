#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT
find src/main/java src/test/java -name '*.java' -print0 | xargs -0 javac --release 21 -d "$BUILD_DIR"
java -ea -cp "$BUILD_DIR" com.wickidcow.slimefununified.policy.PolicyRulesSelfTest

# Fail the policy workflow when archive-exclusion regression fixtures fail.
python3 -m unittest discover -s tests -p 'test_owner_exclusion.py'

python3 -m unittest discover -s tests -p 'test_source_collisions.py'
