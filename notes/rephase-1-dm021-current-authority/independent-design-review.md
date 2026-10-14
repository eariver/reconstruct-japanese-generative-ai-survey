# Independent design review — DM021 retained-aware current-authority (P2V) contract

2026-10-14. Fresh author-independent design reviewer, distinct from General
analysis author and Astra/root. DESIGN ONLY. Read actual source, no
code/schema/test/fixture/import/copy/restoration/network/DB/index/ref/commit
writes, no historical script/suite reruns, no subagents. Only NEW file written
is this review. No runtime proof, no canonical audit, no adoption authority.

## 0. Sources read / reviewed contract identity

- Task: `notes/rephase-1-dm021-current-authority/task.md` (Astra-authored,
  design-only, stop at Human Commit Point).
- Authoritative contract in full:
  `outputs/rephase-1-dm021-current-authority-contract-decision.md`,
  135 lines, full SHA256
  `2ea1d98f1b3658430342e4ec2a2cd9639327557ca6ae2d6d4ea0665708f5f8fd`.
- Packet: `notes/rephase-1-dm021-current-authority/README.md`,
  `analysis.md` (445-line initial General proposal, NOT selected),
  `source-binding.md` (229 lines), `astra-feedback.md` F1–F6,
  `correction.md` (222 lines, F1–F6 correction).
- Prior P2R: `outputs/rephase-1-dm021-p2r-assessment.md` §4 plus mandatory
  `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/astra-closeout-resolution.md`
  (late-plant post-removal qualification, 1818-line erratum, proof-logger
  narrowing) and `independent-final-resolution.md` §§1–10 (BOUNDED_PASS with §10
  qualifications). Fixed P1 contract `07e89990…`, P2R contract `194fd7de…`
  unchanged.
