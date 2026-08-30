# Scope and modules

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [ProjetDeCompensation2526.en.md](ProjetDeCompensation2526.en.md), [02-Stakeholders-and-defense.md](02-Stakeholders-and-defense.md) |

## Academic frame

Gym Buddies is the individual compensation project for 2025/2026. It is worth **5 ECTS** and must demonstrate competence in three modules:

| Module | How this project proves it |
| --- | --- |
| Software Engineering | UML, layered architecture, specs, test plan, reviews, critical analysis |
| Web Technologies | JWT-secured web API, member frontend, back-office, realtime messaging, media |
| Algorithms and Advanced Programming | Friend suggestions, filtered search, user matching — designed, implemented, justified |

## Product goal

Connect athletes so they can train together, motivate each other, and find a gym buddy.

## In scope (assignment list)

The brief is non-exhaustive. The following are **in scope** and each has a functional spec:

1. Friends news feed
2. Posts, reposts, likes on posts and comments
3. Instant or recurring events, public or private, with applications and organizer approval
4. Nested comments (several levels)
5. Friend requests with approval
6. Public or private profiles
7. Advanced parameterized search
8. Personalized friend suggestions (algorithm justified)
9. User account creation and administration
10. Admin / moderator accounts
11. Instant messaging: private text, images, audio
12. JWT authentication
13. Controlled access to every file
14. Thousands of test fixtures
15. Image management that does not fill local disks

Also in scope because the brief requires them as *work*, not only as features:

- Functional and technical specifications
- UML: use case, activity, sequence, class
- Backend + frontend + back-office
- Reasonable test plan (functional, unit, integration)
- Backend unit tests
- Critical analysis and improvements
- Justification of libraries, languages, frameworks

## Explicitly out of scope (unless the instructor expands the brief)

- Native iOS / Android clients (the web app must be usable on a phone browser)
- Payments, premium subscriptions, ads
- Wearable / health-platform integrations
- Public social graph export
- Multi-tenant white-label

Record any change to this list in this wiki. There will be **no** instructor scoping meeting (see cadrage below).

## Instructor cadence

| Step from the brief | Status | Notes |
| --- | --- | --- |
| Discuss and scope the project with the instructor | Will not happen (instructor on holiday) | Joaquim, 2026-08-19 — see below |
| Write functional and technical specifications | Written | This wiki. Not blocked on a cadrage meeting |
| Provide UML diagrams | Written (Approved, Mermaid) | [../60-UML-diagrams](../60-UML-diagrams/README.md) |
| Design and write algorithms | Written (Approved) | [../50-Algorithms](../50-Algorithms/README.md) — implement in the product tickets |
| Implement backend, frontend, back-office | In progress on `develop` | Angular 22 + Spring exist on `develop` (auth + health only). Remaining product is ticketed after this spec pass. |
| Test plan and unit tests | Strategy written (Approved) | [../80-Testing](../80-Testing/README.md) — application tests ship with each feature ticket |
| Critical analysis | Written (pre-remaining-product) | [../91-Critical-analysis](../91-Critical-analysis/README.md) |
| Justify library choices | Approved | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md) |

## Instructor cadrage (2026-08-19)

Joaquim recorded on **2026-08-19** that there will be **no** instructor cadrage. The instructor is on holiday.

The ISEP brief only says “Discuter et cadrer le projet avec l'enseignant” / “Discuss and scope the project with the instructor” ([ProjetDeCompensation2526.fr.md](ProjetDeCompensation2526.fr.md), [ProjetDeCompensation2526.en.md](ProjetDeCompensation2526.en.md)). It does **not** say wiki pages stay **Draft** until that meeting.

Product functional-specification pages are **not** blocked on a meeting. Existing FS `Status` fields are not mass-rewritten here. Implementation still goes wiki → OpenAPI tag → implement ([../70-Engineering-practices/08-Feature-implementation.md](../70-Engineering-practices/08-Feature-implementation.md)).

Do not invent minutes for a meeting that will not happen. Technical choices stay **Approved** unless a later wiki change overturns them.

## Non-goals for this wiki

This repository does not contain application source code. It contains the decisions those repositories must follow. How to run and ship: [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).
