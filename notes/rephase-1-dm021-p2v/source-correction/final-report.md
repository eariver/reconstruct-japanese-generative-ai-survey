# DM021-P2V Co-Worker A final report — source/tests/runtime corrections + verification

2026-10-16 JST. Execution per root `execution-selection.md` (smoke 2 exact
positives → full focused module → GEN complete18patch → proof SAVED apply).
B4 tools used AS-SAVED except one corrected local copy (see §6); originals
preserved byte-identical. No subagents/network/intake/Production/commits/
branch changes. Independent review is not this report's approval; root review
follows.

## 1. Final source pins (current basis for all green runs)

Candidate `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`,
detached `409b292756dd1277b9dfae87679934c0d2ce251c` / tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status 102 rows (18 source 3M15A
+ 84 caches), HEAD/tree/index pinned PRE and finally-POST in every run.

| Path | SHA256 | Bytes | Mode | Change vs P2R 16-file basis |
|---|---|---|---|---|
| `scripts/survey_editorial_correction_proposal_v2.py` (P1) | `cdd69fe7c24de6dda9ee503cfcfbc791a9d7e421141dbb23586f1e4431c27eab` | 113535 | 0o664 | M private factoring only (selection V1); public shape/absence/final checks preserved |
| `scripts/survey_editorial_current_authority_v2.py` (observer) | `79a3396cf07d85cfeb11df9f85910ba8aed2ed63f965713edab5b076d580d3f4` | 37896 | 0o664 | A read-only `observe_current_authority` + `CurrentAuthorityError` (no owned/token/pending) |
| `tests/test_survey_editorial_current_authority_v2.py` | `d3224797410c9f08f98563801ae957a19344d76773339b9c252e2d0ab5a6fc80` | 68592 | 0o664 | A 13 behavioral-oracle methods (2 type probes + 11 `observe` callers) |
| + 15 inherited paths (6 schemas − 0 changed, 5 scripts, 4 tests) | (see `expected18-source-correction-v4.json`) | — | 0o664 | byte-identical to P2R `expected16-correction2c.json` (0 mismatches) |

Current static18: `expected18-source-correction-v4.json` in this packet
(supersedes v1 `e00ccd`, v2 `04b7b4b9`, v3 `e98e9df6`; all preserved as history
via diffs; old `expected18-draft.json` untouched). P1/observer hashes unchanged
since correction start (`cdd69`/`79a339`); only the test file evolved
(`c7ba` → `e00ccd` → `04b7b4b9` → `e98e9df6` → `d3224797`). 0 schema/P2R/
config changes. Complete test diff vs R2 baseline: `test-c7ba-to-d3224797.diff`.

Inherited15 confirmation: 15 static18 entries excluding P1 module and 2 new
P2V paths all equal P2R `expected16-correction2c.json` entries (script-checked,
0 mismatches). 84 cache guard facts: full3 `run_p2v_b4.post.json`
`cache_detail` holds exactly 84 `{sha256,bytes,mode}` entries; PRE/POST status
102 rows each; cache prefix stayed absent with bytecode writes disabled; no
source cleanup.

## 2. Test method → actual helper/injection coverage (final v4, 13 methods)

All behavioral methods call actual `observe_current_authority` (+
`prepare_proposal`/`validate_proposal`/`capture_retention`/`verify_retention`/
`_scope_review_for`/`_compare_supplied_to_rederived`) and assert semantic
result/error + immediate no-write/injected-only delta BEFORE repair.

