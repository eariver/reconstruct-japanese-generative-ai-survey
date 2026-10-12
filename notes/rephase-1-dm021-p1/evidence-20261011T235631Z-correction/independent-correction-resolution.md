# DM021-P1 correction resolution — independent re-review (author-independent)

2026-10-12. Same independent reviewer as Phase-B `independent-implementation-
review.md` (which found only the frozen-partition bug and was therefore NARROW
— see §0). Read `notes/rephase-1-dm021-p1/astra-review-r1.md` (R1–R6, root found
much more than the prefix bug), correction packet
`notes/rephase-1-dm021-p1/evidence-20261011T235631Z-correction/` (report, source
pins, freezes, `run_correction.py`, `proof_apply.py`, `gen_correction_patch.py`,
run/proof logs, 3 failed attempts, `initial-preserve/`), and actual corrected
source in `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/
candidate-partial-b40de60` read-only (no candidate edits, no network, no
commits, no subagents, no broad rerun; no OWN-copy execution — all findings are
source/log-cited, no concrete ambiguity required a probe).

## 0. Correction of the earlier narrow review

The prior independent review (`evidence-20261011T201412Z-phaseB/
independent-implementation-review.md`, SHA `be39f196...`) correctly identified
the load-bearing `_frozen_member_kind` partition bug but MISSED every other
R1–R6 defect root later found: mutable-publication frozen misclassification,
incomplete graph (State/predecessor/transitive/bundle/later-review/Candidate),
retention misclassification, silent-repair binding, path-safety/token gaps,
CWD snapshot, late-recheck gaps, predecessor misattribution, oracle attribution
gaps, and reconstruction-only patch proof. Those misses are withdrawn; this
resolution verifies each R1–R6 item against actual corrected code, not against
the worker report alone.

## 1. Identity pins (actually observed, match report)

- Base: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status exactly 3M10A
  (`freeze-pre.json` == `freeze-post.json`, verified `diff` empty).
- M `reader-surface-gate-v2.schema.json` `fe4a96f4...` 6894B, M
  `reader-surface-semantic-review-v2.schema.json` `e8598239...` 4219B
  (P1 M, unchanged bytes from Phase B), M `survey_reader_surface_gate_v2.py`
  `e7305884...` 94511B — all `0o664`, LF2I-preserved.
- A `editorial-correction-proposal-v2.schema.json`
  `5623c0d92e3dfc5415e1ab73c73b3d5f1b147f265f2255469cede2ec333a4607` 3945B;
  A `survey_editorial_correction_proposal_v2.py`
  `9f3aea2567a39db5490daebc83aeca3a49346558a7170ab7244bb6bf6a82c6e2`
  82601B/1408 lines; A `test_survey_editorial_correction_proposal_v2.py`
  `a7b04dc13a096a265c1b2109995df5341518e500a88b221231f7b46b1d3c0ac9`
  87348B/1468 lines/9 methods; other 7 LF2I paths byte-stable
  (`4dadf873/7bae9d2a/c09c5558/d480e11d/4d235a38/ce687447/4a03b564`).
- Patch `complete-p1-correction-13path.patch` 550730B SHA256
  `147014b4307b8dd56860491c51c06502962692c100804086aa7277210e3f52d7`,
  13 `diff --git` (verified count; headers cover all 3M+10A).
  `run.exit=exit=0`, `proof-apply.exit=exit=0` (empty check stdout/stderr =
  clean apply, no warnings). `deps.txt`: Python 3.14.4 `optimize=0`,
  jsonschema 4.23.0, pypdf 6.16.2, git 2.53.0.
- `initial-preserve/` holds prior P1 bytes (`118d49e5/54b17f05/1b62b2d7`,
  semantic M `e8598239`) + prior patch `5f087f13`/474268B untouched. No old
  packet overwritten.

## 2. R1 — frozen/graph/retention: FIXED (verified in source)

- Frozen partition bug FIXED: `_frozen_member_kinds:482-515` uses
  `startswith("receipt:accepted:")/"receipt:authored:"/"upstream:"` + exact
  manuscript roles, gated by `_frozen_kind:475-479`; sorted scan; one entry per
  `(kind,path)` (`830-841`), preserving ALL union roles (not first-wins).
  `FROZEN_REF_PREFIXES:61-76` DROPS mutable `publication-semantic-input/
  publication-authored-input` (now `None` → COPY, `703-715`) and KEEPS
  `drafting-authored-archive/drafting-archive` + all accepted authority
  (`production-profile/issue-architecture/synthesis-*/draft-*/evidence-*/
  evidence-card/candidate-/selection/materiality-/discovery-/screening-/
  edition-views-/profile-completeness`). Mutable publication-authored correctly
  EXCLUDED from digest; State (`state:authority`), QA (`quality:*`), tools
  (`receipt:tool-closure`), outputs, reviews, Candidate, checkpoint/
  revalidation, `reader:before-input`, `receipt:record` all correctly EXCLUDED
  (no matching arm). Report claim §R1 accurate.
