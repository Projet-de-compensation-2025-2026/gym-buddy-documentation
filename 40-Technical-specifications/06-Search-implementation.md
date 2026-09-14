# Search implementation

`JdbcSearchCatalog` retrieves candidate people and events from PostgreSQL. `SearchService` applies visibility and filters, computes scores, sorts and cursor-pages the candidates in Java. The current implementation does not execute PostgreSQL full-text `ts_rank` queries or use a GIN search index.

`SearchText` lowercases text and splits it on non-ASCII-letter/digit characters. Every query token must match a substring in the searchable fields. Field groups contribute weights of 1.0, 0.4 and 0.2. This simple tokenizer has limitations for accented and non-Latin text.

Ranking combines 0.45 text, 0.20 recency, 0.20 geography and 0.15 social proximity. Person recency decays over 90 days; event recency over 14 days. Geographic score decreases to zero at 50 km. Accepted friends and friends of friends influence social ranking. Deterministic identifier tie-breaking supports pagination.

Filters compose with AND; selected alternatives within a multi-valued filter compose with OR. Distance filtering is optional and requires coordinates. Private profiles/events are filtered according to authorization before results are exposed.

For N catalog candidates and M matching results, the current path includes an O(N) scan and O(M log M) sort plus relationship lookups. There is no measured indexed-query performance claim. A database-backed search plan with appropriate indexes is a future scaling improvement.

See [functional search requirements](../30-Functional-specifications/08-Advanced-search.md) and [algorithm justification](../50-Algorithms/02-Filtered-search.md).
