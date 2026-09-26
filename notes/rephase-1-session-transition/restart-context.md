# Restart context and recovery

2026-09-21 JST. This is the minimum operational context not safely inferred from a fresh chat. No implementation or test was run during session-transition preparation.

Continuation note (2026-09-22 JST): the preparation statements below are historical. Increment A is now complete at `1a9649129d1745fed0b98db46ef15f014407e6fc`, tree `5e933aa54034ed227216252a2c8707a59f293acf`, parent f1, in independent Ubuntu fixture `/tmp/jgas-rephase-increment-a-sol-copy`. See [current handoff](../../handoff/rephase-1-continuation.md) and [A packet](../rephase-1-increment-a/README.md) for current work; do not redispatch A from the old pending-decision paragraph. The A packet contains exact commit metadata, f1 delta/full baseline patch and changed-file copies for independent recovery if `/tmp` is lost. Verify the actual recovered identity/tree and obtain affected fresh review; do not assume content recovery recreates the reviewed commit. The full-patch temporary-index diagnostic is explicitly not clean application proof. All isolation, fixed-baseline and no-overwrite rules below remain applicable.

Continuation note (2026-09-27 JST): Increment B is complete within its selected Weekly scope at `c04f32ad46109403e8a63faaa8394a90ee6b869c`, tree `7dbcbbdb499ea6c7d33417a16144107320e1fd06`, parent `cb96ab97045b0d0767f38806809d33e383bac73d`, in independent Ubuntu fixture `/tmp/jgas-rephase-increment-b-sol-implementation`. [B manifest](../rephase-1-increment-b/candidate.json), [A-to-B patch](../rephase-1-increment-b/increment-b.patch), changed-file copies, [final test evidence](../rephase-1-increment-b/final-test-report.md), and [final independent bounded review](../rephase-1-increment-b/independent-implementation-completion-review.md) are durable. The 14-module run has 131 successes and one historical W34 skip; its failed pip inventory remains separate. Do not rerun older scripts or infer that content recovery recreates the original commit/history. Verify any recovered identity and rebind affected evidence. A/B closeout is a Human commit/Push checkpoint; next work is the current plan's bounded Profile/support and application-prerequisite analysis, not a repeat of B. Whole candidate remains NOT_READY.

## Read and authority order

1. Current Human instructions and `AGENTS.md`.
2. Compact `handoff/rephase-1-continuation.md`.
3. `outputs/rephase-1-implementation-plan.md`; consult the Summary intake for deferred-item scope, then relevant source/evidence only for the assigned increment.

Old handoffs/assessments are historical decisions, not competing current work queues. The prior B3 design and its two reviews support direction/evidence qualifications, not runtime acceptance. The Summary's restart policy does not authorize production maintenance or change the Human-fixed baseline. An ordinary Human commit of these documents does not authorize another trial by its title alone.

## Identities and preserved work

| Item | Identity / location |
|---|---|
| Workspace | `D:\Git\reconstruct-japanese-generative-ai-survey` |
| WSL view | `/mnt/d/Git/reconstruct-japanese-generative-ai-survey` |
| Reconstruct HEAD observed at this preparation | `8e225fa346ab5be4fc8c2f1d2fc21c964b5c79af`; historical observation, not a required future HEAD |
| Fixed production | `774dd39a951c9ac3818e83dfffd4c7666efb0a20` |
| Original five-file r2 local candidate | `46472e41e353de56685e737fc91e85fcc2005312` |
| a1 / tree | `d38f023ce200619f7f49ce17a348755f05e0e021` / `960585ef29b55567efdf08901de489e4f3bb8fe5` |
| f1 / tree | `bf32edf98ba8f605169d7188bbc764de74ee4f6e` / `ebd351479ec222a08b8ea67ae4aae64ad0eb927e` |
| f1 source fixture | Ubuntu `/tmp/jgas-rephase-freeze-b1b2` |
| a1 retained fixture | Ubuntu `/tmp/jgas-rephase-application-r2`; earlier audit copy `/tmp/jgas-rephase-application-audit-r2` |
| Inert fixture origin | `https://example.invalid/rephase-application.git`; no alternates/shared database |
| Task-local Python | `/tmp/jgas-rephase-application-venv/bin/python`, CPython 3.12.14 |
| Durable f1 recovery inputs | `notes/rephase-1-freeze/application.patch`, `repair.patch`, `candidate.json`, `candidate-commit.txt`, `candidate-files/` |
| Fixed source cache | `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/`; ignored convenience cache, not durable sole authority |

