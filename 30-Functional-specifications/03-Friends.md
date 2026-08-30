# Friends

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [09-Friend-suggestions.md](09-Friend-suggestions.md), [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md) |

## Intent

Adding a friend **requires approval**. There is no silent follow. Accepted friendship is symmetric and unlocks private profiles, friends-only events, and DMs.

## Actors

Member (requester, addressee), staff (read-only in back-office).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-FRND-01 | A member can send a friend request to another active member. |
| FS-FRND-02 | The addressee can accept or decline. Only **accepted** pairs are friends. |
| FS-FRND-03 | The requester can cancel a pending request. |
| FS-FRND-04 | Either friend can unfriend (row becomes absent or `declined` with audit). |
| FS-FRND-05 | A member can block another. Block hides both from each other’s feed, search ranking, suggestions, and prevents new requests or DMs. |
| FS-FRND-06 | No self-friend. Duplicate pending requests return `CONFLICT`. |
| FS-FRND-07 | Friends lists are visible to the owner; whether friends-of-friends can see the list: **owner + friends** only (private-by-default). |
| FS-FRND-08 | Friendship is symmetric after accept. |

## Business rules

- One unordered pair. Store direction on insert (`requester_id`, `addressee_id`) plus a unique index on `LEAST(requester_id, addressee_id), GREATEST(...)`.
- Status ∈ `pending` \| `accepted` \| `declined` \| `blocked`.
- Unfriend deletes the row (or sets `declined`). Either side may send a new request afterwards.
- Block: upsert status `blocked` with the blocker as requester. Reverse pending requests are cancelled. Existing DMs remain readable (FS-MSG-10) but send is `FORBIDDEN`.
- Self-friend and request to `closed`/`locked` → `NOT_FOUND`.
- Incoming/outbound pending lists are owner-only.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/friendships` | FS-FRND-07 |
| `POST` | `/api/v1/friendships` | FS-FRND-01 |
| `POST` | `/api/v1/friendships/{id}/accept` | FS-FRND-02 |
| `POST` | `/api/v1/friendships/{id}/decline` | FS-FRND-02 |
| `DELETE` | `/api/v1/friendships/{id}` | FS-FRND-03, FS-FRND-04 |
| `POST` | `/api/v1/blocks` | FS-FRND-05 |
| `DELETE` | `/api/v1/blocks/{userId}` | FS-FRND-05 |

## UI

| Route | Mockup |
| --- | --- |
| `/friends` | [07-friends.jpg](../20-Architecture/mockups/07-friends.jpg) — Pending (inbound accept/decline, outbound cancel) + My Friends (Unfriend, Block, search). |

Add Friend on a profile uses the same `POST /friendships`. Suggestions “Add Friend” is [09-Friend-suggestions.md](09-Friend-suggestions.md).

## Acceptance

- Given A sends a request to B, when B has not answered, then A does not see B’s friends-only events.
- Given B accepts, when A opens B’s private profile, then FS-PROF-04 full view applies.
- Given B blocked A, when A sends a request, then the API returns `NOT_FOUND` or `FORBIDDEN` without confirming B’s existence beyond what search already revealed.
- Given A and A, when A requests self, then `VALIDATION` or `CONFLICT`.
- Given a pending request, when A posts a second, then `CONFLICT`.

## Errors

| Situation | Code |
| --- | --- |
| Already friends / pending | `CONFLICT` |
| Target locked, closed, or missing | `NOT_FOUND` |
| Blocked | `FORBIDDEN` or `NOT_FOUND` |
| Self-friend | `VALIDATION` |

## Links

- Activity: [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md)
- Suggestions: [09-Friend-suggestions.md](09-Friend-suggestions.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
