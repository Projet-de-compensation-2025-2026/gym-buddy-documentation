# Git workflow

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md), [06-Versioning.md](06-Versioning.md), [07-CI-CD.md](07-CI-CD.md) |

Gym Buddies follows the **Gitflow** branching model as documented by Atlassian:

[Gitflow Workflow (Atlassian Git tutorial)](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

That tutorial is the reference. This page only records how we apply it here (branch names, tickets, commits, multi-repo). Gitflow was originally published by [Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/); Atlassian’s page is what we cite.

Gitflow fits a **release-based** academic project: `1.0.0` is the compensation-project ship (see [06-Versioning.md](06-Versioning.md)). Until that release, integration happens on `develop` and `main` only receives versioned releases and hotfixes.

## Overall flow (from Atlassian)

1. A `develop` branch is created from `main`
2. `feature/*` branches are created from `develop`
3. When a feature is complete it is merged into `develop`
4. A version is cut by the **Release** workflow in [07-CI-CD.md](07-CI-CD.md) (the Jenkins-style job). It format-checks, tests, smokes, then **squash-merges `develop` onto `main`** and tags `vX.Y.Z`.
5. `main` therefore contains **only** those tagged squash commits. Humans do not push to `main`. Feature PRs never target `main`.
6. If production is broken, a `hotfix/*` branch is created from `main`, merged into `develop`, then Release is run again so `main` still only moves by a tagged squash.

A long-lived `release/*` freeze branch remains allowed (Atlassian). Day-to-day we do not open one: the Release workflow *is* the release.

`feature` branches **never** merge into `main`.

## Branch names

| Branch | Role (Atlassian) | Our convention |
| --- | --- | --- |
| `main` | Official release history | **Only** tagged squash commits from Release (`v0.2.0`, later `v1.0.0`) |
| `develop` | Integration of finished features | Default branch. Every PR/push runs CI |
| `feature/<ticket>-<slug>` | One feature, parent = `develop` | Ticket id when the work has a ticket: `feature/42-event-capacity` |
| `release/<semver>` | Optional freeze | Prefer the Release workflow; use a branch only for a long freeze |
| `hotfix/<ticket>-<slug>` | Patch production, parent = `main` | Land on `develop`, then run Release |

Documentation-only work in this wiki uses the same model (`feature/12-fix-search-spec` off `develop`).

Initialize once per repository:

```bash
git checkout main
git checkout -b develop
git push -u origin develop
```

Or `git flow init` with the prefixes above (`feature/`, `release/`, `hotfix/`, tag prefix `v`).

## Commits: Conventional Commits + ticket in the scope

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

### When the commit implements a ticket

The **scope is the ticket number**. Do not put a topical word in the scope instead of the ticket.

```
feat(#42): reject accept when the event is full
fix(#88): rotate refresh jti on logout
docs(#12): add FS-EVT-07 capacity rule
test(#42): cover remainingSeats == 0
```

The commit **body** must also name this documentation repository so GitHub can link the issue from *any* Gym Buddies repo:

```
Refs: <owner>/gym-buddy-documentation#42

Implements FS-EVT-07
```

Replace `<owner>` with the GitHub user or organization. `#42` in the scope is the issue id on the **documentation** repository (tickets live there; see [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md)).

### When the commit is not for a ticket

**Do not invent a ticket number.** Do not put `#0` or a fake id in the scope. Use a short topical scope:

```
docs(wiki): repair broken link in architecture README
chore(ci): pin the checkout action
```

Product and specification work should still start from a ticket. Ticket-less commits are for tiny housekeeping only.

### Types we use

`feat` · `fix` · `docs` · `test` · `refactor` · `chore` · `ci`

## Pull requests

- Open the PR against `develop`. Never against `main` (Release owns `main`; see [07-CI-CD.md](07-CI-CD.md))
- Title includes the ticket when there is one: `[#42] Reject accept when the event is full`
- Description links the ticket and the wiki page the ticket already points at
- Review checklist: [03-Review-process.md](03-Review-process.md)

## Multi-repo order

A behaviour change usually touches more than one repository. Order:

1. Wiki page updated (this repo) — unless the ticket is already pointing at a complete spec
2. OpenAPI contract in `gym-buddy-openapi` if the HTTP surface changes
3. `gym-buddy-service` implements the contract
4. `gym-buddy-ui` consumes the generated client
5. Changelog under `Unreleased` in each repo that shipped a user-visible change

All of those commits that belong to the same ticket use the **same** scope `(#42)` and the same `Refs:` line.

## Instructor access

Every **private** GitHub repository must include [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr). Check this before the first academic milestone, not the night of the deadline.
