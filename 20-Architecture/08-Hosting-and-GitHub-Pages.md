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
| Member frontend (Angular) | **Yes** | `ng build` emits static files. Deploy the `dist/` folder to Pages (project site or `gh-pages` branch / Actions). |
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

- Build with a production `baseHref` of `/gym-buddy-ui/` (project site) or a custom domain
- Environment: `apiBaseUrl` pointing at the **real** backend (`https://vps-c39cdf03.vps.ovh.net/api/v1` once Spring exists), not at Pages
- CORS on the backend must allow the Pages origin
- Cookies (`SameSite`, `Secure`) must match HTTPS Pages

## Backend and database (OVH VPS)

Chosen host: **OVH VPS-2 2027** in Gravelines, Ubuntu 26.04, hostname `vps-c39cdf03.vps.ovh.net`.

Rejected for the API (fine as notes, not the plan): Render, Fly.io, Railway as the primary runtime. They hide the VM the pipeline already deploys to.

| Need | Where |
| --- | --- |
| Java API (probe today) | Docker on the VPS, bound to `127.0.0.1:8080` |
| HTTPS | Caddy on the hostname → loopback `:8080`, Let’s Encrypt |
| PostgreSQL 18 / Redis / MinIO | Local compose first. On the VPS later: private Docker network, ports not published |
| Public `:8080` | Never. UFW denies it. |

UFW: 22 open; 80 denied except during certificate HTTP-01; 443 allowed only from the operator IPv6 prefix configured on the server (the prefix is not written in this public wiki); 8080 denied.

GitHub Actions is the only pipeline: CI on `develop`, a separate Release job onto `main`, then Deploy. Details: [../70-Engineering-practices/07-CI-CD.md](../70-Engineering-practices/07-CI-CD.md) and [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).

A tagged squash commit on `main` **is** the deploy. Static repos (this wiki, Angular, OpenAPI UI) go to GitHub Pages. `gym-buddy-service` builds a Docker image to GHCR and `replace.sh` replaces the container on the VM. Compose remains the **local** story.

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
