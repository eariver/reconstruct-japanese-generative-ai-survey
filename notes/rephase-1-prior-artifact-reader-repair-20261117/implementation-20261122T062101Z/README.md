# Prior-artifact reader repair — bounded implementation (no commit)

Root: `../astra-repair-resolution.md` FULL §§1–2. Independent map GO (`../independent-map-review.md` + machine). Source-only map `../integration-map.md` + machine.

Author copy: `.rephase-1-editorial-runtime/prior-artifact-reader-implementation-20261122T062101Z/candidate-work` (independent `cp -a`, no hardlinks — inodes differ, no alternates/commondir, inert origin `https://invalid.invalid/inert.git` preserved, no remote/config/HOME mutation, cache exclusion explicit — no `__pycache__`/`*.pyc` created with `PYTHONDONTWRITEBYTECODE=1`).

## Source identity (full, no prefix)

- HEAD `3231a0c280287411513bba359f4d3d2b6703d591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367` (`rev-parse.txt`, `HEAD.txt`).
- `f591` missing in new DB (`cat-file -e` exit 1), `d591` exists. Prior `f591` prose superseded, frozen files untouched.
- 774/774 intended files match frozen manifest `0dc361cb…`/187361B (bytes+SHA256+physical mode 0 mismatch). `source_identity.author_head f591` ignored ONLY with corrigendum; bytes authority unchanged.
- States/CP/completion/four refs/14 outputs match `entry-binding-r2-machine.json` (W34 State `a858…`/4162, SP State `38a634…`/4266, W34 Profile `2a8c…e121`/2371, SP Profile `aff0…`, CP `73ab…`/`2a528…`, guards absent, forward `EVIDENCE_REVIEWED/SELECTION_COMPLETE` absent). Tracked `M sources/*` in both old and new copies are inherited worktree-vs-HEAD deltas (real-material outputs), not test mutation — hashes still match entry-binding; only new `M scripts/survey_stage_validation_v2.py` + `?? tests/test_prior_artifact_reader_repair_v2.py` are this unit.

## Change (one function + one test, existing imports only)

`scripts/survey_stage_validation_v2.py::_prior_artifacts` 351–411 (diff `raw/source-diff.patch`, 47 lines):

- Per-row `low.load_typed_checkpoint_record` before dedup; `ResearchAuthorityError` → `StageValidationError` fail-closed.
- `PREARCH`: `name not in DM022_PREARCH_CHECKPOINTS → DM022_WRONG_FAMILY` even if `rel` seen; distinct `rel` → `agent._validate_checkpoint_record(...,revalidation=None,pending_basis=None)` (770–805 PREARCH branch: provenance SHA, typed load, role 186–287, same path-AND-sha triplet, issue, `_validate_prearchitecture_core_proof` 290 → `low.check_supersession_record...` 4949 FULL graph, no State/LIVE guard/HIGH); `errs` joined on raise; merge exact 4 rows with live `sha256_file` + `resolve()` conflict, NO `superseded` override; `seen.add`, `continue`.
- `LEGACY`: `family != LEGACY → refuse`; existing 362–375 byte-for-byte with `bound_prior/superseded` allowance; active7 376–422, `_merge_artifacts`, entry/prepublish READY, report unchanged. No `validate_agent_state`/guard/HIGH in reader. No new module/schema/family/flag/cache/verified-dict/public flag/third validator.

New `tests/test_prior_artifact_reader_repair_v2.py` 408 lines, SHA `926af0…`, mode `0o664`: genuine HIGH-adopt synth PREARCH (WEEKLY/THEMATIC) via `test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests` (`_chain_root/_materialize_production_discovery_acceptance/_make_evidence_reviewed_state/_prepare_and_decide/high.adopt_revision/_build_selection_input`) + real `run_selection_architecture_v2_interactive.run` 7 outputs, own epoch (no 480 literal), process-scoped Git identity, inert origin, no empty/amend/config.

## Focused evidence (actual, 2026-11-22T06:29:38Z–06:33:27Z UTC, 228.541s, exit 0)

`python3 -u -m unittest tests.test_prior_artifact_reader_repair_v2 -v` in new copy, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0`, scrubbed `GIT_*` overrides, `raw/stderr.txt` (1455B), `raw/exit.txt 0`:

- Weekly PREARCH public `validate_stage EVIDENCE→SELECTION` PASS (exact `CORE_STAGE_CONTRACT` keys, `implementation_commit_sha==HEAD`, no-overwrite rerun) → `build_stage_checkpoint/advance` to SELECTION_COMPLETE → public Architecture validate → advance to ARCHITECTURE_ESTABLISHED pending Human. Old code would refuse with `'from_state' required`.
- Thematic same full route PASS.
- LEGACY same-record stays LEGACY, public PASS.
- Negatives fail-closed no report: wrong-family alias after seen (`DM022_WRONG_FAMILY`), unknown kind (`UNKNOWN_KIND_X`), malformed SELF (`00*32`), split SHA (`11*32` triplet/provenance), artifact drift one-byte/missing, `_merge_artifacts` replace-refusal collision, guard: `_prior_artifacts` allows guard while `validate_stage` refuses `DM022_TRANSITION_ACTIVE`, restore re-passes. Two faults first failed on too-narrow regex (provenance drift before kind/SELF) — preserved in earlier run, fixed by updating provenance in temp State so entry passes and exact kind/SELF predicate fires; final 8/8 PASS.

No real W34/SP validation/writer/regeneration, no CURRENT pack, no State/Profile repin, no manual CORE report, no source commit (author commit NOT authorized yet). Failures preserved, retries uniquely logged. New scope gaps STOP to root.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Return for root + independent implementation review before commit/real-material stage.
