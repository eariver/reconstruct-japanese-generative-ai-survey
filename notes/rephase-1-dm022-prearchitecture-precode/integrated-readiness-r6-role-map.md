# DM022 — R6 role map delta (AUTHOR, PRE-CODE ONLY, fixes R5-PUB-1)

2026-10-28 AUTHOR delta. PRE-CODE ONLY. Human `ab84b4f` assumed.
No source/runtime/import/tests/build/fixture/restore/network/Git writes.
Actual93 proof-copy READONLY. No candidate/reconstruct Commit/Push.
Preserves EXACT: R5 `integrated-readiness-r5-family-map.md/json`,
R4 `integrated-readiness-r4.md/json` + `schema-proposals-r4/*.schema.json` (5 files),
all R3/R2/reviews, `independent-readiness-review.md` §§0–7 (NOT_READY, R5-PUB-1),
`astra-precode-gate-resolution.md` 37 lines (mandatory, §3 binding).
This file + `integrated-readiness-r6-role-map.json` are the ONLY writes of this unit.
No schema changes (no exact schema error). No MAP-COMPLETE/PASS.

Binds: decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B
(unmodified); root §5 + gate resolution §§1–4 (precedence/boundary/admission, §3
research-vs-publication correction). All `file:line` below proof-copy
(`409b292`/tree `8ce36998` +93/742) unless `workspace:`. Method: `Read`/`Grep`/`ast`
as DATA. No `scripts.*` imports.

R5 §2 “ADD PREARCH branch” as written is overbroad (R5-PUB-1). This R6 narrows it
to upstream-only and gives the concrete per-site role table replacing R5 JSON
`per_function_branches[7]`. R5 literal G67/G71/G76 lists kept in R5 JSON (not
repeated here beyond counts).

## 1. Role boundary (binding)

New PREARCH (`kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`,
`reason=REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`, `operation` EVIDENCE→EVIDENCE,
`producer_boundary` CANDIDATES→EVIDENCE, roles evidence/materiality/completeness,
4 `NamedRef`, SELF + sole `DM022_SUPERSESSION_PROOF`) is an accepted UPSTREAM
RESEARCH node only (evidence/materiality/completeness roles of the G76 accepted
graph at the §3 `EVIDENCE_REVIEWED` window). It is NEVER:
publication `_record_kind`, activation predicate, State
`publication_revalidation_provenance` selector value, or publication `supersedes`
chain link. A PREARCH record supplied as activation/validation checkpoint, or as
validation/freeze/release (or unrelated selection) checkpoint, must refuse as
wrong family (`HISTORY_DIGEST_MISMATCH` / `DM022_WRONG_FAMILY`, entry + seam none
+ writes none) even though it parses as a valid Stage Checkpoint.

Research vs publication `supersedes` remain separate predecessor/anchor chains
(research: `parent_checkpoint`/`original_anchor`/`supersedes[]` in PREARCH record;
publication: `supersedes {path,sha256}` in revalidation/activation records +
`_walk_chain_backwards` newest→oldest). Neither chain inherits authority from a
label in the other.

Future normal forward artifacts CONTAINING a reference to accepted PREARCH vs
PRETENDING to be selection/validation: after adoption, normal forward
Selection/Architecture/Draft/validation checkpoints MAY contain references to the
accepted PREARCH graph as prior research (e.g. `basis.*_sha256` recomputed from
R4 Matrix/Selection/Architecture bytes built on new research; `prior_checkpoint`
or lineage notes pointing at retained before-State/COPY + `supersedes`/parent/
anchor for provenance). Their OWN record keeps a normal forward kind
(`from_state != to_state` per `stage_plan`, e.g. `EVIDENCE_REVIEWED→SELECTION_COMPLETE`,
plus `CORE_STAGE_CONTRACT` review, NOT `kind=PREARCH...`). A record whose OWN
`kind/from→to/producer` claims PREARCH while sitting at a selection/validation/
freeze/release path is pretending and must refuse. Containing a hash pointer to
prior accepted research is allowed; being the wrong kind at the wrong stage is not.

## 2. Generic decoder vs authoritative checks (no caller flag, no malicious inference)

