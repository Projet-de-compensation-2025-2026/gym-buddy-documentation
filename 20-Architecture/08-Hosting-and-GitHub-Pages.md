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
| Member frontend (Angular) | **Yes** — **live** | Project site https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ returns HTTP **200** and serves the Angular app with production `baseHref` `/gym-buddy-ui/` (ticket **#30** Done; first UI tag **v0.1.0**). Root 200 is the acceptance. **Live v1.0.0** still uses site-root `404.html` for non-root member paths. **Unreleased** ticket **#99**: known static client routes are real files (HTTP 200). |
| Back-office (Angular, same frontend repo) | **Yes** | Isolated `gym-buddy-admin` bundle inside `gym-buddy-ui` at `/admin/` (not a fourth repo). **Unreleased** ticket **#75**: known staff client routes are copied from that admin bundle so they do not fall through the member `404.html`. |
| OpenAPI contract + reference UI | **Not live** | `gym-buddy-openapi` GitHub Pages is **not** live. Release run [32155209479](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/actions/runs/32155209479) created tag **v0.1.0**, then failed only on deploy/pages: “Failed to create deployment (status: 404)… Ensure GitHub Pages has been enabled.” Live https://projet-de-compensation-2025-2026.github.io/gym-buddy-openapi/ is HTTP **404**. The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. |
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
- **Live tag v1.0.0:** Direct `/register` (and other client routes) return **HTTP 404** with the same SPA `index.html` body (`404.html` copied by Deploy). That was GitHub Pages’ static fallback, **not** a broken app. Unreleased tickets **#99** / **#75** copy known routes as real files (next section).
- First tag **v0.1.0** pointed at `http://127.0.0.1:8080/api/v1`.
- Live Pages is **v0.1.1** and embeds `https://vps-c39cdf03.vps.ovh.net/api/v1`.
- UI `develop` **`7916fa8`** has that VPS `apiBaseUrl`.
- Service `develop` **`aea1c56`** CORS is **proven from Joaquim’s PC**: Pages origin ACAO **200** + credentials; foreign/evil origin **403**.
- Live bundle is `main-4WJYST2C.js`: embeds `https://vps-c39cdf03.vps.ovh.net/api/v1` (no `127.0.0.1`) and includes the password eye.
- Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified).
- Password eye is on live **v0.1.1**. Ticket **#34** is **Done**.
- Today’s VPS container is **aea1c56**.
- Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** Todo **#37**. Ticket **#89** is the leftover session cookie: refresh is `HttpOnly; Secure; SameSite=None; Partitioned; Path=/api/v1/auth` so a github.io → VPS credentialed XHR can send it. Access JWT stays in memory. Do not store refresh in `localStorage`. Contract: [../40-Technical-specifications/02-JWT-authentication.md](../40-Technical-specifications/02-JWT-authentication.md).
- Approved toolchain stays TypeScript **`~6.0.2`** + **pnpm**. Ticket **#24** stays cancelled.

## SPA client routes (GitHub Pages has no rewrite)

GitHub Pages is static files only. There is **no** SPA rewrite. Project sites have **one** custom 404: site-root `404.html`. Hash routing is not used.

**Live tag v1.0.0:** Deploy copies only member `index.html` → `404.html`. Cold GET of `/login`, `/register`, and every other member path is HTTP **404** with the member SPA body. `/admin/` is 200 (admin bundle). `/admin/login` and the other staff client paths are HTTP 404 **member** `404.html` (`<app-root>`, not `<admin-root>`). That is tickets **#99** (member tree) and **#75** (admin tree).

