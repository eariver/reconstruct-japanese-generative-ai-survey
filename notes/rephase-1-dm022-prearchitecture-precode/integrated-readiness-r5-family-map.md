# DM022 — R5 family map delta (AUTHOR, PRE-CODE ONLY, closes R4-C1)

2026-10-28 AUTHOR delta. PRE-CODE ONLY. Human `ab84b4f` assumed.
No source/runtime/import/tests/build/fixture/restore/network/Git writes.
Actual93 proof-copy READONLY. No candidate/reconstruct Commit/Push.
Preserves EXACT: R4 `integrated-readiness-r4.md/json` + `schema-proposals-r4/*.schema.json`
(5 files), all R3/R2/reviews, `independent-readiness-review.md` §§0–6 (NOT_READY).
This file + `integrated-readiness-r5-family-map.json` are the ONLY writes of this unit.
No schema changes (no exact schema error). No MAP-COMPLETE/PASS.

Binds: decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B
(unmodified); root §5; BOTH FINAL-BINDING design reviews (selection only).
Source: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
= `409b292`/tree `8ce36998` +93/742. All `file:line` below proof-copy.
Method: `Read` + `Grep` (stdlib) + `ast` as DATA. No `scripts.*` imports.

R4 literal G67/G71/G76 lists kept (R5 JSON `families_*` verbatim from R4;
counts 67/71/76, 50/63/70/73, 29/34/36/41). This delta adds the missing
owned-epoch helper BRANCH replacements so old93 exact 67/71 checks do not brick 76.
No generic “update branch”; every predicate names actual function + signature +
argument origin + callsite branch condition.

## 0. Narrow compatibility selected (not auto-adopt)

ROOT already selected narrow G71→G76 mechanical compatibility subject to EXACT
listed code/schema/config addition + predicate-equivalence + UNCHANGED research/
Profile/Architecture/Draft/reader authority. This is NOT auto-adopt nor upstream
permission. Explicit operation admission recomputes ALL current proofs (U) or
checks (C) as normal with truthful Core reason, same prePreview window; HIST
family classification alone confers NO operation permission. G67 existing R3
adapter may compose known family delta under exact conditions; NO arbitrary
migration beyond G76. Any config/Profile/review/recipe/accepted-input semantic
delta outside allowed path + known schema-family fingerprint must refuse.
“no automatic 71→76” means none from family label alone; ROOT explicit narrow
validated adapter selected, not broad migration.

## 1. Owned-epoch families (literal lists kept in JSON)

- G67: pipeline OLD67 (67, `_OLD_PIPELINE_67:99-167`), staged OLD50 per-route
  (50 = OLD_PY_30 + OLD_SCHEMAS_14 + route3 + staged1 + style1 + recipe1),
  implicit3, quality3, roots. Historical only; no renewal modules; no PREARCH kind.
- G71: pipeline NEW71 (71 = OLD67 + 4 `_NEW_SCHEMAS_4:350-360`), staged NEW63
  per-route (63 = OLD50 + FAMILY_PY_2 + NEW_PY_3 + NEW_SCHEMAS_4 + FAMILY_SCHEMAS_4),
  canon Weekly29 (`survey_weekly_derivation_v2.py:28-58`) + Longform34
  (`survey_longform_generated_v2.py:52-87`), implicit3/quality3/roots.
  Current before DM022; no PREARCH kind.
- G76: pipeline NEW-DM76 (76 = NEW71 + 5 `schemas/dm022-*.schema.json`),
  replay per-route 70 (= NEW63 + 2 modules + 5 schemas), union73 (= 70 + other
  route3), canon Weekly36 (= 29+7) + Longform41 (= 34+7), implicit3/quality3/roots.
  New 2 modules pinned; HIGH file-pin ONLY, runtime-loaded root/bytes verified;
  P3S lazy bindings per current93 precedent; extra module => return root.
  Counts proposed, not measured source.

