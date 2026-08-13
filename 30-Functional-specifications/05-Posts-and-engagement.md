# Posts, reposts, and likes

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [04-News-feed.md](04-News-feed.md), [06-Nested-comments.md](06-Nested-comments.md) |

Members publish posts, repost others, and like posts or comments.

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

## Acceptance

- Given a friends-only post, when a stranger likes it, then the API returns `NOT_FOUND`.
- Given a public post, when a member likes twice, then there is a single like row (idempotent toggle: second call unlikes).
- Given a repost, when the original is deleted, then the repost disappears from feeds.

## Errors

| Situation | Code |
| --- | --- |
| Empty body and no media | `VALIDATION` |
| Too many images | `VALIDATION` |
| Duplicate repost | `CONFLICT` |
