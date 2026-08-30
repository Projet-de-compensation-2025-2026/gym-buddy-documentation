# Target HTTP surface (remaining product)

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-API-conventions.md](01-API-conventions.md), [08-OpenAPI-contract.md](08-OpenAPI-contract.md), [../30-Functional-specifications/00-Conventions.md](../30-Functional-specifications/00-Conventions.md) |

Paths are relative to `/api/v1`. **Today** the `$ref` tree only documents health + auth (`register` / `login` / `refresh` / `logout`). This page is the remaining contract Kernel must add to `gym-buddy-openapi` (`openapi/openapi.yaml` + path/component files). It is **not** a second source of truth once the YAML exists — if they disagree, fix both in the same ticket.

Shared rules: JSON, Bearer access JWT, cursor pagination envelope, error envelope, `Idempotency-Key` on creating POSTs — [01-API-conventions.md](01-API-conventions.md). Fail closed: missing ACL → `NOT_FOUND` (no existence leak) unless a row already says `FORBIDDEN`.

## Consuming a new contract

Consumers currently pin gym-buddy-openapi tag **v0.1.0**. After an OpenAPI feature PR merges to `develop`:

1. Cut a new **0.1.x** OpenAPI tag via Release **or**, if Release cannot run yet, temporarily pin the new `develop` SHA.
2. Point `gym-buddy-service` and `gym-buddy-ui` at that pin and regenerate.
3. Controllers implement generated interfaces. The UI uses the orval client. Do **not** vendor YAML. Do **not** commit generated Java sources.
4. Application versions stay **0.1.x**. Service `pom.xml` stays **0.2.0-SNAPSHOT** until Release writes it. Do **not** invent **1.0.0**. Do **not** restore `openapi/bundled.yaml`.

## Accounts (leftover after ticket #12)

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `POST` | `/auth/password` | FS-ACCT-05 | Body `{ currentPassword, newPassword }`. Revoke other refresh `jti`s. |
| `POST` | `/me/close` | FS-ACCT-07 | Body `{ password }`. Sets `users.status=closed`. Login afterwards is generic `FORBIDDEN`. Staff may restore via unlock. Mockup copy “recover by logging back in” is **not** the contract. |

Register / login / refresh / logout already exist. Do not reticket them.

## Profiles

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/profiles/me` | FS-PROF-01 | Owner, full profile. |
| `PATCH` | `/profiles/me` | FS-PROF-06 | Owner. Handle change must stay unique (FS-ACCT-02). |
| `GET` | `/profiles/{handle}` | FS-PROF-03/04 | Stranger on `private` → stub only. Login required (FS-PROF-05). |

## Friends

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/friendships` | FS-FRND-07 | Query `filter=accepted\|incoming\|outgoing`. Owner + friends may list accepted. |
| `POST` | `/friendships` | FS-FRND-01 | Body `{ handle }` or `{ userId }`. |
| `POST` | `/friendships/{id}/accept` | FS-FRND-02 | Addressee only. |
| `POST` | `/friendships/{id}/decline` | FS-FRND-02 | Addressee only. |
| `DELETE` | `/friendships/{id}` | FS-FRND-03/04 | Cancel pending (requester) or unfriend (either). |
| `POST` | `/blocks` | FS-FRND-05 | Body `{ userId }`. |
| `DELETE` | `/blocks/{userId}` | FS-FRND-05 | Unblock. |

## Posts, likes, reposts

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `POST` | `/posts` | FS-POST-01 | Body + optional `mediaIds` (max 4). |
| `GET` | `/posts/{id}` | FS-POST-02 | Visibility. |
| `PATCH` | `/posts/{id}` | FS-POST-03 | Author, within 15 minutes. |
| `DELETE` | `/posts/{id}` | FS-POST-04 | Author soft-delete. |
| `POST` | `/posts/{id}/reposts` | FS-POST-05 | |
| `DELETE` | `/posts/{id}/reposts` | FS-POST-06 | Undo. |
| `PUT` | `/posts/{id}/like` | FS-POST-07 | Idempotent like. |
| `DELETE` | `/posts/{id}/like` | FS-POST-07 | Unlike. |
| `GET` | `/posts/{id}/likes` | FS-POST-08 | Author only for nominative list. |

## Nested comments

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/posts/{id}/comments` | FS-CMT-06 | Page of roots. |
| `POST` | `/posts/{id}/comments` | FS-CMT-01/02 | Optional `parentId`. |
| `GET` | `/comments/{id}/replies` | FS-CMT-06 | Expand thread. |
| `DELETE` | `/comments/{id}` | FS-CMT-05 | Author tombstone. |
| `PUT` | `/comments/{id}/like` | FS-CMT-07 | |
| `DELETE` | `/comments/{id}/like` | FS-CMT-07 | |

## Feed

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/feed` | FS-FEED-01..06 | Cursor `before`. Default size 20, max 50. |

