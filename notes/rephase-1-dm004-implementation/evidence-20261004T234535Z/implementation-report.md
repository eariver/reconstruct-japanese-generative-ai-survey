# DM-004 bounded implementation report (General Co-Worker return)

Final candidate **`6ffed32298fdaf87874a643b0f9f9b8f837c0256`**, tree
`c3d6ad6ffdadf2d5780a3cd5109555c87fe394cc`, parent chain
6ffed32→22598f1→d80b5ee→3dc4288→e1705b7, in
`/tmp/opencode/jgas-dm004-impl-20261004T234416Z`, branch
`codex/dm004-release-validate-state`. Independent byte-copy (`cp -a`) of the
read-only e170 impl DB; zero shared object inodes; no alternates/hardlinks;
inert `example.invalid` origin; no Git-root overrides. Four normal local
commits, no amend/bypass/config. Source e170 DBs verified still at e170.

## Change (2 files, +394/−1, runtime +19 lines)

- `scripts/survey_agent_control_v2.py` (blob `7c6450c`): new read-only
  `validate-state --state` subcommand reusing global `--repo-root/--config`,
  `_path` handling and the shared public `validate_agent_state`. Valid → exit
  0 + JSON (`state`, `valid: true`, lifecycle/control fields); nonempty errors
  → `AgentControlError` → existing catch → exit 2 with stderr. No
  write/transition/repair. Workflow YAML **unchanged** (0 lines).
- `tests/test_survey_dm004_release_validate_state_v2.py` (blob `76e4fe5`,
  375 lines): 6 methods / 10 subcases, zero mocks.

## Root corrections applied (vs proposal)

Generic CLI (valid FROZEN also passes; RELEASED-only wording rejected);
`survey_production_v2.py validate-state` recorded as non-equivalent
(`verify_state_basis`/`validate_state_semantics`, init-pin/global-contract/
legacy-attestation, exit 0/1 style — proven live: same dangling state →
legacy 1 vs new 2); inline-YAML “untestable” rationale corrected (testable
by extraction; rejected for single-authority/zero-YAML-diff reasons).

## Oracles (real validators, synthetic release ref only)

- Parent witness (run-00, pre-edit): exact workflow argv → exit 2,
  `invalid choice: 'validate-state'`, not import failure. Persisted.
- New 6/6 OK (run-05, 106s): FROZEN+RELEASED CLI exit 0/bytes-unchanged
  (rel+abs paths); 5 invalid-State subcases exit 2 discriminative/no-write;
  3 argparse refusals exit 2; extracted heredoc+2-CLI closure → RELEASED/
  COMPLETE with FROZEN-named checkpoint bound; set-e sentinel suppressed;
  legacy non-equivalence. Fixture: imported DM001/019 SpecialFixture,
  T0+5h..T0+11h (Sept 12, before real now), real Freeze/merge/record/
  checkpoint advance, `RELEASE_REF=synthetic:dm004-offline-no-remote`.
- Affected 14/14 OK (run-06, 7s): controller 5 + release-checkpoint 9 with
  their retained mock scope disclosed (not acceptance).
- First failures preserved: run-01 (4: fixture collision, RELEASED-named
  checkpoint assumption ×2, sentinel typo), run-02 (1: same typo second
  site) → correction commits d80b5ee/22598f1/6ffed32.

## Portable successor + restore

Pack `dm004-e1705b7-to-6ffed32.pack` (43,270 B, SHA256
`7e147a60…59c95dd0b4e`, 18 objects: 4 commits/9 trees/5 blobs) + patch +
source copies + machine manifest. Restored `/tmp/opencode/
jgas-dm004-restore-20261004T235816Z/candidate-partial-b40de60` from all 4
hash-gated inputs via saved `restore_dm004.sh` (log kept): actual HEAD/
tree/parent/clean, full chain to shallow-774, both modes/blobs/bytes equal,
zero inode sharing, inert remote, no alternates.

## Limits / no blocker

Valid RELEASED fixture WAS constructible — no broadening blocker. Offline
synthetic only: no gh/network/live Release/Actions/PR/production; missing
26,309 blobs + unbundled runtime inherited; no full-suite rerun; no adoption.
Whole candidate NOT_READY. Awaiting Astra diff/oracle/evidence review, then
independent review; Human Commit Point ends unit.
