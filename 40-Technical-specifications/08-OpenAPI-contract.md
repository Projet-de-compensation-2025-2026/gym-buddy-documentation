# OpenAPI contract

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-API-conventions.md](01-API-conventions.md), [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md), [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md) |

The HTTP API is specified in a **dedicated repository**, not discovered from a running backend.

**Repository:** https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi (private, default branch `develop`)

`gym-buddy-openapi` is the source of truth for **all** API: routes, operations, request/response contracts, and entities. `gym-buddy-service` and `gym-buddy-ui` **consume** that contract. They do **not** re-implement it. That is the locked target. **Today** both apps still hand-write the shapes. Do **not** claim codegen already landed.

## Source of truth

| Artifact | Role |
| --- | --- |
| `gym-buddy-openapi` (git) | Canonical contract. Reviewed, tagged, SemVer’d. |
| Static Swagger UI / Redoc on GitHub Pages | Human-readable copy of a **tag** |
| Backend | Implements the tagged spec; contract tests fail the build on drift |
| Frontend | Generates a TypeScript client from the same tag |
| Spring `springdoc` `/v3/api-docs` | Optional **dev** convenience only. Never the published contract. |

Do **not** treat Spring `springdoc` `/v3/api-docs` as the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Document | OpenAPI 3.1.0 stub (`info.version` `0.1.0`). Single file. | Full `/api/v1`. Repo **MAY** split into multi-file `$ref` (entities / requests / responses / paths) and **MUST** publish a single bundled document consumers can generate from. |
| Health | `GET /api/v1/healthz` and `GET /api/v1/readyz` (stub **and** service) | `GET /api/v1/healthz` and `GET /api/v1/readyz` |
| Auth | Stub documents `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (openapi #4 / ticket #12). UI on `develop` has `/register`, `/login`, and a log-out control that call register / login / logout (ui #3). Service on `develop` implements them (service #5 / `e2ef2aa`). Ticket #12 is closed. | Same four operations, plus the rest of `/api/v1` |
| `gym-buddy-service` | Handwritten Java DTOs and controllers. **No** `openapi-generator` (or equivalent) at build. `pom.xml` is not yet a consumer of the spec. | Generates models + API interfaces from the published bundle at build. Controllers **implement** those generated interfaces. `pom.xml` is the consumer, **not** a second contract. Do **not** commit hand-edited generated sources. |
| `gym-buddy-ui` | Handwritten `src/app/api/models.ts` + `auth-api.service.ts`. **No** orval / openapi-typescript (or equivalent) at build. | Generates the TypeScript client/types from the spec at build (orval or openapi-typescript). Consume the OpenAPI **repo / tag / bundle**. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. |
| Codegen | **Not landed.** Do not write that the service or UI already generate from the spec. | Build-time generation in both consumers. |

Locked health paths: [01-API-conventions.md](01-API-conventions.md). The service implements `healthz` / `readyz` on `develop`. Public contract is not `/actuator/health`.

Auth paths on the stub (server prefix `/api/v1`; [gym-buddy-openapi#4](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/4)):

| Method | Path | Notes (stub **and** service on `develop`; not claimed on the VPS) |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Body: `email`, `handle`, `password`, `displayName`. Creates the user. No tokens. |
| `POST` | `/api/v1/auth/login` | Body: `{ email, password }` → access JWT in JSON + `Set-Cookie` refresh. Access is not a cookie. |
| `POST` | `/api/v1/auth/refresh` | Cookie only → new access, rotated refresh `jti`. |
| `POST` | `/api/v1/auth/logout` | Revokes refresh `jti` in Redis denylist; clears cookie. |

This page is still the contract source of truth. The service on `develop` implements those four operations (service #5 / `e2ef2aa`). Ticket #12 is closed. Those operations run on the VPS container (`develop` **`aea1c56`**). Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**.

## Locked rules

1. `gym-buddy-openapi` owns routes, operations, request/response bodies, and entities. Service and UI consume that document. They do **not** invent a parallel contract in Java or TypeScript.
2. Do **not** treat Spring `springdoc` `/v3/api-docs` as the published contract (dev convenience only).
3. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. Consume the OpenAPI repo, a tag, or the published bundle.
4. The OpenAPI repo **MAY** split into multi-file `$ref` (entities / requests / responses / paths). It **MUST** still publish one bundled document the service and UI generate from.
5. Target service: generate models + API interfaces at build. Controllers implement the generated interfaces. `pom.xml` is the consumer, not a second contract. Do **not** commit hand-edited generated sources.
6. Target UI: generate the TypeScript client/types at build (orval or openapi-typescript). Same bundle / tag as the service.
7. Documentation stays **`0.3.0`**. Application repos stay **`0.1.x`**. Ticket **#24** stays cancelled. Ticket **#37** stays **Not Ready**. Do **not** claim login-from-Pages.

## Why not “just expose `/v3/api-docs`”

- The spec would exist only while Java is up
- Frontend CI would depend on a running server
- Accidental controller changes would silently rewrite the public API
- The instructor cannot review a contract that lives only in memory

A separate repo makes the contract a first-class deliverable, hostable on GitHub Pages next to this wiki.

## Workflow

This is the **target** order. Today step 3 is still handwritten consumption.

1. Ticket on this documentation repo, linking the relevant FS/TS page
2. Change the YAML/JSON in `gym-buddy-openapi` on a Gitflow `feature/#n-…` branch. If the tree is split, publish the bundled document consumers generate from.
3. Consume that revision from backend (OpenAPI Generator → Java models + API interfaces) and frontend (orval or openapi-typescript). Controllers implement the generated interfaces. The UI does **not** vendor a copy of the YAML.
4. Implement

Do not commit hand-edited generated sources.

## Versioning

The OpenAPI document’s `info.version` **is** the product public-API version (`0.y.z` until `1.0.0`). See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md). Application repos stay on **`0.1.x`** until the documentation `0.3.0` foundation is done. This page does **not** bump either number.
