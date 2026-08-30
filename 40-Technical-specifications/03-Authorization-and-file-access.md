# Authorization and file access

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../30-Functional-specifications/12-Media-and-files.md](../30-Functional-specifications/12-Media-and-files.md), [04-Image-storage.md](04-Image-storage.md) |

The brief requires **security and controlled access for all files**.

## Object ACL is not enough

MinIO/S3 bucket policies are a backstop. **Product authorization** lives in the API because visibility depends on friendship, event membership, and conversation membership.

## Access algorithm

```
canRead(user, media):
  if media.status != ready: deny
  if user.role in {admin, moderator}: allow          # back-office only
  parent = loadParent(media)
  match parent.kind:
    avatar  → profile visible to user (FS-PROF)
    post    → user can view the post (FS-POST / FS-FEED)
    comment → (no media at MVP)
    message → user ∈ conversation.members
    event   → user can view the event (FS-EVT)
  else deny
```

Never leak existence: deny and missing both return `NOT_FOUND`.

## Two download modes

| Mode | Use | Rule |
| --- | --- | --- |
| Signed GET | Browsers (`<img src>`, audio) | Presigned URL, 60 s, GET only, content-type fixed |
| Proxy stream | When the bucket must stay private on a network that cannot hit MinIO | API re-runs `canRead` then streams |

Signed URLs are **capability tokens**. They can be forwarded; keep TTL short. Do not issue a URL until `canRead` is true.

## Upload

1. `POST /media` `{ kind, mime, bytes }` → quota check → `media` row `pending` + `{ uploadUrl, mediaId }`
2. Client PUT bytes to `uploadUrl` (also short-lived)
3. Worker (or hook) verifies magic bytes, size, duration; writes variants; sets `ready`
4. Client attaches `mediaId` to post/message/profile

Orphan `pending` rows older than 1 h are deleted.

## Encryption

TLS in transit. Bucket encryption at rest if the provider offers it. No application-level E2E for files at MVP (called out in critical analysis).
