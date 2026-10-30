# DM022 G71->G76 compatibility witness progress (dedicated executor)

Author: G71-G76 compatibility witness executor/author, NOT independent reviewer.
Binding: selected `a345bb95` INCLUDING §11, precode ROOT `0425c530` INCLUDING §5
(§3 + §5.2), independent-cross-family-boundary-review §8 (API sequence
source-feasible, NOT test proof), whole-lifecycle Attempts 8-9 (same-G76
editorial/U/C done, G71 control never attempted).
Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all runtime authors idle). Own ONLY `tests/test_dm022_g71_g76_compatibility_v2.py`
+ `tests/dm022_g71_g76_fixture_v2.py` plus this progress doc and
`evidence/g71-g76-20261029T041142Z/*`. No edits to any existing runtime/test
files. No ordinary candidate/reconstruct commit, root DB objects, new fake
production root, Human readback, network/old runner/cleanup.

## Identity (actual, not re-certified planning pins)

- OLD read-only: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  actual409 `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce36998…`, 742
  files, pipeline71, no DM022 modules. HEAD/tree verified pre-run.
- NEW intended TOOL (candidate-work, frozen, not re-hashed here):
  `survey_editorial_publication_v2.py` `3a8721569d3c…` (CURRENT-only, no OWN
  fallback), `survey_publication_v2.py` `f0486c54e8a6…` (C2 Freeze fix),
  `survey_versioned_renewal_history_v2.py` `a9de2c97eb40…`,
  `survey_versioned_renewal_source_v2.py` `b139f493f791…`,
  `survey_agent_control_v2.py` `b6506a8b3344…` (B preserved walker).
  Config pipeline76 (5 DM022 schemas), 2 new modules +5 schemas.
- G71 source epoch (genuine, no DM022, TinyTeX): pre-existing worktree
  `.rephase-1-editorial-runtime/dm022-g71-control-20261029T001711Z/worktree`
  commit `13a7752…` (final93 +93, pipeline71). Reused as OLD base (read-only
  reference, not mutated).
- G71 fixture epoch (SAME-fixture, source before data, PROCESS identity,
  inert origin, no shares, no empty commits):
  successful run `G71 epoch 86f51eeedeed…` (fixed4 run 20261029T042856Z),
  parent G71 `86f51ee…`, G76 `9074cc9cf97e…` (genuine delta, 62 files,
  upstream 7 pins byte-identical). Earlier epochs `50de687…`, `a261ea88…`,
  `369ce7d7…`, `e20825f3…`, `6ad3e0b8…` are preserved failed/harness-fix runs,
  never overwritten.
- Fixture: `/tmp/dm022-g71-keep-ny24cxee` (preserved, mkdtemp, no auto-cleanup),
  HEAD `9074cc9cf97e…`/tree `cee19c25…`, origin `https://example.invalid/g71-witness.git`,
  no alternates, no shares (copytree, no --link), PROCESS identity
  `Synthetic G71 witness`.
- DURABLE (outside packet, independent DB, no shares, inert origin):
  - FROZEN `…/dm022-g71-g76-durable-20261029T044241Z` HEAD `9074cc9c…`,
    903 files excl .git, working tree FROZEN (State FROZEN, renewal
    ACTIVATED/VERSIONED_ACTIVE, CURRENT proof green, PUBLIC State green,
    Candidate/Preview/Freeze done, RELEASED blocked below).
  - prePreview `…/dm022-g71-g76-prepreview-20261029T044319Z` HEAD `9074cc9c…`,
    clean working tree, lifecycle VALIDATED_DRAFT (VERSIONED_ACTIVE prePreview,
    no Preview, no renewal yet – clean HEAD checkout, ideal for C1 HighU).
  Actual paths/pins, not cleanup dangling; no GitDB in packet (packet has pins
  + raw only).

## Script/API/source (actual execution, fresh subprocess inside fixture)

