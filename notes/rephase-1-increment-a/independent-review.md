# Increment A — independent bounded implementation review

2026-09-21 JST. Reviewer: fresh independent Auditor (`increment_a_independent_review`), separate from implementation Workers and root/Astra's author-side review. The reviewer read committed source, callers, schemas, tests, and raw execution evidence; did not author candidate code/tests, run the test suite, alter fixtures, or perform production/reconstruct Git writes.

## Conclusion and findings

**Bounded review PASS for Increment A at the exact identity below. No actionable P1/P2/P3 implementation finding identified within this increment.** The evidence supports exact stage-selected Reader Manuscript admission at DRAFT_COMPLETE, inherited VALIDATED_DRAFT, and establishment/readback of active publication revalidation. This is partial B3 only. It is not the canonical seven-point audit, whole-B3 acceptance, application readiness, adoption, real Human approval, all-profile certification, or demonstrated lifecycle savings.

No correction to candidate code is requested by this review. Evidence limitations below remain qualifications; they must not be silently replaced by a claim that every attempt was clean or every publication route was exercised.

## Reviewed identity

- Candidate: `1a9649129d1745fed0b98db46ef15f014407e6fc`.
- Tree: `5e933aa54034ed227216252a2c8707a59f293acf`.
- Parent f1: `bf32edf98ba8f605169d7188bbc764de74ee4f6e`, tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`.
- Fixed production comparison baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. No production/current-main inspection or refresh was performed.
- Reviewed repository: `/tmp/jgas-rephase-increment-a-sol-copy`; independent Git database, inert origin `https://example.invalid/rephase-increment-a.git`.

The reviewer independently checked commit/tree/parent, the f1-to-candidate diff, unchanged tracked working-tree bytes, and all four changed-file SHA-256 values. The durable `candidate-files/` copies match the inspected files and `candidate.json`:

| File | SHA-256 |
|---|---|
| `scripts/survey_agent_control_v2.py` | `a61322106d964dfdd7945e7df8d7a16d34bf0110c257615e205a776f13659070` |
| `scripts/survey_reader_surface_gate_v2.py` | `3be61aefb2b0e67a9cc5bf477486bfe02322318219d031eb50607816728d9be8` |
| `scripts/survey_stage_validation_v2.py` | `7cdb1cdc6bb6245affc79c052c8b450fe9cdb30ee7080742d88b670b9aa65265` |
| `tests/test_survey_exact_manuscript_admission_v2.py` | `69e72162f691fa542e57e44a1398080d650ad9442b2745935f8f3044478496f0` |

The delta contains these four files only: three runtime modules and one dedicated test module. A changed head/base/tree requires a new scoped review; this result does not transfer automatically.

## Code and authority review

1. `scripts/survey_reader_surface_gate_v2.py:1509` requires exactly one MANUSCRIPT_MANIFEST and exactly one PRIMARY_SOURCE. At lines 1525–1568 it resolves the caller-selected manifest, compares its canonical repository path and actual file hash, schema-loads those exact bytes, checks issue/publication Profile agreement, and compares the primary path/hash against that manifest. Existing scanned-file hash/byte-count checks and persisted semantic-review checks remain after this new admission check. A fresh Gate digest cannot substitute another manifest for the selected one. No new ledger, selector, or approval source was introduced.
2. `scripts/survey_stage_validation_v2.py:510` and `:561` both pass `expected_manuscript_path=manuscript_path`. The first uses required current DRAFT_COMPLETE artifacts; the second uses inherited artifacts, including the bounded revalidation substitution handled by `_prior_artifacts`. Existing full manuscript/Candidate validation, exact source/PDF/review references, and prior authority validation remain in the path. `survey_publication_v2.py:160` recursively validates the manuscript for the latter route, so the Gate's schema-only manifest load does not weaken stage manuscript validation.
3. `scripts/survey_agent_control_v2.py:1381` uniquely selects manuscript and Gate from the checkpoint's preserved/superseded artifact rows. At `:1422` it invokes exact Gate admission after the existing QA validation and before a revalidation record or State pointer is written. Missing or duplicate selected roles fail closed.
4. The callsite inventory found no other production call to this Gate validator needing stage forwarding. `survey_reader_surface_gate_v2.py:1782` is standalone CLI inspection, where the single recorded-manifest fallback is explicitly permitted. `survey_reader_publication_v2.py:638` produces the Gate from its supplied manifest; it is not an admission wrapper. No schema, Human Gate, Freeze/Release producer, or permission bypass was added.