Derive owned family from EXACT config registered path sets + Contract8 recompute +
schema fingerprints + expected module/mode/membership, never 7-file presence/hard
count. Historical G67/G71 verification stays OWN epoch (no old tool LIVE).
Current G76 supports new PREARCH CP in accepted graph through initial
publication/editorial/renewal + normal lifecycle. New PREARCH only admitted G76
creation window; older histories no such kind.

## 2. Per-function branches (actual names, no invention)

### History historian (bootstrap: allow third exact set, identical predicates)

- `_recompute_contract8_at_epoch(repo_root, epoch, research_profile, publication_profile, label, _cache):169-260`.
  Origin: `repo_root` caller repo; `epoch` 40-hex from retained record/history graph
  (NOT live HEAD); profiles from record/basis; `label` caller string; `_cache`
  per-invocation dict. Current93: pipeline exactly OLD67 or NEW71 (71=OLD67+4new),
  else `UNSUPPORTED_MIGRATION`; versions `2.0-rc1`; quality3 exact; profiles 3+2;
  NUL-framed aggregate over pipeline + `DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA`
  (`:86-88`); mode `100644` else FAIL. R5: accept OLD67|NEW71|NEWDM76 (76 literal);
  NEWDM76 delta ONLY 5 DM022 schemas; recompute identically; unknown set
  (missing/extra beyond 4+5 delta, wildcard, partial) => `UNSUPPORTED_MIGRATION`;
  mode/blob missing => FAIL. Bootstrap ONLY third exact set + identical recompute.
- `_derive_tool_generation(repo_root, epoch, label, _cache):1304-1411`.
  Origin: `epoch` retained-record commit (NOT live HEAD). Current93: probe 7 renewal
  paths via `_git_tree_mode` at epoch; owned-epoch config pipeline OLD67/NEW71 exact +
  versions/quality/profiles + Contract8; 7+NEW71=>NEW; 0+OLD67=>OLD; 7+OLD67=>REJECT;
  partial=>UNKNOWN; 0+NEW71=>Contract8 BLOB_MISSING FAIL. R5: probe 7 renewal +
  7 DM022 paths (2 modules + 5 schemas, mode `100644` at epoch); pipeline
  OLD67/NEW71/NEWDM76 exact + Contract8 (updated fn) + schema fingerprints +
  module/mode/membership; 14+NEWDM76=>G76; 7+NEW71=>G71; 0+OLD67=>G67;
  7+OLD67=>REJECT; partial=>UNKNOWN; 0+NEWDM76=>BLOB_MISSING FAIL.
  Returns `G67|G71|G76` (not OLD|NEW); callers handle three values, no silent mapping.
- `_expected_receipt_closure(route, generation):1263-1277` / `_expected_staged_code_deps(route, generation=OLD):1280-1301`.
  Origin: `route` WEEKLY_GENERATED_V2|LONGFORM_GENERATED_V1 from caller record/graph;
  `generation` OWN-epoch derived G67|G71|G76 (never caller flag).
  Current93: OLD=>50 (30+14+route3+staged1+style1+recipe1); NEW=>63 (+2+3+4+4).
  R5: G67=>50; G71=>63; G76=>70 (63+2+5); union73 = union(weekly70,longform70).
  Unknown => `UNSUPPORTED`. Staged `_verify` enforces len 50|63|70 + sorted.
- `_verify_receipt_closure_exact(repo_root, closure, epoch, route, generation, label, _cache):1414-1450` /
  `_verify_staged_code_deps_exact(repo_root, code_deps, epoch, route, label, generation=None, _cache):1453-...`.
  Origin: `closure/code_deps` retained manifest lists (`{name,path,sha256}` /
  `{path,sha256,byte_count}`); `epoch` OWN-epoch commit; `generation` must equal
  derived else `HISTORY_TOOL_EPOCH_DRIFT`. Predicates unchanged: non-empty, expected
  set via fns above, len + `name==path` (no alias) + hex + no-dup + set equality +
  `_verify_tool_blob` at epoch per row (receipt) / sorted order (staged).
  R5: expected sets G67|G71|G76 (50/63/70 literal); epoch OWN, never live HEAD.
