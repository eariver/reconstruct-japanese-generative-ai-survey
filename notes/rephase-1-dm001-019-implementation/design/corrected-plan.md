# DM-001/019 corrected execution plan (selection-bound; no code/tests yet)

Parent `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3` / tree `65703243…` /
baseline `774dd39a…`; reconstruct `066436d…`. Original `design.md` unchanged;
this plan supersedes it where they conflict.

## Rejected initial provisions (do not implement)

1. Canonical `build_freeze(release_identity=…)` required-tag param — keep
   existing public signature; no caller tag/slug/Profile override.
2. `require_convergent_release_identity` — no issue/slug convergence gate.
3. Shape/placeholder Manifest preflight + delayed equality — full Manifest
   known pre-write; validate both complete schemas + conflicts first.
4. Canonical-serialization-on-retry — existing equal-payload files keep
   their bytes; hash actual existing bytes.
5. W1 "legacy-only Freeze succeeds", W2 "wrapper reaches PDF gap", W4
   "conflict at final validator" — corrected below (§4).
6. Retrospective-as-divergent-fallback — Thematic divergent positive is
   mandatory (§3).

## 1. Interfaces (Astra items 1–4)

- `publication.build_freeze(repo,cand,appr,frozen_at,freeze,manifest)`:
  signature unchanged. Internally: `validate_candidate` → read
  `candidate["quality_bundle"]` ref → `quality.validate_bundle` (validates
  Profile hash + `core.validate_profile`, pub-qual 232–250) → load named
  `production_profile` path/hash → `core.load_json` + repo-local check →
  derive slug via shared `public_issue_slug_from_profile` → tag via shared
  `profile_release_identity`. No scanning, no `publication→agent/profiled`
  import (agent:34 already imports publication).
- Shared in `survey_publication_v2.py`: slug pair, `prepare_freeze_inputs`
  (candidate + approval + exact approval-candidate path/hash + Candidate-bound
  pre-preview VISUAL via `reader.validate_review_record(VISUAL)` + source/PDF/
  page binds + bundle→Profile resolution), `build_freeze_payload`,
  `build_manifest_payload`, `preflight_freeze_pair`, `install_freeze_pair`.
  Private expected-Profile equality may narrow wrapper call only; never
  replaces resolved authority; no public dict/tag fast path.
- `profiled.public_issue_slug/release_identity`: thin delegating shims.
  `profiled.build_profiled_freeze` keeps real `_safe_state_profile`
  (`validate_agent_state`, RELEASE_CANDIDATE, approved Preview, current
  Profile SHA, bundle≡current-Profile) then delegates to shared
  prepare/payload/preflight/install. Other `_write_immutable` producers
  (Candidate/review/Release) untouched.

## 2. Preflight + writer (items 5–9; Freeze/Manifest only)

- Bytes first: `freeze_bytes = core.json_bytes(freeze_payload)` if target
  absent; if existing regular file parses equal, keep its bytes, hash actual
  bytes (`sha256_file`/read). Finalize full Manifest (incl. true
  `freeze_record_sha256`), schema-validate BOTH, conflict-check BOTH targets
  + BOTH parent chains (lexical/lstat pre-resolution: escape, same-target,
  target≡input incl. hardlink, nonregular/symlink target, symlinked/non-dir
  ancestor) before any write/mkdir. Manifest-without-Freeze fails closed
  (documented); equivalent-pair / equivalent-Freeze+missing-Manifest resume.
- Install: pair-specific `O_CREAT|O_EXCL` (`xb`/os.open) + revalidate type/
  path/content on race-refusal. Ownership = exclusively-opened fd identity
  (fstat ino/dev), never existence-before-call. Inputs/State/pre-existing
  files never overwritten/removed.
- Failure rule: completed valid Freeze retained for identical retry; remove
  incomplete file ONLY if this call created it (owned fd) AND residual bytes
  verify as known partial prefix of intended bytes; else leave + raise
  explicit failure (no rollback/no-write claim). Distinct tested outcomes:
  OSError pre-open / mid-write+flush / close / Manifest-install. Post-write
  `validate_release_manifest` is a recheck, not the first gate. No CAS,
  locks, crash-atomicity, fsync claims.

## 3. Fixtures — real validators, true Special State

