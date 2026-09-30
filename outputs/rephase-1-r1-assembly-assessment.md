# R1 e4-lineage assembly — Astra bounded completion

Recorded **2026-09-30T09:11:43+09:00** (root clock). **The seven-path assembly unit is complete at 481dec0**, with exact source/mode equivalence, selected fresh verification, root review and a separate author-independent assembly review. **Whole candidate remains NOT_READY; step 4/B3 and the canonical seven-point audit remain open.** This is isolated-candidate assembly, not production adoption.

Human explicitly requested that work pause at coherent boundaries and present a **Commit Point**. This unit ends here; the next prerequisite unit below is not started. Ordinary reconstruct Commit/Push remains Human-owned.

## Fixed assembled candidate

| Field | Value |
|---|---|
| HEAD | **`481dec0c0233d7871df79a07a88aa5fe2291daa3`** |
| Tree | **`657032438c6ed8b1c055d5a120b67b4b261a5092`** |
| Direct parent | **`e4c82692abee6acedbba07815b0d74ccefb80a7e`** |
| Branch | `codex/rephase-1-r1-assembly` |
| Independent fixture | `/tmp/jgas-rephase-r1-assembly-20260929T143833Z` |
| Inert origin | `https://example.invalid/rephase-increment-b.git` |
| Source increment | Reviewed R1 `b74db679f03908048db91420a8f262d412b8f58c`, seven paths only |
| Production baseline | `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, unchanged |
| Reconstruct starting HEAD | Human commit `a22d69308e9bbfb84cee9d8530c258a2a911d059`, clean and locally tracking origin/main |

This candidate restores **e4 ancestry**, unlike R1's fresh-root a1a4242-based implementation candidate. e4, B, R1 and prior witness databases remain preserved. Root independently read the assembled HEAD/tree/parent, tracked-clean status and exact seven-path raw tree diff; it also checked every resulting Git blob/mode against the reviewed b74 manifest. Python caches remain untracked, not silently deleted.

## Assembly and equivalence

[Milestone-1 manifest](../notes/rephase-1-r1-assembly/20260929T143833Z-assembly/manifest.json) / [report](../notes/rephase-1-r1-assembly/20260929T143833Z-assembly/report.md) / [actual apply-check record](../notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/apply-check.txt).

- General copied the e4 checkout **including its independent `.git` database** by byte-preserving native copy into a new absent destination; no archive/full clone/new-root substitution/worktree/shared objects. Own gitdir/common-dir, no alternates/symlinks, preserved sparse/shallow metadata and inert origin were checked. All 6,235 original physical object files were reported inode-distinct and byte-equal. A later preserved read-only observation confirms all those source object paths still present, none shared/mismatched, with 12 newly created objects (6,247 total).
- Four existing-path preimages match e4 and the R1 basis; the three additions were absent. The reviewed `a1a4242→b74` patch hash is `7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01`.
- **Actual `git apply --check` and `git apply` both exited 0 with empty stdout/stderr** on exact e4 in the new DB. `--stat` was not substituted for application checking. The local commit used normal arguments/process-local identity with no bypass flags.
- Result is exactly four modifications plus three additions. Full trees have 32,149→32,152 entries; unrelated mode/blob references are unchanged. All seven result mode/blob identities equal b74. The inherited missing blobs were not fetched, imported from R1's unverified worktree data, or validated merely by preserving their references.

| Result path | b74 / 481 common blob |
|---|---|
| `scripts/survey_weekly_mechanical_refresh_v2.py` | `41b289f8dc5f4340b9cf83669b30b8595ae65e15` |
| `scripts/survey_agent_control_v2.py` | `d11febc540f5611ed52e34168992efb81b58a44f` |
| `scripts/survey_reader_surface_gate_v2.py` | `89b5b859a316cd0633a009ca808049fceabea999` |
| `scripts/survey_weekly_derivation_v2.py` | `6d14009c43b762200179bce14354f809e06a5509` |
| `tests/test_survey_weekly_mechanical_refresh_v2.py` | `0c76bb0a2c92922f192bb2062c06197ce28df7fe` |
| `tests/test_survey_publication_revalidation_v2.py` | `6c468def9731f9eef4b6db4f1538cc19936e4e69` |
| `docs/weekly-mechanical-refresh.md` | `10d03d97f38ec31f18e87c0e54fe588261ef7c1d` |

All seven modes are `100644`. Source equality does not automatically transfer the earlier 97-method PASS; fresh checks were selected for the assembly boundary.

## Fresh verification and review

[Root verification task](../notes/rephase-1-r1-assembly/verification-task.md) / [milestone-2 report](../notes/rephase-1-r1-assembly/20260929T145048Z-verification/report.md) / [manifest](../notes/rephase-1-r1-assembly/20260929T145048Z-verification/manifest.json).

**Four selected methods passed once, 332.190 seconds, exit 0, no failures/errors/skips**: first/repeat refresh; healthy prior metadata revalidation followed by refresh; artifact-only/no-op refusal; unsupported pre-install control change. [Raw unittest result](../notes/rephase-1-r1-assembly/20260929T145048Z-verification/raw/four-tests.stderr) / [exit](../notes/rephase-1-r1-assembly/20260929T145048Z-verification/raw/four-tests.exit). These exercise assembled source in **fresh synthetic Git fixtures**; their individual histories are not e4 ancestry and their research/reviews/PDFs are not real publication evidence.

The separate [read-only source-history diagnostic](../notes/rephase-1-r1-assembly/20260929T145048Z-verification/raw/diagnostic.stdout) exercised the **actual assembled Git DB**:

1. Current eight-file closure passes `_verify_head_bytes` at exact 481dec0.
2. Historical closure built from actual local `git show e4:<path>` bytes passes historical verification at e4 (all eight blobs available).
3. Ordinary replay with that old e4 basis rejects specifically with `ValueError: Weekly receipt implementation or contract changed since renderer commit` — not a missing-object or import failure. The success sentinel is outside the exception handler. Diagnostic exit 0; raw output includes actual HEAD/tree/parent, source path/hash and all seven file hashes.

The fresh [independent assembly reviewer](../notes/rephase-1-r1-assembly/independent-assembly-review.md) rechecked actual objects/trees/isolation metadata and raw verification scope, and issued **BOUNDED_PASS for assembly/source-equivalence/fresh-checks only**, with no blocker. It neither authored the candidate nor ran tests or modified it. Root read the completed report and raw results; root also did not run tests. Together with exact code equivalence and the preceding bounded R1 implementation review, these support assembly completion. They are not a repeat full R1 audit or a whole-application verdict.

## Evidence qualifications

- Some original pre-copy/full-comparison stdout was tool-observed and summarized, not saved as raw files. Preserved script sources and the later explicitly labelled new observation do not recreate those missing outputs. The reviewer independently corroborated final identity/tree facts; it did not claim to repeat the original inode walk.
- The four-test raw stdout/stderr do **not** contain embedded HEAD/hash headers. Binding relies on the saved runner's expected-HEAD/tree/clean-index preconditions, recorded argv/cwd, execution record and the later diagnostic's actual source pins. The reviewer judged this sufficient for this narrow assembly; do not describe it as stronger per-test raw identity evidence. Future runs should save the wrapper output too; no rerun is selected solely to improve presentation.
- The diagnostic's before/after checks cover HEAD/tree/parent and tracked/index cleanliness. They are not a global snapshot of untracked files. The inspected diagnostic executes read-only Git/source checks, not edition State/Gate writes.
- An unnecessary `pip freeze` inventory attempt failed because pip is absent. Package versions were obtained with `importlib.metadata`; this setup observation is separate from successful test/diagnostic exits. No clean-all-setup claim.
- “Normal commit/no bypass” is supported; existence or execution of particular hooks was not independently demonstrated. Milestone-1 “hooks ran normally” language is qualified by milestone 2.
- R1's older four prohibited hook-bypass flags, fresh-root/unverified data and overwritten round3 logs remain historical limitations. This new assembly does not retroactively repair them. Its own packet uses new directories, and its seven-file application result is specific to **e4**, not clean application of the whole stack onto the production baseline.
- No broad 97-method rerun or automatic PASS transfer occurred. Inherited sparse/promisor/shallow limits remain; historical RELEASED editions were neither revalidated nor declared invalid. Whole candidate **NOT_READY**, step 4/B3 OPEN, canonical seven-point audit unstarted; net lifecycle saving remains unmeasured.

## Next bounded unit after this Commit Point

The initial [Profile/application dispositions](rephase-1-profile-application-assessment.md) identified **DM-001: the profile-aware Freeze helper uses the legacy post-approval visual-review type instead of the Candidate-bound pre-preview VISUAL record**. This is a justified canonical Freeze prerequisite, separate from R1. Its source is unchanged by this assembly.

On Human continuation, assign General a **small fixed-481dec0 DM-001 contract/callsite/test-oracle task before code**: compare `survey_profiled_freeze_v2.build_profiled_freeze` with lower-level `survey_publication_v2.build_freeze`, exact Candidate/Preview Approval/Profile/source/PDF/visual relationships and Special public-slug behavior. Return the minimum runtime/test paths and positive Weekly/Special + wrong/stale/conflicting authority negatives for Astra scope decision. Preserve existing Human approval, phase order and lower-level f1 conclusions; accurately labelled synthetic records may test type/identity, but not real visual quality. No production defect-record/main refresh or real Freeze/Release is authorized.

Do not repeat R1/assembly tests, repair all deferred items, or merge review authorities. Special/support semantics, build transfer/real PDF preflight, DM-003/004, optional findings transport, diagnostics/application readiness and independent canonical audit keep their separate dispositions. The next unit is **not started**. Reconstruct Commit/Push remains Human-owned; present this completed unit as a Commit Point and stop.
