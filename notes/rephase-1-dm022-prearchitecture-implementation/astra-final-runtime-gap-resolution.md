# Astra final runtime gap resolution — required corrections, no waiver

2026-10-29. Both-route corrected-research→editorial→C→U→U→RELEASED and the genuine Weekly G71→G76→RELEASED control have successful raw evidence on the reviewed runtime. That does not waive the remaining mapped failure/regression conditions.

## 1. Prepublish readiness is required

The late-guard author found entry-only paths. Root directly read current `survey_agent_control_v2.py:2227–2486`: `build_stage_checkpoint`, `advance_with_checkpoint`, `approve_architecture` each have only an entry READY; their final `core.write_json` sites have no immediate readiness check. `approve_publication_preview` delegates its approval-file write to a guarded builder but later writes State without its own final check. These are **source defects**, not merely optional test coverage. Earlier independent “all mutators entry+prepublish CLOSED” wording is superseded for these paths pending correction and fresh resolution.

B must recheck full passive readiness immediately before each mapped canonical checkpoint/approval/State/review/presentation/invalidation write, including human-gate and bridge dispatch where they themselves write. Preserve detached validators as guard-free. A wrapper whose actual mutation is delegated may rely on the child's checked write boundary only when that exact call path is identified and tested; one grep hit in a wrapper is not proof of both phases. No caller-owned-guard exception, generic permission token, or weakening of strict State/approval predicates.

Extend late-seam tests with real positive counterparts, actual post-entry guard/completion injection before the final READY call, and immediate preservation assertions allowing only already completed prefix writes. Cover the remaining Evidence/Draft/retention/editorial/Release families as well. An invalid proposal or pre-existing retained root that rejects before the target seam is a setup issue, not the intended negative. Do not mark skipped cases as passed.

## 2. Finish affected fixture adaptations

DM001/019, local DM003-W1, DM004 and Weekly-refresh regressions remain red because their older fixture builders lack the now-required Profile-bound State or omit inherited/new untracked source files. Apply the already selected fixture-only adaptation: existing State constructor, explicitly synthetic initial context, complete finite source-copy inventories, source commit before authority. Do not make absent State legal in runtime. Keep old negative oracles and actual workflow predicates; fix setup to reach those predicates. No “bounded HighU closeout” stopping point may discard these required regressions.

## 3. Evidence and visual corrections

The saved A21 raw (`A4-path-normalization-20261028T164439Z/dm022-a4-full-20261028.txt`) contains21 `ok`, `Ran21`, `OK`, no skipped result. A conditional root-user skip in the source is not an observed skip in that run. Independent review must append that correction. Its incidental `fab1ee` observation has no saved raw; do not use it as a Human-commit readback or redo that readback.

The independent visual reviewer actually inspected six initial/editorial PDFs (30 pages), **not the C PDFs**. Locate and preserve the actual final C build outputs and their exact manuscript/reader/review/source/log bindings from the successful final runs. Do not substitute another editorial PDF for C or rebuild and call it the reviewed byte identity. If those outputs were not retained, record the loss and execute a new source-bound C witness with retention; only the new outputs may receive the new visual verdict. U exact-target reuse requires no duplicate inspection when exact path/SHA identity is proved.

New runtime guard corrections require a fresh source freeze, affected successful lifecycle confirmation and independent supplemental resolution. Test-only fixes afterward require their own exact source/run binding. No old overall PASS transfer, no global atomicity claim, no ordinary Commit/Push or requested Human-commit readback.
