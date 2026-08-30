const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Gym Buddies — ISEP compensation 2025/2026";
pres.author = "Joaquim Kéloglanian";

const BG = "F7F5F0";
const INK = "1A1A1A";
const MUTED = "7A7A7A";
const ACCENT = "00535B";
const HAIR = "D9D5CC";
const CARD = "FFFFFF";

const HEAD = "Georgia";
const BODY = "Calibri";

const W = 13.3;
const H = 7.5;
const ML = 0.8;
const MR = 0.8;
const MT = 0.6;

function addBase(slide, { pageNum, footer } = {}) {
  slide.background = { color: BG };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: ML,
    y: MT,
    w: 0.18,
    h: 0.18,
    fill: { color: ACCENT },
    line: { color: ACCENT, width: 0 },
  });
  if (pageNum) {
    slide.addText(String(pageNum).padStart(2, "0"), {
      x: W - 1.0,
      y: H - 0.5,
      w: 0.6,
      h: 0.3,
      fontFace: BODY,
      fontSize: 10,
      color: MUTED,
      align: "right",
      margin: 0,
    });
  }
  if (footer) {
    slide.addText(footer, {
      x: ML,
      y: H - 0.5,
      w: 10,
      h: 0.3,
      fontFace: BODY,
      fontSize: 10,
      color: MUTED,
      italic: true,
      margin: 0,
    });
  }
}

function addEyebrow(slide, text) {
  slide.addText(text.toUpperCase(), {
    x: ML + 0.35,
    y: MT - 0.06,
    w: 10,
    h: 0.3,
    fontFace: BODY,
    fontSize: 10,
    color: MUTED,
    charSpacing: 3,
    valign: "middle",
    margin: 0,
  });
}

