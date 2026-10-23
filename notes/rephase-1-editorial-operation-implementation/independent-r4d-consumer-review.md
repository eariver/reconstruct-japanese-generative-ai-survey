# Independent R4d consumer/readback review — P1/P2V/P2R/P3S + normal consumers (CHANGES_REQUIRED)

Author-independent. Read-only. No tests executed, no imports executed, no network, no Git mutation.
Stable SOURCE only. No source edits. No synthetic genuine approval.

## 1. Basis and method

- Stable SOURCE: `/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60`
  HEAD `4191503bfe1bd6aadd90a107dc4fd7c601e53f6c` (from `R4d-report.md` §3;
  `source-manifest-r4d.json` 719 pins). I did not re-derive HEAD/tree by Git
  execution; I accept the worker-reported identity as the review basis and
  traced file bytes by `Read`/`Grep` only.
- Governing: `outputs/rephase-1-editorial-operation-contract-decision.md` (R3/V,
  §§4–6/8–9), `notes/rephase-1-editorial-operation-implementation/astra-implementation-selection.md`
  (frozen L interface, exact 50/22/27 closures, single role resolver),
  `astra-verification-return-r3.md`, `astra-verification-return-r4.md`.
- Returns read: `correction-r3/R3-report.md`, `correction-r3b/R3c-report.md`,
  `correction-r4c/R4c-report.md`, `correction-r4d/R4d-report.md`,
  `correction-r4d/source-manifest-r4d.json` (head section),
  `correction-r4d/reg-legacy31-exit.txt` (`0`), `reg-legacy31-stderr.txt` (head),
  `reg-p1-exit.txt`/`reg-p1-stdout.txt` (head),
  `correction-r4c/fixture-*-r4c-20261021T161000Z.py` existence only (not executed).
- Scope owned here: P1 (`survey_editorial_correction_proposal_v2.py`),
  P2V (`survey_editorial_current_authority_v2.py`), P2R
  (`survey_editorial_retention_v2.py`), P3S (`survey_editorial_staged_source_v2.py`),
  low selection (`survey_publication_set_v2.py`), high operation
  (`survey_editorial_publication_v2.py` signatures/CLI only), agent
  (`survey_agent_control_v2.py` selected functions),
  stage (`survey_stage_validation_v2.py`), production
  (`survey_production_v2.py` selected functions), Freeze
  (`survey_profiled_freeze_v2.py`), orchestrator/handoff/human_gate resolvers,
  export workflow (`.github/workflows/survey-production-v2-export-publication-preview.yml`),
  canonical refusals (R1/agent/semantic/wrappers), `survey_agent_tool_v2.py`
  narrow override, committed test `test_group_c_editorial_consumers_v2.py` and
  `test_survey_editorial_activation_faults_r4c.py` (static read only).
- Explicitly NOT owned / not traced beyond actual reads: deep H receipt/Gate/Reader
  internals, L low-level I/O/cache primitives, schema syntax, full history search.
  The parallel `independent-r4d-authority-review.md` owns deep H/L/IO/cache.
  No all-callers proof is claimed beyond the actual reads listed in §2–§8.

## 2. P1 repeated pre-Preview — static trace PASS with one unproved second-repeat fixture gap

Actual reads on stable source:

- Dispatch no silent pass-through:
  `scripts/survey_editorial_correction_proposal_v2.py:79-119`
  (`_dispatch_generated_receipt`): editorial kind `EDITORIAL_PUBLICATION_SOURCE_V1`
  validated via H with repo-relative relativization (`_rel_for_h`, 96–104);
  unknown kind raises `RECEIPT_KIND_UNKNOWN` (117); legacy kinds return `None`
  for H-owned Weekly/Longform strict dispatch (113–119). No caller-verified object.
- No untrusted receipt-kind param: P2V signature has no `receipt_kind`
  (verified via `test_group_c_editorial_consumers_v2.py:92-93` assertion and
  stable `survey_editorial_current_authority_v2.py:120-129` — kind derived from
  State/proposal/pinned receipt, `P2V_AFTER_ACTIVATION_REFUSED` at 196–197).
  Group-C test `test_handoff_gate_signatures_strict` statically enforces this.
