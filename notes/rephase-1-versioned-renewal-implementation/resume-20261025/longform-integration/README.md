# LONGFORM integration — owned evidence (parallel with Weekly, no shared writes)

Human f84fcf5 explicitly requests parallel. LONGFORM only. READONLY input/candidate/other-route fixture.
This dir + owned runtime `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/` only.
No product edits/network/ordinary commits/old-runner exec/failed cleanup/reset/cache purges.
SOURCE-only meaningful fixture commits permitted/required before authority (G1/G2/G3/G4/G5 in fixture DB only).

## 1. Frozen input + baseline (READONLY, verified)

- Reconstruct HEAD `f84fcf5` at start (clean except untracked resume packets).
- Frozen FIXEDINPUT `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  736 intended files, `dst-hash-intended` SHA `d7d7f6df0bbde842c0270d00f493b01e5be2d19fd48ccae56086f5cf4ca3a129` (736 lines).
  Pins: H `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467` (277869B),
  S `20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306` (127981B),
  HIGH `9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152` (202862B),
  PUB `90d90738dc2fc0c57a22f9656659a6e3665d262919b17f259811d035dac3d8c6` (92396B),
  Reader `098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c` (46395B).
- Baseline READONLY genuine old R3 `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-longform`
  HEAD `721a04d85532d7855f3e54cc411f5847c787726e`, tracked 721, untracked 136 + ignored 2 logs,
  old E including ignored PDF/log exact names/hashes, real 5-page PDF
  `sources/SP001/publication/v2/editorial-corrections/lf-boot-1/publication/build/main.pdf` 79530B SHA `12e2bdfb0aabe4d3d7ca9df3600e565a26de067e8b8e7104a1fd9ff26d8e7a48` (5 pages),
  State `sources/SP001/production-state.json` VALIDATED_DRAFT, r1 `2bd14fc72491` active.

## 2. Owned isolated fixture (LONGFORM only)

- Parent `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/` (new, no collision with Weekly `versioned-renewal-weekly-20261025T052132Z`).
  `setup-20261025T060000Z/` evidence: clone `--no-hardlinks`, inert origin `https://example.invalid/versioned-renewal-chain-longform.git`,
  root/gitdir/inode/noalternates/noGitrootenv verified, `TMPDIR` workspace-local.
- Copy captured E: 136 others + 2 ignored logs, per-file `copy2` + SHA verify (not blind cache).
- Overlay EXACT 736 from snapshot-work manifest, SHA/bytes verified, `mismatches=[]`.
- SOURCE-only commit G1 `381c05f486d4956efa275843f7158d9392942d0d` (47 files, no E rewrite, no `git add -A`):
  `config/survey-production-v2.json`, 5 schemas (incl 4 versioned-renewal), 15 scripts (incl 3 renewal), 8 tests, etc.
  Tree `025a067300b0db56158ae639e2d79534a52dafd4` (same as Weekly G1 tree, different commits = independent DBs).
  Scope: 721 baseline old source vs actual candidate 409 distinct (ancestry `721a04d` retained, `merge-base --is-ancestor` 0).
- Later SOURCE-only epochs (all in fixture DB, no shared writes):
  G2 `5740d67` (style+Core comment), G3 `e25a467` (H comment), G4 `efea07d` (S comment), G5 `18587b6` (HIGH comment).
  Style `templates/survey/jgaisurvey.sty` SHA `b1cbbdd93711...` after G2, unchanged through G3/G4/G5 (verified).
  Current HEAD `18587b67d2f96e7e5b761712eb5aa5f5ebbb3c9a`, tree differs per epoch (genuine changed-tool epochs).

## 3. Full LONGFORM public sequence (fixed current code, fresh child per epoch, 1200s bound)

All HIGH calls via fresh `python3 -c` with fixture-first `sys.path.insert(0, root)`, unique UTC `now_iso`, PID heartbeats, raw `*-stdout.txt/*-stderr.txt/*-exit.txt`.

- **Bootstrap U** `run-u1-20261025T060000Z.py`:
  U1 `high-u1-longform` REUSE prepare 0 → QA 0 → finalize 0 (`REUSED_TARGETS`) → validate-set 0 → activate 0 (`ACTIVATED r2 f653c92cef...`) → history 0 (`HISTORICAL_IDENTITY_VERIFIED`, chain 2, FILE refs, `schema_pointer ""` never `/`).
  HIST/CURRENT strictState: `verify_versioned_history` + `agent.validate_agent_state==[]` (fix `u1-current-state-fix` 0, `u1-file-refs-fix` 0 with CURRENT proof readback).
  Old receipt TOOL_DRIFT oracle recorded (old EDITORIAL receipt at 721 vs new proof at G1, detached CURRENT check only on new proof).
  Real U readonly `ALREADY_ACTIVE`: second activate same set 0 `ALREADY_ACTIVE r2` (`u1-activate-again`).
  Alias refusal: symlink `publication-set.json.alias.json` → activate 2 `RECORD_COLLISION` (expected, `u1-activate-alias` 2), resume 0 `ALREADY_ACTIVE`.
  Harness bug: initial `u1-history-pre` (passed set as record) 1 + `u1-current-state` (missing fixture import) 1 → fixed by `u1-current-state-fix`/`u1-file-refs-fix` 0. Failed probes preserved, not erased.
  Alias artifact removed after test to unblock P1 tree (logs preserved, not failed-renewal cleanup).

