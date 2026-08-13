# Nested comments

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [05-Posts-and-engagement.md](05-Posts-and-engagement.md) |

Comments exist on posts and nest over **several levels**.

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

## Acceptance

- Given a comment at depth 3, when a member replies, then depth 4 is stored.
- Given a comment at depth 4, when a member replies, then the API rejects the payload.
- Given a deleted parent, when a child is fetched, then the parent appears as a tombstone and the child body is intact.

Depth is stored on the row to avoid recursive checks on every write.
