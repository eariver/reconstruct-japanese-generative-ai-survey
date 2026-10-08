# DM003-W1 — shared approved-Preview agreement bounded completion

**Successor update 2026-10-07:** [DM-004 at409b292](rephase-1-dm004-assessment.md) bounded repairs the agent validation CLI/local closure prerequisite with new21-method evidence and independent review. This does not backfill W1's missing command/guard transcripts. Current next unit is LONGFORM_SPECIAL direct-source/supporting-surface contract analysis after the DM004 Commit Point; W1/DM004 tasks below remain historical.

Recorded **2026-10-05T00:43:16+09:00** (Astra clock). Started after Human Push at clean reconstruct **a375eb9c1213b89f66cd5449cca8126fd1c60b7c**, local tracking synchronized without fetch. **Local DM003-W1 is bounded repaired at e1705b7. Stop at this Human Commit Point.** Production baseline **774dd39a951c9ac3818e83dfffd4c7666efb0a20** is unchanged. Whole candidate **NOT_READY**, step4/B3 OPEN, canonical seven-point audit unstarted.

## 1. Scope and exact identity

| Field | Current value |
|---|---|
| Successor HEAD | **e1705b7fed01369767ab9d827c0360117d54aa1f** |
| Tree | **3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557** |
| Direct parent | **222a37e9ee2aa96724a491f2c04c2583a86b9650** |
| Source DB / branch | `/tmp/opencode/jgas-dm003w1-impl-20261004T072423Z` / `codex/dm003w1-preview-agreement` |
| Independently restored DB / branch | `/tmp/opencode/jgas-dm003w1-restore-20261004T073938Z/candidate-partial-b40de60` / `dm003w1-final` |
| Runtime | `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python`, pinned3.12.14 |

Both available DBs are at **actual HEAD e1705b7**, clean. Available chain is e170→222→ff6c67f→490414c→b40de60→real774dd39a, shallow only at774. Original and restored222 inputs remain clean and unchanged. Root independently read actual successor/restore identity, full three-path delta and the new pack hash; General performed implementation/tests/restoration.

[Packet entry](../notes/rephase-1-dm003-w1-implementation/README.md), [machine manifest](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/implementation-manifest.json), mandatory [later binding supplement](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/final-binding-supplement.json) and [evidence qualification](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/evidence-qualification.md).

| Changed path (all100644) | Final Git blob |
|---|---|
| `scripts/survey_agent_control_v2.py` | `d58db79b8ce43a2cb55814a38ff7542ff556f86a` |
| `tests/test_survey_dm003_w1_preview_agreement_v2.py` | `0eb328b1a1ac9d41302e3a229836a3d9273c6bbd` |
| `tests/test_survey_dm001_019_freeze_equivalence_v2.py` | `25a7881e573b91e58a9f68f92e8cb3ee77335d9f` |

One normal independent-DB commit, three paths, +331/−1; only **four new runtime lines**. The existing test edit is the authorized single W4 error-oracle update plus explanatory comment. No wrapper/stage/schema/config/workflow change; no generic checkpoint discovery or new authority.

## 2. Repair and preserved invariants

Parent [DM-003 witness S3](rephase-1-dm003-assessment.md) proved canonical checkpoint approval A1 + Human-side A2 (same Candidate) passed State validation and let the wrapper write an A2-bound pair, then failed the stage equality backstop. That original evidence remains unchanged; it was not rerun or re-labelled as repaired behavior.

The successor adds agreement checking inside the existing passed-Preview/checkpoint-authority-dict branch of `_validate_agent_state`:

```python
if state.get("human_gates", {}).get("publication_preview") == "approved":
    human = state.get("human_gate_provenance", {}).get("publication_preview")
    if human != authority:
        errors.append("Human Preview and checkpoint approval authorities disagree")
```

