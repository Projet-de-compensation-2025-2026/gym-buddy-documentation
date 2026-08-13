# Instant messaging

| Field | Value |
| --- | --- |
| Status | Draft |
| Related | [../40-Technical-specifications/05-Messaging-transport.md](../40-Technical-specifications/05-Messaging-transport.md), [12-Media-and-files.md](12-Media-and-files.md) |

Private conversations support **text**, **images**, and **audio recordings**. There is no public/group chat at MVP (an event thread is an improvement).

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

## Acceptance

- Given A and B are not friends, when A POSTs a message to B, then `FORBIDDEN`.
- Given an image message, when C (stranger) guesses the media URL, then they receive `FORBIDDEN` or an expired signed URL ([../40-Technical-specifications/03-Authorization-and-file-access.md](../40-Technical-specifications/03-Authorization-and-file-access.md)).
- Given the socket is down, when A sends text, then the message is still persisted and B sees it after refresh.

Group chats, read receipts beyond unread count, and E2E encryption are listed as improvements.
