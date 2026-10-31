# Profile/support independent pre-code readiness review (fresh reviewer)

2026-10-31. Fresh independent reviewer: not author A/B/C, not integrator, not ROOT.
Scope: bounded pre-code map ONLY. Human continued with bounded precode, no Human Commit readback.
No runtime/import/tests/build/fixtures/network/restore/Git/HEAD/status/readback/mutation performed.
Source READONLY `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(actual409/tree8ce +133paths54M79A/768 files; patch `25b488784d02a156db693459dce6c1d369e7144f1c9b3a846b1b7260`/4931836B;
manifest `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa`/185422B).
Baseline774 unchanged.

Read FULL, including §7 / §5:

- Decision `outputs/rephase-1-profile-support-contract-decision.md`
  FULL SHA256 `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54de260527e2d` /20472B INCLUDING §7.
- Contract ROOT `notes/rephase-1-profile-support-contract/astra-review-resolution.md`
  FULL SHA256 `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a` /7225B INCLUDING §5.
- Working gate `notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md` FULL (NOT_READY, §§1–4).
- Combined proof-C-now-available: `integrated-readiness-r2.md` + `integrated-readiness-r2.json`
  plus `source-family-closure-map-r2.md` + `source-family-closure-map-r2.json` (33,928B).
  Initial `source-family-closure-map.md/json`, `admission-callsite-map.md/json`,
  `obligation-input-derivation-map.md/json` preserved as history, not re-audited.

Method: source text-read only against final133 bytes cited below. No author claim accepted.
No mandatory §6 detail deferred to implementation.

## 1. Verdict

**PRE_CODE_NOT_READY (bounded). No code / no adoption approval.**

R2 + C-R2 are a substantial integration advance, but they still contain
wrong-role proofs, reversed semantics, misidentified write windows, ellipsis
return shapes, wrong authority hashes, and a missing operations/oracle table.
All are pre-code blockers: they change where checks run, what bytes they read,
and whether history is re-gated. Fix the minimum repairs in §3, then return
for fresh readiness + Astra confirmation. No overall code/adoption approval;
no full-suite/test-count claim.

What is now correct and retained (not blockers):

- Canonical owner `survey_evidence_v2._source_class:177-183` fail-closed, 10 additive rows
  normative, old rows unchanged; no conditional classifier / default SECONDARY /
  PR-never-primary / URL-sniff / legacy-enum / supplement-SOCIAL expansion.
- Loss helper home in `survey_screening_v2.py` (owns `parent_refs`, `PROVENANCE_KEYS:47-48`,
  `validate_discovery:113-183`), separate from unchanged `validate_discovery_expansion:243-322`.
- Staged/canonical split per gate §1: Evidence/Screening are staged replay members,
  interactive/agent-first drivers are NOT; HIGH/LOW are in both staged and canonical36/41
  (weekly `survey_weekly_derivation_v2.py:70-81`, longform `survey_longform_generated_v2.py:92-103`
  via identical `DM022_7`); drivers covered only via control-root diff predicates, not blobs.
- No new module/schema/family/request-field presumed; G76 stays only under exact-76 +
  member-wise equality + fresh CURRENT proof (counts never authority).

## 2. Blocking findings (exact source predicate / interface)

### B1 — R2 §6 DiscoveryCP proof uses wrong-role PREARCH verifiers (recursion/LIVE)

R2 `integrated-readiness-r2.md:379-384` + JSON `dm022_true_RE.typed_proof` cites as
DiscoveryCP proof for ordinary Screening/Evidence admission:

- `load_typed_checkpoint_record:310` + `_verify_own_epoch_commit:620` +
  `_verify_adopted_graph_full:783` + `_verify_completion_full:914`.

Actual source predicates refuse this reuse:

- `_verify_own_epoch_commit:620-648` proves a *PREARCH DM022 codeset*: pinned set must
  equal exactly `_MAPPED_DM022_CODESET` (2 modules + 5 schemas), Contract8 recomputed
  from recorded-commit objects. Ordinary Discovery has no PREARCH checkpoint, no DM022
  codeset, no Contract8.
- `_verify_adopted_graph_full:783-811` requires `typed["family"]=="PREARCH"` (`:809-810`)
  and loads 4 DM022 artifacts + request/manifest own-epoch pins. Ordinary S1/S2/N1/E1/E2
  have no PREARCH record.
- `_verify_completion_full:914-991` calls `_verify_adopted_graph_full` (`:936`) and then
  reloads LIVE canonical State (`:984-991` `source_root/production-state.json` + triplet +
  FULL graph revalidation). Using it inside ordinary admission or LOW pure helpers
  injects LIVE State recursion and HIGH lifecycle into a path that must be State-free /
  detached PATHS-only (`survey_research_authority_v2.py:1-36`, top-level ONLY `core+schema_gate:48-49`).

Required pure Discovery/Screening proof before State COPY (no LIVE agent):

- `read_jsonl` + `validate_discovery_set` + SHA drift (`survey_screening_v2.py:374-379,403-411`,
  `accepted_ids==root_ids:408-411`), `_canonical_root_acceptance:325-350` (State-bound
  accepted path vs DIRECT `:382-395` fallback), `validate_acceptance` on the acceptance
  file, `validate_discovery_expansion:243-322` only for DERIVED mode (`:428`).
- LOW true-R/E must thread these validated `root_records/root_path` values from the
  pinned before-State COPY + accepted Discovery/Screening refs, never LIVE `agent` /
  `verify_state_basis` / HIGH guard / completion. No `agent.validate_agent_state`,
  no `production.verify_state_basis`, no `_verify_*` PREARCH/completion call in LOW bodies.

### B2 — New pre-package helper takes dicts, not paths; marker boundary incomplete

R2 ownership + JSON `ownership.prepackage_helper`:
`resolve_prepackage_root_effective(repo_root,state,profile,discovery_path,accepted_discovery_path|None)`
in `survey_screening_v2.py`. `state`/`profile` are dicts.

This violates the path-based authority boundary already required by gate §2.3 and by
LOW PATHS-only rule (`survey_research_authority_v2.py:12-18`: never accepts caller
State/ledger/completeness/proof dicts as authority; public entries take repo_root + PATHS only).
A dict-taking helper is a caller-verified-flag risk and cannot be pinned to SHA/ID/count/schema.

Also S1 has no package yet (`prepare_package:492-567`: no package exists before
`output_dir/input/batches/*.jsonl:525` + `package.json:566`). R2 correctly forbids a dummy
package or resolver-on-future-path, but does not pin the exact replacement checks:

- No-marker initial DIRECT ONLY when State has no accepted-Discovery provenance AND is in
  the existing initial window (`lifecycle_state ISSUE_INITIALIZED` + no
  `discovery-accepted-v2.json` via `_canonical_root_acceptance` pattern `:345-350`).
  Then incoming Discovery is both R and E.
- Accepted-marker present → full State root bind: reload State file + Profile file +
  accepted Discovery JSONL with SHA/ID/count/schema checks; missing/mismatched marker or
  provenance refuses. Never DIRECT fallback. Fixture tolerance is not a bypass flag.

Repair must spell exact `(repo_root:Path, state_path:Path, discovery_path:Path,
accepted_discovery_path:Path|None)` threading, file reloads, and all callers
(S1 `prepare_package`, S2/E1/E2/H1 entry points, CLIs/handlers).

### B3 — HIGH first-write misidentified; adopt gate prefix missing

R2 check-table H1 `first_write`: "R-owned `revision_root/candidate/**` ONLY via
`_exclusive_write_bytes:83`". Actual first writes in `prepare_revision:456-781` are
retention COPYs, not candidate bytes:

- First COPY at `:538` `state_copy_info = _copy_regular_exclusive(live_abs, state_copy, ...)`,
  then 7-slot COPYs `:563-600` (`_copy_regular_exclusive`), candidate writes only from `:605`.
- Adopt re-verifies (`adopt_revision:1064-1142`: LIVE parse, `verify_live_eligibility`,
  HEAD/tree, contract/tools, before-State SHA, retention inventory equality, then
  `_prove_before_graph_unbound:1127` before ANY guard/checkpoint/State mutation,
  then `prove_revision_from_paths:1140` before `proof/proposed-graph-proof.json:1142` write).

R2 places the DM022 DM016+DM017 eligibility "before R candidate writes" (`:278-293`)
and cites HIGH post-write `None,None at prepare:677,682` as the gap. Both are too late /
imprecise:

- `:677/:682` pass `None,None` for `root_records/root_path` to
  `_validate_evidence_acceptance_content` / `_validate_edition_views_acceptance_content`
  AFTER exclusive R writes have already occurred (`:605-671`).
- New-policy eligibility must run BEFORE the first COPY at `:538` at prepare, and be
  re-verified at adopt BEFORE any guard claim (`:1127` window) and before the proof write
  (`:1140-1142`), with existing source/epoch/drift behavior stated (resume reuses bound
  guard/retention/planned bytes; readback detached read-only `:1379`).

### B4 — Residual-union order reversed vs actual adapter

R2 `integrated-readiness-r2.md:349-351` (+ §5): "STABLE: `list(input.residual)` then append
missing `closure.limitations` in order (adapter `:66-69`)".

Actual `run_evidence_v2_agent_first.py:55-76`:

- `normalized = list(closure_limitations)` (`:66`), then `for limitation in residual:
  if limitation not in normalized: append` (`:67-69`).

Order is closure-first, residual-appended — the reverse of R2. The normal-builder fold-in
must preserve the actual adapter order byte-exactly (direct==agent-first byte-equal +
residual order oracle depends on it). Current `_build_completeness:554` copies
`closure_input["limitations"]` verbatim (no union) — the union is proposed, not current
behavior — so the map must state current COPY vs proposed UNION without swapping operands.

### B5 — Closure "all 8 from provenance" overclaims operator fields

R2 `§5` + JSON `inputs_3_5.closure_8` / `closure_rules`: "Thematic `closure` 8 fields ALL
from provenance (`completeness:81-142`, `_build_completeness:527-556`)".

Actual `_build_completeness:547-556` + `_thematic_closure_errors:81-142`:

- Provenance-derived (4): `expansion_passes`, `final_pass_new_sources`,
  `final_pass_new_material_obligations`, `final_pass_new_material_obligations_open`
  (bound to `research_pass` in `survey_completeness_v2.py:101-141`).
- Operator-supplied, NOT provenance-derived (4): `targeted_gap_fill_completed`,
  `open_material_obligations`, `limitations`, `status` (copied from
  `closure_input`: `:552-555`; `COMPLETE/LIMITED/NEEDS_RESEARCH` judgment enforced in
  `:2224-2242` with residual-subset + gap-fill + zero-open predicates).

Map must split 4-proven vs 4-operator, cite the validator that binds each, and refuse
`SOURCE passes`-style false-completeness against actual `research_pass` provenance.
No boolean-operator shortcut for status.

### B6 — New-helper return shapes still ellipsis; ROOT Qs left open

R2 leaves as "Astra confirms before code":

- `find_declaration_loss(root_records, effective_records)` → `list[(parent_id,OID)]`,
  `compute_obligation_universe(...)` split vs single-home (R2 §1.2, C-R2 Q1);
- `resolve_prepackage_root_effective` full data return (paths? SHAs? counts? R+E lists?
  marker kind?) — R2 §1.3 gives name + inputs only;
- keyword-only spelling `validate_interactive_input(...,*,discovery_records,root_discovery_records)`
  + `_validate_completeness_input(...)` confirmed, but `_build_completeness` tuple KEEP vs
  internal derivation, agent-first wrapper `*args/**kwargs` forwarding breakage with new
  REQUIRED kwargs (`run_evidence_v2_agent_first.py:88-91`), and HIGH function-local import
  shape for pure leaves are all deferred.

Gate §4 requires exact new/changed signatures, FULL data return shapes, caller census
including test helpers, insertion order before writes/idempotent branches. Ellipsis +
"confirm later" is NOT_READY. Pin every signature, return dict keys, `None`-refuses rule,
and the complete prod/test/adapter caller list with the S1-root-source, runner-table,
and adapter thin-vs-delete decisions resolved (not listed as open Q1–Q7).

### B7 — Authority hashes still mistranscribed in C-R2 (proof-C blocker)

Normative (verified `wc -c` 20472B / 7225B):

- Decision FULL `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54de260527e2d`.
- ROOT FULL `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`.

`source-family-closure-map-r2.md:7-8` still prints truncated forms
(`...5b5d74e260527e2d`, `...9729a65...`, missing `cdbc9b205b1eec54d` / `e`),
despite §1 claiming hash correction. Integrated JSON authority block is correct;
the R2 md is not. All future maps must copy the FULL hashes byte-exactly from
`outputs/...` / `astra-review-resolution.md`; truncated tool-output reads are never
authority. Also `source-family-closure-map-r2.json` is a single 33,928B line —
reviewable only via byte tools, not `Read`-truncated preview; keep literal arrays
in the md or split JSON lines so reviewers can verify member-wise without execution.

### B8 — Missing operations table: history-valid vs new-refuse + multi-source + noop/idempotent/partial-failure

Decision §6.4–6.6 + gate §4 require a concrete oracle table. R2 §9 lists planning-only
bullets, not a bound table. Required before code (no new tests run now, but sites,
orders, and expected refuse/preserve behavior must be pinned):

- Old-history valid loss vs NEW refuse: old accepted graphs WITH declaration loss remain
  valid under their accepted contract; new S1/S2/N1/E1/E2/H1 refuse `DECLARATION_LOSS`
  before writes. State which validators stay historical-only
  (`validate_discovery_expansion`, `_content` cores, renewal content cores) and that
  idempotent re-reads (`S2:953-954`, `E2:1191-1192/1864-1865`) preserve original validity
  and MUST NOT apply new policy to history.
- Multi-DID / multi-source: ambiguous primary-subject refused rather than coerced;
  two parents sharing one OID with global-set equality but `(R2,O1)` uncovered →
  `DECLARATION_LOSS` refuse (synthetic D1/D2 labelled); DROP/HOLD/CONTEXT never erase
  declarations; DROP excluded from tasks (`prepare:601-604`) but still loss-checked.
- Noop / idempotent / partial-failure: `U==P` initial-only 3-field pass (WEEKLY `2026-W35`
  null, THEMATIC `SP001` 3→8, RETRO `SP-2025-H2` null); re-accept idempotent branches
  without new-policy re-gating; guarded no-overwrite (`exists-or-symlink→refuse`,
  digest-dir `exists` check, HIGH `O_EXCL` only) + failure windows (TOCTOU preserved,
  partial PRESERVED, `INDETERMINATE` preserve, no auto-rollback) per site S1/S2/E1/E2/E3/N1/H1.

### B9 — True-R/E propagation across ALL LOW+HIGH sites not yet closed

R2 §6 lists LOW `derive_before:1172`, `package:1310`, `cards:1458`, `accept:1550`,
`ledger:1675`, `completeness:1795`, `prove:2002`, `check:2401` + HIGH prepare/adopt/resume/readback
as receiving "TRUE validated root context". Actual code today derives R/E inside each
builder from request refs + before-State COPY bytes (`derive_before_context:1196-1297`:
COPY SHA/byte_count → COPY triplet → `load_typed_checkpoint_record` → live re-hash
`:1227-1236` → `read_jsonl+validate_discovery_set:1247-1255` → non-DROP allowlist +
exact-cover `:1256-1272` → OLD 4-artifact graph `:1273-1297`), but:

- HIGH prepare still calls `_validate_*_content(...,None,None)` at `:677/:682` (E-as-R gap).
- The exact per-site parameter change (which functions gain `root_records/root_path`,
  positional vs keyword-only, `None`-refuses rule) and the full LOW/HIGH callsite
  propagation (HIGH `prepare:603,618,686,695` LOW-builder calls, `adopt:1140` prove call,
  all `None,None` / E-as-R passers) are not pinned with before/after signatures.
- Cross-bind `request.discovery_ref==E`, `request.screening_ref==selected old Screening`,
  logical State paths stay canonical with COPY supplying bytes — correct direction, but
  the map must prove no new request field/schema is needed by showing the before-State
  already carries the chain, and return the exact gap if any R authority is
  absent/unrecoverable (gate §3). No broadened RETRO DM022 schema, no next complete-reader
  contract, no new family presumed.

## 3. Minimum coherent repairs (no code; map-only)

1. Replace R2 §6 typed-proof with pure Discovery/Screening chain (B1): cite
   `read_jsonl/validate_discovery_set/SHA/accepted_ids==root_ids/DIRECT-vs-DERIVED`
   + `_canonical_root_acceptance`; delete `_verify_own_epoch_commit/_verify_adopted_graph_full/
   _verify_completion_full` from ordinary admission; keep them HIGH/LOW lifecycle-only.
2. Respec pre-package helper as paths-only with exact return dict + SHA/ID/count/schema
   checks + DIRECT-vs-accepted-marker truth table (B2); list every caller + CLI shape.
3. Correct HIGH table to first-COPY `:538` + 7-slot COPYs, place DM016/DM017 before first COPY
   and re-verified at adopt before guard claim (`:1127`) / proof write (`:1140-1142`);
   fix `None,None` sites `:677/:682` to true R/E (B3/B9).
4. Fix residual order to closure-first + residual-append per `agent_first:66-69`; state
   current COPY vs proposed UNION explicitly (B4).
5. Split closure 4-proven vs 4-operator with validator cites; drop "all 8 from provenance"
   (B5).
6. Close all signatures + FULL return shapes + caller census (prod/test/adapter) +
   S1-root-source / runner-table / adapter thin-vs-delete / HIGH-import decisions —
   no open Qs carried into code (B6).
7. Reprint FULL decision/ROOT hashes byte-exact in every map; split or mirror the
   single-line closure JSON so `Read` can verify literals (B7).
8. Add the §2 operations table: history-valid vs new-refuse, shared-OID loss, unknown-type
   incl DROP, 3/5/U exactness, multi-DID/source ambiguous-primary refuse, noop/idempotent/
   partial-failure + guard/no-overwrite windows with no new-policy on history branches (B8).
9. Provide per-site LOW/HIGH true-R/E before/after signatures + cross-bind proof + missing-R
   gap rule; explicitly scope DM022 `research_profile` to WEEKLY/THEMATIC, RETRO excluded,
   non-four-family/Retro reader deferred (B9).

Scope: existing Evidence, Screening, normal interactive Evidence, agent-first entry,
HIGH eligibility + LOW pure helpers, tests/docs only. No new schema/module/family ID,
no old-closure rewriting, no Production refresh/rebaseline, no Human Commit readback.
SourceClass/claim table stays normative fixed-10 (decision §3); field maps stay
`SourceClass`/claim; no default-SECONDARY.

## 4. No repeated audit; stop point

This review does not re-audit DM022 closeout, renewal, editorial, P1/P2R/P2V/P3S,
or the full 133-path source. It binds only the pre-code readiness gate above.
On repair completion: fresh readiness check + Astra confirmation required BEFORE code.
Then stop at Human Commit Point; non-four-family/Retrospective complete-reader/correction,
representative quality, fixed candidate/diagnostics/audit, Human adoption/operation,
and measured work reduction remain OPEN. Whole NOT_READY / step4B3 OPEN /
audit unstarted / DM021+022 OPEN; Profile/quality/adoption/savings OPEN.

## 5. R3 review (2026-10-31, docs-only) — verdict remains PRE_CODE_NOT_READY

Read R3 as combined proof (no author PASS trust): `integrated-readiness-r3.md` (69,124B,
830 lines) + `integrated-readiness-r3.json` (32,572B, multiline). No imports/tests/Git/
network/Human readback. Source still READONLY final133. B1–B9 above preserved; this §5
is the R3 delta verdict against B1–B9 + ROOT §5. Dedicated root-kernel parallel return
`detached-root-context-map` is not yet basis-reviewed; code stays BLOCKED until that
kernel + this coupled map are jointly closed.

R3 advances retained (not re-blocked): residual order fixed closure-first (§5.1 per
`agent_first:66-69`); HIGH first-write corrected to first COPY `:538` + 7-slot COPYs with
adopt prefix `:1127/:1140-1142`; decision/ROOT FULL hashes correct (§0 + JSON authority);
caller census + runner-remove / adapter thin-delegation + Q-closure substantially narrowed;
history-vs-new + noop/idempotent/partial-failure tables added (§§9–10).

Remaining BLOCKERS (minimum delta repairs, map-only):

### RB1 — R3 §4 still labels LIVE-State-bound loaders as State-free

R3 `§4:336-343` lists as "State-free file/contract/digest": `screening.validate_acceptance`
+ public `resolve_effective_discovery_basis` (+ `_resolve_effective_discovery_basis_content`
+ `_validate_screening_acceptance_content` + evidence equivalents).

Actual:

- Public `validate_acceptance:897-916` calls `validate_package_basis:910` which loads LIVE
  State + `verify_state_basis:695-711` + `state_sha256` drift, then calls public
  `resolve_effective_discovery_basis:915` (which reads package State via
  `_canonical_root_acceptance:325-350` + `core.load_json(state)` + profile/source_root).
- Public `resolve_effective_discovery_basis:353-439` is State-bound via the same
  `_canonical_root_acceptance` + `accepted.validate_acceptance` + SHA/ID/count branch.
- `resolve_active_screening_acceptance:442-489` loads LIVE State `:456`, enforces
  post-Screening lifecycle `:459-462`, calls `agent.resolve_checkpoint_artifact:467-473`
  + `current_stage_basis_override:482` + LIVE `validate_acceptance:483`.
- Only `_content` variants are State-free: `_resolve_effective_discovery_basis_content:809-856`
  (explicitly "never calls `_canonical_root_acceptance` nor checkpoint/override", session
  root from caller `:819-822`), `_validate_screening_acceptance_content:859-894`,
  `evidence._validate_screening_acceptance_content:1352-1409`,
  `_check_screening_package_files_content:629-651`,
  `_validate_screening_package_basis_content:654-693`. `discovery.validate_acceptance:274-298`
  is State-free (cfg + x_manifest + Raw/graph re-hash, never State).

R3 correctly forbids `_canonical_root_acceptance:325-350` in LOW recovery (`§4:324-327`),
but other transitive LIVE paths above remain listed as pure. Repair: split §4 into
public-LIVE-entry column vs `_content`-State-free column; LOW/detached map may cite only
`_content` + `discovery.validate_acceptance` + `read_jsonl/validate_discovery_set/expansion`.

### RB2 — Ordinary DiscoveryCP DOES contain record-owned Contract8 (R3 says none)

R3 `§4:347-349` says ordinary roles use "original recorded tools
(`implementation_sha` threading + `verify_state_basis` at current-operation entry only)"
with no Contract8. Actual ordinary checkpoint verifies Contract8 via agent:

- `_validate_checkpoint_record:770-904` → `_validate_core_stage_report:665-731` with
  required report keys `:680-684`, lifecycle/issue `:692-697`, profile/state authority
  `:698-712` (historical State path only `:710-712`), `contract:713-717`
  (`expected_contract=record.get("contract")` vs `core.contract_identity`, not LIVE recompute),
  `implementation:718-722` (record-owned `repository_commit_sha`), artifacts `:730-731`,
  all artifact/review refs re-hashed `:865-887`.

Repair: state ordinary CP includes record-owned Contract8 + impl + report predicates
(cite `:680-722/:865-902`), historical-state-path rule, never LIVE recompute; keep
Contract8 out of LOW bodies (agent entry only, per LOW header `:12-18`).

### RB3 — R3 §6.4:569 accidentally applies ordinary 3/5 to HIGH

R3 line 569: "NEW DM016 + DM017 + 3/5/U shape run BEFORE first COPY". HIGH DM022 uses
7-field `fullObligation` (`dm022-revision-request-v2.schema.json:232-244` `minLength:1`)
+ LOW fallback, separate; decision §4.2 / R3 §5 itself keeps ordinary 3/5 gate "never
reused for DM022". Repair: delete "+ 3/5/U shape" from H1 prepare/adopt; HIGH new-operation
= unknown-source (canonical leaf per R `source_records` incl DROP) + loss per
`(parent,OID)` on R effective basis + request shape only, before first COPY `:538` and
re-verified at adopt `:1127` + before `:1142` proof write.

### RB4 — §5.2 heading "4 provenance + 4 operator" misclassifies row-status COUNT

Formula right, heading wrong. Actual `_build:520-523,535`:
`needs_research=sum(status==NEEDS_RESEARCH)`, `open_material_obligations=needs_research`.
That is a row-status COUNT — neither `research_pass` provenance nor operator judgment
(`targeted_gap_fill_completed:bool`, `limitations`, `status` are the 3 true operator
inputs, cross-checked `:2224-2243`). Residual order fix retained. Repair: rehead as
4 provenance + 1 row-status COUNT + 3 operator (or 4-3-1), keep formulas; no code change.

### RB5 — Patch hash still short by `f3`; decision/root correct

R3 §0 + JSON `patch_sha256` print `...7144f1c494...` (62 chars), missing `f3` vs actual
full 64-char `...7144f1f3c494...`. Decision FULL `62b14add...` /20472B and ROOT FULL
`021a0d7c...` /7225B are correct — retain byte-exact. Baseline `774dd39a...` unchanged.
Repair: reprint patch FULL 64-char + `wc -c` 4931836B / manifest 185422B; transcription
only, no frozen-source alteration.

### RB6 — Prepackage truth-table + return MODE gaps

(a) R1 `is_file()==False → absent → DIRECT` conflates absent vs nonregular/unreadable:
symlink/dir/unreadable marker must refuse, not DIRECT. (b) Missing State-provenance
required-root check: if State `checkpoint_provenance` claims accepted Discovery expected,
missing marker is a gap (refuse), not initial DIRECT; R3 §6.2 R5 states the principle
(marker alone / lifecycle alone never authorizes) but R1–R4 rows do not enforce it.
(c) `accepted_discovery_path` "auto-derived, explicit only for tests" has no source-binding
proof: caller/test path must still bind via `_repo_file` + SHA/ID/count/schema to the
State-bound accepted path, not caller assertion; no `allow_unbound` flag (already
forbidden — preserve). Actual test semantics preserved: initial-direct legacy
(`resolve_effective:382-395` DIRECT) + canonical-marker bind, no unbound bypass.
(d) Return `mode: DIRECT | ACCEPTED_BOUND` (+ `marker_kind`) collapses DIRECT vs
DERIVED: downstream needs `DIRECT vs DERIVED_EXPANSION` (cf. `_content:851-856` +
`:428` expansion) for loss/expansion handling. Repair: split R1 absent vs
nonregular/unreadable-refuse; add State-provenance required-root predicate to R1–R4;
pin caller-path binding checks; return `mode: DIRECT | ACCEPTED_DIRECT | ACCEPTED_DERIVED`
(or keep `ACCEPTED_BOUND` + `derivation: DIRECT | DERIVED_EXPANSION` field) with exact
branch predicates.

### RB7 — Generic `full` / `TRUE` / `unchanged` claims remain; kernel + coupled map OPEN

R3 §§4/6/8 still assert "FULL checks", "FULL dict", "full content proof",
"TRUE validated root context", "config/source-family unchanged" without per-site binding
for every LOW/HIGH callsite (which of `derive_before:1172/package:1310/cards:1458/
accept:1550/ledger:1675/completeness:1795/prove:2002/check:2401` + HIGH
`prepare:603,618,686,695/adopt:1140` gains `root_records/root_path`, positional vs
keyword-only, `None`-refuses, before/after signatures). C-R2 membership direction is now
correct (Evidence/Screening staged, drivers not, HIGH/LOW both staged+canonical via
`DM022_7`), but "unchanged" still needs actual frames: exact-76 list + member-wise
equality + fresh CURRENT proof (`_derive_current_family_from_disk`,
`verify_tool_basis`/`_verify_head_bytes`, Contract8, callsite pins) per §8, never counts.
Current/idempotent side-effects (§§9.3/10) + unused-class-helper disposition still generic
per branch (S1 fresh-temp vs S2/E2 idempotent vs H1 exclusive vs resume
`ALREADY_ACTIVE`/`INDETERMINATE`). Repair: replace each generic with exact
predicate/site/arg binding; keep code BLOCKED until kernel `detached-root-context-map`
+ this coupled map are jointly reviewed and Astra confirms.

Verdict: R3 is a major delta repair but RB1–RB7 remain. No author PASS trust. No code
readiness until RB1–RB7 delta + kernel & coupled map closed + fresh readiness + Astra
confirmation. Preserve whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN;
Profile/quality/adoption/savings OPEN. Stop at Human Commit Point.

## 6. R4 review (coupled R3 + focused kernel + ROOT §6; docs-only) — logic READY bounded, gate still NOT_READY

Read actual R4, not author "all closed" claim: `integrated-readiness-r4.md` (37,038B,
436 lines) + `integrated-readiness-r4.json` (16,638B) + coupled kernel
`detached-root-context-map.md` (18,627B) + `.json` (10,130B) + ROOT gate FULL including §6
(`astra-precode-gate-resolution.md` 13,968B SHA256
`da37cb8dcf931377075ef01219539206c4fa5f447589f6cb2d7bd74150dbb544`, verified by
`wc -c`/`sha256sum`; §§1–5 unchanged, §6 new). No imports/tests/Git/network/Human
readback. Source still READONLY final133. §§1–5 above (B1–B9, RB1–RB7) preserved.

Spot-verified against final133 bytes (text-read only):

- Public Screening `validate_acceptance:897-916` calls `validate_package_basis:910`
  (loads State, `sha256(state)==basis.state_sha256`, `verify_state_basis:695-711`) +
  public `resolve_effective:915` (via `_canonical_root_acceptance:325-350` LIVE State);
  `resolve_active:442-489` loads LIVE State `:456` + `agent.resolve_checkpoint_artifact:467-473`
  + override `:482`. Only `_content` siblings are State-free
  (`_resolve_effective_content:809-856` never canonical/checkpoint/override `:819-822`,
  `_validate_screening_acceptance_content:859-894`,
  `evidence._validate_*_content:1255-1283/1322-1349`, `_check_*_content:629-651/654-693`).
  R4 §RB1 correctly splits public-LIVE vs `_content`-only (R3 error closed).
- Ordinary checkpoint carries record-owned Contract8: agent
  `_validate_checkpoint_record:770-904` → `_validate_core_stage_report:665-731` with exact
  12 keys `:680-686` (not 13), `CORE/PASS:687-688`, lifecycle/issue `:689-697`,
  profile `:698-701`, state live-equality if `state_path is not None:705-708` else
  historical canonical-path-only `:710-712` (no live SHA — preserved), contract
  `expected_contract=record.contract:713-717` (no current recompute),
  impl `:718-722`, `recorded_at:723-726`, artifact-map equality `:727-731`. R4 §RB1/RB2 +
  kernel §1 state this exactly (FILE vs result-set digest split, previous ECP vs DCP,
  exactly-1 CORE row `:665-667` not a ban on extra schema-valid rows, all deterministic
  refs rehashed `:878-890`). R3 "no Contract8" closed.
- S1 `prepare_package:492-567` entry `ISSUE_INITIALIZED|DISCOVERY_COLLECTED:504-505`,
  non-empty refuse `:517-518`, batch `mkdir:520` + `write_jsonl:525` + `write_json:566`
  (check-then-write, NOT O_EXCL); H1 first COPY `:538` `_copy_regular_exclusive`,
  7-slot COPYs `:563-600`, candidate only `:605` `_exclusive_write_bytes:83`,
  adopt `_prove_before_graph_unbound:1127` before guard + `prove:1140` before proof
  write `:1142`. R4 operation branches cite these orders exactly (source-first
  read→write order correct).
- New-helper spellings are syntactically valid plain Python (no `required-after-optional`
  `SyntaxError`): public loaders positional PATHS-only
  (`(repo_root,request_path,before_copy_path)`, `(repo_root,request_path,live_state_path)`,
  `(repo_root,state_path,discovery_path,accepted_discovery_path|None)`), private kernel
  keyword-only after bare `*` (`def _derive_root_effective_kernel(*, repo_root, ...)`),
  existing `*_from_paths` keep positional + add keyword-only `*, before_copy_path: Path|None=None`
  (valid `X|None=None` optional). Schemas unchanged; no new module/schema/family presumed.
- Closure heading now correct 4+1+3 per ROOT §5 formulae (R4 §RB7): provenance/status-derived
  4 (`expansion_passes/final_pass_new_sources/final_pass_new_material_obligations(_open)`
  via `research_pass` + `MATERIAL_OBLIGATION_STATUS`), row-status COUNT 1
  (`open_material_obligations=needs_research`), operator-fed 3
  (`targeted_gap_fill_completed/status/limitations` closure-first + residual-append per
  `agent_first:66-69`, cross-checked `:2184-2243`). R3 "4 operator" withdrawn.
- HIGH 7-field only vs normal 3/5 fixed (R4 §RB5; R3 §6.4:569 withdrawn):
  HIGH uses `fullObligation:232-244` + loss/classification before first COPY; ordinary 3/5
  stays N1-only.
- Prepackage truth table preserves lstat-ENOENT-only absence (R1), expected path can never
  override State/canonical marker (R2–R5, no `allow_unbound`), `authorityKind`
  `NO_MARKER|STAGE_CLAIMED|CANONICAL_MARKER` + `basisMode` `DIRECT|DERIVED_EXPANSION`
  split (ambiguous `ACCEPTED_BOUND` removed). Root/E propagated all sites, no
  `None→DIRECT` (DIRECT only via `derived.resolve()==root.resolve()+sha equal:413-426` /
  content `:851-854`, else `DERIVED_EXPANSION:428`; `_content None→DIRECT:837-843`
  stays history-only for legacy fixtures).
- Closure matrix records actual import edges (Evidence top `core,schema_gate,screening:21`,
  Screening top `core` only + function-local `:397`, LOW top `core+schema_gate:48-49`,
  HIGH `core,schema_gate,low` + function-local `agent:312,466`/`evidence:616,673`);
  new policy only at new writers (S-prepare/S-accept/E-prepare/E-accept/views/N1/HIGH-prepare/adopt),
  idempotent/history branches revalidate without new gates (`S2:953-954/E2:1191-1192`);
  recipe/control current-proof unchanged member counts are logical field binds
  (exact-76 + member-wise equality + fresh CURRENT proof), never a promise of old PASS.
  Caller `derive_before` previous-checkpoint bind is `before_checkpoint.evidence` (ECP
  ArtifactRef) + COPY evidence provenance, never Discovery provenance; before/after
  ArtifactRef/SizedRef/NamedRef typeFields preserved per §RB2.

Remaining BLOCKERS (minimum delta; transcription / hardening only, no runtime):

1. Metadata pins still wrong in R4 (gate-final hash blocker): R4 §0 line 17 + JSON
   `authority.patch_sha256` print `...7144f1c494...` (62 chars, missing `f3`) vs ROOT §6
   FULL 64-char `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260`
   /4931836B. Decision FULL `62b14add...` /20472B, ROOT FULL `021a0d7c...` /7225B, manifest
   FULL `31fa4a72...` /185422B, gate `da37cb8d...` /13968B, kernel md `6d80ffeb...` /18627B
   + json `fac3e0e3...` /10130B are correct in R4 JSON — retain byte-exact. Baseline
   `774dd39a951c9ac3818e83dfffd4c7666efb0a20` is a 40-hex commit (not SHA256) — R4 §0
   line 18 labels it correctly; any JSON field naming it `*_sha256` must be relabeled
   `baseline_commit`, not hashed. Repair: append correct FULL patch string (add `f3`)
   + relabel baseline field; prior truncated strings are never alternative identities.
   No frozen-source alteration; transcription only. Required before gate final hash;
   no final case-acceptance overclaim.
2. Optional-`None` hardening (path-only rule): R4 §RB4 still spells five LOW
   `*_from_paths` extensions as keyword-only `*, before_copy_path: Path|None=None`
   (+ `*, request_path` where missing) with "derive from request/manifest refs if
   possible, else refuse". Any derivation from LIVE `request.before_state.path`
   (logical path, not COPY) or basename-only is FORBIDDEN — R4 already rejects this for
   cards ("Cannot (logical path, not COPY)" → HIGH must pass retained
   `rev_root/retention/state-before.json` explicitly, else refuse) and for accept
   ("HIGH passes both explicitly; refuse if absent"). Harden to: `before_copy` may be
   derived ONLY from validated `checkpoint.revision_root` + `retention_plan{path,sha256,
   byte_count}` (SizedRef `_verify_sized_ref_bytes`) + `before_state.sha256/byte_count`
   bound (`f"{revision_root}/retention/state-before.json"`, `sha==manifest.before_state.sha256`)
   and only when a bound CP exists (`checkpoint.retention_plan` + `revision_root` present,
   e.g. DM022 adopted path); legacy checkpoints without those fields, and all new-operation
   entry points without a bound CP, MUST take REQUIRED keyword-only PATH inputs on all
   calls/tests (no `=None` default, no best-effort/hypothetical fallback). `root None`
   never means DIRECT; `derive_before_context` 4-positional compat shim must validate a
   caller-supplied `previous_checkpoint_path` against derived `before_checkpoint.evidence`
   (ECP), never trust it. Repair: change `=None` to REQUIRED on new-operation signatures
   (keep `=None` only where the bound-CP derivation above is proven + refuse-otherwise),
   delete any `request.before_state.path`/basename fallback sentence; re-list all
   callers/tests with explicit PATH args.

Otherwise R4 + kernel close RB1–RB7 and the §6 contract extension (items 1–5) is precise
for ROOT decision. No new code/tests/Git/network/Commit/Human readback authorized.

Verdict: DESIGN MAP READY bounded (technical logic closed subject to blockers 1–2);
GATE still PRE_CODE_NOT_READY until (1) correct pins appended, (2) REQUIRED-PATH
hardening applied with full caller list, (3) fresh readiness re-check of that delta +
final Astra confirmation BEFORE code. No code authorization; no final-case acceptance.
Preserve whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN;
Profile/quality/adoption/savings OPEN. Stop at Human Commit Point.

## 7. FINAL R5 readiness verdict (ROOT path-hardening delta; docs-only)

Read FULL, no author PASS trust: `integrated-readiness-r5-path-hardening.md` (8,429B,
SHA256 `502d3bfac0bd47b022c66c3e64690408be1610c68963051cdd09c2ab3690bb25`) +
`.json` (2,926B, SHA256 `df8c041ba7ce13688b94f2b3b0f615d4be48f1d54b8638b8351112873aa5a0b4`)
— actual R5 author-ROOT delta, documentation only (`status:
DELTA_FOR_INDEPENDENT_REVIEW_NOT_IMPLEMENTATION`, `runtime_executed: false`).
Working ROOT gate snapshot §§1–6: `astra-precode-gate-resolution.md` 13,968B SHA256
`da37cb8dcf931377075ef01219539206c4fa5f447589f6cb2d7bd74150dbb544` (verified by
`wc -c`/`sha256sum`; §§1–5 unchanged, §6 binds R3 + kernel). This is a working-gate
snapshot, NOT the contract ROOT (`astra-review-resolution.md` FULL
`021a0d7c…`/7225B INCLUDING §5); if the gate later appends §7+, its hash changes —
do not mistake this snapshot for a full ROOT. §§1–6 above (B1–B9, RB1–RB7, R4 review)
preserved as NOT_READY history; this §7 is the FINAL delta verdict only.

Source final133 unchanged, READONLY
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(actual409/tree8ce +133paths54M79A/768). No imports/runtime/tests/build/fixtures/network/
Git/Commit/Human readback. Data-only length/hash validation only (no candidate execution).

### Pins now full (length-validated, transcription-corrected)

Data-only hex-length check (all hex, no alternative identities):

- Decision INCLUDING §7: `62b14add…` 64ch /20472B. Contract ROOT INCLUDING §5:
  `021a0d7c…` 64ch /7225B. Patch: `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260`
  64ch /4931836B (R5 §1; R3/R4 62ch missing `f3` withdrawn). Manifest:
  `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` 64ch /185422B.
  Baseline **commit** `774dd39a951c9ac3818e83dfffd4c7666efb0a20` 40ch (not a SHA256 field;
  R5 §1 labels it correctly; any `*_sha256` naming for it must read `baseline_commit`).

R3/R4/C-R2 truncated headers identify no alternative artifact; literal closure arrays are
consumed only with the corrected binding above + actual membership checks.

### Last-2-findings closure (R5 deltas verified against R4 text)

1. Four public LOW APIs are now REQUIRED keyword-only PATHs, no `None` (R5 §2 exact
   blocks; ellipses denote bodies only, R4 predicates apply):
   `build_revision_cards_views_from_paths(..., *, before_copy_path: Path)`,
   `accept_revision_evidence_views_from_paths(..., *, request_path: Path, before_copy_path: Path)`,
   `build_versioned_ledger_from_paths(..., *, request_path: Path, before_copy_path: Path)`,
   `build_versioned_completeness_from_paths(..., request_path, old_completeness_path, *, before_copy_path: Path)`.
   Valid plain `*, x: Path` required-keyword syntax (no `required-after-optional`
   `SyntaxError`); no supplied collection/Context/verified-flag added; `None` refuses;
   never infers COPY from LIVE logical path or basename. HIGH prepare supplies
   `request_abs` + verified `rev_root/retention/state-before.json`; all direct test calls
   supply the same explicit keywords from actual fixture artifacts (mechanical migration at
   implementation, not executed here); acquired DATA drivers not edited. Existing
   4-positional `derive_before_context(repo_root,request_path,before_copy_path,
   previous_checkpoint_path)` / `build_revision_package_from_paths` /
   `prove_revision_from_paths` / `check_supersession_record_from_paths` preserved with
   required PATHs; supplied previous path must equal ECP
   (`request.before_checkpoint.evidence` == COPY `checkpoint_provenance.evidence`, file SHA
   checked), never DCP. New loaders `derive_ordinary_root_effective_context` (LOW,
   pinned COPY) + `derive_current_root_effective_context` (HIGH, after strict LIVE
   eligibility, before first COPY) remain required positional PATHs, no fake future COPY.
2. Private adopted-full retains 3 args (`repo_root,checkpoint_path,checkpoint_sha`; R4
   optional `before_copy_path` removed; R5 §3). Record-bound internal derivation only:
   exact-SHA checkpoint + request SizedRef + revision identity/root + retention-plan
   SizedRef + manifest + `before_state` SHA/byte_count → fixed
   `revision_root/retention/state-before.json` → LOW D/S context loader. Never reads
   `request.before_state.path` for historical bytes; never basename discovery; never
   optional public COPY default; never context→adopted-full recursion (one-way: D/S-only
   context → outer ECP/full). Ordinary history contract is record-owned Contract8/
   implementation with canonical historical State path only (R5 §3 line 64: no
   `core.contract_identity` fallback with supplied record contract); exactly-1 matching
   CORE row (extra schema-valid rows permitted, all deterministic refs rehashed); FILE SHA
   vs `result_set_sha256` recomputed digest/run-dir identity distinct.
3. S1 expected-path semantics (R5 §4): `None` = no additional expectation, helper still
   derives canonical marker + State provenance, never suppresses a present marker;
   non-`None` must match independently derived canonical/State-bound authority
   (foreign/missing/mismatched refuse); ENOENT-only absence; symlink/nonregular/unreadable/
   malformed refuse; State DCP claim must bind DCP/acceptance chain, never initial DIRECT.
   `authorityKind` × `basisMode` (`DIRECT|DERIVED_EXPANSION`) split retained; unknown-type +
   per-parent loss preflight before first directory/COPY write; legacy direct-basis
   resolvers unchanged.
4. R4 stands (current-vs-history, pure-CP 12 keys `agent:680-686`, record-owned contract
   no current fallback, 4+1+3 closure + closure-first residual, HIGH DM0227 with no
   ordinary 3/5, literal membership + control/current-proof obligations, operation-branch
   source-first orders, planning-only oracles). No new schema/module/family, no old-record
   rewrite, no default class/permission token.

Declared mandatory oracles remain planning-only predicates for implementation; they are
NOT runtime proof here, and no new unapproved network is required or authorized.

### Whole-map precedence + qualifications for ROOT final

Precedence (conflicts): R5 overrides R4/R3/kernel conflicting signatures, fallback
sentences, and transcription errors; otherwise R4 operation branches + kernel loader +
R3 census + C-R2 arrays + decision §§6–7 / ROOT §5 / gate §§1–6 stand. R3 "all closed"
stays WITHDRAWN; R4 optional-`None` sentences are superseded by R5 REQUIRED keywords;
C-R2 headers remain invalid transcriptions.

Small qualifications to bind at ROOT final (no conditional waiver invented):

- Test-keyword migration (R3/R4 census fixtures → explicit REQUIRED keywords) is
  implementation work with actual fixture artifacts; DATA files stay unedited, no
  test-only fallback permitted.
- HIGH current loader vs LOW COPY loader permission split stands: shared kernel confers
  none; permission comes from HIGH eligibility vs LOW COPY pin.
- No full-suite/test-count sum; no Production refresh/rebaseline; no Commit readback.
- Any future gate append (§7+) changes the working-gate hash; rebind that snapshot hash
  at final, do not reuse this §7 snapshot as a full ROOT.

### Verdict

No essential pre-code gap remains. **PRE_CODE_READY bounded** (pre-code map complete:
R2 B1–B9 → R3 RB1–RB7 → R4 logic → R5 path/transcription hardening, all source-pinned).
Whole-map precedence as above. Code remains BLOCKED until ROOT future confirmation
(final Astra confirmation) AFTER this review; then stop at Human Commit Point.
Non-four-family/Retrospective complete-reader/correction, representative quality, fixed
candidate/diagnostics/audit, Human adoption/operation, measured work reduction remain OPEN.
Whole Step4B3 OPEN / audit unstarted / DM021+022 OPEN; Profile/quality/adoption/savings OPEN.

(End — independent FINAL R5 readiness verdict; PRE_CODE_READY bounded; ROOT future confirmation required before code.)

## 8. FINAL-BINDING ROOT confirmation (gate §7 appended by ROOT; docs-only)

Read FULL gate with appended §7, no author PASS trust:
`notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md` FULL
20,159B SHA256 `bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa`
(data-only `wc -c`/`sha256sum`; §§1–6 unchanged, §7 new FINAL-BINDING, 93 lines total).
This FULL (with §7) is bound separately from the old working §§1–6 snapshot 13,968B
SHA256 `da37cb8dcf931377075ef01219539206c4fa5f447589f6cb2d7bd74150dbb544`
(which remains valid history for §§1–6 only, never a full ROOT). §§1–7 above preserved.

§7 (lines 69–93) declares **PRE_CODE_READY — bounded interface/design map only**,
superseding the working NOT_READY; prior author/review errors remain history. No
implementation/runtime/import/test/build/fixture/restore/network readback occurred in
the pre-code unit. Implementation map = R3 inventory + C-R2 literal arrays + focused
detached-root map, overridden by R4, then R5 hardening, then this full ROOT resolution;
`integrated-readiness-r5-path-hardening.md/json` to be read in full; R3/R4 optional
defaults, ECP/DCP confusion, LIVE-labelled-pure functions, wrong closure headings and
mistyped pins are not alternative instructions. Selected contract FULL
`62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` /20472B INCLUDING §7
and contract ROOT FULL `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`
/7225B INCLUDING §5 remain unchanged.

Verified §7.1–§7.2 introduce no waiver or broadening of any essential predicate:

- Four LOW public builders gain REQUIRED keyword-only PATHs (positions kept);
  `derive_before_context` validates supplied previous ECP against request/COPY evidence
  provenance; private adopted-full keeps 3 args, COPY derived only from verified
  checkpoint/retention/layout/before-State binding, never LIVE logical State.
- DCP/SCP ordinary checkpoints: schema/producer/issue/artifact/result hashes, exactly-one
  CORE, profile/report fields; historical report State path-only; record-owned
  Contract8/implementation (no current-contract fallback, no PREARCH seven-file proof);
  D/S-only recovery, outer ECP/parent proof separate and acyclic.
- HIGH current context after strict LIVE eligibility before first COPY; LOW historical
  context from pinned COPY + accepted refs; request discovery = E, R from accepted chain;
  explicit true R/path on all new content calls, never E-as-R / `None,None`.
- S1 marker/provenance derived canonically; supplied path expected-binding only;
  `None` never suppresses a marker; ENOENT-only absence; claimed-root mismatch never
  DIRECT fallback; documented initial-direct / initial-valid-marker cases kept, no new
  lifecycle gate.
- DM016 ten, ordinary 3/5→derived7, U, every `(parent,OID)`, DM0227 separation,
  closure-first residual union, 4 provenance/status counters +1 row-status count +3
  operator-fed closure fields fixed; no auto-fulfilment or class downgrade.
- New policy before new writes only; content-addressed reacceptance/readback keeps
  original predicates; no new policy in shared expansion/content validation; resume =
  bound admitted operation under existing guards/epochs/retained context.
- G76 memberships as mapped (no new runtime module/schema/family; pipeline76,
  replay70/union73, canonical36/41, DM022 seven-file pins; Evidence/Screening staged,
  HIGH/LOW also canonical, drivers control-root-bound not replay blobs); edits change
  tool bytes and require fresh CURRENT proof; no old PASS/epoch transfer; new gap →
  Astra before broadening.
- §7.2 scopes the WHOLE upstream implementation to AFTER the NEXT Human continuation
  (canonical10 + admission sites; root/effective prep + detached recovery; 3/5→7/residual
  parity; callers + adapter; DM022 prepare/adopt eligibility + historical readback; no
  helper-only completion; independent workcopy/snapshots; root reviews, not runs).
  Verification/oracles stay planning-only predicates here (NOT runtime proof, no new
  network): all-10 types + old mappings; unknown incl DROP refused pre-write; 3 Profiles;
  direct/agent-first parity; shared-OID/loss refusals; shapes/dimensions/statuses/
  traceability; healthy-history vs ineligible-new; DIRECT + DERIVED DM022 flows, repeat
  correction, downstream consumers; drift/guard/no-overwrite/idempotence/partial-failure/
  epoch/closure regressions. Compat `.py` stays DATA; synthetic fixtures never genuine
  approval nor TS-001 evidence. Closeout binds delivered source + meaningful runs +
  author-independent review + failed/partial outcomes; candidate/reconstruct Commit/Push
  Human-owned; no Production writes/intake/rebaseline. Non-four-family/Retrospective
  complete-reader next gate, then quality → fixed candidate/audit → operation → savings.
- Human Commit Point — stop, do not auto-start implementation. Whole NOT_READY/step4B3OPEN/
  audit unstarted/DM021+022 OPEN and Profile-wide acceptance/quality/adoption/savings OPEN
  refer to the broader gates, not this pre-code map. Line 93 requires final independent
  confirmation to bind the FULL resolution including §7, not the §§1–6 snapshot.

No contradiction found; nothing in §7 waives an essential predicate or broadens scope
(no new module/schema/family, no lifecycle gate, no `None`-DIRECT, no E-as-R, no
current-contract fallback, no PREARCH proof on ordinary checkpoints, no DATA promotion,
no runtime/adoption claim). Independent R5 verdict (§7 above) already PRE_CODE_READY
bounded on source/interface predicates; §7 confirms that same bound.

FINAL verdict: **bounded PRE_CODE_READY — source/interface map ONLY (not runtime,
not adoption, not publication)**. Whole-map precedence: decision §§6–7 / ROOT §5 /
gate FULL §§1–7 > R5 > R4 > R3/kernel/C-R2 (conflicts); otherwise all stand. Next: whole
upstream implementation ONLY after NEXT Human continuation, with updated assessment,
entry, and docs check as the last gate before code. Any newly discovered
import/reader/authority gap returns to Astra before broadening.

(End — FINAL-BINDING ROOT confirmation; bounded PRE_CODE_READY source/interface ONLY.)



