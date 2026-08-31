# Improvements

| Field | Value |
| --- | --- |
| Status | Proposed |

Ranked. “Now” means before the defense if time remains. “Later” is post-MVP. “Out of scope” stays unless the instructor expands the brief.

## Now (if time)

1. Exact matching on the weekly opt-in set when \(n \le 80\), and a table comparing greedy vs exact
2. `pg_trgm` for typo-tolerant city / handle search
3. Event discussion thread (reuse comments)
4. Rate limits on login, register, media, messages
5. Recorded backup of the demo (network will fail)
6. Operator `GYM_BUDDY_BOOTSTRAP_STAFF` so academic shots 15–16 exist
7. Configure VPS object storage so `POST /media` mints signed URLs (chat image/audio and post images)

## Later

| Idea | Why |
| --- | --- |
| RS256 access tokens | Split verify from issue |
| Elasticsearch / Meilisearch | If people+events grow past comfortable SQL |
| Group chats per event | Natural once matching ships |
| E2E encryption for DM | Real privacy; hard with image/audio and moderation |
| Native mobile | Better audio capture; large extra surface |
| Calendar sync (ICS) | Recurring events already have RRULE |
| Push notifications | Retention, not academic value |
| PostGIS | Serious geo |
| Recommendation offline metrics dashboard | Stronger algorithm chapter |

## Out of scope

Payments, ads, wearables, public graph export, multi-tenant white-label.

When an improvement is adopted, move it to a spec page and add a changelog bullet; do not leave it only here.
