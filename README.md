# Gym Buddies documentation

This repository is the **source of truth** for Gym Buddies: a social application that connects athletes (for example fitness practitioners) so they can train together, motivate each other, and find their gym buddy.

It is a Confluence-style wiki adapted for Markdown and GitHub. Other Gym Buddies repositories (`gym-buddy-service`, `gym-buddy-ui`, `gym-buddy-openapi`) should link here instead of duplicating product or process decisions. This wiki is intended to be published on [GitHub Pages](20-Architecture/08-Hosting-and-GitHub-Pages.md).

| | |
| --- | --- |
| Product | Gym Buddies |
| Academic frame | ISEP compensation project 2025/2026 (5 ECTS) |
| Modules covered | Software Engineering, Web Technologies, Algorithms and Advanced Programming |
| Deadline | 31 August 2026 |
| Defense | 20 min presentation + 30 min Q&A (in person or remote) |
| Instructor | [maurras.togbe@isep.fr](mailto:maurras.togbe@isep.fr) (must be added to GitHub) |

## How this wiki is organized

Top-level folders follow `XX-Section-name`, where `XX` is `00`–`99`. Numbers are spaced so new sections can be inserted without renaming everything.

| Folder | What you will find |
| --- | --- |
| [00-Project-brief](00-Project-brief/README.md) | Official assignment (FR/EN), academic scope, stakeholders, defense constraints |
| [10-Getting-started](10-Getting-started/README.md) | How to read this wiki, related repositories, glossary |
| [20-Architecture](20-Architecture/README.md) | Software architecture, Java backend / Angular frontend, data model, stack, GitHub Pages |
| [30-Functional-specifications](30-Functional-specifications/README.md) | Product behavior for every feature listed in the assignment overview |
| [40-Technical-specifications](40-Technical-specifications/README.md) | JWT, file access, image storage, messaging transport, search, fixtures, API conventions |
| [50-Algorithms](50-Algorithms/README.md) | Friend suggestions, filtered search, user matching — with justification |
| [60-UML-diagrams](60-UML-diagrams/README.md) | Use case, activity, sequence, and class diagrams |
| [70-Engineering-practices](70-Engineering-practices/README.md) | Gitflow, SemVer, Conventional Commits, tickets, feature workflow, CI/CD |
| [80-Testing](80-Testing/README.md) | Test plan, unit / integration / functional tests, fixture strategy |
| [90-Changelog](90-Changelog/README.md) | Version history for the product and for this wiki |
| [91-Critical-analysis](91-Critical-analysis/README.md) | Critique of the solution and possible improvements |
| [99-Academic-deliverables](99-Academic-deliverables/README.md) | Report outline, presentation plan, screenshot checklist |

Every folder has its own `README.md`. Start there when you land in a section.

## Start here

1. Read the English assignment: [00-Project-brief/ProjetDeCompensation2526.en.md](00-Project-brief/ProjetDeCompensation2526.en.md)
2. Skim [10-Getting-started/01-How-to-use-this-wiki.md](10-Getting-started/01-How-to-use-this-wiki.md)
3. Open [20-Architecture/01-Software-architecture.md](20-Architecture/01-Software-architecture.md) for the system map
4. Jump to a feature in [30-Functional-specifications](30-Functional-specifications/README.md)

## Assignment coverage

Everything required by the compensation brief is recorded in this repository:

| Brief item | Where it lives |
| --- | --- |
| Project framing, 5 ECTS, modules, individual work, deadline, defense | [00-Project-brief](00-Project-brief/README.md) |
| Functional specifications | [30-Functional-specifications](30-Functional-specifications/README.md) |
| Technical specifications | [40-Technical-specifications](40-Technical-specifications/README.md) |
| UML (use case, activity, sequence, class) | [60-UML-diagrams](60-UML-diagrams/README.md) |
| Algorithms (suggestions, filtered search, matching) | [50-Algorithms](50-Algorithms/README.md) |
| Backend, frontend, back-office design | [20-Architecture](20-Architecture/README.md) |
| Test plan + unit tests especially on the backend | [80-Testing](80-Testing/README.md) |
| Critical analysis and improvements | [91-Critical-analysis](91-Critical-analysis/README.md) |
| Justification of libraries, languages, frameworks | [20-Architecture/07-Technology-choices.md](20-Architecture/07-Technology-choices.md) |
| Report, screenshots, architecture, data model, UML, PowerPoint | [99-Academic-deliverables](99-Academic-deliverables/README.md) |
| Code practices and workflows | [70-Engineering-practices](70-Engineering-practices/README.md) |
| Version changelogs | [90-Changelog](90-Changelog/README.md) |

## Document status

Pages use a short status table:

| Status | Meaning |
| --- | --- |
| `Draft` | Written from the brief; not yet validated with the instructor |
| `Proposed` | Concrete design waiting for a decision |
| `Approved` | Locked for implementation |
| `Deprecated` | Kept for history only |

Until the instructor meeting in [00-Project-brief/01-Scope-and-modules.md](00-Project-brief/01-Scope-and-modules.md) is recorded, treat product pages as **Draft** and technical choices as **Proposed**.

## Contributing

See [70-Engineering-practices/04-Documentation-conventions.md](70-Engineering-practices/04-Documentation-conventions.md). Do not fork product decisions into application repositories: change them here, then implement.
