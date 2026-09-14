# Authorization and file access

The API authorizes every signed download using the active account, media state and its parent resource. A private S3-compatible bucket supplies storage; its policy alone cannot express friendship or conversation access.

`MediaService.url` requires an active authenticated viewer. Missing and denied media both return `NOT_FOUND`. Its checks are ordered:

1. The media must be ready and not deleted. Hidden media is denied to ordinary members.
2. If the owner is missing or closed, only staff can read it.
3. Staff can inspect ready media for moderation. The owner can read their own ready media.
4. Other viewers need access to the attached post, event or conversation. An avatar requires a public profile or accepted friendship. Unsupported/unattached media is denied.

These rules are implemented in `MediaService.canRead` and `CompositeAttachedMediaAccess` with `PostAttachedMediaAccess`, `EventAttachedMediaAccess` and `MessageAttachedMediaAccess`. A signed URL remains a transferable capability until its 60-second expiry; later visibility changes do not revoke an already issued URL immediately.

## Upload and download

`POST /api/v1/media` accepts JSON `{kind, mime, bytes}` and reserves quota before returning a media ID and a 60-second signed PUT URL. The browser PUTs bytes directly to object storage. The scheduled processor verifies content, size and image/audio limits, creates sanitized immutable serving objects/variants and marks valid media ready. Parent creation/update attaches the media ID.

`GET /api/v1/media/{id}/url` returns a 60-second signed GET after authorization. There is no application proxy-stream or multipart-upload endpoint. [Image storage](04-Image-storage.md) describes processing limits and quota accounting.

## Lifecycle

The sweep retries pending ingestion. Unprocessed pending objects older than one hour and their rows are removed. Rejected uploads have their object tree deleted; their metadata supports rejection tracking. Completed upload keys receive a later cleanup pass to remove replayed bytes. Deleted media is denied immediately but its objects remain for a seven-day grace period and continue counting toward quota until physical purge. Processed serving keys differ from the mutable upload key.

TLS protects browser transport. The application does not implement end-to-end encryption or claim verified storage encryption at rest. Current deployment and migration checks are recorded in [release verification](../80-Testing/06-Release-verification.md).
