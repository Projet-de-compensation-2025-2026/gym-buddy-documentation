# Feature implementation workflow

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md), [03-Review-process.md](03-Review-process.md), [02-Git-workflow.md](02-Git-workflow.md), [07-CI-CD.md](07-CI-CD.md), [../30-Functional-specifications/00-Conventions.md](../30-Functional-specifications/00-Conventions.md) |

How a feature goes from an idea in the assignment (or a later request) to a merge on `develop`. This page is the process. Ticket fields live in [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md). Git and CI rules stay on their own pages.

The product owner is **Joaquim Kéloglanian**. No ticket moves to `Todo`, and no implementation starts, without his explicit green light.

## Sequence

```mermaid
flowchart TD
  consult[1. Consult Joaquim Kéloglanian]
  mature[2. Feature matures]
  specs[3. Update functional and technical specifications]
  ticket[4. Open a ticket from the template]
  notReady[Status: Not Ready]
  review[Joaquim reads, reviews, green-lights]
  todo[Status: Todo]
  start[5. Implementation starts]
  inProgress[Status: In Progress]
  land[6. Implemented, tested, formatted, merged to develop]
  done[Status: Done]

  consult --> mature --> specs --> ticket --> notReady
  notReady --> review --> todo --> start --> inProgress --> land --> done
```

### 1. Consult Joaquim Kéloglanian

The first step is always a conversation with Joaquim. Scope, what “done” looks like, and which wiki pages will own the feature are decided here — not invented in a ticket.

Do not open a ticket in this step. Do not start a `feature/*` branch.

### 2. Let the feature mature

Keep talking until the feature is concrete enough to write as requirements: actors, rules, errors, and what a test would assert. If it is still a sketch, stay here.

### 3. Update the specifications

Once the feature has matured, **write or update the wiki first**:

| Kind of change | Where it lands |
| --- | --- |
| What the product does | [30-Functional-specifications](../30-Functional-specifications/README.md) (`FS-…` requirements) |
| How it is built | [40-Technical-specifications](../40-Technical-specifications/README.md) (`TS-…` when they exist) |
| Algorithm to justify | [50-Algorithms](../50-Algorithms/README.md) |
| Shape of the system | [20-Architecture](../20-Architecture/README.md) |
| HTTP surface | [40-Technical-specifications/08-OpenAPI-contract.md](../40-Technical-specifications/08-OpenAPI-contract.md) — the YAML itself stays in `gym-buddy-openapi` |

A ticket that points at a missing or stale spec is invalid. Change the spec in this repository, then open the ticket.

### 4. Create the ticket

Open a GitHub Issue on **`gym-buddy-documentation`** using the existing template [`.github/ISSUE_TEMPLATE/ticket.yml`](../../.github/ISSUE_TEMPLATE/ticket.yml). Fill **every** field. An empty optional-looking box is not optional here.

| Template field | What to put |
| --- | --- |
| Title | `[GB] ` plus one imperative outcome |
| Type | Feature, Bug, Chore, or Docs |
| Documentation page | Relative path(s) in **this** wiki. Required. Example: `30-Functional-specifications/07-Events.md`. Add the matching technical page when one exists. |
| Spec IDs | `FS-…` / `TS-…` from those pages |
| Implementation repository | Every repo that will change (`gym-buddy-documentation`, `gym-buddy-service`, `gym-buddy-ui`, `gym-buddy-openapi`) |
| Acceptance | Checklist copied or cited from the linked spec |

The ticket **must** point at the documentation it implements. A title such as “implement events” with no wiki path is incomplete — go back to step 3.

The ticket **must** be attached to the existing, singular GitHub Project [**Gym Buddy Project**](https://github.com/orgs/Projet-de-compensation-2025-2026/projects/1). Do not create a second project. Do not leave the issue sitting only in the repo issues list.

Newly created tickets default to **`Not Ready`**.

## Statuses

There are exactly four. They are the Status field on **Gym Buddy Project**. Do not invent extra columns (`Backlog`, `Ready`, `In review`, …).

| Status | Meaning | Who may set it |
| --- | --- | --- |
| `Not Ready` | Ticket exists, every template field is filled, it is on **Gym Buddy Project**, and it points at wiki pages. It is **not** approved for implementation. | Default at creation |
| `Todo` | Joaquim Kéloglanian has **explicitly** read the ticket, reviewed the linked specs, and given the green light | **Only** Joaquim, after that review |
| `In Progress` | Implementation of this ticket has started (branch, first commit, or first draft PR) | Whoever starts the work, **as soon as** it starts |
| `Done` | The change is implemented, tested, formatted, and **merged into `develop`** | After the merge to `develop` (CI green — see [07-CI-CD.md](07-CI-CD.md)) |

### `Not Ready` → `Todo`

Filling the template is not a green light. `Todo` is set **only** when Joaquim has:

1. Read the ticket
2. Reviewed the linked documentation
3. Said explicitly that implementation may start

Nobody else promotes a ticket to `Todo`. A verbal “looks fine, go” in the consult (step 1) does **not** skip this review: that consult happens *before* the specs and the ticket exist.

### `Todo` → `In Progress`

Set `In Progress` the moment work on the ticket begins. Do not leave a live `feature/<id>-…` branch on `Todo`.

Implementation still follows [02-Git-workflow.md](02-Git-workflow.md): branch from `develop`, PR back to `develop`, commit scope `(#<id>)`, `Refs: Projet-de-compensation-2025-2026/gym-buddy-documentation#<id>`.

### `In Progress` → `Done`

A ticket becomes `Done` when **all** of these are true:

1. The behaviour in the linked spec is implemented
2. Tests required by that spec (and [80-Testing](../80-Testing/README.md)) exist and pass
3. Format checks pass (CI `format` / [07-CI-CD.md](07-CI-CD.md))
4. The PR is merged into **`develop`**

A green CI run on an open PR is not `Done`. A squash onto `main` (a Release) is not what closes the ticket. Tickets close on `develop`; Release packages whatever is already there.

## What this page does not replace

- Ticket field rules: [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md)
- Branch names and commit messages: [02-Git-workflow.md](02-Git-workflow.md)
- PR checklist: [03-Review-process.md](03-Review-process.md)
- How `develop` is proven and how `main` is tagged: [07-CI-CD.md](07-CI-CD.md)
