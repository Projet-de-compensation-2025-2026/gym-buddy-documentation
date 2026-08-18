# API conventions

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/03-Backend.md](../20-Architecture/03-Backend.md), [08-OpenAPI-contract.md](08-OpenAPI-contract.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The human-readable rules on this page must match the machine-readable document in `gym-buddy-openapi`. If they disagree, fix both in the same ticket.

## Base

- Prefix: `/api/v1`
- JSON only (`Content-Type: application/json`) except media upload
- Auth: `Authorization: Bearer <access_token>`
- Time: ISO-8601 UTC
- IDs: UUID strings

## Pagination

Cursor pagination for lists (feed, search, messages, comments).

```json
{
  "data": [ { "id": "…" } ],
  "page": { "next": "opaque-or-null", "size": 20 }
}
```

Do not use `page=3` for the feed; rows inserted concurrently would shift offsets.

## Errors

```json
{
  "error": {
    "code": "VALIDATION",
    "message": "capacity must be between 1 and 100",
    "details": [{ "path": "capacity", "issue": "range" }]
  }
}
```

Codes are listed in [../30-Functional-specifications/00-Conventions.md](../30-Functional-specifications/00-Conventions.md).

## Idempotency

`POST` that create friendships, applications, likes, or messages accept an optional `Idempotency-Key` header. Replays within 24 h return the original result.

## Versioning

Breaking changes increment `/api/v2`. Additive fields are allowed in v1.

## Health

Locked public contract (unauthenticated):

| Path | Meaning |
| --- | --- |
| `GET /api/v1/healthz` | Liveness — the process is up |
| `GET /api/v1/readyz` | Readiness — PostgreSQL and object storage are reachable |

Do not publish `/actuator/health` as the contract. Actuator may exist internally.

### Today

| Surface | Path today | Notes |
| --- | --- | --- |
| `gym-buddy-service` on `develop` | `GET /api/v1/healthz` and `GET /api/v1/readyz` | Implemented (ticket #11). `readyz` is `200` or `503` with `details` for `postgres` / `objectStorage`. |
| CI smoke | `GET /api/v1/healthz` only | The smoke image is built without Postgres/MinIO. Probe `GET /` is not today’s smoke. |
| `gym-buddy-openapi` stub | `GET /api/v1/healthz` and `GET /api/v1/readyz` | Stub and service agree (openapi #2 / ticket #11). |
| This page | `healthz` / `readyz` | Source of truth for the public health contract. Not `/actuator/health`. |
