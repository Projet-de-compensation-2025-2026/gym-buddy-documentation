# How to use this wiki

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../70-Engineering-practices/04-Documentation-conventions.md](../70-Engineering-practices/04-Documentation-conventions.md) |

## Numbering

Folders and, inside a section, pages use `XX-Name`.

- `00`–`09` reserved for framing
- `10`–`89` product and engineering
- `90`–`99` history, critique, academic packaging

Leave gaps (this tree already does: 00, 10, 20, …) so a new top-level section does not force a mass rename.

## Where to look

| I need… | Go to |
| --- | --- |
| The official subject | [../00-Project-brief](../00-Project-brief/README.md) |
| “What should this button do?” | [../30-Functional-specifications](../30-Functional-specifications/README.md) |
| “How do we store / auth / stream?” | [../40-Technical-specifications](../40-Technical-specifications/README.md) |
| “Why this algorithm?” | [../50-Algorithms](../50-Algorithms/README.md) |
| A diagram for the report | [../60-UML-diagrams](../60-UML-diagrams/README.md) |
| How to open a PR | [../70-Engineering-practices](../70-Engineering-practices/README.md) |
| How to take a feature from spec to `develop` | [../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md) |
| How to run locally / ship to the VPS | [04-Environment-and-pipeline.md](04-Environment-and-pipeline.md) |

## Page contract

Every content page starts with a status table (`Draft` / `Proposed` / `Approved` / `Deprecated`) and a **Related** line. Acceptance criteria are numbered so tests can cite them (`FS-EVENTS-08`).

## Editing rules (short)

1. Change the wiki **before** or **in the same PR description** as the code that depends on it.
2. Update [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md) when a decision or a shipped behavior changes.
3. Do not leave a second conflicting spec in an application repo README.

Full rules: [../70-Engineering-practices/04-Documentation-conventions.md](../70-Engineering-practices/04-Documentation-conventions.md).
