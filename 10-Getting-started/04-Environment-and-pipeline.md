# Environment and pipeline

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Related-repositories.md](02-Related-repositories.md), [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md), [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md) |

How to run Gym Buddies locally, how a change is proven and released, and how the live API lands on the VPS. This page is the runbook. The CI/CD contract lives in [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md). Feature work still starts on the wiki: [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md).

## Today versus target

Be honest at the defense. The pipeline, the VPS API replace path, the **local data-plane files**, and the **Java 25 LTS / Spring Boot** service exist on `develop` (`pom.xml`, ticket #11). Local compose runtime is **proven on a laptop** ([gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`; evidence: [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md)). `gym-buddy-service` `develop` implements `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` ([gym-buddy-service#5](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/5) / `e2ef2aa`): Argon2id, HS256 access JWT, refresh cookie, Redis denylist — [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md). OpenAPI stub (openapi #4) and UI pages (ui #3) were already on `develop`. Ticket #12 is **closed / Done**. VPS apply **is done**. Ticket **#20** is **Done / closed**. The VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` on `127.0.0.1:8080` both return **200**. API bind `127.0.0.1`; data-plane ports unpublished. A bad loopback `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. It is **not** a GHCR pull, a Release tag, or a successful replace-from-registry. Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. `gym-buddy-ui` GitHub Pages is **live** (ticket **#30** Done; first tag **v0.1.0**): https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ returns **HTTP 200** with production `baseHref` `/gym-buddy-ui/`. Root 200 is the acceptance. Direct `/register` is **HTTP 404** with the SPA index body (`404.html`) — not a broken app and not a working auth route. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. Ticket **#31** is **Done / closed**. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Documentation `0.3.0` foundation: [../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md). There is no planned application `0.2.0` next slice.

| Piece | Today (August 2026) | Target (locked) |
| --- | --- | --- |
| `gym-buddy-service` | Java 25 LTS / Spring Boot (`pom.xml` on `develop`). Flyway `V1__baseline.sql` and `V2__users_and_profiles.sql`. Implements `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (service #5 / `e2ef2aa`). Ticket **#47** is **Done** (`develop` **`3ffdef8`** / service #11): `generate-sources` generates models + API interfaces from gym-buddy-openapi tag **v0.1.0** `$ref` tree (`openapi/openapi.yaml`). It no longer fetches `develop` / `openapi/bundled.yaml`. Ticket **#41** stays **Done** as history (`c40f122` / service #10 from that bundle). Branch `feature/47-openapi-package` is gone. Only `develop` + `main` remain. `AuthController` implements `AuthApi`; `HealthController` implements `DefaultApi`. Generated sources are **not** committed. Login JSON is `accessToken` only (spec). Handle `minLength` 1. SameSite=`Lax` unchanged. `pom.xml` stays **0.2.0-SNAPSHOT**. Do **not** treat `springdoc` `/v3/api-docs` as the source of truth. Do **not** claim the service is handwritten. `compose.yaml` and `.env.example` are in the repo. VPS Java container on the host is `develop` **`aea1c56`**. `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. Caddy register/login is **proven from the operator network**. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. | Java 25 LTS / Spring Boot modular monolith. Keep pinning the versioned `gym-buddy-openapi` **package / tag** (`v0.1.0` `$ref` tree landed, ticket **#47** Done). Controllers implement generated interfaces. `pom.xml` is the consumer, not a second contract. |
| `gym-buddy-openapi` | OpenAPI 3.1 (`info.version` `0.1.0`). **Today:** `$ref` tree on `develop` **`8ae3bb8`**. `openapi/bundled.yaml` is **gone on `develop`** ([gym-buddy-openapi#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/7) / ticket **#54** Done / **`8ae3bb8`**). The `$ref` tree stays. CI no longer requires the file. Tag **v0.1.0** still contains `openapi/bundled.yaml` (blob sha `a71ee49b5b9d5665ce3fb6b026868c13a7bfec06`) — that is **history**. Do **not** claim the tag was rewritten. Dual maintenance is gone. `package.json` is **0.1.0**. Same six routes / operationIds as before (`getHealthz`, `getReadyz`, `postAuthRegister`, `postAuthLogin`, `postAuthRefresh`, `postAuthLogout`). Editors edit the `$ref` tree. Both consumers pin tag **v0.1.0** and generate from `openapi/openapi.yaml` (service **`3ffdef8`** / ticket **#47** Done; UI **`47eac9c`** / ticket **#48** Done; lockfile **`9c7c123`**). Ticket **#40** stays **Done** as history (`$ref` tree + checked-in bundle on **`7fa5108`**). Git tag **v0.1.0** exists (ticket **#46** Done; annotated **`6373a11`** → **`9c7c123`** on `main`). The service on `develop` implements the four auth operations. This repo is the HTTP source of truth. Ticket **#41** is **Done** (`c40f122`). Ticket **#42** is **Done** (`b8da6bf`). Ticket **#47** is **Done**. Ticket **#48** is **Done**. Do **not** claim the service is handwritten. GitHub Pages is **not** live. Release run [32155209479](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/actions/runs/32155209479) created tag **v0.1.0**, then failed only on deploy/pages: “Failed to create deployment (status: 404)… Ensure GitHub Pages has been enabled.” Live https://projet-de-compensation-2025-2026.github.io/gym-buddy-openapi/ is HTTP **404**. The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. | **Versioned package.** Generators read the `$ref` tree (`openapi/openapi.yaml`). Already tagged **v0.1.0**. Both consumers pin that **tag/version**. Dual maintenance is gone. `bundled.yaml` is **gone on `develop`**. Full contract; health stays `GET /api/v1/healthz` and `GET /api/v1/readyz`. |
| `gym-buddy-ui` | Angular 22 (app version `0.1.0`; includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`), **TypeScript `~6.0.2`**, **`packageManager`: `pnpm@11.22.0`** (ui #4 / `63bebed`; ticket **#23** Done; committed `pnpm-lock.yaml`; `minimumReleaseAge` **40320**): `/register`, `/login`, and a log-out control that call `POST /api/v1/auth/register`, `/login`, `/logout` (ui #3). Ticket **#48** is **Done** (`develop` **`47eac9c`** / ui #11): pin `github:Projet-de-compensation-2025-2026/gym-buddy-openapi#v0.1.0` (lockfile **`9c7c123`**). orval reads `node_modules/gym-buddy-openapi/openapi/openapi.yaml`. No `bundled.yaml` GET. Branch `feature/48-openapi-package` is gone. Only `develop` + `main` remain. Ticket **#42** stays **Done** as history (`b8da6bf` from `openapi/bundled.yaml`). **No** vendored YAML in the UI tree. Do **not** vendor `openapi.yaml` into this repo. TypeScript stays **`~6.0.2`**. App version stays **0.1.0**. `AuthApi` is a thin wrapper; login / refresh / logout keep `withCredentials`. Access JWT in memory. Refresh cookie credentials sent (`path /api/v1/auth`). No friends / feed / events. Service auth is on `develop`. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. GitHub Pages **live** (ticket **#30** Done; first tag **v0.1.0**): https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ is HTTP **200**, production `baseHref` `/gym-buddy-ui/`. Root 200 is the acceptance. Direct `/register` is HTTP **404** with the SPA index body (`404.html`) — Pages fallback, not a broken app and not a working auth route. A password visibility toggle (eye) is on `develop` (`75fbbce` / ui #9 / ticket #34 Done). The live **v0.1.1** bundle (`main-4WJYST2C.js`) includes the password eye. UI `develop` **`7916fa8`** has production `apiBaseUrl` `https://vps-c39cdf03.vps.ovh.net/api/v1`. Live Pages is **v0.1.1** and embeds that VPS URL. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`. Ticket **#31** is **Done / closed**. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed). Do **not** claim TypeScript 7 landed. | Angular 22 + **TypeScript 6** (`~6.0.2`) + **pnpm** (Corepack pin, committed `pnpm-lock.yaml`, `minimumReleaseAge` **40320** minutes, `onlyBuiltDependencies` and/or ignore-scripts) member app + back-office. Keep pinning the versioned `gym-buddy-openapi` **package / tag** (`v0.1.0` `$ref` tree landed, ticket **#48** Done). Do **not** vendor a copy of the YAML. |
| Health | Service implements unauthenticated `GET /api/v1/healthz` (liveness) and `GET /api/v1/readyz` (`200` or `503` with `details` for `postgres` / `objectStorage`). CI smoke hits **`GET /api/v1/healthz` only** — the smoke image is built without Postgres/MinIO. Probe `GET /` is not today’s service smoke. | Same public paths. Do not smoke `/actuator/health`. |
| Local data plane | Laptop compose **proven** ([gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`, 2026-08-18 10:40:55Z): `cp .env.example .env && docker compose up -d --build`. Postgres 18.6, Redis 8.10.0, MinIO `RELEASE.2025-09-07T16-13-09Z`, Java 25.0.3 Temurin / Spring Boot 4.1.0. Binds `127.0.0.1` only (`8080`, `5432`, `6379`, `9000`, `9001`). `GET /api/v1/healthz` → 200 `{"status":"ok"}`. `GET /api/v1/readyz` → 200 `{"status":"ok"}`. Evidence: [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md). `.env` stays gitignored; only `.env.example` is in git. **Not** the VPS. | Same file |
| VM | Apply **done**. Ticket **#20** **Done / closed**. VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200** on `127.0.0.1:8080`. API bind `127.0.0.1`; data-plane ports unpublished. A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. | Same loopback API + private data plane; GHCR replace when a version is tagged |
| Caddy (operator network) | **Proven** (Sentinel, from his PC). `GET /api/v1/healthz` → **200**. `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**. `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. CORS is **proven from Joaquim’s PC** on **aea1c56**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. Today’s VPS container is **aea1c56**. Password eye is on live **v0.1.1**. Ticket **#34** is **Done**. First tag **v0.1.0** pointed at localhost — that is history, not today. | Same public entry; **#31** Done; Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. |
| Production object storage | `SPRING_PROFILES_ACTIVE=prod` **refuses to start** if S3-compatible storage is missing | Same |

Public health is `healthz` / `readyz`, not `/actuator/health`.

## Ready-to-code checklist

A laptop is ready when all of these are true:

1. **JDK 25 LTS** installed (see [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md)).
2. **Docker** and Compose v2 available.
3. **Node** matching `gym-buddy-ui` `engines`. **Today and approved:** Corepack + the pinned `packageManager` (`pnpm@11.22.0`, ui #4 / `63bebed`; ticket **#23** Done), then `pnpm install` from the committed `pnpm-lock.yaml`. TypeScript is **6** (`~6.0.2`). Angular 22 includes `@angular/compiler-cli` **22.1.2**, peer `>=6.0 <6.1`. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Ticket #24 is cancelled. Do **not** claim TypeScript 7 landed. Do not install `pnpm@latest`.
4. Clone the four repositories (URLs in [02-Related-repositories.md](02-Related-repositories.md)). Default branch is `develop` everywhere.
5. `compose.yaml` and `.env.example` are in `gym-buddy-service` (ticket #7).
6. Copy `.env.example` to `.env` locally. Fill secrets there. Never commit `.env`.
7. `docker compose up -d --build` binds every published port to `127.0.0.1`.
8. Flyway **V1 baseline** and **V2** (`users` + `profiles`) are on `develop`. Remaining domain tables from [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) are later.
9. `gym-buddy-openapi` is the HTTP source of truth. Edit the `$ref` tree **before** implementing a new route. **Today** both consumers pin tag **v0.1.0** and generate from `openapi/openapi.yaml` (tickets **#47** / **#48** Done). `openapi/bundled.yaml` is **gone on `develop`** ([gym-buddy-openapi#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/7) / ticket **#54** Done / **`8ae3bb8`**). The `$ref` tree stays. CI no longer requires the file. Tag **v0.1.0** still contains `openapi/bundled.yaml` (blob sha `a71ee49b5b9d5665ce3fb6b026868c13a7bfec06`) — that is **history**. Do **not** claim the tag was rewritten. Dual maintenance is gone. Ticket **#41** and ticket **#42** stay **Done** as history.
10. Point the UI at `http://localhost:8080/api/v1`.

`docker compose up -d --build` is how a laptop starts the data plane plus the Spring API. That boot is **proven** on a laptop ([gym-buddy-service#6](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/6) / `025a351`; [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md)). The API uses Postgres, Redis, and MinIO (`readyz` 200). This is **not** how the VPS runs.

## Local Compose

Compose is the **local** story. It is not how the VPS runs. File: `compose.yaml` at the root of [gym-buddy-service](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service).

```bash
cp .env.example .env
docker compose up -d --build
# optional SMTP catcher
docker compose --profile mail up -d
```

Clone `gym-buddy-ui` next to `gym-buddy-service` (`../gym-buddy-ui`). Compose builds that tree into an nginx image and publishes **http://127.0.0.1:4200** (member) and **http://127.0.0.1:4200/admin/** (back-office). The UI proxies `/api` to the API container so login cookies stay first-party. `pnpm start` on the host is still valid if you do not want the UI image.

Recorded laptop run (2026-08-18 12:40 PT / 10:40:55Z): `GET /api/v1/healthz` and `GET /api/v1/readyz` both 200 `{"status":"ok"}`. Published ports were `127.0.0.1` only. Write-up: [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md) on `gym-buddy-service` `develop`. Do not paste secrets. `.env` stays gitignored. That proof predates the UI image; `127.0.0.1:4200` is the later Compose add-on.

| Service | Image role | Host bind | Port |
| --- | --- | --- |
| UI | nginx: member + `/admin/` + `/api` proxy | `127.0.0.1` | `4200` |
| API | Spring Boot (Java 25 LTS image) | `127.0.0.1` | `8080` (`API_HOST_PORT` if that port is already taken) |
| PostgreSQL | **18** (not 19), image `postgres:18.6` | `127.0.0.1` | `5432` (`POSTGRES_HOST_PORT` if that port is already taken) |
| Redis | Cache / refresh denylist, image `redis:8-alpine` | `127.0.0.1` | `6379` |
| MinIO | S3 API | `127.0.0.1` | `9000` |
| MinIO console | Local admin UI | `127.0.0.1` | `9001` |
| MailHog (optional, profile `mail`) | SMTP catcher | `127.0.0.1` | SMTP `1025`, UI `8025` |

Bind `127.0.0.1` on every published port. Do not publish the data plane to `0.0.0.0`.

The API container is given Docker-network URLs (`postgres`, `redis`, `minio`). `.env.example` documents the **host** URLs (`127.0.0.1`) for `psql` / Redis Insight / the MinIO console.

### Environment catalog (keys only)

Values live in a local `.env` that is **not** committed. This table is names and purpose only.

| Key | Where | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Local / VPS env file | PostgreSQL 18 connection |
| `REDIS_URL` | Local / VPS env file | Cache, refresh denylist, rate limits |
| `JWT_ACCESS_SECRET` | Local / VM | HS256 signing secret for access tokens |
| `S3_ENDPOINT` | Local MinIO / later production bucket | S3-compatible API URL |
| `S3_BUCKET` | Local / production | Bucket name |
| `S3_ACCESS_KEY` | Local / production | Object-store access key |
| `S3_SECRET_KEY` | Local / production | Object-store secret key |
| `S3_REGION` | Local / production | Region string the client library expects |
| `FIXTURE_SEED` | Local / CI fixtures | Fixed seed `20260813` |
| `DEMO_ADMIN_PASSWORD` | Local `.env` / VPS env file | Password for `demo.admin` (fixture seed or staff bootstrap). Placeholder only. |
| `DEMO_MOD_PASSWORD` | Local `.env` / VPS env file | Password for `demo.mod` (fixture seed or staff bootstrap). Placeholder only. |
| `GYM_BUDDY_BOOTSTRAP_STAFF` | VPS env file, optional | `true` inserts missing `demo.admin` / `demo.mod` on API start. Leave unset / `false` afterwards. Does **not** enable `POST /admin/fixtures` on `prod`. |
| `SPRING_PROFILES_ACTIVE` | Local / VM | `local` / `test` / `prod`. Production refuses to start without object storage. |
| `DEPLOY_HOST` | GitHub Actions only | SSH host for service Deploy |
| `DEPLOY_USER` | GitHub Actions only | SSH user |
| `DEPLOY_SSH_KEY` | GitHub Actions only | SSH private key (PEM) |
| `DEPLOY_PORT` | GitHub Actions only, optional | SSH port, default `22` |
| `DEPLOY_BIND` | VM replace script, optional | Container publish address, default `127.0.0.1`. `0.0.0.0` is refused. |
| `DEPLOY_NETWORK` | VM replace script, optional | Docker network to join, default `gym-buddy-data` |
| `DEPLOY_ENV_FILE` | VM replace script, optional | VPS env file, default `/etc/gym-buddy/vps.env` (not in git) |

`POSTGRES_PASSWORD` is a compose helper used to create the PostgreSQL role. It is not an application key; the API reads `DATABASE_URL`.

Do not put JWT values, key material, or demo passwords in this wiki.

### Demo users

These handles always exist after a local fixture seed. Passwords live in the local `.env` only.

| Handle | Role |
| --- | --- |
| `demo.alex` | member |
| `demo.blake` | member, friend of alex |
| `demo.mod` | moderator |
| `demo.admin` | admin |

Flyway on `develop` is **V1 baseline** plus **V2** (`users` + `profiles`, service #5 / `e2ef2aa`). Later migrations will implement the rest of [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md). Fixture generation uses **Datafaker** with `FIXTURE_SEED=20260813` — [../40-Technical-specifications/07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md).

### Live VPS staff (no prod fixtures)

`POST /api/v1/admin/fixtures` stays **FORBIDDEN** on `prod`. Live v1.0.0 therefore has **no** `demo.admin` / `demo.mod` until an operator bootstraps them (ticket **#78**). Academic shots 15–16 need a documented staff sign-in.

One-shot (preferred): on the host, in `/etc/gym-buddy/vps.env` (not in git):

```text
GYM_BUDDY_BOOTSTRAP_STAFF=true
DEMO_ADMIN_PASSWORD=
DEMO_MOD_PASSWORD=
```

Fill the two password placeholders on the host. `replace.sh` forwards those keys when they are set. Restart the API once. The process inserts `demo.admin` (`demo.admin@fixtures.gym.test`, role `admin`) and `demo.mod` (`demo.mod@fixtures.gym.test`, role `moderator`) **only if those handles and emails are missing**. Then **remove** `GYM_BUDDY_BOOTSTRAP_STAFF` (or set `false`) and replace again so the flag is off. Accounts stay. Do not commit real production passwords. `.env.example` / `deploy/vps.env.example` stay placeholders.

CLI equivalent (same env, still allowed on `prod` because it is not the fixture generator):

```bash
GYM_BUDDY_BOOTSTRAP_STAFF=true mvn -q compile exec:java \
  -Dexec.mainClass=fr.projetcompensation.gymbuddy.fixtures.StaffBootstrapCli
```

SQL/SSH fallback if the flag cannot be used (no secrets in this wiki; hash is Argon2id — prefer the bootstrap so the API hashes):

```sql
-- Inspect only:
SELECT handle, email, role, status FROM users
 WHERE handle IN ('demo.admin', 'demo.mod');
```

Do not `DELETE` member rows to make room. Do not run fixture `--reset` on prod.

### Live email-handle (ticket #103)

QA found public handle `joaquim.keloglanian@gmail.com` (`Test1`). Handle is not an email. After the service rejects `@` on register / profile edit, an operator may rename or close that one live row. No bulk wipe.

```sql
-- If the short handle is free:
UPDATE users
   SET handle = 'joaquim.keloglanian'
 WHERE handle = 'joaquim.keloglanian@gmail.com';

-- If that handle is taken, close instead (staff unlock can restore):
UPDATE users
   SET status = 'closed'
 WHERE handle = 'joaquim.keloglanian@gmail.com';
```

### Production refuse-without-S3

When `SPRING_PROFILES_ACTIVE=prod`, the API must exit on startup if `S3_ENDPOINT` / `S3_BUCKET` / credentials are missing. Falling back to a local `uploads/` directory is forbidden. That is the assignment’s “do not fill local storage” rule.

## Pipeline (`gym-buddy-service`)

Read from the live workflows on `develop` (August 2026). The public documentation repo uses the same **three names** (CI / Release / Deploy) but Deploy publishes GitHub Pages, not a container. Both models are written in [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md).

| Workflow | File | Trigger | What it does |
| --- | --- | --- |
| **CI** | `.github/workflows/ci.yml` | `pull_request` and `push` to `develop` only. **No** `workflow_dispatch`. | Format `--write` (apply; `github-actions[bot]` commits if dirty), then tests, then smoke in the same job. Never publishes. |
| **Release** | `.github/workflows/release.yml` | **`workflow_dispatch` only**. Inputs: optional `version`, `bump` (`auto` / `patch` / `minor` / `major`). | Format `--write`, tests, smoke, compute SemVer, move changelog, commit prep on `develop`, **squash-merge `develop` onto `main`**, annotated tag `vX.Y.Z`, sync `main` back to `develop`, then **calls Deploy**. **Locked target:** also write the SemVer into UI `package.json` and service `pom.xml` (and any matching lock the existing Release already touches) so humans do not hand-edit versions. New application versions stay **0.1.x** unless the wiki says otherwise. **Today** Both Release auto-bumps **have landed**. Ticket **#53** is **Done**. UI [gym-buddy-ui#12](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui/pull/12) / **`63259a4`**. Service [gym-buddy-service#12](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/12) / **`98c4ba0`**. Branch `feature/53-release-semver` is gone. Release writes computed SemVer into UI `package.json` and service `pom.xml` before the tag. Auto bump still refuses **1.0.0+**. `package.json` stays **0.1.0**. `pom.xml` stays **0.2.0-SNAPSHOT** until a later 0.1.x Release. **No** Release was dispatched. Do **not** invent **1.0.0**. Do **not** claim a 0.2.0 product release. OpenAPI Release already runs `sync_package_version.py` — OpenAPI-only. |
| **Deploy** | `.github/workflows/deploy.yml` | `workflow_call` from Release, or a `v*` tag. | Build and push `ghcr.io/projet-de-compensation-2025-2026/gym-buddy-service:vX.Y.Z` (and `:latest`). SSH to the VPS and run `deploy/replace.sh`. |

Successful release used as the reference: [actions/runs/32058005982](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/actions/runs/32058005982) (tag **v0.1.1**).

Image name:

```text
ghcr.io/projet-de-compensation-2025-2026/gym-buddy-service:vX.Y.Z
```

### How to dispatch a patch release

From a machine that can talk to the private service repo:

```bash
gh workflow run Release --repo Projet-de-compensation-2025-2026/gym-buddy-service -f bump=patch
```

Or pin the number:

```bash
gh workflow run Release --repo Projet-de-compensation-2025-2026/gym-buddy-service -f version=0.1.2
```

GitHub UI: **Actions → Release → Run workflow** on `develop`. There is no “release on every green push”. CI does not deploy.

Release fails closed: if format, tests, or smoke fail, there is no commit on `main` and no tag.

**Locked target:** that same Release writes the SemVer into UI `package.json` and service `pom.xml` (and any matching lock / changelog it already touches). Humans do not hand-edit those versions. New application versions stay **0.1.x** unless the wiki says otherwise. **Today** Both Release auto-bumps **have landed**. Ticket **#53** is **Done**. UI [gym-buddy-ui#12](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui/pull/12) / **`63259a4`**. Service [gym-buddy-service#12](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/12) / **`98c4ba0`**. Branch `feature/53-release-semver` is gone. Release writes computed SemVer into UI `package.json` and service `pom.xml` before the tag. Auto bump still refuses **1.0.0+**. `package.json` stays **0.1.0**. `pom.xml` stays **0.2.0-SNAPSHOT** until a later 0.1.x Release. **No** Release was dispatched. Do **not** invent **1.0.0**. Do **not** claim a 0.2.0 product release. OpenAPI Release already syncs `package.json` + `info.version` — OpenAPI-only. Live UI is **v0.1.1**.

### How a deploy lands on the VPS

1. Deploy logs in to GHCR as `github.actor` with `GITHUB_TOKEN`.
2. It builds the tagged commit and pushes `:vX.Y.Z` and `:latest`.
3. If `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_SSH_KEY` are set, it copies `deploy/replace.sh` over SSH and runs it with the image name plus `GHCR_USERNAME` / `GHCR_TOKEN`.
4. `replace.sh` on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`) **skip-pulls local tags** (uses the image already on the host). For a GHCR tag it still logs in to `ghcr.io` and `docker pull`s. Then it stops and removes the previous container and `docker run`s with `--network gym-buddy-data` (or `DEPLOY_NETWORK`), `-p ${DEPLOY_BIND:-127.0.0.1}:${DEPLOY_HOST_PORT:-8080}:8080`, and `-e` for `SPRING_PROFILES_ACTIVE=prod`, `DATABASE_URL`, `REDIS_URL`, `JWT_ACCESS_SECRET`, `S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_REGION` from `/etc/gym-buddy/vps.env` (or `DEPLOY_ENV_FILE`). It fails if that file, a required key, or the Docker network is missing. It refuses `DEPLOY_BIND=0.0.0.0`. Skip-pull for local tags is what is true about `replace.sh` today. It is **not** a GHCR pull, a Release, or a successful replace-from-registry.

That is still **`docker run`** for the API, not `docker compose up -d` of the API. The data-plane file is `deploy/compose.yaml`. Today’s VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**. That is **not** a GHCR pull, a Release tag, or a successful replace-from-registry.

`DEPLOY_BIND` defaults to `127.0.0.1`. The container is not published on a public interface. Caddy is the only process that talks to `127.0.0.1:8080`.

If the three SSH secrets are missing, Deploy still pushes the image and **skips** the SSH replace (exit 0). Secret **names** only: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, optional `DEPLOY_PORT`.

### Health smoke

| When | What the smoke hits |
| --- | --- |
| Today (CI smoke) | `GET /api/v1/healthz` on the container. Body includes `"status"` and `"ok"`. The smoke image is built **without** Postgres/MinIO, so CI does **not** hit `readyz`. |
| Today (implemented) | `GET /api/v1/readyz`: `200` when PostgreSQL and object storage are reachable, else `503` with `details` naming `postgres` and/or `objectStorage` (Testcontainers / local compose). |
| Not today | Probe `GET /`. `/actuator/health` is not the public contract. |

The OpenAPI stub **and** the service implement `GET /api/v1/healthz` and `GET /api/v1/readyz` (ticket #11 / [gym-buddy-openapi#2](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/2)). The stub documents `POST /api/v1/auth/register`, `/login`, `/refresh`, `/logout` (openapi #4); the service on `develop` implements them (service #5 / `e2ef2aa`). Ticket #12 is closed. A bad loopback `POST /api/v1/auth/register` on the VPS returned **422 `VALIDATION`** (auth routes exist). Caddy from the operator network is the completed register/login proof (`201` / `200` + JWT). Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only.

## VPS

| Field | Value |
| --- | --- |
| Offer | OVH VPS-2 2027, Gravelines |
| OS | Ubuntu 26.04 |
| Hostname | `vps-c39cdf03.vps.ovh.net` |
| HTTPS | `https://vps-c39cdf03.vps.ovh.net` (not world-readable) |

### Caddy

Caddy reverse-proxies the hostname to `127.0.0.1:8080` and obtains a Let’s Encrypt certificate. Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**. Caddy is **not** proven from the GitHub Pages origin. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. Today’s VPS container is **aea1c56**. Password eye is on live **v0.1.1**. Ticket **#34** is **Done**. Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`. First tag **v0.1.0** pointed at localhost — that is history, not today.

### UFW policy

| Port | Policy |
| --- | --- |
| 22 | Open worldwide (SSH) |
| 80 | Denied |
| 8080 | Denied (the API is localhost-only) |
| 443 | Allowed only from the operator IPv6 prefix on the VPS UFW |

Do not publish the operator prefix in this public wiki.

### VPS data plane (apply done on loopback)

[gym-buddy-service#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/7) squash-merged as `a07e21e`. Operator steps: [`docs/vps-data-plane.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/vps-data-plane.md). Ticket #20 is **Done / closed** (Sentinel confirmed the VPS rebuild).

| Path | Role |
| --- | --- |
| `deploy/compose.yaml` | Private data plane: PostgreSQL 18.6, Redis, MinIO on named network `gym-buddy-data`. No published ports. The API is **not** in this file. |
| `deploy/vps.env.example` | Key template. Copy to `/etc/gym-buddy/vps.env` on the host (not in git). |
| `deploy/replace.sh` | `docker run` of the API. Joins `gym-buddy-data`. Injects VPS env. `DEPLOY_BIND` default `127.0.0.1`; `0.0.0.0` refused. Skip-pull for local tags is on `develop` (service #8 / `fb1e618`). Today’s VPS Java container on the host is `develop` **`aea1c56`**. **Not** a GHCR pull / Release / replace-from-registry. |
| `docs/vps-data-plane.md` | Operator runbook |

**Apply is done.** Ticket **#20** is **Done / closed**. Sentinel confirmed the VPS rebuild:

- VPS Java container on the host is `gym-buddy-service` `develop` **`aea1c56`**
- Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` on `127.0.0.1:8080` both **200**
- API bind `127.0.0.1`; data-plane ports unpublished
- A bad loopback `POST /api/v1/auth/register` → **422 `VALIDATION`** (auth routes exist)
- `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). That is what is true about `replace.sh`
- **Not** a GHCR pull, a Release tag, or a successful replace-from-registry
- Caddy is **proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Caddy is **not** proven from the GitHub Pages origin. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only.

The API container reaches Postgres / Redis / MinIO by Docker DNS (`postgres`, `redis`, `minio`). Public story is Caddy → `127.0.0.1:8080`, proven from the operator network (not from the GitHub Pages origin).

Local compose (laptop `compose.yaml`) and VPS data-plane compose (`deploy/compose.yaml`) are different files. The laptop may bind those ports to `127.0.0.1` for `psql` / Redis Insight / the MinIO console. The VM must not.

### Inspecting container logs

There is no Grafana, Loki, OpenShift, or Argo log UI. Inspect is SSH plus Docker logs. Do not put those on the 8 GB VPS.

SSH to `vps-c39cdf03.vps.ovh.net` (port 22, open worldwide). Do not publish the operator username or the operator IPv6 prefix.

API container `gym-buddy-service` (`DEPLOY_CONTAINER_NAME`; `docker run`, not compose of the API; bound to `127.0.0.1:8080`; today `develop` **`aea1c56`**):

```bash
docker logs gym-buddy-service
docker logs --tail 200 -f gym-buddy-service
```

Data-plane logs from a `gym-buddy-service` checkout on the VPS (`deploy/compose.yaml`, project `gym-buddy-vps`, network `gym-buddy-data`; Postgres 18.6, Redis, MinIO; no published `5432` / `6379` / `9000` / `9001`; host env `/etc/gym-buddy/vps.env`):

```bash
docker compose --env-file /etc/gym-buddy/vps.env -f deploy/compose.yaml logs postgres
docker compose --env-file /etc/gym-buddy/vps.env -f deploy/compose.yaml logs redis
docker compose --env-file /etc/gym-buddy/vps.env -f deploy/compose.yaml logs minio
```

`docker ps` lists running names if you prefer `docker logs <name>`. Laptop `compose.yaml` is a different file (published `127.0.0.1` ports). It is **not** the VPS.

Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` are the pulse, not a substitute for logs:

```bash
curl -sS -D- http://127.0.0.1:8080/api/v1/healthz
curl -sS -D- http://127.0.0.1:8080/api/v1/readyz
```

Apply / replace stays in the service operator runbook: [`docs/vps-data-plane.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/vps-data-plane.md). Do not duplicate it here.

A later log UI would need a wiki page first (loopback or the existing IPv6 lock, never public) and a Todo card before anyone implements. Not this page.

### Certificate renewal

Let’s Encrypt **HTTP-01** needs port **80** reachable from the world for a few seconds during issuance or renewal. Do **not** leave 80 open in UFW after the challenge.

**tls-alpn-01** cannot work while 443 is firewalled from the world (only the operator IPv6 prefix is allowed). Plan renewals: open 80 briefly for HTTP-01, then deny it again. Do not switch 443 to “anywhere” just to make ALPN easier.

## What still has to be implemented

The next slice is **documentation `0.3.0`** (technical foundation). Local compose runtime is **done** on a laptop (ticket #19 / service #6 / `025a351`). Sign-up / sign-in / log-out is **on `develop`** (openapi #4, ui #3, service #5 / `e2ef2aa`; ticket #12 **closed / Done**). VPS apply is **done** (ticket **#20** **Done / closed**; container `develop` **`aea1c56`**). `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). Caddy is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). A bad loopback `POST /api/v1/auth/register` returned **422 `VALIDATION`** (auth routes exist). Ticket **#23** (pnpm) is **Done**. Ticket **#30** (first UI Pages Release) is **Done**: https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ is HTTP **200**. Joaquim cancelled the TypeScript 6→7 migration (ticket #24 cancelled/closed); TypeScript 7 is **not** remaining work. Stay on TypeScript `~6.0.2` until Angular actually supports 7. Do **not** claim TypeScript 7 landed. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Password eye is on live **v0.1.1**. Ticket **#34** is **Done**. Today’s VPS container is **aea1c56**. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. Ticket **#40** is **Done** as history (`$ref` tree + checked-in `openapi/bundled.yaml` on **`7fa5108`**). Ticket **#54** is **Done** (`develop` **`8ae3bb8`**; no `bundled.yaml`). Ticket **#41** is **Done** as history (`c40f122` from that bundle). Ticket **#47** is **Done** (`gym-buddy-service` `develop` **`3ffdef8`** / service #11; generate from gym-buddy-openapi tag **v0.1.0** `$ref` tree). Ticket **#42** is **Done** as history (`b8da6bf` from `bundled.yaml`). Ticket **#48** is **Done** (`gym-buddy-ui` `develop` **`47eac9c`** / ui #11; pin `gym-buddy-openapi#v0.1.0` / **`9c7c123`**; orval reads `node_modules/gym-buddy-openapi/openapi/openapi.yaml`; Sentinel accepted first-party). Both consumers pin **v0.1.0** and generate from `openapi/openapi.yaml`. `openapi/bundled.yaml` is **gone on `develop`** ([gym-buddy-openapi#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/7) / ticket **#54** Done / **`8ae3bb8`**). The `$ref` tree stays. CI no longer requires the file. Tag **v0.1.0** still contains `openapi/bundled.yaml` (blob sha `a71ee49b5b9d5665ce3fb6b026868c13a7bfec06`) — that is **history**. Do **not** claim the tag was rewritten. Dual maintenance is gone. Ticket **#53** is **Done**. Both Release auto-bumps **have landed** (UI **`63259a4`**; service **`98c4ba0`**). Versions on disk are unchanged. Do **not** un-Done **#40** / **#41** / **#42** / **#46** / **#47** / **#48** / **#53** / **#54**. Do **not** claim the service or UI is handwritten. Git tag **v0.1.0** exists (ticket **#46** Done). `gym-buddy-openapi` GitHub Pages is **not** live (HTTP **404**). The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. The items below are still open.

| Work | Where |
| --- | --- |
| Expand `/api/v1` past health + auth | `gym-buddy-openapi` |
| Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo it. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth` | `gym-buddy-ui` + UFW / cookies |
| Ticket **#24** stays cancelled | TypeScript 6→7 is **not** remaining work |
| `gym-buddy-openapi` GitHub Pages is **not** live (HTTP **404**; Release [32155209479](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/actions/runs/32155209479) tagged **v0.1.0**, then failed only on deploy/pages). The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. | **Not** remaining work |
| Remaining Angular surfaces (friends / feed / events / back-office) | `gym-buddy-ui` |
| Instructor cadrage minutes | [../00-Project-brief/01-Scope-and-modules.md](../00-Project-brief/01-Scope-and-modules.md) — still **Not done** |

`compose.yaml` and `.env.example` landed in `gym-buddy-service` with ticket #7. Runtime proof is [`docs/local-compose-proof.md`](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/local-compose-proof.md) on `gym-buddy-service` `develop` (service #6 / `025a351`).

## Feature workflow

Wiki first, ticket on this documentation repo, Atlas sets `Todo`, Kernel sets `In Progress`. Full sequence: [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md).
