# Independent review — W34 Evidence scaling assessment (planning only, no code/runtime)

Reviewer: fresh independent reviewer, NOT the assessment author, NOT a codewriter.
Scope: `evidence-scaling-assessment.md` + execution logs 35–42 + packet `README.md` + final138
proof-copy source, read-only. No runtime/tests/import/fixtures/network/Git readback/source
edits/subagents. This review decides the next coherent unit; it is not implementation,
not a design PASS, not a runtime audit, not adoption approval.

Method note: log/pin citations below were re-read directly (log stdout/stderr/exit/killed-notes;
proof-copy `scripts/survey_evidence_v2.py`, `scripts/run_evidence_v2_interactive.py`,
`scripts/survey_research_authority_v2.py`, `scripts/survey_completeness_v2.py`). Line numbers
refer to the proof-copy final138 source.

## 1. Facts accepted (verified from logs + source)

- W34 `run()` (log38, `w34-evidence-run-38.py`): PRE-only stdout 8 lines, stderr 0, exit **143
  SIGTERM** after ~14 min hang (start 16:51:32Z, PID 3048844). No `evidence/v2`, no State advance
  (log42: `evidence/v2 exists=False`, lifecycle still `CANDIDATES_NORMALIZED`). A failed/partial
  run is a material performance blocker, not a semantic failure. Accepted.
- `rchar 228011353736B (228GB)` is a **LOGICAL byte count (page-cache re-reads), not
  physical-disk proof**. The author's explicit `rchar ≠ disk` discipline is correct and must be
  retained; no disk-cost claim follows. Full unmodified completion time is UNKNOWN; no linear
  extrapolation to wall-clock is legitimate (page-cache warmth, card/validation CPU beyond
  `task_source_ids`, Views/ledger/completeness phases, timeout/OOM all unmeasured).
- No claim of deadlock/infinite hang is made; no blanket no-outputs claim beyond the observed
  scope. Correct.
- Scale parameters confirmed: 409 tasks (352 PARTIAL/49 VERIFIED/8 NEEDS_MORE historical),
  428 supplement rows → 425 distinct Raws, 189286753B distinct (log36: 457 GETs, 426 DATA incl
  manifest); supplement `ce6f977a…`/389414B, basis E439 `0a23be47…` + screening FILE `b9d963d8…`.
- Package building itself is cheap (log40: supplement validate WITH override 2.8s, prepare 5.6s,
  first-5 `task_authority_sources` 4.0s); the full-409 `task_source_ids` loop was killed after
  1:34 with 17GB logical in 1 min (~283MB/s linear, 99.9% CPU, exit 143, log41). The blowup is
  isolated to per-task revalidation, not package building. Accepted.
- Direct `validate_evidence_authority_supplement` without preloads refuses with `Screening package
  basis drift: state_sha256` (log39/stderr) — State-basis binding is enforced, not bypassable by
  caller context. Accepted; this is the exact property any repair must preserve.
- Existing efficient shortcut confirmed: `_supplement_entries_for_package(..., screening_acceptance,
  discoveries)` skips re-resolution when both are provided (survey_evidence_v2.py 298–309); used
  by `prepare_evidence_package` (623–635), `validate_evidence_package_basis` (991–997), renewal
  content (944–947). `task_authority_sources(repo_root, task, package)` (451–455) has **no such
  optional args** and passes none at 470. No existing public path avoids the repeat; no cache,
  no `lru_cache`, no caller-verified-dict shortcut. Accepted.
- Precedent for the repair shape exists in-tree: `_check_evidence_tasks_content` (823–890) takes
  an already-validated `supplement_entries` dict and does pure per-task binding checks over it
  (no per-task Raw revalidation). Validate-once + pure-slices is therefore consistent with existing
  architecture, not an invented pattern. Accepted as concept support.
- Existing-test pins verified present: `tests/test_survey_evidence_v2.py:716` and
  `tests/test_profile_support_upstream_repair_v2.py:615` both call public `task_authority_sources`
  directly — public standalone behavior must stay unchanged or these tests must be re-bound
  explicitly. (Minor, non-load-bearing: the author's `supplement-bound-exactly-once 873–885` pin
  does not match the read content at those lines, which are `_build_completeness` tail /
  `_archive_input` head. No conclusion depends on it.)

## 2. Load-bearing correction 1 — the repeat count is understated ~3x, and §2's "package-linear downstream" claim is false as written

