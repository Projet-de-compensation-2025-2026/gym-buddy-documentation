# Visual design

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [04-Frontend.md](04-Frontend.md), [05-Back-office.md](05-Back-office.md), [07-Technology-choices.md](07-Technology-choices.md) |

Visual tokens and mockups for the member app and the back-office. Joaquim replaced the earlier Stitch canvas PNGs with higher-quality JPG screens on `fix/mockups`. The committed source of truth is this page plus the files under [`mockups/`](mockups/). The Stitch project [Gym Buddy Web App](https://stitch.withgoogle.com/projects/2603399363233092540) is a **related link**, not the SoT.

These JPGs are **mockup screens**, not live Angular screenshots. Academic report shots stay on [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md) and must wait for a stable UI.

Design tokens Joaquim added for this pass live in [`mockups/00-DESIGN.md`](mockups/00-DESIGN.md) (frontmatter + brand notes). The measured tables below stay from the earlier Stitch captures until a later wiki change replaces them.

## Color palette

Do not invent extra brand hues. Three tables: Stitch board chips, pixels sampled from the earlier mockup chrome, and a derived dark mapping. Prefer **Measured on screenshots** for implementation, except the primary seed (see the 1-RGB webp note).

### Stitch tokens

The style-guide PNGs (`00-style-guide.png`, `00-style-guide-theme.png`) are gone on this branch. Use [`mockups/00-DESIGN.md`](mockups/00-DESIGN.md) for Joaquim’s current token dump.

| Role | Hex | Notes |
| --- | --- | --- |
| Primary | `#006D77` | Seed / primary buttons |
| Secondary | `#83C5BE` | Mint teal, supporting |
| Tertiary | `#E29578` | Terracotta accent |
| Neutral | `#111827` | Text / ink on the board (screens use a different ink — see next table) |

### Measured on screenshots

Pixel-sampled from the earlier Stitch canvas captures. **Prefer this table for implementation.** Primary on the mockup chrome is `#006E78` (11188 px mode). That is a **1-RGB webp delta** from the board seed; the token to implement is still **`#006D77`**. Reject `#008D97` (distance 43.8 from the seed; white-on-it contrast 3.99, fails AA).

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

Joaquim asked for light + dark without regenerating mockups. **Derived mapping**, not sampled from a dark file. No new brand hues.

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

Headline, Body, and Label are all **Inter** (Stitch theme panel and `00-DESIGN.md`).

- Headline: **Inter**
- Body: **Inter**
- Label: **Inter**

Implementation note: load Inter from Google Fonts (or fontsource) in `gym-buddy-ui`. Suggested weights: **400** (body), **500** (label), **600/700** (headline). Do not add a second family.

## Icons

Stitch did **not** name an icon library.

Recommendation for Angular 22: **Material Symbols Outlined** (`material-symbols-outlined` font, or `@angular/material` + Material Symbols). One set only. Do not add Font Awesome or Lucide unless a later wiki change says so.

## Mockups

Each row is a member route from [04-Frontend.md](04-Frontend.md) or a back-office surface from [05-Back-office.md](05-Back-office.md). Captions describe the mockup screen, not a running app. Filenames match `mockups/*.jpg` on this branch.

Dropped from this pass (no replacement file): `03-feed-lower`, `04-post-detail`, `16-settings-privacy-danger`, and the two style-guide PNGs.

### Member application

| Route | Spec | Mockup | Caption |
| --- | --- | --- | --- |
| `/register` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Register](mockups/01-register.jpg) | High-quality mockup of the member register screen. |
| `/login` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Login](mockups/02-login.jpg) | High-quality mockup of the member login screen. |
| `/` (feed) | [FS feed](../30-Functional-specifications/04-News-feed.md) | ![Feed](mockups/03-feed.jpg) | High-quality mockup of the friends news feed. |
| `/posts/:id` (comments) | [FS comments](../30-Functional-specifications/06-Nested-comments.md) | ![Post comments](mockups/04-post-comments.jpg) | High-quality mockup of the nested comment thread on a post. |
| `/u/:handle` (public) | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Public profile](mockups/05-public-profile.jpg) | High-quality mockup of a public profile visible to any member. |
| `/u/:handle` (public, partial) | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Public profile partially hidden](mockups/05-public-profile-partially-hidden.jpg) | High-quality mockup of a public profile with some fields hidden. |
| `/u/:handle` (private stub) | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Private profile](mockups/06-private-profile.jpg) | High-quality mockup of the private-profile stub a stranger sees. |
| `/friends` | [FS friends](../30-Functional-specifications/03-Friends.md) | ![Friends](mockups/07-friends.jpg) | High-quality mockup of the friends list with search and Unfriend / Block. |
| `/friends/suggestions` | [FS suggestions](../30-Functional-specifications/09-Friend-suggestions.md) | ![Friend suggestions](mockups/08-suggestions.jpg) | High-quality mockup of friend suggestions with Add Friend / Dismiss. |
| `/events` | [FS events](../30-Functional-specifications/07-Events.md) | ![Events](mockups/09-events.jpg) | High-quality mockup of Upcoming Sessions with Instant / Recurring filters. |
| `/events/new` | [FS events](../30-Functional-specifications/07-Events.md) | ![Create event](mockups/10-new-event.jpg) | High-quality mockup of the Create Event form. |
| `/events/:id` | [FS events](../30-Functional-specifications/07-Events.md) | ![Event detail](mockups/11-event-detail.jpg) | High-quality mockup of event detail with Apply to Join and occurrence list. |
| `/search` | [FS search](../30-Functional-specifications/08-Advanced-search.md) | ![Search](mockups/12-search.jpg) | High-quality mockup of people/events search with filters. |
| `/messages` | [FS messaging](../30-Functional-specifications/10-Instant-messaging.md) | ![Inbox](mockups/13-inbox.jpg) | High-quality mockup of the inbox thread list. |
| `/messages/:id` | [FS messaging](../30-Functional-specifications/10-Instant-messaging.md) | ![Chat](mockups/14-chat.jpg) | High-quality mockup of a chat thread. |
| `/settings/profile` | [FS profiles](../30-Functional-specifications/02-User-profiles.md) | ![Edit profile](mockups/15-settings-profile.jpg) | High-quality mockup of Edit Profile. |
| `/settings/privacy` | [FS accounts](../30-Functional-specifications/01-Accounts-and-administration.md) | ![Privacy](mockups/16-settings-privacy.jpg) | High-quality mockup of profile visibility and password fields. |

