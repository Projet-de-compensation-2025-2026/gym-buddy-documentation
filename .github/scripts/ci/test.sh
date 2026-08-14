#!/usr/bin/env bash
# Structural tests for the documentation wiki.
# Application repos replace this file with JUnit / ng test / spec lint.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"

python3 - <<'PY'
from pathlib import Path
import sys

root = Path(".").resolve()
skip_dir_names = {
    ".git",
    ".github",
    "_includes",
    "_site",
    ".jekyll-cache",
    "node_modules",
    "vendor",
}

missing_readme = []
for path in sorted(root.rglob("*")):
    if not path.is_dir():
        continue
    if any(part in skip_dir_names for part in path.relative_to(root).parts):
        continue
    if not (path / "README.md").is_file():
        missing_readme.append(str(path.relative_to(root)))

required = [
    Path("70-Engineering-practices/07-CI-CD.md"),
    Path(".github/workflows/ci.yml"),
    Path(".github/workflows/release.yml"),
    Path(".github/workflows/deploy.yml"),
    Path(".github/scripts/ci/format.sh"),
    Path(".github/scripts/ci/smoke.sh"),
    Path(".github/scripts/ci/next_version.py"),
    Path(".github/scripts/ci/prepare_changelog.py"),
    Path("_config.yml"),
    Path("README.md"),
]
missing_required = [str(p) for p in required if not p.is_file()]

errors = []
if missing_readme:
    errors.append("Folders without README.md:\n  - " + "\n  - ".join(missing_readme))
if missing_required:
    errors.append("Missing required pipeline files:\n  - " + "\n  - ".join(missing_required))

if errors:
    print("TEST FAIL\n" + "\n".join(errors), file=sys.stderr)
    sys.exit(1)

print("TEST OK: every content folder has README.md and pipeline files exist")
PY