- Early scope, not fake checkpoint: 1683–1699 — `_scope_ref` exact
  `{path,sha256}` from `scope_review_ref` (1686–1690), authored roles exact
  `{"proposed-publication-authoring","accepted-draft-archive"}` (1692–1694),
  FULL accepted list compare via shared `_frozen_names_check` + path equality
  (1695–1703); comment at 1696–1698 explicitly rejects single
  validation-checkpoint fake row. Ordinary branch runs same check at 1718–1721.
  `scope_review_ref` pinned (1689–1690) and gate-bound at 1738–1746
  (`scope_review_ref` path, `expected_surface_path=envelope_reader_rel`,
  same proposed-scope target equality, no copied review path).
- KEEP priors / State COPY / finite closure: `_build_graph`
  `survey_editorial_correction_proposal_v2.py:687-781` — mutable = effective +
  outputs + receipt + reviewed input + quality results + State (698–708) +
  pre-TeX scope-aware (`scope_review_ref` for editorial, 711–718) + mutable
  authoring inputs (723–729); versioned repeat discards prior versioned
  receipt-owned inputs from mutable (735–777), KEEP prior seal (746–749),
  KEEP prior receipt/reviewed/staged/quality/pre-TeX/authored (754–777),
  live State stays COPY (780–781). Policy deterministic at 783–785.
  Bound Candidate always active versioned when `VERSIONED_ACTIVE` (1023–1036),
  canonical initial otherwise (1037–1045) with alias refusal (1048–1051) and
  exact active-before binding checks (1061–1072). Prior seal/staged/proposal/
  retention nodes+edges at 1081–1103; checkpoint wrappers at 1105–1113;
  finite typed Evidence/Screening/Discovery transitives at 1115+ (no generic
  path-string recursion).
- No `validation-checkpoint` fake: 1695–1699 + 1720–1721.

Unproved (not a code bug, blocks readiness claim):
- Second pre-Preview correction on **4191503** has no new execution. R3c
  `verify-weekly-r3c-20261021T150000Z` / `verify-longform-r3c-20261021T152000Z`
  (both r1→r2 `ACTIVATED`, same anchor, `REAL TL2026 5pp`, `exit 0`) are bounded
  exact-epoch evidence on SNAPSHOT `0d9857e6…` (R3c-report §§47–62), not
  transferable to 4191503. R4c two-actives + inert checkpoints are on `b54a1f2`
  (R4c-report §§3–4). R4d-report §5 explicitly did not rebuild fixtures; rerun
  on 4191503 is ordered but not done. No automatic PASS transfer.

## 3. P2V before-only — static trace PASS

- `survey_editorial_current_authority_v2.py:180-197`: kind derived from
  State/proposal/pinned receipt (no caller enum, no `None` bypass); strict L
  selection; `VERSIONED_ACTIVE` requires true repeat
  (`proposal basis active_revalidation_ref == State pointer`), else
  `P2V_AFTER_ACTIVATION_REFUSED` (196–197). Ordinary receipt after old
  activation is refused; only new-active-basis true repeat proceeds.
- Retained-aware bridge intact: live vs retained cross-check (246–256),
  retained `verify_retention` same-invocation (277–281), SHA equalities
  (287–292), COPY/KEEP policy shape checks (319–342), final live/retained
  pin-drift rechecks (implied by 559–563 `PIN_DRIFT`). Read-only, no bearer.
- No receipt-kind caller token (see §2). No P1 public post-capture bypass
  introduced by P2V (P2V only observes; capture stays in P1/P2R).

## 4. P2R historical namespace — static trace PASS

- `survey_editorial_retention_v2.py:1737+` (`verify_retention`): standalone
  read-only, no P1/Git/HEAD; proposal/retention filename enforcement
  (1745–1752), schema pins (1757–1768), proposal_id/issue/Profile/path/sha
  equalities incl. `proposal_ref.path == supplied proposal path` (1771–1779),
  ordered plan projection no-reorder (1785–1803), KEEP `retained_ref == source`
  (1808–1813), COPY must carry `retained_dest/sha/byte_count` and must not carry
  `retained_ref` (1814–1816+). State COPY / Profile KEEP invariant preserved
  in capture path (1037–1067: KEEP must not carry COPY fields, COPY must not
  carry `retained_ref`, dest recomputation vs `proposal_dir/retained/`).
