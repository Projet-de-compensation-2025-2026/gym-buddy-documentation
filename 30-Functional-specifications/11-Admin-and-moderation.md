# Admin and moderator accounts

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [01-Accounts-and-administration.md](01-Accounts-and-administration.md), [../20-Architecture/05-Back-office.md](../20-Architecture/05-Back-office.md) |

Staff accounts are **created and administered**, not self-serve.

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

## Acceptance

- Given a moderator token, when they call `PATCH /admin/users/:id/role`, then `FORBIDDEN`.
- Given an admin hides a post, when a member fetches it, then `NOT_FOUND`, and an audit row exists.
- Given the last admin, when they demote themselves, then `CONFLICT`.
