# Documentation conventions

| Field | Value |
| --- | --- |
| Status | Approved |

## Folder names

`XX-Section-name` with two digits and hyphenated Title-Case. Pages inside a section: `XX-Short-name.md`.

## Every folder

Must contain `README.md` that:

- States the section’s job in two sentences
- Lists child pages in a table
- Links back to the wiki home and to the next section

## Page header
  
```markdown
# Title

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [other.md](other.md) |
```

Statuses: `Draft` · `Proposed` · `Approved` · `Deprecated`.

## Language

English is the working language of this wiki. The official French assignment stays in `00-Project-brief` and is not rewritten in section pages.

## Links

Prefer relative links so the wiki works on GitHub and locally. Do not link to line numbers in application repos.

## Diagrams

Mermaid only, unless a binary image is unavoidable (screenshot). Screenshots for the report live under `99-Academic-deliverables` when added.

## Changelog

User-visible or decision-visible edits add a bullet under `Unreleased` in [../90-Changelog/CHANGELOG.md](../90-Changelog/CHANGELOG.md).

## What not to put here

- Secrets
- Personal notes unrelated to the product
- Generated OpenAPI dumps (those belong in `gym-buddy-openapi`, not here and not as a live backend endpoint)
