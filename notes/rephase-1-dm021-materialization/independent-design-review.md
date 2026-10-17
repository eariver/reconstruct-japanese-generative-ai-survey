# DM021 materialization — independent design review (fresh, author-independent)

2026-10-16 JST. Fresh reviewer distinct from General analysis/correction
authorship and Astra/root selection. Design-only: no implementation, tests,
imports, runtime, fixtures, copy/restore, network, DB/index/ref/commit writes.
Only NEW file written in this unit is this review. Read-only means were
directory/file reads plus `git rev-parse`/`status` (sanitized env) against the
active candidate; no suite/proof execution, no cache imports, no patch
application.

## 0. Reviewed contract identity and source observation scope

- Reviewed contract: `outputs/rephase-1-dm021-staged-source-contract-decision.md`
  (104 lines), full SHA256
  `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`.
  This SHA is the reviewed decision; any edited contract bytes require
  re-review.
- Reconstruct HEAD (boundary context only, Human-authorized P2V closeout):
  `5595d214375f77c93fc3376799fb29b145bc5e32` — not candidate, production, or
  adoption authority; authorizes nothing in this unit.
- Candidate source observed read-only (no new byte proof):
  `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`,
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  status 3 modified tracked + 15 new source + 84 `__pycache__/*.pyc`
  (= 102 status rows; 18 source + 84 caches, matching the documented shape).
  P1 `cdd69fe7`, observer `79a3396c`, test `c567715d` pins and complete-18
  patch `dc5ae07b` bytes/modes are inherited from P2V TB1 proof, NOT
  rehashed or executed here. Cache bytes were not re-verified (path census
  only, consistent with packet README §15). No old 13+1 runtime acceptance
  is transferred to P3S; P2V scoped 13+1 remains its own bounded scope.
- Packet read fully: `notes/rephase-1-dm021-materialization/` README, `task.md`,
  `analysis.md` (623-line initial proposal), `source-binding.md`,
  `astra-feedback.md` (M1–M6), `correction.md`, `astra-feedback-r2.md`,
  `correction2.md`. Where final differs, final supersedes (listed in §5).

## 1. What the final selects (correctly narrower than history)

Final selects post-review staged TeX/Bib/style materialization with an
independent staged-set replay verifier in a closed proposal-owned namespace,
expected **3A/0M** (`contract:27-39`):

1. `scripts/survey_editorial_staged_source_v2.py`
   (`materialize_staged_source` + `verify_staged_source`);
2. `schemas/editorial-staged-source-manifest-v2.schema.json`;
3. `tests/test_survey_editorial_staged_source_v2.py`.

No edits to P1/P2R/P2V, loaders, renderers, receipt, Gate, controller, config,
or CLI (`contract:33`). This is the useful boundary: P1 already derives
proposed canonical reader bytes and P2V already observes scope-bound current
basis; reader-JSON-only staging would duplicate P1 and is correctly rejected
(`contract:9`, superseding initial `analysis.md` §6 / `correction.md` M4).
Unsupported positions from history stay withdrawn: direct-reader role /
4th-Gate inference from `_collect_pending_rows`, public-P1-after-retention
preflight, adoption-first readback, zero invalid-live window, fully-specified
P4, and `correction.md` State-bytes-healthy claim (`correction.md:16-21`,
`correction2.md:10-34`, `contract:16-23`).

## 2. Source verification (spot-checked at pinned bytes)

All `file:line` below are observations at the verified HEAD, not standing
references.

- **P2V scope/full-before ordering and coexistence.** `observe_current_authority`
  def `survey_editorial_current_authority_v2.py:101`; scope-before-final-receipt
  `current_authority:406-457` (scope `SCOPE` via `p1mod._validate_scope`,
  then `_final_full_receipt_recheck` at `:453`, then second
  `verify_retention` at `:460`, then `reverify`/snapshot/HEAD final boundary
  `:467-508`); `RESULT_SCOPE_BOUND` at `:37,:429`. Scope drift is pinned
  (`:421-442`). Fresh in-call P2R at `:235-248` with pin comparisons
  `:243-248`. This supports `contract:41,70-76` (fresh P2V-with-scope inside
  writer call, no prior dict/token; stable-fact re-observation without
  full-map equality).
