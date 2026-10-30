# Independent follow-up — DM022 A4 final-source correction review (read-only, no code)

Same independent reviewer as R2/A3. Follow-up source review only, NOT final audit, NOT whole-lifecycle
acceptance, NOT publication/lifecycle approval. No source/test execution, no Git mutation, no Human
readback, no code writing. Previous `independent-research-r2-review.md` / `-a3-review.md` unchanged.

Binding order: contract `a345bb95` INCLUDING §11, pre-code §5, ROOT FULL `0425c530`/13788B INCLUDING §5,
readiness §§8–9, R3→R4+5 schemas→R5→R6→ROOT, R2 §§B1–B8, `astra-a3-integration-resolution.md` (BINDING §§1–4).
Author claim read: `author-A4-return.md` §§1–4. Evidence read (no re-execution):
`evidence/A4-correction-20261028T140520Z/a-binding.json` (priv 756, `14ef836d…`; A4 LOW `2df25c5d…`/148801B,
HIGH `2fe12b9e…`/87249B = A3 bytes, evidence `8b55dc6c…`, A-test `a2e48ba1…`/63453B, all priv==cand;
priv-vs-cand 0 diffs; schemas byte-identical), `a4-raw-binding.md`, `dm022-a4-test-raw-20261028.txt`
(37 lines, 19/19, `61939974…`, exit 0).

Fixed reference (READ-ONLY): `/tmp/dm022-a4-final` == `/tmp/dm022-a4-private` (same LOW SHA
`2df25c5d…`; both 148801B; `ls` shows both paths, content-identical). Full current idle candidate-work
incl B SizedRef fix at that point, minus `.git` (756 intended files). B/C files read only for interface
points cited below; A-files idle per task (no further A edits expected).

Method: static read of `/tmp/dm022-a4-final` bytes + line refs. `grep`/`sed -n` only to print already-read
ranges. No imports, no unittest/pytest, no fixtures, no workspace `git`.

## 1. Astra §§1–3 verified in actual A4 code (not author claims)

**§1 — SizedRef selected; repeat positive replaces blocker. CLOSED in source.**
Current snapshot enforces exact 3-key SizedRef in BOTH PREARCH branches (A did not edit B; read-only):
`survey_agent_control_v2.py:213-230` (`_validate_prearchitecture_record_content`: `set(result) !=
{"path","sha256","byte_count"}` → refuse + `byte_count int>=1`) and `:606-624`
(`_validate_core_stage_report` PREARCH branch: same exact-keys + `byte_count` + `stat().st_size` equality
`:623-624`). Legacy `CORE_STAGE_CONTRACT` path unchanged (separate branch). A writes schema-conformant
records (A4 §2) and no longer pins a blocker: A3 `test_repeat_correction_blocked…` GONE, replaced by
`test_repeat_correction_preserves_original_anchor_both_routes:706-751` (WEEKLY+THEMATIC `subTest`, rev1→
adopt→rev2→adopt, per-file refs resolve to real bytes, `evidence-package.sha256` mechanical present,
rev2 `parent==rev1 FILE bytes`, `original_anchor` carried, `supersedes` appends rev1, resolver+checker pass
on second-generation record) plus `test_malformed_review_result_refuses:752-765` (tampered `reviews[0].result.sha256`
→ `load_typed_checkpoint_record` refuses via SELF). Malformed check is genuine SELF-digest refusal, not a
keyword assert. R-A3-1 resolved in this fixed snapshot.

**§2 — public resolve runs FULL at SAME checkpoint; acyclic. CLOSED in source.**
`LOW resolve_research_authority:1021-1120` now (docstring `:1022-1039` corrected from A3 overclaim):
structural peek → `_load_typed_four_refs` classification (`:1056`) → PREARCH-only gate (`:1057-1067`,
legacy keeps historical shape, FULL never retrofitted) → `require_same_triplet` (`:1068`) →
`_verify_adopted_graph_full(selected_path,selected_sha)` (`:1069`) → report/proof/decision/retention actual
reloads with cross-binds at SAME SHA (`:1071-1093`: report schema, `proof/decision/request` + `before_state`
vs record, report `manifest` vs STORED manifest bytes, retained COPY vs `before_state`) → final pin recheck
(`:1094-1105`: State re-read + `require_same_triplet` + `checkpoint_path/sha` equality + checkpoint FILE
re-hash; any drift → refuse, never a different selection after an earlier READY). Returns
`full["artifacts/artifact_refs"]` (`:1117-1118`), data-only. Private `_load_typed_four_refs:396` stays NARROW
(classification/file/sha/schema/digest/shape per its docstring); every public authority result (resolve,
`check:2309`, completion, cleanup postread, resume `ALREADY_ACTIVE`) passes the FULL phase first. Call graph:
`_load` (leaf) ← `_verify_adopted` (`:787`) ← `check` (`:2340`) / `_verify_completion` (`:911,966`) /
HIGH postread / `resolve` (`:1069`); `check` never calls `resolve`, `resolve` never calls `check`.
Acyclic verified by `grep` (no `resolve` inside `check`, no `check` inside `resolve`). No caller verified
dicts (all path reloads), no current-State validation (`agent.validate_agent_state` never called in LOW),
no operational guard in detached paths (`require_no_active_guard` only in READY/HIGH, not in resolve/check/
FULL). R-A3-2 interface resolved at A scope; remaining B/C wiring is call-site hygiene, not an A predicate
gap (see §3).

