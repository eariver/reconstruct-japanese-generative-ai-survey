# Author-S style-template CURRENT fix — unique run

- Human HEAD: f84fcf5321be3798c862c0156278afbba01f89f6 (workspace main, untracked packet only).
- Writable candidate: versioned-renewal-env-20261023T185000Z/candidate-work, actual409 HEAD 409b292, ONLY own files patched:
  - scripts/survey_versioned_renewal_source_v2.py (style CURRENT fix + preserved F1/F2/F3)
  - tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py (appended style tests, F1-F3 preserved)
- Frozen baseline versioned-renewal-freeze-20261024T174422Z/snapshot-work (731 files) KEEP READONLY; fixture = frozen731 + ONLY own fixed S (HIGH parallel patch not mixed). No H/HIGH/schema edits.

## Source fix (BOTH routes, U+C)
- Fixed CURRENT template path `templates/survey/jgaisurvey.sty` via `_to_rel` + `_fd_read` (FD-safe, no caller style path from `trio["style"]["path"]`).
- Compare output trio style bytes == CURRENT template bytes; error `REUSE_TARGET_MISMATCH` for U (`REUSED_TARGETS`), `RENEWAL_PROOF_DIGEST` for C (`NEW_TARGETS`) per ROOT allowance.
- `validate_generated_closure` with CURRENT style text (not trio self).
- `trio_digest` uses `sha256(CURRENT style bytes)` (not prior output self).
- Live primary/bib vs re-derived kept; live style enforced via equality above.
- Closure (includes style template) + end rechecks (basis/proof/trio/closure fresh) capture CURRENT style; no global cache, fresh every call. Caller proof cannot choose style path.

## Tests (real 721a04d + old E, fresh copies, SOURCE-only commit before authority)
- Healthy unchanged style PASS (weekly U, prior trio style == CURRENT template).
- U negative: genuine committed style epoch (templates/... comment-only, still UTF-8, committed) + staged `style_input_ref` forged to new SHA (so H live passes) + staged/receipt/seal/record/basis digests updated + basis/proof closure updated to new style + new epoch, exact prior trio (old staged copy) held → `REUSE_TARGET_MISMATCH: output trio style differs from CURRENT style template`, NOT earlier `BASIS_CURRENT_TOOL_DRIFT` (closure) nor `HISTORY_*` (H). Proves S seam, not tool drift.
- C healthy: new R trio (rendered primary/bib + style copy of CURRENT template) → `CURRENT_PROOF_VALID`, copy consistency (new R style == CURRENT template).
- C postcheck: mutate new R style after proof → refusal (`RENEWAL_PROOF_DIGEST` style path, also trio reverify), repair (restore) PASS.
- Preserved F1-F3 8 tests (pinned reverify, JSONL pin, artifact-only PASS, control/dirty/staged/untracked/mode/wrong-root, no-blind HEAD!=epoch). Full: 11 tests, exit 0.
- Intermediate: drift test first failed at H (live style drift) before staged forge; fixed test-only (added staged forge, manual proof without verify) to isolate S seam, no source change. Preserved as test fix, not source failure. No source failures to preserve in final run.

## Unexecuted (explicit)
- Longform route repeats for style seams (weekly only here; longform shares same fixed template path/code shape, covered by existing longform scope tests, not duplicated to bound runtime).
- Normal direct Candidate/Preview/Freeze/Release + renewal→editorial + repeat C→U→U + affected regressions + independent final review (successor scope, not this narrow style unit).

Whole unit ongoing, no CommitPoint/acceptance.
