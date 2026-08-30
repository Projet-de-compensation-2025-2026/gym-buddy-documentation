# Friends news feed

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Posts-and-engagement.md](05-Posts-and-engagement.md), [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md) |

## Intent

The home surface is a **friends news feed**: posts and reposts from accepted friends (plus the viewer’s own), newest activity first.

## Actors

Authenticated member.

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

## Business rules

- An item is either a `post` or a `repost`. Reposts show the reposter as actor and link the original if the viewer may view it; if the original is deleted/hidden, omit the item (FS-POST).
- Composer on the feed creates a post ([05-Posts-and-engagement.md](05-Posts-and-engagement.md)). Visibility default `friends`. Mockup 03 shows image and **video** icons: images follow FS-POST-01 (max 4); **video is out of scope**.
- Ranking beyond recency is not MVP.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/feed` | FS-FEED-01..06 |

Create/like/comment use the posts and comments APIs.

## UI

| Route | Mockup |
| --- | --- |
| `/` | [03-feed.jpg](../20-Architecture/mockups/03-feed.jpg) — composer, visibility select, cards with like/comment counts. |

Empty state: short copy + button to `/friends/suggestions`.

## Acceptance

- Given A and B are friends and C is not, when B posts a friends-only update, then A sees it and C does not.
- Given B reposts C’s public post, when A opens the feed, then A sees the repost attributed to B, linking to C’s original if A may view it.
- Given a hidden post, when A pages the feed, then that id is absent and no “deleted” placeholder is shown.
- Given no friends and no own posts, when A opens `/`, then the suggestions CTA is visible.

## Errors

| Situation | Code |
| --- | --- |
| Not logged in | `UNAUTHENTICATED` |
| `size` > 50 | `VALIDATION` |

## Links

- Posts: [05-Posts-and-engagement.md](05-Posts-and-engagement.md)
- Sequence (post + like): [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
