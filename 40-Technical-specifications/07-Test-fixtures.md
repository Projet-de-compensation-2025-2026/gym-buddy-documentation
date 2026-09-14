# Test fixtures

The school brief requires thousands of fixtures. Java Datafaker factories and `JdbcFixtureGenerator` create related users, profiles, friendships, posts, comments, events/applications and text conversations in a disposable PostgreSQL database.

## Run locally

Configure the service's local database/object-store environment and keep the Spring `prod` profile disabled. From the service repository:

```sh
mvn compile exec:java -Dexec.mainClass=fr.projetcompensation.gymbuddy.fixtures.FixturesCli -Dexec.args="--users 3000 --posts-per-user 5 --events 800"
```

The entry point starts the required Spring context without an HTTP listener. `--reset` deletes all users and related data in the configured test database, not only rows previously created by fixtures. Use it only with a disposable database; omit it to preserve existing rows. The generator uses `FIXTURE_SEED` (default `20260813`) and a fixed January 2026 time origin. An explicit `--seed` overrides that environment setting; omitting it preserves the configured seed. Focused tests verify both argument forms and precedence.

| Entity | Default requested count | Maximum accepted count |
| --- | ---: | ---: |
| Users | 3,000 | 10,000 |
| Friendships | 12,000 | 50,000 |
| Posts | 15,000 | 50,000 |
| Comments | 20,000 | 80,000 |
| Events | 800 | 5,000 |
| Applications | 4,000 | 20,000 |
| Messages | 10,000 | 50,000 |
| Media metadata | 5,000 | 20,000 |

Explicit flags also accept friendships, posts, comments, applications, messages and media counts. Counts are clamped; graph feasibility can reduce generated totals. `FriendshipFactory` biases selections toward low-index hubs and matching city/sport clusters, with bounded attempts. This is synthetic graph structure, not a measured real-world distribution.

## Media and accounts

Media rows reuse ten stock object keys to bound storage. The stock payload is a decodable 32×32 JPEG pattern, verified by an image-decoder regression test. Reusing these tiny objects bounds fixture storage; it does not establish the quality of real user images, which are tested separately through signed uploads and processing.

Named fixture users include `demo.alex`, `demo.blake`, `demo.mod` and `demo.admin`. Password values belong in local secret configuration; bulk synthetic users share a precomputed hash per generation. Fixtures are test data and must not be used as production credentials.

Generation/reset HTTP actions and the CLI are disabled under the `prod` profile. The separate environment-gated `StaffBootstrapCli` only creates missing designated staff accounts and is not the bulk generator. Staff bootstrap and bulk fixture generation are separate operations; current deployment evidence is recorded in the release-verification page.

## Evidence

Unit tests cover factory relationships and argument/guard behavior. Disposable PostgreSQL integration tests exercise a bounded 1,000-user fixture set. This proves the tested dataset and constraints; the full default 3,000-user live deployment and its performance have not been verified. See [test plan](../80-Testing/01-Test-plan.md) and [release verification](../80-Testing/06-Release-verification.md).
