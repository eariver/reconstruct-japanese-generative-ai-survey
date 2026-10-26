# Raw progress — LONGFORM full, WEEKLY pending (precise, no whole PASS)

## LONGFORM (full renewal→editorial complete, with performance qualifications)

- Fixture: NEW independent clone valid U4 prePreview (`.../versioned-renewal-longform-repair-.../renewal-longform`
  HEAD `047f8ad` r7 `06af38...` + lf-ed-1/2/3 failed roots preserved) → NEW parent
  `.../versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform`,
  `git clone --no-hardlinks`, inert origin, no alternates, `nlink==1`, `dev:ino` disjoint,
  no `GIT_*`, workspace TMPDIR. Copy 270 untracked E/renewals/lifecycle/ignored + alias exclusion,
  `E_HASH` via `copy2`+SHA. Overlay FIXED739 738 files (style `b1cbbdd...` preserved, not baseline
  `035645...`), `mismatches=[]`, variant manifest. Overlay patch edpub 85814 + new test 5e5a.
  SOURCE-only `add` 2 paths, E overlap 0. G7 commit `a7772a1` (ancestry `721a04d` OK, message G7
  archive-correction, no E rewrite, no `git add -A`).

- U5 fresh CURRENT on G7 (prior r7 → r8 `3d39535d...` REUSE, style preserved):
  `run-u5-longform-.../u5-prepare/qa/finalize/activate/history/full-check` all exit 0 (1200s, fresh Python
  per phase, PID heartbeats, `now_iso` monotonic). `HISTORICAL_IDENTITY_VERIFIED` chain 7
  (r1 EDITORIAL + U1/C1/U2/U3b/U4/U5), `schema_pointer ""`, FILE SHAs. `verify_renewal_source_proof`
  CURRENT + `agent.validate_agent_state==[]` OK. Old proofs expired (old epoch vs new G7, `old!=new`
  genuine). Chrono `now>=r7`, new IDs distinct, invalid orphans preserved (lf-ed-1/2).

- Editorial lf-ed-4 NEW (on U5 r8, not lf-ed-3 reuse; lf-ed-3 failed `ACCEPTED_DRAFT` preserved):
  staged changed-reader authoring (headline/deck + 3 paras, para3 `The synthesis stays inside authorized
  evidence.`, longform tweak, `core.json_bytes`, no deletion) + P1 `prepare_proposal` 0 (1200s) +
  P1 stage reader+proposal 0 (operator writes, P1 writes nothing) + P2R `capture_retention` 0 +
  `verify_retention` 0 + P2V `observe_current_authority` 0 + scope `scope-review-v2.json` 0 (manual G7,
  no P1 re-run due to retention conflict, preserved) + P3S63 `materialize STAGED_ROOT_EXISTS`
  (already present from G7 materialize, preserved) + `verify_staged_source` 0 (preload 35 py,
  63 deps, `STAGED_SOURCE_REPLAY_VERIFIED`) + specs (manuscript/toolchain from lf-boot-1) 0 +
  `prepare_publication` 0 (OWN fix PASS, real TL2026 `lualatex/biber`, 5 pages, new EDITORIAL
  receipt `EDITORIAL_PUBLICATION_SOURCE_V1/LONGFORM_GENERATED_V1` with `authored_refs`
  proposed-publication-authoring (new lf-ed-4) + accepted-draft-archive (same Draft `b869...` as
  renewal U5 `authoring_refs`, path+sha exact), reviewed NEW reader `62336c...`, staged newP path +
  new retention, closure 63). Prior receipt `VERSIONED_RENEWAL_SOURCE_V1` with renewal
  `authoring_refs` (not old `authored_refs`) now dispatches via fully validated public
  `validate_renewal_receipt` (detached CURRENT proof + HIST+CURRENT), no fallback, no kind/digest
  rewrite, route equality enforced. Old EDITORIAL/initial branches unchanged.

