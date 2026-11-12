# Jev archive intake — independent content review (not acquisition author)

Reviewer role: independent content reviewer. No new network. All transport facts below are
offline re-verifications of the acquisition author's packet
`notes/rephase-1-selection-architecture-20261105/intake-20261106T001808Z-jev-archive/`
(`manifest.json` 4289B SHA256 `671bfab8105b76119e6a6722d9f934edebeb2b5752c60898a5`;
helper `intake_helper.py` 11670B SHA256 `30f050fde9af36256f324a36c0b488a98329efc7054499849fccb6510dcb6c6`).
Raw `*.body.bin` / `*.meta.json` unchanged; decoded DATA is NEW
(`u1.snapshot.decoded.html`, `u2.snapshot.decoded.html`; u3 raw is already plain HTML).
See NEW `decoded-manifest.json` in the same packet for the byte/hash table.

## 1. Authorization and request-count bound — CONFIRMED

Human authorized exactly 3 archive-index queries + 3 selected snapshot body captures for the
3 exact original locators, snapshots restricted to `2026-09-01..2026-09-21T16:10:00Z`
(`jev-archive-intake-authorization.md`). Observed: 3 index + 3 snapshot = 6 logical requests,
all exit 0 / HTTP 200, no retries, no mirrors, no new URLs, no API-reference fetch, no
current-publisher refetch, no interval broadening. PASS.

## 2. Raw hash/byte/header verification — all MATCH

| file | bytes | SHA256 | meta-recorded vs actual |
|---|---|---|---|
| u1.index.body.bin | 2697 | `495c93a8…d36ff7` | MATCH |
| u2.index.body.bin | 1093 | `487d4aec…6706728` | MATCH |
| u3.index.body.bin | 1104 | `41dfc593…284cf4bc` | MATCH |
| u1.snapshot.body.bin | 42836 | `10bf6607…45e61aee3` | MATCH (Content-Length 42836 agrees) |
| u2.snapshot.body.bin | 49007 | `62bf012c…68036c1d36` | MATCH |
| u3.snapshot.body.bin | 350662 | `97a5dd74…4d651b69` | MATCH |

Index responses are HTTP 200 `application/json`, zero redirects, `response_url == request_url`.
Snapshot `request_url` values are exactly the authorized `.../web/<ts>id_/<exact-original-URL>`
form with `id_` (original-content, no toolbar rewrite). Snapshot HTTP status 200 for all three
is TRANSPORT success only, not semantic PASS.

## 3. Request vs served timestamps, redirect chain, date bound — CONFIRMED with one material distinction

- u1: request `20260921033022` → served memento `Mon, 21 Sep 2026 03:30:22 GMT`
  (`x-archive-orig-date` identical), no redirect. `<= 20260921161000`. PASS.
- u2: request `20260921041355` → served memento `Mon, 21 Sep 2026 04:13:55 GMT`
  (`x-archive-orig-date` identical), no redirect. `<= 20260921161000`. PASS.
- u3: request `20260921091419` → **302** → served `20260920205053id_/...`
  (memento `Sun, 20 Sep 2026 20:50:53 GMT`, `x-archive-orig-date` identical). `<= cutoff`. PASS
  as a bound historical capture, BUT the served bytes bind to the **20260920205053** CDX row,
  not the selected `20260921091419` row. Logical requests = 6; HTTP redirect-transport hops = 7
  (6 logical + 1 archive-internal 302 that resolves the selected resource, not a new search).
  Do NOT cite u3 as "the 20260921091419 revision"; cite it as "served 20260920205053 via
  selected 20260921091419".

Exact original URLs: all three index row sets contain ONLY the exact authorized original URL
(`matchType=exact` honored; 18 + 8 + 9 rows, every row `original` equals the authorized locator,
every timestamp `<= 20260921161000`), and each selected timestamp is the row maximum. PASS.

## 4. CDX digest domain — verified offline where defined; no fake equality

CDX `digest` = SHA1 of the archived **wire bytes**, base32-encoded (verified offline):
u1 `6XH5…333MNF` MATCHES raw gzip bytes; u2 `TUIO…CRHAN` MATCHES raw gzip bytes;
served u3 bytes MATCH CDX row `20260920205053` digest `ABQR…5PSIG` and NOT the requested
`20260921091419` digest `E2BR…5GE6S` (that revision was not served — archive redirected to
nearest). CDX `length` is WARC-record length, never asserted equal to HTTP payload bytes
(u1 43980 vs 42836; u2 51619 vs 49007; u3 55087 vs 350662). PASS with the u3 row distinction.

