# Advanced search

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md), [../40-Technical-specifications/06-Search-implementation.md](../40-Technical-specifications/06-Search-implementation.md) |

Members search people and events with **parameters**, not only a single text box.

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

## Acceptance

- Given public profiles in Lyon who list `weightlifting`, when a member searches people with `sports=weightlifting` and `city=Lyon`, then those profiles are returned and private strangers are not.
- Given a full event, when `remaining=true`, then it is omitted.

Algorithm and ranking: [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md).