- **P1 `_validate_scope` shape.** Def
  `survey_editorial_correction_proposal_v2.py:1775` takes
  `(col: _Collector, root, scope_review_value, proposal, state, profile)`;
  raw-first `col.safe` at `:1778`; public review loader call at `:1795-1799`
  (`surface_gate.load_and_validate_reader_surface_semantic_review`); post-loader
  re-read at `:1802` plus digest bindings `:1804-1807`; after-binding from
  persisted `proposed_reader_ref` `:1786-1793`; authority triple
  `:1816-1823`; substantive check `:1829-1834`; returns `REVIEW_BOUND_PROPOSAL`
  (`:51,:1835`) or `REVIEW_REQUIRED` (`:50,:1810`). `_Collector.__init__`
  (`:87-103`) pins HEAD + config — so constructing a live `_Collector`
  inside the artifact verifier would add HEAD/config assumptions, exactly as
  `contract:86` warns. `_Collector.safe` is raw-first alias/traversal/
  nonregular refusal (`:126-166`), i.e. `col.safe + metadata` as required;
  State/Profile are passed data for identity/comparison, not admission.
- **P2R historical chain.** `verify_retention(root, proposal_path,
  manifest_path)` def `survey_editorial_retention_v2.py:1731`; I1 chain
  `state:authority COPY → retained State → State.profile → KEEP Profile`
  at `:1827-1881` (COPY shape `:1838`, provisional dest `:1850-1859`,
  retained-State read `:1860`, profile-ref match `:1872-1880`); KEEP rehash at
  `:1961-1963`; `_Session` dirfd no-follow reader `:175-274`,
  `safe_read :369`, `repinned :463`; retained inventory rooted at
  `retained_rel` (`:759-772`, expected sets `:829-846`), i.e. a
  `staged-source/` sibling is outside the retained inventory — coexistence as
  `contract:46-47,76,96` requires is structurally plausible, subject to the
  §4 proof obligation (any enumeration refusal is a blocker, not a patch
  license).
- **Renderers / canonicalizers / helpers.** Longform `render_main :293`,
  `render_bibliography :468`; Weekly `render_main :400`,
  `render_bibliography :445` (`survey_weekly_derivation_v2.py`,
  `survey_longform_generated_v2.py`); `CURRENT_CLOSURE` at Longform `:52`
  and Weekly `:28` with exact-name/cardinality checks (`:570,:593` /
  `:619,:713`); `tex_escape` reused from `render_article_draft_tex`
  (Longform `:39`, Weekly `:19`; extensive call sites e.g. Longform
  `:314-456`). `STYLE_PATH = Path("templates/survey/jgaisurvey.sty")` in both
  modules (Longform `:43`, Weekly `:24`); receipt replay binds style to
  `(root / STYLE_PATH).read_bytes()` (Longform `:744-751`, Weekly analogous
  `:759-766`). This supports `contract:73,87-88,94` (deterministic replay,
  style-input vs output distinction, CURRENT_CLOSURE + enumerated extras).
- **Public Gate review loader.** `load_and_validate_reader_surface_semantic_review`
  def `survey_reader_surface_gate_v2.py:958`, strict schema/digest/surface/
  identity/substantive-check enforcement (`:983-1069`). Correct reuse target
  for either the `_Session`-adapter path (final) or the public-loader path
  (correction2); see §4 condition.
- **Generated receipt strictness.** Longform `validate_receipt` def `:665`
  (envelope `:660`), tool basis `:680`, contract equality `:683`, review
  reload+bind `:686-697`, readback context `:698-700`, canonical sibling/paths
  `:710-730`, FILE-byte replay `:741-757`. Weekly parallel `:726-773`.
  Supports `contract:19,68,87`.