**§3 — own-epoch proof is recorded-commit objects, not stored-claim equality. CLOSED in source.**
`_MAPPED_DM022_CODESET:546-558` is the finite 7 (2 modules + 5 schemas); `_DM022_SCHEMA_IDS:560-566` pins
selected `$id`s. `_git_read:569-594` is read-only (`cat-file/ls-tree/show` + `cat-file --batch`), scrubbed
`GIT_*`, `GIT_OPTIONAL_LOCKS=0`, no fetch, no HEAD pinning, no worktree/State read. `_verify_own_epoch_commit:
597-757` (called from `_verify_adopted_graph_full:872`): commit 40-hex exists (`cat-file -e`, `:629`); manifest
`tool_pins.path set == EXACTLY mapped set` (`:622-625`, extra/missing refused, no caller-arbitrary list);
every pinned path is `100644 blob` in that commit (`ls-tree -r … -- needed`, `:654-672`, missing/mode/kind
refuse); single-batched blob read with header/size/body checks (`:674-708`); pinned SHA == commit bytes
(`:709-711`); schema `$id` on commit bytes (`:713-719`); Contract8 recomputed byte-for-byte from COMMIT objects
(`:723-752`, mirrors `core.contract_identity`/`aggregate_file_hash`, profile names from COMMIT profile bytes
via stored request ref) and required to equal BOTH checkpoint contract and manifest pins (`:753-756`).
Stored record↔manifest equality kept as well, with object proof on top (not instead). Historical reads never
substitute LIVE tools (all bytes from `blob_bytes[rel]`), never demand `HEAD==recorded epoch` (no `rev-parse
HEAD` in LOW; `core.repository_commit_sha`/HEAD only in HIGH prepare eligibility for the LIVE invocation,
not in own-epoch), never recurse into current State. Imports are stdlib `subprocess` + already-closed
`core/schema_gate` only — no unmapped dependency, no Astra return needed. Finite-set/mode/fingerprint/Contract8/
profile/rulecheck all present; no fields-only equality; no caller list.

After-LIVE-advance behavior (BOTH paths) verified:
- Completion (`_verify_completion_full:889-1018`) does NOT pin LIVE to old expected bytes or slot absence:
  LIVE canonical `source_root/production-state.json` reloaded (`:959-961`), same-record triplet bound to THIS
  checkpoint (`:962-965`, stale checkpoint → refuse, correct), then FULL graph revalidated (`:966`, booleans
  recomputed), seven_plan vs inventory vs slots with regeneration tolerance (`:995-1017`: absent→present
  `continue`, new-content `continue`, same-byte-new-inode `continue`, only same-inode stale refuses). No
  `LIVE==expected_after` byte comparison here (that check lives ONLY in HIGH `write_cleanup_completion` at
  adoption time, correct old-stage binding). No lifecycle `EVIDENCE_REVIEWED` re-imposition (no lifecycle
  check in completion/check/resolve FULL paths; `check` docstring explicitly “valid after LIVE advances”).
  Forward Selection/Architecture/Draft provenance does not break the evidence/materiality/completeness
  same-record triplet (only those three checked).
- Own-epoch never forces `current tools==old commit`: all Contract8/pins/blobs from recorded-commit objects;
  `HEAD`/LIVE files never compared to recorded epoch in LOW FULL paths.

RAW genuine-claim proof (external independent, not self-minted) verified:
`prove_revision_from_paths` decision shape (`:2108-2115`: `assessment.{interpretation,event_semantics,
provenance_check}` + `reviewer.{provider,model,invocation,recorded_at}` non-empty strings,
`raw_refs` non-empty SizedRefs with live re-hash) + per-affected content binding (`:2196-2202`: NEW card
first-claim text must occur in a basename-routed Raw file’s bytes; SHA-only refused by
`test_raw_binding_refuses_unbound_claim`). Decision is a SUPPLIED input (`decision_path` + `manifest_ref`
FILE-sha binding, `:1958-1965` range + stale-decision refusal in tests), never minted by HIGH; HIGH’s own
`reviews[]` is the deterministic `DM022_SUPERSESSION_PROOF` (map-selected proof kind), not a Human genuine
approval; synthetic reviewer in fixtures is `SYNTHETIC_FIXTURE_*` (never claimed genuine). Independence beyond
shape (external authorship) remains procedural — code proves supplied-file binding + content binding, not
authorship; correctly not claimed as provenance attestation here.

Residual source hygiene verified: B1 atomic `os.link` claim with pid+counter+sha8 temp identity, partials
preserved, no autosnapshot delete (`HIGH:66-166`, `os.replace` only at State switch `:868`); B2 zero runner
imports (`grep` only docstring mention); per-file manifest/proof refs non-empty enforced; exclusive temp +
inode-pinned State switch + checked slot clearing + idempotent completion retained from A3 (HIGH bytes
identical `2fe12b9e…`).

