# QA — Gym Buddy v1.0.0 public / auth (GitHub Pages)

| Field | Value |
| --- | --- |
| Status | Recorded 2026-08-30 |
| Related | [03-Screenshots.md](03-Screenshots.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md), [../30-Functional-specifications/01-Accounts-and-administration.md](../30-Functional-specifications/01-Accounts-and-administration.md), [../20-Architecture/mockups/01-register.jpg](../20-Architecture/mockups/01-register.jpg), [../20-Architecture/mockups/02-login.jpg](../20-Architecture/mockups/02-login.jpg) |
| Target | https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ |
| API | `https://vps-c39cdf03.vps.ovh.net/api/v1` |
| Bundle | `main-VXEXHKAI.js` (Pages `Last-Modified: Sun, 30 Aug 2026 18:25:19 GMT`; UI tag **v1.0.0**) |
| Tooling | Playwright Chromium, viewports 1280×800 and 390×844 |
| Screenshots | [screenshots/qa-v1.0.0/public/](screenshots/qa-v1.0.0/public/) |

These are **live Angular shots**, not wiki mockup JPGs. Mockups are cited only as expected layout.

This crawl is **public / auth**. It does not claim the rest of the 1.0.0 product (friends, events, admin) was proven.

Ticket **#37** stays **closed**. Create-account + sign-in from this Pages origin **succeeded** on 2026-08-30 (this crawler’s network). Failures below are separate product bugs (session refresh / logout cookie, visual, validation UX, routing). Do **not** Todo #37.

## Method

- HTTP GET of Pages URLs (status + body length) plus browser `goto` / `reload`.
- Form journeys: empty submit, invalid email, short password, password = email, password = handle, unique register, duplicate email, duplicate handle, case-folded duplicate email, garbage login, unique login, logout, invalid route.
- `fetch` from the Pages origin against `/healthz`, `/readyz`, `/auth/register`, `/auth/login`, `/auth/refresh` with `credentials: include`.
- Console + failed network (Playwright). No application `pageerror` exceptions were recorded.

## What passed

