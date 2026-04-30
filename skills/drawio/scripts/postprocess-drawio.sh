#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <diagram.drawio>" >&2
  exit 2
fi

file=$1
if [[ ! -f "$file" ]]; then
  echo "File not found: $file" >&2
  exit 2
fi

if command -v npx >/dev/null 2>&1; then
  npx --no-install @drawio/postprocess "$file" >/dev/null 2>&1 || true
fi
