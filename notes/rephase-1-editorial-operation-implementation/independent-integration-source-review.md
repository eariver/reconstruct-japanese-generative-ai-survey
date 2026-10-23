# Independent integration source review — H correctness after partial Weekly activation (no PASS)

Fresh author-independent source review. No code authorship. No tests, no
imports, no Git writes, no network. Readonly via Read/Glob/Grep only.
L/C/H paused; integrator runs diagnostic only on copied FIX23, not DST.
This review reads latest stable DST
`/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
plus integrator packet evidence; it does not re-execute, does not edit DST,
does not accept harness guesses.

Governing read:

- `outputs/rephase-1-editorial-operation-contract-decision.md` d880 (contract §§4/6/8/9).
- `notes/rephase-1-editorial-operation-implementation/astra-implementation-selection.md` (frozen interfaces/closure).
- `notes/rephase-1-editorial-operation-implementation/independent-draft-h2-review.md` (prior H2, §§1–2 smoke blockers + §§3–4 gaps; used as baseline, not re-argued except where fixed/regressed).
- `notes/rephase-1-editorial-operation-implementation/correction-h3/H3-report.md` (62 lines, claims only; verified against real paths below, not trusted).
- Integrator packet `notes/rephase-1-editorial-operation-implementation/integration-20261021T120000Z/`:
  `smoke-weekly-activation.py:1–286` (harness logic, read as evidence of call order/args, not as correctness proof),
  `smoke/smoke-weekly-stdout22.txt:21–41`, `smoke-weekly-stderr22.txt:1–12`,
  `smoke-weekly-stdout23.txt:21–42`, `smoke-weekly-stdout24.txt:21–42`,
  `smoke-weekly-exit22.txt` (`2`), `smoke-weekly-exit23.txt`/`exit24.txt` (`124`),
  `smoke-weekly-stderr23/24.txt` (empty), `freeze/git-status.txt`,
  `freeze/tracked-modified-sha.txt`, `freeze/untracked-new-sha.txt`,
  `freeze/contract-diagnostics.txt`, `freeze/import-diagnostics.txt`.
  Earlier attempts 1–21 not re-read in full; attempt 22 (exit 2) + 23/24
  (exit 124 after partial activation) are the load-bearing evidence.
  `history/` directory listing only (23 names, no body audit).

Exact DST read coverage (all line numbers DST current, 3303-line H):

- `scripts/survey_editorial_publication_v2.py:1–60` (header/imports/constants),
  `:70–118` (`EXPECTED_ARGV_*`, `ALLOWED_*`, `CONTROLLED_SYSTEM_PATH_SUFFIX`,
  `_resolve_toolchain_executable` head, `_check_blocking_log_patterns` head),
  `:226–473` (`_lexical_rel`, `_safe`, `_check_file`, `_read_bytes_bounded`,
  `_exclusive_write_bytes:331–410`, `_exclusive_write_json`),
  `:502–560` (`_require_scope_bound`, `_verify_staged`),
  `:564–1029` (`validate_editorial_receipt` full, incl. `:657–714` authored/
  before-receipt/accepted, `:715–752` reader/scope/proof/trio,
  `:778–932` route-loader rederivation Weekly/Longform,
  `:933–1029` closure-50/contract/commit/`_verify_head_bytes`/extra-closure),
  `:1030–1121` (`_validate_toolchain_spec`, `_validate_manuscript_spec`),
  `:1124–1394` (`_run_disposable_build` full, incl. `:1216–1255` argv/env,
  `:1299–1341` exec/full-raw/log-patterns, `:1342–1394` PDF/pages/drift/return),
  `:1397–1756` (`prepare_publication`, incl. `:1702–1744` build-record body,
  `:1749–1756` 6-key return),
  `:1759–1811` (`_editorial_closure_rows` 50, `_canonical_closure_names` 22/27),
  `:2147` (`finalize` 2-key return, via grep; finalize body pre/post pins
  sampled at `:1836–1878`),
  `:2580–3027` (`activate_publication` full, incl. `:2631–2665` early
  ALREADY_ACTIVE, `:2681–2698` basis/predecision, `:2883–2970` retained/
  candidate/digest prewrite checks, `:2940–3027` record-write/State-replace/
  postreadback),
  `:3030–3161` (`resume_activation` full, incl. `:3095–3119` orphan/
  INDETERMINATE/before-State/P2V/still-old),
  `:3163–3303` sampled (`verify_activation_history`, `resolve_selection`, CLI;
  full bodies not re-audited beyond prior H2 + H3 claim match).
- API-frozen only (def-line + minimal signature context, no body audit):
  `scripts/survey_editorial_current_authority_v2.py:101–155`
  (`_require_selection_strict`, `observe_current_authority` head —
  confirms `receipt_kind` param removed, strict no-fallback),
  `scripts/survey_publication_set_v2.py` grep def lines (no body),
  Gate/Reader/P3S bodies not re-audited (prior H2 slices + H3 “Gate pure-call
  in H module only” claim checked at H call sites, not by re-auditing Gate).
- Grep-only: H `accepted_refs|BEFORE|load_derivation|closure`,
  `EXPECTED_ARGV|ALLOWED_|_exclusive_write|INDETERMINATE|ALREADY_ACTIVE`,
  `prepare/finalize return`, `STATE_REPLACE|expected_old|observed`;
  P2V `except Exception` (29 hits, sampled `:101–155` for fallback status);
  L `except Exception.*pass|return.*CANONICAL` (no hits).

NOT done: no execution, no import, no fixture run, no Git mutation, no
FIX23 copy read (diagnostic-only copy, per brief not the review target), no
full L/C audit, no Longform body, no R1 body, no whole-matrix claim.

Result: **no implementation PASS**. Partial Weekly activation through
`CANDIDATE_ACTIVE_OK` on attempts 23/24 is real progress (prepare/finalize/
activate/receipt/Gate/candidate all returned success once), but the matrix
is incomplete: repeat (`ALREADY_ACTIVE`) hung (exit 124, stderr empty, no
`REPEAT`/`SMOKE_WEEKLY_ACTIVATION_OK` in stdout 23/24), Longform unrun,
P1/P2V repeat unproven, R1×2 anchor/refuse-after unrun, negatives unrun.
Attempt 22 exit 2 is harness-arg shape (`str` passed to
`validate_candidate(Path)`, `smoke-weekly-activation.py:271` vs
`survey_publication_v2.py:750`), not source — fixed in harness by 23/24
(`cand_path` Path at `:271` equivalent), so not a source blocker.

## 1. Remaining verified blocker — `accepted_refs` equality skipped when before-receipt is EDITORIAL

DST `survey_editorial_publication_v2.py:808–827` (Weekly) and `:878–893`
(Longform):

```
// H comment :808–810 — “before-initial full list must equal ctx;
// before-editorial carries only validation-checkpoint …, so skip full
// equality and rely on retained archive + surface checks below.”
if not before_is_editorial:   // :813, :879
    gen_accepted vs ctx_accepted exact sorted compare → ACCEPTED_MISMATCH
