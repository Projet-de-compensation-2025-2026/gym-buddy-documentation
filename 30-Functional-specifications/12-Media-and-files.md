# Media and files

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../40-Technical-specifications/04-Image-storage.md](../40-Technical-specifications/04-Image-storage.md), [../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md) |

## Intent

Images (and chat audio) must **not** pile up on the API host disk, and **every file** has controlled access.

## Actors

Member (owner or viewer), worker (variants), staff (inspect/revoke).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-MED-01 | Clients never write to a public `/uploads` directory on the API. |
| FS-MED-02 | Upload is a two-step: metadata + signed PUT to object storage, or multipart through the API that streams to the bucket. |
| FS-MED-03 | Allowed images: `image/jpeg`, `image/png`, `image/webp`. Max 8 MiB each. |
| FS-MED-04 | Allowed audio: `audio/webm`, `audio/mpeg`. Max 8 MiB, max 120 s. |
| FS-MED-05 | Per-user quota: 1 GiB. Over quota → `PAYLOAD_TOO_LARGE` / `CONFLICT` with a clear code `QUOTA_EXCEEDED`. |
| FS-MED-06 | A file is reachable only if the caller could view its parent (avatar if profile visible, post image if post visible, chat image if conversation member). |
| FS-MED-07 | Download uses a **short-lived signed URL** (default 60 s) or a streaming endpoint that re-checks auth. |
| FS-MED-08 | Soft-deleted parents make existing URLs fail after expiry; the object is scheduled for deletion (grace 7 days). |
| FS-MED-09 | The API stores only metadata + object key. Thumbnails are extra objects in the same bucket. |

## Business rules

- `canRead` algorithm: [../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md). Deny and missing both `NOT_FOUND`.
- Production refuses to start without S3 config ([../40-Technical-specifications/04-Image-storage.md](../40-Technical-specifications/04-Image-storage.md)).
- Mockup 15 “Max 2MB” is leftover; the contract is **8 MiB**.
- Strip EXIF. Variants `sm`/`md` WebP. Temp dir cap 256 MiB.
- Orphan `pending` rows older than 1 h are deleted.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `POST` | `/api/v1/media` | FS-MED-02 |
| `GET` | `/api/v1/media/{id}/url` | FS-MED-07 |
| `DELETE` | `/api/v1/media/{id}` | FS-MED-08 |

## UI

No dedicated member route. Avatar on [15-settings-profile.jpg](../20-Architecture/mockups/15-settings-profile.jpg); post images on the feed/post mockups; chat image/audio on [14-chat.jpg](../20-Architecture/mockups/14-chat.jpg). Staff: [20-admin-media.jpg](../20-Architecture/mockups/20-admin-media.jpg).

## Acceptance

- Filling the local API disk with 1 000 avatars is impossible: bytes land in MinIO.
- Given a friends-only post image, when a stranger requests a signed URL, then `NOT_FOUND`.
- Given a valid participant, when they request a URL, then GET on that URL succeeds until expiry.
- Given quota already 1 GiB, when they `POST /media`, then `QUOTA_EXCEEDED`.

## Errors

| Situation | Code |
| --- | --- |
| Bad mime / over 8 MiB | `VALIDATION` or `PAYLOAD_TOO_LARGE` |
| Quota | `QUOTA_EXCEEDED` (`CONFLICT` or `413`) |
| Cannot read | `NOT_FOUND` |
| Magic-byte mismatch after PUT | `VALIDATION` (status `rejected`) |

## Links

- Storage: [../40-Technical-specifications/04-Image-storage.md](../40-Technical-specifications/04-Image-storage.md)
- ACL: [../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md)
- Activity (upload): [../60-UML-diagrams/02-Activity.md](../60-UML-diagrams/02-Activity.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
