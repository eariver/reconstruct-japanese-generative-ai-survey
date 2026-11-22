# Independent real-validation review — prior-artifact reader repair (read-only, fresh)

Role: fresh independent outcome/source reviewer, not author/operator/root. No validator/writer/runtime imports, tests, network, source/ref/config writes, subagents. Stdlib JSON/hash/pathlib/stat only plus read-only `ps` for owned PIDs and read-only Git with explicit named DB, lazy fetch disabled, no reconstruct readback.

Bound inputs (read FULL):
- `notes/rephase-1-prior-artifact-reader-repair-20261117/astra-repair-resolution.md` FULL, mandatory §§3–4 latest deviations.
- `notes/rephase-1-prior-artifact-reader-repair-20261117/real-validation-20261122T065238Z/README.md`, `machine.json`, `launcher-prior-reader-validation.py`, `raw/SP/*`, `raw/W34/*`, `raw/SP-harness-import-failure-20261122T065315Z/*`.
- Actual NEW real `.rephase-1-editorial-runtime/prior-artifact-reader-real-20261122T065145Z/candidate-work` and author `.rephase-1-editorial-runtime/prior-artifact-reader-implementation-20261122T062101Z/candidate-work`.
- Prior entry `notes/rephase-1-selection-architecture-resume-20261117/entry-binding-r2.md` + machine for States/Profiles/CP/completion/8 refs/14 outputs expectations.
- Frozen manifest `notes/rephase-1-selection-scaling-repair-20261116/source-packaging/final-20261116T031000Z/complete-selection-scaling-manifest.json` SHA256 `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150`/187361B.

## 1. Source binding (fresh stdlib, both copies)

- Declared new source: HEAD `e59fa9bc5f323a640fd922412de7757e60eb5944`, parent `3231a0c280287411513bba359f4d3d2b6703d591` (d591, not f591), tree `e5e888cbb285dc32c60b422a41b24acc044378e6`, commit body 390B, SHA1(`commit 390\0`+body) recompute match True.
- Read-only Git explicit named DB, `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 GIT_NO_LAZY_FETCH=1`, `--git-dir=<named>/.git --work-tree=/tmp/ignore`, no reconstruct Git:
  - Both `author` and `real` copies: `rev-parse HEAD` = e59…, `HEAD^` = d591, `HEAD^{tree}` = e5e8…, `cat-file commit HEAD` 390B recompute e59… True, `log -1 --format=%B` = `Prior-artifact typed reader: strict PREARCH dispatch in _prior_artifacts + focused public tests (2 files)`, author `Prior artifact reader repair <prior-artifact-reader@example.invalid>`.
- Declared delta: 775 = old 774 manifest 0dc3… + changed `scripts/survey_stage_validation_v2.py` SHA256 `1e4c818b144ebeed7a4365cb00b5e43ed93e9bff4d1396691432ba77a515787e`/51927B + new `tests/test_prior_artifact_reader_repair_v2.py` SHA256 `1fb831673b8291813ab0480720f84467e334374619a87fe072ff00c63438d4db`/30019B, both `0o664`.
- Fresh hash both copies (hashlib):
  - `scripts/survey_stage_validation_v2.py` 51927B 1e4c… both OK.
  - `tests/test_prior_artifact_reader_repair_v2.py` 30019B 1fb8… both OK.
  - Other 773/773 vs frozen manifest bytes+SHA256+physical mode 0 mismatch, 0 missing, both copies. Total 775 bound.
- No head ref mutate, no shipping pack, no ordinary Commit/Push observed in this review.

## 2. States / Profiles / CP / completion / refs / outputs (fresh now)

