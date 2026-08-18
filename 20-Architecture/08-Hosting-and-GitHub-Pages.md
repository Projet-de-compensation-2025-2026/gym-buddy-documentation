# Hosting and GitHub Pages

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [07-Technology-choices.md](07-Technology-choices.md), [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

Goal: put as much of Gym Buddies as possible on **GitHub Pages**, including this documentation. The Java API and its data plane run on an OVH VPS.

## What GitHub Pages actually is

[GitHub Pages](https://docs.github.com/en/pages) is **static hosting**: HTML, CSS, JavaScript, images, and files. It does **not** run a JVM, a servlet container, PHP, or PostgreSQL. There is no server-side process and no persistent disk you can treat as a database.

That constraint decides what can live on Pages and what cannot.

## Verdict per piece

| Piece | On GitHub Pages? | How |
| --- | --- | --- |
| This documentation wiki | **Yes** | Jekyll (built in) turns the Markdown tree into a site. Config is already in this repo (`_config.yml`). |
| Member frontend (Angular) | **Yes** — **live** | Project site https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ returns HTTP **200** and serves the Angular app with production `baseHref` `/gym-buddy-ui/` (ticket **#30** Done; first UI tag **v0.1.0**). Root 200 is the acceptance. |
| Back-office (Angular, same frontend repo) | **Yes** | Second configuration / `baseHref`, same static model. |
| OpenAPI contract + reference UI | **Yes** | Host the YAML/JSON plus a static [Swagger UI](https://swagger.io/tools/swagger-ui/) or Redoc build in `gym-buddy-openapi`. |
| Java backend | **No** | Needs a process (Spring Boot). Pages cannot run it. Lives on the OVH VPS. |
| PostgreSQL | **No** | Needs a database engine. Pages cannot run it. |
| MinIO / object storage | **No** | Same reason. |
| WebSockets / JWT login against a real API | **No**, not on Pages itself | The Angular app on Pages **calls** an API hosted elsewhere. |

A “JSON file on Pages” is not a substitute for the backend: no auth, no writes, no per-user ACL.

## Documentation site (this repository)

Yes — and it is the first Pages site we enable.

GitHub Pages + Jekyll already understands a Markdown wiki if we enable the official plugins that do **not** require front matter on every page:

- `jekyll-optional-front-matter` — `.md` files without YAML are still pages
- `jekyll-default-layout` — apply the theme layout
- `jekyll-relative-links` — `07-Events.md` links keep working
- `jekyll-readme-index` — each folder’s `README.md` becomes that folder’s index
- `jekyll-titles-from-headings` — H1 becomes the page title

`_config.yml` at the repo root turns those on. `_includes/head-custom.html` loads Mermaid so the UML pages render in the browser (Jekyll does not compile Mermaid by itself).

### How to switch it on

1. Push `_config.yml` and `_includes/head-custom.html` to `main` (or `develop` if you build Pages from there — default is `main`).
2. GitHub → this repo → **Settings → Pages**.
3. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. Wait for the Action / Pages build.
5. Project-site URL: `https://projet-de-compensation-2025-2026.github.io/gym-buddy-documentation/`

**Private repositories:** Pages can be published, but visibility depends on the plan. GitHub Free makes Pages sites public even if the repo is private. A private site needs GitHub Team/Enterprise (the [Student Developer Pack](https://education.github.com/pack) often includes this). The instructor still needs GitHub access to the **repo**; Pages is for reading the wiki in a browser.

If the first build fails on Mermaid or a plugin, use **GitHub Actions** (`actions/jekyll-build-pages` or a small MkDocs/VitePress job) and publish the `gh-pages` branch. The content stays this Markdown tree.

## Frontend on Pages

**Today (2026-08-18, ticket #30 Done):** the member app is on the GitHub Pages project site.

- Live URL: https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/
- Root returns **HTTP 200** and serves the Angular app with production `baseHref` `/gym-buddy-ui/`. Root 200 is the acceptance.
- Direct `/register` (and other client routes) return **HTTP 404** with the same SPA `index.html` body (`404.html` copied by Deploy). That is GitHub Pages’ static fallback, **not** a broken app and **not** a working auth route.
- First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`.
- Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`.
- UI `develop` **`7916fa8`** has that VPS `apiBaseUrl`.
- Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**.
- Live bundle is `main-4WJYST2C.js`: embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye.
- Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified).
- Password eye is on live **v0.1.1**. Ticket **#34** is **Done**.
- Today’s VPS container is **aea1c56**.
- Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven (UFW 443 IPv6-only; refresh cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`). Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF.
- Approved toolchain stays TypeScript **`~6.0.2`** + **pnpm**. Ticket **#24** stays cancelled.

## Backend and database (OVH VPS)

Chosen host: **OVH VPS-2 2027** in Gravelines, Ubuntu 26.04, hostname `vps-c39cdf03.vps.ovh.net`.

Rejected for the API (fine as notes, not the plan): Render, Fly.io, Railway as the primary runtime. They hide the VM the pipeline already deploys to.

| Need | Where |
| --- | --- |
| Java API | Docker on the VPS, bound to `127.0.0.1:8080`. Today’s VPS container is **aea1c56**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200**. `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. Service #5 / `e2ef2aa` is the auth-landing SHA (history of when auth landed), not today’s container. |
| HTTPS | Caddy on the hostname → loopback `:8080`, Let’s Encrypt. **Proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. **Not** proven from the GitHub Pages origin. UFW 443 is Joaquim’s IPv6 prefix only (do not publish that prefix). Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. |
| PostgreSQL 18 / Redis / MinIO | Local compose proven on a laptop (`docs/local-compose-proof.md`). VPS apply **done** (ticket **#20** **Done / closed**; [gym-buddy-service#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/7) / `a07e21e`): `gym-buddy-data`, ports unpublished |
| Public `:8080` | Never. UFW denies it. |

UFW: 22 open; 80 denied except during certificate HTTP-01; 443 allowed only from the operator IPv6 prefix configured on the server (the prefix is not written in this public wiki); 8080 denied.

To inspect Java API / Postgres / Redis / MinIO logs: SSH, then `docker logs` — [Inspecting container logs](../10-Getting-started/04-Environment-and-pipeline.md#inspecting-container-logs).

GitHub Actions is the only pipeline: CI on `develop`, a separate Release job onto `main`, then Deploy. Details: [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md) and [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).

A tagged squash commit on `main` **is** the GHCR deploy path. Static repos (this wiki, Angular, OpenAPI UI) go to GitHub Pages. Today’s VPS container is **aea1c56** (`docker run`, not compose of the API). That is today’s Java container and the CORS-proof SHA. Service #5 / `e2ef2aa` is the auth-landing SHA (history of when auth landed), not today’s container. `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. It is **not** a GHCR pull, a Release tag, or a successful replace-from-registry. Laptop compose remains the **local** story. Caddy is the public entry and is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). CORS is **proven from Joaquim’s PC** on **aea1c56** (Pages origin ACAO **200** + credentials; foreign/evil origin **403**). Caddy is **not** proven from the GitHub Pages origin. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Login-from-Pages is ticket **#37**, **Not Ready**, **not** proven (UFW 443 IPv6-only; refresh cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`). Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Live Pages is **v0.1.1**; `main-4WJYST2C.js` embeds the VPS URL and the password eye. Ticket **#34** is **Done**. Ticket **#24** stays cancelled.

## Target topology

```text
GitHub Pages                         OVH VPS (always-on process)
─────────────────                    ────────────────────────────
documentation wiki  ─┐
Angular member app  ─┼─ static ──►  Caddy :443 ──► 127.0.0.1:8080
Angular back-office ─┤               │
OpenAPI + Swagger   ─┘               └── Spring API ──► PostgreSQL 18
                                     └── object storage (MinIO / S3)
                          ▲
                          └── HTTPS + JWT, CORS allow Pages origins
```

## What to say at the defense

We publish every **static** artifact on GitHub Pages (wiki, Angular, OpenAPI UI). We do **not** pretend Pages runs Java or PostgreSQL; those stay on a small OVH VPS behind Caddy. That is the honest reading of the platform, not a missing feature.
