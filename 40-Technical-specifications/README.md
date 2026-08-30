# 40 — Technical specifications

How the product is implemented. Functional pages describe *what*; these pages describe *how*, at a level an engineer can code against.

## Contents

| Document | Brief item |
| --- | --- |
| [01-API-conventions.md](01-API-conventions.md) | Shared HTTP, error, and pagination rules |
| [02-JWT-authentication.md](02-JWT-authentication.md) | JWT authentication |
| [03-Authorization-and-file-access.md](03-Authorization-and-file-access.md) | Security and controlled access for all files |
| [04-Image-storage.md](04-Image-storage.md) | Image management without filling local disks |
| [05-Messaging-transport.md](05-Messaging-transport.md) | Instant messaging transport (text, image, audio) |
| [06-Search-implementation.md](06-Search-implementation.md) | Implementing parameterized search |
| [07-Test-fixtures.md](07-Test-fixtures.md) | Creating thousands of test fixtures |
| [08-OpenAPI-contract.md](08-OpenAPI-contract.md) | Dedicated OpenAPI repository as the HTTP source of truth |
| [09-Target-HTTP-surface.md](09-Target-HTTP-surface.md) | Remaining `/api/v1` operations Kernel must add to the `$ref` tree |

Companion pages:

- Stack justification: [../20-Architecture/07-Technology-choices.md](../20-Architecture/07-Technology-choices.md)
- Data model: [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md)
- Test plan: [../80-Testing](../80-Testing/README.md)

## Next

[50-Algorithms](../50-Algorithms/README.md) · [Back to home](../README.md)
