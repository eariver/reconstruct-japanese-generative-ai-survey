# DM021-P2V — retained-aware current-basis observation contract

2026-10-14. Astra selects **a read-only current-basis observer**, DM021-P2V, using data-only factoring of P1 and unmodified P2R retained-set verification. This is a **design decision, not an implementation or runtime PASS**. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Full correction promotion/reason/State adoption remains unselected.

Basis: [P2R assessment](rephase-1-dm021-p2r-assessment.md) §4 and mandatory final qualifications; fixed P1 contract07e89990 / P2R contract194fd7de. Source is unchanged actual409+16file composite (P1 module5d2fde45, P2R module3833b14a/schema347e5499/test4155baab, complete16patch5b79218e), plus preserved84 caches. [Analysis packet](../notes/rephase-1-dm021-current-authority/README.md) retains General's initial proposal, root feedback and correction. This selection supersedes incompatible recommendations there. Read independent design review and mandatory Astra resolution together with this contract.

## 1. Meaning and necessary limits

P2R proves persistence of COPY bytes plus required KEEP refs bound to a supplied proposal. It intentionally does not validate mutable live originals/current State. P1 rederives current authority/proposed reader but rejects existing retention destinations. P2V combines **fresh checks in one invocation**, without deleting retention, faking State or interpreting an earlier success dict as permission.

Three comparisons must remain distinct:

| Comparison | Authority/data | Required equality |
|---|---|---|
| Current basis vs supplied proposal | Actual strict canonical State/Profile/checkpoint/active receipt/Gate/upstream and rederived reader/graph | Exact P1 header/basis/proposed/plan and staged reader bytes |
| Retained-set consistency | Same supplied proposal + manifest + retained State/Profile/COPY/KEEP/staged refs | Full P2R validation, exact path/hash/size/schema/inventory |
| Stability during this call | Initially pinned narrow files, dynamically discovered expected refs, then validated-root/control inventories | No changed known bytes/identity/type or inventory additions/removals at declared later checks |

No complete proposal-time edition directory map was persisted. Do not invent one from graph digests or capture_inputs. An unreferenced file added outside the closed retained tree **before** this invocation is not automatically stale unless an actual current validator makes it so. A valid scope review can be created after capture outside `retained/`; it must exist and be pinned when this invocation uses it. Within the observer call, no allowed writer delta exists: retention already exists and the observer writes nothing.

No whole-history/creator/anti-rollback attestation: a coherently restored set of identical valid bytes at canonical paths cannot be distinguished from continuous history without an external monotonic/authenticated authority, which is not selected. The implementation must not itself restore/forge/de-reference State, delete retention or roll bytes back to pass. That rule is not a claim that every external rollback can be detected. Matching files do not prove who created them. P2R capture's existing-root refusal is unchanged; P2V never takes ownership of that root.

## 2. Exact selected delta / API

Relative to the current16-file component, expected **2A+1M, no schema changes**:

1. A `scripts/survey_editorial_current_authority_v2.py`
2. M `scripts/survey_editorial_correction_proposal_v2.py` — private data factoring only; existing public prepare/validate signatures, schemas, scope meanings, absence/alias/overlap checks and success conditions remain strict.
3. A `tests/test_survey_editorial_current_authority_v2.py`

Future composite would be18 paths,3M15A relative to409 (P1 module was already an added path). Current source remains16 until a separate implementation unit. P2R module/schema/test, proposal/review schemas, config/controller/publisher/Gate/receipt and all other source remain unchanged. More paths require an exact blocker and fresh scope decision.

```
observe_current_authority(root, state_path, proposal_path, manifest_path,
                          scope_review_path=None) -> observation
```

No `mode`, ignore-destination flag, caller-supplied verified_set, trusted result/token/context or alternate State bytes. All authority is read from actual named files. The optional argument supplies an existing review file, never a fabricated approval.

Result is an in-memory dict, no writer/CLI/new persisted schema:

```
{
  "result": "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE" | "CURRENT_BASIS_OBSERVED_SCOPE_BOUND",
  "state_ref": {"path": ..., "sha256": ...},
  "proposal_ref": {"path": ..., "sha256": ...},
  "retention_manifest_ref": {"path": ..., "sha256": ...},
  "scope_review_ref": null | {"path": ..., "sha256": ...},
  "observed_head": ...,
  "measured": {"before_graph_digest": ..., "preserved_upstream_digest": ...,
               "proposed_reader_sha256": ..., "graph_nodes": ..., "graph_edges": ...,
               "copy_files": ..., "keep_refs": ...},
  "input_hashes": {repo_relative_path: sha256, ...}
}
```