- TinyTeX absolute from START: `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex`
  + `biber` (verified is_file before any build, every driver).
- G71 epoch (OLD code only, fixture-bound imports verified via
  `inspect.getfile(core).startswith(fixture_root)`, never hot root):
  `SurveyEvidenceV2Tests` sandbox/discovery/screening/evidence/views +
  `build_materiality_ledger` + hand-built legacy EVIDENCE_REVIEWED (no DM022,
  no PREARCH) + `run_selection_architecture_v2_interactive.run` (NEW
  independent Selection input, audit no-overwrite) + public
  `agent.build_stage_checkpoint`/`advance_with_checkpoint`
  EVIDENCE_REVIEWED→SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED + synthetic
  ArchitectureGate (explicit nongenuine) + pure `derive_draft_package` (historical
  synthetic, avoids old ScreeningStateSHA bug – normal G71 Draft after advance
  would hit `state_sha256` drift, labelled accurately, no G76 patch imported)
  + `derive_draft_package` content validation + synthesis + DRAFT_COMPLETE +
  weekly derivation + surface-only + explicit synthetic surface review + full
  render + REAL disposable lualatex+biber PDF (isolated build dir, pid/exit/full
  log per step, `%PDF` + pypdf pages asserted, exact transfer, no overwrite) +
  manuscript + deterministic QA + synthetic semantic/visual + reader-surface
  gate + VALIDATED_DRAFT (strict State valid).
- G71 editorial R3 (OLD 63-closure, CURRENT-only at G71 disk):
  P1 `prepare_proposal`/`validate_proposal` REVIEW_REQUIRED (real revised deck,
  not fake Core reason) → P2R `capture_retention` RETAINED_SET_CAPTURED →
  external synthetic scope (explicit nongenuine) → P2V `observe_current_authority`
  CURRENT_BASIS_OBSERVED_SCOPE_BOUND (genuine current-before, not cached) →
  P3S `materialize_staged_source` via fixture-code subprocess (fresh
  fixture-bound runtime, pid/exit/raw unique) → `prepare_publication` REAL
  TinyTeX build (CURRENT63, CURRENT-only admission – final93 shape, no OWN
  fallback) → external synthetic postrender reviews at exact new manuscript/PDF
  (never old rebind) → `finalize_publication` + `activate_publication`
  VERSIONED_ACTIVE (mode via `resolve_publication_selection`, PREARCH? No –
  G71 has no PREARCH, family LEGACY? Actually mode VERSIONED_ACTIVE, no
  PREARCH readback – G71 has no DM022, labelled accurately).
- Snapshot/pin ALL accepted authorities pre-overlay (7 upstream paths):
  canonical State, candidate-matrix, candidate-selection, architecture,
  architecture-review-summary, draft synthesis-input/result (exact SHAs in
  `g71-probe-fixed4-…stdout`, `upstream pins: 7`).
- Install EXACT NEW G76 TOOL delta in SAME fixture (62 files: config +5 schemas
  + mapped scripts including 2 new DM022 modules + B/C1/C2 mapped changes;
  tests included in overlay list but not control – genuine code/schema/config
  delta, no outside-control intent; accepted research/Profile/Architecture/Draft/
  reader/reviews/State pointer untouched – verified byte-identical post-overlay).
  New meaningful source commit `9074cc9c…` (genuine G71→G76: pipeline71→76,
  Contract8, 7 renewal +7 DM022 files, 5 schemas; old≠new, no empty commit,
  PROCESS identity). Post-commit `git status` 0 lines on control roots
  (PYTHONDONTWRITEBYTECODE=1 + pre-add `__pycache__` purge – earlier dirty
  `BASIS_CURRENT_TOOL_DRIFT` was harness `__pycache__` tracked, fixed, preserved).
