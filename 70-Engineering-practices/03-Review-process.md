# Review process

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [08-Feature-implementation.md](08-Feature-implementation.md), [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md) |

Even on an individual project, every merge to `develop` (features) or `main` (releases / hotfixes) gets a **self-review checklist**. Treat it as the Software Engineering module’s process evidence.

## Checklist

- [ ] Ticket exists on `gym-buddy-documentation`, is on **Gym Buddy Project**, and **links a wiki page** ([05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md), [08-Feature-implementation.md](08-Feature-implementation.md)) — or the commit has **no** ticket id in the scope
- [ ] Ticket is `In Progress` while the PR is open; it becomes `Done` only after the merge to `develop`
- [ ] Commit scopes follow [02-Git-workflow.md](02-Git-workflow.md): `(#42)` if there is a ticket, topical otherwise
- [ ] `Refs: <owner>/gym-buddy-documentation#<id>` in the commit/PR body when a ticket exists
- [ ] Spec IDs in the description (`FS-…`, `TS-…`)
- [ ] Wiki updated if behavior or a decision changed
- [ ] OpenAPI repo updated **first** if the HTTP surface changed
- [ ] Unit tests for new domain rules (backend)
- [ ] No new local-disk upload path
- [ ] JWT / ACL: fail closed, no existence leak
- [ ] Fixtures still run (or not required)
- [ ] Changelog note if user-visible
- [ ] CI workflow **`ci`** is green on the PR (format, tests, smoke) — see [07-CI-CD.md](07-CI-CD.md)

## What “looks good” is not enough

Reject (or do not merge) if:

- A private profile field is returned to a stranger
- A signed URL is minted before `canRead`
- An algorithm change has no justification update in `50-Algorithms`
- Capacity accept has a race without a transactional check

## After the instructor can comment

If the instructor opens issues on GitHub, answer on the issue and fold the decision into this wiki. Do not leave the only record in a chat.