### Back-office

| Surface | Spec | Mockup | Caption |
| --- | --- | --- | --- |
| Users | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin users](mockups/17-admin-users.jpg) | High-quality mockup of User Management. |
| Content | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin content](mockups/18-admin-content.jpg) | High-quality mockup of Content Moderation. |
| Reports | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin reports](mockups/19-admin-reports.jpg) | High-quality mockup of the Reports Queue. |
| Media | [FS media](../30-Functional-specifications/12-Media-and-files.md) | ![Admin media](mockups/20-admin-media.jpg) | High-quality mockup of Media Management. |
| Fixtures | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin fixtures](mockups/21-admin-fixtures.jpg) | High-quality mockup of Database Fixtures generate/reset. |
| Audit | [FS admin](../30-Functional-specifications/11-Admin-and-moderation.md) | ![Admin audit](mockups/22-admin-audit.jpg) | High-quality mockup of the append-only Audit Log. |

## What these are not

- Not the academic screenshot checklist in [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md). Do not copy these JPGs there. That gallery waits for real Angular shots after the UI is stable.
- Not a live UI. `gym-buddy-ui` on `develop` still has `/register`, `/login`, and log-out only.
- Ticket **#37** is **closed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** Todo it. Do **not** start Kernel on it.
- Expanding `/api/v1` past health + auth is still open. These mockups do not implement those routes.
