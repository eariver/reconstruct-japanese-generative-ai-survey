# DM022 pre-Architecture — Task B R2 pre-code map: schemas / producers / generation DAG (Astra CHANGES_REQUIRED repair)

AUTHOR-side pre-code return, Task B R2. Preserves R1 (`schemas-generation-dag.md/json`) unchanged. No implementation, no runtime/import/tests/build/fixtures/restore/network/Git mutation/source writes. Human `ab84b4f` assumed; 55 bare Gitlinks preserved untouched, no re-audit.

Binding inputs (read-only):

- Selected decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` **including §11**, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351 B.
- Mandatory `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` **including §5**.
- BOTH independent reviews WITH FINAL-BINDING addenda (selection only; B2/B4 pre-code OPEN at entry).
- Packet `notes/rephase-1-dm022-prearchitecture-contract/README.md`; `AGENTS.md` current entry.
- Actual source read-only: proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60` = actual `409b292`/tree `8ce36998` + 93 paths 40M53A/742. All `file:line` below are that proof-copy unless stated `workspace:`.
- Aligned revised siblings in same dir (read, not edited): `authority-consumer-map.md` (Scope A, B2 table + LOW/HIGH abstract + terminology — now fixed to functional names per ROOT §7 below), `guard-resume-oracles.md/json` (Task C, owns seven-slot/guard/retention/HEAD-tree/IO-resume/oracles — referenced, not duplicated), `inventory.json` (28-row B2 map).

Author is not independent acceptance. Externally supplied author-independent research/authority-consumption decision is ingress data (before/after/raw/allowlist hashes, immutable files); no new Sol/Human Gate, no genuine PASS generated inside the writer, no hash-only/raw rebind/caller-verified-dict/pending-flag permission, no `production.verify_state_basis` substitution.

B4 is NOT claimed closed by R1. This R2 repairs all 10 ROOT findings. B4 closes as a concrete map only when Astra + author-independent readiness reviewer confirm this R2 **plus** the still-required C/A closures (§15). Implementation remains blocked.

---

## 0. R1 → R2 changed decisions (all 10 ROOT findings)

R1 file preserved as history; every row below is a binding change in R2.

