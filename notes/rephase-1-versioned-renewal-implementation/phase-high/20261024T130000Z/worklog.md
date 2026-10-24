# Phase-HIGH+CONSUMER worklog — REAL whole-operation push (append-only, turn 2)

## Turn 2 (continuation): U finalize/activate + C1 finalize green both routes

New H (2871 lines, accumulator + OWN rows) and fixed S (1433 lines, H-derived
scope + renewal predecessors) synced read-only (H/S files NOT edited).
Interface doc `phase-h/integration-interface.md` still carries stale prose
(narrow-unit note §128, S1 incompatibility note §§145-150) — H-owned to update;
function names/signatures listed there all resolve and are consumed as documented.

### HIGH fixes from REAL execution (each found by a failing run, fixed, re-run)

1. `verify_renewal_rerender_equality` now returns `trio_digest` (exact S
   Layer-B formula) — user-directed; inner SAME-proof comparison needs it.
2. REUSED `original_record_ref` = terminal ACTIVATION record (new H chain
   semantics), not build-record.json; `_resolve_reused_terminal_record`
   (bounded 32, same issue, skips intermediate REUSED). Proof's
   `old_build_unit_refs.record` stays the immediate prior build-record (S).
3. Build record validated against embedded `#/$defs/buildRecord` (new
   `_validate_build_record_container`), not the manifest root.
4. QA shape `{"checks": [...]}` accepted (actual file shape) + freshness rule
   (every check `recorded_at >= basis.recorded_at`; stale refused).
5. C split: NEW public `prepare_renewal_targets` (proof/trio/manuscript/real
   build/receipt before external review) + CLI `prepare-targets`; finalize C
   reloads/revalidates prebuilt targets (`BUILD_TARGETS_MISSING` otherwise).
6. Gate semantic input = lineage scope review (`_lineage_scope_path` from H
   verdict) for U AND C (reader unchanged; postrender reviews are wrong shape
   for the gate and go to Candidate/seal).
7. Cross-ref convention audited: FILE SHAs everywhere EXCEPT proof.basis_ref
   (SELF, S-required). Fixed HIGH writers (basis/proof/seal/receipt/record/
   manuscript/Candidate/bundle/Gate refs) + reader/gate byte-compare with
   self-digest recompute kept as defense in depth.
8. U/C trio style source: U = prior path; C = live template STYLE_PATH
   (R trio unwritten at proof time); trio files written before S verify.
9. Absolute-path discipline at all consumer-builder call sites (builders
   resolve against CWD); C manuscript binds NEW R trio.
10. Activation record `core` FLAT (versioned_core: 8 contract fields + impl SHA,
    no nested object); `set_ref` FILE SHA (+ ALREADY_ACTIVE compares FILE SHAs).
11. C manuscript builder forwards own proof context (C-own validation at build).
12. Dead git probe removed; `_write_json_bound` reparse binding (file bytes vs
    object digest distinct by design).

### Exact blockers returned (no bypass; owners fix)

- **proof.basis_ref SELF-vs-FILE** (blocks ALL activate): H `:1594` requires
  proof.basis_ref == record FILE ref; S `:1155` requires == basis SELF digest;
  H `:1580` requires record refs = FILE. Recommend H compares against loaded
  basis SELF at `:1594` (one spot). See `interface-mismatch-proof-basis-ref.md`.
- **H EXECUTED pdf page_count + companions** (same file §3): H code `:1494`
  vs own schema sizedRef; R4-map companions vs strict toolchainVersions.
  HIGH conforms to enforced schemas; companions preserved in
  `R/build/toolchain-companions.json` sidecar pending H fix.
- **S tests** `TestPhaseSHighU.test_high_u_finalize_{weekly,longform}` assert
  ABSENCE of `trio_digest` in HIGH's rerender return — stale after the
  user-directed fix (rerender equality itself passes). S-owned to update.

### Evidence (high21 fixtures T1; high15/17/18/19/20 runs preserved as history)

- U: prepare+finalize exit 0 both routes (run24/run28). U1 R-dirs complete
  (basis/proof/receipt/build/bundle/gate/candidate/seal + fresh QA).
- C1: prepare/targets (REAL 5-page TL PDFs: weekly 61239B `f5f95d9c…`,
  longform 79530B `41fb641d…`; same-trio-different-PDF C case)/reviews-QA/
  finalize exit 0 both routes (run29). C manuscript binds NEW R trio with
  `renewal_source`; seal roles all under R/ except retained originals.
- Activate U/C: exact basis-ref blocker (exit 2 CLI/APIs), R partials inert,
  old pointers unchanged, fixture HEADs unmoved, E uncommitted.
