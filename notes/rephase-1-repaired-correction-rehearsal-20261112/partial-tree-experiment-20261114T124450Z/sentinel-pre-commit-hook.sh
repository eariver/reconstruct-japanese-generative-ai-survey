#!/bin/sh
# sentinel pre-commit hook for partial-tree experiment - proves normal commit ran hooks (no bypass)
echo "pre-commit-ran pid=$$ ppid=$PPID date=$(date -u +%Y%m%dT%H%M%SZ)" >> "$(git rev-parse --git-dir)/pre-commit-sentinel.log"
exit 0
