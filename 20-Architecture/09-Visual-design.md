# Visual design

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [04-Frontend.md](04-Frontend.md), [05-Back-office.md](05-Back-office.md), [07-Technology-choices.md](07-Technology-choices.md) |

Visual tokens and Stitch mockups for the member app and the back-office. The design source Joaquim used is the Stitch project [Gym Buddy Web App](https://stitch.withgoogle.com/projects/2603399363233092540). That URL is a **related link**, not the source of truth. This page plus the PNGs under [`mockups/`](mockups/) are the committed source of truth.

The PNGs are **Stitch canvas captures** (1280×800, some Stitch chrome visible). They are **not** live Angular screenshots. Academic report shots stay on [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md) and must wait for a stable UI.

## Color palette

Measured and transcribed from the Stitch style-guide board. Do not invent extra brand hues.

![Stitch style-guide board for Gym Buddy](mockups/00-style-guide.png)

Stitch style-guide board (light mode). Each chip also shows a tint/shade ramp on this PNG. Those ramp hexes are **not** transcribed here.

Light mode (Stitch style guide, transcribed exactly):

| Role | Hex | Notes |
| --- | --- | --- |
| Primary | `#006D77` | Seed / primary buttons |
| Secondary | `#83C5BE` | Mint teal, supporting |
| Tertiary | `#E29578` | Terracotta accent |
| Neutral | `#111827` | Text / ink |

### Dark mode (derived mapping)

Joaquim asked for light + dark without regenerating mockups. Map **roles only**. The dark column is a **derived mapping**, not sampled from a dark Stitch file.

| Role | Light | Dark |
| --- | --- | --- |
| Primary | `#006D77` | `#83C5BE` (lighter teal on dark surfaces so buttons still read) |
| Secondary | `#83C5BE` | `#006D77` |
| Tertiary | `#E29578` | `#E29578` (same accent) |
| Neutral / text | `#111827` | `#F9FAFB` |
| Surface / page | `#FFFFFF` | `#111827` |
| Surface / card | `#F9FAFB` | `#1F2937` |
| Danger (Close account / hide) | `#B91C1C` | `#FCA5A5` |

`#FFFFFF`, `#F9FAFB`, `#1F2937`, and `#FCA5A5` are **derived for theme pairing**; they are not style-guide chips. `#B91C1C` is the **measured** Danger Zone red from [`mockups/16-settings-privacy-danger.png`](mockups/16-settings-privacy-danger.png) (Close Account / Danger Zone on the privacy Stitch capture).

## Typography

Transcribed exactly from the Stitch theme panel:

![Stitch theme panel naming Inter](mockups/00-style-guide-theme.png)

Stitch theme panel. Headline, Body, and Label are all Inter.

- Headline: **Inter**
- Body: **Inter**
- Label: **Inter**

Implementation note: load Inter from Google Fonts (or fontsource) in `gym-buddy-ui`. Suggested weights: **400** (body), **500** (label), **600/700** (headline). Do not add a second family.

## Icons

Stitch did **not** name an icon library.

Recommendation for Angular 22: **Material Symbols Outlined** (`material-symbols-outlined` font, or `@angular/material` + Material Symbols). One set only. Do not add Font Awesome or Lucide unless a later wiki change says so.

Nav in the mockups is home / search / person plus icon buttons; those match Material Symbols Outlined.

## Mockups

Each row is a member route from [04-Frontend.md](04-Frontend.md) or a back-office surface from [05-Back-office.md](05-Back-office.md). Captions describe the Stitch mockup, not a running app.

### Member application

| Route | Spec | Mockup | Caption |
| --- | --- | --- | --- |
| `/register` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Register](mockups/01-register.png) | Stitch mockup of the member register screen (canvas capture, includes Stitch chrome). |
| `/login` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Login](mockups/02-login.png) | Stitch mockup of the member login screen (canvas capture, includes Stitch chrome). |
| `/` (feed) | [FS feed](../30-Functional-specifications/04-News-feed.md) | ![Feed](mockups/03-feed.png) | Stitch mockup of the friends news feed (upper canvas). |
| `/` (feed, lower) | [FS feed](../30-Functional-specifications/04-News-feed.md) | ![Feed lower](mockups/03-feed-lower.png) | Stitch mockup of the same feed scrolled to the lower posts. |
| `/posts/:id` | [FS posts](../30-Functional-specifications/05-Posts-and-engagement.md) | ![Post detail](mockups/04-post-detail.png) | Stitch mockup of a single post with engagement actions. |
| `/posts/:id` (comments) | [FS comments](../30-Functional-specifications/06-Nested-comments.md) | ![Post comments](mockups/04-post-comments.png) | Stitch mockup of the nested comment thread on a post. |
| `/u/:handle` (public) | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Public profile](mockups/05-public-profile.png) | Stitch mockup of a public profile visible to any member. |
| `/u/:handle` (private stub) | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Private profile](mockups/06-private-profile.png) | Stitch mockup of the private-profile stub a stranger sees. |
| `/friends` | [FS friends](../30-Functional-specifications/03-Friends.md) | ![Friends](mockups/07-friends.png) | Stitch mockup of the friends list with search and Unfriend / Block actions. |
| `/friends/suggestions` | [FS suggestions](../30-Functional-specifications/09-Friend-suggestions.md) | ![Friend suggestions](mockups/08-suggestions.png) | Stitch mockup of friend suggestions with Add Friend / Dismiss and interest tags. |
| `/events` | [FS events](../30-Functional-specifications/07-Events.md) | ![Events](mockups/09-events.png) | Stitch mockup of Upcoming Sessions with Instant / Recurring filters and Create Event. |
| `/events/new` | [FS events](../30-Functional-specifications/07-Events.md) | ![Create event](mockups/10-new-event.png) | Stitch mockup of the Create Event form (title, activity, place, schedule, capacity). |
| `/events/:id` | [FS events](../30-Functional-specifications/07-Events.md) | ![Event detail](mockups/11-event-detail.png) | Stitch mockup of event detail with Apply to Join, organizer queue, and occurrence list. |
| `/search` | [FS search](../30-Functional-specifications/08-Advanced-search.md) | ![Search](mockups/12-search.png) | Stitch mockup of people/events search with filters for city, sports, and experience. |
| `/messages` | [FS messaging](../30-Functional-specifications/10-Instant-messaging.md) | ![Inbox](mockups/13-inbox.png) | Stitch mockup of the inbox thread list with unread badges. |
| `/messages/:id` | [FS messaging](../30-Functional-specifications/10-Instant-messaging.md) | ![Chat](mockups/14-chat.png) | Stitch mockup of a chat thread with text, shared image, and a voice bubble. |
| `/settings/profile` | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Edit profile](mockups/15-settings-profile.png) | Stitch mockup of Edit Profile (photo, display name, username, bio, city). |
| `/settings/privacy` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Privacy](mockups/16-settings-privacy.png) | Stitch mockup of profile visibility (Public / Private) and change-password fields. |
| `/settings/privacy` (danger) | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Privacy danger zone](mockups/16-settings-privacy-danger.png) | Stitch mockup of Update Password plus the Danger Zone Close Account control. |

