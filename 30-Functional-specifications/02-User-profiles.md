# User profiles

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md), [12-Media-and-files.md](12-Media-and-files.md) |

## Intent

Each account has a profile that is **public** or **private**. Athletes discover each other from the profile; strangers must not see a private bio, sports, or location.

## Actors

Member (owner or viewer), staff (full view in back-office only).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-PROF-01 | A profile contains display name, bio, sports, experience, city, optional coordinates, preferred time windows, avatar. |
| FS-PROF-02 | The owner can set `visibility` to `public` or `private`. |
| FS-PROF-03 | A **public** profile is readable by any authenticated member and may appear in search. |
| FS-PROF-04 | A **private** profile is fully readable by the owner, accepted friends, and staff. Others see a stub (handle, avatar or placeholder, visibility, “request friend”). |
| FS-PROF-05 | Unauthenticated visitors may see public profiles; they must not see private stubs beyond handle if we allow public handle pages — default: **login required** to view any profile. |
| FS-PROF-06 | The owner can edit all fields; nobody else can (staff can lock the account instead). |
| FS-PROF-07 | Avatar upload follows media rules ([12-Media-and-files.md](12-Media-and-files.md)). |

## Business rules

- Flyway V2 today stores only `display_name`. Remaining columns: `bio`, `visibility` (default `public`), `sports text[]`, `experience_level`, `city`, `lat`, `lng`, `preferred_windows` JSON, `avatar_media_id`.
- `experience_level` ∈ `beginner` \| `intermediate` \| `advanced`.
- `sports` is a small controlled vocabulary plus free-text tags (max 12, each 2–32 chars). Seed: `weightlifting`, `running`, `crossfit`, `yoga`, `hiit`, `cycling`, `swimming`, `climbing`, `martial-arts`, `team-sports`.
- `preferred_windows`: list of `{ weekday: 0–6, start: "HH:MM", end: "HH:MM" }`, max 14.
- Stub payload for a stranger on a private profile: `handle`, `displayName` omitted or initials only, `visibility=private`, `avatar` if the owner did not hide it (default: show avatar), no bio/sports/city/windows/friend count.
- Friend count on a **full** view is the number of `accepted` friendships. Do **not** invent a Workouts / Current Focus progress entity. Mockup 05’s “142 WORKOUTS” and “Current Focus” bars are leftovers. Show friend count; optional “sessions” = accepted event attendances if events exist, otherwise omit.
- Username on Edit Profile **is** `handle` (FS-ACCT-02 uniqueness).
- Mockup 15 “Security / Notifications / Billing” nav: Security/Privacy goes to [01-Accounts-and-administration.md](01-Accounts-and-administration.md). Notifications and Billing are **not** product.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/profiles/me` | FS-PROF-01 |
| `PATCH` | `/api/v1/profiles/me` | FS-PROF-02, FS-PROF-06 |
| `GET` | `/api/v1/profiles/{handle}` | FS-PROF-03, FS-PROF-04, FS-PROF-05 |

Avatar bytes: [12-Media-and-files.md](12-Media-and-files.md) (`kind=avatar`).

## UI

| Route | Mockup |
| --- | --- |
| `/u/:handle` public | [05-public-profile.jpg](../20-Architecture/mockups/05-public-profile.jpg), [05-public-profile-partially-hidden.jpg](../20-Architecture/mockups/05-public-profile-partially-hidden.jpg) |
| `/u/:handle` private stub | [06-private-profile.jpg](../20-Architecture/mockups/06-private-profile.jpg) |
| `/settings/profile` | [15-settings-profile.jpg](../20-Architecture/mockups/15-settings-profile.jpg) |
| `/settings/privacy` visibility cards | [16-settings-privacy.jpg](../20-Architecture/mockups/16-settings-privacy.jpg) |

Chrome: Inter, primary `#006D77`, member nav Feed / Events / Friends / Search / Messages. Tokens: [../20-Architecture/mockups/00-DESIGN.md](../20-Architecture/mockups/00-DESIGN.md).

## Acceptance

- Given a private profile and a stranger, when the stranger opens `/u/:handle`, then they do not see bio, sports, or location.
- Given the same profile and an accepted friend, when they open it, then they see the full profile.
- Given `visibility = public`, when a member searches by sport + city, then this profile is a candidate ([08-Advanced-search.md](08-Advanced-search.md)).
- Given an unauthenticated caller, when they `GET /profiles/{handle}`, then `401 UNAUTHENTICATED`.
- Given owner PATCH with a taken handle, then `409 CONFLICT`.

## Errors

| Situation | Code |
| --- | --- |
| Not logged in | `UNAUTHENTICATED` |
| Unknown / closed handle | `NOT_FOUND` |
| Duplicate handle | `CONFLICT` |
| Invalid sports / windows / experience | `VALIDATION` |

## Links

- Data model: [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md)
- Media: [12-Media-and-files.md](12-Media-and-files.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
- Use cases: [../60-UML-diagrams/01-Use-cases.md](../60-UML-diagrams/01-Use-cases.md)