- Graph COMPLETE (vs prior omissions): live `state:authority` COPY node
  (`573-579`) + `STATE_CHECKPOINT`/`STATE_ACTIVE_RECORD` edges (`593,600`);
  full `supersedes` chain walk limit 32 with shape/cycle/issue/prior/chronology/
  depth checks (`601-638`); manuscript supports + approval summary/attention
  (`640-661`); Gate→receipt/reader/pre-TeX with binding equality
  (`663-693`); accepted/authored with dup + `UNCLASSIFIED_DEPENDENCY` (accepted
  must be frozen; authored publication-* allowed COPY, else frozen-gated,
  `695-717`); tool/outputs (`718-724`); quality results + profile/source/pdf
  nodes with `BUNDLE_SOURCE/PDF_DIVERGED` equality (`726-760`); later reviews
  as NODES with exact `LATER_REVIEW_DIVERGED` path+sha equality to effective
  manuscript/source/pdf (`762-786`, not edge-only); Candidate from validated
  `profile.paths.source_root` (`788-794`, not `parent.parent`) with all 6
  bindings + `CANDIDATE_INVALID` wrap + `CANDIDATE_DIVERGED` path+sha
  (`810-821`), COPY, unadopted. Mutable = ALL effective (later reviews
  INCLUDED, prior exclusion fixed) + outputs + receipt + reviewed-input +
  quality results + State + pre-TeX + candidate + publication-authored
  (`539-560`); tools/checkpoint/prior/frozen KEEP. Original shas stay metadata
  via checkpoint file, never live nodes. `HASH/POLICY` preserved. No generic
  resolver. PASS.
- Qualification: bundle-profile edge exists (`733-737`) but equality to the
  State-bound profile is a `pass` (`738-742`), unlike source/PDF which refuse
  on divergence. `quality.validate_bundle` already enforces profile-file drift
  + validity + issue binding (`survey_quality_v2.py:236-250`), and both files
  are pinned/retained, so no false accept arises in fixtures; still, a stale-
  but-valid same-issue profile would not trigger `BUNDLE_*_DIVERGED`. Minor
  inconsistency, not load-bearing for this component; recommend a
  `BUNDLE_PROFILE_DIVERGED` refusal for symmetry in a future touch (no rework
  required for this verdict).

## 3. R2 — binding/no-repair: FIXED

- Schema (`editorial-correction-proposal-v2.schema.json`, 112 lines):
  `basis.active_revalidation_ref` REQUIRED nullable (`30-46`); `proposed`
  requires `authoring_input_ref + proposed_reader_ref +
  proposed_reader_canonical_sha256` (`58-63`); retention drops singular `role`,
  keeps sorted `roles`, enforces `retained_ref XOR retained_dest` via
  `allOf/if/then` (`77-96`). Matches R2 ask. Pre-TeX M unchanged.
- `_pipeline:952-1121` derives `expected_proposal_dir` from VALIDATED
  `source_root + proposal_id`, requires authoring ALREADY at
  `<dir>/authoring-input.json` (`AUTHORING_NOT_STAGED`, P1 writes nothing),
  planned reader ref prospective (`planned_reader_rel` + canonical sha, file
  need not exist at prepare), preserves nonempty author `change_description`
  (optional `prepare_proposal(..., change_description)`, placeholder only when
  omitted), adds `_proposed_upstream_check` (proposed vs before
  accepted/archive/profile, `1135-1154`) after validated receipt.
- `validate_proposal:1262-1408` compares ALL: 7 top-level header keys,
  full `basis`, authoring PATH+sha, reader PATH+sha + canonical sha (+
  ref-sha==canonical-sha), exact retention; allows any nonempty description
  (equality by construction, `1366-1367`); requires exact canonical dir via
  resolved relative comparison (`1307-1314`, not final-2 names), `proposal.json`
  filename, all three `PROPOSAL_FILES` via `safe` (regular/alias/FIFO), exact
  staged bytes; returns SUPPLIED proposal UNCHANGED + separate `measured`
  binding (`1401-1408`, no inserted `proposed_reader_sha256`). Forged-header /
  wrong-PATH / wrong-digest / missing-nullable / wrong-dir / extra-omitted-
  conflicting retention oracles present (`test_proposal_binding_and_retention`,
  `test_refusal_and_scope_matrix`). PASS. Report §R2 accurate.

## 4. R3 — raw-first safety/canonical State/token: FIXED

