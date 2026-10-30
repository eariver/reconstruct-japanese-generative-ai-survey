# Independent re-review — DM022 A3 correction (A-scope actual source, no code writing)

Same independent reviewer as R2 `independent-research-r2-review.md` (§§B1–B8). Early blocking
re-review only, NOT final audit, NOT whole-implementation acceptance, NOT publication/lifecycle approval.

Date: 2026-10-28. Binding order unchanged: contract `a345bb95` INCLUDING §11, pre-code §5,
ROOT FULL `0425c530`/13788B INCLUDING §5, readiness §§8–9, then R3→R4+5 schemas→R5→R6→ROOT.
R2 review preserved (not overwritten); this file is the A3 delta. Author claim read:
`author-A3-return.md` §§1–5. Evidence read (no re-execution):
`evidence/A3-correction-20261028T134500Z/a3-binding.json`,
`a3-raw-binding.md`, `dm022-a3-test-raw-20261028.txt` (37 lines, 19/19, SHA256 `abb66f3d…`),
`private-source-manifest.json` (756 files, SHA256 `b73c4d93…`).

Fixed reference (READ-ONLY, no runtime/test/source/Git/Human-readback, no candidate edits):

- `/tmp/dm022-a3-fresh` = R2 snapshot 756 files + ONLY 4 A3-modified A-owned files overlaid
  (binding `a3-binding.json` §§fixed_source/other_files_differ: priv-vs-R2 diff exactly 4 paths;
  schemas byte-identical). Hashes match A3 §1:
  LOW `aee60132…`/132244B, HIGH `2fe12b9e…`/87249B,
  `survey_evidence_v2.py` `8b55dc6c…`/125817B (additive-only per A3 §1),
  A-test `9755279f…`/62293B, fixture helper unchanged `7fdc692c…`.
- Candidate `candidate-work` B-files may drift (SizedRef fix pending) but A-files idle per task;
  this review binds ONLY `/tmp/dm022-a3-fresh` A-scope + R2 B/C call sites as cited (no B/C re-review).

Method: static read of `/tmp/dm022-a3-fresh` bytes + line refs. No imports, no unittest/pytest,
no fixtures, no `git` in workspace root. `grep`/`sed -n` only to print already-read ranges.

## 1. R2 §§B1–B8 closure in actual A3 code (not claims)

- **B1 RESOLVED in A code.** HIGH `_exclusive_write_bytes:69-166` now single-syscall atomic
  `os.link(tmp, path)` (`:142-144`, EEXIST→refuse, no overwrite). Temp is `O_CREAT|O_EXCL`
  + short-write + `fsync` + checked close + re-read verify (`:95-140`), preserved on failure
  (`:104,110,116,120,124,133,140,144` “temp preserved at …”), unlinked ONLY after successful
  link (`:146`), then dir `fsync` + postread equality (`:150-162`). Docstring `:70-81` correctly
  scopes `os.replace` to `replace_state_triplet` ONLY. `_copy_regular_exclusive:202-226` pre-checks
  dst absence (`:204`) but final claim is the atomic link inside `_exclusive_write` (`:210`), so the
  pre-check is fast-path only, not a race. `replace_state_triplet` retains held-descriptor/
  before/recheck/postread + inode pinning (separate path, allowed). No hidden `unlink` of partial
  finals. Test `test_late_final_plant_blocks_and_resume_recovers` + `test_replace_tmp_exists_refuses`
  pin the seam (see §3).
- **B2 RESOLVED in A code.** Zero `run_evidence_v2_interactive` imports in LOW or A-tests
  (`grep` §A3-return §4 matched; `/tmp` LOW imports `:48-49` top-level core+schema only,
  function-local leaf imports `:417-418,560-561,598,887,939,1016-1017,1157,1248,1361-1362,1478-1479,1659-1661`
  + `import jsonschema:201` stdlib-wrapped, no agent/State/circularity). Pure record/card/view logic
  now in A-owned `survey_evidence_v2.py:1549` (`validate_research_record_content`), `:1647`
  (`build_research_card_content`), `:1782` (`build_research_view_content`) + `task_authority_sources:413`
  and `_DM022_*` constant sets mirroring the interactive contract; LOW calls leaf helpers at all four
  former runner sites. Closure is core+schema+leaf only. B keeps runner copies for the normal path
  (coordination point documented in-module, no duplication of authority).
