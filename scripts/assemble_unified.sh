#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Fail closed even when the pin file is absent/invalid or Java 25 is unavailable.
# Never leave a stale experimental JAR that appears to belong to this invocation.
mkdir -p "$ROOT/build/output"
OUTPUT="$ROOT/build/output/SlimefunUnified-0.4.0-prototype.jar"
rm -f "$OUTPUT"
PIN="$(tr -d '\r\n[:space:]' < "$ROOT/upstream/legacy-core.sha")"
if [[ ! "$PIN" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "Refusing an invalid Slimefun Legacy source SHA: $PIN" >&2
  exit 1
fi
if ! java -version 2>&1 | grep -qE 'version "25[.]|openjdk 25'; then
  echo "A Java 25 runtime is required to compile the pinned Paper 26.3 core." >&2
  exit 1
fi

# Exercise archive-path exclusion regression fixtures on every experimental build.
python3 -m unittest discover -s "$ROOT/scripts" -p "test_owner_exclusion_paths.py" -v


WORK="$ROOT/build/upstream/Slimefun-Legacy"
mkdir -p "$ROOT/build/upstream" "$ROOT/build/output"
if [[ ! -d "$WORK/.git" ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/wickidcow/Slimefun-Legacy.git "$WORK"
fi
git -C "$WORK" fetch --no-tags --depth=1 origin "$PIN"
git -C "$WORK" checkout --force --detach "$PIN"
# Remove files left by earlier imports/overlays before copying pinned sources.
# --force checkout alone does not remove untracked OR ignored files from previous builds.
# These are disposable source checkouts: purge ignored Java/resources too before import.
git -C "$WORK" clean -ffdx
if [[ "$(git -C "$WORK" rev-parse HEAD)" != "$PIN" ]]; then
  echo "Pinned source verification failed" >&2
  exit 1
fi
# Compile exact-source ExtraHeads code into this ONE plugin, never as a nested JAR.
EXTRA_PIN="$(tr -d '\r\n[:space:]' < "$ROOT/upstream/extraheads.sha")"
if [[ ! "$EXTRA_PIN" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "Invalid ExtraHeads source SHA: $EXTRA_PIN" >&2
  exit 1
fi
EXTRA_WORK="$ROOT/build/upstream/SF_ExtraHeads"
if [[ ! -d "$EXTRA_WORK/.git" ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/wickidcow/SF_ExtraHeads.git "$EXTRA_WORK"
fi
git -C "$EXTRA_WORK" fetch --no-tags --depth=1 origin "$EXTRA_PIN"
git -C "$EXTRA_WORK" checkout --force --detach "$EXTRA_PIN"
# Remove files left by earlier imports/overlays before copying pinned sources.
# --force checkout alone does not remove untracked files from previous builds.
git -C "$EXTRA_WORK" clean -ffdx
if [[ "$(git -C "$EXTRA_WORK" rev-parse HEAD)" != "$EXTRA_PIN" ]]; then
  echo "ExtraHeads exact source verification failed" >&2
  exit 1
fi
python3 "$ROOT/scripts/check_source_collisions.py" "$WORK" "$EXTRA_WORK"
python3 "$ROOT/scripts/check_source_collisions.py" --check-assets "$EXTRA_WORK"
cp -R "$EXTRA_WORK/src/main/java/." "$WORK/src/main/java/"
mkdir -p "$WORK/src/main/resources/unified/addons/extraheads"
cp "$EXTRA_WORK/src/main/resources/config.yml" "$WORK/src/main/resources/unified/addons/extraheads/config.yml"
cp "$EXTRA_WORK/LICENSE" "$WORK/src/main/resources/unified/addons/extraheads/COPYING-MIT"
printf '%s\n' "$EXTRA_PIN" > "$WORK/src/main/resources/unified/addons/extraheads/source.sha"
# Bring SoulJars into the SAME plugin JAR from its exact baseline source commit.
SOUL_PIN="$(tr -d '\r\n[:space:]' < "$ROOT/upstream/souljars.sha")"
if [[ ! "$SOUL_PIN" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "Invalid SoulJars source SHA" >&2
  exit 1
fi
SOUL_WORK="$ROOT/build/upstream/SF_SoulJars"
if [[ ! -d "$SOUL_WORK/.git" ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/wickidcow/SF_SoulJars.git "$SOUL_WORK"
fi
git -C "$SOUL_WORK" fetch --no-tags --depth=1 origin "$SOUL_PIN"
git -C "$SOUL_WORK" checkout --force --detach "$SOUL_PIN"
# Remove files left by earlier imports/overlays before copying pinned sources.
# --force checkout alone does not remove untracked files from previous builds.
git -C "$SOUL_WORK" clean -ffdx
if [[ "$(git -C "$SOUL_WORK" rev-parse HEAD)" != "$SOUL_PIN" ]]; then
  echo "SoulJars exact source verification failed" >&2
  exit 1
fi
# WORK already contains ExtraHeads after the earlier copy; checking WORK against SoulJars covers core and ExtraHeads without false-positive self-collisions.
python3 "$ROOT/scripts/check_source_collisions.py" "$WORK" "$SOUL_WORK"
python3 "$ROOT/scripts/check_source_collisions.py" --check-assets "$SOUL_WORK"
cp -R "$SOUL_WORK/src/main/java/." "$WORK/src/main/java/"
mkdir -p "$WORK/src/main/resources/unified/addons/souljars"
cp "$SOUL_WORK/src/main/resources/config.yml" "$WORK/src/main/resources/unified/addons/souljars/config.yml"
cp "$SOUL_WORK/LICENSE" "$WORK/src/main/resources/unified/addons/souljars/COPYING-GPLv3"
printf '%s\n' "$SOUL_PIN" > "$WORK/src/main/resources/unified/addons/souljars/source.sha"
# Import pinned SlimyTreeTaps Java source as a distinct module in this same plugin build.
TAPS_PIN="$(tr -d '\r\n[:space:]' < "$ROOT/upstream/slimytreetaps.sha")"
if [[ ! "$TAPS_PIN" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "Invalid SlimyTreeTaps source SHA" >&2
  exit 1
fi
TAPS_WORK="$ROOT/build/upstream/SF_SlimyTreeTaps"
if [[ ! -d "$TAPS_WORK/.git" ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/wickidcow/SF_SlimyTreeTaps.git "$TAPS_WORK"
fi
git -C "$TAPS_WORK" fetch --no-tags --depth=1 origin "$TAPS_PIN"
git -C "$TAPS_WORK" checkout --force --detach "$TAPS_PIN"
# Remove files left by earlier imports/overlays before copying pinned sources.
# --force checkout alone does not remove untracked files from previous builds.
git -C "$TAPS_WORK" clean -ffdx
if [[ "$(git -C "$TAPS_WORK" rev-parse HEAD)" != "$TAPS_PIN" ]]; then
  echo "SlimyTreeTaps exact source verification failed" >&2
  exit 1
fi
python3 "$ROOT/scripts/check_source_collisions.py" "$WORK" "$TAPS_WORK"
python3 "$ROOT/scripts/check_source_collisions.py" --check-assets "$TAPS_WORK"
cp -R "$TAPS_WORK/src/main/java/." "$WORK/src/main/java/"
mkdir -p "$WORK/src/main/resources/unified/addons/slimytreetaps"
cp "$TAPS_WORK/src/main/resources/config.yml" "$WORK/src/main/resources/unified/addons/slimytreetaps/config.yml"
cp "$TAPS_WORK/LICENSE" "$WORK/src/main/resources/unified/addons/slimytreetaps/COPYING-MIT"
printf '%s\n' "$TAPS_PIN" > "$WORK/src/main/resources/unified/addons/slimytreetaps/source.sha"
python3 "$ROOT/scripts/apply_overlay.py" --source "$WORK" --unified "$ROOT"
# Fail before compilation if an excluded module path entered the assembled tree.
python3 "$ROOT/scripts/check_excluded_source.py" "$WORK"
# Preserve source attribution and the pinned SHA in an internal build receipt.
mkdir -p "$WORK/src/main/resources/unified"
printf '%s\n' "$PIN" > "$WORK/src/main/resources/unified/legacy-source.sha"
cp "$ROOT/LICENSE" "$WORK/src/main/resources/unified/COPYING"
COMMIT_DATE="$(git -C "$WORK" show -s --format=%ct HEAD)"
(
  cd "$WORK"
  SOURCE_COMMIT="$PIN" SOURCE_DATE_EPOCH="$COMMIT_DATE" \
    ./gradlew --no-daemon -PprojectVersion=Unified-0.4.0-prototype spotlessApply shadowJar
)
JAR="$(find "$WORK/build/libs" -maxdepth 1 -name 'Slimefun-Unified-0.4.0-prototype.jar' -type f -print -quit)"
if [[ -z "$JAR" ]]; then
  echo "Expected pinned-source build output not found" >&2
  ls -lh "$WORK/build/libs" >&2 || true
  exit 1
fi
# Never leave a previously published artifact looking current after a failed build.
# Stage the new output privately and publish only after BOTH gates pass.
STAGED="$(mktemp "$ROOT/build/output/.SlimefunUnified-0.4.0-prototype.XXXXXX.jar")"
trap 'rm -f "$STAGED"' EXIT
cp "$JAR" "$STAGED"
python3 "$ROOT/scripts/verify_unified_jar.py" "$STAGED" "$PIN" "$EXTRA_PIN" "$SOUL_PIN" "$TAPS_PIN"
python3 "$ROOT/scripts/check_owner_exclusion.py" "$STAGED"
mv -f "$STAGED" "$OUTPUT"
trap - EXIT
echo "PROTOTYPE assembled: $OUTPUT"
