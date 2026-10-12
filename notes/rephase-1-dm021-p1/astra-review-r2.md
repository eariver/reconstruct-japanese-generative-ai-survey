# DM021-P1 correction re-review — remaining source gaps

2026-10-12 JST. Preserve correction36-test packet and its independent qualified PASS. Root inspected actual module9f3aea25: the following R1/R4 requirements are still not implemented despite “complete” wording. No extra path/scope is selected.

## C1 — transitive authority graph still stops at receipt roots

`_build_graph:528–841` adds receipt.accepted_refs and authored_refs, but contains NO collector for actual accepted Evidence package/tasks, screening acceptance/package/tasks/results, edition-view acceptance/package/results, profile completeness or candidate selection; it also omits upstream State-bound checkpoint wrapper nodes. Prefix names alone do not create these nodes. These required local dependencies are consumed by existing validators, and the selected frozen digest/retention graph explicitly includes their authority. Root R1 was not closed by iterating the existing receipt refs.

Implement a finite typed traversal of the actual State/checkpoint + accepted-record schemas, using existing validators and explicit known fields/implicit sibling paths. Include exact current local dependencies with source SHA verification and role union. Checkpoint wrapper/history metadata stays operational KEEP, not frozen digest; immutable research/source/approval dependencies enter frozen digest. Historical recorded State SHA and old superseded artifact SHAs remain provenance, NOT current live-file expectations. No generic “any path-looking string” recursion, no URLs opened, no fake staged State.

Add an independent expected-path oracle using the REAL fixture's known screening/views/completeness/selection/Evidence package+task+card paths, not just `receipt.accepted_refs` as both implementation and oracle. Prove each is in the graph/retention with proper policy and each actual frozen research dependency contributes to the digest; State/checkpoint wrappers/QA/tool/pub data stay excluded. If a necessary schema relation cannot be derived without new authority, stop with the exact gap instead of omitting it.

## C2 — exact profile binding cannot be a no-op

At738–742, bundle-profile mismatch executes `pass` although the comment says refusal. This violates the chosen exact current-profile relationship; “no false acceptance in current fixtures” is not a source guarantee. Require exact path+SHA equality to State-bound Profile (and consistent selected manuscript Profile/Architecture/typed approval), with a controlled `BUNDLE_PROFILE_DIVERGED` or equivalent. Add a same-issue valid alternate/same-byte alternate-path profile negative through an actual valid fixture/bundle setup, not a broad unrelated hash failure. Preserve other source/PDF/Candidate cross-bindings.

## C3 — final all-control predicate is still only a comment

`validate_proposal:1391–1399` recomputes `contract_identity` only. That does NOT re-run receipt/current-tool ancestry/dirty/untracked/all-control-root checks, and registered contract files are not every scripts/schema control path. `_Collector.reverify` pins directly consumed files + HEAD/config only. A dirty unlisted helper or the new proposal module/schema can drift during the scope loader yet return REVIEW_BOUND_PROPOSAL.

Re-run the ACTUAL full generated-receipt/current-tool predicate before return in both entry points, after scope/schema work, and recheck the known file/dir snapshots afterward. No pending bypass. Add a late-scope and late-prepare seam modifying a tracked helper under scripts outside CURRENT_CLOSURE (or a new P1 control file), leaving HEAD/config/14 closure bytes unchanged; it must refuse. A contract-only equality test is insufficient. Preserve legitimate artifact-only commit positive behavior.

## C4 — don't walk unvalidated profile-selected directories

Public entries currently call `_tree_map` from preview Profile contents before `_pipeline`'s strict State/eligibility/authority checks. Validate and bind State/Profile first, then inspect only the validated roots. Add an invalid/unbound Profile-path case proving no unvalidated broad tree read occurs. A call-observation spy may prove the walker wasn't invoked; never mock authority success. Normalize root once across the API. Remove dead no-op loops/duplicate checks while touching those exact sections only.

## Evidence / follow-up

Keep corrected 3A1M budget; no controller/receipt/writer/reason changes. Complete13path patch must be generated without transient `git add -N` in the active candidate index (earlier generator did this and reset it; disclose as an avoidable mutation, not “untouched”). Generate in an independent copy or use no-index new-file diffs. Apply the exact saved patch to another independent actual409 baseline and verify13 bytes/modes/status/base/isolation. Preserve all old scripts/logs, no empty commits/network.

Fresh focused P1 tests + actual affected controls at final pins, no old36 transfer. Same independent reviewer must explicitly revisit graph-complete/profile-no-op/control-recheck PASS claims against actual code and concrete expected-set oracles. Return exact source/evidence or blocker; wholeNOT_READY/DM021OPEN remains.
