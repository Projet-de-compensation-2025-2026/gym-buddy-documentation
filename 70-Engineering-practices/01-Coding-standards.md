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
6. Format with the repo tools (Spotless / Palantir for Java, Prettier + Angular ESLint for the frontend). CI **applies** `format.sh --write`; `github-actions[bot]` commits if the tree is dirty. A format-on-commit hook is not required.
7. The tree must be clean after that bot commit (and after merge). Test and smoke still run in the same CI job.
8. HTTP shapes come from `gym-buddy-openapi`, not from ad-hoc DTOs that drift.

## Java (backend)

- Target **Java 25 LTS**
- `null` avoided at boundaries: `Optional` for absence, Bean Validation on incoming payloads
- Constructor injection only; no field `@Autowired`
- Packages follow modules (`…auth`, `…events`, `…suggestions`)
- Business rules live in plain Java; Spring annotations stay in adapters
- No wildcard imports

## TypeScript / Angular (frontend)

- **Approved and today** (`gym-buddy-ui` `develop`, app `0.1.0`): TypeScript **6** (`~6.0.2`), `strict` true. Angular 22 `@angular/compiler-cli` **22.1.2** peers `>=6.0 <6.1`. Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed). Do **not** treat 7.0.0 or 7.0.2 as the approved compiler. Do not pin `@typescript/native-preview` / `tsgo`.
- Standalone components, typed forms
- Do not store the access token in `localStorage` (XSS)
- Empty, loading, and error states are mandatory for list pages
- No `any` without a one-line reason
- Consume the **generated** OpenAPI client; do not hand-write duplicate interfaces

## Node package manager (frontend and any Node work)

**Approved:** **pnpm**. Stop using npm as the project package manager. These are requirements, not optional.

1. Set `packageManager` to a pinned `pnpm@X.Y.Z`. Enable **Corepack** so CI and agents use that same binary. Do not install `latest` (`corepack prepare pnpm@latest`, `npm i -g pnpm@latest`, or an unpinned `pnpm` on `PATH`).
2. Commit `pnpm-lock.yaml`. CI installs from that lockfile.
3. Four-week supply-chain delay. The setting is in **minutes**: **40320**.
   - Canonical (current pnpm): `pnpm-workspace.yaml` → `minimumReleaseAge: 40320`
   - Older pnpm fallback: `.npmrc` → `minimum-release-age=40320`
   - **Do not invent a `package.json` field.** pnpm does not read this from `package.json`.
4. Disable or tightly allow dependency lifecycle scripts (`onlyBuiltDependencies` and/or ignore-scripts). Required. Empty allow-list unless a native addon must build. Keep the allow-list in `pnpm-workspace.yaml` (or `.npmrc` for older pnpm), not a made-up `package.json` key.

**Today and approved** `gym-buddy-ui` on `develop` is **`pnpm@11.22.0`** (ui #4 / `63bebed`; ticket **#23** Done): committed `pnpm-lock.yaml`, `minimumReleaseAge` **40320**. TypeScript is **6** (`~6.0.2`). Ticket #24 is cancelled. Do **not** claim TypeScript 7 shipped.

Renovate / Dependabot cooldown must be at least as long as this floor (four weeks). The pipeline contract is [07-CI-CD.md](07-CI-CD.md).

## SQL / Flyway

- Migrations are the only schema change path
- No raw SQL string concatenation; parameterized only (`PreparedStatement` / Spring `NamedParameterJdbcTemplate`)
- Destructive migrations require a note in the PR

## Comments

Comment *why*, not *what*. Do not narrate commits inside the source.
