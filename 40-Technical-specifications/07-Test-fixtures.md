# Test fixtures

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../80-Testing/01-Test-plan.md](../80-Testing/01-Test-plan.md), [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md) |

The brief requires **thousands of test fixtures**.

## Goals

- Local demo looks alive (feed, search, suggestions, events)
- Algorithms have a non-trivial graph
- Tests can opt into a small deterministic set **or** a large seeded set

## How

Factory classes (`UserFactory`, `PostFactory`, …) on top of **Datafaker** (Java) with a **fixed seed** (`FIXTURE_SEED=20260813`). This matches the Approved stack. Do not add `@faker-js/faker` to the backend.

A CLI / back-office action:

```
./mvnw -pl fixtures exec:java -- --users 3000 --posts-per-user 5 --events 800
```

Default target (order of magnitude):

| Entity | Count |
| --- | --- |
| Users | 3 000 |
| Friendships (accepted) | 12 000 |
| Posts | 15 000 |
| Comments | 20 000 |
| Events | 800 |
| Applications | 4 000 |
| Messages | 10 000 |
| Media metadata | 5 000 (reuse a handful of real objects) |

## Media note

Do **not** store 15 000 unique JPEGs. Upload ~10 stock images to MinIO and point many `media` rows at those keys, or use 1×1 pixel fixtures in unit tests. This keeps the “no local disk” rule and the “thousands of rows” rule.

## Graph shape

- Power-law-ish friends: a few hubs, many low-degree users (so suggestions have mutual friends)
- Clusters by `city` + `sports` (so search and matching are visibly right)
- Named demo accounts that always exist:

| Handle | Role | Password |
| --- | --- | --- |
| `demo.alex` | member | local `.env` only |
| `demo.blake` | member, friend of alex | local `.env` only |
| `demo.mod` | moderator | local `.env` only |
| `demo.admin` | admin | local `.env` only |

## Safety

- Fixture reset is **disabled** when the Spring profile is `prod`
- The command truncates only if `--reset` is passed
- Passwords for bulk users are a single known hash to speed inserts

## Tests vs demo

| Suite | Dataset |
| --- | --- |
| Unit | In-memory objects, no DB |
| Integration | Migrations + tiny factories (tens of rows) |
| Functional / demo | Large seed, optional |
