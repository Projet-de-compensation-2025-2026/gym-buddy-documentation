# Personalized friend suggestions

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../50-Algorithms/01-Friend-suggestions.md](../50-Algorithms/01-Friend-suggestions.md) |

The product proposes people to add as friends. The **algorithm must be justified** (brief). This page is the product contract; the algorithm page is the justification.

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

## Acceptance

- Given A and B share two friends and the same sport, when A opens suggestions, then B ranks above an unrelated public profile.
- Given A dismissed B, when A reloads within 30 days, then B is absent.

Justification, weights, complexity: [../50-Algorithms/01-Friend-suggestions.md](../50-Algorithms/01-Friend-suggestions.md).
