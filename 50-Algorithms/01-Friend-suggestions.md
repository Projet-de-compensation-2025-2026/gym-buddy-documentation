# Friend suggestion algorithm

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../30-Functional-specifications/09-Friend-suggestions.md](../30-Functional-specifications/09-Friend-suggestions.md) |

## Problem

For a member \(u\), return \(k\) other members they do not already know, ranked by how likely a useful gym friendship is.

This is the assignment’s “personalized friend suggestions (algorithm used must be justified)”.

## Constraints

- Thousands of users (fixtures), not millions
- Must explain each card (“why this person”)
- Must respect blocks, pending requests, private profiles
- Response-time target: < 200 ms p95; requires measurement on fixture data.

## Approach: two-stage generate-and-score

### Stage A — candidate generation

Build a set \(C(u)\) of size ≤ 200:

1. Friends of friends (FoF) not already connected — primary
2. Same `city` (or radius ≤ 15 km) ∩ at least one shared sport
3. Co-participants in the same accepted event (last 90 days)

Union, minus `{u}`, friends, pending, blocked, dismissed-30d, locked.

FoF dominates social products and is cheap if we store adjacency lists.

### Stage B — scoring

\[
S(u,v) = w_1 \hat{m} + w_2 J + w_3 G + w_4 T + w_5 E
\]

| Symbol | Feature | Range | Default \(w\) |
| --- | --- | --- | --- |
| \(\hat{m}\) | Mutual friends, Adamic–Adar: \(\sum_{z \in N(u)\cap N(v)} 1/\log(1+\deg(z))\) min-max normalized on \(C(u)\) | 0–1 | 0.35 |
| \(J\) | Jaccard of `sports` sets | 0–1 | 0.25 |
| \(G\) | Geo: \(1 - \min(d_{km}, D)/D\) with \(D=25\), or 0.4 if same city and no coords | 0–1 | 0.15 |
| \(T\) | Overlap of `preferred_windows` (hours / week shared ÷ 10, capped at 1) | 0–1 | 0.15 |
| \(E\) | Experience closeness: 1 if equal, 0.5 if adjacent, 0 else | 0–1 | 0.10 |

Weights sum to 1. They are explicit constants in the scorer, allowing a sensitivity discussion.

**Primary reason** on the card = feature with the largest \(w_i \cdot \text{feature}_i\).

### Stage C — serve

Read top \(k\) from `suggestion_scores` for \(u\). If the row set is older than 48 h, run Stage A+B **only for \(u\)** (FoF query is indexed).

Recompute:

- Nightly for all users (batch)
- On a request when stored scores are absent, older than 48 hours, or predate the viewer’s latest relationship change. This refresh is synchronous; an incremental neighbor worker is not implemented.

## Complexity

Candidate generation caps the scored set at 200. Graph-neighbor intersections, recent attendance and profile compatibility still require data access; the cap alone does not make the entire request constant-time. Scoring traverses candidate features and the implementation sorts all scores in O(C log C), then takes the requested top k (default 20, maximum 50). It does not use a top-k heap.

Stored scores live in PostgreSQL. A daily job at 03:15 UTC refreshes suggestions and assigns weekly matches. Database query count and nightly duration need fixture-scale measurements.

## Why not the alternatives

| Alternative | Why rejected |
| --- | --- |
| Random public users | Not personalized; fails the brief |
| Collaborative filtering (ALS) | Needs implicit feedback volume we will not have on day one; opaque “why” |
| Graph embeddings / GNN | Unjustifiable training cost; cannot explain a card |
| Only mutual friends | Ignores sport/schedule, the actual gym-buddy signal |
| Only geo | Creates a phonebook of neighbors, including incompatible sports |

Adamic–Adar + domain features is standard, explainable, and matches “Algorithms and Advanced Programming” without fake ML.

## Evaluation (for the report)

On fixture clusters (city × sport):

- **Precision@10**: fraction of suggestions that share ≥ 1 sport and are in the same cluster
- **Coverage**: % of users who receive ≥ 5 suggestions
- **Abuse**: 0 blocked users in any list (invariant test)

These are proposed evaluation metrics, not measured results. Existing tests verify scoring and exclusion rules; report measured precision and coverage only after running an explicit evaluation.

## Pseudocode

```
function suggest(u, k):
  C ← fof(u) ∪ sameCityAndSport(u) ∪ recentCoParticipants(u)
  C ← C minus forbidden(u)
  for v in C:
    score[v] ← weightedFeatures(u, v)
  return topK(score, k) with reasons
```
