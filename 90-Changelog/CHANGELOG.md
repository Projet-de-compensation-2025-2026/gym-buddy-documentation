# Changelog

All notable changes to **Gym Buddies** (product) and to **this documentation repository** are recorded here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning 2.0.0](https://semver.org/).

Until the first application release, versions refer to the **documentation contract**. Application repos will add their own `CHANGELOG.md` and must not contradict this one on user-visible behavior.

**Documentation `0.3.0` is the technical-foundation contract.** Application repos stay on `0.1.x` until that foundation is done on `develop` and then tagged. Documentation `0.2.0` (2026-08-14) remains the already-tagged wiki process/specs tag. There is no planned application `0.2.0` next slice. See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md).

## [Unreleased]

### Added

- Environment and pipeline runbook: local compose plan (PostgreSQL 18, Redis, MinIO, API, optional MailHog), env key catalog, CI/Release/Deploy as built, OVH VPS + Caddy + UFW
- How to record the instructor cadrage (no invented minutes)
- Academic report chapter map, presentation speaker notes, screenshot checklist including VPS health
- Ticket form auto-adds every new issue to [Gym Buddy Project](https://github.com/orgs/Projet-de-compensation-2025-2026/projects/1) (`projects: Projet-de-compensation-2025-2026/1`) and requires a confirmation checkbox
- Ticket form requires [`70-Engineering-practices`](../70-Engineering-practices/README.md) on every issue (code style, git, PRs, CI/CD) so every repo and every agent follows the same workflow
- Local data plane is now in `gym-buddy-service` (`compose.yaml`, `.env.example`); MailHog stays behind the `mail` profile
- Application service layer on `gym-buddy-service` `develop` (ticket #11): Java 25 LTS / Spring Boot (`pom.xml`), Flyway `V1` baseline, `GET /api/v1/healthz` and `GET /api/v1/readyz`
- Environment page: SSH + `docker logs` inspect runbook for the VPS API (`gym-buddy-service`) and data-plane `postgres` / `redis` / `minio`. There is no Grafana / Loki / OpenShift / Argo log UI.

### Changed

- CI applies `format.sh --write` in all four repos; `github-actions[bot]` commits if the tree is dirty. Test and smoke stay in the same job. Docs Prettier still ignores `*.md`
- Implementation branches are created or linked from the ticket’s Development panel so the project item shows the branch. The ticket form cannot auto-link a future branch
- Related-repository table now uses the four real GitHub URLs
- CI/CD: VM replace is `replace.sh` + `docker run` on `127.0.0.1`, not `docker compose up -d`; GHCR login on the VM; service CI smoke is `GET /api/v1/healthz` (not probe `GET /`)
- Hosting: backend is the OVH VPS `vps-c39cdf03.vps.ovh.net`, not a generic PaaS
- Fixtures: Datafaker (Java), not `@faker-js/faker`
- Technology-choices cadence row: Approved
- Changelog compare links point at this repository
- Tickets: attaching to Gym Buddy Project is required at creation, not later
- Tickets: citing `70-Engineering-practices` is required at creation
- Documentation `0.3.0` is the technical-foundation contract; application repos stay on `0.1.x` until it is done. This replaces planned application `0.2.0` as the next slice. Documentation `0.2.0` (2026-08-14) stays as the wiki process/specs tag.
- Runbook today-vs-target: local compose and Java 25 LTS / Spring Boot (`pom.xml`, Flyway V1) are on `gym-buddy-service` `develop`
- Tickets: Atlas (ops agent) owns `Not Ready` → `Todo` and `In Progress` → `Done`; Done requires Sentinel confirmation against functional requirements in this wiki. Joaquim remains product owner for consult / scope and no longer makes those two board moves by hand.
- Tickets: Kernel sets `Todo` → `In Progress` when they start the work (after creating or linking the branch from the issue Development panel). Atlas still owns only those two transitions. Do not leave a card in `Todo` while Kernel is implementing. Sentinel does not move the board. Joaquim is not the merge/board gate.
- OpenAPI stub **and** the service implement `GET /api/v1/healthz` and `GET /api/v1/readyz` (ticket #11); CI smoke hits `healthz` only (smoke image has no Postgres/MinIO). Probe `GET /` is not today’s service smoke
- OpenAPI stub on `develop` documents `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (openapi #4 / ticket #12). `gym-buddy-ui` `develop` (app version `0.1.0`, ui #3) has `/register`, `/login`, and a log-out control that call register / login / logout; access JWT stays in memory; refresh cookie credentials are sent.
- Service on `develop` implements those four auth operations ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. Flyway `V2__users_and_profiles.sql`. Ticket #12 is closed. Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**.
- Local compose runtime is proven on a laptop (ticket #19 / [gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`): `cp .env.example .env && docker compose up -d --build`; `GET /api/v1/healthz` and `GET /api/v1/readyz` both 200 `{"status":"ok"}`; binds `127.0.0.1` only (`8080`, `5432`, `6379`, `9000`, `9001`). Evidence: `gym-buddy-service` [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md). Not the VPS.
- VPS apply **done**. Ticket **#20** is **Done / closed**. Sentinel confirmed the rebuild: VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` on `127.0.0.1:8080` both **200**. API bind `127.0.0.1`; data-plane ports unpublished. A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. **Not** a GHCR pull, a Release tag, or a successful replace-from-registry. Ticket **#12** stays closed (openapi #4 + ui #3 + service #5).
- Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`. Live Pages is **v0.1.1** and embeds the VPS `apiBaseUrl`. Ticket **#31** is **Done / closed** for **only** `apiBaseUrl` + CORS + that live bundle. Do **not** write that signup/login from github.io works. UFW 443 is Joaquim’s IPv6 prefix only (do not publish that prefix). Documentation `0.3.0` is **not** bumped.
- Approved backend stack is **Java 25 LTS** (stack rewrite, not a pin). The ~18s `setup-java` deaths were a Maven cache permission denied under `contents:read`, not Temurin 26 failing to install (same failure on 25 and 26).
- Approved frontend toolchain is **TypeScript 6** (`~6.0.2` on `gym-buddy-ui` `develop`) and **pnpm** with a four-week `minimumReleaseAge` of **40320** minutes (`pnpm-workspace.yaml`; older pnpm `.npmrc` `minimum-release-age=40320`). Corepack pin, committed `pnpm-lock.yaml`, no `latest`, `onlyBuiltDependencies` and/or ignore-scripts, Renovate/Dependabot cooldown ≥ four weeks. Do not invent a `package.json` field for the age floor. Today `gym-buddy-ui` `develop` is **`pnpm@11.22.0`** (ui #4 / `63bebed`; ticket **#23** Done; committed lockfile; `minimumReleaseAge` **40320**) and TypeScript `~6.0.2`. Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed). Reason: `typescript@7.0.0` is 404 on npm; latest 7.0.x Kernel found is **7.0.2** (2026-07-08, Go `tsc`); 7.0.2 installs and standalone typecheck passes; `ng build` fails because Angular 22 still uses the TS 6 API (`ts.readConfigFile is not a function`). Kernel did not pin `@typescript/native-preview`, `tsgo`, or Angular next. App version stays `0.1.0`. Do **not** claim TypeScript 7 landed. Do **not** treat 7.0.0 or 7.0.2 as approved or as a next step.
- `gym-buddy-ui` GitHub Pages **live**. Ticket **#30** is **Done**. First UI tag was **v0.1.0** (localhost `apiBaseUrl`). Current live tag is **v0.1.1**. Bundle `main-4WJYST2C.js` embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye. Sentinel confirmed https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ returns **HTTP 200** and serves the Angular app with production `baseHref` `/gym-buddy-ui/`. Root 200 is the acceptance. Direct `/register` returns **HTTP 404** with the SPA index body (`404.html`). That is Pages’ static fallback, **not** a broken app and **not** a working auth route. Ticket **#31** is **Done / closed** (Atlas). UI `develop` **`7916fa8`** has that VPS `apiBaseUrl`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. Do **not** write that signup/login from github.io works. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. `SameSite=Lax` will **not** ride a github.io → VPS credentialed XHR. Do **not** start Kernel. Ticket **#34** stays Done. Ticket **#24** stays cancelled. Approved toolchain stays TypeScript **`~6.0.2`** + **pnpm**.
- Password eye is on live **v0.1.1** (`main-4WJYST2C.js`) and on `gym-buddy-ui` `develop` (`75fbbce` / ui #9). Ticket **#34** is **Done**.
- CORS is **proven** from Joaquim’s PC on service `develop` **`aea1c56`**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Live Pages is **v0.1.1** and embeds that VPS URL. First tag **v0.1.0** pointed at localhost. Ticket **#31** is **Done / closed** for **only** `apiBaseUrl` + CORS + live **v0.1.1**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. Ticket **#34** stays Done. Ticket **#24** stays cancelled. Documentation `0.3.0` is **not** bumped.
- Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Live Pages is **v0.1.1**. Bundle `main-4WJYST2C.js` embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye. Password eye is on live **v0.1.1**. Ticket **#34** is **Done**. Today’s VPS container is **aea1c56**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. First tag **v0.1.0** pointed at localhost — that is history, not today. Ticket **#24** stays cancelled. Documentation `0.3.0` is **not** bumped.

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
