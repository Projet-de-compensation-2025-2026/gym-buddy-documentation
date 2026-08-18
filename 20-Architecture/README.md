# 20 — Architecture

How Gym Buddies is split into systems, where data lives, and why the proposed stack exists. This section satisfies the brief’s **software architecture**, **data model**, and **justification of technical choices**.

## Contents

| Document | Description |
| --- | --- |
| [01-Software-architecture.md](01-Software-architecture.md) | Logical view: clients, API, workers, storage, realtime |
| [02-System-context.md](02-System-context.md) | Actors and external systems (C4 context) |
| [03-Backend.md](03-Backend.md) | API, domain modules, jobs |
| [04-Frontend.md](04-Frontend.md) | Member-facing web application |
| [05-Back-office.md](05-Back-office.md) | Admin / moderator console |
| [06-Data-model.md](06-Data-model.md) | Relational model covering every overview feature |
| [07-Technology-choices.md](07-Technology-choices.md) | Java 25 LTS, Angular 22, TypeScript 7.0.0 + pnpm (approved; UI `develop` is still TS ~6.0.2 + npm), PostgreSQL 18, OpenAPI repo |
| [08-Hosting-and-GitHub-Pages.md](08-Hosting-and-GitHub-Pages.md) | Pages for wiki / Angular / OpenAPI UI; OVH VPS + Caddy for Java. Runbook: [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

Implementation details that are not architectural (JWT shape, signed URLs, fixture generation) live in [40-Technical-specifications](../40-Technical-specifications/README.md).

## Next

[30-Functional-specifications](../30-Functional-specifications/README.md) · [Back to home](../README.md)