// when before_is_editorial True: no compare at all
```

`before_is_editorial` is set at `:694–699` when the proposal-basis receipt’s
`authored_refs` are `{proposed-publication-authoring, accepted-draft-archive}`
with kind `EDITORIAL_PUBLICATION_SOURCE_V1`. Archive path+sha and surface
bytes are still compared (`:830–844`, `:894–907`, `:849–866`, `:912–930`),
and `validation-checkpoint` vs strict State is still compared (`:709–714`),
but the full `accepted_refs` list from current ctx
(`weekly.load_derivation:805` / `longform.load_derivation_for_readback:874`)
is never compared to the record when the chain’s before-receipt is already
editorial.

Cause: generic before-receipt handling added for repeat (`:666–707`,
correctly accepts both initial `{publication-semantic-input,
drafting-authored-archive}` and prior-editorial roles without demanding the
initial-old role) was coupled to skipping the research-equality check.
Contract requires the opposite coupling: role-shape tolerance, equality
strictness unconditional. Root’s known concern is confirmed on real paths:
**`validate_editorial_receipt` must unconditionally compare current ctx
(new proposed authoring) vs record `accepted_refs` and Draft/archive and
reader, not trust historical P3S alone.** P3S proof (`:745–752`,
`STAGED_SOURCE_REPLAY_VERIFIED` + `observed_refs`) proves the staged trio was
materialized from retained bytes; it does not prove current accepted research
is unchanged. On a second pre-Preview correction (before-receipt =
first editorial receipt), a changed research/contract/archive input that
preserves the staged trio bytes would pass receipt while `ctx.accepted_refs`
differs — exactly the repeat path Longform/repeat/R1 tests must exercise.
Priority 1 before any repeat/Longform/R1 test. No new design proposed here;
the fix is to remove the `if not before_is_editorial` guard while keeping
the `:691–701` role-shape tolerance (initial vs editorial authored roles).

Nonblocking note: first-activation smoke (before-receipt initial) does compare
(`:813–827` executed on attempts 23/24, which used initial before-receipt),
so this blocker did not cause the observed partial-activation hang; it
blocks the *next* tests, not the past partial.

## 2. Unexplained hang — repeat `ALREADY_ACTIVE` exit 124 (no cause claimed)

Evidence: stdout 23 `:39–42` shows `ACTIVATE ACTIVATED`, `RECEIPT_ACTIVE_OK`,
`GATE_ACTIVE_OK`, `CANDIDATE_ACTIVE_OK READY_FOR_PUBLICATION_PREVIEW`, then
nothing — no `REPEAT`, no `SMOKE_WEEKLY_ACTIVATION_OK`. Exit files 23/24 are
`124` (timeout), stderr 23/24 empty. Stdout 22 stops earlier (`:39–41`,
`GATE_ACTIVE_OK` then exit 2 from harness `str`-vs-`Path` at
`smoke-weekly-activation.py:271`, confirmed by stderr 22 `:6–12`).

H repeat path entered is `activate_publication` early-`ALREADY_ACTIVE`
(`:2631–2665`): `resolve_publication_selection` (read-only, no P2V yet),
exact pointer+sha match (`:2641–2646`), strict `validate_agent_state`
(`:2648–2653`), full `validate_prepared_set` (`:2654–2655`, which re-runs
full `validate_editorial_receipt` incl. route-loader `load_derivation:805`
+ `render_main/render_bibliography` + `_verify_head_bytes`-class git
subprocesses `:985–1004` + `pypdf` pages). Initial activate already ran the
same full set once (`:2630`), so a deterministic hang only on the second
identical validation is not explained by code shape alone. H3 moved
`ALREADY_ACTIVE` before P2V/anchor/seq (`:2636` comment, H3-report §2) —
ordering is correct and is not the hang cause on real paths.

No harness guess accepted (per brief): the packet contains no per-call
flushing/timing to isolate whether the hang is in `resolve_selection`,
strict State, receipt `load_derivation`, render, git `cat-file/merge-base/
diff/show`, or `pypdf`. The harness’s `DEBUG_SET_PATH/DEBUG_SET_REF` prints
(`smoke-weekly-activation.py:239–240`, visible stdout 23 `:37–38`) prove args
were repo-relative `str` (matching H `_lexical_rel`), so arg shape is not
the hang cause either.

Priority 2: before Longform/repeat/R1, instrument the repeat call only
(per-call unbuffered markers + subprocess timeouts already present at H
`:1184,1199,1301` for build/version/git paths, but receipt’s
`load_derivation` + `_verify_head_bytes`/`verify_tool_basis` git calls at
`:985–1004` have no H-side timeout — they inherit helper timeouts; capture
which helper never returns). Do not change activation semantics to work
around the hang; do not claim `ALREADY_ACTIVE` proven until a repeat
returns `ALREADY_ACTIVE` with strict State + full set on the record.

## 3. Temporal/hash loops — no strict loop on real paths (non-blocking, with one repeat caveat)

Checked: receipt (`:564–1029`) calls strict State (`agent.validate_agent_state`),
P3S historical (`_verify_staged:745`), route loaders
(`weekly.load_derivation:805` / `longform.load_derivation_for_readback:874`),
closure/contract/commit (`:933–1019`); never calls Gate, seal, activation,
or P2V (`:785–786` comment “we never call P2V here” holds — no `observe_`
call in receipt body per grep). Gate editorial branch (prior H2 slice, H3
unchanged in Gate file) loads the receipt *file* for ref comparison, never
calls H `validate_editorial_receipt` — no State→Gate→receipt cycle.
Seal+State→source-proof direction is receipt→load_derivation→agent-State→L
selection→`validate_seal`/`validate_activation_record` (L-owned); H never
feeds seal bytes back into the receipt’s `load_derivation` inputs (inputs
are `state_rel` + `new_authoring_rel:789–797`, both pinned pre-derivation).
After-activation “current new path” repeat success is structurally possible:
`load_derivation` on active State with NEW second-proposal authoring is the
documented repeat path (P2V true-repeat header at P2V `:120–130` confirms
editorial repeat requires true repeated before-graph, not cosmetic).

Caveat (tied to §1, not a separate loop): because §1 skips `accepted_refs`
equality on editorial-before, a repeat receipt *could* succeed via the
`ctx.surface == reviewed_obj` + archive checks while `ctx.accepted_refs`
drifts — that is a missing-check false-accept, not a hash loop. Fixing §1
closes it without introducing a loop (comparison is dict equality, no
re-entrant validation).

## 4. Declared return counts vs required-keys schema — holds

- `prepare_publication:1749–1756` returns 6 keys
  (`proposal_dir, publication_dir, build{pdf,log,digest}, build_record,
  receipt, manuscript`). Contract §6 declares `-> prepared_paths` without
  enumerating keys; harness consumes only `publication_dir`-derived paths
  plus printed JSON (stdout 23 `:32`), no key-count assertion — no mismatch.
- `finalize_publication:2147` returns `{"set_ref","set_sha256"}` (2 keys).
  Harness `:227–238` reads `set_ref["set_ref"]` then `DEBUG_SET_REF` prints
  the same 2-key dict (stdout 23 `:35–38`) — matches. No missing-key failure
  observed through `FINALIZE` on 23/24.
- `activate_publication:3027` returns
  `{"status","record_path","state_path","observed"}`; `resume:3161`
  `{"status","record_path","state_path","observed"}`; `ALREADY_ACTIVE:2661`
  returns the *record* path from the State pointer (not the seal path —
  `:2657–2661` comment correct). Harness `:252–254` handles `str|Path`
  `_set_path` and asserts `ACTIVATED` (`:254`, stdout 23 `:39`) — holds for
  first activation. Repeat return shape unproven only because the call hung
  (§2), not because the shape is wrong.
- Build record body `:1716–1737` declares all 13 schema keys
  (`schema_version,kind,issue_id,proposal_ref,staged_manifest_ref,recipe_ref,
  declared_inputs{primary,bibliography,style},recipe{fixed_steps},
  toolchain{executable,versions,argv,env},outputs{pdf,log,digest},
  exit_code:0,recorded_at,build_sha256`) with `build_sha256` over the body
  minus itself (`:1738`) and `validate_instance` pre-write (`:1741–1743`) —
  H2 §1 list-of-lists defect is fixed on real paths (`recorded_argv` flat at
  `:1245,:1384`, spec-exact check at `:1243–1244` + spec validator
  `:1056–1058`). `PREPARE` succeeded on 23/24 (stdout `:32`), confirming the
  schema gate passes at least once.

## 5. Build validation — actual guards/recipes/sorted-names/env-array/output body hold

- Guards: staged trio exact `{main,bibliography,style}` (`:1131–1136`,
  receipt `:756–757`, seal/finalize equivalents); pre/post pins
  (`:1168–1177`, `:1357–1370`); recipe markers (`REQUIRED_RECIPE_MARKERS:74`,
  enforced `:1086–1088`,`:1164–1166`); blocking log patterns
  (`_check_blocking_log_patterns:166`, enforced `:1341` on
  `logs+main.log`); PDF/log existence+regular+nonempty (`:1321–1334`); `pypdf`
  strict `>=1` (`:1344–1355`); exit-0-only (`:1314–1316`, `exit_code:0` in
  record `:1735`).
- Recipes: `EXPECTED_ARGV_LUALATEX_BIBER:70` / `EXPECTED_ARGV_LATEXMK:71`
  flat tuples; spec must EXACT-equal expected (`:1056–1058`,
  re-checked at build `:1243–1244`); executed `cmds` use absolute
  exe/companion (`:1218–1238`); recorded `argv` is the bare flat tuple
  (`:1245`, returned `:1384`, stored `:1729`) — schema `array<string>` holds.
- Toolchain exe: `_resolve_toolchain_executable:121` (link+real+sha pin,
  stable recheck `:1151–1153`), companion same-dir resolution
  (`:1226`,`:1233–1236`), no `PATH`/shell lookup. Versions recorded with
  controlled `PATH=bindir:/usr/bin:/bin` (`:1182`,`:1199`,`:1249`), no ambient
  `TEXMF*/TZ/LANG` merge (H3 fix holds — `allowed_env` starts
  `{"PATH":…}` at `:1249`, spec `PATH` refused at `:1253–1254`).
- Sorted names / env array: closure rows sorted-unique + `path==name`
  (`:1779–1793`); build `env` recorded sorted (`:1385`
  `{k: allowed_env.get(k) for k in sorted(allowed_env)}`); `argv` flat list
  (`:1384`). Output record body 13 keys + `recipe_ref` hash + declared
  inputs/outputs with `file_ref` bytes (`:1730–1733` via `_safe`+bounded
  read+`stat`), `exit_code` const 0, digest-minus-self — matches
  `editorial-publication-build-record-v2.schema.json` shape (prior H2 review
  scope; no schema re-audit needed).
- Full-raw preservation: `full_raw` per-cmd `{cmd,exit,stdout≤1M,stderr≤1M}`
  (`:1304–1307`), human `logs` full (`:1309`), failed root preserved with tmp
  path in error (`:1316`,`:1325–1370`), no `rmtree`/truncation (grep: no
  `shutil.rmtree` in H; `import shutil` already removed per H3-report §2,
  confirmed at DST `:18–27` imports — `shutil` absent).

## 6. Safe-write positive proof — preflight/final boundaries incl. State-by-proxy hold

- `_exclusive_write_bytes:331–410` + `_exclusive_write_json:437…`:
  `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW` (`:375–381`), no exists-check trusted
  (`TARGET_EXISTS:382–383`), short-write loop/fsync/`fstat` identity
  (`:390–406`), same-fd lseek+readback byte equality (`:407–…`), final
  re-read pin, never unlink unknown/partial. `parent.mkdir(exist_ok)` at
  `:342` precedes the post-mkdir ancestor `lstat` walk (`:346–374`) —
  pre-existing TOCTOU note from prior H2 §5 retained as non-blocking
  single-writer qualification; healthy-fixture smoke unaffected (prepare
  `P/publication` absent-check + exclusive build3/manuscript/receipt/record
  writes all succeeded on 23/24).
- Preflight/final boundaries: every receipt input (`:610–617`), proposal/
  staged/retention/scope (`:502–518`,`:544–545`), closure rows (`:1781–1783`),
  build inputs pre/post (`:1171`,`:1359`), outputs (`:1771`,`:1731–1733`)
  go through `_safe` (lexical-before-resolve + ancestor/leaf `lstat`) +
  `_check_file` (regular + size bounds) + `_read_bytes_bounded`
  (`O_RDONLY|O_NOFOLLOW` + short-read loop). State expected-by-proxy:
  `expected_old` bytes read once (`activate:2617`, `resume:3051`) and passed
  as the expected value to agent `_atomic_replace_state_bytes`
  (`:2981`,`:3134`) with still-old rechecks immediately before record write
  (`:2940–2941`) and before State replace (`:2969–2970`, resume `:3118–3119`);
  post-replace immediate readback classifies `old/new/unknown`
  (`:2992–2996`, resume `:3142`) with primary+secondary preserved
  (`:3025`,`:3160`), never deleting the record. No expected-hash blessing
  (comparisons are byte equality vs passed `data`/`expected_old`, digests
  recomputed minus-self).

## 7. Orphan resume — no direct unknown-State overwrite (holds on real paths)

`resume_activation:3095–3099`: `supersedes != state_pointer` (and not both
null) → `INDETERMINATE` with `observed unknown`, preserving all bytes, no
overwrite/rollback/adoption. `ALREADY_ACTIVE` (`:3083–3094`) requires exact
`pointer.path==record_rel` + `sha==record_sha_now` plus strict State + full
set, read-only. Orphan install (`:3100–3134`) revalidates full set
(`:3103`), `before_state_ref == current State` (`:3107–3108`), fresh P2V
(`:3112`), still-old (`:3118–3119`), then guarded replace (`:3134`) with
post checks (`:3137–3160`). No path writes State from an unknown pointer.
Untested at runtime (no resume attempt in 22–24 logs), so reported as
source-holds, execution-unproven — not a blocker, must be exercised with an
explicit orphan fixture before whole-readiness, after §1–§2.

## 8. L/C fallback removal — verified where H depends, not duplicated

- P2V `observe_current_authority` signature is now
  `(root,state,proposal,manifest,scope=None)` (`:120–122`, no `receipt_kind`
  caller-policy param) with strict `_require_selection_strict:105–117`
  raising `SELECTION_INVALID` (never fallback) — R1-integration
  `receipt_kind` bypass is removed at the H-call boundary. Remaining 29
  `except Exception` hits in P2V are local wraps (`_wrap_p1/_wrap_p2r`,
  pin re-raises), not canonical-fallback returns; full P2V body not
  re-audited per brief.
- L `survey_publication_set_v2.py`: targeted grep for
  `except Exception.*pass|return.*CANONICAL` finds no hits — the LC-review
  §3.1 fail-open swallow pattern is not present in that grep shape. Full L
  body not re-audited; H correctly treats every L call as fail-closed
  (`hasattr` exact-need checks at H `:2608–2610`,`:3043–3045`; every L call
  wrapped to `*_BEFORE/RECORD_INVALID/SELECTION_BEFORE`, never swallowed).
- H call compatibility (frozen only): H passes 5 positional args to P2V
  (`_require_scope_bound` → `observe_current_authority(root,state,proposal,
  retention,scope)`), `str|Path` to P3S `verify_staged_source`, `Path` to
  Reader/Gate/quality/candidate validators per their `Path` params — all
  match current def lines; the attempt-22 `str`-to-`validate_candidate`
  failure was harness-side (`smoke-weekly-activation.py:271`), not H
  (H always passes `_safe(...)` Paths, e.g. finalize candidate
  validation sites). No H-side fallback remains (grep: no
  `setmod.activate_selection/write/resume/verify` calls; `hasattr` only for
  real-helper exact-need).

## 9. Scoped nonblocking cost/performance concerns (do not gate smoke)

- Receipt does full route-loader rederivation + render + closure-50 pin +
  commit ancestry + filtered 22/27 `_verify_head_bytes`/`verify_tool_basis`
  + extra-closure git `show` per row on *every* `validate_editorial_receipt`
  call, and `validate_prepared_set` + activate/resume call receipt multiple
  times per operation (activate: `:2630` + post-replace revalidation;
  ALREADY_ACTIVE repeat: `:2654`). On healthy fixtures this is seconds, not
  minutes; on repeat-heavy operation (second correction + resume + history)
  it multiplies. Acceptable for correctness-first integration; revisit only
  with measured timings after §1–§2, never by caching scope/closure across
  prewrite boundaries (genuine fresh P2V/scope at each boundary must stay).
- `full_raw` retains ≤1 MB stdout+stderr per build command in memory
  (`:1307`) plus full `logs` strings (`:1309`) — bounded and necessary for
  failure preservation; no change needed unless multi-hundred-MB TeX logs
  observed (none in 23/24 REAL TL2026 build, which produced a valid PDF).
- Controlled `PATH=bindir:/usr/bin:/bin` + explicit `HOME`-only-if-documented
  is correct isolation; if future TL2026 companion (perl `latexmk`) needs
  more OS helpers, add them explicitly to `CONTROLLED_SYSTEM_PATH_SUFFIX`
  with version pins, never by restoring ambient `PATH`.

## 10. Priorities before Longform / repeat / R1 tests

1. **Fix §1 unconditional `accepted_refs` compare** (H `validate_editorial_receipt`
   `:808–827`/`:878–893`). Required before second-correction repeat,
   Longform repeat (same skip shape), and R1×2→correction (cumulative anchor
   with editorial-before). Keep `:691–701` role tolerance; delete the skip.
2. **Explain §2 repeat hang with per-call evidence** (not a harness guess):
   rerun repeat-`ALREADY_ACTIVE` alone on the activated FIX23 copy with
   unbuffered markers around `resolve_selection` → strict State → full set →
   receipt `load_derivation` → render → git helpers → `pypdf`, plus helper
   subprocess timeouts surfaced. Do not proceed to Longform/repeat/R1 matrix
   until one repeat returns `ALREADY_ACTIVE` read-only (or a code defect is
   filed with the hanging call identified).
3. Then, in order: Longform initial activation (exercises `:867–930`
   `canonical_reader_bytes`/`validate_heading_syntax` path unrun so far);
   explicit second pre-Preview correction (exercises §1 fix + P1/P2V
   repeat before-graph); explicit orphan-resume fixture (§7 execution proof);
   R1×2→correction cumulative anchor + refused-after-activation
   (needs L/C anchor + refusal paths, H already refuses canonical writer
   pre-write per selection — verify, don’t re-audit L/C here); full
   negative matrix on public callers only after 1–2 green.

No final implementation PASS claimed: first-activation positives
(prepare/finalize/activate/receipt/Gate/candidate + `INERT_HEALTHY` on
23/24) are single-route, single-attempt, synthetic-review evidence with an
incomplete matrix (no repeat, no Longform, no R1, no resume, no negatives,
no regression). Synthetic semantic/visual reviews in the harness
(`smoke-weekly-activation.py:211–218`, `reviewed_by="smoke synthetic …"`)
are visibly synthetic and are not genuine approvals; H never generated PASS
(runtime `REVIEW_NOT_PASS` + Gate editorial-derivation enforcement hold).
Whole-readiness, audit, Human adoption, and work-savings remain open per
contract §10.

(End — readonly source review; one new file only; L/C bodies not duplicated
except API-frozen call-compatibility as cited.)