- **G2 style+Core + U-fail + C1** `run-g2-20261025T060000Z.py` + `run-g2-resume-...py`:
  G2 commit `5740d67` (style comment + HIGH comment, schema/semantic unchanged).
  U-fail `high-ufail-longform` REUSE prepare 0 → QA 0 → finalize 2 `REUSE_TARGET_MISMATCH` (current style vs retained trio, expected), inert preserved (`ufail-inert-ls`, no set, no record, no cleanup).
  C1 `high-c1-longform` RENDER prepare 0 → targets 0 (`NEW_TARGETS`, proof `932c77b7...`, trio at `.../renewals/high-c1-longform/staged-source/`, no fake P3S, no companions sidecar) → verify-targets 0 (PDF 5 pages, SHA `4ce0495c...` at new R path, `REUSED_BUILD` vs `EXECUTED_BUILD` distinguished) → reviews-qa 0 (fresh supplied QA + synthetic semantic/visual at NEW targets, PID-line parse fixed in resume) → finalize 0 (`NEW_TARGETS`) → activate 0 (`ACTIVATED r3 c41159de...`) → history 0 (3 refs EDITORIAL+U1+C1).

- **G3/G4 + U2 + U3 fail + G5 + U3b (C→U→U)** `run-g34-uu-...py` + `run-g5-u3b-...py`:
  G3 `e25a467` (H comment), G4 `efea07d` (S comment), style unchanged verified.
  U2 `high-u2-longform` (prior C1 r3, now `2026-10-25T05:31:17...` >= r3 `05:28:26...`) prepare 0 → QA 0 → finalize 0 → activate 0 (`ACTIVATED r4 3f76b3d7...`) → history 0 (4 refs) → proof readback 0. State switch r3→r4, r3 preserved immutable.
  U3 `high-u3-longform` (prior U2, same epoch) prepare 0 → QA 0 → finalize 0 → activate 2 `SEAL_BIND/HISTORY_TOOL_EPOCH_DRIFT: REUSED_BUILD renewal_tools.old must differ from new` (genuine Core-change required, preserved incomplete, r5 orphan file created but State stays r4). This replaces previous run55 FAILED longform U3 (`HISTORY_ANCESTOR`); new failure is different code (TOOL_EPOCH_DRIFT, not chronology). Orphan r5 `recorded_at 05:33:56...` preserved, not altered/rewound.
  G5 `18587b6` (HIGH comment, style unchanged) → U3b `high-u3b-longform` (prior U2 r4, now `05:37:49...` >= r4) prepare 0 → QA 0 → finalize 0 → activate 0 (`ACTIVATED r6 f76d5552...`) → history 0 (5 refs EDITORIAL+U1+C1+U2+U3b, chain_length 5, n_bindings 52). Validates older embedded C proof/build lineage HIST not forced latest, current new proof every readback, no old State equality (r6 active, r4 preserved). C→U→U complete as `r1→r2 U1→r3 C1→r4 U2→r6 U3b` (r5 orphan skipped, per map).

- **Renewal→EDITORIAL** `run-ed-direct-...py` + `run-ed-retry-...py`:
  NEW proposal `lf-ed-1` staged changed-reader authoring (headline/deck/summary changed, same accepted research/Draft/Architecture) then P1 `prepare_proposal` → 1 `TREE_ALIAS: symlink .../high-u1-longform/publication-set.json.alias.json` (harness artifact, fixed by removal, logs preserved).
  Retry `lf-ed-2` after alias removal → `Timeout (0:05:00)!` in `jsonschema`/`referencing` via P1 prepare (faulthandler single dump, 300s). Same class as run54/59/61 timeouts (history/git + jsonschema). Recorded as blocker, no PASS, no infinite retry. Full P1/P2R/P2V/P3S63 + real build/postrender/finalize/activate OPEN.
  No P1Core fake, no helpers new canonical publication. Hist new EDITORIAL63 must work under new producer epoch preserving old50 history — OPEN.

- **Normal DIRECT** `run-direct-20261025T060000Z.py`:
  Lifecycle on U3b r6: `validate_set` OK, but `build_freeze` → 1 `ValueError: renewal checkpoint wrapper evidence artifact materiality-ledger not allowed (exact producer map)` at `scripts/survey_publication_v2.py:684` (`_prepare_freeze_inputs`, `_FIXED_PRODUCERS` evidence allows only `evidence-acceptance/edition-views-acceptance`, but retained wrapper `CANDIDATES_NORMALIZED.json` bundles `materiality-ledger/profile-completeness`). Codepath mismatch returned to root, no product patch in worker. State pinned (no mutation), old priors `r1/r2/r3/r4/r6` preserved. Typed proof through nested reviews & Freeze deps OPEN.
  R1/canonical refusal: `R1_REFUSAL_PRECONDITION_OK` (VERSIONED_ACTIVE) + `r1-refusal-full` attempted `refresh_mechanical_evidence` → refused before writes, `R1_NO_WRITES_OK` (full log in `run-direct`? Actually `run-ed-direct` shows precondition; full R1 test in `run-direct` was not reached due to lifecycle fail — outstanding).

