# DM-004 Release workflow/CLI/State-validation contract analysis (INTERNAL, no code yet)

Status: General Co-Worker first internal design/contract return ONLY. No source edits, no tests run, no fixture writes. Root decision required before code within this active unit.

## 1. Read-only environment verification (actual, not inferred)

- Impl DB `/tmp/opencode/jgas-dm003w1-impl-20261004T072423Z`, branch `codex/dm003w1-preview-agreement`: HEAD `e1705b7fed01369767ab9d827c0360117d54aa1f`, tree `3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557`, parent `222a37e9ee2aa96724a491f2c04c2583a86b9650`, `status --porcelain` clean, origin `https://example.invalid/...` inert, no alternates file.
- Restored DB `/tmp/opencode/jgas-dm003w1-restore-20261004T073938Z/candidate-partial-b40de60`, branch `dm003w1-final`: same HEAD/tree/parent, clean, same inert origin.
- Env: `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`, no Git-root overrides. Pinned venv `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python` = 3.12.14 (observed only, not executed for tests).
- `apply_patch`: NOT AVAILABLE (`command not found`); implementation must state this and use another minimal-edit path later.
- No network/main fetch, no Summary refetch (only saved §CV2-DM-004 re-read), no recovery, no old-suite execution, no subagents.

## 2. Exact source pins (fixed e170)

| Path | Git blob at e170 |
|---|---|
| `.github/workflows/survey-production-v2-release.yml` | `de6531d70453dacf9745dae75564020da104420c` |
| `scripts/survey_agent_control_v2.py` | `d58db79b8ce43a2cb55814a38ff7542ff556f86a` |
| `scripts/survey_release_checkpoint_v2.py` | `35ee8292352d4982cc28d077443c3bc7dc7064bf` |
| `tests/test_survey_release_checkpoint_v2.py` | `3757f1940d0b6e593724b4c97951fbba11f32b9d` |
| `tests/test_survey_agent_control_v2.py` | `93e0d440572552f4ae163bdb69788fcca6675421` |

Raw reads via `git show HEAD:<path>` only; worktree files not modified. Controller is 2366 lines; `main()` at ~2228; `validate_agent_state()` at 348-350 delegates to `_validate_agent_state()` (returns `list[str]`, empty = valid).

## 3. The fault (source-grounded)

- Final provenance-closure step runs, under `set -euo pipefail` + `PYTHONPATH=.`:
  `python scripts/survey_release_checkpoint_v2.py --repo-root . --state "$STATE" ...` (valid) then
  `python scripts/survey_agent_control_v2.py --repo-root . validate-state --state "$STATE"` (INVALID).
- Controller `main()` registers exactly 5 subcommands (`advance-stage`, `approve-architecture`, `approve-publication-preview`, `revalidate-publication-surface`, `refresh-mechanical-evidence`); `subparsers(required=True)`. `validate-state` matches none → argparse exit 2 → step fails AFTER public Release/reconcile + `build_release_record`, BEFORE provenance PR. This matches saved Summary CV2-DM-004 recurrences (W36 run 35345335385 → W39 run 36581201216, recovery via `survey_release_checkpoint_v2.py` + Python API `validate_agent_state`, no public-Release recreation).
- Globals `--repo-root/--config` precede subcommand; `--state` is per-subcommand. The invalid argv order already follows the correct convention, so a same-name subcommand is the minimal contract repair.

## 4. Intended post-checkpoint semantics (actually encoded)

- `build_release_checkpoint` requires FROZEN State + canonical `stage_plan.FROZEN` (`action_kind WORKFLOW_DISPATCH`, `next_state RELEASED`), validates Release Record↔Merge Verification binding, writes one compact checkpoint at `canonical_checkpoint_path`, then `main()` calls `advance_with_checkpoint` → `lifecycle_state RELEASED`, `machine_checkpoints.release=passed` + provenance, history append, `refresh_state_control` → `next_action None`, `terminal_reason COMPLETE` (per `derive_control_fields`: RELEASED → `(None, COMPLETE)`). Existing test `test_success_path_advances_to_released_and_terminal_complete` asserts exactly this. So the missing gate must validate a RELEASED/COMPLETE State, NOT a valid FROZEN State.

