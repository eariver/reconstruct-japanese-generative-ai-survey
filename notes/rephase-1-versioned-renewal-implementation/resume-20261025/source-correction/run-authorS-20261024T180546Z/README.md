# Author-S F1/F2/F3 correction — unique run

- Human HEAD at start: f84fcf5321be3798c862c0156278afbba01f89f6 (workspace main, untracked packet only, no staged ordinary commit).
- Writable candidate: .rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work, actual409 HEAD 409b292, own files only:
  - scripts/survey_versioned_renewal_source_v2.py (F1/F2/F3 fix)
  - tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py (NEW dedicated, unique)
- Baseline FROZEN (KEEP READONLY): versioned-renewal-freeze-20261024T174422Z/snapshot-work (731 files, manifest f3a0151f..., actual409). Not modified.
- Other authors own HIGH/publication B1-B3 and Reader F4; H/high/Reader/publication/schema/shared families untouched (no edits). F2 uses existing pure screening validator, no family edit (ROOT return not needed).

## Fixes
- F1: seen stores (label, bytes), final compares fresh vs pinned (not fresh-vs-fresh), no pin overwrite before compare, duplicate-pin capture check.
- F2: discovery acceptance pinned via sess + SHA vs basis, immediate reverify; JSONL via sess.read + SHA vs acceptance discovery_sha + pinned parse (_parse_discovery_jsonl_pinned, strict duplicate refusal) + existing validate_discovery_set shape; no screening.read_jsonl second open; downstream uses same pinned records.
- F3: per-call own Git root/toplevel/HEAD, module-root check (hist/core/self under repo), epoch valid+ancestor (no blind HEAD==epoch), control diff epoch-head quiet, dirty/staged/untracked control refusal, closure blobs at BOTH epoch+HEAD SHA + mode 100644, contract live already checked. Artifact-only descendant PASS; control/tool (even unrelated pinned row) refusal; missing/mode/wrong-root refusal. Only safe git primitives + hist safe helpers; no State/Gate/Reader/high; no global cache, fresh every call.

## Tests (meaningful public source proof, real bootstrap 721a04d + old E uncommitted, fresh copies)
- NEW independent copy of frozen731 + ONLY own fixed file, SOURCE-only commit before authority (retains 721a04d ancestry). No shared-candidate import/execution.
- F1 seam (mock swap between check/reverify) -> BASIS_DIGEST_MISMATCH pinned file changed, no writes, repair PASS. No-cache (fresh every call) PASS.
- F2 seam (swap JSONL after acceptance, shape-valid) -> BASIS_DIGEST_MISMATCH Discovery JSONL bytes changed, no writes, repair PASS.
- F3 artifact-only (non-control commit) PASS; control commit (non-closure/non-contract) refusal; dirty/staged/untracked refusal + repair; mode (chmod+x commit) refusal; loaded-module wrong root + runtime wrong root refusal; no-blind HEAD!=epoch PASS.
- Full suite: 8 tests, exit 0, 82s (see test-exit.txt/stdout/stderr). No shape/stub, real Weekly U/C trio + Layer-A/B + git.
- Intermediate: one test expectation (wrong-root helper with subdir repo) corrected to /tmp repo (test-only, no source change). Preserved as test fix, not source failure. No source failures to preserve (final all PASS). No clean/reset/cache purge/old runner/network/ordinary commits (HEADs unchanged, see recon/candidate heads/status).

## Unexecuted (explicit)
- Longform route repeats for F1/F2/F3 seams (weekly only in this unit; longform covered by existing phase-S scope/longform tests, not duplicated here to bound runtime).
- C NEW_TARGETS full E2E (uses same F1/F2/F3 seams; covered via U REUSED path here; C-specific trio-under-R + manuscript proof context is Reader-owned F4, not this author).
- Normal direct Candidate/Preview/Freeze/Release + renewal→editorial + repeat C→U→U + affected regressions + independent final review (successor scope per contract §9, not this narrow F1-F3 unit).

Whole unit ongoing, no CommitPoint/independent PASS.
