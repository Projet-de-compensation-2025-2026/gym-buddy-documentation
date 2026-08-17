# Software architecture

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-System-context.md](02-System-context.md), [07-Technology-choices.md](07-Technology-choices.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

Gym Buddies is a **modular monolith** behind a single API, with two web clients. That is enough to cover Software Engineering and Web Technologies without paying a microservices tax on an individual project.

## Logical view

```mermaid
flowchart LR
  subgraph clients [Clients]
    FE[Member frontend]
    BO[Back-office]
  end

  subgraph edge [Edge]
    API[HTTP API]
    WS[WebSocket gateway]
  end

  subgraph app [Backend modular monolith]
    Auth[Auth and users]
    Social[Friends feed posts comments]
    Events[Events and applications]
    Search[Search and suggestions]
    Chat[Messaging]
    Media[Media and access]
    Admin[Admin and moderation]
  end

  DB[(PostgreSQL)]
  OBJ[(MinIO / S3)]
  REDIS[(Redis)]

  FE --> API
  FE --> WS
  BO --> API
  API --> app
  WS --> Chat
  app --> DB
  Media --> OBJ
  Chat --> OBJ
  Search --> REDIS
  Auth --> REDIS
```

## Why a modular monolith

| Option | Why not (for this project) |
| --- | --- |
| Many microservices | Operational cost dwarfs the academic benefit |
| Serverless-only | Harder realtime messaging and local fixtures |
| BFF per client | Two clients can share one versioned HTTP API |

Modules are **bounded contexts** in one deployable. They may not import each other’s tables; they talk through application services. That keeps a future split possible without doing it now.

## Runtime pieces

| Piece | Responsibility |
| --- | --- |
| Member frontend | Feed, profile, events, search, chat |
| Back-office | Accounts, roles, reports, fixture triggers |
| HTTP API | Commands and queries, JWT, authorization |
| WebSocket gateway | Message delivery, typing/presence (optional) |
| PostgreSQL | System of record |
| MinIO (S3 API) | Images and audio — **not** the API disk |
| Redis | Refresh-token denylist, rate limits, suggestion cache |

## Cross-cutting rules

1. Every mutating request is authenticated except `POST /api/v1/auth/register` and `POST /api/v1/auth/login`.
2. Every file download goes through an authorization check or a short-lived signed URL. See [../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md).
3. Clients never receive a permanent object-store key they can guess.
4. Background work (thumbnail, audio probe, suggestion recompute) is asynchronous.

## Quality attributes (targets)

| Attribute | Target |
| --- | --- |
| Auth | Access token ≤ 15 min; refresh rotated |
| Feed first page | < 300 ms p95 on fixture data (local) |
| Suggestion request | < 200 ms p95 using precomputed candidates |
| Media | No unbounded writes to the API container disk |
| Tenancy | Single deployment, role-based access |

## Physical deployment

- **Local:** Docker Compose in `gym-buddy-service` (plan — file not in the repo yet). Ports bind to `127.0.0.1`.
- **Defense / live API:** OVH VPS `vps-c39cdf03.vps.ovh.net`. Caddy terminates HTTPS and proxies to `127.0.0.1:8080`. The API container is replaced by `replace.sh`, not compose.
- **Static sites:** GitHub Pages (this wiki, later Angular and OpenAPI UI).

Details: [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).
