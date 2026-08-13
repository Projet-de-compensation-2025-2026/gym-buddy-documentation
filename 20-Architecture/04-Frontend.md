# Frontend (member application)

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [05-Back-office.md](05-Back-office.md), [../30-Functional-specifications](../30-Functional-specifications/README.md) |

The member frontend is the athlete-facing web app: **Angular 22** + **TypeScript 7.0** ([07-Technology-choices.md](07-Technology-choices.md)). It talks to the backend through a client **generated from** `gym-buddy-openapi`. The static build is eligible for GitHub Pages ([08-Hosting-and-GitHub-Pages.md](08-Hosting-and-GitHub-Pages.md)).

## Surfaces

| Area | Routes (indicative) | Spec |
| --- | --- | --- |
| Auth | `/login`, `/register` | [../30-Functional-specifications/01-Accounts-and-administration.md](../30-Functional-specifications/01-Accounts-and-administration.md) |
| Feed | `/` | [../30-Functional-specifications/04-News-feed.md](../30-Functional-specifications/04-News-feed.md) |
| Post | `/posts/:id` | [../30-Functional-specifications/05-Posts-and-engagement.md](../30-Functional-specifications/05-Posts-and-engagement.md) |
| Profile | `/u/:handle` | [../30-Functional-specifications/02-User-profiles.md](../30-Functional-specifications/02-User-profiles.md) |
| Friends | `/friends`, `/friends/suggestions` | [03](../30-Functional-specifications/03-Friends.md), [09](../30-Functional-specifications/09-Friend-suggestions.md) |
| Events | `/events`, `/events/new`, `/events/:id` | [../30-Functional-specifications/07-Events.md](../30-Functional-specifications/07-Events.md) |
| Search | `/search` | [../30-Functional-specifications/08-Advanced-search.md](../30-Functional-specifications/08-Advanced-search.md) |
| Inbox | `/messages`, `/messages/:id` | [../30-Functional-specifications/10-Instant-messaging.md](../30-Functional-specifications/10-Instant-messaging.md) |
| Settings | `/settings/profile`, `/settings/privacy` | Profiles + accounts |

## Client responsibilities

- Hold the access token in memory; hold the refresh token in an `HttpOnly` cookie **or** secure storage as decided in [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md).
- Never talk to MinIO with long-lived keys. Upload via the API or a signed PUT.
- Render nested comments incrementally (do not fetch an unbounded tree).
- Degrade chat to HTTP polling if the WebSocket drops.
- Respect profile and event visibility: hide actions the API would reject.

## Accessibility and demo

The UI must be usable at a laptop viewport for the defense and remain usable on a phone browser. Screenshots for the report are listed in [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md).
