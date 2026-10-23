# R4 return — central CODE corrector (4 confirmed bugs, DST only)

## 1. Bug1 export absolute-vs-relative (workflow)

Cause: `_selection_for_state` returns L `candidate_path` as absolute `Path`
(`resolve_publication_selection` returns `candidate_path: Path` absolute via
`resolve_raw_path`/`root.joinpath`). Workflow `_norm` is strict repo-relative
(rejects absolute/`..`/`\`). Both manual (`exp_rel=_norm(exp...)`) and PR branches
called `_norm` on absolute L path → `SystemExit: unsafe path (must be strict
repo-relative): '/tmp/.../publication-candidate-v2.json'` (lifecycle R3c
`verify_*_lifecycle.py:348` preserved). Raw caller absolute/traversal/alias still
must refuse; exact State-bound candidate, unknown branch failclosed, inert not
exported, ambiguous fail.

Fix (DST `.github/workflows/survey-production-v2-export-publication-preview.yml` only):
- Added `_rel_expected(exp)`: normalizes L-internal expected path relative to
  verified `root` (`relative_to`, escapes refuse), then `_norm`. `None`/empty/
  unknown shape refuses failclosed. Raw caller input still goes through strict
  `_norm` (absolute/traversal/alias refuse preserved).
- Added mode check in `_selection_for_state` (`CANONICAL|VERSIONED_ACTIVE` only,
  unknown branch failclosed, L errors propagate, no fallback).
- Replaced all 4 `exp_rel=_norm(exp...)` (manual VERSIONED_ACTIVE/CANONICAL, PR
  VERSIONED_ACTIVE/CANONICAL) with `_rel_expected(exp)`. Inert-set guards
  (`publication-set.json` alone refuses), ambiguous State (`len!=1` refuses),
  exact equality (State-bound vs requested/changed) preserved.

Test (actual extracted workflow code, both manual+PR shared helpers, not
'would refuse' helper assert): `test-r4-bug1-export.py` execs workflow block,
verifies `_norm` strict, `_rel_expected` absolute→relative, escape/unknown refuse,
caller absolute refuse, unknown mode failclosed. Exit 0.
Raw: `r4-bug1-stdout/stderr/exit.txt` (0).

## 2. Longform receipt AFTER RELEASED `state_sha256` drift

Cause: `validate_editorial_receipt` (high) calls
`longform.load_derivation_for_readback` (NEW authoring) → `_derive_authority_context`
→ `_longform_records` → `evidence.validate_evidence_acceptance` →
`validate_evidence_package_basis` checks `state_sha256` vs live State.
After activation + lifecycle (RELEASED), live State SHA differs from evidence
package basis (historical accepted-stage basis vs mutable live State).
Weekly passes post-RELEASED in single-root because its internal
`current_stage_basis_override` patches the same module instance; Longform fails
in harness bulk with two roots because `scripts` namespace accumulates
`[longform,weekly]`, `rt.evidence` (old weekly) ≠ `lf.evidence` (new longform),
so global patch misses longform's instance → `ValueError: Evidence package
basis drift: state_sha256` (`survey_evidence_v2.py:741` via `survey_longform_derivation_v2:442`
→ `survey_editorial_publication_v2:876`). Baseline LF readback vs new high call
both use same `_longform_records` path; difference is only module-identity split
in bulk harness, not contract. Single-root isolated both pass.

Fix (DST `scripts/survey_agent_tool_v2.py` only, justified runtime-tool scope):
- `current_stage_basis_override` now patches ALL loaded `survey_evidence_v2`,
  `survey_screening_v2`, `survey_production_v2` instances in `sys.modules`
  (suffix match + top-level), with same content-addressed historical wrapper
  (acceptance must bind exact `package_sha256`, only `state_sha256` floats to
  current; all other basis/contracts rerun). No ignore/pending boolean, no broad
  skip, no package SHA rewrite, no caller-wrapper assumption. Scope is exactly
  evidence/screening basis + State validator during context; restores all.
- Double-wrap guarded via `__historical_wrapped__`. Public receipt keeps strict
  State (via `verify_current_stage_basis`), unchanged accepted research (via
  rederivation + acceptance binding), current tools (closure/contract), and works
  later lifecycles. No fundamental contract change needed; correct layering is
  same checked historical basis, robust to instance split.
- Trace: baseline `load_derivation_for_readback` (direct) vs high
  `validate_editorial_receipt`→same loader both pass single-root; bulk harness
  split reproduced (weekly PASS, longform FAIL) then fixed by multi-instance patch.
  False worker terminal0 that captured failed readback remains PARTIAL (lifecycle
  itself healthy, receipt blocker preserved until this fix lands + combined freeze).

Test: `test-r4-bug2-runtime.py` verifies multi-instance patch + restore,
checked historical allow only when acceptance binds, tampered refuses, other drift
propagates (no broad skip). Exit 0. Raw: `r4-bug2-*`.

## 3. Orphan fork `max+1` → predecessor+1 + intent refuse

Cause: `_next_record_seq` used `max(existing)+1`. With State old r1 + complete
orphan r2 (same before-State/predecessor/set intent, set2), max=2 → next=3,
creates r3 superseding r1, forking over orphan (dynamic orphan fork,
`verify-faults-r3c-20261021T151500Z` source case). Ordinary activate only checked
`record_path_abs` lstat for next path (r3 doesn't exist → no collision), so fork
proceeds. No detection of exact existing intent elsewhere.

Fix (DST `scripts/survey_editorial_publication_v2.py` only):
- `_next_record_seq`: deterministic `predecessor_seq+1` from State pointer
  (`publication_revalidation_provenance`), not directory max. Null→0→1.
  Unknown branch (unparseable predecessor path) refuses. Legacy max inspected
  only for declaration (if `legacy_max>predecessor_seq`, records exist beyond
  pointer; next will collide if slot taken, forcing resume; never auto-advance
  to `max+1`). Compatible with strictly increasing + depth32; no latest-directory
  authority, no duplicate same-intent auto adoption, no foreign same-bytes adoption.
  Legacy writer (`survey_agent_control_v2.revalidate_publication_surface` max+1)
  unchanged (ordinary R1 before versioned continues, no silent legacy policy change).
- Added `_refuse_if_intent_exists(repo,record_base,exclude_rel)`: scans all
  `publication-surface-revalidation-rN.json` (lstat, no follow, exact naming),
  loads each, matches exact intent (`issue_id,supersedes,before_state_ref,set_ref,
  prior_checkpoint` + editorial kind/reason). Complete records only (incomplete/
  foreign same-bytes without exact refs never match). If same intent exists at
  different path, raises `INTENT_COLLISION` pre-write (ordinary activate refuses,
  explicit `resume_activation` of that exact record after full revalidation required).
- Called in `activate_publication` after `record_base` schema validation, before
  retained pin/first write. Existing `RECORD_COLLISION` (next path exists) preserved.
- Resume already does full revalidation (record+set+before-State+P2V+State drift);
  only exact complete orphan accepted, no latest authority, no auto adoption.

Root brief declaration: legacy max inspected, not used; predecessor+1 chosen as
deterministic, compatible with strictly increasing sequence semantics (gaps allowed
for orphan detection, next never skips). No foreign same-bytes adoption.

Test: `test-r4-bug3-orphan.py` temp repo verifies predecessor+1 (r1+orphan r2→next 2,
not 3), collision exists, intent r5 same→refuse, different intent allows, normal
(predecessor latest→next max+1) passes, unknown branch refuses. Exit 0.

## 4. fsync swallow + owned inode recheck

Cause: agent `_exclusive_create_record_bytes` and `_atomic_replace_state_bytes`
(`survey_agent_control_v2.py:1941,2008`) did `except OSError: pass` on `os.fsync`;
high `_exclusive_write_bytes` (`:399`) and disposable build temps (`:1278,1290`)
same. Silent durability failure, false CAS impression. High `activate_publication`
captured `record_owned_id` (fd dev/ino) but never rechecked before State write;
same-byte foreign swap (identical content, different inode) would be mistaken for
ours (stat-after-close claim).

Fix (DST agent + high, minimal shared-helper scope):
- Agent: both fsync swallows now `raise AgentControlError(... fsync failed; live
  bytes preserved ...)` (propagate/classify, no false CAS guarantee). Preserves
  owned partial (no delete on failure), live State preserved on temp fsync fail.
  Other `except OSError: return False/preserve` (identity/existence checks) untouched.
- High: `_exclusive_write_bytes` + build input/recipe temps same propagate as
  `EditorialError FSYNC_FAILED/PRESERVED_INCOMPLETE` (build root preserved, no rmtree).
- High activate: after P2V + State drift check, before `_atomic_replace_state_bytes`,
  rechecks `record_path_abs` still holds `record_owned_id` inode + `record_bytes`
  (lstat symlink refuse, `(st_dev,st_ino)` equality, `read_bytes` equality).
  Same-byte foreign swap refuses (`RECORD_OWNERSHIP/EXPLICIT_RECOVERY`, observed old,
  record preserved, never deletes referenced record). Preserves primary+secondary
  errors (P2V/State/record ownership chain), owned partial, unknown State.
- Affected legacy regressions: legacy writer paths unchanged except fsync classify;
  ordinary R1 before versioned continues (healthy control passes).

Test: `test-r4-bug4-fsync-owned.py` mocks `os.fsync` fault → all three writers
propagate + preserve; same-byte different-inode → `_record_identity_matches` False
+ recheck refuses; referenced never deleted; healthy create/replace passes. Exit 0.

## Run outcomes (focused, temp dirs, quota-checked)

- Quota at run: `/tmp` 7.5G/5.9G/1.7G 79% (no large fullscope, no storage touch).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/r4-pycache` in bash
  BEFORE python (no SRC pycache growth; DST `__pycache__` unchanged).
- Tests saved BEFORE execution under `correction-r4/` (no env false EOF masked exits,
  numeric exits via `echo $?`):
  - bug1 exit 0, bug2 exit 0, bug3 exit 0, bug4 exit 0 (raw `r4-bug*-stdout/stderr/exit.txt`).
- `py_compile` 3/3 OK for edited agent/high/runtime (external pycache).
- No tests in DST original or SOURCE snapshot; no clean/reset/raw delete/network/
  ordinary commits. OLD positives/faulted copies unchanged evidence; future testing
  new source epoch (R4 pins in `README.md`).

## Current pins (DST after R4, observed)

- export `c38423be...`, high `3f9d8e9e...`, agent `fb41bde6...`, runtime `fb25cf55...`,
  longform `c09c5558...` (unchanged), evidence `f7478d86...` (unchanged).
- Pre-edit archive + corrective identity note in `correction-r4/README.md`.
- Canonical7+active7 4-key retained (no relaxation).

## Essential blocker (not whole PASS)

Whole operation still in progress until corrected source + required runtime matrix,
independent review, packaging complete. Needs combined new SOURCE freeze (untouched
718 image, no tests inside) + fresh authority fixtures + full §9 positive/negative
matrix on public callers (both routes, second correction, R1×2 anchor, active vs
historical, ALREADY_ACTIVE/resume, close/postread faults) + root review. No Human
Commit Point claimed here; ordinary Commit/Push Human-owned. No new regression
attributed preexisting (all 4 are new R4 fixes, prior R3c failures preserved).
