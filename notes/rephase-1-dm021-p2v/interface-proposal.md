# DM021-P2V Phase A — concrete V1–V5 interface/helper/call-graph/field/snapshot/fixture return

2026-10-15 JST. General Phase A only. Read-only; no code/tests/fixtures/copies/restores/commits/network. Source is `source-binding.md` in this packet: actual detached `409b292…/8ce36998…` +16-file `5d2fde45/3833b14a/…` +84 caches, all16 ALL_MATCH, cache path-set equal, reconstruct `b385deb…` clean, contract `2ea1d98f…`. Fixed contract `outputs/rephase-1-dm021-current-authority-contract-decision.md`, mandatory Astra V1–V5 `notes/rephase-1-dm021-current-authority/astra-review-resolution.md`, independent §§0–16 (esp. §16) govern. This return is for Astra selection. No implementation until selection.

Selected delta (contract §2): **2A1M / 0 schema**:

- A `scripts/survey_editorial_current_authority_v2.py`
- M `scripts/survey_editorial_correction_proposal_v2.py` (private data factoring only)
- A `tests/test_survey_editorial_current_authority_v2.py`

No schemas/P2R/config/controller/Gate/publisher/receipt/CLI changes. Future composite 18 paths, 3M15A vs 409 (P1 module already added path); inherited 15 of current 16 remain byte-identical, P1 module changes deliberately, P2R module/schema/test unchanged. More paths require exact blocker + fresh scope. No `mode`/ignore-destination/caller `verified_set`/trusted token/context/alternate State bytes.

Public API (exact, contract §2):

```python
def observe_current_authority(root: str | Path, state_path: str | Path,
                              proposal_path: str | Path, manifest_path: str | Path,
                              scope_review_path: str | Path | None = None) -> dict[str, Any]: ...
```

Read-only observation, in-memory dict only, no writer/CLI/new persisted schema. No bearer/adoption permission.

---

## V1 — exact factoring / fixed completion proof

### V1.0 Actual P1 signatures read (candidate-relative, no imports)

`scripts/survey_editorial_correction_proposal_v2.py` (1830 lines, `5d2fde45`):

- `class _Collector` `:87–233`: `__init__(root)`, `rel(path)->str`, `safe(value,label)->Path` (lexical→alias→resolve→regular→read, `STABILITY_VIOLATION` on re-read mismatch), `pinned(ref,label)->str` (exact `{path,sha256}` + live-byte equality), `reverify()->None` (ancestor-alias + bytes + HEAD + config).
- `_resolve_tree_base(root_resolved,value,label)->Path` `:236–264`.
- `_tree_map(root,source_root,survey_root)->dict[str,str]` `:267–318` (full byte map, alias/FIFO refusal, `.git` excluded; **no empty-dir inventory** — see V3).
- `_check_proposal_id(proposal_id)->None` `:321–324`.
- `_eligibility(state)->None` `:327–342` (VALIDATED_DRAFT + approved Architecture + pending Preview without provenance + pending downstream + inactive exception).
- `_route_of(profile)->str` `:345–352` (THEMATIC+LONGFORM_SPECIAL → LONGFORM, WEEKLY+WEEKLY_MAGAZINE → WEEKLY).
- `_original_checkpoint(col,root,state)->tuple[dict,list]` `:355–377` (State-pinned `{path,sha256}`, identity/producer, 7-row shape, `{name,path,sha256}` rows).
- `_active_effective(col,root,cfg,state,original_rows)->tuple[dict,dict|None]` `:380–411` (`ACTIVE_PATH_REBIND` `:401–402`, superseded/preserved drift, ORIGINAAL fallback when no record, live-byte agreement).
- `_load_profile(col,state)->dict` `:414–428` (State-bound `{path,sha256}`, issue binding).
- `_derive(col,root,route,state_path,authored_value)->dict` `:431–445` (route loaders + `archive_path` pin, requires `surface/accepted_refs/archive_path/authored_path/profile/state`).
- `_canonical(route,surface)->bytes` `:448–451` (Longform `canonical_reader_bytes` vs Weekly `core.json_bytes`).
- `_build_graph(col,root,cfg,state,original_rows,effective,active_record,receipt,receipt_rel,gate_record,manuscript,bundle,pretex,state_rel,profile)->tuple[dict,list]` `:563–~1230` (mutable⇒COPY else KEEP `:597–599`, State node, checkpoint/effective edges, predecessor chain, manuscript/support, receipt outputs, bundle/pretex/authored mutables).
- `_retention_plan(col,graph,proposal_dir)->list[dict]` `:1231–1288`: `inputs=set(col.files)` `:1238`; live-input overlap `:1269–1270`; namespace overlap `:1271–1274`; duplicate-dest `:1275–1277`; **absent-required incl. dangling alias `:1278–1284`**.
- `_pipeline(col,root,state_path,new_authored_value,proposal_id,tree_entry,change_description=None)->dict` `:1291–1492`: returns `{proposal,proposed_canonical,before_canonical,graph,frozen,effective,original_rows,active_record,route,before_authored_rel,new_authored_rel,reader_rel,planned_reader_ref,proposal_dir}` `:1486–1492` — not `input_hashes`, not scope, not final receipt. Covers State/config/canonical `:1291–1321`, staged authoring `:1334–1338`, original/active `:1344–1349`, manuscript/Gate/receipt routing `:1351–1384`, derivation + `NO_EDITORIAL_CHANGE` `:1386–1391`, receipt/Gate/bundle/pre-TeX `:1393–1430`, graph/digests/retention `:1431–1438`, tree/reverify `:1439–1442`, proposal object `:1454–1485`.
- `_frozen_names_check(receipt,context)->None` `:1495–1503`; `_proposed_upstream_check(before,proposed)->None` `:1506–1525`.
- `_canonical_state_path(root,cfg,profile)->Path` `:1528–1533`.
- `_validated_state_profile_for_tree(col,root,state_path_value)->tuple[state,cfg,profile]` `:1536–1569` (strict authority BEFORE broad walk).
- `_final_full_receipt_recheck(col,root,result,label)->None` `:1572–1598` (actual route `validate_receipt` + `col.reverify()`).
- `prepare_proposal(root,state_path,authoring_path,proposal_id,change_description=None)->dict` `:1601–1632`: authority `:1616`, tree `:1617–1618`, pipeline `:1619–1620`, schema `:1621–1622`, final receipt after schema `:1624`, reverify + final tree `:1626–1631`.
- `_validate_scope(col,root,scope_review_value,proposal,state,profile)->str` `:1635–1695`: ordinary loader + digest binding, absent block → `REVIEW_REQUIRED` `:1668–1670`, `WITHIN_APPROVED_AUTHORITY` + exact before/after/upstream + substantive `EDITORIAL_CORRECTION_SCOPE` PASS `:1671–1695`.
- `validate_proposal(root,state_path,proposal_path,scope_review_path=None)->dict` `:1698–1830`: pins config/proposal `:1710–1723`, strict authority before canonical dir/tree `:1728`, canonical dir compare `:1729–1741`, layout/staged `:1743–1771`, description/path prechecks `:1756–1769`, broad walk only after `:1770–1771`, pipeline `:1774–1775`, ALL-field comparisons `:1778–1801`, State/Profile reload `:1802–1808`, optional scope `:1809–1812`, final FULL receipt AFTER scope `:1813–1814`, `col.reverify` + final tree `:1816–1821`, return supplied UNCHANGED + `input_hashes` + `measured` `:1823–1830`.
- Constants `:44–54`: `PROPOSAL_SCHEMA`, `PROPOSAL_ID_RE`, `PROPOSAL_FILES=("authoring-input.json","reader-surface-input-v2.json","proposal.json")`, `SCOPE_VERSION/SCOPE_CHECK_ID`, `RESULT_REQUIRED="REVIEW_REQUIRED"`, `RESULT_BOUND="REVIEW_BOUND_PROPOSAL"`.