At turn start only the new transition packet was untracked; earlier work had been committed by the Human. Do not assume the old uncommitted list or HEAD from previous packets is current. Run a read-only status first and preserve any new Human edits. Ordinary final commit/Pull/Push remain Human-owned.

## If `/tmp` survives

The following eight-file instructions describe the retained **f1** fixture. For current B continuation, use B's own manifest and 21 changed-file hashes at `c04f32a`; do not reset B to f1 or treat these historical f1 instructions as a request to rebuild completed work.

Co-Worker verifies HEAD/tree, all eight f1 file hashes, clean tracked worktree/index, own `.git`, no alternates and inert origin. Untracked pycache was recorded; do not blindly delete it or infer candidate drift. Make a **copy with independent object files, not hardlinks/shared object databases**, into a new task-specific fixture, then create only a local `codex/` review branch there. No inherited `GIT_DIR`, `GIT_WORK_TREE`, object-directory or alternates overrides. Preserve f1 read-only.

## If `/tmp` is gone

Do not run the historical preparation scripts unchanged: they use fixed `/tmp` targets and overwrite old manifests/logs; some assume ignored caches and would resolve dependency versions anew. Do not install `candidate-files` directly into a production checkout.

Co-Worker may reconstruct a new **independent** repo from the fixed production SHA only, materialize the paths required for the assigned work, then apply the durable full `notes/rephase-1-freeze/application.patch`. Verify all eight hashes and expected full candidate tree. Acquire any missing assets strictly at the fixed SHA with hash verification, before removing acquisition remotes and making origin inert. No lazy production fetch during tests. A content-equivalent reconstruction with different local commit metadata is **not** the old exact reviewed commit; record the new identity and obtain fresh affected verification/review. Never label it `bf32edf98` unless its real object hash matches.

Reference mechanics, not auto-run scripts: `notes/rephase-1-application/prepare_candidate.py`, `hydrate_test_assets.py`, `test-assets.json`, and `runtime-setup.md`. The full application patch can reconstruct the content without depending on ignored original r2 raw files. Historical raw commit metadata aids identity verification but is not permission to share reconstruct's Git object database. Build a new packet and leave earlier logs/manifests intact.

Runtime pin evidence: uv 0.12.15; CPython 3.12.14; jsonschema 4.23.0; pypdf 6.16.2; attrs 26.1.0; jsonschema-specifications 2025.9.1; referencing 0.37.0; rpds-py 2026.6.3; typing-extensions 4.16.0. These are observed previous resolutions, not production dependency upgrades. Use fixed Core requirements; record deviations rather than silently refreshing. Environment provisioning and test execution belong to Co-Worker.

## Known traps / do not rediscover by default

