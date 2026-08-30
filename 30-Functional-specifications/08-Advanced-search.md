# Advanced search

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md), [../40-Technical-specifications/06-Search-implementation.md](../40-Technical-specifications/06-Search-implementation.md) |

## Intent

Members search people and events with **parameters**, not only a single text box.

## Actors

Authenticated member.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-SRCH-01 | Search has two indexes: `people` and `events`. |
| FS-SRCH-02 | Common parameter: free-text `q` matched against names, bios, titles, descriptions. |
| FS-SRCH-03 | People filters: sports (any-of), experience, city, radius (km) if the viewer has coordinates, profile visibility (never returns private profiles the viewer cannot see), friend-state (`any` \| `not-friends`). |
| FS-SRCH-04 | Event filters: activity, visibility the viewer may see, date from/to, remaining capacity `> 0`, radius, organizer-is-friend. |
| FS-SRCH-05 | Results are paginated (cursor). Each item includes the reason it matched (debug flag for staff / tests only). |
| FS-SRCH-06 | Blocked users and hidden content never appear. |
| FS-SRCH-07 | Default sort: relevance then recency. Optional sort: distance, start time. |
| FS-SRCH-08 | Unauthenticated search is disabled at MVP. |

## Business rules

- Filters AND across fields; sports OR inside the field. Algorithm: [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md).
- Private strangers never appear. Public profiles do. Friends’ private profiles may appear.
- Radius 1–50 km. Mockup 12 shows miles; **implement kilometres** in the API (`radiusKm`). The UI may label km.
- People tab and Events tab are separate queries (two paths). The mockup’s mixed grid is a visual; Kernel may render the active tab’s results as cards.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/search/people` | FS-SRCH-01..08 |
| `GET` | `/api/v1/search/events` | FS-SRCH-01..08 |

Query parameters: `q`, `sports` (repeat), `experience`, `city`, `radiusKm`, `friendState`, `activity`, `from`, `to`, `remaining` (bool), `organizerIsFriend`, `sort=relevance\|distance\|starts_at`, `before`, `size`.

## UI

| Route | Mockup |
| --- | --- |
| `/search` | [12-search.jpg](../20-Architecture/mockups/12-search.jpg) — Filters (q, location+radius, sports, experience), People / Events tabs, CONNECT / JOIN EVENT actions that call friendships / events APIs. |

## Acceptance

- Given public profiles in Lyon who list `weightlifting`, when a member searches people with `sports=weightlifting` and `city=Lyon`, then those profiles are returned and private strangers are not.
- Given a full event, when `remaining=true`, then it is omitted.
- Given a blocked user, when they would match `q`, then they are absent.
- Given no Bearer token, when `/search/people` is called, then `401`.

## Errors

| Situation | Code |
| --- | --- |
| Not logged in | `UNAUTHENTICATED` |
| `radiusKm` out of 1–50 | `VALIDATION` |
| Unknown `sort` | `VALIDATION` |

## Links

- Algorithm: [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md)
- SQL plan: [../40-Technical-specifications/06-Search-implementation.md](../40-Technical-specifications/06-Search-implementation.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
