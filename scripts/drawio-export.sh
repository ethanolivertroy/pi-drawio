#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <input.drawio> <png|svg|pdf|jpg> [output-file]" >&2
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 2
fi

input=$1
format=$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')
output=${3:-"${input}.${format}"}

case "$format" in
  png|svg|pdf|jpg) ;;
  *) echo "Unsupported format: $format" >&2; exit 2 ;;
esac

if [[ ! -f "$input" ]]; then
  echo "Input file not found: $input" >&2
  exit 2
fi

is_wsl=false
if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
  is_wsl=true
fi

find_drawio() {
  if command -v drawio >/dev/null 2>&1; then
    command -v drawio
    return 0
  fi

  if command -v draw.io >/dev/null 2>&1; then
    command -v draw.io
    return 0
  fi

  if [[ "$(uname -s 2>/dev/null || true)" == "Darwin" ]]; then
    local mac_app="/Applications/draw.io.app/Contents/MacOS/draw.io"
    if [[ -x "$mac_app" ]]; then
      printf '%s\n' "$mac_app"
      return 0
    fi
  fi

  if [[ "$is_wsl" == true ]]; then
    local default_win="/mnt/c/Program Files/draw.io/draw.io.exe"
    if [[ -x "$default_win" ]]; then
      printf '%s\n' "$default_win"
      return 0
    fi

    local win_user="${WIN_USER:-}"
    if [[ -z "$win_user" ]] && command -v cmd.exe >/dev/null 2>&1; then
      win_user=$(cmd.exe /c 'echo %USERNAME%' 2>/dev/null | tr -d '\r' | tail -n 1 || true)
    fi

    if [[ -n "$win_user" ]]; then
      local per_user="/mnt/c/Users/${win_user}/AppData/Local/Programs/draw.io/draw.io.exe"
      if [[ -x "$per_user" ]]; then
        printf '%s\n' "$per_user"
        return 0
      fi
    fi
  fi

  return 1
}

if ! drawio_cmd=$(find_drawio); then
  echo "draw.io CLI not found. Install draw.io Desktop to enable export, or open the .drawio file directly: $(cd "$(dirname "$input")" && pwd)/$(basename "$input")" >&2
  exit 127
fi

args=("$drawio_cmd" -x -f "$format" -b 10 -o "$output")
if [[ "$format" == "png" || "$format" == "svg" || "$format" == "pdf" ]]; then
  args+=( -e )
fi
args+=( "$input" )

"${args[@]}"

if [[ ! -s "$output" ]]; then
  echo "Export did not create a non-empty output file: $output" >&2
  exit 1
fi

printf '%s\n' "$output"
