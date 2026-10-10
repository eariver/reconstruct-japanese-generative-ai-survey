# LF-2I R3 correction config registration note

2026-10-10. `config/survey-production-v2.json` remains unchanged in this
correction round.

Mechanism: both new schemas/scripts live under existing
`implementation_control_roots` (`schemas`, `scripts`), so `verify_tool_basis`
(`survey_longform_generated_v2.py`) already refuses uncommitted overlay bytes
via `git diff --quiet commit HEAD -- control_paths`, dirty-HEAD and
untracked-control checks, plus per-row closure byte equality against both the
recorded commit and HEAD. Since this round, the publisher additionally re-runs
that full predicate (P3) at every snapshot recheck with the validated recorded
commit/closure, so config or unlisted-helper drift after initial verification
refuses pre-write and pre-receipt. The note documents this pinning mechanism
rather than claiming registration was performed. No config edit is invented
absent a demonstrated threading gap.
No dispatcher/lifecycle/policy, reason-taxonomy, fidelity-schema, role, or
Production change in this round. Source path budget unchanged (publisher +
integration test only).