Exact key/type/canonical-path validation and structured `CurrentAuthorityError` with code/phase/original cause are required in the pre-code return. `scope_review_ref` is present when a supplied ordinary valid review was read, even if it lacks a correction-scope block and the outcome is NEEDS_SCOPE. No success on invalid supplied review. Counts/digests are measured, not copied into agreement. Duplicate path/hash contradictions in the merged observation refuse; merging is only after live/retained checks, not a way to change planner inputs.

This is a bounded observation of present facts, not a durable authorization token, semantic judgment, reviewed Core-change reason or permission for later mutation. Names alone do not guarantee correct downstream use. A future writer must establish its own fresh authority and failure/write contract.

## 3. Fixed completion paths, shared data derivation

Reject General's initial enum `ABSENT_REQUIRED/RETAINED_BOUND` plus caller `verified_set`: changing a boolean to an enum does not eliminate a bypass. Instead use shared **data-producing private helpers**, with fixed public completion paths. “Data-only” means no readiness/permission result; the helper may perform read-only validation/I/O and is not necessarily a mathematically pure function. Private Python helpers are not a security-capability boundary; required checks are enforced by the supported public entry points.

Map the extraction to actual P1 code:

- `_retention_plan:1231–1288`: separate deterministic row/path/policy construction and common safety/namespace checks from the absence requirement. Existing P1's wrapper always performs all current absence, alias, collision and live-input overlap checks before returning success. Common safety and overlap checks also apply in P2V; only existing destinations are handled by full retained-set verification instead of an absence verdict.
- `_pipeline:1291–1492`: extract reusable current-basis/context derivation, including actual State eligibility/canonical State, original checkpoint/current active resolution, independent before/after reader derivation, upstream equality, full receipt/Gate/pre-TeX/bundle checks, graph/digests and plan data. It returns data/context, not input_hashes or observer readiness. Existing `_pipeline` wrapper used by public P1 applies its fixed absence policy; no branch selected by caller flags.
- `validate_proposal:1715–1801`: reuse or extract narrow loading/layout/staged-ref checks and complete supplied-vs-rederived comparisons (headers, exact entire basis/proposed/retention plan, nonempty descriptive text, staged canonical FILE bytes). Calling the factored pipeline alone is insufficient. Avoid a second handwritten copy of the full validation sequence.
- Existing `prepare_proposal` and `validate_proposal` retain schema validation, optional scope semantics where applicable, **full final receipt recheck after scope/schema**, pinned stability and final tree checks (`prepare:1621–1631`, `validate:1802–1821`). Every success still requires absent COPY destinations; P1 called after capture still refuses.
- New observer always requires actual P2R `verify_retention` on the exact proposal/manifest plus fresh common current-basis checks and cross-binding/final stability. A returned VERIFIED dict is checked for bound proposal/manifest SHA but is not a caller-supplied proof or sufficient by itself.

**Two dependency stores:** the live derivation collector contains only inputs discovered by current authority/rederivation (including staged proposal inputs). Retained COPY/manifest/inventory pins live in a separate read session/outer snapshot. `_retention_plan` currently tests `col.files` for live-input overlap (`1238,1269–1274`); merging retained destinations there before planning would create false self-overlap. Never solve that by removing arbitrary input paths from safety checks. Compare the stores' expected hashes without conflating live originals and retained copies. The final input_hashes observation may union them only with conflict rejection.

Before code, General must present the exact named helper extraction/call graph and demonstrate that no P1 public success loses a completion check and no new observer success can skip historical/current/final checks. Helpers should factor existing logic, not rewrite600+lines or change authority semantics. If the budget cannot accommodate a coherent split, return an exact blocker rather than duplicate the validator or expand the public API implicitly.

## 4. Fresh basis and epoch predicates

