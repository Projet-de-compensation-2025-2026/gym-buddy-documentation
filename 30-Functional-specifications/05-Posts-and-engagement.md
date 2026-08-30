# Posts, reposts, and likes

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [04-News-feed.md](04-News-feed.md), [06-Nested-comments.md](06-Nested-comments.md) |

## Intent

Members publish posts, repost others, and like posts or comments.

## Actors

Member (author or viewer), moderator/admin (hide).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-POST-01 | A member can create a post with text (1–2000 characters) and optional images (max 4). |
| FS-POST-02 | A post has `visibility` `friends` (default) or `public`. |
| FS-POST-03 | The author can edit body within 15 minutes; edits set `edited_at`. |
| FS-POST-04 | The author can delete their post (soft-delete). Comments become inaccessible. |
| FS-POST-05 | A member who can **view** a post can **repost** it. Repost has no extra body at MVP. |
| FS-POST-06 | A member cannot repost the same post twice. They can undo a repost. |
| FS-POST-07 | A member who can view a post or comment can like / unlike it (toggle). |
| FS-POST-08 | Like counts are visible to anyone who can view the target. The nominative liker list is visible to the author only at MVP. |
| FS-POST-09 | Moderators can hide a post. It leaves feeds and returns `NOT_FOUND` to members. |

## Business rules

- Empty body **and** no media → `VALIDATION`. Body may be empty if 1–4 images are attached.
- Images: `mediaIds` of `kind=image` owned by the author and `ready` ([12-Media-and-files.md](12-Media-and-files.md)). Video is out of scope (ignore the feed composer’s video icon).
- `canView(post)`: author; staff in back-office; if `public` any member; if `friends` accepted friends. Hidden/deleted → members get `NOT_FOUND`.
- Like is a unique `(user_id, target_type, target_id)` row. PUT inserts; DELETE removes. A second PUT does not double-count.
- Repost unique `(user_id, post_id)`. If the original is deleted or hidden, reposts drop from feeds.
- Share-to-external-network control on mockup 04 is **not** product.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `POST` | `/api/v1/posts` | FS-POST-01 |
| `GET` | `/api/v1/posts/{id}` | FS-POST-02 |
| `PATCH` | `/api/v1/posts/{id}` | FS-POST-03 |
| `DELETE` | `/api/v1/posts/{id}` | FS-POST-04 |
| `POST` | `/api/v1/posts/{id}/reposts` | FS-POST-05 |
| `DELETE` | `/api/v1/posts/{id}/reposts` | FS-POST-06 |
| `PUT` | `/api/v1/posts/{id}/like` | FS-POST-07 |
| `DELETE` | `/api/v1/posts/{id}/like` | FS-POST-07 |
| `GET` | `/api/v1/posts/{id}/likes` | FS-POST-08 |

## UI

| Route | Mockup |
| --- | --- |
| Composer on `/` | [03-feed.jpg](../20-Architecture/mockups/03-feed.jpg) |
| `/posts/:id` | [04-post-comments.jpg](../20-Architecture/mockups/04-post-comments.jpg) — like/repost counts; comment thread is [06-Nested-comments.md](06-Nested-comments.md). |

## Acceptance

- Given a friends-only post, when a stranger likes it, then the API returns `NOT_FOUND`.
- Given a public post, when a member likes twice (PUT then PUT), then there is still a single like row; unlike is DELETE.
- Given a repost, when the original is deleted, then the repost disappears from feeds.
- Given 15 minutes + 1 s after create, when the author PATCHes, then `FORBIDDEN` or `VALIDATION`.

## Errors

| Situation | Code |
| --- | --- |
| Empty body and no media | `VALIDATION` |
| Too many images / video | `VALIDATION` |
| Duplicate repost | `CONFLICT` |
| Cannot view | `NOT_FOUND` |
| Edit window elapsed | `FORBIDDEN` |

## Links

- Comments: [06-Nested-comments.md](06-Nested-comments.md)
- Media: [12-Media-and-files.md](12-Media-and-files.md)
- Sequence: [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
