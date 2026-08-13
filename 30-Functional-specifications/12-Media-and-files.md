# Media and files

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../40-Technical-specifications/04-Image-storage.md](../40-Technical-specifications/04-Image-storage.md), [../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md) |

Images (and chat audio) must **not** pile up on the API host disk, and **every file** has controlled access.

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

## Acceptance

- Filling the local API disk with 1 000 avatars is impossible: bytes land in MinIO.
- Given a friends-only post image, when a stranger requests a signed URL, then `NOT_FOUND`.
- Given a valid participant, when they request a URL, then GET on that URL succeeds until expiry.

Technical design: [../40-Technical-specifications/04-Image-storage.md](../40-Technical-specifications/04-Image-storage.md).