## 4. Current fixture HEAD/tree/recordset

- HEAD `18587b67d2f96e7e5b761712eb5aa5f5ebbb3c9a` (G5), ancestry `721a04d →381c05f G1 →5740d67 G2 →e25a467 G3 →efea07d G4 →18587b6 G5`, `git log --oneline -6` in `run-g5-u3b/g5-log`.
- State `sources/SP001/production-state.json` VALIDATED_DRAFT, pointer `sources/SP001/publication/v2/publication-surface-revalidation-r6.json` SHA `f76d555227b2ad353ca97f0477fe7caa539b5a676e367eac95d46090f9b511e6`.
- Records: `r1 2bd14fc7...` (EDITORIAL), `r2 f653c92c...` (U1), `r3 c41159de...` (C1), `r4 3f76b3d7...` (U2), `r5 <orphan incomplete, TOOL_EPOCH_DRIFT>` , `r6 f76d5552...` (U3b active). History `u3b-history` chain 5, `HISTORICAL_IDENTITY_VERIFIED`.
- Candidates/sets/proofs (FILE SHAs in run dirs):
  U1 set `.../high-u1-longform/publication-set.json`, Candidate old PDF `.../publication/build/main.pdf` 79530B `12e2bdfb...` 5 pages (REUSED).
  C1 set `.../high-c1-longform/publication-set.json` SHA `2a0339fa...`, Candidate new PDF `.../high-c1-longform/build/main.pdf` `4ce0495c...` 5 pages (EXECUTED_BUILD, NEW_TARGETS).
  U2 set `.../high-u2-longform/publication-set.json`, U3b set `.../high-u3b-longform/publication-set.json`.
  Proofs/bases/receipts/builds/bundles/gates in respective `renewals/<id>/` with `proof.basis_ref` FILE SHAs, `schema_pointer ""`.
- PDFs: U1 5 pages (reused), C1 5 pages (new R build via TL2026 `lualatex/biber` at `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux`).

## 5. Outstanding errors / blockers (no whole-unit PASS, no CommitPoint)

1. `high-u3-longform` activate 2 `HISTORY_TOOL_EPOCH_DRIFT` (expected genuine-change refusal, preserved incomplete, superseded by U3b r6). Not a defect to retry blindly.
2. Renewal→editorial P1 `prepare_proposal` on U3b r6: `TREE_ALIAS` (harness alias, fixed) then `Timeout 300s` in `jsonschema` (same class as run54/59/61). No successful `lf-ed-*` proposal. Full P1/P2R/P2V/P3S63 + build/postrender/finalize/activate OPEN.
3. Normal DIRECT `build_freeze` on U3b: `ValueError ... materiality-ledger not allowed` at `survey_publication_v2.py:684` (`_prepare_freeze_inputs`, exact producer map). Mismatch returned to root, no patch. Full Candidate/stage→Preview/Freeze/Release/readback OPEN. R1/canonical full refusal test OPEN (precondition only).
4. Missing `*-exit.txt` where stdout shows success? None for LONGFORM positives (all exits present). Prior `u1-history-pre`/`u1-current-state` harness bugs fixed with `*-fix` 0, preserved as history.
5. No independent final implementation review, no affected regressions (original routes/R1 slow/DM004 etc.), whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic NO-GO, synthetic reviews/Human approvals content NO-GO, no genuine PASS producer.

## 6. Files (LONGFORM only)

- `setup-20261025T060000Z.sh` + `setup-.../` (G1 fixture, 47-file SOURCE-only)
- `run-u1-20261025T060000Z.py` + `run-u1-.../` (U1 + ALREADY_ACTIVE/alias/resume) + `run-u1-fix-...py` (CURRENT/FILE/DRIFT fix)
- `run-g2-...py` + `run-g2-resume-...py` + `run-g2-.../` (G2 + U-fail + C1)
- `run-g34-uu-...py` + `run-g34-.../` (G3/G4 + U2 + U3 fail) + `run-g5-u3b-...py` + `run-g5-.../` (G5 + U3b C→U→U)
- `run-ed-direct-...py` + `run-ed-.../` (editorial probe + direct precondition) + `run-ed-retry-...py` (lf-ed-2 timeout) + `run-direct-...py` + `run-direct-.../` (Freeze mismatch + R1)
- Owned runtime `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/` (fixture DB + tmp, no shared writes).

No whole-unit independent PASS. Ordinary Commit/Push Human-owned.