`scripts/survey_editorial_retention_v2.py` (2080 lines, `3833b14a`): `verify_retention(root,proposal_path,manifest_path)->dict` `:1731–2080` (no P1/Git/HEAD; header/basis/proposed `:1764–1777`, ordered plan `:1778–1826`, I1 chain `:1827–1843`, provisional dest `:1844–1860`, retained State/Profile `:1860–1900`, canonical dir/manifest `:1901–1915`, dest recomputation `:1916–1925`, inventory + COPY/KEEP rehash + staged refs `:1926–1988`, `capture_inputs` historical `:1989–2019` with mandatory P2R deps `:2017–2019`, canonical bytes `:2041–2042`, final re-inventory `:2043–2056`, reverify + close `:2056–2066`, returns `{result:RETAINED_SET_VERIFIED,manifest_sha256,proposal_sha256,checked:{copy_files,keep_refs,staged_refs:2}}`). Reusable primitives: `_Session` `:175–521` (`safe_read`, `repinned`, `reverify`, `_close_all` `:243–278` primary-preserving), `_control_paths` `:599–622`, `_snapshot_expanded` `:667–756` (files+dirs incl. empty+sizes), `_retained_inventory` `:759–817`, `_retained_expected_sets` `:829–848`, `_expected_retained_dest` `:825–826`, `_check_canonical_bytes` `:592–598`.

Route predicates (verified by read): Longform `verify_tool_basis:519–582`, Weekly `_verify_head_bytes:577–631` (ancestor + exact control/style/contract + dirty/untracked refusal + closure vs commit+HEAD; uncommitted overlay refuses).

### V1.1 Proposed private factoring (M file only, no public signature/schema change)

Data-only = no readiness/permission result; helpers may perform read-only I/O, not mathematically pure. Private helpers are not a capability boundary; fixed public entry points enforce completions. No enum/bool/mode/`verified_set`/caller token.

In M `scripts/survey_editorial_correction_proposal_v2.py`, add exactly:

