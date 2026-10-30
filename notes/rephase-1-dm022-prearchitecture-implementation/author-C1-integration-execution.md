# C1 integration execution — H positive + fixed source + affected suites (NO CommitPoint)

Date: 2026-10-28 UTC. Owner C1 (replacement executor, prior C1 stopped). Human whole unit continued, NO Human Commit readback. C1 owns ONLY (per coordination): `survey_versioned_renewal_history_v2.py` (H), `survey_versioned_renewal_source_v2.py` (S), `survey_versioned_renewal_v2.py` (HIGH renewal), `survey_weekly_derivation_v2.py`, `survey_longform_derivation_v2.py`, `survey_longform_generated_v2.py`, `survey_editorial_staged_source_v2.py`, `config/survey-production-v2.json`, existing C1 test helpers. No A/B/C2 source/test edits. No ordinary candidate/reconstruct commit/push, no Human readback, no Git config/network/Production/adoption/cleanup, no `git clean/reset`, no old-runner reuse, no fixture deletion, no masked timeout/non-collected PASS. Root review required, unit ongoing.

Binding: contract a345bb95 INCLUDING §11, precode assessment §5, ROOT 0425c530 INCLUDING §5 (FULL 0425c530/13788B), readiness §§8–9 FINAL-BINDING, R3→R4+5schemas→R5→R6→ROOT, astra-history-wiring-findings.md (source-only, separate from A4 bounded PASS), author-C1-historian-wiring-correction.md §§4–5 (ONE H positive pending + affected batch), A4 return (HIGH prepare/adopt WORKS 21 tests), B StateSizedRef/acceptedDrafting fixed, C2 Release fixed. Prior C1 ‘awaiting A2 HIGH adoption’ is STALE — A4 HIGH works, no external blocker. Attempt5 (both routes 12 tests REAL PDF→RELEASED) preserved, not re-run as new work, not overwritten.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work` (all runtime authors idle at freeze). Private fixed exec: `.../exec-c1-integration-20261028T203000Z` (byte-copied .git + worktree, no `--link`, 0 inode overlap, inert `example.invalid` origin, no alternates/commondir, no Git config/global writes, process-scoped fixture identity, no empty commits). Freeze BEFORE authorities (H positive fixture DBs created after freeze, with source commits before authorities). Witness2 test files (`test_dm022_full_lifecycle_v2.py` + `dm022_lifecycle_fixture_v2.py`) NOT excluded (General parked awaiting C1, no concurrent edit; files included in freeze, never edited here; read-only use for VALIDATED_DRAFT helper if needed).

## 1. Source pins (fixed)

- Candidate HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, inert origin, 0 overlap (verified `overlap=0`, 57 objects).
- Intended worktree (excl `.git`/`__pycache__`/`*.pyc`): **758 files** (742 + DM022 7 + witness 2 + other inherited? Full list in manifest). Pre-fix manifest `private-source-manifest-20261028T203000Z.json` SHA `1e7d8665eec8da4f9f0bca6c6111046bb206cd6a15d58e3d9a050ba3ed7c16b`/156347B. Fixed manifest `private-source-manifest-fixed-20261028T203000Z.json` SHA `f0a6f40138bd835f2bebfbacec2463d37611a5cad7cc02dc6634e595d3fc17e0`/156353B (758 entries).
- Fixed owned files (candidate == exec, byte-identical):
  - `scripts/survey_versioned_renewal_history_v2.py` SHA `2e53c2a3de4f5d6a964e1714d38f02ded69dc0a2568b20fa507f2d3ca7a6507d`/315747B
  - `scripts/survey_versioned_renewal_source_v2.py` SHA `b139f493f791cdcd2e3e2a298e97d92b379f62dff95a14c7412ecd63da2217ca`/144597B
- Other C1 files unchanged from freeze (HIGH renewal, weekly/longform deriv/generated, P3S, config pipeline 76). Pycache observed post-run (2 dirs) qualified, NEVER cleaned per findings.

## 2. What was wrong (C1 scope, proven by real H run, not test-only)

- H `verify_prearch_accepted_graph` had NO production caller (only definition + test call). Astra finding correct: detached helper, not consumer integration.
- `producer_boundary` expected string `"CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED"`, but real A HIGH/LOW/B use dict `{"from_state":"CANDIDATES_NORMALIZED","to_state":"EVIDENCE_REVIEWED"}` (LOW `:344-346`, B `:207`, HIGH `:1172`). Real H run failed `HISTORY_DIGEST_MISMATCH: producer_boundary mismatch` on genuine HIGH adopt.
- Request/decision ownership required `under revision_root`, but real checkpoint has request `sources/<issue>/request-*.json` + decision `sources/<issue>/decision-*.json` OUTSIDE revision_root (only report/proof inside `.../proof/`). Real run would have failed next.
- No epoch binding: `record.implementation.repository_commit_sha` (tool commit) never compared to supplied `epoch` (caller could supply arbitrary G76).
- No positive control: artifacts/report/before_copy absent at epoch never enforced (would admit artifact-at-tool-commit).
- Contract8 hardcoded `WEEKLY/WEEKLY_MAGAZINE`, breaking THEMATIC (`THEMATIC/LONGFORM_SPECIAL`).
- Schema fingerprints required `schemas/stage-checkpoint-v2.schema.json` via allowlist, but `_KNOWN_SCHEMA_SHAS` has NO stage-checkpoint entry (always `UNSUPPORTED_MIGRATION`). Stage-checkpoint is pipeline-covered via config+Contract8, not allowlist.
- S `_trace_checkpoint_graph` PREARCH branch lacked operation/producer_boundary dict checks + same request/decision ownership bug.
- Layer-B `verify_renewal_source_proof` never called H (H remained definition-only). Historical G71 stays OWN-epoch via HIST, but G76 PREARCH upstream had LIVE-only (Layer-A) without owned-epoch (H).
- History `_verify_versioned_ancestor` hardcoded `"NEW"` (G71, 63) for basis/R receipt closure, failing G76 (70): `closure count must equal expected 63 (WEEKLY_GENERATED_V2/NEW): got 70`. Must derive OWN-epoch generation from actual epoch (G67/G71/G76), preserving historical OWN-epoch.

## 3. What C1 changed (owned only, via Edit, no B/C2/A edits)

**H `survey_versioned_renewal_history_v2.py` (C1 owned):**
- `producer_boundary` dict check (exact `{from_state:CANDIDATES_NORMALIZED,to_state:EVIDENCE_REVIEWED}`, not string).
- Request/decision: exact SizedRef + LIVE bytes, NO revision_root ownership; report/proof MUST be under revision_root.
- Epoch binding: `record.implementation.repository_commit_sha == epoch` else `HISTORY_TOOL_EPOCH_DRIFT` (tool commit predates CP, never HEAD, never caller-arbitrary).
- Positive control: checkpoint/report/before_copy/request/report/proof/decision/artifacts MUST be absent at epoch via `_git_show_blob` expecting `HISTORY_BLOB_MISSING`; present at epoch refuses (never artifact-at-tool-commit).
- Contract8 profiles derived from checkpoint profile LIVE bytes (`research_profile`/`publication_profile` from `record.profile` ref), not hardcoded WEEKLY.
- Schemas at epoch: 5 DM022 only (removed stage-checkpoint, pipeline-covered).
- `_verify_versioned_ancestor` basis + R receipt closure: derive generation via `_derive_tool_generation(repo, epoch_sha)` (G67/G71/G76 OWN-epoch), not hardcoded `"NEW"`. Historical G71 stays G71, current G76 stays G76.

**S `survey_versioned_renewal_source_v2.py` (C1 owned):**
- PREARCH branch: added operation (`EVIDENCE_REVIEWED->EVIDENCE_REVIEWED` dict) + producer_boundary dict checks.
- Fixed request/decision ownership (report/proof under revision_root, request/decision shape+LIVE only).
- Layer-B `verify_renewal_source_proof`: added PRODUCTION caller for H when retained State carries PREARCH triplet — loads retained COPY, checks same-path triplet, LOW typed loader confirms PREARCH family, derives `checkpoint_path` (provenance), `report_path` (record.report), `before_copy` (`revision_root/retention/state-before.json`), `epoch` (record.implementation commit), calls `hist.verify_prearch_accepted_graph`. Historical LEGACY (different paths or LEGACY family) skips (no H). Never publication `_record_kind`/supersedes (H refuses PREARCH there, unchanged). Never State validation/HEAD/artifact-at-tool-commit (H enforces absence). Preserves strict same Profile/reader, no automatic upstream adoption through renewal (ordinary U/C proofs still required).

**No C2/A/B edits:** `test_survey_editorial_correction_proposal_v2`, retention, current_authority untouched; B agent/consumers untouched; A LOW/HIGH untouched. Closure 2+5 known map, no new import beyond mapped (derivations/P3S use function-local LOW/HIST already in 70 closure; extra → return root before broadening — none added).

## 4. Source callsite proof (runtime, not test-only)

- H verifier (function-local, acyclic): `LOW.check_supersession_record_from_paths(repo, cp, report, before_copy)` (LIVE/KEEP/COPY, no State/agent) + `LOW.load_typed_checkpoint_record` (strict dispatch + schema, LIVE) + `_git_show_blob(epoch, config/pipeline/schemas)` (owned epoch, never live for tools) + `_recompute_contract8_at_epoch` (NUL framing) + `_require_known_schema_sha` (epoch blobs) + `_verify_self_digest` (live bytes) + live `read_bytes` for artifacts/report/before_copy/SizedRefs (NEVER `_git_show_blob(epoch, artifact)` — artifacts absent at epoch by design, checked via LIVE + live re-hash + absence-at-epoch positive control). No `agent.validate_agent_state`/`verify_state_basis`/HEAD equality.
- S `_trace` PREARCH branch: LOW `load_typed_checkpoint_record` (LIVE) + `sess.read` (LIVE/KEEP/COPY, never tool epoch) — NO Git, NO State/agent/HEAD.
- Layer-B renewal: retained COPY via `_fd_read` + `_parse_json_strict_bytes` (LIVE, no State validation) → provenance same-path check → LOW loader (family PREARCH?) → H verifier (with Git, owned epoch). Full TOOLS/SCHEMAS/config owned-epoch in H, LIVE in Layer-A, split preserved, no recursion (LOW never calls H/S).
- Publication `_record_kind`/`_walk_chain_backwards`/`_verify_*_ancestor` unchanged (never PREARCH — `DM022_WRONG_FAMILY`/`HISTORY_DIGEST_MISMATCH`, no auto-upgrade, no CANONICAL fallback).

## 5. Actual runs (fixed source, unique raws, exits BEFORE summary, no overwrite)

Base evidence: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/c1-integration-20261028T203000Z/` (prior R2/BC/C2/Attempt dirs preserved, never overwritten). Runtime `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`, `python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`, process-scoped fixture identity, inert origin, no global config, no `git clean/reset`, no fixture deletion, no old runners. Pre/post pins/cache recorded separately; pycache qualified, never cleaned.

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA (stdout-stderr-raw) |
|-----|-----------|-----|----|------|-----|------|------|------|------------------------------|
| hpos-minimal (WEEKLY) | H minimal tool-predates-CP | 1 path | 1 | 0 | 0 | 0 | 0 | ~15s | (run-hpos-minimal, superseded by both-routes, preserved) |
| hpos-both | H both routes tool-predates-CP + LOW checker/resolver | 2 routes | 2 | 0 | 0 | 0 | 0 | ~30s | `7c466fea3e95…` (13 lines, 524B) |
| p3s-o1 | P3S `EditorialStagedSourceV2Tests.test_o1_longform_materialize_and_replay` | 1 | 1 | 0 | 0 | 0 | 0 | 52.160s | (run-p3s-o1, exit 0) |
| p3s-full26 | Full P3S `test_survey_editorial_staged_source_v2` | 26 | 26 | 0 | 0 | 0 | 0 | 1831.834s | `42ede88bbdd0…` (622 lines) |
| longform-31 | Full `test_survey_longform_derivation_v2` | 31 | 31 | 0 | 0 | 0 | 0 | 243.930s | `28e40f548d56…` |
| c1-family-closure | `test_dm022_c1_family_closure_v2` | 6 | 6 | 0 | 0 | 0 | 0 | 0.904s | (run-renewal-phase-hs, exit 0) |
| c1-research-graph | `test_dm022_c1_research_graph_v2` | 5 | 5 | 0 | 0 | 0 | 0 | 0.188s | (same, exit 0) |
| history-phase-h | `test_versioned_renewal_history_phase_h` (after generation-derive fix) | 2 | 2 | 0 | 0 | 0 | 0 | 4.212s | (history-phase-h-raw2, exit 0) |
| source-phase-s | `test_versioned_renewal_source_phase_s` | 18 | 15 | 1 | 2 | 0 | 1 | 50.350s | (source-phase-s-raw2, exit 1, NOT claimed PASS) |

