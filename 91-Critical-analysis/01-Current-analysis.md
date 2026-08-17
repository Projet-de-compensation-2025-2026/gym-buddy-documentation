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

## Weaknesses

- Java 26 is the latest GA but not the LTS (that is 25). A library may force a temporary pin to 25.
- TypeScript 7.0 is new (Go native compiler, July 2026). Angular 22 may trail it by a patch; that gap is a tooling risk, not a product one.
- GitHub Pages cannot host the Java API or PostgreSQL. The API runs on the OVH VPS; 443 is limited to the operator network, so a stranger cannot open the demo URL without that prefix on UFW.
- JWT HS256 + Redis denylist is not an identity platform (no step-up auth, no device list).
- Nested comments capped at depth 4 and stored `depth` will need a migration if the cap changes.
- Greedy matching is a 1/2-approximation; we do not yet show empirical gap vs exact.
- Search quality on messy city strings will be poor without geocoding.
- Instant messaging is not E2E encrypted; staff can read plaintext in the DB.
- Large fixtures with shared image keys make the demo look repetitive.
- The service is still a Python probe. Spring, compose, and Angular are not started.

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

Do not claim machine learning if we ship weighted sums. The justification pages exist so the defense can be precise. Do not claim Spring is in production while the probe image is what Deploy ships.
