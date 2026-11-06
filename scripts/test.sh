#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT
find src/main/java src/test/java -name '*.java' -print0 | xargs -0 javac --release 21 -d "$BUILD_DIR"
java -ea -cp "$BUILD_DIR" com.wickidcow.slimefununified.policy.PolicyRulesSelfTest
