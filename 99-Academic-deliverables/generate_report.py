"""Assemble Gym-Buddies-report.pdf from the wiki (ticket #71)."""

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
# Parent develop SHA plus this #71 live-screenshot PR (not a mockup gallery).
DOC_SHA = "ab679f9+#71"
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
    ("01-register-login.png", "Figure 1. After register on Pages v1.1.0 the SPA lands on login with “Account created. Sign in to continue.”"),
    ("02-public-profile.png", "Figure 2. A public profile shows display name, bio, sports, city, and experience (FS-PROF)."),
    ("03-private-profile-stranger.png", "Figure 3. A stranger on a private profile sees only a stub and Request Friend (FS-PROF-04)."),
    ("04-friend-request-pending.png", "Figure 4a. Outbound friend request stays pending until the addressee accepts (FS-FRND)."),
    ("04-friend-request.png", "Figure 4b. After accept, Blake appears under My Friends."),
    ("05-friends-feed-post-repost.png", "Figure 5. Friends feed shows Blake’s post and “Alex Live reposted” (FS-FEED)."),
    ("07-comment-thread.png", "Figure 6–7. The same post has a like plus a three-level comment thread (FS-POST, FS-CMT)."),
    ("08-friends-only-event.png", "Figure 8. Friends-only evening lift: place, 90 minutes, capacity 1 (FS-EVT)."),
    ("09-event-applications-pending.png", "Figure 9a. Organizer queue with Blake pending (matching score 0.30)."),
    ("09-event-applications.png", "Figure 9b. After the last seat is accepted, a later friend sees Full / 1 (FS-EVT-07)."),
    ("10-recurring-event-occurrences.png", "Figure 10. WEEKLY run club materialises the next 90 days of occurrences (FS-EVT-03)."),
    ("11-advanced-search.png", "Figure 11. People search with query, city, sport, and experience filters (FS-SRCH)."),
    ("12-suggestions-why.png", "Figure 12. Suggestions empty on prod: no 3 000-user fixtures and recompute is async (FS-SUGG-03)."),
    ("13-chat-text-image-audio.png", "Figure 13. DM text delivered; image/audio fail because live object storage is not configured (FS-MSG)."),
    ("14-denied-media.png", "Figure 14. A stranger opening a friends-only post sees “post not found” — no existence leak (FS-MED-06)."),
    ("17-architecture.png", "Figure 17. Modular monolith from the wiki Mermaid in 20-Architecture/01-Software-architecture.md."),
    ("18-data-model.png", "Figure 18. Core ER from the wiki Mermaid in 20-Architecture/06-Data-model.md."),
    ("19-https-health.png", "Figure 19. Operator-network probe: GET /api/v1/healthz and /readyz return HTTP 200."),
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
            "gym-buddy-documentation (commit <b>%s</b>). It is not a second specification. "
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
            "The brief does not require wiki pages to stay Draft until that meeting. Implementation "
            "followed wiki, then the OpenAPI tag, then generate, then implement.",
            "body",
        ),
        P("Repositories", "h2"),
        grid(
            [
                ["Repository", "Role", "URL"],
                [
                    "gym-buddy-documentation",
                    "Wiki, tickets, Gym Buddy Project",
                    "github.com/.../gym-buddy-documentation",
                ],
                [
                    "gym-buddy-openapi",
                    "OpenAPI 3.1 $ref tree (HTTP source of truth)",
                    "github.com/.../gym-buddy-openapi",
                ],
                [
                    "gym-buddy-service",
                    "Java 25 LTS / Spring Boot API",
                    "github.com/.../gym-buddy-service",
                ],
                [
                    "gym-buddy-ui",
                    "Angular 22 member app + /admin",
                    "github.com/.../gym-buddy-ui",
                ],
            ],
            [38 * mm, 52 * mm, w - 90 * mm],
        ),
        P("2. Problem and users", "h1"),
        P(
            "Athletes who want a training partner have no product that combines a friends graph, "
            "public/private profiles, capacity-limited sessions, and explainable “why this person” "
            "suggestions. Gym Buddies is that product for members; staff get a separate back-office "
            "bundle. Native mobile, payments, and wearables are out of scope.",
            "body",
        ),
        P("3. Functional overview", "h1"),
        grid(
            [
                ["Area", "FS prefix", "On develop"],
                ["Accounts / JWT", "FS-ACCT", "Register, login, refresh, logout, password, close"],
                ["Profiles", "FS-PROF", "Public / private, stub for strangers"],
                ["Friends", "FS-FRND", "Request, accept, block"],
                ["Feed / posts / comments", "FS-FEED / POST / CMT", "Friends feed, likes, depth 4"],
                ["Events", "FS-EVT", "Instant / WEEKLY, apply, transactional capacity"],
                ["Search / suggestions", "FS-SRCH / SUGG", "People+events; FoF generate-and-score"],
                ["Messaging / media", "FS-MSG / MED", "Text, image, audio; MinIO signed URLs"],
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
            "Runtime: PostgreSQL 18 (system of record), Redis (refresh denylist, suggestion cache), "
            "MinIO (images and audio — never an API /uploads directory). The UI is static on GitHub "
            "Pages; the API is a Docker image on an OVH VPS behind Caddy, bound to 127.0.0.1:8080.",
            "body",
        ),
        P(
            "Core entities: User, Profile, Friendship, Post, Comment, Event (plus occurrences and "
            "applications), Media, Conversation/Message, AuditEvent. Identifiers are UUIDs. "
            "Timestamps are UTC. Soft-delete keeps nested threads and moderation consistent. "
            "The wiki ER diagram is the authoritative picture (20-Architecture/06-Data-model.md).",
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
            "FoF is O(d^2) per user; nightly all-users is fine at 3 000 users. Collaborative filtering "
            "was rejected: no implicit-feedback volume, and it cannot explain why.",
            "body",
        ),
        P("5.2 Filtered search", "h2"),
        P(
            "People and events are two indexes with cursor pagination. Filters include sports, city, "
            "radius, remaining capacity, and friend-state. Private strangers never appear. "
            "Default sort is relevance then recency. PostgreSQL is enough at this scale; "
            "Elasticsearch was rejected for MVP.",
            "body",
        ),
        P("5.3 User matching", "h2"),
        P(
            "Weekly opt-in greedy assignment with a unique pair, no block edges, and a draft instant "
            "event of capacity 1 (visibility friends). Greedy is a 1/2-approximation; the wiki records "
            "that we do not show an empirical gap versus exact. Event accept order (FS-EVT-13) reuses "
            "the same matching score as a suggested queue, not as a capacity override.",
            "body",
        ),
        P("6. Security", "h1"),
        P(
            "Access JWT is HS256 in JSON. Refresh is a cookie (HttpOnly, Secure, SameSite=None, "
            "Partitioned, path /api/v1/auth) rotated on use and denylisted in Redis on logout. "
            "SameSite=Lax was the v1.0.0 session-drop from github.io; live 1.1.0 uses None+Partitioned "
            "so Chromium stores the cookie in the Pages partition. Passwords are Argon2id, never logged. "
            "Missing ACL returns NOT_FOUND (no existence leak) unless a spec names FORBIDDEN. "
            "File downloads are 60-second signed GETs minted only after canRead — on this VPS "
            "POST /media currently returns “media is not configured”, so that path is honest, not claimed. "
            "Member calls to /admin/* return NOT_FOUND. Staff JavaScript is a separate Angular bundle.",
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
            "Gitflow: feature branches from develop, PRs to develop, Conventional Commits with the "
            "documentation ticket in the scope (feat(#59): …) and Refs: …/gym-buddy-documentation#N. "
            "GitHub Actions: format, tests, HTTP smoke on every PR. Release squash-merges develop "
            "onto main, tags vX.Y.Z, and deploys. Live GitHub Pages is <b>v1.1.0</b> "
            "(known member and admin routes HTTP 200). The SPA talks to "
            "https://vps-c39cdf03.vps.ovh.net/api/v1. Operator-network healthz/readyz are 200.",
            "body",
        ),
        P("8. Tests and fixtures", "h1"),
        P(
            "Backend unit tests name FS IDs (fsEvt07_concurrentLastSeatAcceptsExactlyOne, "
            "fsProf04_strangerOnPrivateProfileSeesStub, …). Integration tests use Testcontainers. "
            "CI smoke hits GET /api/v1/healthz. Fixtures: Datafaker, seed 20260813, default 3 000 "
            "users / 12 000 accepted friendships / 15 000 posts. CI uses tens of rows "
            "(FixtureMagnitude.tiny()). Spring profile prod cannot reset. About ten stock MinIO "
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
            "After v1.1.0, the main gaps are honest: suggestion matching is greedy, not exact; "
            "DMs are not E2E encrypted; search on messy city strings has no geocoder; GitHub Pages "
            "cannot host Java. Live Pages login from this operator PC <b>does</b> work "
            "(SameSite=None; Partitioned). Prod has no demo.admin (#78 not SSH-run) and no object "
            "storage, so admin shots 15–16 and signed media URLs are not claimed. Suggestions for "
            "three live users were empty (no 3 000-user fixtures). With two weeks less I would drop "
            "weekly matching, audio DMs, and recurrence beyond WEEKLY+UNTIL.",
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
        P("Live screenshots (Pages v1.1.0, 2026-08-31)", "h2"),
        P(
            "Figures below are captures from the running Angular UI, not wiki mockup JPGs. "
            "demo.alex passwords are not in git; three fresh members were registered and friended. "
            "Admin 15–16 are omitted: demo.admin is missing on prod (ticket #78).",
            "body",
        ),
    ]
    for name, caption in FIGURES:
        out.append(figure(name, caption))
    out += [
        grid(
            [
                ["#", "Shot", "FS"],
                ["1", "Register / login", "FS-ACCT"],
                ["2–3", "Public profile; private stub", "FS-PROF"],
                ["4", "Friend request", "FS-FRND"],
                ["5–7", "Feed, likes, nested comments", "FS-FEED / POST / CMT"],
                ["8–10", "Event create, accept, recurrence", "FS-EVT"],
                ["11–12", "Search; suggestion why (empty on prod)", "FS-SRCH / SUGG"],
                ["13–14", "Chat text; stranger NOT_FOUND", "FS-MSG / MED"],
                ["15–16", "Admin — blocked, no staff login", "FS-ADM"],
            ],
            [18 * mm, w - 42 * mm, 24 * mm],
        ),
        P(
            "UML (use case, activity, sequence, class) is in 60-UML-diagrams. Selected HTTP surface "
            "is 40-Technical-specifications/09-Target-HTTP-surface.md. No cadrage minutes were invented.",
            "body",
        ),
        P(
            "Formalities: email maurras.togbe@isep.fr by 31 August 2026. Working language of the wiki "
            "is English; translate if the instructor requires French. Cite wiki commit %s." % DOC_SHA,
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