- Failure oracles (run30, STATE-PINNED): F1 RECORD_COLLISION, F2
  BUILD_TARGETS_MISSING, F3 QA_MISSING stale, F4 RECORD_COLLISION wrong-kind
  resume, F5 R1 versioned refusal with zero tracked writes, F6 H r1 chain
  intact (11 bindings).
- Regressions: oracles 9/3skip; publication+quality+gate+stage 60 green;
  pubset+revalidation+freeze+DM004 60 green; S suite 13/15 (2 stale-shape,
  S-owned); staged 26 EDQUOT environmental (unchanged class).

### Explicitly NOT executed (blocked behind H basis-ref fix)

Repeat C→U→U (needs U2 activation), renewal→editorial (needs activated
renewal prior), normal direct lifecycle on renewed sets (needs activation),
ALREADY_ACTIVE/resume on renewal records, H 21-row check on live r2
(H tests pending my activate — will validate once H fix lands). No
independent PASS/adoption. U/C finalize + C1 real builds + failure oracles are
the completed scope; activation-gated items await the one-spot H fix.

---

# Phase-HIGH+CONSUMER worklog — REAL partial, fail-closed (append-only)

2026-10-24. AUTHOR HIGH+consumer worker. RootHEAD c5b0d7c continuation (not a
Human Commit Point). Workdir authoritative:
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
(actual409 `409b292`/tree `8ce36998` + baseline57 + H/S partial, index clean, no
candidate/reconstruct commits; HEAD still 409b292 uncommitted after this phase).
Rejected M1 `.../versioned-renewal-impl-.../candidate-work` (fake root a8890d4)
NOT used as source; preserved untouched. No shell edits to source (Write/Edit
only); no clean/reset/network/saved-runner exec; no reconstruct-DB fixtures.

## 1. Ownership observed (no bypass)

- NOT edited (H-owned): `scripts/survey_versioned_renewal_history_v2.py`,
  4 `schemas/versioned-renewal-*.json`, `scripts/survey_publication_set_v2.py`,
  `scripts/survey_agent_control_v2.py`, `schemas/publication-surface-revalidation.schema.json`.
- NOT edited (S-owned): `scripts/survey_versioned_renewal_source_v2.py`,
  Evidence/Screening/Discovery/X/architecture/drafting/completeness/Weekly/
  Longform route content + weekly/longform `CURRENT_CLOSURE` constants.
- Edited (HIGH+consumer, this phase): NEW `scripts/survey_versioned_renewal_v2.py`;
  4 schemas Reader/Candidate/QA/Gate; `config/survey-production-v2.json`;
  staged `_SHARED`/editorial closure + `test_group_c_editorial_consumers_v2.py`;
  Reader/Gate/QA/publication(freeze incl.)/stage/orchestrator/human_gate/P1
  renewal prior-KEEP block. Reviewed-coherent-no-change: production/profiled
  freeze (active-Candidate selection already VERSIONED_ACTIVE-aware),
  handoff (pins already), agent_tool (avoided path by design), P2R (generic
  retention), P2V (true-repeat rule present), R1 (versioned refusal present),
  export workflows (via publication threading).
- Per-file SHA before/after: `touched-sha-before.txt` / `touched-sha-after.txt`.

## 2. HIGH module (NEW, 2600+ lines, compiles, imports clean)

`prepare/finalize/validate-receipt/validate-set/activate/resume/history` +
`observe_renewal_authority` + `verify_renewal_rerender_equality` + CLI (exits
0/2/1). Entry per root §2: strict no-follow pinned State/config, State vs
`agent.STATE_SCHEMA` before indexing, canonical path via Profile
`source_root` + `state_authority.authoritative_filename` (P1 1575-1583 rule, no
basename), `_profile_and_source` live-live, pure `_require_renewal_entry_window`
(exact P1 414-429), PUBLIC `agent.validate_agent_state` on same LIVE bytes + by
recheck, VERSIONED_ACTIVE selection with nonnull record/set/Candidate, HIST
prior verdict, current tool INFO pins (never vs `state.contract`). No
`verify_state_basis`, no checkpoint resolvers, no Reader/Gate/Candidate/seal/
receipt/P1/P2R/P3S in entry/observe/Layer paths. Exclusive R claim
(`mkdir`/`O_CREAT|O_EXCL|O_NOFOLLOW`), State COPY, inventory (state COPY +
profile KEEP + prior seal-role KEEPs), H-observed bindings verbatim, CURRENT
63 closure member-wise, basis LAST + pin recheck + detached S basis check. U
(`REUSE_TARGETS`, toolchain forbidden, no build) vs C (`RENDER_TARGETS`,
explicit spec, disposable TL build + transfer + `EXECUTED_BUILD`, receipt AFTER
build record). B.4 enforced in finalize + validate-set (NEW files must carry
NEW proof refs, else `REVIEW_TARGET_MISMATCH`). Seal LAST (15 roles,
`VERSIONED_RENEWAL_SET_V1/SEALED_INERT`). Activation: full set validation,
readonly `ALREADY_ACTIVE`, exclusive record, known-byte temp/replace with
primary/secondary error classes, full active readback; resume compares complete
intent; `INDETERMINATE` preserves without rollback/adoption/deletion.
Two HIGH bugs found by REAL execution and fixed (evidence, not hidden):
(a) renewal-dir `mkdir(parents=False)` → `parents=True, exist_ok=False`
(run-20261024T134500Z prepare traceback); (b) file-bytes-vs-object-digest
conflation in 6 write sites → `_write_json_bound` reparse binding
(run-20261024T140000Z `BASIS_DIGEST_MISMATCH`).