The State schema already ensures a non-null authority has exactly path/SHA fields. Thus approved Human null, different path, or different SHA fail the new agreement invariant when checkpoint authority is present. A missing/non-dict checkpoint still fails the existing lacks-provenance path; it does not need the new branch to fail closed. Existing passed-status, canonical path, actual file SHA and typed-approval checks remain necessary even when both refs agree.

The real wrapper reaches this shared validator through `_safe_state_profile` before choosing an approval or writing outputs. The later stage equality guard is retained as a backstop. Healthy pending State remains valid; an inert approval file is not an active approval. This is **not** a new validator for every possible pending Human-reference corruption, nor a change to the narrower `_pending_conditions` revalidation contract.

The runtime edit repairs the measured pre-write boundary without adding a reviewer, duplicate wrapper policy or filesystem resolver. Earlier DM-001/019 Freeze construction/source/Profile/PDF checks retain their own bounded conclusions; their old56 tests are not transferred wholesale to this new HEAD.

## 3. Fresh verification and actual oracle scope

General's [implementation task](../notes/rephase-1-dm003-w1-implementation/implementation-task.md) corrected the initial design's pending-State assumptions and authorized only the narrow guard plus its tests. Root read the entire new test module, the runtime diff and the existing oracle change.

**Final results:24 successful methods, no failures/errors/skips** (6 new +16 affected +2 selected DM001/019):

| Evidence | Methods | Scope |
|---|---:|---|
| [run-06 new module](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/run-06-final-newmod.log) | 6 | S3 split rejected by real State and actual wrapper before outputs; null/path-only/hash-only cases; equal-stale/noncanonical/malformed refs still refused; healthy Special→FROZEN and Weekly Freeze; healthy pending/inert-file control |
| [run-07 affected](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/run-07-final-affected-16.log) | 16 | Agent controller5 + local stage3 + Freeze boundary8, including existing revalidation/pending/typed authority paths |
| [run-08 selected DM001/019](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/run-08-final-dm001-selected.log) | 2 | W4 negative/no-write oracle at the earlier shared gate; actual extracted workflow Python authority predicate on the existing synthetic controls |

The six-method count includes internal subcases, not six total scenarios or an inflated count of assertions. New S3 uses separately authored, individually valid A1/A2 records for the same C1; it checks actual wrapper refusal, stable State bytes, no outputs and an empty full regular-file inventory diff under the two fixture roots. The Special healthy control checks exactly two additions with no other inventory changes; the Weekly healthy test checks the expected two additions and manifest validity, **not a full removed/modified-file oracle**. Other negatives have their narrower State/output assertions. No global/continuous filesystem no-write claim.

Tests use real validators and wrapper, synthetic records/PDF/Human labels, no authority-success mocks in the new regressions. This is not real editorial/visual/Human acceptance, full upstream pipeline execution, full Retrospective support or a live Release workflow. Reused affected tests retain their individual fixture limits. No full56/R1/Weekly rerun was selected.

**Failures retained:** run-01's pending-fixture setup attempted an inert approval before a Candidate existed; the fixture was corrected to the RC-advanced Weekly pattern without weakening validators. Run-04 exposed the anticipated earlier error location for a Human-only SHA drift: shared disagreement now precedes the wrapper's old `approval authority drift` error. The narrowly authorized existing assertion was updated; no-write assertions stayed. Both failures remain historical evidence, not clean-first-run claims.

### Binding and preservation qualification

General reports running fresh asserted guard scripts before/after each run, but those command/guard outputs were **tool-observed only and not persisted**. Run-02..08 contain unittest output, without durable literal argv/cwd/runtime/env/exit headers or guard transcripts. The guard sources are retained and final live identity/source hashes independently corroborated, but that does **not** manufacture per-run raw binding. Run-01 is a contemporaneous notes header plus transcribed stream subset/full traceback, not a byte-exact complete redirect capture.