1. **Package `basis.state_path` (R1 §4/§8 table).** R1 said `basis.state_path` = retained COPY path. **R2:** ALWAYS `package.basis.state_path` = original canonical LIVE source path (repo-relative, e.g. the canonical `production-state.json` path that `prepare_evidence_package(repo_root,state_path,…)` records via `_rel(repo_root,state_path)` at `survey_evidence_v2.py:640-652`), `package.basis.state_sha256` = exact before bytes (`sha256_file(state_path)` at pin time). Retained COPY (e.g. `R/retention/before-state.json`) is a **separate map entry with same bytes** (`copy_sha256 == basis.state_sha256`, verified by re-hash), never a rebinding of `basis.state_path`. Rationale: `validate_evidence_package_basis:898-946` enforces `state_sha` drift + `verify_state_basis`; State-free `_validate_evidence_package_basis_content:839-895` enforces `basis.state_path == canonical_state_path` identity (`:860-864`) with **no live SHA equality**; `agent_tool._historical_state_basis_wrapper:53-118` allows State-SHA drift **only** after content-addressed acceptance (`package_sha == acceptance.package_sha`) + full same-source binding. Rebinding basis to a COPY path would break both the canonical-path check and the content-addressed evolution rule. R2 §3 binds this.
2. **State-bound producer reuse (R1 §4 “unchanged callsite-only”).** R1 claimed `accept_evidence_results / accept_edition_views / prepare_evidence_package / validate_profile_completeness` can be reused unchanged by omitting `implementation_sha`. **R2:** those public funcs call State-bound validators (`accept_evidence_results:1159-1167` → `validate_evidence_package_basis:898` → `verify_state_basis:959` + `validate_screening_acceptance:490` with impl SHA; `accept_edition_views:1506` → `validate_evidence_acceptance:1412` (State-bound); `prepare_evidence_package:550` → `core.verify_state_basis`; `build_materiality_ledger:1579` → `validate_screening/evidence/views` with impl SHA; `run_evidence_v2_interactive:747-758` → `validate_profile_completeness` with impl SHA). R2 defines exact narrow shared primitives (pure, §4) + wrapper-delegation/exclusive-writer plan preserving all content/digest/dirname rules with old public behavior intact. LOW exposes **read-only/pure builders only** (return dicts / write only to caller-owned temp via HIGH exclusive writer); it never calls public State-bound acceptors as “detached writers”.
3. **LOW public signature (R1 §8 `validate_revision_graph` with caller dicts).** R1 public LOW took `ledger/completeness/expectations` dicts and returned `[] PASS`. **R2:** public LOW entries take **`repo_root + request/candidate/proof/checkpoint PATHS only** and derive context internally from pinned source/COPY/previous-checkpoint (re-hash + schema + content checks). Private pure in-memory helpers (dicts-in/dicts-out) exist **only after trusted internal load** and are never public authority. R2 §5 binds the PATHS-only public API.
4. **Report ↔ checkpoint cycle (R1 §§9-10).** R1 pre-adoption report contained `checkpointRef`, while checkpoint validation required the report → cycle. **R2:** pre-adoption REPORT refs request/candidate/proof/decision/before-COPY + all-4-artifacts, actual operation + producer boundary, current tools/work-ref — **NO `checkpointRef`, NO `afterStateHash`, NO `guard hash`**. Checkpoint references the completed report (`report: SizedRef`). Optional POST completion report/receipt (separate type) may bind `checkpoint + derived expectedAfterState + slot inventory + guard release`, but the checkpoint never back-references it. Status bools (`triplet_match`, `lineage_match`, `proof_pass`, …) are **descriptive recomputed observations**, never bearer permission. R2 §§6/9 bind this.
5. **`run(request+decision)` future-ref (R1 §8).** R1 `run(repo_root,state_path,request_path,decision_path,revision_id)` generated the candidate after the decision that purportedly reviews it. **R2:** split public API — `prepare_*` (immutable candidate + manifest, no decision input) → external decision (binds already-existing immutable prepare outputs) → `adopt_*/finalize` (validates decision + proof/report + guard/checkpoint/switch/clear/postread/release). No function requires a future ref. Final names chosen consistent with Task C phases (§7).
6. **Generic 4-key refs (R1 §13).** R1 used one generic `{path,sha256,byte_count,kind}` for all refs. **R2:** exactly three ref shapes, no generic: `ArtifactRef={path,sha256}`, `SizedRef={path,sha256,byte_count}`, `NamedRef={name,path,sha256}` (`sha` in ROOT shorthand = `sha256` hex64 per existing `artifactAuthority: stage-checkpoint-v2.schema.json:111-119` / `namedAuthority:126-134` / `survey-production-state.schema.json:102-110`). Tagged `kind`/enum variants only where the declaring schema states them (e.g. checkpoint `artifacts[].name` enum, guard `phase` owned by C). R2 §8 binds every field to one shape.
7. **Bare shapes / SELF confusion / module budget (R1 §§8-9).** R1 left `contract: object`, `...`, `SELF` ambiguous and fixed an arbitrary 2-module/4-schema budget with DM-issue runner names. **R2:** all `required/if-then/additionalProperties/digest` lists are literal complete shapes (§9, no ellipsis/bare-object/`SELF`-object). Named content digests follow project convention (`result_set_sha256`, `view_set_sha256`, `package_sha256` pattern → `revision_proof_sha256`, `preadoption_report_sha256`, `supersession_checkpoint_sha256`), each = `sha256_object(body-minus-self)`; FILE SHA (`sha256_file`) is distinct and separately bound. Guard/retention/completion embedded schemas are **coordinated with C** (`guard-resume-oracles.md` owns guard/record/write-set/fault oracles + retention manifest + completion receipt shape; R2 references, never duplicates). Module count justified: **2 modules + 5 required schemas + 1 optional POST receipt** is minimal to keep prepare/manifest vs proof vs pre-adoption-report vs checkpoint vs POST-receipt distinct types/stages with a one-way SHA DAG (§§2/9); merging any two would force a self/future-SHA cycle. Adopted ROOT-preferred functional names: LOW `scripts/survey_research_authority_v2.py`, HIGH `scripts/survey_prearchitecture_acceptance_v2.py` (no permanent DM-issue runner name). Function-local imports/extraction avoid the real `evidence(top)→screening(top)→agent(function-local: survey_screening_v2.py:465,480)` chain (actual call graph, not a name ban) — §9.
8. **Changed-package mechanics (R1 §7).** R1 invented `ledger.self_digest`; claimed unchanged `cardSHA` can coexist with changed mechanical `basis.task_sha`; allowed arbitrary “propagation” reasons. **R2:** enumerates exact source schema fields (§10); package has **no** `self_digest` (basis fields per `evidence-v2-run-package.schema.json` only). `card.basis.task_sha256` change ⇒ task bytes changed ⇒ card bytes changed ⇒ card SHA changes; unchanged `cardSHA` is held **only if** `task_sha256` (and all other basis + semantic fields) are unchanged. Unchanged `view.view_sha256` is held **only if** `cardSHA` still unchanged (view `evidence_sha256` binds card SHA). Semantic-projection exclusions list **only specific actual basis hashes** (e.g. `ledger.basis.evidence_acceptance_sha256`), each independently derived (recompute digests, compare FILE SHAs); no arbitrary reason permit.
9. **DM017 union (R1 §§3.4/5).** R1 derived `dimension/description` from Profile for all obligations, inventing values for named-only IDs. **R2:** consumes **full explicit obligation rows** (all 7 `OBLIGATION_KEYS` per `survey_completeness_v2.py:25-35`) including named-only `dimension/description`; derives the ID set (Profile-initial ∪ Discovery-named `provenance.obligation_ids`) + references (`discovery_ids` = declaring DIDs, `evidence_task_ids` via ledger); verifies unchanged `dimension/description` for every existing ID against the **old valid completeness** (before-State checkpoint refs), never invents from Profile. R2 §11 binds this.
10. **New authority role (R1 §§6/9-10).** R1 added `reviews[]` row `DM022_SUPPLIED_DECISION kind AGENT_RESEARCH PASS` as a new authority role and treated the supplied decision as a generic PASS dict / writer-generated genuine PASS. **R2:** no new `AGENT_RESEARCH` authority role enum beyond the existing `reviews[].kind ∈ {DETERMINISTIC,AGENT_RESEARCH,AGENT_EDITORIAL,AGENT_VISUAL}` (`stage-checkpoint-v2.schema.json:74`); no new record branch invents a role. Checkpoint `reviews[]` carries **only** `DM022_SUPERSESSION_PROOF kind DETERMINISTIC status PASS result=proof SizedRef` (local content proof, not approval). The supplied independent decision is bound as a separate **`decision: SizedRef`** field (FILE re-hash + allowlist + content checks per §6 of R1, retained), i.e. provided report **data**, never a generic PASS dict and never a writer-generated genuine PASS (admit ≠ Selection/Architecture/Human approval). Branch defined/explained in §12.

Staging clarification (ROOT detail, binds §2): immutable before-State/slot snapshots **may** be captured as prepare inputs **within the NEW owned R** before candidate generation (no old-authority mutation: no canonical writes, no State writes, no guard claim yet; snapshots are inert preparation with present/absent inventory). After the external decision, adopt **seals/reverifies the final retention inventory** (present bytes still equal captured old bytes, still unaccepted/unbound, guard not yet held) **before** claiming the guard. Destructive order is unchanged from the decision (`guard → record → State triplet switch → checked clear → postread → release guard → regen`). Prepared candidate manifest (prepare output) and final proof/pre-adoption-report (adopt inputs/outputs) are **distinct types/stages** so the external decision binds already-existing immutable outputs; every DAG edge is one-way with no self-reference. Guard/cleanup-completion details are owned by C.

---

## 1. Scope, bindings, alignment

Same decision/hash/source/AGENTS pins as R1 §1 (not repeated to save space; R1 preserved). Added alignment:

- Scope A (`authority-consumer-map.md`): terminology (§0 table: kind/reason, operation vs producer boundary, checkpoints, artifacts, report, path, history, agent-vs-core), new-kind branch predicates (§§1/34-36: live-SHA/issue/contract/impl/review-result/artifact-map STRICT, `from==to==EVIDENCE_REVIEWED` + `producer_boundary` + same-ref triplet + new proof/report, `canonical_checkpoint_path:1608-1610` / `_validate_stage_artifacts:1622-1655` exempt only inside the new branch), B2 28-row table + `inventory.json` (all rows either R4-resolve or explicit-refuse; `VERSIONED_ACTIVE`/renewal/editorial walkers fail-closed unknown until updated — §3g). R2 reuses these invariants verbatim and fixes only the B4/producer/schema/DAG surface per the 10 findings. B2 remains implemented-or-refused per caller in code; this R2 does not claim B2 closure.
- Task C (`guard-resume-oracles.md/json`): owns seven-slot boundary (profile-`source_root`-relative 7 incl. audit `orchestration/v2/interactive/selection-architecture-audit.json:330-343` unguarded-today vs `199-201` six-guarded), retention COPYs (before-State + every present slot + present/absent inventory + accepted/Human-bound scans + post-copy bytes/inode/identity + changed/foreign refuse), guard root/path/schema/owner/FD-inode-hash + every-producer check table + no-State-arg caller rule, active-research R4 readback rule (§11.2), selected order with phase predicates, F1–F13 failure/resume/write-set oracles (no auto-rollback, no CAS/crash claim), HEAD/tree predicate + complete path set + code-before-authorities (E) + artifact-only descendant rule, public oracles O-W1/O-T1/O-W2/O-T2/O-R1/O-G1–G3/N1–N12. R2 references C for all guard/retention/completion/IO/HEAD/oracle shapes and defines only the revision/proof/report/checkpoint side with compatible `SizedRef/NamedRef` + `phase` coordination (no competing guard schema).

All `file:line` are the proof-copy.

---

## 2. Staging with before-snapshot clarification (one-way DAG, no old-authority mutation)

`A` = attempt owner (executor+invocation). `R=<source_root>/research/v2/acceptance-revisions/<revision_id>` (safe single segment, Profile-derived root, no latest-scan). `G` = guard file (C-owned shape). `S_before`/`S_expected` = known-byte State files. `M` = prepare manifest. `P` = deterministic proof. `RPT` = pre-adoption report. `CP` = typed checkpoint.

```text
prepare phase (no decision input, no guard claim, no canonical/State mutation):
  pin current basis (S_before bytes + HEAD/tree/contract + live pins, HIGH-side)
  → capture immutable before snapshots within NEW owned R (S_before COPY + every present 7-slot COPY + present/absent inventory; inert preparation, old authority untouched)
  → generate truthful candidate under R (package/tasks/cards/views versioned ledger/completeness inputs, §10) bound to S_before + existing Discovery/Screening
  → emit immutable revision manifest M (SizedRef list of every prepare output, §9; FILE SHA is M identity, no embedded self field)
external decision (binds already-existing immutable M outputs; no future ref):
  supplied independent bundle D references M FILE SHAs + before SHAs + Raw SHAs + allowlist (immutable files only, §6 R1 retained)
adopt/finalize phase (validates D + seals + guards + records + switches + clears + verifies):
  seal/reverify final retention inventory (present bytes still equal captured old bytes, still unaccepted/unbound) → claim + revalidate G (C §4)
  → complete deterministic proof P (LOW pure, refs M + D + before, §9) → complete pre-adoption report RPT (refs M + P + D + before + all-4-artifacts + operation/boundary + tools/workref; NO checkpoint/afterState/guard refs, §6)
  → complete typed checkpoint CP (refs completed RPT + P + D + before + retention plan; SELF-excluded digest + FILE SHA, §9)
  → prevalidate S_expected (S_before with ONLY provenance.{evidence,materiality,completeness} → SAME new CP ref) → ONE known-byte State switch → checked clear of remaining exact old slots → postread/inventory → release OWN G → normal regen (C §§6-7)
