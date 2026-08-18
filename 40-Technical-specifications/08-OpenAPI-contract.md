# OpenAPI contract

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-API-conventions.md](01-API-conventions.md), [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md), [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md) |

The HTTP API is specified in a **dedicated repository**, not discovered from a running backend.

**Repository:** https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi (private, default branch `develop`)

`gym-buddy-openapi` is the source of truth for **all** API: routes, operations, request/response contracts, and entities. `gym-buddy-service` and `gym-buddy-ui` **consume** that contract. They do **not** re-implement it. That is the locked target. The **next** locked target (not landed today): `gym-buddy-openapi` is a **versioned package** that `gym-buddy-service` and `gym-buddy-ui` depend on. Generators read the `$ref` tree (`openapi/openapi.yaml`), **not** a second checked-in `bundled.yaml`. OpenAPI must be **tagged**. Consumers pin a **tag/version**, not a raw develop SHA GET. Drop dual maintenance: the tree is the edit format; the package/checkout is how consumers see it. `bundled.yaml` is **no longer** the consumer source of truth. **Today** `gym-buddy-ui` generates the TypeScript client/types at build with **orval 8.22.0** from `gym-buddy-openapi@7fa5108` `openapi/bundled.yaml` (ui #10 / ticket **#42** Done; `develop` **`b8da6bf`**). Branch `feature/42-openapi-client` is gone. `AuthApi` is a thin wrapper; login / refresh / logout keep `withCredentials`. There is **no** `openapi.yaml` (or any YAML copy) in the UI tree. **Today** `gym-buddy-service` `generate-sources` fetches `openapi/bundled.yaml` from `gym-buddy-openapi` `develop` / **`7fa5108`** (service #10 / ticket **#41** Done; `develop` **`c40f122`**). Branch `feature/41-openapi-codegen` is gone. `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite unchanged. `pom.xml` stays **0.2.0-SNAPSHOT**. **Today** OpenAPI git tag **v0.1.0** exists (`info.version` `0.1.0`; ticket **#46** Done). Spring `springdoc` `/v3/api-docs` is still **not** the source of truth.

## Source of truth

| Artifact | Role |
| --- | --- |
| `gym-buddy-openapi` (git) | Canonical contract. Reviewed, tagged, SemVer’d. |
| `$ref` tree (`openapi/openapi.yaml` + paths / components) | **Edit source.** Editors change this tree, not a bundle. **Target:** generators read this tree. |
| `openapi/bundled.yaml` | **Today** (ticket **#40** Done): checked-in consumer document. Service and UI still generate from this file. **Not** the target consumer source of truth. |
| Versioned package / git tag | **Target:** how service and UI depend on the contract. Pin a tag/version, not a raw develop SHA GET. **Today:** git tag **v0.1.0** exists (ticket **#46** Done). |
| Static Swagger UI / Redoc on GitHub Pages | Human-readable copy of a **tag** |
| Backend | Implements the tagged spec; contract tests fail the build on drift |
| Frontend | Generates a TypeScript client from the same tag |
| Spring `springdoc` `/v3/api-docs` | Optional **dev** convenience only. Never the published contract. |

Do **not** treat Spring `springdoc` `/v3/api-docs` as the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

## Today versus target

| | Today | Target |
| --- | --- | --- |
| Document | OpenAPI 3.1 (`info.version` `0.1.0`). **Landed:** `$ref` tree plus a **checked-in** consumer bundle `openapi/bundled.yaml` ([gym-buddy-openapi#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/5) / ticket **#40** Done; `develop` **`7fa5108`**). Branch `feature/40-openapi-split` is gone. Editors edit the `$ref` tree. Consumers generate from **`openapi/bundled.yaml`**. Do **not** edit the bundle as source. Git tag **v0.1.0** exists (ticket **#46** Done). | `gym-buddy-openapi` is a **versioned package**. Generators read the `$ref` tree (`openapi/openapi.yaml`), **not** a second checked-in `bundled.yaml`. OpenAPI must be **tagged**. Consumers pin a **tag/version**, not a raw develop SHA GET. Drop dual maintenance: the tree is the edit format; the package/checkout is how consumers see it. `bundled.yaml` is **no longer** the consumer source of truth. Full `/api/v1`. |
| Health | `GET /api/v1/healthz` (`getHealthz`) and `GET /api/v1/readyz` (`getReadyz`) — spec **and** service | `GET /api/v1/healthz` and `GET /api/v1/readyz` |
| Auth | Same four operations as before (`postAuthRegister`, `postAuthLogin`, `postAuthRefresh`, `postAuthLogout`; openapi #4 / ticket #12). UI on `develop` has `/register`, `/login`, and a log-out control that call register / login / logout (ui #3). Service on `develop` implements them (service #5 / `e2ef2aa`). Ticket #12 is closed. Refresh cookie stays `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. | Same four operations, plus the rest of `/api/v1` |
| `gym-buddy-service` | **Landed:** `generate-sources` fetches `openapi/bundled.yaml` from `gym-buddy-openapi` `develop` / **`7fa5108`** ([gym-buddy-service#10](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/10) / ticket **#41** Done; `develop` **`c40f122`**). Branch `feature/41-openapi-codegen` is gone. `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite unchanged. `pom.xml` stays **0.2.0-SNAPSHOT**. | Depends on the versioned `gym-buddy-openapi` **package / tag**. Generates models + API interfaces from the `$ref` tree (`openapi/openapi.yaml`) at build — **not** `bundled.yaml`, **not** a raw develop SHA GET. Controllers **implement** those generated interfaces. `pom.xml` is the consumer, **not** a second contract. Do **not** commit generated sources. |
| `gym-buddy-ui` | **Landed:** generates the TypeScript client/types at build with **orval 8.22.0** from `gym-buddy-openapi@7fa5108` `openapi/bundled.yaml` ([gym-buddy-ui#10](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui/pull/10) / ticket **#42** Done; `develop` **`b8da6bf`**). Branch `feature/42-openapi-client` is gone. `AuthApi` is a thin wrapper; login / refresh / logout keep `withCredentials`. **No** `openapi.yaml` (or any YAML copy) in the UI tree. App version stays **0.1.0**. TypeScript stays **`~6.0.2`**. | Depends on the versioned `gym-buddy-openapi` **package / tag**. Generates the TypeScript client/types from the `$ref` tree (`openapi/openapi.yaml`) at build (orval). Pin a tag/version. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. |
| Codegen | **Both landed** from **`openapi/bundled.yaml`**. UI: **orval 8.22.0** / ticket **#42** Done (`develop` **`b8da6bf`**). Service: `generate-sources` / ticket **#41** Done (`develop` **`c40f122`**). Generated Java sources are **not** committed. | Build-time generation in both consumers from the versioned package / tag `$ref` tree (`openapi/openapi.yaml`). |

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

This page is still the contract source of truth. The service on `develop` implements those four auth operations (service #5 / `e2ef2aa`; codegen wrapper is service #10 / **`c40f122`**). Ticket #12 is closed. Those operations run on the VPS container (`develop` **`aea1c56`**). Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Refresh cookie stays `SameSite=Lax` (unchanged). Ticket **#40** is **Done**. Ticket **#41** is **Done**. Ticket **#42** is **Done**. Ticket **#46** is **Done**. Do **not** un-Done them. Git tag **v0.1.0** exists. The versioned **package** / `$ref`-tree consumer slice (ticket **#47** In Progress, **#48** Not Ready) has **not** landed.

## Locked rules

1. `gym-buddy-openapi` owns routes, operations, request/response bodies, and entities. Service and UI consume that document. They do **not** invent a parallel contract in Java or TypeScript.
2. Do **not** treat Spring `springdoc` `/v3/api-docs` as the published contract (dev convenience only).
3. Do **not** copy or vendor `openapi.yaml` into `gym-buddy-ui`. **Today** consume **`openapi/bundled.yaml`** (tickets **#41** / **#42** Done). **Target:** consume the versioned **package / tag**; generators read `openapi/openapi.yaml`.
4. **Today** the OpenAPI repo **is** a multi-file `$ref` tree (entities / requests / responses / paths) plus a **checked-in** consumer bundle. Editors edit the `$ref` tree. Consumers generate from **`openapi/bundled.yaml`**. Do **not** treat the bundle as the editing source. **Target:** drop dual maintenance. The tree is the edit format; the package/checkout is how consumers see it. `bundled.yaml` is **no longer** the consumer source of truth.
5. **Today** the service generates models + API interfaces at build from that bundle (ticket **#41** Done; `generate-sources` fetches `gym-buddy-openapi` `develop` / **`7fa5108`**; service `develop` **`c40f122`**). `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. `pom.xml` is the consumer, not a second contract. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite unchanged. `pom.xml` stays **0.2.0-SNAPSHOT**. **Target:** depend on the versioned package / tag; generate from `openapi/openapi.yaml`.
6. **Today** the UI generates the TypeScript client/types at build from that bundle with **orval 8.22.0** (ticket **#42** Done; `gym-buddy-openapi@7fa5108` `openapi/bundled.yaml`; `develop` **`b8da6bf`**). `AuthApi` is a thin wrapper; login / refresh / logout keep `withCredentials`. Same bundle / SHA as the service. Do **not** copy or vendor YAML into the UI. **Target:** depend on the versioned package / tag; generate from `openapi/openapi.yaml`.
7. **Today** git tag **v0.1.0** exists (`info.version` `0.1.0`; ticket **#46** Done). **Target:** consumers pin that **tag/version**, not a raw develop SHA GET — not landed until **#47** / **#48**.
8. Documentation stays **`0.3.0`**. Application repos stay **`0.1.x`**. Service `pom.xml` stays **0.2.0-SNAPSHOT**. Ticket **#24** stays cancelled. Ticket **#37** stays **Not Ready**. Do **not** claim login-from-Pages. Ticket **#40** is **Done**. Ticket **#41** is **Done**. Ticket **#42** is **Done**. Ticket **#46** is **Done**. Do **not** reopen #36 / #38 / #39 / #43 / #44 / #45.

## Why not “just expose `/v3/api-docs`”

- The spec would exist only while Java is up
- Frontend CI would depend on a running server
- Accidental controller changes would silently rewrite the public API
- The instructor cannot review a contract that lives only in memory

A separate repo makes the contract a first-class deliverable, hostable on GitHub Pages next to this wiki.

## Workflow

This is the **target** order. Today step 2 (the `$ref` tree + checked-in bundle) **has landed** (ticket **#40** Done). Today step 3 from **`openapi/bundled.yaml`**: UI **has landed** (orval 8.22.0 / ticket **#42** Done). Service **has landed** (`generate-sources` / ticket **#41** Done). Git tag **v0.1.0** exists (ticket **#46** Done). The **next** slice is the versioned package + generate from the `$ref` tree (ticket **#47** In Progress, **#48** Not Ready). That consumer slice has **not** landed. Expanding `/api/v1` past health + auth is also still open.

1. Ticket on this documentation repo, linking the relevant FS/TS page
2. Change the `$ref` tree in `gym-buddy-openapi` on a Gitflow `feature/#n-…` branch (`openapi/openapi.yaml` and the files it `$ref`s). **Today** also regenerate the checked-in **`openapi/bundled.yaml`** because consumers still read it. Do not hand-edit the bundle as source. **Target:** no second consumer document; the package/checkout is how consumers see the tree.
3. **Today** consume **`openapi/bundled.yaml`** from backend (OpenAPI Generator → Java models + API interfaces) and frontend (orval). **UI landed** — ticket **#42** Done (`develop` **`b8da6bf`**). **Service landed** — ticket **#41** Done (`develop` **`c40f122`**). Generated Java sources are **not** committed. **Target:** depend on the versioned package / tag; generate from `openapi/openapi.yaml`. Controllers implement the generated interfaces. The UI does **not** vendor a copy of the YAML.
4. Implement

Do not commit hand-edited generated sources.

## Versioning

The OpenAPI document’s `info.version` **is** the product public-API version (`0.y.z` until `1.0.0`). Today that number is **`0.1.0`**. `package.json` is also **`0.1.0`**. **Today** git tag **v0.1.0** exists (the only OpenAPI tag; annotated **`6373a11`** points to **`9c7c123`** on `main`, `release: v0.1.0`; `develop` tip **`5285b7c`**, `chore(release): sync develop with v0.1.0`; ticket **#46** Done; Sentinel confirmed). **Target:** consumers pin that tag/version — not landed until **#47** / **#48**. See [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md). Application repos stay on **`0.1.x`** until the documentation `0.3.0` foundation is done. Service `pom.xml` stays **0.2.0-SNAPSHOT**. This page does **not** bump either number.
