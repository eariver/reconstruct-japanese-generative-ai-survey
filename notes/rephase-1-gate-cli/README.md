# Gate CLI persisted-review unit — evidence entry

**Bounded complete at e4c8269.** [Astra assessment and next work](../../outputs/rephase-1-gate-cli-assessment.md) / [candidate identity](candidate.json) / [General implementation report](implementation-report.md) / [General independent review](independent-review.md).

- Final candidate `e4c82692abee6acedbba07815b0d74ccefb80a7e`; tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`; parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`. Patch is **B c04f32a → e4c8269**, not the full production-baseline diff.
- [Final run](logs/candidate-relevant-tests-e4c8269.log) and [exit](logs/candidate-relevant-tests-e4c8269.exit): 32 methods / no skips / exit 0. Earlier attempted results and the first test draft belong to their own source states; see `attempts/6d87edd/` and implementation report.
- `changed-files/` contains the two exact candidate files. `.gitattributes` preserves this packet's bytes. Recovery of content does not necessarily recreate the original commit or its ancestry; rebind verification if identity changes.
- Parent failures: `logs/parent-witness/`; first parent setup raw-log loss remains disclosed. Other failed development logs remain in `logs/`.
- Reviewer procedure departure and corrected evidence claims: [integrity record](integrity-verification-log.md). Root rechecked final HEAD/tree, clean tracked worktree and copied-file blob identities after the disclosed temporary checkouts. No tests were rerun by root/reviewer.
- **Do not auto-run saved `setup/`, `witness/` or `run-candidate-tests.sh`.** They document prior operations and can overwrite outputs or assume fixed temporary paths; the last runner does not abort on head mismatch. Any future justified task must use unique log names and fail-closed identity/isolation preflight. Completed tests need no replay for decoration.

All review/research fixtures are synthetic. This packet does not prove full CLI findings transport, Special/support closure, build transfer, Weekly regeneration, canonical Human Gates, application readiness or production adoption.
