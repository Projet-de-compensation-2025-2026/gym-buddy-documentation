# Search implementation

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [../50-Algorithms/02-Filtered-search.md](../50-Algorithms/02-Filtered-search.md), [../30-Functional-specifications/08-Advanced-search.md](../30-Functional-specifications/08-Advanced-search.md) |

## Stack at MVP

PostgreSQL:

- `tsvector` columns on `profiles` and `events` (and `posts` if we expose post search later)
- B-tree on `city`, `activity`, `starts_at`, `experience_level`
- `text[]` GIN on `sports`
- Optional `earthdistance` / `cube` for radius

No Elasticsearch until the improvement list is acted on.

## Request

`GET /search/people` and `GET /search/events` with query parameters matching FS-SRCH. Jakarta Bean Validation (and the OpenAPI schema) validate ranges (`radius` 1–50 km, dates, enums).

## Execution plan (people)

1. Authorize (must be a member)
2. Base set: `status = active` and not blocked
3. Visibility predicate (public OR friend OR self)
4. Equality / array filters
5. Optional radius (`earth_distance`)
6. `q` via `@@ plainto_tsquery`
7. Order by rank + distance
8. Keyset pagination

Events follow the same shape plus `starts_at` window and `capacity - accepted > 0`.

## Why SQL is enough

Fixture-scale (thousands to tens of thousands of rows) is well inside PostgreSQL. The academic value is the **filter algebra and ranking**, not operating a search cluster. See algorithm justification.
