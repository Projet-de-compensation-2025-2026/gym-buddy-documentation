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
| `gym-buddy-ui` | https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui | Private | Angular member app **and** Angular back-office. **Today and approved on `develop`:** TypeScript **6** (`~6.0.2`) + **`pnpm@11.22.0`** (ui #4 / `63bebed`; ticket **#23** Done; committed lockfile; `minimumReleaseAge` **40320**). Ticket #24 (TS 6→7) is **cancelled/closed** | GitHub Pages (static `ng build`) |

Default branch on every repository: **`develop`**. Feature work never targets `main`.

The instructor account [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr) must be a collaborator on every **private** repository.

## Why an OpenAPI repository

The contract is a **git artifact**, not a runtime accident:

- Reviewers (and the instructor) read the spec without booting Java
- Frontend generates a TypeScript client from a tagged spec (`v0.3.0`), not from whatever a local server emitted today
- Backend is checked **against** that spec (contract tests / generated interfaces)
- The same YAML is published on Pages as human-readable API docs

Spring may still expose `/v3/api-docs` in development as a convenience. That endpoint is **not** the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

Today the OpenAPI stub **and** the service implement `GET /api/v1/healthz` and `GET /api/v1/readyz`. Those remain the public health paths — [../40-Technical-specifications/01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md). The public contract is not `/actuator/health`. The same stub documents `POST /api/v1/auth/register`, `/login`, `/refresh`, and `/logout` (openapi #4 / ticket #12). The UI on `develop` has a basic sign-up page, sign-in page, and log-out control that call register / login / logout (ui #3). The service on `develop` implements those operations ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. Ticket #12 is closed. Do not claim login is running on the VPS.

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

VPS apply **is done**. Ticket **#20** is **Done / closed**. The VPS container is `gym-buddy-service` `develop` **`e2ef2aa`** (service #5; auth on develop), Kernel rebuilt from develop **`e2ef2aa`** after apply (not still only `:local`). Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` on `127.0.0.1:8080` both return **200**. API bind `127.0.0.1`; data-plane ports unpublished. A bad `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist; **not** a successful signup or login). Do **not** write a completed register/login on the VPS. `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. **Not** a GHCR pull, a Release tag, or a successful replace-from-registry. Do not claim Caddy is proven.

How to run it, which ports to bind, and how a release reaches the VPS: [04-Environment-and-pipeline.md](04-Environment-and-pipeline.md).