- Revalidation `Fixture` is Weekly-only (hardcoded ISSUE/WEEKLY_MAGAZINE,
  ROLLING_WINDOW, checks). Do NOT stub `validate_agent_state` /
  `_safe_state_profile` and do NOT edit its file: new test module builds a
  parallel `SpecialFixture` reusing the same real calls
  (`reader.build_manuscript_manifest`, `quality.build_bundle`,
  `reader.build_review_record` SEMANTIC+VISUAL, `publication.build_candidate`,
  `stage.validate_stage`, `agent.build_stage_checkpoint/advance_with_
  checkpoint/approve_publication_preview`) with THEMATIC/LONGFORM_SPECIAL,
  `OPEN_HISTORY_AS_OF`, `surveys/special/{issue}` roots. Divergent variant
  sets `survey_root=surveys/special/2025-H2`-style with `issue_id=SP-2025-H2`
  BEFORE hashing downstream artifacts (never mutate bound Profile after).
  Weekly wrapper tests use issue-matching `survey_dirname`, not default
  `"survey"`. State files are real; negatives mutate real bytes (drift SHA,
  break lifecycle/gate, unlink approval) and assert real error provenance.

## 4. Pinned witnesses (pre-repair at b40 copies; post-repair fail-closed)

- W1 (corrected): canonical VISUAL lives at fixture `visual-review-v2.json`;
  (a) no legacy file → parent wrapper legacy load/type refusal (profiled
  79/87 path); (b) extra valid legacy at hardcoded path + valid canonical
  elsewhere → parent late exact-visual refusal (`validate_release_manifest`
  408–409) WITH residual Freeze/Manifest bytes recorded. Post-repair: both
  builders bind Candidate VISUAL only; legacy presence/absence irrelevant.
- W2 (corrected): C1≠C2 same issue/PDF, distinct path/hash; approval→C1,
  select C2. Wrapper may refuse earlier via State/checkpoint provenance —
  record actual provenance error, do not claim PDF-gap reach. Lower-level
  parent `build_freeze(C2,A1)` demonstrates PDF-only defect; post-repair both
  entrypoints raise approval-Candidate path+hash mismatch pre-write.
- W3 (mandatory): Thematic convergent (SP001→special/SP001) AND divergent
  (internal≠slug) wrapper+canonical equivalence: same `frozen_at`, same
  repo-relative refs → byte-identical Freeze+Manifest, `validate_release_
  manifest` + FROZEN admission pass. Retrospective pure-slug regression
  retained; full flow optional.
- W4 (corrected): conflict raises at `profiled:134`/`publication:382`
  `_write_immutable` ("refusing to overwrite divergent…"), not validator:135.
  Record exact error + before/after bytes (Freeze installed pre-fix = partial-
  write defect). Canonical-only copy may demo it. Post-repair: preflight
  refuses with NEITHER target touched.

## 5. Consumers + workflow predicate (item 14)

- Equivalence uses TWO independent snapshots (identical rel-paths, same
  `frozen_at`) or fixture-owned output reset — never wrapper-accepting
  canonical's existing pair. Real Weekly State→FROZEN admission mandatory
  (`validate_stage` + checkpoint + advance + `validate_agent_state==[]`);
  Special wrapper authority validated likewise.
- Release predicate: extract+execute the pinned `release.yml:59–103` Python
  block fail-closed from the b40 file in-test (import/subprocess of actual
  block), no hand-copy, no grep-only, no network/Actions/Release effects;
  pre-repair divergent bytes must trip `tag != expected_tag`.

## 6. Path scope (budget)

- Runtime (edit): `scripts/survey_publication_v2.py`,
  `scripts/survey_profiled_freeze_v2.py`. No schema/workflow/stage/config.
- Tests (new only): `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
  (L-/W-/S-/W1–W4 methods per design §7 as corrected above). Existing files
  read-only imports unless concrete fixture need is demonstrated to Astra.
- Regression after (run, not decorate): `test_survey_publication_v2`,
  `test_survey_profiled_freeze_v2`, `test_survey_freeze_stage_boundary_v2`.
  Implement/test in a NEW independent byte-copy of b40, pinned venv, inert
  origin, unique outputs. Stop for Astra diff/oracle review, then independent
  reviewer. No commit/push.
