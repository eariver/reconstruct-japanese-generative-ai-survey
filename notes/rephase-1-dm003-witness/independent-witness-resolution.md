# DM-003 supplement — scoped independent resolution (file-only, no execution)

Reviewer role: scoped independent resolution of NEW corrected DM-003 evidence only.
Not source implementation. No source/tests/runtime execution, no network/Git
mutations, no agents. Worker/root files untouched. Original
`independent-witness-review.md` (CHANGES_REQUIRED) stays intact as the initial-packet
record. Shipping 222 unchanged. This resolution executed nothing; it only read files.

Review mode: read-only file review of `correction-decision.md` and
`dm003-supplement-20261003T202828Z/{REPORT.md,run_dm003_supplement.py,
evidence/supplement-manifest.json,per-scenario ops/guards/byte inventories}`.
No wall-clock/Git/process execution is claimed. Pins below are file-recorded values.
Scope is witness/disposition only: single synthetic Special scaffold per scenario,
no Weekly/all-profile, no FROZEN advance, no production operation.

## Sources read

- `notes/rephase-1-dm003-witness/correction-decision.md` (22 lines).
- Supplement `REPORT.md` (56 lines), `run_dm003_supplement.py` (583 lines, full read),
  `evidence/supplement-manifest.json` (header/canonical/limits; long single line,
  tail truncated at Read limit — REPORT + ops/diffs supply the remainder).
- Per-scenario: `evidence/S1-R2/ops.json` (21 ops), `S2/ops.json` (13 ops),
  `S3/ops.json` (12 ops); `guard.before/after.json` for S1-R2/S2/S3;
  `guard.baseline.json`; `run-manifest-S1/S2/S3.json` (S3 fully read);
  `summary-S1-R2/S2/S3.json`; `S1-FAILURE/SCENARIO-FAILURE.traceback.txt`;
  inventories `s1-00..07`, `s2-00..03`, `s3-00..01`; diffs
  `s1-approval/freeze/stage-window`, `s2-removal/approval/freeze/stage-window`,
  `s3-wrapper-window`; metas/bin markers `s1-candidate-c1/c2`,
  `s1-orphan-vs-report-rows`, `s1-direct-mismatch/surplus` tracebacks,
  `s3-approval-a1/a2`, `s3-candidate-c1`, `s3-wrapper-outcome`,
  `s3-wrapper-window`, `s3-state-errors`, `s3-stage` traceback.
- Actual 222 source (read-only, witness copy):
  `survey_agent_control_v2.py:396-423`,
  `survey_profiled_freeze_v2.py:33-67`,
  `survey_stage_validation_v2.py:132-151`.
- Prior review header (`independent-witness-review.md:1-15`) to confirm intactness;
  no re-read of full initial packet beyond correction scope.

## Identity / isolation (file-recorded)