- **B3 RESOLVED in A code.** `LOW _validate_against_report_def:189-222` validates against EXACT
  `report $defs/completionReceipt` (loads installed report schema, `combined={"$defs":defs,"$ref":"#/$defs/<name>"}`,
  `Draft202012Validator` + `FormatChecker`, no repo-file closure, no agent/circularity). Installed schema
  verified to carry the pointer: `/tmp/.../schemas/dm022-preadoption-report-v2.schema.json` `$defs` includes
  `completionReceipt` (+`retentionManifest`,`guardIntentCoord`). `_verify_completion_full:675-804` does the FULL
  chain: checkpoint FILE/sha+family, receipt `$defs` schema (`:704`), issue/revision/checkpoint cross-bindings
  (`:705-710`), retention 7 rows exactly bound to stored manifest snapshots dict-equality (`:711-732`),
  COPY-derived expected_after recompute byte-compared never trusted (`:734-742`), LIVE canonical
  `source_root/production-state.json` reload + same-record triplet bound to THIS checkpoint (`:745-751`),
  FULL adopted-graph revalidation (recomputes booleans, `:752`), seven_plan vs inventory vs slots
  (`:754-803`). `require_completion_consistent:2232-2251` (R4 signature, location-only repo discovery)
  delegates to it (`:2250`); `require_research_operation_ready:2254-2305` calls it for PREARCH triplets
  (`:2305`) after guard-absence (`:2285`). HIGH `write_cleanup_completion` postread now calls
  `low._verify_adopted_graph_full` (HIGH `write_cleanup:942-1007`, esp. postread FULL block) instead of
  trusting booleans. E+guard-absent `ALREADY_ACTIVE` (`HIGH resume:1310-1320`) goes through this FULL path.
- **B4 RESOLVED in A code.** `_verify_completion_full slot rule :781-803`: old-absent slots with present files
  `continue` (legitimate regeneration, `:784-789`); present-plan allows new-content bytes (`:796-798`) and
  same-byte-new-inode (`:799-802`); only same-inode stale refuses (`:803`), fail-closed when identity
  unavailable. Old absence/inode window not reapplied post-completion. Shared by READY and completion,
  so normal regeneration (incl. old-absent slots) passes READY after valid completion. Covered by
  `test_absent_slot_regeneration_ready_and_readback` (see §3).
- **B5 RESOLVED in A code.** `LOW prove_revision_from_paths:1644-2034` now: request load+schema from stored
  manifest ref (`:1752-1761`) + profile/discovery/screening live re-hash (`:1762-1764`) + Discovery JSONL
  (`:1768-1771`); per-file manifest refs verified non-empty with live re-hash for package/evidence/views/
  ledger/completeness (`:1772-1779`) + `tasks/cards/views` non-empty code-enforced (`:1791-1797`,
  empty→refuse); digest recomputes kept (`:1798-1806`); FULL validators with exact session basis
  (`disc_abs` DIRECT root): `_validate_evidence_acceptance_content:1808`, `_validate_edition_views…:1812`,
  `_validate_materiality_ledger_content:1818`, `_validate_profile_completeness_content:1825` (+errs check);
  decision assessment/reviewer/raw non-empty shapes (`:1835-1843`); Raw content binding: every affected DID
  routes to ≥1 Raw file whose basename contains the DID AND whose bytes carry the NEW card’s first claim
  text (`:1922-1930`, SHA-only refused by `test_raw_binding…`); mechanical projections extended to
  package/result_set/view_set/ledger-basis/completeness-basis, emitted only on actual differ (`:1962-1982`,
  derived set); `rows_checked>0` kept (`:1983-1984`, empty package refused upstream). HIGH prepare populates
  per-file `tasks/cards/views` SizedRefs from validated accepted-run copies + refuses empty task/view sets
  (`HIGH:702-713`, `ordered_task_metas`/`ordered_view_rows`, `task_refs/card_refs/view_refs`), mirrored into
  proof `proposed` (`LOW:2003-2014`) with verification. Schema unchanged per no-broadening rule (empty arrays
  still schema-allowed, code-enforced non-empty — correct layering).
