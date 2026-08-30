# Back-office

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [09-Visual-design.md](09-Visual-design.md), [../30-Functional-specifications/11-Admin-and-moderation.md](../30-Functional-specifications/11-Admin-and-moderation.md), [../30-Functional-specifications/01-Accounts-and-administration.md](../30-Functional-specifications/01-Accounts-and-administration.md) |

The back-office is a **separate Angular application** (or a clearly isolated `/admin` configuration with its own bundle) **inside `gym-buddy-ui`**. It is not a fourth repository. Members must not receive staff UI in the member JavaScript bundle.

## Who uses it

| Role | Can |
| --- | --- |
| Moderator | Search users/posts/events, hide/unhide content, close reports |
| Admin | Everything a moderator can, plus roles, lock/unlock accounts, trigger fixtures, view audit log |

JWT access tokens for staff include `role ∈ {moderator, admin}`. The API enforces this; the UI only hides buttons.

## Visual design

Staff-console visual tokens and mockups for Users, Content, Reports, Media, Fixtures, and Audit: [09-Visual-design.md](09-Visual-design.md). Those JPGs are Joaquim’s mockup screens, not a live back-office.

## Surfaces

| Area | Purpose |
| --- | --- |
| Users | Find account, change role, lock, reset visibility |
| Content | Posts, comments, events — hide with reason |
| Reports | Queue of member reports |
| Media | Inspect an object’s ACL and revoke signed access |
| Fixtures | Generate or reset thousands of rows (non-production) |
| Audit | Append-only staff actions |

## Why it is separate

1. The brief asks to **design and implement** backend, frontend, **and** back-office.
2. Staff workflows (tables, filters, bulk actions) fight member UX (feed, chat).
3. Smaller member bundle, clearer authorization story at the defense.

Staff authentication still uses the same JWT issuer as the member app.
