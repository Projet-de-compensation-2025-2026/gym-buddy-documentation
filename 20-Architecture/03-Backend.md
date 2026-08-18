# Backend

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-Software-architecture.md](01-Software-architecture.md), [../40-Technical-specifications/01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The approved / target backend is a single **Java 25 LTS** service (Spring Boot — see [07-Technology-choices.md](07-Technology-choices.md)) exposing HTTP and a WebSocket gateway. It **implements** the contract published in [`gym-buddy-openapi`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi); it does not own that contract.

Today [`gym-buddy-service`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service) `develop` **is** that stack: `pom.xml` exists (ticket #11). Register / login / refresh / logout **are** implemented on the service ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist. The UI has the matching pages (ui #3). OpenAPI stub documents the same four paths (openapi #4). Ticket #12 is closed. Do not claim login is running on the VPS.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Runtime | Java 25 LTS / Spring Boot (`pom.xml` on `develop`) | Java 25 LTS / Spring Boot modular monolith |
| Contract | Service implements `GET /api/v1/healthz` and `GET /api/v1/readyz`, plus `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (service #5 / `e2ef2aa`). OpenAPI stub documents the same four auth paths (openapi #4). Public contract is **not** `/actuator/health`. | Full `/api/v1`; health stays `healthz` / `readyz` |
| Data plane | Local compose **proven on a laptop** (PostgreSQL 18.6, Redis, MinIO; [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md)). Flyway **V1** + **V2** (`users` + `profiles`). VPS apply **done** (ticket **#20** **Done / closed**): container `develop` **`e2ef2aa`** (service #5; Kernel rebuilt from develop **`e2ef2aa`** after apply; not still only `:local`); loopback `GET healthz` and `GET readyz` **200** on `127.0.0.1:8080`; API bind `127.0.0.1`; ports unpublished. A bad `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry | Same local compose; private VPS data plane; full domain schema |

Do not write a completed register/login on the VPS. A bad `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist; **not** a successful signup or login). Do not claim Caddy is proven, or domain tables beyond Flyway V2. Local laptop compose is proven. Service auth is on `develop` (`e2ef2aa`). Ticket #12 is closed / Done. Ticket **#20** is **Done / closed**.

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
