# QA v1.0.0 — Angular back-office

| Field | Value |
| --- | --- |
| Date | 2026-08-30 |
| Agent | QA crawler (`qa-admin`) |
| Target | Gym Buddy **v1.0.0** admin Angular app (`gym-buddy-admin`, output `dist-admin`) |
| Viewports | 1280×800 desktop, 390×844 mobile (Playwright Chromium) |
| Screenshots | [screenshots/qa-v1.0.0/admin/](screenshots/qa-v1.0.0/admin/) (64 PNG) |
| Specs | [20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md), [30-Functional-specifications/11-Admin-and-moderation.md](../30-Functional-specifications/11-Admin-and-moderation.md), mockups 17–22 |
| Branch | `feature/71-qa-admin` (from `develop`) |

Wiki mockup JPGs were **not** copied. Every shot below is from the live GitHub Pages build.

## Live URL discovery

Tried, in order:

| URL | HTTP | What loaded |
| --- | --- | --- |
| https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/admin/ | **200** | `<admin-root>`, title **Gym Buddy Admin**, `base href="/gym-buddy-ui/admin/"`, bundle `main-T4ESUBGX.js` |
| https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/admin/login | **404** | **Member** SPA (`<app-root>`, title Gym Buddy, `base href="/gym-buddy-ui/"`) via site-root `404.html` |
| https://projet-de-compensation-2025-2026.github.io/gym-buddy-admin/ | **404** | GitHub Pages “There isn’t a GitHub Pages site here.” |

The back-office **is** published, as a second Angular project inside `gym-buddy-ui` (`pnpm exec ng build gym-buddy-admin` → `dist-admin` → `_site/admin/`). That matches [20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md) (“not a fourth repository”). **Do not** treat `gym-buddy-admin` Pages 404 as “admin not deployed”. The real v1.0.0 ship bug is that **only the directory index works**; every staff client route 404s into the member app.

Deploy copies **member** `index.html` to `_site/404.html` and never writes `_site/admin/404.html`. GitHub Pages has one custom 404 at the site root, so `/admin/login`, `/admin/users`, `/admin/content`, `/admin/reports`, `/admin/media`, `/admin/fixtures`, `/admin/audit` all serve the member bundle.

Live admin `apiBaseUrl` is `https://vps-c39cdf03.vps.ovh.net/api/v1` (no localhost). `GET /api/v1/healthz` from this crawler: **200** `{"status":"ok"}`. CORS preflight from `https://projet-de-compensation-2025-2026.github.io` on `GET /admin/users`: **200** with ACAO + credentials.

## Passes (do not reticket)

| Check | Evidence |
| --- | --- |
| Admin bundle is a separate app | `/admin/` title Gym Buddy Admin, `<admin-root>`, not the member landing |
| Leftover mockup chrome is **absent** from the live login + admin JS | No Dashboard, Bookings, Analytics, Invite User, Export CSV, Billing, + New Session in `main-T4ESUBGX.js` or on-screen text |
| No self-serve staff register | Admin login has Email + Password + Sign in only. Member `POST /auth/register` returns `role: "member"` |
| Member login on admin does **not** leak staff UI | After a valid member JWT: red **Staff accounts only.** Nav Users/Content/Reports/Media/Fixtures/Audit never appears |
| Member `GET/POST /api/v1/admin/*` is **NOT_FOUND** (FS-ADM) | Bearer member token → 404 `{"error":{"code":"NOT_FOUND","message":"not found"}}` on users, reports, media, audit, hide, fixtures |
| Staff routes are not member UI | Member landing has no Admin Portal chrome |
| Login empty submit validates | “Enter a valid email and password.” |

## Findings (bugs)

Severity: **blocker** / **high** / **medium**. Tickets opened on `gym-buddy-documentation` with type **Bug**, label `bug`, Gym Buddy Project status **Not Ready**. Numbers filled after create.

### B1 — Admin SPA deep links 404 into the member app — **blocker**

Refreshing or sharing `/admin/login`, `/admin/users`, `/content`, `/reports`, `/media`, `/fixtures`, `/audit` returns HTTP **404** and boots the **member** app (Sign in / Sign up). `staffGuard` then `navigateByUrl('/login')` is the same trap after a reload.

Console: `Failed to load resource: the server responded with a status of 404 ()` for every staff path.

Shots: `desktop-10-deeplink-login.png`, `desktop-10-deeplink-users.png` (same member landing for content/reports/media/fixtures/audit), `mobile-10-deeplink-*.png`, `desktop-00-gym-buddy-admin-pages-404.png` (the unused host).

Only `/admin/` (trailing slash / `index.html`) boots the admin app, then client-redirects to `/admin/login` without a full reload — that path works until the user refreshes.

### B2 — Desktop login card is crushed into the 14rem nav column — **high**

`.shell` is always `grid-template-columns: 14rem 1fr`. When the aside is not rendered (signed-out), `main` occupies the **first** 224px track. The “card” is ~160px wide; email/password inputs and the Sign in button overflow the white panel. Emails clip (`demo.admin@fixtures.gym.t…`, `qaadmmtg6c74d@qa.gym.t…`).

