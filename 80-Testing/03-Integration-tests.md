# Integration tests

The service runs JUnit tests against disposable PostgreSQL, Redis and S3-compatible storage through Testcontainers. Docker is required; CI requires the integration suites to execute and rejects skipped container tests. Unit-only local results are recorded separately.

| Suite | Boundary exercised |
| --- | --- |
| `AuthIT`, `ProfilesIT` | Persistent accounts/authentication and profile visibility. |
| `ConversationsIT` | Stored direct conversations/messages and participant access. |
| `EventsIT` | Persisted events, applications and transactional capacity behavior. |
| `MediaIT`, `ReadinessIT` | Real signed object-storage operations, media processing and dependency readiness. |
| `FixtureGeneratorIT` | Related fixture rows and a bounded 1,000-user dataset with database constraints. |
| `AdminCatalogIT` | Staff listing SQL with optional filters and PostgreSQL parameter typing. |
| `PostgresImageIT` | Replacement database image startup/tool/locale behavior; it does not prove a production-data migration. |

The S3 compatibility checks cover signed PUT/GET/HEAD/delete, object metadata, anonymous access denial and tampered upload length. Image scanning is a separate security check. A database migration additionally requires protected dump/restore rehearsal with every table's counts/content hashes and index/constraint checks; starting an empty replacement database is insufficient.

Each suite controls its own disposable data. Do not infer one universal transaction rollback fixture or test duration. Run the repository's normal Maven verification command and inspect the test report; [release verification](06-Release-verification.md) records the precise executed revision and outcomes.
