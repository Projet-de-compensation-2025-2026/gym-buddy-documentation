# Integration tests

| Field | Value |
| --- | --- |
| Status | Approved |

## Scope

One real API process, real PostgreSQL, real or testcontainer MinIO, Redis if refresh denylist is exercised.

## Contracts to lock

| Contract | Assert |
| --- | --- |
| `POST /auth/login` | 200 + cookie; bad password 401 generic |
| `GET /profiles/:handle` as stranger vs friend | stub vs full |
| `POST /friendships` duplicate | 409 |
| `GET /feed` | only friends’ items |
| `POST /events/:id/applications` as stranger on friends-only | 404/403 |
| `POST /applications/:id/accept` twice to overflow | second 409 |
| `POST /media` then unsigned GET of key | denied |
| `GET /search/people` | private stranger absent |
| `POST /admin/users/:id/role` as moderator | 403 |
| Production guard on fixtures | 403 / disabled |

## Data

Each test builds the rows it needs via factories (tens, not thousands). A `beforeEach` transaction rollback keeps tests isolated.

## Time

Prefer < 5 minutes on CI. If MinIO is unavailable, skip media cases with an explicit `describe.skip` rather than a false green.
