# DM021-P1 Phase A — exact interface proposal (F14/F16)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(detached HEAD, no branch/commit). HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`,
available chain 409→…→e170→222→…→b40→774, status exactly 2M7A, all 9 SHA256/modes
match correction3 manifest. Runtime inspect-only: Python 3.14.4, git 2.53.0; no app
imports/tests, no installs. Reconstruct workspace untouched (only new
`notes/rephase-1-dm021-p1/` untracked). STOP for Astra before candidate code.

## 1. Finite before-graph: roles, edges, dedup, conflicts

Seven checkpoint roles (config `DRAFT_COMPLETE.artifacts` + Gate,
`survey_agent_control_v2.py:685-693`): `reader-manuscript`, `validated-source`,
`publication-pdf`, `quality-regression-bundle`, `semantic-review`, `visual-review`,
`reader-surface-gate`. Typed edges (no generic path-following resolver):
E1 manuscript→Profile/Architecture/approval/primary/BIBLIOGRAPHY/STYLE (Gate
requires `supporting_files` roles + canonical `main.tex`/`references.bib`/`jgaisurvey.sty`
paths, `survey_reader_surface_gate_v2.py` Longform/Weekly structured blocks);
E2 Gate→selected manuscript + reviewed reader input + pre-TeX review + generated
receipt (`validate_longform_reader_input`/`validate_reader_input`, receipt
`reviewed_reader_input`/`semantic_review` path+SHA equality);
E3 receipt→accepted refs + publication authoring archive + Draft archive +
reader/review/output refs + current tool/contract basis (`verify_tool_basis:519`,
`_verify_head_bytes:577`, `CURRENT_CLOSURE` rows);
E4 quality bundle→source/PDF/check-result files; E5 later reviews→exact
manuscript/source/PDF (`reviewed_surface{path,sha256}`, `review_sha256` self-digest
`gate:997-1008`); E6 original checkpoint + State-bound predecessor chain + upstream
authority (Profile/Architecture/Draft/Synthesis/Evidence refs).
Dedup: one physical path may carry many logical edges; retention destinations
dedupe by repo-relative path, first row wins only on byte equality.
Conflicts (all stop, never fallback): same path with two SHAs across roles;
duplicate checkpoint role names (`_collect_pending_rows:729-732`); changed path
outside allowed roles (`:740`); unknown executable input; unresolvable required ref.

## 2. Three identities; literals vs local refs

Original: `checkpoint_provenance.validation{path,sha256}` + its artifact rows,
verified by file hash + checkpoint schema + issue/from-DRAFT_COMPLETE/to-VALIDATED_DRAFT/
`checkpoints∋validation` identity (`:711-720`). Active-before: live State plus
optional `publication_revalidation_provenance` pointer resolved by
`_resolve_publication_revalidation:1090-1149` (issue match, reason class,
pre-decision establishment, `prior_checkpoint == active validation ref`, prior bytes
verified); pointer absent → original rows re-verified; referenced-invalid → stop.
Proposed-after: immutable `<source_root>/publication/v2/editorial-corrections/<proposal_id>/`
(`authoring-input.json`, `reader-surface-input-v2.json`, `proposal.json`, review record);
no State authority; FILE bytes must differ from active-before reader bytes or
`NO_EDITORIAL_CHANGE` refusal (never rerouted to R1).
Provenance literals (URLs, reviewer names, `review_reference`, external keys) are never
opened as paths. Every file input resolves via `core.repo_local_path`/`_safe`:
repo-local, no absolute/traversal/symlink, then SHA256-pinned.

## 3. Epoch predicate F14 (exact; no pending bypass, no new allowlist)

`SAME_EPOCH_AND_BASIS` holds iff ALL of: (a) receipt renderer commit is an ancestor
of HEAD (`merge-base --is-ancestor`); (b) `git diff --quiet commit..HEAD` clean over
control set `{DEFAULT_CONFIG} ∪ implementation_control_roots ∪ STYLE_PATH ∪ all
contract_files` (config `:87`); (c) `git diff --quiet HEAD` clean over the same set;
(d) no untracked control source (except `__pycache__`/`*.pyc`); (e) closure name-set
equals `CURRENT_CLOSURE` and each row SHA equals file bytes equals
`git show {commit}:{name}` equals `git show {head}:{name}`; (f) before-graph snapshot
recheck: State bytes, config bytes, HEAD, validation ref, changed/kept row snapshot,
predecessor pointer all equal (`_verify_pending_binding:748-772` pattern); (g) same-Core:
establishment lifecycle/architecture/preview/freeze/release pre-decision + valid
`recorded_at` instant. Longform uses `verify_tool_basis`, Weekly `_verify_head_bytes`.
P1 never constructs a pending basis (`built_checked_pending_publication_basis` and
`require_change` paths forbidden); pre-feature/mixed-epoch/code-contract-authority
drift stops. Harmless artifact-only commits pass (a)-(g); anything else is not
"artifact-only". Uncommitted control overlay refuses as implementation basis by (c)-(e).

## 4. Exact representations F16

