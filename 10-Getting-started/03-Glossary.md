# Glossary

| Field | Value |
| --- | --- |
| Status | Draft |

| Term | Meaning in this project |
| --- | --- |
| Member | Authenticated athlete using the product |
| Buddy | Another member the user trains with; usually an accepted friend |
| Friend request | Directed invitation; the addressee must accept |
| Feed | Reverse-chronological (then ranked) stream of posts from friends |
| Post | Member-authored status, possibly with media |
| Repost | Share of an existing post onto the reposter’s identity |
| Like | Toggle engagement on a post or a comment |
| Nested comment | Comment whose parent is another comment on the same post |
| Event | Training session: instant (one-off) or recurring, public or private |
| Instant event | Single occurrence at a given datetime |
| Recurring event | Series described by a recurrence rule plus exceptions |
| Application | Request to join an event; organizer accepts or declines |
| Profile visibility | `public` (discoverable) or `private` (restricted) |
| Suggestion | System-proposed member the user does not already follow as a friend |
| Matching | Pairing members with events or with other members for a session |
| Fixture | Generated data used in development and tests (thousands of rows) |
| Back-office | Staff UI for admins and moderators |
| Controlled file | Any stored blob (image, audio) reachable only after authorization |
| JWT | JSON Web Token used as the access credential |
| Organizer | Member who created an event (role on that event, not a global role) |

Identifiers in specs look like `FS-EVENTS-03` (functional) or `TS-JWT-02` (technical). Use them in tests and review comments.