| Method | Subcases → actual predicate / injection point |
|---|---|
| `test_public_api_has_no_caller_token` (probe) | signature has exactly 5 params, no mode/verified_set/token/context/dest_policy |
| `test_error_shape_no_owned` (probe) | `CurrentAuthorityError(code,phase,detail)` shape, no `owned`, no single-string ctor |
| `test_longform_observe_needs_scope` | actual longform recipe `_complete(_chain())`→`_state_path`→`_advance_to_validated_draft`→`_authored(chain,worker)` + `narrative_sections` delta → P1 stage/prepare/validate → capture → observe NEEDS_SCOPE + SHA bindings + no-write |
| `test_weekly_observe_scope_bound_after_capture` | ordinary-without-block (scope check removed + rehashed) → NEEDS_SCOPE + ref; after-capture valid scope outside `retained/` → SCOPE_BOUND; REJECT → `SCOPE_NOT_WITHIN_AUTHORITY`; full no-write each |
| `test_p1_baseline_and_postcapture_refusal` | post-capture prepare + validate → exact `RETENTION_DEST_CONFLICT` + no-write each; observer NEEDS_SCOPE |
| `test_mutable_persistence_positive_current_negative` | COPY-policy receipt asserted; live +1B → P2R VERIFIED vs observer refuse; files+special+head+status no-write BEFORE repair |
| `test_keep_drift_refuses_both` | KEEP +1B → RetentionError + CurrentAuthorityError; full no-write BEFORE repair; positive after |
| `test_r1_active_owner_and_stale_refuses` | genuine non-emitted Python comment + `refresh_mechanical_evidence` via fixture code + same-byte fixture-code proof + fixture-code prepare (ACTIVE) + fixture-code observe NEEDS_SCOPE; 2nd comment+refresh (supersedes) → stale refuses on honest earlier guard `REF_DRIFT` (KEEP recheck preempts BASIS; documented) + no-write |
| `test_real_control_change_and_artifact_head` | real contract-file +1B → observer refuse + full no-write BEFORE repair; `docs/` artifact commit → conditional accept + no-write |
| `test_retained_missing_extra_empty_dir` | missing COPY → RetentionError + observer refuse; extra `retained/late-file.json` → `INVALID_RETENTION`; `retained/before/empty-dir` → `INVALID_RETENTION`; full snapshots BEFORE restoration each |
| `test_alias_fifo_no_read_and_late_addition` | alias leaf → `PATH_ALIAS\|TREE_ALIAS\|PROPOSAL_LAYOUT` with timeout; FIFO → `os.open` leaf tracking (never opened) + 30s timeout + special inventory + no-write; mid-call (after `_final_full_receipt_recheck`, before final): control → `CONTROL_DRIFT`, edition empty-dir → `EDITION_DRIFT`, retained extra → `INVALID_RETENTION`, KEEP bytes → `PIN_DRIFT\|STABILITY\|REF_DRIFT\|COPY_DRIFT`, scope rewrite (after `_pin_proposal_layout`) → `STABILITY_VIOLATION` (edition-snapshot preempts SCOPE_DRIFT; documented); injected-only deltas BEFORE repair |
| `test_scope_invalid_matrix` | malformed → `SCOPE_UNREADABLE`; non-PASS → `SCOPE_ORDINARY_INVALID`; wrong-before → `SCOPE_WRONG_BEFORE`; wrong-after → `SCOPE_ORDINARY_INVALID\|SCOPE_WRONG_AFTER\|SCOPE_DIGEST`; stale-upstream → `SCOPE_STALE_UPSTREAM`; REJECT/OWNER → `SCOPE_NOT_WITHIN_AUTHORITY`; empty change_summary → `SCOPE_BLOCK_SHAPE`; empty evidence → `SCOPE_ORDINARY_INVALID` (schema preempts block-shape; documented); bad scope check → `SCOPE_CHECK_NOT_PASS\|SCOPE_ORDINARY_INVALID`; tamper-no-rehash → `SCOPE_ORDINARY_INVALID` (loader digest guard; documented); 4 shared comparator refusals (`HEADER`/`BASIS`/`RETENTION`/`PROPOSED_BYTES_MISMATCH`) on real prepared data; full no-write each |
| `test_close_fault_and_no_write` | success + `/proc/self/fd` leak check; success-path `_Session._close_all` fault (stack-checked, 3rd call = outer final, real-close-then-raise, no leak) → `CLOSE_FAILED`; pre-observe KEEP primary (`REF_DRIFT` at RETAINED) + outer `_close_all` fault (2nd call) → primary `REF_DRIFT` preserved + `secondary closes` attached + injected-only delta BEFORE repair; success after each |

## 3. Runtimes / failures / skips (exact, from durable B4 evidence)

- Smoke1 `evidence-20261015T213000Z-smoke` (manifest v1): 1/2 — longform ok,
  weekly FAIL on Co-Worker A's own bogus capture no-write assertion (capture is
  a writer). Preserved; fixed by retained-only foreign-write check (v2).
- Smoke2 `evidence-20261015T213500Z-smoke2` (manifest v2): **2/2 OK in 867.068s**,
  child_rc=0 wrapper_rc=0, 0 skips.
- Full1 `evidence-20261015T220000Z-full` (manifest v2, orphan: wrapper killed by
  tool-timeout, POST guards absent): 9/13 in 5404.048s — 4 honest mismatches:
  edition duplicate injection, close secondary preemption, R1 BASIS→REF_DRIFT,
  scope empty-evidence block-shape→ordinary-invalid. Preserved as history.
- Full2 `evidence-20261015T223000Z-full2` (manifest v3, wrapper survived,
  exit 0 with failures): 11/13 in 5508.827s — 2 honest earlier-guard
  preemptions: scope-midcall STABILITY_VIOLATION (not SCOPE_DRIFT),
  digest-tamper SCOPE_ORDINARY_INVALID (not SCOPE_DIGEST_MISMATCH). Preserved.
