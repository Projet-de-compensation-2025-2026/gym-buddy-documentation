# Use case diagrams

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../30-Functional-specifications](../30-Functional-specifications/README.md) |

## Actors and goals

```mermaid
flowchart LR
  visitor([Visitor])
  member([Member])
  organizer([Organizer])
  mod([Moderator])
  admin([Admin])

  visitor --> UC1[Register]
  visitor --> UC2[Log in]

  member --> UC3[Edit profile visibility]
  member --> UC4[Send / accept friend request]
  member --> UC5[Publish post / repost / like]
  member --> UC6[Comment nested]
  member --> UC7[Read friends feed]
  member --> UC8[Search people and events]
  member --> UC9[Open suggestions]
  member --> UC10[Send private text / image / audio]
  member --> UC11[Apply to event]
  member --> UC12[Report content]

  organizer --> UC13[Create instant or recurring event]
  organizer --> UC14[Accept or decline applications]

  mod --> UC15[Hide content]
  mod --> UC16[Lock account]

  admin --> UC17[Change roles]
  admin --> UC18[Run fixtures]
```

Organizer is a **role on an event**, not a distinct account type (include relationship with Member).

## Primary use case — find a gym buddy

| | |
| --- | --- |
| Actor | Member |
| Precondition | Authenticated, profile completed |
| Main success | Member searches / uses suggestions → sends friend request → accepted → creates or applies to a session → trains |
| Extensions | Decline, block, event full, private profile stub |

## Primary use case — friends-only session (brief example)

| | |
| --- | --- |
| Actor | Organizer (member) |
| Precondition | Has at least one friend if visibility is `friends` |
| Main success | Create event (place, duration, time, capacity, friends-only) → friends apply → organizer accepts until full |
| Extensions | Recurring weekly; cancel occurrence; withdraw |