- Exact source (read-only):
  `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`,
  actual detached `409b292756dd1277b9dfae87679934c0d2ce251c` /
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` + 16-file overlay + 84 caches.
  This review re-observed HEAD via `rev-parse` (rc 0, matches), status count 100
  rows, `wc -l` P1 1830 / P2R 2080 / Longform 758 / Weekly 773, and readonly
  `sha256sum` P1 `5d2fde456d42d494acc93d3ce6cab51bcd3ee56178b62cdf9eb31554db03c346`
  / P2R `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2`
  (prefixes match `expected16-correction2c.json` / final reports). No imports,
  no execution, no Git mutations. Counts below are summary-scope observations,
  not a new raw evidence packet (see §11).

Contract supersedes incompatible initial recommendations where they differ.
Corrected `correction.md` is the controlling General position; `analysis.md`
enum/verified_set, `CURRENT_READINESS_*` names, proposal-time whole-tree claim,
and old-byte-only revalidation claim are withdrawn/superseded as noted below.

## 1. Actual P1/P2R/Longform/Weekly reads (candidate-relative)

P1 `scripts/survey_editorial_correction_proposal_v2.py` (1830 lines):

- `_retention_plan:1231–1288`: deterministic row/path/policy construction;
  `inputs=set(col.files)` at `:1238`; live-input overlap `:1269–1270` and
  namespace overlap `:1271–1274`; duplicate-dest `:1275–1277`;
  absent-required (incl. dangling alias) `:1278–1284`. Verified by read.
- `_pipeline:1291–1492`: returns `{proposal, proposed_canonical,
  before_canonical, graph, frozen, effective, …}` at `:1486–1492` — not
  `input_hashes`, not scope, not final receipt. Covers State/config/canonical
  `:1291–1321`, staged authoring `:1334–1338`, original/active `:1344–1349`,
  manuscript/Gate/receipt routing `:1351–1384`, derivation + `NO_EDITORIAL_CHANGE`
  `:1386–1391`, receipt/Gate/bundle/pre-TeX `:1393–1430`, graph/digests/retention
  `:1431–1438`, tree/reverify `:1439–1442`, proposal object `:1454–1485`.
- `_validated_state_profile_for_tree:1536–1569`: strict State/Profile/canonical-root
  authority before broad walk (C4). Verified.
- `_final_full_receipt_recheck:1572–1598`: actual full route `validate_receipt`
  (Longform vs Weekly), not contract-only, plus `col.reverify()`. Verified.
- `prepare_proposal:1601–1632`: authority `:1616`, tree `:1617–1618`, pipeline
  `:1619–1620`, schema `:1621–1622`, final receipt after schema `:1624`,
  reverify + final tree `:1626–1631`. Verified.
- `_validate_scope:1635–1695`: ordinary loader + digest binding, absent block →
  `RESULT_REQUIRED` at `:1668–1670`, `WITHIN_APPROVED_AUTHORITY` + exact
  before/after/upstream + substantive `EDITORIAL_CORRECTION_SCOPE` PASS
  `:1671–1695`. Verified.
- `validate_proposal:1698–1830`: pins config/proposal `:1710–1723`, strict
  authority before canonical dir/tree `:1728`, canonical dir compare `:1729–1741`,
  layout/staged `:1743–1753`, description/path prechecks `:1756–1769`, broad walk
  only after `:1770–1771`, pipeline `:1774–1775`, ALL-field comparisons
  `:1778–1801` (header/basis/authoring/reader-ref/canonical-digest/description/
  ref-digest/retention/staged-bytes), State/Profile reload `:1802–1808`,
  optional scope `:1809–1812`, final FULL receipt AFTER scope `:1813–1814`,
  `col.reverify` + final tree `:1816–1821`, return supplied UNCHANGED +
  `input_hashes` from `col.files` + `measured` `:1823–1830`. Verified.
- `_eligibility:327–342`, `_original_checkpoint:355–377`,
  `_active_effective:380–411` (`ACTIVE_PATH_REBIND` at `:401–402`, no filename
  choice), `_Collector safe/pinned:107–179`, `reverify:191–233`,
  `_tree_map:267–318` (intra-call snapshot, alias/FIFO refusal, `.git` excluded).

P2R `scripts/survey_editorial_retention_v2.py` (2080 lines):

- `verify_retention:1731–2080`: no P1/Git/HEAD; header/basis/proposed `:1764–1777`,
  ordered plan projection `:1778–1826`, I1 State-authority chain `:1827–1843`,
  provisional dest mapping BEFORE retained-State read `:1844–1860`, retained
  State/Profile + label agreement `:1860–1900`, canonical dir/manifest
  `:1901–1915`, dest recomputation `:1916–1925`, inventory + COPY/KEEP rehash +
  staged refs `:1926–1988`, `capture_inputs` historical scope `:1989–2019` with
  mandatory P2R deps `:2017–2019`, canonical bytes `:2041–2042`, final
  re-inventory `:2043–2056`, reverify + close before `RETAINED_SET_VERIFIED`
  `:2056–2066`. Verified by read (excerpts).
- `_retained_expected_sets:829–848` (exact file + dir closure, late file/empty-dir
  refusal), `_Session _close_all:243–278` (primary-preserving secondary
  accounting), `safe_read:369–431` with close-after-read. Verified.

Route predicates:

- Longform `verify_tool_basis:519–582` in `survey_longform_generated_v2.py`:
  ancestor check, exact control/style/contract equality commit-vs-HEAD, clean HEAD
  over controls, no uncommitted control source, closure completeness + byte
  equality vs both commit and HEAD. Uncommitted overlay refuses as committed
  basis. Verified.
- Weekly `_verify_head_bytes:577–631` in `survey_weekly_derivation_v2.py`:
  same shape (ancestor, control equality, dirty/untracked refusal, closure vs
  commit+HEAD). Verified.

These citations confirm the contract's `file:line` map is accurate; no invented
helper responsibilities found.

## 2. Data-only factoring — feasible and coherent

Contract §3 rejects General's initial
`_retention_plan_with_policy(...,verified_set)` / `_pipeline_common(...,
dest_policy, verified_set)` enum. Changing a boolean to an enum does not
eliminate a bypass when the caller supplies the acceptance set. Rejection is
correct and required.

Selected shape is coherent:

- “Data-only” explicitly means no readiness/permission result; the helper may
  perform read-only validation/I/O and is not necessarily a mathematically pure
  function. Private helpers are not a security-capability boundary; required
  checks are enforced by fixed public entry points. This correctly narrows the
  initial “pure” wording and prevents treating a private helper as a new
  acceptance API.
- Fixed completions: existing P1 wrappers always perform absence/alias/collision/
  live-overlap checks before success; new observer always performs actual
  same-invocation P2R `verify_retention` on exact pinned proposal/manifest plus
  fresh common current-basis checks and cross-binding/final stability. No `mode`,
  ignore-destination flag, caller `verified_set`, trusted result/token/context, or
  alternate State bytes (contract §2 API). A returned `VERIFIED` dict is checked
  for bound proposal/manifest SHA but is not sufficient by itself. This closes
  the trusted-token window without duplicating ~600 lines.
- No P1 public signature/schema/scope-meaning change; only private factoring in
  the 1M. Public P1 success still requires absent COPY destinations
  (`:1278–1284`); P2V success requires full retained-set verification instead of
  an absence verdict. Each success path is fixed at its call site.

Feasibility caveat is handled fail-closed: contract requires General to present
the exact named helper extraction/call graph before code and demonstrate that no
P1 public success loses a completion check and no observer success can skip
historical/current/final checks; if the budget cannot accommodate a coherent
split, return an exact blocker rather than duplicate the validator or expand the
public API implicitly. That deferral is appropriate for a design decision; it is
a mandatory pre-code condition (§12), not a current hole.

## 3. Separate live collector / retained snapshot — avoids overlap

Contract §3 “Two dependency stores” correctly diagnoses the concrete hazard:
`_retention_plan:1238` builds `inputs=set(col.files)` and `:1269–1274` refuses
namespace overlap. Pinning retained destinations into that same collector before
plan generation would self-overlap (false `RETENTION_OVERLAP`). The fix —
live collector (P1 `_Collector`: live authority inputs only, retained dests never
pinned there before plan) separate from retained reader (P2R `_Session`-style),
cross-binding by hash comparison without conflation, final `input_hashes` union
only with duplicate path/hash contradiction refusal and only after checks — is
the only safe factoring. Contract explicitly forbids solving it by removing
arbitrary input paths from safety checks. Verified against actual `:1238`,
`:1269–1274`. Coherent.

## 4. Exact all-field comparisons beyond `_pipeline`

Contract correctly states `_pipeline` alone is insufficient and maps the missing
pieces to public `validate_proposal:1715–1801` (headers, exact entire
basis/proposed/retention plan, nonempty descriptive text, staged canonical FILE
bytes) plus `_validate_scope` and `_final_full_receipt_recheck`. It requires
reusing or extracting narrow loading/layout/staged-ref checks and complete
supplied-vs-rederived comparisons, avoiding a second handwritten copy of the
full sequence.

Minor precision note: contract §1/§4 phrase this as “Exact P1 header/basis/
proposed/plan and staged reader bytes” and “complete supplied proposal
fields/plan” with a citation to `validate:1715–1801`, while `correction.md` F1a
enumerates the `:1778–1801` key list explicitly. The contract’s wording plus
citation is sufficient for design, but the pre-code return must enumerate the
exact comparison set (header keys, basis equality, authoring PATH+sha, reader
PATH+sha/canonical sha, ref-digest consistency, retention equality, staged-bytes
equality) so no field is silently dropped. Recorded as mandatory pre-code
condition, not a blocker.

## 5. Strict current root before broad walk

Contract §5.1–§5.3 requires narrow pins of proposal/manifest/State/config/Profile
and schemas (plus supplied scope if any) with lexical/alias/nonregular/FIFO/
escape refusal before reading; actual strict live-State/Profile/canonical-root
checks (`_validated_state_profile_for_tree:1536–1569`) before broad
current-tree walks; expected proposal/manifest namespace derived from current
Profile + exact proposal_id independently of untrusted manifest prefixes; failed
current-State guard refuses regardless of historical readback. This preserves P1
`validate:1728–1771` / `prepare:1616–1618` ordering. Verified against source.
Coherent; historical retained Profile validity alone does not establish current
roots (explicit).

## 6. Scope before final full receipt

Contract §5.6 requires binding optional review via existing `_validate_scope`
semantics, then running the actual full route receipt/current-tool recheck after
scope (not a contract-only shortcut), matching P1 `validate:1809–1814`
(scope `:1809–1812`, `_final_full_receipt_recheck:1813–1814`). It also requires
retained validation to be freshly completed in the same invocation after shared
data equality if any later helper could affect its checked view (bounded second
black-box check permitted, not a new semantic review). This correctly closes the
F3 window where later helpers reread live objects. Coherent.

## 7. Original pins, zero-delta inventories, no laundering

Contract §5.1 (“Byte counts, hashes and relevant file/ancestor identities are
preserved, not resnapshotted to a new baseline after a mismatch”), §5.3
(regular-file bytes + directories including empty + safe type/mode/identity;
fail on unreadable/missing declared inputs/walk errors; initial retention
present; final expected delta zero; known-byte hashes alone do not detect
additions), and §5.7 (final boundary verifies all consumed live and retained
bytes against ORIGINAL pins and expected row bytes/sizes, relevant ownership
identities, full current control/edition/retained inventory, schemas/P2V source
dependencies and HEAD; later checks must not re-snapshot changed bytes into
truth; close every descriptor with explicit primary/secondary disposition)
together forbid resnapshot laundering and require full inventories including new
empty dirs/files. This corrects the initial proposal-time whole-tree + retained-
delta allowance to intra-call zero-delta (retention already present at entry;
observer writes nothing). Coherent; matches `col.reverify:191–233` and
`_Session:243–278,501–519,2056–2066` patterns without claiming global CAS.

Pre-code must still show how edition empty-dir coverage is achieved
(`_tree_map` entry-vs-final plus explicit control/edition/retained inventories),
since `_tree_map` alone is an intra-call snapshot. Recorded as pre-code detail,
not a design hole.

## 8. Current State byte equality + R1 active-before

Contract §4.1–§4.2 selects strict `validate_agent_state`, healthy
`VALIDATED_DRAFT` / approved Architecture / pending Preview without provenance /
pending downstream / inactive exception (`_eligibility:327–342`), canonical live
State from validated Profile/config (no historical clone or pending-basis
admission), live State bytes/path exactly equal to `proposal.basis.state_ref`
(no timestamp/counter/metadata exception), original checkpoint exact
(`:355–377`), active-before exact via `_active_effective:380–411` (fail-closed
invalid, exact coverage, `ACTIVE_PATH_REBIND` refusal, live-byte agreement;
null↔null, ref↔same ref; later different active record is stale, no migration,
no filename-selected record). Verified against source. Defensible bounded
choice; explicitly stated. Coherent.

## 9. HEAD movement, clean closure, uncommitted overlay

Contract §4.4–§4.6 correctly limits HEAD handling: renderer-commit existence
(`git cat-file -e`) alone insufficient; ancestry, exact control/style/contract
changes, dirty/untracked-source refusal, and recorded/current committed closure
bytes are material (matches `verify_tool_basis` / `_verify_head_bytes` reads);
artifact-only HEAD evolution accepted only when full predicates + exact proposal
equality pass; HEAD must stay stable during the call; do not require
HEAD==renderer_commit indiscriminately nor infer eligibility from
`contract_identity` alone; code/control changes outside predicates refuse; no
old-epoch migration.

Contract §4.6 correctly states the writable actual409+uncommitted overlay is a
source/review identity, not a valid committed renderer basis by default
(receipt predicates reject uncommitted control source); future positives must
use independently committed meaningful fixture source incorporating changed
P1+new2 before producing authority; no candidate commit authorized; no claim that
a pre-upgrade captured production proposal remains valid; old 25/36 evidence
does not transfer. This is the correct handling of the current 16-file
uncommitted state. Coherent.

## 10. Historical fingerprints — no invented history

Contract §1, §4.7 correctly state: no complete proposal-time edition directory
map was persisted (do not invent one from graph digests or `capture_inputs`);
unreferenced file added outside closed retained tree before invocation is not
automatically stale unless an actual current validator makes it so; valid scope
created after capture outside `retained/` must exist and be pinned when used;
within-call allowed writer delta is zero. No whole-history/creator/anti-rollback
attestation without external monotonic/authenticated authority (not selected);
implementation must not restore/forge/de-reference State, delete retention, or
roll back to pass (rule distinct from unproved universal detection); matching
files do not prove creator; P2R capture existing-root refusal unchanged; P2V
never takes ownership. `capture_inputs` producer/extras are historical
fingerprints; current equality required only where independently required by
rederived proposal/current validators or actual COPY/KEEP/staged/proposal refs.
Matches P2R `:2009–2019` scope comment and closeout qualifications. Coherent;
avoids the withdrawn whole-tree and origin-attestation overclaims.

## 11. Result shape — fixed observation, no bearer permission

Contract §2 API
`observe_current_authority(root, state_path, proposal_path, manifest_path,
scope_review_path=None)` with no mode/ignore-destination/caller-verified-set/
trusted-token/context/alternate-State is the correct fixed boundary.

Result `CURRENT_BASIS_OBSERVED_NEEDS_SCOPE` /
`CURRENT_BASIS_OBSERVED_SCOPE_BOUND` (contract naming supersedes correction’s
`CURRENT_READINESS_*`; both are observation-only, new naming is clearer and
accepted) with `state_ref`/`proposal_ref`/`retention_manifest_ref`/
`scope_review_ref` (path+sha256), `observed_head`, `measured`
(before_graph_digest/preserved_upstream_digest/proposed_reader_sha256/
graph_nodes/graph_edges/copy_files/keep_refs), `input_hashes` (repo-relative
path→sha256). Requirements — exact key/type/canonical-path validation,
structured `CurrentAuthorityError` with code/phase/original cause in pre-code
return, `scope_review_ref` present when a supplied ordinary valid review was
read even if NEEDS_SCOPE, no success on invalid review, measured counts/digests
not copied into agreement, duplicate path/hash contradictions refuse — are
stated. §2/§6 explicitly state non-durable observation only, never a bearer
permission, reason, State adoption, or future-mutation authorization; names alone
do not guarantee correct downstream use; future writer needs fresh authority;
no new role/gate. Scope matrix (§6: no scope → NEEDS_SCOPE; ordinary valid
without block → NEEDS_SCOPE with ref; invalid → refuse; WITHIN+exact
before/after/upstream/substantive PASS → SCOPE_BOUND observation only;
REQUIRES_OWNER/REJECT/wrong/stale/substanceless → refuse) preserves existing
`_validate_scope` semantics. Coherent.

## 12. Budget, extraction, affected tests, promotion boundary

- Budget 2A1M / 0 schema (new `scripts/survey_editorial_current_authority_v2.py`,
  private-only M `scripts/survey_editorial_correction_proposal_v2.py`, new
  `tests/test_survey_editorial_current_authority_v2.py`) ⇒ future 18 paths,
  3M15A vs 409; current remains 16 until separate implementation; P2R
  module/schema/test, proposal/review schemas, config/controller/publisher/Gate/
  receipt unchanged; more paths require exact blocker + fresh scope. This
  corrects analysis “18–19” to exact 18. Plausible after the factoring map;
  exact line counts properly deferred until diff (no net-savings claim).
- Extraction responsibilities are mapped to actual code (§3: `_retention_plan`,
  `_pipeline`, `validate_proposal:1715–1801`, `prepare:1621–1631`,
  `validate:1802–1821`, live vs retained stores). The remaining exact named
  helper/call-graph demonstration is a mandatory pre-code deliverable, not
  assumed done.
- Minimal affected tests (§7: Longform prose + Weekly envelope real
  P1-prepare→stage→P2R-capture→observer positives with public P1 still refusing
  after capture; real R1-owner predecessor vs stale-active refusal; persistence-
  positive/freshness-negative on mutable COPY-original vs KEEP-drift-refuses-both;
  scope absent/ordinary/malformed/stale/valid-after-capture; receipt ancestry/
  clean-control/closure/contract with artifact-only HEAD control + real
  control-source-change refusal; missing/extra/empty-dir/alias/special-file/
  mixed-proposal/manifest/false-caller-context/zero-delta late-drift/close-fault;
  affected P1/P2R regressions only, no decorative full-suite rerun; each
  injection snapshots immediate mutated-pre/post before restoration, preserving
  the P2R late-plant qualification) are meaningful, use real accepted-chain
  synthetic fixtures (never genuine approvals), correctly allow ordinary scope
  created after capture outside retained, and preserve P1 strict behavior.
  Concrete method counts properly deferred until diff.
- Useful boundary independent of unselected full promotion: P2V observes
  read-only readiness now; staged-review/materialization/receipt/Gate/QA/
  reason/State promotion remains unselected and is stated as not required for
  P2V; controller `REVIEWED_CORE_CHANGE` surface-row support is acknowledged
  without adding editorial reason (correcting analysis §7 old-byte-only error
  per F6). If separation proved impossible, contract requires returning an exact
  blocker instead of silently choosing full promotion. No new Human role/gate or
  production-owned fixture prerequisite. The independence claim is justified at
  design scope.

## 13. Observation summary vs raw scope

This review’s HEAD/tree/status-count/hash/mode and `file:line` citations are
summarized direct observations (transient `rev-parse`/`status`/`sha256sum`/`wc`
reads, `Read`/`Grep` file citations), not a persisted raw-proof packet. Same
applies to packet `source-binding.md` §§1–3 per `correction.md` F6: directly
observed but honestly labeled summary since no raw packet was persisted; 84-cache
path-set equality is distinct from byte rehash and no cache execution occurred.
Durable P2R source/hash/evidence basis remains in
`evidence-20261014T000000Z-correction2/`; no continuous no-drift, runtime
acceptance, or old-suite PASS transfer is claimed here.

## 14. Concrete blockers vs mandatory pre-code conditions

Concrete blockers: none found. No useful-boundary impossibility, no required
public API expansion, no schema change, no new role/gate, no production fixture
prerequisite, no creator/anti-rollback promise needed. If General’s pre-code
return shows the private factoring cannot be split coherently within 2A1M
without duplicating validation logic or changing authority semantics, that
return must state the exact blocker and stop — that path is specified, not
currently triggered.

Mandatory pre-code conditions (must be satisfied before any implementation;
absence blocks code, not design PASS):

1. Exact named private helper extraction/call graph demonstrating no P1 public
   success loses a completion check and no observer success skips
   historical/current/final checks; field-equality set enumerated per
   `validate:1778–1801` plus staged-bytes equality.
2. Exact `CurrentAuthorityError` code/phase/detail shapes and result
   key/type/canonical-path validation.
3. Raw-read/schema/closure snapshot sequencing preserving strict-authority-
   before-broad-walk, scope-before-final-receipt, and original-pin (no
   resnapshot laundering) with empty-dir/full-inventory handling.
4. Current-vs-historical pin table (which hashes must byte-equal now vs which
   `capture_inputs`/closure rows are historical fingerprints only).
5. Source-import/fixture binding (independent committed meaningful fixture
   source for positives; uncommitted candidate never a positive basis) and
   concrete oracle commands with pre/post same-byte evidence (no post-all-checks
   injection magic; seams before declared later checks).

## 15. Verdict

**DESIGN_BOUNDED_PASS** — the selected read-only current-basis observer with
data-only factoring, fixed completions, separate live/retained stores, strict
ordering, exact equality, conditional HEAD handling, historical-fingerprint
limits, fixed `CURRENT_BASIS_OBSERVED_*` observation, and 2A1M/0-schema budget
is feasible, coherent with actual P1/P2R/Longform/Weekly source, and usefully
bounded independently of unselected full promotion, subject to §14 pre-code
conditions. No implementation, runtime, canonical-audit, or adoption authority
follows. DM021 remains OPEN; whole NOT_READY, step4/B3 OPEN, audit unstarted.
Stop at Human Commit Point.

## 16. Scoped closeout — Astra V1–V5 resolution (appended, §§0–15 preserved)

2026-10-14. Read `astra-review-resolution.md` V1–V5 only; no source/test/hash
reruns, no network, no whole audit. Confirmed coherent with reviewed fixed
contract `2ea1d98f…` (§0); no contract edits made or requested.

- V1 exact factoring/comparisons: aligns with §§2/4; pre-code enumeration of
  every header/basis/proposed/plan field plus staged FILE-byte condition remains
  mandatory, not assumed done.
- V2 logical separation: accept that equivalent tagged partitions of a snapshot
  store are allowed; my §3 “only safe factoring” is read as the selected
  design, not a uniqueness proof. Logical live/retained domain separation,
  no retained-dest insertion before planning, no arbitrary-ref removal, and
  conflict-refusal merge remain required.
- V3 ordering/inventories: aligns with §§5–7; `_tree_map` alone does not cover
  required empty-dir inventory, full configured controls (DEFAULT_CONFIG,
  control roots, style, contract files) required not just known consumed hashes,
  scope-before-final-receipt and immediate pre/post no-write evidence (not the
  narrowed P2R late-plant pattern) remain mandatory.
- V4 result/predicates: aligns with §§8/10/11; no P2V pending-basis
  construction/admission, current-vs-historical fingerprint table, conditional
  HEAD handling, and non-bearer observation with no semantic re-review/gate
  remain required.
- V5 fixtures: aligns with §§9/12; independently committed meaningful fixture
  source, uncommitted worktree not a positive basis, Longform/Weekly/R1 plus
  affected P1/P2R regressions remain required.
- Evidence attribution (§3 of resolution): confirmed — this review’s tool
  observations are summarized, not saved raw proof; I rehashed only P1/P2R
  modules plus the contract and observed HEAD/status count, with no independent
  all16 rehash claim. Durable basis remains the P2R packet with §10 limits.

Verdict maintained: **DESIGN_BOUNDED_PASS** subject to §§14–16 pre-code V1–V5.
No new blocker, no source change, no further check required in this unit.