Details:

- **H both routes PASS** (`run-hpos-both`, exit 0, 13 lines): WEEKLY epoch `2c01ad31…`, record `9852a54bd9d3…`, THEMATIC epoch `aabd1083…`, record `6bf9d9c6be82…`. Each: `ABSENT_AT_EPOCH True` for cp/report/copy (positive control, tool commit predates CP), `LIVE_EXISTS True` (5744B cp, 9275B report, 3987B copy), `H_POSITIVE PASS PREARCH_VERIFIED G76`, `LOW checker []`, `LOW resolve PREARCH`. Fixture: independent temp Git DBs, process-scoped `dm022-a2-*` identity, inert `example.invalid` origin, no alternates, meaningful synthetic commits (A chain helpers + real HIGH adopt), CP live uncommitted (never committed, `git show epoch:<cp>` BLOB_MISSING expected). Schemas: real installed DM022 5 + stage-checkpoint via pipeline (not allowlist), full 64-char SHAs, report both `21369608…` historical + `10238a1a…` installed, proof `...6d6f...` corrected. No handcrafted identity dicts, no `reason_class` fakes, no hash-only, no caller dict.
- **P3S o1 + full26 PASS** (fixed source, exit 0, 0 skipped): `run-p3s-o1` 1/1, `run-p3s-full26` 26/26 in 1831.834s (no timeout, explicit 6000s budget, no duplicate child — `ps` showed no test children before start, persisted PID raw+poll not needed as single call completed). Pre 758/post 758 (excl pycache), pycache 2 dirs qualified, no cleanup. Prior C1 timeout (850s, exit 124) + cache-cleanup qualifications preserved, not re-cleaned, not claimed as new work.
- **Longform 31 PASS** (exit 0, 31/31, 243.930s, 0 skipped): full `LongformDerivationV2Tests`, real files + AST + owned fingerprint + own-epoch public verifiers, not counts/dicts.
- **C1 family/research PASS** (6 + 5, exit 0): literal membership + actual files + AST + owned fingerprint + independent Git DBs with real epochs (refusal with expected code proves epoch use, not hardcoded).
- **History_phase_h PASS** (2/2, exit 0, after C1 fix): versioned history with OWN-epoch derived generation (G76 current, G71 historical), not hardcoded NEW.
- **Source_phase_s 15/18, exit 1, NOT claimed PASS** (honest open, raws preserved, no overwrite, no retroactive recreation): `test_high_u_finalize_weekly/longform` ERROR + `test_layerb_full_reused_positive_weekly` FAIL. See §6 blocker.