Real copy fresh now (author States same, reports differ as expected):
- W34 `sources/2026-W34/production-state.json` 4162B `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`, lifecycle `EVIDENCE_REVIEWED`, history len 4, init `48082356` — match entry-binding.
- SP `sources/SP-efficient-llm-2026/production-state.json` 4266B `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`, same lifecycle/shape — match.
- W34 Profile 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`, SP Profile 13748B `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45` — match.
- W34 CP `.../w34-repaired-20261112-r2/checkpoint/record.json` 6054B `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`, SP CP `.../sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5` — match, kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`.
- Completion W34 1972B `80c12d0c53a76f21e3000c4e48a8e4ab843c2c63ac9cc69aeb3c9f20ddc46835`, SP 2009B `70d8c0896d2ce37c0aea2dc4e92cc4ef5008c48eddd54d2994d1f9c9fe41b8eb` — match.
- Retention state-before W34 4087B `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0`, SP 4194B `180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220` — match.
- Eight typed refs all match entry-binding (fresh): W34 evidence 126592B `eef77479…`, views 159502B `3727485a…`, ledger 186214B `066230f4…`, profile-completeness 71532B `d869027a…`; SP evidence 49237B `7f04e9ad…`, views 64222B `45d60f9f…`, ledger 66850B `5cf81f8f…`, profile-completeness 34249B `b4378609…`.
- Fourteen outputs all match fresh now: W34 matrix 683098B `f4469c85…`, selection 375063B `f3a5000f…`, architecture 24447B `9a76294e…`, summary 314350B `1b7f6076…`, attention 18437B `d68b5f31…`, input 378396B `15375476…`, audit 1436B `61d6a0bc…`; SP matrix 239359B `2f62e2a8…`, selection 76603B `4e6884d6…`, architecture 33219B `4af84ab3…`, summary 67700B `d0092e13…`, attention 15918B `482f3c21…`, input 72613B `072f90b6…`, audit 1530B `ad5474da…`.
- Guard `orchestration/v2/acceptance-revision.guard.json` absent both (file-existence only) — match.
- Canonical checkpoints absent both editions: `orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json` absent, `SELECTION_COMPLETE.json` absent — no checkpoint/advance dispatched, match expectation.
- New pre/post inventories: SP `pre-inventory.txt` HEAD e59 + State 38a…, `post-inventory.txt` State 38a… + report exists True 1704B; W34 `pre-inventory.txt` HEAD e59 + State a858… only, no `post-inventory.txt` in packet (limitation, see §5). Author copy States same as real, reports absent both (pre-validation state).

## 3. SP PASS report (actual 1704B)

- Path `sources/SP-efficient-llm-2026/orchestration/v2/stage-validation/prior-reader-selection-r1.json` EXISTS in real copy, 1704B SHA256 `e42455130c8c68f5ca8975e521d0b32e4e1b31a6eb7ef5bbf53dc5907e66bd4f` — match declared.
- JSON 12 keys: `schema_version/check_id/status/issue_id/from_state/to_state/production_state/production_profile/implementation_commit_sha/contract/artifacts/recorded_at`.
- `CORE_STAGE_CONTRACT PASS`, `EVIDENCE_REVIEWED→SELECTION_COMPLETE`, issue `SP-efficient-llm-2026`, impl `e59…` (current HEAD, no fake old impl), `production_state` 38a… + `production_profile` aff0… unchanged, artifacts matrix `2f62…`/selection `4e68…` match 14 outputs, contract 8 keys (pipeline/quality/research/publication version+sha).
- Raw SP: `argv.txt` exact normal CLI (`--repo-root <real> --config config/survey-production-v2.json --state sources/SP-... --artifact matrix/selection --output .../prior-reader-selection-r1.json --recorded-at 2026-11-22T06:53:45Z`), `cwd.txt` real copy, `env-whitelist.txt` `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 ... launcher v2`, `start.txt` 2026-11-22T06:53:45Z, `end.txt` 07:07:45Z, wall ~840s, `pid.txt` 1528119, `exit.txt` 0, `stdout.txt` report path (243B), `stderr.txt` 0B, `stack-trace.txt` 10822B (2× 5-min faulthandler dumps, see §4).
- No reviews/checkpoint/advance; State pre/post unchanged.

## 4. W34 blocked (report absent, phase beyond prior Schema)

