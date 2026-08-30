# QA v1.0.0 — member app (live)

| Field | Value |
| --- | --- |
| Date | 2026-08-30 |
| Target | https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ |
| API | https://vps-c39cdf03.vps.ovh.net/api/v1 |
| Bundle | `main-VXEXHKAI.js`, `ng-version="22.1.2"`, `base href="/gym-buddy-ui/"` |
| Pages `Last-Modified` | 2026-08-30 18:25:19 GMT |
| Crawler | Playwright Chromium, viewports 1280×800 and 390×844 |
| Screenshots | [screenshots/qa-v1.0.0/member/](screenshots/qa-v1.0.0/member/) |
| QA account | `qa.member.1788116222086@example.com` / handle `qamember1788116222086` / displayName `QA Member` |

This is a live crawl of the **v1.0.0** member SPA on GitHub Pages against the OVH VPS. It is not a mockup gallery. Passwords are not recorded here.

## Method

1. HTTP-probe every listed path (`curl` / `fetch`).
2. Unauthenticated Playwright pass on desktop and mobile (`page.goto`, including deep links).
3. Register a unique member, then sign in (client-side navigation, no full reload).
4. Authenticated pass via in-app nav (Feed, Events, Friends, Search, Messages, Settings, avatar, Suggestions CTA).
5. Interactions: compose + like, comment thread, friend Connect, create event, search filters, stranger profile.
6. Reload / deep-link session check.
7. Capture page PNG + overlay of console / failed XHR / HTTP ≥400 per route.

Registration and sign-in **did work** from `github.io` in this crawl (Paris edge). CORS preflight from the Pages origin returned ACAO `https://projet-de-compensation-2025-2026.github.io` with credentials. The crawl was **not** blocked by CORS. Authenticated work used in-app routing because a full reload drops the session (below).

## What works

| Surface | Evidence |
| --- | --- |
| `GET /api/v1/healthz` and `/readyz` | 200 `{"status":"ok"}` |
| Register `POST /auth/register` | 201 from both Node and the SPA |
| Login `POST /auth/login` | 200 `accessToken`; SPA lands on the feed |
| Password eye | Present on register, login, privacy |
| Inter + teal `#006D77` (`rgb(0, 109, 119)`) | Computed on primary buttons; Inter loaded |
| Feed composer, like, own post | `POST /posts` 201 id `813e5b5a-…`; `PUT …/like` 204; UI “Liked” |
| Nested comments | `POST …/comments` 201; thread on `/posts/{id}` |
| Friends request | `POST /friendships` 201 pending; Friends outbound + profile “Cancel request” |
| Create event + detail | `POST /events` 201 id `647dcb2e-…`; `GET /events/{id}` 200 |
| Suggestions empty state | Copy + “Match me this week” |
| Inbox empty state | “No conversations yet. Message a friend to start.” |
| Settings profile / privacy | Visibility, password, close-account (no Billing / Notifications leftovers) |
| Public stranger profile | `/u/probe1788116222086` stub + Add/Cancel |

## HTTP probes (Pages)

| Path | Status | Notes |
| --- | --- | --- |
| `/gym-buddy-ui/` | 200 | Member index |
| `/gym-buddy-ui/index.html` | 200 | |
| `/gym-buddy-ui/404.html` | 200 | Same SPA body |
| `/gym-buddy-ui/login`, `/register`, `/friends`, `/search`, `/suggestions`, `/events`, `/events/new`, `/messages`, `/settings/profile`, `/settings/privacy`, `/u/demo.alex`, `/posts/1` | **404** | Same 18084-byte SPA HTML (`Content-Type: text/html`). Browser still boots Angular. Console: `Failed to load resource: 404`. |

Unauthenticated deep links that the router treats as guarded then client-redirect to `/login` (still a 404 document). `/friends/suggestions` and `/settings` land on the marketing home instead of `/login`.

## Defects (ticketed)

