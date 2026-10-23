# Independent final authority resolution — R6 strict source (author-independent)

Fresh AUTHOR-INDEPENDENT resolution. Not author / Worker / root. Scope is ONLY
the R5-directed authority fixes + R6 cross-binding in high/low IO, schema-cache,
agent record/State writer, staged source, and new strict schemas as tasked.
Consumer/export (R5 items 4–5) belongs to the other reviewer and is NOT
duplicated here.

No tests / imports / source edits / network / Git mutation in this resolution.
Only read-only file reads plus read-only Git observation (`rev-parse`,
`status`, `log`, `remote -v`) plus this ONE new resolution file. Mutable DST was
NOT re-read for source excerpts; all source citations are the final strict
SOURCE below. No fix closure beyond what the source shows; no runtime rerun.

## 1. Source identity (exact observed vs manifest — qualified)

Final strict SOURCE (workspace-ignored):

- Root: `.rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60`
- Manifest `notes/rephase-1-editorial-operation-implementation/correction-r6/source-manifest-r6.json`
  claims: `head ce90246b907c86e9bdeb930dec0e83a5637f2805`,
  `tree 53349a4efbdd5e3b4153a8e5975101fdd59f132b`, `count 720`, snapshot `R6-strict`.
- Read-only Git observed (no mutation): `rev-parse HEAD` →
  `ce90246b907c86e9bdeb930dec0e83a5637f2805` (matches manifest);
  `rev-parse HEAD^{tree}` → `53349a4efbdd5e3b4153a8e5975101fdd59f132b`
  (matches manifest, 40 chars); `log --oneline -2` shows `ce90246 SOURCE strict
  R6: ...` on top of `fa0beac SOURCE snapshot: R6 tolerance ...`;
  `remote -v` → `https://example.invalid/workerR4d-r4d-snapshot.git` (inert;
  origin name retains R4d lineage, noted not adopted as ancestry proof).
- Qualification: `status --porcelain=v1` observed `?? scripts/__pycache__/` at
  observation time — NOT clean. If any manifest/packaging claims “no pycache /
  untouched,” that claim does NOT match this observation; tracked-file pins
  (720) were NOT re-hashed entry-by-entry here. Untracked pycache is a packaging
  hygiene condition (remove before freeze), not a logic finding. No runtime
  rerun is claimed.

Governing read: d880 contract decision (§§4/7/9 cited below); root R5
disposition `astra-verification-return-r5.md` (items 1–3 in this scope; 4–5
other reviewer); root R6 adjudication `astra-final-matrix-return-r6.md`
(Candidate↔seal path+SHA cross-binding, reviewed-target rebind, external
outside-permitted); prior `independent-r4d-authority-review.md` §§1–12 +
Appendix A override (CHANGES_REQUIRED on duplicate/close/canonical-State —
this resolution verifies each against R6 source, it does not re-argue them).

## 2. Exact read scope (this resolution) / unproved

R6 SOURCE paths below are under the §1 root:

- `scripts/survey_schema_v2.py`: strict parser `:49–130`, cache
  `:147–209`, strict loaders `:212–263` (fully read for the strict/cache scope).
- `scripts/survey_production_v2.py`: `_strict_object_pairs` + strict
  `load_json` `:121–143` only.
- `scripts/survey_editorial_publication_v2.py` (3920 lines): strict helpers
  `:194–220`; canonical-State `:328–384`; read/write close `:387–561`;
  receipt strict-State + canonical call `:700–759`; seal-roles build
  `:2400–2530`; prepared-set canonical + strict pre-parse + cross-binding
  `:2560–2895`; seq/intent/record/State failure classification (grep-verified
  `:2981`, `:3084–3151`, `:3539–3637`, `:3734–3777`; owned-recheck
  `:3559–3578`). Remainder UNREAD here.