- `_require_known_schema_sha(schema_path, schema_sha, label):432-438` +
  `_KNOWN_SCHEMA_SHAS:410-429` + `OWNER_REGISTRY:380-400` +
  `_ALLOWED_SCHEMA_PATHS:402` + `_resolve_json_pointer:441-468` (`''`=whole doc,
  `'/'` forbidden) + `_validate_instance_against_schema_blob:471-...`.
  Origin: `schema_path` fixed repo-rel from record/registry; `schema_sha` hex from
  retained record. Current93: path in finite allowlist else `UNSUPPORTED`; sha in
  frozenset(old/new known) else `UNSUPPORTED` (no foreign even with registered path).
  R5: allowlist ADDS 5 DM022 paths with pinned shas (R4 proposal shas retained known;
  implementation shas pinned at code, old stay valid for history); registry ADDS DM022
  rows (request/manifest/proof/report/checkpoint + retention/guard/completion embedded
  pointers) with fixed file + pointer + validator; unknown still `UNSUPPORTED`.
  newCP reader uses same registry (no separate trust).
- `verify_versioned_history(repo_root, record_path):3864` /
  `verify_renewal_retention(root, basis_path):4200` + kind helpers
  `_is_legacy_record:1165` / `_is_editorial_record:1169` / `_is_renewal_record:1177` /
  `_record_kind:1197` + `_walk_chain_backwards:1222` + `_verify_editorial_ancestor:1966` +
  `_verify_versioned_ancestor:2808` (newCP reader).
  Origin: `record_path` retained record ref `{path,sha256}`; graph via bounded
  `_walk_chain_backwards` (CHAIN_LIMIT, no live State). Current93: kind dispatch
  LEGACY|EDITORIAL|VERSIONED via `reason_class+kind` (no caller inference).
  R5: ADD PREARCH branch (`kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` +
  `reason=REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` + `EVIDENCE->EVIDENCE` +
  `producer_boundary` + 3 roles + 4 NamedRef + SELF + sole `DM022_SUPERSESSION_PROOF`)
  admitted ONLY at G76 (creation window; current76 readback + future76 same-contract
  forward). G67/G71 epochs have no such kind (unknown=>`HISTORY_DIGEST_MISMATCH`,
  no auto-upgrade). Dispatch via new LOW `load_typed_checkpoint_record` for PREARCH
  files; legacy/editorial/renewal keep old `CHECKPOINT_SCHEMA` path. Retained
  before-State/COPY + `supersedes`/parent/anchor + SELF/proof verify at OWN epochs;
  never live-before equality; never `HEAD==historical checkpoint/toolEpoch`.

### Source current (bootstrap: 70/73 + G76 CURRENT tools)

- `_expected_closure_names(route):1403-1405` (returns `hist._expected_receipt_closure(route,"NEW")`).
  R5: `(route, family)`: G71=>NEW (63); G76=>70 (63+2+5); G67=>OLD (50) for historical
  receipt only. Origin: `route` only; family from derived OWN epoch (never caller flag).
- `verify_renewal_source_proof(root, basis_path, proof_path):1408-...` (Layer-B detached,
  NO State, every readback incl after activation). R5 at G76: recompute CURRENT closure
  70/73 member-wise (actual imports/contract + current committed source, not length) +
  contract_identity vs supported + schemas vs current disk + supported==observed +
  HIST verdict (owner epoch-bound old refs, E live/COPY). Historical G67/G71 proofs stay
  OWN-epoch. Never calls agent/State/Reader/Gate/Candidate/seal/P1/P2R/P3S.
