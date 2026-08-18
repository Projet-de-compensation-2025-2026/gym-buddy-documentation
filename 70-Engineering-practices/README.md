# 70 — Engineering practices

How we write, review, and ship code and documentation across **every** Gym Buddies repository. This directory is the org-wide source of truth for conventions, standards, and workflows. Agents and humans follow it; they do not invent a second process.

**Every ticket** must cite this directory (the issue form requires it).

## Contents

| Document | Description |
| --- | --- |
| [01-Coding-standards.md](01-Coding-standards.md) | Language-agnostic rules plus Java, Angular/TypeScript **6**, and pnpm supply-chain defaults |
| [02-Git-workflow.md](02-Git-workflow.md) | [Gitflow (Atlassian)](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) + [Conventional Commits](https://www.conventionalcommits.org/) |
| [03-Review-process.md](03-Review-process.md) | What a review must check (including “does it match the wiki?”) |
| [04-Documentation-conventions.md](04-Documentation-conventions.md) | Numbering, page template, linking, changelog entries |
| [05-Tickets-and-GitHub-projects.md](05-Tickets-and-GitHub-projects.md) | Issues live here, must link a wiki page **and this directory**, commit scope = ticket id |
| [06-Versioning.md](06-Versioning.md) | [Semantic Versioning 2.0.0](https://semver.org/) — `0.y.z` until the academic `1.0.0`; documentation `0.3.0` is the technical-foundation contract; application repos stay on `0.1.x` until it is done |
| [07-CI-CD.md](07-CI-CD.md) | GitHub Actions: CI on `develop`, Release squash+tag onto `main`, Deploy (Pages or `replace.sh`). Node: Corepack, lockfile, no `latest`, updater cooldown ≥ four weeks |
| [08-Feature-implementation.md](08-Feature-implementation.md) | Consult Joaquim → update specs → ticket on **Gym Buddy Project** → `Not Ready` / `Todo` / `In Progress` / `Done` |

Operator runbook (local compose, env keys, VPS): [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).

These practices exist so the software-engineering module is visible in the daily workflow, not only in UML.

## Next

[80-Testing](../80-Testing/README.md) · [Back to home](../README.md)