- **B6 CODE CLOSED in A-owned FULL paths; INTERFACE REMAINS (see §2).** `_load_typed_four_refs:395-523`
  docstring now states the narrow contract explicitly (`:396-415`: classification + file/sha + schema +
  digest-equality + ledger shape/basis-key + completeness shape/obligation-shape ONLY; row linkage vs
  discoveries, basis vs live files, closure/provenance NOT proven here; “No acceptance path may treat this
  loader alone as full acceptance; mutating producers and READY must go through the FULL paths”). New shared
  `_verify_adopted_graph_full:545-672` runs the FULL graph: `_load` + request load/validate (`:577-586`) +
  profile/discovery/screening live re-hash (`:592-598`) + Discovery JSONL (`:600-603`) + FULL evidence
  (`:614`), views (`:618`), ledger (`:625`), completeness (`:633-640`) with `root_records/disc_abs` DIRECT basis
  + own-epoch pins from STORED files only (manifest via `revision_root`, contract/implementation vs stored
  `tool_pins`, `:644-658`, never current source, so stays valid after LIVE advances). Wired into
  `check_supersession_record_from_paths:2037-…` (replacing the partial “FULL” label, `:2068` calls
  `_verify_adopted_graph_full`), HIGH `write_cleanup_completion` postread, and `_verify_completion_full`
  (`:697,752`, hence `require_completion_consistent`, `require_research_operation_ready`, resume
  `ALREADY_ACTIVE`). Composition is acyclic: `_load` (leaf) ← `_verify_adopted` (calls `_load :572-575`) ←
  `check`/`_verify_completion`/HIGH-postread (call `_verify_adopted`); `resolve` calls `_load` only
  (`:831`), never `check`; `check` never calls `resolve`. Allowed (no recursion). OWN-epoch + stored-file
  discipline + COPY-expectedAfter-old-stage (retained COPY, not current window) + partial-guard/missing-
  completion-UNKNOWN preservation (READY guard-first; resume `B` lost-guard→INDETERMINATE,
  `E`+guard-absent+unverifiable→INDETERMINATE, `UNKNOWN`→INDETERMINATE with `live_sha256`, retention-mismatch→
  INDETERMINATE; HIGH `resume_bound_attempt:1259-1352`) all verified in code.
- **B7 RESOLVED in A code (incl. B7b).** HIGH `_prove_before_graph_unbound:346-398` (downstream pending +
  both gates pending + provenances null + no approval files + review-index schema-valid with no APPROVED) +
  `_prove_slot_not_human_presented:401-429` (per-slot scan of review records for slot path/SHA, absent-index
  common case) wired into `prepare:554,582` BEFORE any COPY. `accepted_bound/gate_bound:False` is now the
  PROVEN outcome (`HIGH:552-554` comment), not constants. Manifest `retention_snapshots` and
  `retention/inventory.json` carry identical 13-key rows (`HIGH:727-730` vs `:757-762`), enforced per-slot
  exact equality in adopt/resume/completion (`LOW:718-732` manifest-vs-inventory, `HIGH resume` retention-vs-
  manifest checks). Idempotent completion compares semantic intent excluding `recorded_at` and reuses bytes
  without rewrite (`HIGH write_cleanup:996-1005`, `idempotent:True`, bytes-verified; differing intent refuses).
- **B8 A-SCOPE FAULTS CLOSED; WHOLE-OPERATION + REPEAT-POSITIVE STILL OPEN (see §2–§3).**
  19 tests = 5 carried A2 positives + 14 new fault/negative/later-seam tests (raw `dm022-a3-test-raw…:1-33`).
  `test_repeat_correction_blocked_on_result_authority_shape` is the EXPECTED-BLOCKER pin (refusal with no
  writes, `rev-repeaty` dir absent + guard absent asserted), NOT a repeat-positive proof — correctly labeled
  as cross-owner need (A3 §3). Remaining fault tests assert actual seams/counters/no-write snapshots, not
  early preemption (see §3). Integration witnesses on the frozen all-owner snapshot (both-route
  positive/negative/later-lifecycle incl. G71→G76 control, G76→initial→editorial/renewal, genuine
  forwarded-State readback via B/C forward writers, affected regressions, B/C suites) + independent
  implementation review remain for root after all authors return (A3 §5, ROOT whole-implementation request
  unchanged). No whole-audit/publication/lifecycle claimed here.

## 2. EXACT remaining blocking predicate(s)

