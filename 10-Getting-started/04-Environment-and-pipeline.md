# Environment and pipeline

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Related-repositories.md](02-Related-repositories.md), [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md), [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md) |

How to run Gym Buddies locally, how a change is proven and released, and how the live API lands on the VPS. This page is the runbook. The CI/CD contract lives in [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md). Feature work still starts on the wiki: [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md).

## Today versus target

Be honest at the defense. The pipeline, the VPS API replace, the **local data-plane files**, and the **Java 25 LTS / Spring Boot** service exist on `develop` (`pom.xml`, ticket #11). The OpenAPI stub documents auth, and the UI has sign-up / sign-in / log-out pages. End-to-end register / login / logout is **not** done (service #5 still open). PostgreSQL on the VPS and a **proven** local compose boot also do **not**. That remaining work is the **documentation `0.3.0` technical foundation** ([../70-Engineering-practices/06-Versioning.md](../70-Engineering-practices/06-Versioning.md)). There is no planned application `0.2.0` next slice.

| Piece | Today (August 2026) | Target (locked) |
| --- | --- | --- |
| `gym-buddy-service` | Java 25 LTS / Spring Boot (`pom.xml` on `develop`). Flyway `V1__baseline.sql`. `compose.yaml` and `.env.example` are in the repo. Latest released tag **v0.1.1**. | Java 25 LTS / Spring Boot modular monolith |
| `gym-buddy-openapi` | OpenAPI 3.1.0 stub (`info.version` `0.1.0`): `GET /healthz` and `GET /readyz` under `/api/v1`, plus `POST /auth/register`, `/login`, `/refresh`, `/logout` (openapi #4 / ticket #12). The UI calls those auth endpoints; the service has **not** implemented them. | Full contract; health stays `GET /api/v1/healthz` and `GET /api/v1/readyz` |
| `gym-buddy-ui` | Angular 22 (app version `0.1.0`): `/register`, `/login`, and a log-out control that call `POST /api/v1/auth/register`, `/login`, `/logout` (ui #3). Access JWT in memory. Refresh cookie credentials sent (`path /api/v1/auth`). No friends / feed / events. End-to-end auth waits on the service. | Angular 22 member app + back-office |
| Health | Service implements unauthenticated `GET /api/v1/healthz` (liveness) and `GET /api/v1/readyz` (`200` or `503` with `details` for `postgres` / `objectStorage`). CI smoke hits **`GET /api/v1/healthz` only** — the smoke image is built without Postgres/MinIO. Probe `GET /` is not today’s service smoke. | Same public paths. Do not smoke `/actuator/health`. |
| Local data plane | `compose.yaml` in `gym-buddy-service`: Postgres 18, Redis, MinIO, Spring API, optional MailHog. All binds `127.0.0.1`. Files exist (ticket #7). **Runtime boot is not claimed** (documentation `0.3.0`). | Same file |
| VM | One API container, bound to `127.0.0.1:8080`. Caddy terminates TLS. No compose on the VM. | Same API replace, plus a **private** data-plane compose on the Docker network (5432 / 6379 / 9000 not published) |
| Production object storage | `SPRING_PROFILES_ACTIVE=prod` **refuses to start** if S3-compatible storage is missing | Same |

Public health is `healthz` / `readyz`, not `/actuator/health`.

## Ready-to-code checklist

A laptop is ready when all of these are true:

1. **JDK 25 LTS** installed (see [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md)).
2. **Docker** and Compose v2 available.
3. Clone the four repositories (URLs in [02-Related-repositories.md](02-Related-repositories.md)). Default branch is `develop` everywhere.
4. `compose.yaml` and `.env.example` are in `gym-buddy-service` (ticket #7).
5. Copy `.env.example` to `.env` locally. Fill secrets there. Never commit `.env`.
6. `docker compose up -d` binds every published port to `127.0.0.1`.
7. Flyway **V1 baseline** is on `develop`. Full domain tables from [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) are later.
8. The OpenAPI stub in `gym-buddy-openapi` is the HTTP source of truth. Expand it **before** implementing a new route.
9. Point the UI at `http://localhost:8080/api/v1`.

`docker compose up -d` is how a laptop starts the data plane plus the Spring API. That boot is **not** claimed today (documentation `0.3.0`). When it is proven, the API uses Postgres, Redis, and MinIO (`readyz`).

## Local Compose

Compose is the **local** story. It is not how the VPS runs. File: `compose.yaml` at the root of [gym-buddy-service](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service).

```bash
cp .env.example .env
docker compose up -d
# optional SMTP catcher
docker compose --profile mail up -d
```

| Service | Image role | Host bind | Port |
| --- | --- | --- |
| API | Spring Boot (Java 25 LTS image) | `127.0.0.1` | `8080` |
| PostgreSQL | **18** (not 19), image `postgres:18.6` | `127.0.0.1` | `5432` |
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
| `DATABASE_URL` | Local / later VM data plane | PostgreSQL 18 connection |
| `REDIS_URL` | Local / later VM data plane | Cache, refresh denylist, rate limits |
| `JWT_ACCESS_SECRET` | Local / VM | HS256 signing secret for access tokens |
| `S3_ENDPOINT` | Local MinIO / later production bucket | S3-compatible API URL |
| `S3_BUCKET` | Local / production | Bucket name |
| `S3_ACCESS_KEY` | Local / production | Object-store access key |
| `S3_SECRET_KEY` | Local / production | Object-store secret key |
| `S3_REGION` | Local / production | Region string the client library expects |
| `FIXTURE_SEED` | Local / CI fixtures | Fixed seed `20260813` |
| `SPRING_PROFILES_ACTIVE` | Local / VM | `local` / `test` / `prod`. Production refuses to start without object storage. |
| `DEPLOY_HOST` | GitHub Actions only | SSH host for service Deploy |
| `DEPLOY_USER` | GitHub Actions only | SSH user |
| `DEPLOY_SSH_KEY` | GitHub Actions only | SSH private key (PEM) |
| `DEPLOY_PORT` | GitHub Actions only, optional | SSH port, default `22` |
| `DEPLOY_BIND` | VM replace script, optional | Container publish address, default `127.0.0.1` |

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

Flyway on `develop` is **V1 baseline** only. Later migrations will implement [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md). Fixture generation uses **Datafaker** with `FIXTURE_SEED=20260813` — [../40-Technical-specifications/07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md).

### Production refuse-without-S3

When `SPRING_PROFILES_ACTIVE=prod`, the API must exit on startup if `S3_ENDPOINT` / `S3_BUCKET` / credentials are missing. Falling back to a local `uploads/` directory is forbidden. That is the assignment’s “do not fill local storage” rule.

## Pipeline (`gym-buddy-service`)

Read from the live workflows on `develop` (August 2026). The public documentation repo uses the same **three names** (CI / Release / Deploy) but Deploy publishes GitHub Pages, not a container. Both models are written in [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md).

| Workflow | File | Trigger | What it does |
| --- | --- | --- |
| **CI** | `.github/workflows/ci.yml` | `pull_request` and `push` to `develop` only. **No** `workflow_dispatch`. | Format `--write` (apply; `github-actions[bot]` commits if dirty), then tests, then smoke in the same job. Never publishes. |
| **Release** | `.github/workflows/release.yml` | **`workflow_dispatch` only**. Inputs: optional `version`, `bump` (`auto` / `patch` / `minor` / `major`). | Format `--write`, tests, smoke, compute SemVer, move changelog, commit prep on `develop`, **squash-merge `develop` onto `main`**, annotated tag `vX.Y.Z`, sync `main` back to `develop`, then **calls Deploy**. |
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

### How a deploy lands on the VPS

1. Deploy logs in to GHCR as `github.actor` with `GITHUB_TOKEN`.
2. It builds the tagged commit and pushes `:vX.Y.Z` and `:latest`.
3. If `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_SSH_KEY` are set, it copies `deploy/replace.sh` over SSH and runs it with the image name plus `GHCR_USERNAME` / `GHCR_TOKEN`.
4. `replace.sh` logs in to `ghcr.io`, `docker pull`s the tag, stops and removes the previous container, then:

```text
docker run -d --name gym-buddy-service --restart unless-stopped \
  -p "${DEPLOY_BIND:-127.0.0.1}:${DEPLOY_HOST_PORT:-8080}:8080" "$IMAGE"
```

That is **`docker run`**, not `docker compose up -d`. The VM does not compose the API today.

`DEPLOY_BIND` defaults to `127.0.0.1`. The container is not published on a public interface. Caddy is the only process that talks to `127.0.0.1:8080`.

If the three SSH secrets are missing, Deploy still pushes the image and **skips** the SSH replace (exit 0). Secret **names** only: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, optional `DEPLOY_PORT`.

### Health smoke

| When | What the smoke hits |
| --- | --- |
| Today (CI smoke) | `GET /api/v1/healthz` on the container. Body includes `"status"` and `"ok"`. The smoke image is built **without** Postgres/MinIO, so CI does **not** hit `readyz`. |
| Today (implemented) | `GET /api/v1/readyz`: `200` when PostgreSQL and object storage are reachable, else `503` with `details` naming `postgres` and/or `objectStorage` (Testcontainers / local compose). |
| Not today | Probe `GET /`. `/actuator/health` is not the public contract. |

The OpenAPI stub **and** the service implement `GET /api/v1/healthz` and `GET /api/v1/readyz` (ticket #11 / [gym-buddy-openapi#2](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/pull/2)). The stub also documents the four auth operations (openapi #4 / ticket #12); the service has **not** implemented them.

## VPS

| Field | Value |
| --- | --- |
| Offer | OVH VPS-2 2027, Gravelines |
| OS | Ubuntu 26.04 |
| Hostname | `vps-c39cdf03.vps.ovh.net` |
| HTTPS | `https://vps-c39cdf03.vps.ovh.net` (not world-readable) |

### Caddy

Caddy reverse-proxies the hostname to `127.0.0.1:8080` and obtains a Let’s Encrypt certificate.

### UFW policy

| Port | Policy |
| --- | --- |
| 22 | Open worldwide (SSH) |
| 80 | Denied |
| 8080 | Denied (the API is localhost-only) |
| 443 | Allowed only from the operator IPv6 prefix on the VPS UFW |

Do not publish the operator prefix in this public wiki.

### Adding data services (documentation `0.3.0` foundation)

PostgreSQL and the Java service on the VPS are part of the documentation `0.3.0` foundation. They are **not** running on the VM today.

When PostgreSQL, Redis, and MinIO move onto the VM, run them on the Docker network next to the API. Do **not** publish `5432`, `6379`, or `9000` on the host. The API container reaches them by Compose/Docker DNS. The public story stays: Caddy → `127.0.0.1:8080`.

Local compose (laptop) and VM data-plane compose are different files with the same service names. The laptop may bind those ports to `127.0.0.1` for `psql` / Redis Insight / the MinIO console. The VM must not.

### Certificate renewal

Let’s Encrypt **HTTP-01** needs port **80** reachable from the world for a few seconds during issuance or renewal. Do **not** leave 80 open in UFW after the challenge.

**tls-alpn-01** cannot work while 443 is firewalled from the world (only the operator IPv6 prefix is allowed). Plan renewals: open 80 briefly for HTTP-01, then deny it again. Do not switch 443 to “anywhere” just to make ALPN easier.

## What still has to be implemented

The next slice is **documentation `0.3.0`** (technical foundation). None of the foundation items below are done.

| Work | Where |
| --- | --- |
| Prove local compose at runtime: `docker compose up -d` on a laptop; Postgres 18, Redis, MinIO, Java 25 LTS Spring service; binds `127.0.0.1`; `GET /api/v1/healthz` 200 and `GET /api/v1/readyz` 200. Files exist (tickets #7 / #11); boot is not claimed. | Laptop + `gym-buddy-service` |
| PostgreSQL and the Java service on the OVH VPS (`vps-c39cdf03.vps.ovh.net`). Private data-plane on the Docker network; do not publish `5432` / `6379` / `9000`. Public story stays Caddy → `127.0.0.1:8080`. Today: one `docker run` API container (tag **v0.1.1**). | Operator + `gym-buddy-service` |
| Sign-up and sign-in (log-out stays in the same ticket) | Ticket #12 — OpenAPI stub and UI pages are on `develop`; service #5 is still open. Product slice is **not** done |
| Expand the OpenAPI contract past health + the four auth operations (rest of `/api/v1`) | `gym-buddy-openapi` |
| Remaining Angular surfaces (friends / feed / events / back-office) | `gym-buddy-ui` |
| Instructor cadrage minutes | [../00-Project-brief/01-Scope-and-modules.md](../00-Project-brief/01-Scope-and-modules.md) — still **Not done** |

`compose.yaml` and `.env.example` landed in `gym-buddy-service` with ticket #7.

## Feature workflow

Wiki first, ticket on this documentation repo, Atlas sets `Todo`. Full sequence: [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md).
