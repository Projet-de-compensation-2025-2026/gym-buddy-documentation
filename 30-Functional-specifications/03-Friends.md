# Friends

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [09-Friend-suggestions.md](09-Friend-suggestions.md), [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md) |

Adding a friend **requires approval**. There is no silent follow.

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

## Acceptance

- Given A sends a request to B, when B has not answered, then A does not see B’s friends-only events.
- Given B accepts, when A opens B’s private profile, then FS-PROF-04 full view applies.
- Given B blocked A, when A sends a request, then the API returns `NOT_FOUND` or `FORBIDDEN` without confirming B’s existence beyond what search already revealed.

## Errors

| Situation | Code |
| --- | --- |
| Already friends / pending | `CONFLICT` |
| Target locked or missing | `NOT_FOUND` |
| Blocked | `FORBIDDEN` |
