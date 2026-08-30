# Test plan

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../40-Technical-specifications/07-Test-fixtures.md](../40-Technical-specifications/07-Test-fixtures.md) |

The brief asks for a **reasonable** plan covering functional, unit, and integration tests — not 100% of every getter.

## Test pyramid

| Layer | Where | Share of effort | Tool |
| --- | --- | --- | --- |
| Unit | Domain services, algorithms, security rules | ~60% | JUnit 5 + AssertJ |
| Integration | API + DB + bucket (Testcontainers: PostgreSQL, MinIO) | ~25% | JUnit 5 + MockMvc / WebTestClient |
| Functional | Critical user journeys in a browser | ~15% | Playwright against Angular |

Backend unit tests are the academic priority.

## Risk-based coverage

Must have automated tests:

| Risk | Tests |
| --- | --- |
| JWT forged / expired / wrong `typ` | Unit + integration |
| Private profile / friends-only event leak | Integration |
| Capacity race on accept | Integration (transaction) |
| Comment depth cap | Unit |
| Suggestion forbids friends/blocks | Unit on a fixture graph |
| Matching double-assigns | Unit |
| Signed URL without `canRead` | Integration |
| Fixture command refused in production | Unit |

Should have:

- Feed pagination
- Search filters (sports + city + remaining)
- Message persist when WS is down
- Role guard on `/admin`

Won’t automate at MVP:

- Visual polish
- Mail rendering
- Full 3 000-user performance (one manual EXPLAIN + one timed suggestion run is enough for the report)

## Definition of done for a feature

1. FS IDs listed in the PR
2. Unit tests for every new business rule
3. At least one integration test if an HTTP contract changed
4. Functional test only if the journey is in [04-Functional-tests.md](04-Functional-tests.md)

## Environments

| Env | Data |
| --- | --- |
| CI unit | No I/O |
| CI integration | Ephemeral Postgres (+ MinIO if services available) |
| Local demo | Large fixtures |
| Production | Fixtures disabled |

## Traceability

Name tests after IDs: `FS-EVT-07 rejects accept when full`.
