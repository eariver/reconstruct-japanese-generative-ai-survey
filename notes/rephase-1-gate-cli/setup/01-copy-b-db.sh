#!/usr/bin/env bash
# Byte-copy the surviving Increment B fixture into a NEW independent native-Linux
# Git DB. No clone, no alternates, no hardlinks to the source, no inherited Git
# root/index overrides. Preserves B entirely and leaves the source read-only.
set -euo pipefail

SRC=/tmp/jgas-rephase-increment-b-sol-implementation
DST=/tmp/jgas-rephase-gate-cli

if [ ! -d "$SRC" ]; then
  echo "SRC_MISSING: $SRC" >&2
  exit 2
fi
if [ -e "$DST" ]; then
  echo "DST_EXISTS: $DST" >&2
  exit 3
fi

mkdir -p "$DST"
# cp -a copies file contents (never creates links back to SRC); --no-preserve=links
# is unsupported with -a, so copy with explicit preserve set excluding links to
# guarantee no intra-copy hardlink sharing either.
cp -r --preserve=mode,timestamps,ownership "$SRC/." "$DST/"

echo "COPY_DONE $SRC -> $DST"
