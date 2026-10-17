# Correction 2 — staged source materializer gaps (R2)

2026-10-16 JST. General second correction. `analysis.md`,
`source-binding.md`, and `correction.md` are PRESERVED intact; this file
withdraws or narrows only the items below. Design-only: no code/tests/
fixtures/network/runtime/copy/commits. Read-only basis: active
`candidate-partial-b40de60` (HEAD `409b292`, 18/18 v5 MATCH) plus fixed
P1/P2R/P2V contracts and the P2V B1 resolution. Summaries, not raw.

## 1. Withdrawn: "State bytes unchanged ⇒ healthy" and "only review-binding gap" (`correction.md` §3, lines ~156–181)

**Explicitly withdrawn.** Strict State validation does not stop at State
JSON bytes: `_validate_agent_state`
(`scripts/survey_agent_control_v2.py:353`) resolves the active
revalidation record and checkpoint provenance against LIVE bytes
(`resolve_active_publication_revalidation` at `:391`,
provenance/drift checks at `:396–412` and following). Replacing live
checkpoint artifacts invalidates the old State even when the State file
itself is untouched. The pending-basis mechanism bounds only what its
callers admit: Weekly `load_derivation` accepts a checked pending basis
(`survey_weekly_derivation_v2.py:475–487`); Longform has NO pending-basis
entry — `load_derivation` is strict DRAFT_COMPLETE-only (`:1101–1127`)
and `load_derivation_for_readback` takes no pending parameter and runs
strict `validate_agent_state` (`survey_longform_derivation_v2.py:1142–
1182`). The Weekly fallback is mechanical-refresh replay machinery, never
editorial permission — it is not cited as such anywhere in this design.

Consequence: the install→adoption window is NOT bounded by existing
machinery for the primary (Longform) route, and review-path binding is
NOT the only gap. Design-open, stated plainly: future editorial
checked-context / public post-adoption readback semantics; truthful
reason/binding representation; install ownership/failure window; and
unadopted-Candidate collision disposition. **P4 is not fully designed.**
No zero-downstream-changes claim survives.

## 2. Corrected coexistence oracle: P1 MUST refuse, P2R/P2V pass

`correction.md` §§1–2 ("P1 still bound after staging") is corrected:
public P1 `validate_proposal` on a retained proposal MUST refuse
(destination conflict via `_require_retention_dests_absent`,
`survey_editorial_correction_proposal_v2.py:1287–1306`) — that refusal is
part of the oracle, proving retention occupancy. Required post-staging
triple: (a) public P1 refuses with the retention-destination code;
(b) P2R `verify_retention` still `RETAINED_SET_VERIFIED` (retained tree
untouched — inventory scoped to `<proposal_dir>/retained`,
`survey_editorial_retention_v2.py:1927–1952`); (c) fresh P2V with scope
still `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`. Staged files are never
consumed by these observers; they must be proven unperturbing, with any
enumeration refusal an implementation blocker (not a patch license).

## 3. Artifact verifier: exact historical namespace, no faked present

`verify_staged_source(root, proposal_path, staged_manifest_path)` —
explicit proposal path REQUIRED (no bare-manifest verification; namespace
cannot be derived safely from the manifest alone):

- Staged manifest carries a REQUIRED `retention_manifest_ref`
  (path+sha256). The verifier calls actual P2R `verify_retention` on the
  supplied proposal + bound manifest in-call (read-only, needs no live
  authority — P2R §4). No implicit old-P2V token is accepted.
- Canonical namespace comes from HISTORY, never mutable live State:
  retained State COPY (a `COPY_BEFORE_REPLACEMENT state:authority`
  row — P2V B1 resolution) → its profile ref → KEEP Profile bytes
  (P2V contract §4.7; every KEEP row rehashed in P2R verify at
  `:1961–1963`) → `paths.source_root` → expected
  `<source_root>/publication/v2/editorial-corrections/<proposal_id>/`;
  the supplied proposal path's parent must equal it, and
  `staged-source/` must hang beneath it. Historical parsing of
  State/Profile bytes is provenance reconstruction, not current-State
  admission.
- Scope binding is rechecked against historical metadata with EXISTING
  checks: the narrow adapter calls the public
  `surface_gate.load_and_validate_reader_surface_semantic_review`
  (the exact call P1 makes at `proposal_v2.py:1795–1801`) with expected
  values taken from the supplied proposal (`proposed_reader_ref`
  path+sha) and retained issue/Profile, then applies the triple rule
  (before == `basis.active_reader_input_ref`, after == proposed ref,
  upstream == `preserved_upstream_digest`) plus the substantive
  scope-PASS check. Private P1 `_validate_scope` (`:1775`) expects a live
  `_Collector`; the adapter does NOT construct one (that would fake
  current authority) — it reuses the public review loader + manifest
  pins, all inside the builder module (no new interface beyond §6
  budget, no blanket current-git reliance).

