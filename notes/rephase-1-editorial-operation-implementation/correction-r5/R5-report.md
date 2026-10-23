# R5 return — prescribed contract gaps (strict JSON / close / canonical State / export / SHA pin)

## 0. Prior final-witness ses_ea0e26595ffe + partials (before new tests)

- `ps aux` shows no live python test child (only opencode web, redis, system). No duplicate live child to avoid.
- Provider `server_error` is not a test verdict. Current packet `correction-r4e/` partials are completed logs, not ongoing:
  fixture weekly/longform exit 0, lifecycle weekly/longform exit 0, fault weekly/longform exit 0,
  export manual/inert/old exit 0, export pr-positive exit 1 (expected refusal: `PR_POSITIVE_FAIL refused: exactly one changed ... found 0`),
  pr-inert/unrelated exit 0. No partial writes in progress.
- Source hashes: DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60` HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` dirty 57 (tracked M + untracked editorial/tests/__pycache__/tmpvr07sdme).
  Frozen SOURCE `/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60` HEAD `4191503bfe1bd6aadd90a107dc4fd7c601e53f6c` tree `8ecd325c762bd70b37b847ad831234245345aa20` clean, manifest 719.
- Storage before copies: `/tmp` 7.5G 6.0G 1.6G 80%, `/` 469G 90G 355G 21%. New snapshot on root disk (`/home/eariver/tmp-opencode`) due to `/tmp` quota (EDQUOT on `.git/objects` copy). No autodelete (only own failed `/tmp` partial removed).

## 1. Before-code gap path/lines (actual DST, no blind rewrite)

- Gap1 strict JSON:
  - `survey_schema_v2.py:126-185` `load_schema`/`validate_instance`/`load_and_validate_json` used plain `json.loads` (last-wins), no duplicate hook; cache holds only validators (no instance caching) but schema duplicates would last-wins cached.
  - `survey_editorial_publication_v2.py` high loads lenient: `506 core.load_json(staged)`, `583 state`, `593 cfg`, `628 proposal`, `640 staged_manifest`, `685 gen_receipt json.loads`, `724 scope json.loads`, `1038/1100 spec load_and_validate`, `1443 _js.loads staged`, `1508/1518/1527/1544 _js2.loads state/profile/proposal/gen`, `1644/1948 cfg core.load_json`, `1914/1924/1932 _jc.loads checks/state/staged`, `2198 _js3.loads _load_json_rel`, `2342 sealed load_and_validate`, `2463/2483 _jb.loads build/state`, `2519 _jc2.loads chain`, `2581 _jp.loads profile`, `2709 _ji.loads intent`, `2775/2826/3022/3032/3153/3180/3199 _ja.loads state/proposal/retained/new/post`, `3236/3302/3325 _jr.loads resume`, `3447 cfg core.load_json`; plus supplied semantic/visual/QA deps via `reader.validate_review_record`/`quality.validate_bundle`/`gate.validate_reader_surface_gate`/`publication.validate_candidate` without strict pre-parse.
- Gap2 close:
  - `survey_editorial_publication_v2.py:328-357 _read_bytes_bounded` finally `os.close except OSError: pass` (swallow, primary preserved secondary lost).
  - `:360-485 _exclusive_write_bytes` finally same swallow.
  - `survey_agent_control_v2.py:1939-1962 _exclusive_create_record_bytes` `with open(xb)` auto-close masks (body error + close OSError chains as context, close alone raw OSError not AgentControlError).
  - `:2052-2065 _atomic_replace_state_bytes` same `with open(tmp,xb)` mask.
- Gap3 canonical State:
  - `survey_editorial_publication_v2.py:563 validate_editorial_receipt` (`state_rel` lexical+safe only, no Profile/config source_root/authoritative_filename expected-path equality, no retained/cloned refusal).
  - `:2324 validate_prepared_set` same (relies on receipt only, no direct canonical check). `verify_activation_history` separate (record-only, no State) correct.