- Public HIGH renewal U (genuine G71→G76 Core change, REUSE_TARGETS – actual
  replay exact Targets, no new build):
  `prepare_renewal` (entry `_observe_renewal_entry` LIVE canonical State+config,
  PUBLIC `agent.validate_agent_state` epoch-agnostic per §8.2 → `_load_prior_graph`
  typed historical bytes only, never LIVE permission → COPY claim + historian
  `verify_versioned_history` OWN-epoch structural → CURRENT70 closure recompute
  from live disk → basis LAST → `observe_renewal_authority` live-live + CURRENT
  member-wise + detached `validate_renewal_basis`) →
  `finalize_renewal` (detached `verify_renewal_source_proof` CURRENT70
  member-wise on every readback, no caller-verified dict, no pending) →
  `verify_renewal_source_proof` CURRENT_PROOF_VALID true →
  `activate_renewal` VERSIONED_ACTIVE via normal HIGH full PUBLIC State
  validation (PRE-activate `[]`, POST-activate `[]`, repeat CURRENT proof true).
  Old G71 OWN history passes (`_derive_tool_generation` G71, CURRENT G76,
  63 vs 70, delta 2+5). Old G71 editorial receipt (63-row, G71 contract,
  `validated-source-manifest.json`) at G76 correctly REFUSES (expected
  `STAGED_REFUSED TOOL_DRIFT … scripts/survey_agent_control_v2.py` – old staged
  proof pinned G71 bytes vs CURRENT G76 disk; stale refusal IS the control
  signal, exactly like renewal “old full current receipt correctly fails”).
  New matched typed CURRENT proof enables NEW G76 renewal (no private bypass).
- Normal downstream (G71 has no PREARCH trio, so no Freeze-trio block):
  Candidate `build_stage_checkpoint`/`advance` → RELEASE_CANDIDATE (strict
  valid) → synthetic Preview approval (explicit nongenuine) → `build_freeze`
  (canonical `source_root/publication/v2/freeze-record-v2.json` +
  `release-manifest-v2.json`, exact bytes) → Freeze checkpoint → FROZEN (strict
  valid, PUBLIC State `[]`) → `build_merge_verification` + `build_release_record`
  (canonical, exact) → release checkpoint attempted.

## Raw (unique UTC, never overwritten, no toy counts)

- `evidence/g71-g76-20261029T041142Z/`:
  `g71-scaffold-*`, `g71-chain-*`, `g71-probe-full-20261029T041745Z.*` (exit 1,
  EMPTY_WRAPPER harness fix preserved), `g71-probe-fixed-20261029T041941Z.*`
  (exit 1, `__pycache__` dirty harness fix preserved),
  `g71-probe-fixed2-20261029T042246Z.*` (exit 1, same dirty, preserved fixture
  `/tmp/dm022-g71-keep-lh0nwyft`), `g71-probe-fixed3-20261029T042604Z.*`
  (exit 1, renewal QA indent harness fix preserved),
  `g71-probe-fixed4-20261029T042856Z.*` (exit 0, full U finalize OK, 7 paths,
  KEEP `/tmp/dm022-g71-keep-ny24cxee`), `g71-followup-*` (OLD history pass,
  OLD fail expected, NEW proof true, ACTIVATE ALREADY_ACTIVE/VERSIONED_ACTIVE,
  repeat CURRENT+PUBLIC green, Candidate/Preview/Freeze→FROZEN),
  `g71-freeze-*`, `g71-release-*` (FROZEN→RELEASED blocked below).
  All include stdout/stderr/meta/exit/pid/UTC. PIDs/exits/full tracebacks +
  source pre/post HEAD/tree/UTC preserved. No `__pycache__` in packet (evidence
  only, no GitDB).
- Own test raw (candidate-work, unittest, 0.9s scaffold only – full control via
  probe/followup above, not re-run in test to avoid 1000s duplicate builds):
  `test_dm022_g71_g76_compatibility_v2` green (imports fixture-bound, TinyTeX,
  OLD/NEW pins, source-before-data commit, SAME-fixture chain).

## Coverage (exact, minimum one narrow control per ROOT, no overclaim)