- Public P1 destination conflict preserved: COPY dest recomputed from
  supplied proposal dir (1850–1865, 1922–1931); outside-retained refused.
- No new invented retention-manifest location: refs come from exact receipt/
  staged `retention_manifest_ref`, not a hardcoded new path.

## 5. P3S 50 closure + writer/verify split — static trace PASS with fragility note

- Fixed 50: `survey_editorial_staged_source_v2.py:85-166` — 30 py + 14 schemas +
  3 route + staged + style + recipe = 50 (sorted-unique, no discovery);
  `P2V_MODULE` pinned at 61; `_SHARED_PY` includes low/high/current-authority
  (101–106); size/shape enforced at 161–168; extra-import requires expansion
  return (169–200).
- Verifier skips unloaded P2V file-pin but writer binds loaded version — as
  specified: 588–591 skip runtime binding when
  `sys.modules.get("scripts.survey_editorial_current_authority_v2") is None`
  (verifier path, file-pin via `dep_pins` still binds bytes); 592–618 fall
  through to full path+bytes binding when loaded (writer path, lazy-imported
  at 647 in `materialize_staged_source`). `TOOL_DRIFT` / `RUNTIME_BINDING_*`
  refusals at 595–618; `.pyc`-only refused (601–603). Recipe/style/schemas
  correctly file-pin-only (560–566, 574–579), not false `TOOL_DRIFT`.
- Fragility (unproved, not a current bug): correctness depends on
  `sys.modules` presence distinguishing verifier vs writer. No committed unit
  test exercises both branches (verifier-without-P2V-loaded vs
  writer-with-P2V-loaded) in isolated processes; only static
  `test_p3s50_and_recipe_binding` (AST count + string presence). A future
  harness that pre-imports P2V before verifier would silently switch branches.
  Require an explicit two-process test or a phase parameter instead of relying
  on ambient import state.

## 6. Low selection / anchor / legacy upstream — static trace PASS (R4d fix verified structurally)

- `_full_original_union` (`survey_publication_set_v2.py:1464-1485`): full
  `(name,path)->sha256` union over ALL checkpoint rows, dup-refusing,
  shape-checked. No seven-only filtering.
- `_anchored_canonical7` (1488–1588): VALIDATION_CHECKPOINT → original seven
  verified live (1506–1514); LEGACY_REVALIDATION → full-union cumulative rules
  (1530–1571), NEW guard `superseded name ∈ PUBLICATION_ROLES_7`
  (1543–1546, research never rebinds), live-verify EVERY effective row
  SHA-before-byte_count (1573–1580, scope `canonical`/`upstream` label at 1575),
  then project exactly seven (1581–1588).
- `derive_canonical_anchor` (915–1029+): full-union map (940–947), same
  superseded-canonical guard (1026–1029), cumulative `prior_sha == original`
  (implied by 1547–1550 + legacy-prefix validation), strict sequence/
  chronology/depth-32/cycle/duplicate checks, mixed later-legacy-after-editorial
  fail-closed (1005–1006).
- `resolve_publication_selection` (1624–1800): no-pointer genuine CANONICAL
  (1661–1676) with anchored verified 4-key rows; invalid pointer (even `{}`)
  fail-closed via shape checks (1642–1643, 1677–1681) — no invalid-pointer
  fallthrough. Legacy mode (1693–1766) enforces union equality to original
  validation (1729), live SHA-before-size (1735–1740), anchor/head cross-check
  (1744–1753). Editorial `VERSIONED_ACTIVE` (1768–1798) checks recorded anchor
  vs chain (1770–1771), seal drift (1774–1775), anchored canonical7 +
  verified active7 with seal byte_count cross-check, candidate drift (1784).
- `resolve_publication_artifact_path` (1803–1846): genuine no-pointer candidate
  fast path exact `None` only (1819–1822); every other role recomputes via
  selection + SHA drift check (1834–1835, 1844–1845); unknown role refused
  (1815–1816); invalid/malformed pointer never takes fast path (1823, 1881–1887).
