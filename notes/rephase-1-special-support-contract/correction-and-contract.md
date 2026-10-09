# LONGFORM_SPECIAL correction + finite contract (before code; analysis.md preserved)

Fixed 409b292/tree 8ce36998 at `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` (HEAD/tree verified,
tracked clean, inert origin, shallow). Read-only; no code/tests/network/agents, no AGENTS/old-packet edits.
`analysis.md` stands except as corrected below. Whole candidate NOT_READY, step4/B3 OPEN.

## C1. Generation entrypoint correction (finding 1)

- Public entry is `scripts/run_semantic_publication_v2_interactive.py` (blob ba5aaacb): `_prepare_revision:23-64`
  parses `--repo-root/--state/--input`, returns without deletion unless exact RELEASE_CANDIDATE +
  `next_action PUBLICATION_PREVIEW` + pending gate + no provenance:32-39; only then unlinks 8 owned outputs
  (main.tex/references.bib/jgaisurvey.sty/longform manifest+input/preflight/subject/empty-wrapper:46-63,
  symlink/non-file refusal:58-63), then calls `_base.main():67-68`. Traced only; not executed.
- `_base.main:122` (blob 4aa20a4b) demands `next_action stage:semantic-publication-validation` for the initial
  route, but `config/survey-production-v2.json:330-333` sets DRAFT_COMPLETE handler to
  `stage:reader-publication-validation`. So base initial guard as written does not match configured initial
  handler; existing generation code != demonstrated supported initial route. Do not proclaim dead globally:
  the mismatch may be an obsolete literal (cf. B decision on the same stale literal) or a genuinely unsupported
  initial path — Astra decides after a real-caller check, not from this analysis.
- Base writes `main.tex/references.bib/jgaisurvey.sty/validated-source-manifest/preflight` at :187-205 with only
  `preflight_tex` + no-write guards, and **no persisted pre-TeX Reader-Surface semantic-review Gate** before
  those writes (no Gate/review call in base file). `normalized_revision.review_reference` is free text
  (`_nonempty`, base:85), not a persisted review record. Pending-revision deletion above is a revision-retry
  convenience, not certification; do not certify pending behavior.

## C2. Accepted-authority limit; Thematic-only renderer (finding 2)

