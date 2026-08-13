# Scope and modules

| Field | Value |
| --- | --- |
| Status | Draft |
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

Record any change to this list after the instructor scoping discussion.

## Instructor cadence

| Step from the brief | Status | Notes |
| --- | --- | --- |
| Discuss and scope the project with the instructor | Not done | Book this before locking the stack |
| Write functional and technical specifications | In progress | This wiki |
| Provide UML diagrams | In progress | [../60-UML-diagrams](../60-UML-diagrams/README.md) |
| Design and write algorithms | In progress | [../50-Algorithms](../50-Algorithms/README.md) |
| Implement backend, frontend, back-office | Not started | Application repositories |
| Test plan and unit tests | Drafted | [../80-Testing](../80-Testing/README.md) |
| Critical analysis | Drafted | [../91-Critical-analysis](../91-Critical-analysis/README.md) |
| Justify library choices | Proposed | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md) |

## Non-goals for this wiki

This repository does not contain application source code. It contains the decisions those repositories must follow.