- `resolve_stage_artifact_path` (1849–1895): candidate token must equal
  canonical token (1872–1879), otherwise exact template behavior + alias/
  traversal refusal (1888–1895). `resolve_publication_mode` (1909–1932) and
  `assert_canonical_publication_mode` (1951–1959) probe-only, fail-closed on
  invalid pointer, live drift never changes mode.
- Agent `_validate_checkpoint_record` editorial branch
  (`survey_agent_control_v2.py:405-436`): for `validation` only, original
  canonical templates historical, active roles via seal; anchored `canonical7`
  exact 4-key shape (430) vs chain-derived anchor; other checkpoints keep
  `superseded={}` (435–436). No research rebind. `_resolve_checkpoint_artifact`
  (662–800): seven publication roles project to active seal only after anchor
  validation (769–792); other roles retain historical semantics (766–768).
  Constants match: `ACTIVE_PUBLICATION_ROLES_7`
  (`survey_agent_control_v2.py:49-57`) == `PUBLICATION_ROLES_7`
  (`survey_publication_set_v2.py:89-97`).

## 7. Normal consumers — static trace mostly PASS, two CHANGES_REQUIRED gaps

Traced actual signatures (all require `repo_root,cfg,state,profile,name,template`
or `root,cfg,state` with no optional skip — enforced by
`test_group_c_editorial_consumers_v2.py:67-93`):

- Stage: `survey_stage_validation_v2.py:45-56` (`_require_selection` genuine
  `None` → `None`, invalid → propagate L error, no fallback);
  `63-70` thin L adapter, no swallow; `73-100` active-candidate binding
  recomputes via L + path + byte drift checks; `_prior_artifacts` 227–312
  validates historical rows, then VERSIONED_ACTIVE overlays active7 via L
  (291–302) + candidate binding (303–312). Historical + active7 independently
  materialized; `effective7` exact seven check at 289–290.
- Production: `survey_production_v2.py:39-44` genuine-`None` vs fail-closed;
  `56-67` active candidate via L when `VERSIONED_ACTIVE`, else canonical
  default; `validate_state_semantics:827-852` exact active Candidate in revised
  mode, canonical default otherwise, approval/candidate/PDF/page-count/byte
  bindings checked (838–852). Freeze/Manifest output paths stay canonical
  stable. PASS.
- Freeze: `survey_profiled_freeze_v2.py:29-50` strict selection first, active
  via `resolve_stage_artifact_path` when `VERSIONED_ACTIVE` (48–49), else
  canonical default; `build_profiled_freeze:80-99` requires RELEASE_CANDIDATE +
  approved Preview + Profile drift check + candidate/approval issue binding.
  Source/PDF/visual resolve via candidate (`publication._prepare_freeze_inputs`
  at 98) — active candidate path is active-aware, but Freeze record source/PDF
  bytes are derived from the candidate, not independently re-resolved per role
  via L. Bounded PASS; per-role PDF/visual independent re-resolution after
  Freeze is unproved (see §9).
- Orchestrator: `survey_orchestrator_v2.py:140-151` thin L adapter, propagates
  L errors; `_configured_expected_artifacts:154-170` recomputes via resolver;
  `_configured_gate_inputs:173-201` recomputes + `is_file` + stale-canonical
  path check (193–200). Handoff: `survey_handoff_v2.py:55-64` thin L adapter;
  `expected_output_contract:67-82` recomputes via resolver;
  `build_handoff:111-123` enforces outputs == contract + path equality.
  HumanGate: `survey_human_gate_v2.py:221-230` thin L adapter;
  `_reviewed_artifacts:249-305` recomputes via resolver + stale-canonical path
  check (263–270) + `validate_candidate` + PDF `sha256` drift check (299–303).
- Config templates: `config/survey-production-v2.json:230`
  (`PUBLICATION_PREVIEW` gate `publication-candidate` token) and `:361`
  (`VALIDATED_DRAFT` `publication-candidate` token) are the canonical tokens
  enforced by `resolve_stage_artifact_path:1872-1879`. New 5 schemas registered
  in `contract_files.pipeline` (67 entries, asserted by
  `test_config_registry_exact`); implementation scripts correctly NOT in
  `contract_files` (asserted at `test_group_c…:36-37`).

