# Evidence correction + qualifications — final22 supplement (append-only, no rewrites)

This file corrects/qualifies records in
`notes/rephase-1-initial-build-integration/final22-integration-20261019T135318Z/`
without modifying any original raw/harness file there. Originals govern where they
conflict with summaries. No source-code changes, no Production actions, no commits.

## 1. N5a label is wrong in JSON; raw governs

`negatives-part1.json` (+ per-route done files) record for `weekly-N5a` and
`special-N5a`:
`{"oracle": {"exit": 1, "matched": "Reviewed surface SHA-256 mismatch"}}`.
The raw oracle output in `weekly/special-n5a-review-stderr.txt` (exit 1) is:
`ValueError: Reviewed surface bytes drifted for sources/<ISSUE>/publication/v2/reader-surface-input-v2.json: recorded <sha>, current disk <sha>`.
The harness (`run_final22_negatives2.py`) correctly asserted the `bytes drifted`
string. The JSON `matched` label is wrong and must not be cited; the raw governs.
(Supplement repeats the reviews at stage gates with the correct expectation text.)

## 2. Stale special base files are superseded, not final

The following base-name files belong to the discarded pre-attempt6 special run
(build succeeded, later review-depth fault) and must NOT be cited as final:
`special-transfer.json` (`1d65eedc…`), `special-qa.json`, `special-state.json`,
`special-surface-compare.json` (`identical:false`), `positive-summary.json`
(`special exit 1`), `special-worker-exit/stdout/stderr.txt`,
`special-pass2-*`, `special-trio.json`, `special-manuscript-pin.json`,
`special-pretex-review-pin.json`, `special-qa.json`.
Final special records are ONLY the `*-attempt6.*` set:
`special-transfer-attempt6.json` (`71a2c98a…`), `special-qa-attempt6.json`,
`special-positive-report-attempt6.json`, `special-main-attempt6.pdf/log/pdf.sha256`,
`special-extracted-attempt6.txt`, `special-page-attempt6-*.png`,
`special-surface-compare-correction.json`.
Weekly final records carry no suffix (single successful run). Do not rename or
delete the superseded base files (failure history); use this index to resolve them.

## 3. N3c repair + partial-set wording withdrawn and corrected

- `negatives-part1.json:special/weekly-N3c` has NO `repair` key (copy left diverged;
  positive fixtures untouched; neg copies disposable). The "24/25 with same-copy
  repair" phrasing is withdrawn. Exact count: 25 negatives total (12 part1 + 8
  part2 + 5 part3); 23/25 carry a same-copy repair + positive control; N3c ×2
  (both routes) prove refusal without same-copy repair.
- Weekly-N3c final oracle is `Publication Candidate PDF authority diverges from
  coupled quality bundle` (candidate binding rewritten to other-route bytes with
  real-hash digest recompute; bundle validates, candidate-vs-bundle comparison
  refuses). The intermediate attempt that also rebound the bundle was preempted by
  `Publication Candidate quality bundle bytes drifted` (preserved in
  `weekly/special-n3*-bundle-preempted.*` where present) — honest preemption, not
  the claimed oracle.
- N7 `partial_set` is 4 present files
  (`jgaisurvey.sty, main.pdf, main.tex, references.bib`: 3 pre-existing trio +
  1 newly written `main.pdf` before the `main.log` PermissionError), NOT
  `[main.pdf]` alone. The README shorthand "after exactly one write
  (`partial_set=[main.pdf]`)" is withdrawn; the inventory in
  `negatives-part3.json` (`immediate_after_inventory`) governs. Supplement C3
  re-demonstrates the same shape with the exclusive helper.

## 4. No-write scope is bounded, not uniform

Explicit unchanged-state assertions exist only where recorded:
N1/N4a/N4b (`watch_unchanged true` over the watched 4–7 files), N3b/N6/N7 and
supplement C3 (`state_unchanged` / `state_qa_unchanged` over watched State/bundle/
candidate rows). N2a stores `after` without a before-comparison; N5a/N5b/N2b/N3a/N3c
rely on repair PASS (revalidation) rather than fault-present byte equality.
Do NOT claim uniform fault-present no-write proof. The supplement stage negatives
(NEG-S1/S2) record exact before/after file-map + HEAD/status equality (no-write proven
there, including that `validate_stage` writes nothing on refusal).

