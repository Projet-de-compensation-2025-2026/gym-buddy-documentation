# Class diagram

| Field | Value |
| --- | --- |
| Status | Approved |
| Related | [../20-Architecture/06-Data-model.md](../20-Architecture/06-Data-model.md) |

Conceptual view of the implemented records and services. Selected fields are simplified for readability; this is not an exhaustive Java API listing. Business operations live in services, rather than invented record methods.

```mermaid
classDiagram
  class User {
    +UUID id
    +String email
    +String handle
    +Role role
    +Status status
  }

  class Profile {
    +Visibility visibility
    +String[] sports
    +Level experience
    +String city
    +Float lat
    +Float lng
    +Window[] preferredWindows
  }

  class Friendship {
    +User requester
    +User addressee
    +FriendStatus status
  }

  class Post {
    +String body
    +Visibility visibility
  }

  class Comment {
    +Comment parent
    +int depth
  }

  class Event {
    +String activity
    +Date startsAt
    +int durationMin
    +int capacity
    +String recurrence
    +Visibility visibility
  }

  class EventOccurrence {
    +UUID id
    +UUID eventId
    +Instant startsAt
    +Instant cancelledAt
  }

  class EventApplication {
    +UUID occurrenceId
    +AppStatus status
  }

  class Conversation {
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
  }

  class SuggestionService {
  }

  class MatchingService {
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
  Event "1" --> "*" EventOccurrence
  EventOccurrence "1" --> "*" EventApplication
  User "1" --> "*" EventApplication
  User "*" --> "*" Conversation
  Conversation "1" --> "*" Message
  User "1" --> "*" Media
  SuggestionService ..> User
  MatchingService ..> Event
  MatchingService ..> User
  User "1" --> "*" SuggestionDismissal
```

Enums: `Role`, `Status`, `Visibility`, `FriendStatus`, `AppStatus`, `MsgType`, `MediaKind`, `Level`.
