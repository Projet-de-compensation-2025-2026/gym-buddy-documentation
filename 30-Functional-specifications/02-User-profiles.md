# User profiles

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) |

Each account has a profile that is **public** or **private**.

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

## Acceptance

- Given a private profile and a stranger, when the stranger opens `/u/:handle`, then they do not see bio, sports, or location.
- Given the same profile and an accepted friend, when they open it, then they see the full profile.
- Given `visibility = public`, when a member searches by sport + city, then this profile is a candidate ([08-Advanced-search.md](08-Advanced-search.md)).
