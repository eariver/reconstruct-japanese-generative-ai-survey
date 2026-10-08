# DM-004 — Release closure validation CLI bounded completion

Recorded **2026-10-07**, final source/restore observation at **22:20:37+09:00**. Human continuation began at clean reconstruct **5f34b8eb137f741f425164a3b0e5e9ae36c14200**, local tracking synchronized without fetch. **DM-004 is bounded repaired at409b292. Stop at this Human Commit Point.** Production baseline **774dd39a951c9ac3818e83dfffd4c7666efb0a20** is unchanged. Whole candidate **NOT_READY**, step4/B3 OPEN, canonical seven-point audit unstarted.

## 1. Exact candidate and scope

| Field | Current value |
|---|---|
| HEAD | **409b292756dd1277b9dfae87679934c0d2ce251c** |
| Tree | **8ce3699861505f32d1d60bdc185d4d4f635aedb2** |
| Direct parent | 34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4 |
| Unit base | e1705b7fed01369767ab9d827c0360117d54aa1f |
| Implementation DB / branch | `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` / `codex/dm004-release-validate-state` |
| Independent restored DB / branch | `/tmp/opencode/jgas-dm004final-restore-20261007T131353Z/candidate-partial-b40de60` / `dm004final` |
| Runtime | existing task-local CPython3.12.14 venv, unchanged pins |

Root independently read actual final HEAD/tree/direct parent, clean restored status and full available chain to baseline774. Both final DBs are clean; parent e170 inputs remain preserved. Seven normal independent-DB commits capture implementation and fixture/oracle corrections; no amend or ordinary reconstruct Commit/Push.

Only **two shipping paths**, +537/−0 from e170:

| Path | Final mode/blob |
|---|---|
| `scripts/survey_agent_control_v2.py` | 100644 / `4bbf73bfacc25f487d16080afa73f9e0e2c8d612` |
| `tests/test_survey_dm004_release_validate_state_v2.py` | 100644 / `f72c12e0d0723956af729291b6757bf22d753346` |

Runtime is **23 added lines**: parser registration and read-only dispatch using existing helpers. Workflow YAML remains byte-identical, blob **de6531d70453dacf9745dae75564020da104420c**. No schema/config/State validator/release-checkpoint producer change. [Final machine manifest](../notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/final-manifest.json), [packet entry](../notes/rephase-1-dm004-implementation/README.md).

## 2. Contract selected and implemented

The existing workflow's local closure step creates a Release Record, invokes `survey_release_checkpoint_v2.py` to adopt FROZEN→RELEASED, then calls:

```sh
PYTHONPATH=. python scripts/survey_agent_control_v2.py --repo-root . validate-state --state "$STATE"
```

The agent controller previously had no such subcommand. The bounded parent witness at e170 records exact **argparse exit2 / invalid choice**, not an import or State-file failure. It is a standalone command-contract witness; actual production recurrences remain secondary evidence from the saved Summary, not newly fetched/replayed editions.

The new command resolves/contains State within repo_root **before loading**, invokes shared **`validate_agent_state`**, and returns:

- Valid: exit0 with JSON identifying the normalized State path, `valid: true` and lifecycle/control fields.
- Invalid State/authority/path/read/JSON: controlled stderr and exit2; no success JSON or repair/transition.
- Bad command/missing required argument: argparse refusal, separate from semantic validation.

This is generic State validation: valid **FROZEN** and **RELEASED/COMPLETE** are both demonstrated. It does not impose a RELEASED-only rule or replace the release-checkpoint producer. In the actual workflow sequence, that producer establishes RELEASED/COMPLETE and the new CLI independently validates the result. Existing typed approval/W1/checkpoint/schema checks remain in force.

The alternative `survey_production_v2.py validate-state` was not selected: its `verify_state_basis`/`validate_state_semantics` use initialization/global-contract and legacy checkpoint-attestation rules rather than the agent-first API. That **source contrast**, not differing exits for one invalid fixture, explains the choice. Inline workflow Python would be testable, but the controller entry preserves the intended call and existing CLI error machinery with no YAML duplication. Nothing deletes or turns the required check into an always-successful print.

## 3. New behavioral tests and actual workflow execution