```

Destructive order identical to the decision (guard→record→State→clear→release). Prepare snapshots are immutable preparation, not the guarded destructive sequence. M vs P/RPT vs CP vs optional POST receipt are distinct types/stages; each SHA edge points backward only (M←D←P←RPT←CP←State←POST-receipt). No self/future SHA.

---

## 3. Package basis fix (Finding 1)

ALWAYS, for both old and new packages (`evidence-v2-run-package.schema.json` basis shape):

```json
{"profile_path": "<repo-rel>",
 "profile_sha256": "<hex64>",
 "state_path": "<canonical LIVE repo-rel, e.g. <source_root>/production-state.json as recorded by prepare>",
 "state_sha256": "<hex64: exact bytes of that LIVE path at pin time>",
 "discovery_path": "<repo-rel>",
 "discovery_sha256": "<hex64>",
 "screening_acceptance_path": "<repo-rel>",
 "screening_acceptance_sha256": "<hex64>"}
```

- New DM022 package: `state_path` = original canonical LIVE source path (same string the normal `prepare_evidence_package:539-681` records at `:644-652` via `_rel(repo_root,state_path)`); `state_sha256` = exact before bytes `sha256_file(S_before)` at prepare-pin time. Verified State-free by `_validate_evidence_package_basis_content:839-895` (`basis.state_path == canonical_state_path` at `:860-864`, file/contract drift at `:867`, screening via State-free content at `:874-886`, no `verify_state_basis`/`repository_commit_sha`).
- Retained COPY (e.g. `R/retention/before-state.json`) is a **separate manifest entry** `{source_rel: <canonical LIVE path>, copy_rel: <R retention path>, source_sha256, copy_sha256, byte_count, st_dev/ino both sides}` with `copy_sha256 == source_sha256 == basis.state_sha256` (re-hashed on capture + resealed in adopt). It is **not** substituted into `basis.state_path`. Any “copied-path rebinding” (rewriting basis to the COPY path) is refused.
- Old accepted package State-SHA evolution (different `state_sha256` at a different lifecycle) is governed **only** by the content-addressed acceptance rule: `agent_tool._historical_state_basis_wrapper:53-118` permits the historical drift **iff** `sha256_file(package_path) == acceptance.package_sha256` (sibling acceptance binds exact package bytes) **and** full same-source binding holds (state path inside repo, regular file, no symlink/traversal, `adjusted_basis.state_sha256 := sha256_file(current State)` then re-run original validator). DM022 proof follows the same discipline: old package `state_sha` stays historical (validated detached via retained COPY + `historical_state`), new package `state_sha` is the new before; neither is rewritten to the other’s path.

---

## 4. Narrow shared primitives + wrapper delegation / exclusive writers (Finding 2)

### 4.1 Pure (State-free, no `implementation_sha`, no State load) — LOW may call

From `survey_evidence_v2.py` / `survey_screening_v2.py` / `survey_completeness_v2.py` (exact names, no invention):

- `_check_evidence_package_fields_content(package):719-728`, `_check_evidence_package_files_content(repo_root,package):731-766` (profile/discovery/screening/prompt/contract SHA drift; no State SHA, no `verify_state_basis`), `_check_evidence_tasks_content(repo_root,package_path,package,acceptance,discoveries,supplement_entries):769-836` (task bytes/filename/deterministic `task_filename:472-474` + `stable_task_id:467-469`, `_validate_task:684-716`, supplement bound-exactly-once `:819-835`), `_supplement_entries_for_package(...,implementation_sha=None,screening_acceptance,discoveries):379-410` + `validate_evidence_authority_supplement(...,implementation_sha=None,…):212-324` State-free branch (`:260-271` loads screening/discovery without impl SHA when provided), `task_authority_sources(repo_root,task,package):413-446`, `_screening_acceptance_digest:482-487`, `_evidence_result_set_digest:1152-1156`, `_view_set_digest:1494-1495`, `_check_evidence_acceptance_results_content:1216-1253`, `_check_views_acceptance_rows_content:1286-1319`, `_check_ledger_rows_content:1658-1723`, `_check_completeness_result_content:1804-1912`, `_validate_evidence_package_basis_content:839-895`, `_validate_evidence_acceptance_content:1255-1283`, `_validate_edition_views_acceptance_content:1322-1349`, `_validate_materiality_ledger_content:1725-1768`, `_validate_completeness_content:1915-1941`, `survey_completeness_v2._validate_obligation_shape:50-78`, `_thematic_closure_errors:81-142`, `_check_profile_completeness_extra_content:145-238`, `_validate_profile_completeness_content:241-262`, `screening._validate_screening_acceptance_content` + `_resolve_effective_discovery_basis_content` (session-root, no State), `validate_evidence_card:965-…` (pure card/shape/basis/role checks; `repo_root` optional for source-type map), `validate_edition_view:1437-1491`.
- Digest/dirname rules preserved verbatim: `result_set_sha256 = sha256_object({package_sha256, results sorted by evidence_task_id})`, `run_dir = accepted_root / result_set_sha256`, `acceptance_path = run_dir / evidence-accepted.json` (+ `package.json`, `tasks/`, `results/` exact copies); `view_set_sha256 = sha256_object(rows sorted by evidence_task_id)`, `run_dir = accepted_root / view_set_sha256`, `acceptance_path = run_dir / edition-views-accepted.json` (+ `views/`); `_exact_regular_files:449-464` (no symlinks, files-only, exact set); task/view filename determinism (`task_filename`/`view_filename`); acceptance idempotent-iff-revalidates else refuse-incomplete (`accept_evidence_results:1190-1194`, `accept_edition_views:1532-1538` logic, reused by HIGH writers with R roots + State-free revalidation).

### 4.2 State-bound (old public behavior intact — HIGH/normal paths keep calling these unchanged)

`validate_evidence_package_basis:898-946` (pure + `verify_state_basis:959` + state-SHA drift + screening-with-impl-SHA), `validate_screening_acceptance:490-536` + `screening.validate_package_basis` (with `verify_state_basis`), `validate_evidence_acceptance:1412-1434`, `validate_edition_views_acceptance:1555-1577`, `validate_materiality_ledger:1771-1794`, `validate_completeness:1944-…` / `validate_profile_completeness:265-290` (with impl SHA), `accept_evidence_results:1159-1213`, `accept_edition_views:1498-1552`, `prepare_evidence_package:539-681` (with `verify_state_basis:550` + `state_path` equality `:557`), `build_materiality_ledger:1579-1655`, `run_evidence_v2_interactive.run:586-774` (canonical Ledger/Completeness producer, `CANDIDATES_NORMALIZED:602`, refuse-overwrite `:715-732`), `write_materiality_ledger:1797-1801` (refuse-if-exists).

Wrapper delegation (implementation scope, behavior-preserving): refactor each State-bound public func to call its §4.1 pure core first, then the State-bound suffix (State load / `verify_state_basis` / impl-SHA screening) — no predicate weakened, no call-site-only “detached reuse”. New DM022 code calls **only** §4.1 cores + new HIGH exclusive writers below.

### 4.3 Exclusive writers (HIGH-owned, versioned-R only, no canonical overwrite)

For each R output, HIGH performs: `O_CREAT|O_EXCL` exclusive create of `run_dir` + files (or `core.write_json` equivalent under held guard + pre-existence check — exact primitive owned by C §4.1, referenced here), copy exact bytes (`shutil.copy2`-equivalent + re-hash), `schema_gate.validate_instance` + State-free `_validate_*_content` revalidation, post-write `sha256_file` + `byte_count` + `st_dev/st_ino` capture into manifest/proof. Canonical `source_root/materiality-ledger-v2.json` / `profile-completeness-v2.json` are **never** opened for write by these writers; `write_materiality_ledger(canonical)` / canonical `core.write_json` remain refused paths in supersession mode (C §4.2 row). LOW never writes R outputs directly; it returns in-memory dicts/bytes or writes only to HIGH-owned temp staging passed as `Path` args (caller-owned, exclusive).

---

## 5. LOW public API takes PATHS (Finding 3)

**Module (ROOT-preferred functional): `scripts/survey_research_authority_v2.py`** — typed checkpoint/4-ref proof, no `agent`/`currentState`/`HIGH` calls. Top-level imports **only** `core`, `schema_gate` (leaf). Every `evidence/screening/completeness/discovery/agent` access is **function-local import + pure-core extraction** (avoids the real `evidence(top:21)→screening(top)→agent(function-local: screening:465,480)` chain; actual call graph, not a name ban).

Public LOW entries (PATHS-only; derive context internally from pinned source/COPY/previous-checkpoint; never accept caller-verified dicts):

```python
def load_revision_request(repo_root: Path, request_path: Path) -> dict[str, Any]
  # _repo_file + sha256_file + schema_gate.load_and_validate_json(request_path, dm022-revision-request schema).
  # Returns trusted request dict (internal). No State.