## 5. Orphan N2 rows

`weekly-n2-receipt-{stdout,stderr,exit}.txt` (no a/b suffix) are remnants of the
first naive receipt-tamper attempt (refused at the envelope digest before replay).
`negatives-part1.json` has no generic `weekly-N2` key (only N2a/N2b). Ignore for
final counts; preserved as failure history, not evidence of a 26th negative.

## 6. Lost raw scope (no reconstruction)

The following were deleted by operator cleanup globs/resets during the final22 unit
(the `rm`/`git clean` commands ran in `/tmp/opencode` fixtures and the evidence dir;
sources and committed DBs were never touched):
- `weekly-n2b-receipt-*-envelope-preempted.txt` (naive receipt-tamper refusal
  `… source receipt digest mismatch`): destroyed by overbroad
  `rm weekly-n2b-receipt-*.txt` glob. Message text preserved in prose only.
- `weekly-n3c-rebound-{stdout,stderr,exit}.txt` (rebound-ok step): deleted in the
  N3c rework cleanup. Step outcome (`rebound-ok`, exit 0) preserved in prose only.
- `special-neg-n8-ghost` work copy and `special-n8-*` raws: never created (run
  ordering); N8 evidence lives in `negatives-part3.json` + `special-n8-ghost-write/read`
  raws only.
- `git clean -fd` runs on `jgas-final22-fixtures-…/special-final22` (3×, before
  attempt2/attempt4/attempt6 reruns) + one `git clean -fdx` (before attempt6):
  removed generated authority outputs (chain/state/reviews/pass2/manuscript/gate/
  bundle/candidate/freeze/release files) plus ignored `*.log` (including the stale
  `surveys/special/SP001/main.log` `61d524f7…`, recorded in
  `final22-integration-…/special-stale-log-note.txt`; its bytes equal the preserved
  attempt1 build-dir log). No unique authority evidence lost: all pins/raws had
  already been written to evidence before each reset; SOURCE commits intact.
- Fixture pair history (all preserved, none cleaned since creation):
  `jgas-final22-fixtures-…/{weekly,special}-final22` = RELEASED positives (untouched
  by negatives/supplement). `jgas-final22-neg-…/*` = per-negative disposable copies
  (kept). `jgas-supplement-fixtures-…/{weekly,special}-supp` (attempt1 harness-bug
  failure, chain→pass2 outputs present), `-supp2` (attempt2 pin-path failure, empty),
  `-supp3` (unused; created then superseded by pin fix before any run — clean SOURCE),
  `-supp4` (helper-containment failure at transfer; chain→pass2 outputs present),
  `-supp5` (successful supplement run; RELEASE_CANDIDATE). Orphan
  `jgas-supplement-builds-…/weekly-stage-orphan-unexplained` (3 packet-identical
  files, `899f0f2a…`, timestamped before the run that asserted its absence;
  origin unexplained, content authenticated by sha, preserved aside, never used
  as a transfer source).
- Do NOT reconstruct any deleted file. Do NOT rerun old harnesses (they overwrite).

## 7. Bash-edit deviations (documented, not repeated)

Against the dedicated-editor instruction, mechanical multi-line patches were applied
via `python3` heredocs in bash for: `run_final22_positive.py --only-route/--suffix`
+ checkpoint resume, `worker_supplement_route` pin filenames are NOT among them
(those used Edit). Full list: `run_final22_positive.py` (orchestrator flags),
`worker_final22_route.py` `_Ev` namespacing + `cwd=EVB` + review-evidence mapping +
readback archive path, `run_final22_negatives{,2,3}.py` (new-file staging fixes,
N2a/N5a/N5b oracle corrections, checkpoint files), `transfer_exclusive.py` docstring
line only (code edits via Edit). The faulty-v1/v2 archives + this note preserve what
changed; scripts remain exact-run evidence, not certified rerun tools.

## 8. Measured deterministic checks are narrow, not full QA