- `scripts/survey_publication_set_v2.py` (2142 lines): file refs `:300–324`;
  seal roles/external `:470–534`; receipt/manuscript/bundle/candidate/gate-review
  bindings `:590–930`; build bindings + chain `:933–1095`; anchor full-union
  `:1647–1736`. Selection/resume bodies beyond cited greps UNREAD here.
- `scripts/survey_agent_control_v2.py`: record writer `:1925–2009`, identity
  `:2012–2030`, State writer `:2033–2114+` (explicit-close scope) only.
- `scripts/survey_editorial_staged_source_v2.py`: verifier docstring + strict
  pins `:1772–1829`; P2V writer/verifier split (grep `:580–700`, `:863–1281`)
  only; role loops (grep `:1259–1757`) presence only.
- Tests/raw read (no execution): `correction-r6/test-r6-crossbinding.py` (full
  205 lines, doc + healthy/seal-only cases), `test-r6-L-focused.py` `:1–120`
  (scope doc + helpers), `test-r6-target-neg-strict.py` `:1–100`,
  `test-r6-target-neg-fresh.py` `:1–100`, `test-r6-malformed2.py` `:1–60`
  (scope docs), `fixture-weekly-r6-external.py` `:1–100` (scope doc + source
  pin argv); raws `r6-seal-only-L-old/new-stdout.txt`,
  `r6-cand-only-L-new-stdout.txt`, `r6-target-rebind-L-new-stdout.txt`,
  `r6-target-neg-fresh/strict-L/H-stdout.txt`,
  `r6-external-consistent-L-new-stdout.txt`, `r6-healthy-control-stdout.txt`,
  `r6-malformed-manuscript-missing-primary-stdout.txt`,
  `r6-malformed-review-missing-manuscript-stderr.txt` (empty),
  `r6-L-focused-summary.json`, `r6-malformed-summary.json`;
  `final-r5b-faults/coverage-table.md` (full 86 lines);
  `final-r5b-faults/matrix_a2.py` `:270–336` (equal-SHA-wrong-path case).
- UNPROVED here: any test execution or fixture run (all raws are Worker-recorded,
  adopted as records not reruns); final two-route/fault matrix completion;
  consumer/export wiring; semantic/visual genuineness; cost. H-side/activate
  halves of the external-positive control beyond the observed L raw are per test
  doc, individually qualified in §6.

## 3. R5 item 1 — strict duplicate before hash validation — FULFILLED as read

Contract §4 exact: “All new records use strict objects
(`additionalProperties:false`), duplicate-key refusal …” (no hash exception).

- Shared parser: `survey_schema_v2.py:_strict_object_pairs:49–60` refuses at
  every object level; `parse_json_strict_bytes:64–88`, `loads_strict:90–100`,
  `load_json_strict:104–122`, `load_and_validate_json_strict:124–143` thread it;
  `load_schema` + `validate_instance` strict-parse schemas first (`:219–220`,
  `:245–246`) so a duplicate-containing schema never last-wins into cache;
  cache (`_get_compiled_validator:172–209`) still holds ONLY compiled validators
  (content-keyed, external-ref skip — §8), no authority/result/instance caching.
- Core: `survey_production_v2.py:121–143` — same hook in `load_json`; valid
  duplicate-free legacy JSON stays valid (hook only fires on actual duplicates);
  no caching added.
- High: `_strict_json_from_bytes:194–209` + `_strict_json_from_text:212–220`
  normalize to typed `DUPLICATE_KEY`/`JSON_INVALID` BEFORE digest/schema; 50
  call sites observed via grep (receipt/state/cfg/proposal/staged/scope/checks/
  bundle/manuscript/reviews/Gate/candidate/build/retention/chain/profile/intent/
  new/post, e.g. `:343, :633, :713, :725, :768, :782, :829, :869, :2073, :2085,
  :2095, :2376, :2638, :2655, :2674, :2687, :2712, :2732, :2748, :2901, :2938,
  :3130, :3195, :3448, :3460, :3583, :3612`), including strict pre-parse BEFORE
  `reader/quality/gate/publication` validators for manuscript (`:2638`), bundle
  (`:2655`), QA result docs (`:2674`), reviews (`:2687`), Gate (`:2712`),
  Candidate (`:2732`). Low independently crosschecks the same discipline:
  `load_json_strict` + `load_and_validate_json_strict` for seal/roles/records
  (`:537, :572, :728, :766`, record `:1020`). This closes the Appendix A A.1 gap
  (high last-wins with fresh hash) in source as read. Legacy-valid-unchanged is
  a code shape (hook fires only on duplicates), not runtime-proven here.