## 4. Replay code/tool policy (explicit)

Re-render executes CURRENT code; an informational `producer_HEAD` does
not immunize anything. Exact rendering+validation dependency set,
recorded in the manifest as `code_deps` (path+sha256 each): the route
renderer module(s) (`survey_weekly_derivation_v2.py` /
`survey_longform_derivation_v2.py` + `survey_longform_generated_v2.py`
canonical-bytes function), the reader-input schema(s) used by
validation, and the style SOURCE file
(`STYLE_PATH`, not the staged copy — staged style binds to the actual
pinned style input bytes, never to itself). Verify pins current bytes
of every `code_deps` entry and requires equality with recorded shas:
match → replay is meaningful; mismatch → `TOOL_DRIFT` refusal
(code-relative scoping stated in the result, not silent acceptance, not
historical-code execution). An artifact-only HEAD advance alone never
invalidates anything (bytes, not HEAD, are compared). Post-live-State
independence of `verify_staged_source` is CONDITIONAL: it holds only
while KEEP bytes, tool deps, staged refs, and referenced paths are
intact — arbitrary future schema/path/code changes may refuse, and no
independent rederivation of accepted research from current State is
claimed by an artifact-only verifier.

## 5. Record-last, failure shape, self-readback rule

- ONE immutable completion artifact: `staged-source-manifest.json`
  with `status: STAGED_ONLY`, written LAST, closed and read back. No
  status-rewriting: a failed invocation writes NO manifest; torn
  close-failed bytes possibly left on disk are INVALID (digest mismatch
  on later read) and a later verifier observing them attests nothing
  about that invocation's success.
- Owned namespace is exactly 4 files
  (`main.tex`, `references.bib`, `jgaisurvey.sty`,
  `staged-source-manifest.json`) plus the ancestor closure
  (`staged-source/`; the proposal dir pre-exists and is not owned). No
  aux/build outputs inside. No existing-root reuse or takeover by byte
  equality without a separate justified contract.
- Drift check after self-readback compares ORIGINAL expected
  bytes/input pins, never a fresh snapshot of changed outputs.
- Fresh P2V re-observation after the materializer's own writes compares
  STABLE proposal facts (proposal/reader/scope/manifest refs, basis
  digests) — never the full `input_hashes` map, which would self-include
  the new staged files (M5 trap restated as a MUST-NOT).

## 6. Build-claim qualification and exact 3A proposal

Withdrawn as phrased: "no PDF-build entry exists." Correct statement —
the repository HAS build workflows/tooling; what is absent is a
SELECTED managed staged-build entry in this design. P3 supplies ordinary
exact staged source inputs for inspection or a SEPARATE disposable
build, certifying neither workflow integration, rendered QA, new Human
Preview, nor Gate admission; no auxiliaries enter the closed 4-file root.

Exact budget **3A / 0M** (any live-validator/loader/P1/P2R/P2V
modification is a blocker to Astra, not edit authority):

1. A `scripts/survey_editorial_staged_source_v2.py` —
   `materialize_staged_source(root, state_path, proposal_path,
   manifest_path, scope_review_path)` (current-before readiness: fresh
   in-call P2V-with-scope → SCOPE_BOUND; derive via actual route
   loaders with Weekly pending fallback FORBIDDEN; exclusive 4-file
   write, manifest last, replay+readback) and
   `verify_staged_source(root, proposal_path, staged_manifest_path)`
   (authority-free integrity + §3 historical namespace + §4 code-dep
   pinning), incl. the narrow scope adapter.
2. A `schemas/staged-correction-source-manifest-v1.schema.json` —
   strict keys incl. REQUIRED `retention_manifest_ref`, stable refs,
   `code_deps`, digests; unknown-field rejection; `2.0-rc1` convention.
3. A `tests/test_survey_editorial_staged_source_v2.py` — synthetic
   accepted-chain Longform-prose (primary) + Weekly-envelope + R1
   oracles: determinism, FILE-byte equality, coexistence triple (§2),
   namespace-exclusivity, TOOL_DRIFT, close-fault invalidity, manifest
   tamper, post-adoption verify independence, artifact-only-HEAD
   non-invalidation. No genuine approvals, no old-suite transfer.

Real remaining promotion debt (open, not designed): post-adoption
readback representation (§1), truthful reason/binding, install window
ownership/failures, Candidate collision. Net lifecycle savings
unmeasured; any interface/State/adoption expansion is a separate
decision. No new Human role/Gate, no production fixture.