- `_verify_current_tools_committed(repo, basis, dep, cfg_cur):246-...` +
  `_control_paths_for_current(repo, cfg):227-243` (DEFAULT_CONFIG +
  `implementation_control_roots` + contract_files values + style, sorted unique, lexical).
  Current93: epoch valid + ancestor-of-HEAD (NO blind HEAD==epoch); control diff
  epoch->HEAD quiet (artifact-only may move HEAD); rows live==committed at BOTH
  epoch+HEAD mode `100644`; wrong-root refusal; `BASIS_CURRENT_TOOL_DRIFT` fail-closed.
  R5 at G76: epoch=G76 commit, HEAD descendant required, control diff quiet per R4 head
  rule, rows live==committed at BOTH for 70/73/36/41; dirty/staged/untracked control
  refusals unchanged. `_control_paths` unchanged (lexical); G76 5 schema paths arrive
  via config-registered contract_files (not hardcoded).

### HIGH current tool epoch (no logic change; pins expand via families)

- `_current_commit(repo):460-465` (per-call `rev-parse HEAD`, no cache).
- `_observe_renewal_entry(root, state_path):619-...` (LIVE canonical State + config
  strict no-follow pinned bytes, `agent.STATE_SCHEMA`, Profile-derived canonical State
  path, prePreview/Exception window, PUBLIC `agent.validate_agent_state` on same LIVE
  bytes, recheck pinned bytes; INFO pins only, never `production.verify_state_basis`;
  NEVER checkpoint resolvers/screening/evidence State branches/Reader/Gate/Candidate/
  seal/P1/P2R/P3S).
- `_recheck_entry_pins(repo, entry, phase):808-819` (zero-delta State/cfg/Profile pins).
- `_derive_old_tool_epoch(repo, basis):2066-...` (history-graph `staged_producer_head|
  receipt_epoch|basis_current_epoch`, never caller; fallback prior seal receipt).
- `_require_renewal_entry_window(state):560-...` (VALIDATED_DRAFT+approved; ineligible
  at EVIDENCE_REVIEWED).
  R5: window/eligibility UNCHANGED (DM022 creation stays ineligible via renewal entry;
  DM022 uses HIGH `prearchitecture_acceptance`, not renewal prepare). At G76 same
  zero-delta + ancestor rules operate on G76 pins/controls. Future76-only: HIGH DM022
  modules own DM022 adoption (not renewal HIGH).

### Canonical + P3S/editorial closures (bootstrap: accept 36/41 + 70/73 as current G76)

- Weekly `current_closure(root):683` (29 literal) + `_verify_head_bytes:687` +
  `verify_closure_at_commit:809` + `build_receipt:744` + `_inspect_receipt_envelope:779` +
  `validate_receipt:836`; Longform `current_closure:535` (34) + `verify_tool_basis:539` +
  `verify_closure_at_commit:605` + `build_receipt:626` + `_inspect_receipt_envelope:661` +
  `validate_receipt:685`; P3S/editorial = staged code deps (50/63) + receipt closures.
  R5: G71 canon 29/34 retained (historical + current pre-DM022). G76 canon 36/41
  (=29/34+2+5 literal) as CURRENT while G76 active; historical receipts stay OWN-epoch.
  Staged 70/union73 as CURRENT G76 (member-wise, actual imports/contract + current
  committed source). No length-only check.

### LOW typed checkpoint vs normal (17 + 8 reconciliation)

ALL 17 sites migrate to shared `LOW.load_typed_checkpoint_record(repo_root,path)->
{family:LEGACY|PREARCH, record}` (strict duplicate-key parse; kind absent=>old schema;
kind==PREARCH...=>new DM022 schema; else refuse): agent `42,489,819,1011,1532,1758,
1774,1971,2397`; pubset `56,1213,1627,1981`; `editorial_correction:557`;
`release:121`; `stage_validation:288`; `weekly_refresh:931`.
Branches: `:348` MUST NOT be called for PREARCH (branch before lookup; producer NONE);
`:365` bypass `CORE_STAGE_CONTRACT` ONLY inside PREARCH (replace with
`DM022_SUPERSESSION_PROOF`+SELF+artifact re-hash); `:481` ADD PREARCH branch;
`:761` ADD PREARCH dispatch; `:902` KEEP legacy + ADD R4 resolver;
`:1608` exempt canonical ONLY inside PREARCH; `:1703` UNTOUCHED (new PREARCH builder
separate); `:1768` REFUSE PREARCH (HIGH single-file switch only).
What calls new LOW: P1/P2R/P2V/P3S/source/H/Freeze + publication hist graph + renewal
walkers for PREARCH files (retained refs + OWN-epoch graph, no live State).
What must NOT: history walkers MUST NOT call `agent.validate_agent_state`
(OWN-epoch git-show only); agent validator MUST NOT call operational guard (calls
detached proof only); LOW MUST NOT call agent/HIGH/public State validation;
advance/build MUST NOT install PREARCH via forward stage.