The missing capture is a deviation from the requested evidence discipline. Astra and the independent reviewer accept bounded source/oracle/result binding for this small unit with that limitation; no cosmetic green rerun was used to conceal it. The later read-only `final-binding-observation.raw` is explicitly a **new observation**, not historical command reconstruction. Future runners need unique saved pre/test/post transcripts and actual exits; do not reuse these fixed-path scripts blindly.

## 4. Exact portable successor and restoration

Three preserved inputs support the available exact chain:

| Input | Bytes | SHA256 |
|---|---:|---|
| b40 partial archive in candidate-recovery packet | 5,152,199 | `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c` |
| DM001/019 final20-object pack | 46,164 | `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99` |
| [W1 222→e170 pack](../notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack) | **57,856** | **`97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9`** |

The W1 pack has **7 actual objects:1 commit/3 trees/3 blobs**. Restored actual HEAD/tree/parent/clean status, all three file mode/blob/byte identities, seven-object availability, shallow cutoff and the whole available six-commit chain were verified. The later binding observes zero object-file inode intersection between impl/restored stores, no alternates and inert remotes; both222 inputs stay untouched. This is not a dangling final-ref-only checkout.

The extraction/import commands were tool-observed but no full restore-script capture was saved. `run-09` preserves a limited post-checkout record; its nonverbose pack-verification sections are empty. Actual restored objects plus manifests and the new independent read-only observations support the **final artifact result**, not certification of a reusable restoration script or replay of all acquisition steps. Any future restore must freshly hash-gate all3 inputs, safely extract to an absent independent destination, import packs, switch actual HEAD, and verify clean chain/objects/bytes/inode separation. Do not execute old unsafe restore scripts.

Inherited26,309 missing blobs, baseline-shallow history and unbundled pinned runtime remain. There is no all-history/all-assets backup or production adoption claim.

## 5. Review conclusion and next bounded unit

[Independent implementation review](../notes/rephase-1-dm003-w1-implementation/independent-implementation-review.md) and mandatory [evidence resolution/wording clarification](../notes/rephase-1-dm003-w1-implementation/independent-evidence-resolution.md) returned **BOUNDED_PASS for DM003-W1 only**, no remaining blocker. They qualify missing guard/restore-command raw, the original README's misleading “no shipping change” phrase, and narrow the pending/Weekly/absent-checkpoint claims. The isolated candidate **did** change; Production and its fixed baseline did not.

**Astra disposition: local DM003-W1 bounded repaired at e1705b7.** The DM-003 omitted-pointer nonblocker disposition remains; no generic provenance-completeness closure or upstream CV2-DM status change. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. Ordinary reconstruct Commit/Pull/Push remains Human-owned. **Stop here.**

### Next General task after Human continuation

Select the separate **DM-004 Release workflow command/State-validation contract** prerequisite at fixede170. The saved Summary/source disposition identifies a nonexistent `survey_agent_control_v2.py validate-state` invocation after release/checkpoint work. Now that the selected Freeze admission/pre-write boundary is locally repaired, clarify this remaining ordinary-path closure failure before claiming a usable end-to-end application; its priority is the publication closure boundary, not merely the short apparent diff.

General's first internal return should compare the exact current workflow call with the actual CLI parser and shared State-validation contract, including expected post-checkpoint lifecycle, argument order, errors and exit behavior. Propose the smallest correction and offline positive/invalid-State/command-failure oracles that **retain necessary validation**; do not merely delete the failing command or replace validation with an always-successful status print. Astra selects concrete paths/contract before code; implementation/tests and fresh independent review then stay in that bounded unit. Use isolated synthetic release-record/State fixtures and extracted local workflow logic; **no workflow dispatch, network/public Release recreation, provenance PR or Production State mutation**.

No new DM-004 analysis/execution has started in this closeout. Reuse captured Summary, fixed source and existing portable candidate; no recovery/old-suite rerun. Special/support/DM-016/017, build transfer, rendered/semantic sufficiency, broader application verification and final audit retain separate dispositions.