1. `_retention_rows_for_graph(col: _Collector, graph: dict[str,Any], proposal_dir: str) -> list[dict[str,Any]]`
   - Extract of current `:1241–1277` verbatim: deterministic row/path/policy construction + traversal/alias/overlap/conflict checks (`RETENTION_DIR_TRAVERSAL/DEST_TRAVERSAL/ESCAPE/ALIAS/OVERLAP/CONFLICT`), `inputs=set(col.files)` snapshot at entry, namespace overlap, duplicate-dest. **Excludes** `:1278–1284` absent check. Returns sorted rows.
2. `_require_retention_dests_absent(col: _Collector, rows: list[dict[str,Any]]) -> None`
   - Only current `:1278–1284` per COPY row: `(col.root/dest).is_symlink() or exists()` → `RETENTION_DEST_CONFLICT` (dangling alias refuses). No other logic.
3. `_retention_plan(col,graph,proposal_dir)` — keep name/signature; body becomes `rows=_retention_rows_for_graph(...); _require_retention_dests_absent(col,rows); return rows`. Byte-identical behavior for all existing P1 callers. No caller flag.
4. `_pipeline_data(col: _Collector, root: Path, state_path: Path, new_authored_value: str|Path, proposal_id: str, tree_entry: dict[str,str], change_description: str|None) -> dict[str,Any]`
   - Extract of current `:1291–1492` except calls `_retention_rows_for_graph` instead of `_retention_plan`, and **omits** final `col.reverify()` + `_tree_map` equality (`:1439–1442`) — those stay in callers as fixed completions (so data helper never asserts stability/readiness by itself). Returns identical dict keys as current `:1486–1492`.
5. `_pipeline(...)` — keep name/signature; body becomes `data=_pipeline_data(...); _require_retention_dests_absent(col, _retention_rows-equivalent from data["proposal"]["retention_plan"]); col.reverify(); tree-equality; return data`. Preserves exact P1 fixed absence + stability + tree completion. No policy parameter.
6. `_pin_proposal_layout(col: _Collector, root: Path, state_path_value: str|Path, proposal_path_value: str|Path, profile_validated: dict[str,Any]) -> tuple[dict, str, str, str, Path, Path, dict]`
   - Narrow extraction of `:1710–1771`: config pin + JSON, proposal pin + `PROPOSAL_FILENAME` + JSON + schema gate, `_check_proposal_id`, `expected_dir` derivation, `observed_dir_rel` equality, `PROPOSAL_FILES` layout via `col.safe`, `staged_authored`/`staged_reader` pins, `change_description` nonempty + authoring/reader canonical-path prechecks (`:1756–1769`), `_tree_map` entry snapshot. Returns `(proposal,proposal_id,expected_dir,observed_dir_rel,staged_authored,staged_reader,tree_entry)`. No derivation, no comparison, no scope, no receipt.
7. `_compare_supplied_to_rederived(supplied: dict[str,Any], rederived: dict[str,Any], staged_reader_bytes: bytes, proposed_canonical: bytes) -> None`
   - Exact `:1778–1801` sequence, no second copy: 7 header keys (`schema_version/proposal_id/issue_id/research_profile/publication_profile/route/status`) → `HEADER_MISMATCH`; `basis` exact → `BASIS_MISMATCH`; `proposed.authoring_input_ref` exact → `PROPOSED_AUTHORING_MISMATCH`; `proposed.proposed_reader_ref` exact → `PROPOSED_READER_MISMATCH`; `proposed_reader_canonical_sha256` exact → `PROPOSED_DIGEST_MISMATCH`; `change_description` exact (already nonempty by caller) → `CHANGE_DESCRIPTION_MISMATCH`; `proposed_reader_ref.sha256 == proposed_reader_canonical_sha256` → `PROPOSED_REF_DIGEST_MISMATCH`; `retention_plan` exact → `RETENTION_MISMATCH`; `staged_reader_bytes == proposed_canonical` → `PROPOSED_BYTES_MISMATCH`. Raises `ProposalError`; returns `None` on equality.

Reuse as-is without modification (called by both P1 wrappers and new observer via private import; no P2R changes):

- `_Collector/safe/pinned/reverify`, `_resolve_tree_base`, `_check_proposal_id`, `_eligibility`, `_route_of`, `_original_checkpoint`, `_active_effective`, `_load_profile`, `_derive`, `_canonical`, `_Graph/_build_graph` (+ `_frozen_names_check`, `_proposed_upstream_check`, `_canonical_state_path`), `_validated_state_profile_for_tree`, `_final_full_receipt_recheck`, `_validate_scope`, `_tree_map` (for edition-tree byte map only; empty-dir/full-control coverage comes from P2R primitives in V3, not from changing `_tree_map`).

In A `scripts/survey_editorial_current_authority_v2.py`, import only the above private P1 names + P2R `_Session/_control_paths/_snapshot_expanded/_retained_inventory/_retained_expected_sets/_expected_retained_dest/_check_canonical_bytes`-equivalents (or narrow same-file equivalents if import cycle forbids; no P2R source change either way). No new public helper exported as readiness; new module exposes only `observe_current_authority` + `CurrentAuthorityError`.

### V1.2 Fixed-completion call graphs (no caller-selected branch)

