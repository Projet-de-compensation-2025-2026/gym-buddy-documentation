# Current analysis

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

This page is updated after implementation. It already records **design-level** strengths and weaknesses so the report is not written the night before the defense.

## Strengths

- The product goal is narrow and demoable: find a buddy, train together.
- A modular monolith matches a one-person team and still shows Software Engineering structure.
- Suggestions (explainable scoring) and matching (constrained assignment) are distinct algorithms — not one fuzzy “AI” slide.
- Object storage + signed URLs answers the brief’s storage and security items directly.
- Spec IDs give tests and the report a traceability story.
- Two clients (member + back-office) satisfy the implementation triad without a mobile program.
- The live API already has a pipeline (CI → Release → GHCR → `replace.sh`) and a named host (`vps-c39cdf03.vps.ovh.net`) behind Caddy.
- Local compose boots on a laptop: Postgres 18.6, Redis, MinIO, and the Java 25 LTS Spring API answer `healthz` / `readyz` 200 (`docs/local-compose-proof.md` on `gym-buddy-service` `develop`).

## Weaknesses

- TypeScript 7.0 is new (Go native compiler, July 2026). Angular 22 may trail it by a patch; that gap is a tooling risk, not a product one.
- GitHub Pages cannot host the Java API or PostgreSQL. The API runs on the OVH VPS; 443 is limited to the operator network, so a stranger cannot open the demo URL without that prefix on UFW.
- JWT HS256 + Redis denylist is not an identity platform (no step-up auth, no device list).
- Nested comments capped at depth 4 and stored `depth` will need a migration if the cap changes.
- Greedy matching is a 1/2-approximation; we do not yet show empirical gap vs exact.
- Search quality on messy city strings will be poor without geocoding.
- Instant messaging is not E2E encrypted; staff can read plaintext in the DB.
- Large fixtures with shared image keys make the demo look repetitive.
- Angular 22 auth pages exist on `develop` (ui #3). Service auth is on `develop` (service #5 / `e2ef2aa`): `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout`. Ticket #12 is closed / Done. Do not write a completed register/login on the VPS. Local compose is proven on a laptop. VPS apply is **done**. Ticket **#20** is **Done / closed**. VPS container is `develop` **`e2ef2aa`** (Kernel rebuilt from develop **`e2ef2aa`** after apply; not still only `:local`). Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`. API bind `127.0.0.1`; data-plane ports unpublished. A bad `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. Caddy is not proven. Flyway on `develop` is V1 + V2 (`users` + `profiles`).

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Scope creep (groups, stories, live GPS) | Miss 31 Aug 2026 | Out-of-scope list in `00-Project-brief` |
| Recurrence edge cases (DST, exceptions) | Buggy events | Support WEEKLY + UNTIL only at MVP |
| Race on event capacity | Oversell seats | Transaction + `SELECT FOR UPDATE` |
| Private data leaks in search | Failed security story | Integration tests listed in the plan |
| Single student bus factor | No backup | Wiki is the backup: another engineer could implement from it |
| Certificate renewal while 443 is firewalled | HTTPS expires | Open port 80 briefly for HTTP-01, then deny it again |

## Academic honesty

Do not claim machine learning if we ship weighted sums. The justification pages exist so the defense can be precise. `gym-buddy-service` `develop` is Java 25 LTS / Spring Boot (`pom.xml`) and implements register / login / refresh / logout (service #5 / `e2ef2aa`). Ticket #12 is closed / Done. VPS apply is **done**. Ticket **#20** is **Done / closed**. The VPS container is `develop` **`e2ef2aa`** (Kernel rebuilt from develop **`e2ef2aa`** after apply; not still only `:local`). Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`. A bad `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist; **not** a completed register/login). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull, a Release tag, or a successful replace-from-registry. Do not claim Caddy is proven. Local laptop compose is proven (`docs/local-compose-proof.md`).
