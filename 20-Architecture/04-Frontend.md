# Frontend (member application)

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Back-office.md](05-Back-office.md), [../30-Functional-specifications](../30-Functional-specifications/README.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The member frontend is the athlete-facing web app. **Approved stack:** **Angular 22** + **TypeScript 6** (`~6.0.2`) + **pnpm** ([07-Technology-choices.md](07-Technology-choices.md), [../70-Engineering-practices/01-Coding-standards.md](../70-Engineering-practices/01-Coding-standards.md)). It talks to the backend through a client **generated from** [`gym-buddy-openapi`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi). The static build is hosted on GitHub Pages at https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ ([08-Hosting-and-GitHub-Pages.md](08-Hosting-and-GitHub-Pages.md)).

Today `gym-buddy-ui` on `develop` (app version `0.1.0`, ui #3 / ticket #12) is Angular 22 + **TypeScript `~6.0.2`** + **`packageManager`: `pnpm@11.22.0`** ([gym-buddy-ui#4](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui/pull/4) / `63bebed`): committed `pnpm-lock.yaml`, `minimumReleaseAge` **40320**. Ticket **#23** (pnpm) is **Done**. Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed). Do **not** claim TypeScript 7 landed. Do **not** treat 7.0.0 or 7.0.2 as the next compiler.

Today the app has `/register`, `/login`, and a log-out control that call `POST /api/v1/auth/register`, `/login`, `/logout`. Access JWT stays in memory. Refresh cookie credentials are sent (`path /api/v1/auth`). No friends / feed / events. The service on `develop` implements those endpoints (service #5 / `e2ef2aa`). Ticket #12 is closed. Caddy register/login is **proven from the operator network**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. A password visibility toggle (eye) is on `gym-buddy-ui` `develop` (`75fbbce` / ui #9 / ticket #34 Done). The live **v0.1.1** bundle (`main-4WJYST2C.js`) includes the password eye.

**Today (ticket #30 Done):** GitHub Pages hosts the production build at https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/. Sentinel confirmed the root returns **HTTP 200** and serves the Angular app with production `baseHref` `/gym-buddy-ui/`. Root 200 is the acceptance. Direct `/register` returns **HTTP 404** with the SPA index body (`404.html`). That is Pages’ static fallback, **not** a broken app and **not** a working auth route. Live Pages is **v0.1.1**; bundle `main-4WJYST2C.js` embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye. UI `develop` **`7916fa8`** has that VPS `apiBaseUrl`. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`. Ticket **#31** is **Done / closed** for **only** `apiBaseUrl` + CORS + that live bundle. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. `SameSite=Lax` will **not** ride a github.io → VPS credentialed XHR. Do **not** write that signup/login from github.io works. Do **not** start Kernel.

## Toolchain (today vs approved)

| Piece | Today (`develop`, app `0.1.0`) | Approved target |
| --- | --- | --- |
| Angular | 22 | 22 |
| TypeScript | `~6.0.2` | **TypeScript 6** (`~6.0.2`). Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on `~6.0.2` until Angular actually supports 7. Ticket #24 cancelled. |
| Package manager | **`pnpm@11.22.0`** (ui #4 / `63bebed`) | **pnpm**, pinned in `packageManager`, activated with **Corepack**. Commit `pnpm-lock.yaml`. Do not install `latest`. |
| Supply-chain floor | `minimumReleaseAge` **40320** (ui #4 / `63bebed`) | `minimumReleaseAge` **40320** minutes (four weeks). Canonical: `pnpm-workspace.yaml`. Older pnpm: `.npmrc` `minimum-release-age=40320`. **Not** a `package.json` field. |
| Lifecycle scripts | npm defaults | Disable or tightly allow (`onlyBuiltDependencies` and/or ignore-scripts). Required. |

## API base URL

| Environment | `apiBaseUrl` |
| --- | --- |
| Local | `http://127.0.0.1:8080/api/v1` (`environment.ts`; `ng serve` proxies `/api`) |
| GitHub Pages (today) | Live tag is **v0.1.1**. Bundle `main-4WJYST2C.js` embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye. UI `develop` **`7916fa8`** has that VPS `apiBaseUrl`. First tag **v0.1.0** pointed at localhost. Ticket **#31** is **Done / closed** for **only** `apiBaseUrl` + CORS + that live bundle. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. `SameSite=Lax` will **not** ride a github.io → VPS credentialed XHR. Do **not** start Kernel. |
| Live API (operator network) | `https://vps-c39cdf03.vps.ovh.net/api/v1` — Today’s VPS container is **aea1c56**. Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` also **200**. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. **Not** a GHCR pull. Caddy is **not** proven from the GitHub Pages origin. Ticket **#31** is **Done / closed** for **only** `apiBaseUrl` + CORS + live **v0.1.1**. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. |

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
