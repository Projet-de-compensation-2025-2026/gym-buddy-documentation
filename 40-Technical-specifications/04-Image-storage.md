# Image storage

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [03-Authorization-and-file-access.md](03-Authorization-and-file-access.md), [../10-Getting-started/04-Environment-and-pipeline.md](../10-Getting-started/04-Environment-and-pipeline.md) |

The brief: **avoid running out of local storage**.

## Decision

Store bytes in an **S3-compatible bucket** (MinIO in development). The API container’s disk holds only temp files during processing, capped and cleaned.

When `SPRING_PROFILES_ACTIVE=prod`, the API **must refuse to start** if `S3_ENDPOINT` / `S3_BUCKET` / credentials are missing or unreachable. Falling back to a local `uploads/` directory is forbidden.

## Layout

```
s3://gym-buddy/
  original/{userId}/{mediaId}
  variant/{userId}/{mediaId}/sm   # 320w webp
  variant/{userId}/{mediaId}/md   # 960w webp
```

Keys are unguessable UUIDs. Directory listing is disabled.

## Processing

A Java image worker (Thumbnailator / ImageIO) :

- Strip EXIF (GPS in gym selfies is a privacy bug)
- Re-encode (no stored bombs)
- Produce `sm` / `md`
- Reject dimensions > 8000 px or compression bombs (decompressed size cap)

Temp dir: `os.tmpdir()/gb-media` with a 256 MiB quota. Fail the job rather than fill the disk.

## Quotas

| Limit | Value |
| --- | --- |
| Per file | 8 MiB |
| Per user | 1 GiB (sum of `media.bytes` for non-deleted) |
| Per post | 4 images |
| Variants | Count toward quota |

When a post or account is deleted, objects are marked and a daily job hard-deletes after 7 days.

## Why not local disk

| Local `uploads/` | Object storage |
| --- | --- |
| Fills the VM; fixtures × images die | Dedicated volume / cloud bucket |
| Hard to share between API replicas | Shared by key |
| Accidental static-file hosting | No public list; signed GET only |

This is also the justification paragraph for the report.
