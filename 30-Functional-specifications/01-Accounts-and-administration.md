# Accounts and administration

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [11-Admin-and-moderation.md](11-Admin-and-moderation.md), [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md), [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md) |

## Intent

Members create and manage their account (register, log in, log out, change password, close). Admins lock accounts and change roles. JWT is the session mechanism.

## Actors

Visitor, member, admin.

## Requirements

| ID | Requirement | Today |
| --- | --- | --- |
| FS-ACCT-01 | A visitor can register with email, handle, password, display name. | **Done** (#12) |
| FS-ACCT-02 | Email and handle are unique (case-insensitive). | **Done** (#12) |
| FS-ACCT-03 | Password ≥ 10 characters, not equal to email or handle. Stored as Argon2id, never logged. | **Done** (#12) |
| FS-ACCT-04 | Successful login returns an access JWT and a refresh credential. | **Done** (#12) |
| FS-ACCT-05 | The member can change password if they present the current password. | Remaining |
| FS-ACCT-06 | The member can log out; the refresh credential is revoked. | **Done** (#12) |
| FS-ACCT-07 | The member can close their account (soft-delete): content is hidden, files become inaccessible. | Remaining |
| FS-ACCT-08 | An admin can lock / unlock an account. Locked users cannot authenticate. Unlock also restores `closed`. | Remaining (admin) |
| FS-ACCT-09 | An admin can set `role` to `member`, `moderator`, or `admin`. The last admin cannot be demoted. | Remaining (admin) |
| FS-ACCT-10 | Registration of the first user may become `admin` (bootstrap). Later users are `member`. | **Done** (#12) |

## Business rules

- `users.status` ∈ `active` \| `locked` \| `pending_verification` \| `closed`. Flyway V2 currently omits `closed`; remaining work adds it.
- Closed is not “log in to recover”. After `POST /me/close`, login and refresh fail with the same generic `FORBIDDEN` as a locked account. Staff restore with unlock. Mockup 16’s “recover by logging back in” is leftover copy, not the contract.
- Password change (`POST /auth/password`) verifies the current password, writes a new Argon2id hash, and denylists every refresh `jti` except none — the client must log in again **or** the current refresh is rotated once and all others revoked. Prefer: revoke all refresh tokens; return 204; client goes to `/login`.
- Handle remains unique on profile edit (FS-ACCT-02). Handle is **not** an email: it must not contain `@` and must not equal the account email (`VALIDATION` on `POST /auth/register` and `PATCH /profiles/me`, ticket **#103**).
- JWT details: [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md). Do not reticket register / login / refresh / logout.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `POST` | `/api/v1/auth/password` | FS-ACCT-05 |
| `POST` | `/api/v1/me/close` | FS-ACCT-07 |

Lock / role routes live on the admin ticket ([11-Admin-and-moderation.md](11-Admin-and-moderation.md)). Full table: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md).

## UI

| Route | Mockup | Notes |
| --- | --- | --- |
| `/register`, `/login` | [01-register.jpg](../20-Architecture/mockups/01-register.jpg), [02-login.jpg](../20-Architecture/mockups/02-login.jpg) | **Done** (#12, #34 eye). |
| `/settings/privacy` | [16-settings-privacy.jpg](../20-Architecture/mockups/16-settings-privacy.jpg) | Remaining: Change Password + Danger Zone Close Account. Profile Visibility belongs to [02-User-profiles.md](02-User-profiles.md). Do **not** implement Notifications. |

## Acceptance

- Given a free email, when the visitor registers with a valid password, then they can log in. (**#12**)
- Given a locked or closed account, when they post credentials, then the API returns `FORBIDDEN` without revealing whether the password was correct.
- Given an access token after logout/refresh-revoke, when they call a protected route after refresh fails, then they are `UNAUTHENTICATED`. (**#12**)
- Given the current password, when the member posts a valid new password, then the old password no longer logs in and previous refresh cookies fail.
- Given a wrong current password on change, when they post, then `FORBIDDEN` and the hash is unchanged.
- Given Close Account with the current password, when they confirm, then their profile, posts, and media URLs are hidden and login fails.

## Errors

| Situation | Code |
| --- | --- |
| Duplicate email/handle | `CONFLICT` |
| Weak password | `VALIDATION` |
| Wrong current password | `FORBIDDEN` |
| Close without password | `VALIDATION` |
| Already closed / locked login | `FORBIDDEN` (generic) |

## Out of scope here

OAuth social login, WebAuthn, self-service reopen. Improvements: [../91-Critical-analysis/02-Improvements.md](../91-Critical-analysis/02-Improvements.md).

## Links

- JWT: [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md)
- Admin: [11-Admin-and-moderation.md](11-Admin-and-moderation.md)
- Sequence (login): [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md)
- Use cases: [../60-UML-diagrams/01-Use-cases.md](../60-UML-diagrams/01-Use-cases.md)