## 5. Bodies are actual TypeSafe content, not archive error/challenge/toolbar

- u1 decoded title `Introducing System One Models & Jev - TypeSafe AI Blog`,
  `og:url` exactly the authorized locator; visible `Sep 15, 2026` byline + embedded
  `2026-09-15T00:00:00.000Z`, Framer `ssr-released-at 2026-09-18T08:31:26.653Z`,
  `page-optimized-at 2026-09-20T23:50:00.411Z`, comment `Published Sep 20, 2026, 11:49 PM UTC`.
- u2 decoded title `System One - TypeSafe AI`, `og:url` exactly the authorized locator;
  `dateModified 2026-09-17T11:55:10.949Z`; Mintlify docs chrome.
- u3 raw title `Models - TypeSafe AI`, `og:url` exactly the authorized locator;
  `dateModified 2026-09-20T02:53:36.007Z`; Mintlify docs chrome.
- The only `captcha` string in u2/u3 is a Next.js chunk name (`CaptchaProvider`) inside the
  Mintlify bundle manifest — not a challenge page. No Wayback toolbar injection (`id_` mode).

## 6. Substantive read — mechanisms / eval / availability / price / latency / aliases at captured Sept 20/21

All claims below are **vendor/project claims inside the captured bodies**, not independent validation.

- **D070 launch (u1, served 2026-09-21T03:30:22Z):** new stack = new model architecture +
  **parallel sampler** + training method **RLCD** (Reinforcement Learning for Calibrated Decisions);
  typed probabilistic outputs instead of generated strings; **70–500 ms end-to-end (40–200x)**,
  **$0.042/MTok input, outputs free**, no-type-errors-by-construction; workflow evals vs
  **GPT-6 Astra / Fable 5.1 average** as reference (**193.6x faster / 444.6x cheaper** headline);
  vendor's own nuance admits **laptop-based evals (West Coast)**, **subsidy unprovable**,
  workflow-authorship and reference-answer bias, OpenRouter-routed hallucination baselines.
  RLCD internals undisclosed (name + purpose only). Early access; waitlist; founder
  Diogo Almeida (ex-OpenAI/ChatGPT methods) byline.
- **D071 concepts (u2, served 2026-09-21T04:13:55Z):** **Choice / Score / Noul primitives**
  with per-output probabilities + **confidence**, all questions evaluated **in parallel** via
  state + typed question map in one POST (`POST /v1/systemone`, `model: jev-latest` default);
  **calibration measured across groups, no per-answer guarantee** (first-party caveat);
  **text input only** (strings/JSON/text arrays; no image/audio/video yet); refund-workflow
  decomposition doctrine; confidence-gated escalation. No waitlist/early-access text on this page
  revision; no atomicity/255-cardinality doctrine in visible text (those are Nov-current scope).
- **D141 models (u3, served 2026-09-20T20:50:53Z):** single model **jev-1.13.0**;
  **$42/BTok ($0.042/MTok) input-only billing, outputs free**; **250k tok/s + 1200 req/min**;
  **64k context (32k state + longest question)**; **text only**; **jev-latest → jev-1.13.0 and
  jev-preview → jev-1.13.0** ("no preview build available right now"); explicit **alias-drift
  warning** (pin versioned ID; response `model` field reports answering ID); no per-account
  fine-tuning/LoRA (shared RLCD weights; domain via state/instructions); English-primary,
  CJK weaker; zero-data-retention for enterprise; `GET /v1/models` lists aliases.
  **No jev-1.14.x string** in this revision ("1.14" hits are SVG path-data false positives).
- **D142 API:** NOT authorized, NOT fetched. Nothing in u1/u2/u3 substitutes for the
  `https://docs.typesafe.ai/api` contract: u2 links the API reference for the full request shape
  but does not contain schema fields or confidence-derivation math. D142 stays summary-only and
  **cannot be closed by the concepts body**.

## 7. Correction scope vs latest accepted cards, historical summaries, Nov current bodies

- **D070 card** (`task-b8b9…` 7468B `6090eee4…`, PARTIAL): claims 1–3 (RLCD/parallel/typed outputs;
  70–500 ms / $0.042 / no-type-error / 193.6x-444.6x vendor evals; laptop/adapter/OpenRouter nuance
  admissions) are now **confirmed present in the 2026-09-21 archived body**, upgrading "current
  body contains vendor claims" to "**09-21 revision** contains vendor claims". Correction needed:
  source role changes from `DATA.sp11-launch.html` current-only (270966B `278478f0…`,
  Last-Modified 2026-10-28, mixed Sep-15 CMS field + Oct-28 visible publish) to the archived
  revision (raw 42836B gzip `10bf6607…` / decoded 253542B `14ae3118…`, served 2026-09-21T03:30:22Z).
  Limitations 1–2 (no independent reproduction; RLCD internals undisclosed) STAND.
  Limitation 3 (historical UNCONFIRMED) is now closable for the launch page at this timestamp.