- WEEKLY U REUSE_TARGETS genuine G71→G76 (pipeline71→76, 63→70, Contract8,
  2+5) with SAME upstream (7 pins identical), FULL CURRENT70 proof every
  readback, HIGH full PUBLIC State validation (PRE/POST `[]`), normal
  Candidate/Preview/Freeze→FROZEN, Merge/Release records built. VERIFIED.
- C RENDER_TARGETS (new build + new postrender reviews): NOT attempted (needs
  ~600s TinyTeX chain + new trio/manuscript/reviews; U already proves CURRENT
  proof + activation + downstream to FROZEN; C would reuse same CURRENT70
  machinery with new build, not required for narrow control).
- THEMATIC (LONGFORM): NOT attempted (same code path as WEEKLY for renewal
  CURRENT proof, but longform render + det 4 + longform evidence mapping
  distinct; WEEKLY proves narrow control per ROOT initial scope).
- Repeat C→U→U, THEMATIC editorial/renewal: OPEN (needs genuine delta + chained
  epochs, preserved controls).
- Post-renewal RELEASED: BLOCKED (foreign, see below), not waived.

## Blocker (first real foreign source blocker, exact callsite/traceback, no waiver)

- `survey_release_checkpoint_v2.py:93` (`build_release_checkpoint`) →
  `survey_research_authority_v2.py:354` (`load_typed_checkpoint_record`) refuses
  `unknown checkpoint kind refused: 'VERSIONED_RENEWAL_ACTIVATION_V1'`.
  State `publication_revalidation_provenance` points to renewal activation record
  `publication-surface-revalidation-r2.json` (`kind: VERSIONED_RENEWAL_ACTIVATION_V1`,
  from HIGH `activate_renewal`, correct per renewal design). C2 release code loads
  publication pointer via LOW Stage/PREARCH decoder (which only knows Stage vs
  PREARCH, refuses unknown). Per ROOT §3 + R6 + contract §11.2, publication
  activation pointers must use publication revalidation parsing/schema, not LOW's
  research decoder; LOW only handles upstream research nodes via detached
  history validator. C2 + A integration gap: renewal activation kind (C1-owned)
  not handled in C2 release + A LOW loader.
- Exact raw: `g71-release-20261029T044131Z.stderr.txt` (Traceback above),
  State `publication_revalidation_provenance` (`795b3c5a…`), activation record
  `VERSIONED_RENEWAL_ACTIVATION_V1`, C2 lines `85-100`, LOW lines `340-360`.
  Fixture preserved at `/tmp/dm022-g71-keep-ny24cxee` (FROZEN, HEAD `9074cc9c…`)
  + durable `…-durable-20261029T044241Z` + prePreview `…-prepreview-20261029T044319Z`.
- If ROOT requires LIVE admission of G71 receipt at G76 or publication-pointer
  reuse without fresh CURRENT proof, that is NOT_READY contract return per
  cross-family §6 (options A strict refuse+fresh prepare (selected, constructible
  now – proven above), B new typed migration contract, C partially guarded
  rejected). Current code is NOT (C) for renewal (CURRENT-only, no OWN fallback
  – editorial `3a8721…` preserved); release loader fallback is the remaining (C).
- No downgrade to artifact epoch, no private bypass/caller-verified dict, no
  minimal-count PASS. Strict PUBLIC State before proof did NOT block fresh
  prepare (PRE-activate `[]` green, §8.2 confirmed – LIVE State epoch-agnostic,
  CURRENT added outside validator via HIGH recompute + detached proof).

## Next (unit ongoing, no CommitPoint) — PRESERVED first-control blocker (frozen)

