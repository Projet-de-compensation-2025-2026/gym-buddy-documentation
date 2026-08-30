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
- Each feature page lists **target HTTP operations** (paths relative to `/api/v1`). The YAML in `gym-buddy-openapi` is still the machine-readable source of truth; the table is what Kernel must add there. Canonical inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md).
- Cite the mockup file under [../20-Architecture/mockups/](../20-Architecture/mockups/). Mockups may contain Stitch leftovers (Billing, Notifications as a product, workout tracking, video posts, admin Bookings / Analytics / Invite User / Export CSV / + New Session). **Implement only surfaces that have an FS ID.** Do not invent entities from leftover chrome.
- After OpenAPI for a slice lands on `develop`, consumers pin a new **0.1.x** tag (or the new `develop` SHA only until that tag exists). Do **not** invent `1.0.0`. Do **not** restore `openapi/bundled.yaml`. Do **not** treat `springdoc` `/v3/api-docs` as truth.
