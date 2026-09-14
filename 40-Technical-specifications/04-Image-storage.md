# Images, audio and object storage

Media metadata and ownership live in PostgreSQL. Object bytes live in a private SeaweedFS bucket through the S3 API, both locally and on the VPS. No AWS-hosted bucket is assumed.

1. The authenticated API validates ownership, quota and the requested media kind, then creates an upload record and a short-lived signed PUT URL.
2. The browser uploads directly to object storage using the configured public HTTPS endpoint.
3. Completion validates the actual content. Images are decoded, stripped of metadata and processed into bounded variants; audio duration is checked.
4. Before issuing a short-lived signed GET URL, the API checks the media's owning resource and the caller's current access.

| Limit | Reviewed implementation |
| --- | --- |
| Signed URL lifetime | 60 seconds |
| Individual upload | 8 MiB |
| Owner quota | 1 GiB, including pending, ready and retained deleted objects plus variants |
| Image dimensions | At most 8,000 pixels per side and 64 megapixels |
| Image variants | Bounded 320 / 960 pixel variants |
| Audio duration | 120 seconds |
| Processing temporary space | Bounded `gb-media` temporary directory; 256 MiB cap |

The service stores processed images under an immutable serving key distinct from the upload key, preventing later replacement through an unexpired upload URL. Rejected and stale uploads are cleaned up; deleted media has a seven-day grace period before cleanup and retains its quota charge until physical purge. Integration tests cover these protections; browser evidence is recorded separately.

The VPS internal endpoint is `http://storage:8333`; that hostname is not browser reachable. `S3_PUBLIC_ENDPOINT` must be the externally reachable HTTPS origin. Caddy must preserve the signed host and object path and allow the Pages origin's PUT/GET/HEAD requests. Keep the bucket private and its administration ports unpublished.

See [authorization](03-Authorization-and-file-access.md), [media requirements](../30-Functional-specifications/12-Media-and-files.md) and [release verification](../80-Testing/06-Release-verification.md).
