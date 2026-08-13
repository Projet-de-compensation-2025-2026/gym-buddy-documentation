# Functional specification conventions

| Field | Value |
| --- | --- |
| Status | Approved |

## Template

Each feature page contains:

1. Intent (one paragraph)
2. Actors
3. Requirements `FS-<AREA>-<nn>`
4. Business rules
5. Acceptance criteria (Given / When / Then or a checklist that tests can cite)
6. Error catalog
7. Links to technical, algorithm, and UML pages

## Visibility model

Used by profiles, posts, and events:

| Value | Who can see / join |
| --- | --- |
| `public` | Any authenticated member (visitors: read-only if the page says so) |
| `friends` | Accepted friends of the owner / organizer |
| `private` | Owner + explicitly accepted participants (events) or owner only (drafts) |

Staff (`moderator`, `admin`) can **see** hidden or private content in the back-office, not in the member feed.

## Shared error codes

| Code | HTTP | Meaning |
| --- | --- | --- |
| `UNAUTHENTICATED` | 401 | Missing / expired access token |
| `FORBIDDEN` | 403 | Authenticated but not allowed |
| `NOT_FOUND` | 404 | Missing **or** hidden from this caller (no existence leak) |
| `CONFLICT` | 409 | Duplicate friendship, double apply, … |
| `VALIDATION` | 422 | Payload fails schema |
| `RATE_LIMITED` | 429 | Abuse control |
| `PAYLOAD_TOO_LARGE` | 413 | Media over quota |

## Writing rules

- Requirements are testable. Avoid “the system should be user-friendly”.
- Do not prescribe CSS.
- If a number is a product decision (max comment depth, max event capacity), put it in the feature page and reference it from tests.
