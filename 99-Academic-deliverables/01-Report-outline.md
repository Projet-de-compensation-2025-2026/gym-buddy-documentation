# Report outline

| Field | Value |
| --- | --- |
| Status | Assembled — `Gym-Buddies-report.pdf` (wiki `2fcabfa`). Live screenshots 1–16 still operator-captured |
| Related | [../00-Project-brief/ProjetDeCompensation2526.en.md](../00-Project-brief/ProjetDeCompensation2526.en.md), [03-Screenshots.md](03-Screenshots.md) |

The report **summarizes** this wiki and the implementation. It is not a second specification. Assemble it in the last weeks; keep screenshots current.

**Blocked on:** Spring + Angular implementation, screenshot set, instructor cadrage notes. Do not export a PDF that pretends those exist.

## Required contents (brief)

| Required | Source in this wiki |
| --- | --- |
| Link to the private GitHub repositories | [../10-Getting-started/02-Related-repositories.md](../10-Getting-started/02-Related-repositories.md) — all four URLs, instructor collaborator |
| Screenshots of major features | [03-Screenshots.md](03-Screenshots.md) |
| Software architecture | [../20-Architecture/01-Software-architecture.md](../20-Architecture/01-Software-architecture.md) |
| Data model | [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) |
| UML diagrams | [../60-UML-diagrams](../60-UML-diagrams/README.md) |
| Justification of technical choices | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md) + [../50-Algorithms](../50-Algorithms/README.md) |
| Functional specifications | [../30-Functional-specifications](../30-Functional-specifications/README.md) (attach or point at tagged revision) |
| Technical specifications | [../40-Technical-specifications](../40-Technical-specifications/README.md) |

Also include, because the task list asks for them:

- Test plan and unit-test summary — [../80-Testing](../80-Testing/README.md)
- Critical analysis — [../91-Critical-analysis](../91-Critical-analysis/README.md)
- How it is hosted and shipped — [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md)

## Repository URLs to cite

- https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation
- https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service
- https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui
- https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi

## Chapter map (write from the wiki, do not redesign)

| # | Chapter | Pull from | Notes when writing |
| --- | --- | --- | --- |
| 1 | Introduction and academic framing | `00-Project-brief` | 5 ECTS, three modules, individual work, deadline 31 August 2026 |
| 2 | Problem and users | brief + `02-System-context` | Athletes who want a training partner |
| 3 | Functional overview | `30-Functional-specifications` | One table of FS areas, then 1–2 pages of highlights (feed, events, suggestions) |
| 4 | Architecture and data model | `20-Architecture/01`, `06` | Modular monolith, four repos, ER of 6–8 core entities |
| 5 | Algorithms | `50-Algorithms` | Suggestions, filtered search, matching — formula + complexity + why not ML |
| 6 | Security | `40-Technical-specifications/02` + `03` | JWT HS256, Argon2id, `canRead`, signed URLs |
| 7 | Implementation notes | service / UI READMEs + environment runbook | Backend, frontend, back-office, VPS + Caddy. Be honest about probe vs Spring if still mid-build |
| 8 | Tests and fixtures | `80-Testing` + `07-Test-fixtures` | Pyramid, Datafaker, seed `20260813`, 3 000 users |
| 9 | Critical analysis and improvements | `91-Critical-analysis` | Pre-impl critique plus what you would change after coding |
| 10 | Conclusion | — | What the three modules demonstrated |
| 11 | Appendix | UML, selected OpenAPI, cadrage notes | Cite the documentation commit hash |

## Formalities

- Due 31 August 2026 by email to [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr)
- Language: confirm with the instructor (assignment is French; this wiki is English). If the report must be French, translate from this outline, do not rewrite the design.
- Cite the documentation repo commit hash used for the PDF export.
- File name when it exists: `Gym-Buddies-report.pdf` in this folder or a release asset. Do not commit a hollow PDF.
