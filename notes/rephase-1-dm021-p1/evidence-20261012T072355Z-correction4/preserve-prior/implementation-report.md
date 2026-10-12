# DM021-P1 R3 correction implementation report (worker → root + same independent source/evidence resolution)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(HEAD409b292/tree8ce, detached, no branch/commit/network/Production). 13 paths 3M10A,
same 3A1M; LF2I 9 pins + pre-TeX `e8598239` preserved. R2 packet + 36-test PASS
preserved in `preserve-prior/` (module `8bf87871`, test `00ba3ef1`, report, 36 raw).
R3 edits module+test only (schema `5623c0d9` unchanged).

## Final pins (freeze-pre==post)

HEAD409b292/tree8ce, 3M10A. Module `69790944` 104046B, test `84a6e4a11` 106226B,
all 0o664. No other runtime/config/controller/receipt changes.

## R3-C1 — State-bound checkpoints (no wrappers-only, no guessed fallback)

`_build_graph(col,root,cfg,state,…)` now takes `cfg` for `resolve_checkpoint_artifact`.
Cached validated records per checkpoint (first artifact full API validation, rest
reuse pinned record, no redundant per-row revalidation, no fake names).

- Wrappers: every `state.checkpoint_provenance` `{path,sha256}` pinned,
  `checkpoint-wrapper:<name>` KEEP operational (never frozen), `STATE_CHECKPOINT` edges.
  History SHAs stay provenance (no live nodes for old SHAs).
- Exact map via API: `discovery/discovery-acceptance`,
  `screening/screening-acceptance`, `evidence/evidence-acceptance` +
  `evidence/edition-views-acceptance` (pair also checked via
  `resolve_active_evidence_views` same-checkpoint binding, no cross-run join),
  `materiality/materiality-ledger`, `completeness/profile-completeness`,
  `selection/candidate-matrix` + `selection/candidate-selection`,
  `architecture/issue-architecture` + `architecture-review-summary` +
  `architecture-review-attention`, `draft/synthesis-input` + `synthesis-result`
  + dynamic `draft-package:*`/`draft-result:*` discovered from pinned draft record
  (no pid guessing). Each artifact: `checkpoint-artifact:<cp>:<name>` provenance
  + `upstream:<kind>` frozen (union, same KEEP), `CHECKPOINT_ARTIFACT` edge from wrapper.
- Views files via acceptance `views[]` + validator `view_filename` convention
  (`views/<file>` siblings, verified `view_sha256`): `upstream:edition-view:<id>`.
  Evidence `package.json`+`tasks/*.json`, screening `package.json`+`results/*.json`+
  `input/batches/*.jsonl`, discovery raw retained from prior R2 container walk
  (explicit fields, now from checkpoint-bound acceptances, union, no conflict).
- Guessed `profile-completeness.json`/`-v2.json` presence lookup REMOVED (authority
  fallback forbidden). Completeness ONLY via `completeness` checkpoint ref.
- Original rows honest: nodes still effective bytes (no old-byte live nodes),
  edges relabelled `EFFECTIVE <name>` (not `CHECKPOINT_ROW` false literal refs);
  original path/sha metadata preserved in `original_rows` return, not graph live nodes.

Frozen: any `upstream:*` → frozen kind (research, incl. selection/views/completeness);
`checkpoint-wrapper:*`/`state:*`/QA/tool/pub/candidate operational excluded. URLs/
historical SHAs provenance only. Missing/unclassifiable required relation would be
explicit `CHECKPOINT_*`/`VIEWS_*` blocker, not omit (none hit; views absent-but-
unrequired not applicable — views acceptance + files exist in both fixtures via
checkpoint, included).

## Oracle (checkpoint fields + container maps, stale proof)

`_assert_transitives_expected_set` rebuilt: expected via `agent.resolve_checkpoint_artifact`
in TEST (independent, same exact map, not receipt list) + container maps via explicit
acceptance fields (`package.tasks`, `input.batches`, `batches/result_sha256`,
`views[]`+`view_filename`, draft record artifacts — independently loaded, not P1 graph).
Asserts each in graph/retention KEEP + frozen (research) vs wrappers KEEP not frozen,
pub/QA/State/receipt/candidate excluded; no count surrogate. Stale
`source_root/stale-profile-completeness.json` (same bytes/basis as real, valid-looking,
NOT checkpoint-bound, created BEFORE prepare so tree includes it) asserted NOT in
graph/frozen in Longform+Weekly positives — proves no presence/glob inference.
Selection/views retention+frozen explicitly proved via checkpoint expected (matrix+
selection, views acceptance+files).

## C2/C3/C4 retained

- C2 `_check_bundle_profile_exact` (path+SHA, manuscript coherent, live-bytes check;
  file-tamper yields checkpoint drift `STATE_INVALID` first, same-SHA path unit proves
  `BUNDLE_PROFILE_DIVERGED`).
- C3 `_final_full_receipt_recheck` (full `validate_receipt`, no bypass) after schema
  (prepare) and after scope (validate) + validated tree; late-prepare/scope helper
  (`scripts/survey_production_v2.py` outside closures) seams refuse; artifact-only passes.
- C4 `_validated_state_profile_for_tree` BEFORE any `_tree_map`, `Path(root).resolve()`
  once, invalid `source_root="/"` spy proves 0 walker calls; dead retention loop +
  duplicate digest check removed.

## Tests

Strict `run_correction.py`: **36/36 OK in 3255.889s, exit 0, pre/post identical**.
Python 3.14.4, `optimize==0`, sanitized no-network Git, exclusive logs. Gate 27/27
(affected shared-schema control), P1 9/9 (C1 oracles both routes, R1×2, ordinary
compat). Old36 no transfer. No R3 failures to preserve (first R3 run passed).

## Patch/proof (copy method, no index writes)

`gen_correction_patch.py` byte-copies ACTIVE to `/tmp/.../R3-gen-...`, `add -N`+`diff`
THERE (disposable index), copies patch out, deletes copy — ACTIVE
`diff --cached --name-only` empty (verified). Patch 591663B
`611cfd75f12f960b606e697b50ea4a50782a214ce06e86a2687b2c9fa7f01fc6`, 13 diffs,
base HEAD409/tree8ce. `proof_apply.py` byte-copies ACTIVE to `/tmp/.../R3-verify-...`
(inert origin, no alternates, inode separation), reverts ONLY 13 in COPY to clean409,
`apply --check`+`apply` AS SAVED exit 0, all13 hashes/modes/status/base equal.
No commits/branches/network/subagents/protected edits. Prior `add -N` in ACTIVE
(R1/R2 generators) disclosed as avoidable; R2+R3 generators copy-based.

STOP for root + same independent source/evidence resolution. Whole NOT_READY, DM021
OPEN. Commit/Push Human-owned. No completeness claimed if transitive missing (none).
