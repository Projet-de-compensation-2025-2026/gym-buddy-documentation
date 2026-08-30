# Filtered search algorithm

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../30-Functional-specifications/08-Advanced-search.md](../30-Functional-specifications/08-Advanced-search.md), [../40-Technical-specifications/06-Search-implementation.md](../40-Technical-specifications/06-Search-implementation.md) |

## Problem

Given a query \(q\) and a filter vector \(F\), return a page of people or events the caller is allowed to see, ordered by a defined rank.

## Filter algebra

Filters are **predicates conjoined** (AND). Multi-valued sports use **OR inside the field** (ANY).

\[
R = \{ x \in X \mid \mathrm{auth}(u,x) \land \bigwedge_i f_i(x) \land \mathrm{text}(x,q) \}
\]

`auth` is the visibility predicate (not a ranking signal).

## Text

PostgreSQL `plainto_tsquery` on a weighted `tsvector`:

- People: `display_name` A, `handle` A, `bio` B, `city` C, `sports` B
- Events: `title` A, `activity` A, `description` B, `place` C

Empty \(q\) means “filters only”.

## Rank

\[
\mathrm{rank}(x) = \alpha\,\mathrm{ts\_rank} + \beta\,\mathrm{recency} + \gamma\,\mathrm{geo} + \delta\,\mathrm{social}
\]

| Term | People | Events | Default |
| --- | --- | --- | --- |
| `ts_rank` | FTS | FTS | \(\alpha=0.45\) |
| `recency` | last profile update | start time closeness to now (future only) | \(\beta=0.20\) |
| `geo` | same as suggestions | distance to event | \(\gamma=0.20\) |
| `social` | 1 if friend, 0.5 if FoF, else 0 | 1 if organizer is friend | \(\delta=0.15\) |

Callers may override **sort** to `distance` or `starts_at`, which replaces the composite with that key (still filtered).

## Pagination

Keyset: `(rank, id)` or `(starts_at, id)`. Avoid `OFFSET`.

## Complexity

With indexes from the data model, each filter is \(O(\log n + |page|)\). A wide FTS on 3k rows is a sequential bitmap AND — acceptable. Document the EXPLAIN plan in the report if asked.

## Why not inverted-index-from-scratch

Implementing a toy inverted index would demonstrate IR, but:

- Visibility + radius + capacity need a real query planner
- PostgreSQL FTS **is** an inverted index
- Time is better spent on suggestions and matching, which the brief names explicitly

If we need highlighting and typo-tolerance later, add trigram (`pg_trgm`) before Elasticsearch.

## Invariants (tests)

- Private strangers never appear
- Blocked never appear
- Full events omitted when `remaining=true`
- Changing only `sort` does not change the *set* of ids on an unpaginated query, only the order