**R-A3-1 [BLOCKING, cross-owner, NOT an A-code waiver]: B agent PREARCH review-`result` shape rejects the
selected SizedRef.** Selected checkpoint schema (`schemas/dm022-supersession-checkpoint-v2.schema.json:90-107`)
requires `reviews[].result` to be a SizedRef `{path,sha256,byte_count}`. B agent demands exactly
`{path,sha256}` in BOTH PREARCH branches in `/tmp/dm022-a3-fresh` (R2 B files, A untouched):
`scripts/survey_agent_control_v2.py:223` (`_validate_prearchitecture_record_content`:
`set(review.get("result")) != {"path","sha256"}` → “requires deterministic result authority”) and
`:570` (`_validate_core_stage_report` PREARCH branch: same check). A writes schema-conformant records,
so `agent.validate_agent_state` on an adopted PREARCH State fails there. Pinned by
`test_repeat_correction_blocked_on_result_authority_shape:732-754` (second `prepare` on adopted PREARCH
State refuses “deterministic result authority” BEFORE any A write: no `rev-repeaty` dir, guard absent —
proof of no-write blocking, not A logic failure). A-lineage for repeat (HIGH adopt `:1131ff` parent =
previous record, `original_anchor` carried, `supersedes` appended) is implemented and executes once B
accepts the shape. **Fix (B-owner, return to Astra before broadening):** accept SizedRef review results in
both PREARCH branches (subset check on `path+sha256`, e.g. `{"path","sha256"} ⊆ set(result)`, mirroring the
report-ref discipline at `:251-252` which already expects `{path,sha256,byte_count}`); keep byte_count
ignored-or-verified but never a refusal reason. Until then the REQUIRED repeated-correction witness
(ROOT §5.2 + contract §10 + A3 §3) cannot execute. Flagged as pending integration; A must NOT work around
by writing non-conformant `{path,sha256}` records.

**R-A3-2 [BLOCKING interface, A-doc + B/C wiring]: active public resolver still advertises FULL while
granting partial; B/C mutating consumers resolve via it alone.** `LOW resolve_research_authority:807-848`
docstring `:810-813` still claims “typed checkpoint + 4-artifact loads with live re-hash and FULL content
checks,” but the body calls the NARROWED `_load_typed_four_refs:831` + `require_same_triplet:832` only
(no request/manifest, no FULL validators, no own-epoch pins). The narrowed contract lives ONLY in
`_load_typed_four_refs:408-415`. Any caller reading the resolver docstring as FULL and using
`artifacts/artifact_refs` as mutating authority gets hash/shape-only permission. Actual B/C call sites in
the reference (R2 B/C files, A untouched) that resolve via it:
`run_selection_architecture_v2_interactive.py:76` (`_dm022_resolve_ledger_completeness`) + `:258`
(four-ref for generation), `run_drafting_synthesis_v2_interactive.py:86`,
`survey_editorial_correction_proposal_v2.py:1495` (`_ckpt_resolve`), plus observers
`survey_editorial_current_authority_v2.py:73`, `survey_weekly_derivation_v2.py:633`,
`survey_longform_derivation_v2.py:1052`, HIGH `readback_revision:1370`. Mitigation TODAY is compositional:
mutating entries call `_dm022_require_ready` (FULL via `_verify_completion_full`) BEFORE resolving
(e.g. selection `run:248` READY → `:252,258` resolve; agent entry `:142` READY + `:258` FULL check), so the
SAME LIVE bytes were FULL-verified for the SAME checkpoint SHA immediately prior. That composition is
sound ONLY if (a) the resolver docstring is corrected to “classification-grade, NOT acceptance,” and
(b) every MUTATING consumer binds the FULL check to the SAME checkpoint SHA it then resolves
(READY’s `_verify_completion_full` for `cp_rel/cp_sha` == resolver’s `structural.checkpoint_path/sha256`,
no TOCTOU gap), or calls the FULL entry directly. **Fix:** (A, one-line doc scope, no logic change)
correct `resolve_research_authority` docstring to the narrowed contract + “mutating producers and READY
must go through `check_supersession_record_from_paths` / `_verify_adopted_graph_full` /
`_verify_completion_full` / `require_research_operation_ready` for the SAME ref; this resolver is for
detached diagnosis/readback only.” (B/C, wiring) For each MUTATING use above, either replace
`low.resolve_research_authority(repo_root, state_path)` with
`low.check_supersession_record_from_paths(repo_root, checkpoint_path, report_path, before_copy_path)`
(empty==pass) or `low._verify_adopted_graph_full(repo_root, checkpoint_path, checkpoint_sha)` for the
SAME triplet ref (plus existing READY), and use the returned `artifacts/artifact_refs` (same shape).
Read-only observers (`editorial_current_authority`, HIGH `readback` without `revision_path` FULL) may keep
the narrowed resolver IF documented as diagnosis-only and never as write permission. C1 derivation helpers
(`weekly/longform_derivation`) need the same rule if their resolved refs feed writes. Until the docstring is
fixed + B/C mutating sites bind FULL to the SAME ref, R-A3-2 stays the last A-interface blocker. No new
family/schema, no hash-only permission granted by A-owned FULL paths themselves.