The assessment (§2, lines 31–32) states downstream `accept_edition_views` / `build_materiality_ledger`
/ `validate_profile_completeness` (via `survey_completeness_v2`) "do **not** call
`task_authority_sources`; they revalidate screening/evidence/views/ledger/completeness bindings
(hashes + coverage), package-linear, not per-task Raw loops." **This is incorrect as a blanket
statement.** Verified transitive chain in proof-copy source:

- `validate_evidence_card(..., repo_root=...)` calls `task_authority_sources(repo_root, task,
  package)` at line 1070 → full `_supplement_entries_for_package` (470) = 425-Raw revalidation
  **per task**.
- `_check_evidence_acceptance_results_content` (1279–1315) calls `validate_evidence_card(...,
  repo_root=repo_root)` **per task** (1304–1310).
- `validate_evidence_acceptance` (1475–1497) calls the above (1496) — so every caller re-sweeps
  all tasks' Raws.
- `accept_edition_views` (1892–1956) calls `validate_evidence_acceptance` (1901) → per-task sweep;
  idempotent re-read path calls `validate_edition_views_acceptance` (1928) → same (1967).
- `build_materiality_ledger` (1983–2059) calls `validate_evidence_acceptance` (1996, sweep N),
  `validate_edition_views_acceptance` (1997 → 1967 → sweep N+1), then `validate_materiality_ledger`
  (2055 → 2186/2189/2190 → **two more** per-task sweeps).
- `validate_completeness` (2348–2370) calls `validate_materiality_ledger` (2363) → three more
  per-task sweeps; `run()` invokes it via `validate_profile_completeness` (run 889 →
  survey_completeness_v2.py 276–286).
- The same shape exists in the renewal content core: `_validate_evidence_acceptance_content`
  (1318–1346) calls `_check_evidence_acceptance_results_content` (1345) → per-task Raw loops.

Counting `run()` (678–918) end to end, one unmodified attempt performs on the order of **10–14
full per-task supplement sweeps** (~409 × 425 ≈ 174k file reads ≈ ~77GB logical each, order
~1TB logical total plus card CPU) — not "~4×409". Enumerated: `task_source_ids` dict (769),
`_build_card` loop (790 → runner 375 → 470), inline card-validate loop (791 → 1070 → 470),
`accept_evidence_results` per-task loop (1230 → 1070 → 470), `validate_evidence_acceptance` at
run 810 (→ 1496 → per-task), `accept_edition_views` (836 → 1901 → per-task),
`validate_edition_views_acceptance` (844 → 1967 → per-task), `build_materiality_ledger`
(859 → 1996/1997/2055 → four per-task sweeps), `validate_profile_completeness` (889 → 2363 →
three more). Only the pure row/binding sub-checks (`_check_views_acceptance_rows_content`,
`_check_ledger_rows_content`, `_check_completeness_result_content`) are package-linear; every
acceptance wrapper re-sweeps per task.

Consequences:

1. The author's alternative-(A) verdict ("possible but unbounded") holds **more strongly**, not
   less. Observed 228GB at kill is consistent with dying in phase 1–2 of a ~10+ sweep run. This
   is still not a wall-clock forecast — it only raises the lower-bound reasoning.
2. The author's §4/§7 repair scope ("`run()`'s three per-task loops + accept boundary") is
   **necessary but not sufficient to be worthwhile**: fixing only the three `run()` loops while
   leaving the accept/Views/ledger/completeness chain untouched saves roughly 3 of ~10+ sweeps.
   The minimum coherent unit MUST include the per-task `validate_evidence_card(repo_root)` call
   sites inside `accept_evidence_results` (1230), `_check_evidence_acceptance_results_content`
   (1304), and the `validate_evidence_acceptance` wrappers (1901, 1967, 1996, 2189) — i.e. the
   whole transitive accept/validate chain — or the repair does not move total work materially.
3. No speculative generic tool-cache follows from this correction: the fix stays a private
   per-operation validated context + pure task slices, at more call sites than listed. No
   automatic LOW-performance generalization (see §4).

## 3. Load-bearing correction 2 — the threading mechanism is unsettled; concept viable, detail not implementation-ready

The assessment (§4) requires operation-scoped `entries` "passed privately within `run`, not via
public signature." **No such Python mechanism exists without one of:**

- (a) module-global / dynamic-scope handoff — cache-like; must then prove no cross-operation
  reuse, no readback poisoning, exception-safe discard;
