# Technology choices

These choices describe the implemented system. Exact dependency versions are maintained in each repository's build files and lockfile.

| Choice | Reason and tradeoff |
| --- | --- |
| Java 25 / Spring Boot / Spring MVC | A typed backend with established HTTP, validation and testing support; one deployable keeps operations manageable for an individual project. |
| JDBC / PostgreSQL / Flyway | Explicit SQL and reviewable migrations make persistence behavior visible. There is no JPA/Hibernate mapping layer. |
| Angular / TypeScript / pnpm | Shared frontend language, generated clients and reproducible workspace builds for member and staff applications. |
| OpenAPI Generator / Orval | One versioned API contract generates backend interfaces and frontend clients; consumer pins must be updated together. |
| JJWT / Argon2id / Spring Security Crypto | JWT signing and password hashing use maintained libraries; resource authorization remains explicit application code. |
| Redis / Lettuce | Atomic refresh-token operations and messaging pub/sub. Suggestions persist in PostgreSQL, not Redis. |
| SeaweedFS / AWS S3 SDK | Private object storage works on the VPS and locally without an AWS account. An HTTPS public presigner endpoint is necessary for browser uploads. |
| Thumbnailator / ImageIO codecs / WebP | Image decoding, metadata removal and bounded variants; native codec versions need security review alongside Java dependencies. |
| Custom weekly recurrence | Small, explicit support for the required weekly recurrence subset. It is not a general RFC 5545 calendar engine. |
| JUnit / Mockito / Testcontainers | Domain tests are fast; real PostgreSQL/Redis integration tests require Docker and must not be counted as passed when skipped. |
| GitHub Actions / Pages / Docker / Caddy | Versioned static sites and an HTTPS API deployment. Image labels and tag-based checkout establish release provenance. |

Search and recommendation algorithms are explained in [Algorithms](../50-Algorithms/README.md). Performance targets are not benchmark results. See [critical analysis](../91-Critical-analysis/01-Current-analysis.md) for limitations.
