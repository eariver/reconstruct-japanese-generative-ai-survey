# DM-001 contract/callsite/test-oracle analysis — BLOCKED (fixed-481 fixture missing)

- Role: **General Co-Worker**, fixed-481 DM-001 contract/callsite/test-oracle analysis ONLY. No implementation, no tests.
- Recorded: **2026-10-03T12:51:48+09:00** (local clock; `2026-10-03T035148Z`).
- Scope bound: compare `scripts/survey_profiled_freeze_v2.py build_profiled_freeze` vs `scripts/survey_publication_v2.py build_freeze` and actual named callers/validators at fixed candidate only; inventory Candidate-bound pre-preview VISUAL, Preview Approval, Profile/source/PDF, canonical Human gate relations, Special public slug; distinguish DM-003; identify minimum runtime/test paths and canonical caller chain; propose Weekly/Special positives + wrong/stale/conflicting negatives + parent-defect oracle + no-write assertions without executing tests.
- Entry read (no reload of whole history):
  - `AGENTS.md` (role contract, fixed baseline `774dd39a...`, fixed B/A/e4/R1/481 identities, Commit Point rule)
  - `outputs/rephase-1-r1-assembly-assessment.md:7-21,70-72` (fixed assembled candidate table; DM-001 next-unit definition)
  - `outputs/rephase-1-profile-application-assessment.md:26` (DM-001 disposition row) and `:32-42` (historical CLI unit, not to redispatch)
  - `handoff/rephase-1-continuation.md:2,9,17` (next is DM-001 minimal contract at fixed 481; do not repeat R1/assembly/witness)
  - `outputs/rephase-1-implementation-plan.md:3-5,17-24` (current continuation pointer; baseline/f1/B3 context)
  - `notes/rephase-1-r1-assembly/README.md:10-14` (fixed 481 identity/fixture/branch)
  - `notes/rephase-1-profile-application/analysis.md:87-92` (prior DM-001 source-grounded comparison at B — secondary only, see §4)
  - `notes/rephase-1-session-transition/deferred-intake.md:19` (DM-001 disposition — secondary only)

## 1. Fixed-candidate identity verification — FAILED (fixture absent)

Expected (from `outputs/rephase-1-r1-assembly-assessment.md:10-16` and `notes/rephase-1-r1-assembly/README.md:10`):

| Field | Expected |
|---|---|
| HEAD | `481dec0c0233d7871df79a07a88aa5fe2291daa3` |
| Tree | `657032438c6ed8b1c055d5a120b67b4b261a5092` |
| Direct parent | `e4c82692abee6acedbba07815b0d74ccefb80a7e` |
| Branch | `codex/rephase-1-r1-assembly` |
| Fixture | `/tmp/jgas-rephase-r1-assembly-20260929T143833Z` |
| Origin | `https://example.invalid/rephase-increment-b.git` (inert) |

Method (read-only; no checkout/write/hydration/refs/object mutation):

- Env `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0` on every git invocation.
- No `checkout`, `apply`, `fetch`, `clone`, `gc`, `commit`, `update-ref`, `symbolic-ref`, `worktree`, hydration, alternates/object-sharing changes. No restore attempted.
- Commands run:
  - `ls -ld /tmp/jgas-rephase-r1-assembly-20260929T143833Z`
  - `git -C <fixture> rev-parse HEAD`, `rev-parse HEAD^{tree}`, `log --oneline -2 --decorate`, `status --porcelain --untracked-files=no`, `diff --name-only`, `diff --cached --name-only`, `branch --show-current`, `remote -v`, `rev-parse HEAD^`
  - `ls -1 /tmp/`; `ls /tmp/jgas*`; `ls -d /tmp/*rephase* /tmp/*jgas*`
  - Reconstruct context only: `git rev-parse HEAD`, `git log --oneline -5`, `git status --porcelain --untracked-files=no`, `git log --all --oneline --grep="481dec0"`, `git cat-file -t 481dec0...`

Raw evidence:

