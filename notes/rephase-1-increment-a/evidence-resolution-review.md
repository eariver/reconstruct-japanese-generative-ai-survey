# Increment A — late evidence resolution review

2026-09-22 JST. Reviewer: fresh scoped Sol resolution reviewer, separate from the Increment A implementation Workers, root/Astra's author-side review, and the original independent Auditor. This review is limited to the evidence-only clarifications added after the original independent bounded implementation review. It did not rerun tests or the full audit, author or change candidate code/tests, inspect production/current main, edit the original report, or perform a reconstruct commit/push.

## Scope and inputs

Reviewed `independent-review.md`, `candidate.json`, `commands.md`, `isolation-command.sh`, `isolation.log`, `parent-witness.log`, `failure-history.md`, `application-patch-check.log`, `packet-verification.log`, and `README.md`. Candidate identity and file bytes were independently read from the existing Ubuntu fixture `/tmp/jgas-rephase-increment-a-sol-copy`; durable packet copies and saved patches were read from this evidence directory.

This is a resolution supplement to the original bounded Increment A report. It is not a new independent implementation audit and does not enlarge that report's scope.

## Identity and byte verification

Read-only Ubuntu checks independently resolved:

- candidate commit `1a9649129d1745fed0b98db46ef15f014407e6fc`;
- tree `5e933aa54034ed227216252a2c8707a59f293acf`;
- parent f1 `bf32edf98ba8f605169d7188bbc764de74ee4f6e`;
- exactly four changed paths: the three runtime modules and the dedicated test module listed in `candidate.json`.

The fixture had no tracked working-tree difference. Each working-tree blob ID equaled its `HEAD` tree entry. SHA-256 values calculated independently from the fixture, from `HEAD`, and from the durable `candidate-files/` copies all agreed with `candidate.json`:

| File | SHA-256 |
|---|---|
| `scripts/survey_agent_control_v2.py` | `a61322106d964dfdd7945e7df8d7a16d34bf0110c257615e205a776f13659070` |
| `scripts/survey_reader_surface_gate_v2.py` | `3be61aefb2b0e67a9cc5bf477486bfe02322318219d031eb50607816728d9be8` |
| `scripts/survey_stage_validation_v2.py` | `7cdb1cdc6bb6245affc79c052c8b450fe9cdb30ee7080742d88b670b9aa65265` |
| `tests/test_survey_exact_manuscript_admission_v2.py` | `69e72162f691fa542e57e44a1398080d650ad9442b2745935f8f3044478496f0` |

Fresh renderings of both saved patches also matched their recorded packet hashes: f1-to-candidate `increment-a.patch` is `e5ab9712869ad02b3db7c51cae8371028468f93b7f3fda7fb500efa57c1fc0a1`; fixed-baseline-to-candidate `application.patch` is `0f4bee2c53e96a2f7dd58a76bee2bdc4040e77114f4102ec3523940886d2bb41`.

## Findings and resolution

No material discrepancy was found in the late clarifications, and none changes the original report's bounded Increment A PASS or its code finding set.

1. `parent-witness.log` now records both `EXPECTED_EXIT_CODE: 1` and actual `EXIT_CODE: 1`. Its four traces remain assertion failures because the parent did not raise the expected stage or agent-control rejection. This resolves the parent-run numeric-exit omission; it does not resolve the separately retained first-clone setup omission.
2. `isolation-command.sh` preserves the executed read-only shell body, and its command order and requested observations correspond to `isolation.log`. The original report's statement that the literal combined isolation argv/body was absent is therefore stale and is superseded by this supplement. The log still discloses untracked Python cache directories rather than claiming an empty status.
3. `failure-history.md` explicitly identifies the initial 10-test failure record as a retained tail and states that the complete initial transcript was not persisted. The final exact-head `dedicated-unittest.log` separately lists 11 test methods and reports `Ran 11 tests`/`OK`; the candidate test source shows that one of those methods iterates six named cardinality subtests. The clarification is internally consistent and prevents treating the six subtests as six extra methods.
4. `application-patch-check.log` records exit 0 together with `invalid object ... sources/2026-W32/candidates/README.md` and explicitly classifies the result as not a clean application proof. `failure-history.md` gives the same classification and attributes the diagnostic to the unrelated missing promisor object. The exact application-patch bytes are reproducible, but application readiness is not established. By contrast, `packet-verification.log` records the bounded f1 delta apply check as `OK`.

One non-material bookkeeping discrepancy remains: the `PACKET_FILES` size inventory in `packet-verification.log` predates the late evidence-only edits. Its sizes for `README.md`, `candidate.json`, `commands.md`, `failure-history.md`, and `parent-witness.log` no longer describe the final files, and it does not list the later `isolation-command.sh` or `application-patch-check.log`. This makes that section a pre-clarification inventory rather than a final packet manifest. It does not affect the matching candidate-file hashes, patch hashes, candidate identity, or the explicit limitations above.

## Retained limits

The first failed independent-clone attempt still lacks persisted exact source argv and numeric exit code. The initial 10-test failing record remains tail-only. Preliminary working-tree green runs do not replace the final exact-head logs. The full application patch has matching bytes but no clean temporary-index application proof. No tests were rerun for this resolution review.

The evidence remains synthetic Weekly fixture evidence with the reader-input limitation described in the original review. It does not establish Increment B, reader-input completeness or derivation, whole B3, clean fixed-baseline application, all-profile or real publication evidence, lifecycle savings, canonical seven-point acceptance, adoption, or Human approval. The supplement supports only the original report's exact-candidate Increment A scope; B3 remains open and the whole candidate remains not ready.
