#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <file>" >&2
  exit 2
fi

file=$1
if [[ ! -e "$file" ]]; then
  echo "File not found: $file" >&2
  exit 2
fi

abs=$(cd "$(dirname "$file")" && pwd)/$(basename "$file")

if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
  if command -v wslpath >/dev/null 2>&1 && command -v cmd.exe >/dev/null 2>&1; then
    cmd.exe /c start "" "$(wslpath -w "$abs")" >/dev/null 2>&1 || {
      echo "$abs"
      exit 1
    }
    exit 0
  fi
fi

case "$(uname -s 2>/dev/null || true)" in
  Darwin)
    open "$abs" >/dev/null 2>&1 || { echo "$abs"; exit 1; }
    ;;
  Linux)
    if command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$abs" >/dev/null 2>&1 || { echo "$abs"; exit 1; }
    else
      echo "$abs"
      exit 1
    fi
    ;;
  MINGW*|MSYS*|CYGWIN*)
    start "" "$abs" >/dev/null 2>&1 || { echo "$abs"; exit 1; }
    ;;
  *)
    echo "$abs"
    exit 1
    ;;
esac