{
  const s = pres.addSlide();
  s.background = { color: BG };
  s.addShape(pres.shapes.RECTANGLE, {
    x: ML,
    y: MT,
    w: 0.18,
    h: 0.18,
    fill: { color: ACCENT },
    line: { color: ACCENT, width: 0 },
  });
  s.addText("ISEP · COMPENSATION PROJECT 2025/2026 · 5 ECTS", {
    x: ML + 0.35,
    y: MT - 0.06,
    w: 10,
    h: 0.3,
    fontFace: BODY,
    fontSize: 10,
    color: MUTED,
    charSpacing: 2,
    margin: 0,
  });
  s.addText("Gym Buddies", {
    x: ML,
    y: 2.3,
    w: 11,
    h: 1.0,
    fontFace: HEAD,
    fontSize: 48,
    color: INK,
    margin: 0,
  });
  s.addText("Find a training partner. Train together. Stay motivated.", {
    x: ML,
    y: 3.35,
    w: 11,
    h: 0.45,
    fontFace: BODY,
    fontSize: 18,
    color: ACCENT,
    italic: true,
    margin: 0,
  });
  s.addText("Joaquim Kéloglanian  ·  20 min + 30 min Q&A  ·  wiki commit 2fcabfa", {
    x: ML,
    y: 6.6,
    w: 11,
    h: 0.35,
    fontFace: BODY,
    fontSize: 14,
    color: MUTED,
    margin: 0,
  });
  s.addNotes(
    "One line: social app to find a gym buddy. Do not start with the stack.",
  );
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 2, footer: "Gym Buddies · problem" });
  addEyebrow(s, "Problem");
  s.addText("Athletes train alone.", {
    x: ML,
    y: 1.15,
    w: 11.5,
    h: 0.7,
    fontFace: HEAD,
    fontSize: 32,
    color: INK,
    margin: 0,
  });
  const cards = [
    ["No partner", "A session dies when nobody is free at the same hour and gym."],
    ["No graph", "Existing social apps are not built around sport, place, and time."],
    ["No trust", "Public profiles leak; private ones hide the people you need."],
  ];
  cards.forEach((c, i) => {
    const x = ML + i * 3.9;
    s.addShape(pres.shapes.RECTANGLE, {
      x,
      y: 2.3,
      w: 3.6,
      h: 3.2,
      fill: { color: CARD },
      line: { color: HAIR, width: 1 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x,
      y: 2.3,
      w: 0.12,
      h: 3.2,
      fill: { color: ACCENT },
      line: { color: ACCENT, width: 0 },
    });
    s.addText(c[0], {
      x: x + 0.35,
      y: 2.55,
      w: 3.05,
      h: 0.6,
      fontFace: HEAD,
      fontSize: 20,
      color: INK,
      margin: 0,
    });
    s.addText(c[1], {
      x: x + 0.35,
      y: 3.3,
      w: 3.05,
      h: 1.8,
      fontFace: BODY,
      fontSize: 16,
      color: MUTED,
      margin: 0,
    });
  });
  s.addNotes("Keep it human. No stack yet.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 3, footer: "Gym Buddies · scope" });
  addEyebrow(s, "Scope");
  s.addText("Three modules, one product.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.55,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  s.addTable(
    [
      [
        { text: "In scope", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
        { text: "Out of scope", options: { bold: true, color: "FFFFFF", fill: { color: INK } } },
      ],
      [
        "Feed, posts, likes, nested comments, friends, public/private profiles, events, search, suggestions, DMs, JWT, MinIO, fixtures, admin",
        "Native iOS/Android, payments, ads, wearables, white-label, E2E encryption, group chat",
      ],
    ],
    {
      x: ML,
      y: 1.9,
      w: 11.7,
      colW: [6.0, 5.7],
      border: { pt: 0.5, color: HAIR },
      fontFace: BODY,
      fontSize: 14,
      color: INK,
      valign: "top",
    },
  );
  s.addText("Cadrage with the instructor did not happen (holiday). Specs are not blocked on that meeting.", {
    x: ML,
    y: 5.5,
    w: 11.7,
    h: 0.5,
    fontFace: BODY,
    fontSize: 14,
    color: MUTED,
    italic: true,
    margin: 0,
  });
  s.addNotes("Point at 01-Scope-and-modules.md. Mention cadrage will not happen.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 4, footer: "Demo 1 · social  ·  live as demo.alex" });
  addEyebrow(s, "Demo 1 — social · 4 min");
  s.addText("Feed, post, comment, like, friend.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.55,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  const steps = [
    ["01", "Sign in", "demo.alex from .env"],
    ["02", "Feed", "Friends + own, cursor 20"],
    ["03", "Post", "Text, optional images"],
    ["04", "Thread", "Depth cap 4, likes"],
    ["05", "Friend", "Request → accept"],
  ];
  steps.forEach((st, i) => {
    const x = ML + i * 2.35;
    s.addText(st[0], {
      x,
      y: 2.1,
      w: 2.1,
      h: 0.4,
      fontFace: BODY,
      fontSize: 12,
      color: ACCENT,
      margin: 0,
    });
    s.addText(st[1], {
      x,
      y: 2.5,
      w: 2.1,
      h: 0.45,
      fontFace: HEAD,
      fontSize: 20,
      color: INK,
      margin: 0,
    });
    s.addText(st[2], {
      x,
      y: 3.05,
      w: 2.1,
      h: 0.8,
      fontFace: BODY,
      fontSize: 14,
      color: MUTED,
      margin: 0,
    });
  });
  s.addText("If the live app fails, play the offline recording. Do not invent a story.", {
    x: ML,
    y: 4.6,
    w: 11.7,
    h: 0.4,
    fontFace: BODY,
    fontSize: 16,
    color: ACCENT,
    italic: true,
    margin: 0,
  });
  s.addNotes("Live as demo.alex. FS-FEED, FS-POST, FS-CMT, FS-FRND.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 5, footer: "Demo 2 · session" });
  addEyebrow(s, "Demo 2 — session · 4 min");
  s.addText("Friends-only event. Apply. Last seat.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.55,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  s.addTable(
    [
      [
        { text: "Rule", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
        { text: "FS", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
        { text: "What to show", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
      ],
      ["Capacity 1–100 excluding organizer", "FS-EVT-01", "Create weightlifting, friends, 3 seats"],
      ["Apply once per occurrence", "FS-EVT-05", "demo.blake applies"],
      ["Accept is transactional", "FS-EVT-07", "Fourth accept → CONFLICT"],
      ["WEEKLY + BYDAY, 90-day window", "FS-EVT-03", "List materialised occurrences"],
    ],
    {
      x: ML,
      y: 1.9,
      w: 11.7,
      colW: [4.2, 2.0, 5.5],
      border: { pt: 0.5, color: HAIR },
      fontFace: BODY,
      fontSize: 14,
      color: INK,
      valign: "middle",
    },
  );
  s.addNotes("Show a full event and a rejected extra applicant. SELECT FOR UPDATE.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 6, footer: "Demo 3 · buddy" });
  addEyebrow(s, "Demo 3 — buddy · 2 min");
  s.addText("Explainable suggestion, then a DM.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.55,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: ML,
    y: 2.0,
    w: 5.6,
    h: 3.6,
    fill: { color: CARD },
    line: { color: HAIR, width: 1 },
  });
  s.addText("Why this person", {
    x: ML + 0.35,
    y: 2.2,
    w: 5.0,
    h: 0.4,
    fontFace: HEAD,
    fontSize: 18,
    color: INK,
    margin: 0,
  });
  s.addText("Primary reason = argmax of wi × feature. FoF (Adamic–Adar), sports Jaccard, geo, windows, experience. Not ML.", {
    x: ML + 0.35,
    y: 2.75,
    w: 5.0,
    h: 2.4,
    fontFace: BODY,
    fontSize: 16,
    color: MUTED,
    margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: ML + 6.0,
    y: 2.0,
    w: 5.7,
    h: 3.6,
    fill: { color: CARD },
    line: { color: HAIR, width: 1 },
  });
  s.addText("Then message", {
    x: ML + 6.35,
    y: 2.2,
    w: 5.1,
    h: 0.4,
    fontFace: HEAD,
    fontSize: 18,
    color: INK,
    margin: 0,
  });
  s.addText("Friends only. Text, one image, or audio ≤ 120 s. WebSocket + HTTP fallback. Bytes in MinIO.", {
    x: ML + 6.35,
    y: 2.75,
    w: 5.1,
    h: 2.4,
    fontFace: BODY,
    fontSize: 16,
    color: MUTED,
    margin: 0,
  });
  s.addNotes("Read the why line on a suggestion card. FS-SUGG-03, FS-MSG.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 7, footer: "Architecture" });
  addEyebrow(s, "Architecture · 2 min");
  s.addText("Four repos. One modular monolith.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.5,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  const repos = [
    ["documentation", "Wiki, tickets, Gym Buddy Project"],
    ["openapi", "HTTP contract. Tagged $ref tree."],
    ["service", "Java 25 · Spring · Flyway · VPS"],
    ["ui", "Angular 22 · Pages · orval client"],
  ];
  repos.forEach((r, i) => {
    const y = 1.85 + i * 1.05;
    s.addShape(pres.shapes.RECTANGLE, {
      x: ML,
      y,
      w: 11.7,
      h: 0.9,
      fill: { color: CARD },
      line: { color: HAIR, width: 1 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: ML,
      y,
      w: 0.12,
      h: 0.9,
      fill: { color: ACCENT },
      line: { color: ACCENT, width: 0 },
    });
    s.addText("gym-buddy-" + r[0], {
      x: ML + 0.4,
      y: y + 0.12,
      w: 4.5,
      h: 0.65,
      fontFace: HEAD,
      fontSize: 18,
      color: INK,
      margin: 0,
    });
    s.addText(r[1], {
      x: ML + 5.1,
      y: y + 0.12,
      w: 6.2,
      h: 0.65,
      fontFace: BODY,
      fontSize: 16,
      color: MUTED,
      margin: 0,
    });
  });
  s.addNotes("Wiki + OpenAPI + service + UI. Pages for static; OVH for Java. Postgres, Redis, MinIO.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 8, footer: "Data model" });
  addEyebrow(s, "Data model · 1 min");
  s.addText("Eight entities. Not the whole ER.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.5,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  const ents = ["User", "Friendship", "Post", "Comment", "Event", "Media", "Message", "Audit"];
  ents.forEach((name, i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const x = ML + col * 3.0;
    const y = 2.0 + row * 2.0;
    s.addShape(pres.shapes.RECTANGLE, {
      x,
      y,
      w: 2.7,
      h: 1.6,
      fill: { color: CARD },
      line: { color: HAIR, width: 1 },
    });
    s.addText(name, {
      x,
      y: y + 0.5,
      w: 2.7,
      h: 0.6,
      fontFace: HEAD,
      fontSize: 22,
      color: INK,
      align: "center",
      margin: 0,
    });
  });
  s.addNotes("UUIDs, UTC, soft-delete. PostgreSQL 18. Flyway V1–V12 + fixtures.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 9, footer: "Algorithm" });
  addEyebrow(s, "Algorithm · 3 min");
  s.addText("Suggestions: generate, then score.", {
    x: ML,
    y: 1.05,
    w: 11.5,
    h: 0.5,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  s.addText("S(u,v) = 0.35 m̂ + 0.25 J + 0.15 G + 0.15 T + 0.10 E", {
    x: ML,
    y: 1.65,
    w: 11.5,
    h: 0.45,
    fontFace: BODY,
    fontSize: 20,
    color: ACCENT,
    margin: 0,
  });
  s.addTable(
    [
      [
        { text: "Term", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
        { text: "Meaning", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT } } },
      ],
      ["m̂", "Adamic–Adar on mutual friends, min-max on C(u)"],
      ["J", "Jaccard of sports"],
      ["G", "Geo, D = 25 km, or 0.4 same city"],
      ["T / E", "Window overlap / experience closeness"],
    ],
    {
      x: ML,
      y: 2.25,
      w: 11.7,
      colW: [1.6, 10.1],
      border: { pt: 0.5, color: HAIR },
      fontFace: BODY,
      fontSize: 15,
      color: INK,
    },
  );
  s.addText("FoF is O(d²) per user. Nightly all-users ≈ 3k × 64. No all-pairs. Not ML.", {
    x: ML,
    y: 5.55,
    w: 11.7,
    h: 0.4,
    fontFace: BODY,
    fontSize: 16,
    color: MUTED,
    italic: true,
    margin: 0,
  });
  s.addNotes("One formula. Complexity on 3k users. Why not ALS: no implicit feedback, opaque why.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 10, footer: "Security" });
  addEyebrow(s, "Security · 1.5 min");
  s.addText("Fail closed. No existence leak.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.5,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  const sec = [
    ["JWT", "HS256 access in JSON. Refresh cookie HttpOnly + Secure + SameSite=Lax. Redis denylist."],
    ["Passwords", "Argon2id. Never logged. ≥ 10 characters."],
    ["canRead", "Mint a 60 s signed GET only after ACL. Deny and missing both NOT_FOUND."],
    ["Admin", "Member calls to /admin/* return NOT_FOUND. Staff JS is a separate bundle."],
  ];
  sec.forEach((row, i) => {
    const y = 1.8 + i * 1.05;
    s.addText(row[0], {
      x: ML,
      y,
      w: 2.4,
      h: 0.9,
      fontFace: HEAD,
      fontSize: 18,
      color: ACCENT,
      margin: 0,
    });
    s.addText(row[1], {
      x: ML + 2.6,
      y,
      w: 9.1,
      h: 0.9,
      fontFace: BODY,
      fontSize: 16,
      color: INK,
      margin: 0,
    });
  });
  s.addNotes("Stranger cannot fetch an object key. TS-JWT, FS-MED-06/07.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 11, footer: "Tests and fixtures" });
  addEyebrow(s, "Tests · 1 min");
  s.addText("Pyramid + a seeded graph.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.5,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  const stats = [
    ["3 000", "users"],
    ["12 000", "friendships"],
    ["15 000", "posts"],
    ["20260813", "seed"],
  ];
  stats.forEach((st, i) => {
    const x = ML + i * 3.0;
    s.addText(st[0], {
      x,
      y: 2.1,
      w: 2.7,
      h: 0.7,
      fontFace: HEAD,
      fontSize: 28,
      color: ACCENT,
      align: "center",
      margin: 0,
    });
    s.addText(st[1], {
      x,
      y: 2.8,
      w: 2.7,
      h: 0.4,
      fontFace: BODY,
      fontSize: 16,
      color: MUTED,
      align: "center",
      margin: 0,
    });
  });
  s.addText("JUnit names FS IDs. CI uses tens of rows, never the 3k set. Prod profile cannot reset. GitHub Actions: format, test, HTTP smoke on every PR to develop.", {
    x: ML,
    y: 3.7,
    w: 11.7,
    h: 1.4,
    fontFace: BODY,
    fontSize: 16,
    color: INK,
    margin: 0,
  });
  s.addNotes("Datafaker, seed 20260813. demo.alex / demo.blake.");
}

{
  const s = pres.addSlide();
  addBase(s, { pageNum: 12, footer: "Limits" });
  addEyebrow(s, "Limits and Q&A");
  s.addText("What I would drop with two weeks less.", {
    x: ML,
    y: 1.1,
    w: 11.5,
    h: 0.55,
    fontFace: HEAD,
    fontSize: 28,
    color: INK,
    margin: 0,
  });
  s.addText(
    [
      { text: "Weekly matching opt-in — greedy 1/2-approx, not exact.", options: { bullet: true, breakLine: true } },
      { text: "Audio DMs — text + image would still satisfy the brief.", options: { bullet: true, breakLine: true } },
      { text: "Recurring events beyond WEEKLY+UNTIL.", options: { bullet: true, breakLine: true } },
      { text: "Live Pages login from the public internet (UFW + SameSite=Lax).", options: { bullet: true } },
    ],
    {
      x: ML,
      y: 1.85,
      w: 11.7,
      h: 2.6,
      fontFace: BODY,
      fontSize: 18,
      color: INK,
      paraSpaceAfter: 8,
    },
  );
  s.addText("Ask: Java 25? Stranger image key? Suggestion complexity? Racing accepts? RRULE? How a tag reaches the VPS?", {
    x: ML,
    y: 4.7,
    w: 11.7,
    h: 1.1,
    fontFace: BODY,
    fontSize: 16,
    color: MUTED,
    italic: true,
    margin: 0,
  });
  s.addNotes("Answers point at a spec ID. CI → Release → GHCR → replace.sh → Caddy.");
}

pres.writeFile({
  fileName: "Gym-Buddies-defense.pptx",
}).then(() => {
  console.log("wrote Gym-Buddies-defense.pptx");
});