**Unreleased (tickets #99 and #75):** UI Deploy runs `stage_pages.py` after `ng build`. It copies each known client route to `path/index.html` **and** sibling `path.html` (GitHub Pages pretty URL for `/path` without a trailing slash) so a cold GET is HTTP **200** (or another non-error status) and the browser does not log `Failed to load resource: 404` for those paths.

Member copies (member bundle, `<app-root>`, `base href="/gym-buddy-ui/"`):

- `/`, `/register`, `/login`, `/events`, `/events/new`, `/friends`, `/search`, `/messages`, `/inbox`, `/suggestions`, `/friends/suggestions`, `/settings`, `/settings/profile`, `/settings/privacy`

Site-root `404.html` remains the member index. It is the fallback for **unknown** paths **and** for parameterized routes Pages cannot enumerate: `/events/:id`, `/messages/:id`, `/posts/:id`, `/u/:handle`. Those still boot the member SPA via HTTP 404 + `404.html`. That is honest.

Admin copies from the isolated `gym-buddy-admin` bundle **inside** `gym-buddy-ui` (`dist-admin` → `/admin/`, live `/gym-buddy-ui/admin/`). Do **not** publish a fourth repo at `gym-buddy-admin`.

- `admin/index.html`
- `admin/login`, `admin/users`, `admin/content`, `admin/reports`, `admin/media`, `admin/fixtures`, `admin/audit` (each `index.html` + sibling `.html`)

Those files are the admin SPA (`<admin-root>`, title Gym Buddy Admin, `base href="/gym-buddy-ui/admin/"`). They never fall through the member `404.html`.

`admin/404.html` is also copied from the admin index. GitHub Pages **will not** serve it for unknown `/admin/*` paths — only the site-root `404.html` is the custom 404. Unknown staff URLs still receive the member fallback. Known staff routes are real files so they do not depend on that.

This lands on live Pages at the next Release. Do **not** dispatch Release from these tickets. Do **not** enable OpenAPI Pages. Do **not** reopen #37.

## Backend and database (OVH VPS)

Chosen host: **OVH VPS-2 2027** in Gravelines, Ubuntu 26.04, hostname `vps-c39cdf03.vps.ovh.net`.

Rejected for the API (fine as notes, not the plan): Render, Fly.io, Railway as the primary runtime. They hide the VM the pipeline already deploys to.

| Need | Where |
| --- | --- |
| Java API | Docker on the VPS, bound to `127.0.0.1:8080`. Today’s VPS container is **aea1c56**. Loopback `GET /api/v1/healthz` and `GET /api/v1/readyz` **200**. `replace.sh` skip-pull for local tags is on `develop` (service #8 / `fb1e618`). **Not** a GHCR pull / Release / replace-from-registry. Service #5 / `e2ef2aa` is the auth-landing SHA (history of when auth landed), not today’s container. |
| HTTPS | Caddy on the hostname → loopback `:8080`, Let’s Encrypt. **Proven from the operator network** (Sentinel, from his PC): `GET /api/v1/healthz` → **200**; `POST /api/v1/auth/register` (email + handle + password + displayName) → **201**; `POST /api/v1/auth/login` → **200** + access JWT. The API is not the bug. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. **Not** proven from the GitHub Pages origin. UFW 443 is Joaquim’s IPv6 prefix only (do not publish that prefix). Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`. |
| PostgreSQL 18 / Redis / MinIO | Local compose proven on a laptop (`docs/local-compose-proof.md`). VPS apply **done** (ticket **#20** **Done / closed**; [gym-buddy-service#7](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/7) / `a07e21e`): `gym-buddy-data`, ports unpublished |
| Public `:8080` | Never. UFW denies it. |

UFW: 22 open; 80 denied except during certificate HTTP-01; 443 allowed only from the operator IPv6 prefix configured on the server (the prefix is not written in this public wiki); 8080 denied.

To inspect Java API / Postgres / Redis / MinIO logs: SSH, then `docker logs` — [Inspecting container logs](../10-Getting-started/04-Environment-and-pipeline.md#inspecting-container-logs).

GitHub Actions is the only pipeline: CI on `develop`, a separate Release job onto `main`, then Deploy. Details: [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md) and [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).

A tagged squash commit on `main` **is** the GHCR deploy path. This wiki and the Angular app go to GitHub Pages. `gym-buddy-openapi` GitHub Pages is **not** live (HTTP **404**; Release [32155209479](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/actions/runs/32155209479) tagged **v0.1.0**, then failed only on deploy/pages). The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. Today’s VPS container is **aea1c56** (`docker run`, not compose of the API). That is today’s Java container and the CORS-proof SHA. Service #5 / `e2ef2aa` is the auth-landing SHA (history of when auth landed), not today’s container. `replace.sh` skip-pull for local tags is on `develop` ([gym-buddy-service#8](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/pull/8) / `fb1e618`). That is what is true about `replace.sh`. It is **not** a GHCR pull, a Release tag, or a successful replace-from-registry. Laptop compose remains the **local** story. Caddy is the public entry and is **proven from the operator network** (healthz **200**, register **201**, login **200** + JWT). CORS is **proven from Joaquim’s PC** on **aea1c56** (Pages origin ACAO **200** + credentials; foreign/evil origin **403**). Caddy is **not** proven from the GitHub Pages origin. Sentinel IPv4 `104.30.175.37` (US) → `https://vps-c39cdf03.vps.ovh.net/api/v1/healthz` TLS unexpected EOF. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages (UFW 443 IPv6-only; refresh cookie `HttpOnly`+`Secure`+`SameSite=Lax`, path `/api/v1/auth`). Do **not** Todo **#37**. Joaquim’s Pages login is operator-home only. Ticket **#31** is **Done / closed** (apiBaseUrl + CORS + live v0.1.1 verified). Live Pages is **v0.1.1**; `main-4WJYST2C.js` embeds the VPS URL and the password eye. Ticket **#34** is **Done**. Ticket **#24** stays cancelled.

## Target topology

```text
GitHub Pages                         OVH VPS (always-on process)
─────────────────                    ────────────────────────────
documentation wiki  ─┐
Angular member app  ─┼─ static ──►  Caddy :443 ──► 127.0.0.1:8080
Angular back-office ─┘               │
                                     └── Spring API ──► PostgreSQL 18
                                     └── object storage (MinIO / S3)
                          ▲
                          └── HTTPS + JWT, CORS allow Pages origins

OpenAPI + Swagger is **not** on Pages today (HTTP **404**).
Do **not** treat enable-Pages as remaining work.
```

## What to say at the defense

We publish the wiki and the Angular app on GitHub Pages. We do **not** pretend Pages runs Java or PostgreSQL; those stay on a small OVH VPS behind Caddy. `gym-buddy-openapi` GitHub Pages is **not** live (HTTP **404**; Release [32155209479](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi/actions/runs/32155209479) tagged **v0.1.0**, then failed only on deploy/pages). The package/tag is **not** broken. Do **not** treat “enable OpenAPI Pages + re-run deploy” as remaining work to start. Joaquim has not asked for the spec site. Atlas will not Todo that ticket unless he wants it. Ticket **#37** is **closed / completed** (Joaquim 2026-08-19: create-account + sign-in is enough). Do **not** claim login-from-Pages. Do **not** Todo **#37**. That is the honest reading of the platform, not a missing feature.
