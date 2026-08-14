#!/usr/bin/env bash
# Prove the *built* wiki runs: serve _site and curl a real HTML page.
# A successful Jekyll compile is not enough; this process must answer HTTP.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"

if [[ ! -d _site ]]; then
  echo "SMOKE FAIL: _site/ is missing. Build Jekyll before this script." >&2
  exit 1
fi

port="${SMOKE_PORT:-4173}"
python3 -m http.server "$port" --bind 127.0.0.1 --directory _site &
server_pid=$!
cleanup() { kill "$server_pid" 2>/dev/null || true; }
trap cleanup EXIT

ok=0
for _ in $(seq 1 40); do
  for path in "/" "/index.html" "/gym-buddy-documentation/" "/gym-buddy-documentation/index.html"; do
    body="$(curl -fsS "http://127.0.0.1:${port}${path}" 2>/dev/null || true)"
    if [[ "$body" == *"Gym Buddies"* ]]; then
      echo "SMOKE OK: ${path} returned HTML containing 'Gym Buddies'"
      ok=1
      break 2
    fi
  done
  sleep 0.25
done

if [[ "$ok" -ne 1 ]]; then
  echo "SMOKE FAIL: static server never returned a Gym Buddies page on port ${port}" >&2
  echo "--- _site listing (first 40) ---" >&2
  find _site -maxdepth 3 -type f | head -40 >&2 || true
  exit 1
fi