## 4. R5 item 2 — close primary+secondary, no swallowing — FULFILLED as read

Contract §7 table exact: “close/postreplace validation failure | report primary
plus secondary errors and observed old/new/unknown disposition.” §9 exact:
“every record/State write/close/late-readback failure classified …”.

- High read `:387–438`: `READ_CLOSE_COMBINED` / `CLOSE_FAILED`, primary never
  masked, never suppressed. High write `:496–561`: `WRITE_CLOSE_COMBINED` /
  `CLOSE_FAILED`, owned partial/unknown preserved, no referenced delete.
- Agent record `:1936–2009`: explicit `O_RDWR|O_EXCL|O_NOFOLLOW` + manual close;
  primary+secondary ordered, close never masks/suppresses; docstring states the
  guarantee explicitly. Agent State temp `:2052–2114+`: same manual-close
  discipline (`with-open would auto-mask` noted in code). Fsync still typed
  nonzero; no CAS/power-loss promise (docstrings). Observed old/new/unknown +
  never-delete-referenced is caller-side (high `:3552–3637`, `:3734–3777`
  grep-verified), unchanged from the R4d-read shape. This closes Appendix A A.2
  in source as read. Fault-oracle execution itself (R5b `c-record-*`/`c-state-*`
  PASS per coverage table) is Worker-recorded, NOT rerun here.

## 5. R5 item 3 — canonical current State vs separate history — FULFILLED as read

Contract §§4.1/6/7: receipt/set validators claim CURRENT (strict current State,
current research/tools); `verify_activation_history(root, record_path)` is the
separate historical API (no State).

- `_require_canonical_current_state:328–384`: Profile/config
  `source_root`/`authoritative_filename` derivation, exact `state_rel` equality,
  retained/history/cloned refusal (`STATE_NOT_CANONICAL`), no-alias resolve
  check. Called in `validate_editorial_receipt` (`:730–734`, after strict
  State/config parse `:713–728`) and `validate_prepared_set` (`:2569–2579`,
  before schema/digest). Inert-new-set-against-old-current still valid (no
  already-active requirement — docstring + call placement before selection).
  History separateness: receipt/set take `state_path`; history takes only
  `record_path` (signature per prior read + R5 report “unchanged”; history body
  NOT re-read line-level here — qualified). This closes Appendix A A.3 for the
  two current APIs in source as read. Retained-decoy negatives
  (`STATE_NOT_CANONICAL`, CLI exit 2) are Worker-recorded (coverage table
  `A_state_clone_retained` PASS), NOT rerun here.

## 6. R6 adjudication — Candidate-6 ↔ seal-15 path+SHA+sizes/pages, review targets, external placement — FULFILLED as read

R6 rule exact (adjudication §§2–3): compare each Candidate ref to the selected
role by path AND SHA (+ declared byte/page counts where present); same-SHA
different location is NOT interchangeable; reviewed-target rebind refuses even
with fresh enclosing digests; reviews may live repo-contained OUTSIDE
`P/publication/` when refs are consistent (no forced basename).

- Low Candidate-6 (`_validate_candidate_bindings:765–795`): the five named refs
  (`reader_manuscript/source/quality_bundle/semantic_review/visual_review`) +
  `pdf` each require path+SHA equality AND `byte_count` equality with the seal
  role; comment states the R6 fix explicitly (same-SHA different location
  refused). High mirrors it (`:2791–2810`).