No other A-scope blocker remains. B1–B5,B7 code-closed; B6 FULL paths code-closed; B8 A-faults closed.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN, Profile/quality/adoption/savings OPEN remain
until root binds the frozen all-owner snapshot + executes ROOT whole-implementation witnesses + independent
implementation review. Ordinary Commit/Push Human-owned; stop at Human Commit Point.

## 3. Test-scope note (19 tests: 1 expected-blocker + 18 positive/fault, actual seams)

Raw `dm022-a3-test-raw-20261028.txt:1-33` (37 lines, `Ran 19 tests … OK`, `EXIT:0` per `a3-raw-binding.md`).
Scope per test names + assertions (static read of `/tmp/.../test_…:477-981`, no re-execution):

- Positives (5 carried): Weekly/Thematic full prepare→adopt→resume→readback (incl. per-file manifest refs,
  FULL adopted-graph validation, checker, resolver+`artifact_refs`, CLI `prepare`), loader dispatch, guard/slots.
  `ALREADY_ACTIVE/RESUME_CLEARED/RESUME_ADOPTED` accepted as terminal states per map §7 (not overclaim).
- Expected blocker (1, NOT positive proof): `test_repeat_correction_blocked…:732-754` asserts B-refusal
  (“deterministic result authority”) + `rev-repeaty` dir absent + guard absent (no-write snapshot). Correctly
  pins R-A3-1; `test_repeat_correction_anchor_and_per_file_binding:703-730` covers first-correction lineage
  inputs + per-file bindings but NOT second-correction success (docstring says so explicitly).
- Faults (13, actual seams/counters/no-write, NOT early preemption): Raw-content refusal pre-guard with
  guard-absent + LIVE==before asserted (`:603-609`); late checkpoint-final plant → atomic refuse + plant intact
  + guard held + LIVE==before, then plant removal → `RESUME_ADOPTED` + slots cleared + completion consistent
  (`:611-646`); completion tamper ×3 (checkpoint-sha/disposition/expected_after) → `require_completion`
  refuses + resume `INDETERMINATE` (`:648-674`); absent-slot regeneration → `READY` passes + readback PREARCH
  (`:676-701`, old-absent `absent_legitimate` rows asserted); interrupted-clear E+guard-held → `RESUME_CLEARED`
  + slot gone + guard released (`:816-853`, agent-validation + readback still work while guard held);
  unknown LIVE bytes → `INDETERMINATE` + `live_sha256` + records preserved (`:855-871`); slot ownership:
  unreadable pre-guard refuse + same-byte-new-inode refuse with `source_ino` inequality asserted, then
  `RESUME_CLEARED` after unlink (`:873-907`); State-tmp plant → switch refuses + recovery to `RESUME_ADOPTED`
  (`:909-936`); completion idempotent reuse → bytes identical + `idempotent:True` (`:938-965`); unreadable
  paths fail-closed never coerced to absent (`:967-981`). Stale HEAD/decision/unsupported-profile/named-gap
  (`:756-814`) asserts stale-pin refusals + named-union enforcement (+ named-positive). Each asserts the
  post-fault record/byte/guard preservation required by map §7; no synthetic genuine approvals; no old
  test-count transfer.

## Independence

- NOT Owner A/A3/B/C1/C2, NOT Astra author-side; no source/schema/test/fixture/config edits; no runtime,
  tests, restores, network, Git mutations, or Human commit readback. Only R2 worktree-equivalent
  `/tmp/dm022-a3-fresh` A-scope bytes + packet/evidence docs above were read.
- Line refs are to `/tmp/dm022-a3-fresh/...`; `candidate-work` B-files may have drifted (SizedRef fix pending) —
  re-verify B line numbers (`agent_control:223,570`, selection `:76,258`, drafting `:86`, correction `:1495`,
  current-authority `:73`, derivations, readback `:1370`) at the next freeze.
- Early blocking re-review, NOT final audit/acceptance. May later serve as final reviewer only with a fresh
  fixed all-owner snapshot + full raw + affected regressions. No code edited by this reviewer.
