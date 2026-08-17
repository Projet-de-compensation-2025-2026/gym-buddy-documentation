# Changelog

All notable changes to **Gym Buddies** (product) and to **this documentation repository** are recorded here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/).

Until the first application release, versions refer to the **documentation contract**. Application repos will add their own `CHANGELOG.md` and must not contradict this one on user-visible behavior.

## [Unreleased]

### Added

- Environment and pipeline runbook: local compose plan (PostgreSQL 18, Redis, MinIO, API, optional MailHog), env key catalog, CI/Release/Deploy as built, OVH VPS + Caddy + UFW
- How to record the instructor cadrage (no invented minutes)
- Academic report chapter map, presentation speaker notes, screenshot checklist including VPS health

### Changed

- Related-repository table now uses the four real GitHub URLs
- CI/CD: VM replace is `replace.sh` + `docker run` on `127.0.0.1`, not `docker compose up -d`; GHCR login on the VM; probe smoke is `GET /`, target is `/api/v1/healthz` and `/readyz`
- Hosting: backend is the OVH VPS `vps-c39cdf03.vps.ovh.net`, not a generic PaaS
- Fixtures: Datafaker (Java), not `@faker-js/faker`
- Technology-choices cadence row: Approved
- Changelog compare links point at this repository

## [0.2.0] — 2026-08-14

### Changed

- Engineering practices now follow [Gitflow (Atlassian)](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) and [SemVer 2.0.0](https://semver.org/); `1.0.0` is the compensation-project ship, earlier tags stay on `0.y.z`
- Commits that implement a GitHub Issue use the ticket id as the Conventional Commits scope; ticket-less commits must not invent one
- Tickets live on this repository, attach to the singular **Gym Buddy Project**, must link a wiki page, and are referenced from every other repo
- Feature work follows consult → specs → ticket: statuses are `Not Ready`, `Todo` (Joaquim’s green light only), `In Progress`, and `Done` (merged to `develop`)
- Stack: Java 26 + Spring Boot backend, Angular 22 + TypeScript 7 frontend, PostgreSQL 18, dedicated `gym-buddy-openapi` repository (not a live `/v3/api-docs` as source of truth)
- Hosting: GitHub Pages for this wiki, the Angular apps, and the OpenAPI UI; Java and PostgreSQL cannot run on Pages
- Releases onto `main` are automated squash+tag commits; version numbers are computed from Conventional Commits and can be overridden by hand

### Added

- Feature implementation workflow: consult Joaquim Kéloglanian, update functional and technical specs, then open a fully filled ticket on **Gym Buddy Project**
- CI/CD contract: GitHub Actions CI on every `develop` PR/push, a separate Release workflow that squash-merges and tags `main`, Deploy of that tag (Pages / Docker + VM). Private-repo Pages and branch-protection need GitHub Pro or a public repo.
- Confluence-style wiki structure (`XX-Section-name`) covering the 2025/2026 compensation brief
- Functional specifications for every overview feature
- Technical specifications for JWT, file ACL, image storage, messaging, search, fixtures
- Algorithms: friend suggestions, filtered search, user matching
- UML (use case, activity, sequence, class) in Mermaid
- Engineering practices, test plan, critical analysis, academic deliverable outlines

## [0.1.0] — 2026-08-13

### Added

- English and French assignment text under `00-Project-brief`

[Unreleased]: https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/releases/tag/v0.2.0
[0.1.0]: https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/releases/tag/v0.1.0
