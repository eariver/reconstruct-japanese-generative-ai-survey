# Increment B — independent scoped resolution review

2026-09-26 JST. **SCOPED RESOLUTION PASS for B-IR-01 and B-IR-02 at the exact successor below.** No additional blocking finding was identified in the six-path correction delta. This is a fresh independent reviewer, separate from candidate authors, test executors and root's author-side review. It is not a fresh full Increment B implementation review, canonical seven-point audit, application acceptance, adoption or Human approval.

The prior Auditor's [independent review](independent-review.md) remains preserved as **IN PROGRESS — no final successor judgment**. That reviewer was no longer live when this task was assigned; this report does not infer a latest stop reason. Its broader implementation observations remain that Auditor's work, not newly performed or silently finalized by this reviewer. This report independently resolves the two named findings and binds their correction/evidence to the final candidate.

## Exact candidate and independent packet verification

- Candidate: `c04f32ad46109403e8a63faaa8394a90ee6b869c`.
- Tree: `7dbcbbdb499ea6c7d33417a16144107320e1fd06`.
- Immediate parent / reviewed initial B attempt: `cb96ab97045b0d0767f38806809d33e383bac73d`.
- Increment A diff base: `1a9649129d1745fed0b98db46ef15f014407e6fc`.
- Fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`; no refresh or production inspection was performed.
- [Manifest](candidate.json): 21 paths, comprising 13 runtime/schema/style and 8 test paths.
- [A-to-successor patch](increment-b.patch): 287397 bytes; SHA-256 `bdff2c296867b31dbc2946526ec97490c054bc48c4ab9a8473eb5ded1248ab81`.

Read-only Git/Python inspection independently confirmed exact HEAD/tree/parent, clean tracked state, inert origin `https://example.invalid/rephase-increment-b.git`, and absence of an alternates file in `/tmp/jgas-rephase-increment-b-sol-implementation`. All 21 manifest paths exactly match `git diff --name-only A..c04`; each packet copy, current worktree file and committed blob is byte-identical with the recorded size/SHA-256. The patch is byte-identical to `git diff --binary A..c04`. This is packet identity verification, not a new application/apply proof or reconstruction of the original isolation procedure.

The complete `cb96..c04` delta was read: `survey_weekly_derivation_v2.py`, `survey_weekly_semantic_publication_v2.py`, the main Increment B integration test, the boundary matrix test, and the two legacy test migrations. No candidate source, fixture, Git object or history was changed and no tests were rerun by this reviewer. An initial read-only display helper requested source lines beyond EOF after its identity/hash assertions had succeeded; the corrected source read and complete packet verification subsequently exited 0. This was a review-display error, not a candidate test failure.

## Finding dispositions

### B-IR-01 — P2 evidence gap: resolved within the selected live substitution obligation

The original gap was that a pure projection variant and a live NONE-mode mutation did not prove substitution between two distinct, actually accepted Discovery IDs with Result refs unchanged. The new [boundary test](changed-files/tests/test_survey_increment_b_boundary_matrix_v2.py), `test_live_accepted_second_discovery_id_rejects_stale_result_refs` (line 150), supplies the missing oracle.

I inspected its fixture hooks and the shared real producer/checkpoint chain. Hooks expand authored Screening/Selection/Architecture inputs before actual producers run; they do not stub validator or acceptance decisions. The test confirms the two accepted Discovery IDs, two Draft Package Evidence inputs, unequal resolved refs, the accepted Result's original deck refs and a positive `load_derivation` baseline. It then changes only the archive's deck Discovery ID, requires the specific `authored deck Discovery placement differs` failure, verifies unchanged State/Evidence/Package/Result hashes, restores the archive and replays the identical positive surface. The relevant [runtime comparison](changed-files/scripts/survey_weekly_derivation_v2.py) is at lines 288–292.

The exact-head final raw log records this method as `ok`. This closes the specific live two-ID oracle gap. It does not turn synthetic research/review inputs into real editorial approval, nor claim every citation placement has been separately exercised through a second accepted edition.

### B-IR-02 — P2 admission defect: resolved under the closed canonical-directory contract

I read the [original inert sibling probe](inert-sibling-probe.patch) and [raw output](inert-sibling-probe.log): the initial candidate accepted an extra `hyperref.sty` through actual receipt and Gate readback, with one test / 148.576 seconds / exit 0. This establishes admission of an undeclared local dependency; it does not establish executed TeX shadowing or changed PDF output.

The correction matches the selected [contract addendum](../../outputs/rephase-1-increment-b-contract-decision.md):