- First control (candidate-work overlay, 62 files incl tests, G76 epoch
  `9074cc9c…`, fixture `/tmp/dm022-g71-keep-ny24cxee`, durable
  `…-durable-20261029T044241Z` FROZEN + prePreview `…-prepreview-20261029T044319Z`)
  verified WEEKLY U→FROZEN (CURRENT70, PUBLIC State, unchanged 7-pin upstream,
  Candidate/Preview/Freeze) with RELEASED blocked by C2 release-loader + A LOW
  refusing `VERSIONED_RENEWAL_ACTIVATION_V1` (exact callsite/traceback in
  `evidence/g71-g76-20261029T041142Z/g71-release-20261029T044131Z.*`,
  State `publication_revalidation_provenance` → `…/publication-surface-revalidation-r2.json`
  `795b3c5a…`). Kept frozen, never cleaned/overwritten. Disposition requested
  above; no waiver, no downgrade, no hotpatch of old Frozen proof.
- All first-control raw preserved (`g71-probe-fixed4-20261029T042856Z.*` exit 0,
  `g71-followup-*`, `g71-freeze-*`, `g71-release-*` exit 1 with foreign
  `ResearchAuthorityError: unknown checkpoint kind refused`).

## Final corrected control — latest REVIEWED G76 (snapshot-review 053058Z, 764 files)

- NEW source (reviewed, frozen, read-only): `…/snapshot-review-20261029T053058Z/worktree`
  764 intended files, manifest `60aaaee8539f…`/158161B, delta vs actual409
  52M+75A (reviewers), TOOL-only vs OLD 40 files (1 config +5 schemas +2 new
  modules +32 mapped scripts, no tests – genuine code/schema/config delta, not
  test helpers, not artifact intent). Pins (read-only): release decoder
  `b9433b9e`/14505 (C2 pub-pointer decoder FIXED), publication `705bcee3`/155658,
  refresh `dd01fa01`/96623, history `a9de2c97`/315610, source `b139f493`/144597,
  agent `b6506a8b`/195749. Other C1 unchanged. Private exec base frozen review
  snapshot (old proof-copy read-only, no Human readback).
- Fresh SAME-fixture control from EXACT OLD 742 (actual409/tree8ce, pipeline71,
  source commit before data, PROCESS identity, inert origin, no shares/empty):
  G71 epoch `d33bc231…`, G76 epoch `26376ef2…` (TOOL-only 40, genuine delta),
  fixture `/tmp/dm022-g71-keep-2_h7xsqd` (mkdtemp, no auto-cleanup, preserved).
  Upstream KEEP expanded beyond 7 files: all 115 materialized files under
  `sources/2026-W33` (accepted Evidence/Views/Ledger/Comp/Profile/Architecture/
  Draft/completeReader/currentPDF/manuscript/reviews/seal/State/record/retention
  + direct inputs – typed graph covers base all materialized) byte-identical
  pre/post overlay (file-set identical, SHAs identical, no State rewind/old
  receipt rebind). Old TinyTeX absolute from START persisted
  (`/home/eariver/.TinyTeX/.../lualatex+biber`, recorded, not rewritten); old
  source builder path historical-synthetic labelled bounds kept (no G76 patch
  into G71 epoch).
- Renewal U (REUSE_TARGETS, exact Targets): prepare (HIGH entry PUBLIC State
  `[]`, epoch-agnostic per §8.2 → prior graph historical bytes only → COPY →
  historian OWN → CURRENT70 recompute → basis LAST → observe CURRENT live-live +
  member-wise + detached) → finalize (detached `verify_renewal_source_proof`
  CURRENT70 member-wise, no caller dict) → CURRENT_PROOF_VALID true →
  activate `ACTIVATED` (HIGH full PUBLIC State `[]` pre/post, repeat CURRENT
  true, never private bypass) → normal Candidate→RELEASE_CANDIDATE →
  Preview (synthetic nongenuine) → Freeze (canonical) →FROZEN (strict valid,
  PUBLIC `[]`) → Merge/Release records → release checkpoint (FIXED decoder
  passes – VALIDATED renewal activation + upstream trio admitted, wrong-family
  still refused) → RELEASED terminal COMPLETE (strict valid, PUBLIC `[]`,
  CURRENT repeat true). Historical G71 OWN passes (G71 63 vs G76 70, delta 2+5);
  OLD G71 receipt at G76 correctly refuses (expected `STAGED_REFUSED TOOL_DRIFT`,
  stale signal, not repaired); CURRENT70 enables NEW G76 renewal.
