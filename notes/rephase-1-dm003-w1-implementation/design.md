# DM003-W1 narrow repair — internal design (no code/tests yet)

Status: DESIGN ONLY for Astra narrow selection. No runtime code/test/ref/commit
executed. `apply_patch` not available in this session; saved via Write tool.

## 1. Source pins (verified read-only 2026-10-04)

- Shipping parent HEAD `222a37e9ee2aa96724a491f2c04c2583a86b9650`,
  tree `dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`,
  parent `ff6c67f68e12b3093901248219f2de2872e54d73`.
- Primary: `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`
  (`codex/dm001019-freeze-implementation`): HEAD/tree/parent exact,
  `status --porcelain` clean, origin inert `example.invalid`, no `GIT_*` overrides.
- Restored 222 also available at
  `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`
  (same HEAD verified). Runtime: pinned `.../candidate-recovery-tooling-20261003T0435Z/venv/bin/python` 3.12.14.
- Env for all future reads: `GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file GIT_OPTIONAL_LOCKS=0`.
- Actual source read: `scripts/survey_agent_control_v2.py:403-416`
  (checkpoint-only Preview check), `:448-495` + `:692-704`/`:1799-1802`
  (pending/inert rules), `scripts/survey_profiled_freeze_v2.py:33-62`
  (trusts State, consumes human ref), `scripts/survey_stage_validation_v2.py:126-139`
  (sole `human != checkpoint` disagree guard). No other guard assumed.

## 2. Minimal common condition

In `_validate_agent_state`, inside the existing
`name == "publication_preview" and wanted == "passed"` branch, after the
current canonical-path/drift/typed-`validate_preview_approval` checks pass,
require: `human = state["human_gate_provenance"]["publication_preview"]`
is a dict with exactly `{path, sha256}`, non-null, and
`human["path"] == checkpoint["path"] and human["sha256"] == checkpoint["sha256"]`.
- Malformed human ref (non-dict / missing keys / null) → structural error,
  distinct message from individually-valid-but-divergent conflict.
- `sha-only` or `path-only` match still fails (AND required).
- Pending/inert paths untouched: `pending` still forbids any Preview provenance;
  rule fires only when `wanted == "passed"` (approved).
- No schema/config/workflow/new checkpoint names/filesystem scan/wrapper duplication.
- Stage `disagree` backstop kept; `_safe_state_profile` inherits via shared validator.

## 3. Callsite / test budget / isolation

- Callsite: one edit in `scripts/survey_agent_control_v2.py` (~403-416 region).
- New focused module only (e.g. `tests/test_survey_dm003_w1_preview_agreement_v2.py`)
  on a NEW independent DB copy of 222 (inert origin, no alternates/hardlinks);
  reuse real Special LONGFORM_SPECIAL + Weekly fixture helpers already used by
  DM-001/019 equivalence tests. Cases, each real-validator + actual-wrapper
  no-write byte-inventory (pre/post regular-file diff, State bytes stable,
  outputs-absent asserted pre-call): healthy approved agree → BUILD;
  pending control → validator rejects, wrapper no-write; FROZEN valid-context
  compat (agreed refs advance, no new reject); same-C1 split S3 replay
  (exact A1 canonical vs A2 rival, distinct path/hash, both typed-valid,
  same candidate bytes) → validator rejects, wrapper no-write; missing human
  ref + sha-only-mismatch structural cases (malformed vs valid-conflict messages).
  No authority-success mocks; no DM001/019 test edits except as §4.
- Affected existing (nominated, not full 56+R1):
  `test_survey_dm001_019_freeze_equivalence_v2.py` (healthy agree-path methods only),
  `test_survey_profiled_freeze_v2.py` + `test_survey_stage_validation_v2.py`
  (approved-State happy paths touching `_validate_agent_state`).
  Reuse saved parent S3 bytes/traceback; new targeted parent method only if Astra
  demands it, bounded + justified in implementation return.

## 4. Packaging

New candidate commit on independent DB with fresh per-module HEAD/tree/source-hash
guards (not reused common capture); durable successor objects via actual
available chain (b40 partial archive + 20-object successor pack) + current-HEAD
restoration planned at implementation time. Reconstruct AGENTS/handoff untouched.
