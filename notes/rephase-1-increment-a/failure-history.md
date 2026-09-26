# Failure history and preliminary runs

These outcomes are retained separately from the final exact-head results.

## Independent-copy setup failure

The first `git clone --no-local` attempt against the historical partial-object f1 repository failed before a usable fixture existed. Git reported missing promisor blob `e98f7364d1641ef632e57e86f1cb27ac8e6578d5`, repository-corruption/pack failure text, early EOF, and invalid index-pack output. The exact source argv was not separately persisted; the raw log names target `/tmp/jgas-rephase-freeze-b1b2-before`. This is a setup failure, not an Increment A defect witness. The retained candidate and parent fixtures were instead independent `cp -a` copies whose object files have distinct inodes/link count 1, no alternates, inert origins, and no inherited Git-root overrides.

## Initial dedicated test fixture error

The first 10-test draft run produced 9 passes and 1 error in 8.660 seconds. `test_gate_rejects_swapped_primary_from_exact_manifest` tried to build a Reader Manuscript with a noncanonical primary through the production builder; the real builder correctly raised `ValueError: Reader primary source must be the canonical survey_root/main.tex`. This was a test-fixture construction error, not a product failure. The test was corrected to build the valid alternate first and then create a schema-valid swapped-primary adversarial manifest. The next 10-test run passed.

Retained failing tail (the complete initial raw transcript was not persisted):

```text
ERROR: test_gate_rejects_swapped_primary_from_exact_manifest (tests.test_survey_exact_manuscript_admission_v2.ExactManuscriptAdmissionV2Tests.test_gate_rejects_swapped_primary_from_exact_manifest)
Traceback (most recent call last):
  File "/tmp/jgas-rephase-increment-a-sol-copy/tests/test_survey_exact_manuscript_admission_v2.py", line 323, in test_gate_rejects_swapped_primary_from_exact_manifest
    alternate = self.build_alternate_manuscript(fix, different_primary=True)
  File "/tmp/jgas-rephase-increment-a-sol-copy/tests/test_survey_exact_manuscript_admission_v2.py", line 91, in build_alternate_manuscript
    reader.build_manuscript_manifest(
  File "/tmp/jgas-rephase-increment-a-sol-copy/scripts/survey_reader_publication_v2.py", line 351, in build_manuscript_manifest
    _validate_manifest_semantics(repo_root, payload, suppressions=suppressions)
  File "/tmp/jgas-rephase-increment-a-sol-copy/scripts/survey_reader_publication_v2.py", line 219, in _validate_manifest_semantics
    raise ValueError("Reader primary source must be the canonical survey_root/main.tex")
ValueError: Reader primary source must be the canonical survey_root/main.tex

Ran 10 tests in 8.660s
FAILED (errors=1)
```

## Preliminary green runs

- The corrected 10-test dedicated draft passed in 8.881 seconds.
- Before the requested cardinality/readback additions, 71 tests across the then-current dedicated and affected modules passed in 80.690 seconds.
- After adding missing/duplicate/conflicting cases for both surface kinds and active-revalidation readback, an 11-test preliminary dedicated run passed in 12.099 seconds.

Those runs were working-tree checks and do not replace the final exact-head logs.

## Full application-patch cached check diagnostic

The full patch was generated directly by `git diff --binary 774dd39a951c9ac3818e83dfffd4c7666efb0a20..1a9649129d1745fed0b98db46ef15f014407e6fc`, and its saved SHA-256 matches a fresh rendering. A later temporary-index `git apply --cached --check` emitted `invalid object 100644 10598cd8723c9cdfdf455d4e5391f91bf95b1a9c for 'sources/2026-W32/candidates/README.md'` because the inherited historical repository is a partial-object clone missing that unrelated promisor blob. Git returned exit 0, but this is not recorded as a clean application proof. The f1 delta patch separately passed `git apply --check` in the independent f1 parent repository.

## Diagnostic command quoting error

An early one-line inode diagnostic embedded awk `$1` in a PowerShell double-quoted command, so PowerShell removed `$1` and awk emitted `syntax error`. This did not affect any repository. The final isolation command used `find ... -links +1` and completed successfully.