## Events

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/events` | FS-EVT | Query: `kind=instant\|recurring`, window. Visibility-filtered. |
| `POST` | `/events` | FS-EVT-01..04 | Instant or `RRULE`. |
| `GET` | `/events/{id}` | FS-EVT-03 | Includes occurrences for 90 days + remaining seats. Organizer also gets matching rank of pending applicants (FS-EVT-13). |
| `PATCH` | `/events/{id}` | FS-EVT-09 | |
| `POST` | `/events/{id}/cancel` | FS-EVT-08 | Series or `occurrenceId`. |
| `POST` | `/events/{id}/applications` | FS-EVT-05 | Optional `occurrenceId`. |
| `DELETE` | `/applications/{id}` | FS-EVT-10 | Withdraw. |
| `POST` | `/applications/{id}/accept` | FS-EVT-06/07 | Transactional seat check. |
| `POST` | `/applications/{id}/decline` | FS-EVT-06 | |

## Search

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/search/people` | FS-SRCH-01..08 | Query params from [06-Search-implementation.md](06-Search-implementation.md). |
| `GET` | `/search/events` | FS-SRCH-01..08 | |

## Suggestions and matching

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/suggestions` | FS-SUGG-01..03 | Default 20, max 50. Each item has `reason`. |
| `POST` | `/suggestions/{userId}/dismiss` | FS-SUGG-04 | 30 days. |
| `POST` | `/matching/opt-in` | FS-MATCH-01 | Weekly buddy opt-in. |
| `DELETE` | `/matching/opt-in` | FS-MATCH-01 | |
| `GET` | `/matching/me` | FS-MATCH-02/03 | Current proposed pair / draft event if any. |

## Messaging

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `GET` | `/conversations` | FS-MSG-09 | Inbox, unread counts. |
| `POST` | `/conversations` | FS-MSG-01 | Body `{ userId }`. Friends only. Idempotent pair. |
| `GET` | `/conversations/{id}/messages` | FS-MSG-06 | Cursor `before`. |
| `POST` | `/conversations/{id}/messages` | FS-MSG-03..05 | `type=text\|image\|audio`. |
| `DELETE` | `/messages/{id}` | FS-MSG-08 | Sender, 10 minutes. |
| `GET` | `/ws` | FS-MSG-07 | WebSocket. See [05-Messaging-transport.md](05-Messaging-transport.md). |

## Media

| Method | Path | FS | Notes |
| --- | --- | --- | --- |
| `POST` | `/media` | FS-MED-02 | `{ kind, mime, bytes }` → `mediaId` + signed PUT. |
| `GET` | `/media/{id}/url` | FS-MED-07 | Short-lived signed GET after `canRead`. |
| `DELETE` | `/media/{id}` | FS-MED-08 | Owner; grace-delete object. |

## Admin / moderation

Prefix `/admin`. `role=moderator` or `admin`. Members calling these get `NOT_FOUND` (do not advertise staff routes).

| Method | Path | FS | Who |
| --- | --- | --- | --- |
| `GET` | `/admin/users` | FS-ADM, FS-ACCT-08/09 | Staff |
| `POST` | `/admin/users/{id}/lock` | FS-ACCT-08, FS-ADM-04 | Staff |
| `POST` | `/admin/users/{id}/unlock` | FS-ACCT-08 | Staff (also restores `closed`) |
| `PATCH` | `/admin/users/{id}/role` | FS-ACCT-09, FS-ADM-02 | Admin only |
| `GET` | `/admin/content` | FS-ADM-03 | Staff. Query `type=post\|comment\|event\|media`, optional `q` / `hidden` |
| `POST` | `/admin/content/{type}/{id}/hide` | FS-ADM-03 | Staff. `type=post\|comment\|event\|media` |
| `POST` | `/admin/content/{type}/{id}/unhide` | FS-ADM-03 | Staff |
| `GET` | `/admin/reports` | FS-ADM-07 | Staff |
| `POST` | `/admin/reports/{id}/resolve` | FS-ADM-07 | Staff |
| `POST` | `/reports` | FS-ADM-07 | Member. Body `{ targetType, targetId, reason }` |
| `GET` | `/admin/media` | FS-MED, FS-ADM | Staff |
| `POST` | `/admin/fixtures` | FS-ADM-05 | Admin, non-`prod` |
| `POST` | `/admin/fixtures/reset` | FS-ADM-05 | Admin, non-`prod`, `--reset` equivalent |
| `GET` | `/admin/audit` | FS-ADM-06 | Admin (moderators: read own + content actions) |

## Out of this surface

- Video posts, stories, group chat, E2E encryption, OAuth, Billing, Notifications product, Export CSV, Invite User, admin Bookings / Analytics / Dashboard widgets.
- Health and the four auth operations already on tag **v0.1.0**.
