# DM-001/019 implementation return — bounded General report

2026-10-03. Active unit completed per `implementation-task.md` under
`design/astra-selection.md` (corrected plan where consistent; original
design's rejected alternatives stay historical). No reconstruct
Commit/Push, Production/Summary writes, network, or next-unit expansion.
Astra review + distinct independent implementation review follow.

## 1. Candidate identity and isolation

- Successor **`490414cef5be71d3b373171d8abeb0674b1f1c71`**,
  tree **`f5009749e1b2bcd49b35c5c4320ec76f4c3568a6`**,
  direct parent **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`**
  (fixed-baseline recovery candidate; its tree `65703243…` untouched).
- Work DB `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`, branch
  `codex/dm001019-freeze-implementation`, inert origin, no alternates,
  own gitdir, pack inodes distinct from both sources, tracked-clean after
  commit. Evidence `evidence-impl-20261003T100801Z/00-isolation/`.
- Parent sources preserved: original + restored DBs untouched; portable
  recovery archive untouched. Parent witnesses ran on a separate
  byte-copy (`.../jgas-dm001019-parentwit-20261003T100801Z`), verified
  still at b40 and tracked-clean afterwards.
- Changed paths (only): `scripts/survey_publication_v2.py`
  (blob `12f22e87…`), `scripts/survey_profiled_freeze_v2.py`
  (`8d218aa9…`), new `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
  (`03cc6f9e…`). No schema/stage/workflow/config/other-producer edits.
  Commit used process-local `-c user.name/email`, real time, no amend,
  no hook bypass, no config rewrite. `git diff --check` exit 0.

## 2. Selected contract vs actual behavior

- Public `build_freeze` signature unchanged (verified by smoke assert).
  Internally resolves Candidate → validated bundle → named Profile
  (`prepare_freeze_inputs`); no caller tag/slug/Profile override, no
  convergence gate. Old two-string `publication.release_identity` kept
  but no builder calls it.
- Slug authority lives once in `publication`
  (`public_issue_slug_from_profile`, `profile_release_identity`);
  `profiled.*` are delegating shims (release workflow + existing tests
  keep working; `test_survey_profiled_freeze_v2` 4/4 green unchanged).
- Both builders enforce exact approval Candidate path+hash
  (`does not bind the exact Publication Candidate`), Candidate-bound
  pre-preview VISUAL, source/PDF/page chain, Candidate-bound Profile.
  Wrapper additionally requires State issue equality and bundle≡State-current
  Profile; keeps real `validate_agent_state`/lifecycle/approved-gate/
  approval-drift gates. Legacy `validate_visual_review` no longer on any
  Freeze path; legacy `build_visual_review` producer kept for compat only.
- Preflight computes exact bytes first (existing equal-payload files keep
  their bytes; SHA over actual bytes), then validates both full schemas
  and both target/parent conflicts (escape, same-target, input
  overlap incl. hardlink, symlink/nonregular targets, symlinked/non-dir
  ancestors) with zero writes. Compatible-Manifest-without-Freeze fails
  closed (documented conservative disposition).
- Pair-only exclusive writer (`O_CREAT|O_EXCL|O_NOFOLLOW`, write loop,
  owned-fd identity + known-prefix-partial verified cleanup, completed
  Freeze retained on Manifest failure, post-install byte rechecks).
  Other `_write_immutable` producers byte-identical behavior; profiled's
  now-unused private copy removed. No CAS/crash-atomicity/fsync claims.

## 3. Parent witnesses (b40, separate copy; logs in `10-parent-witness/`)

- W1a wrapper legacy load/type refusal: schema error naming the missing
  legacy `pdf_path`, no files written.
- W1b wrapper late exact-visual refusal (`Freeze record visual review
  diverges…`) with residual Freeze+Manifest SHAs recorded — the late-check
  defect, using canonical VISUAL at a non-hardcoded path so checkpoints
  stay valid.
- W2 lower-level mixed-Candidate (distinct path/hash, identical PDF)
  ACCEPTED with both outputs written — the PDF-only gap.
- W4 existing divergent Manifest: `refusing to overwrite divergent Release
  manifest` at the writer, Freeze residual written, Manifest unchanged.
- W3 workflow predicate (extracted fail-closed, dedented, executed
  locally): convergent `special/SP001` exit 0 with full authority stdout;
  divergent `special/SP002` exit 1
  (`Release Manifest public identity mismatch: special/SP002 !=
  special/SP002-DIVERGED`).
- Honest paths recorded: revalidation Fixture is Weekly-only (extended via
  canonical-layout subclass, not stubs); second Candidate chain shares the
  canonical `main.tex`/PDF (manuscript rule) with distinct bundle/review/
  candidate bytes; wrapper mixed-State case would trip State provenance
  first (covered at shared-prepare level instead).

## 4. Final exact-head tests (committed `490414c`; logs in `30-tests/`)

New `tests/test_survey_dm001_019_freeze_equivalence_v2.py`: **19/19 OK**,
0 failures/errors/skips (182 s). Weekly + Thematic convergent/divergent
positives on real State fixtures (no `_safe_state_profile`/
`validate_agent_state` mocks); canonical↔wrapper byte equality both
orders (L-2, W-3b); legacy/mixed/divergent negatives pre-write with
before/after byte assertions; 8-case writer conflict matrix incl.
compatible-Manifest-without-Freeze; idempotent retry; real pre-open,
mid-`os.write` partial (owned-partial removed), and Manifest-install
(completed Freeze retained + retry) fault injection at the write
boundary; genuine `FROZEN` admission (Weekly + Special); saved workflow
predicate exit 0 with exact tags for all three pairs.
Affected existing at same HEAD: publication 8/8, profiled 4/4,
freeze-stage-boundary 8/8 — all OK. Total **39 methods, 0 skips**.

## 5. Limitations and residuals

- Initial run1 had 2 failures + 1 error, all harness-oracle side
  (missing legacy schema copy in self-contained root; directory-target
  error-specificity prompting a preflight reorder; stale-approval oracle
  naming the real drift gate). Raw logs preserved (`new-module-run1*`);
  nothing reworded into success.
- Per-method HEAD pinning is not claimed; each module run is bound to
  exact HEAD/tree/parent/clean-tracked guards in its log dir.
- L-8(a) read-only-dir refusal assumes non-root execution (uid 1000 here).
- No global atomicity: Manifest-install failure leaves a valid Freeze
  requiring identical retry (tested); foreign residuals are never
  deleted (tested: explicit refusal, bytes preserved).
- Retrospective full flow not claimed; existing pure identity regression
  untouched. DM-003/004, build transfer, DM-016/017/018/020, findings
  transport, whole-candidate audit remain separate.

## 6. Successor packaging and stop

- `50-packaging/`: `successor.patch` (101,721 bytes) verified with
  `git apply --check` against pristine b40 (exit 0, parentwit untouched);
  `successor-manifest.json` (machine-generated from parsed git output:
  HEAD/tree/parent, 3 file modes+blobs+worktree SHAs, 7 new objects);
  `changed-files/` copies + SHA256 list. Restore path: verified parent
  portable snapshot (prerequisite, untouched) + this delta; old restore
  scripts were not rerun; no full clone/bundle created.
- No fixture objects in reconstruct's DB; reconstruct worktree itself
  unmodified by this unit (only new packet files, uncommitted, Human-owned).
  Root review, then independent reviewer distinct from the implementer.
  Stop here.