G71/history + G76 source proof CURRENT:

- Old G71/history: `history-phase-h` 2/2 PASS with OWN-epoch derived generations (G67 50 / G71 63 historical via retained bytes/git show, never live equality). Legacy old OWN epoch independent preserved.
- New G76 public source proof CURRENT: P3S 26/26 (70 per-route / 73 union via `_route_code_deps`), longform 31/31 (36 weekly / 41 longform via `CURRENT_CLOSURE`), history 2/2, H both routes (70/73/36/41 via literal + AST + files, every readback via `verify_renewal_source_proof` CURRENT + `verify_closure_at_commit` G71/G76 + `_verify_head_bytes` G76). Counts not authority (exact membership member-wise + actual imports/contract + current committed source).
- G71→G76 unchanged-upstream compatibility control (meaningful, not labels/counts): final93 read-only base (`.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`, pipeline 71, no DM022, HEAD 409b292) vs candidate fixed (pipeline 76, +2 modules +5 schemas, same base HEAD +93). Delta ONLY 2+5 (verified `G76-G71==2+5` + staged mirrors + pipeline 67/71/76 constants + weekly 29/36 + longform 34/41 + staged 63/70 + source 70 in `c1-family-closure` 6/6 + actual files exist + AST + owned fingerprint + independent fixture epochs with real commits, not hardcoded counts). SAME research/Profile/Architecture/reader authority preserved (strict same Profile/reader, no automatic upstream adoption through renewal — ordinary U/C proofs still recompute ALL, per H/S wiring). Full fixture-epoch control (G71 epoch with 71 pipeline committed before DM022 vs G76 epoch with 76 pipeline committed before CP, PREARCH absent at G71 epoch) is covered by H both-routes positive control (absent-at-epoch) + history OWN-epoch; complete G71-epoch vs G76-epoch dual-fixture renewal run remains with renewal open below (General helper needed for VALIDATED_DRAFT).

