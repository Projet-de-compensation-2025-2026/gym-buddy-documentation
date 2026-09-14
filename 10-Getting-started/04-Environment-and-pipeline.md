# Environment and delivery

Use each repository's README for the exact build commands. The service requires Java 25 and Maven; the UI uses the Node/pnpm versions declared in its workspace. Docker is required for the local PostgreSQL, Redis and SeaweedFS stack and container integration tests.

| Configuration | Purpose |
| --- | --- |
| `DATABASE_URL`, database credentials | PostgreSQL connection |
| `REDIS_URL` | Refresh credentials and messaging |
| `JWT_ACCESS_SECRET` | JWT signing key |
| `S3_ENDPOINT` | Internal object-store endpoint |
| `S3_PUBLIC_ENDPOINT` | HTTPS endpoint used in browser signed URLs |
| `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_REGION` | Private S3-compatible storage |
| `SPRING_PROFILES_ACTIVE` | Runtime profile |

Local service configuration and Compose live in `gym-buddy-service`. VPS configuration is kept outside Git at `/etc/gym-buddy/vps.env`. PostgreSQL binds 127.0.0.1:5432 and SeaweedFS S3 binds 127.0.0.1:8333. Redis and storage administration ports remain unpublished. Keep named data volumes during application replacement.

Release workflows create semantic version tags. Deployment must check out that exact tag and verify the application version before building the image or site. Service images carry version and source-revision labels. A successful build is not proof of a successful deployment: check readiness and exercise the browser journeys afterward.

On an empty database, the first registration becomes administrator as specified by FS-ACCT-10. For an existing database, the staff bootstrap CLI is an explicit operator action with supplied strong credentials. Restrict initial deployment access until the intended administrator is created. Bulk fixtures belong in an isolated non-production database. Neither credentials nor private tokens, signed URLs or production data belong in Git, screenshots or logs.

See [CI/CD](../70-Engineering-practices/07-CI-CD.md), the service [operator runbook](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/vps-data-plane.md), and [release verification](../80-Testing/06-Release-verification.md).
