# Versioning

Use Semantic Versioning `MAJOR.MINOR.PATCH` and Git tags `vMAJOR.MINOR.PATCH` in all four repositories. Breaking public behavior increments the major version; compatible features increment minor; compatible fixes increment patch. Build manifests use the same release version without the tag's `v` prefix.

A release is the combination of its tag, exact source commit, tested artifacts and deployed result. Tags and GitHub Release objects are separate; the presence of a tag does not imply release notes or successful deployment.

The OpenAPI contract and its consumers are versioned independently. Pin consumers to the exact published compatible contract revision and regenerate clients/interfaces. Do not claim a version is current from old documentation: inspect repository refs and deployed artifact provenance.

History-only cleanup must preserve every source tree. Embedded contract-pin changes are separate functional commits and require regeneration/testing. See [Git workflow](02-Git-workflow.md).