Existing `prepare_proposal` (unchanged semantics, refactored body):

```text
_Collector → _validated_state_profile_for_tree → _tree_map(entry)
→ _pipeline_data → _require_retention_dests_absent → col.reverify + _tree_map(final)
→ schema_gate.validate_instance → _final_full_receipt_recheck → col.reverify + _load_profile + _tree_map(final)
```

Existing `validate_proposal` (unchanged semantics):

```text
_Collector → _pin_proposal_layout (config/proposal/schema/dir/layout/staged/tree_entry)
→ _pipeline_data(staged_authored) → _compare_supplied_to_rederived (ALL fields + staged bytes)
→ _require_retention_dests_absent (on rederived retention_plan; P1 still refuses post-capture)
→ state/profile reload → _validate_scope? → _final_full_receipt_recheck (AFTER scope)
→ col.reverify + _load_profile + _tree_map(final) → return supplied UNCHANGED + input_hashes/measured
```

New `observe_current_authority` (always current+retained, never absent-verdict):

```text
narrow pins → _validated_state_profile_for_tree (BEFORE broad walk) → control/edition snapshots
→ P2R verify_retention (exact pinned proposal/manifest) + retained pins/inventory (retained _Session)
→ _pin_proposal_layout + _pipeline_data (live _Collector) + _compare_supplied_to_rederived
→ live State/path byte equality + retained-manifest cross-binding (V2)
→ _validate_scope? (existing semantics) → _final_full_receipt_recheck (AFTER scope)
→ fresh retained revalidation if later helpers could affect view (bounded second verify_retention allowed)
→ final ORIGINAL-pin/identity/inventory/HEAD/close boundary (V3)
→ return CURRENT_BASIS_OBSERVED_* (V4), no input mutation
```

Proof obligation (pre-implementation, in diff): show `git diff` of M file contains only the 7 helper extractions + 2 wrapper thin bodies, no public signature/schema/scope-meaning change; show every `prepare/validate` success path still executes `_require_retention_dests_absent` + `_final_full_receipt_recheck` + `reverify` + final `_tree_map`; show every observer success path executes `verify_retention` + `_compare_supplied_to_rederived` + `_validated_state_profile_for_tree` + `_final_full_receipt_recheck` + final zero-delta inventory. If coherent split cannot fit 2A1M without duplicating ~600-line validator or changing authority semantics, **stop with exact blocker** (file:line + duplicated range + why import-reuse fails) instead of expanding API.

### V1.3 Every compared field + staged canonical-byte condition (exact)

Via `_pin_proposal_layout` + `_pipeline_data` + `_compare_supplied_to_rederived` (citations `validate:1715–1801`):

- Header (7): `schema_version, proposal_id, issue_id, research_profile, publication_profile, route, status` — exact equality, `HEADER_MISMATCH` otherwise.
- Basis (exact dict): `state_ref{path,sha256}`, `validation_checkpoint_ref` (exact State validation record), `active_revalidation_ref` (exact record or `None`), `active_reader_input_ref{path,sha256}`, `before_graph_digest`, `preserved_upstream_digest`, `generated_receipt_ref{path,sha256}`, `renderer_commit`, `contract_identity` — `BASIS_MISMATCH`.
- Proposed: `authoring_input_ref{path,sha256}` exact (`PROPOSED_AUTHORING_MISMATCH`); `proposed_reader_ref{path,sha256}` exact (`PROPOSED_READER_MISMATCH`); `proposed_reader_canonical_sha256` exact (`PROPOSED_DIGEST_MISMATCH`); `change_description` nonempty + exact (`CHANGE_DESCRIPTION_EMPTY/MISMATCH`); `proposed_reader_ref.sha256 == proposed_reader_canonical_sha256` (`PROPOSED_REF_DIGEST_MISMATCH`).
- Retention: `retention_plan` list exact (ordered, per-row `roles/path/sha256/byte_count/policy` + `retained_ref` XOR `retained_dest/retained_sha256/retained_byte_count`) — `RETENTION_MISMATCH`.
- Staged bytes: `staged_reader.read_bytes() == proposed_canonical` (`PROPOSED_BYTES_MISMATCH`); `staged_authored` bytes == `authoring_input_ref.sha256` (layout precheck `PROPOSED_AUTHORING_MISMATCH`); planned `proposed_reader_ref.path` must equal `<expected_dir>/reader-surface-input-v2.json`, authoring path must equal `<expected_dir>/authoring-input.json` (`PROPOSED_READER_PATH/AUTHORING_PATH`).
- Layout/canonical: proposal filename must be `proposal.json` (`PROPOSAL_FILENAME`); `observed_dir_rel == expected_dir` derived from current Profile `source_root` + `proposal_id` (`PROPOSAL_LAYOUT`); all `PROPOSAL_FILES` present via `col.safe` (alias/FIFO refusal).
- Live derivation context (inside `_pipeline_data`, not compared as free text but enforced): strict `validate_agent_state` + `_eligibility`, canonical State path, staged-authoring location, original checkpoint exact (`:355–377`), active-before exact via `_active_effective` (`:380–411`, `ACTIVE_PATH_REBIND` refusal), manuscript/Gate/receipt routing, `NO_EDITORIAL_CHANGE` refusal when proposed==before, receipt/Gate/bundle/pre-TeX predicates (`:1393–1430`), `_frozen_names_check` + `_proposed_upstream_check`, graph/digests.

