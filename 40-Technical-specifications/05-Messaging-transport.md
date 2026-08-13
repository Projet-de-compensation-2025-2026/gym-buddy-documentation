# Messaging transport

| Field | Value |
| --- | --- |
| Status | Proposed |
| Related | [../30-Functional-specifications/10-Instant-messaging.md](../30-Functional-specifications/10-Instant-messaging.md) |

## Persistence first

`POST /conversations/:id/messages` writes the row, then publishes to the gateway. A dropped socket never loses a message.

## WebSocket

- URL: `/ws` with `Authorization: Bearer` (or one-time ticket from `POST /auth/ws-ticket`)
- Events:
  - `message.created`
  - `message.deleted`
  - `conversation.updated`
- Rooms: `user:{id}` (server joins after auth). Do not trust client-sent room names.

## HTTP fallback

`GET /conversations/:id/messages?before=` remains the source of truth. The frontend polls every 10 s if the socket is closed.

## Media messages

The message row references `media_id`. The payload sent on the socket contains metadata + a signed URL minted **for that recipient** at fan-out time (or the client fetches `/media/:id/url` itself — simpler, preferred).

## Presence

Optional `presence` map in Redis with 30 s TTL. Not required for the defense.

## Scale note

One node + Redis pub/sub is enough. Sticky sessions are unnecessary if every node subscribes to Redis.
