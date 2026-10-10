# LF-2I correction config registration note

2026-10-10. `config/survey-production-v2.json` remains unchanged in this correction.

Mechanism: the new receipt/reader contract-file bytes are fully pinned by the
receipt closure (`current_closure` includes both new schemas plus the trusted
style and shared Gate/runtime/schema paths) AND the existing
`implementation_control_roots` + configured `contract_files` equality/ancestry
check inside `verify_tool_basis`. Any unlisted shared-helper change or contract
drift refuses via `git diff --quiet commit HEAD -- control_paths`, dirty-HEAD
and untracked-control checks, plus per-row byte equality against both the
recorded commit and current HEAD. No dispatcher/lifecycle policy repair was
performed and no new authority/role was introduced. This documents the pinning
mechanism rather than claiming config registration was performed.
