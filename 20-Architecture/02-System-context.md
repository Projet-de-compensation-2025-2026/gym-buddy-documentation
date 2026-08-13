# System context

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [01-Software-architecture.md](01-Software-architecture.md), [../60-UML-diagrams/01-Use-cases.md](../60-UML-diagrams/01-Use-cases.md) |

## System context

```mermaid
flowchart LR
  member([Member])
  staff([Admin / moderator])
  instructor([Instructor])

  gb[Gym Buddies]

  email[Outbound email]
  geo[Geocoding optional]
  gh[GitHub]

  member -->|uses web app| gb
  staff -->|uses back-office| gb
  gb --> email
  gb -.-> geo
  instructor -->|reads private repos| gh
```

## Actors

| Actor | Enters through | Primary goals |
| --- | --- | --- |
| Visitor | Member frontend | Register, browse public profiles/events if allowed |
| Member | Member frontend | Feed, friends, events, chat, search |
| Moderator | Back-office (+ limited in-app tools) | Hide content, handle reports |
| Admin | Back-office | Roles, account locks, fixtures, settings |
| Instructor | GitHub / email | Evaluate the project — not a runtime actor |

## External systems

| System | Required at MVP? | Notes |
| --- | --- | --- |
| SMTP / mail provider | Yes for verification; can be MailHog in dev | Do not block local fixtures on real mail |
| Object storage | Yes | MinIO locally, S3-compatible in deploy |
| Geocoding | No | Members may type a free-text place + optional lat/lng |
| Push notifications | No | In-app + websocket is enough for the defense |

GitHub is part of the **academic** system, not the runtime.
