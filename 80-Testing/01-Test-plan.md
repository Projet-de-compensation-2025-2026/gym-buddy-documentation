# Test plan

The school brief requires functional, unit and integration tests, including backend unit tests. Coverage is organized around failures users could encounter rather than a percentage of getters tested.

| Layer | Scope | Tools |
| --- | --- | --- |
| Unit/component | Domain rules, algorithms, validation, authorization and UI state. | JUnit/AssertJ; Angular test tooling. |
| Integration | Real SQL, migrations, Redis and signed private object storage. | JUnit and Testcontainers. |
| Browser | Real member/staff journeys, privacy, uploads, errors and mockup comparison at desktop/mobile widths. | Interactive browser automation and screenshots. |

## Required scenarios

- Register/login/refresh/logout; invalid credentials; forged or expired JWT; account closure and role boundaries.
- Public/private profiles, friend request/accept/decline/cancel/unfriend/block/unblock, and unauthorized direct URLs.
- Feed/posts/reposts/likes; nested comment depth and tombstones; pagination and empty states.
- Instant/weekly events, invitations, applications, acceptance/decline/withdrawal, occurrence cancellation and last-seat contention.
- Combined people/event filters, explainable suggestions, exclusions/dismissals, matching opt-in persistence and no double assignment.
- Text/image/audio messages, delivery with socket fallback, sender deletion and conversation access.
- Signed media upload/download, content validation, quota, hidden/deleted media, processing limits and cleanup.
- Moderator/admin lists, report resolution, moderation, audit, role changes and production fixture guards.

## Evidence and completion

A feature requiring deployed behavior needs a real browser check after release, including failure paths and persistence where relevant. Compare major routes with the supplied mockups and check mobile overflow, input labels and loading/error states. Passing unit tests do not establish visual parity or production readiness.

Container integration tests must run in CI; explicitly distinguish unavailable local Docker from executed tests. Fixture performance and relevance measurements are separate from dataset creation. The bounded 1,000-user integration dataset does not establish the latency of a full 3,000-user deployment.

Record requirement IDs, tested revision/environment, observed result and remaining limitations in [release verification](06-Release-verification.md). [Fixture details](../40-Technical-specifications/07-Test-fixtures.md) describe reproducibility and safe local generation.