- Gap4 export:
  - `.github/workflows/survey-production-v2-export-publication-preview.yml:79-90 _all_states` `glob without recursive=True` (** non-recursive), no canonical filter, no retained/history exclusion, no symlink lstat rejection, `json.loads` lenient before `_selection_for_state`; matching by `issue_id` alone conflates retained copy; ambiguous only on count!=1.
- Gap5 SHA pin:
  - `survey_orchestrator_v2.py:154-170 _configured_expected_artifacts` path-only, no SHA vs pin.
  - `:173-201 _configured_gate_inputs` path check only, `core.sha256_file` recorded never compared to `cand_ref[sha256]`.
  - `survey_handoff_v2.py:67-82 expected_output_contract` + `111-123 build_handoff` path equality only.
  - `survey_human_gate_v2.py:249-303 _reviewed_artifacts` path check + PDF drift only, no candidate SHA vs pin.

## 2. Fixes (dedicated Edit/Write only, no shell source edits)

- Gap1: `survey_schema_v2.py` added shared bounded strict parse (`_strict_object_pairs`, `parse_json_strict_bytes`, `loads_strict`, `load_json_strict`, `load_and_validate_json_strict`); made `load_schema`/`validate_instance`/`load_and_validate_json` strict (valid legacy still valid, duplicates refused before digest/schema, no State/result caching, cache still validators only). `survey_production_v2.py:core.load_json` made strict via local `_strict_object_pairs` (valid legacy still valid). High added `_strict_json_from_bytes/_strict_json_from_text` and replaced all 30+ `json.loads`/`core.load_json` authority loads with bounded O_NOFOLLOW + strict (receipt/state/cfg/proposal/staged/scope/checks/bundle/manuscript/gate/candidate/build/retention/chain/profile/intent/new/post); added strict pre-parse before `reader/quality/gate/publication` validators for semantic/visual/QA result docs and seal roles; source-config duplicates now refuse (never cache last-wins); unknown branch refuses (strict before branch).
- Gap2: High `_read_bytes_bounded` now captures primary, explicit close with `READ_CLOSE_COMBINED`/`CLOSE_FAILED` (ordered primary+secondary, never suppress, never mask). `_exclusive_write_bytes` same with `WRITE_CLOSE_COMBINED`/`CLOSE_FAILED`, preserves owned partial/unknown, no referenced delete. Agent `_exclusive_create_record_bytes` and `_atomic_replace_state_bytes` temp creation replaced `with open` with explicit `O_RDWR|O_EXCL|O_NOFOLLOW` + write/fsync/fstat/lseek/readback + explicit close combining primary+secondary as `AgentControlError` (fsync/close surfaced typed nonzero, no CAS guarantee). Kept byte/inode checks, partial preservation, old/new/unknown observed.
- Gap3: Added `_require_canonical_current_state` (validated Profile/config source_root/authoritative_filename + exact `state_rel` equality/no aliases, rejects `retained/history/copy/deep`, resolves no-alias). Called in `validate_editorial_receipt` and `validate_prepared_set` (inert still valid against old current State, no requirement target already active). `verify_activation_history` unchanged (historical only).
- Gap4: Workflow `_all_states` now `recursive=True`, filters to exact `sources/<issue>/production-state.json` + `specials/<issue>/production-state.json`, excludes `retained/history/copy`, lstat-rejects symlinked files/ancestors, regular-file only. `_strict_loads` (duplicate refusal) for State/config/candidate/Profile; `_selection_for_state` checks canonical + Profile-derived expected path; `_issue_of_candidate` strict + symlink rejection. Manual/PR add Profile source_root cross-check (candidate under source_root, retained/history refused, alias refused), exactly one issue/candidate, active only, no latest fallback/unknown toleration.
- Gap5: Orchestrator `_configured_expected_artifacts` (active pin when file exists, SHA must match, no fabricated SHA for absent futures) and `_configured_gate_inputs` (SHA+path vs low pin, not path-only) now compare `core.sha256_file == cand_ref[sha256]` and refuse drift. Handoff `build_handoff` same SHA+path check (loader+producer agree). HumanGate `_reviewed_artifacts` same SHA check. No caller-verified dict (all refs reloaded + hash-checked via low).

