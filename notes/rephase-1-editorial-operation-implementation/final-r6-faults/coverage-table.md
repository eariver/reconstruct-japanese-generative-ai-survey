# R6 FINAL matrix — coverage table (no source edits, synthetic/NO_GO)

Final SOURCE: `.rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60`
HEAD `ce90246b907c86e9bdeb930dec0e83a5637f2805`, tree `53349a4efbdd5e3b4153a8e5975101fdd59f132b`, 720 files, `status` only `?? scripts/__pycache__/` (untracked cache preserved/excluded, no clean claim, no tracked dirty).
Bases (originals readonly): `final-r6/weekly-inert` State r1 `8c2d0f...` r2 ABSENT set2 `d2d538...`, `weekly-prelc` State r2 `baf841...` VALIDATED_DRAFT pending; `longform-inert` r1 `448513...`, `longform-prelc` r2; `weekly/longform` RELEASED r2 (2×2 + 3 advances). Manifests `final-r6-positives/inert-manifest-*.json`, `final-epoch-*.json` same HEAD. Old 0d/b54/R5 not used for final epoch.
Scratch ONLY `.rephase-1-editorial-runtime/final-r6-faults/` (ROOT approved, 993M+), `tmp/`+`pycache/` under it. Every fixture own `.git`/toplevel NOT reconstruct, `cp -a` no hardlinks/alternates/inert origin. ENV no-bytecode BEFORE Python (`-B`, `PYTHONDONTWRITEBYTECODE=1`), per-case subprocess `PYTHONPATH=<fixture>` `cwd=<fixture>`. Scripts BEFORE run via dedicated editor. Raw cmd/cwd/exit/dt/stdout/stderr/source pins/fired seam/terminal in tool responses + summaries below; fixtures preserved with `FAULT_FIXTURE_README` + snapshots, never cleanup/reset/purge/rawdelete/network/commits, no `/home/tmp`/`/dev/shm`. R5b original scope preserved (not rerun where unaffected).

## R6 targeted (new code: low/high cross-binding path+SHA)

| Case | Fixture (INERT base State r1 set2 sealed) | Public entry | Fired seam / error | Write window / repair / raw refs | Exit | Status |
|---|---|---|---|---|すすめ|---|
| R6_seal_only (repeat R5b UNEXPECTED_PASS) | `r6-seal-only` (seal semantic_review → forged same-SHA path, fresh `set_sha256` via `sha256_object`, Candidate still old) | `validate_prepared_set` | `SEAL_BIND: candidate semantic_review must equal seal semantic-review (path+SHA)` | no writes, preserved, old UNEXPECTED_PASS preserved in R5b `matrix_a2` | API 0 | PASS — R6 fix verified |
| R6_target_rebind (actual reviewed TARGET sameSHA) | `r6-target-rebind` (copy SAME manuscript bytes outside `publication/` to `external-reviews/reader-manuscript-copy.json`, update `review.reader_manuscript` + `review_sha256=sha256_object(base)` + candidate `semantic_review`/`candidate_sha256` + seal `semantic-review`/`publication-candidate`/`set_sha256` consistently, leave seal `reader-manuscript` original) | `validate_prepared_set` | `CANDIDATE_INVALID: Publication Candidate semantic review manuscript drift` (candidate-level exact target, not digest preemption; `review_sha256` + `candidate_sha256` fresh so content digests pass) | no writes, preserved | API 0 | PASS — exact target path refused |
| R6_external_counter | `correction-r6/r6-external-consistent-*` (already recorded, exit 0) | R6 public positive | reviews at `P/external-reviews`, Candidate+seal consistently point there, unchanged targets | — | 0 (recorded) | PASS — permissible, no mandatory filename invented |

## TRUE accepted/authored boundary (INERT State1 healthy, P2R KEEP unchanged, fresh receipt_sha)

| Case | Fixture | Public entry | Fired seam | Window/repair | Exit | Status |
|---|---|---|---|---|すすめ|---|
| R6_accepted_profile | `r6-accepted-profile` (copy same-byte `production-profile.json` to `.../external-reviews/profile-copy.json` outside publication, change ONLY `receipt.accepted_refs` row.path + fresh `receipt_sha256=sha256_object`, P2R KEEP unchanged) | PUBLIC `validate_editorial_receipt` directly | `ACCEPTED_MISMATCH`/path-current binding (not stale State) | no writes, preserved | 0 | PASS |
| R6_authored_before | `r6-authored-before` (receipt `authored_refs` proposed-publication-authoring → `wk-r6-1/authoring-input.json` old + fresh `receipt_sha256`) | PUBLIC `validate_editorial_receipt` | `AUTHORED_MISMATCH` (distinct from rederive scope already in A_deep_reader) | preserved | 0 | PASS |

## Public prepare failure/extra input (NEW source-only wk-r6-3-fault with actual P1/P2R/scope/P2V/P3S, no rewind/overwrite)

| Case | Fixture | Public entry | Fired seam | Window/repair/raw | Exit | Status |
|---|---|---|---|---|すすめ|---|
| R6_prepare_invalid_exe | `r6-prepare-new-v3` (NEW ID, P1 new headline + P2R + scope + P2V `SCOPE_BOUND` + P3S `VERIFIED`, manuscript/toolchain specs, invalid `/nonexistent/lualatex`) | PUBLIC `prepare_publication` | `TOOLCHAIN_EXE` before transfer, no PDF forged, no publication authority | incomplete preserved, real Tool build exists (no repeat success) | 0 (refused) | PASS |
| R6_prepare_extra_argv | same NEW fixture, toolchain `argv` + `extra-input-flag` | PUBLIC `prepare_publication` | `TOOLCHAIN_ARGV must EXACTLY equal fixed recipe` before transfer | preserved, no fake PDF | 0 | PASS |