No field dropped; pre-code diff must show `_compare_supplied_to_rederived` called once by both `validate_proposal` and observer (no second handwritten copy).

---

## V2 — two dependency stores and same-byte cross-binding

Two logical domains, never merged before planning. An equivalent implementation may use tagged partitions of one store iff tags enforce the same separation; logical domains remain distinct.

- **Live store**: P1 `_Collector` (`files: rel->bytes`, `head`, `config_sha`). Contains ONLY current-authority/rederivation inputs discovered via `_validated_state_profile_for_tree` → `_pin_proposal_layout` → `_pipeline_data` (including staged proposal inputs). Retained COPY destinations are **never** pinned here before planning; `_retention_rows_for_graph` reads `set(col.files)` for overlap detection while retained dests live elsewhere. Do not remove arbitrary refs to make overlap pass (contract forbids). Live pins: State, `DEFAULT_CONFIG`, Profile, original checkpoint + rows, active record + predecessor chain, manuscript + supports + approval, Gate record, receipt + reviewed reader + semantic review, bundle, archive, before/new authored inputs, derived surfaces (pinned via `_derive`), supplied proposal + staged authoring/reader, supplied scope review (if any), proposal schema, `_tree_map` snapshot (separate from `col.files`), full control/edition snapshots (V3).
- **Retained store**: P2R `_Session`-style reader (reuse `_Session.safe_read/repinned/reverify/_close_all` without changing P2R, or narrow same-file equivalents). Contains ONLY retained verification inputs: supplied proposal bytes, manifest bytes, both schemas, retained State bytes, KEEP Profile bytes, every COPY `retained_dest` bytes, every KEEP `retained_ref` bytes, staged authoring/reader re-pins, retained inventory files/dirs/sizes, `capture_inputs` required-path hashes where independently required. Never calls P1/Git/HEAD; never requires mutable live COPY originals.
- **Own/schema/current-control deps**: pin `P2V module file` + `P1 module file` + both schemas (`editorial-correction-proposal-v2`, `editorial-retention-manifest-v2`) + `DEFAULT_CONFIG` + `_control_paths(cfg)` expansion (`implementation_control_roots` + `contract_files` + `templates/survey/jgaisurvey.sty`) via `_snapshot_expanded` in BOTH stores or a dedicated control snapshot compared at final boundary; contract/style/closure bytes enforced by receipt predicates, not by trust.
- **Later-reopen binding**: every later `safe`/`safe_read`/`repinned` compares to ORIGINAL pins (`STABILITY_VIOLATION/FILE_REPLACED/REF_DRIFT/CONFIG_DRIFT/HEAD_MOVED`); never resnapshot a changed byte as new truth. `verify_retention` returned `RETAINED_SET_VERIFIED` dict is checked for bound `proposal_sha256/manifest_sha256` equality to original pins but is **not** sufficient alone — observer additionally compares its returned row hashes to original retained pins and re-runs retained inventory.
- **Cross-binding**: exact shared expectations compared without conflation — proposal SHA, `basis`/`proposed` dicts, per-row `path/sha256/byte_count`, staged authoring/reader SHA, `before_graph_digest/preserved_upstream_digest/proposed_reader_sha256`, manifest `proposal_ref.path/sha256`. Final `input_hashes` unions live + retained maps **only after** all checks, with duplicate path + differing hash → refuse (`INPUT_HASH_CONFLICT`); identical path+hash duplicates allowed (same bytes observed in both domains, e.g. staged files).

---

## V3 — strict-current-before-walk, scope-before-final-receipt, final inventories

Complete order with actual helper + failure boundary. No async step; no past observation reused as authority. If reordered for safer pre-read binding, preserve initial pins + strict-live-before-broad-walk; return exact order in diff.

