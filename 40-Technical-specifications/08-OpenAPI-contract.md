# OpenAPI contract

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-API-conventions.md](01-API-conventions.md), [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md), [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md) |

The HTTP API is specified in a **dedicated repository**, not discovered from a running backend.

**Repository:** https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi (private, default branch `develop`)

`gym-buddy-openapi` is the source of truth for **all** API: routes, operations, request/response contracts, and entities. `gym-buddy-service` and `gym-buddy-ui` **consume** that contract. They do **not** re-implement it. That is the locked target. **Today** both apps still hand-write the shapes. Do **not** claim codegen already landed. That is tickets **#41** (service) and **#42** (UI).

## Source of truth

| Artifact | Role |
| --- | --- |
| `gym-buddy-openapi` (git) | Canonical contract. Reviewed, tagged, SemVer’d. |
| `$ref` tree (`openapi/openapi.yaml` + paths / components) | **Edit source.** Editors change this tree, not the bundle. |
| `openapi/bundled.yaml` | **Checked-in consumer document.** Service and UI generate from this file. |
| Static Swagger UI / Redoc on GitHub Pages | Human-readable copy of a **tag** |
| Backend | Implements the tagged spec; contract tests fail the build on drift |
| Frontend | Generates a TypeScript client from the same tag |
| Spring `springdoc` `/v3/api-docs` | Optional **dev** convenience only. Never the published contract. |