- `ls -ld /tmp/jgas-rephase-r1-assembly-20260929T143833Z` → `ls: cannot access '/tmp/jgas-rephase-r1-assembly-20260929T143833Z': No such file or directory`
- Every `git -C /tmp/jgas-rephase-r1-assembly-20260929T143833Z ...` → `fatal: cannot change to '/tmp/jgas-rephase-r1-assembly-20260929T143833Z': そのようなファイルやディレクトリはありません`
- `ls -1 /tmp/` (2026-10-03) contains only `opencode`, `snap-private-tmp`, `systemd-private-*`, `unleash-repo-schema-v1-codeium-language-server.json` — **no `/tmp/jgas*`, no `/tmp/*rephase*`**.
- `ls /tmp/jgas*` → `No such file or directory`. Same for `/tmp/*rephase*`, `/tmp/*jgas*`.
- Reconstruct `git log --all --oneline --grep="481dec0"` → empty (no output). `git cat-file -t 481dec0c0233d7871df79a07a88aa5fe2291daa3` → `fatal: git cat-file: could not get object info` (expected: 481 lives in the independent assembly DB, never in reconstruct's DB; no object sharing by design).
- Reconstruct HEAD at inspection time: `a6d834be7da6828740bcddd9b63477064015de80` (local `git rev-parse HEAD`); recent log `a6d834b / a22d693 / d175600 / d665af8 / 35a5b20`. Tracked `status --porcelain --untracked-files=no` → empty (clean tracked/index as observed; not a global untracked snapshot and not candidate verification).

Result:

- **Actual HEAD/tree/parent/clean-tracked/index at fixed 481: UNVERIFIED — fixture directory absent.** Per task instruction, **stopped here; no restore, no substitute fixture, no hydration, no ref/object mutation.**
- Consequence: the seven-path mode/blob equivalence (`outputs/rephase-1-r1-assembly-assessment.md:32-42`), the four-test binding, and the actual-DB diagnostic could not be re-pinned by this unit. This unit adds no new identity evidence for 481 and does not challenge the preserved assembly packet; it only records that the live `/tmp` DB is gone.

## 2. Source comparison — NOT PERFORMED (blocked)

None of the following was inspected at fixed 481 because the fixture is missing and no substitute source was used:

- `scripts/survey_profiled_freeze_v2.py` (`build_profiled_freeze`) vs `scripts/survey_publication_v2.py` (`build_freeze`): no fixed-481 bytes read, no line ranges established, no caller/validator chain walked.
- Actual named callers/validators (expected set from prior inventory, not re-verified): stage validator, agent control, reader-publication validator, quality bundle, Weekly publisher/derivation, Special renderer/wrapper, workflows — **not traced at 481**.
- Candidate-bound pre-preview VISUAL vs legacy post-approval visual type; Preview Approval; Profile/source/PDF relations; canonical Human gate relations; Special public slug — **not inventoried at 481**.
- Helper status question ("dead/type-mismatch only vs other authority/forwarding/no-write gaps prerequisite") — **no fixed-481 answer**.
- DM-003 generic provenance distinction; minimum runtime/test paths; canonical caller chain — **no fixed-481 answer**.
- Positive Weekly/Special matrix (which profiles actually supported), wrong/stale/conflicting authority negatives, parent-defect oracle, no-write assertions, affected tests — **not produced for 481**.
- Existing test fixture validity / needed modifications — **not evaluated; zero tests executed** (as instructed).

No code/test writes were made. No production main, Issues, defect records, or authorized Summary refresh was touched (another Worker handles the single authorized Summary). No reconstruct or production commits. No agents spawned.

## 3. What was deliberately NOT substituted

- Reconstruct worktree bytes at `a6d834b` were **not** used as a stand-in for fixed-481 source. Changed head invalidates automatic transfer (AGENTS.md candidate discipline).
- Preserved e4/B/R1 databases were not probed for recovery because none are present in `/tmp`, and any recovery is a Human-authorized fixture procedure, not a Co-Worker restore.
- Saved assembly packet blobs/manifests (`notes/rephase-1-r1-assembly/`) were not re-hydrated into a new DB or treated as live source.

## 4. Secondary pointers only (not fixed-481 verification)

For Root convenience — **do not treat as 481 evidence**:

- Prior source-grounded DM-001 comparison at B: `notes/rephase-1-profile-application/analysis.md:87-92` — profiled helper binds fixed `publication/v2/visual-review-v2.json` (`survey_profiled_freeze_v2.py:79`) then `publication.validate_visual_review` against legacy post-approval `visual-review-record-v2` (`survey_publication_v2.py:24,319-327`, docstring `:291-295`); canonical lower-level `build_freeze` (`survey_publication_v2.py:330-383`) reads `candidate["visual_review"]` via `reader.validate_review_record(..., VISUAL)` (`survey_reader_publication_v2.py:26,544+`); RELEASE_CANDIDATE stage uses candidate-bound pre-preview visual (`survey_stage_validation_v2.py:583-585`). Type mismatch judged real in fixed B source at that time; f1 exercised only lower-level path; synthetic schema-valid records deemed sufficient for type/identity equivalence, real visual/PDF judgment kept as separate acceptance gap.
- Dispositions: `outputs/rephase-1-profile-application-assessment.md:26`; `notes/rephase-1-session-transition/deferred-intake.md:19` (DM-001 separate application-path prerequisite, not B1/B3 scope); `outputs/rephase-1-r1-assembly-assessment.md:70-72` (next-unit task definition: compare helpers, exact Candidate/Preview Approval/Profile/visual relations, Special public slug, minimum path/positive-negative proposal).
- These line refs are **B-era or planning text**. Whether they still hold byte-for-byte at 481 is exactly what the blocked fixed-481 inspection was meant to establish.

## 5. Minimum implementation proposal — NONE VALIDATED

No runtime/test-path proposal can be positively grounded without fixed-481 bytes. Conditional next step only (for Root/Human decision, not started):

1. Human authorizes and performs fixture recovery (independent byte-copy DB / preserved backup procedure per `notes/rephase-1-session-transition/restart-context.md` and `notes/rephase-1-r1-assembly/session-closeout.md` §7 context-persistence note: saved files vs Human commits vs `/tmp` DB durability are distinct; missing raw logs are not to be recreated from summaries). Co-Worker must not self-restore.
2. Re-run this exact DM-001 contract/callsite task at pinned `481dec0` (HEAD/tree/parent/clean-tracked/index re-verified read-only first), then only: `build_profiled_freeze` vs `build_freeze` diff, named caller/validator inventory, VISUAL/approval/Profile/source/PDF/Human-gate/Special-slug map, DM-003 separation, minimum runtime/test paths + caller chain, positive/negative/no-write oracle table, existing-fixture validity assessment without executing tests.
3. Root selects unit and architecture after receiving that analysis plus the updated Summary (per task close).

No Weekly/Special profile support claim, no negative-oracle list, and no test-modification list is offered in this blocked unit.

## 6. Unresolved questions for Root

1. Fixture recovery authority: is there a Human-held complete Git DB backup for `/tmp/jgas-rephase-r1-assembly-20260929T143833Z` (independent DB, inert origin, no hardlinks/alternates), or must the assembly be re-derived from preserved e4 + reviewed R1 patch via the recorded procedure? Co-Worker attempted no recovery.
2. Reconstruct HEAD moved `a22d693` (assembly-assessment basis) → `a6d834b` (observed now). Does Root need a delta check that no entry/handoff/gitattributes or candidate bytes were altered before re-dispatching the DM-001 task?
3. Are the other preserved `/tmp` DBs (e4 gate-CLI, B, R1 mechanical, witness supp) also accepted as lost, or are they held elsewhere? Current `/tmp` shows none.
4. On continuation, should the DM-001 task remain strictly read-only analysis (no test execution) at fixed 481, or be expanded to include intended-parent defect witnesses? Current instruction was analysis-only; no witnesses were run.
5. Seven-point audit and step 4/B3 remain OPEN per assembly assessment; whole candidate NOT_READY — confirmed unchanged by this blocked unit. No new PASS, no transfer, no adoption inference.

## 7. Evidence and limits summary

- This report is the **only** new artifact of this unit: `notes/rephase-1-dm001-contract/report.md` (new directory; no entry/handoff/gitattributes edits; no code/test writes; no tests; no commits).
- Candidate identity/limits: expected 481 identity table in §1; actual live verification **absent**; limits are the missing DB, non-global untracked-file observation scope, and no per-test raw binding (inherited from assembly qualifications, not re-verified).
- Attribution: General Co-Worker analysis only (Muse Spark 1.3 per Human report; serving model unexposed). Not Astra review, not independent audit, not Human authority. Worker result is not approval.
- Commit Point: per Human boundary, stop here and present this blocked point; do not auto-start implementation or fixture recovery.