Canonical reader bytes (both routes): `core.json_bytes` (`json.dumps(ensure_ascii=False,
indent=2)+"\n"`, `survey_production_v2.py:86`); Longform exposes it as
`derivation.canonical_reader_bytes` (`:949-951`, "digest is SHA256 of THESE bytes").
Digest rule: `sha256_bytes(canonical_bytes)` — never `sha256_object` for reader bytes.
Canonicality check: `path.read_bytes() == canonical_reader_bytes(loads(path))`.
Before-graph digest: `sha256_object({"roles": rows sorted by role, "edges": sorted edge
tuples})` where each row is `{role,path,sha256,bytes}`. Preserved-upstream digest:
`sha256_object` of sorted upstream-authority refs `{kind,path,sha256}` (accepted
Profile/Architecture/Draft/Synthesis/Evidence/archive refs, not live State bytes).
`proposal_id`: `^[a-z0-9][a-z0-9-]{0,63}$`. Retention rows `{role,path,sha256,bytes,
policy,retained_ref|retained_dest}`; policy ∈ {`KEEP_IMMUTABLE` (upstream/checkpoint/
prior records), `COPY_BEFORE_REPLACEMENT` (old mutable artifacts)}; destinations under
`<proposal_dir>/retained/before/<repo-relative path>`; plan validates only, writes nothing.
Operation snapshot (State/predecessor/code/retention) stays separate from the semantic
old-reader/new-reader/frozen-upstream relation; staleness fails the former, never
reinterprets the latter.

## 5. APIs (new narrow; existing callees)

`prepare_proposal(root, state_path, authoring_path, proposal_id)`: read-only; strict
State validation (`agent.validate_agent_state`, `_pending_conditions:696-708` must be
empty), resolve original + active-before (§2), real derivation (Longform
`load_derivation_for_readback`, NOT `load_derivation`'s DRAFT_COMPLETE-only gate;
Weekly `load_derivation(..., pending_basis=None)`), project + validate proposed reader,
enforce byte-difference; returns in-memory `{proposal, canonical_reader_bytes, binding
{before_graph, graph_digest, upstream_digest, refs}}` — never approval, never paths
created. `validate_proposal(root, state_path, proposal_path, scope_review_path=None)`:
re-derives everything from named FILE bytes, compares canonical proposed bytes and all
bindings/plan rows; returns `REVIEW_REQUIRED` (default / absent scope block) or
`REVIEW_BOUND_PROPOSAL` (scope block valid, §6) plus `input_hashes`; never Reader PASS,
Gate, or revalidation record. Existing callees only: `validate_agent_state`,
`resolve_active_publication_revalidation`, route loaders/projectors/validators,
`validate_receipt`, review loader (`reader.validate_review_record`), `core.json_bytes/
sha256_*`. No controller/revalidation-schema/publisher/receipt/Gate/stage/fidelity/
Freeze/Release writes; extra runtime path returns to Astra first.

## 6. Optional scope block (existing schema only)

Strict `editorial_correction_scope` object inside `reader-surface-semantic-review-v2.
schema.json` (additive; ordinary reviews unaffected): `{version: EDITORIAL_CORRECTION_
SCOPE_V1, decision ∈ {WITHIN_APPROVED_AUTHORITY, REQUIRES_OWNER_DECISION, REJECT},
before_reader_input{path,sha256}, preserved_upstream_sha256, change_summary≠∅,
evidence_locations≠∅}` plus a `checks[]` entry with `check_id: EDITORIAL_CORRECTION_
SCOPE`. `reviewed_surface{path,sha256}` is the AFTER artifact. `REVIEW_BOUND_PROPOSAL`
requires semantic `decision==PASS` AND scope `WITHIN_APPROVED_AUTHORITY` AND exact
before/after/upstream binding through the existing review loader AND `review_sha256`
self-digest match. Assessor is the existing ChatGPT reviewer; P1 checks shape/bindings,
never independence or semantic truth; no new Human gate/role.

## 7. Real-fixture strategy; refusal/no-write oracles (no success mocks)

Longform primary: LF2I-integration pattern (`test_survey_longform_publication_
integration_v2.py:112-178`): independent temp Git DB, process-scoped identity, inert
origin, real producers + `stage:reader-publication-validation` → healthy VALIDATED_DRAFT
(new synthetic issue); authored `longform_revision` prose delta inside approved DIDs,
`new_external_evidence=false`, exact one-row-per-package. Weekly subset: increment-B
pattern (`_chain/_complete_authorities/_advance`): healthy VALIDATED_DRAFT via real
`weekly.load_derivation`; authored envelope (cover/frontmatter/final_summary) positive +
headline/deck/block/authored-body mutations → archive-drift refusals (`:313-332`).
Predecessor: revalidation-`Fixture` pattern (real `revalidate_publication_surface`
record + State pointer) when constructible; otherwise predecessor-absent positive and
forged/invalid-pointer stops. Oracles: owned-tree/State/refs snapshots equal pre/post
(`_snapshot`/`_assert_no_write_except` pattern); `NO_EDITORIAL_CHANGE` on same bytes;
missing/extra/conflicting retention rows, aliases/traversal, stale State/config/HEAD/
predecessor, absent current dependency → refuse; absent scope → `REVIEW_REQUIRED`;
wrong-before/after, stale upstream, REJECT/NEEDS-Owner → never bound; ordinary pre-TeX
reviews stay compatible (additive schema). If healthy authority is unconstructible
without forgery/mutation/bypass, return the exact blocker — no pending exception.

## 8. Astra decision needed

(a) Confirm §1 edge set + §4 digest constructions as the 3A+1M contract baseline.
(b) Confirm proposal-id grammar and `editorial-corrections/<id>/` + `retained/before/`
layout. (c) Authorize Phase B read-only module/schema/test build under §5 callee list,
or redirect on any demonstrated loader gap. No blockers found in Phase A.
