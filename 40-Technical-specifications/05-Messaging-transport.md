# Messaging transport

HTTP endpoints create conversations, persist messages, list history and update read state. The WebSocket gateway publishes message and unread-count events; Redis pub/sub distributes notifications. Conversation membership and blocks are checked on the server.

The Angular chat opens `/ws` with its access token and also polls messages every ten seconds as a fallback. A message arriving without navigation demonstrates delivery, but does not by itself identify whether WebSocket or polling delivered it. Do not log handshake query tokens.

Text and media messages use the same conversation authorization. Image and audio bytes use the [private media flow](04-Image-storage.md). An inaccessible conversation must show an error without its contents or an active composer.

Verify with separate browser sessions: create a conversation, send both ways, receive without reloading, observe unread/read state, delete an own message and deny an unrelated account. Media upload and playback need separate live checks.