Do **not** treat Spring `springdoc` `/v3/api-docs` as the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Document | OpenAPI 3.1 (`info.version` `0.1.0`). **Landed:** `$ref` tree plus a **checked-in** consumer bundle `openapi/bundled.yaml` ([gym-buddy-openapi#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/5) / ticket **#40** Done; `develop` **`7fa5108`**). Branch `feature/40-openapi-split` is gone. Editors edit the `$ref` tree. Consumers generate from **`openapi/bundled.yaml`**. Do **not** edit the bundle as source. | Full `/api/v1`. Same packaging: edit the `$ref` tree; keep `openapi/bundled.yaml` current. |
| Health | `GET /api/v1/healthz` (`getHealthz`) and `GET /api/v1/readyz` (`getReadyz`) — spec **and** service | `GET /api/v1/healthz` and `GET /api/v1/readyz` |
| Auth | Same four operations as before (`postAuthRegister`, `postAuthLogin`, `postAuthRefresh`, `postAuthLogout`; openapi #4 / ticket #12). UI on `develop` has `/register`, `/login`, and a log-out control that call register / login / logout (ui #3). Service on `develop` implements them (service #5 / `e2ef2aa`). Ticket #12 is closed. Refresh cookie stays `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. | Same four operations, plus the rest of `/api/v1` |
| `gym-buddy-service` | Handwritten Java DTOs and controllers. **No** `openapi-generator` (or equivalent) at build. `pom.xml` is not yet a consumer of the spec. Ticket **#41**. | Generates models + API interfaces from **`openapi/bundled.yaml`** at build. Controllers **implement** those generated interfaces. `pom.xml` is the consumer, **not** a second contract. Do **not** commit hand-edited generated sources. |
| `gym-buddy-ui` | Handwritten `src/app/api/models.ts` + `auth-api.service.ts`. **No** orval / openapi-typescript (or equivalent) at build. Ticket **#42**. | Generates the TypeScript client/types from **`openapi/bundled.yaml`** at build (orval or openapi-typescript). Consume the OpenAPI **repo / tag / bundle**. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. |
| Codegen | **Not landed.** Do not write that the service or UI already generate from the spec. | Build-time generation in both consumers (tickets **#41** / **#42**). |

Locked health paths: [01-API-conventions.md](01-API-conventions.md). The service implements `healthz` / `readyz` on `develop`. Public contract is not `/actuator/health`.

The six routes / operationIds on `develop` **`7fa5108`** (server prefix `/api/v1`; same as before the split):

| Method | Path | operationId | Notes (spec **and** service on `develop`) |
| --- | --- | --- | --- |
| `GET` | `/api/v1/healthz` | `getHealthz` | Liveness. Unauthenticated. |
| `GET` | `/api/v1/readyz` | `getReadyz` | Readiness. Unauthenticated. |
| `POST` | `/api/v1/auth/register` | `postAuthRegister` | Body: `email`, `handle`, `password`, `displayName`. Creates the user. No tokens. |
| `POST` | `/api/v1/auth/login` | `postAuthLogin` | Body: `{ email, password }` → access JWT in JSON + `Set-Cookie` refresh. Access is not a cookie. |
| `POST` | `/api/v1/auth/refresh` | `postAuthRefresh` | Cookie only → new access, rotated refresh `jti`. |
| `POST` | `/api/v1/auth/logout` | `postAuthLogout` | Revokes refresh `jti` in Redis denylist; clears cookie. |

This page is still the contract source of truth. The service on `develop` implements those four auth operations (service #5 / `e2ef2aa`). Ticket #12 is closed. Those operations run on the VPS container (`develop` **`aea1c56`**). Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Refresh cookie stays `SameSite=Lax`. Ticket **#40** is **Done**. Tickets **#41** / **#42** have **not** landed.

## Locked rules

1. `gym-buddy-openapi` owns routes, operations, request/response bodies, and entities. Service and UI consume that document. They do **not** invent a parallel contract in Java or TypeScript.
2. Do **not** treat Spring `springdoc` `/v3/api-docs` as the published contract (dev convenience only).
3. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. Consume the OpenAPI repo, a tag, or **`openapi/bundled.yaml`**.
4. **Today** the OpenAPI repo **is** a multi-file `$ref` tree (entities / requests / responses / paths) plus a **checked-in** consumer bundle. Editors edit the `$ref` tree. Consumers generate from **`openapi/bundled.yaml`**. Do **not** treat the bundle as the editing source.
5. Target service: generate models + API interfaces at build from that bundle (ticket **#41**). Controllers implement the generated interfaces. `pom.xml` is the consumer, not a second contract. Do **not** commit hand-edited generated sources.
6. Target UI: generate the TypeScript client/types at build from that bundle (ticket **#42**; orval or openapi-typescript). Same bundle / tag as the service.
7. Documentation stays **`0.3.0`**. Application repos stay **`0.1.x`**. Ticket **#24** stays cancelled. Ticket **#37** stays **Not Ready**. Do **not** claim login-from-Pages. Ticket **#40** is **Done**. Do **not** reopen #36 / #38 / #39 / #43.

## Why not “just expose `/v3/api-docs`”

- The spec would exist only while Java is up
- Frontend CI would depend on a running server
- Accidental controller changes would silently rewrite the public API
- The instructor cannot review a contract that lives only in memory

A separate repo makes the contract a first-class deliverable, hostable on GitHub Pages next to this wiki.

## Workflow

This is the **target** order. Today step 2 (the `$ref` tree + checked-in bundle) **has landed**. Today step 3 is still handwritten consumption.

1. Ticket on this documentation repo, linking the relevant FS/TS page
2. Change the `$ref` tree in `gym-buddy-openapi` on a Gitflow `feature/#n-…` branch (`openapi/openapi.yaml` and the files it `$ref`s). Regenerate the checked-in **`openapi/bundled.yaml`**. Do not hand-edit the bundle as source.
3. Consume **`openapi/bundled.yaml`** from backend (OpenAPI Generator → Java models + API interfaces) and frontend (orval or openapi-typescript). Controllers implement the generated interfaces. The UI does **not** vendor a copy of the YAML. **Not landed** — tickets **#41** / **#42**.
4. Implement

Do not commit hand-edited generated sources.

## Versioning

The OpenAPI document’s `info.version` **is** the product public-API version (`0.y.z` until `1.0.0`). Today that number is **`0.1.0`**. See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md). Application repos stay on **`0.1.x`** until the documentation `0.3.0` foundation is done. This page does **not** bump either number.