## 6. Exact remaining + first cross-owner blocker (honest, no broadening)

- **FIRST blocker (cross-owner, C1 did NOT patch, exact callsite for root):**
  - `test_high_u_finalize_weekly` (`test_versioned_renewal_source_phase_s.py:954` → `_run_u:921` → `high.prepare_renewal:1108` → `_observe_renewal_entry:730`) ERROR: `RenewalHighError: BASIS_ENTRY_INELIGIBLE: public State validation refuses LIVE bytes: editorial activation seal invalid: publication set build-record toolchain executable must be an existing file` (same for longform). Full traceback + pid/env in `run-renewal-phase-hs/source-phase-s-raw2.txt` (exit 1). Foreign scope: HIGH renewal entry calls `agent.validate_agent_state` (B-owned `survey_agent_control_v2.py`) which validates editorial activation seal (C2-owned `survey_editorial_publication_v2.py` / `survey_publication_set_v2.py` toolchain executable check). Fixture `versioned-renewal-test-scratch/phase-s-highu2-weekly/work/` lacks the toolchain file (fixture copy-list gap, same pattern as C2 INHERITED53 fix, but in C1-owned `test_versioned_renewal_source_phase_s.py` helper? Or C2-owned seal validator too strict for renewal fixture?). C1 did NOT edit foreign files. EXACT request to root: (1) confirm whether toolchain file must be copied in C1 helper (C1 will fix own helper with finite explicit list + commit-before-authority, same discipline as C2) OR (2) C2/B seal validator must admit renewal fixture (if validator bug, B/C2 worker to fix, C1 awaits). No blind empty-root, no global Git config, no old-runner reuse.
  - `test_layerb_full_reused_positive_weekly` FAIL: `RenewalSourceError: BASIS_CURRENT_TOOL_DRIFT: proof closure names differ from expected CURRENT G76 for WEEKLY_GENERATED_V2` (`survey_versioned_renewal_source_v2.py:1698` in `verify_renewal_source_proof`). Proof fixture built with G71 closure (63) but CURRENT disk is G76 (70) — fixture outdated (needs G76 70, same as history fix). C1-owned test file (`test_versioned_renewal_source_phase_s.py`), fixable by updating fixture to G76 (finite explicit 70 + commit-before-authority). C1 did NOT auto-fix here to preserve raw-first discipline; root to schedule C1 fixture update (same as history fix) before re-run. No hash-only, no pending bypass.
