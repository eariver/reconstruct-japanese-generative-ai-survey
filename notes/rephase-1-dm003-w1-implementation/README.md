# DM003-W1 — bounded shared-State repair complete

Read [Astra assessment/current next task](../../outputs/rephase-1-dm003-w1-assessment.md). **Local W1 bounded repaired at e1705b7; stop at Human Commit Point.** Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. Production baseline774dd39a unchanged.

## Current candidate

- HEAD **e1705b7fed01369767ab9d827c0360117d54aa1f**, tree **3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557**, direct parent222a37e9ee2aa96724a491f2c04c2583a86b9650.
- Implementation `/tmp/opencode/jgas-dm003w1-impl-20261004T072423Z`, branch `codex/dm003w1-preview-agreement`; independent restore `/tmp/opencode/jgas-dm003w1-restore-20261004T073938Z/candidate-partial-b40de60`, branch `dm003w1-final`. Both actual final HEAD and clean; original222 DBs preserved.
- Four runtime lines in `_validate_agent_state`, one new focused test module and one authorized existing W4 assertion update. Stage backstop, wrapper, schemas/config/workflow unchanged. Approved refs must agree; existing canonical/hash/typed checks remain. Normal pending State is valid and an inert file does not approve it.

## Evidence order

1. [Initial design](design.md) → [Astra selection/implementation task](implementation-task.md), which corrects pending-State assumptions and defines the exact scope.
2. `evidence-20261004T072423Z/`: original report/manifest, test logs, guard/generator source, patch+pack. Final `run-06/07/08` = **6 new +16 affected +2 selected =24 successful methods**, no skips. Initial pending-fixture error and predicted old-oracle failure retained.
3. **Mandatory [evidence qualification](evidence-20261004T072423Z/evidence-qualification.md)**: guard invocations/argv/env were tool-observed, not saved alongside the unittest-only logs; run-01 is a transcribed subset; restore command script not captured. Do not claim durable per-run raw guard binding or infer no source changed from the original README phrase.
4. [Later machine binding](evidence-20261004T072423Z/final-binding-supplement.json) + [labelled new read-only observation](evidence-20261004T072423Z/final-binding-observation.raw): actual HEAD/tree/chain, all3 bytes/modes/blobs,7 objects, no-sharing/inert/remotes, untouched222 inputs. Not retroactive test guard proof.
5. [Independent implementation review](independent-implementation-review.md) and [evidence resolution with wording clarification](independent-evidence-resolution.md): W1-only BOUNDED_PASS, no blocker, explicit evidence/fixture/history limits.

## Portable inputs

Parent b40 archive (`faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`, 5,152,199B) + DM001/019 final20-object pack (`2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99`, 46,164B) + [W1 pack](evidence-20261004T072423Z/w1-222-to-e1705b7.pack) (**`97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9`**, **57,856B**,1 commit/3 trees/3 blobs). The exact available chain e170→222→ff→490→b40→774 is restored; shallow only at774, inherited26,309 missing blobs and runtime-not-bundled remain.

Saved scripts are historical evidence, not certified rerun instructions. Future restore uses a new absent directory, all3 hash gates, safe extraction/import, actual HEAD switch and clean/object/byte/inode verification. No patch-rebuilt identity or fixture objects in reconstruct's DB.

Next after Human continuation: **DM-004 exact workflow/CLI/State-validation contract**, short concrete General return before code, then selected isolated correction/tests/review. Preserve validation; no live Actions/Release or Production operations. DM-003 generic discovery remains unselected. Ordinary reconstruct Commit/Push is Human-owned.