- `_Collector:87-233`: root normalized once; `safe:126-179` does lexical
  `\`/`..` + leaf `is_symlink` (lstat, no follow) + ancestor symlink walk
  (`_check_ancestors:107-124`) BEFORE `resolve()`, post-resolve containment +
  `lstat` `S_ISREG` (FIFO/device/dir/symlink refused, never opened) + pinned
  bytes + stability; `reverify:191-233` rechecks ancestor alias + `S_ISREG` +
  bytes + HEAD + config (config routed through `safe:100-102,933-937`, loaded
  from pinned bytes — prior direct-read fixed). State/Profile/proposal/review
  loads use pinned bytes (no second-read switch). Canonical State enforced via
  `source_root/authoritative_filename` + `STATE_NOT_CANONICAL` (`944-950`,
  helper `1157-1162`); clone-State refused (tested `shadow-state`).
  `PROPOSAL_ID_RE:46` + `fullmatch:321-324` (trailing newline refused; schema
  `^...$` is ECMA-strict). Retention dests get raw ancestor checks even when
  absent (incl. dangling alias) + exact/ancestor-descendant namespace overlap
  vs live inputs + absent-required (`844-917`). Matrix covers
  traversal/alias/ancestor/FIFO/shadow/newline through PUBLIC APIs
  (`bad-id-newline/alias/traversal/ancestor-alias/fifo-sentinel/shadow-state`).
  PASS. Report §R3 accurate.
- Note: `_retention_plan:864-868` contains a dead no-op ancestor loop before
  the real relative-parts walk (`869-897`); harmless (real checks execute),
  recommend removal on next touch.

## 5. R4 — root-anchored snapshot + late rechecks: FIXED

- `_resolve_tree_base:236-264` + `_tree_map:267-318`: bases joined to `root`
  (never CWD), symlink dirs/files + FIFO/device refused (`TREE_ALIAS/
  TREE_NOT_REGULAR`), `.git` removed only after alias checks, never silently
  skipped. CWD-independence proven (`chdir("/tmp")` equality in
  `test_artifact_only_vs_control_drift_and_tree`). Pins precede consumption
  (State/Profile/checkpoint/effective/manuscript/Gate/receipt/archive/reader
  via `safe` before validator reuse; validators' re-reads are stability-
  checked). `validate_proposal` rechecks `reverify()` + full `_tree_map` AFTER
  scope (`1387-1390`; pipeline tree check no longer the last word) and
  re-derives `contract_identity` equality after scope (`1393-1399`); proposed-
  vs-before upstream equality enforced. Late mutation seams exercised
  (upstream/container/record/control/scope at late phases with injected-delta
  vs forbidden-write separation). PASS. Report §R4 accurate.

## 6. R5 — tests/R1 owner/no-write: FIXED (36 actual oracles)

- `Ran 36 tests ... OK` in 2736.162s = 9 P1 + 27 Gate (affected control only;
  no old-32 transfer; old 32 superseded). 9 P1:
  `longform_prose, weekly_envelope, honest_predecessor (RELABLED generic
  Core-change: docstring line 828, emitted-TeX-comment + manual QA + real
  generic adoption — explicitly NOT R1), refusal_matrix, ordinary_compat,
  proposal_binding_and_retention, artifact_only_vs_control_drift_and_tree,
  candidate_observed_and_stale, r1_mechanical_refresh_owner`. Names verified in
  `run.stderr.txt`.
- Real R1 owner (`test_r1_mechanical_refresh_owner:1354+`): TWO successive
  NON-EMITTED Python comment-only commits (no output change, asserted
  `surface == before_surface` AND `main.tex == before_main` for both),
  each followed by `survey_weekly_mechanical_refresh_v2.
  refresh_mechanical_evidence` executed in FIXTURE-committed code (sanitized
  subprocess, process identity, inert origin), asserting `VALIDATED` State,
  `publication_revalidation_provenance` set, second `supersedes` non-null
  (chain depth), `ORIGIN=ACTIVE`, then P1 prepare/validate via fixture code
  with no-write asserts. If R1 unconstructible the test fails with the gap
  (no fake pointer/reason/empty commit). Authentic, not a generic-label claim.
  PASS.
- Each-call no-write: `_snapshot` records regular hashes + symlink/dir/FIFO
  inventory (never opens FIFO) + HEAD/status; EVERY negative/scope/drift/
  candidate/binding case snapshots AFTER fault mutation, immediately before the
  P1 call, before cleanup (verified `*_no-write` labels throughout matrix/
  binding/drift/candidate/longform/weekly). Prior aggregate-only comparison
  fixed. PASS.
- Full-set oracles (not counts): frozen expected-SET includes profile/arch/
  approval/synthesis/draft-package+result/evidence-card/drafting-archive and
  EXCLUDES publication-authored (+ State/QA/tool/outputs by construction,
  `longform:700-716` +Weekly equivalents); retention ONE row per node, sorted
  unique roles, XOR `retained_ref/dest`, `retained_dest` under
  `retained/before/`; `REQUIRES_OWNER_DECISION` (`needs-owner`) + wrong-AFTER
  added; artifact-only commit ALLOWED vs control `closure`-dirty REFUSED
  (`RECEIPT_INVALID` wrap); Candidate proper (real `build_candidate` 6-field
  agreement, COPY) vs stale (`CANDIDATE_INVALID`) vs absent-allowed; forged-
  header/wrong-PATH/wrong-digest/missing-nullable/wrong-dir/extra-omitted-
  conflicting retention + `HASH/POLICY` + union-roles unit; ordinary compat
  preserved via real loader (no semantic acceptance). PASS. Report §R5
  accurate.
- Isolation: independent Git DBs, `UNTRACKED_SOURCES` pinned, process identity
  via `-c`, inert origins, no empty commits, sanitized `GIT_NO_LAZY_FETCH/
  OPTIONAL_LOCKS/ALLOW_PROTOCOL=file`, `setUp` refuses inherited `GIT_*`,
  no `fetch/clone`, no network. PASS.

## 7. R6 — runner/patch proof/packaging: FIXED

- Runner `run_correction.py`: deps → exact-13 freeze (hash/mode/bytes/status/
  HEAD409/tree8ce) pre AND finally-post → sanitized no-network Git +
  `optimize==0` refuse → unittest (2 modules only) → finally-post freeze,
  exclusive logs, timeout-partial preservation, `__pycache__` cleanup. Observed
  `pre head/tree` + `post ... files_same=True head_same=True status_same=True`
  path in code; `run.exit=exit=0`. PASS.
- Patch: `gen_correction_patch.py` uses `git add -N` + `git diff HEAD` for
  proper new-file headers (13/13). `proof_apply.py` byte-copies ACTIVE DB with
  `cp -a` to `/tmp/opencode/jgas-dm021p1-correction-verify-20261011T235631Z/`,
  verifies copy 3M10A + all13 bytes, reverts ONLY 13 overlays in the COPY
  (`checkout HEAD -- 3M` + `rm 10A`), verifies clean (`status=""`,
  HEAD409/tree8ce, `proof-freeze-clean.json`), `git apply --check` + `git
  apply` AS SAVED exit 0 (empty check out/err = clean), verifies applied
  files/modes/status == `freeze-pre` (`proof-freeze-applied.json`; independently
  re-verified here: files/status/head/tree all equal, 13 headers). Active
  source/archive untouched; no candidate commits/branches/network/protected-DB
  writes. This SUPERSEDES the prior reconstruction-only proof. PASS.
- Qualification (must not repeat): `gen_correction_patch.py` performs
  transient `git add -N` + `git reset HEAD -- NEW` in the ACTIVE worktree
  (index intent, no commit, worktree untouched; final status still `??`, not
  `A`, and freeze pre==post proves reset). The task instruction prefers
  `add -N` ONLY in an independent copy. No lasting mutation occurred, and the
  apply proof itself is in the disposable copy — but future patch generations
  must do the `add -N`/diff inside the copy, not active. Recorded as process
  qualification, not a correctness failure.
- Attempts preserved: `attempt-1-failed-unboundlocal/`,
  `attempt-2-failed-snapshot/`, `attempt-3-failed-1plus1/` + initial 32-packet
  untouched. PASS.

## 8. Residual qualifications (not blockers)

- (i) Bundle-profile equality is `pass`, not `BUNDLE_PROFILE_DIVERGED` (§2);
  validator-level drift/validity still enforced. Recommend symmetric refusal on
  next touch.
- (ii) Transient `add -N` in active during patch gen (§7); reverted, no
  lasting index change; do not repeat.
- (iii) Dead no-op loop `_retention_plan:864-868` + duplicated
  `REVIEW_DIGEST_UNBOUND` check (`686-689`); harmless, remove on next touch.
- (iv) `captured_sha`-style dead locals removed; scope `after_ref` shape guard
  (`1215-1217`) correctly fails closed on missing persisted ref.

## 9. Verdict: BOUNDED_PASS (correction, qualified)

All six R1–R6 groups are implemented in actual source and exercised by actual
36-method oracles with exact pins, read-only discipline (no roles/reason/
adoption/PASS/writes; `REVIEW_REQUIRED/REVIEW_BOUND_PROPOSAL` only), full
typed/transitive validation without pending/fake State, authentic dual R1
same-byte predecessors plus a relabeled generic Core-change predecessor, and
an actual `git apply` proof to an independent actual409 copy. Reported claims
in `implementation-report.md` verified line-by-line above; no report-truth
assumption. Prior narrow-review misses corrected (§0).

Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted; DM-021 remains OPEN
(P1 preparatory only, no live repair/adoption). No 43/31/32 transfer (old 32
superseded). Stop at Human Commit Point; ordinary reconstruct Commit/Push
remains Human-owned. No automatic next unit.