- **Control pending loop / revalidation Gate-then-State.** `_collect_pending_rows`
  loop `for row in record["artifacts"]` at `survey_agent_control_v2.py:726`
  with canonical-role-only classification `:737-740`; QA block `:1900-1929`;
  Gate call `:1931`; record exclusive-create `:2031`; State replace
  `_atomic_replace_state_bytes` at `:2042`; post-State validation `:2044`.
  Supports `contract:17-20` adoption diagnosis (Gate→receipt→readback before
  State write) and the expressly OPEN promotion debt.
- **Explicit-path manuscript/bundle/Candidate.** `build_manuscript_manifest`
  `:297` / `validate_manuscript_manifest :358`
  (`survey_reader_publication_v2.py`); `validate_bundle(repo_root, path, ...)`
  `:232` (`survey_quality_v2.py`); `build_candidate :668`
  (`survey_publication_v2.py`). Validators take explicit paths (object-level),
  while Gate derivation `:1145` enforces canonical suffix `:1162-1169`,
  `:1201-1203` and receipt-next-to-surface `:1173,:1206` with triple equality
  `:1178-1181,:1211-1214` and output↔manuscript equality for exactly
  `main.tex`/`references.bib`/`jgaisurvey.sty` (`:1190-1197`) — matching the
  closed 4-file set (`contract:46-56`). This sustains the M4 correction:
  staged TeX has real explicit-path consumers for inspection/replay but no
  live Gate/receipt/manuscript consumer until promotion is designed.
- **Schema filename convention.** Existing schemas are all `*-v2.schema.json`
  (`editorial-correction-proposal-v2`, `editorial-retention-manifest-v2`,
  `longform-publication-source-manifest-v2`, etc.). Final proposes
  `schemas/editorial-staged-source-manifest-v2.schema.json` (`contract:30`) —
  conforming. Correction2's
  `schemas/staged-correction-source-manifest-v1.schema.json`
  (`correction2:152`) violates it; final supersedes it.
- **Result semantics.** Final returns `STAGED_SOURCE_MATERIALIZED` with exact
  manifest/output refs (`contract:75`) and `STAGED_SOURCE_REPLAY_VERIFIED`
  with observed refs/digests, never eligibility/admission/token
  (`contract:90`). Correct: materialized/replay only.

## 3. Design judgments confirmed (no rubber stamp)

- **Writer freshness.** `contract:41,70-76` requires actual
  `observe_current_authority(..., scope_review_path)` to return SCOPE_BOUND
  inside the writer's own invocation with refs matched to pins; no earlier
  dict, enum, caller token, alternate State, or public-P1-after-retention.
  Matches the corrected M2 withdrawal and the P2V observation-only contract.
- **Owned set / record-last / fault shape.** Exact
  `<proposal_dir>/staged-source/` with `main.tex`, `references.bib`,
  `jgaisurvey.sty`, `staged-source-manifest.json` (`contract:46-56`); absent
  root required, no takeover/retry/cleanup; manifest LAST with close/readback;
  pre-write refusal leaves nothing; post-claim partials preserved with
  phase/per-file/primary+secondary disposition; no truncation/rewrite/rollback/
  resume; incomplete reported as incomplete, never success (`contract:68-79`).
  Partial-or-complete-valid-bytes on manifest-write/close failure with
  indeterminate (not success) reporting plus later verifier attesting only
  byte match — not prior success — is the correct supersession of
  correction2 §5's blanket "failed invocation writes no manifest / torn bytes
  always invalid." No `STAGED_INCOMPLETE` status rewriting, no
  always-invalid failed-manifest claim (both correctly absent).
- **Manifest binding.** `contract:58-65` requires exact `proposal_ref`,
  `retention_manifest_ref`, `scope_review_ref`, labels + supported route,
  complete `basis`/`proposed` (no omitted before identity), 3 output refs,
  style-input ref to the fixed template, explicit replay dep list, producer
  HEAD as provenance only; self-digest excluding digest field; no full P2V
  hashmap self-inclusion; invocation snapshots in memory, stable refs persisted.
  This closes M5 traps. Fixed refs/digests are checked, not signatures; no
  HEAD-equality, tool-migration, or creator-attestation overclaim
  (`contract:89`).