General implemented/tests; Astra reviewed runtime, the full test source, runners/raw outcomes and restoration; a separate reviewer checked each fixed candidate/correction from author-independent context. Root did not run runtime tests.

**Final409b292:21 successful methods, no failures/errors/skips** — [final run directories](../notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/):

| Run | Methods | Accepted scope |
|---|---:|---|
| `run-01-final-newmod` | **7** | Behavioral CLI/path/validation/no-write/whole-local-step/fail-fast tests using real validators and synthetic records |
| `run-02-final-affected` | **14** | Existing controller5 + release-checkpoint9 unit regressions; the latter retain their pre-existing mocks and are **not** substituted for acceptance |

The new module contains18 internal subcase executions (2+4+3+6+3), not18 extra methods. It uses the existing real-validator SpecialFixture, real approval/Freeze/stage advance to FROZEN, real Merge Verification/Release Record, and real checkpoint CLI to RELEASED. New authority oracles have no success mocks. Dates are consistent with the actual CLI's default current timestamp; synthetic release reference is `synthetic:dm004-offline-no-remote`.

Key evidence:

- Generic CLI succeeds on valid FROZEN and RELEASED, preserving inventoried State/authority bytes. Ordinary relative/absolute and normalized in-repo paths work; foreign cwd uses explicit repo-root/PYTHONPATH and returns canonical relative paths.
- Absolute/relative/symlink escapes reject before load. Outside malformed JSON yields the containment error, not a later parse error. Path-case no-write assertions are narrower than the full authority inventories used by the central positive/semantic-negative tests; no global filesystem claim.
- Drifted release provenance, missing Release Record, pending release checkpoint on RELEASED, schema-invalid parsed State, malformed JSON and missing State all reject. Semantic failures assert their specific validator messages; parse/read failures remain distinct. Inventories/State bytes are compared **immediately after CLI, before fixture repair**.
- The actual named workflow **local run block is extracted and executed as a whole bash script**, including its real heredoc and both CLI commands, not a hand-copied command approximation. Extraction pins the unique step/block and excludes neighboring live steps. Exact fixture diff is three additions (Release Record, CORE_STAGE_CONTRACT report, FROZEN checkpoint), one State modification, no removals/other changes; final State is RELEASED/COMPLETE with correct release provenance and shared validation clean.
- Fail-fast uses the **unmodified extracted validation line**, State supplied via its actual environment variable, with semantic-invalid provenance and a harmless trailing sentinel. Exit2/error match, sentinel absent, State/authority inventories unchanged. No real provenance PR step is executed.

This proves the selected **offline post-publication closure interface**, not an actual public Release, external exact-byte download/reconciliation, Actions environment, complete upstream research, rendered QA or Human judgment. No GH/network/PR/push operations were used as test oracles. Retrospective/all-profile publication remains unproved.

## 4. Corrections and evidence discipline

All initial commits/reports/logs remain. [Initial independent review](../notes/rephase-1-dm004-implementation/independent-implementation-review.md) required containment repair at6ffed32; [correction resolution](../notes/rephase-1-dm004-implementation/independent-correction-resolution.md) verified34f934e; [final resolution](../notes/rephase-1-dm004-implementation/independent-final-resolution.md) confirmed the test-only cleanup and final21-method/restore binding.

- Initial CLI used lexical `_path`/`relative_to`, allowing relative escape to appear in a success result. Final code routes through existing `_rel`/`repo_local_path` before State load and reports the canonical relative path.
- Initial workflow test executed only the extracted heredoc and rebuilt two CLI argv manually. Initial negative tests restored files in `finally` before final byte comparisons, which could hide effects. Root required verbatim whole-block execution and immediate pre-repair no-write checks; the reviewer explicitly corrected its prior overclaims.
- Initial runner persisted guards but did not assert source hashes against HEAD, ignored Git error codes/inherited overrides and returned0 on child failure. The final saved **v2 runner** checks Git exits, uses a tight env, pins both source files' worktree bytes against expected committed bytes before/after, and propagates child failures.
- Initial fixture-collision/checkpoint-name/sentinel errors, the correction runner's blob-ID-vs-content-SHA guard refusal and correction test tuple/cwd failures are retained. No clean-first-run claim. The earlier source-grep “rationale test” was removed as documentation rather than meaningful behavior coverage; the final fail-fast line no longer uses Python string substitution.
- Initial6+14 and corrected8+14 results belong to their recorded heads; they are not transferred to409. Final7+14 ran after the final commit. Initial diffstat typo (+394/−1 instead of+394/−0) is qualified in the correction record.