## 5. Options compared (no broad CLI framework)

- **A (SELECTED): add `validate-state` subcommand** (~20 lines: subparser + dispatch). Reuses shared `validate_agent_state`; prints JSON `{"state":..., "valid": true}` exit 0, else stderr + exit 2. Workflow YAML UNCHANGED (invalid line becomes valid). Testable offline with the exact pinned argv. Single authority, no YAML logic duplication.
- **B (REJECTED): inline `PYTHONPATH=. python -c 'validate_agent_state...'` in YAML.** Duplicates loader/exit logic in shell, untestable as CLI contract, diverges from sibling `survey_release_checkpoint_v2.py` CLI pattern.
- **C (REJECTED): delete the line / replace with `echo ok` status print.** Destroys the required post-write gate: a divergent checkpoint/State could still open the provenance PR; always-success masks invalid authority. Violates the "retain necessary validation" order.

## 6. Selected minimal fix + path budget

- `scripts/survey_agent_control_v2.py`: ADD `validate-state` subparser (`--state`, uses global `--repo-root/--config`); dispatch loads cfg + State, calls `validate_agent_state`, exit 0 valid / exit 2 invalid (`AgentControlError(ValueError)` already maps to 2). ~20-30 added lines, zero changed lines.
- `.github/workflows/survey-production-v2-release.yml`: ZERO lines (argv kept byte-identical by design).
- Tests: ONE new focused file `tests/test_survey_dm004_release_validate_state_v2.py` (~150-200 lines, 6 methods, see §7). No edits to existing oracles, schema, config, helpers. No new authority/roles.
- Shell-step rule for implementation: execute ONLY the extracted `build/checkpoint + validate-state` Python block offline in synthetic fixtures; NEVER `gh`, `git push`, live Release, Actions dispatch, or provenance PR steps.

## 7. Offline oracle matrix (planned, NOT yet executed)

| # | Proposed method | Setup (synthetic, real validators) | Command (pinned `python3.12`) | Expect exit / writes |
|---|---|---|---|---|
| 1 | `test_validate_state_accepts_released_complete` | FROZEN→RELEASED via REAL `build_release_checkpoint`+`advance_with_checkpoint`, then on-disk RELEASED | `survey_agent_control_v2.py --repo-root <tmp> validate-state --state <state>` | 0; State bytes unchanged; stdout JSON valid |
| 2 | `test_validate_state_wrong_command_fails` | same fixture | `... validate-states --state <state>` (typo) | 2 (argparse); no writes |
| 3 | `test_validate_state_rejects_invalid_authority` | RELEASED with drifted release-provenance SHA | same valid argv | 2; stderr names drift; no writes, no PR |
| 4 | `test_validate_state_rejects_missing_state` | state path absent | same argv | 2 (`OSError`); no writes |
| 5 | `test_validate_state_rejects_pending_release_provenance` | RELEASED with `release` checkpoint reset to pending | same argv | 2; no writes |
| 6 | `test_extracted_workflow_block_offline` | fresh synthetic FROZEN; run EXACT two-command block (checkpoint CLI + validate-state CLI) | both CLIs, pinned interpreter | 0/0; ends RELEASED/COMPLETE; State hash advances once then stable |

Fixture cost: temp-dir-per-test under repo root (existing pattern), synthetic records/PDF labels only; REAL `validate_agent_state`/`advance_with_checkpoint` in #1/#6, narrow mocks only where full canonical history is out of scope (#3-#5 document which validator branch fires). Limits: no gh/network/PDF bytes; does not prove live Actions or all-profile acceptance.

## 8. Awaiting root decision

Approve (a) `validate-state` subcommand contract + stdout/stderr/exit semantics, (b) zero-line workflow retention, (c) new-file-only test budget + matrix above — or redirect — BEFORE any code. Next unit after approval: isolated-DB implementation, offline matrix execution, pack/restore, independent review; no Human commit/push by agent.
