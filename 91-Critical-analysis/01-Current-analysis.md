# Current analysis

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

This page is updated after implementation. Product tickets **#59–#70** are on `develop` (auth, profiles, friends, media, posts, comments, feed, events, search, suggestions, messaging, admin, fixtures). Academic pack **#71** captured live v1.1.0 UI on 2026-08-31.

## Post-implementation (2026-08-31, live v1.1.0)

What shipped matches the wiki: OpenAPI `$ref` tree first, generated Java interfaces and orval client, Gitflow PRs to `develop`, FS-named tests, Datafaker seed `20260813`. Application tag **v1.1.0** is live on GitHub Pages (known member and admin routes HTTP 200). Create-account + sign-in from `github.io` works (ticket **#37** stays closed). Refresh cookie is `HttpOnly; Secure; SameSite=None; Partitioned` so Chromium stores it in the Pages partition (ticket **#89**).

Gaps that remain honest after that Release:

- **Staff bootstrap (#78) was not SSH-run.** `demo.admin` / `demo.mod` are missing on prod. Academic shots 15–16 (role change + audit, hidden post) could not be taken. Member login to `/admin/login` correctly returns “Staff accounts only.”
- **Object storage is not configured on the VPS.** `POST /api/v1/media` and `GET /media/{id}/url` return 401 `UNAUTHENTICATED` / `media is not configured`. Chat image/audio and post images fail; fail-closed ACL still shows “post not found” to a stranger on a friends-only post.
- **Prod fixtures are off** (`POST /admin/fixtures` stays `FORBIDDEN` on `prod`). Suggestions for three live users were empty (FS-SUGG-07 recompute is async / nightly; no 3 000-user graph).
- Greedy matching is not exact; DMs are not E2E; staff could read plaintext if messaging persisted.

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
- Large fixtures with shared image keys make the demo look repetitive **when fixtures run**. Live prod has **no** 3 000-user seed, so the demo graph is whatever members register.
- Live Pages is **v1.1.0**. Register / login / feed / friends / events / search / messages work from this operator PC. CORS + `SameSite=None; Partitioned` is what made the session stick after v1.0.0’s `SameSite=Lax` drop. Ticket **#37** stays **closed**. Do **not** Todo **#37**.
- VPS object storage is **not** serving signed uploads (`media is not configured`). MinIO is in the architecture; the live host does not yet mint 60 s URLs.
- Flyway on `develop` includes the domain tables past V2; prod still cannot reset fixtures.

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

Do not claim machine learning if we ship weighted sums. The justification pages exist so the defense can be precise. Live **v1.1.0** is a tagged product: Pages + VPS Caddy `healthz` **200** from the operator network, register **201**, login **200**. Ticket **#37** is **closed / completed**. Do **not** Todo **#37**. Do not claim staff fixtures or MinIO signed URLs on prod until #78 is applied and object storage is configured. Local laptop compose is proven (`docs/local-compose-proof.md`).
