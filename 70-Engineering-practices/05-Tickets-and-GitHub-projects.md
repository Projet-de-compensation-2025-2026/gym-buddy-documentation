# Tickets and GitHub Projects

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Git-workflow.md](02-Git-workflow.md) |

Work is tracked as **GitHub Issues**, organized on a **GitHub Project**. The Project is the board; the Issue is the ticket.

## Where tickets live

Tickets are opened on **this** repository (`gym-buddy-documentation`), not on the backend, frontend, or OpenAPI repos.

Reasons:

- Every ticket must point at a page in this wiki
- One sequence of ids (`#1`, `#2`, …) is shared across all implementation repos
- Commits in other repos can still link here with `Refs: <owner>/gym-buddy-documentation#42`

The GitHub Project (board columns such as Backlog / Ready / In progress / In review / Done) is attached to this repository or to the GitHub organization, and it includes issues from this repo.

## Mandatory ticket contents

A ticket is not ready for implementation unless it has **all** of the following:

| Field | Rule |
| --- | --- |
| Title | Imperative, scoped to one outcome |
| Type | Feature, Bug, Chore, or Docs (label) |
| **Wiki link** | Path or URL of at least one page in **this** repository (functional spec, technical spec, algorithm, architecture, test plan, …) |
| Spec IDs | `FS-…` / `TS-…` when the page defines them |
| Target repo | `gym-buddy-documentation`, `gym-buddy-service`, `gym-buddy-ui`, and/or `gym-buddy-openapi` |
| Acceptance | Checklist copied or cited from the spec |

The issue template under [`.github/ISSUE_TEMPLATE/ticket.yml`](../../.github/ISSUE_TEMPLATE/ticket.yml) makes the wiki link **required**.

Valid wiki links (examples):

- `30-Functional-specifications/07-Events.md`
- `https://<owner>.github.io/gym-buddy-documentation/30-Functional-specifications/07-Events.html` (once Pages is on)
- Several pages if the ticket genuinely spans them

A ticket that only says “implement events” with no wiki link is incomplete. Create or update the spec first, then open the ticket.

## Tickets must reference this repository

- The issue itself lives here
- Implementation PRs in other repos mention `gym-buddy-documentation#<id>` in the PR body
- Commits that implement the ticket use `(#<id>)` as the Conventional Commit scope and a `Refs: <owner>/gym-buddy-documentation#<id>` footer ([02-Git-workflow.md](02-Git-workflow.md))

## One ticket, several commits

A ticket may produce many commits (spec tweak, OpenAPI, backend, tests, frontend). All of them keep the same scope `(#42)` as long as they are for that ticket.

## Commits without a ticket

If there is no ticket, **do not** put a ticket number in the commit scope. Use a topical scope (`wiki`, `ci`, `deps`). Do not create dummy issues after the fact just to decorate a typo-fix unless you want the board to show it.

## Suggested board columns

| Column | Meaning |
| --- | --- |
| Backlog | Idea; wiki page may still be Draft |
| Ready | Wiki link present, acceptance clear |
| In progress | A `feature/<id>-…` branch exists |
| In review | PR against `develop` |
| Done | Merged to `develop` (or to `main` for a hotfix) |

The academic ship (`1.0.0`) is a **release**, not a ticket column. Tickets close when their change is on `develop`; the release branch packages them.
