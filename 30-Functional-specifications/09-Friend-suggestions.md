# Personalized friend suggestions

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../50-Algorithms/01-Friend-suggestions.md](../50-Algorithms/01-Friend-suggestions.md), [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md) |

## Intent

The product proposes people to add as friends. The **algorithm must be justified** (brief). This page is the product contract; the algorithm page is the justification. Weekly buddy matching (who to *train with*) is specified here as FS-MATCH so it is implemented, not only written.

## Actors

Authenticated member.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-SUGG-01 | A member can open a suggestions list (min 0, default 20, max 50). |
| FS-SUGG-02 | Candidates are not the viewer, not already friends, not pending, not blocked either way. |
| FS-SUGG-03 | Each card shows display name, shared sports, mutual friends count (if > 0), city if visible, and a primary score reason in plain language (“3 mutual friends”, “same gym times”). |
| FS-SUGG-04 | The member can dismiss a suggestion (`not now`); it is suppressed for 30 days. |
| FS-SUGG-05 | “Add friend” from a card creates a normal request ([03-Friends.md](03-Friends.md)). |
| FS-SUGG-06 | Suggestions respect private profiles: a private stranger may appear only as a stub if the scoring features used are allowed (mutual friends, not hidden bio). |
| FS-SUGG-07 | Recompute at least daily and after friend-graph changes (async). Stale scores older than 48 h must not be served if a recompute is pending — fall back to on-the-fly top-k for the viewer. |
| FS-MATCH-01 | A member may opt into “match me this week”. |
| FS-MATCH-02 | The service runs the greedy maximal matching in [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md) on the opt-in set (nightly). |
| FS-MATCH-03 | Each matched pair gets a **proposed instant event** draft (`visibility=friends`, capacity 1) at the overlapping window. Members still accept (human in the loop). No edge across a block; a person is assigned at most once. |

## Business rules

- Scoring, weights, FoF generation, complexity: [../50-Algorithms/01-Friend-suggestions.md](../50-Algorithms/01-Friend-suggestions.md). Do not ship a black-box ML model.
- Primary reason = feature with the largest \(w_i \cdot feature_i\). Map to copy: `mutual friends` → “N mutual friends”; `J` → shared sport name; `T` → “same gym times”; `G` → “near you” / city; `E` → “similar experience”.
- Dismiss table: `(viewer_id, candidate_id, until)`.
- Matching is **not** friend suggestions. It is a weekly assignment. Organizer accept-ranking on events is FS-EVT-13, not this list.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/suggestions` | FS-SUGG-01..03 |
| `POST` | `/api/v1/suggestions/{userId}/dismiss` | FS-SUGG-04 |
| `POST` | `/api/v1/matching/opt-in` | FS-MATCH-01 |
| `DELETE` | `/api/v1/matching/opt-in` | FS-MATCH-01 |
| `GET` | `/api/v1/matching/me` | FS-MATCH-02, FS-MATCH-03 |

Add Friend is `POST /friendships`.

## UI

| Route | Mockup |
| --- | --- |
| `/friends/suggestions` | [08-suggestions.jpg](../20-Architecture/mockups/08-suggestions.jpg) — cards with reason line, sports chips, Add Friend / Dismiss. |

Weekly opt-in: a toggle on this page (“Match me this week”) is enough. No extra mockup.

## Acceptance

- Given A and B share two friends and the same sport, when A opens suggestions, then B ranks above an unrelated public profile.
- Given A dismissed B, when A reloads within 30 days, then B is absent.
- Given a blocked user, when suggestions are served, then they are absent (unit invariant).
- Given three opt-ins where only one pair shares a sport and a window, when the greedy job runs, then that pair is matched and the third is unmatched; no double assignment.

## Errors

| Situation | Code |
| --- | --- |
| Not logged in | `UNAUTHENTICATED` |
| Dismiss unknown / self | `NOT_FOUND` |
| `size` > 50 | `VALIDATION` |

## Links

- Suggestion algorithm: [../50-Algorithms/01-Friend-suggestions.md](../50-Algorithms/01-Friend-suggestions.md)
- Matching algorithm: [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md)
- Friends: [03-Friends.md](03-Friends.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
