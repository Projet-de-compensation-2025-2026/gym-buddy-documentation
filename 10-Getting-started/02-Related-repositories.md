# Related repositories

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/01-Software-architecture.md](../20-Architecture/01-Software-architecture.md), [../20-Architecture/08-Hosting-and-GitHub-Pages.md](../20-Architecture/08-Hosting-and-GitHub-Pages.md) |

Gym Buddies is documented **once** here and implemented in **three** other repositories. Names below are the intended layout; replace the GitHub URLs when each repo exists.

| Repository | Responsibility | Hosted on |
| --- | --- | --- |
| `gym-buddy-documentation` (this repo) | Product, architecture, specs, practices, academic packaging, **tickets** | GitHub Pages (Markdown → Jekyll) |
| `gym-buddy-openapi` | Versioned OpenAPI 3 contract + static Swagger/Redoc | GitHub Pages (static) |
| `gym-buddy-backend` | Java API, domain, jobs, WebSocket, fixtures | **Not** Pages — always-on host |
| `gym-buddy-frontend` | Angular member app **and** Angular back-office | GitHub Pages (static `ng build`) |

The instructor account [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr) must be a collaborator on every **private** repository.

## Why an OpenAPI repository

The contract is a **git artifact**, not a runtime accident:

- Reviewers (and the instructor) read the spec without booting Java
- Frontend generates a TypeScript client from a tagged spec (`v0.3.0`), not from whatever a local server emitted today
- Backend is checked **against** that spec (contract tests / generated interfaces)
- The same YAML is published on Pages as human-readable API docs

Spring may still expose `/v3/api-docs` in development as a convenience. That endpoint is **not** the source of truth. If it disagrees with `gym-buddy-openapi`, the repository wins.

## Rules for application repos

1. Do not copy functional specs into application trees. Link to `30-Functional-specifications`.
2. Do not hand-edit generated clients; change the OpenAPI repo and regenerate.
3. Tickets live in **this** documentation repo and must link to a wiki page ([../70-Engineering-practices/05-Tickets-and-GitHub-projects.md](../70-Engineering-practices/05-Tickets-and-GitHub-projects.md)).
4. The report cites all four repositories.

## Local development picture

```
gym-buddy-documentation/     ← you are here (wiki + GitHub Project)
gym-buddy-openapi/           ← HTTP contract
gym-buddy-backend/           ← Java 26 + Spring Boot
gym-buddy-frontend/          ← Angular 22 (member + back-office)
```

A compose file in the backend repo starts PostgreSQL 18, MinIO, Redis, and the API. The Angular apps point at that API. OpenAPI files are consumed as a git submodule, a published npm/Maven package, or a raw tagged URL — pick one in the backend README and stick to it.