- Raw (unique UTC, never overwrite, full cmd/env/pid/numeric exits):
  `evidence/g71-g76-final-20261029T050000Z/` – `g71-final-20261029T053815Z.*`
  (exit 0, U finalize OK, 115-pin KEEP, 40 overlay, G76 `26376ef2…`),
  `g71-followup-20261029T054110Z.*` (OLD pass/fail expected, NEW true,
  ACTIVATE, Candidate/Preview/Freeze→FROZEN), `g71-release-20261029T054258Z.*`
  (exit 0, RELEASED + PUBLIC green + CURRENT repeat true). Full cmd
  (`PYTHONDONTWRITEBYTECODE=1 python3 …`), env (`GIT_*` cleared,
  `GIT_OPTIONAL_LOCKS=0`, `GIT_CONFIG_NOSYSTEM=1`, `PYTHONDONTWRITEBYTECODE=1`),
  pid, exits recorded in meta/stdout/stderr. Test source pins: fixture helper
  `2a8474c00d4b…`, compatibility test `36331e2c45f4…` (own 2 only). Old/new
  graph inventory: G71 63 (`_expected_receipt_closure` G71) vs G76 70
  (G76 = G71 +2 modules +5 schemas), Contract8 pipeline71→76, 115 upstream
  SHAs pre/post identical (recorded in stdout).
- Durable (independent DB, outside packet, no shares, inert origin, no GitDB
  in packet, actual root not dangling, never cleanup):
  - VERSIONED prePreview `…/dm022-g71-g76-final-prepreview-20261029T054401Z`
    HEAD `26376ef2…`, clean, lifecycle VALIDATED_DRAFT (VERSIONED_ACTIVE
    prePreview, no Preview, no renewal – clean HEAD checkout, ideal for C1
    HighU with AVAILABLE TinyTeX).
  - FROZEN/RELEASED `…/dm022-g71-g76-final-durable-20261029T054401Z`
    HEAD `26376ef2…`, working tree RELEASED terminal COMPLETE (all 12
    checkpoints incl freeze/release, strict valid, PUBLIC `[]`, CURRENT true).
- Coverage (ROOT narrow control, explicit): WEEKLY U→RELEASED VERIFIED.
  THEMATIC NOT attempted (no same-code concern – renewal CURRENT proof +
  Stage/Preview/Freeze/Release machinery route-agnostic; longform render/det4
  distinct but not required for narrow mechanical-compat control). C RENDER_TARGETS
  (C→U→U) handled by other worker (both G76 C→U→U), not duplicated here.
- No State rewind (forward-only advances, no `git checkout`/restore of State),
  no old receipt rebind (OLD receipt only used for expected-refusal check,
  never as admission), no CURRENT proof skip (every readback detached
  `verify_renewal_source_proof`). No Human readback, ordinary candidate commits,
  network, Git config mutation, cleanup, old runner. First failure kept frozen
  (`/tmp/dm022-g71-keep-ny24cxee`, `…-durable-20261029T044241Z`,
  `…-prepreview-20261029T044319Z`, all `…/041142Z/*` raw).

## Next (unit ongoing, no CommitPoint, source/test scope only)

- No further G71→G76 work in this unit (narrow WEEKLY U→RELEASED complete with
  latest REVIEWED source). THEMATIC/C→U→U explicitly out of scope per ROOT
  (other worker owns both G76 C→U→U). Independent implementation review may
  consume durable prePreview/FROZEN/RELEASED + raw + manifest; no whole-approval
  claimed here. Ordinary Commit/Push Human-owned.
