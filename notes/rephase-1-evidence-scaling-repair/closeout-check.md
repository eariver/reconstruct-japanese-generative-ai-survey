# Evidence scaling repair — closeout document check (bounded, DATA-only)

2026-11-04. Bounded documentation check only. Write scope is this file. No project runtime/import/tests/build/fixtures/network/Git commands/Commit readback/Production checkout/source or State edits, no subagents. Methods were Read/Grep/Glob plus existing saved `*.txt`/`*.json`/`*.md` reports as DATA. No old saved runners executed. No Raw 189MB rehash, no 409 rerun. No `apply_patch` binary use beyond this doc write.

## 1. Files read FULL

- `notes/rephase-1-evidence-scaling-repair/astra-closeout-resolution.md` FULL (87 lines).
- `outputs/rephase-1-evidence-scaling-implementation-assessment.md` FULL (58 lines).
- `notes/rephase-1-evidence-scaling-repair/README.md` FULL (33 lines).
- `notes/rephase-1-evidence-scaling-repair/final-implementation-review.md` FULL (48 lines, §7 FINAL-BINDING).
- Current top `AGENTS.md` entry (CURRENT 2026-11-04 evidence scaling repair block).
- `handoff/rephase-1-continuation.md` CURRENT 2026-11-04 block (lines 1-13) plus preserved history headers.
- `outputs/rephase-1-implementation-plan.md` CURRENT 2026-11-04 block (lines 3-5).
- `outputs/rephase-1-completion-roadmap-20261019.md` CURRENT 2026-11-04/11-02/11-01 top blocks (lines 3-9) and §4 order header.
- `notes/rephase-1-session-transition/restart-context.md` CURRENT 2026-11-04 top block (line 3).
- Packet DATA only: `source-packaging/final-20261103T174718Z/independent-packaging-report.md` FULL (114 lines), `patch-sha256.txt`, `patch-bytes.txt`, `manifest-sha256.txt`, `manifest-bytes.txt`, `manifest-json-sha256.txt`, `manifest-json-bytes.txt`, `workcopy-pins-stdout.txt`, `gen-verify771-stdout.txt`, `real-w34-retry-20261103T172327Z/README.md` §§1-9, `affected-verification-20261103T175000Z/README.md` §§0-5.
- Relevant JSON parse only: `source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json` header (lines 1-14) plus pin rows for the 4 delivered paths via Grep (lines 3059/3346/3514/4025 in both `manifest.json` and `complete-evidence-scaling-manifest.json`). No full retained-fault-fixture parse, no all-historic-hundreds link walk.

## 2. Source/delivery identity — PASS

- Final is actual `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` + **139 delta paths = 57M + 82A / 771 intended files = 689 available base + 82 new**. All three current docs state this identically. Root normal candidate HEAD stays 409; no ordinary new shipping commit claimed.
- Full DIRECT409 patch includes inherited 138; never layer old patches. Applied proof path is correct: `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60`. Author workcopy under ignored runtime only.
- No source/semantic-quality/human-quality/audit/savings claim in checked docs. All state WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN/quality-adoption-savings OPEN and Human Commit Point stop.

## 3. DATA hashes/sizes — PASS (existing reports, no manual truncated authority)

- `source-packaging/final-20261103T174718Z/complete-evidence-scaling-409.patch`: expected `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49` / 5408065B. Matches `patch-sha256.txt` line 1 and `patch-bytes.txt` line 1 and packaging report §1. Assessment §4, README §Source, handoff line 7, plan line 3, restart line 3 state same full hash/bytes.
- `source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json` (same bytes as `manifest.json`): expected `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143` / 202204B. Matches `manifest-sha256.txt`, `manifest-bytes.txt`, `manifest-json-sha256.txt`, `manifest-json-bytes.txt` (all 202204B, same SHA) and packaging report §1.
- Counts/modes from machine manifest: `gen-verify771-stdout.txt` CAND 771 GEN 771, 0 mismatch; report §§0/3/6: 139 files (82A/57M/0 D/R), 84615 insertions/975 deletions, 771 = 689 + 82, git modes 770x100644 + 1x100755, physical 0/771 mismatch, FULLVERIFY-OK across CAND/GEN/PROOF/MANIFEST. Root §2 and assessment §4 counts match; no contradiction.
- Actual full-source 3 pins + test19 full hash, Root table vs machine manifest (full 64-char, Grep-verified in both manifest copies + `workcopy-pins-stdout.txt` + report §4):
  - `scripts/survey_evidence_v2.py` `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a` / 158943B.
  - `scripts/run_evidence_v2_interactive.py` `5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543` / 45833B.
  - `scripts/survey_research_authority_v2.py` `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b` / 218692B.
  - `tests/test_evidence_scaling_v2.py` `7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e` / 106616B (FINAL19).
