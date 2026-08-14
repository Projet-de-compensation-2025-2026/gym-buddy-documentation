#!/usr/bin/env bash
# Format the wiki. CI passes --check; Release passes --write.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"

mode="${1:---check}"

# Markdown is not auto-reflowed: tables and Mermaid break. YAML / JSON / HTML are.
npx --yes prettier@3.6.2 "$mode" \
  --ignore-path .prettierignore \
  --print-width 100 \
  ".github/**/*.{yml,yaml}" \
  "_config.yml" \
  "_includes/**/*.html" \
  ".prettierrc.json"
