# Current analysis

| Field | Value |
| --- | --- |
| Status | Proposed |
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

- Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed). Approved and today is TypeScript **6** (`~6.0.2`). Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on TypeScript `~6.0.2` until Angular actually supports 7. `typescript@7.0.0` is 404 and **7.0.2** cannot land (`ts.readConfigFile is not a function`). That is why the slice was dropped, not a deferred target. Do **not** claim TypeScript 7 landed.
- GitHub Pages cannot host the Java API or PostgreSQL. The API runs on the OVH VPS; 443 is limited to the operator network, so a stranger cannot open the demo URL without that prefix on UFW.
- JWT HS256 + Redis denylist is not an identity platform (no step-up auth, no device list).
- Nested comments capped at depth 4 and stored `depth` will need a migration if the cap changes.
- Greedy matching is a 1/2-approximation; we do not yet show empirical gap vs exact.
- Search quality on messy city strings will be poor without geocoding.
- Instant messaging is not E2E encrypted; staff can read plaintext in the DB.
- Large fixtures with shared image keys make the demo look repetitive.
- Angular 22 auth pages exist on `develop` (ui #3). Service auth is on `develop` (service #5 / `e2ef2aa`): `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout`. Ticket #12 is closed / Done. Local compose is proven on a laptop. VPS apply is **done**. Ticket **#20** is **Done / closed**. VPS Java container on the host is `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`. API bind `127.0.0.1`; data-plane ports unpublished. A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. Caddy is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Ticket **#37** is **closed / completed**. Do **not** claim login-from-Pages. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**. First tag **v0.1.0** pointed at localhost. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. Ticket **#31** is **Done / closed**. Ticket **#37** is **closed / completed**. Do **not** claim login-from-Pages. Do **not** Todo **#37**. Flyway on `develop` is V1 + V2 (`users` + `profiles`).

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

Do not claim machine learning if we ship weighted sums. The justification pages exist so the defense can be precise. `gym-buddy-service` `develop` is Java 25 LTS / Spring Boot (`pom.xml`) and implements register / login / refresh / logout (service #5 / `e2ef2aa`). Ticket #12 is closed / Done. VPS apply is **done**. Ticket **#20** is **Done / closed**. The VPS Java container on the host is `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`. A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull, a Release tag, or a successful replace-from-registry. Caddy is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Ticket **#37** is **closed / completed**. Do **not** claim login-from-Pages. Ticket **#31** is **Done / closed**. Ticket **#37** is **closed / completed**. Do **not** claim login-from-Pages. Do **not** Todo **#37**. Local laptop compose is proven (`docs/local-compose-proof.md`).
