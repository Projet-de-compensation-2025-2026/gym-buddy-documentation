# Events

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../50-Algorithms/03-User-matching.md](../50-Algorithms/03-User-matching.md), [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md) |

A member can create an **instant** or **recurring** training event, **public** or **private** (friends-only). Interested members apply; the organizer accepts or declines. Capacity is limited.

The brief’s example: a weightlifting session open only to friends, at a given place, for a given duration, at a precise time, with limited spots.

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

## Acceptance

- Given a friends-only session with capacity 3, when a stranger applies, then `NOT_FOUND` or `FORBIDDEN`.
- Given 3 accepted friends, when the organizer accepts a 4th, then `CONFLICT`.
- Given a weekly rule and a 90-day window, when the event is fetched, then the API lists the materialised occurrences, not only the rule string.

## Errors

| Situation | Code |
| --- | --- |
| Start in the past (create) | `VALIDATION` |
| Capacity exceeded | `CONFLICT` |
| Double apply | `CONFLICT` |
| Not a friend on friends-only | `FORBIDDEN` |
