# CI/CD

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Git-workflow.md](02-Git-workflow.md), [06-Versioning.md](06-Versioning.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

How Gym Buddies is built, proven, released, and put on a machine. Tooling is **GitHub Actions** (the Jenkins-style job runner that lives next to the code). There is no separate Jenkins server.

The operator runbook (ports, compose plan, VPS, Caddy, UFW) is [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md). This page is the pipeline contract.

## What we are automating

Three promises, three workflows. They are not the same job.

| Workflow | File | Trigger | Promise |
| --- | --- | --- |
| **CI** | `.github/workflows/ci.yml` | Every pull request **to `develop`**, and every push **on `develop`** | The change is formatted, tested, and the built artifact actually **runs** |
| **Release** | `.github/workflows/release.yml` | Manual `workflow_dispatch` (the “Jenkins release” button) | Format → test → smoke → **squash-merge `develop` onto `main`** → **annotated tag `vX.Y.Z`** |
| **Deploy** | `.github/workflows/deploy.yml` | A `v*` tag on `main`, or called by Release | Distribute that version: GitHub Pages and/or a Docker image on the target VM |

`main` is **only** those tagged squash commits. Humans do not push to `main`. Feature branches never target `main`.

```text
feature/* ──PR──► develop          CI on every PR and every push
                      │
                      │  Actions → Release  (button, optional version)
                      ▼
                    main   one squash commit + tag vX.Y.Z
                      │
                      ▼
                   Deploy  Pages and/or GHCR + replace.sh on the VM
```

## CI vs CD (the words)

| | Continuous integration | Continuous delivery | Continuous deployment |
| --- | --- | --- | --- |
| Question | Does this change still build, stay formatted, pass tests, and **run**? | Could we ship this right now? | Did we just ship it? |
| Here | The **CI** workflow on `develop` | The **Release** workflow: it *could* publish, but a human starts it | The **Deploy** workflow after a successful tagged commit on `main` |

We do **not** deploy every green commit on `develop`. We do deploy every successful **tagged** squash commit on `main`. That is continuous deployment of **releases**, not of every merged feature.

## How this is operated (no extra website required)

Everything is Git + the GitHub API:

- Workflows live in the repository. Pushing them to `develop` is enough for GitHub to register them.
- You start a release from **Actions → Release → Run workflow**, or `gh workflow run Release`.
- Branch rules, the `develop` default branch, and GitHub Pages can be set with `gh` (and are, when this page is first applied).
- The only thing that **cannot** be invented from a laptop is a machine you have not given us: SSH host, user, and key. Those go in repository **Actions secrets**. Until they exist, Deploy still builds and publishes the image (or Pages site) and **skips** the SSH step.

You do not need Jenkins, a second CI product, or to click through GitHub’s UI for the pipelines themselves.

**GitHub Free limits on private repos** (this org today):

- Repository **rulesets** and classic **branch protection** require GitHub Pro (or a public repo). Workflows still run; they are not blocked. The public `gym-buddy-documentation` repo *does* have rulesets (`ci` required on `develop`, linear history on `main`).
- **GitHub Pages** on a private repo also needs Pro (or the [Student Developer Pack](https://education.github.com/pack)). Public repos can publish Pages. Until then, service deploy is GHCR + SSH; UI/OpenAPI Pages jobs will fail closed on a private repo.

## Success criteria (this page’s contract)

1. **Every pull request targeting `develop` starts the CI workflow.** A push directly to `develop` does too.
2. **`main` only moves via the Release workflow.** The result is a **squash** commit whose message is `release: vX.Y.Z` and an annotated tag `vX.Y.Z` on that commit.
3. Release **fails closed**: if format, tests, or the smoke run fail, there is **no** commit on `main` and **no** tag.
4. Versioning is **automatic** from Conventional Commits and the previous tag. You may **override** the number when you start the workflow.
5. A successful tag on `main` **is** the deploy: Pages for static repos, Docker image + VM replace for `gym-buddy-service`.

## The three jobs in detail

### CI — prove the change

Runs on `ubuntu-latest`. It never publishes.

| Step | What “pass” means |
| --- | --- |
| Format | The tree matches the formatter. This wiki: Prettier on YAML / JSON / HTML (`prettier --check`). Markdown is **not** auto-reflowed (tables and Mermaid). Application repos: Spotless / Prettier. CI does **not** rewrite files. |
| Test | Repo-specific tests. In this wiki: every content folder still has a `README.md`, required pipeline files exist. Later: JUnit, Angular unit tests, OpenAPI lint. |
| Smoke | The **built** thing is started and answers HTTP. Compiling is not enough. This wiki: Jekyll writes `_site/`, a local static server is started, `curl` must get a page that contains “Gym Buddies”. Service **today** (Python probe): container starts and `GET /` returns 2xx. Service **target** (Spring): `GET /api/v1/healthz` and `GET /api/v1/readyz` return 2xx. Do not treat `/actuator/health` as the public smoke. |

Required check name on `develop`: **`ci`**.

### Release — the dedicated “make a version” pipeline

This is the Jenkins-style job. It is **not** folded into CI.

Start it on `develop`:

```bash
gh workflow run Release
# or pin the number
gh workflow run Release -f version=0.2.0
# or force the bump kind
gh workflow run Release -f bump=minor
```

Inputs:

| Input | Default | Meaning |
| --- | --- | --- |
| `version` | empty | If set (e.g. `0.3.0` or `1.0.0`), that number is used. Must be SemVer `X.Y.Z` and **greater** than the latest `v*` tag. |
| `bump` | `auto` | Used only when `version` is empty: `auto`, `patch`, `minor`, `major`. |

`auto` reads commit subjects on `develop` since the last tag:

| Commits since last tag | Bump |
| --- | --- |
| `feat!:` / `type!:` / `BREAKING CHANGE` | major — except while we are on `0.y.z`, a breaking change bumps **minor** (SemVer §4). **`1.0.0` is never chosen automatically**; pass `version=1.0.0` for the academic ship. |
| `feat:` / `feat(…):` | minor |
| anything else (`fix`, `docs`, `chore`, `ci`, …) | patch |

If there is no `v*` tag yet, the baseline is the last changelog version (`0.1.0` for this wiki).

Release then, in order:

1. Checks out `develop` (full history + tags).
2. **Applies** the formatter (`prettier --write`).
3. Runs the same tests as CI.
4. Builds the project and **smokes it** (process up, HTTP 2xx).
5. Computes the version (manual or automatic).
6. Moves `CHANGELOG.md` bullets from `Unreleased` into `## [X.Y.Z] — `.
7. Commits any prep onto `develop` as `chore(release): prepare vX.Y.Z`.
8. `git merge --squash` of `develop` onto `main`, commit `release: vX.Y.Z`, annotated tag `vX.Y.Z`, push `main` and the tag.
9. Merges `main` back into `develop` (`chore(release): sync develop with vX.Y.Z`) so the next squash does not replay history.
10. Calls **Deploy**.

If any of 2–4 fail, steps 7–10 do not run.

On `gym-buddy-service` this is how **v0.1.1** was cut.

### Deploy — distribution

Triggered by the `v*` tag (and always invoked by Release, because a push made with `GITHUB_TOKEN` does not start new workflows).

| Repository | Artifact | Where it goes |
| --- | --- | --- |
| `gym-buddy-documentation` | Jekyll `_site/` | GitHub Pages |
| `gym-buddy-ui` | `ng build` static files | GitHub Pages (when the repo can publish Pages) |
| `gym-buddy-openapi` | Spec + Swagger/Redoc | GitHub Pages (when the repo can publish Pages) |
| `gym-buddy-service` | Docker image | `ghcr.io/projet-de-compensation-2025-2026/gym-buddy-service:vX.Y.Z` **and** SSH `replace.sh` on the VPS |

Service deploy on the VM (secrets are set):

1. Build `docker build` of the tagged commit.
2. Push to GHCR.
3. SSH to `DEPLOY_HOST` as `DEPLOY_USER`.
4. `replace.sh` runs `docker login ghcr.io` with `GITHUB_TOKEN` and `github.actor` (private image).
5. Pull the new tag, stop the previous container, `docker run` the new one bound to `${DEPLOY_BIND:-127.0.0.1}:${PORT:-8080}:8080`.

This is **not** `docker compose up -d` on the VM. Compose is the **local** (and later private data-plane) story. The public HTTP entry is Caddy on the hostname, proxying to loopback `:8080`.

## Repository rules (so `main` stays clean)

| Branch | Rule |
| --- | --- |
| `develop` | Default branch. PRs target this. No force-push, no delete. The **CI** workflow still runs on every PR; do not merge a red one. A required-check ruleset is not used here: it would also block the Release job from syncing `main` back onto `develop`. |
| `main` | Linear history only. No force-push, no delete. **Not** opened by feature PRs. Only Release writes it. |
| `feature/*` | From `develop`, PR back to `develop`. |
| `release/*` | Optional long freeze. Day-to-day releases do **not** use this branch; they use the Release workflow. |
| `hotfix/*` | From `main`, merge to `develop`, then run Release so `main` still only moves by a tagged squash. |

Classic Gitflow’s “open `release/0.3.0` and merge by hand” is replaced by the Release workflow. The Atlassian branch *names* stay in [02-Git-workflow.md](02-Git-workflow.md); the *button* that cuts a version is Actions.

## Secrets

| Secret | Required for | Used by |
| --- | --- | --- |
| *(none)* | CI, Release, Pages, GHCR push | `GITHUB_TOKEN` |
| `DEPLOY_HOST` | SSH replace on the VM | Service Deploy |
| `DEPLOY_USER` | SSH replace on the VM | Service Deploy |
| `DEPLOY_SSH_KEY` | SSH private key (PEM) | Service Deploy |
| `DEPLOY_PORT` | Optional, default `22` | Service Deploy |

Set secrets with:

```bash
gh secret set DEPLOY_HOST
gh secret set DEPLOY_USER
gh secret set DEPLOY_SSH_KEY < deploy_key.pem
```

Do not commit keys. Do not put the VM password in the wiki.

## Per-repo scripts

Each repository owns four scripts. Workflows call them; they do not inline stack-specific commands.

| Script | CI | Release |
| --- | --- | --- |
| `.github/scripts/ci/format.sh` | `--check` | `--write` |
| `.github/scripts/ci/test.sh` | yes | yes |
| `.github/scripts/ci/smoke.sh` | yes (after build) | yes (after build) |
| `.github/scripts/ci/next_version.py` | no | yes |
| `.github/scripts/ci/prepare_changelog.py` | no | yes |

When application code appears, **change the scripts**, not the workflow names or triggers. The contract on this page stays. Service smoke moves from `GET /` to `/api/v1/healthz` + `/readyz` when `pom.xml` exists.

## What to say at the defense

We use GitHub Actions as the only CI/CD runner. Pull requests onto `develop` always run format, tests, and a live smoke. A separate Release workflow is the only way onto `main`: it squash-merges, tags SemVer (automatic or typed in), and that tag is the deploy. The API image is pulled on an OVH VPS, bound to localhost, and served by Caddy.