CHANGES_REQUIRED gaps (concrete, not style):

1. **Export State discovery includes non-authoritative States and has no
   alias/canonical-path guard; `**` non-recursive.**
   `.github/workflows/survey-production-v2-export-publication-preview.yml:79-90`
   (`_all_states`): `import glob as _glob` (line 67) + `sorted(set(
   _glob.glob('sources/*/production-state.json') +
   _glob.glob('sources/**/production-state.json') +
   _glob.glob('specials/**/production-state.json')))` (line 82) passes no
   `recursive=True`, so `**` does not recurse (Python `glob` semantics).
   Deep `sources/a/b/production-state.json` / `specials/a/b/...` are missed
   while top-level duplicates are double-counted. No exclusion of
   historical/retained/copied/noncanonical States (`*/retained/*`,
   `*/history/*`, `*copy*`, checkpoint copies) and no symlink/alias rejection
   or canonical Profile-derived State-path check before
   `json.loads((root/state_rel).read_bytes())` at 122–123.
   Matching by `issue_id` alone (147–156 manual, 215–224 PR) can then conflate
   a retained copy carrying the same `issue_id` with the live authoritative
   State; `ambiguous State paths` refusal (154–155, 223–224) triggers only on
   count ≠1, not on noncanonical membership. Inert-set guard (141–142, 205–207)
   and stale-canonical mismatch guards (161–162, 229–230) do not cover this.
   Committed `test_export_no_absolute_relative_bug`
   (`test_group_c_editorial_consumers_v2.py:127-132`) asserts only `_norm`,
   old-bug absence, no-swallow, and `ambiguous`+`inert` strings — it does not
   cover `recursive=True`, noncanonical exclusion, or alias refusal.
   Fix: pass `recursive=True` (or enumerate exact expected roots), filter to
   exact canonical `sources/<issue>/production-state.json` +
   `specials/<issue>/production-state.json` (or Profile-derived canonical
   State path), exclude `*/retained/*` and any non-`production-state.json`
   historical/copied States, `lstat`-reject symlinked State files/ancestors
   before read, and fail on ambiguous/mismatched/inert/no-State/invalid-root/
   config-caller-controlled inputs. Until fixed, export standalone
   post-`RELEASED` provenance is unproved for nested Special layouts.

2. **Orchestrator/handoff recompute paths but do not byte-compare to the
   active pin; stale-bytes-same-path not refused at the loader.**
   `survey_orchestrator_v2.py:173-201`: after `resolve_configured_artifact_path`
   (187) and `is_file` (189–190), VERSIONED_ACTIVE checks only
   `cand_ref["path"] != rel` (197–200); `core.sha256_file(path)` at 201 is
   recorded, never compared to `cand_ref["sha256"]`.
   `survey_orchestrator_v2.py:154-170` (`_configured_expected_artifacts`) and
   `survey_handoff_v2.py:67-82` (`expected_output_contract`) + `111-123`
   (`build_handoff` path equality) have the same shape: path equality to the
   resolver, no `sha256 == selection pin` comparison. Stage
   (`survey_stage_validation_v2.py:97-100,300-301`) and HumanGate PDF
   (`survey_human_gate_v2.py:299-303`) do byte-compare; the two
   producer-side loaders do not. Contract §8 requires “recompute and compare
   in loaders, not only producers.” A same-path drifted candidate would be
   recorded with a new hash rather than refused as stale.
   Fix: after recompute, compare `core.sha256_file(resolved) ==
   sel["candidate_ref"]["sha256"]` (and for each active7 role where applicable)
   and refuse on mismatch, propagating selection errors (no swallow).

## 8. Canonical refusals, runtime tool, receipt post-RELEASED — static trace PASS with pending matrix

- Canonical revalidation writer refuses editorial + revised mode before writes:
  `survey_agent_control_v2.py:2109-2129` (`REVIEWED_EDITORIAL_CORRECTION`
  refused at 2110–2114; `assert_canonical_publication_mode` before any
  destructive action/guard at 2121–2129).
