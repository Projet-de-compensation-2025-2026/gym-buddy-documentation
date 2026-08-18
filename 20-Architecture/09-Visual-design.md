# Visual design

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [04-Frontend.md](04-Frontend.md), [05-Back-office.md](05-Back-office.md), [07-Technology-choices.md](07-Technology-choices.md) |

Visual tokens and Stitch mockups for the member app and the back-office. The design source Joaquim used is the Stitch project [Gym Buddy Web App](https://stitch.withgoogle.com/projects/2603399363233092540). That URL is a **related link**, not the source of truth. This page plus the PNGs under [`mockups/`](mockups/) are the committed source of truth.

The PNGs are **Stitch canvas captures** (1280×800, some Stitch chrome visible). They are **not** live Angular screenshots. Academic report shots stay on [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md) and must wait for a stable UI.

## Color palette

Do not invent extra brand hues. Three tables: Stitch board chips, pixels sampled from the mockup chrome, and a derived dark mapping. Prefer **Measured on screenshots** for implementation, except the primary seed (see the 1-RGB webp note).

### Stitch tokens

![Stitch style-guide board for Gym Buddy](mockups/00-style-guide.png)

Transcribed from the Stitch style-guide board. Each chip also shows a tint/shade ramp on this PNG. Those ramp hexes are **not** transcribed here.

| Role | Hex | Notes |
| --- | --- | --- |
| Primary | `#006D77` | Seed / primary buttons |
| Secondary | `#83C5BE` | Mint teal, supporting |
| Tertiary | `#E29578` | Terracotta accent |
| Neutral | `#111827` | Text / ink on the board (screens use a different ink — see next table) |

### Measured on screenshots

Pixel-sampled from the Stitch canvas captures. **Prefer this table for implementation.** Primary on the mockup chrome is `#006E78` (11188 px mode). That is a **1-RGB webp delta** from the board seed; the token to implement is still **`#006D77`**. Reject `#008D97` (distance 43.8 from the seed; white-on-it contrast 3.99, fails AA).

| Role | Measured | Implement | Notes |
| --- | --- | --- | --- |
| primary | `#006E78` | `#006D77` | Teal buttons; 1-RGB webp delta |
| primary_hover | `#00545A` | `#00545A` | |
| primary_soft / badge_bg | `#CDF2F1` | `#CDF2F1` | |
| on_primary | `#FFFFFF` | `#FFFFFF` | |
| accent_orange | `#E09577` | `#E29578` | Style-guide terracotta, lossy; board said `#E29578` |
| surface_bg | `#F4F6F8` | `#F4F6F8` | |
| surface_card / input | `#FFFFFF` | `#FFFFFF` | |
| surface_muted | `#E8E8EC` | `#E8E8EC` | |
| text_primary | `#212325` | `#212325` | Not `#111827` on the screens |
| text_secondary | `#6E7174` | `#6E7174` | |
| border | `#E5E7E9` | `#E5E7E9` | |
| success | primary teal | `#006D77` | No separate green |
| success_bg | `#F8FEF9` | `#F8FEF9` | |
| warning / danger | `#8D302F` on `#FEDAD6` | `#8D302F` / `#FEDAD6` | Text on wash |

Secondary `#83C5BE` is a Stitch board chip only. It was not a mode on the mockup chrome and is not an implement token here.

### Dark mapping

Joaquim asked for light + dark without regenerating mockups. **Derived mapping**, not sampled from a dark Stitch file. No new brand hues.

| Role | Light (implement) | Dark |
| --- | --- | --- |
| filled button | `#006D77` (`#006E78` measured) | Keep `#006E78` / `#006D77` as **filled buttons only** (white text contrast 6.00) |
| body text | `#212325` | `#FFFFFF` / `#E5E7E9`. Do **not** use teal as body text on dark (fails AA) |
| surface_bg | `#F4F6F8` | `#212325` |
| surface_card | `#FFFFFF` | `#26282A` |
| input | `#FFFFFF` | `#232526` |
| surface_muted | `#E8E8EC` | `#1F2123` |
| border | `#E5E7E9` | `#6E7174` |
| success / badge | `#CDF2F1` as badge background | Pale teal `#CDF2F1` for success / badge **text** on dark |
| warning / danger | `#8D302F` on `#FEDAD6` | Invert: text `#FEDAD6` on `#8D302F` |

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
