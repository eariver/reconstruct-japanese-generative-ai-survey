# R4d return — narrow source correction (low full-union + helper recipe closure)

## 1. Diagnosis (root hypothesis confirmed in code + fixture)

Failing tests build validation checkpoints whose `artifacts` union is
7 publication roles PLUS upstream rows (e.g. `evidence-accepted`, 8 rows total;
see `test_survey_publication_revalidation_v2._checkpoint_records`). Legacy
records preserve those upstream rows unchanged (writer only supersedes
under-surface changed files, refuses upstream drift). `_anchored_canonical7`
built its `original_map` from `_canonical7_from_validation` (7-only filter),
so every preserved upstream row hit line 1531 `preserved artifact mismatch`,
and the union check could never match. `derive_canonical_anchor` already used
the full union (lines 940-947) and passed — the defect was confined to the
anchored projection used by `resolve_publication_selection` (line 1704).
Reproducing on 0d only proved pre-R4, not pre-existing production.

## 2. Fix (low + no agent wrap + test-only helpers; dedicated edits only)

`scripts/survey_publication_set_v2.py`:
- New `_full_original_union(prior_record, label)`: full (name,path)->sha256
  union over ALL checkpoint artifact rows, shape-checked, dup-refusing.
- `_anchored_canonical7` legacy branch rewritten: validate legacy cumulative
  rules over the FULL union (superseded known + prior==original; preserved
  known + sha==original; union equality), NEW guard
  `superseded name ∈ PUBLICATION_ROLES_7` (research roles never rebind),
  live-verify EVERY effective row via `_verified_row_4key` (SHA before
  byte_count, stored size cross-checked; upstream rows labeled
  `selection anchored upstream`), then project exactly the 7 roles.
  No-legacy branch and `_canonical7_from_validation` untouched.
- `derive_canonical_anchor` legacy loop: added the same superseded-canonical
  guard (research never rebinds); its full-union map building unchanged.
- Agent wrap: assessed NOT needed. Low errors stay fail-closed exceptions by
  design (`_require_selection` propagates); the fix removes the false refusal
  at its source. No agent file changed in R4d.

`tests/test_survey_editorial_correction_proposal_v2.py`,
`tests/test_survey_editorial_retention_v2.py`,
`tests/test_survey_editorial_current_authority_v2.py` (test-only):
- Each source factory (`_make_source_root` / `_make_p2r_source_root` /
  `_make_p2v_source_root`) now copies the exact TRACKED root `.latexmkrc`
  into the temp fixture and verifies SHA equality (no dummy recipe, no skip,
  no test logic touched). Factory `ls-files` prefixes omit the root recipe
  while the new recipe closure (`RECIPE_REF`, Weekly/Longform
  `CURRENT_CLOSURE`, P3S recipe binding) requires it — this gap is ours (new
  closure dependency), hence fixed, not dismissed. Staged helper already
  carried `.latexmkrc` (`UNTRACKED_P3S_SOURCES`) and is unchanged.
- Pre-existing stale `UNTRACKED_*` lists left intact (still valid: files now
  tracked are covered by `ls-files`; the loops re-verify presence+SHA).
  Original P1-9 setup-error shape preserved in
  `correction-r4c/reg-editorial_correction_proposal_v2-stderr.txt` (missing
  `.latexmkrc` via `current_closure`) and copied to
  `correction-r4d/failed-legacy31-*` is the legacy set; P1 original error
  retained in r4c logs.

Prebytes archived in `correction-r4d/` (low, agent, 3 helpers + staged helper
unchanged copy + failed legacy-31 raw). No clean/reset/network/ordinary commits.

## 3. New SOURCE freeze (untouched after commit)

`/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60`
built from b54a1f2 archive + the 4 DST fixed files (byte-verified MATCH):
- HEAD `4191503bfe1bd6aadd90a107dc4fd7c601e53f6c`
- tree `8ecd325c762bd70b37b847ad831234245345aa20` (40 chars, from git)
- 719 files (recomputed, not assumed: fileset == v1 fileset, content diff ==
  exactly the 4 files; no new tests added in R4d).
- Valid JSON manifest `correction-r4d/source-manifest-r4d.json` (719 pins,
  SHA/bytes/mode; tree 40; spot-checks OK). Inert origin, no alternates.
- Snapshot AND regress clone verified `status` clean post-run.

## 4. Authoritative runs (fresh clone @ 4191503, no DST authority)

- legacy revalidation 31/31 OK (was 28/31; the 3 anchor errors fixed).
- P1 read-only 9/9 OK incl. `test_r1_mechanical_refresh_owner` (R1 affected
  check; was 0/9 setup errors). No validation-success mocks anywhere.
- retention 25/25 OK. current-authority 14/14 OK. staged 26/26 OK
  (24 direct + o12b/o12f retried with TMPDIR scratch on root disk after two
  EDQUOT setup-copy failures; failures were quota-only, code untouched,
  scratch removed after).
- agent 5/5, state authority 2/2, low set 18/18, schema cache 6/6,
  new fault 4/4 OK (unchanged from R4c; code identical).
- Runtime branch unchanged: `survey_agent_tool_v2.py` byte-identical to
  b54a1f2/restored pre-R4 (`0ff3bd9a`); no automatic whole-PASS claimed beyond
  the suites above. Fixture-embedded receipt checks (R4c weekly/longform
  SECOND_RECEIPT) already cover receipt on the same 7 semantics; R1x2 same-7
  path covered by P1 r1-owner + legacy chain tests.

## 5. Fixtures: no rebuild (coordinate with root)

R4c two-actives + inert references (b54a1f2 epoch) are preserved as evidence
and remain valid: their anchors are VALIDATION_CHECKPOINT (no legacy records),
so the low change does not alter their validation (no-legacy branch untouched);
helper change affects only test fixture assembly, not fixture bytes.
Per instruction, NOT rebuilding: return existing paths only if needed for the
final matrix epoch —
weekly/longform actives + inert roots under `/tmp/opencode/jgas-*-r4c-...`
+ `correction-r4c/inert-manifest-{weekly,longform}.json`.
If root orders a final-matrix epoch on 4191503, the parameterized fixture
scripts (`correction-r4c/fixture-*-r4c-20261021T161000Z.py`) rerun unchanged
against the new snapshot (EXPECT_HEAD/EXPECT_COUNT argv, no stale strings).

## 6. Storage

Removed only my own disposables (smoke clone, superseded regress clone, 4
editorial-build roots from my fixture runs, home scratch). All needed copies,
raws, others' data untouched. /tmp ~80% (quota is the binding constraint;
TMPDIR-on-root-disk used once for the quota-blocked staged pair, then removed).

## 7. Pins for root

- NEW SOURCE: `/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60`
  HEAD `4191503bfe1bd6aadd90a107dc4fd7c601e53f6c`
  tree `8ecd325c762bd70b37b847ad831234245345aa20`, 719 files, manifest
  `correction-r4d/source-manifest-r4d.json`.
- Authoritative clone: `/tmp/opencode/jgas-r4d2-regress-20261021T170000Z/candidate-partial-b40de60`
  @ 4191503 (clean). All raw logs under `correction-r4d/reg-*`.
- Blocker: none new. Narrow correction only; not a Human Commit Point.