1. **Raw-safe narrow pins** (`_Collector.safe` / `_Session.safe_read`, lexical→alias→regular→read): supplied proposal, manifest, State, `DEFAULT_CONFIG`, Profile (via State ref), both schemas, supplied scope (if any, pinned but not validated yet). Reject lexical aliases/nonregular/FIFO/escape before reading (`PATH_*`). Pin actual current HEAD via checked sanitized Git (`_git_head`-equivalent, `GIT_*` stripped + 3 forced vars, rc checked, 40-hex). Preserve byte counts/hashes/ancestor identities; never resnapshot after mismatch.
2. **Strict live-State/Profile/canonical-root BEFORE broad walks** (`_validated_state_profile_for_tree:1536–1569` + `_eligibility:327–342` + `_canonical_state_path`): strict `validate_agent_state`, healthy VALIDATED_DRAFT/approved Architecture/pending Preview-no-provenance/pending downstream/inactive exception, canonical State path equality, Profile SHA/issue binding, repo-local roots. Derive expected proposal/manifest namespace from current Profile `source_root` + exact `proposal_id`, independently of untrusted manifest prefixes. Failed guard refuses regardless of historical readback. No historical cloned State or pending-basis admission (`_load_profile`, `_derive` longform `load_derivation_for_readback` vs weekly `load_derivation` without editorial authority).
3. **Validated snapshots** (`_snapshot_expanded` + `_tree_map` + `_control_paths`): `source_root`/`survey_root` edition trees, `DEFAULT_CONFIG` + `implementation_control_roots` + `style` + flattened `contract_files`, plus emission of expected control/edition inventory (regular-file bytes + directories **including empty** + safe type/mode/identity; fail on unreadable/missing/walk errors). Initial retention present; final expected delta zero. Known-byte hashes alone do not detect additions — `_tree_map` alone insufficient (no empty-dir inventory); use bounded P2R `_snapshot_expanded`/`_retained_inventory` or equally narrow new-module equivalents, not a generic framework.
4. **Same-invocation retained validation** (`verify_retention` on exact pinned proposal/manifest paths): compare returned `proposal_sha256/manifest_sha256` to original pins. Pin actual COPY/KEEP/staged/historical State/Profile bytes against explicit plan/ref hashes/sizes in retained session + exact closed inventory (`_retained_expected_sets:829–848`, `_retained_inventory`). Helper reopening files cannot switch proposal/manifest/row. No caller token; no claim of witnessing original capture.
5. **Common current derivation + supplied comparisons (live store)** (`_pin_proposal_layout` + `_pipeline_data` + `_compare_supplied_to_rederived`): live State/original checkpoint/active-before/graph/reader/plan vs same supplied proposal + independently validated retained manifest. Uses separate live collector (V2).
6. **Optional scope + full receipt AFTER scope** (`_validate_scope:1635–1695` with existing semantics, then `_final_full_receipt_recheck:1572–1598` actual route `validate_receipt`, not contract-only). Retained validation freshly completed in this invocation after shared-data equality if any later helper could affect its view (bounded second `verify_retention` permitted, not a new semantic review).
7. **Final boundary** (all consumed live + retained bytes vs ORIGINAL pins + expected row bytes/sizes, relevant ownership identities via `lstat` dev/ino/mode where P2R patterns apply, full current control/edition/retained inventory incl. empty dirs, schemas/P2V source deps, HEAD stability): later reads not exempt; never resnapshot changed bytes into truth. Close every descriptor with explicit primary/secondary disposition (`_Session._close_all` primary-preserving; live `_Collector` has no fds but `reverify()` + HEAD/config/tree rechecks serve as close-equivalent; report `CLOSE_FAILED` on failure). Prove no-write via immediate pre/post or known-injection deltas BEFORE repair (narrowed P2R late-plant post-removal pattern NOT reused).

Failure codes at each gate are the existing `ProposalError`/`RetentionError`/`CurrentAuthorityError` codes (V4); any drift refuses with no observer writes.

---

## V4 — precise result/errors and current-vs-historical predicate table

### V4.1 Result shape (in-memory only)

```python
{
  "result": "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE" | "CURRENT_BASIS_OBSERVED_SCOPE_BOUND",
  "state_ref": {"path": str, "sha256": str},               # canonical live State, byte-exact to proposal.basis.state_ref
  "proposal_ref": {"path": str, "sha256": str},            # supplied proposal repo-rel + sha256
  "retention_manifest_ref": {"path": str, "sha256": str},  # supplied manifest repo-rel + sha256
  "scope_review_ref": None | {"path": str, "sha256": str}, # present when supplied ordinary valid review read, even if NEEDS_SCOPE
  "observed_head": str,                                    # 40-hex HEAD pinned at entry + reverified stable at exit
  "measured": {
    "before_graph_digest": str, "preserved_upstream_digest": str,
    "proposed_reader_sha256": str, "graph_nodes": int, "graph_edges": int,
    "copy_files": int, "keep_refs": int,
  },
  "input_hashes": {str: str},                              # union of live + retained rel->sha256, conflict-refusal
}
```

Exact key/type/canonical-path validation required (reject extra/missing keys, non-64-hex sha, non-repo-local paths). `scope_review_ref` present when supplied ordinary valid review read even if it lacks correction block and outcome is NEEDS_SCOPE. No success on invalid supplied review. Counts/digests measured, not copied into agreement. Duplicate path/hash contradictions in merged observation refuse. Names alone do not guarantee downstream use; future writer needs fresh authority; no bearer token, no reason/State adoption, no new role/gate.

Scope matrix (existing `_validate_scope` semantics preserved):

| Case | Result |
|---|---|
| No scope arg | NEEDS_SCOPE |
| Supplied ordinary valid pre-TeX review without correction block | NEEDS_SCOPE + exact `scope_review_ref` |
| Supplied invalid review | refuse (`SCOPE_*`) |
| `WITHIN_APPROVED_AUTHORITY` + exact before/after/upstream + substantive `EDITORIAL_CORRECTION_SCOPE` PASS | SCOPE_BOUND (observation only) |
| `REQUIRES_OWNER_DECISION`/REJECT/wrong/stale/substance-less | refuse |

