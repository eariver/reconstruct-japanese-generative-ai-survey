# DM021-P2V — retained-aware current-basis observer assessment

**Successor design 2026-10-17 JST:** §4's materialization/admission/promotion analysis is complete as [P3S staged-source selection](rephase-1-dm021-staged-source-contract-decision.md), with [independent design review / mandatory Astra S1–S5](../notes/rephase-1-dm021-materialization/README.md). P2V source/scoped13+1/fullpatchdc5ae07b unchanged. Next is P3S concrete interface/dependency/fixture return before separate implementation; full live promotion remains unselected and DM021 OPEN. Prior P2V closeout was committed/pushed5595d21 by Astra on Human's explicit request; this successor design has its own Commit Point.

2026-10-16 JST. **BOUNDED COMPLETE** for the selected read-only component under [contract2ea1d98f](rephase-1-dm021-current-authority-contract-decision.md), with mandatory [Astra closeout resolution](../notes/rephase-1-dm021-p2v/astra-closeout-resolution.md) and [independent final resolution](../notes/rephase-1-dm021-p2v/source-correction/independent-final-resolution.md). **Scoped13+1 evidence, not a full14-method run.** Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Stop at Human Commit Point.

Started at Human `b385deb69f5472377737ea2a4138b2d20b119dec`, clean/local tracking synchronized without fetch. General authored initial interface/code, then bounded A source/test and B tooling corrections; Astra reviewed actual code/oracles/drafts/raw and selected execution; author-independent implementation review required the isolated State oracle and resolved its test-only addition. Worker results, root judgment, independent review and Human publication authority remain distinct.

## 1. Implemented scope

`observe_current_authority(root,state_path,proposal_path,manifest_path,scope_review_path=None)` checks:

1. Actual strict canonical current State/Profile/eligibility, raw State byte equality, original checkpoint/current active-before, full current receipt/Gate/control/upstream predicates and rederived proposal/reader/graph/plan.
2. Actual P2R verification of the same pinned proposal/manifest, complete retained COPY/KEEP/staged bindings and exact inventory.
3. Within-call original pins, schemas/source dependencies, HEAD and control/edition/retained inventories, with checked closes before observation returns.

P1 data-only factoring preserves its public prepare/validate result shape, complete comparisons, destination-absence completion, optional scope and final full receipt/snapshot checks. The new observer always completes current+retained validation, never accepts a caller mode/skip/verified token. Live planner pins remain separate from retained/full-tree snapshots. Optional existing scope yields `CURRENT_BASIS_OBSERVED_NEEDS_SCOPE` or `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`, with exact State/proposal/manifest/review refs, observed HEAD, measured digests/counts and input hashes. A valid scope may be created after capture outside retained/. Invalid supplied review refuses.

This is no writer, reason enum, State adoption, semantic approval, creator/anti-rollback attestation or bearer permission for later mutation. There is no proposal-time whole-edition inventory claim, no pending-basis bypass or retained-old-State substitution. P2R remains unchanged and persistence-positive does not imply current-basis-positive. Full promotion and staged reviewed-path integration remain unselected.

## 2. Exact source / preservation

Selected2A1M /0schema relative to P2R:

| Path | SHA256 | Bytes |
|---|---|---:|
| M `scripts/survey_editorial_correction_proposal_v2.py` | `cdd69fe7c24de6dda9ee503cfcfbc791a9d7e421141dbb23586f1e4431c27eab` | 113535 |
| A `scripts/survey_editorial_current_authority_v2.py` | `79a3396cf07d85cfeb11df9f85910ba8aed2ed63f965713edab5b076d580d3f4` | 37896 |
| A `tests/test_survey_editorial_current_authority_v2.py` | `c567715dfb4ffa04e7d70dfcf42072cf194d0d9239c2e5b664f7098eaa62009f` | 74061 |

All physical0664/logicalGit100644. Inherited15 of P2R's16 unchanged, including all P2R source/schema/tests and proposal/review schemas. No config/controller/receipt/Gate/publisher/CLI changes.

- Active `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`.
- Current final saved-patch apply copy `/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/TB1proof-clean409-copy` (now patch-applied, not clean despite its name).
- Actual detached HEAD **409b292756dd1277b9dfae87679934c0d2ce251c**, tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**, plus **18 uncommitted paths3M15A**. HEAD alone excludes the overlays. No candidate commit/branch; no staged/intent delta observed (not literally an empty tracked-file index).
- Active preserves84 preknown caches; final full3 and B1 target guards bind full102 status rows, source18/cache84 hashes/modes/sizes, HEAD/tree/index, checked child/wrapper exits. Fresh absent cache prefixes/disabled writes avoid in-tree cache execution; no cleanup to pass final guards.
- Final manifest: [v5 expected18](../notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json).
- Complete18 patch [TB1 GEN packet](../notes/rephase-1-dm021-p2v/source-correction/evidence-20261016TB1-gen/), **948373B**, SHA256 **dc5ae07b4acb19da2c1d56856f055dd4050530c23286cc0f45c1ae4dcc5ef514**. Saved-patch [TB1 proof](../notes/rephase-1-dm021-p2v/source-correction/evidence-20261016TB1-proof/) applies directly to independent clean actual409 and matches all18 pins/modes/status. It already includes P1/LF2I/LF1/P2R.

