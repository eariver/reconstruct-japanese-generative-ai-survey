# LF-2I R2 correction config registration note

2026-10-10. `config/survey-production-v2.json` remains unchanged in this
correction round.

Mechanism: both new schemas/scripts live under existing
`implementation_control_roots` (`schemas`, `scripts`), so `verify_tool_basis`
(`survey_longform_generated_v2.py`) already refuses uncommitted overlay bytes
via `git diff --quiet commit HEAD -- control_paths`, dirty-HEAD and
untracked-control checks, plus per-row closure byte equality against both the
recorded commit and HEAD. The note documents this pinning mechanism rather
than claiming registration was performed. No config edit is invented absent a
demonstrated threading gap (independent reviewer endorsed this decision).
No dispatcher/lifecycle/policy, reason-taxonomy, fidelity-schema, role, or
Production change in this round. Source path budget unchanged (publisher +
integration test only).