- Full3 `evidence-20261016T000000Z-full3` (manifest v4, wrapper survived):
  **13/13 OK in 5523.310s**, child_rc=0 wrapper_rc=0 post_errors=[],
  0 skips/failures/errors. PRE/POST: HEAD `409b292…`, tree `8ce36998…`,
  102 status rows, 84 caches, `/usr/bin/python3` 3.14.4.
- No old25/36 reruns, no decorative suites, no optimized-mode run.

## 4. Failure diagnosis discipline (all preserved, none weakened)

Every red run was diagnosed to the actual operative predicate; expectations
were corrected to honest earlier guards with explanatory comments, never
broadened to generic catches: capture-writer foreign-write check; KEEP-row
preemption of BASIS (R1 stale); schema-gate preemption of block-shape
(empty evidence); loader-digest preemption (tamper-no-rehash);
snapshot-stability preemption of scope-drift (in-edition scope file);
`_close_all`-boundary targeting after preemption analysis. No source defect was
found in P1/observer through all runs; all fixes stayed test-only within 2A1M
(test path remains Added vs 409; no new paths).

## 5. Complete18 patch + saved-patch apply proof (final pins)

- GEN `evidence-20261016T000000Z-gen2` (B4 `gen_complete18_b4.py`
  `bd6c2e8f…`, absolute-path invocation): exit 0 —
  `complete-p2v-18path.patch` **942823B**, saved hash
  **`71d5154d5de422c22faf53a48288cbeb209adde57fcc84320aff20078005fb52`**,
  disposable-DB/index generation only (no active index).
- PROOF `evidence-20261016T000000Z-proof2` (corrected local `proof_apply18_b4v2.py`,
  see §6; `--source` P2V candidate byte-copied to `clean409-copy`): exit 0 —
  `APPLY_PROOF_OK head=409b292756dd1277b9dfae87679934c0d2ce251c files=18
  patch=71d5154d5de4`; applied freeze HEAD/tree `409b292…/8ce36998…`, 18 files
  match static18; candidate verified unchanged after proof; no archive/fake-root/
  active-index/candidate commit.

## 6. Tool failures → corrections (originals preserved, never edited)

- B4 GEN with relative `--outdir` fails (`disposable read-tree rc=128`,
  relative `GIT_INDEX_FILE` resolved inside repo). Preserved in
  `evidence-20261016T000000Z-gen/`. Workaround: absolute `--outdir` (gen2
  green). Reported as tool limitation; no tool edit.
- B4 `proof_apply18_b4.py` (`bff8dff3…`) has two genuine bugs: (i) SyntaxError
  `nonlocal code` on parameter `code` in `_emit` (process never starts);
  (ii) missing `if __name__ == "__main__"` guard (script no-ops RC=0).
  Preserved byte-identical under `verification-tools/`. Corrected local copy
  `proof_apply18_b4v2.py` (`6fd12225…`: 6-line provenance header + 1-line
  removal + 3-line guard) used for proof2 green. B/Root may adopt or replace;
  the original was not modified.
- Proof `--source` must contain all18 for the source-freeze guard: P2R-active
  (16-file) refused honestly (`freeze lstat failed` on missing observer file;
  evidence preserved in the removed proof2 dir, then reused path); P2V
  candidate as source is correct (byte-copied, verified unchanged).

## 7. Evidence paths (all under `notes/rephase-1-dm021-p2v/source-correction/`)

- `preserved-before/` (cdd69/79a339/c7ba + draft manifest + original reports)
- `expected18-source-correction.json` (v1) / `-v2` / `-v3` / `-v4` (final) +
  `test-c7ba-to-*.diff` chain + `preservation-manifest.json`
- `evidence-20261015T213000Z-smoke/` (1/2 fail, preserved)
- `evidence-20261015T213500Z-smoke2/` (2/2 OK)
- `evidence-20261015T220000Z-full/` (orphan 9/13, POST-less, preserved)
- `evidence-20261015T223000Z-full2/` (11/13, exit 1, preserved)
- `evidence-20261016T000000Z-full3/` (**13/13 OK**, exit 0)
- `evidence-20261016T000000Z-gen/` (GEN refusal, preserved) /
  `evidence-20261016T000000Z-gen2/` (patch `71d5154d…`)
- `evidence-20261016T000000Z-proof2/` (**APPLY_PROOF_OK**)
- `proof_apply18_b4v2.py` (corrected tool copy) + this `final-report.md` +
  earlier `correction-report.md` (scaffolding preserved; its §8 STOP and
  pre-run pins now superseded by this final verification, original kept).

Whole NOT_READY, step4/B3 OPEN, audit unstarted, DM021 OPEN. Ordinary
Commit/Push Human-owned. Awaiting root + fresh author-independent review.