- Path `sources/2026-W34/orchestration/v2/stage-validation/prior-reader-selection-r1.json` ABSENT in real copy (and author) — match declared.
- Raw W34: `argv.txt` exact normal CLI with W34 issue/paths `--recorded-at 2026-11-22T07:08:03Z`, `cwd.txt` real copy, `env-whitelist.txt` same launcher v2, `start.txt` 07:08:03Z, `end.txt` `2026-11-22T07:28:53Z (tool 1250s timeout, >1200s bound)`, `pid.txt` 1529795, `exit.txt` 124, `stdout.txt` 0B, `stderr.txt` 0B, `stack-trace.txt` 11463B, `timeout-note.txt` `timeout 1200s bound exceeded, tool killed after 1250s, child reaped, report absent, State unchanged`, `pre-inventory.txt` HEAD e59 + State a858… (no post-inventory file).
- Stack phase (faulthandler, 5-min repeats, separate packet file):
  - SP dumps (2): `_evidence_basis→_selection_basis→_validate_stage_semantics` at `_repo_file/_assert_pin_repo_ancestors` and supplement `sha256_file/_supplement_entries_for_package` → `_validate_evidence_acceptance_content` → `_verify_adopted_graph_full→check_supersession_record...→_validate_prearchitecture_core_proof→_validate_checkpoint_record` + `_recheck_phase_pins/_recheck_supplement_context/_supplement_source_file`. No `from_state` refusal.
  - W34 dumps (4, incl 2 `<invalid frame>`/pathlib windows): `_prior_artifacts` refusal GONE; stuck in full semantics `_evidence_basis/_selection_basis/_validate_stage_semantics`: `_recheck_phase_pins→_recheck_supplement_context→_validate_evidence_acceptance_content` (+ screening variant `validate_screening_acceptance→validate_package_basis→verify_current_stage_basis→validate_agent_state→_validate_checkpoint_record→_validate_prearchitecture_core_proof→check_supersession...→_verify_adopted_graph_full`) and supplement Raw `_supplement_source_file/relative_to` + FULL PREARCH proof. Precise cost question preserved.
- Classification: sampled stacks show work at those locations, not deadlock proof and not exact cost attribution. Proves progress beyond repaired prior-reader Schema, not exact W34 Selection cost. Exact cost remains UNKNOWN, now bounded below by >1200s for W34 Selection on this copy.

## 5. Launcher, PIDs, timeout/exit, deviations (honest)

- Launcher file `launcher-prior-reader-validation.py` 2455B SHA256 `5bdf027b5e6fb04931cc2110a96f0bcf9f7f9d87002f9086f6d5dde9089dbfd2` is v2 (adds repo-root to `sys.path`, mirrors `python -m`, stdlib `faulthandler/runpy/sys/pathlib`, `dump_traceback_later(300,repeat)` to separate `raw/<ED>/stack-trace.txt`, executes unchanged module main through `runpy.run_module` with exact normal CLI argv, no project mock/wrap/fake proof/checked context/source patch). Bound as operation evidence, not shipping source.
- Raw v1 missing (honest): `raw/SP-harness-import-failure-20261122T065315Z/` preserves `argv.txt` (recorded-at 06:53:15Z, same SP target, stackfile `raw/SP/stack-trace.txt`), `pid.txt` 1526696, `start/end.txt` 06:53:15Z, `exit.txt` 1, `stderr.txt` 1226B `ModuleNotFoundError: No module named 'scripts'` → `ImportError: ... scripts.survey_stage_validation_v2`, `stdout.txt` 0B, `stack-trace.txt` 0B, `pre-inventory.txt`, `post-inventory.txt`, `cwd/env-whitelist`. No separate v1 script bytes preserved; v1 failure inferred from stderr + v2 diff prose. Do not reconstruct lost v1 bytes.
- First SP launcher import failure is genuine recorded exit 1, but operator changed launcher and retried without root return despite §3 `Stop each edition on first refusal/import error/timeout; no local repair/retry/timeout extension`. Second SP attempt `attempt.txt` `launcher fixed v2 ... + direct -m equivalent; SP attempt2`, PID 1528119, exit 0. This is unauthorized local retry v2, no excuse genuine first. Later SP PASS does not retroauthorize it.
- W34 had no enforced 1200s child deadline (launcher only dumps, no kill; no `timeout` command; packet `env` notes `no timeout command (tool bound 1250s)`). Actual run 07:08:03Z–07:28:53Z = 1250s tool kill, exceeding dispatched 1200s bound. Exit 124 is tool/wrapper timeout-kill convention (with `timeout-note.txt` observer evidence), not normal validator CLI exit and not validator `StageValidationError` refusal. `stderr/stdout` 0B consistent with kill, not with validator report path. Classify honestly as external kill.
- Review deadline 1200 not implemented; tool 1250 kill actual exit 124 may be wrapper convention/manual not normal CLI exit — inspected raw `exit.txt` + `timeout-note.txt` + `end.txt` observer evidence as above.
- Owned PIDs read-only: `ps -o pid,ppid,stat,cmd -p 1528119,1529795` on 2026-11-22 returned header only, `ps_exit:1`, no rows. Both children currently reaped/absent, no kill issued, no unrelated search. First-failure PID 1526696 not re-checked per scope (only 1528119/1529795 + documented parent if needed). No directly documented owned launcher parent PID needed beyond reaped children.
- SP reaped and W34 pre unchanged, so W34 run was lawful single attempt in source/authority terms, but timeout/retry deviations above remain and operator `no extension/retry` prose is withdrawn for those actions per Astra §4. Source/code and real State not authorized to change during attempts — verified unchanged above.

