# Screenshot checklist

| Field | Value |
| --- | --- |
| Status | Live v1.1.0 captured 2026-08-31 (member shots 1–14, wiki 17–18, VPS 19). Admin 15–16 blocked: no staff login on prod |
| Related | [screenshots/README.md](screenshots/README.md) |

Captured from the **running Angular UI** on GitHub Pages tag **v1.1.0** (`https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/`) against `https://vps-c39cdf03.vps.ovh.net/api/v1`. These are **not** wiki mockup JPGs.

`demo.alex` / `demo.blake` passwords are not in git and Docker Desktop was down, so three fresh members were registered and friended (`alex71mthjayav`, `blake71mthjayav`, `casey71mthjayav`). Store images next to this file (`screenshots/`).

| # | Shot | File | FS | Notes 2026-08-31 |
| --- | --- | --- | --- | --- |
| 1 | Register / login | [01-register.png](screenshots/01-register.png), [01-register-login.png](screenshots/01-register-login.png) | FS-ACCT | Create-account + “Account created. Sign in” from Pages. |
| 2 | Public profile | [02-public-profile.png](screenshots/02-public-profile.png) | FS-PROF | Alex Live, Paris, weightlifting / running. |
| 3 | Private profile as stranger (stub) | [03-private-profile-stranger.png](screenshots/03-private-profile-stranger.png) | FS-PROF-04 | Blake private stub + Request Friend. |
| 4 | Friend request pending / accepted | [04-friend-request-pending.png](screenshots/04-friend-request-pending.png), [04-friend-request.png](screenshots/04-friend-request.png) | FS-FRND | Outbound pending, then accepted friends list. |
| 5 | Friends feed with a post and a repost | [05-friends-feed-post-repost.png](screenshots/05-friends-feed-post-repost.png) | FS-FEED | Blake’s post + “Alex Live reposted”. |
| 6 | Post with likes | [06-post-likes.png](screenshots/06-post-likes.png) | FS-POST | Liked / 1 Like on the same post. |
| 7 | Comment thread 3+ levels | [07-comment-thread.png](screenshots/07-comment-thread.png) | FS-CMT | Levels 1–3 on the post detail. |
| 8 | Create friends-only event | [08-friends-only-event-form.png](screenshots/08-friends-only-event-form.png), [08-friends-only-event.png](screenshots/08-friends-only-event.png) | FS-EVT | Place, 90 min, capacity 1, visibility friends. |
| 9 | Application pending / accepted / full | [09-event-applications-pending.png](screenshots/09-event-applications-pending.png), [09-event-applications.png](screenshots/09-event-applications.png) | FS-EVT-06/07 | Blake pending (score 0.30); Casey sees Full / 1. |
| 10 | Recurring event occurrence list | [10-recurring-event-occurrences.png](screenshots/10-recurring-event-occurrences.png) | FS-EVT-03 | WEEKLY Saturday run, Next 90 Days. |
| 11 | Advanced search with several filters | [11-advanced-search.png](screenshots/11-advanced-search.png) | FS-SRCH | q=Live, city=Paris, sport=weightlifting, intermediate. |
| 12 | Suggestions with “why” text | [12-suggestions-why.png](screenshots/12-suggestions-why.png) | FS-SUGG-03 | **Empty.** Prod has no 3 000-user fixtures; FoF of three live users did not yield a card (recompute is async / nightly). |
| 13 | Chat: text + image + audio | [13-chat-text-image-audio.png](screenshots/13-chat-text-image-audio.png) | FS-MSG | Text delivered. Image/audio: live API `media is not configured`. |
| 14 | Denied media (or expired URL) | [14-denied-media.png](screenshots/14-denied-media.png), [14-denied-media-api.png](screenshots/14-denied-media-api.png) | FS-MED-06 | Stranger UI: friends-only post → “post not found” (no existence leak). `GET /media/{id}/url` is 401 `media is not configured` — no signed URL to expire. |
| 15 | Back-office: role change + audit | [15-admin-login-blocked.png](screenshots/15-admin-login-blocked.png), [15-admin-member-rejected.png](screenshots/15-admin-member-rejected.png) | FS-ADM | **Blocked.** `demo.admin` / `demo.mod` are not on prod (#78 bootstrap not SSH-run). Member login → “Staff accounts only.” No staff password in git. |
| 16 | Back-office: hidden post | — | FS-ADM-03 | **Blocked** (same staff login). |
| 17 | Architecture diagram (wiki Mermaid) | [17-architecture.png](screenshots/17-architecture.png) | Deliverable | Export of `20-Architecture/01-Software-architecture.md`. |
| 18 | Data model diagram | [18-data-model.png](screenshots/18-data-model.png) | Deliverable | Export of `20-Architecture/06-Data-model.md`. |
| 19 | HTTPS probe / health on the VPS | [19-https-health.png](screenshots/19-https-health.png) | Hosting | Operator network: `healthz` and `readyz` HTTP 200 `{"status":"ok"}`. |

Each figure in the report gets a one-sentence caption.

Shots 1–14, 17–19 are in git. Shots 15–16 wait on an operator `GYM_BUDDY_BOOTSTRAP_STAFF` boot ([../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md)).
