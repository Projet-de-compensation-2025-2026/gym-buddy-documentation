# Frontend (member application)

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Back-office.md](05-Back-office.md), [../30-Functional-specifications](../30-Functional-specifications/README.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The member frontend is the athlete-facing web app. **Approved stack:** **Angular 22** + **TypeScript 7.0.0** + **pnpm** ([07-Technology-choices.md](07-Technology-choices.md), [../70-Engineering-practices/01-Coding-standards.md](../70-Engineering-practices/01-Coding-standards.md)). It talks to the backend through a client **generated from** [`gym-buddy-openapi`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi). The static build is eligible for GitHub Pages ([08-Hosting-and-GitHub-Pages.md](08-Hosting-and-GitHub-Pages.md)).

Today `gym-buddy-ui` on `develop` (app version `0.1.0`, ui #3 / ticket #12) is Angular 22 + **TypeScript `~6.0.2`** + **`packageManager`: `npm@10.9.8`**. That is not the approved toolchain. Do not claim the UI already uses TypeScript 7 or pnpm. Implementation tickets will move the repo; today-rows stay on 6.0.2 / npm until they land.

Today the app has `/register`, `/login`, and a log-out control that call `POST /api/v1/auth/register`, `/login`, `/logout`. Access JWT stays in memory. Refresh cookie credentials are sent (`path /api/v1/auth`). No friends / feed / events. The service has **not** implemented those endpoints, so end-to-end sign-up / sign-in is not done.

## Toolchain (today vs approved)

| Piece | Today (`develop`, app `0.1.0`) | Approved target |
| --- | --- | --- |
| Angular | 22 | 22 |
| TypeScript | `~6.0.2` | **7.0.0** from the `typescript` npm package (`tsc` is the Go binary / Project Corsa). Not `@typescript/native-preview` / `tsgo`. |
| Package manager | `npm@10.9.8` | **pnpm**, pinned in `packageManager`, activated with **Corepack**. Commit `pnpm-lock.yaml`. Do not install `latest`. |
| Supply-chain floor | none | `minimumReleaseAge` **40320** minutes (four weeks). Canonical: `pnpm-workspace.yaml`. Older pnpm: `.npmrc` `minimum-release-age=40320`. **Not** a `package.json` field. |
| Lifecycle scripts | npm defaults | Disable or tightly allow (`onlyBuiltDependencies` and/or ignore-scripts). Required. |

## API base URL

| Environment | `apiBaseUrl` |
| --- | --- |
| Local | `http://127.0.0.1:8080/api/v1` (`environment.ts`; `ng serve` proxies `/api`) |
| Live (operator network) | `https://vps-c39cdf03.vps.ovh.net/api/v1` — today’s VPS container is still the health-only replace (tag **v0.1.1**), not auth |

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
