# OpenAPI contract

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-API-conventions.md](01-API-conventions.md), [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md), [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md) |

The HTTP API is specified in a **dedicated repository** (`gym-buddy-openapi`), not discovered from a running backend.

## Source of truth

| Artifact | Role |
| --- | --- |
| `gym-buddy-openapi` (git) | Canonical contract. Reviewed, tagged, SemVer’d. |
| Static Swagger UI / Redoc on GitHub Pages | Human-readable copy of a **tag** |
| Backend | Implements the tagged spec; contract tests fail the build on drift |
| Frontend | Generates a TypeScript client from the same tag |
| Spring `springdoc` `/v3/api-docs` | Optional **dev** convenience only. Never the published contract. |

## Why not “just expose `/v3/api-docs`”

- The spec would exist only while Java is up
- Frontend CI would depend on a running server
- Accidental controller changes would silently rewrite the public API
- The instructor cannot review a contract that lives only in memory

A separate repo makes the contract a first-class deliverable, hostable on GitHub Pages next to this wiki.

## Workflow

1. Ticket on this documentation repo, linking the relevant FS/TS page
2. Change the YAML/JSON in `gym-buddy-openapi` on a Gitflow `feature/#n-…` branch
3. Tag / consume that revision from backend (OpenAPI Generator → Java interfaces or Spring contract tests) and frontend (TypeScript client)
4. Implement

Do not commit hand-edited generated sources.

## Versioning

The OpenAPI document’s `info.version` **is** the product public-API version (`0.y.z` until `1.0.0`). See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md).
