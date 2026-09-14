# Frontend

The `gym-buddy-ui` repository contains Angular member and staff applications. Both use the versioned OpenAPI package to generate their API clients. Feature components own their screen behavior; shared services handle authentication, requests and cross-screen state.

The member application covers profiles, feed, posts, comments, friendships, search, suggestions, events and private conversations. The staff application covers users, content, reports, media, audit records and fixture operations. Staff access is enforced by the API as well as navigation guards.

Production builds are static GitHub Pages assets. The configured API base points to the HTTPS VPS. Authentication uses an access token in memory and a credentialed refresh cookie. Chat combines a WebSocket connection with a ten-second HTTP polling fallback.

The [mockup index](mockups/README.md) defines visual references; [functional specifications](../30-Functional-specifications/README.md) define required behavior. Browser verification must cover desktop, narrow screens, empty/error states and two-account interactions. See [release verification](../80-Testing/06-Release-verification.md).