- Review TARGETS (`_validate_gate_review_bindings:798–930` + high `:2846–2856`):
  each review’s `reader_manuscript` (exact unsized `{path,sha256}`) must equal
  seal reader-manuscript; `source`/`pdf` (exact sized) must equal seal
  validated-source/publication-pdf including `byte_count`; `page_count` must
  agree with Candidate PDF; `review_kind`/`status`/checks/Profile enforced with
  ONE strict shape, legacy-fallback refused for editorial seal
  (`:819–829`). Gate binds exact manuscript/receipt/early-scope, never
  postrender (`:866–930`, incl. `review_sha256`==early-scope,
  surface==seal-reader-input, scanned surfaces path+SHA+bytes, STYLE via
  SUPPORTING_SOURCE).
- Manuscript trio / bundle / build (`:686–762`, `:933–1015`; high `:2446–2530`):
  sized refs require `byte_count` present+equal, unsized require exact
  `{path,sha256}` (byte_count absent per schema); bundle `production_profile`
  mandatory pinned; build declared unsized-exact + outputs sized-exact. No
  fixture-mode skip (“ONE strict shape, no fixture mode” comments; missing
  mandatory identity refuses — malformed M1 raw confirms:
  `reader-manuscript primary_source must be exact {path,sha256,byte_count}`;
  M1–M3 summary all PASS; M2/M3 individual raws beyond the summary + test doc
  NOT line-verified here — qualified).
- fileLocation vs TARGET identity (distinct, as tasked): seal role `path` is the
  artifact fileLocation; review-internal `reader_manuscript/source/pdf` are the
  reviewed TARGET identity. R6 refusals fire on TARGET path mismatch with SAME
  SHA: L rebind raw `publication set semantic-review reader_manuscript must
  equal seal reader-manuscript (path+SHA)`; L fresh raw identical; H fresh raw
  `CANDIDATE_INVALID … semantic review manuscript drift` (via strict State →
  seal → Candidate chain); H strict raw identical class. Old UNEXPECTED_PASS is
  preserved as record (`r6-seal-only-L-old-stdout.txt`: `L_UNEXPECTED_PASS`) and
  the same fixture now refuses (`r6-seal-only-L-new-stdout.txt`: `candidate
  semantic_review must equal seal semantic-review (path+SHA)`; cand-only new
  identical). Field/path binding, not digest preemption.
- External placement: low `:512–526` permits semantic/visual review paths
  repo-contained OUTSIDE `<P>/publication` (lexical safety + exact
  Candidate↔seal path+SHA binding; inside-only NOT required; fixed
  source/manuscript/build/Candidate paths stay exact `:496–511`); high
  `_seal_roles:2413–2419` takes review paths FROM the Candidate binding (no
  forced basename/relocation). Control observed: actual public Weekly finalize
  with reviews under `<P>/external-reviews/` (fixture script scope doc) then
  `L_PASS 2026-W37` raw (`r6-external-consistent-L-new-stdout.txt`); H-validate
  + activate halves are per test doc (`test-r6-crossbinding.py:22–27`), their
  individual raws NOT re-verified here — qualified, not claimed beyond L.

## 7. Remaining invariants (still present as read; Low/H crosschecked, not comment)

- Orphan: `_next_record_seq` predecessor+1 (grep `:2981`), `RECORD_COLLISION`
  ordinary-refuse (`:3386`), `_refuse_if_intent_exists` + `INTENT_COLLISION`
  (`:3084–3151`), call order (`:3376–3443`), create-failure collision
  (`:3544`); agent `_record_identity_matches` inode+bytes (`:2012–2030`) used at
  `:2467, :2556, :2604` (grep). Owned-inode pre-State recheck read at
  `:3559–3578` (symlink/inode/bytes, same-byte foreign swap refuses,
  `RECORD_OWNERSHIP`/`EXPLICIT_RECOVERY`, preserved). Full activate/resume body
  flow beyond cited lines NOT re-read here; behavioral orphan/resume/already/
  indeterminate evidence is Worker-recorded (coverage-table Group C PASS), NOT
  rerun — qualified.
