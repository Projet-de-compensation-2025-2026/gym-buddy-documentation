# Improvements

Required features and defects remain tracked as acceptance gaps until verified; they are not future scope. Beyond that baseline, useful improvements are:

- Move search filtering/ranking closer to PostgreSQL after measuring fixture-scale bottlenecks.
- Measure recommendation precision and coverage, then tune documented weights.
- Add durable incremental suggestion recomputation if scheduled/on-read refresh is insufficient.
- Add release provenance and critical browser journeys as release gates.
- Expand recurrence formats only when required, using compatibility tests.

Prioritize measured user impact and maintenance cost. Avoid introducing services or libraries solely for architectural appearance.
