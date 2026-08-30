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
- Request path &lt; 200 ms p95 → **precompute candidates**

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

Weights sum to 1. They are constants in config so the defense can show a sensitivity argument.

**Primary reason** on the card = feature with the largest \(w_i \cdot \text{feature}_i\).

### Stage C — serve

Read top \(k\) from `suggestion_scores` for \(u\). If the row set is older than 48 h, run Stage A+B **only for \(u\)** (FoF query is indexed).

Recompute:

- Nightly for all users (batch)
- On accept-friend, for both endpoints and their neighbors (incremental)

## Complexity

Let \(d\) be average degree (~8 with 3k users / 12k edges).

| Step | Time |
| --- | --- |
| FoF | \(O(d^2)\) per user |
| Score one candidate | \(O(d + |sports|)\) |
| Score \(\|C\|=200\) | negligible |
| Nightly all users | \(O(n d^2)\) ≈ 3k × 64 — fine in a script |

No \(O(n^2)\) all-pairs.

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

These metrics are unit-tested on a tiny hand-built graph and integration-tested on a slice of fixtures.

## Pseudocode

```
function suggest(u, k):
  C ← fof(u) ∪ sameCityAndSport(u) ∪ recentCoParticipants(u)
  C ← C minus forbidden(u)
  for v in C:
    score[v] ← weightedFeatures(u, v)
  return topK(score, k) with reasons
```
