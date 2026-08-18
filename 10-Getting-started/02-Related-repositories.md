# Related repositories

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/01-Software-architecture.md](../20-Architecture/01-Software-architecture.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md), [04-Environment-and-pipeline.md](04-Environment-and-pipeline.md) |

Gym Buddies is documented **once** here and implemented in **three** other repositories.

| Repository | URL | Visibility | Responsibility | Hosted on |
| --- | --- | --- | --- | --- |
| `gym-buddy-documentation` (this repo) | https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation | Public | Product, architecture, specs, practices, academic packaging, **tickets** | GitHub Pages (Markdown → Jekyll) |
| `gym-buddy-openapi` | https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi | Private | Versioned OpenAPI 3 contract + static Swagger/Redoc | GitHub Pages when the plan allows (static) |
| `gym-buddy-service` | https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service | Private | Java 25 LTS / Spring Boot API (`pom.xml` on `develop`), domain, jobs, WebSocket, fixtures | OVH VPS — see [04-Environment-and-pipeline.md](04-Environment-and-pipeline.md) |
| `gym-buddy-ui` | https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui | Public | Angular member app **and** Angular back-office. **Today and approved on `develop`:** TypeScript **6** (`~6.0.2`) + **`pnpm@11.22.0`** (ui #4 / `63bebed`; ticket **#23** Done; committed lockfile; `minimumReleaseAge` **40320**). Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Ticket #24 (TS 6→7) is **cancelled/closed**. Ticket **#30** Done: first tag **v0.1.0** | GitHub Pages — https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ (HTTP **200**, production `baseHref` `/gym-buddy-ui/`). Direct `/register` is HTTP **404** with the SPA index body (`404.html`), not a working auth route. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**. First tag **v0.1.0** pointed at localhost. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. Ticket **#31** is **Done / closed**. Do **not** claim login-from-Pages |

Default branch on every repository: **`develop`**. Feature work never targets `main`.

The instructor account [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr) must be a collaborator on every **private** repository.

## Why an OpenAPI repository

The contract is a **git artifact**, not a runtime accident:

- Reviewers (and the instructor) read the spec without booting Java
- Frontend generates a TypeScript client from a tagged spec (`v0.3.0`), not from whatever a local server emitted today
- Backend is checked **against** that spec (contract tests / generated interfaces)
- The same YAML is published on Pages as human-readable API docs

Spring may still expose `/v3/api-docs` in development as a convenience. That endpoint is **not** the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

Today the OpenAPI stub **and** the service implement `GET /api/v1/healthz` and `GET /api/v1/readyz`. Those remain the public health paths — [../40-Technical-specifications/01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md). The public contract is not `/actuator/health`. The same stub documents `POST /api/v1/auth/register`, `/login`, `/refresh`, and `/logout` (openapi #4 / ticket #12). The UI on `develop` has a basic sign-up page, sign-in page, and log-out control that call register / login / logout (ui #3). The service on `develop` implements those operations ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. Ticket #12 is closed. Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**.

## Rules for application repos

1. Do not copy functional specs into application trees. Link to `30-Functional-specifications`.
2. Do not hand-edit generated clients; change the OpenAPI repo and regenerate.
3. Tickets live in **this** documentation repo and must link to a wiki page ([../70-Engineering-practices/05-Tickets-and-GitHub-projects.md](../70-Engineering-practices/05-Tickets-and-GitHub-projects.md)).
4. The report cites all four repositories using the URLs in the table above.

## Local development picture

```
gym-buddy-documentation/     ← you are here (wiki + GitHub Project)
gym-buddy-openapi/           ← HTTP contract
gym-buddy-service/           ← Java 25 LTS + Spring Boot (`pom.xml` on develop)
gym-buddy-ui/                ← Angular 22. Today and approved: TypeScript ~6.0.2 + pnpm@11.22.0. Ticket #24 cancelled.
```

A laptop `compose.yaml` in the backend repo starts PostgreSQL 18, MinIO, Redis, and the API. That boot is **proven** ([`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md) on `gym-buddy-service` `develop`). The Angular apps point at `http://localhost:8080/api/v1`. OpenAPI files are consumed as a git submodule, a published package, or a raw tagged URL — pick one in the backend README and stick to it. This is **not** the VPS story.

VPS apply **is done**. Ticket **#20** is **Done / closed**. The VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` on `127.0.0.1:8080` both return **200**. API bind `127.0.0.1`; data-plane ports unpublished. A bad loopback `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. **Not** a GHCR pull, a Release tag, or a successful replace-from-registry. Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. Ticket **#31** is **Done / closed**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**.

How to run it, which ports to bind, and how a release reaches the VPS: [04-Environment-and-pipeline.md](04-Environment-and-pipeline.md).