- Old final138 byte-preserved: packaging report §0 cites patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e` / 5247647B and manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc` / 186847B. Existing old-packet reports match: `notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/patch-sha256.txt`, `patch-bytes.txt`, `manifest-sha256.txt`, `manifest-bytes.txt` return same four values. No modification observed.
- Frozen Profile contract `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` / 20472B and precode ROOT `bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` / 20159B are cited unchanged in handoff/plan/restart-top and Root scope; this check does not rehash those docs, records the stated pins as references only.
- Root current closeout + assessment record: closeout FULL 87 lines and assessment FULL 58 lines were read as above; full SHA/size of those two live docs is not frozen here because the independent review concurrently appends closeout confirmation (see §6). Link-exists is sufficient for this doc check.

## 4. Evidence conditions — PASS with stated limits

- Final19 is one actual run (19/19); other affected batches are separate: Profile 28, Evidence/runner/agent/source-class 26, DM022 C7, A2-selected 5 of 25, family 6, graph/presence 8, consumers 3. No sum, no whole-old-suite claim. Matches Root §4, assessment §4, affected README §§2-3.
- Actual 409 `e84a82aca000c990597ea8cf60f548e2ff187bd1` ran test `d486809c...` (18 methods); delivered test is `7b862305...` (19). Packaging report §7 proves only that one test file differs, other 770 identical. Qualified source/run composite, not a single all-final snapshot. Stated correctly.
- Actual Weekly CURRENT proof: real `verify_renewal_source_proof` CURRENT_PROOF_VALID + SAME stored proof drift refusal + repaired positive (supplement `current-supplement-20261104T003000Z`). Old 478 is closure/file assertions only, not 478 tests or full CURRENT proof. Stated correctly.
- Metrics window precise: 45238986845B logical `rchar` delta (~45.24GB) / 175.26s wall / ~160.18s user CPU is same-process `/proc/self/io` observation including guards and in-run verification, `read_bytes` 0 (page-cache logical, not disk). No speedup/savings claim. Old ~228GB/14:38 is transcribed, unfinished at 143 tasks, no raw dump, not a comparable baseline. Stated correctly.
- Initial mode warning preserved/corrected before clean check0/apply0 with whitespace (first check0 with 85B mode warning on `survey_core_execution_bridge_v2.py`, chmod 775, second check0 0B, apply0 with 1085B whitespace warnings; `gen-diff-check` exit 2 with 392B preserved). No full-hydration/tree-clean/safe-rerunner claim. Stated correctly.
- Initial false coverage, F5 outer-return failure, Views/HEAD test delivery merge, bd80 escaped-facade failure, LOW planned-FILE-hash withdrawal, CURRENT fixture git-config/HOME deviation, fixture-toolchain/harness failures are all preserved/qualified in Root §5 and final review §§4-5. No erasure observed.

## 5. States, next, authority — PASS

- Both real-rehearsal States are CANDIDATES_NORMALIZED (current new e84 copy success vs original 480 failed held), not EVIDENCE_REVIEWED. No Gate advance, no new PDF, no publisher-truth PASS. Stated correctly.
- Next is actual W34 Evidence/authority-consumption review then necessary Selection/Architecture, plus SP same-stage owned-unaccepted Ledger/Completeness disposition with guards. No auto-cleanup/force/fake REQUEST_CHANGES/new generic reader/R4 auto-start. Matches Root §6, assessment §5, README §Next.
- Prior body-17 permissions are not new crawl/current-main/local-Production-checkout authority. Reuse-capture bounds stated; no new standing crawl observed.
- Worker unnecessary HEAD read is recorded/quarantined (Root §5 last bullet, retry README §9); Root did not repeat/use it as authority. Docs do not claim zero worker readback. Correct.
- Ordinary Commit/Push/Production mutation: none claimed. Meaningful isolated fixture commits are distinct (retry `e84a82a`, affected snapshot `e746a5db`, CURRENT fixture `969bd4f`, final19 fixtures) in ignored runtime DBs with inert origins, not ordinary candidate/reconstruct commits. Correct.

## 6. Links, whitespace, precedence, stop — PASS

