# Freeze transitive correction — PUB shared-wrapper + M1-M6 (owned only)

2026-10-25. FRESH AUTHOR PUB correction. Replaces failed operation session taskinvalidparameters; no cause investigation.

Binding: `AGENTS.md` Re:Phase-1 (contract478f0051 incl §11 unchanged), ROOT `7d7d5a4552eb7a1abcbafa79d8f358ff10ec96e885b55f09f271766b136cab57` §6,
`notes/rephase-1-versioned-renewal-implementation/resume-20261025/astra-integration-corrections.md`,
`independent-operation-review.md` §§5-6 (M1-M6 narrow OPEN + 5 Root corrections CLOSED),
`weekly-integration/result-matrix.md` §5 + `longform-integration/README.md` §3/§5 Freeze blocker
`ValueError ... materiality-ledger not allowed (exact producer map)` at `survey_publication_v2.py:684`.

## Ownership

- OWN ONLY: `scripts/survey_publication_v2.py` + new dedicated tests in this packet.
- Other authors P1/H; don't edit those/source/HIGH/Reader.
- FIXED736 INPUT READONLY `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work`
  PUB `90d90738dc2fc0c57a22f9656659a6e3665d262919b17f259811d035dac3d8c6` same current before change.
- Current candidate `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  actual409+inherited57+partial implementation. Before change PUB `90d90738…`, after fix `be5c29f2…` (grouping) → final `TBD` (with M1-M6).
- Preserve failed root V1 evidence in `operation-correction/` (not deleted).

## Fix summary (actual complete PUB function, not header-only)

### Shared wrapper (weekly/longform blocker)

- Collect retained `checkpoint_provenance` fixed research stage refs grouped by EXACT `(path,sha)` FIRST,
  union configured producer stages/artifact roles for shared `CANDIDATES_NORMALIZED` evidence/materiality/completeness.
- Validate expected `from/to/checkpoints` and required artifact set exactly; don't first validate as `evidence` then reject ledger.
- Preserve `Profile.source_root`/config-bound paths, no literal `sources/{issue}`.
- External QA bundle `checks[].result` files, not invented `R/qa-checks.json`.
- ALL historical scope refs allowed typed lineage, not global count1.

Expected (pipeline order, exact):
- discovery: ISSUE_INITIALIZED→DISCOVERY_COLLECTED, checkpoints [discovery], required {discovery-acceptance}
- screening: DISCOVERY_COLLECTED→CANDIDATES_NORMALIZED, checkpoints [screening], required {screening-acceptance}
- evidence+materiality+completeness shared: CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED, checkpoints [evidence,materiality,completeness],
  required {evidence-acceptance,edition-views-acceptance,materiality-ledger,profile-completeness}
- selection: EVIDENCE_REVIEWED→SELECTION_COMPLETE, checkpoints [selection], required {candidate-matrix,candidate-selection}
- architecture: SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED, checkpoints [architecture],
  required {issue-architecture,architecture-review-summary,architecture-review-attention}
- draft: ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE, checkpoints [draft],
  required static {synthesis-input,synthesis-result} + valid dynamic draft-package:/draft-result: (no other).

### M1-M6 typed transitive (exact field names + known implicit relativa, no generic walker)

- M1 Evidence: package `tasks[]{evidence_task_id,path~tasks/task-[hex20].json,sha256}` relative to package parent;
  acceptance `results[]{evidence_task_id,sha256,filename}` → `run_dir/tasks/<basename>` + `run_dir/results/<basename>` (same-basename-as-task);
  `authority_supplement{path,sha256}` + `sources[]{raw_path,raw_sha256,byte_count}` under `source_root`; prompt/contracts explicit paths.
- M2 Screening: package `input.batches[]{batch_id,path~input/batches/batch-[0-9]{3}.jsonl,sha256}` relative to package parent;
  `results/<batch_id>.json` with `result_sha256` from acceptance `batches[]`; prompt/result_contract explicit.
- M3 Discovery: `records[].raw_refs[]{path,sha256,byte_count}` (repo-relative, e.g. raw/source.json) + `discovery_path` JSONL already pinned.
- M4 X: `production_profile{path,sha256}`, `runs[].task{path,sha256}`, `runs[].result.raw{path,sha256,byte_count}` (x-source-intake-v2 exact).
- M5 Views: `views[]{evidence_task_id,view_sha256}` → `views-accepted/<view_set_sha256>/views/view-{sha256(task_id)[:20]}.json` (view_filename convention).
- M6 Ledger/Selection/Synthesis/Draft/archive: basis SHAs only, rows inline per schemas (no separate file refs);
  explicit per-type loads verify no hidden `path/sha256` in rows + already-pinned artifacts cover all.
- All E live/COPY SHA/size FD-bound (`_fd_read_bytes` + `_strict_json_from_pinned`, no second fresh read without expected SHA);
  current tools/config/schema actual current (closure + explicit prompt/contracts); historical T Git-epoch (H scope, not live-old compare).
- Retention COPY→retained_dest, KEEP→live path (not T rows from receipt closure/graph); snapshot complete historically validated E.
- Both snapshot + preflight lex/inode overlap use complete deduped typed refs.

## Verification plan (no whole PASS/CommitPoint)

- Fresh independent copy existing baseline old R3 (721a04d) + fixed736 (736 files, manifest d7d7f6df…) + ONLY this PUB patch
  source-only commit before U authority (don't execute candidate while others write).
- U activate + synthetic Preview→Freeze should success; recorded_at monotonic.
- Timings: old U finalize 65s, new H batch faster at fixed70. Use 1200s phase bound + terminal exit/PID logs, not 300s fixed harness;
  if timeout profile exact counts, no helper fake PASS.
- Late-swap at prep→install Evidence card/task/raw/view/retention COPY/config/scope must refuse with zero new Freeze Manifest,
  exact byte repair healthy control. Partial unit controls, not string tests.
- No network/old runner exec/cleanup failed fixtures/candidate or reconstruct ordinary commit.

## Pins (initial, updated after run)

- Reconstruct HEAD: f84fcf5321be3798c862c0156278afbba01f89f6
- FIXED736: snapshot-work HEAD 409b292, 736 files, dst-hash d7d7f6df0bbde842c0270d00f493b01e5be2d19fd48ccae56086f5cf4ca3a129
- Candidate-work before: PUB 90d90738… (1616 lines, 92396B)
- Candidate-work after grouping fix: PUB be5c29f256ef463168e9229bff96fdf319260007eb2008b1a7b9116f988db2dd (1682 lines)
- Final PUB after M1-M6: TBD (this packet)
- Fixture: TBD (fresh weekly U1, see setup-*/run-*/ raw)
