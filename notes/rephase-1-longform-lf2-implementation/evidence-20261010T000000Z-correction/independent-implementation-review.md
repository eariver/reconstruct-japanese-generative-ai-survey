# LF-2I independent implementation/evidence review — CHANGES_REQUIRED

2026-10-10. Fresh author-independent reviewer (not root, not prior General workers).
Read-only identity/source review initially; no broad-suite rerun, no candidate
edits/commits/network/Production actions/old scripts/subagents. No disposable
probe was needed: the single blocking defect is proved statically from saved
source lines (no dynamic execution required to establish absence of a check).

## 1. Identity reviewed (read-only)

- Composite `/tmp/opencode/jgas-lf2-design-20261009T113013Z`:
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
  Status observed read-only: 2M + 7A + `__pycache__` side effects, matching
  packet claim (caches disclosed separately, not claimed untouched).
- Final 9-path pins verified by direct `sha256sum` read (match
  `hash-manifest.json` / runner EXPECTED):
  - `scripts/survey_reader_surface_gate_v2.py` `e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4`
  - `schemas/reader-surface-gate-v2.schema.json` `fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c`
  - `schemas/longform-publication-source-manifest-v2.schema.json` `4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca`
  - `schemas/longform-reader-input-v2.schema.json` `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643`
  - `scripts/survey_longform_derivation_v2.py` `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149`
  - `scripts/survey_longform_generated_v2.py` `d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2`
  - `scripts/survey_longform_semantic_publication_v2.py` `1020e4c60077f47ef77c8deaae67a037c525b05c257f077a2a664cc0498d90e7`
  - `tests/test_survey_longform_derivation_v2.py` `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913`
  - `tests/test_survey_longform_publication_integration_v2.py` `16864fa72f14f25fff257f98a2205df2c0e2a521e62e44a2702ccc0d892e767d`
- Selected contract `4795a586c4fc77ff2cb168ca98216f6ecbb084f26e0fd10268b7c5d6778a36d6` + F1–F3
  resolution govern; DM-021 disposition permits initial + healthy readback only.

## 2. R1–R8 source fixes vs contract (actual code)

- **R1 PASS.** Publisher splits pass1/pass2; pass2 missing-surface refuses
  without silent pass1 (`survey_longform_semantic_publication_v2.py:273-281`);
  pass1 pre-mkdir eligibility refuses undeclared survey entries and
  pre-existing partial outputs (312-316); all derivation/scan/heading/
  render/closure/tool/build-dir/publication-dir preflights precede any
  `mkdir`/write (202-262, 368-416 before 418-419). Same-byte reuse only on
  healthy owned exact bytes (298-310).
- **R2 PASS (bounded).** Publisher `_safe`/`_resolve_contained`/
  `_strict_dir_preflight` (47-125) and derivation `_safe` (173-205) check raw
  lexical leaf `islink` (incl. dangling) before resolve, then ancestors, then
  resolved containment. Tests prove State leaf, input parent, review
  leaf/dangling, directive file/symlink, publication-dir direct preflight with
  immediate `_snapshot` equality. Note: publication-dir is proved via direct
  `_strict_dir_preflight` unit, not end-to-end aliased-`publication/` pass1;
  input-leaf dangling follows the same shared code path as the proved State
  leaf (acceptable bounded inference, recorded as limitation).
- **R3 PARTIAL — blocking, see §4.** Raw exact input bytes preserved
  (212-217; archive write uses `input_raw_bytes` at 472; test asserts
  archived == pre-pass2 raw at 1113-1114). Prospective receipt built and
  schema-validated before any source `mkdir`/write (375-416). `_snapshot_`
  /`_recheck_` before writes and before receipt cover State, every
  `accepted_refs` row, publication input bytes, canonical surface, review
  file, closure and commit (153-189, 370-371, 447-449, 496-501). **Missing:**
  drafting archive (`context["archive_path"]`, receipt `authored_refs[1]`)
  is neither snapshotted nor rechecked.
- **R4 source PASS, test partial (non-blocking).** `_write_bytes_exclusive`
  (132-146) never unlinks; callers retain/report `written + failing`, refuse
  receipt success on incomplete sets, refuse partial retries unchanged
  (429-431, 450-482, 483-501, 505-519 including receipt-write `OSError`).
  Test proves mid-write fault retention (writes half `references.bib`,
  retains `main.tex` + partial `bib`, no receipt, retry refuses). Explicit
  close-failure and receipt-install fault injection are not separately
  demonstrated; both share the same helper/except path, so this is a test-
  strength note, not a source defect.