def derive_before_context(repo_root: Path, request_path: Path, before_copy_path: Path, previous_checkpoint_path: Path) -> dict[str, Any]
  # Loads + re-hashes: before-State COPY, Profile, Discovery JSONL, Screening acceptance (+package), previous checkpoint record + its 4 artifacts.
  # Verifies: COPY bytes == request.before_state.sha256, previous checkpoint issue/membership/artifact SHAs, old completeness available for dim/description checks (§11).
  # Returns internal context {profile_path, discovery_path, screening_acceptance_path, previous_checkpoint, old_ledger, old_completeness, ...}. No State, no impl SHA.
def build_revision_package_from_paths(repo_root: Path, request_path: Path, before_copy_path: Path, output_dir: Path) -> Path
  # Derives before_context internally, then private pure _build_package_in_memory(...) using §4.1 cores (stable_task_id/task_filename, supplement binding, basis with canonical LIVE state_path + before state_sha per §3).
  # Writes ONLY to caller-owned output_dir (HIGH-owned R staging, exclusive). Returns package.json PATH.
def build_revision_cards_views_from_paths(repo_root: Path, package_path: Path, request_path: Path, results_dir: Path, views_dir: Path) -> tuple[Path, Path]
  # Loads package + request internally; validates per-task authority via task_authority_sources (function-local); builds + validates cards/views via validate_evidence_card/validate_edition_view (pure).
def accept_revision_evidence_views_from_paths(repo_root: Path, package_path: Path, results_dir: Path, views_dir: Path, profile_path: Path, evidence_accepted_root: Path, views_accepted_root: Path) -> tuple[Path, Path]
  # State-free accept: recomputes _evidence_result_set_digest/_view_set_digest, exclusive-creates run_dirs under the given R roots, copies bytes, validates via _validate_*_content. No State-bound acceptors.
def build_versioned_ledger_from_paths(repo_root: Path, profile_path: Path, discovery_path: Path, screening_acceptance_path: Path, evidence_acceptance_path: Path, views_acceptance_path: Path) -> dict[str, Any]
  # Pure _check_ledger_rows_content over internally loaded inputs. Caller (HIGH) writes via exclusive writer. No build_materiality_ledger State-bound call.
def build_versioned_completeness_from_paths(repo_root: Path, profile_path: Path, discovery_path: Path, screening_acceptance_path: Path, evidence_acceptance_path: Path, views_acceptance_path: Path, ledger_path: Path, request_path: Path, old_completeness_path: Path) -> dict[str, Any]
  # Union builder per §11 (full explicit rows, dim/description verified vs old_completeness_path) + _check_completeness_result_content + _check_profile_completeness_extra_content. No _build_completeness initial-only call.
def prove_revision_from_paths(repo_root: Path, revision_manifest_path: Path, decision_path: Path, before_copy_path: Path) -> Path
  # Loads manifest + decision + before context internally; re-hashes every SizedRef/NamedRef; runs §4.1 _validate_*_content family over R outputs; checks affected/unaffected per §10; emits proof file PATH (exclusive). No caller ledger/completeness/expectations dicts.
def check_supersession_record_from_paths(repo_root: Path, checkpoint_path: Path, report_path: Path, before_copy_path: Path) -> list[str]
  # Detached checkpoint validation: kind/reason/operation/producer_boundary/checkpoints/artifacts lineage + report/proof/decision FILE re-hash + named-digest recompute + artifact live re-hash against R (no State). [] == PASS (descriptive, not permission).
```

Private pure in-memory helpers (suffix `_in_memory`, dicts-in/dicts-out) may exist **only** behind the above PATHS-only entries after trusted internal load (e.g. `_build_package_in_memory`, `_compare_ledgers_in_memory`). They are never public authority.

---

## 6. Pre-adoption report vs checkpoint (Finding 4 — no cycle)

- **Pre-adoption report** (`schemas/dm022-preadoption-report-v2.schema.json`, §9): refs **request + candidate manifest + proof + decision + before-COPY + all-4-artifacts (proposed R refs)**, actual `operation={from:EVIDENCE_REVIEWED,to:EVIDENCE_REVIEWED}` + `producer_boundary={from:CANDIDATES_NORMALIZED,to:EVIDENCE_REVIEWED}`, current tools/work-ref (`repository_commit_sha`, `tree_sha`, `orchestrator_version`, `contract` 8 fields, `recorded_at`, `executor`), `affected_ids`, `mechanical_projections[]`, `validations[]` (DETERMINISTIC proof row only). Contains **NO** `checkpointRef`, **NO** `afterStateHash`/`expectedAfterState`, **NO** `guard hash` (guard existence/phase may be noted descriptively as `guard_claimed: bool` + `guard_path` string for coordination, never a hash authority).
- **Checkpoint** (`schemas/dm022-supersession-checkpoint-v2.schema.json`, §9): refs **completed report** (`report: SizedRef`), plus `proof SizedRef`, `decision SizedRef`, `request SizedRef`, `before_state SizedRef + before_checkpoint triple + parent/anchor + supersedes + revision_id + R + retention_plan SizedRef + contract + implementation + profile + executor/recorded_at + checkpoint_sha256`. Checkpoint validation requires the report (report exists first). Report never requires the checkpoint. One-way.
- **Optional POST completion receipt** (`schemas/dm022-completion-receipt-v2.schema.json`, §9; C coordinates slot/guard details): may bind `checkpoint SizedRef + derived expectedAfterState SizedRef + slot inventory + guard release observation + postread result`. The checkpoint **never back-references** it. It is readback/resume evidence, not checkpoint-validation input.
- Status bools (`triplet_match`, `lineage_match`, `proof_pass`, `retention_sealed`, `guard_held_by_self`) are **descriptive recomputed observations** (re-derive on every check from FILE re-hashes + digest recomputes + State re-read). They confer no permission; HIGH acts only after re-deriving them + LIVE `validate_agent_state` + guard-holder identity match.

---

## 7. Split public API — prepare → decision → adopt (Finding 5)

**Module (ROOT-preferred functional): `scripts/survey_prearchitecture_acceptance_v2.py`** — State/guard/writes/CLI. Top-level imports only `core`, `schema_gate`, LOW (`survey_research_authority_v2`); `agent/evidence/screening/completeness/discovery` imports are **function-local** inside each entry (avoids top-level cycle). No permanent DM-issue runner name. CLI (if any) is a thin `argparse` wrapper over these four entries (exact flags are implementation scope; no new caller flags/verified dicts).

```python
def prepare_revision(repo_root: Path, state_path: Path, request_path: Path, revision_id: str) -> Path
  # Pins S_before (LIVE validate_agent_state + §3 window + HEAD/tree/contract + live pins); captures immutable before snapshots within NEW owned R (no old-authority mutation);
  # generates truthful candidate under R via LOW PATHS-only builders (§5); emits immutable revision manifest M (R/revision-manifest.json, §9). No decision_path input. Returns M PATH.
def adopt_revision(repo_root: Path, state_path: Path, revision_path: Path, decision_path: Path) -> dict[str, Any]
  # Loads M + D (both already-existing immutable files; refuses future-ref: M FILE SHAs must equal D.before/after refs); seals/reverifies final retention inventory; claims + revalidates G (C-owned);
  # completes proof P + pre-adoption report RPT + checkpoint CP via LOW (PATHS-only); prevalidates S_expected; performs ONE known-byte State switch; checked-clears remaining exact old slots; postreads + verifies inventory; releases OWN G.
  # Returns {revision_path, manifest_path, proof_path, report_path, checkpoint_path, state_sha_before, state_sha_after}.
def resume_revision(repo_root: Path, state_path: Path, revision_path: Path) -> dict[str, Any]
  # Explicit resume only (C F8-F13): reloads M/record/graph/review/COPY/guard by revision_path; re-derives LIVE eligibility + guard-holder identity; may switch (S==B), clear-remaining (S==E), or return ALREADY_ACTIVE; else INDETERMINATE (preserve, no restore/delete/adopt).
