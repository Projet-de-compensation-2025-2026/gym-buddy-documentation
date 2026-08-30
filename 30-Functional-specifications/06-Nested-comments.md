# Nested comments

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Posts-and-engagement.md](05-Posts-and-engagement.md) |

## Intent

Comments exist on posts and nest over **several levels** (cap 4). Deleted comments tombstone; children stay.

## Actors

Member who can view the parent post; author; staff.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-CMT-01 | A member who can view a post can comment on it (`parent_id` omitted). |
| FS-CMT-02 | A member who can view a comment can reply to it (`parent_id` set). |
| FS-CMT-03 | Maximum depth is **4** (root = 0). A reply beyond that returns `VALIDATION`. |
| FS-CMT-04 | Body is 1–1000 characters. No media in comments at MVP. |
| FS-CMT-05 | Author can delete their comment. Children remain; the body is replaced by a tombstone (“comment deleted”). |
| FS-CMT-06 | Comments are listed depth-first or by page of roots + expand thread. Default: page roots (20), load replies on demand. |
| FS-CMT-07 | Likes on comments follow FS-POST-07. |
| FS-CMT-08 | Staff can hide a comment (tombstone + `hidden`). |

## Business rules

- `depth` is stored on the row (`parent.depth + 1`, root `0`) so writes do not recurse.
- Hidden/deleted parent: children still load; parent body is the tombstone string. Do not leak the original body.
- Page roots with `before` cursor; `GET /comments/{id}/replies` returns children (not unbounded). Mockup 04 “Load 3 more replies” is this expand.
- Cannot comment on a post the caller cannot view (`NOT_FOUND`).

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/posts/{id}/comments` | FS-CMT-06 |
| `POST` | `/api/v1/posts/{id}/comments` | FS-CMT-01, FS-CMT-02 |
| `GET` | `/api/v1/comments/{id}/replies` | FS-CMT-06 |
| `DELETE` | `/api/v1/comments/{id}` | FS-CMT-05 |
| `PUT` | `/api/v1/comments/{id}/like` | FS-CMT-07 |
| `DELETE` | `/api/v1/comments/{id}/like` | FS-CMT-07 |

## UI

| Route | Mockup |
| --- | --- |
| `/posts/:id` thread | [04-post-comments.jpg](../20-Architecture/mockups/04-post-comments.jpg) — nested indent, like + reply, tombstone, load-more replies. |

## Acceptance

- Given a comment at depth 3, when a member replies, then depth 4 is stored.
- Given a comment at depth 4, when a member replies, then the API rejects the payload.
- Given a deleted parent, when a child is fetched, then the parent appears as a tombstone and the child body is intact.

## Errors

| Situation | Code |
| --- | --- |
| Depth > 4 | `VALIDATION` |
| Empty / too long body | `VALIDATION` |
| Post or parent not viewable | `NOT_FOUND` |
| Not the author on delete | `FORBIDDEN` |

## Links

- Posts: [05-Posts-and-engagement.md](05-Posts-and-engagement.md)
- Class (`Comment.depth`): [../60-UML-diagrams/04-Class.md](../60-UML-diagrams/04-Class.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
