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

Documentation and application artifacts may sit on different `0.y.z` numbers until `1.0.0`. This wiki already tagged **documentation** `0.2.0` on 2026-08-14 (process + specs). The **application** `0.2.0` is the next feature slice on `gym-buddy-service`, `gym-buddy-ui`, and `gym-buddy-openapi`.

| Tag | Artifact | Meaning |
| --- | --- | --- |
| `0.1.0` | Docs + service | Assignment text; pipeline probe |
| `0.1.1` | Service | GHCR + VPS probe replace |
| `0.2.0` | Docs (2026-08-14) | Wiki process, specs, Gitflow, CI/CD contract |
| **`0.2.0` (application, planned)** | Service + UI + OpenAPI | PostgreSQL 18, Redis, MinIO, **Java 25 LTS / Spring Boot service layer**, basic **sign-up / sign-in / log-out** pages. Local compose already specified. |
| `1.0.0` | All four repos, same day | Academic ship |

Application `0.2.0` is done when all of these are true on `develop` and then tagged on `main` via Release:

1. `gym-buddy-service` is a Spring Boot app (Java 25 LTS) with Flyway, `GET /api/v1/healthz` and `GET /api/v1/readyz`
2. Local `compose.yaml` runs PostgreSQL 18, Redis, MinIO, and that API on `127.0.0.1`
3. OpenAPI documents register / login / logout / refresh under `/api/v1/auth` (`healthz` / `readyz` already on the stub)
4. JWT access + refresh as in [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md); logout denylists refresh `jti` in Redis
5. `gym-buddy-ui` has a basic sign-up, sign-in, and log-out page that call that API
6. Each repo changelog records the slice under `## [0.2.0]`

Out of scope for application `0.2.0`: friends, feed, events, search, chat, admin lock/role UI, production data-plane on the VPS.

## Who picks the number

The Release workflow computes the next version unless you type one.

| How you start Release | Result |
| --- | --- |
| `gh workflow run Release` | `auto`: `feat` → minor, breaking → minor while on `0.y.z` (major after `1.0.0`), otherwise patch |
| `gh workflow run Release -f bump=minor` | Force that bump from the latest `v*` tag |
| `gh workflow run Release -f version=0.4.0` | Use **exactly** `0.4.0` (must be greater than the latest tag) |
| `gh workflow run Release -f version=1.0.0` | Academic ship. **`1.0.0` is never chosen automatically** |

For the application slice, pin the number: `gh workflow run Release -f version=0.2.0` on each of service, UI, and OpenAPI when that slice is on `develop`.

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
| This documentation wiki | Yes | Same scheme; `0.1.0` and `0.2.0` already used for the wiki contract |

At `1.0.0`, tag **all four** repositories `v1.0.0` on the same day so the report can cite one number.

A backend must not claim `1.0.0` while it implements an OpenAPI document still at `0.x`.

## Changelog

Each repository keeps a `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. This wiki’s file is [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md).

Move bullets from `Unreleased` to a dated `## [0.y.z]` section when the Release workflow squash-merges to `main`. The workflow does this itself (`prepare_changelog.py`).

Planned application `0.2.0` work stays under `Unreleased` in this wiki until that slice is tagged on the application repos; then add a dated note here that the product slice shipped.