def readback_revision(repo_root: Path, state_path: Path, revision_path: Path | None = None) -> dict[str, Any]
  # Read-only (guard-independent) + guarded-adoption check: validates LIVE State (if revision_path given, checks triplet == CP refs + 4-artifact live re-hash + lineage from retained COPY); returns descriptive {triplet_match, lineage_match, guard_state, slots_present/absent} (no permission token).
```

`prepare_*` never takes `decision_path`; `adopt_*` never generates candidate bytes (only validates already-existing M outputs + completes P/RPT/CP). `resume_*` never allocates/forks on collision (same `revision_id`/guard held by another → refuse). Names match C phases (`pin/generate/retain/claim/complete/prevalidate/switch/clear/postread/release/regen`) with `prepare≈pin+generate+retain-capture`, `adopt≈seal+claim+complete+prevalidate+switch+clear+postread+release`.

---

## 8. Typed refs (Finding 6)

Every file ref in request/manifest/proof/report/checkpoint/receipt/retention uses exactly one shape (`sha` in ROOT shorthand = `sha256` hex64 below, matching existing `artifactAuthority`/`namedAuthority` key `sha256`):

- `ArtifactRef = {path: repo-relative normalized string (no .., no absolute, no backslash, no symlink traversal; resolved stays under repo_root), sha256: ^[0-9a-f]{64}$}` — used for checkpoint provenance / State refs / `production_state`/`production_profile` bindings (matches `artifactAuthority`).
- `SizedRef = {path, sha256, byte_count: integer ≥1 (== stat().st_size)}` — used for every file with bytes (request, manifest, package/tasks/cards/views, supplement, Raw, acceptances, versioned ledger/completeness, proof, report, decision, retention plan/COPYs). `sha256 == sha256_file(path)` re-hashed on every load.
- `NamedRef = {name, path, sha256}` — used **only** for checkpoint `artifacts[]` (matches `namedAuthority`; `name` enum per declaring schema, e.g. `evidence-acceptance|edition-views-acceptance|materiality-ledger|profile-completeness`).

Tagged `kind`/enum variants appear **only** where the declaring schema states them (e.g. `operation.from/to`, `producer_boundary.from/to`, `checkpoints[]`, `artifacts[].name`, `materiality.status`, `overall_status`, guard `phase` owned by C). No generic `kind` on every ref; no bare `object`/`...`/`CHECKED` placeholders; no `{path,sha,byte_count,kind}` generic. Every duplicate SHA states equality explicitly (e.g. `ledger.basis.evidence_acceptance_sha256 == sha256_file(R evidence-accepted.json) == proof.proposed.evidence_acceptance.sha256`).

---

## 9. Literal schemas + digests + modules/imports (Finding 7)

### 9.1 Ref $defs (repeated literally in each NEW schema; no cross-file $ref cycle)

```json
{"$defs": {
  "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
  "gitsha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
  "ArtifactRef": {"type": "object", "additionalProperties": false, "required": ["path", "sha256"], "properties": {"path": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}}},
  "SizedRef": {"type": "object", "additionalProperties": false, "required": ["path", "sha256", "byte_count"], "properties": {"path": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}, "byte_count": {"type": "integer", "minimum": 1}}},
  "NamedRef": {"type": "object", "additionalProperties": false, "required": ["name", "path", "sha256"], "properties": {"name": {"type": "string", "minLength": 1}, "path": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}}}
}}
```

`path` safety (all schemas): `path` must satisfy `core.repo_local_path` semantics (relative, no `..`, no absolute, no `\`; resolved stays under `repo_root`; no symlink traversal via `_repo_file` semantics). `sha256 == sha256_file(path)`; `byte_count == stat().st_size` (SizedRef only).

### 9.2 Digest convention (named, project-consistent; FILE distinct)

- Content digest: `<thing>_sha256 = sha256_object(canonical JSON of all sibling fields EXCEPT itself, sort_keys=True, separators=(",",":"))` — same function as `core.sha256_object:163-165`. Examples: `revision_proof_sha256`, `preadoption_report_sha256`, `supersession_checkpoint_sha256`. Verified by recompute-excluding-self.
- FILE SHA: `sha256_file(path)` recorded in the referencing `SizedRef/NamedRef/ArtifactRef` (`sha256` key). Distinct from the content digest above (content digest binds logical body; FILE SHA binds exact bytes including formatting/newline). Both checked.
- No generic `SELF` object/field; no bare `{"contract": object}` — `contract` is always the literal 8-field shape below; no `...`.

Literal `contract` (all schemas that carry it):

```json
"contract": {"type": "object", "additionalProperties": false, "required": ["pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version", "quality_contract_sha256", "research_profile_version", "research_profile_sha256", "publication_profile_version", "publication_profile_sha256"], "properties": {"pipeline_contract_version": {"type": "string", "minLength": 1}, "pipeline_contract_sha256": {"$ref": "#/$defs/sha256"}, "quality_contract_version": {"type": "string", "minLength": 1}, "quality_contract_sha256": {"$ref": "#/$defs/sha256"}, "research_profile_version": {"type": "string", "minLength": 1}, "research_profile_sha256": {"$ref": "#/$defs/sha256"}, "publication_profile_version": {"type": "string", "minLength": 1}, "publication_profile_sha256": {"$ref": "#/$defs/sha256"}}}
```

Literal `implementation`: `{"type":"object","additionalProperties":false,"required":["repository_commit_sha","orchestrator_version"],"properties":{"repository_commit_sha":{"$ref":"#/$defs/gitsha"},"orchestrator_version":{"type":"string","minLength":1}}}`.

### 9.3 `schemas/dm022-revision-request-v2.schema.json` (NEW, required)

```json
{"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.invalid/schemas/dm022-revision-request-v2.schema.json", "title": "DM022 revision request", "type": "object", "additionalProperties": false,
 "required": ["schema_version", "issue_id", "revision_id", "research_profile", "before_state", "before_checkpoint", "affected_ids", "records", "completeness", "runner", "tool_pins"],
 "properties": {
  "schema_version": {"const": "2.0-rc1"}, "issue_id": {"type": "string", "minLength": 1},
  "revision_id": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"},
  "research_profile": {"enum": ["WEEKLY", "THEMATIC"]},
  "before_state": {"$ref": "#/$defs/SizedRef"},
  "before_checkpoint": {"type": "object", "additionalProperties": false, "required": ["evidence", "materiality", "completeness"], "properties": {"evidence": {"$ref": "#/$defs/ArtifactRef"}, "materiality": {"$ref": "#/$defs/ArtifactRef"}, "completeness": {"$ref": "#/$defs/ArtifactRef"}}},
  "affected_ids": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
  "supplement_manifest": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/SizedRef"}]},
  "records": {"type": "array", "minItems": 1, "items": {"type": "object"}},
  "completeness": {"type": "object", "additionalProperties": false, "required": ["obligations"], "properties": {"obligations": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/fullObligation"}}}},
  "runner": {"type": "object", "additionalProperties": false, "required": ["provider", "model", "invocation", "generated_at"], "properties": {"provider": {"type": "string", "minLength": 1}, "model": {"type": "string", "minLength": 1}, "invocation": {"type": "string", "minLength": 1}, "generated_at": {"type": "string", "format": "date-time"}}},
  "tool_pins": {"type": "object", "additionalProperties": false, "required": ["repository_commit_sha", "orchestrator_version", "contract"], "properties": {"repository_commit_sha": {"$ref": "#/$defs/gitsha"}, "orchestrator_version": {"type": "string", "minLength": 1}, "contract": {"type": "object", "additionalProperties": false, "required": ["pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version", "quality_contract_sha256", "research_profile_version", "research_profile_sha256", "publication_profile_version", "publication_profile_sha256"], "properties": {"pipeline_contract_version": {"type": "string", "minLength": 1}, "pipeline_contract_sha256": {"$ref": "#/$defs/sha256"}, "quality_contract_version": {"type": "string", "minLength": 1}, "quality_contract_sha256": {"$ref": "#/$defs/sha256"}, "research_profile_version": {"type": "string", "minLength": 1}, "research_profile_sha256": {"$ref": "#/$defs/sha256"}, "publication_profile_version": {"type": "string", "minLength": 1}, "publication_profile_sha256": {"$ref": "#/$defs/sha256"}}}}
 },
 "allOf": [
  {"if": {"properties": {"research_profile": {"const": "THEMATIC"}}}, "then": {"properties": {"completeness": {"required": ["closure"]}}, "required": ["completeness"]}},
  {"if": {"properties": {"research_profile": {"const": "WEEKLY"}}}, "then": {"not": {"required": ["thematicOnly"]}}}
 ],
 "$defs": {"sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "gitsha": {"type": "string", "pattern": "^[0-9a-f]{40}$"}, "ArtifactRef": {"type": "object", "additionalProperties": false, "required": ["path", "sha256"], "properties": {"path": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}}}, "SizedRef": {"type": "object", "additionalProperties": false, "required": ["path", "sha256", "byte_count"], "properties": {"path": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}, "byte_count": {"type": "integer", "minimum": 1}}}, "fullObligation": {"type": "object", "additionalProperties": false, "required": ["obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"], "properties": {"obligation_id": {"type": "string", "minLength": 1}, "dimension": {"type": "string", "minLength": 1}, "description": {"type": "string", "minLength": 1}, "status": {"enum": ["SATISFIED", "LIMITATION", "NEEDS_RESEARCH", "NOT_APPLICABLE"]}, "discovery_ids": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}}, "evidence_task_ids": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}}, "rationale": {"type": "string", "minLength": 1}}}}
```

Notes: `records[]` items are the exact per-Profile interactive shapes from `run_evidence_v2_interactive._validate_record:119-214` (COMMON + WEEKLY/THEMATIC fields, `source_bindings` iff multi-source); `completeness.obligations[]` are **full explicit rows** (all 7 keys, §11), not status-only; `supplement_manifest==null` iff no affected ID needs new Raw (else `SizedRef` to `evidence-authority-supplement-v2` manifest validated by `validate_evidence_authority_supplement`). `records` must cover exactly non-DROP DIDs; `affected_ids ⊆ non-DROP` (checked, not trusted).

### 9.4 `schemas/dm022-revision-manifest-v2.schema.json` (NEW, required — prepare output)

Immutable prepare inventory. **No embedded self-digest** (FILE SHA is identity, avoids cycle).

Required: `schema_version, issue_id, revision_id, R, request(SizedRef), before_state(SizedRef), before_checkpoint({evidence,materiality,completeness: ArtifactRef}), retention_snapshots[] (each {slot, source_rel, copy_rel, present: bool, source_sha256|null, copy_sha256|null, byte_count|null} with present==false ⇒ SHAs null), candidate_outputs {package(SizedRef), tasks[](SizedRef), cards[](SizedRef), views[](SizedRef), evidence_acceptance(SizedRef), views_acceptance(SizedRef), ledger(SizedRef), completeness(SizedRef), supplement_manifest(SizedRef|null)}, tool_pins (same literal shape as request), recorded_at, executor`. `additionalProperties:false` throughout; `if research_profile==THEMATIC then candidate ledger closure fields present` is validated downstream (not here). Every `SizedRef` re-hashed at adopt.

### 9.5 `schemas/dm022-revision-proof-v2.schema.json` (NEW, required — deterministic proof)

Required: `schema_version, issue_id, revision_id, R, manifest(SizedRef), decision(SizedRef), before_state(SizedRef), proposed {package, evidence_acceptance, views_acceptance, ledger, completeness (all SizedRef), result_set_sha256, view_set_sha256 (both $defs/sha256), tasks/cards/views (SizedRef arrays)}`, `affected_ids[]`, `unaffected_comparison {rows_checked: integer≥0, mechanical_projections[]}`, `validations[] (each {check_id: string, kind: {const: DETERMINISTIC}, status: {const: PASS}, executor: string, result: SizedRef})`, `recorded_at, executor, revision_proof_sha256 ($defs/sha256)`. `mechanical_projections[]` items: `{field_path: string (actual schema path, e.g. materiality-ledger.basis.evidence_acceptance_sha256), old_sha256: $defs/sha256|null, new_sha256: $defs/sha256, reason: string}` — directory-prefix rules forbidden. `revision_proof_sha256 == sha256_object(all other top-level fields)` (recompute-excluding-self); every `SizedRef.sha256 == sha256_file(path)`.

### 9.6 `schemas/dm022-preadoption-report-v2.schema.json` (NEW, required — pre-adoption, no checkpoint/after/guard refs)

Required: `schema_version, issue_id, revision_id, R, request(SizedRef), manifest(SizedRef), proof(SizedRef incl. revision_proof_sha256 equality), decision(SizedRef), before_state(SizedRef), before_checkpoint({evidence,materiality,completeness: ArtifactRef}), proposed_artifacts {evidence_acceptance, views_acceptance, ledger, completeness (SizedRef)}`, `operation {from_state: {const: EVIDENCE_REVIEWED}, to_state: {const: EVIDENCE_REVIEWED}}`, `producer_boundary {from_state: {const: CANDIDATES_NORMALIZED}, to_state: {const: EVIDENCE_REVIEWED}}`, `affected_ids[], mechanical_projections[] (copied from proof, no new reasons)`, `tool_pins (literal contract shape), work_ref {repository_commit_sha: gitsha, tree_sha: gitsha, contract (literal 8-field)}`, `recorded_at, executor, preadoption_report_sha256`. **Forbids** `checkpoint`, `expectedAfterState`, `guard` hash fields (`additionalProperties:false` enforces; `guard_claimed: {type: boolean}` + `guard_path: {type: string}` descriptive coordination allowed, never a hash authority). `preadoption_report_sha256 == sha256_object(body-minus-self)`.

### 9.7 `schemas/dm022-supersession-checkpoint-v2.schema.json` (NEW, required — typed record)

Required: `schema_version=="2.0-rc1", kind: {const: PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1}, reason: {const: REVIEWED_ACCEPTED_UPSTREAM_CORRECTION}, issue_id, operation (same EVIDENCE→EVIDENCE consts), producer_boundary (same CANDIDATES→EVIDENCE consts), checkpoints: {const array exactly ["evidence","materiality","completeness"] via contains-all + min/maxItems 3 + uniqueItems}, artifacts: {minItems 4, maxItems 4, items NamedRef + contains each name in {evidence-acceptance, edition-views-acceptance, materiality-ledger, profile-completeness}}`, `before_state(SizedRef), before_checkpoint({evidence,materiality,completeness: ArtifactRef} same-record old refs), parent_checkpoint(ArtifactRef), original_anchor(ArtifactRef), supersedes[] (each {path, sha256, revision_id})`, `revision_id, R (string), request(SizedRef), retention_plan(SizedRef), proof(SizedRef), decision(SizedRef), report(SizedRef to completed pre-adoption report), contract (literal 8-field), implementation (literal 2-field), profile(ArtifactRef), executor, recorded_at, supersession_checkpoint_sha256`. `reviews[]`: `minItems 1, maxItems 1`, sole item `{check_id: {const: DM022_SUPERSESSION_PROOF}, kind: {const: DETERMINISTIC}, status: {const: PASS}, executor, evidence: string, result: SizedRef (== proof)}` — **no** `CORE_STAGE_CONTRACT` row, **no** `AGENT_RESEARCH` decision row (decision is the separate `decision` field, §12). `additionalProperties:false`. Conditionals: `supersedes==[] iff parent_checkpoint==original_anchor` (`if/then` with `properties` + `required`); `checkpoints` order-insensitive set check via `allOf contains`. `supersession_checkpoint_sha256 == sha256_object(body-minus-self)`; every `artifacts[].sha256 == sha256_file(artifacts[].path)`.

### 9.8 `schemas/dm022-completion-receipt-v2.schema.json` (NEW, optional POST only)

Required: `schema_version, issue_id, revision_id, checkpoint(SizedRef to completed CP), expected_after_state(SizedRef), slot_inventory {present[], absent[]}, guard_release {guard_path: string, released_by: string, released_at: date-time, holder_match: boolean}, postread {triplet_match: boolean, artifacts_rehashed: boolean}, recorded_at, completion_receipt_sha256`. The checkpoint **never** references this file. Descriptive bools only.

Guard/retention/completion embedded details (guard file record, retention manifest rows, F-row oracles, HEAD/tree predicate, slot writer/ownership/faults) are **owned by C**; R2 carries them only as `SizedRef` + `phase`/path strings for coordination, with exact shapes deferred to C’s binding return. Module/file budget justification: 2 modules (functional LOW/HIGH per ROOT) + 5 required schemas (request/manifest/proof/pre-adoption-report/checkpoint — each a distinct stage/type; merging manifest↔proof would force decision to bind a future ref; merging proof↔report would force report to contain its own digest input; merging report↔checkpoint would recreate the Finding-4 cycle) + 1 optional POST receipt (readback-only, never validation input). No further files without explicit ROOT justification.

Function-local import discipline (all new code): top-level `from __future__ import annotations`, stdlib, `core`, `schema_gate`, LOW-imports-HIGH? No — HIGH top-level imports LOW only (`from scripts import survey_research_authority_v2 as low`). All `evidence/screening/completeness/discovery/agent/agent_tool` accesses are **function-local** (`from scripts import survey_evidence_v2 as evidence` inside the needing function, same for `screening/completeness/agent`), then call only §4.1 pure cores (LOW) or `agent.validate_agent_state` / `core.repository_commit_sha` (HIGH eligibility). This avoids materializing the real `evidence(top)→screening(top)→agent(fn-local)` chain at import time.

---

## 10. Changed-package mechanics (Finding 8 — exact fields, no invention)

Source schemas (proof-copy): `evidence-v2-run-package.schema.json` (required `schema_version,issue_id,research_profile,basis,prompt,contracts,tasks,expected_outputs,rules` + optional `authority_supplement`; `basis` required `profile_path/profile_sha256,state_path/state_sha256,discovery_path/discovery_sha256,screening_acceptance_path/screening_acceptance_sha256`; `prompt=={path: const config/prompts/evidence-verification-v2.md, sha256}`; `contracts.{run_package,task,card}(+supplement iff supplement)` const paths + SHAs; `tasks[]` required `evidence_task_id,path ^tasks/task-[0-9a-f]{20}\.json$,sha256,discovery_ids[1]` + optional `authority_supplement_source_ids[] ^supplement-src-[0-9a-f]{16}$`; `expected_outputs=={one_result_per_task:true,filename_rule:same-basename-as-task}`), `evidence-v2-card.schema.json` (required `CARD_KEYS:32-36`; `basis` required `task_sha256,screening_acceptance_sha256,prompt_sha256,result_contract_sha256`), `edition-evidence-view.schema.json` (required `evidence_task_id,evidence_sha256,materiality,scope_dimensions,profile_annotations`), `materiality-ledger.schema.json` (required `schema_version,issue_id,research_profile,basis,rows`; `basis` required **exactly** `production_profile_sha256,discovery_sha256,screening_acceptance_sha256,evidence_acceptance_sha256,edition_views_acceptance_sha256,evidence_set_sha256,edition_view_set_sha256` — **no `self_digest`**), `profile-completeness-result.schema.json` (required `basis{production_profile_sha256,materiality_ledger_sha256},overall_status,obligations,residual_limitations,closure`).

Mechanical derivation (each independently recomputed, listed per-field in `mechanical_projections[]`; no arbitrary reason):

- Package: `basis.state_path` same string (canonical LIVE path, §3); `basis.state_sha256` = new before (differs from old package `state_sha` iff State bytes advanced — expected, listed as `evidence-run-package.basis.state_sha256` with `reason: new-before-State bytes`); `tasks[].sha256` differs **only** for affected `evidence_task_id` (task bytes changed via new `authority_supplement_source_ids`); package FILE SHA + `tasks[]` order/sort unchanged. `basis.profile/discovery/screening` SHAs, `prompt/contracts` SHAs must equal current files (if HEAD tool files unchanged, equal old; if changed, listed with `reason: current-tool contract bytes` + HEAD predicate — no silent migration).
- Cards: `basis.task_sha256` differs **iff** task bytes changed (affected only). Unchanged `cardSHA` held **only if** `task_sha256 + screening_acceptance_sha256 + prompt_sha256 + result_contract_sha256` all equal old **and** all semantic fields equal (FILE SHA equality is the check). Affected cards: `status/entities/artifact/temporal.events/sources/claims/metrics/limitations/verification` may change per §7.3 R1 (retained); `issue_id/evidence_task_id` immutable. No projection may hold an old card SHA while changing any `basis.*` field.
- Views: `evidence_sha256 == sha256_file(card file)` (binding). Unchanged `viewSHA` held **only if** bound `cardSHA` unchanged **and** `materiality/scope_dimensions/profile_annotations` equal. Affected views change `evidence_sha256/materiality/scope_dimensions/annotations` per R1 §7.3; `issue_id/research_profile/evidence_task_id` immutable.
- Acceptances: `evidence-accepted.json package_sha256` (new package FILE SHA), `result_set_sha256 = sha256_object({package_sha256, results sorted})` (recomputed), `results[].sha256` (unaffected equal, affected new), dirname `== result_set_sha256`; `edition-views-accepted.json evidence_acceptance_sha256` (new evidence FILE SHA), `view_set_sha256` (recomputed), `views[].view_sha256` (unaffected equal iff card unchanged). Listed as `evidence-acceptance.result_set_sha256`, `...package_sha256`, etc.
- Ledger: `basis.evidence_acceptance_sha256/edition_views_acceptance_sha256/evidence_set_sha256/edition_view_set_sha256` change (new FILE/digest SHAs — the **only** permitted basis exclusions, each with recomputed values); `basis.production_profile/discovery/screening_acceptance` equal (Profile/Discovery/Screening frozen). Rows: unaffected DIDs full 8-field equality (`discovery_id,origin,screening_decision,downstream_disposition,evidence_task_ids,evidence_view_statuses,duplicate_group,rationale`); affected DIDs only `downstream_disposition/evidence_view_statuses/rationale` may change (`evidence_task_ids` same stable IDs, `discovery_id/origin/screening_decision/duplicate_group` immutable).
- Completeness: `basis.materiality_ledger_sha256` changes (new ledger FILE SHA — only permitted basis exclusion); `basis.production_profile_sha256` equal. Obligations not referencing affected DIDs/tasks: full 7-field equality. Obligations referencing affected: only `status/rationale` (and derived `evidence_task_ids` linkage, same IDs) may change; `obligation_id/dimension/description/discovery_ids` immutable and verified vs old (§11). `overall_status/residual_limitations/closure` re-derived via unchanged rules (listed as derived, not excluded).

---

## 11. DM017 union with full explicit rows (Finding 9)

Request `completeness.obligations[]` carries **full explicit rows** (all 7 `OBLIGATION_KEYS: survey_completeness_v2.py:25-35` — `obligation_id,dimension,description,status,discovery_ids,evidence_task_ids,rationale`), **including** named-only `dimension/description` where the ID is absent from `profile.research_scope.initial_obligations`. LOW (PATHS-only, §5):

- derives the required ID set = Profile-initial IDs ∪ Discovery-named IDs (`provenance.obligation_ids` over all Discovery records from the pinned Discovery JSONL via `screening.read_jsonl`, same enumeration as `_check_profile_completeness_extra_content:213-236`);
- derives references: `discovery_ids` = declaring DIDs (sorted, per `named:213-220`), `evidence_task_ids` = via ledger rows (`ledger_task_by_discovery`, same as runner `_build_completeness:481-507` mapping but over the union, not initial-only);
- verifies **unchanged `dimension/description`** for every existing ID against the **old valid completeness** (loaded via `before_checkpoint.completeness` → old `profile-completeness-v2.json`, validated State-free): `new.dimension == old.dimension`, `new.description == old.description`; refuses invention from Profile for named-only IDs and refuses silent drops (`silently dropped …:209/223` errors preserved);
- validates the built result with the **unchanged** `survey_completeness_v2.validate_profile_completeness:265-290` + `schema_gate.validate_instance(..., profile-completeness-result.schema.json)` (never the incomplete `_build_completeness:471-507` / `_validate_completeness_input:217-258` initial-only path).

No new obligation IDs (Discovery frozen); any unknown ID in request vs old-union → refuse.

---

## 12. No new authority role / no genuine PASS (Finding 10)

- Existing `reviews[].kind` enum (`stage-checkpoint-v2.schema.json:74` — `DETERMINISTIC,AGENT_RESEARCH,AGENT_EDITORIAL,AGENT_VISUAL`) is reused **without** adding a new role. New checkpoint `reviews[]` contains **exactly one** row: `{check_id: DM022_SUPERSESSION_PROOF, kind: DETERMINISTIC, status: PASS, executor, evidence: string, result: SizedRef(== proof)}`. This is a local content-proof binding (recomputed digests + FILE re-hashes), not an approval.
- The supplied independent decision is bound as **`decision: SizedRef`** (FILE re-hash + `affected_ids ⊆ non-DROP` + Raw re-read + before/after SHA binding per R1 §6). Its reviewer metadata (`executor/recorded_at`) is informational; authority comes from file binding + LOW revalidation. It is **provided report data**, never a generic `{status:PASS}` dict, and the writer **generates no genuine PASS** (no Selection/Architecture/Human approval, no `approve_architecture`-equivalent, admit ≠ approval).

---

## 13. Import DAG + SHA acyclicity (updated)

```text
survey_research_authority_v2 (LOW leaf; top: core, schema_gate only; evidence/screening/completeness/discovery/agent via function-local + §4.1 pure extraction)
  ↑ (pure PATHS-only calls; no State/guard/HEAD)
survey_prearchitecture_acceptance_v2 (HIGH; top: core, schema_gate, LOW; agent/evidence/screening/completeness function-local in prepare/adopt/resume/readback)
  ↑ (no reverse imports; agent never imports LOW/HIGH at top)
survey_agent_control_v2 (Owner A; existing; new-kind branch calls LOW pure validators function-locally for detached checks)
```

SHA/data DAG (each node refs only prior SHAs; no self/future):

```text
(1) before snapshots in NEW R (S_before COPY + slot COPYs + present/absent inventory; no old-authority mutation)
 → (2) revision manifest M (refs (1) FILE SHAs; FILE SHA is M identity, no embedded self)
 → (3) external decision D (refs (1)+(2) FILE SHAs + Raw SHAs + allowlist; immutable file, no future ref)
 → (4) deterministic proof P (refs (1)+(2)+(3); revision_proof_sha256 = sha256_object(body-minus-self); FILE SHA distinct)
 → (5) pre-adoption report RPT (refs (1)+(2)+(3)+(4) + proposed 4-artifact R refs + operation/boundary + tools/workref; preadoption_report_sha256 = sha256_object(body-minus-self); NO checkpoint/afterState/guard-hash refs)
 → (6) checkpoint CP (refs completed (5)+(4)+(3)+(1) + retention plan + contract/impl/profile; supersession_checkpoint_sha256 = sha256_object(body-minus-self); reviews[] = sole DETERMINISTIC proof row)
 → (7) State triplet refs (three ArtifactRefs → same CP FILE SHA; State FILE SHA computed after write + postread verify_agent_state + same-record check)
 → (8) optional POST receipt (refs (6)+(7) + slot inventory + guard release; CP never backrefs)
```

Guard (C-owned, transient coordination) is claimed/revalidated between seal and CP completion and released after postread; HIGH checks it at entry/before-publish; unknown/mismatched/foreign fail closed. No second live pointer.

---

## 14. Owner A + exact producer funcs (arbitrary-R + stale-before handling)

Owner A = `scripts/survey_agent_control_v2.py` (existing; new-kind branch + `resolve_active_four_refs` returning same-record `{evidence,views,ledger,completeness}` with live re-hash; B2 table + `inventory.json` 28 rows define every caller disposition — referenced, not repeated).

Exact producer funcs (actual names, no invention) with R2 delegation:

- Versioned writes (HIGH exclusive, R roots only): same digest/dirname/copy/idempotent-iff-revalidates logic as `accept_evidence_results:1186-1212` / `accept_edition_views:1529-1552` but with `accepted_root=R/…` + State-free `_validate_*_content` revalidation (never State-bound `validate_*` on canonical paths); `write_materiality_ledger(R/…,ledger)` (same refuse-if-exists `:1797-1799` semantics on the R path); `core.write_json(R/profile-completeness-v2.json,result)` after `validate_profile_completeness` (State-free completeness path per §4.1 + union builder §11) + `schema_gate.validate_instance`; `build_evidence_authority_supplement(...,output_path=R/…supplement….json,supplement_id=…):327-376` (same `refusing to overwrite:342-343` + validate-then-unlink-on-failure `:363-375`).
- Narrow cores reused (§4.1 list verbatim); State-bound wrappers (`validate_evidence_package_basis`, `validate_screening_acceptance`, `validate_evidence_acceptance`, `validate_edition_views_acceptance`, `validate_materiality_ledger`, `validate_completeness/validate_profile_completeness`, `prepare_evidence_package`, `build_materiality_ledger`, `accept_*`) keep exact old behavior for normal paths (wrapper-delegation in implementation scope).
- Stale-before handling: every adopt/resume reloads pinned `S_before` COPY + R bytes + previous checkpoint and re-runs §4.1 State-free validators + `task_authority_sources` + `validate_evidence_card/view` + supplement binding + obligation union + closure derivation; LIVE State checked separately via `agent.validate_agent_state` + `core.repository_commit_sha`. `S==B→resume-may-switch`, `S==E→clear-remaining-or-ALREADY_ACTIVE`, else `INDETERMINATE` (preserve, no restore/delete/adopt; C F1–F13).

---

## 15. Ready vs BLOCKERS (honest — R2 does not claim MAP-complete)

**Ready by R2 (map-complete for B4/producer/schema/DAG surface):** §§2-14 (staging one-way DAG, basis-path fix, narrow primitives + delegation/exclusive writers, PATHS-only LOW, report/checkpoint cycle fix + POST receipt, split prepare/adopt/resume/readback API, three typed refs, literal schemas + named digests + functional modules + function-local imports, exact changed-package field mechanics, DM017 full-row union, no-new-role/no-PASS rule, updated import/SHA DAGs, Owner-A/producer/stale rules).

**Remaining BLOCKERS (code blocked until closed by owning returns + Astra + independent readiness review; must not be waived as “review later”):**

- B1: C seven-slot writer/ownership/fault oracles for slot 7 (audit `run:330-343` unguarded-today → successor 7-path preflight + caller-input vs generated-archive distinction + partial-run non-fabrication) — owned by C binding return.
- B2: per-caller R4-or-refuse implementation + post-acceptance tests for all 28 `inventory.json` rows (canonical Ledger/Completeness/Matrix/Selection + Draft/Synthesis/Reader/publication/operator/handoff/Gate/history + R1/editorial/renewal walkers) — owned by A map + code; R2 references, does not implement.
- C: guard file/record/claim/revalidate/release + every-producer check sites (incl. no-State-arg callers) + unknown/mismatched fail-closed + F1–F13 IO/resume oracles + HEAD/tree complete path set + artifact-only descendant enforcement + O/N oracle instantiation — owned by C binding return.
- Profile: DM016 supported-type allowlists per witness (no alias relabel; 10 absent Thematic types stay OPEN) + DM017 exact named-obligation rows + archived-HTML/retrieval-provenance + timestamp/event-meaning fields + INSPECT binding + unaffected-comparison + negative matrix — Profile/schema owners.
- Schema-owner binding: exact `check_id` strings (`DM022_SUPERSESSION_PROOF`), schema file placement/registration, `stage-checkpoint-v2.schema.json` strict branch text for `from==to==EVIDENCE_REVIEWED` + `producer_boundary` + same-triplet + new-report (no `CORE_STAGE_CONTRACT` forgery), `contract_identity`/`repository_commit_sha` pinning in `tool_pins/work_ref`.

If any required predicate/writer cannot be included without weakening, return the exact blocker and revisit A1-vs-A2 (decision §§9/11.4) — never implement a partially guarded A1.

---

*Task B R2. Preserves R1 unchanged. Bound to decision `a345bb95…` incl §11 + root §5 + both FINAL-BINDING reviews + C/A siblings. Proof-copy read-only; implementation blocked. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN.*