- Windows integration remains unestablished: prior failures involved shell argument handling, fixed-Core backslash paths and tzdata. Use the established native Ubuntu boundary for candidate tests; don't change Core to make Windows setup pass.
- Linux lacks `rg` in the fixture environment; use Windows `rg`, or `grep`/Python there. PowerShell-to-WSL quoting of `|` and shell metacharacters can change argument meaning; use explicit argument-safe commands/scripts. No destructive multi-shell file operations.
- Python 3.10 cannot import some fixed Core syntax. Use the recorded 3.12 runtime. No fallback “PASS” after import errors.
- The previous broad a1 suite ended without a completion record; cause unknown. Three asset-related reruns passed after 41 fixed files were hydrated. W34 old-history and explicit legacy skips remain gaps. Do not claim full CI or finish it solely for this narrow next increment.
- New boundary tests imported a fixture module via `importlib`, avoiding imported TestCase aliases that duplicate unittest discovery. Synthetic upstream history/blank fixture PDF/low-level Human approval are not a full edition or canonical durable Human Gate roundtrip.
- Initial B3 annotation was schema-invalid. Preserved initial/current artifacts and separate resolution report distinguish it from the corrected schema-permitted field control; even corrected full fixture is function-only, not a valid publisher CLI input.
- Independent report availability is not proof the author reviewed later root edits. Initial Astra B3 review stopped at a usage limit; fresh Sol verified two corrected design/evidence inputs only. No runtime implementation acceptance follows.
- Root historically executed tests and code, but the **new role rule overrides that practice**. Astra defines/reviews; Co-Worker implements/runs. Usage limits do not authorize role substitution or fabricated reviewer attribution.

## Pending decisions made explicit

Increment A exact-manuscript binding and Increment B's selected Weekly source-closure/pending-revalidation implementation are complete within their bounded scopes. B's final exact-head tests and final independent implementation review are saved; no B test or author task remains to resume. The original Auditor's in-progress report is historical and is superseded for the final judgment by a different reviewer's explicit completion report, not silently promoted to PASS. Whole B3/application readiness still needs supporting semantics and real profile-route evidence. DM-001/003/004 must be dispositioned before whole-path claims, separately from f1's proven scope. No plan to repair all 15 deferred items, refresh old execution indexes, merge review authorities, follow main, or run production Actions exists.

## Current restart distinctions — checked 2026-09-27

- The writable reconstruct workspace was still at Human commit `369c95499b0d1068e6909c33c68278fb05a9a115` when checked, with A/B packets and closeout documents uncommitted. This is an observation, not a required future HEAD. The isolated B candidate `c04f32a` belongs to its separate WSL Git database. Committing/Push of reconstruct preserves the durable evidence; it does not publish that fixture's branch or adopt its code into production. Recheck status after any Human commit.
- B's `increment-b.patch` is **A-to-B**, not a full production-baseline application patch. The retained f1/A packets supply earlier content deltas. Manifests, patches and changed-file copies support content recovery, but the packet does not certify a complete standalone Git database or recovery of every original intermediate commit. If `/tmp` is lost, distinguish recovered content/tree from exact original commit/ancestry; record any new identity and obtain affected fresh verification/review. The previously recorded full-application missing-object diagnostic remains unresolved.
- In the B packet, unsuffixed `final-matrix.sh/.log/.exit` belongs to the failed **cb96** attempt. `final-matrix-c04f32a.sh/.log/.exit` is the completed final run. Do not resume or rerun either merely because an agent disappeared; final exit `0` and the complete 132-method log already exist. Historical attempt files and scripts are evidence, not the next work queue.
- Final B used `/tmp/jgas-rephase-application-venv/bin/python3.12`, Python 3.12.14. That run's `pip show` inventory failed because the environment had no pip module. Earlier recorded dependency pins are historical observations, not a successful final-run version inventory. A later metadata query cannot retroactively repair that command's outcome. No dependency install or test rerun is needed for document continuation.
- `.gitattributes` now marks both A/B packet directories `-text` to preserve hash-bound bytes across commit/checkout. This is reconstruct-only artifact handling and does not alter the reviewed B code. Commit scope includes the currently untracked A/B packets as well as the updated entry/assessment files; do not rely on WSL `/tmp` alone.
- Human asked to be notified at a good commit/Push boundary. A/B completion was identified as such a boundary; this is a notification preference, not authorization for agent commit/Push. The next bounded Profile/support/application analysis has not started. It should first return caller/authority paths, demonstrated versus missing coverage, justified prerequisites versus deferred scope, and the minimum evidence needed for each proposed next change. Astra decides scope before further implementation; no current-main refresh or new approval role is implied.

This packet captures the decisions required for continuation. No active Worker/Auditor state or giant chat history is a prerequisite. Fresh roles start from file-defined tasks and exact inputs.