This review also inspected the existing manuscript/primary validation, Candidate validation, prior-artifact/revalidation resolution, both relevant schemas, the Gate producer, and the reused publication-revalidation fixture rather than treating the Worker summary as the oracle.

## Tests and actual outcomes

Reviewed [dedicated raw output](dedicated-unittest.log), [affected raw output](affected-regression.log), [parent failures](parent-witness.log), [commands/runtime](commands.md), [isolation inventory](isolation.log), [setup failure](setup-failure.log), and [failure history](failure-history.md).

| Run | Observed result | Scope |
|---|---|---|
| Exact candidate dedicated module | 11 tests, exit 0, OK; no failures/errors/skips reported | Both stage positives and alternate-manifest negatives; cardinality, primary mismatch, stale bytes, fresh forged digest; revalidation write/readback boundaries |
| Exact candidate affected existing modules | 61 tests, exit 0, OK; no failures/errors/skips reported | Reader-Surface Gate, publication revalidation, Freeze-stage boundary modules |
| Separate f1 parent witnesses | 4 tests, exit 1, four assertion failures | Each expected stage/revalidation exception was **not raised**; these are intended defect witnesses |

The dedicated cardinality test (`tests/test_survey_exact_manuscript_admission_v2.py:299`) contains six subcases: missing, duplicate, and conflicting surfaces for each of manifest and primary. These are six subtests inside one of the 11 reported test methods, not six additional methods.

The two stage negatives (`:253`, `:281`) create a real alternate manuscript/reviews with the same issue/Profile and primary source, then exercise real stage loaders. They isolate manifest identity rather than an unrelated primary or malformed JSON failure. The parent command selects only compatible stage/revalidation tests, so none fails merely because f1 lacks the new keyword parameter. All four raw parent traces end in `StageValidationError not raised` or `AgentControlError not raised`.

The revalidation negative (`:445`) checks State bytes and revalidation-record inventory remain unchanged. The active-record adversarial test (`:481`) refreshes hashes in the synthetic record/State so old-hash rejection does not substitute for the intended downstream admission check. The positive (`:420`) establishes revalidation and then exercises the actual inherited stage path. No authority/Git-success mocks are used in the dedicated module.

## Evidence qualifications and retained limits

- These are synthetic Weekly research/editorial/visual/Human fixtures, real loaders and local Git-aware execution, not actual Human judgments or publication evidence. The existing fixture has a `final_summary` reader-input field (`tests/test_survey_publication_revalidation_v2.py:365`) instead of the publisher's required `final_summary_paragraphs`. The manuscripts used for the alternate-identity witnesses are schema/validator-valid, but the fixture does **not** establish a complete publisher-valid reader input. Increment B must resolve that independently; this review does not accept reader-input completeness, semantic derivation, supporting-file semantics, or direct-primary semantic closure.
- The swapped-primary case deliberately mutates an already valid manifest into a schema-valid adversarial manifest, then invokes the Gate validator directly. It proves the new manifest/primary equality check; it is not an all-stage positive for a noncanonical primary.
- Final runs used WSL Ubuntu, CPython 3.12.14, jsonschema 4.23.0 and pypdf 6.16.2. Native Windows, real Actions, full CI, all-profile publication, historical editions, and canonical durable Human-Gate round trips were not demonstrated here. No broad historical PASS is transferred.
- The first independent-clone setup failed with a missing promisor object/pack failure. Its exact source argv and numeric exit code were not persisted. The initial 10-test draft had a real fixture-construction error (production builder correctly rejected noncanonical `main.tex`); its failing tail is retained, not a complete raw run. Preliminary green working-tree runs do not replace the final exact-head runs. The diagnostic awk quoting error is separately retained. These omissions do not negate the final bounded evidence, but prevent claiming complete raw records for every preliminary attempt.
- `commands.md` says the exact isolation commands are in `isolation.log`; the latter actually records categories and output rather than literal combined argv. This is a reproducibility qualification, not an admission-code defect. The reviewer additionally inspected current Git root/common directory/config, no alternates, no `.git` symlinks, no multiply linked object files, no inherited `GIT_*` environment, inert origin, and exact identity. Packet parent/original-f1 identities and clean tracked status were reviewed. Untracked Python cache directories are disclosed, not concealed as a completely empty status.
- No net lifecycle-saving estimate is established. Necessary later diagnostics, integration/application prerequisites, independent final acceptance and the canonical seven-point audit remain separate work.

The independent result is therefore **Increment A supported at this exact candidate; B3 OPEN and whole candidate NOT_READY**.