- New LOW decoder `load_typed_checkpoint_record(repo_root, path)->{family, record}`
  does GENERIC parse only: strict duplicate-key parse → `kind` absent ⇒ validate
  old `stage-checkpoint-v2.schema.json`; `kind==PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`
  ⇒ validate new DM022 schema; else refuse. No `.get(kind,legacy)` fallback, no raw
  mutation, no role/producer decision, no State/guard/HEAD read. Same for
  `_resolve_research_from_state_bytes` structural shape (`{path,sha256}` shape,
  same-record equality, path safety, kind dispatch) — no file-content validation
  beyond shape, no `agent.validate`, no `verify_state_basis`.
- Authoritative expected-role/producer checks are supplied by the CALLER (expected
  `checkpoint`/`artifact_name`/`from→to` params origin: State provenance key,
  `stage_plan` entry, `REQUIRED_CURRENT` map, function argument) OR by the shared
  semantic validator (`_producer_for_checkpoint:348` for legacy forward producer
  lookup; PREARCH branch in `_validate_checkpoint_record:481`/
  `_resolve_checkpoint_artifact:761` checking `operation`/`producer_boundary`/
  `checkpoints`/`artifacts` + same-record triplet + lineage + SELF/proof digest).
  Generic parse valid ≠ permission: parsing a valid PREARCH never authorizes
  standing in for `validation`/`freeze`/`release`. No public caller-verified flag
  (every ref reloaded via file/path + `lstat`+read+hash + live re-hash + schema;
  caller dicts never trusted). No role inferred from malicious record (`kind`/
  `reason` alone insufficient; must match caller-expected role + producer boundary
  + same-record triplet + lineage + G76 window, else refuse wrong family).
- Constant declarations vs runtime loaders: `agent:42` / `pubset:56`
  `CHECKPOINT_SCHEMA = Path("schemas/stage-checkpoint-v2.schema.json")` (plus
  `REVALIDATION_SCHEMA`, `STATE_SCHEMA`, `DEFAULT_CONFIG` consts) are Path
  declarations only — no data path invented. Migration adds the new DM022 schema
  file constant in LOW (new file, old const byte-identical) and migrates the 17
  call sites below to the shared LOW loader; no edit to old const value.

## 3. 17-row per-site expected role/producer map (replaces R5 branches[7])

`decoder` = shared LOW generic parse; `authority` = caller expected role and/or
shared semantic validator. `admit` = PREARCH accepted ONLY if stated expected
roles + boundary + G76; else `refuse`. Full rows in JSON (`sites_17`); summary:

