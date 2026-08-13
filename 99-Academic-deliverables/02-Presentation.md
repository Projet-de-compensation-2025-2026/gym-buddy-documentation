# Presentation (PowerPoint)

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../00-Project-brief/02-Stakeholders-and-defense.md](../00-Project-brief/02-Stakeholders-and-defense.md) |

Defense: **20 minutes** + **30 minutes Q&A**, in person or remote.

## Slide spine (≈ 12 slides)

| # | Slide | Minutes | Talk about |
| --- | --- | --- | --- |
| 1 | Title | 0.5 | Gym Buddies, ISEP 2025/2026, your name |
| 2 | Problem | 1 | Athletes train alone; need a buddy |
| 3 | Scope | 1 | Modules, in-scope list, explicit out-of-scope |
| 4 | Demo 1 — social | 4 | Feed, post, nested comment, like, friend accept |
| 5 | Demo 2 — session | 4 | Friends-only event, apply, accept, capacity |
| 6 | Demo 3 — buddy | 2 | Suggestions + DM image |
| 7 | Architecture | 2 | Modular monolith, three apps, MinIO, Postgres |
| 8 | Data model | 1 | 6–8 entities, not the whole ER |
| 9 | Algorithm deep dive | 3 | Suggestions **or** matching — formula + why not ML |
| 10 | Security | 1.5 | JWT + `canRead` + signed URL |
| 11 | Tests and fixtures | 1 | Pyramid + 3 000 users |
| 12 | Limits and Q&A | 0.5 | Honest gaps |

If demo environments fail, slides 4–6 become the recorded video. Keep that file **offline**.

## Q&A (30 min) — likely questions

- Why Java 26 / why not the 25 LTS? Why Angular rather than React?
- How do you stop a stranger fetching an image key?
- Complexity of suggestions on 3k users?
- What happens when two accepts race?
- How is a recurring event stored?
- Show a unit test for matching.
- What would you drop if you had two weeks less?

Answers should point at a spec ID, not a new story.

## File

Store the `.pptx` in this folder when it exists (`Gym-Buddies-defense.pptx`). Do not commit huge screen-recordings to git; link them from the private drive or release assets.
