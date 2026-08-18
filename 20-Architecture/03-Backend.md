# Backend

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-Software-architecture.md](01-Software-architecture.md), [../40-Technical-specifications/01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The approved / target backend is a single **Java 25 LTS** service (Spring Boot — see [07-Technology-choices.md](07-Technology-choices.md)) exposing HTTP and a WebSocket gateway. It **implements** the contract published in [`gym-buddy-openapi`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi); it does not own that contract. Today the service repo is still the Python probe — see the table below.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Runtime | Python 3.12 probe image, `GET /` HTML | Java 25 LTS / Spring Boot |
| Contract | OpenAPI stub `GET /api/v1/healthz` and `GET /api/v1/readyz` | Full `/api/v1`, health `healthz` / `readyz` |
| Data plane | None on the VPS | PostgreSQL 18, Redis, MinIO (local compose first) |

Do not claim Spring is running until `pom.xml` exists in [`gym-buddy-service`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service).

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