- Cache: schema bytes parsed fresh + instance+format validated every call
  (`:212–263`); `_CACHE` holds compiled validators only, content-keyed, LRU-64;
  `_has_external_ref` covers `$ref`/`$dynamicRef`/`$recursiveRef` non-`#`
  (`:147–209`, recursive). Fresh-schema/fresh-instance, not authority/result.
- P3S / role loop: verifier `verify_staged_source` docstring “No P2V, no
  current-State validation, no HEAD comparison … retained bytes only”
  (`:1774–1778`) with strict pins (`:1793–1829`); writer-side fresh P2V calls vs
  verifier-never (grep `:580–700`, `:863–1281` presence only); staged trio role
  loops iterate fixed expected outputs (grep `:1259–1757` presence only). No
  current-before/after-active in the verifier as read. Full P3S re-proof NOT
  re-verified here.
- Anchor: `_full_original_union` over ALL checkpoint rows + `_anchored_canonical7`
  projection to exactly 7 with research-rebind refusal and SHA-before-size
  (`:1647–1736` as read). Chain/cycle/depth behavior per cited `:1023–1095`
  presence; R1×2 anchor replay NOT rerun here.

## 8. Remaining blocking code conditions (explicit; no downgrade)

1. Packaging hygiene (non-logic, must clear before freeze): untracked
   `scripts/__pycache__/` observed in the R6 SOURCE (§1). Not a cross-binding
   defect; still, a “clean / no-residue” packaging claim must NOT be made until
   removed and re-observed. No other tracked-byte claim is made here (720 pins
   NOT re-hashed).
2. Evidence incompleteness (not code): final two-route operation on the ce90246
   epoch, R1×2 anchor/refuse-after, active-vs-historical readback, remaining §9
   negatives (per R5-report §5 + coverage-table INCOMPLETE + R6 adjudication §4:
   accepted-ref mismatch on inert target with fresh digest, public prepare
   failure/extra input, chain depth32/cycle handling, export full execution,
   P1/retention/current-authority/staged suites on ce90246), plus the owning
   reviewer’s consumer/export resolution (R5 items 4–5). Individual M2/M3,
   external-positive H/activate, and history-body lines are qualified as above.
No other blocking code condition was FOUND in the read scope (§§3–7). This is a
bounded source statement, not a downgrade: any matrix failure reopens the
verdict. No further code changes are planned on this scope unless such a
blocker appears; packaging (pycache removal + manifest re-observation) is
expected regardless.

## 9. Verdict

Code/source **BOUNDED PASS ONLY**: the R5 items 1–3 + R6 cross-binding
requirements listed in §§3–6 are fulfilled IN SOURCE AS READ at ce90246
(strict duplicate before hash on all new H records/specs/external results with
valid legacy unchanged; close primary+secondary with no swallowing; canonical
current State at both current APIs with history separate; Candidate-6 ↔ seal-15
by path+SHA+declared sizes/pages even for same-SHA alternative paths; review
TARGET ↔ role binding; outside-publication reviews permitted when consistent;
no fixture tolerance or mandatory-identity skip found). Low/H crosscheck each
other’s bindings in actual code, not comments; fileLocation vs TARGET kept
distinct.

This is EXPLICITLY NOT a blanket implementation PASS: whole-operation
acceptance stays pending final two-route/fault-matrix evidence on ce90246,
the separate consumer/export resolution, representative-quality/DM/profile/
audit/Human-adoption dispositions, and clean packaging re-observation. Prior
Appendix A CHANGES_REQUIRED is discharged ONLY for the code conditions above;
evidence conditions remain open. Production NO-GO unchanged.

**Stop. No code/test/build/fixture/source changes made; no runtime rerun; no
new scope proof invented. Ordinary Commit/Push Human-owned. This file is the
ONLY write in this resolution unit.**
