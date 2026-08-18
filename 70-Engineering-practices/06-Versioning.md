# Versioning

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Git-workflow.md](02-Git-workflow.md), [07-CI-CD.md](07-CI-CD.md), [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md) |

Gym Buddies versions follow **Semantic Versioning 2.0.0**:

[Semantic Versioning 2.0.0 (semver.org)](https://semver.org/)

Cite that page the same way we cite [Conventional Commits](https://www.conventionalcommits.org/). The public API those numbers describe is the HTTP contract in `gym-buddy-openapi` (and the behaviour specified in this wiki).

## The compensation-project rule

| Version | Meaning |
| --- | --- |
| `0.y.z` | Everything **before** the academic delivery. The public API is **not** stable ([SemVer §4](https://semver.org/#spec-item-4)). |
| `1.0.0` | The version **shipped for the ISEP compensation project** (report, GitHub access, defense). This is the first stable public API ([SemVer §5](https://semver.org/#spec-item-5)). |
| `1.y.z` / `2.0.0` | After the course, if the product continues |

Until `1.0.0` we stay on **major version 0**. We do **not** jump to `1.x` for intermediate demos.

Start at `0.1.0`. During `0.y.z`, increment **y** when we add a feature slice worth tagging, and **z** for fixes, as SemVer’s own FAQ recommends for initial development. Tags on `main` look like `v0.1.0`, `v0.2.0`, `v0.2.1`, … then `v1.0.0`.

Gitflow: only commits on `main` are tagged, and only by the Release workflow ([07-CI-CD.md](07-CI-CD.md)). `develop` is unreleased (`Unreleased` in the changelog).

## Planned slices (0.y.z)

Documentation and application artifacts may sit on different `0.y.z` numbers until `1.0.0`. This wiki already tagged **documentation** `0.2.0` on 2026-08-14 (process + specs). That tag stays. The next slice is **documentation `0.3.0`**: the technical-foundation contract. Application repos (`gym-buddy-service`, `gym-buddy-ui`, `gym-buddy-openapi`) stay on **`0.1.x`** until that foundation is actually done on `develop` and then tagged. There is no planned application `0.2.0` next slice.

| Tag | Artifact | Meaning |
| --- | --- | --- |
| `0.1.0` | Docs + service | Assignment text; pipeline probe |
| `0.1.1` | Service | GHCR + VPS probe replace |
| `0.2.0` | Docs (2026-08-14) | Wiki process, specs, Gitflow, CI/CD contract |
| **`0.3.0` (documentation, planned)** | Docs | Technical-foundation contract |
| `0.1.x` | Service / UI / OpenAPI (current) | Stay here until the documentation `0.3.0` foundation is done on `develop` and then tagged |
| `1.0.0` | All four repos, same day | Academic ship |

On `develop` today (ticket #11, not yet a product tag): `gym-buddy-service` is already a Spring Boot app (Java 25 LTS) with Flyway **V1 baseline**, `GET /api/v1/healthz` and `GET /api/v1/readyz`. The OpenAPI stub documents auth and the UI has sign-up / sign-in / log-out pages (ui #3). Register / login / logout is **not** a done product slice: the service has not implemented those operations (service #5 still open). Local `compose.yaml` and `.env.example` exist (ticket #7). Runtime boot of that compose is **not** claimed. The VPS is still one `docker run` API container (tag **v0.1.1**). PostgreSQL does **not** run on the VPS today.

Documentation `0.3.0` is done when all of these are true on `develop` and then tagged on `main` via Release (coding agents can then work from this point):

1. **Local compose proven at runtime** — not just files in git. `docker compose up -d` on a laptop has been booted: PostgreSQL 18, Redis, MinIO, Java 25 LTS Spring service, binds `127.0.0.1`. `GET /api/v1/healthz` returns 200 and `GET /api/v1/readyz` returns 200. Today those files exist (tickets #7 / #11); **runtime boot is not yet claimed**.
2. **PostgreSQL and the Java service run on the existing OVH VPS** (`vps-c39cdf03.vps.ovh.net`). Not laptop-only compose. Private data-plane on the Docker network; do not publish `5432` / `6379` / `9000`. Public story stays Caddy → `127.0.0.1:8080`. Today the VM is still one `docker run` API container (tag **v0.1.1** probe/replace).
3. **Sign-up and sign-in** (existing ticket #12; log-out stays in that ticket because it is already specified). OpenAPI stub and UI pages exist on `develop`. The service has **not** landed. **Not done today**.
4. **Developers and coding agents can work** on `gym-buddy-service`, `gym-buddy-ui`, and `gym-buddy-openapi`, push to `develop`, and when a version is stable, update the remote machines via the existing Release → Deploy path.

Do not invent extra product features for this slice: no friends, feed, events, search, chat, or admin UI.

## Who picks the number

The Release workflow computes the next version unless you type one.

| How you start Release | Result |
| --- | --- |
| `gh workflow run Release` | `auto`: `feat` → minor, breaking → minor while on `0.y.z` (major after `1.0.0`), otherwise patch |
| `gh workflow run Release -f bump=minor` | Force that bump from the latest `v*` tag |
| `gh workflow run Release -f version=0.4.0` | Use **exactly** `0.4.0` (must be greater than the latest tag) |
| `gh workflow run Release -f version=1.0.0` | Academic ship. **`1.0.0` is never chosen automatically** |

For the documentation `0.3.0` wiki tag, pin the number on this repository when that contract is on `develop`: `gh workflow run Release -f version=0.3.0`. Application repos stay on `0.1.x` until the foundation is done; pin their numbers on those repos when they are tagged. Do not assume they become `0.3.0`.

The number is written as an annotated git tag `vX.Y.Z` on the squash commit on `main`.

## What each number means (after 1.0.0)

From [semver.org](https://semver.org/):

1. **MAJOR** — incompatible API changes
2. **MINOR** — backward-compatible functionality
3. **PATCH** — backward-compatible bug fixes

Before `1.0.0`, anything may change; we still record those changes in the changelog so the report can show history.

## Which artifacts share a version

| Artifact | Versioned? | Notes |
| --- | --- | --- |
| OpenAPI contract (`gym-buddy-openapi`) | Yes | This **is** the public API number |
| Backend | Yes | Implements a given contract version |
| Frontend | Yes | Consumes a given contract version |
| This documentation wiki | Yes | Same scheme; `0.1.0` and `0.2.0` already used for the wiki contract; `0.3.0` is the planned foundation contract |

At `1.0.0`, tag **all four** repositories `v1.0.0` on the same day so the report can cite one number.

A backend must not claim `1.0.0` while it implements an OpenAPI document still at `0.x`.

## Changelog

Each repository keeps a `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. This wiki’s file is [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md).

Move bullets from `Unreleased` to a dated `## [0.y.z]` section when the Release workflow squash-merges to `main`. The workflow does this itself (`prepare_changelog.py`).

Documentation `0.3.0` foundation work stays under `Unreleased` in this wiki until that contract is tagged on `main`. Application repos stay on `0.1.x` until the foundation is done on `develop` and then tagged; then add a dated note here that the foundation shipped.
