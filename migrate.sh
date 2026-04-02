#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 /path/to/target-agent-workspace"
  exit 1
fi
cp -r workspace/. "$TARGET/"
echo "Overlay applied to: $TARGET"