- **D071 card** (`task-cc12…` 5972B `bc7dedb1…`, PARTIAL): claims 1–3 (Choice/Score/Noul + parallel;
  group-calibration caveat; decomposition/workflow doctrine) are **confirmed present in the
  2026-09-21 archived body** (dateModified 2026-09-17). Correction: rebind from current-only
  `DATA.sp12-concepts.html` (165512B `b58d91ae…`, dateModified 2026-10-14) to the archived
  revision (raw 49007B `62bf012c…` / decoded 307198B `35770834…`). Note scope delta: the card's
  "255-cardinality / score-then-choose" phrasing is **absent from the archived visible text**
  (Nov-current addition or another docs page) — that sub-claim stays current-scope, not 09-21.
  Limitations 1–2 (no independent calibration/CJK testing; API details belong to D142) STAND.
- **D141 card** (`task-4700…` 6321B `aad7cc3f…`, PARTIAL): claim 1 must be **corrected**, not just
  rebased: the card's "aliases both resolving to 1.13.0" was read from the Nov current body, but the
  Nov body actually shows **both aliases → 1.14.0** plus a 1.13 + 1.14 table (219035B `59b6c17b…`,
  dateModified 2026-11-01) — internally stale at current scope. The archived 2026-09-20 revision
  shows **jev-1.13.0 only, both aliases → 1.13.0**. Correction: historical 09-20 version pin is
  `jev-1.13.0` + aliases→1.13.0 (raw 350662B `97a5dd74…`); current alias state (→1.14.0) is
  post-cutoff drift and must not be back-projected. Claims 2–3 (alias-drift warning; no per-account
  tuning) are present in BOTH revisions and are stable. Limitations 1–2 STAND.
- **Historical summaries** (`discovery-observations-d10…` 4453B `0b8bd0ab…`;
  `discovery-observations-r2…` 3751B `f7eeec68…`, both observed 2026-09-21, SUMMARY_CAPTURED):
  S70/S71/S141 mechanism/price/latency/availability summaries are **corroborated nearly verbatim**
  by the archived bodies; S142's "no benchmark/calibration protocol + INDEPENDENT_EVIDENCE_NOT_FOUND"
  negative finding is **unchanged** (no protocol in any fetched body). S72/S73/S74 secondary/community
  leads are untouched by this intake.
- **D142 card** (`task-21ce…` 3681B `7d7d26d2…`, PARTIAL): NO correction available from this intake.
  Its `VERIFIED` target label ("Contract-role recorded…") remains inconsistent with PARTIAL status;
  keep PARTIAL + "page body outstanding".

## 8. O10 — what this covers / what is still missing

Covered: timestamp-bound historical bodies for D070 (2026-09-21T03:30:22Z), D071
(2026-09-21T04:13:55Z), D141 (2026-09-20T20:50:53Z); exact full pins in `decoded-manifest.json`;
request-vs-served and CDX-domain bindings; vendor-claim vs independent-validation separation.
Still missing: D142 body (any date); the unserved u3 `20260921091419` (E2BRC…) revision —
  treat as unretrieved, archive redirected to nearest; any 2026-09-15 launch revision (earliest
  CDX row is `20260915192610`, not fetched — authorization allowed only the newest eligible);
  RLCD algorithm internals; any independent benchmark/reproduction of latency/price/accuracy/
  calibration; peer-reviewed corroboration (S73 stays community-grade).

## Verdict

**BODY_VERSION_CONFIRMED (bounded, per-body):** u1 at 2026-09-21T03:30:22Z, u2 at
2026-09-21T04:13:55Z, u3 at **2026-09-20T20:50:53Z** (via documented 302 from requested
20260921091419). Uncertainty is confined to: (a) the unserved u3 20260921091419 revision;
(b) pre-09-20 revisions; (c) D142 entirely.
**No semantic PASS is claimed** from HTTP 200s or index metadata — semantic upgrade of
D070/D071/D141 (PARTIAL → historical VERIFIED or corrected-PARTIAL) requires the normal
Evidence re-review path, not this intake.