Unlike the older W1 packet, **final pre/post guard JSON, actual argv/cwd/runtime/env, raw stdout/stderr and numeric exits are persisted** in absent per-run directories. They assert expected HEAD/tree/clean status and both shipping source hashes against committed blobs; parent/branch are also recorded. This is per-run bracketing, not continuous/per-test attestation. It does not repair older packets' missing capture.

## 5. Portable exact successor and limits

[Final explicit object pack](../notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack): **48,240 bytes**, SHA256 **e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf**, **32 objects =7 commits/16 trees/9 blobs**, generated from e170..409 including all intermediate commits.

It requires the existing three parent inputs: b40 archive `faf6792f…` (5,152,199B), DM001/01920pack `2c2a8e6f…` (46,164B), W1sevenpack `97d384fe…` (57,856B). Exact full hashes are in the final manifest/restore script and current handoff. A fresh absent restore used all4 hash gates, explicit pack imports and actual HEAD switch/materialization. Current restored HEAD/tree/parent are409/8ce36998/34f, clean; all two-file modes/blobs/worktree bytes and source copies agree. Full physical object inventory comparison reports **109 source files vs107 restored, zero shared device/inode pairs**; no alternates, inert origin, shallow only at real774. Root independently read current restored HEAD/status/full13-commit available chain and final pack hash; current source copies are separately byte-bound.

The saved restore script/logs now preserve the executed steps. Some script postconditions are printed for verification rather than an independently certified general recovery API; it has fixed paths and trusts the exactly hash-bound previously reviewed archive. Treat it as **evidence for this exact restore**, not a general safe-rerun tool. Future restoration still needs fresh absent paths/hash/member/actual-HEAD/clean/object checks. Inherited26,309 missing blobs and unbundled pinned runtime remain; no complete-history/runtime backup claim.

## 6. Astra disposition and next bounded unit

**DM-004 command/State-validation prerequisite is locally bounded repaired at409b292**, with source review, meaningful final21-method evidence, corrected independent resolutions and exact restored identity. This does not mark upstream CV2-DM-004 CORE_FIXED or authorize Production deployment, real Release/provenance PRs or whole application acceptance. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. **Stop at Human Commit Point; ordinary reconstruct Commit/Pull/Push remains Human-owned.**

### Next General unit after Human continuation

Return to the unresolved **LONGFORM_SPECIAL direct-source/supporting-surface reader boundary**, using fixed409 source and the existing B/step4 dispositions. The selected Freeze/State/Release CLI prerequisites are now locally repaired; more generic deferred-maintenance work is not automatically next.

General should produce a concrete contract/callsite/acceptance proposal for the actual Special route: primary TeX, declared supporting TeX/includes, reader-visible bibliography/source notes and trusted style/helper output; where each enters the manuscript/Gate and which exact pre-TeX or later review authority covers it. Determine the smallest supported closure/unsupported-input policy that preserves existing review responsibilities and source/semantic identity separation. Compare a bounded declared-source review target with a profile adapter only against actual callers/costs; no universal TeX parser or copied-all-internal-metadata target.

This next bounded unit is **analysis/contract decision before code**, not a full all-profile inventory rerun. Preserve direct-primary capability with honest limits; do not infer whole support semantics from hashes or transfer later Publication Review PASS into pre-TeX authority. No new reviewer role/authority consolidation is selected. Distinguish Thematic and Retrospective reach; retain DM-016/017 upstream source-class/obligation prerequisites and DM-006/013/018/020 quality/acceptance inputs without automatic implementation. Build-transfer/real PDF preflight and final application/audit remain separate. Return concrete fields/paths/oracles and any necessary authority decision to Astra; no code or additional intake until that choice is made.

No next-unit analysis has started in this closeout. Reuse saved Summary and available409 DB; no current-main refresh, recovery repetition, real publication or old-suite coverage decoration.
