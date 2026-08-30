# Functional tests

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../99-Academic-deliverables/03-Screenshots.md](../99-Academic-deliverables/03-Screenshots.md) |

Browser-level journeys. Keep the set small and aligned with the defense demo.

## Journeys (Playwright)

| ID | Journey | FS IDs |
| --- | --- | --- |
| FT-01 | Register, log in, complete public profile | FS-ACCT, FS-PROF |
| FT-02 | A requests B, B accepts, A sees B’s private bio | FS-FRND, FS-PROF |
| FT-03 | A posts, B likes and comments twice (nested) | FS-POST, FS-CMT, FS-FEED |
| FT-04 | A creates friends-only event capacity 1; B applies; A accepts; C cannot | FS-EVT |
| FT-05 | Search people by sport + city | FS-SRCH |
| FT-06 | Suggestions shows a FoF; add friend | FS-SUGG |
| FT-07 | Friends exchange a text and an image | FS-MSG, FS-MED |
| FT-08 | Admin hides a post; member feed omits it | FS-ADM |

## Non-goals

Pixel-perfect snapshots. Assert text, roles, and URL. Capture screenshots as **artifacts** for the report (see academic checklist), not as the assertion.

## Demo script

FT-02 → FT-04 → FT-07 is the 20-minute spine. Automate them so a regression the night before the defense is visible.