- Base :154-186 resolves cited DIDs against `acceptance.parent/interactive-evidence.json` rows (:156) for
  entity/materiality/status, with `row.sources` fallback and single-`source_bindings` inference (:170-178).
  There is no exact hash binding shown from each bib/prose row back to its accepted Evidence card bytes and
  Draft refs (contrast B's receipt + `_refs` placement replay). Current limit: HOLD/NEEDS_MORE/canonical-URL
  presence checks, not accepted-card replay. Do not label all bib/longform prose "accepted by construction".
  No SourceMap/DM-016/17 blanket repair selected here.
- Generated renderer is Thematic-hardcoded: `_kicker THEMATIC LINEAGE` (:56), cross-family
  `GLM/Qwen/DeepSeek/Kimi` columns (:138-144), `sp001...` bib keys (:192). Profile enums allowing
  THEMATIC and RETROSPECTIVE_PERIOD != operational proof for both. Distinguish: (i) generated-renderer source
  (Thematic-shaped, above) vs (ii) manual direct API path whose actual callers are
  `reader.build_manuscript_manifest:297-355` (role/path inputs -> sized artifacts, no-overwrite:352-354),
  `reader.build_reader_surface_gate:638-705` (requires persisted PASS review:651-657, builds authority:676-686,
  calls evaluate:695-704), Gate CLI `scan-manuscript/validate-gate/scan-file` (:1844-1896, state only for Weekly
  replay:1855/1861), and stage DRAFT_COMPLETE/VALIDATED_DRAFT exact-binding checks
  (`survey_stage_validation_v2.py:470-521/523-573`, gate with `expected_manuscript_path`:511-518/563-570).

## C3. STYLE scope correction (finding 3)

- STYLE hash binding is NOT missing: `_validate_artifact_ref` sized binding at manifest build
  (`survey_reader_publication_v2.py:221-236`) + Gate `scanned_surfaces` entry for every support file
  (`survey_reader_surface_gate_v2.py:1217-1232`). Correction: missing piece is lexical scan and
  declaration/dependency/semantic coverage — STYLE (`.sty`) falls through the
  `SUPPORTING_SOURCE and suffix == .tex` scan gate (:1752; same in `validate_manuscript_surface:1752`),
  so no `scan_tex` runs on it, and no Special equivalent of Weekly `validate_generated_closure`/
  CURRENT_CLOSURE/build-dir inventory exists. Exact scope: bytes bound, content unjudged.

## C4. Review-target contradiction repaired (finding 4)

- Withdraw analysis.md's mechanical-only exemption as stated: with no defined projection from raw TeX bundle
  to reader values, an "opaque byte change without re-review" rule would assert semantic equivalence without
  a parser. Corrected rule: review target is a **projected reader-value representation**, not the raw bundle.
  Concretely: primary `main.tex` bytes + enumerated declared supports are the *bound inputs*; the *review
  target* is the deterministic projection actually emitted (rendered prose strings, bib field values, cover/
  kicker/box texts passed into style macros, citation placement/order). Anything not in that projection
  (commit hashes in comments, external mechanical metadata files listed explicitly) is OUTSIDE semantic identity.
- Two coherent choices for Astra: (A-conservative, recommended) invalidate semantic review on ANY bound-input
  byte change, and permit reuse-free mechanical rebuilds only for explicitly listed external metadata
  (e.g. receipt-internal digests never emitted into TeX); cost = more re-reviews, no parser, no false
  equivalence claim. (B-IR) build a complete Special reader IR + deterministic renderer proof (Weekly-scale
  investment). No generic "comment/layout change is safe" exemption without (B-IR). Style semantic defaults
  (`\SurveyEditionDescriptor` etc., `jgaisurvey.sty:60-100`) are bound as implementation bytes via manifest+Gate;
  their *emitted values* for the issue are review-target values. Never copy coverage/internal metadata into
  reader semantics unless actually emitted (`special-layout-policy.md:78-85` keeps IDs/provenance out of body).

## C5. Gate route + fidelity limits (finding 5)

- A new Special bundle target is NOT admissible under current `derivation.oneOf` (DIRECT_PRIMARY/PRIMARY_ONLY
  or WEEKLY_GENERATED_V2 receipt). It needs an explicit new `route/scope` + target artifact + producer +
  readback/replay + schema. The "no new schema" claim is withdrawn; budget schema paths below.
- Do not touch `survey_reader_fidelity_v2.py` automatically: current fidelity resolves locations only in raw
  `main.tex` (`parse_longform_blocks`, `validate_reader_fidelity:252-319`) and cannot read included files.
  If SUPPORTING_SOURCE TeX may carry reader blocks, fidelity change is a separate scoped decision with its own
  block-resolution proof, not a free rider.

## C6. No parser overclaim; implementable restriction (finding 6)

- `scan_tex_file:623-636` is leakage lint over masked text (`mask_tex_comments_and_structural_macros:496-537`
  masks only listed `\label/\cite/\Needspace/\documentclass/\usepackage/\bibliography/\addbibresource/
  \input/\include/\pagestyle/\ref` forms:511-526); it is not a dependency parser and knows nothing of
  `\def/\csname/\catcode/\directlua`/computed filenames. A "closed membership list" alone therefore cannot prove
  all executed TeX deps known. Supported-language restriction (selected): Special bound inputs may use only the
  renderer-emitted construct set plus static `\usepackage{jgaisurvey}` / single `\addbibresource{references.bib}`;
  `\input/\include` (any form), dynamic filename construction, and style-internal file reads are refused for the
  supported route; anything else is an explicit mechanical-build prerequisite OUTSIDE this increment (real PDF
  build closure stays separately dispositioned). What this increment CAN claim without a universal parser:
  declared-surface byte binding + leakage lint + exact review-target replay for the restricted language.
  Declared-surface binding is distinct from complete build closure; do not present it as a complete Special PASS.
  No new reviewer/role, no late-PASS reuse, no generic build framework.

## Finite contract option (implementable; hard choices left to Astra)

- Scope: declared-surface binding-only increment for the manual/direct route under conservative (A): exact
  manifest+Gate byte binding incl. STYLE, restricted-language refusal, projected review-target definition,
  persisted pre-TeX review Gate ordering for future generation calls (not retroactively claimed for base),
  new Special `route/scope` + receipt/bundle schema + readback validator + CLI/stage threading.
- Actual path budget (edit candidates, not edits): `scripts/survey_reader_surface_gate_v2.py`
  (Special inventory + STYLE/support scan + new route branch + restricted-language refusal);
  `schemas/reader-surface-gate-v2.schema.json` (new route/scope); `scripts/survey_reader_publication_v2.py`
  (manifest closure validation + build/readback threading); `schemas/reader-manuscript-v2.schema.json` only if
  membership representation must change; new narrow Special receipt/bundle schema + derivation/readback helper
  (Weekly-analog, Special-minimal); `scripts/survey_stage_validation_v2.py` + Gate CLI threading for the new
  route; `scripts/survey_reader_fidelity_v2.py` ONLY if Astra puts reader blocks in included files.
  Base renderer/wrapper changes are NOT in this increment beyond documenting C1's guard mismatch.
- Tests/docs (proposed only): real loader/validator + mutation oracles per analysis.md §5 under the restricted
  language; `tests/test_longform_publication_v2.py` (blob 0a897c71) is fixture-only unit preflight/text checks
  (no State/Git/PDF/production proof) as are layout-string special tests generally; operating role is defined by
  `docs/special-layout-policy.md` (blob 5151fa1e) §4 (assigned-Evidence-only, reviewed artifact SHA-bound,
  new-external-Evidence flag) — a policy constraint, not machine proof.
- Unresolved hard choices for Astra: (i) initial-route guard mismatch — correct literal vs declare unsupported;
  (ii) (A-conservative) re-review cost vs (B-IR) adapter investment; (iii) whether included-TeX reader blocks are
  ever supported (forces fidelity work); (iv) mechanical-build closure prerequisite boundary. No abstract
  "all metadata" target; no code until selection + scoped independent review.