Five disposable independent worktrees and two temp indexes were relocated out of the notes packet to avoid embedded gitlinks; [mapping/current observations](../notes/rephase-1-dm021-p2v/source-correction/relocation-record.md) preserves before/after content identity and historical raw paths. Active and P2R original/proof copies remain preserved. Check availability before reuse. If lost, use the [four portable409 inputs](../notes/rephase-1-dm021-contract/availability-at-closeout.md) with a new fail-closed restore, then full18patch DIRECTLY to clean409; no layered older overlays, old-script rerun, fake-root history or network refresh. Partial/shallow DB/missing26309blobs/unbundled runtime remain, not full-history backup.

## 3. Verification and bounds

- Full3: **13/13 successful /5523.310s /no skips /child0+wrapper0**, P1cdd69/observer79a339/testd3224797. Two probes plus11 behavioral methods; smoke2 positives were later included, not added distinct coverage.
- Independent B1: **1/1 /492.646s /child0+wrapper0**, final testc567715d, same runtime modules. Exact additive diff and old13/helper body hashes establish prior13/setup unchanged; **no full14 run claimed**. New file has14 methods (2 probes+12 behavioral),1236 lines. Targeted-only scope was explicitly selected by root and accepted independently.
- B1 isolates a raw State whitespace change: parsed JSON and strict State validation remain healthy, State is COPY not KEEP, P2R verifies persistence, P2V refuses exact BASIS_MISMATCH with immediate no-write; restore succeeds. Same-byte unreferenced State clone refuses canonical-path selection while canonical State with clone present remains valid.
- Real synthetic Longform prose, Weekly envelope, real R1 non-emitted-code refresh owner, ordinary/valid-after-capture/invalid scope, P1 baseline/post-capture absence, mutable-vs-KEEP drift, real control changes/artifact-only HEAD, retained missing/extra/empty dirs, aliases/FIFO no-read, cross-helper additions/drift and close-fault/primary preservation are exercised. These are mechanics, not genuine semantic/visual/Human approvals or publication acceptance.

Mandatory qualifications: preempted R1-stale REF_DRIFT and scope/schema/loader refusal codes do not prove later intended codes; some assertions allow bounded code families. Close tests are coupled to counted internal close boundaries. No isolated schema-switch or optimized-mode run. Initial scaffolding and false guard/oracle claims were rejected before execution and remain visible. Smoke1 failed; full1 was POST-less/orphan after wrapper timeout; full2 failed11/13 with **exit1**, correcting its report typo. Full3 and B1 supply the scoped green evidence. No P1-36/P2R-25 or old-run PASS transfer.

GEN relative-path failure, original proof SyntaxError/missing-main no-op, and wrong-source proof refusal are distinct setup faults. The wrong-source refusal raw was deleted with a reused outdir and is lost, not preserved/reconstructed; new TB1 proof used unique paths. Earlier inode sampling/bytecode-prefix observations are qualified; final proof verifies actual available content/separation. Scripts are exact-run evidence, not certified universal rerunners. Snapshot equality is not continuous no-drift/global CAS/crash atomicity. See mandatory root/independent resolutions for the precise scope rather than report summaries alone.

## 4. Next bounded unit after Human continuation

**General: changed-reader materialization/admission/promotion contract analysis BEFORE code**, on current18 source with P1/P2R/P2V contracts and saved intakeafdb3df3. Reuse available fixed source, no old-suite/restoration/intake refresh by default. Return a concrete minimal contract to Astra covering:

1. Immutable reviewed proposed-reader/scope paths through generated corrected source, receipt/Gate/build/QA and normal Candidate/Preview; compare explicit versioned-target bindings with genuine new live-path review costs, never rebind by equal SHA or assume a second semantic review is free/default.
2. A real writer's fresh preflight and bounded input/ownership/write/failure/retry boundaries: P2V's observation is not a reusable write token. Separate staged-only materialization from live replacement/adoption alternatives and show the exact caller/validator path for each.
3. Truthful correction reason/record and original-checkpoint/active-before/new-after State bindings, preserving accepted upstream, retained history, existing independent reviews and normal Human Architecture/Preview/Freeze/Release. Resolve the healthy-State/canonical-path replay cycle rather than invent a former State or public bypass.
4. Exact minimal path/API/schema/test budget, meaningful Longform/Weekly/R1 oracles, cost/benefit and a coherent next implementation boundary or precise blocker. Full promotion remains unselected until that decision; no automatic enum/State/CLI/publisher change, production-owned fixture prerequisite or new Human role/Gate.

Stop at current Human Commit Point. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Ordinary reconstruct Commit/Push and any candidate-commit authorization remain Human-owned.
