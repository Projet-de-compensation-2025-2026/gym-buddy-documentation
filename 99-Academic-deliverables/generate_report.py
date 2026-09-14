"""Assemble the academic report from documented implementation and dated evidence."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.utils import ImageReader

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = str(HERE / "Gym-Buddies-report.pdf")
SHOTS = HERE / "screenshots"
# Versions verified on the deployed website.
DOC_SHA = "1.2.0, 2026-09-14"
TEAL = colors.HexColor("#00535B")
INK = colors.HexColor("#141B2B")
HAIR = colors.HexColor("#BEC8CA")
MUTED = colors.HexColor("#3E494A")
SURFACE = colors.HexColor("#F9F9FF")


def styles():
    base = getSampleStyleSheet()
    s = {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=22,
            leading=26,
            textColor=INK,
            spaceAfter=8,
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            textColor=TEAL,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=12,
            leading=15,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            spaceAfter=10,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            textColor=MUTED,
            spaceAfter=4,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            leading=11,
            textColor=INK,
        ),
        "cell_h": ParagraphStyle(
            "cell_h",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=8,
            leading=11,
            textColor=colors.white,
        ),
    }
    return s


S = styles()

FIGURES = [
    ('release-1.2.0/release-profile-avatar.png', 'Figure 1. Saved profile avatar, rendered on the released member application.'),
    ('release-1.2.0/release-image-post.png', 'Figure 2. A synthetic member created an image post; its detail renders the processed image.'),
    ('release-1.2.0/release-event-cover.png', 'Figure 3. Public event with uploaded cover, title, location and capacity.'),
    ('release-1.2.0/release-weekly-occurrence-isolation.png', 'Figure 4. Applications and cancellation are isolated by weekly occurrence.'),
    ('release-1.2.0/released-chat-media-desktop.png', 'Figure 5. Image delivery without reload and audio playback between two synthetic friends.'),
    ('release-1.2.0/released-admin-users.png', 'Figure 6. Released staff user list filtered to the synthetic member accounts.'),
    ('release-1.2.0/released-admin-audit.png', 'Figure 7. Audit records for synthetic moderation actions.'),
    ('release-1.2.0/released-admin-fixtures-disabled.png', 'Figure 8. Fixture operations are explicitly disabled in production.'),
]


def P(text, style="body"):
    return Paragraph(text, S[style])


def figure(filename, caption, max_h=88 * mm):
    path = SHOTS / filename
    if not path.is_file():
        return [P("[missing %s]" % filename, "caption")]
    src = ImageReader(str(path))
    iw, ih = src.getSize()
    max_w = A4[0] - 36 * mm
    w, h = max_w, max_w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih
    img = Image(str(path), width=w, height=h)
    img.hAlign = "CENTER"
    return KeepTogether([img, P(caption, "caption"), Spacer(1, 4)])


def grid(rows, col_widths):
    data = []
    for i, row in enumerate(rows):
        style = "cell_h" if i == 0 else "cell"
        data.append([P(c, style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL),
                ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
                ("GRID", (0, 0), (-1, -1), 0.4, HAIR),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(18 * mm, A4[1] - 5.5 * mm, "Gym Buddies — ISEP compensation 2025/2026")
    canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 5.5 * mm, f"wiki {DOC_SHA}")
    canvas.setFillColor(MUTED)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(18 * mm, 12 * mm, "Joaquim Kéloglanian")
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def story():
    w = A4[0] - 36 * mm
    out = []
    out += [
        P("ISEP — Digital Engineering School", "meta"),
        P("Compensation project 2025/2026 · 5 ECTS · due 31 August 2026", "meta"),
        Spacer(1, 8),
        P("Gym Buddies", "cover_title"),
        P(
            "An individual web application that connects athletes so they can train together, "
            "motivate each other, and find a gym buddy.",
            "caption",
        ),
        P("Joaquim Kéloglanian", "meta"),
        P(
            "This report <b>summarizes</b> the wiki in "
            "gym-buddy-documentation (<b>%s</b>). It is not a second specification. "
            "Functional and technical rules live in that repository." % DOC_SHA,
            "body",
        ),
        P("1. Introduction and academic framing", "h1"),
        P(
            "The assignment covers Software Engineering, Web Technologies, and Algorithms "
            "and Advanced Programming. Work is individual. Defense is 20 minutes plus 30 minutes "
            "of questions. The instructor account maurras.togbe@isep.fr must be a collaborator "
            "on every private repository.",
            "body",
        ),
        P(
            "There was no instructor cadrage meeting (instructor on holiday, recorded 2026-08-19). "
            "The supplied assignment therefore remained the basis for required features and deliverables.",
            "body",
        ),
        P("Repositories", "h2"),
        grid(
            [
                ["Repository", "Role", "URL"],
                [
                    "gym-buddy-documentation",
                    "Wiki, tickets, Gym Buddy Project",
                    '<link href="https://github.com/Projet-de-compensation-2025-2026/gym-buddy-documentation">Open repository</link>',
                ],
                [
                    "gym-buddy-openapi",
                    "OpenAPI 3.1 $ref tree (HTTP source of truth)",
                    '<link href="https://github.com/Projet-de-compensation-2025-2026/gym-buddy-openapi">Open repository</link>',
                ],
                [
                    "gym-buddy-service",
                    "Java 25 LTS / Spring Boot API",
                    '<link href="https://github.com/Projet-de-compensation-2025-2026/gym-buddy-service">Open repository</link>',
                ],
                [
                    "gym-buddy-ui",
                    "Angular 22 member app + /admin",
                    '<link href="https://github.com/Projet-de-compensation-2025-2026/gym-buddy-ui">Open repository</link>',
                ],
            ],
            [38 * mm, 52 * mm, w - 90 * mm],
        ),
        P("2. Problem and users", "h1"),
        P(
            "Gym Buddies helps athletes find a training partner by combining a friends graph, "
            "public/private profiles, capacity-limited sessions, and explainable “why this person” "
            "suggestions. Members use the social application; staff get a separate back-office "
            "bundle. Native mobile, payments, and wearables are out of scope.",
            "body",
        ),
        P("3. Functional overview", "h1"),
        grid(
            [
                ["Area", "FS prefix", "Required behavior"],
                ["Accounts / JWT", "FS-ACCT", "Register, login, refresh, logout, password, close"],
                ["Profiles", "FS-PROF", "Public / private, stub for strangers"],
                ["Friends", "FS-FRND", "Request, accept, block"],
                ["Feed / posts / comments", "FS-FEED / POST / CMT", "Friends feed, likes, depth 4"],
                ["Events", "FS-EVT", "Instant / WEEKLY, apply, transactional capacity"],
                ["Search / suggestions", "FS-SRCH / SUGG", "People+events; FoF generate-and-score"],
                ["Messaging / media", "FS-MSG / MED", "Text, image, audio; SeaweedFS signed URLs"],
                ["Admin / fixtures", "FS-ADM", "Roles, hide, audit; Datafaker seed 20260813"],
            ],
            [42 * mm, 32 * mm, w - 74 * mm],
        ),
        P(
            "Highlights for the defense: the friends news feed (FS-FEED), friends-only events with "
            "a last-seat CONFLICT (FS-EVT-07), and suggestion cards that print a primary reason "
            "(FS-SUGG-03).",
            "body",
        ),
        P("4. Architecture and data model", "h1"),
        P(
            "Gym Buddies is a <b>modular monolith</b> behind one HTTP API and a WebSocket gateway. "
            "Two Angular clients (member and /admin) share that API. Bounded contexts "
            "(auth, social, events, search, chat, media, admin) live in one deployable. "
            "Microservices were rejected: operational cost dwarfs the academic benefit for one student.",
            "body",
        ),
        P(
            "Runtime: PostgreSQL 18 (system of record), Redis (refresh credential state and messaging pub/sub), "
            "SeaweedFS (private images and audio, with bounded temporary processing space). The UI is static on GitHub "
            "Pages; the API is a Docker image on an OVH VPS behind Caddy, bound to 127.0.0.1:8080.",
            "body",
        ),
        P(
            "Core entities: User, Profile, Friendship, Post, Comment, Event (plus occurrences and "
            "applications), Media, Conversation/Message, AuditEvent. Identifiers are UUIDs. "
            "Timestamps are UTC. Soft-delete keeps nested threads and moderation consistent. "
            "The wiki ER diagram explains the logical model; service Flyway migrations define the physical schema.",
            "body",
        ),
        P("5. Algorithms", "h1"),
        P("5.1 Friend suggestions", "h2"),
        P(
            "Two-stage generate-and-score. Candidates (at most 200): friends of friends, same city "
            "and sport, co-participants in the last 90 days; minus self, friends, pending, blocked, "
            "dismissed, locked. Score S(u,v) = 0.35 m + 0.25 J + 0.15 G + 0.15 T + 0.10 E, with "
            "m = Adamic-Adar on mutual friends, J = Jaccard of sports, G = geo (D = 25 km), T = window "
            "overlap, E = experience closeness. The card primary reason is argmax of weight times feature. "
            "Scores are stored in PostgreSQL and refreshed nightly or on demand. The scorer sorts "
            "at most 200 candidates in O(C log C); graph queries add cost that must be measured. Collaborative filtering "
            "was rejected: no implicit-feedback volume, and it cannot explain why.",
            "body",
        ),
        P("5.2 Filtered search", "h2"),
        P(
            "People and events are two indexes with cursor pagination. Filters include sports, city, "
            "radius, remaining capacity, and friend-state. Private strangers never appear. "
            "The service loads catalog candidates from PostgreSQL, filters and ranks them in Java, "
            "then returns a stable page. This requires an O(N) scan and O(M log M) sort. "
            "PostgreSQL full-text indexes are a future improvement, not the current implementation.",
            "body",
        ),
        P("5.3 User matching", "h2"),
        P(
            "Weekly opt-in greedy assignment with a unique pair, no block edges, and a draft instant "
            "event of capacity 1 (private, with the peer invited) at the start of the overlapping window. Greedy is a 1/2-approximation; the wiki records "
            "that we do not show an empirical gap versus exact. Event accept order (FS-EVT-13) reuses "
            "the same matching score as a suggested queue, not as a capacity override.",
            "body",
        ),
        P("6. Security", "h1"),
        P(
            "Access JWT is HS256 with a 15-minute lifetime. Refresh credentials last 14 days in an "
            "HttpOnly, Secure, SameSite=None, Partitioned cookie at /api/v1/auth. Redis atomically "
            "consumes rotated credentials. Passwords use Argon2id. Services enforce ownership, "
            "membership, visibility and staff permissions. Media reads receive 60-second signed URLs "
            "only after authorization. SeaweedFS is deployed behind an HTTPS object gateway. Real browser "
            "checks passed image upload, avatar update, event cover and audio playback on both accounts. "
            "The first registration on an empty database becomes admin; an operator CLI can provision "
            "staff on an existing database. Initial access therefore needs operator control.",
            "body",
        ),
        P("7. Implementation notes", "h1"),
        P(
            "OpenAPI 3.1 in gym-buddy-openapi is the HTTP source of truth. The service generates "
            "Java models and API interfaces at build (controllers implement those interfaces; "
            "generated sources are not committed). The UI generates a TypeScript client with orval "
            "from node_modules/gym-buddy-openapi/openapi/openapi.yaml. Spring springdoc /v3/api-docs "
            "is never the published contract.",
            "body",
        ),
        P(
            "Focused branches and reviewed pull requests use one-line Conventional Commits. "
            "A verified issue may appear in the scope, for example feat(#59): add profile editing. "
            "Release tags use vMAJOR.MINOR.PATCH. Deployment must build the exact tagged source "
            "and record the image revision. The browser uses the HTTPS API at "
            "https://vps-c39cdf03.vps.ovh.net/api/v1. A tag or passing build alone does not establish "
            "that a repair is deployed.",
            "body",
        ),
        P("8. Tests and fixtures", "h1"),
        P(
            "Backend unit tests name FS IDs (fsEvt07_concurrentLastSeatAcceptsExactlyOne, "
            "fsProf04_strangerOnPrivateProfileSeesStub, …). Integration tests use Testcontainers. "
            "CI smoke hits GET /api/v1/healthz. Fixtures: Datafaker, seed 20260813, default 3 000 "
            "users / 12 000 requested friendships / 15 000 posts. CI verifies both small and 1 000-user "
            "datasets. The final backend CI passed 294 tests with no skipped integrations. Spring profile prod cannot reset. Ten stock object-storage "
            "objects are reused so the 5 000 media metadata rows do not fill the disk.",
            "body",
        ),
        P("9. Critical analysis", "h1"),
        P(
            "Strengths: a demoable goal; a modular monolith that still shows Software Engineering "
            "structure; two distinct algorithms (explainable scoring vs constrained assignment); "
            "object storage that answers the brief’s disk and ACL items; spec IDs that tests cite.",
            "body",
        ),
        P(
            "The September release was checked in separate member and staff browser sessions. Image/audio delivery, "
            "moderation, event acceptance and occurrence isolation passed. The database migration preserved "
            "23 tables with content, schema and sequence comparisons. Scanned API, PostgreSQL, Redis and "
            "SeaweedFS images had zero CRITICAL findings; Caddy retains lower-severity advisories. Search scans "
            "candidates in Java; recommendation latency and relevance need fixture-scale measurement. "
            "Weekly matching uses a greedy approximation, and recurrence supports a weekly subset. "
            "Audio messaging and recurring events are required by the brief and cannot be dropped "
            "while claiming full compliance. See the dated release verification page for remaining gaps.",
            "body",
        ),
        P("10. Conclusion", "h1"),
        P(
            "Software Engineering is evidenced by UML, Flyway, Gitflow, tickets on one board, and "
            "reviews against FS IDs. Web Technologies is evidenced by a versioned OpenAPI contract, "
            "JWT, WebSocket, Angular, and signed media. Algorithms is evidenced by FoF generate-and-score, "
            "filtered search, and weekly matching — implemented in Java, unit-tested, without a hidden SaaS.",
            "body",
        ),
        P("11. Appendix", "h1"),
        P("Released website evidence (version 1.2.0, 14 September 2026)", "h2"),
        P(
            "Figures below show the published member and staff applications using synthetic test accounts. "
            "Passwords and production configuration are not included. Historical August captures remain "
            "separately dated in the screenshot archive.",
            "body",
        ),
    ]
    for name, caption in FIGURES:
        out.append(figure(name, caption))
    out += [
        grid(
            [
                ["#", "Shot", "FS"],
                ["1–2", "Avatar and image publication", "FS-PROF / POST"],
                ["3–4", "Event cover and occurrence isolation", "FS-EVT"],
                ["5", "Image and audio conversation", "FS-MSG / MED"],
                ["6–8", "Staff users, audit and fixture guard", "FS-ADM"],
            ],
            [18 * mm, w - 42 * mm, 24 * mm],
        ),
        P(
            "UML (use case, activity, sequence, class) is in 60-UML-diagrams. Selected HTTP surface "
            "is 40-Technical-specifications/09-Target-HTTP-surface.md.",
            "body",
        ),
        P(
            "The brief specified delivery to maurras.togbe@isep.fr by 31 August 2026. Working language of the wiki "
            "is English; the defense deck and rehearsal guide are in French. Source review: %s." % DOC_SHA,
            "caption",
        ),
    ]
    return out


def main():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Gym Buddies — compensation report",
        author="Joaquim Kéloglanian",
    )
    doc.build(story(), onFirstPage=header_footer, onLaterPages=header_footer)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
