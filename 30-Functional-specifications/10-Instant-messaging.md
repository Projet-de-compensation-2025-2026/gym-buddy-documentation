# Instant messaging

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../40-Technical-specifications/05-Messaging-transport.md](../40-Technical-specifications/05-Messaging-transport.md), [12-Media-and-files.md](12-Media-and-files.md) |

## Intent

Private conversations support **text**, **images**, and **audio recordings**. There is no public/group chat at MVP (an event thread is an improvement).

## Actors

Two accepted friends; staff may inspect in back-office (no E2E).

## Requirements

| ID | Requirement |
| --- | --- |
| FS-MSG-01 | Two members who are **friends** can open a direct conversation (created on first message). |
| FS-MSG-02 | Non-friends cannot message each other (`FORBIDDEN`). |
| FS-MSG-03 | Text messages: 1–4000 characters. |
| FS-MSG-04 | Image messages: one image, types and size as in FS-MED. |
| FS-MSG-05 | Audio messages: one clip, max 120 seconds, `audio/webm` or `audio/mpeg`. |
| FS-MSG-06 | Only the two participants can list or fetch messages and media. |
| FS-MSG-07 | Messages are delivered over WebSocket when both are connected; otherwise they appear on next HTTP fetch. |
| FS-MSG-08 | Sender can delete their message for everyone within 10 minutes (tombstone). |
| FS-MSG-09 | Inbox lists conversations by last message time, with unread count. |
| FS-MSG-10 | Blocking ends the ability to send; history remains visible to each side. |

## Business rules

- Persistence first: HTTP write, then fan-out. A dropped socket never loses a message ([../40-Technical-specifications/05-Messaging-transport.md](../40-Technical-specifications/05-Messaging-transport.md)).
- One conversation per unordered friend pair.
- Presence (“Online” on mockup 14) is optional Redis TTL; not required for acceptance.
- Read receipts beyond unread count are out of scope. Unread increments until the viewer `GET`s the thread (or sends a `read` event).
- Composer icons: image, audio, text. No video, no file-other.

## Target HTTP

| Method | Path | IDs |
| --- | --- | --- |
| `GET` | `/api/v1/conversations` | FS-MSG-09 |
| `POST` | `/api/v1/conversations` | FS-MSG-01 |
| `GET` | `/api/v1/conversations/{id}/messages` | FS-MSG-06 |
| `POST` | `/api/v1/conversations/{id}/messages` | FS-MSG-03..05 |
| `DELETE` | `/api/v1/messages/{id}` | FS-MSG-08 |
| `GET` | `/api/v1/ws` | FS-MSG-07 |

Media attach uses [12-Media-and-files.md](12-Media-and-files.md).

## UI

| Route | Mockup |
| --- | --- |
| `/messages` | [13-inbox.jpg](../20-Architecture/mockups/13-inbox.jpg) — thread list, last preview, unread badge, compose. |
| `/messages/:id` | [14-chat.jpg](../20-Architecture/mockups/14-chat.jpg) — text bubbles, image, audio player, composer (image / mic / text). |

## Acceptance

- Given A and B are not friends, when A POSTs a message to B, then `FORBIDDEN`.
- Given an image message, when C (stranger) guesses the media URL, then they receive `FORBIDDEN` or an expired signed URL ([../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md)).
- Given the socket is down, when A sends text, then the message is still persisted and B sees it after refresh.
- Given A blocked B, when B POSTs to the conversation, then `FORBIDDEN`; history GET still works for both.

## Errors

| Situation | Code |
| --- | --- |
| Not friends | `FORBIDDEN` |
| Empty text / oversize | `VALIDATION` |
| Stranger conversation | `NOT_FOUND` |
| Delete after 10 minutes | `FORBIDDEN` |

## Links

- Transport: [../40-Technical-specifications/05-Messaging-transport.md](../40-Technical-specifications/05-Messaging-transport.md)
- Sequence (image): [../60-UML-diagrams/03-Sequence.md](../60-UML-diagrams/03-Sequence.md)
- HTTP inventory: [../40-Technical-specifications/09-Target-HTTP-surface.md](../40-Technical-specifications/09-Target-HTTP-surface.md)