1. Strict current `validate_agent_state`, healthy VALIDATED_DRAFT, Architecture approved, Preview pending without provenance, downstream pending, inactive exception. Canonical live State from validated Profile/config; no historical cloned State or pending-basis admission (`_validated_state_profile_for_tree:1536–1569`, `_eligibility:327–342`). Historical retained Profile validity alone does not establish current roots.
2. Live State bytes/path must equal `proposal.basis.state_ref` exactly; no timestamp/counter/metadata exception. Original validation checkpoint and active revalidation pointer/ref/content remain exact. Real R1 predecessors existing **before** proposal are supported through current `_active_effective:380–411`; a later different active record is stale. No filename-selected record or fallback from referenced-invalid authority.
3. Independently rederive current before/proposed reader and typed graph through current actual route loaders. Compare complete supplied proposal fields/plan and canonical staged FILE bytes as current public P1 does. Preserve accepted Draft/upstream and Longform-authored-prose/Weekly-envelope scope.
4. Full current receipt predicates remain mandatory: Longform `verify_tool_basis:519–582` and receipt validation, Weekly `_verify_head_bytes:577–631` and receipt validation, plus current State/Gate/bundle/review checks. A renderer commit's mere existence is insufficient: ancestry, exact control/style/contract changes, dirty/untracked-source refusal and recorded/current committed closure bytes are material. No controller pending context is added to this observer. Any existing Weekly loader fallback cannot bypass the observer's independent strict live-State guard.
5. Artifact-only HEAD evolution may be accepted only when those full predicates and exact proposal equality pass; HEAD must stay stable during this call. Do not require HEAD==renderer_commit indiscriminately, or infer eligibility from contract_identity equality alone. Code/control changes not covered by current predicates refuse; no old-epoch migration is selected.
6. The writable actual409+uncommitted overlay is a source/review identity, **not** a valid committed renderer basis by default. Existing Longform/Weekly receipt predicates reject uncommitted control source. Future engineering positives must use independently committed meaningful fixture source incorporating the changed P1 +new2 BEFORE producing authority. No candidate commit is authorized, and no claim that a pre-upgrade captured production proposal automatically remains valid is made. Old25/36 evidence does not transfer to the refactor.
7. P2R capture_inputs producer/extras are historical fingerprints. Require current equality only where independently required by rederived proposal/current validators or actual COPY/KEEP/staged/proposal refs. Do not transform every recorded input into a blanket current-code/whole-tree historical lock.

## 5. Same-invocation ordering and final window

The concrete implementation must satisfy this ordering/dependency contract; no asynchronous step or past observation is reused as authority:

1. Raw-safe narrow pins of supplied proposal/manifest/State/config/Profile and relevant schemas (and supplied scope if any); reject lexical aliases/nonregular/FIFO/escape before reading. Scope/staged identity parsing does not generate approval. Pin actual current HEAD through checked sanitized Git routing. Byte counts, hashes and relevant file/ancestor identities are preserved, not resnapshotted to a new baseline after a mismatch.
2. Perform actual strict live-State/Profile/canonical-root checks **before** broad current-tree walks. Derive the expected proposal/manifest namespace from this current Profile and exact proposal_id, independently of untrusted manifest prefixes. A failed current-State guard refuses, regardless of historical readback status.
3. Snapshot validated source_root/survey_root and the complete declared controls: DEFAULT_CONFIG, implementation_control_roots, style path and flattened configured contract_files. Include regular-file bytes, directories (including empty), safe type/mode/identity as relevant; fail on unreadable/missing declared inputs/walk errors. Initial retention is present in these snapshots; final expected delta is zero. Known-byte hashes alone do not detect additions.
4. Invoke P2R verification using exact pinned proposal/manifest paths; compare its returned file hashes to the original pins. Pin actual COPY/KEEP/staged/historical State/Profile bytes against the explicit plan/ref hashes/sizes in the separate retained reader and exact closed inventory. A helper that reopens files cannot silently switch which proposal/manifest or row is being validated. No verification token supplied by caller; no claim that this observer witnessed the original capture invocation.
5. Run common current derivation/plan and supplied-proposal comparisons using the separate live collector; compare live State/original checkpoint/active-before/graph/reader/plan to the same supplied proposal and independently validated retained manifest. If helpers are reordered for a safer pre-read binding, preserve all initial pins and strict-live-before-broad-walk constraints; return the exact order before code.
6. Bind optional review using existing `_validate_scope` semantics. Then run the **actual full route receipt/current-tool recheck after scope**, not a contract-only shortcut. Retained validation must also be freshly completed in this invocation after shared data equality if any later helper could affect its checked view; a second black-box check is permitted as a bounded tradeoff, not a new semantic review.
7. Final boundary verifies all consumed live and retained bytes against ORIGINAL pins and expected row bytes/sizes, relevant ownership identities, full current control/edition/retained inventory, schemas/P2V source dependencies and HEAD. Later checks must not re-snapshot changed bytes into truth. Close every descriptor with explicit primary/secondary error disposition before returning. A later helper's reads are not exempt from the final observation window.

Reuse existing narrow P1 data and P2R safe-reader/inventory helpers where feasible without changing P2R; no new generic filesystem/lock/journal framework. Standalone P2R still does not acquire current authority. Preserve the distinction between no writes by this observer and refusal on an external injected change. No continuous no-drift, global CAS, crash atomicity or universal hostile-race exclusion is claimed. An injection after every last observation is not a promised detection oracle.