## 3. New SOURCE freeze (untouched after commit)

- NEW SOURCE: `/home/eariver/tmp-opencode/jgas-editorial-r5-20261022T120000Z/candidate-partial-b40de60` (cp -a from frozen, independent inodes, no hardlinks).
- Overlay: 8 fixed files (schema/high/agent/core/orchestrator/handoff/humangate/export workflow) + 1 new test `tests/test_survey_editorial_r5_gaps_v2.py`.
- Commit: `0e092f94ef0d4974a5fb1716296505685f07e384` tree `2129060ba2d6ff40219870189b11226d0c659f0d`, 720 files (719+1), `git status` clean, origin `https://example.invalid/workerR4d-r4d-snapshot.git` inert, no `objects/info/alternates`, no `__pycache__`/residue/tmp, `find -links +1` empty, 4-sample nlink=1, `count-objects` 769/0 packs.
- Manifest: `correction-r5/source-manifest-r5.json` FULL valid JSON (720 pins SHA/bytes/mode, head/tree/count). Before bytes: `correction-r5/*.pre-r5` (8 files). No reconstruct commit.

## 4. Authoritative runs (regress clone @ 0e092f9, no DST authority, TMPDIR on root disk)

- Clone: `/home/eariver/tmp-opencode/jgas-r5-regress-20261022T120000Z/candidate-partial-b40de60` @ 0e092f9 clean (cp -a, independent).
- R5 gaps `test_survey_editorial_r5_gaps_v2` 12/12 OK (strict nested/same-value/duplicate-not-cached/valid-legacy, close success/write/agent fsync/close, canonical accept/retained-reject/historical-separate, export canonical/symlink/ambiguity, SHA mismatch/future-no-SHA).
- Legacy revalidation `test_survey_publication_revalidation_v2` 31/31 OK.
- Agent+cache+low `test_survey_agent_control_v2` + `test_survey_schema_cache_v2` + `test_survey_publication_set_v2` 29/29 OK (agent 5, cache 6, low 18).
- Faults `test_survey_editorial_activation_faults_r4c` 3/4 in regress on ext4 (1 failure `test_foreign_same_byte_record_identity_refused` due to ext4 inode reuse after unlink+rewrite same inode 20464300, not code; same test 4/4 OK in DST on tmpfs). Group-C plain-function file has 0 unittest tests (needs pytest, signatures preserved, not run).
- P1/retention/current-authority/staged full suites NOT rerun (save resources, no 2-route build matrix until root reviews; P1 temp `git add` needs TMPDIR on root disk and 719+ tracked schemas, which regress clone now has, but heavy builds deferred).

## 5. Pins for root

- NEW SOURCE HEAD `0e092f94ef0d4974a5fb1716296505685f07e384` tree `2129060ba2d6ff40219870189b11226d0c659f0d`, 720 files, manifest `correction-r5/source-manifest-r5.json`.
- Regress clone @ 0e092f9 clean (same HEAD/tree).
- Public APIs unchanged signatures (7 high + low selection/resolver, agent writers, orchestrator/handoff/gate resolvers); behavior now strict/close/canonical/SHA-pinned.
- Blocker: none new (narrow correction only). Remaining: second pre-Preview correction on 0e092f9, R1×2 anchor/refuse-after, active vs historical readback, full §9 negatives (wrong seal/manuscript/Candidate, old-Candidate-after, inert-not-adopted, unknown branch, research change, old/new reader, equal-SHA-different-path, stale/failed/missing reviews, build failure/drift, seal role/unknown/dup, anchor error/cycle/depth/sequence, State/predecessor drift, approved/foreign Candidate, canonical-writer-after, every write/close/late-readback with observed delta + resume/healthy control), export full execution on 0e092f9, P3S branch test, P1-9/retention-25/current-14/staged-26 on 0e092f9, whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022 OPEN. No whole PASS claimed. Stop at Human Commit Point; ordinary Commit/Push Human-owned.