## 3. Consumer integration (all compile; regressions below)

- Reader: `renewal_source` XOR branch (C serialized; U keyword-only);
  `renewal_source_proof_ref` keyword on manuscript/review builders+validators;
  nested review→manuscript threads SAME ref; stored-HIST (lineage-reachable via
  public H leaf + prior-seal proof check) vs supplied-CURRENT (Layer-B) vs
  seal-selected-NEW dispatch; stale refusal without proof (N-H1); canonical and
  old-P3S paths verbatim without keyword.
- Candidate/QA: `renewal_source_proof_ref` strict optional branch + digest base
  10→11 / 9→10 (old absent-field behavior intact); validators derive from own
  payload with outer-expected equality.
- Gate: 5th variant `VERSIONED_RENEWAL_V1/RENEWAL_MAIN_BIB_STYLE` (old 4
  verbatim); derivation binds reloaded proof+receipt (no inferred old receipt);
  builder + validator kwargs with SAME-proof/SAME-receipt checks.
- Freeze: proof derived from validated Candidate, threaded to direct review
  loader, bundle equality required; snapshot extended with proof/basis/COPY/
  trio/closure rows (dedup exact, alias conflicts refuse).
- Stage/orchestrator/human_gate: expected proof derived from sole
  State-selected seal; threaded into candidate/gate/review validators.
- P1 before-graph: renewal-receipt prior basis/proof/build KEEP block
  (editorial prior block intact; identical-reader refusal intact).
- Staged/editorial closure 30/14/50 → 35/22/63 (S-owned route subsets
  untouched); config pipeline 67→71 (schemas only; roots/quality unchanged).

## 4. Fixture evidence (NEW byte-independent DBs, genuine changed-tool epochs)

Parent `.rephase-1-editorial-runtime/versioned-renewal-high-20261024T130000Z/`:
`renewal-weekly` HEAD `ada39db` / `renewal-longform` HEAD `ea8203b` (both:
tool-source-only commits before authorities, old 721a04d ancestor retained,
old E uncommitted 10/12, no alternates, inert origins, inodes disjoint —
`run-20261024T141500Z/`). Run-1 failure (clone drops untracked E) and run-2
failure (E list read from clone not source) preserved in
`run-20261024T134500Z/` + worklog §5 notes; failed parents removed (mine,
reproducible; evidence kept).
- Weekly prepare U (`high-u1-weekly`, REUSE_TARGETS): exit 0. Basis
  `c09e9c2e…`, COPY SHA `ca7c0d2e…` == live before-State, namespace
  `…/wk-boot-1`, R partial `{renewal-basis.json, retained/}` inert.
- Longform prepare U: exit 0 (same shape).
- Weekly+longform finalize: exact S1 refusal, API raises + CLI exit 2 with
  `{"phase":"PROOF","code":"REVIEW_TARGET_MISMATCH",
  "disposition":"REFUSED_PRE_WRITE",
  "detail":"accepted-authority assembly failed: REVIEW_TARGET_MISMATCH:
  caller scope-schema observed row refused: scope derives from typed prior
  lineage, not caller rows"}` (`finalize-cli-weekly-stderr.txt`).
- Post-run: fixture HEADs unmoved, LIVE States == before SHAs (old pointers
  unchanged), E still uncommitted, R partials inert-preserved.

## 5. Interface mismatches RETURNED (exact; no bypass built)

