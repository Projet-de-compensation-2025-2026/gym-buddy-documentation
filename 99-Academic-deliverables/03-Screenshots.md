# Screenshot checklist

| Field | Value |
| --- | --- |
| Status | Draft — checklist complete; images blocked on UI |

Capture after the UI is stable. Prefer the `demo.alex` / `demo.blake` accounts. Store images next to this file (`screenshots/`) when they exist. Do not commit placeholder images.

| # | Shot | Feature | FS |
| --- | --- | --- | --- |
| 1 | Register / login | Accounts | FS-ACCT |
| 2 | Public profile | Profiles | FS-PROF |
| 3 | Private profile as stranger (stub) | Profiles | FS-PROF-04 |
| 4 | Friend request pending / accepted | Friends | FS-FRND |
| 5 | Friends feed with a post and a repost | Feed | FS-FEED |
| 6 | Post with likes | Engagement | FS-POST |
| 7 | Comment thread 3+ levels | Comments | FS-CMT |
| 8 | Create friends-only event (place, duration, time, capacity) | Events | FS-EVT |
| 9 | Application pending / accepted / full | Events | FS-EVT-06/07 |
| 10 | Recurring event occurrence list | Events | FS-EVT-03 |
| 11 | Advanced search with several filters | Search | FS-SRCH |
| 12 | Suggestions with “why” text | Suggestions | FS-SUGG-03 |
| 13 | Chat: text + image + audio | Messaging | FS-MSG |
| 14 | Denied media (or expired URL) | File ACL | FS-MED-06 |
| 15 | Back-office: role change + audit | Admin | FS-ADM |
| 16 | Back-office: hidden post | Moderation | FS-ADM-03 |
| 17 | Architecture diagram (export from wiki Mermaid) | Deliverable | — |
| 18 | Data model diagram | Deliverable | — |
| 19 | HTTPS probe / health on the VPS (operator network) | Hosting | — |

Each figure in the report gets a one-sentence caption. Do not paste 19 shots without commentary.

Shots 1–16 wait for Angular. Shots 17–18 can be exported from this wiki now. Shot 19 can be taken from `https://vps-c39cdf03.vps.ovh.net` on the operator network.
