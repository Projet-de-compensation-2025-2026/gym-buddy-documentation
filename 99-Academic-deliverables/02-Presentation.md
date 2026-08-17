# Presentation (PowerPoint)

| Field | Value |
| --- | --- |
| Status | Draft — slide spine complete; `.pptx` not built |
| Related | [../00-Project-brief/02-Stakeholders-and-defense.md](../00-Project-brief/02-Stakeholders-and-defense.md) |

Defense: **20 minutes** + **30 minutes Q&A**, in person or remote.

**Blocked on:** a demoable UI (or a recorded fallback). Do not commit an empty `Gym-Buddies-defense.pptx`.

## Slide spine (≈ 12 slides)

| # | Slide | Minutes | Talk about | Speaker notes |
| --- | --- | --- | --- | --- |
| 1 | Title | 0.5 | Gym Buddies, ISEP 2025/2026, Joaquim Kéloglanian | One line: social app to find a gym buddy. |
| 2 | Problem | 1 | Athletes train alone; need a buddy | Keep it human. No stack yet. |
| 3 | Scope | 1 | Modules, in-scope list, explicit out-of-scope | Point at `01-Scope-and-modules.md`. Mention cadrage if it happened. |
| 4 | Demo 1 — social | 4 | Feed, post, nested comment, like, friend accept | Live as `demo.alex`. If it fails, play the offline recording. |
| 5 | Demo 2 — session | 4 | Friends-only event, apply, accept, capacity | Show a full event and a rejected extra applicant. |
| 6 | Demo 3 — buddy | 2 | Suggestions + DM image | Read the “why” line on a suggestion. |
| 7 | Architecture | 2 | Modular monolith, four repos, MinIO, Postgres, VPS | Wiki + OpenAPI + service + UI. Pages for static; OVH for Java. |
| 8 | Data model | 1 | 6–8 entities, not the whole ER | User, Friendship, Post, Comment, Event, Media. |
| 9 | Algorithm deep dive | 3 | Suggestions **or** matching — formula + why not ML | One formula on the slide. Complexity on 3k users. |
| 10 | Security | 1.5 | JWT + `canRead` + signed URL | Stranger cannot fetch an object key. |
| 11 | Tests and fixtures | 1 | Pyramid + 3 000 users | Datafaker, seed `20260813`. |
| 12 | Limits and Q&A | 0.5 | Honest gaps | What you would drop with two weeks less. |

If demo environments fail, slides 4–6 become the recorded video. Keep that file **offline**.

## Q&A (30 min) — likely questions

- Why Java 26 / why not the 25 LTS? Why Angular rather than React?
- How do you stop a stranger fetching an image key?
- Complexity of suggestions on 3k users?
- What happens when two accepts race?
- How is a recurring event stored?
- Show a unit test for matching.
- What would you drop if you had two weeks less?
- How does a commit reach the VPS? (CI → Release button → GHCR → `replace.sh` → Caddy)

Answers should point at a spec ID, not a new story.

## File

Store the `.pptx` in this folder when it exists (`Gym-Buddies-defense.pptx`). Do not commit huge screen-recordings to git; link them from the private drive or release assets.