- Postrender QA+reviews + finalize + activate + history/current:
  QA fresh (4 DETERMINISTIC with NEW trio/PDF SHA, page count, scope G7) 0 + semantic (9 checks) +
  visual (5 checks) via `build_review_record` on NEW manuscript/PDF (preload 35 py, synthetic, no
  genuine approval) 0. Finalize seal `publication-set.json` written + `validate_prepared_set` OK,
  but wrapper `ed-finalize` TIMEOUT 1200s (performance, not defect; seal valid, preserved, no retry).
  Activate record r9 `EDITORIAL_PUBLICATION_ACTIVATION_V1` written (G7 epoch `a7772a1`, reason G7,
  set `c4fb7f...`, supersedes r8) + resume State r8→r9 installed (State now r9 `7dfc73...`), wrappers
  TIMEOUT but State updated, preserved. History `HISTORICAL_VALID` (r9, set `c4fb7f...`), CURRENT
  `agent.validate_agent_state==[]` OK, receipt readback OK (`EDITORIAL_PUBLICATION_SOURCE_V1/
  LONGFORM_GENERATED_V1`). No NORMAL lifecycle (stage/Preview/Freeze/Release) — separate workers per task.

- Longform verdict: FULL renewal (U5) + renewal→editorial (lf-ed-4) prepare→QA/reviews→finalize seal→
  activate record→State r9→history/current COMPLETE, with performance TIMEOUT qualifications on
  finalize/activate/resume wrappers (seal/record/State all valid, preserved, no deletion). No
  CommitPoint/whole PASS. Production semantic NO-GO (synthetic), no genuine approval.

## WEEKLY (pending, precise — not complete at prepare only)

- Fixture: NEW independent clone valid U4 prePreview (`.../versioned-renewal-weekly-continuation-.../
  renewal-weekly` HEAD `afab176` r6 `dbeba4...` + wk-ed-renew-1/2/3/4 preserved) → NEW parent
  `.../versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly`, same isolation
  (clone/no-hardlinks/inert/no alternates/nlink1/inode disjoint/no GIT_*/TMPDIR). Copy 228 untracked,
  overlay 739 (style `a4bd...` preserved), patch edpub+test, SOURCE-only G6 commit `b5f5484`
  (ancestry OK).

- U5 fresh CURRENT on G6 (prior r6 → r7 REUSE, style preserved): `u5-prepare/qa/finalize/activate/history`
  all exit 0 (1200s, fresh Python). Chain 7, CURRENT OK. Preserved.

- Editorial wk-ed-renew-5 NEW (on U5 r7, not wk-ed-renew-4 reuse): staged Weekly envelope
  (headline/deck + 3 paras, para3 `The accepted source authors describe the tested method.`) +
  P1 `prepare_proposal` 0 + P1 stage 0 (both 1200s, preserved). P2R capture running when invocation
  timed out (1200s bound, no stdout, no PASS, no failure). P2V/P3S63/specs/prepare/finalize/activate/
  history/current OPEN. Weekly extended same paths needed (same OWN fix, same `authoring_refs`
  dispatch, `WEEKLY_GENERATED_V2` branch) — P1 positives already prove dispatch, but prepare (OWN fix
  seam) NOT yet proven for Weekly. Do NOT claim Weekly complete at prepare only.

- Weekly verdict: U5 COMPLETE, editorial P1/P1-stage COMPLETE, P2R→prepare→finalize→activate PENDING.
  Next worker resumes from P2R (preserved, no restart of P1 positives) with same G6 epoch, fresh U
  already active, new ID wk-ed-renew-5 preserved, then P2V/scope/P3S/specs/prepare (OWN fix) → real build
  → QA/reviews → finalize → activate → history/current. No source fixture commits, same isolation.

## Pins / raw

- Candidate edpub 85814 (264756B), new test 5e5a (4521B, 5/5 OK), H6fe86/P1825dba/PUB3f4039/S20f/HIGH9a/Reader098.
- FIXED739 20f1967f (739), style variants longform b1cbb/weekley a4bd, G7 a7772a1 / G6 b5f5484.
- Longform U5 r8 `3d39535d...`, lf-ed-4 r9 `7dfc73...` (set `c4fb7f...`, receipt EDITORIAL/LONGFORM, Draft `b869...`).
- Weekly U5 r7 (new, REUSE), wk-ed-renew-5 P1 0/stage 0, P2R pending.
- All `*-exit.txt`/`*-stdout.txt`/`*-stderr.txt`/`commands.log`/`now-iso-*` preserved in this dir +
  `run-u5-*/`, `run-ed-*/` subdirs; failed P roots/old C/old timestamps preserved in fixtures
  (lf-ed-1/2/3, wk-ed-renew-1/2/3/4, orphan r5, etc.); no cache purge/temp cleanup/network/old runners.