Computed: `shellGrid = 224px 1056px`. Mobile (`max-width: 48rem`) is a single column and looks fine.

Shots: `desktop-02-admin-root-after-boot.png`, `desktop-03-admin-login-empty-submit.png`, `desktop-05-admin-login-demo-admin-fixture.png`, `desktop-07-admin-login-member-rejected.png` vs `mobile-02-admin-root-after-boot.png`.

### B3 — Admin login has no password visibility toggle — **medium**

Member `/login` has the ticket **#34** eye. Admin login is `input type="password"` only (`hasPasswordEye: false`). Same JWT issuer, same staff who must type long `.env` secrets.

Shots: `desktop-02-admin-root-after-boot.png` vs `desktop-20-member-login-deeplink.png`.

### B4 — `demo.admin` / `demo.mod` do not exist on the VPS — **blocker** (fixture-not-run-on-prod)

Wiki named staff (`demo.admin`, `demo.mod`, emails `demo.*@fixtures.gym.test`, passwords in local `.env` only) are **local fixture seed**. `POST /admin/fixtures` is **disabled on `prod`**. Live login:

| Attempt | Result |
| --- | --- |
| `demo.admin@fixtures.gym.test` / `change-me-local-demo` | **403** `FORBIDDEN` `invalid credentials` |
| `demo.mod@fixtures.gym.test` / same | **403** same |
| handle `demo.admin` in the email field | client “Enter a valid email and password.”; API **422** `VALIDATION` `email` `format` |

Without a staff JWT this crawl **could not open Users / Content / Reports / Media / Fixtures / Audit**. Academic shots 15–16 in [03-Screenshots.md](03-Screenshots.md) stay blocked on prod.

Shots: `desktop-05-admin-login-demo-admin-fixture.png`, `desktop-06-admin-login-demo-mod-fixture.png`, `desktop-04-admin-login-handle-not-email.png`.

### B5 — Member bundle ships the generated admin HTTP client — **high** (FS-ADM-09 / architecture)

Live member `main-VXEXHKAI.js` contains `getAdminUsers`, `postAdminFixtures`, and the string `/admin/users` (orval `GymBuddyAPIService` is shared). Staff **UI** strings (`User Management`, `Admin Portal`, `Database Fixtures`) are absent — good — but members still download staff operations. Architecture: “Members must not receive staff UI in the member JavaScript bundle.”

### B6 — Content Moderation is a UUID paste form; no unhide — **high** (FS-ADM-03)

Live `content.page.ts` (same as shipped bundle): type + id + reason, then `POST .../hide`. No searchable posts/comments/events table as mockup 18. **No unhide control** even though `postAdminContentTypeIdUnhide` exists. Hide-from-report only if `GET /admin/reports` returns rows.

Could not screenshot the authenticated page (B4). Source + live JS.

### B7 — Media Management has no ACL inspector / signed-URL revoke — **high**

Architecture Media: “Inspect an object’s ACL and revoke signed access.” Live page lists `kind`, mime, bytes, id, owner, objectKey, hidden flag, and a **Revoke / hide** that only `POST .../content/media/{id}/hide` with hardcoded reason `revoke signed access`. No ACL table, no active signed URL, no unhide.

Mockup 20 leftover nav must stay unimplemented; the **ACL + revoke** surface is in-scope.

### B8 — Fixtures surface is two buttons + leftover ticket copy; no counts — **medium**

Copy: “Generating thousands of rows is ticket #70; these buttons record the trigger.” Spec counts (3 000 users, 15 000 posts, …) from [07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md) are not shown. Nav includes Fixtures for every staff session; buttons hide unless `isAdmin()`. Prod must return `FORBIDDEN` (acceptance) — cannot prove without a staff token.

### B9 — Lock/hide reasons are hardcoded — **medium** (FS-ADM-04/06)

Users `lock()` always posts `{ reason: "policy abuse" }`. No prompt. Audit will only ever record that string from this UI.

### B10 — Fixtures and Audit sit in the staff nav for moderators — **medium**

Architecture: moderator = search/hide/close reports; admin = plus roles, lock/unlock, fixtures, **audit log**. `app.html` always renders Users, Content, Reports, Media, **Fixtures**, **Audit** once `isStaff()`. Fixtures page gates buttons; Audit page still calls `GET /admin/audit`.

### B11 — Unauthenticated `/api/v1/admin/*` is 401 `ISO-8859-1` — **medium**

`GET /admin/users` without a token: **401** `UNAUTHENTICATED` `Content-Type: application/json;charset=ISO-8859-1`. Member-with-token is correctly **404 NOT_FOUND**. Spec error table is about members; 401 for missing JWT is reasonable, but the Latin-1 charset is wrong.

### B12 — Admin login is email-only while fixtures are documented as handles — **medium**

Staff docs list `demo.admin` / `demo.mod` as **handles**. The form is `input type="email"` + `Validators.email`. Typing the documented handle never reaches the API.

## Leftover chrome checklist (mockups 17–22)

