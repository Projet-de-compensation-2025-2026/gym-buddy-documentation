# Messaging transport

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../30-Functional-specifications/10-Instant-messaging.md](../30-Functional-specifications/10-Instant-messaging.md) |

Canonical paths: [09-Target-HTTP-surface.md](09-Target-HTTP-surface.md) (`/conversations`, `/conversations/{id}/messages`, `/messages/{id}`, `/ws`).

## Persistence first

`POST /api/v1/conversations/{id}/messages` writes the row, then publishes to the gateway. A dropped socket never loses a message.

## WebSocket

- URL: `/api/v1/ws` with `Authorization: Bearer` (or one-time ticket from `POST /api/v1/auth/ws-ticket` if cookie-only clients need it)
- Events:
  - `message.created`
  - `message.deleted`
  - `conversation.updated`
- Rooms: `user:{id}` (server joins after auth). Do not trust client-sent room names.

## HTTP fallback

`GET /api/v1/conversations/{id}/messages?before=` remains the source of truth. The frontend polls every 10 s if the socket is closed.

## Today (v1.1.1)

From GitHub Pages the WebSocket at `/api/v1/ws` does not stay up (browser close **1006**). `GET /api/v1/ws` without Upgrade is **426**. **HTTP fetch is the MVP** for the Pages origin: friends open a conversation with `POST /conversations`, then list and send messages over HTTP. Do not claim live WS from github.io. Ticket **#125**.

## Media messages

The message row references `media_id`. The payload sent on the socket contains metadata + a signed URL minted **for that recipient** at fan-out time (or the client fetches `/media/:id/url` itself — simpler, preferred).

## Presence

Optional `presence` map in Redis with 30 s TTL. Not required for the defense.

## Scale note

One node + Redis pub/sub is enough. Sticky sessions are unnecessary if every node subscribes to Redis.