## 3. Timing (exact)

- Historical: LOW historical checkpoint/report validation verifies OWN recorded
  tools/schema lineage (epoch config blob mode `100644` + pipeline exact +
  versions/quality/profiles + Contract8 NUL aggregate + schema fingerprints +
  module/mode/membership) via retained bytes/git-show, never live HEAD.
- Current: active current producer validates content NOW under current code (fresh
  content validators + live re-hash + current Contract8/closure/schema checks);
  does NOT require old acceptance-report commit == new publicationToolHEAD
  (otherwise future G76→G76 renewal would brick); full current publication proof
  still fresh current tools.
- Readback: new PREARCH CP later State readback retains role3 sameRecord support
  (triplet same-record + lineage + retained COPY, no live-before equality, no
  window/HEAD re-check).

Stage/basis OLD `.contract` at its recorded implementation epoch separate
`producer_head` vs renderer commit (old evidence NOT at tool commit; CURRENT 76
proof uses new 76 everywhere).

## 4. Admission + scope (explicit)

Operation admission recomputes ALL current proofs (U) or checks (C) as normal with
truthful Core reason, same prePreview window; HIST family classification alone
confers NO operation permission. G67 adapter composes G71→G76 delta only under
exact conditions above; NO arbitrary migration beyond G76. Config/Profile/review/
recipe/accepted-input semantic delta outside allowed path (2 modules + 5 schemas +
17 sites + 8 branches + pipeline 71→76 registration) + known schema-family
fingerprint must refuse. Bootstrap existing-file scope: history/source/closure
verifiers gain G76 exact-set branches + registry 5-path additions + loader dispatch
(old-shape-preserving, SAME authority). Future76-only new: LOW/HIGH DM022 modules +
5 schemas + PREARCH branches + guard/completion/retention (only at G76 window/when
PREARCH present). No 7-file presence-only. No forcing old record into G76.

Required witnesses (precode oracles only, no execution): G71 current versioned
publication → G76 mechanical renewal with UNMODIFIED upstream as bootstrap compat
negative counterexample (no actual upstream adoption there); G76 DM022 accepted CP
→ initial publication → later editorial/renewal under G76 + history readback G67/G71.

## 5. Residual + stop

R4-C1 closed by per-function branches above (no generic deferral; no invented fns;
all names/lines source-grounded; R4 literal lists kept in JSON). No MAP-COMPLETE/
PASS, no implementation authorization. Root + independent review before code.
Per-invocation pins open. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
Stop internal; ordinary Commit/Push Human-owned. Decision hash `a345` unmodified.

### Preservation + citations

R4 + schemas preserved exact; R3/R2/reviews preserved. Source-grounded as cited
inline (history `:81-260/432-468/1165-1204/1222/1263-1301/1304-1411/1414-.../1966/
2808/3864/4200`; source `:227-283/407/533/933/1379/1403-1408`; renewal
`:460/560/619/808/1068/2066/3247`; weekly `:28-58/585/683/744/836`;
longform `:52-87/535/626/685/1020/1157/1198`; agent `:42/348/365/481/761/902/1608/
1703/1768`; pubset `:56/1213/1627/1981`; editorial `:557`; release `:121`;
stage_validation `:288`; weekly_refresh `:931`).

(End of file)