Each row is one GitHub **Bug** on `gym-buddy-documentation`, label `bug`, type Bug, Gym Buddy Project **Not Ready**. Closed as duplicates of the public crawl: **#98 → #89** (session cookie), **#100 → #94** (Video leftover), **#110 → #95** (unknown-route 404 UI).

| Issue | Defect | Shot | FS |
| --- | --- | --- | --- |
| [#96](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/96) | `GET /api/v1/events?size=50` is HTTP **500** even after a successful `POST /events` + `GET /events/{id}` 200. Organizer cannot see their own session in the list. | `spa-desktop-events.png`, `spa-desktop-events-console-network.png` | FS-EVT |
| [#97](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/97) | Events list paints **both** “Request failed” (red) **and** “No upcoming sessions.” Dual error/empty state. | `spa-desktop-events.png` | FS-EVT |
| [#98](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/98) | Session dies on reload / cold deep link. Access JWT is memory-only; Playwright `context.cookies()` is empty after login (refresh cookie never stored for `github.io` → `vps.ovh.net`, `SameSite=Lax`). Reload of `/` shows the marketing landing. | `spa-desktop-feed.png` then `spa-desktop-feed-after-reload.png` | FS-ACCT-04, TS-JWT |
| [#99](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/99) | Every member client route except `/` is HTTP 404 with the SPA index. Console 404 on `/login`, `/register`, `/friends`, … | `unauth-desktop-register-after-submit-console-network.png` | Hosting |
| [#100](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/100) | Feed composer still has a **Video** control. Wiki leftover chrome: images only, max 4, no video. | `spa-desktop-feed.png`, `unauth-desktop-login-after-submit.png` | FS-POST-01 |
| [#101](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/101) | People search does not send `q` until **Apply Filters**. Typing `alex` / Enter still calls `GET /search/people?size=20` (directory). | `spa-desktop-search.png` vs `spa-desktop-search-apply-filters-alex.png` | FS-SRCH-02 |
| [#102](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/102) | Search **Events** tab leaves `/search` and opens `/events` (the 500 list). `GET /api/v1/search/events` was never issued in this crawl. | `spa-desktop-search.png`, `spa-desktop-search-events-real.png` | FS-SRCH-01 |
| [#103](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/103) | Live handle `joaquim.keloglanian@gmail.com` (displayName Test1). Profile URL `/u/joaquim.keloglanian@gmail.com`. Handle must not be an email. | `spa-desktop-profile-email-handle.png` | FS-ACCT-01/02 |
| [#104](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/104) | Copy “**1 Likes**” / “**1 Comments**”. | `spa-desktop-post-after-comment.png` | FS-FEED-06 |
| [#105](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/105) | Profile **Info** shows “Flexible” when `preferredWindows: []`. | `spa-desktop-profile-self.png` | FS-PROF-01 |
| [#106](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/106) | 390×844 header wraps: nav on one row, avatar / Settings / Log out on the next; composer controls wrap. No compact mobile chrome. | `spa-mobile-feed.png` | Frontend a11y |
| [#107](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/107) | `/suggestions` underlines **Friends** in the top nav (wrong active item). | `spa-desktop-suggestions.png` | FS-SUGG |
| [#108](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/108) | Unauthenticated `/friends/suggestions` and `/settings` show the marketing home instead of `/login`. Other guarded routes do redirect. | `unauth-desktop-suggestions-alt.png`, `unauth-desktop-settings.png` | FS-ACCT, FS-PROF-05 |
| [#109](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/109) | Search filter rail always shows **10 km** radius though the viewer has no coordinates (`lat`/`lng` null). FS-SRCH-03: radius only if the viewer has coordinates. | `spa-desktop-search.png` | FS-SRCH-03 |
| [#110](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation/issues/110) | Unknown path `/this-route-does-not-exist` shows the marketing home (unauth) or the feed (authed client nav). No not-found UI. | `unauth-desktop-unknown.png` | Frontend |

## Route notes (authenticated, in-app)

| Route | Result | Shot |
| --- | --- | --- |
| `/` feed | Empty-state CTA, then own post after compose. Video leftover. | `spa-desktop-feed.png`, `spa-desktop-feed-after-compose.png` |
| `/friends` | Empty inbound/friends; outbound pending after Connect. | `spa-desktop-friends.png`, `spa-desktop-friends-after-connect.png` |
| `/search` | People directory (no `q`) + filters. Cards omit handle, so two “QA Admin Crawler” look identical. Connect works. | `spa-desktop-search.png` |
| `/suggestions` | Empty state + weekly match checkbox. Nav active = Friends. | `spa-desktop-suggestions.png` |
| `/events` | 500 + dual empty/error. Create Event CTA works. | `spa-desktop-events.png` |
| `/events/new` | Form matches mockup 10 closely. Recurrence Off. Submit 201. | `spa-desktop-events-new-blank.png`, `spa-desktop-events-new-submitted.png` |
| `/events/647dcb2e-…` | Detail OK (Friends-Only, 8/8 seats, Next 90 Days). Locale `sam. 5 sept.` (fr). | `spa-desktop-events-new-submitted.png` |
| `/messages` | Empty inbox + compose pencil. No thread to open (no accepted friends). | `spa-desktop-messages.png` |
| `/settings/profile` | Edit profile. Max 8 MiB (correct vs leftover “Max 2MB”). Sport chips listed. | `spa-desktop-settings-profile.png` |
| `/settings/privacy` | Public/Private, password, close account. No Billing / Notifications. | `spa-desktop-settings-privacy.png` |
| `/u/{self}` | Public profile, 0 friends, “Flexible”. | `spa-desktop-profile-self.png` |
| `/u/probe1788116222086` | Stranger + Cancel request. | `spa-desktop-profile-probe.png` |
| `/posts/813e5b5a-…` | Like, comment composer, delete, reply. | `spa-desktop-post-detail.png`, `spa-desktop-post-after-comment.png` |

`demo.alex` / `demo.blake` are **not** in live people search. Prod has other crawler/probe accounts, not the named demo pair.

## Console / XHR (unique)

- `Failed to load resource: 404` on every deep link (`/login`, `/friends`, …).
- `Failed to load resource: 500` on `GET https://vps-c39cdf03.vps.ovh.net/api/v1/events?size=50` (repeated). Body: `{"status":500,"error":"Internal Server Error","path":"/api/v1/events"}`.
- No `pageerror` Angular exceptions in this crawl.
- No CORS failures from this network.
- No broken `<img>` naturalWidth=0.

## Leftover chrome hunt

| Item | Live? |
| --- | --- |
| Billing / Notifications | **Absent** (privacy is Profile + Privacy only) |
| Workout tracker / Current Focus bars | **Absent** |
| Video composer | **Present — bug** |
| External share | **Absent** (Like / Repost / Comment only) |
| Avatar “Max 2MB” | **Absent** (shows 8 MiB) |
| Miles | **Absent** (km) |
| “Recover by logging back in” | **Absent** (close-account copy matches spec) |

## Mockup vs live (severe only)

Tokens: Inter + primary `#006D77` match [20-Architecture/09-Visual-design.md](../20-Architecture/09-Visual-design.md). Not filed as token bugs.

Severe mismatches filed above: Video on feed (mockup leftover, out of contract); events list unusable; search Events tab not an in-page index; mobile wrap vs “usable on a phone browser”.

## Blocked / not exercised

- Chat image/audio (FS-MSG-04/05): no accepted friend, empty inbox.
- Event apply / accept / full (FS-EVT-05..07): list 500; created event is friends-only with 0 applicants.
- Nested comments depth 4: only one root comment created.
- Signed URL / denied media (FS-MED-06): no avatar upload in this pass.
- `demo.alex` stranger private stub: account missing on live.

## Screenshot index

Files live under `screenshots/qa-v1.0.0/member/`. Prefixes:

- `unauth-desktop-*` / `unauth-mobile-*` — cold `page.goto` (many are login or marketing because of 404 + guard).
- `spa-desktop-*` / `spa-mobile-*` — authenticated in-app navigation.
- `*-console-network.png` — overlay of console + XHR for that step.