## 2. Tests 19 — positive repeat both routes + malformed negative; actual fault seams; not whole lifecycle

Raw `dm022-a4-test-raw…:1-33` (37 lines, `Ran 19 … OK`): 5 carried positives (Weekly/Thematic full
prepare→adopt→resume→readback with per-file refs, FULL incl own-epoch, checker, resolver, CLI prepare;
loader dispatch; guard/slots) + 14 faults. Replacing the A3 blocker pin:
`test_repeat_…_both_routes:706-751` executes TWO successive adoptions per profile and asserts FILE-byte
lineage (`parent==rev1 FILE {path,sha256}`, anchor carried, `supersedes` appends, resolver revision==rev2,
checker `[]` on second-generation record) — real positive repeat, not a refusal pin.
`test_malformed_…:752-765` tampers `reviews[0].result.sha256` and asserts SELF-digest refusal (no writes).
Other faults assert actual seams/counters/no-write snapshots (static read of `/tmp/.../test_…:589-996`):
Raw-content refusal pre-guard with guard-absent + LIVE==before (`:589-609`); late checkpoint-final plant →
atomic refuse + plant intact + guard held + LIVE==before, then plant removal → `RESUME_ADOPTED` + slots
cleared + completion consistent (`late_final…`); 3× completion tamper (checkpoint-sha/disposition/
expected_after) → `require_completion…` refuses + resume `INDETERMINATE`; absent-slot regeneration →
`READY` passes + readback PREARCH (old-absent `absent_legitimate` asserted); interrupted-clear E+guard-held →
`RESUME_CLEARED` + slot gone + guard released (root-skipped when euid 0, honest); unknown LIVE → 
`INDETERMINATE` + `live_sha256` + records preserved; slot ownership (unreadable pre-guard refuse;
same-byte-new-inode `source_ino` inequality → refuse, then unlink → `RESUME_CLEARED`); State-tmp plant →
switch refuses + recovery; completion idempotent reuse (bytes identical, `idempotent:True`); unreadable paths
fail-closed never coerced; stale HEAD/decision/unsupported-profile/named-gap (+named-positive). No early-
preemption-only tests; each asserts post-fault preservation required by map §7. Single-Discovery
`target-source` fixtures + synthetic decisions only — representative, not exhaustive.

**Does NOT prove whole lifecycle** (correctly not claimed by A4 §4): no normal forward Architecture/Draft/
publication + later editorial/renewal on the adopted record, no G71→G76 unchanged-upstream control, no
affected regressions, no B/C suites, no seven-slot normal-regeneration end-to-end beyond READY+readback.
Those remain runtime-coverage OPEN, not source-predicate gaps.

## 3. Verdict — bounded source-correction PASS (A-scope + B SizedRef incl.); runtime/integration OPEN

No remaining source predicate blocker in the frozen A4 bytes. R-A3-1 resolved (exact 3-key SizedRef + real
size checks in current snapshot; positive repeat both routes green). R-A3-2 resolved at A scope (public
resolve is FULL at SAME SHA with report/proof/decision/retention/COPY + final recheck, acyclic; narrow
`_load` stays internal). If a B/C mutating callsite ever resolves WITHOUT the FULL path for the SAME ref
(e.g. future edits dropping READY or calling the narrow loader directly), that would be a NEW caller-side
blocker at the precise points `run_selection_architecture:76,258`, `run_drafting:86`,
`editorial_correction:_ckpt_resolve`, `weekly/longform_derivation`, `editorial_current_authority` (observer
only) — but in the frozen bytes each mutating entry is READY-gated (`require_research_operation_ready` →
`_verify_completion_full` → `_verify_adopted_graph_full` + own-epoch) AND `agent.validate_agent_state`
runs on the same LIVE bytes, and `resolve` itself is now FULL, so no hash-only authority path remains.
Distinguish: **source predicates CLOSED; runtime coverage OPEN** (frozen all-owner integration snapshot,
full Weekly/Thematic correction + repeat + normal regeneration/Architecture/Draft/publication + later
editorial/renewal, G71→G76 control, failure/resume seams, affected regressions, B/C suites, independent
implementation review). Do not accept author “19/19” as whole-operation proof — it is bounded A-scope proof
with B fix included, exactly as A4 §3 scopes it. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN,
Profile/quality/adoption/savings OPEN. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## Independence

NOT Owner A/A4/B/C1/C2, NOT Astra author-side; no source/schema/test/fixture/config edits; no runtime, tests,
restores, network, Git mutations, or Human commit readback. Only `/tmp/dm022-a4-final` A-scope bytes +
packet/return/resolution docs above were read. Line refs are to `/tmp/dm022-a4-final/...`; re-verify at the
next freeze if `candidate-work` moved. Early source review only; may later final-review only with a fresh
fixed all-owner snapshot + full raw + affected regressions. No code edited by this reviewer.
