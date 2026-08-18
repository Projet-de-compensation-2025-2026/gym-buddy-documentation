# Tickets and GitHub Projects

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [02-Git-workflow.md](02-Git-workflow.md), [08-Feature-implementation.md](08-Feature-implementation.md) |

Work is tracked as **GitHub Issues**, organized on the singular GitHub Project [**Gym Buddy Project**](https://github.com/orgs/Projet-de-compensation-2025-2026/projects/1). The Project is the board; the Issue is the ticket. Do not create a second project.

When a feature is implemented from a specification, follow [08-Feature-implementation.md](08-Feature-implementation.md) first (consult Joaquim Kéloglanian, update the specs, then open the ticket).

## Where tickets live

Tickets are opened on **this** repository (`gym-buddy-documentation`), not on the backend, frontend, or OpenAPI repos.

Reasons:

- Every ticket must point at a page in this wiki
- One sequence of ids (`#1`, `#2`, …) is shared across all implementation repos
- Commits in other repos can still link here with `Refs: <owner>/gym-buddy-documentation#42`

**Gym Buddy Project** is the only board. Every ticket is attached to it **at creation**. There is no “open the issue, add it to the board later” step.

How that is enforced:

1. The issue form [`.github/ISSUE_TEMPLATE/ticket.yml`](../../.github/ISSUE_TEMPLATE/ticket.yml) sets `projects: ["Projet-de-compensation-2025-2026/1"]`. GitHub adds the issue to the project when the form is submitted. The opener needs write access on the project (org members do).
2. The same form has a required checkbox: the ticket belongs on Gym Buddy Project and must not be removed.
3. Blank issues are disabled (`config.yml`). Use the Ticket form.
4. If an issue is created **outside** the form (API, `gh issue create`), attach it to the project in the same action. Status starts at `Not Ready`.

New items default to `Not Ready`. The four statuses and who may change them are defined in [08-Feature-implementation.md](08-Feature-implementation.md).

## Mandatory ticket contents

A ticket is not ready for implementation unless it has **all** of the following:

| Field | Rule |
| --- | --- |
| Title | Imperative, scoped to one outcome |
| Type | Feature, Bug, Chore, or Docs (label) |
| **Wiki link** | Path of the **feature** page in this repository (functional spec, technical spec, algorithm, architecture, test plan, …) |
| **Engineering practices** | Always [`70-Engineering-practices`](README.md). Org-wide code style, Gitflow / Conventional Commits, PR review, tickets, versioning, CI/CD. Required so every repository and every agent uses the same workflow. |
| Spec IDs | `FS-…` / `TS-…` when the page defines them |
| Target repo | `gym-buddy-documentation`, `gym-buddy-service`, `gym-buddy-ui`, and/or `gym-buddy-openapi` |
| Acceptance | Checklist copied or cited from the spec |
| **Gym Buddy Project** | Attached at creation. Status visible on the board. |

The issue template under [`.github/ISSUE_TEMPLATE/ticket.yml`](../../.github/ISSUE_TEMPLATE/ticket.yml) makes the feature wiki link **and** `70-Engineering-practices` required, attaches the issue to the project, and requires a checkbox that the opener will follow this directory.

Valid feature wiki links (examples):

- `30-Functional-specifications/07-Events.md`
- `https://<owner>.github.io/gym-buddy-documentation/30-Functional-specifications/07-Events.html` (once Pages is on)
- Several pages if the ticket genuinely spans them

A ticket that only says “implement events” with no wiki link is incomplete. Create or update the spec first, then open the ticket.

A ticket that does not cite `70-Engineering-practices` is incomplete. That directory is not optional documentation; it is the process the implementation must follow.

A ticket that exists only in the repo issues list, and not on [Gym Buddy Project](https://github.com/orgs/Projet-de-compensation-2025-2026/projects/1), is incomplete. Attach it before anyone treats it as `Not Ready`.

## Tickets must reference this repository

- The issue itself lives here
- Implementation PRs in other repos mention `gym-buddy-documentation#<id>` in the PR body
- Commits that implement the ticket use `(#<id>)` as the Conventional Commit scope and a `Refs: <owner>/gym-buddy-documentation#<id>` footer ([02-Git-workflow.md](02-Git-workflow.md))

## One ticket, several commits

A ticket may produce many commits (spec tweak, OpenAPI, backend, tests, frontend). All of them keep the same scope `(#42)` as long as they are for that ticket.

## Ticket and branch

GitHub does not show a branch on the project ticket until the issue and the branch are associated. Create each implementation branch from the issue’s **Development → Create a branch** action, or link the PR/branch there, so the project item exposes it. Several branches or PRs can be linked to one ticket. The ticket form cannot auto-create or auto-link a future branch. The feature sequence is in [08-Feature-implementation.md](08-Feature-implementation.md).

## Commits without a ticket

If there is no ticket, **do not** put a ticket number in the commit scope. Use a topical scope (`wiki`, `ci`, `deps`). Do not create dummy issues after the fact just to decorate a typo-fix unless you want the board to show it.

## Board statuses

Exactly four. These replace any older Backlog / Ready / In review layout.

Atlas alone sets `Not Ready` → `Todo`. Atlas sets `In Progress` → `Done` only after Sentinel confirms the work was implemented and satisfies the functional requirements. No other transitions.

Create each implementation branch from the issue’s **Development → Create a branch** action, or link the PR/branch there, so the project item exposes it.

| Status | Meaning | Who sets it |
| --- | --- | --- |
| `Not Ready` | Default at creation. Specs and template are filled; not yet set to `Todo` | Default at creation |
| `Todo` | The ticket and linked specs are complete enough to implement | Atlas alone (`Not Ready` → `Todo`) |
| `In Progress` | Implementation of this ticket has started | Whoever starts the work |
| `Done` | Implemented, tested, formatted, and merged into `develop` | Atlas (`In Progress` → `Done`), only after Sentinel confirms |

Rules and the full feature sequence: [08-Feature-implementation.md](08-Feature-implementation.md).

The academic ship (`1.0.0`) is a **release**, not a ticket status. Tickets become `Done` on `develop`; Release packages them.