| Check | Result |
| --- | --- |
| Pages root `/gym-buddy-ui/` | HTTP **200**, Angular 22 app, `baseHref` `/gym-buddy-ui/` |
| Password eye (#34) | Present on login and register; `aria-label="Show password"` toggles `type=password` → `type=text` |
| Unique register from Pages | **201** then client navigates to `/login`. Example: `qa.public.1788116283363@example.com` / handle `qapub1788116283363` |
| Duplicate email | UI `email already registered` (API **409** `CONFLICT`) |
| Duplicate handle | UI `handle already taken` |
| Case-insensitive duplicate email | UI `email or handle already registered` (FS-ACCT-02) |
| Password = email or handle | Client blocks with the generic 10+ / not-email-or-handle banner (FS-ACCT-03) |
| Garbage login | API **403** `FORBIDDEN` `{ "error": { "code": "FORBIDDEN", "message": "invalid credentials" } }`; UI shows that message |
| Unique login from Pages | **200** `accessToken` (HS256, `typ=access`, `role=member`); SPA opens the friends feed |
| Empty feed (new user) | Copy + **Find suggestions** CTA (FS-FEED-07) |
| CORS from Pages origin | `GET /healthz` **200** `{"status":"ok"}`; ACAO `https://projet-de-compensation-2025-2026.github.io`; `Access-Control-Allow-Credentials: true`. `OPTIONS /auth/login` **200** |
| Log-out control | Header button `data-testid="log-out"` exists after sign-in |
| Trailing slash `/login/` | Browser ends on `/login` and still renders sign-in (HTTP 404 body is the SPA) |
| Refresh of `/login` | SPA still renders sign-in (same 404.html fallback) |

## Hosting: deep links are HTTP 404 with the index body

Hash routing is **not** used. Direct GET:

| URL | HTTP | Body |
| --- | --- | --- |
| `/gym-buddy-ui/` | 200 | SPA index (18084 bytes) |
| `/gym-buddy-ui/index.html` | 200 | same |
| `/gym-buddy-ui/login` | **404** | same SPA index (etag `6a94758f-46a4`) |
| `/gym-buddy-ui/login/` | **404** | same |
| `/gym-buddy-ui/register` | **404** | same |
| `/gym-buddy-ui/does-not-exist` | **404** | same |
| `/gym-buddy-ui/404.html` | 200 | same |

This is GitHub Pages’ static fallback (`404.html` copied from `index.html`), as already described in [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md). **Refresh and share of `/login` still boot the app in Chromium.** The document.status is 404, so the console logs `Failed to load resource: … 404` on every client route. That does **not** by itself break sign-in.

**Separate Angular bug:** after the SPA boots, `/does-not-exist` is rewritten to `/` (logged-out home). There is no in-app not-found page. See finding F5.

## Session / cookies (do not reopen #37)

Login JSON from the Pages origin is only `accessToken`. Node GET of the same `POST /auth/login` **does** receive:

```text
Set-Cookie: refresh=<jwt>; Path=/api/v1/auth; Max-Age=1209600; Secure; HttpOnly; SameSite=Lax
```

Playwright’s cookie jar on `github.io` stayed **empty**. `POST /api/v1/auth/refresh` from the page with `credentials: include` returned **401** `UNAUTHENTICATED` `"refresh credential is missing"`. Full reload of `/` after a successful sign-in shows the logged-out marketing home.

That matches the wiki: `SameSite=Lax` will not ride a github.io → VPS credentialed XHR. First-login JWT in memory still proves create-account + sign-in. **#37 stays closed.** The user-visible gaps (reload drops the session; log out prints the missing-cookie error) are filed as a **new** bug.

## Findings

Issue numbers are Gym Buddy Project tickets on `gym-buddy-documentation` (Status **Not Ready**). Opened from this crawl: [#91](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/91) (F1), [#90](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/90) (F2), [#92](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/92) (F3), [#89](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/89) (F4), [#95](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/95) (F5), [#93](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/93) (F6), [#94](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/94) (F7).

### F1 — Login and register screens do not match mockups 01 / 02

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/login`, `/gym-buddy-ui/register` |
| **Expected** | [01-register.jpg](../20-Architecture/mockups/01-register.jpg): centered card, Display name → Handle → Email → Password (Min 10 characters) with eye, teal **Register**. [02-login.jpg](../20-Architecture/mockups/02-login.jpg): centered card, Gym Buddy mark, Email Address / Password with eye, teal **Log In**. Primary `#006D77` ([09-Visual-design.md](../20-Architecture/09-Visual-design.md)). FS-ACCT-01..04. |
| **Actual** | Full-width uncarded form under a header. Field order on register is Email, Handle, Password, **Display name last**. No placeholders. Password label is just “Password”. **Sign in** / **Create account** computed style `background rgb(240, 240, 240)`, `border-radius 0`, **no** `btn-primary` class, ~1024px wide. Feed **Post** and **Find suggestions** *do* use `btn-primary` `#006D77`. “Remember me” / “Forgot password?” from mockup 02 are leftover chrome (no FS ID) and were **not** treated as missing features. |
| **Screenshots** | [screenshots/qa-v1.0.0/public/02-login-desktop.png](screenshots/qa-v1.0.0/public/02-login-desktop.png), [10-register-desktop.png](screenshots/qa-v1.0.0/public/10-register-desktop.png), [02-login-mobile.png](screenshots/qa-v1.0.0/public/02-login-mobile.png) |
| **Console / network** | none (pure UI) |
| **Ticket** | [#91](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/91) |

### F2 — Auth validation is one generic banner; API errors are dumped raw

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/login`, `/gym-buddy-ui/register` |
| **Expected** | Error catalog in [01-Accounts-and-administration.md](../30-Functional-specifications/01-Accounts-and-administration.md) (`VALIDATION`, `CONFLICT`, `FORBIDDEN`) and [01-API-conventions.md](../40-Technical-specifications/01-API-conventions.md) (`details[].path`). Visitor can tell *which* field failed. |
| **Actual** | Empty login, invalid email, and short password all share one red line: “Enter a valid email and password.” / “Check email, handle, password (10+ characters, not email or handle), and display name.” No per-field message, no invalid outline. Garbage login shows lowercase `invalid credentials`. Duplicate email `email already registered`. Duplicate handle `handle already taken`. Logout (F4) shows `refresh credential is missing` above the sign-in heading. |
| **Screenshots** | [05-login-empty-submit-desktop.png](screenshots/qa-v1.0.0/public/05-login-empty-submit-desktop.png), [06-login-invalid-email-desktop.png](screenshots/qa-v1.0.0/public/06-login-invalid-email-desktop.png), [07-login-garbage-credentials-desktop.png](screenshots/qa-v1.0.0/public/07-login-garbage-credentials-desktop.png), [13-register-empty-submit-desktop.png](screenshots/qa-v1.0.0/public/13-register-empty-submit-desktop.png), [15-register-short-password-desktop.png](screenshots/qa-v1.0.0/public/15-register-short-password-desktop.png), [18-register-duplicate-desktop.png](screenshots/qa-v1.0.0/public/18-register-duplicate-desktop.png), [31-register-password-equals-email-desktop.png](screenshots/qa-v1.0.0/public/31-register-password-equals-email-desktop.png), [33-register-duplicate-handle-desktop.png](screenshots/qa-v1.0.0/public/33-register-duplicate-handle-desktop.png) |
| **Console / network** | `POST …/auth/login` 403 `{"error":{"code":"FORBIDDEN","message":"invalid credentials","details":null}}`; `POST …/auth/register` 409 for duplicates |
| **Ticket** | [#90](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/90) |

### F3 — Successful register has no confirmation

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/register` → `/gym-buddy-ui/login` |
| **Expected** | FS-ACCT-01: visitor registers then can log in. Copy on the page says “You will sign in on the next page.” A created account should be obvious (banner and/or prefilled email). |
| **Actual** | Unique register **201**, then empty Sign in with no success text and no prefilled email. Same screen as a cold visit. |
| **Screenshots** | [17-register-unique-result-desktop.png](screenshots/qa-v1.0.0/public/17-register-unique-result-desktop.png) |
| **Console / network** | `POST /api/v1/auth/register` 201 `{ id, email, handle, displayName, role: "member" }` |
| **Ticket** | [#92](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/92) |

### F4 — Pages session dies on refresh; log out prints a cookie error

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/` after sign-in; Log out |
| **Expected** | FS-ACCT-04 access JWT + refresh credential; FS-ACCT-06 log out revokes refresh. After sign-in, reload should stay signed in **or** recover via refresh. Log out should return a clean signed-out home/login, not an API dump. |
| **Actual** | Sign-in from Pages works (access JWT in memory). Playwright cookies on `github.io`: **[]**. Reload of `/` → logged-out marketing stub. `POST /auth/refresh` from the page: **401** `"refresh credential is missing"`. Log out lands on `/login` with that same red line above the heading. Root cause: refresh cookie `SameSite=Lax; Path=/api/v1/auth` on the VPS host is not stored for a github.io XHR (third-party). **Not a regression of create-account + sign-in.** Related closed **#37**. |
| **Screenshots** | [23-session-before-reload-desktop.png](screenshots/qa-v1.0.0/public/23-session-before-reload-desktop.png), [24-session-after-reload-desktop.png](screenshots/qa-v1.0.0/public/24-session-after-reload-desktop.png), [30-after-logout-desktop.png](screenshots/qa-v1.0.0/public/30-after-logout-desktop.png), [20-feed-after-login-desktop.png](screenshots/qa-v1.0.0/public/20-feed-after-login-desktop.png) (full navigation also drops the memory JWT) |
| **Console / network** | Login 200 `accessToken` (no cookie in the browser jar). Refresh 401 `{"error":{"code":"UNAUTHENTICATED","message":"refresh credential is missing","details":null}}`. Node probe of the same login **does** see `Set-Cookie: refresh=…; SameSite=Lax`. |
| **Ticket** | [#89](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/89) (new; **#37 stays closed**) |

### F5 — Unknown client routes redirect to home

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/does-not-exist` |
| **Expected** | A not-found state (or keep the bad path visible). Sharing a typo should not silently look like the marketing home. |
| **Actual** | HTTP 404 + SPA boot, then Angular navigates to `https://…/gym-buddy-ui/` (logged-out home). No “not found” copy. |
| **Screenshots** | [22-invalid-route-desktop.png](screenshots/qa-v1.0.0/public/22-invalid-route-desktop.png) |
| **Console / network** | `Failed to load resource: the server responded with a status of 404 ()` url=`…/does-not-exist` |
| **Ticket** | [#95](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/95) |

### F6 — Empty-feed CTA goes to `/suggestions`, not `/friends/suggestions`

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/` (signed in, empty feed) → CTA |
| **Expected** | [04-News-feed.md](../30-Functional-specifications/04-News-feed.md) empty state button to `/friends/suggestions`. [09-Friend-suggestions.md](../30-Functional-specifications/09-Friend-suggestions.md) and [04-Frontend.md](../20-Architecture/04-Frontend.md) list `/friends/suggestions`. |
| **Actual** | `<a routerlink="/suggestions" data-testid="empty-feed-cta" href="/gym-buddy-ui/suggestions">Find suggestions</a>`. The `/suggestions` page does render (Friend Suggestions + Match me this week). Spec path is still `/friends/suggestions`. |
| **Screenshots** | [19-login-unique-result-desktop.png](screenshots/qa-v1.0.0/public/19-login-unique-result-desktop.png), [27-suggestions-cta-desktop.png](screenshots/qa-v1.0.0/public/27-suggestions-cta-desktop.png) |
| **Console / network** | client navigation only |
| **Ticket** | [#93](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/93) |

### F7 — Feed composer still shows a Video control

| | |
| --- | --- |
| **URL** | `/gym-buddy-ui/` (signed in) |
| **Expected** | [09-Visual-design.md](../20-Architecture/09-Visual-design.md) leftover table: “Video post composer icon” on mockup 03 → **Images only (max 4). No video.** FS-FEED composer notes the same. |
| **Actual** | `<span title="Video posts are out of scope" class="nav-disabled">Video</span>` next to Image. Disabled leftover chrome is still shipped on the live feed. |
| **Screenshots** | [19-login-unique-result-desktop.png](screenshots/qa-v1.0.0/public/19-login-unique-result-desktop.png), [19-login-unique-result-mobile.png](screenshots/qa-v1.0.0/public/19-login-unique-result-mobile.png) |
| **Console / network** | none |
| **Ticket** | [#94](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/94) |

## Console / network summary

Application JavaScript did not throw. Console `error` lines were resource statuses:

- **404** on every deep link (`/login`, `/register`, `/login/`, `/does-not-exist`) — Pages fallback.
- **403** on garbage `POST /api/v1/auth/login`.
- **409** on duplicate `POST /api/v1/auth/register`.
- **401** on `POST /api/v1/auth/refresh` from the Pages origin (F4).

No CORS *block* was logged from this origin on 2026-08-30. UFW 443 did **not** TLS-EOF this crawler (unlike Sentinel’s 2026-08-18 IPv4 note on #37).

## Screenshot index

All files live under `screenshots/qa-v1.0.0/public/`. Desktop 1280×800 and mobile 390×844 unless noted.

| File | State |
| --- | --- |
| `01-home-logged-out-*` | `/` logged out |
| `02-login-*` | `/login` |
| `03-login-filled-hidden-*` | login filled, password masked |
| `04-login-password-toggle-*` | eye shows password |
| `05-login-empty-submit-*` | empty submit |
| `06-login-invalid-email-*` | `not-an-email` |
| `07-login-garbage-credentials-*` | unknown user |
| `08-login-trailing-slash-*` | `/login/` |
| `09-login-refresh-*` | reload `/login` |
| `10-register-*` | `/register` |
| `11-register-filled-hidden-*` | register filled, masked |
| `12-register-password-toggle-*` | eye on register |
| `13-register-empty-submit-*` | empty submit |
| `14-register-invalid-email-*` | invalid email |
| `15-register-short-password-*` | password `short` |
| `16-register-unique-filled-*` | unique payload filled |
| `17-register-unique-result-*` | after 201 → empty login |
| `18-register-duplicate-*` | duplicate email |
| `19-login-unique-result-*` | signed-in empty feed |
| `20-feed-after-login-*` | full navigation to `/` dropped the memory JWT |
| `22-invalid-route-*` | `/does-not-exist` → home |
| `23-session-before-reload-desktop.png` | signed-in feed |
| `24-session-after-reload-desktop.png` | same tab after reload, signed out |
| `27-suggestions-cta-desktop.png` | `/suggestions` from empty-feed CTA |
| `30-after-logout-desktop.png` | log out → `refresh credential is missing` |
| `31-register-password-equals-email-desktop.png` | FS-ACCT-03 client check |
| `32-register-password-equals-handle-desktop.png` | FS-ACCT-03 client check |
| `33-register-duplicate-handle-desktop.png` | `handle already taken` |
| `34-register-duplicate-email-case-desktop.png` | case-insensitive email |

## Out of scope for this crawl

Friends, events, search, messages, settings, admin, fixtures, media ACL. Empty feed and the suggestions CTA were only opened because they are the post-login `/` state.
