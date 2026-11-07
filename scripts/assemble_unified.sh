#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="$(tr -d '\r\n[:space:]' < "$ROOT/upstream/legacy-core.sha")"
if [[ ! "$PIN" =~ ^[[:xdigit:]]{40}$ ]]; then
  echo "Refusing an invalid Slimefun Legacy source SHA: $PIN" >&2
  exit 1
fi
if ! java -version 2>&1 | grep -qE 'version "25[.]|openjdk 25'; then
  echo "A Java 25 runtime is required to compile the pinned Paper 26.3 core." >&2
  exit 1
fi

WORK="$ROOT/build/upstream/Slimefun-Legacy"
mkdir -p "$ROOT/build/upstream" "$ROOT/build/output"
if [[ ! -d "$WORK/.git" ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/wickidcow/Slimefun-Legacy.git "$WORK"
fi
git -C "$WORK" fetch --no-tags --depth=1 origin "$PIN"
git -C "$WORK" checkout --force --detach "$PIN"
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
if [[ "$(git -C "$EXTRA_WORK" rev-parse HEAD)" != "$EXTRA_PIN" ]]; then
  echo "ExtraHeads exact source verification failed" >&2
  exit 1
fi
python3 "$ROOT/scripts/check_source_collisions.py" "$WORK" "$EXTRA_WORK"
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
if [[ "$(git -C "$SOUL_WORK" rev-parse HEAD)" != "$SOUL_PIN" ]]; then
  echo "SoulJars exact source verification failed" >&2
  exit 1
fi
# Check ALL three source trees together: pairwise core checks miss addon-to-addon collisions.
python3 "$ROOT/scripts/check_source_collisions.py" "$WORK" "$EXTRA_WORK" "$SOUL_WORK"
cp -R "$SOUL_WORK/src/main/java/." "$WORK/src/main/java/"
mkdir -p "$WORK/src/main/resources/unified/addons/souljars"
cp "$SOUL_WORK/src/main/resources/config.yml" "$WORK/src/main/resources/unified/addons/souljars/config.yml"
cp "$SOUL_WORK/LICENSE" "$WORK/src/main/resources/unified/addons/souljars/COPYING-GPLv3"
printf '%s\n' "$SOUL_PIN" > "$WORK/src/main/resources/unified/addons/souljars/source.sha"
python3 "$ROOT/scripts/apply_overlay.py" --source "$WORK" --unified "$ROOT"
# Preserve source attribution and the pinned SHA in an internal build receipt.
mkdir -p "$WORK/src/main/resources/unified"
printf '%s\n' "$PIN" > "$WORK/src/main/resources/unified/legacy-source.sha"
cp "$ROOT/LICENSE" "$WORK/src/main/resources/unified/COPYING"
COMMIT_DATE="$(git -C "$WORK" show -s --format=%ct HEAD)"
(
  cd "$WORK"
  SOURCE_COMMIT="$PIN" SOURCE_DATE_EPOCH="$COMMIT_DATE" \
    ./gradlew --no-daemon -PprojectVersion=Unified-0.3.0-prototype spotlessApply shadowJar
)
JAR="$(find "$WORK/build/libs" -maxdepth 1 -name 'Slimefun-Unified-0.3.0-prototype.jar' -type f -print -quit)"
if [[ -z "$JAR" ]]; then
  echo "Expected pinned-source build output not found" >&2
  ls -lh "$WORK/build/libs" >&2 || true
  exit 1
fi
# Never leave a previously published artifact looking current after a failed build.
# Stage the new output privately and publish only after BOTH gates pass.
OUTPUT="$ROOT/build/output/SlimefunUnified-0.3.0-prototype.jar"
STAGED="$(mktemp "$ROOT/build/output/.SlimefunUnified-0.3.0-prototype.XXXXXX.jar")"
rm -f "$OUTPUT"
trap 'rm -f "$STAGED"' EXIT
cp "$JAR" "$STAGED"
python3 "$ROOT/scripts/verify_unified_jar.py" "$STAGED" "$PIN" "$EXTRA_PIN" "$SOUL_PIN"
python3 "$ROOT/scripts/check_owner_exclusion.py" "$STAGED"
mv -f "$STAGED" "$OUTPUT"
trap - EXIT
echo "PROTOTYPE assembled: $OUTPUT"
