# Coding standards

| Field | Value |
| --- | --- |
| Status | Approved |

## Applies to

All Gym Buddies application repositories. This wiki uses Markdown rules in [04-Documentation-conventions.md](04-Documentation-conventions.md).

## Universal

1. One obvious module per bounded context (see backend modules).
2. Domain rules do not import HTTP, Spring Web, or Angular.
3. No secrets in git. `.env.example` / `application-example.yml` list keys only.
4. Fail closed: missing auth → 401; missing ACL → 404.
5. Functions that implement FS/TS IDs mention those IDs in the test name.
6. Format on commit (Spotless / Palantir for Java, Prettier + Angular ESLint for the frontend).
7. Lint must pass in CI.
8. HTTP shapes come from `gym-buddy-openapi`, not from ad-hoc DTOs that drift.

## Java (backend)

- Target **Java 26** (fallback Java 25 LTS if a dependency cannot run on 26)
- `null` avoided at boundaries: `Optional` for absence, Bean Validation on incoming payloads
- Constructor injection only; no field `@Autowired`
- Packages follow modules (`…auth`, `…events`, `…suggestions`)
- Business rules live in plain Java; Spring annotations stay in adapters
- No wildcard imports

## TypeScript / Angular (frontend)

- **TypeScript 7.0**, `strict` true
- Standalone components, typed forms
- Do not store the access token in `localStorage` (XSS)
- Empty, loading, and error states are mandatory for list pages
- No `any` without a one-line reason
- Consume the **generated** OpenAPI client; do not hand-write duplicate interfaces

## SQL / Flyway

- Migrations are the only schema change path
- No raw SQL string concatenation; parameterized only (`PreparedStatement` / Spring `NamedParameterJdbcTemplate`)
- Destructive migrations require a note in the PR

## Comments

Comment *why*, not *what*. Do not narrate commits inside the source.
