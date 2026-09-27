# Gate CLI persisted-review admission — Astra completion assessment

Recorded 2026-09-27; root clock observed `2026-09-27T18:48:24+09:00`. **Selected Gate CLI unit complete at `e4c8269`**, with General implementation/testing, Astra source/oracle review and a separate General scoped independent review. Whole step 4/B3/application remain OPEN/NOT_READY. This is author-side synthesis, not Human adoption or canonical seven-point audit.

## Fixed candidate and scope

- Candidate: **`e4c82692abee6acedbba07815b0d74ccefb80a7e`**, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`.
- Base is preserved B `c04f32ad46109403e8a63faaa8394a90ee6b869c`. The intermediate `6d87edd` introduced the runtime fix and first test draft; e4c8269 corrected only test oracles. Runtime bytes are identical at those two heads.
- Independent native-Linux DB `/tmp/jgas-rephase-gate-cli`, branch `codex/rephase-1-gate-cli`, inert origin. Parent B remains in its original separate DB at c04f32a. Root rechecked both identities/status after review: tracked trees clean, disclosed Python caches only.
- [Manifest](../notes/rephase-1-gate-cli/candidate.json), [B-to-successor patch](../notes/rephase-1-gate-cli/increment-gate-cli.patch), SHA-256 `29b7f187417df5f7524087c25a4f0931d4906ba3ffd502104baa59e8cd3cb726`, 34,507 bytes. This is not a full production-baseline application patch.
- Exactly two candidate paths: `scripts/survey_reader_surface_gate_v2.py` (CLI/help only) and new `tests/test_survey_gate_cli_persisted_review_v2.py`. Root compared packet copies with committed blobs: `ea1eb652ab49eb479e17318712d84c318bfaf475` and `c839a2fef18f22ebe7bf347c8090a2dac74080e0`, respectively; both match. Independent packet hash verification is recorded separately.
- Production baseline remains `774dd39a951c9ac3818e83dfffd4c7666efb0a20`; no production/main access, deployment or adoption.

## What is repaired

`scan-manuscript --semantic-authority` now resolves the input relative to `--repo-root` with the existing containment helper before reading it. A persisted `SEMANTIC_EDITORIAL` reader-surface review is forwarded as a repository-relative `semantic_review_path` to the existing strict loader. The CLI no longer reconstructs a partial authority dictionary from `source.sha256` or supplies a hardcoded PASS/reviewer default. Actual schema/digest/surface/check/identity validation remains in the existing owner.

Absolute contained paths, repo-relative paths and a differing cwd work. The alternate authority-object route remains validated by its existing branch. `--semantic-review` is still a distinct findings input, not an authority substitute. No reader schema, publisher, lifecycle, substantive review responsibility or Gate authority changed.

Parent witnesses prove **rejection of valid input**, not an old successful approval bypass: absolute path failed on missing `surface_sha256`; relative path failed on unnormalized `relative_to`; a differing-cwd variant failed to load. The same persisted review passed the existing lower-level entry points. Hardcoded attempted PASS synthesis was removed, but the old evaluator already reopened the persisted record through strict validation; do not convert that code smell into an unproved acceptance exploit.

## Tests and Astra review

[Final raw run](../notes/rephase-1-gate-cli/logs/candidate-relevant-tests-e4c8269.log) / [numeric exit](../notes/rephase-1-gate-cli/logs/candidate-relevant-tests-e4c8269.exit): **32 test methods, 32 successes, no skips, 65.075 seconds, exit 0**, at exact e4c8269 head/tree/parent. This is 27 affected existing Gate methods + 5 dedicated CLI methods. The latter include 16 subTest blocks / 18 executed subcases; those are not 18 extra methods. CPython 3.12.14 and dependency versions are recorded by `importlib.metadata` in the raw log. No successful B full-matrix rerun was needed.

Root read the runtime diff, full first test draft and corrective delta, parent raw traces/controls, final run/exit and final independent review. Required corrections before completion:

1. Replace an alternate manuscript that was only schema-shaped (noncanonical primary path) with two genuinely validator-valid same-issue manifests; prove exact selected-manuscript admission rather than fixture-invalid rejection.
2. Positively validate a wrong-target review before asserting the actual route rejection. Preserve deliberately broken digest tests separately from freshly rehashed semantic negatives.
3. Prove findings cannot substitute authority; remove normative tests that locked in the inherited array-loading defect/arbitrary-object acceptance.
4. Upgrade generated-Weekly no-write evidence from a small watchlist to all regular files outside `.git`: the actual CLI adds only the declared Gate. Direct-primary negatives retain their explicitly limited watchlist; this is not whole-State mutation evidence for every negative.

Generated Weekly uses real accepted producer/checkpoint validators, two-pass publisher generation, actual CLI with `--state`, and independent Gate/receipt readback. Fixture-constructor/argv patches do not stub authority validators or Git success. Reviews and research are synthetic, not real Human judgments/publication. Direct-primary coverage is Weekly primary identity, not Special support closure.

## Independent review and evidence qualifications

The fresh [General independent reviewer](../notes/rephase-1-gate-cli/independent-review.md) issued its own **bounded PASS** at e4c8269, no blocking finding in this unit. It did not author candidate code/tests or run tests. Root required corrections to its evidence description: attempted PASS synthesis is not a demonstrated old bypass; arrays fail at object-only `core.load_json` before the evaluator; limited negative snapshots do not prove whole-upstream immutability.

**Reviewer procedure deviation is retained:** despite a read-only task, the reviewer checked the isolated fixture out to B and back twice while investigating patch stats. This changed worktree/HEAD/reflog and was not a pristine read-only review. Its corrected [integrity record](../notes/rephase-1-gate-cli/integrity-verification-log.md) discloses that action. Root independently read the four checkout reflog entries at 18:40:46 and 18:44:40 JST, confirmed return to exact e4c8269 and clean tracked worktree, and verified both committed-file/copy identities. The original B DB remained c04f32a. No candidate authorship or test execution was performed by that reviewer, so its separate scoped code/evidence judgment remains usable; the procedure deviation is not endorsed or hidden. Future reviews must use exact `git show`/diff and avoid checkout or evidence-producing scripts.

The reviewer's `git apply --check --stat` result is not accepted here as clean application evidence. Exact diff/hash/blob identity supports this increment's packet integrity; full baseline application remains unproved. Historical missing promisor objects and the earlier application limitations remain separate.

The first parent-control setup failure's raw log was overwritten before the task correction; it is disclosed, not recreated. Later development failures and corrections are preserved in the [implementation report](../notes/rephase-1-gate-cli/implementation-report.md) and raw logs, and [6d87edd](../notes/rephase-1-gate-cli/attempts/6d87edd/README.md) is archived. The final green run does not make initial attempts clean.

Saved shell runners are **historical evidence, not safe rerun entry points**: they may overwrite logs, and the final runner warns rather than aborting on changed HEAD/dirty tracked files. Final recorded identity matches and contains no dirty-tree warning; this supports that run only. Any future justified run requires a new unique output location and a fail-closed exact-head/clean-tree guard. No new tests are warranted merely to polish an archived runner.

## Deferred transport and next unit

Observed optional findings transport remains defective: `--semantic-review` advertises an array but `core.load_json` accepts only objects. An object may be ignored as findings; the [probe](../notes/rephase-1-gate-cli/logs/findings-transport-probe-20260927T1/findings-transport-probe.json) preserves this without normative acceptance. Disposition: **deferred separate CLI findings/suppressions transport question**; do not claim full CLI feature correctness. Persisted review findings still undergo existing strict checks and are tested by this unit. No blanket suppression relaxation or automatic follow-on repair is selected.

**Next selected work is analysis, not another implementation:** General should formulate the bounded Weekly post-VALIDATED_DRAFT regeneration contract at e4c8269, using the already-completed Profile/application inventory rather than repeating it. Distinguish (a) artifact-only commits, (b) metadata-only renewal already evidenced by B, (c) changed implementation with unchanged complete reader input, and (d) changed reader content/output. Trace existing pending-context/revalidation callers and concrete publisher-owned output sets; determine valid current-tool/accepted-upstream authority and semantic-review reuse/invalidation. Include the compile → allowed output transfer → Gate admission boundary and existing QA/log needs as a dependency, not a new build framework. Return a minimal interface/ownership/test proposal and explicit stop conditions before code. No deletion of publication authority, lifecycle relaxation, automatic old-PASS reuse, production workflow execution or new reviewer consolidation.

Special/support and DM-001/003/004 retain the [step-4 dispositions](rephase-1-profile-application-assessment.md). Whole application and canonical seven-point audit remain open; no net lifecycle saving is measured. This completed CLI packet and updated entry documents are a Human commit/Push checkpoint; ordinary reconstruct commit/Push remains Human-owned.