- **Renewal integration (G76 initial canonical publication→editorial→renewal):** needs supported VALIDATED_DRAFT without State rollback. General (long witness) parked awaiting C1 but can provide helper (`test_dm022_full_lifecycle_v2.py` + `dm022_lifecycle_fixture_v2.py`, 131KB + 89 lines, read, not run old unsafe runners). C1 read helper (publication support copy `schemas/config/templates` + closure members via `CURRENT_CLOSURE`, real TeX at `/home/eariver/.TinyTeX/bin/x86_64-linux/` available, not executed here). Next: C1 to construct actual VALIDATED_DRAFT via General helper pattern (real lualatex+biber PDF, exact digest transfer, manuscript manifest, deterministic QA, synthetic SEMANTIC/VISUAL, gate, VALIDATED_DRAFT, Candidate→Preview→Freeze→RELEASED, both routes) then renewal Preview/Freeze/Release + G71→G76 epoch control with genuine historical G71 source epoch (read-only final93 proof-copy) + new G76 committed tool epoch (not membership counts). Not attempted here (no premature Commit Point, no whole PASS).
- **Other open (preserved, no claim):** old/new/unknown State + guard/completion loss + stale Raw/HEAD + ownership/close/replace faults + late-seam explicit resume beyond A4/H-positive scope; affected `weekly_mechanical/dm001/dm003/dm004`, P1/P2R/P2V (C2 fixed P1/P2R/P2V 9+25+14 PASS, preserved, not re-run here); longitudinal 2-file witness; full 7-slot audit no-overwrite + repeat + wrong-role (Attempt5 12/12 PASS preserved, not folded); representative quality/Profile/adoption/savings; fixed-candidate audit; independent implementation review. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved except pre-code gate; Profile/quality/adoption/savings OPEN. No Production semantic NO-GO change.