- (b) backward-compatible private kwarg (e.g. `_supplement_entries=None`) threaded through the
  public accept/validate functions — signature-visible, operator-callable, so the fail-closed rule
  for operator-supplied values must be specified (refuse? ignore? use is the authority escape);
- (c) private parallel accept-chain functions duplicating the public bodies — mirror bloat.

Related: a card-builder mirror **already exists** — runner `_build_card` (run 367ff) mirrors
`survey_evidence_v2.build_research_card_content` (1710ff) nearly line-for-line, with the split
documented at 1557–1570 ("the interactive runner (B-owned) keeps its own copies ... LOW never
imports it"). The proposed `_build_card_with_entries` / `_validate_card_with_entries` mirrors
risk adding a **third** copy. The repair must factor **ONE canonical body** shared by
public/batch paths (e.g. the dict-taking core used by both, with the existing public functions
as thin reload-then-delegate wrappers), not copy-paste validators.

Additional unsettled callers that must be dispositioned explicitly (in or out, with
behavior-preservation rules), because they call the same per-task-with-`repo_root` paths:

- LOW revision paths: `build_revision_cards_views_from_paths` (LOW 2345 → `build_research_card_content`
  → 1726 full revalidation per task; 2348 → `validate_evidence_card(repo_root)` per task) and
  `accept_revision_evidence_views_from_paths` (2459, per-task `validate_evidence_card` with
  `repo_root`). Same quadratic shape at 409 scale if ever used there; author lists as
  "dependency-noted, out of scope unless Root includes" — agree, but the exclusion must be
  explicit and the shared-helper factorization (if any) must keep LOW's `ds_context` root/effective
  + `before_copy_path` binding and the 1557–1570 no-runner-import closure intact.
- Renewal/history readbacks: `_validate_evidence_acceptance_content` (1345 → per-task loops);
  plus the ~10 other `validate_evidence_acceptance` callers (architecture base 113/299,
  longform/weekly derivation, drafting base 339/428, handlers 293, stage validation 501,
  prearchitecture acceptance 711, research authority 946/3123, renewal source 1196). These are
  NOT on the W34 hot path; their behavior (full revalidation) must not change silently as a side
  effect of touching shared internals.

Verdict on readiness: the assessment establishes a **viable technical selected concept**
(validate-once per operation + pure per-task slices + package-linear final re-hash; precedent at
823–890), but **not implementation-ready detail**. Do not fabricate a design PASS: private context
scope, threading mechanism, and the widened caller closure are unsettled.

## 4. Requirements the repair unit must meet (in addition to assessment §4)

1. **Final-boundary Raw re-hash, package-linear per canonical write.** After the repair, the last
   Raw-byte touch before a write moves from "last per-task card check" to an earlier package-linear
   point, widening the TOCTOU window. Each canonical write boundary (Evidence accept, Views accept,
   ledger, completeness, archive/audit) must re-hash manifest path+SHA, package path+SHA, task
   bytes, State/Profile paths+SHAs (and screening/Evidence/Views acceptances where bound) **plus a
   package-linear full Raw re-hash** immediately before the write under the same
   `implementation_sha`. The `entries` dict is a read optimisation, never a write authority.
   Raw bytes, not just manifest file hash, at the final pin recheck.
2. **Read-only validators keep full freshness before RETURN, not only writers.** Any
   `validate_*` called outside the owning `run()`/`accept_*()` invocation reloads fully as today.
   No operator-passable parameter on any public function may become authority. Note
   `validate_interactive_input` already accepts caller-supplied `task_source_ids` (run 318,
   341–352) for binding-**subset checks only** — the repair must not promote that input (or any
   like it) into validation authority. Input context is derived inside the path-checked owner only.
3. **Partial-fault window honesty.** Fault injected *before the first* canonical write → expect
   zero canonical writes. Fault injected *after an earlier accepted output* (e.g. Evidence accepted,
   Views fails) → expect the earlier outputs present, later ones absent, fail-closed thereafter.
   The assessment's oracle §6.3 ("no canonical writes") is valid only for the pre-first-write case;
   forbid any "all-canonical no-writes for late fault after earlier accepted output" test claim.
4. **No invented atomicity / no interleaving-exhaustion claims.** The repair reduces redundant reads;
   it does not add snapshot isolation. Tests must not claim identical refusal for every concurrent-
   modification interleaving. Distinguish snapshot-input semantics (only if the repair actually
   snapshots manifest bytes at entry — it does not today) from the existing repeated-observation
   semantics actually preserved.
5. **Preserved guarantees, explicitly:** public `task_authority_sources` / `_build_card` /
   `validate_evidence_card(..., repo_root)` standalone behavior unchanged (standalone reload
   fully — existing tests at 716/615 keep passing unchanged); signatures/standalone IO and
   current-vs-history semantics unchanged; LOW/history existing guarantees remain (no automatic LOW
   generalization unless the shared-helper factorization demands caller compatibility, then
   explicitly scoped); no SourceClass/semantic-policy downgrade (pure slicing preserves classes);
   no new module/schema/family/API flag/cache framework; no authority-cache escape; no
   operator-verified-dict.
6. **Epoch handling agreed:** a repaired source is a new epoch (`repository_commit_sha` changes);
   existing rehearsal State bound to the old impl must not be silently rebased. Assessment §5
   Option I (fresh isolated lineage from init with already-captured DATA; prefix cost is seconds)
   is the auditable default for repair validation; Option II only via explicit Root authorization
   with fresh `verify_state_basis`/acceptance checks. No file overwrites, manifest swaps, or State
   edits as continuity.

## 5. Recommendation — bounded necessary REPAIR (concept selected, implementation gated on a short interface map)

- **Run unmodified: reject as plan.** Legitimate only as an explicitly cost-accepted bounded retry
  with timeout/observation; retrying duplicates the blowup per killed-note, and every future
  409-scale Weekly/Special edition would pay it again. Unknown cost is not zero; deferral moves
  work, it does not remove it.
- **Subsets / deferral: reject as completion.** Temp-only small batches are valid *equivalence
  oracles* (repaired private path vs unmodified public path, byte-identical cards/views where
  unmodified can finish) but subset outputs can never satisfy exact-coverage gates
  (`validate_interactive_input` 354–357: exact non-DROP 409/409; ledger exact-coverage;
  completeness universe U). No silent needs-drop, no fake full-W34 claim.
- **Repair: SELECT the concept, GATE the code.** The concept (one full validation per operation,
  pure per-task slices, package-linear final re-hash per write, public standalone unchanged) is
  the only alternative that keeps file reads package-linear where pins are unchanged while keeping
  late-drift refusal. But code must wait for a **short concrete interface map** — not a renewed
  broad precode carousel — fixing: (i) the exact threading mechanism (a/b/c in §3 with fail-closed
  operator-input rule and exception-safety); (ii) the full affected closure (the §2 accept/validate
  chain, plus explicit in/out disposition of LOW revision paths, renewal content core, and the ~10
  readback callers); (iii) the ONE-canonical-body factorization for card build/validate given the
  existing two-copy split; (iv) the per-write final re-hash rule (§4.1); (v) readback-freshness
  preservation (§4.2). That map is the next coherent unit's first deliverable; implementation
  follows only after Root accepts it.
- **Cost discipline:** count forward costs only — implementation + small-equivalence +
  current-full-409 completion (wall-clock + rchar as observation, never a recurring baseline) +
  fidelity-via-small-equivalence (no fabricated 409 byte-identity against a run that never
  completed; assert instead status preservation 352/49/8, R369/E439 exact, 3-oblig completeness,
  no-overwrite holds, `CANDIDATES_NORMALIZED` until legitimate advance) + late-fault Raw/manifest/
  task/State/Profile/drift negatives with partial-window honesty + DIRECT/DERIVED/historical
  CURRENT negatives (E-as-R, DROP-target, wrong-task, stale-basis refuse) + public-standalone
  negatives (manifest change between two direct calls → second refuses; no cache) +
  cross-operation no-reuse probe (manifest swap between two sequential operations → second sees new
  bytes) + current proof + audit rebind — versus real recurring work every 409-scale edition.
  Sunk PRE_CODE_READY cost and the existing implementation's existence must not prefer code;
  the assessment's "no ubiquitous cache / no new-feature gate / minimize total work subject to
  quality/provenance/Human" constraints stand.

## 6. Result

Author-independent planning verdict: the scaling assessment's measurements are sound and its
unmodified/subset alternatives are correctly rejected, but its §2 downstream-chain claim is
materially wrong (transitive per-task Raw sweeps through every acceptance wrapper, ~10–14 sweeps
per `run()`, not ~4) and its §4/§7 repair scope is therefore too narrow and
mechanism-unsettled. **Next coherent unit: short concrete interface map per §5, then the bounded
repair — only if Root authorizes. No automatic implementation, no code/runtime/audit/adoption
approval from this review. Stop at Human Commit Point.**