- R1 refuses revised mode before guard/output:
  `survey_weekly_mechanical_refresh_v2.py:823-839`
  (`_require_canonical_mode_for_r1` via `require_active_or_canonical(...,
  want_versioned=False)`), called at 890–891 before guard/output creation.
  R1→correction (initial R1×2 before activation) remains supported; R1 after
  activation refuses (message cites §10, no editorial-reason bypass).
- Wrappers/semantic canonical writers refuse revised mode before writes:
  `survey_semantic_quality_v2.py:176`,
  `run_semantic_publication_v2_interactive.py:45-51`,
  `run_semantic_publication_v2_interactive_base.py:128`,
  `test_wrappers_entry_refusal_no_swallow` asserts L guard presence + no
  `except-return` swallow. PASS statically.
- Runtime tool narrow, no broad patch:
  `scripts/survey_agent_tool_v2.py:121-143`
  (`current_stage_basis_override` patches exactly three functions
  `core.verify_state_basis`, `screening.validate_package_basis`,
  `evidence.validate_evidence_package_basis` with `try/finally` restore at
  140–143), used only by `run_helper` at 167 inside
  `with current_stage_basis_override():`. No `for ... in sys.modules` /
  `for ... in list(sys...)` all-instances loop (Grep confirms only P3S
  `sys.modules.get` tripwire reads at
  `survey_editorial_staged_source_v2.py:589-593`, which is a read, not a
  patch). Restored hash `0ff3…` claimed by R4c-report §1; hash not re-derived
  here (read-only, no execution), but static shape matches the narrow-override
  requirement — do not support patching the wrong namespace globally.
- Standalone post-`RELEASED` receipt: high
  `validate_editorial_receipt` (`survey_editorial_publication_v2.py:563+`)
  is standalone (strict State via `agent.validate_agent_state` at 603–608,
  no global patch, no caller `pending/ignore` flag), and R4c isolated
  per-fixture receipt (`correction-r4c/test-r4c-longform-receipt-isolated.py`,
  R4c-report §2: fresh subprocess per fixture, single-root `sys.path`,
  `RELEASED` `RECEIPT_PASS` for both Longform SP001/lf-r3c-2 and Weekly
  2026-W37) passes. The R4-observed mixed-harness failure (Weekly+Longform in
  one process, `scripts` namespace accumulation) is a harness isolation defect,
  not a source bug. Production runtime correctly stays unchanged. Do not add a
  global namespace patch to accommodate the mixed harness.
- Legacy 31 now 31/31 within unit (not upstream pre-existing):
  `correction-r4d/R4d-report.md §4` + `reg-legacy31-exit.txt:0` with
  `reg-legacy31-stderr.txt` all-`ok` head (n1–n11 including
  `test_r1_partial_record_write_retained_fail_closed`). This supersedes the
  R4c 28/31 + `reg-legacy-reval-0dcheck` pre-existing-failure record (R4c-report
  §6) **for this code epoch only**; it is not an upstream production claim and
  does not transfer to other epochs.
- New R4d full matrix pending: R4d authoritative runs are unit regressions
  only — legacy 31/31, P1 9/9, retention 25/25, current-authority 14/14,
  staged 26/26, agent 5/5, state-authority 2/2, low 18/18, schema-cache 6/6,
  fault 4/4 (R4d-report §4) — plus failed-legacy31 preservation. No
  prepare→finalize→activate→normal Preview/Freeze/Release lifecycle,
  second-correction, R1×2→activation, orphan-resume, fault/negative matrix was
  executed on 4191503. R3c second-correction + R1-anchor and R4c orphan-resume
  remain bounded exact-epoch observations (0d9857e / b54a1f2), not 4191503
  proof. Whole readiness, production semantic quality, and Human adoption
  remain NO-GO/open per contract §10.

## 9. Test-coverage gaps — explicitly listed (not PASS)

Committed tests on stable source (static inventory, not executed):

- `test_group_c_editorial_consumers_v2.py` (8 tests): config 67 + 5 schemas,
  stage fail-closed/genuine-initial, orchestrator/handoff/gate signatures +
  no-`receipt_kind`, single-`resolve_stage_artifact_path`, P3S 30+14 + recipe
  strings, export `_norm`/no-swallow/ambiguous+inert strings, wrappers L-guard
  strings. All static/behavioral-shape; none executes export, none executes
  public CLI, none drives normal Preview→Freeze→Release bytes.