The "genuine" QA rows are bounded predicates only: two identifier tokens
(`ISSUE`, `Target Model`) in `main.tex` bytes AND `pdftotext -layout` output;
surface↔draft title/URL mapping for one claim / single DID; `pypdf` page parse
(5) + hash/bytes + workflow log gate on real compiler output; wrapper-body
non-emptiness (1 weekly / 5 special). No full-content, semantic, or density
certification. `AGENT_SEMANTIC/VISUAL` checks exist ONLY as explicitly synthetic
type-fixture review records. Production semantic/visual NO-GO (placeholders,
`example.invalid`, `Unknown`/`Example`, single DID, filler four-family) is unchanged
and independent of this witness.

## 9. Supplement result pointers (new, governed)

- Stage negatives: `weekly/special-neg-s1.txt` =
  `StageValidationError: Reader-Surface Gate validation failed: … MANUSCRIPT_MANIFEST
  does not bind the exact expected Reader Manuscript: expected …-decoy-v2.json …
  got …reader-manuscript-v2.json …` (DRAFT_COMPLETE advance with decoy manuscript +
  decoy reviews + exact gate); `weekly/special-neg-s2.txt` =
  `StageValidationError: Publication Candidate does not bind exact reader_manuscript`
  (VALIDATED_DRAFT advance with decoy candidate). No-write snapshots:
  `weekly/special-neg-s{1,2}-snapshot.json` (file-map + HEAD/status equal).
  Recipient states: healthy checkpoints `…-validated-draft-checkpoint.json`,
  final `RELEASE_CANDIDATE`.
- Transfer helper: `transfer_exclusive.py` (module docstring = exact behavioral delta
  vs old check-then-copy). Same helper used for positive transfers
  (`weekly/special-transfer.json`), conflict (`FileExistsError`, no takeover, shas
  unchanged), failed build (`no built main.pdf`, no writes), partial (`PermissionError`
  after 1 write; inventory 3trio+1pdf; State/QA/bundle/candidate unchanged; restore
  in NEW target OK, partial preserved). Raw in `transfer-controls.json` +
  per-control stdout/stderr/exit.

## 10. S2 preempted at line 555, not the Gate site (supplement NEG-S2 preserved as Candidate backstop only)

Per root correction, supplement `weekly/special-neg-s2.txt` records
`StageValidationError: Publication Candidate does not bind exact reader_manuscript`,
which is raised by `_validate_stage_semantics` at the candidate-vs-prior-refs check
(`survey_stage_validation_v2.py` line ~555), BEFORE the Gate check (line ~572).
It is valid evidence that a decoy candidate cannot advance VALIDATED_DRAFT, but it
must NOT be cited as Gate-site refusal. It is preserved unchanged as the Candidate
backstop; no valid-manuscript-alternate reading is claimed for it.

The Gate site at VALIDATED_DRAFT is covered ONLY by the new targeted negatives
(`weekly/special-neg-g-targeted2.txt`):
`StageValidationError: Reader-Surface Gate validation failed: … MANUSCRIPT_MANIFEST
does not bind the exact expected Reader Manuscript: expected
…/reader-manuscript-v2.json … got …/reader-manuscript-decoy-v2.json …`
(that direction: expected = active manuscript from merged refs, got = injected decoy
gate bytes). Reached via real public `validate_stage` after the actual
`_prior_artifacts`/`_merge_artifacts` completed, with a late filesystem fault that
called the original merge first and only then swapped the validated gate file
(seam count asserted == 1; function restored afterwards; no validator error faked,
no Git authority stubbed). Fault-present snapshot shows ONLY the gate file changed
(plus recorded state refs/seam count in `…-neg-g-snapshot-targeted2.json`; no report
file written on refusal). Repair restored only the owned injected bytes (sha-verified);
the same actual stage call then passed (`…-neg-g-healthy-targeted2.json`, report
written as the expected diagnostic). The companion `…-helper-probe-targeted2.txt`
direct-helper mismatch is labeled helper-level only and is NOT counted as stage
coverage. The supplement NEG-S1 (DRAFT_COMPLETE advance refusal,
`expected …-decoy-v2.json … got …reader-manuscript-v2.json` — opposite direction,
same line-572 gate check) stands as the DRAFT_COMPLETE gate-site evidence.
No full-suite rerun, no rebuild (trio pins equal to recorded positive builds),
no source/reconstruct changes, no commits.