## 6. Limits (not obscured)

- Fresh current hashes here verify current bytes only; they do not retro-certify every pre-window. Original pre/post inventories are spot copy (`HEAD + State` + SP report existence), not full-tree proofs. W34 has pre only, no post file; current State match corroborates narrowly, not as retroactive per-run proof.
- Full 775 worktree-vs-manifest verified now for both copies; committed blobs/modes vs worktree for 775 via `rev-parse/cat-file` + worktree hash only — no `diff --stat` whole-tree claim where partial DB missing blob would block (STOP rule respected in operator packet).
- Stacks are same-child `/proc` windows, not whole-tree/disk/net totals; `Timeout (0:05:00)!` dumps show locations, not deadlock or exact speedup/cost.
- Independent synthetic both-routes PASS referenced from implementation review, not re-executed here. No real W34/SP writer/regeneration, no CURRENT pack, no State/Profile repin, no manual CORE report observed.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN preserved.

## 7. Verdict

Bounded reader-repair mechanical SP PASS (real normal Selection report-only, exit 0, 1704B e424…, 12 fields, current impl, unchanged State/Profile/artifacts) plus synthetic Weekly+Thematic both-routes PASS (transcribed, not re-run here) supports compatibility fix. Real W34 Selection remains BLOCKED by observed cost (>1200s, tool 1250s kill, exit 124, report absent, phase beyond prior Schema). This is not Selection/Architecture full PASS, not Human approval, not R4 audit, not benefit/savings proof.

## 8. Minimal next investment (no code authorized here)

Observed full-stage revalidation cost question only: bounded single-attempt real W34 Selection with enforced child deadline + same scoped faulthandler observability, on frozen e59, no source change, no generic reader/new module/schema/family, no auto retry/extension. If W34 still exceeds bound, return concrete phase/cost blockers before broadening. No performance implementation selected here; source map + actual stacks will support closeout decision. No validator/writer/runtime/test/network/source/ref/config writes in this review.

Exact binding: e59 `e59fa9bc5f323a640fd922412de7757e60eb5944` / d591 `3231a0c280287411513bba359f4d3d2b6703d591` / tree `e5e888cbb285dc32c60b422a41b24acc044378e6` / 390B recompute True / 775 (773 unchanged + 1e4c…/51927 + 1fb8…/30019) both copies / SP 1704B `e42455130c8c68f5ca8975e521d0b32e4e1b31a6eb7ef5bbf53dc5907e66bd4f` 12 fields PASS / W34 absent / PIDs 1528119 exit0 840s, 1529795 exit124 1250s tool kill, both reaped (`ps_exit:1`) / timeout scope 1200 dispatched not enforced, 1250 actual / launcher v2 2455B `5bdf027b…`, v1 bytes missing honest.
