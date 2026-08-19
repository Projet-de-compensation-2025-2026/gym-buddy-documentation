# Backend

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-Software-architecture.md](01-Software-architecture.md), [../40-Technical-specifications/01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The approved / target backend is a single **Java 25 LTS** service (Spring Boot — see [07-Technology-choices.md](07-Technology-choices.md)) exposing HTTP and a WebSocket gateway. It **implements** the contract published in [`gym-buddy-openapi`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi); it does not own that contract.

Today [`gym-buddy-service`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service) `develop` **is** that stack: `pom.xml` exists (ticket #11) and stays **0.2.0-SNAPSHOT**. Register / login / refresh / logout **are** implemented on the service ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. Ticket **#47** is **Done**: `generate-sources` generates models + API interfaces from gym-buddy-openapi tag **v0.1.0** `$ref` tree (`openapi/openapi.yaml`; service #11 / `develop` **`3ffdef8`**). It no longer fetches `develop` / `openapi/bundled.yaml`. Ticket **#41** stays **Done** as history (service #10 / `c40f122` from that bundle). Branch `feature/47-openapi-package` is gone. Only `develop` + `main` remain. `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite unchanged. The UI has the matching pages (ui #3) and generates its client from gym-buddy-openapi tag **v0.1.0** `$ref` tree (ui #11 / ticket **#48** Done; `develop` **`47eac9c`**; lockfile **`9c7c123`**). Ticket **#42** stays **Done** as history (`b8da6bf` from `bundled.yaml`). OpenAPI stub documents the same four paths (openapi #4). Ticket #12 is closed. Caddy register/login is **proven from the operator network**. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Runtime | Java 25 LTS / Spring Boot (`pom.xml` on `develop`) | Java 25 LTS / Spring Boot modular monolith |
| Contract | Service implements `GET /api/v1/healthz` and `GET /api/v1/readyz`, plus `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (service #5 / `e2ef2aa`). OpenAPI documents the same four auth paths (openapi #4). Public contract is **not** `/actuator/health`. **Landed:** `generate-sources` generates models + API interfaces from gym-buddy-openapi tag **v0.1.0** `$ref` tree (`openapi/openapi.yaml`) ([gym-buddy-service#11](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/11) / ticket **#47** Done; `develop` **`3ffdef8`**). Branch `feature/47-openapi-package` is gone. Only `develop` + `main` remain. It no longer fetches `develop` / `openapi/bundled.yaml`. Ticket **#41** stays **Done** as history (`c40f122` / service #10 from that bundle). `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite unchanged. `pom.xml` stays **0.2.0-SNAPSHOT**. Do **not** treat `springdoc` `/v3/api-docs` as the source of truth. | Full `/api/v1`; health stays `healthz` / `readyz`. Keep pinning the versioned `gym-buddy-openapi` **package / tag**. Controllers implement generated interfaces. `pom.xml` is the consumer, not a second contract. Do **not** commit generated sources. |
| Data plane | Local compose **proven on a laptop** (PostgreSQL 18.6, Redis, MinIO; [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md)). Flyway **V1** + **V2** (`users` + `profiles`). VPS apply **done** (ticket **#20** **Done / closed**): container `develop` **`aea1c56`**; loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`; API bind `127.0.0.1`; ports unpublished. A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). Caddy is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry | Same local compose; private VPS data plane; full domain schema |

Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. First tag **v0.1.0** pointed at localhost — that is history, not today. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. Password eye is on live **v0.1.1**. Ticket **#34** is **Done**. A bad loopback `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist). Do not claim domain tables beyond Flyway V2. Local laptop compose is proven. Today’s VPS container is **aea1c56**. Ticket #12 is closed / Done. Ticket **#20** is **Done / closed**. Ticket **#24** stays cancelled.

## Modules

| Module | Owns | Does not own |
| --- | --- | --- |
| `auth` | Register, login, refresh, logout, password change | Profile fields |
| `users` | Account record, roles, lock/unlock | Friendships |
| `profiles` | Public/private profile, sports, location | Feed ranking |
| `friends` | Requests, accept/decline, blocks | Suggestions scoring |
| `feed` | Assembly of the news feed | Post storage |
| `posts` | Posts, reposts, likes | Comments tree |
| `comments` | Nested comments | Post body |
| `events` | Events, recurrence expansion, applications | Matching scores |
| `search` | Query parsing, filter execution | Suggestion model |
| `suggestions` | Candidate generation + scoring jobs | Friendship writes |
| `messaging` | Conversations, messages, receipts | Object bytes |
| `media` | Upload session, metadata, signed URLs | Chat semantics |
| `admin` | Reports, staff actions, audit log | Member UX |
| `fixtures` | Bulk seed / reset (non-production) | Production data |

## Application layers (inside each module)

```
http/ws controllers
    → application services / use cases
        → domain rules
            → persistence adapters (SQL)
            → object-store adapter
            → cache adapter
```

Domain rules (who can see a private event, whether a comment depth is allowed) are unit-tested without HTTP. See [../80-Testing/02-Unit-tests.md](../80-Testing/02-Unit-tests.md).

## Sync vs async

| Synchronous (request path) | Asynchronous (queue / worker) |
| --- | --- |
| Auth, CRUD, apply to event, send message persist | Image variants, audio duration probe |
| Search on indexed columns | Rebuild suggestion candidates |
| Authorization check before signed URL | Recurrence materialization for far-future windows |

Use the same process and an in-process queue at first; extract a worker process only if the demo host needs it.

## Configuration

All secrets come from the environment (`JWT_ACCESS_SECRET`, `S3_*`, `DATABASE_URL`, `REDIS_URL`). The API must refuse to start in production if object storage is missing — falling back to local disk is forbidden in production (assignment: do not fill local storage). Env catalog: [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).
