# Changelog

All notable changes to **Gym Buddies** (product) and to **this documentation repository** are recorded here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning 2.0.0](https://semver.org/).

Until the first application release, versions refer to the **documentation contract**. Application repos will add their own `CHANGELOG.md` and must not contradict this one on user-visible behavior.

**Documentation `0.2.0` (2026-08-14) is not the application slice.** The next **product** tag on `gym-buddy-service`, `gym-buddy-ui`, and `gym-buddy-openapi` is application `0.2.0`: PostgreSQL 18, Redis, MinIO, Java 25 LTS / Spring Boot service layer, and basic sign-up / sign-in / log-out. See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md).

## [Unreleased]

### Added

- Environment and pipeline runbook: local compose plan (PostgreSQL 18, Redis, MinIO, API, optional MailHog), env key catalog, CI/Release/Deploy as built, OVH VPS + Caddy + UFW
- How to record the instructor cadrage (no invented minutes)
- Academic report chapter map, presentation speaker notes, screenshot checklist including VPS health
- Ticket form auto-adds every new issue to [Gym Buddy Project](https://github.com/orgs/Projet-de-compensation-2025-2026/projects/1) (`projects: Projet-de-compensation-2025-2026/1`) and requires a confirmation checkbox
- Ticket form requires [`70-Engineering-practices`](../70-Engineering-practices/README.md) on every issue (code style, git, PRs, CI/CD) so every repo and every agent follows the same workflow
- Planned **application `0.2.0`**: PostgreSQL 18, Redis, MinIO, Java 25 LTS / Spring Boot service layer, `healthz` / `readyz`, JWT register / login / logout, basic sign-up / sign-in / log-out pages. Out of scope: friends, feed, events, search, chat, admin UI, VPS data plane
- Local data plane is now in `gym-buddy-service` (`compose.yaml`, `.env.example`); MailHog stays behind the `mail` profile

### Changed

- CI applies `format.sh --write` in all four repos; `github-actions[bot]` commits if the tree is dirty. Test and smoke stay in the same job. Docs Prettier still ignores `*.md`
- Implementation branches are created or linked from the ticket’s Development panel so the project item shows the branch. The ticket form cannot auto-link a future branch
- Related-repository table now uses the four real GitHub URLs
- CI/CD: VM replace is `replace.sh` + `docker run` on `127.0.0.1`, not `docker compose up -d`; GHCR login on the VM; probe smoke is `GET /`, target is `/api/v1/healthz` and `/readyz`
- Hosting: backend is the OVH VPS `vps-c39cdf03.vps.ovh.net`, not a generic PaaS
- Fixtures: Datafaker (Java), not `@faker-js/faker`
- Technology-choices cadence row: Approved
- Changelog compare links point at this repository
- Tickets: attaching to Gym Buddy Project is required at creation, not later
- Tickets: citing `70-Engineering-practices` is required at creation
- Versioning: application `0.2.0` is defined as the first Java + data-plane + auth slice (distinct from documentation `0.2.0`)
- Runbook today-vs-target: local compose is in the service repo; Spring / Flyway still absent
- Tickets: Atlas (ops agent) owns `Not Ready` → `Todo` and `In Progress` → `Done`; Done requires Sentinel confirmation against functional requirements in this wiki. Joaquim remains product owner for consult / scope and no longer makes those two board moves by hand.
- OpenAPI stub and wiki now agree on `GET /api/v1/healthz` and `GET /api/v1/readyz` (ticket #11); probe smoke is still `GET /` until Spring
- Approved backend stack is **Java 25 LTS** (stack rewrite, not a pin). The ~18s `setup-java` deaths were a Maven cache permission denied under `contents:read`, not Temurin 26 failing to install (same failure on 25 and 26).

## [0.2.0] — 2026-08-14

Documentation contract only (process + specs). Not the Java application.

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
