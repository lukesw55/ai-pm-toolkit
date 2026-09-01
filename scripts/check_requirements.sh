#!/usr/bin/env bash
# check_requirements.sh — local environment preflight for ai-pm-toolkit.

set -euo pipefail

missing=0

need() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'OK    %s\n' "$1"
  else
    printf 'MISS  %s\n' "$1" >&2
    missing=1
  fi
}

need bash
need python3
need jq

if command -v sha256sum >/dev/null 2>&1; then
  printf 'OK    sha256sum\n'
elif command -v shasum >/dev/null 2>&1; then
  printf 'OK    shasum -a 256\n'
else
  printf 'MISS  sha256sum or shasum\n' >&2
  missing=1
fi

for hook in hooks/*.sh; do
  if [ -x "$hook" ]; then
    printf 'OK    executable %s\n' "$hook"
  else
    printf 'WARN  not executable %s (Claude can still run via shell, but chmod +x is recommended)\n' "$hook" >&2
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "check_requirements: missing required tools" >&2
  exit 1
fi

echo "check_requirements: all required tools found"