### V4.2 Error shape

```python
class CurrentAuthorityError(ValueError):
    def __init__(self, code: str, phase: str, disposition: str, detail: str,
                 owned: dict|None = None, cause: BaseException|None = None): ...
    # message: f"{code}: [{phase}/{disposition}] {detail}"
```

`code` = existing `ProposalError`/`RetentionError` code where applicable (e.g. `STATE_INVALID`, `BASIS_MISMATCH`, `COPY_DRIFT`, `SCOPE_*`, `HEAD_MOVED`, `TREE_MOVED`, `INPUT_HASH_CONFLICT`, `CLOSE_FAILED`), else new `CURRENT_*` only for observer-specific merge/binding faults. `phase` = one of `PIN/AUTHORITY/SNAPSHOT/RETAINED/DERIVE/COMPARE/SCOPE/RECEIPT/FINAL/CLOSE`. `disposition` = `REFUSED_*` (never `VERIFIED`). `owned` carries primary `observed_head`/pin SHAs for diagnostics, never a permission. `cause` chains original `ProposalError`/`RetentionError`/`OSError`.

### V4.3 Current-vs-historical pin table (which hashes must byte-equal NOW)

| Pin | Must byte-equal now? | Authority |
|---|---|---|
| Live State bytes/path vs `proposal.basis.state_ref` | **YES strict** (no timestamp/counter/metadata exception) | `_validated_state_profile_for_tree` + `_compare` BASIS |
| Original validation checkpoint bytes/content | **YES** (`ORIGINAL_CHECKPOINT_DRIFT/IDENTITY_MISMATCH`) | `_original_checkpoint:355–377` |
| Active-before (original rows or active superseded/preserved + predecessor chain) | **YES** (`ACTIVE_*`, `PREDECESSOR_*`, `ACTIVE_PATH_REBIND` refusal; later different active → stale refuse) | `_active_effective:380–411` |
| Canonical live Profile/config + canonical State path | **YES** | `_load_profile`, `_canonical_state_path` |
| Rederived before/proposed reader + typed graph/plan + staged FILE bytes | **YES exact** (all V1.3 fields) | `_pipeline_data` + `_compare` |
| Full current receipt/HEAD ancestry/clean-control/closure/contract | **YES** (artifact-only HEAD accepted only when full predicates + exact proposal equality pass + HEAD stable within call; never `HEAD==renderer_commit` alone or `contract_identity` alone; code/control changes outside predicates refuse) | `_final_full_receipt_recheck` + route `verify_tool_basis/_verify_head_bytes` |
| Retained COPY/KEEP/staged/proposal/manifest bytes vs explicit row/ref hashes/sizes | **YES** (both P2R and P2V refuse on KEEP drift; P2R persistence-positive does not excuse P2V freshness-negative on mutable-original change) | `verify_retention` + retained re-pins + final inventory |
| `capture_inputs` producer/extras (e.g. P2R module/schema fingerprints) | **NO blanket** — historical fingerprints; current equality only where same path independently required by rederived proposal/current validators or actual COPY/KEEP/staged/proposal refs (`:1989–2019` scope) | P2R `:2009–2019` comment + contract §4.7 |
| Whole-edition proposal-time directory map | **NO** — not persisted; do not invent from graph digests or `capture_inputs`; unreferenced file added outside closed retained tree before invocation is not automatically stale unless actual current validator makes it so | contract §1 |
| Creator/whole-history/anti-rollback | **NO claim** — matching bytes do not attest creator/continuous history without external monotonic/authenticated authority (not selected); implementation must not restore/forge/de-reference/delete/roll back to pass | contract §1 |

No P2V pending-basis construction/admission, no old-epoch migration, no live-old-State substitution using retained State, no filename-selected record.

---

## V5 — actual-source fixture/regression/evidence plan

### V5.1 Fixture source binding (meaningful independent commits BEFORE authority)