- `test_survey_editorial_activation_faults_r4c.py` (4 tests): record-fsync,
  State-fsync, foreign-inode, predecessor+1/intent — real OS fault seam, no
  success mocks. Covers §7 fault seams narrowly. Does NOT cover close/
  post-replace readback validation, `INDETERMINATE` (neither-known-nor-expected
  State), `ALREADY_ACTIVE` read-only path, or State-write predecessor drift
  beyond intent collision.
- `test_survey_publication_set_v2.py` (18), `test_survey_publication_revalidation_v2.py`
  (31, now 31/31), `test_survey_editorial_correction_proposal_v2.py` (9),
  `test_survey_editorial_retention_v2.py` (25),
  `test_survey_editorial_current_authority_v2.py` (14),
  `test_survey_editorial_staged_source_v2.py` (26): unit regressions only.
  P1-9/retention-25 previously hit helper `.latexmkrc` sandbox setup errors
  (R3c-report §36; R4d-report §2 fixes factories to copy tracked `.latexmkrc`);
  R4d claims 9/9 + 25/25 on 4191503 — accepted as worker evidence, not
  re-executed here.

Missing (must be added before normal-operation readiness; do not claim PASS
by absence):

1. Public CLI: `survey_editorial_publication_v2.py:3404-3475` seven subcommands
   (`prepare/finalize/validate-receipt/validate-set/activate/resume/verify-history`)
   have no committed CLI test in a fresh process with real fixture States.
   Only `correction-r4c/fixture-*-r4c-*.py` driver scripts (not committed tests)
   exercise them.
2. Normal both stages: no committed test drives healthy
   `VERSIONED_ACTIVE` Candidate through synthetic Preview approval
   (`approve_publication_preview`), `build_profiled_freeze`, Freeze/Release
   checkpoint validation, and `verify_activation_history` historical vs active
   readback on 4191503 for both Weekly and Longform. R3c/R4c fixtures did this
   on prior epochs only.
3. Fault/negative matrix on 4191503: same-issue wrong seal/manuscript/
   Candidate; old canonical Candidate supplied after activation; inert valid
   set not adopted; unconsumed/unknown record branch; research ref change;
   old-authored/new-reader inconsistency; equal-SHA different reviewed path;
   stale/failed/missing external reviews; build failure/extra-input/output/
   hash drift; seal missing role/unknown ref/duplicated role; legacy-anchor
   error/cycle/depth/sequence; State/predecessor drift; approved/foreign
   Candidate; canonical writer after activation; every record/State
   write/close/late-readback failure with observed old/new/unknown disposition
   plus explicit resume/healthy control — per contract §9 — has no committed
   4191503 execution. Only R4c fault scripts (orphan resume) on `b54a1f2`.
4. Export execution: no test executes the 311-line export workflow predicate
   (inert/oldCandidate/ambiguous/noState/invalidRoot/config-caller-controlled
   negatives, absolute-vs-relative, alias, `recursive=True` behavior). Static
   `test_export_no_absolute_relative_bug` is necessary but insufficient.
5. P2V/P3S branch coverage: no committed two-process test for P3S
   verifier-without-P2V-loaded vs writer-with-P2V-loaded binding (§5 note);
   no committed test that ordinary Weekly/Longform receipt after activation
   refuses P2V while true repeat passes on 4191503 (only code + prior-epoch
   e2e).

## 10. Verdict: CHANGES_REQUIRED

Concrete code changes required (§7.1–7.2) plus unproved requirements (§2
second-repeat, §5 P3S branch test, §8 full matrix, §9.1–9.5 tests). Do not
ship, do not claim normal standalone post-`RELEASED` operation, whole
readiness, production semantic approval, or Human adoption on this review.
Independent authority review (deep H/L/IO/cache) remains separate; this review
covers only the consumer/readback scope actually read above and makes no
all-callers proof beyond those reads.

Independent reviewer: no synthetic genuine approval; no source edits made;
no history duplicated beyond the targeted paths cited.
