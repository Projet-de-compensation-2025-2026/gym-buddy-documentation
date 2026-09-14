# Backend

Gym Buddy is a Java 25 / Spring Boot modular monolith. Controllers implement interfaces generated from the separately versioned [OpenAPI contract](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi). Service 1.2.0 uses Spring Boot 4.1.0. [Release verification](../80-Testing/06-Release-verification.md) records the deployed revision.

Requests pass through controllers, application services, domain rules and persistence adapters. Domain packages cover authentication, profiles, friendships, feed, posts, comments, events, search, suggestions, matching, messaging, media and staff administration. Authorization is checked by the service handling each resource.

| Component | Implemented responsibility |
| --- | --- |
| Spring MVC and generated interfaces | HTTP endpoints and validation |
| JDBC / PostgreSQL / Flyway | Durable domain records and schema migrations |
| Custom access-token filter / JJWT | JWT validation and current account checks |
| Spring Security Crypto / Argon2id | Password hashing |
| Redis / Lettuce | Refresh credential state and messaging publication |
| WebSocket gateway | Message and unread-count notifications |
| SeaweedFS through AWS S3 SDK | Private image/audio objects and short-lived signed URLs |
| Scheduled jobs | Suggestion refresh, matching and media cleanup |

Search filtering and ranking run in Java over database candidates. Suggestion scores are stored in PostgreSQL. Image processing occurs in the media completion flow; there is no separate image worker service. Weekly event recurrence is expanded by the project's `WeeklyRrule` implementation in UTC. No event timezone is stored, so local clock time can shift across daylight-saving transitions.

Secrets are external environment configuration. See [environment](../10-Getting-started/04-Environment-and-pipeline.md), [storage](../40-Technical-specifications/04-Image-storage.md) and [verification](../80-Testing/06-Release-verification.md).