- Scoped local Markdown links checked (new current refs only, not all historic hundreds): Root §1 `final-implementation-review.md` exists; §2 `source-packaging/final-20261103T174718Z/independent-packaging-report.md` exists; §3 `real-w34-retry-20261103T172327Z/README.md` + `artifact-manifest.json` exist; §4 `affected-verification-20261103T175000Z/README.md` + `current-supplement-20261104T003000Z/README.md` exist. Assessment §1 packet/README/Root/final-review/packaging-report/`closeout-check.md` refs resolve (this file creates the last target). README §§Read-first/Evidence-map links resolve to existing packet files. No broken scoped link found.
- Self forward-link: `astra-closeout-resolution.md:3` and `README.md:10` and assessment §1 already link to `closeout-check.md` before it existed (pending). This file verifies after creation; no checked file was modified to fix links.
- Concurrent independent review: `final-implementation-review.md` §7 ends with Root-closeout-follows while Root already cites its FINAL-BINDING. Both directions are link-exists; this check does not freeze a mutable hash of the concurrently appended review nor claim observed-before status beyond link existence and Root-reads-after as recorded in Root §§1/5-6.
- Trailing whitespace: Grep ` $` over `notes/rephase-1-evidence-scaling-repair/*.md` returns 0 matches; over `outputs/rephase-1-evidence-scaling-implementation-assessment.md` returns 0 matches. Saved GEN whitespace (`gen-diff-check` exit 2, 392B) and apply whitespace (1085B) are packaging DATA, not doc trailing-whitespace failures.
- Current precedence: implementation-plan line 3, roadmap lines 3-5, restart line 3, handoff lines 3-13 all place CURRENT 2026-11-04 evidence-scaling repair on top; old rehearsal PARTIAL and scaling-next blocks are preserved below as superseded history. No old-next resurrection observed.
- Human Commit Point stop is stated in Root §6, assessment §5, README §Next, handoff, plan, roadmap-top and restart-top. No auto-start instruction observed.
- No source/doc scope contradiction found; per task, no checked file was modified.

## 7. Verdict

**BOUNDED DOC-CHECK PASS** for `astra-closeout-resolution.md` FULL, `outputs/rephase-1-evidence-scaling-implementation-assessment.md`, and packet `README.md` against current top AGENTS/handoff/plan/roadmap-top/restart-top and the DATA reports above.

Actual method: Read-only DATA checks (Read/Grep/Glob + saved hash/size/JSON/raw-report comparison). Exits/raw limits: no new exits produced; relied exits are packaging `check0/0 + check2 0/0 + apply0/1085B`, `gen-diff-check` exit 2 (392B), affected batches each exit 0 with `Ran N OK` in saved `stderr.txt`, real409 exit 0 in saved raw. Raw 189MB not rehashed; manifest JSON parsed for header + 4 pin rows only. This is not an R4 audit, semantic-quality, adoption, or savings verdict.

## 8. Root final data-hash supplement and wording correction

Root performed fresh, data-only `sha256sum` and `stat -c '%s %n'` on the explicitly named files below; both commands exited0. No Git/readback, runtime test, large-Raw rehash or source mutation. This supplements §§3/7's reference-only hash comparison; it does not retroactively change the checker's method. Concurrent changes to the review file do not prevent pinning the separate, unchanged ROOT/assessment files.

| File | Actual SHA256 | Bytes |
|---|---|---:|
| `astra-closeout-resolution.md` FULL | `77b9d338d85d545791836ef1531cf35fa37b7dd861eb84828c70b2b16b59cc3a` | 14246 |
| `outputs/rephase-1-evidence-scaling-implementation-assessment.md` | `c6b562831c69d15706f2a2bbb9596222e092e9b48ce7b3e0116ef44300329425` | 6355 |
| FINAL complete scaling patch | `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49` | 5408065 |
| FINAL complete scaling manifest | `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143` | 202204 |
| `outputs/rephase-1-profile-support-contract-decision.md` | `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` | 20472 |
| Profile pre-code ROOT FULL | `bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` | 20159 |

`manifest.json` was also freshly hashed and matches the complete manifest. Final review§8 confirms ROOT's full scope; §9 corrects its old “143-task” wording. **143 is the failed run's SIGTERM exit code, not a completed-task count.** This also corrects §4 of this document (“unfinished at143 tasks”). The number of tasks processed and exact phase at that old stop remain unestablished. No new performance or completion inference is made.
