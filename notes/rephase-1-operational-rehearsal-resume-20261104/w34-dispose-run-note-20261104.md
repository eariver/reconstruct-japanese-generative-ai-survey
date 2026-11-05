# W34 dispose + normal-run wrapper — source review note (DO NOT EXECUTE)

Single bounded W34 dispose + ONE normal retry. Preserves preflight and SP
successes untouched. No active execution yet; independent source review
required before any Root-authorized run. No subagents, no project
import/run, no network/Production/reconstruct Git while authoring (stdlib
hash/parse/lstat only).

## Reuse (pinned, no SP-hardcoded state)

- r6 low-level helpers via pinned `sp-operator-prepare-r6-20261104.py`
  `2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664`
  (verified-before-import): pinning, source771 + test triangulation,
  full-tree compare. W34-specific State/tree/gates only.
- NOT called: SP-hardcoded state helpers, SP-shaped READY/verified-dict
  fabrication, global mutation bypass. No new shipping API/module/schema.

## Exact scope (actual DATA)

- Baseline W34 tree 1781f/80d + staged r2 input = **1782** live
  (`interactive-evidence-w34-r2-20261104T235848Z.json` 1580317B `1ea562...`).
- Exact2 (both 0o664, nlink 1): Ledger `76ac53f9...`/186202B,
  Completeness `93dbefae...`/71532B. State `7e6a50c2...` CAND unchanged.
- Full expected `1782 -> 1781 -> 1780` per deletion; O_EXCL packet backups
  + same 64-char State SHA checked before each unlink; all source/CP/Human/
  accepted/supp428 Raw + staged input pins; no unknown restore.
- THEN one existing `rn.run(repo, state, staged_input, existing_supplement)`
  (current e84 strict facade; owns facade per phase, no outer facade).
- Normal outputs 409/439/3 LIMITED (tasks/results/views); State stays CAND.
- AFTER validators use ACTUAL EFFECTIVE 439 path (not SP root 369):
  `validate_materiality_ledger` + `validate_profile_completeness` with
  `ctx["effective_path"]` (439 rows), counts from files.
- Audit: archived NEW accepted `interactive-evidence.json` path + staged
  bytes identical; modes == recorded umask (O_EXCL copies stay 0664).
- NEW products: task/result/view dirs only. No Raw/supplement change.
- SP preserved (snapshot only, no SP invoke): SP preflight READY `c7cd05a8...`,
  SP dispose `DISPOSE_RUN.json` `cf26a23c...` still present.
- Retention packet-only NEW exclusive (`.../retention-W34-*` DIRECTLY under
  packet); raw stdout/stderr/numeric exit; failure preserves + no retry.

## Files (packet only, no active writes)

- `w34-operator-dispose-run-20261104.py` 43406B
  `68253077b0f10a3bd17b9c1ecce23e459c06489397ff7641c9be07396d5ae7bd`
- `w34-dispose-run-launcher-20261104.sh` 1079B
  `eaac10f7f7f0b8ec1a3559ec42ab048343e3c6c1115a810223fa8a13b2ca4076`
- `w34-dispose-run-checks-20261104.py` 5261B
  `284edbe6fa81f9e1272862895907c85e35c344478142ec356b2d029716d0041c`
  + raw `...raw.txt` 558B `f9b84a72...` — **19/19 PASS**
- Same manifest `cede7e46...` 991185B / input `1ea562...` 1580317B /
  READY `473bf85b...` 5360B / supplement `ce6f...` unchanged.

## Stdlib checks (actual DATA, no tokens)

DERIVED lists: root 369 / effective 439 / decisions 439 from live files;
invalid 368/438 refused; token strings refused; root-369 rejected for
ledger-439 (EFFECTIVE required). READY shape + staged/retained actuals.
Archival staged==r2, mismatch refused. No project imports.

## Limitations / no execution

Dead placeholder code removed; no token-tests. Source-read helper
signatures only (`rn.run`, `validate_*`, `_resolve/_capture/_finish`,
`_discovery_task_sources`, `_merge_supplement_task_sources`,
`funcs` contexts). No execution until Root + independent source review.
SP plan does not authorize W34; W34 does not touch SP.