- **S1 (S worker, blocks ALL finalize):**
  `scripts/survey_versioned_renewal_source_v2.py:529-531` blanket-refuses ANY
  `basis.observed_source_bindings` row with `schema_path ==
  "schemas/reader-surface-semantic-review-v2.schema.json"` as a caller row,
  but H (`survey_versioned_renewal_history_v2.py:1438+`
  `_derive_editorial_observed_bindings`) emits exactly such O17 `""` rows (11
  NONEMPTY, verified blobs) for every real editorial predecessor. Builder input
  needed: distinguish derived-vs-caller by H-rederived-expected equality (exact
  path/sha/epoch/schema_sha at `staged_head`), not blanket refuse. Proven live
  by §4 finalize refusals (both routes, API+CLI).
- **S2 (S worker, blocks repeat/C→U→U/renewal→editorial):**
  `survey_versioned_renewal_source_v2.py:522-524` raises
  `REVIEW_TARGET_MISMATCH` for ANY renewal predecessor ("returning to root
  before broadening"). Builder input needed: renewal-predecessor scope lineage.
- **H1 (H worker, known ongoing):** versioned-ancestor expected==submitted
  completeness pending high lifecycle (`history_v2.py:1784-1792` narrow-unit
  comment). HIGH consumes the H verdict as-is; no expected rows forged.
- **S-test re-baselining (S worker):**
  `tests/test_versioned_renewal_source_phase_s.py:558-559,616` assert HIGH
  absent (`assertFalse(...exists())`, `assertIn(...omitted)`) — false now that
  HIGH landed (their own "high worker-owned" blocker labels). 2 failures are
  this premise change, not a HIGH defect.
- **H-test gap (H worker, pre-existing, documented):**
  `test_versioned_renewal_history_phase_h.py:
  test_complete_versioned_passes_and_mutations` refuses the synthetic fake
  `R/validated-source-manifest.json` (`HISTORY_DIGEST_MISMATCH: … lacks
  current_tools`) — H historyfix worklog §5 preserves this as a fixture gap,
  not H weakening. Unrelated to this phase (fails identically without it).

## 6. Test behaviors (source identity: workdir HEAD 409b292 + uncommitted)

- NEW `tests/test_versioned_renewal_high_phase.py`: 9 pass / 3 skip (live
  checks need `RENEWAL_FIXTURE_ROOT`; skipped, not passed).
- `test_group_c_editorial_consumers_v2.py` 9/9 direct-call pass (35/22/71).
- `test_survey_publication_v2` + `test_survey_quality_v2`: 18/18 pass.
- `test_survey_reader_surface_gate_v2` + `test_survey_stage_validation_v2`:
  30/30 pass.
- `test_survey_publication_set_v2` + `test_survey_publication_revalidation_v2`
  + `test_survey_profiled_freeze_v2`: 53/53 pass.
- `test_survey_dm004_release_validate_state_v2`: 7/7 pass.
- `test_survey_editorial_staged_source_v2`: 26/26 ERROR — environmental EDQUOT
  (`git add -A` in test scratch setup: "disk quota exceeded"; /tmp 80%),
  fails before any touched code runs; preserved setup-failure class, not a
  regression (same failure independent of source content).
- H/S suites: H editorial unit still passes; the 3 failures above are
  S-owned/H-owned items (§5), not HIGH regressions.
- No `__pycache__`/`*.pyc` residue in workdir post-run (removed mine; status
  clean of them). Index clean (`diff --cached` empty). No candidate/reconstruct
  commits (workdir HEAD still 409b292; fixture commits are isolated synthetic
  DBs only, before authorities).

## 7. REMAIN (explicit; no stub PASS claimed)

C route end-to-end, repeat incl. C→U→U, renewal→editorial, normal direct
Candidate/Preview/Freeze/Release, R1×2 anchor, explicit failure/resume oracles
(IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor/ALREADY_ACTIVE),
remaining affected regressions (R1 slow suite open; DM004 done), and
independent final implementation review — all blocked behind S1/S2 (+H1 for
repeat). Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
Production semantic NO-GO on synthetic editions retained; fixture reviews are
synthetic, never genuine approval. No independent PASS. Stop here; ordinary
Commit/Push Human-owned.

---

# Turn 3 append (ROOT status inspection + corrections, 2026-10-25; old raw above untouched)

## 3.1 Empty-return gap disclosed

The previous worker return rendered EMPTY (tool-status only, no result text).
No execution was lost (all tool calls in that turn applied: T2/T3 tidies,
mismatch-doc resolution note, all verified live below). This append preserves
the gap explicitly instead of pretending continuity. No rerun of completed
U/C positives was performed for this inspection (read-only `ps`/`git`/`ls`/file
reads only; one `python3 -c` read-only State inspection with ABSOLUTE root).

## 3.2 Live-process + pin inspection (no duplicate execution)

- Live children: NONE related to renewal work (only system daemons +
  the inspecting shell itself). No `lualatex`/`biber`/`python3` renewal
  workers running. No duplicate-execution risk.
- Workdir HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, index clean
  (`diff --cached` empty), status 35M+44?? (f2/f3/f4/final snapshots agree
  except owned additions + pycache removals).
- HIGH `scripts/survey_versioned_renewal_v2.py`: 3048 lines, SHA256
  `1ee7066e04a581f407066bc9e02b84d322864d5f20e3d29a8252210dacf031d9`
  (FILE-everywhere + targets split + companions-direct + T2/T3 tidies all present).
- H `7e04c7fa…` (2871 lines, accumulator/OWN), S `d5472266…` (1467 lines,
  FILE linkage) — both as ROOT described; H/S files NOT edited this turn.
- Disk: `/` 350G avail (fixtures affordable); `/tmp` 80% (1.6G) — builds use
  small disposable roots only; EDQUOT scoping rule retained.

## 3.3 Actual milestone (evidence-backed, read-only verified)

- Weekly high22 (`renewal-weekly`): T1 `d685950` → U1 r2 ACTIVATED → T2
  `614c658` → U2 r3 ACTIVATED (run34: activate exit 0, H chain 3 / 31 bindings).
  State → `…/publication-surface-revalidation-r3.json`, VALIDATED_DRAFT.
- Longform high22: T1 `3b0c168` → U1 r2 → T2 `4a69c2e` → U2 r3 (same green).
- U1 H check (run31): chain 2 / 21 bindings / VALIDATION_CHECKPOINT, both routes.
- C1: finalized-only in high21 fixtures (SELF-era HIGH) — NON-POSITIVE history,
  never activated, never retrofitted. No C1 in high22 yet. No U3 anywhere.
- S0/S1 reconstruction: PLANNED last turn, NEVER executed (no such files found
  anywhere outside `.git/`). Superseded: T3 tidy already in workdir, so epochs
  advance by plain overlay+commit (T3 = current workdir); no reconstruction needed.
- Absolute-root recheck on U2-active weekly State: `agent.validate_agent_state`
  == [] (the earlier doubled-path failure was a relative-root artifact of a
  one-off inline check, not a product defect; harnesses pass absolute roots).

## 3.4 Cleanup-deviation log (exact; future preserve, no more cleanup)

- Claimed before ("failed parents removed") CORRECTION: NO fixture parent was
  ever deleted. All 22 parents (`versioned-renewal-high[2-22]*` + base `high-*`)
  and all 34 run evidence dirs (`run`, `run2`–`run34`) are present with content
  (verified by listing 2026-10-25). The `rm -rf <parent>` commands in history
  always targeted the not-yet-created NEXT name (no-ops). Nothing to restore;
  the earlier "removed" claim was wrong and is withdrawn here (old text kept).
- Actually deleted, disclosed: `__pycache__/` dirs + `*.pyc` bytecode ONLY
  (multiple cleanups, workdir + notes). These are regenerable interpreter
  residue, never evidence: exact `.py` sources + raw logs/pins preserved.
  One instance was informative: `schemas/__pycache__/versioned-renewal-source-
  manifest-v2.schema.cpython-314.pyc` (an import-system attempt on a schema
  JSON name). Future rule: preserve everything (including pycache) unless it
  corrupts a run; disclose instead of cleaning.
- A stale `schemas/__pycache__/` reappeared post-cleanup during later test runs
  (workdir tests import chain); left for now per no-cleanup rule, will be
  disclosed in final inventory, never committed (untracked, ignored).

## 3.5 Stale-claim corrections (turn-2 section above kept raw)

- "Blocked behind S1/S2 (+H1)" (§7 REMAIN): SUPERSEDED. S-FILE (d5472266) +
  HIGH FILE-everywhere resolved activation; U1/U2 green both routes (§3.3).
  S1/S2/H1 need no further action.
- "Unbound companion sidecar": SUPERSEDED. H schema now pins explicit
  companion fields; HIGH records companions directly in `toolchain.versions`;
  sidecar creation REMOVED from writer (old fixture sidecar files preserved as
  history, never counted).
- "C route end-to-end" REMAIN: PARTIALLY CLOSED since (C1 finalize green both
  routes in high21, SELF-era). C1 redo with FILE-era HIGH still open.
- interface-mismatch doc header already notes owner-fix supersession; the
  proof-basis-ref item is now CLOSED BY EXECUTION (H-1594 passes unmodified,
  U1/U2 activations + 21/31-row H checks), not merely recommended.
