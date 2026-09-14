# Filtered search algorithm

The implementation first removes invisible candidates, then applies the selected filters, ranks matching results and returns a stable page. This order makes authorization a prerequisite to discovery.

The [technical specification](../40-Technical-specifications/06-Search-implementation.md) documents the actual Java tokenizer, weights and catalog scan. Filtering is O(N) and sorting M matches is O(M log M), before relationship lookup costs. This is understandable and testable for the academic dataset, but its performance at thousands of records must be measured rather than assumed.

The weighted score balances text relevance, freshness, distance and social connection. Explicit weights make ordering explainable. Identifier tie-breaking avoids arbitrary ordering between equally ranked results. Cursor tests must include equal scores and changed filters.

A PostgreSQL full-text/indexed implementation would reduce data transfer and scanning as the dataset grows, but it is a proposed improvement, not the current implementation. Compare actual latency, query counts and relevance on the fixture dataset before adopting it.
