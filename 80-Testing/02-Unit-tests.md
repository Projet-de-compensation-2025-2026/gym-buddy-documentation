# Unit tests

| Field | Value |
| --- | --- |
| Status | Draft |

Especially on the **backend**, as required.

## What is a unit here

A function or class with in-memory dependencies (fake repos, fixed clocks). No HTTP server, no real database.

## Mandatory units (minimum set)

| Area | Examples |
| --- | --- |
| Auth | Password verify, claim builder, refresh rotation logic |
| Friends | Accept, block, self-friend rejection |
| Visibility | `profile.isVisibleTo`, `event.isVisibleTo`, `media.canRead` |
| Comments | Depth increment and cap |
| Events | Remaining seats, cannot apply to self, recurrence expansion for a window |
| Suggestions | Feature math, forbidden-set filter, top-k, primary reason |
| Matching | Greedy pairing uniqueness, no-block invariant |
| Search rank | Sort comparator |
| Quotas | Sum + reject |

## Style

```java
@Test
void fsEvt07_acceptFailsWhenRemainingSeatsIs0() {
    Event event = Event.rehydrate(/* capacity 1, accepted 1 */);
    assertThatThrownBy(() -> event.accept(application))
        .isInstanceOf(CapacityException.class);
}
```

Use a fake clock for “edit window 15 minutes” and “dismiss 30 days”.

## What not to unit-test

Hibernate / Spring internals, generated OpenAPI clients, CSS. Cover those at integration / visual review.
