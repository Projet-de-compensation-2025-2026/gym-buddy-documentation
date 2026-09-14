# API conventions

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/03-Backend.md](../20-Architecture/03-Backend.md), [08-OpenAPI-contract.md](08-OpenAPI-contract.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The human-readable rules on this page must match the machine-readable document in `gym-buddy-openapi`. If they disagree, fix both in the same ticket.

## Base

- Prefix: `/api/v1`
- JSON only (`Content-Type: application/json; charset=UTF-8`) except media upload. Error bodies, including unauthenticated `/api/v1/admin/*`, are UTF-8. Do not emit `charset=ISO-8859-1`.
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

Idempotency requirements are defined per operation in the OpenAPI contract. Do not assume a universal 24-hour replay cache: verify the implementation and duplicate-operation tests for the endpoint.

## Versioning

Breaking changes increment `/api/v2`. Additive fields are allowed in v1.

## Health

Locked public contract (unauthenticated):

| Path | Meaning |
| --- | --- |
| `GET /api/v1/healthz` | Liveness — the process is up |
| `GET /api/v1/readyz` | Readiness — PostgreSQL and object storage are reachable |

Do not publish `/actuator/health` as the contract. Actuator may exist internally.
