# W34 normal adopt — REFUSED at postread validation, NO resume/readback (STOP)

Root §11 one adopt, R2 `w34-repaired-20261112-r2` + decision `09b2feae6dbae50762d66eae849088736c25cda58ba08b95dfcc62fb624cdc11`/4030. Absolute repo, CWD ABS repo, `PYTHONPATH=ABS`, `PYTHONDONTWRITEBYTECODE=1`, clean Git env/HOME, no network/Production/reconstruct-readback/subagents. Outer `w34-adopt-20261114T065242Z.{argv,env,pid,wall-start,stdout,stderr,exit 1}`; no fix/rerun/cleanup.

## Pre-adopt verified (unchanged)
- Source 773 `a7e40c…`, HEAD `cc1c…`/tree `ed2dc4…`; State `d7acd29b…` EVIDENCE_REVIEWED/init480, CP evidence `0979f9f7…`, Profile `2a8c3089…`, Contract8 pipeline `3adfbda2…`/quality `b5b955d5…`, 4 refs `3777133c…/edf21e4de…/f089cc4e…/e8c432dd…`, R1 manifest `54de43ed…`/request `057e186f…` + 4 Raw `85c70376…/a4c2aafe…/da737a85…/56b48291…`, R2 manifest `867eba96…`/438583 + request `bb6042c6…`/1654899, decision packet `09b2feae…`/4030, 7 slots absent, Human pending/null/inactive, guard absent, R2 405/405 byte-eq report `w34-r2-mechanical-postprepare-comparison.md` PASS.

## Decision staging (verbatim, O_EXCL)
- Copied packet `w34-supplied-decision-r2.json` → repo `sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r2-decision.json` `09b2feae…`/4030, mode `0o664`, no R1 decision substitution, no rewrite.

## Adopt result: REFUSED (postread, INDETERMINATE)
- CLI: `adopt --repo-root ABS --state-path sources/2026-W34/production-state.json --revision-path sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r2 --decision-path sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r2-decision.json` → exit `1`, stdout empty, stderr `{"status":"REFUSED","error":"postread FULL adopted-graph validation failed (INDETERMINATE): recorded-commit batch header mismatch for: sources/2026-W34/production-profile.json"}`.
- HIGH internally proved then wrote guard/report/CP/State triplet BEFORE the failing postread (no manual state/schema/source manipulation by operator).

## Actual partials (preserved, no cleanup)
- Guard NEW `sources/2026-W34/orchestration/v2/acceptance-revision.guard.json` (nonce `387ee54f…`, before `d7acd29b…`, expected-after `a8586351…`, work cc1c/ed2dc4, `recorded_at 2026-11-14T06:53:43Z`).
- State `d7acd29b…` → `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`; lifecycle still `EVIDENCE_REVIEWED`, init480, Human pending/null/inactive, history last still `EVIDENCE_REVIEWED@e84` (no new history row); CP evidence/materiality/completeness → R2 `checkpoint/record.json` `73ab28ea…`.
- R2 new: `checkpoint/{record.json 73ab28ea…, proposed-graph-proof.json, supersession-report.json}`, `checkpoint.planned.json/.sha256`, `proof/` vs pre-existing `candidate/request.json/retention/revision-manifest.json`. Old canonical Ledger `f089cc4e…`/186202 + Completeness `e8c432dd…`/71532 + old accepted sets immutable (`edf21e4de…`, `3777133c…`).
- Row counts (adopt-independent, from R2 prepare + decision): 409 tasks/cards/Views (405 unaffected byte-eq per R2 comparison, 4 affected MATERIAL promotions), 439 ledger rows (435 unaffected incl 4 DROP, 4 promoted), completeness 3 obligations LIMITED/closure null (R2 `d869027a…`).

## Strict checks after failure (no resume/readback per STOP)
- No `resume` (would require explicit success; NOT run), no `readback`, no Selection. SP `694f5e49…`/State `180db8c3…` unchanged, no SP guard, R1 `54de43ed…` preserved, source 773 `a7e40c…` (HIGH/LOW `f312f02e…/7f5fc9e0…` unchanged).
- No semantic claim beyond packet decision `09b2feae…` (independent research decision, not Human approval/adoption).
