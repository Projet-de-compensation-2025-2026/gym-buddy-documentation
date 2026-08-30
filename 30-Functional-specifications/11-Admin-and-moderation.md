# Admin and moderator accounts

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [01-Accounts-and-administration.md](01-Accounts-and-administration.md), [../20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md) |

## Intent

Staff accounts are **created and administered**, not self-serve. The brief requires admin / moderator accounts **and** a back-office.

## Actors

Moderator, admin. Members report content. Members must not receive staff JS in the member bundle.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-ADM-01 | Roles: `member`, `moderator`, `admin`. Stored on `users.role`. |
| FS-ADM-02 | Only an admin can promote or demote. Moderators cannot create admins. |
| FS-ADM-03 | Moderators can hide/unhide posts, comments, events, and media, with a reason. |
| FS-ADM-04 | Moderators can lock a member for policy abuse; they cannot change roles. |
| FS-ADM-05 | Admins can do everything moderators can, plus role changes and fixture triggers. |
| FS-ADM-06 | Every staff mutation writes an `audit_events` row (actor, action, target, reason, at). |
| FS-ADM-07 | Members can report a user, post, comment, or event. Reports appear in the back-office queue. |
| FS-ADM-08 | Staff authenticate with the same JWT issuer; access tokens carry `role`. |
| FS-ADM-09 | The member frontend does not expose staff routes. |

Also implements remaining FS-ACCT-08 (lock/unlock) and FS-ACCT-09 (roles) from [01-Accounts-and-administration.md](01-Accounts-and-administration.md).

## Business rules

- Last admin cannot demote or lock themselves (`CONFLICT`).
- Hide is not a member delete: members see `NOT_FOUND`; staff see the row + reason.
- Back-office is a **separate Angular application** (or isolated `/admin` configuration with its own bundle) inside `gym-buddy-ui` ([../20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md)).
- Mockup leftovers **not** to implement: Dashboard widgets, Bookings, Analytics, Invite User, Export CSV, + New Session, Billing. Nav is Users, Content, Reports, Media, Fixtures, Audit.

## Target HTTP

All under `/api/v1`. Member `POST /reports`. Staff `/admin/*` — members get `NOT_FOUND`.

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/admin/users` | FS-ADM, FS-ACCT-08/09 |
| `POST` | `/admin/users/{id}/lock` | FS-ACCT-08, FS-ADM-04 |
| `POST` | `/admin/users/{id}/unlock` | FS-ACCT-08 |
| `PATCH` | `/admin/users/{id}/role` | FS-ACCT-09, FS-ADM-02 |
| `POST` | `/admin/content/{type}/{id}/hide` | FS-ADM-03 |
| `POST` | `/admin/content/{type}/{id}/unhide` | FS-ADM-03 |
| `GET` | `/admin/reports` | FS-ADM-07 |
| `POST` | `/admin/reports/{id}/resolve` | FS-ADM-07 |
| `POST` | `/reports` | FS-ADM-07 |
| `GET` | `/admin/media` | FS-ADM, FS-MED |
| `POST` | `/admin/fixtures` | FS-ADM-05 |
| `POST` | `/admin/fixtures/reset` | FS-ADM-05 |
| `GET` | `/admin/audit` | FS-ADM-06 |

## UI

| Surface | Mockup |
| --- | --- |
| Users | [17-admin-users.jpg](../20-Architecture/mockups/17-admin-users.jpg) — search, role dropdown, lock. Ignore Invite / Export. |
| Content | [18-admin-content.jpg](../20-Architecture/mockups/18-admin-content.jpg) |
| Reports | [19-admin-reports.jpg](../20-Architecture/mockups/19-admin-reports.jpg) |
| Media | [20-admin-media.jpg](../20-Architecture/mockups/20-admin-media.jpg) |
| Fixtures | [21-admin-fixtures.jpg](../20-Architecture/mockups/21-admin-fixtures.jpg) — generate/reset; counts from [../40-Technical-specifications/07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md). Ignore leftover nav. |
| Audit | [22-admin-audit.jpg](../20-Architecture/mockups/22-admin-audit.jpg) |

## Acceptance

- Given a moderator token, when they call `PATCH /admin/users/:id/role`, then `FORBIDDEN`.
- Given an admin hides a post, when a member fetches it, then `NOT_FOUND`, and an audit row exists.
- Given the last admin, when they demote themselves, then `CONFLICT`.
- Given a member token, when they `GET /admin/users`, then `NOT_FOUND` (not `403` that advertises the route).
- Given `prod` profile, when `POST /admin/fixtures` is called, then it is disabled (`FORBIDDEN`).

## Errors

| Situation | Code |
| --- | --- |
| Member hits `/admin/*` | `NOT_FOUND` |
| Moderator changes role | `FORBIDDEN` |
| Last admin demote/lock self | `CONFLICT` |
| Missing hide reason | `VALIDATION` |

## Links

- Back-office architecture: [../20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md)
- Fixtures: [../40-Technical-specifications/07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