HEAD `222a37e9ee2aa96724a491f2c04c2583a86b9650`,
tree `dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`,
parent `ff6c67f68e12b3093901248219f2de2872e54d73`,
branch `codex/dm001019-freeze-implementation`.
Five source hashes identical across `guard.baseline.json` and all reviewed
S1-R2/S2/S3 before/after guards:
`30042258ae01e153507461e51e356c61ae385f1dd33085ca9187586d78fac317`,
`5e38b86b609e2726f9a3af6f0686426b4237b9d6e388e39d8efc360f6ede4bc0`,
`092f1a2db8a728684cd2c5bcee80d8ef01e5353091cc03e732e5fc5b10a07c05`,
`f3b73d857a7281a45fab807659acd8f7a1d869d52ef05e360af703a7626ceec5`,
`0f2393dadab72cecba5672b945d2be35e41089e4face5f0e2753b84a6a4b5806`.
Reviewed S1-R2/S2/S3 guards show `tracked_changes: []` and `status_lines: []`
(cleaner than initial packet's `??` leftovers); `guard.baseline.json` retains
`?? __pycache__` disclosure. Harness scrubs `GIT_DIR/WORK_TREE/CEILING/
COMMON/PREFIX/INDEX` (lines 41-49), pins offline env, enforces
`sys.dont_write_bytecode`, refuses pre-existing fixture paths (lines 199-201),
cleans only witness-owned dirs (212-216), runs exactly one scenario per argv
(no default; unknown/empty exits 2). No candidate commit/network/generic repair.

## S1 — genuine byte-distinct C2, exact path+hash selection, genuine no-writes

Verified:
- C2 via actual `_build_special_second_chain` over same canonical
  source/manuscript/PDF: `s1-candidate-c1.meta` sha
  `619ff4cf034c1597…` (1525 B) vs `s1-candidate-c2.meta` sha
  `c09183a1e7bfa04b…` (1531 B) — `assert c2_sha != c1_sha` (harness:264),
  distinct paths, equal pdf-sha, both `validate_candidate` PASS (258,262).
  `rival-byte-distinct-valid` op records truncated shas + pdf equality.
- Active C1 pins unchanged by second-chain build: `named_pre` captured
  post-approval (248-249), re-compared post-build equal (271);
  `c1_path.read_bytes() == c1_pre_bytes` (272);
  `second-chain-adds-only-4` asserts exact new-file set
  (bundle-2, semantic-2, visual-2, candidate-2) with no recognized-input rewrite
  (276-281). Saved `s1-candidate-c1/c2.bin`, `s1-state-post-approval`,
  `s1-approval-a1.bin` + inventories `s1-02/s1-03`.
- Exact-bind rejection: `publication.build_freeze(C2,A1)` raises exact
  `ValueError: Publication Preview approval does not bind the exact Publication
  Candidate being frozen` (291-292, raw traceback at `publication:189`),
  rival outputs absent, `State` bytes identical (298-300). Not a broad catch:
  exact-message assert, else `AssertionError`.
- Orphan retarget is schema-valid yet path-AND-sha divergent:
  `s1-orphan-vs-report-rows.json` report
  `(publication-candidate, …/publication-candidate-v2.json, 619ff4cf…)`
  vs orphan `(…, …/publication-candidate-2-v2.json, c09183a1…)` — both
  components diverge, fixing initial same-sha indistinguishability.
- Winner is path+hash, not sha-only: `freeze[…path] == C1 rel` AND
  `freeze[…sha256] == c1_sha` (336-337); direct `_prior_artifacts`
  `sel == c1_path` object equality + `sha256_file(sel) == c1_sha` (339-343).
  Surplus key hits exact `StageValidationError: unexpected current stage
  artifacts: publication-candidate` (352, traceback at `stage_validation:212`
  via `validate_stage:621`), no surplus report (357).
- Genuine windows (inventory `assert_diff` exact sets, not self-compare):
  approval `{+approval, ~State}`, freeze `{+freeze,+manifest}` added 2/modified 0,
  stage `{+report-s1}` added 1. `s1-approval/freeze/stage-window.diff.json`
  match ops counts. Correct admission PASS with report-only window.
- 21 ops, `summary-S1-R2.json COMPLETE unexpected []`.

This withdraws and replaces F1: byte-distinct same-PDF conflict now exercised;
old C6/C7 correctly retained only as narrower distinct-path evidence per REPORT.

## S2 — missing-sibling positive with four precise write windows

Verified:
- Removal window exactly `{-VALIDATED_DRAFT.json}` (389-390,
  `s2-removal-window.diff.json`); sibling is the consumed unmapped record
  (`s2-orphan-consumed.bin` saved pre-removal).
- Approval window exactly `{+approval, ~State}` (`s2-approval-window.diff.json`:
  added `gates/publication-preview-approval.json`, modified
  `production-state.json`); freeze window exactly `{+freeze,+manifest}`;
  stage window exactly `{+report-s2}`. Every other fixture byte identical via
  full inventories `s2-00/00b/01/02/03` + saved `s2-state-post-*`,
  `s2-freeze-record/manifest/stage-report` bytes. Sibling never recreated
  (`orphan-still-absent` + cleanup asserts roots gone).
- 13 ops, `summary-S2.json COMPLETE unexpected []`. Guards before/after exact
  222 with `status_lines: []`.

This withdraws and replaces F2 for the central positive: real snapshots exist
here. Old C1/C3 correctly left narrow with no retroactive oracle credit per
REPORT (“old C1/C3 keep their narrower operation-success scope”).

## S3 — split-refs wrapper characterization (finding, not green oracle)

Verified:
- Fresh approved State, `freeze/manifest` asserted absent pre-split
  (`outputs-initially-absent`), so post-split wrapper is tested before any write.
- A1/A2 each standalone `validate_preview_approval` PASS, distinct ids
  (`A1=…28cf2bd1… A2=…3417b2ee…`), both bind same C1 (ops + saved
  `s3-approval-a1/a2.bin`). Split is human→A2, checkpoint stays canonical A1
  (saved `s3-state-pre-split/split.bin`).
- `validate_agent_state == []` (`s3-state-errors.json []`, asserted exact).
  Source-grounded: `agent:402-416` validates only
  `checkpoint_provenance[publication_preview]` canonical path/sha + approval
  validity; no `human_gate_provenance == checkpoint_provenance` comparison exists.
- Post-split wrapper BUILT (not rejected): op `wrapper-after-split`
  `CHARACTERIZED-BUILT via …/publication-preview-approval-rival.json`;
  `s3-wrapper-outcome.json outcome BUILT`, `frozen_approval_path` = rival,
  `frozen_approval_sha256 2567643b…` == A2 meta (`2567643b…`, 701 B) ≠ A1 meta
  (`139288ce…`, 695 B); `frozen_candidate 7bf983b2…` == C1 meta (`7bf983b2…`).
  Window `added=[freeze,manifest] modified=[] removed=[]`; State stable
  (inventory diff proves no State modification; `s3-state-post-wrapper.bin` saved).
  Harness correctly characterizes (BUILT/REJECTED branches, exact recording),
  not a PASS claim; `main()` treats `CHARACTERIZED-*` as non-unexpected.
- Stage then rejects exact `StageValidationError: Human Preview and checkpoint
  approval authorities disagree` (traceback at `stage_validation:139` via
  `:160/:622`), no report written. Correct fail-closed backstop, but after the
  writer already minted a pair.
- 12 ops; `summary-S3.json COMPLETE unexpected []` means characterization
  completed, not that split was refused.

This withdraws and replaces F3 and the premature initial “not defect”:
S3 shows the writer silently admits split authority (here same-C1, so impact is
approval-identity divergence; candidate-divergent admission was not tested and
must not be inferred beyond the pair written).

## Harness / raw / scope checks

- No self-compare: S1/S2/S3 use pre/post inventory `assert_diff` with exact
  allowed added/modified/removed sets; C1 bytes vs saved `c1_pre_bytes`;
  `named_pre` pre/post equality; Path-object + hash selection. Initial
  C1:337-340 / C6:562 tautologies are absent here.
- No broad-catch PASS: negative helpers assert exact type+message
  (`ValueError` bind, `StageValidationError` extra-key/disagree) and raise
  `AssertionError` on wrong outcome; orphan schema `except` records (not ok);
  S3 wrapper records both outcomes as `CHARACTERIZED-*`.
- No fixture-invalid run: fresh `SP-DM003-S1/S2/S3` issues, refusal on
  pre-existing paths, `cleanup` asserts removal, separate `S1|S2|S3` argv with
  per-scenario `run-manifest-*.json` (argv/cwd/env/HEAD/harness+fixture shas).
  First S1 attempt failure (`named_pre` captured pre-approval ordering bug)
  preserved raw in `S1-FAILURE/` with canonical `S1-R2` rerun mapped in
  `supplement-manifest.json` — proper correction hygiene, no overwrite.
- Raw results/exits/artifact scope: `ops.json`, `guard.before/after.json`,
  full inventories + `.bin` + `.meta.json` (including non-JSON bytes),
  exact tracebacks, `supplement-manifest.json` (46 ops = 21+13+12, operations
  not methods). 46-count is truthful; no method inflation.

## Disposition

- **Orphan-map question (DM-003 selected path): nonblocker.** S1 (byte-distinct
  rival ignored; exact C1 path+hash selected) + S2 (missing sibling with exact
  four windows) + initial C2/C3 operation-success (narrowed) jointly establish
  the omitted `checkpoints: []` sibling neither supplies nor blocks the Freeze
  path; typed Preview approval carries the exact Candidate and
  `_prior_artifacts` never consults the sibling. No generic
  provenance scanner/resolver justified.
- **Narrow defect (filed, not repaired): missing human==checkpoint equality gate
  in `_safe_state_profile` / `validate_agent_state`.** Source trace:
  state validator checks checkpoint side only (`agent:403-416`);
  wrapper consumes human side after that check (`profiled:59-62`);
  only stage enforces `human != checkpoint → disagree` (`stage:138-139`).
  S3 byte proof (frozen approval == A2 ≠ A1, State unchanged, stage then rejects)
  confirms the writer mints outputs from split authority. Impact in-witness is
  bounded (same-C1 pair; stage blocked FROZEN advance; no advance attempted on
  rejected stage). Candidate-divergent split consequence was not measured.
  No runtime repair in this unit (not authorized per correction-decision);
  root/Human select repair scope after this resolution. No DM-004, no adoption
  inference, no whole-CLI/suite acceptance.
- **Withdrawals complete:** infeasibility invariant, C1/C6 tautological no-write
  ops, C7 sha-only winner, C5 “not defect / rejects before any write”
  are all explicitly withdrawn in `supplement-manifest.json correction_scope`
  and REPORT §§S1-S3; affected initial C1/C3 observations remain narrowed with
  no retroactive snapshot credit. No further F1-F3 work is owed for disposition.

## Verdict

**BOUNDED_PASS for witness/disposition ONLY** (NOT runtime, NOT whole-candidate
acceptance, NOT shipping approval).

Remaining findings are exactly the filed narrow defect above plus its bounded
limits (same-C1 measured; candidate-divergent split unmeasured; single Special
synthetic scope; no FROZEN advance). No source patch is planned in this unit.
New file only; all prior packets, worker/root files, and shipping 222 untouched.