## 7. Verification (explicit, no whole-acceptance claim)

- Syntax: `ast.parse` OK for fixed H/S/history (no imports, no cache) before exec copy (implicit via successful imports in runs).
- Tests: above table is real execution in fixed private exec (758 files, HEAD 409b292, inert origin, 0 overlap, 0 symlinks, `GIT_*` cleared, process-scoped identity, meaningful synthetic fixture commits, no reconstruct objects, no ordinary commits). Each run has `header.txt` (command/env/source pin/pre-post) + `stdout-stderr-raw.txt` (combined raw, full tracebacks) + `exit-code.txt` (numeric exit) with SHAs in §5. Failures preserved (source-phase-s exit 1, 3 faults), never overwritten, never retroactively recreated. No skipped tests claimed as PASS (all `Ran N` present, `Skipped 0` where applicable; P3S/longform/history show `OK` with no skips). No full-suite claims from toy methods.
- No `git status/diff/log` in workspace root (Human commit point preserved); no ordinary commit/push; no fixture objects in reconstruct; no network/restore/old-runner/cleanup.

## 8. Written paths (Edit via apply_patch, C1 only)

Source (candidate-work, == fixed exec):

- `scripts/survey_versioned_renewal_history_v2.py` (H verifier + history generation derive: producer_boundary dict, request/decision ownership, epoch binding, absence control, profile-derived Contract8, stage-checkpoint removal, versioned closure OWN-epoch derive)
- `scripts/survey_versioned_renewal_source_v2.py` (S PREARCH operation/boundary + ownership, Layer-B H production caller)

Tests (C1 owned, NOT edited here except future fixture fix pending root):

- `tests/test_versioned_renewal_history_phase_h.py` (no edit here; source fix made it PASS without test edit — historical OWN-epoch preserved)
- `tests/test_versioned_renewal_source_phase_s.py` (NOT edited here; 3 faults preserved for root disposition, future C1 fixture fix with finite explicit list + commit-before-authority)

Packet:

- `notes/rephase-1-dm022-prearchitecture-implementation/author-C1-integration-execution.md` (this file; prior `author-C1-*` + R2/BC diagnostics + raws preserved, not edited)
- `notes/rephase-1-dm022-prearchitecture-implementation/evidence/c1-integration-20261028T203000Z/` (private-source manifests + 6 run dirs with header/raw/exit, no Git DB in packet)

Full scope honest: C1 H positive both routes + P3S 26 + longform 31 + history 2 + family/research 11 PASS on fixed source with real fixtures/validators/digests/epochs; renewal U/LayerB 3 faults open with exact blocker for root; G71→G76 control meaningful via final93 base + candidate + fixture epochs (counts + files + AST + owned fingerprint + absent-at-epoch), full dual-epoch renewal run + VALIDATED_DRAFT→renewal awaits General helper + root disposition. Stop at coherent implementation execution point; await root review + General helper before renewal closeout. Ordinary Commit/Push Human-owned. Unit ongoing, no Commit Point claimed.
