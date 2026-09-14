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
| Access | `Authorization` header (memory on the SPA; never `localStorage`) | 15 minutes | `sub`, `role`, `handle`, `typ=access` |
| Refresh | `HttpOnly; Secure; SameSite=None; Partitioned` cookie, path `/api/v1/auth` | 14 days | `sub`, `jti`, `typ=refresh` |

Both are signed with **HS256** at MVP (one secret, `JWT_ACCESS_SECRET`). RS256 is an improvement if a second service must verify.

The refresh cookie is HttpOnly, Secure, SameSite=None and Partitioned, scoped to `/api/v1/auth`. Credentialed CORS allows the Pages origin. The access token stays in memory. Browser cookie behavior must be verified on the actual deployed origins.

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

1. `POST /api/v1/auth/register` → user row + profile
2. `POST /api/v1/auth/login` `{ email, password }` → access JSON + `Set-Cookie` refresh
3. `POST /api/v1/auth/refresh` (cookie) → new access, rotated refresh (`jti` replaced)
4. `POST /api/v1/auth/logout` → refresh credential revoked in Redis
5. Locked user: login and refresh fail

## Password

Argon2id, memory ≥ 19 MiB, one-way. Timing-safe compare. Generic error on unknown email (“invalid credentials”).

## Guards

`AccessTokenFilter` validates the access credential and supplies the current principal. Resource services enforce ownership, membership, visibility and staff permissions. Account state is checked server-side. Refresh rotation consumes the prior credential atomically in Redis; password/account changes invalidate relevant credentials.

## Threat notes

| Risk | Mitigation |
| --- | --- |
| Stolen access token | Short TTL |
| Stolen refresh | Atomic rotation + Redis credential state + Secure cookie |
| XSS reading tokens | Prefer memory for access, HttpOnly for refresh |
| Algorithm none | Library configured to refuse `alg=none` |

Sequence: [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md).