| # | Site | Args/origin | Expected role / producer | PREARCH |
|---|---|---|---|---|
| 1 | `agent:42` const | declaration only | n/a (Path const) | n/a (add LOW DM022 const, old unchanged) |
| 2 | `agent:489` `_validate_checkpoint_record` load | `repo_root, authority{path,sha256}` from State `checkpoint_provenance[checkpoint]`; `checkpoint` param origin = caller provenance key | caller `checkpoint` + `from→to` via `_producer_for_checkpoint:348` (legacy) / PREARCH branch (`EVIDENCE→EVIDENCE` + boundary + 3 roles + 4 refs + SELF) | ADMIT only if expected `checkpoint ∈ {evidence,materiality,completeness}` + boundary at G76; else REFUSE (incl `validation`/`freeze`/`release`/selection) |
| 3 | `agent:819` `_resolve_checkpoint_artifact` load | `repo_root,cfg,state,checkpoint,artifact_name`; origin = `resolve_active_evidence_views:902` (evidence + 2 names), screening:467, etc. | caller `checkpoint`+`artifact_name`; legacy producer lookup; PREARCH needs same 3 roles + 4-name set + SELF/proof | ADMIT only upstream 3 roles + 4 names at G76; else REFUSE; `validation`-projection `868-891` untouched (publication-7 only) |
| 4 | `agent:1011` pending validation load | `checkpoint_path` (pending validation record) | expected `validation` (pending publication validation) | REFUSE PREARCH (wrong family) even if parses |
| 5 | `agent:1532` revalidation prior load | `prior_ref{path,sha256}` from retained history graph | expected prior publication revalidation (LEGACY\|EDITORIAL\|VERSIONED) | REFUSE PREARCH |
| 6 | `agent:1758` builder `validate_instance` | `payload` (forward `from→next` record) | expected forward `record.from==current && record.to==next` | REFUSE PREARCH (EVIDENCE→EVIDENCE matches no `stage_plan` producer; new PREARCH builder separate) |
| 7 | `agent:1774` advance `load_and_validate` | `checkpoint_path` (forward transition record) | expected forward `from==current && to==next && set==stage.checkpoints` | REFUSE PREARCH (producer NONE; HIGH single-file switch only) |
| 8 | `agent:1971` revalidation basis load | `authority{path,sha256}` (revalidation basis checkpoint) | expected publication revalidation basis | REFUSE PREARCH |
| 9 | `agent:2397` revalidation prior load | `validation_ref{path,sha256}` (prior Stage Checkpoint) | expected publication revalidation prior | REFUSE PREARCH |
| 10 | `pubset:56` const | declaration only | n/a | n/a (same as #1) |
| 11 | `pubset:1213` anchor prior load | `validation_ref{path,sha256}` (derive anchor prior) | expected anchor prior publication revalidation | REFUSE PREARCH |
| 12 | `pubset:1627` before-digest prior load | `prior_ref{path,sha256}` (before-digest prior) | expected 7 publication roles (`PUBLICATION_ROLES_7`) cumulative | REFUSE PREARCH (research roles never rebind: `1308-1312/1875-1878`) |
| 13 | `pubset:1981` selection prior load | `validation_ref{path,sha256}` (selection prior) + contract canonical7 check | expected `candidate-matrix/candidate-selection` + contract canonical paths | REFUSE PREARCH (unrelated selection checkpoint must refuse) |
| 14 | `editorial_correction:557` record load | `record_path` via `agent.CHECKPOINT_SCHEMA` (downstream selection/architecture/draft nodes `1502-1542`) | expected downstream selection/architecture/draft (NOT upstream research) | REFUSE PREARCH; upstream PREARCH nodes resolved separately via LOW R4 + same wrapper |
| 15 | `release:121` validate_instance | `payload` (Release Stage Checkpoint) | expected `FROZEN→RELEASED` + freeze/manifest/record artifacts | REFUSE PREARCH |
| 16 | `stage_validation:288` prior load | `path` (prior Stage Checkpoint; expected from `REQUIRED_CURRENT`/prior map) | caller-expected checkpoint: ADMIT only if ∈ upstream 3 roles at G76; else REFUSE | conditional (generic needs caller expected role) |
| 17 | `weekly_refresh:931` refresh load | `checkpoint_path` (refresh validation checkpoint) | expected `validation` (refresh validation) | REFUSE PREARCH |

Oracle per row in JSON: admit ⇒ live re-hash + same-record + lineage + G76 window
verified, proceed; refuse ⇒ `entry + seam none + writes none`,
error `DM022_WRONG_FAMILY for <expected role>` (or `HISTORY_DIGEST_MISMATCH` on
historian chain). Late forward `no live-before equality / no window re-check /
no HEAD equality with revision HEAD` applies ONLY to admitted upstream readback
rows, never to refused publication rows.

## 4. Publication discriminators / chain walkers / selectors (what calls new LOW, what must NOT)

Discriminators (pure, no data path invented — record dict only, no file read):
`pubset:362` `_is_renewal_record` (exact `kind=VERSIONED_RENEWAL_ACTIVATION_V1` +
`reason_class=REVIEWED_VERSIONED_CORE_RENEWAL`, renewal-only), `:377`
`_is_versioned_record` (editorial\|renewal two-branch), `:393` `_is_versioned_seal`
(set only); `agent:85` `_is_renewal_record`, `:99` `_is_versioned_record`, `:115`
`_is_versioned_seal` (same, publication activation family). MUST NOT gain PREARCH:
PREARCH dict returns False on all three (not renewal/editorial/legacy); callers
requiring versioned/legacy must then refuse wrong family (no auto-upgrade, no
caller kind inference, no editorial fallback). `_is_legacy_record`
(pubset `:357` / agent `:76` / history `:1165`: `reason_class==LEGACY_REASON` + no
`kind`) likewise False for PREARCH (has `kind`). No file IO added here.

Revalidation chain walkers (publication `supersedes` chain ONLY, never research
lineage): history `_walk_chain_backwards:1222` (structural load + schema + cycle/
depth bound, `{path,sha256}` links), `_verify_editorial_ancestor:1966`,
`_verify_versioned_ancestor:2808` (+ `_record_kind:1197` dispatch LEGACY|EDITORIAL|
VERSIONED; unknown incl PREARCH ⇒ `HISTORY_DIGEST_MISMATCH`, no inference);
pubset `_walk_chain_backwards:1120` + `nxt=record.get("supersedes"):1141`,
`_check_*` canonical-anchor legacy rows `:1308` (`key[0] not in PUBLICATION_ROLES_7`
⇒ refuse “research roles never rebind”), activation `supersedes:1437-1441`
(`{path,sha256}` + `_check_authority_ref`), KEEP/profile `:1583`, before-digest
`:1646` (`_is_legacy` vs `_is_versioned` branches; PREARCH hits neither ⇒ refuse),
selection-anchor legacy `:1874` (same non-publication-role refuse + cumulative
`prior_sha256` vs original). MUST NOT call new LOW research decoder for chain
membership; MUST NOT call `agent.validate_agent_state`; unknown kind in chain ⇒
refuse (no PREARCH admission). Detached research-history validation for upstream
PREARCH nodes (retained refs + OWN-epoch graph via LOW + retained COPY, no live
State, no `agent.validate`, no HIGH) stays a SEPARATE path called by publication
hist/source walkers when they encounter that upstream node (`load_renewal_accepted_authority:933`
evidence/ledger/completeness nodes; `verify_renewal_retention` retention graph;
P1/P2R/P2V/P3S/source/H/Freeze retained upstream refs) — each chain keeps own
predecessor/anchor checks with no cross-chain inheritance.

Selectors / activation predicates (State `publication_revalidation_provenance`
`{path,sha256}` or None; NO fallback, NO safe default):
pubset `resolve_publication_selection:1992` (pointer None ⇒ CANONICAL anchor
`VALIDATION_CHECKPOINT`; else load + `_is_versioned` branch),
`resolve_publication_artifact_path:2151` (role ∈ `PUBLICATION_ROLES_7` +
`publication-candidate` else `unknown publication role`; PREARCH roles
evidence/materiality/completeness NOT in allowed ⇒ refuse before any read),
`_default_candidate_rel:2215` (None ⇒ canonical token path WITHOUT validation
record; invalid dict incl `{}` fail-closed via central selection),
`resolve_publication_mode:2253` (`_is_versioned_record` ⇒ VERSIONED_ACTIVE else
CANONICAL — R6 fix: explicit PREARCH test BEFORE versioned test; PREARCH ⇒ refuse
wrong family, never default to CANONICAL), `require_active_or_canonical:2267`
(strict branch guard); agent `1066` (pending predecessor equality),
`1091` (pending basis predecessor bind), `1274` (head `publication_revalidation`
branch dispatch: editorial|versioned|legacy else `head branch unknown` — PREARCH
hits else-branch ⇒ refuse, no new arm), `1483` (`_resolve_publication_revalidation`:
None ⇒ (None,[]); else load + issue + `_is_editorial|_is_renewal|_is_legacy` else
refuse), `2509` (Reader-Surface Gate predecessor `supersedes` bind).
All MUST refuse PREARCH even if pointer bytes parse (wrong family, not
CANONICAL fallback). Generic `resolve_raw_path`/`sha256_repo_file` file reads
stay AFTER role/family gate, never before.

## 5. Residual + stop

R5-PUB-1 closed by §§1–4 + JSON (`sites_17` + `discriminators` + `chain_walkers` +
`selectors` + `forward_artifact` rule; replaces R5 JSON `per_function_branches[7]`
narrowing). No other mandatory gaps. No MAP-COMPLETE/PASS, no implementation
authorization. Root + independent review before code. Per-invocation pins open.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved.
Stop internal; ordinary Commit/Push Human-owned. Decision hash `a345` unmodified;
R5/R4/schemas unmodified.

### Preservation + citations

R5/R4/schemas preserved exact; R1/R2/reviews preserved. Source-grounded as cited
inline (pubset `:56/362/377/393/1120/1141/1308/1437/1583/1646/1874/1992/2151/2215/
2253/2267`, `1213/1627/1981`; agent `:42/85/99/115/489/819/1011/1532/1758/1774/1971/
2397/1066/1091/1274/1483/2509`; history `:1165/1169/1177/1197/1222/1966/2808`;
editorial `:557`; release `:121`; stage_validation `:288`; weekly_refresh `:931`).

(End of file)