### Back-office

| Surface | Spec | Mockup | Caption |
| --- | --- | --- | --- |
| Users | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin users](mockups/17-admin-users.png) | Stitch mockup of User Management (search, roles, lock state, Invite User). |
| Content | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin content](mockups/18-admin-content.png) | Stitch mockup of Content Moderation with flagged posts and Approve / Hide Content. |
| Reports | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin reports](mockups/19-admin-reports.png) | Stitch mockup of the Reports Queue with priority tiles and Review / Close Report. |
| Media | [FS media](../30-Functional-specifications/12-Media-and-files.md) | ![Admin media](mockups/20-admin-media.png) | Stitch mockup of Media Management (object list, metadata, ACL, read-only delivery URL). |
| Fixtures | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin fixtures](mockups/21-admin-fixtures.png) | Stitch mockup of Database Fixtures generate/reset cards (non-production warning). |
| Audit | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin audit](mockups/22-admin-audit.png) | Stitch mockup of the append-only Audit Log table (timestamp, staff, action, target). |

## What these are not

- Not the academic screenshot checklist in [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md). Do not copy these PNGs there. That gallery waits for real Angular shots after the UI is stable.
- Not a live UI. `gym-buddy-ui` on `develop` still has `/register`, `/login`, and log-out only.
- Login-from-Pages (ticket **#37**) is still **Not Ready**. Do **not** Todo **#37**.
- Expanding `/api/v1` past health + auth is still open. These mockups do not implement those routes.
