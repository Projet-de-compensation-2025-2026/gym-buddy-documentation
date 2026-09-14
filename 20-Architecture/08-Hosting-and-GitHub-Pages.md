# Hosting

| Surface | Location |
| --- | --- |
| Member application | https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/ |
| Documentation | https://projet-de-compensation-2025-2026.github.io/gym-buddy-documentation/ |
| API | https://vps-c39cdf03.vps.ovh.net/api/v1 |

GitHub Pages serves static assets. Caddy terminates TLS on the VPS and proxies API traffic to the loopback-bound application container. PostgreSQL, Redis and SeaweedFS share the private `gym-buddy-data` Docker network. The API image is deployed by `deploy/replace.sh`; data containers are managed separately by `deploy/compose.yaml`.

Browser media requires a public HTTPS endpoint for signed object URLs. The deployed configuration exposes only the existing bucket's object paths through Caddy to loopback SeaweedFS, preserving the signed host and path. It does not expose the console or grant anonymous bucket access. Signed upload/download browser checks are recorded in the release-verification page.

Use the service [VPS runbook](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service/blob/develop/docs/vps-data-plane.md) for operational commands, backups and rollback. Never put credentials in this documentation.

The 1.2.0 deployment uses a fresh PostgreSQL 18 ICU volume restored from a protected logical backup. The original database and object-store volumes are retained. The installed Compose file explicitly names the restored external volumes and verified runtime images; an ordinary application replacement must preserve that mapping.