| Leftover | Must not ship | Live v1.0.0 |
| --- | --- | --- |
| Dashboard widgets | yes | **absent** |
| Bookings | yes | **absent** |
| Analytics | yes | **absent** |
| Invite User | yes | **absent** |
| Export CSV | yes | **absent** |
| Billing | yes | **absent** |
| + New Session | yes | **absent** |

Nav **intended**: Users, Content, Reports, Media, Fixtures, Audit. Cannot screenshot the signed-in nav (B4); login has no leftover items. Source `admin/app/app.html` matches the intended six links.

## Route crawl (Playwright)

From `/admin/` (SPA boot → `/admin/login`):

| Route | Full document load | After SPA boot |
| --- | --- | --- |
| `/admin/` | 200 admin → client `/login` | Admin Portal sign-in |
| `/admin/login` | 404 **member** app | n/a (never stays admin on refresh) |
| `/admin/users` | 404 member | `staffGuard` would send `/login` if the admin bundle were serving |
| `/admin/content` | 404 member | same |
| `/admin/reports` | 404 member | same |
| `/admin/media` | 404 member | same |
| `/admin/fixtures` | 404 member | same |
| `/admin/audit` | 404 member | same |

Member hitting `/gym-buddy-ui/admin/` while signed in as member: admin app still loads (separate origin path); login with that member JWT shows **Staff accounts only.** and does not render the six-link nav.

## API probes (2026-08-30, this network)

| Call | Status | Body |
| --- | --- | --- |
| `GET /healthz` | 200 | `{"status":"ok"}` |
| `OPTIONS /admin/users` Pages origin | 200 | ACAO github.io, credentials true |
| `GET /admin/users` no token | 401 | `UNAUTHENTICATED` ISO-8859-1 |
| `POST /auth/login` demo.admin@fixtures.gym.test | 403 | `FORBIDDEN` invalid credentials |
| `POST /auth/register` qaadm… | 201 | `role: member` |
| `POST /auth/login` that member | 200 | access JWT `role=member` |
| member `GET /admin/users\|reports\|media\|audit` | 404 | `NOT_FOUND` |
| member `POST /admin/fixtures` | 404 | `NOT_FOUND` |
| member `POST /admin/content/post/{uuid}/hide` | 404 | `NOT_FOUND` |

Refresh cookie is `HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth`. Access token is in the JSON body, so the **first** admin login from Pages can work if a staff user exists (B4). Refresh from github.io will not ride (known #37, closed).

## Console + failed network

No Angular `pageerror`. Failed requests are the 404 document loads of staff routes and the expected 403 logins. No mixed-content, no `127.0.0.1` in the admin bundle.

## Screenshots index

Directory: `99-Academic-deliverables/screenshots/qa-v1.0.0/admin/`. Prefix `desktop-` (1280×800) or `mobile-` (390×844).

| File | What |
| --- | --- |
| `00-gym-buddy-admin-pages-404` | Unused host `gym-buddy-admin` GitHub Pages 404 |
| `01-member-404-html` | Site-root `404.html` (member SPA) |
| `02-admin-root-after-boot` | Live admin login after `/admin/` |
| `03-admin-login-empty-submit` | Validation |
| `04-admin-login-handle-not-email` | `demo.admin` handle rejected |
| `05-admin-login-demo-admin-fixture` | invalid credentials |
| `06-admin-login-demo-mod-fixture` | invalid credentials |
| `07-admin-login-member-rejected` | Staff accounts only. |
| `10-deeplink-{login,users,content,reports,media,fixtures,audit,root}` | Full-load each path |
| `11-spa-history-*` / `12-spa-click-*` | History/click attempts (full load still member 404) |
| `20-member-login-deeplink` | Member login + password eye (contrast) |
| `21-member-root` | Member landing, no admin chrome |
| `22-admin-login-a11y` | Login labels/headings |

## Tickets

Opened from this crawl (type **Bug**, label `bug`, Gym Buddy Project status **Not Ready**):

| Finding | Ticket |
| --- | --- |
| B1 Admin SPA deep links 404 into the member app | [#75](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/75) |
| B2 Desktop login crushed into 14rem nav column | [#76](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/76) |
| B3 No password eye on admin login | [#77](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/77) |
| B4 `demo.admin` / `demo.mod` missing on VPS | [#78](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/78) |
| B5 Member bundle ships admin HTTP client | [#79](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/79) |
| B6 Content is UUID paste, not a queue | [#80](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/80) |
| B7 No unhide | [#81](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/81) |
| B7b Media ACL / signed-URL revoke missing | [#82](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/82) |
| B8 Fixtures counts + ticket #70 leftover copy | [#83](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/83) |
| B9 Hardcoded lock/hide reasons | [#84](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/84) |
| B11 Unauthenticated admin JSON `ISO-8859-1` | [#85](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/85) |
| B10 Fixtures/Audit in moderator nav | [#86](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/86) |
| B12 Handle vs email login | [#87](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/87) |

Did **not** open `[GB] Publish the admin bundle on GitHub Pages`: `/gym-buddy-ui/admin/` is HTTP 200 and serves `gym-buddy-admin`. The unused host `/gym-buddy-admin/` 404 is expected (not a fourth repository). The ship bug is **#75** (deep-link 404 into the member `404.html`).
