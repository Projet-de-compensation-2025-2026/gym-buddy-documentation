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
| Discuss and scope the project with the instructor | Not done | No minutes yet — see below |
| Write functional and technical specifications | Written (Draft until cadrage) | This wiki |
| Provide UML diagrams | Written (Draft) | [../60-UML-diagrams](../60-UML-diagrams/README.md) |
| Design and write algorithms | Written (Draft) | [../50-Algorithms](../50-Algorithms/README.md) |
| Implement backend, frontend, back-office | Probe only | Python probe + CI/CD + VPS. Spring / Angular not started |
| Test plan and unit tests | Strategy written | [../80-Testing](../80-Testing/README.md) — no application test sources yet |
| Critical analysis | Written (pre-implementation) | [../91-Critical-analysis](../91-Critical-analysis/README.md) |
| Justify library choices | Approved | [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md) |

## How to record the instructor cadrage

When the meeting happens, do **not** invent content beforehand. Add a subsection here with:

1. Date and attendees
2. Decisions that change this page (in-scope / out-of-scope)
3. Decisions that change [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md)
4. Anything the instructor asked to see at the defense
5. Link to the ticket or mail thread if one exists

Until that subsection exists, product pages stay **Draft**. Technical choices stay **Approved** for implementation unless the meeting overturns them.

## Non-goals for this wiki

This repository does not contain application source code. It contains the decisions those repositories must follow. How to run and ship: [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md).