- New implementation candidate: own byte-copied available Git DB (inert origin, no alternates/hardlinks/shared objects; inspect every `.git` entry + `config`/`remote`), detached 409, no candidate branch/commit. Preserve P2R active + proof copies untouched.
- Fixture repos: independent DBs per test family, built by copying available source (tracked `git ls-files` + `UNTRACKED_SOURCES` pattern from `test_survey_editorial_correction_proposal_v2.py:75–115` / `_make_p2r_source_root` in `test_survey_editorial_retention_v2.py:62–98`), then committing **meaningful changed P1 + new2 source BEFORE producing authority**: i.e. fixture `git commit` must include the refactored `survey_editorial_correction_proposal_v2.py` (with V1 helpers) + new `survey_editorial_current_authority_v2.py` as committed bytes, with process-scoped synthetic identity (`Synthetic DM021-P2V Fixture`, `p2v-fixture@example.invalid`, inert `https://example.invalid/…` origin), no empty commits, no reconstruct/Production objects. Uncommitted review worktree is never a positive renderer basis (receipt predicates reject uncommitted control source; contract §4.6). Reuse `_make_source_root`/`_copy_base`/`_snapshot`/`_assert_no_write` patterns where they truly preserve source/authority/isolation (read actual helpers `p1t:75–162`, `p2r:62–150`); do not transplant blindly — P2V needs live+retained dual roots and 18-file manifest.
- Real chains only: Longform authored prose (`_new_longform_helper` + accepted-chain recipe) + Weekly envelope (`_new_weekly_helper` + `_build_weekly_validated`) + real R1-owner predecessor(s) via `resolve_active_publication_revalidation` (no forged R1-like pointer; new active pointer after proposal must refuse). Synthetic fixtures are never genuine approvals/publication acceptance.
- Cases (each snapshots immediate mutated-pre/post or exact known injected delta BEFORE any restoration; close faults before declared later check; no post-removal equality overclaim):
  1. Longform + Weekly real `prepare→stage→capture→observe` positives (with scope absent → NEEDS_SCOPE, then valid scope → SCOPE_BOUND); public P1 `prepare/validate` still destination-strict after capture (unretained baseline + post-capture refusal affected regressions).
  2. Real R1 predecessor vs stale-active (new active after proposal refuses; `ACTIVE_PATH_REBIND` + preserved/superseded drift).
  3. Persistence-positive/freshness-negative: mutable COPY-original change (P2R still VERIFIED, P2V refuses basis); KEEP drift refuses both; no live-old-State substitution; exact path/hash identity + wrong-path equal-bytes negatives.
  4. Scope: absent / ordinary-without-block / malformed / non-PASS / wrong-before/after/upstream / REJECT / REQUIRES_OWNER / valid scope created after capture outside `retained/` (must succeed when predicates pass + stable; no fabricated historical-inventory rejection) / no review-path rebinding by equal SHA.
  5. Receipt/HEAD: ancestry/clean-control/closure/contract + artifact-only HEAD movement control (accept only when full predicates pass) + real control-source change refusal (not just contract-string mutation).
  6. Retention boundaries: missing/extra retained files + empty dirs (exact file+dir closure via `_retained_expected_sets`), aliases/special files with explicit no-read checks, mixed proposal/manifest, false caller context unavailable at public API (no `verified_set` param exists), exact zero-delta cross-helper late drift + close faults (`CLOSE_FAILED` primary-preserving).
  7. Affected P1/P2R regressions only (chosen after diff; e.g. P1 unretained + post-capture + scope + receipt paths touched by factoring; P2R `verify_retention` unchanged but exercised via observer). No old25/36 transfer, no decorative broad suite.
- Counts/commands follow actual diff; prefer safe immutable accepted fixture bases/copies when demonstrably equivalent (record equivalence predicate).

### V5.2 Runner/proof strategy (draft readback BEFORE long run)

Before any long run, return for root readback: actual source `git diff` (M file + 2 new files) + static expected18 manifest draft + runner draft + proof draft. Drafts must implement stated guards (not print-only/filtered):

- Runner: fresh absent `PYTHONPYCACHEPREFIX` + `PYTHONDONTWRITEBYTECODE=1` (avoid old cache execution), sanitized Git env (strip `GIT_*`, force 3 vars, checked rc), exact runtime/deps/argv/cwd/forced env recorded (only relevant keys, not whole env), direct exclusive durable child stdout/stderr, static18 comparison + immutable inherited15 comparison + preknown cache inventory+hashes + actual HEAD/tree/index/full raw statuses before + finally-post + checked return codes. Keep every executed script version (new names after execution); process state/PIDs/durable partial outputs permit interruption-safe resume without duplicate runs. No source cache cleanup, no loss of failed evidence, disposable-index/copy patch generation only (never active `add -N`).
- Proof: complete18patch directly vs clean actual409 (contains all prior overlays) + all18 hashes/modes + final saved-patch apply in NEW independent actual409 copy (clean observation must not try to read removed NEW files) + explicit all-entry/inode-set/link/config/status + static-pin checks; cache removals only in declared disposable preparation, not run no-write. Scripts are exact-run evidence, not certified rerunners. P2R logger/late-plant/draft/interruption qualifications stay intact.
- Runtime available (no candidate imports): `Python 3.14.4` at `/usr/bin/python3` (source-binding §1). No new runtime dependency proposed.

### V5.3 Blocker statement (>2A1M gap)

No exact blocker found in Phase A reads: V1 factoring maps to actual `file:line` without wholesale duplication or semantic change; V2–V4 fit selected 2A1M/0-schema (new observer + private P1 factoring + new test); V5 fixture path uses existing accepted-chain recipes + independent committed source. If implementation diff shows coherent split impossible within 2A1M, General must stop with exact blocker (helper name + duplicated line range + measured line delta + why reuse fails) rather than duplicating validator or expanding public API. No new Human role/gate or production-owned-fixture prerequisite claimed.

---

## Stop

Phase A complete. No implementation, no candidate creation, no tests run. Awaiting Astra selection of V1–V5 before any Phase B work. Whole NOT_READY, step4/B3 OPEN, audit unstarted, DM021 OPEN. Commit/Push Human-owned.