- **Verifier independence, conditional.** `contract:83-90` is explicit:
  read-only retained/staged consistency + deterministic replay, not
  current-before readiness; no P2V/State call, no live mutable COPY; requires
  intact immutable refs, full P2R verification, historical layout, scope
  binding, supported replay deps; usable after live mutation ONLY while those
  stay intact; no future-adoption proof. Correct and bounded.
- **No build/Gate/adoption acceptance.** `contract:11,90,96-98` creates no
  managed PDF workflow, manuscript, quality bundle, Gate, Candidate, Preview,
  or live receipt; auxiliaries/PDFs excluded from the closed set; repository
  build tooling existence is not claimed absent; rendered acceptance,
  all-profile, migration, performance, savings remain unproved. Present
  consumers are exactly the verifier + inspection/diff + separate disposable
  build inputs. Full promotion/reason/pointer/role/Candidate collision stays
  OPEN (`contract:21,98`), not falsely fully designed.
- **Budget.** 3A/0M with named files (`contract:27-39`) is the minimal useful
  next step: new TeX/Bib/style outputs arrears P1/P2R/P2V cannot supply, with
  no touched validators. Plausible within precedent (P1/P2R/P2V scoped units).

## 4. Mandatory precode conditions (not current contract blockers)

These must be satisfied at General's concrete return / implementation; they
are conditions because each is constructible from the verified callsites, not
proof the design is already wrong.

1. **Scope-adapter contract.** `contract:86` prefers reusing P1
   `_validate_scope` through a narrowly scoped `_Session` safe-reader adapter
   + actual retained State/Profile data, forbids constructing live
   `_Collector` (HEAD/config) or faking current State, and makes infeasibility
   within 3A an exact returned blocker. Required precode: the adapter's
   method contract (which `_Collector` surface — `safe`/`files`/`reverify` —
   is shimmed over `_Session.safe_read`, how `root`/`head`/`config_sha` are
   neutralized, how retained State/Profile bytes flow without admission, and
   how raw-pin reverify after the reopening loader is preserved). Correction2's
   public-loader alternative (`correction2:71-83`) is a fallback comparison
   point only; final is authoritative. If the shim cannot preserve
   after-binding/substantive-PASS/raw-equality semantics exactly, General must
   return the concrete interface blocker instead of weakening scope rules.
2. **Fixed replay dependency list + import graph.** `contract:88,93` requires
   the implementation-derived exact set: renderer/canonicalizer/reader
   schemas, transitive helpers actually used (`tex_escape`, citation/access
   helpers), scope/review/schema/retention validation code, new module/schema,
   style input; direct-renderer-only insufficient; CURRENT_CLOSURE plus
   enumerated extras with coverage justification; TOOL_DRIFT refusal without
   executing historical code; source-import/runtime identity match. Required
   precode: the closed list with path/SHA/size roles and why no live-only
   helper leaks in. Constructible (see §2 helpers/closures), so a missing
   list today is a precode debt, not a design gap.
3. **Manifest exactness + write/close/drift semantics.** `contract:58-65,68-79`
   requires exact names/types/digest representation, canonical serialization,
   4-file + ancestor closure, no aux/temp, owned-delta-only final comparison
   (no proposal-subtree prefix exemption), original-byte (not rehashed-output)
   self-readback comparison, two P2V observations compared on stable facts
   only. Required precode: field table, digest construction, fd/exclusive/
   short-write/close/readback/fsync-fault matrix, and the two-P2V comparison
   predicate. Fault tests in `contract:96` (short/zero write, close/partial
   manifest, drift before write / after helper / self-readback, alias/FIFO,
   root/file replacement) must all be present; no observer writes before
   fixture repair.
