# Class diagram

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) |

Domain types (not ORM annotations). Align fields with the data model when either changes.

```mermaid
classDiagram
  class User {
    +UUID id
    +String email
    +String handle
    +Role role
    +Status status
    +verifyPassword(raw)
  }

  class Profile {
    +Visibility visibility
    +String[] sports
    +Level experience
    +String city
    +Float lat
    +Float lng
    +Window[] preferredWindows
    +isVisibleTo(viewer) bool
  }

  class Friendship {
    +User requester
    +User addressee
    +FriendStatus status
    +accept()
    +block()
  }

  class Post {
    +String body
    +Visibility visibility
    +like(user)
    +repost(user)
  }

  class Comment {
    +Comment parent
    +int depth
    +reply(user, body) Comment
  }

  class Event {
    +String activity
    +Date startsAt
    +int durationMin
    +int capacity
    +RRule recurrence
    +Visibility visibility
    +remainingSeats() int
  }

  class EventApplication {
    +AppStatus status
    +accept()
    +decline()
  }

  class Conversation {
    +send(sender, payload) Message
  }

  class Message {
    +MsgType type
    +String body
    +Media media
  }

  class Media {
    +String bucketKey
    +MediaKind kind
    +int bytes
    +canRead(user) bool
  }

  class SuggestionEngine {
    +suggest(user, k) Candidate[]
  }

  class MatchingEngine {
    +rankForEvent(event, users) Candidate[]
    +weeklyPairs(users) Pair[]
  }

  class SuggestionDismissal {
    +UUID viewerId
    +UUID candidateId
    +Date until
  }

  User "1" --> "1" Profile
  User "1" --> "*" Friendship
  User "1" --> "*" Post
  Post "1" --> "*" Comment
  Comment "0..1" --> "*" Comment
  User "1" --> "*" Event : organizes
  Event "1" --> "*" EventApplication
  User "1" --> "*" EventApplication
  User "*" --> "*" Conversation
  Conversation "1" --> "*" Message
  User "1" --> "*" Media
  SuggestionEngine ..> User
  MatchingEngine ..> Event
  MatchingEngine ..> User
  User "1" --> "*" SuggestionDismissal
```

Enums: `Role`, `Status`, `Visibility`, `FriendStatus`, `AppStatus`, `MsgType`, `MediaKind`, `Level`.
