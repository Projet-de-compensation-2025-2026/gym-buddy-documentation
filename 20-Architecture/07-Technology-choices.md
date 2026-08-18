# Technology choices

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-Software-architecture.md](01-Software-architecture.md), [08-Hosting-and-GitHub-Pages.md](08-Hosting-and-GitHub-Pages.md), [../91-Critical-analysis/01-Current-analysis.md](../91-Critical-analysis/01-Current-analysis.md) |

The brief requires **justification** of languages, frameworks, and libraries. Language and client/server split below are **decided**. Library versions are the latest stable as of 13 August 2026; pin exact builds in each application repo.

## Decision summary

| Concern | Choice | Why this, not the alternative |
| --- | --- | --- |
| Backend language | **Java 25 LTS** | Course-friendly, strong typing for algorithms and JWT, long toolchain. Current LTS; Joaquim chose 25 LTS for stability. Java 27 is not released yet (expected September 2026). |
| Backend framework | **Spring Boot** (latest stable that supports the chosen JDK) | Modules, Spring Security for JWT, JDBC/JPA, WebSocket, Actuator health. The HTTP contract is **not** owned by Spring’s `/v3/api-docs` endpoint — see OpenAPI below. |
| Frontend language | **TypeScript 7.0.0** (July 2026 Go-native compiler / Project Corsa; [announcement](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)) | Approved. Install from the `typescript` npm package — `tsc` is the Go binary. Do **not** install `@typescript/native-preview` or treat `tsgo` as the project compiler. Today `gym-buddy-ui` `develop` is still TypeScript `~6.0.2`; that is not the target. |
| Node package manager | **pnpm** (Corepack pin, not `latest`) | Required for `gym-buddy-ui` and any Node work. Stop using npm as the project package manager. Four-week release-age floor: `minimumReleaseAge: 40320` (**minutes**) in `pnpm-workspace.yaml`. Older pnpm fallback: `.npmrc` `minimum-release-age=40320`. Do **not** invent a `package.json` field — pnpm does not read the floor from there. Commit `pnpm-lock.yaml`. Disable or tightly allow lifecycle scripts (`onlyBuiltDependencies` and/or ignore-scripts). Today the UI on `develop` is **`pnpm@11.22.0`** (ui #4 / `63bebed`; committed lockfile; `minimumReleaseAge` **40320**). |
| Member UI | **Angular 22** (22.1.x as of August 2026) | Latest Angular; official TypeScript SPA; static `ng build` output can go to GitHub Pages. |
| Back-office | **Angular 22**, second app (or `/admin`) **in the frontend repo** | Same stack as the member app. Not a fourth repository. Staff JS stays in a separate bundle. |
| HTTP contract | **OpenAPI 3** in its **own repository** (`gym-buddy-openapi`) | Source of truth is a versioned spec, not a live endpoint the backend happens to expose. Backend *implements* the spec; frontend *generates* a client from it. |
| Database | **PostgreSQL 18** (18.6 as of 13 August 2026) | Latest **stable** major. PostgreSQL 19 is still beta — do not use it for the project. Arrays, JSON, full-text, constraints, radius search. |
| Cache | **Redis** | Refresh denylist, rate limit, suggestion cache |
| Object storage | **MinIO** locally (S3 API) | Satisfies “do not fill local disk”; production can point at real S3/R2 |
| Auth | **JWT** access + refresh (assignment) | Spring Security + Nimbus JOSE or JJWT; Argon2id for passwords |
| Realtime | **Spring WebSocket** + HTTP fallback | Enough for private chat |
| Validation | **Jakarta Bean Validation** (backend); TypeScript types from OpenAPI (frontend) | One contract, two generated surfaces |
| Persistence | **Flyway** + **Spring Data JPA** (Hibernate) | Versioned SQL migrations; JPA for the domain. Raw SQL allowed for search/ranking. |
| Tests | **JUnit 5** + AssertJ + Testcontainers (backend); Angular unit runner + **Playwright** (functional) | Matches the Java / Angular split |
| Fixtures | **Datafaker** + factory classes | Thousands of rows, deterministic seed |
| Images | Thumbnailator / ImageIO in a worker | Variants without keeping originals on the API disk |
| Recurrence | `org.dmfs:lib-recur` or ical4j (RRULE) | Recurring events |
| Logging | SLF4J + Logback | Spring default, structured JSON in deploy |

## Repositories (decided)

| Repository | Stack |
| --- | --- |
| `gym-buddy-documentation` | Markdown wiki (this repo), GitHub Pages |
| `gym-buddy-service` | Java 25 LTS + Spring Boot + PostgreSQL 18 |
| `gym-buddy-ui` | **Approved:** Angular 22 + TypeScript 7.0.0 + pnpm. **Today on `develop`:** Angular 22 + TypeScript `~6.0.2` + **`pnpm@11.22.0`** (ui #4 / `63bebed`). Ticket **#24** is the TS 7.0.0 follow-up |
| `gym-buddy-openapi` | OpenAPI 3 documents + static reference UI |

There is no separate back-office repository and no “the spec is whatever the running server prints”.

## Alternatives considered and rejected

| Rejected | Reason |
| --- | --- |
| NestJS / Node backend | Decided: Java |
| Next.js / React member UI | Decided: Angular |
| Serving OpenAPI only from a running `/v3/api-docs` | The contract would exist only when the server is up and could drift from git. A dedicated repo is reviewable, versioned, and hostable on Pages |
| MongoDB as system of record | Friend graph, event constraints, nested comments are relational |
| Local `uploads/` folder | Directly contradicts the brief |
| Auth0 / Cognito | Hides the JWT work the brief asks to implement |
| PostgreSQL 19 beta | Not stable |
| Elasticsearch at MVP | PostgreSQL filters + FTS cover parameterized search |

## How this maps to the three modules

| Module | Evidence in the stack |
| --- | --- |
| Software Engineering | Modular Spring app, Flyway schema, Gitflow, SemVer, tickets → wiki |
| Web Technologies | REST from a published OpenAPI, JWT, WebSocket, Angular, signed media |
| Algorithms | Suggestion scoring, filtered ranking, matching — implemented in Java, unit-tested, no hidden SaaS |

## Changing a choice

1. Update this page (status, rationale, date).
2. Add a line under `Changed` in [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md).
3. Touch every spec that named the old library.
