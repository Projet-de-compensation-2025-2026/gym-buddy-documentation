# Accounts and administration

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [11-Admin-and-moderation.md](11-Admin-and-moderation.md), [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md) |

Members can create and manage their account. Admins can lock accounts and change roles.

## Actors

Visitor, member, admin.

## Requirements

| ID | Requirement |
| --- | --- |
| FS-ACCT-01 | A visitor can register with email, handle, password, display name. |
| FS-ACCT-02 | Email and handle are unique (case-insensitive). |
| FS-ACCT-03 | Password ≥ 10 characters, not equal to email or handle. Stored as Argon2id, never logged. |
| FS-ACCT-04 | Successful login returns an access JWT and a refresh credential. |
| FS-ACCT-05 | The member can change password if they present the current password. |
| FS-ACCT-06 | The member can log out; the refresh credential is revoked. |
| FS-ACCT-07 | The member can close their account (soft-delete): content is hidden, files become inaccessible. |
| FS-ACCT-08 | An admin can lock / unlock an account. Locked users cannot authenticate. |
| FS-ACCT-09 | An admin can set `role` to `member`, `moderator`, or `admin`. The last admin cannot be demoted. |
| FS-ACCT-10 | Registration of the first user may become `admin` (bootstrap). Later users are `member`. |

## Acceptance

- Given a free email, when the visitor registers with a valid password, then they can log in.
- Given a locked account, when they post credentials, then the API returns `FORBIDDEN` without revealing whether the password was correct.
- Given an access token after logout/refresh-revoke, when they call a protected route after refresh fails, then they are `UNAUTHENTICATED`.

## Errors

| Situation | Code |
| --- | --- |
| Duplicate email/handle | `CONFLICT` |
| Weak password | `VALIDATION` |
| Wrong current password | `FORBIDDEN` |

## Out of scope here

OAuth social login, WebAuthn. Improvements: [../91-Critical-analysis/02-Improvements.md](../91-Critical-analysis/02-Improvements.md).
