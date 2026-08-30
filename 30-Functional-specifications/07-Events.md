# Events

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md), [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md) |

## Intent

A member can create an **instant** or **recurring** training event, **public** or **private** (friends-only). Interested members apply; the organizer accepts or declines. Capacity is limited.

The brief’s example: a weightlifting session open only to friends, at a given place, for a given duration, at a precise time, with limited spots.

## Actors

Organizer (member who created the event), applicant (member), staff.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-EVT-01 | Organizer provides title, activity, place (text + optional lat/lng), start time, duration (minutes), visibility, capacity (1–100 excluding organizer). |
| FS-EVT-02 | **Instant** event: `recurrence` is empty; one occurrence. |
| FS-EVT-03 | **Recurring** event: RFC 5545 `RRULE` (at least `FREQ=WEEKLY` with `BYDAY`) + optional `UNTIL`. Occurrences are enumerable for a window (default 90 days). |
| FS-EVT-04 | Visibility `public`: any member may view and apply. Visibility `friends`: only accepted friends of the organizer. Visibility `private`: invite-only (organizer adds members; they still must accept). |
| FS-EVT-05 | A member who may view the event can **apply** once per occurrence (or per event if instant). |
| FS-EVT-06 | Organizer **accepts** or **declines** each pending application. |
| FS-EVT-07 | When accepted count reaches `capacity`, further accepts fail with `CONFLICT`. Applicants see “full”. |
| FS-EVT-08 | Organizer can cancel an occurrence or the whole series. Applicants are notified in-app. |
| FS-EVT-09 | Organizer can update place/time before the start if no one is accepted, or with a visible “updated” flag if people are accepted. |
| FS-EVT-10 | Applicant can withdraw while `pending` or `accepted` (before start). A seat is freed. |
| FS-EVT-11 | Organizer cannot apply to their own event. |
| FS-EVT-12 | Past occurrences remain readable to participants; they do not accept new applications. |
| FS-EVT-13 | Organizer detail includes a **suggested accept order** of pending applicants from [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md) (problem 1). Capacity stays a hard constraint. |

## Business rules

- Organizer occupies no capacity seat (capacity is for accepted applicants).
- Accept uses `SELECT FOR UPDATE` (or equivalent) on the occurrence, recounts `accepted`, then writes. Two concurrent accepts must not exceed capacity.
- Recurrence MVP: `FREQ=WEEKLY;BYDAY=...` and optional `UNTIL`. No `EXDATE` exceptions at MVP. Materialize or compute occurrences for 90 days on read.
- Create rejects `starts_at` in the past (`VALIDATION`).
- Cover images on mockup 11 are optional `mediaId` (`kind=image`); not required. “Focus Areas” chips are the `activity` plus optional `tags` (max 8 strings) — not a separate workout-tracking entity.
- In-app cancel notification: persist a `message.system` or a feed-less `notifications` row is **not** required; at MVP, the application status becomes `cancelled` and the detail page shows it. Do not invent a Notifications product.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/events` | FS-EVT list |
| `POST` | `/api/v1/events` | FS-EVT-01..04 |
| `GET` | `/api/v1/events/{id}` | FS-EVT-03, FS-EVT-13 |
| `PATCH` | `/api/v1/events/{id}` | FS-EVT-09 |
| `POST` | `/api/v1/events/{id}/cancel` | FS-EVT-08 |
| `POST` | `/api/v1/events/{id}/applications` | FS-EVT-05 |
| `DELETE` | `/api/v1/applications/{id}` | FS-EVT-10 |
| `POST` | `/api/v1/applications/{id}/accept` | FS-EVT-06, FS-EVT-07 |
| `POST` | `/api/v1/applications/{id}/decline` | FS-EVT-06 |

## UI

| Route | Mockup |
| --- | --- |
| `/events` | [09-events.jpg](../20-Architecture/mockups/09-events.jpg) — Upcoming Sessions, Instant / Recurring filters, Create Event. |
| `/events/new` | [10-new-event.jpg](../20-Architecture/mockups/10-new-event.jpg) — title, activity, place, start, duration, recurrence toggle, visibility, capacity 1–100. |
| `/events/:id` | [11-event-detail.jpg](../20-Architecture/mockups/11-event-detail.jpg) — spots left, Apply to Join, organizer applicant queue (accept/decline), Next 90 Days occurrences. |

## Acceptance

- Given a friends-only session with capacity 3, when a stranger applies, then `NOT_FOUND` or `FORBIDDEN`.
- Given 3 accepted friends, when the organizer accepts a 4th, then `CONFLICT`.
- Given a weekly rule and a 90-day window, when the event is fetched, then the API lists the materialised occurrences, not only the rule string.
- Given two concurrent accepts on the last seat, when both commit, then exactly one is `accepted` and the other is `CONFLICT`.
- Given pending applicants, when the organizer opens detail, then they are ordered by matching score (FS-EVT-13) and the organizer may still accept in any order.

## Errors

| Situation | Code |
| --- | --- |
| Start in the past (create) | `VALIDATION` |
| Capacity exceeded | `CONFLICT` |
| Double apply | `CONFLICT` |
| Not a friend on friends-only | `FORBIDDEN` or `NOT_FOUND` |
| Apply to own event | `FORBIDDEN` |
| Past occurrence apply | `VALIDATION` |

## Links

- Matching: [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md)
- Activity: [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md)
- Sequence (apply): [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
