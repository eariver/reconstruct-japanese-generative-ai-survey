# Claim / version map — archived Sept 20/21 bodies vs cards, summaries, Nov current

Scope: D070 launch / D071 concepts / D141 models. D142 API excluded (not authorized/fetched).
Body pins: raw `u1.snapshot.body.bin` 42836B `10bf6607…`, decoded 253542B `14ae3118…`;
raw `u2.snapshot.body.bin` 49007B `62bf012c…`, decoded 307198B `35770834…`;
raw `u3.snapshot.body.bin` 350662B `97a5dd74…` (plain). Full pins in `decoded-manifest.json`.
Accepted cards: checkpoint `1233b1f6…`; `evidence-accepted.json` 49237B `65784e69…`;
cards D070 `6090eee4…` / D071 `bc7dedb1…` / D141 `aad7cc3f…` / D142 `7d7d26d2…` (all PARTIAL).

## D070 — launch

| material claim | archived u1 (2026-09-21T03:30:22Z) | Nov current (2026-11-01, 270966B `278478f0…`) | disposition |
|---|---|---|---|
| RLCD / parallel sampler / new architecture | present (4 RLCD hits, parallel sampler) | present | card claims 1 CONFIRMED at 09-21 revision; rebind source to archive |
| 70–500 ms, 40–200x, $0.042/MTok in, free out | present | present | vendor claim, historically present; no independent validation |
| 193.6x / 444.6x vs Astra/Fable workflow evals | present + nuance section | present | vendor claim with first-party bias admissions; quarantine retained |
| laptop/West-Coast evals, subsidy unprovable, OpenRouter baselines | present | present | first-party limitation admissions; carry forward |
| early access / waitlist | present | present | availability claim corroborated at 09-21 |
| visible date Sep 15 vs Sep 20 publish comment | Sep-15 byline + embedded 09-15 + Sep-20 publish comment; ssr 09-18 / optimized 09-20 | Sep-15 field + Oct-28 publish comment; ssr 10-27 / optimized 10-28 | page revised between 09-20 and 10-28; 09-15 field is CMS metadata, not a version pin |
| independent reproduction | absent | absent | limitation STANDS (S73 community-grade only) |
| RLCD internals | name only | name only | limitation STANDS |

## D071 — concepts

| material claim | archived u2 (2026-09-21T04:13:55Z, dateModified 09-17) | Nov current (2026-11-01, 165512B `b58d91ae…`, dateModified 10-14) | disposition |
|---|---|---|---|
| Choice / Score / Noul + probabilities + confidence | present w/ ticket/frustration/refund examples | present | card claim 1 CONFIRMED at 09-21 revision |
| calibration = group-level, no per-answer guarantee | present verbatim | present | first-party caveat stable across revisions |
| parallel evaluation, state+question map, POST /v1/systemone, jev-latest default | present | present | stable |
| text-only input (no image/audio/video yet) | present ("currently accepts text input only") | present | stable |
| confidence-gated escalation / workflow combination | present | present | stable |
| atomic-question doctrine / 255-cardinality / score-then-choose | NOT in archived visible text | card cites current scope | sub-claim stays CURRENT-ONLY; do not back-project to 09-21 |
| early access / waitlist on this page | absent | — | availability via D070/S74, not this page revision |
| API schema / confidence math | absent (links out to API ref) | absent | belongs to D142; stays open |

## D141 — models

| material claim | archived u3 (served 2026-09-20T20:50:53Z, dateModified 09-20) | Nov current (2026-11-01, 219035B `59b6c17b…`, dateModified 11-01) | disposition |
|---|---|---|---|
| versioned ID jev-1.13.0 | present (8 hits), only model | present alongside 1.14.0 | historical pin = 1.13.0-only era |
| jev-latest → ? / jev-preview → ? | BOTH → jev-1.13.0 ("no preview build right now") | BOTH → jev-1.14.0 (card text stale: says 1.13.0) | card claim 1 CORRECTED at current scope; historical = 1.13.0 |
| $42/BTok input-only, outputs free | present | present | stable vendor pricing claim |
| 250k tok/s, 1200 req/min, 64k/32k ctx | present | present (limits mutable warning) | stable |
| alias-drift warning (pin IDs; response reports ID) | present | present | stable; material to eval-validity |
| no per-account fine-tuning, RLCD shared weights | present | present | stable; internals undisclosed |
| English-primary / CJK weaker; ZDR enterprise | present | present | stable documented limits |
| jev-1.14.x | ABSENT ("1.14" = SVG false positives) | present (8 hits, 1.13+1.14 table) | 1.14 is post-cutoff drift; must not back-project |

## Version timeline (captured, not asserted beyond captures)

- 2026-09-15: launch byline date (CMS field in both revisions; earliest CDX row `20260915192610`
  NOT fetched — no body authority for 09-15).
- 2026-09-17T11:55:10Z: u2 docs `dateModified` (page content revision marker, not publisher version ID).
- 2026-09-18T08:31:26Z / 2026-09-20T23:50:00Z: u1 Framer ssr / page-optimized stamps.
- 2026-09-20T02:53:36Z: u3 docs `dateModified`; served memento 2026-09-20T20:50:53Z.
- 2026-09-21T03:30:22Z / 04:13:55Z: served u1 / u2 mementos (newest eligible ≤ cutoff).
- Post-cutoff drift (Nov current): launch page Oct-27/28 stamps; concepts dateModified 10-14;
  models dateModified 11-01 + 1.14 + aliases→1.14.

## Independent-validation separation (all vendor/project claims above)

No body in this intake — archived or current — contains RLCD internals, benchmark/calibration
methodology, or third-party reproduction. S73 (awesome-jev, community) remains the only
reproduction-lead set, explicitly NOT peer-reviewed; S72/S74 secondary. O10 historical-body gap
closes for D070/D071/D141 at the stated timestamps; independent-measurement gap does not.
