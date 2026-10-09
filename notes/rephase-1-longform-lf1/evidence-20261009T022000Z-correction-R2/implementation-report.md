# LF-1 R2 correction implementation report (SAME 3 paths)

2026-10-09. New correction Co-Worker (not independent reviewer). Implements
`astra-implementation-review-r2.md` items 1–7 exactly. Uncommitted overlay on
fixed HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`, in
`/tmp/opencode/jgas-lf1-design-20261009T001653Z`. No candidate commit/branch, no
reconstruct/source/restore edits except this new packet
`notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/`. All
prior packets preserved untouched, including the overclaimed
`evidence-20261009T014500Z-correction-R1R6/run-corrected.sh` and its report.
Source original `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` unchanged at
409, clean. No LF-2, no network, no subagents. STOP for Astra and scoped
independent correction/evidence resolution. Whole candidate NOT_READY, step4/B3
OPEN, canonical audit unstarted. No shipping/committed-head PASS.

## 1. Final overlay (SAME 3 paths only)

- `scripts/survey_longform_derivation_v2.py`
  `233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7`
- `schemas/longform-reader-input-v2.schema.json`
  `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643`
- `tests/test_survey_longform_derivation_v2.py`
  `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913`
- `git status` is exactly the three `??` lines; `git diff --name-only HEAD` is
  empty. Patch `overlay.patch` + `overlay-sha256.txt/head/tree` in this packet.

## 2. Code corrections in this round

- **B1 schema dot:** `$defs/citation_key` pattern
  `^[A-Za-z][A-Za-z0-9:_-]*$` → `^[A-Za-z][A-Za-z0-9:._-]*$`, aligning schema
  with the runtime dot-preserving DID/key policy (`_bib_key` preserves dots,
  DID subset allows dots). New `test_dotted_did_full_loader_schema_positive`
  runs a dotted DID (`paper.v1-D001`) through the REAL chain → projector →
  `validate_longform_reader_input` schema positive (key `sp001paper.v1d001`).
- **Pre-read Evidence alias gap:** new `_preflight_evidence_tree` runs FIRST in
  `_longform_records`, before ANY accepted-tree content read. It `_safe`s the
  acceptance file, refuses a symlinked/missing run directory, refuses aliased
  `package.json`/`tasks`/`results` (symlink file/dir, symlinked ancestors,
  non-regular entries) and symlinked/non-file children — stat-only, no content
  reads. Exact-set authority remains the REAL `validate_evidence_acceptance`,
  still called after. New `test_results_dir_alias_refuses_before_read` swaps
  `results/` for an outside-malformed-sentinel alias and proves: alias refusal
  before parsing, observation spies showing the real validator was NEVER called
  and the sentinel was NEVER read and is byte-unchanged, immediate no-write
  inventory, healthy control after disclosed repair.

## 3. Test corrections in this round

- **Full category matrix:** table gains cover anchors, frontmatter
  heading/scope-note, narrative paragraph, timeline text, package synthesis
  paragraph, note title, cross paragraph/Qwen/DeepSeek/Kimi and two list-order
  rows (glance/comparison reversal) — 35 rows on ONE reused chain.
- **Derived-value pure probes** (`test_derived_value_pure_probes_from_loaded_context`,
  ONE chain + spy-captured ordered/records, explicitly labelled PURE throughout):
  accepted deck/headline→surface flow, headline-drift precise refusal, accepted
  `as_of`→`display_as_of`, accepted record title→bibliography, fixed style label
  via precise schema refusal, kicker grammar units. Pure evidence is never
  claimed as accepted-loader PASS.
- **Real-surface immutability** replaces the tautological constant-only
  deepcopy: a REAL returned surface is mutated, a second projection is proved
  byte-identical to the first with trusted constants/output unaffected.
- **Resolver controls:** equal-timestamp same-URL second capture keeps the
  projection (first-capture rule, `urldate 2026-08-22`) complementing the
  different-timestamp ambiguity refusal. Multi-DID-per-card-row is NOT
  constructible through real per-task-card producers, so no loader negative is
  fabricated for it; DID-uniqueness loader proof is the duplicate-card shape
  check plus this disambiguation pair (disclosed scope, not a claim).
- **Precise refusals:** `bad_syn2` now asserts the exact Synthesis-identity
  ValueError instead of a broad exception tuple.
- **HOLD classification (explicit):** pure mutated-HOLD
  (`test_held_back_cite_refuses_at_projection`) is PROJECTOR-level pure-build
  evidence, NOT a loader negative; `NEEDS_MORE` fixture BLOCKED is
  UPSTREAM-readiness evidence only, likewise not a loader negative. The prior
  packet report §91–94 calling the pure HOLD test "direct loader-level" is
  retracted below.

## 4. New Python runner (R1 strict, no bash print script)

`run_evidence.py`: exclusive `open(log,'x')`; ONE shared `guard()` comparing
pinned HEAD/tree/exact-status/zero-tracked/3-hashes PLUS inert-remote-only, no
`alternates`, no hardlinked objects — called BEFORE the child AND in a finally
AFTER it; postguard failure returns 3 even when the child exits 0 (child exit
reported alongside, never masked). Records interpreter path/version,
caller/child cwd, full argv, filtered env, inert remote, file-protocol child
env. Rejects inherited `GIT_*` (all six) and `PYTHONPATH`/`PYTHONHOME`
routing overrides. Proof-only `--expect-*`/`--dst`/`--proof-postdrift-file`
flags are argv-visible and disclosed; real runs use pins only.

Guard proofs (raw logs in this packet):

- `proof-wrong-head.log`: `--expect-head deadbeef…` → exit 2, REFUSE, ZERO
  `CHILD_SPAWN` lines (child never spawned).
- `proof-failing-child.log`: nonexistent test → exit 1, `CHILD_FAILED`,
  postguard PASS.
- `proof-postdrift.log` + `proof-postdrift-shell.log`: disposable independent
  byte-copy (HEAD/tree verified, inert origin, no alternates, ZERO shared
  object inodes with candidate), overlay satisfied preguard, fast pure test
  child exit 0, planted drift canary → `POSTGUARD_FAILED`, exit 3. Candidate
  status verified unchanged before/after; canary exists ONLY in the disposable
  copy. Disposable removed after proof.

## 5. Full-module verification (B2, final hashes, once)

`run-full-module.log`: `python3 run_evidence.py run-full-module.log --
tests.test_survey_longform_derivation_v2` → **31 tests, 2225.376s, OK**
(no failures/errors/skips; bare `OK` = zero skips), exit 0, pre/post guards
asserted PASS on module `233e8655…`, schema `7bae9d2a…`, test `ce68744…`, HEAD
`409b292…`, tree `8ce3699…`. All 31 methods proved on final identity: every
B2-listed contract area (directive file/symlink, lifecycle, no-write, path
escapes, order, Unknown fallback, ambiguity + equal-timestamp control, stable
nonreader, membership/cardinality negatives) plus the 5 new R2 tests. No old-hash
transfer is claimed; the 5-method provenance regression stays separately bounded
historical (not rerun, not claimed fresh).

## 6. Packaging (new independent copy)

`verify-apply.log`: FRESH byte-copy `/tmp/opencode/jgas-lf1-verify-20261009T023000Z`
of original 409 (`cp -a`, no reset of any prior copy): HEAD/tree verified,
clean status, inert origin, no alternates, zero shared object inodes, zero
hardlinked objects. `git apply --check` exit 0, `git apply` exit 0, post-apply
exactly three `??`, zero tracked mods, three SHA256 match final overlay. No
test repeat for packaging. Limits: partial-DB ancestry (inherited 26309 missing
blobs), pinned runtime not bundled; available-partial content only.

## 7. Retractions (without rewriting history)

- Prior `run-corrected.sh` guard claims are OVERSTATED and superseded:
  post HEAD/tree/status/hashes were PRINTED but never COMPARED, child-0 exited
  0 despite post drift, log creation was existence-test + truncate (not
  exclusive), and `cd` under `set +e` could fail without stopping the child.
  That script is preserved but MUST NOT be cited as an asserting guard; the
  Python runner above replaces it.
- Prior packet `implementation-report.md` §91–94 calling the pure mutated-HOLD
  test a "direct loader-level" negative is retracted: it is PROJECTOR-level.
- Original same-device inode observations remain bounded preparation evidence,
  now re-asserted per-run (no-hardlink/no-alternates checks inside `guard()`).

## 8. Qualifications

No LF-2/renderer/Gate/writer/CLI/contract/config changes; fixtures are
independent synthetic Git DBs with process-scoped identity; helper mocks/spies
are observation-only (validator-never-called, read-path recording, ordered
capture) and never replace successful authority validation. If any root
requirement conflicts with actual source, the exact issue is returned above; no
silent weakening. STOP for Astra; scoped independent correction/evidence
resolution required before closeout.