## Chain depth/cycle/chronology (public failure states intended point vs earlier refSHA preemption)

| Case | Fixture/entry | Fired seam | Window | Exit | Status |
|---|---|---|---|---|---|
| R6_chronology | `r6-chronology` (PRELC) ` _next_record_seq` | predecessor+1 (next 3, no max+1 fork, R6 fix) | read-only | 0 | PASS |
| R6_depth_normal | `r6-depth-normal` (PRELC len2) `_build_anchor_chain` len2+1 ≤32 passes | depth check passes | read-only | 0 | PASS; full 33-chain INCOMPLETE heavy (needs 33 schema-valid hash-consistent legacy chain cumulative full union synthetic NOT actual R1x33, not run) |
| R6_cycle_malformed | `r6-cycle-malformed` (r3-cycle with wrong supersedes SHA) `validate_activation_record` | SHA/drift/supersedes refusal (public malformed SHA), not cycle | preserved | 0 | PASS (malformed, not forged cycle) |
| R6_cycle_defensive | synthetic in-memory seen-set probe (private pure branch, NOT public, NOT actual R1x33) | branch probe OK | n/a | 0 | PASS (labelled, don't forge public cycle PASS cryptographically impossible w/o collision) |

## R6 IO/resume regression (same R5b matrix code *adapt params only* to R6 INERT; final epoch new set proven)

| Case | Fixture | Fault (delegate actual until exact fault, no stubs) | Fired seam / observed / delta | Exit | Status |
|---|---|---|---|---|---|
| R6_record fsync/close/combined | `r6-record-*` (INERT) `os.open/write/fsync/close` FD-tracked | `RECORD_*`/`WRITE_CLOSE_COMBINED` primary+secondary, observed old, partial preserved, State old, no deletion | 0 | PASS (representative; R5b zero/short/pre/partial/post preserved as qualified scope, bodies unchanged) |
| R6_state temp_write/replace/postread | `r6-state-*` (INERT) temp FD-tracked `os.open/write/replace/read` | `STATE_REPLACE` observed old + `POSTREAD_FAIL` observed unknown + `POSTREPLACE_FAIL` observed new (corrupt-after-replace) | 0 | PASS (temp_create/fsync/close/pre_replace in R5b preserved qualified; R6 temp_write/replace/postread/new executed) |
| R6_foreign | `r6-foreign-v2` (create replacement WHILE original exists, assert different dev/ino, `os.replace`) | `RECORD_OWNERSHIP` before State write, observed old, State old r1, no deletion | 0 | PASS |
| R6_orphan | `r6-orphan-v2` (INERT + PRELC r2 `baf841...`, State old r1 + record r2, set `d2d538...` matches) ordinary `activate` | `RECORD_COLLISION`/`INTENT_COLLISION` no r3 fork | 0 | PASS |
| R6_resume | same orphan `resume_activation` | `RESUMED` exact r2 (pointer SHA matches), strict readback VERSIONED_ACTIVE | 0 | PASS |
| R6_already | `r6-already-weekly/longform` (PRELC State r2) ordinary `activate` same set | `ALREADY_ACTIVE` readonly (hashes unchanged), LF healthy control (both routes, no double R1) | 0 | PASS |
| R6_unknown/incomplete + CLI | `r6-unknown` (State null, neither old r1 nor new r2) `resume` + CLI `resume` | `INDETERMINATE` preserved; CLI exit 2; incomplete truncated r2 `RECORD_INVALID` preserved, no auto-overwrite | API 0, CLI 2 | PASS |
| R6_record pre/partial/post + CLI validate | `r6-record-pre/partial/post` + CLI `validate-prepared-set` tampered exit 2 | `RECORD_COLLISION`/`WRITE`/`READBACK_MISMATCH`, observed old | API 0, CLI 2 | PASS (R6 representative; R5b full preserved) |

Caught unexpected failure affects overall: any `UNEXPECTED_PASS`/`UNEXPECTED_FORK` fails case (e.g., old R5b fork now fixed to COLLISION). Failures full raw not erased (fixtures + summaries preserved).

## R6 spot negatives (actual public BOUND where needed; R5b full preserved where unaffected)

`r6-neg-unknown` unknown branch PASS; `r6-neg-clone` retained/cloned `STATE_NOT_CANONICAL` vs historical valid + CLI 2 PASS; `r6-neg-review-missing/tamper/inert/dup` PASS; `r6-neg-drift/approved/oldcanon/nonpass(fresh)` PASS. R5b `A/B` full preserved per-source (tamper, reviews, Gate/manuscript, adopted, writers, etc. unchanged bodies).

## INCOMPLETE (no INCOMPLETE gaps without blocker/equivalent)
- A_deep_research true replay (got retention drift preemption; needs retention-excluded target) — preempted, not claimed deep
- A_build PUBLIC NEW-proposal full cycle already done in R6_prepare (above) — done, no longer incomplete
- B_depth33 full chain (needs 33 hash-consistent legacy chain) — INCOMPLETE heavy, static depth check + normal pass only
- B_cycle public hash-consistent (cryptographically impossible) — INCOMPLETE by design, malformed SHA + defensive probe instead
- LF deep separate (shared once + 2route positives, no double count)
- R1 both (separate healthy, not double-counted)

Internal handoff, not Human Commit Point. Production NO_GO, synthetic only.