- **R5 PASS.** `validate_receipt` (665-758) does canonical FILE-byte replay
  (`surface_path.read_bytes() != canonical_reader_bytes(...)` at 741, not
  parsed-object equality), enforces exact edition siblings for reader input /
  archive / receipt (720-730) plus Gate canonical suffix check, preserves
  explicit contained review override, and (F1) itself reloads + validates the
  persisted review (686-697) with same-file-SHA binding; Gate independently
  reloads and binds the same SHA (`_derivation_for_manuscript` Longform
  branch). Fresh-rehash/noncanonical/alt-dir/tampered-output negatives all
  bind replay mismatch, not hash-only oracles.
- **R6 PASS.** `validate_heading_syntax` (256-290) refuses braces/backslash/
  tilde/circumflex in headings and `]`/newlines in optional-arg titles plus
  control chars; canonical package/comment token validated before unescaped
  emission (280-281); `render_bibliography` refuses controls/backslash/braces
  and requires ≥1 entry; `validate_generated_closure` (489-512) is a second
  fidelity-parser traceability barrier. Publisher preflights heading syntax
  before any `mkdir`/write (232-235); replay revalidates. Positive
  punctuation controls and precise no-write negatives proved.
- **R7 substantially PASS (bounded notes).** Immediate owned-tree/`_snapshot`
  equality around each failure before repair; wrong-target/non-PASS/legacy
  review, VISUAL, directive file/symlink, partial-set, snapshot-drift,
  canonical-replay, injected mid-write, actual subprocess CLI pass1/pass2 and
  actual Gate CLI persisted-review path, exact same-issue decoy backstops at
  Gate layer + both stage sites (DRAFT_COMPLETE and VALIDATED_DRAFT) with
  otherwise coherent chains, healthy FROZEN/RELEASED via the normal
  approval/Freeze/Release chain (no `EXCEPTION_*`, no manufactured
  prior-State, `COMPLETE` ghost refuses, default loader refuses FROZEN).
  Mechanical-only rebind proves same reader bytes without claiming a
  regeneration owner. Residual notes (not blockers): no explicit pending-
  establishment State negative in integration (earlier-lifecycle + COMPLETE
  + FROZEN-default refusal cover the mechanism); no malformed-route-string
  no-fallback probe (Weekly/direct-primary negatives live in Gate/contract
  tests); wrong-path same-byte review is shown as permitted explicit override
  with strict binding, not as a refusal case.
- **R8 substantially PASS.** New runner `run_lf2i_correction.py` pins EVERY
  9 hashes/modes pre AND finally-post (`check_identity`), rejects
  `GIT_*`/`PYTHON*` routing overrides, forces `PYTHONDONTWRITEBYTECODE=1` +
  `GIT_TERMINAL_PROMPT=0` for children, captures child returncode/timeout
  directly with exclusive `run.log`, fails postcheck on drift despite child0,
  lists caches separately (retracts old "untouched" overclaim), preserves
  first-return 9 files/modes/hashes + `lf2i-dev1/2.log` + setup-failure packet,
  and builds a complete portable overlay with independent byte-copy
  `git apply --check/apply` exit 0 + zero byte/mode mismatches (no `git
  archive`, partial-DB safe). `apply.log` new-file `git diff --no-index`
  exits 1 are expected difference signals, not failures. Disposable
  pre-drift/child-fail/post-drift proofs are logic-level (hash inequality +
  exit 7) on temp copies only — correctly avoids any real-candidate canary
  but does not exercise `check_identity` refusal on a drifted full copy
  (recorded limitation).

## 3. Patch/apply/runner claims vs old gaps

- Old 191-line 2M-only patch omission is cured: `initial-9/` +
  `initial-9-manifest.json` + `initial-2M.patch` + `initial-complete.patch`
  preserve first-return bytes before edits; `complete-overlay.patch` (2M
  diff + 7A new-file bytes/modes) + `hash-manifest.json` + `apply.log`
  prove full-overlay recovery with byte/mode identity. No object sharing
  claim is made beyond byte/mode comparison onto a fresh byte-copy of HEAD
  blobs (no new HEAD/commit, no fixture/DB mutation).