4. **Coexistence + non-disturbance proof.** `contract:13,96` requires proving
   public P1 still destination-conflict refusal, P2R still VERIFIED, fresh P2V
   still SCOPE_BOUND with complete staging outside `retained/`, plus artifact-
   only HEAD compatibility and TOOL_DRIFT. Staged files are never consumed by
   those observers. Any enumeration refusal found in implementation is a
   blocker, not a patch license.

## 5. Final-vs-correction2 supersessions applied in this review

- Scope adapter: final `_Session`-adapter preference (`contract:86`)
  supersedes correction2 public-loader reuse (`correction2:71-83`).
- Failure shape: final partial-or-complete-valid with indeterminate reporting
  (`contract:77`) supersedes correction2 "no manifest / torn bytes invalid"
  (`correction2:109-114`).
- Dependency policy: final fixed implementation-derived set incl. transitives
  + CURRENT_CLOSURE + extras with precode justification (`contract:88`)
  supersedes correction2 renderer-modules-only `code_deps`
  (`correction2:87-105`).
- Schema identity: final `editorial-staged-source-manifest-v2.schema.json` /
  `kind EDITORIAL_STAGED_SOURCE_V1` / `status STAGED_ONLY` /
  `schema_version 2.0-rc1` (`contract:30,58`) supersedes correction2
  `staged-correction-source-manifest-v1.schema.json` /
  `STAGED_CORRECTION_SOURCE_V1` / `STAGED_INCOMPLETE` shape
  (`correction2:134-156`).
- Writer signature clarification: final
  `materialize_staged_source(root, state_path, proposal_path,
  retention_manifest_path, scope_review_path)` (`contract:35-39`) pins the
  manifest arg as the retention manifest (correction2's bare `manifest_path`
  read accordingly).
- Build claim: final "tooling exists; managed staged-build integration not
  selected; no aux in closed set" (`contract:11`, `contract:56`)
  supersedes any "no PDF-build entry" phrasing.

## 6. Verdict

**DESIGN_BOUNDED_PASS** — subject to the §4 mandatory precode return (API/
error/result/schema shapes, fixed replay dependency list + import graph,
scope-adapter method contract, canonical historical-layout chain,
preflight/final snapshot ordering, fixture/test plan per `contract:93-98`).
No hard contract rewrite is required: no concrete blocker was found that
invalidates the 3A/0M boundary, the closed 4-file namespace, freshness and
ownership rules, historical-namespace verifier, replay/TOOL_DRIFT policy, or
the expressly OPEN promotion debt.

A second full end-to-end (writer + receipt/Gate/manuscript + revalidation +
adoption) in one unit remains correctly rejected as unreviewable scope;
staged verification is correctly not its admission proof. Stop at this design
Human Commit Point; no candidate commit, implementation start, or runtime
acceptance follows from this review.

## 7. Scope qualification (2026-10-17 JST closeout)

This section qualifies §6 ¶284–286 without editing it. The full integrated
promotion is **deferred because concrete adoption predicates are unresolved**
(actual revalidation/Gate/receipt/strict-State cycle, truthful
reason/bindings, install failure window, unadopted Candidate collision per
Astra resolution S1–S5 on fixed contract 42eb8dbb), **not** because a ~10-file
diff is intrinsically unreviewable — contract §2 expressly rejects an
arbitrary file-count rationale, and "minimal" means the selected justified
bounded increment, not a cost proof over all alternatives. Accepted as
coherent refinements: S1 scope adapter uses only the actual method surface
(P1 `_validate_scope` via `col.safe` plus passed metadata) over actual P2R
`_Session` pins and P2R-verified retained State/Profile bytes — no live
`_Collector`, no dummy HEAD/config values or flag-neutralized authority
checks, no fabricated former-State; S2–S5 closed replay-dep/import graph,
manifest/completion/error, fresh-writer snapshot, and fixture/oracle budget
with exact-blocker return. Schema note in §2 is a selected-filename
convention claim only, not a repository-wide all-schemas census. Analysis
closeout clock 2026-10-16T16:55:44Z (= 2026-10-17 JST); contract document date
2026-10-16 preserved. No runtime, source revalidation rerun, or commit is
claimed by this append.

(End of file)
