# OpenAPI contract

The separately versioned [gym-buddy-openapi repository](https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi) owns the API schema. Its source entry point is `openapi/openapi.yaml` and referenced files.

The service generates Java interfaces and models; the UI generates TypeScript clients. Consumer manifests pin a specific published contract revision. Update both consumers and regenerate their outputs after a contract change. Generated runtime documentation is not a second source of truth.

A contract change must pass schema validation, generation and relevant consumer tests. Commit a consumer pin update separately from any history-only rewrite: changing an embedded revision changes the repository tree. Never substitute a guessed or unreachable commit.

See [versioning](../70-Engineering-practices/06-Versioning.md) and [CI/CD](../70-Engineering-practices/07-CI-CD.md).