- Earlier false guard claims (6+33, "both repos untouched") are retracted in
  `evidence-qualification.md`; current manifest asserts only pre/post hash/
  mode + allowed 2M+7A set + separately listed caches, with direct child
  returncode/timeout and exclusive creation (refuses overwrite). `run.log`
  shows 44 tests PASS, exit 0, Python 3.14.4, 1462.728 s. This review does
  not re-execute the suite and does not transfer that PASS as its own
  rerun verdict.

## 4. Blocking finding — CHANGES_REQUIRED

**C1 (R3, source): drafting-archive snapshot/recheck missing.**
`_snapshot_inputs` (`survey_longform_semantic_publication_v2.py:153-165`)
records `state_sha256`, `accepted_refs`, `authored_sha256` (publication input
only), `surface_canonical_sha256`, `closure`, `commit`, `review_sha256` —
but never `context["archive_path"]` (`drafting-authored-archive`, receipt
`authored_refs[1]`). `_recheck_snapshot` (168-188) rechecks those same keys
only. A drift of the drafting archive between `snap_pre` (370) and
before-writes (447) / before-receipt (496) therefore passes both rechecks,
yet `build_receipt` (via `generated.build_receipt` `_artifact` on
`context["archive_path"]`) embeds the drifted hash and the publisher still
exits 0 with an installed receipt whose outputs (pre-drift in-memory
`main_text_pre`/`bibliography_text_pre`) no longer correspond to the
archived authority. Later replay would fail (`independently recomputed
reader input differs`), but the install-time guarantee
("recheck all named accepted/authored/State/reader/review/current-tool
dependencies before writes and before final receipt install") is violated.
*Fix:* add `archive_sha256 = sha256_file(context["archive_path"])` to the
snapshot (via `_safe`-resolved path), recheck it in `_recheck_snapshot`
(same `_safe` + hash compare, stages `pre-write`/`before-writes`/
`before-receipt`), and add a write-seam drift test (mutate archive after
snapshot — e.g. via mocked `_snapshot_inputs`/`_recheck_snapshot` boundary
or direct helper test — proving refusal with no writes and no receipt).
No config, dispatcher, fidelity, reason-taxonomy or Production change is
required for this fix.

## 5. Config-note decision

**Endorsed: `config/survey-production-v2.json` correctly remains unchanged.**
Both new schemas/scripts live under existing `implementation_control_roots`
(`schemas`, `scripts`), so `verify_tool_basis`
(`survey_longform_generated_v2.py:519-582`) already refuses uncommitted
overlay bytes via `git diff --quiet commit HEAD -- control_paths`,
dirty-HEAD and untracked-control checks, plus per-row closure byte equality
against both recorded commit and HEAD. The note documents this pinning
mechanism rather than claiming registration was performed. No config edit
should be invented absent a demonstrated threading gap.

## 6. DM-021 packet check (saved packet only, no refetch)

`intake-and-impact.md` + Astra disposition are correctly bounded: later
evidence (commit `afdb3df3…`, blob `62ee6a6b…`), not baseline adoption;
fixed baseline 774 unchanged; Issue 560 / PR 561 / run 37955511006 /
exception artifacts explicitly unqueried primary records, reported
secondary only; `OPEN_CORE / EDITION_WORKAROUND`, no `CORE_FIXED`, no
`EXCEPTION_*` consumed as fixtures. LF-2I tests contain no
`EXCEPTION_*`/`REVIEWED_EDITORIAL_CORRECTION` strings (verified by grep).
No DM021 overclaim to flag.

## Verdict

**CHANGES_REQUIRED** — single blocking source item C1 above. All other
R1/R2/R4/R5/R6/R8 corrections are accepted as bounded; R3/R7 residual
notes are recorded as limitations, not additional blockers.

## Limitations (not new acceptance)

- Read-only source/packet review only; 44-test PASS is the author's
  evidence (`run.log`/`manifest.json`), not an independent rerun.
- Synthetic accepted-chain + type/identity review/PDF/Human fixtures prove
  only the contract's type/identity route, not genuine semantic/visual
  sufficiency, TeX/PDF build transfer, all-profile viability, or lifecycle
  savings.
- Whole candidate remains NOT_READY; step4/B3 OPEN; canonical audit
  unstarted. No full-publication, canonical-audit, or adoption approval is
  granted by this review.
- No candidate/reconstruct commits, branches, fixtures, refs, network, or
  Production actions were taken by this reviewer.

*Reviewer independence:* fresh scope, no authorship of candidate code/tests,
no prior General/root work in this unit, no relabelling of Worker output.
Exact composite + packet hashes above are the review basis.