## 6. Scope/review behavior and refusal matrix

No scope argument → NEEDS_SCOPE. Supplied ordinary valid pre-TeX review without correction block → NEEDS_SCOPE, with its exact ref reported. Supplied invalid review → refuse. A WITHIN_APPROVED_AUTHORITY correction block must bind exact before reader / proposed reader path+SHA / preserved-upstream digest and substantive scope check; then SCOPE_BOUND is an observation only. REQUIRES_OWNER_DECISION, REJECT, wrong/stale/substance-less scope cannot bind. No generated PASS/new Human Gate/role.

| Case | Required result |
|---|---|
| Valid unchanged live basis + full retained set, no scope | Observed current basis, NEEDS_SCOPE |
| Same + valid exact existing scope | Observed current basis, SCOPE_BOUND |
| Valid scope file newly created after capture outside retained tree | May succeed if actual predicates pass and stable during call; no fabricated historical inventory rejection |
| Mutable live State/COPY original changed, retained bytes still valid | P2R may verify persistence; P2V must refuse freshness/basis |
| Required KEEP/retained/proposal/staged bytes changed | P2R and P2V refuse as applicable; do not promise persistence-positive on KEEP drift |
| New active R1 after proposal; stale/invalid epoch or authority | Refuse, no migration/rebinding/pending bypass |
| Missing/partial/extra retained file/dir, wrong manifest path or row mapping | Refuse; no takeover/cleanup |
| Identical complete same-path retained data of unknown creator | No creator-attestation claim; evaluate current predicates, do not infer successful capture/adoption |
| Control/edition/retained/HEAD/schema/scope drift between helpers | Refuse at declared later checks; report no observer writes |

Existing controller revalidation supports changed surface rows under REVIEWED_CORE_CHANGE; this observer adds no truthful editorial reason or adoption path. Full publication remains a separate design problem.

## 7. Required future implementation evidence and stop

Before implementation, General returns exact helper extraction/API/result/error shapes, raw-read/schema/closure snapshot sequencing, current-vs-historical pin table, source-import/fixture binding and concrete commands/oracles. Stop on a real fixture/API/budget/authority blocker, not a new production-owned-fixture/Human approval prerequisite.

Required engineering coverage (synthetic accepted-chain fixtures, never genuine approvals):

- Longform authored prose and Weekly envelope: real P1 prepare→stage→P2R capture→new observer positives; existing public P1 prepare/validate remain destination-strict after capture. Baseline unretained P1 behavior/result-field/derivation/schema/scope checks remain valid under the refactor.
- Real R1 owner predecessor(s), original-vs-active identity; no forged “R1-like” pointer. New active pointer after proposal refuses.
- Persistence-positive/current-basis-negative live-State or other mutable COPY-original change; KEEP drift refuses both. No live-original substitution using retained State. Exact path/hash identity and wrong-path equal bytes negatives.
- Optional existing scope: absent, ordinary-without-block, malformed/non-PASS/wrong-before/after/upstream/REJECT/REQUIRES_OWNER, valid scope created after capture; no review path rebinding.
- Current receipt ancestry/clean-control/closure/contract checks including artifact-only HEAD movement control, and a real control-source change refusal, not just synthetic contract-string mutation. Full source18 identity and fixture source must be separately bound; no old PASS transfer or candidate commit.
- Missing/extra retained files and empty dirs, aliases/special files with explicit no-read checks, mixed proposal/manifest, false caller context unavailable at public API, exact zero-delta cross-helper late drift and close faults.
- Each external-injection case snapshots immediate mutated-pre/post or exact known injected delta BEFORE any restoration; do not repeat the P2R late-plant post-cleanup overclaim. Catchable seams occur before a specified final check. Code-level call-graph and affected P1/P2R regression evidence accompany the new tests; no decorative entire old-suite rerun.

Performance/storage/review costs are not zero: common derivation may require repeated full receipt work, two dependency stores and final re-inventory. Factoring is selected to reduce duplicated validation logic; no measured net savings or guaranteed small line count is claimed. Estimate focused method counts only after the actual diff; prefer safe immutable accepted fixture bases/copies to repeated expensive setup when demonstrably equivalent.

After qualified author-independent design review and Human continuation, the next unit is P2V concrete interface/fixture return to Astra, then the selected read-only implementation after that return. No automatic full promoter/reason/State/Candidate/Preview work. Stop at this design Human Commit Point; ordinary reconstruct Commit/Push remains Human-owned.
