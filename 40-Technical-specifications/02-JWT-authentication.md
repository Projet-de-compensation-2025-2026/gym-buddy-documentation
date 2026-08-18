# JWT authentication

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../30-Functional-specifications/01-Accounts-and-administration.md](../30-Functional-specifications/01-Accounts-and-administration.md), [01-API-conventions.md](01-API-conventions.md) |

The brief requires **JWT authentication**. Implementation is ours (no outsourced IdP) so the defense can show claims, expiry, and refresh.

All auth HTTP paths are under `/api/v1`.

## Tokens

| Token | Where it lives | TTL | Contains |
| --- | --- | --- |
| Access | `Authorization` header | 15 minutes | `sub`, `role`, `handle`, `typ=access` |
| Refresh | `HttpOnly; Secure; SameSite=Lax` cookie, path `/api/v1/auth` | 14 days | `sub`, `jti`, `typ=refresh` |

Both are signed with **HS256** at MVP (one secret, `JWT_ACCESS_SECRET`). RS256 is an improvement if a second service must verify.

`SameSite=Lax` is enough for same-site operator/Caddy login. It will **not** ride a github.io → VPS credentialed XHR. Ticket **#31** is **Done / closed** for **only** production `apiBaseUrl` + CORS + live **v0.1.1** (`main-4WJYST2C.js`). Login-from-Pages is a **stronger** claim and is **not** proven. Do **not** write that signup/login from github.io works. The other named blocker is UFW 443 (Joaquim’s IPv6 prefix only; do not publish that prefix). Login-from-Pages is docs **#37**, board **Not Ready**. Do **not** Todo **#37**. Do **not** start Kernel. Joaquim’s home-browser login is an operator-IPv6 try, not Done.

## Claims (access)

```json
{
  "sub": "user-uuid",
  "handle": "alex",
  "role": "member",
  "typ": "access",
  "iat": 0,
  "exp": 0
}
```

Do not put email in the access token (leakage via browser logs).

## Flows

1. `POST /api/v1/auth/register` → user row + profile + (optional) verification mail
2. `POST /api/v1/auth/login` `{ email, password }` → access JSON + `Set-Cookie` refresh
3. `POST /api/v1/auth/refresh` (cookie) → new access, rotated refresh (`jti` replaced)
4. `POST /api/v1/auth/logout` → refresh `jti` denylisted in Redis until `exp`
5. Locked user: login and refresh fail

## Password

Argon2id, memory ≥ 19 MiB, one-way. Timing-safe compare. Generic error on unknown email (“invalid credentials”).

## Guards

A Spring Security filter (or `OncePerRequestFilter`) verifies signature, `exp`, `typ=access`, and that `users.status = active`. A method-security expression (`@PreAuthorize("hasRole('ADMIN')")`) or a dedicated voter checks `role` for `/api/v1/admin/*`.

## Threat notes

| Risk | Mitigation |
| --- | --- |
| Stolen access token | Short TTL |
| Stolen refresh | Rotation + Redis denylist + Secure cookie |
| XSS reading tokens | Prefer memory for access, HttpOnly for refresh |
| Algorithm none | Library configured to refuse `alg=none` |

Sequence: [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md).
