# User matching algorithm

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [../30-Functional-specifications/07-Events.md](../30-Functional-specifications/07-Events.md), [01-Friend-suggestions.md](01-Friend-suggestions.md) |

## Problem

The brief lists **matching users** as an algorithm to design. Two concrete problems appear in Gym Buddies:

1. **Session fill:** for an event with remaining seats, rank applicants / suggested invitees
2. **Buddy pair:** for a member who wants “someone to train with this week”, propose a partner and a slot

Suggestions (who to *friend*) are graph-social. Matching (who to *train with*) is a **constrained assignment**.

## Problem 1 — rank for an event

For event \(e\) and candidate \(v\) (applicant or suggested invitee):

\[
M(e,v) = a_1 A + a_2 J + a_3 G + a_4 T + a_5 H
\]

| Term | Meaning | Weight |
| --- | --- | --- |
| \(A\) | 1 if \(v\) applied, 0.3 if only suggested | 0.30 |
| \(J\) | Jaccard(sports, {e.activity}) or 1 if activity ∈ sports | 0.25 |
| \(G\) | Geo closeness to event | 0.20 |
| \(T\) | Window overlap with `starts_at` | 0.15 |
| \(H\) | History: previous accepted co-attendance with organizer | 0.10 |

Used by the organizer UI (“suggested accept order”) and by “people you may invite”.

**Capacity** is not in the score; it is a hard constraint when accepting (FS-EVT-07).

## Problem 2 — weekly buddy assignment

Input: set \(U\) of members who opted into “match me this week”, each with windows and sports.

We build a **weighted undirected graph**:

- Edge \(uv\) if they share a sport, are not blocked, both public-or-friends-ok, and have ≥ 60 min overlapping window
- Weight = \(J + T + G + 0.2\cdot\mathbf{1}_{\text{already friends}}\)

We want a **matching** (each person at most one new buddy this week) of maximum weight.

### Algorithm

Exact blossom (Edmonds) is \(O(n^3)\) and heavier than we need for a few hundred opt-ins.

Use a **greedy maximal matching**:

1. Sort edges by weight descending
2. Scan; add edge if both endpoints are free
3. Break remaining ties with earlier `created_at` (fairness)

Approximation: ≥ 1/2 of maximum weight matching. Good enough, easy to justify, easy to unit-test.

If \(|U| \le 80\), we may run a blossom implementation in a library and compare greedy in a test (algorithmic bonus).

### Output

Each matched pair gets a **proposed instant event** (draft, `visibility=friends`, capacity=1) at the midpoint of the overlapping window. Members still accept (human in the loop).

## Why this and not “just search”

Search is retrieval. Matching adds:

- Hard capacity / one-partner constraints
- A global (or greedy global) objective, not a per-user top-k
- A clear place to discuss complexity and approximation

That is the Algorithms module evidence, distinct from suggestions.

## Tests

- Greedy never assigns one person twice
- No edge across a block
- Empty overlap → no edge
- Tiny graph: greedy result equals the obvious optimum
