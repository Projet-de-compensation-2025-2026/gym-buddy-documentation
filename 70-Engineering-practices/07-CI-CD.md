# CI/CD

Each repository owns its GitHub Actions workflows. CI validates the contract or application build and its relevant tests. Service integration tests need Docker; a skipped container test is not a passing test. UI checks include generated-client consistency, production builds and component tests. Documentation validates links and builds the Pages site.

Release workflows create a versioned release commit and tag. Deploy workflows must check out the requested tag explicitly. For the service, the POM version must match the requested stable SemVer; image labels record the source revision and application version.

GitHub Pages hosts static sites. The API workflow builds/publishes the Docker image and invokes the service deployment script on the VPS. Preserve external secrets and named database/object volumes. Verify readiness, image provenance and key browser journeys after deployment, and retain the previous image for rollback.

Do not equate local candidate tests with deployed behavior. Record both in [release verification](../80-Testing/06-Release-verification.md).
