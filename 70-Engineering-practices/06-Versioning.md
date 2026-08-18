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

On `develop` today (ticket #11, not yet a product tag): `gym-buddy-service` is already a Spring Boot app (Java 25 LTS) with Flyway **V1** + **V2** (`users` + `profiles`), `GET /api/v1/healthz` and `GET /api/v1/readyz`, and `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. The OpenAPI stub documents those paths (openapi #4) and the UI has sign-up / sign-in / log-out pages (ui #3). Ticket #12 is **closed**. Local compose runtime is **proven on a laptop** ([gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`; [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md)). VPS data-plane **files** landed ([gym-buddy-service#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/7) / `a07e21e`). The VPS is still one `docker run` API container (tag **v0.1.1**) until apply. **Apply is not done.** Do not claim VPS `healthz` / `readyz` 200, and do not claim login is running on the VPS. Ticket #20 stays **open / Todo**.

Documentation `0.3.0` is done when all of these are true on `develop` and then tagged on `main` via Release (coding agents can then work from this point):

1. **Local compose proven at runtime** — **done** on a laptop ([gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`, 2026-08-18 10:40:55Z). `cp .env.example .env && docker compose up -d --build` booted PostgreSQL 18.6, Redis 8.10.0, MinIO `RELEASE.2025-09-07T16-13-09Z`, Java 25.0.3 Temurin / Spring Boot 4.1.0, binds `127.0.0.1` only. `GET /api/v1/healthz` → 200 `{"status":"ok"}`. `GET /api/v1/readyz` → 200 `{"status":"ok"}`. Evidence: [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md). **Not** the VPS.
2. **PostgreSQL and the Java service run on the existing OVH VPS** (`vps-c39cdf03.vps.ovh.net`). **Files only today** ([gym-buddy-service#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/7) / `a07e21e`): `deploy/compose.yaml` (PostgreSQL 18.6, Redis, MinIO on `gym-buddy-data`, no published ports), `deploy/replace.sh` joins that network, `deploy/vps.env.example`, [`docs/vps-data-plane.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/vps-data-plane.md). **Apply is not done.** Do not claim VPS `healthz` / `readyz` 200, and do not claim login on the VPS. Public story stays Caddy → `127.0.0.1:8080`. The VM is still one `docker run` API container (tag **v0.1.1**) until an operator applies those files.
3. **Sign-up and sign-in** — **done** on `develop` (ticket #12 **closed**; openapi #4, ui #3, [gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`). `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout`: Argon2id, HS256 access JWT, refresh cookie, Redis denylist. **Not** claimed on the VPS.
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
