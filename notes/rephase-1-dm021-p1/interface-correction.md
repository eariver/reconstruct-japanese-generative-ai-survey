# DM021-P1 interface correction (actual-source ground)

Source paths below are the accepted restored copy
`/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(HEAD409, 2M7A). Supersedes the proposal's E5 review-type language and its
"first row wins" rule; everything else in `interface-proposal.md` stands unless
contradicted here.

## 1. Actual review loaders (pre-TeX vs later are different records)

Pre-TeX scope carrier is ONLY the existing pre-TeX schema via
`surface_gate.load_and_validate_reader_surface_semantic_review(repo_root,
review_path, *, expected_issue_id, expected_publication_profile,
expected_surface_path, expected_surface_sha256, require_pass=True)`
(`survey_reader_surface_gate_v2.py:958-967`). It enforces: repo-local regular
file; strict `reader-surface-semantic-review-v2` schema (legacy fallback
prohibited); `review_kind==SEMANTIC_EDITORIAL`; `review_sha256` recompute over
all other fields; reviewed-surface disk re-verify; required
`READER_PIPELINE_INDEPENDENCE` PASS with substantive detail/evidence; PASS
semantics (all checks PASS, status PASSED, 0 unresolved blocking); issue/profile
identity; reviewer + timestamp presence (`:968-1103`). Its return (`:1105-1119`)
is `{status, decision, reviewed_by, surface_path, surface_sha256, recorded_at,
reviewed_at, review_path, review_sha256, checks, findings,
unresolved_blocking_count, summary}` — unknown extra keys (the scope block) are
NOT retained. P1 therefore: (a) call the loader with the expected
before/after bindings (disk re-verified at call time); (b) separately capture
raw review FILE bytes — `sha256_file` at entry, `core.load_json` of the same
bytes, re-hash after parse, abort on any drift so a second read cannot silently
switch records; (c) read + validate `editorial_correction_scope` from that raw
dict against the new schema fragment. Later/post-PDF
`reader.validate_review_record(repo_root, path, *, issue_id, expected_kind)`
(`survey_reader_publication_v2.py:544`) validates the DIFFERENT
publication-review record (`reader_manuscript/source/pdf/page_count` with
manuscript/source/PDF ref binding, `:560-623`) — never a P1 scope carrier.

## 2. Graph wire: union roles, contradiction stops, fixed families

Node key: normalized repo-relative posix path. Node:
`{path, sha256, byte_count, roles:[sorted union], policy}`. Edge:
`{from_path, edge_type, to_path, to_sha256}`, sorted by tuple. One node per
physical path; logical roles UNION — never first-wins role loss. Contradictions
STOP with names: same path + different sha/size (`HASH_CONFLICT`); KEEP vs COPY
on one path (`POLICY_CONFLICT`); duplicate role in checkpoint rows (existing
`:729-732`); changed path outside allowed roles (`:740`); unknown executable
input; unresolvable required ref. Fixed `edge_type` families: `CHECKPOINT_ROW`
(original 7), `MANUSCRIPT_SUPPORT` (primary/BIBLIOGRAPHY/STYLE),
`GATE_BINDING` (manuscript/reviewed-input/receipt), `RECEIPT_CLOSURE`
(accepted-refs/archive/outputs/tools), `QUALITY_OUTPUT`, `REVIEW_TARGET`
(pre-TeX `reviewed_surface` OR later manuscript-source-pdf triple),
`PREDECESSOR_CHAIN`, `UPSTREAM_AUTHORITY`, `CANDIDATE_OBSERVED` (optional).
Original-7 rows are checkpoint metadata (expected history), resolved to live
nodes for comparison display only. Active-before nodes bind effective current
bytes: revalidation-superseded rows where a valid predecessor resolves, else
re-verified original bytes. Historical generation-State SHAs are displayed
provenance, never live State equality checks. Required local refs: every
`{path,sha256}` via `repo_local` + hash pin. Provenance-only (never followed):
URLs, reviewer names, `review_reference`, executor strings, external keys.
Optional Candidate: observed/unadopted, exact agreement with active-before
publication via the candidate validator or stop; quality result files enter via
quality-bundle rows only.

## 3. Frozen digest membership

`preserved_upstream_digest = sha256_object` over sorted upstream-authority nodes:
approved issue-architecture file, Draft authored archive, accepted draft
packages/results, synthesis input/result, evidence-acceptance, candidate-matrix,
materiality-ledger, Profile file — plus `before_graph_digest` (sorted role rows
`{role,path,sha256,bytes}` + sorted edge tuples) and the canonical before-reader
digest. Transitive deps only through known record types (manuscript
`supporting_files`, receipt `accepted_refs`/`outputs`, review refs). EXCLUDED:
live State bytes, revalidation record bytes, renderer commit/tool metadata beyond
the contract pin, QA/runner metadata, old mutable publication outputs,
timestamps, reviewer identities. `live=False` chain success never claims old
bytes retained.

## 4. Eligibility vs receipt epoch vs within-call snapshot

Three separate layers. Eligibility: healthy VALIDATED_DRAFT + arch approved +
preview pending/no-provenance + downstream pending + exception inactive
(`_pending_conditions:696-708`). Receipt epoch: FULL `validate_receipt`
(Weekly `:726-773`; Longform `:665+`) = head-bytes/tool-basis predicates AND
`tools.contract == core.contract_identity(...)` AND accepted-refs/archive
equality AND deterministic output replay — never just `verify_tool_basis`.
`_verify_pending_binding` is NOT a P1 callee. Across publication→proposal, an
artifact-only HEAD descendant is allowed iff full receipt predicates plus the
entire before-graph re-verify pass at proposal time. Within one inspection,
entry-captured State bytes/HEAD/config/dependency SHAs must remain stable;
mid-call change stops. Receipt commit need not equal HEAD (ancestor +
control-equality suffices). No pending-basis construction, ever.

## 5. Canonical comparison via independent rederivation

Proposed FILE bytes must equal `canonical_reader_bytes(INDEPENDENTLY rederived
proposed surface)` — rederivation runs the real route loader on the supplied
authoring input, never re-serializes the supplied file. Before side likewise:
`NO_EDITORIAL_CHANGE` iff canonical independently-derived-before ==
canonical independently-derived-proposed. A mere wire-format/key-order gap is
not an editorial change. Noncanonical before input (on-disk file ≠ its own
canonical form) is an explicit refusal, not a silent pass. Existing callers'
canonical paths are not weakened to force this.

## 6. Exact proposal keys and scope outcomes

`proposal.json` (strict, `additionalProperties:false` throughout): top
`{schema_version: EDITORIAL_CORRECTION_PROPOSAL_V1, proposal_id, issue_id,
research_profile, publication_profile, route: EDITORIAL_CORRECTION_PROPOSAL_V1,
status: PROPOSED}`; `basis: {state_ref, validation_checkpoint_ref,
active_revalidation_ref|null, active_reader_input_ref, before_graph_digest,
preserved_upstream_digest, generated_receipt_ref, renderer_commit,
contract_identity}` (refs are `{path,sha256}`); `proposed:
{authoring_input_ref, proposed_reader_ref, proposed_reader_canonical_sha256,
change_description}` (nonempty); `retention_plan: [{role, path, sha256, bytes,
policy, retained_ref|retained_dest}]`; NO after/review/PASS/receipt/Gate/
Candidate refs. `validate_proposal` outcomes: scope arg absent → `REVIEW_REQUIRED`
(`NoScope`); supplied ordinary PASS without block → `REVIEW_REQUIRED`
(`OrdinaryWithoutScope`; record stays ordinarily valid, never correction
approval); malformed/wrong-before/wrong-after/stale-upstream/REJECT/
REQUIRES_OWNER_DECISION → typed `INVALID_SCOPE` refusal, never bound
(`InvalidScope`). Zero writes; no PASS generation; no report-as-PASS.
Token/layout accepted: `^[a-z0-9][a-z0-9-]{0,63}$`, repo-local, no
alias/traversal, proposal dir must not collide with live canonical paths or
existing dirs, retained dests finitely derived under `retained/before/`.

## 7. Real predecessor fixture (no handcrafted pointer)

Preferred positive: post-install fixture + real Weekly R1 same-byte refresh
path (b74 pattern: same-edition writer, unchanged reader/output/criteria,
post-install receipts) yielding a genuine `REVIEWED_CORE_CHANGE` revalidation
record over a reviewed Weekly-derivation-only commit — process-scoped identity,
independent DB, real commits, no empty commits. Oracle displays original-7 rows
vs effective active rows (changed vs kept). No handcrafted pointer, no fake
reason. If unconstructible: STOP with the exact gap; forged-pointer negatives
alone cannot replace the positive. Longform primary + Weekly envelope positive
+ Weekly body/upstream negatives remain required.

## 8. First-implementation decision table (Astra)

| # | Decision | Recommended | Alt if blocked |
|---|---|---|---|
| D1 | Review/scope read path (§1) | Loader + raw capture/recheck | STOP (no custom parser) |
| D2 | Graph wire/digest (§2-3) | Fixed families, union roles, contradiction-stop, §3 membership | STOP on membership gap |
| D3 | Epoch layering (§4) | Eligibility ≠ receipt ≠ snapshot; no pending construction | STOP, no bypass |
| D4 | Canonical rule (§5) | Independent rederivation both sides; noncanonical refusal | STOP, no caller change |
| D5 | Proposal keys/outcomes (§6) | Exact §6 keys + NoScope/Ordinary/Invalid matrix | STOP on schema gap |
| D6 | Predecessor (§7) | Real R1 refresh + derivation-only commit | STOP with exact gap |
| D7 | Phase B release | 3A+1M under §5-callee list of proposal (amended by §1 loader) | Narrow on proven loader gap |
