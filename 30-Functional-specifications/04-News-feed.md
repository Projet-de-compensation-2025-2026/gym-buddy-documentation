# Friends news feed

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [05-Posts-and-engagement.md](05-Posts-and-engagement.md), [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md) |

The home surface is a **friends news feed**: posts and reposts from accepted friends (plus the viewer’s own).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-FEED-01 | The feed contains posts authored by the viewer and by accepted friends, and reposts made by them, that the viewer is allowed to see. |
| FS-FEED-02 | Default order is reverse chronological on the **activity time** (post `created_at` or repost `created_at`). |
| FS-FEED-03 | Pagination is cursor-based (`before` timestamp+id). Default page size 20, max 50. |
| FS-FEED-04 | Hidden / deleted posts are omitted. The viewer does not see gaps explained as “deleted”. |
| FS-FEED-05 | Posts with `visibility = public` from non-friends do **not** enter the friends feed (they are reachable from profiles and search). |
| FS-FEED-06 | Each item shows author, time, body, like count, comment count, and whether the viewer liked it. |
| FS-FEED-07 | An empty feed shows suggestions CTA ([09-Friend-suggestions.md](09-Friend-suggestions.md)). |

## Acceptance

- Given A and B are friends and C is not, when B posts a friends-only update, then A sees it and C does not.
- Given B reposts C’s public post, when A opens the feed, then A sees the repost attributed to B, linking to C’s original if A may view it.

Ranking beyond recency (friend-boost, likes) is optional and documented in the filtered-search / ranking algorithm page if enabled.