- [Directory validator](changed-files/scripts/survey_weekly_derivation_v2.py), lines 73–96: bind the raw Profile directory to its physical canonical path; reject symlinked components, non-directories, and any entry outside the three declared regular inputs (`main.tex`, `references.bib`, `jgaisurvey.sty`) plus the regular non-input outputs (`main.pdf`, `main.log`, `main.pdf.sha256`). Directories, symlinks including dangling links, and auxiliaries are rejected; a missing directory or partial allowed set is permitted for producer preflight.
- Receipt replay, lines 673–681: require all three output paths to equal the accepted Profile's canonical `survey_root` paths before applying the directory guard. A same-byte, freshly rehashed decoy directory cannot select the inventory being inspected.
- [Publisher](changed-files/scripts/survey_weekly_semantic_publication_v2.py), lines 120–153: run the guard before generated TeX/Bib/style/receipt writes; preserve review requirements and no-overwrite checks. The previously materialized reader-input JSON is outside this particular no-write assertion.

The [main integration method](changed-files/tests/test_survey_increment_b_weekly_derivation_v2.py), `test_accepted_weekly_two_pass_publication` (line 313), uses real receipt/Gate validators. Its added assertions establish producer no-write on the undeclared package, clean generation after removal, successful admission with the three permitted publication outputs, and rejection of package/class/config/aux/bbl/directory/allowed-name-symlink/dangling-symlink entries. The physical-directory alias negative calls the guard directly; it is not represented as a separately State-adopted symlink Profile. The rehashed identical-output decoy is rejected by both actual receipt and Gate validators. These are subtests/assertions inside one method, not additional independent matrix methods.

The [focused correction run](closed-inventory-focused.log) records one method / 206.633 seconds / OK / exit 0; its development evidence is supplementary. The final exact-head matrix again records the complete corrected integration method as `ok`, providing successor binding. The mechanism and its selected negatives resolve the admission finding without transferring an old-head PASS.

The unchanged Weekly workflow does not establish removal/relocation of ordinary build `.aux`/`.bbl` files before later admission. Their presence deliberately stops admission under this contract. Operational cleanup integration, installed TeX packages, external search paths/tool behavior and actual PDF/visual correctness remain outside this resolution.

## Test migrations and final raw outcome

Both legacy module diffs were inspected. Bibliography checks now exercise the current reviewed-object renderer/schema boundary rather than deleted publisher helpers, retain access-date versus issue/event-date distinctions, key/URL/title/order checks, and use the contract-selected literal `Unknown` author fallback. The B8 historical docstring's organization wording must not be interpreted as proof that the old ad hoc `xAI` field is preserved by this new fixture. The missing-date negative uses a complete derived reader object and fails at its schema boundary. Weekly Evidence tests use real accepted authorities/cards, compare current joined values, retain the status mismatch negative, and distinguish a separate synthetic matrix loader/join negative from canonical checkpoint drift rejection. No runtime validator is weakened by these migrations.

The [final script](final-matrix-c04f32a.sh), [raw log](final-matrix-c04f32a.log) and [exit file](final-matrix-c04f32a.exit) bind execution to the candidate above. The script checks exact HEAD and clean tracked state before running 14 explicit unittest modules. The raw log records Python 3.12.14 and six correction-source/test SHA-256 values, all independently matched to the final manifest. I counted 132 method entries and confirmed **132 methods / 534.724 seconds / `OK (skipped=1)` / `MATRIX_EXIT=0`**, with exit file `0`.

The sole skip is `test_b9_w34_read_only_fixture_regression`: historical commit `6f68fd09955302fd87e5ec0ce77ff06ccaec8448` is unavailable. This is not a passing historical regression, and no history/network retrieval was performed. The raw pre-test `pip show` metadata command failed with `No module named pip`; therefore this run does not independently establish dependency versions through that command. The failure was nonfatal to the following unittest invocation and remains visible, separate from its successful outcome.

Raw artifact SHA-256 bindings:

| Artifact | SHA-256 |
|---|---|
| `final-matrix-c04f32a.sh` | `f885b1a87d951f0b455115bb1135f876fe0c6f67744143930c9d70472148b0d6` |
| `final-matrix-c04f32a.log` | `127c8f3349484e43c2926290115dedf6b144ec0d62f623bd4c826081e7a36fa4` |
| `final-matrix-c04f32a.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |

The initial [cb96 attempt](attempts/cb96ab9/) remains 131 methods / 366.832 seconds / six obsolete-API errors / one skip / exit 1. Earlier integration/setup failures, interrupted work and missing historical evidence retain their original status; the successor result does not rewrite them.

## Judgment limits

The two P2 findings are resolved for the fixed successor and selected scope. Broader independent implementation observations are available only in the preserved prior Auditor report; this supplement does not claim that report reached a final full-review judgment.

Synthetic research, semantic/review records and blank PDF remain synthetic. Pure projection omission/control variants are not separate fully accepted editions; ambiguous Evidence variants and nonreader annotation mutations retain their previously stated authority limits. This is not Windows/Actions/real TeX/Bib/real publication or all-profile evidence. It does not prove publisher CLI regeneration after Core changes, full #495/application integration, a clean full application patch, operational build cleanup, lifecycle savings, whole B3 or canonical seven-point acceptance. Historical RELEASED editions are neither revalidated nor invalidated. **Whole B3 remains OPEN and the whole candidate remains NOT_READY; adoption remains Human-owned.**
