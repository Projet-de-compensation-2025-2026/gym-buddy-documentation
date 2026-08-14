#!/usr/bin/env python3
"""Move CHANGELOG.md Unreleased notes into a dated ## [X.Y.Z] section."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
# Keep a Changelog files in this repo live under 90-Changelog/
CANDIDATES = [
    Path("90-Changelog/CHANGELOG.md"),
    Path("CHANGELOG.md"),
]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: prepare_changelog.py X.Y.Z")
    version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        sys.exit(f"invalid version: {version}")

    path = next((p for p in CANDIDATES if p.is_file()), None)
    if path is None:
        sys.exit("CHANGELOG.md not found")

    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## \[Unreleased\]\s*\n(.*?)(?=^## \[)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        sys.exit("Could not find ## [Unreleased] section")

    body = match.group(1).rstrip() + "\n"
    if not body.strip():
        body = "### Changed\n\n- Release workflow published this version.\n"

    today = dt.date.today().isoformat()
    replacement = (
        f"## [Unreleased]\n\n"
        f"### Added\n\n"
        f"### Changed\n\n"
        f"## [{version}] — {today}\n\n"
        f"{body.lstrip()}\n"
    )
    new_text = text[: match.start()] + replacement + text[match.end() :]

    # Keep-a-changelog footer links, if present
    unreleased_link = re.search(r"^\[Unreleased\]:\s+\S+\s*$", new_text, flags=re.MULTILINE)
    if unreleased_link:
        new_text = (
            new_text[: unreleased_link.end()]
            + f"\n[{version}]: https://github.com/Projet-de-compensation-2025-2026/"
            f"{Path('.').resolve().name}/releases/tag/v{version}"
            + new_text[unreleased_link.end() :]
        )

    path.write_text(new_text, encoding="utf-8")
    print(f"Updated {path} for {version}")


if __name__ == "__main__":
    main()
