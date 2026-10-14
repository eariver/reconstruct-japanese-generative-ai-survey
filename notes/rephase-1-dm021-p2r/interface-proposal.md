# DM021-P2R PhaseA — exact interface/fixture return (before code)

2026-10-13 JST. Co-Worker read-only return. Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60` (detached actual `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` +13files 3M10A, all13 SHA/mode/bytes exact vs `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4/freeze-post.json`; P2R 3A absent; see `evidence-20261013T122831Z-phaseA/`). Fixed contract `outputs/rephase-1-dm021-retention-contract-decision.md` SHA256 `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e`, mandatory `notes/rephase-1-dm021-promotion/astra-review-resolution.md` I1–I4, `independent-design-review.md` §8. Reconstruct HEAD `a45e1bfea675b496b44b01f50460d1458675c840`, status only untracked `task.md` (+ this new evidence/proposal untracked by design). Runtime version probes only: `Python 3.14.4`, `git 2.53.0`. No imports, no tests, no fixtures executed, no restoration, no network, no index/ref/commit mutations. STOP for Astra concrete return before any code.

## 1. Shipping budget (exactly 3A, no modifications)

1. `scripts/survey_editorial_retention_v2.py`
2. `schemas/editorial-retention-manifest-v2.schema.json`
3. `tests/test_survey_editorial_retention_v2.py`

P1 `scripts/survey_editorial_correction_proposal_v2.py` (`5d2fde45…`), proposal schema (`5623c0d9…`), review schema (`e8598239…`), Gate files (LF2I-inherited) unchanged. Capture calls unmodified P1 `validate_proposal` pre-write only, without scope review. Verifier never imports/calls P1. No CLI, config, reason enum, State/controller/Gate/receipt/publisher, live-artifact, branch/commit changes.

## 2. Public APIs (exact signatures)

```python
def capture_retention(root: str | Path, state_path: str | Path, proposal_path: str | Path) -> dict[str, Any]
def verify_retention(root: str | Path, proposal_path: str | Path, manifest_path: str | Path) -> dict[str, Any]
```

Refusals raise `RetentionError(ValueError)` with `CODE: detail` prefix (mirrors P1 `ProposalError`). Success returns plain dicts (JSON-serializable, no bytes). No writes on any preflight refusal; no overwrite/retry/adopt/cleanup after root claim; live originals never mutated.

### 2.1 `capture_retention` return (on `RETAINED_SET_CAPTURED` only)

```python
{
  "result": "RETAINED_SET_CAPTURED",
  "manifest_path": "<proposal_dir>/retained/retention-manifest.json",  # repo-relative posix
  "manifest_sha256": "<sha256 of exact manifest file bytes>",
  "proposal_sha256": "<sha256 of supplied proposal.json bytes>",
  "input_hashes": {rel: sha256, ...},   # verbatim P1 input_hashes + P2R dep pins below
  "retained": {"copy_files": N, "keep_refs": M, "manifest_bytes": K},
}
```

`input_hashes` = P1 `validate_proposal(...)["input_hashes"]` (every `col.files` entry: State, config, Profile, checkpoint, receipt, Gate, manuscript, bundle, reviews, staged authoring/reader, proposal, predecessors, evidence/screening/discovery transitives, tool closure, outputs) **plus** two enumerated P2R deps: `scripts/survey_editorial_retention_v2.py` + `schemas/editorial-retention-manifest-v2.schema.json` (sha256 of live module/schema bytes at capture). Sorted unique in manifest; returned dict preserves same mapping. These are observations, not signatures/approvals.

### 2.2 `verify_retention` return (on `RETAINED_SET_VERIFIED` only)

```python
{
  "result": "RETAINED_SET_VERIFIED",
  "manifest_sha256": "<sha256 of exact manifest bytes>",
  "proposal_sha256": "<sha256 of exact supplied proposal bytes>",
  "checked": {"copy_files": N, "keep_refs": M, "staged_refs": 2},
}
```

`RETAINED_SET_VERIFIED` means the observed bound set is complete **now**; `RETAINED_SET_CAPTURED` means this invocation finished its checks. Neither means current eligibility, semantic approval, historical successful invocation, independent witness, or adoption authority. Missing/malformed/partial never success.

### 2.3 Typed errors (exact codes; `RetentionError("CODE: detail")`)

- Path/safety: `PATH_TRAVERSAL`, `PATH_NOT_REPO_LOCAL`, `PATH_ALIAS`, `PATH_MISSING`, `PATH_NOT_REGULAR`, `PATH_UNREADABLE`, `STABILITY_VIOLATION`, `HEAD_MOVED`, `CONFIG_DRIFT`, `TREE_ALIAS`, `TREE_NOT_REGULAR`, `TREE_MISSING`, `TREE_MOVED`.
- Proposal/manifest shape: `PROPOSAL_FILENAME`, `PROPOSAL_LAYOUT`, `PROPOSAL_UNREADABLE`, `MANIFEST_FILENAME`, `MANIFEST_UNREADABLE`, `SCHEMA_INVALID`, `HEADER_MISMATCH`, `BASIS_MISMATCH`, `PROPOSED_MISMATCH`, `RETENTION_MISMATCH` (row/role/policy/identity divergence), `REF_SHAPE`, `REF_DRIFT`.
- P1 binding: any P1 `ProposalError` propagates unchanged (caller sees original `CODE: detail`; P2R adds `P1_REFUSED: <code>` wrapper context without mutating P1). Post-capture P1 `RETENTION_DEST_CONFLICT` is expected, not a P2R failure.
- Retention ownership: `RETAINED_ROOT_EXISTS` (any existing file/dir/dangling alias at `retained/`, including empty/same-byte foreign), `RETENTION_DEST_TRAVERSAL`, `RETENTION_DEST_ESCAPE`, `RETENTION_DEST_ALIAS`, `RETENTION_OVERLAP`, `RETENTION_DEST_CONFLICT` (duplicate), `ROOT_IDENTITY_CHANGED`, `ANCESTOR_REPLACED`, `WRITE_SHORT`, `WRITE_FAILED`, `CLOSE_FAILED`, `READBACK_MISMATCH`, `FINALIZATION_REFUSED` (late drift/extra/unowned), `MANIFEST_CLOSE_FAILED`.
- Verification verdicts: `INCOMPLETE_RETENTION` (missing/malformed/partial manifest or absent COPY/KEEP), `INVALID_RETENTION` (hash/size/inventory/row/binding mismatch, KEEP drift, staged drift, wrong-path manifest, ambiguous Profile chain), `INDETERMINATE_CLOSE` (manifest bytes present but close-fault flag preserved; never success). KEEP drift refuses even when all COPY match. Live mutable COPY-original drift after capture is **not** a persistence failure and is never read.
- No semantic/PASS/Gate adoption codes; no current-eligibility assertion.

## 3. I1 — historical Profile chain (no basename, no mutable State, no arbitrary Profile row)

Feasible against actual P1 source (all line refs read in candidate):

- P1 State node `state:authority` COPY at `survey_editorial_correction_proposal_v2.py:608-614`; State-bound Profile validation `:414-428` (`state.profile{path,sha256}` exact, issue-bound); bundle/manuscript exact Profile equality `:491-514,679,768-776`; X `upstream:x-production-profile` `:1159-1165` correctly excluded as non-authority; mutable set `:574-595` (effective rows + receipt outputs + receipt + reviewed reader + bundle results + State + pre-TeX + publication-authored inputs) — Profile absent, hence `KEEP_IMMUTABLE`; proposal dir derivation `:1323-1330,:1730-1741`.

Concrete verifier chain (each hop raw-contained + regular-file checked **before** typed parse; canonical roots established before broad inventory):

1. Safe-read supplied `proposal.json` bytes; sha256 = `proposal_sha256`. Schema-validate (proposal schema `5623c0d9…`). Extract `proposal_id`, `basis.state_ref{path,sha256}`, `retention_plan`.
2. Safe-read supplied `manifest_path` bytes; filename must be `retention-manifest.json`; schema-validate (new manifest schema). Require `manifest.proposal_ref.path` == supplied proposal repo-rel path **and** `manifest.proposal_ref.sha256` == `proposal_sha256` (same SHA at wrong path still refuses — no path rebind). Require `manifest.basis` == supplied `proposal.basis` exactly, `manifest.proposed` == supplied `proposal.proposed` exactly, `manifest.proposal_ref.proposal_id/issue_id/research_profile/publication_profile` == proposal header exactly.
3. In `manifest.rows` (one-to-one with proposal `retention_plan`, same order/roles/path/sha/policy, see §5), select rows with `roles ∋ state:authority`. Require exactly one such row, `policy == COPY_BEFORE_REPLACEMENT`, `path/sha256/byte_count` == `basis.state_ref` + retained `retained_dest` present. Any missing/duplicate/disagreeing → `INVALID_RETENTION`.
4. Safe-read retained State bytes at that `retained_dest`; sha256 + byte count must equal row + `basis.state_ref.sha256`. Parse JSON (historical identifiers only; no eligibility inferred). Extract `state.profile{path,sha256}`.
5. Select rows with a KEEP `retained_ref.path` == that exact State-profile path **and** `retained_ref.sha256` == State-profile sha. Require exactly one, `policy == KEEP_IMMUTABLE`. Reject if zero/multiple/disagreeing, if the matched row is COPY, or if any other KEEP row merely labelled `*profile*` disagrees (no arbitrary Profile-labelled row, no basename fallback). Safe-read required KEEP Profile bytes; sha/size must match. Parse Profile; require `profile.paths.source_root/proposal_id` present and repo-local.
6. Derive canonical `expected_proposal_dir = <source_root>/publication/v2/editorial-corrections/<proposal_id>` and `expected_manifest = <dir>/retained/retention-manifest.json`; require supplied proposal dir + manifest path equal these exactly (not manifest-prefix trust, not basename guess). Mutable current State is never consulted for this derivation; X `upstream:x-production-profile` never substitutes.

Before each typed hop: lexical traversal/alias checks, post-resolve containment, `lstat` regular-file gate (never open FIFO/device/dir/symlink). Missing/ambiguous/disagreeing at any hop → `INVALID_RETENTION`.

## 4. I2 — raw-read / snapshot / ownership protocol (no `_Collector` wholesale)

### 4.1 Why not import P1 `_Collector`

`_Collector.__init__` pins current `HEAD` + current config and `safe()` routes through live repo state (`proposal_v2.py:95-103,191-234`). Reusing it in the standalone verifier would pull current-config/HEAD assumptions and P1 epoch discipline into historical readback. Instead:

- **Capture** imports P1 module object only for `validate_proposal` (unmodified public entry) + `ProposalError`, `PROPOSAL_FILES`, plus `core` + `schema_gate`. It does **not** import or subclass `_Collector`, `_Graph`, `_pipeline`, or route loaders directly; all before-graph work arrives via the P1 return + `input_hashes`.
- **Verifier** imports only stdlib (`json, os, stat, pathlib`) + `core` (`json_bytes, sha256_bytes, sha256_object, sha256_file, repo_local_path`) + `schema_gate.validate_instance`. No `agent`, no derivation/weekly/longform/publication/quality/reader/Gate imports. No P1 import at all (prevents accidental `validate_proposal` call or current-authority check).

### 4.2 Minimal local safe-read primitive (both entry points; verifier standalone)

Mirror P1 `safe/pinned/reverify` discipline without P1 state:

- `sread(root, value, label)`: reject backslashes/dotdot lexically; refuse absolute escape; `lstat` leaf symlink → `PATH_ALIAS`; walk lexical ancestors root→parent, refuse symlinked ancestor (`PATH_ALIAS`) before resolution; `resolve()`, require containment in `root`; `lstat` post-resolve: symlink → `PATH_ALIAS`, non-regular (FIFO/device/dir/socket) → `PATH_NOT_REGULAR` (never open); read bytes, pin `files[rel]`; second pin with differing bytes → `STABILITY_VIOLATION`.
- `repinned(ref, label)`: require exact `{path,sha256}` shape; `sread`, compare `sha256_bytes` → `REF_DRIFT` on mismatch.
- `reverify()`: for every pinned rel, re-walk ancestors, re-`lstat` type, re-read bytes, compare; plus `repository_commit_sha(root)` stability for capture (HEAD-move refuses); verifier pins HEAD for evidence binding but does **not** enforce P1 epoch predicate (no receipt/control/contract revalidation).

### 4.3 Wrapper pins, input hashes, edition/control snapshots (capture)

Step 1 (before P1): `sread` proposal + State + Profile via canonical paths; `lstat` retained root — any existing file/dir/symlink/dangling alias (including empty) → `RETAINED_ROOT_EXISTS`, no P1 call, no writes. Pin `HEAD` (`core.repository_commit_sha`), P2R module/schema bytes (`sha256_file`), config bytes (`config/survey-production-v2.json`), control inventory (P1 F14 set: `DEFAULT_CONFIG ∪ implementation_control_roots ∪ STYLE_PATH ∪ contract_files`), and edition trees (`source_root` + `survey_root` via local strict walker mirroring P1 `_tree_map:267-318`: root-anchored bases, symlink-dir/file refusal, FIFO/device refusal, `.git` excluded, `{rel: sha256}` map). Snapshot `input_hashes` only from P1 return (see §2.1); capture raw proposal/State/Profile bytes before P1 and recheck equality after P1 return (switch refuses).

Step 2 (preflight, no writes on failure): recompute expected inventory from P1 `retention_plan`: COPY `retained_dest` set + manifest path + ancestor-dir closure. For each planned COPY: lexical/alias/overlap checks (same as P1 `_retention_plan:1231-1288`: traversal/escape/alias/overlap/duplicate + absent-required incl. dangling alias); `sread` live source bytes, require sha/size == plan row; `repinned` each KEEP `retained_ref`; namespace overlap vs all pinned live inputs refuses; unexpected entries under future `retained/` impossible yet (root absent) — ancestors of destinations must be absent-or-owned-after-claim (checked again after claim).

Step 3 (exclusive claim + writes): `os.mkdir(<proposal_dir>/retained)` exactly (not `makedirs`); `FileExistsError` → no ownership, `RETAINED_ROOT_EXISTS`. On success immediately `lstat` root, record `(st_dev, st_ino, st_mode)` as owned identity + hold an open `O_RDONLY|O_DIRECTORY` fd for `fstat` comparison across the invocation (close at end; close error recorded but does not confer success). Build only required ancestor dirs (`mkdir` one level at a time, each followed by `lstat` + parent-identity recheck). Each COPY: `os.open(dest, O_CREAT|O_EXCL|O_WRONLY, 0o664)`, `fstat` identity record, loop `os.write` until exact pinned bytes done (`WRITE_SHORT` on short with no progress), `os.fsync` (failure → fault), `os.close` with error check (`CLOSE_FAILED`), then `sread` readback requiring sha/size == plan row (`READBACK_MISMATCH`). Before/after each write: `fstat` root fd + `lstat` ancestors + destination parent; unexpected replacement → stop, no foreign cleanup (`ROOT_IDENTITY_CHANGED`/`ANCESTOR_REPLACED`). No temp files: final names written directly via `O_EXCL` (no undeclared entries; closed inventory in §5). Source bytes for COPY are the exact pinned pre-write bytes (never re-read live after writes begin except via reverify).

Step 4 (late rechecks before manifest): re-`repinned` all P1 `input_hashes` entries (State/control/proposal/staged refs), re-hash all written COPY + all KEEP refs, re-pin HEAD/P2R deps, recompute edition/control inventories; allow **only** the exact owned retention delta (new COPY + ancestor dirs) vs Step-1 snapshot — any extra/changed/disappeared input, mode/type change, or unowned output → `FINALIZATION_REFUSED`, partials preserved. Source/survey snapshot comparison excludes nothing except precisely owned new retained entries.

Step 5 (manifest-last): serialize manifest via `core.json_bytes` (see §5), `os.open(manifest, O_CREAT|O_EXCL|O_WRONLY, 0o664)`, full write/`fsync`/close-error handling/readback sha equality, then call internal `verify_retention` logic + final `reverify` + inventory recheck before returning `RETAINED_SET_CAPTURED`. Merely existing manifest insufficient. Partial/malformed/close-failed final artifact preserved, reported `INCOMPLETE_RETENTION`/`INDETERMINATE_CLOSE`, never rewritten into success. Crash may leave physically valid manifest with no delivered success — readback establishes consistency, not historical success event.

No rollback/recursive cleanup/truncation/overwrite/deletion-to-rerun/repair/partial-resume. Failure after claim leaves owned partials + actionable `{paths, statuses}` report; live originals untouched. Retry against any existing retained root refuses (`RETAINED_ROOT_EXISTS`). Prior-success caller may only call read-only `verify_retention` (verification, not idempotent adoption).

## 5. I3 — exact schema / canonical bytes / rows / capture_inputs

Manifest schema `schemas/editorial-retention-manifest-v2.schema.json` (new, strict `additionalProperties: false` throughout):

```json
{
  "schema_version": {"const": "2.0-rc1"},
  "kind": {"const": "EDITORIAL_RETENTION_V1"},
  "status": {"const": "CAPTURED"},
  "proposal_ref": {"path": "<canonical proposal.json repo-rel>", "sha256": "<64hex>",
                   "proposal_id": "<^[a-z0-9][a-z0-9-]{0,63}$>", "issue_id": "nonempty",
                   "research_profile": "nonempty", "publication_profile": {"enum": ["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]}},
  "basis": {"exact copy of P1 proposal.basis object (state_ref, validation_checkpoint_ref, active_revalidation_ref|null, active_reader_input_ref, before_graph_digest, preserved_upstream_digest, generated_receipt_ref, renderer_commit, contract_identity)"},
  "proposed": {"exact copy of P1 proposal.proposed (authoring_input_ref, proposed_reader_ref, proposed_reader_canonical_sha256, change_description nonempty)"},
  "rows": [{"roles": ["sorted unique"], "path": "repo-rel", "sha256": "64hex", "byte_count": ">=1",
            "policy": {"enum": ["KEEP_IMMUTABLE","COPY_BEFORE_REPLACEMENT"]},
            "retained_ref": {"path","sha256"} XOR "retained_dest": "repo-rel",
            "retained_sha256": "64hex", "retained_byte_count": ">=1"}],
  "capture_inputs": [{"path": "repo-rel", "sha256": "64hex"} sorted unique]
}
```

Rules:

- `rows` one-to-one with P1 `retention_plan`: same set of `path`, same sorted `roles`, same `sha256/byte_count/policy`, KEEP `retained_ref == {path,sha256}`, COPY `retained_dest` identical; plus `retained_sha256`/`retained_byte_count` measured at capture, required equal to source row `sha256`/`byte_count` (COPY read-back equality). No omitted/extra/duplicate path or role, conflicting policy/identity. `rows` sorted by `path` (P1 `_retention_plan` already sorts; verifier re-sorts for comparison, order-insensitive equality after sort).
- `capture_inputs`: sorted unique `{path,sha256}` from P1 `input_hashes` verbatim + exactly two P2R dep entries (module + schema). At minimum includes supplied proposal + staged inputs. Observations, not signatures/approvals; not all need remain live after later replacement (never used for current eligibility).
- `proposal_ref.path` is canonical `<source_root>/publication/v2/editorial-corrections/<proposal_id>/proposal.json` derived from retained Profile chain (§3), not trusted manifest prefix.
- Canonical bytes: manifest file = `core.json_bytes(manifest)` (`json.dumps(ensure_ascii=False, indent=2)+"\n"`, `survey_production_v2.py:86`; Longform reader canonical via `canonical_reader_bytes`, Weekly via `core.json_bytes` — P2R does not recompute reader bytes, it copies P1 digests). Digests: file bytes `core.sha256_bytes`, structures `core.sha256_object` (sorted-keys `(",",":")`). No self-hash recursion: manifest never contains its own sha; `capture_inputs` contains P2R module/schema shas but not manifest sha (manifest sha returned out-of-band + verified by readback).
- Closed inventory: only regular files below `retained/` are COPY destinations + final `retention-manifest.json`; directories exactly the ancestor closure including owned root. Unexpected entries (even empty dirs, aliases, special files) refuse completion/readback. No temp entries (see §4.3); any future temp need would require reviewed inventory-protocol change = scope blocker.
- P1 proposal/staged-authoring/staged-reader paths/bytes unchanged, verified through exact refs; nothing moved to new authority; manifest infers no new review target. Mutable live COPY originals never read by verifier; KEEP drift fails even when all COPY match. P1 post-capture refusal required: unchanged P1 `_retention_plan:1278-1282` (`is_symlink() or exists()` → `RETENTION_DEST_CONFLICT`) refuses any later `validate_proposal` on same proposal after capture — P2R tests prove this + prove `verify_retention` succeeds without P1.

## 6. I4 — fixture reuse, method plan, oracles (no execution in PhaseA)

### 6.1 Actual runtime (observed, not executed)

- `Python 3.14.4`, `git 2.53.0` (version probes only this unit). P1 final ran `36/36 (9P1+27Gate), 3308.284s, CPython 3.14.4`. Partial/shallow DB (`missing26309blobs` heritage), unbundled runtime remain as prior observations. Future implementation unit pins exact full source delta, actual HEAD/tree/runtime/argv/env + full raw statuses per run; no filtered-status-only allowlists, no capture-at-run mislabelled as static guard, no cleanup before comparison; all return codes/optimized-mode/error paths explicit; snapshot equality ≠ continuous no-drift/global CAS.

### 6.2 Exact accepted-chain fixture reuse (patterns read, not run)

Reuse P1 `tests/test_survey_editorial_correction_proposal_v2.py` recipes verbatim (independent temp Git DB, process-scoped identity, inert origin, no empty commits, `_make_source_root` + `_snapshot`/`_assert_no_write` discipline). No production fixture, no new Human Gate. Longform prose primary, Weekly envelope-only, accepted Draft/upstream unchanged.

- **Longform** (`test_longform_prose_correction_end_to_end`, `L_ISSUE = lf2i_tests.ISSUE`): `_new_longform_helper` (LF2I `_complete(_chain())` + `_advance_to_validated_draft` + LF1 worker with `_clean_evidence_helper`), authored prose delta `packages[0].narrative_sections[0].paragraphs[0].text += " Revised fixture sentence within approved evidence."`, `_stage_authoring_before_prepare` → `prepare_proposal` → `_stage_reader_and_proposal` → `validate_proposal` (`REVIEW_REQUIRED`). Before≠proposed inequality required.
- **Weekly** (`test_weekly_envelope_positive_and_body_negatives`, `W_ISSUE = incb.ISSUE`): `_new_weekly_helper` + `_build_weekly_validated` (real `_complete_authorities(_chain())`, `_current_state`, materialize-surface-only + full publication, manuscript/Gate/PDF/quality/later-review cascade, `_advance` to healthy `VALIDATED_DRAFT`), authored envelope `cover.headline = "Weekly tested method, revised edition"`, same stage/validate flow. Body negatives (draft-result/synthesis/archive tamper → `STATE_INVALID`/`DERIVATION_REFUSED`; same-byte → `NO_EDITORIAL_CHANGE`) stay P1-side; P2R reuses only the positive envelope path + staged proposal dir.
- **R1 predecessor** (`test_r1_mechanical_refresh_owner`, primary): two non-emitted Python comment-only commits to `scripts/survey_weekly_derivation_v2.py` + two `refresh_mechanical_evidence` via fixture committed code (`_run_fixture_code`), `supersedes` chain depth ≥1, State `publication_revalidation_provenance` installed, then P1 with `cover.headline = "Weekly R1 test, revised edition"` asserting `effective[validated-source].origin == ACTIVE` + non-null `active_revalidation_ref`. Distinguishes original checkpoint from active-before. (Honest generic-Core-change predecessor `test_honest_predecessor_original_vs_active` available as secondary reference; P2R needs only the R1 variant plus predecessor-absent positives.)
- **Staging contract**: authoring already at `<source_root>/publication/v2/editorial-corrections/<id>/authoring-input.json` BEFORE P1 `prepare` (`_stage_authoring_before_prepare`); reader + `proposal.json` staged AFTER prepare (`_stage_reader_and_proposal`). P2R `capture_retention(root, state_path, proposal_path)` consumes that exact 3-file dir + live State; no scope-review file needed (`REVIEW_REQUIRED` suffices).

`_make_source_root.UNTRACKED_SOURCES` (currently 10: 4 scripts + 3 schemas + 3 tests incl. P1) extends to 13 with the 3 P2R paths once implemented (fixture copies pin all13 + trackeds, commit as isolated source basis). No fixture-code execution in PhaseA; all above are read bindings for Astra approval.

### 6.3 Focused method plan (selected; final commands/counts after diff, no P1-36 transfer)

Efficient reuse: one Longform + one Weekly + one R1-Weakly fixture build shared across oracle methods in the same test process where snapshots permit; each capture/verify call wrapped in immediately-around `_snapshot` before/after (after setup/fault mutation, before cleanup). Oracles independent of implementation (filesystem hashes, P1 API refusal codes, `lstat` inventories), never self-derived expectations (no test mirrors `retained_sha == implementation_variable` without re-hash from disk; no `expected == capture_return["x"]` without file re-read).

Proposed focused methods (names indicative; count fixed after Astra-approved diff):

1. `test_longform_capture_verify_positive` — COPY+KEEP inventory/bytes, before≠proposed, old originals unchanged, only exact allowed retention delta added; `verify_retention` → `VERIFIED`; P1 `input_hashes` preserved in manifest `capture_inputs` + 2 P2R deps.
2. `test_weekly_capture_verify_positive` — same on Weekly envelope route.
3. `test_r1_active_capture_verify` — R1-predecessor fixture (ACTIVE origin, non-null active ref); proves checkpoint-vs-active distinction persists through retention.
4. `test_refuse_existing_retained_root` — empty dir + same-byte foreign files + dangling alias at `retained/` all refuse (`RETAINED_ROOT_EXISTS`), no writes, no P1 side effects.
5. `test_refuse_unsafe_paths` — ancestor alias, FIFO (prove no read via `SPECIAL` inventory, never open), out-of-root/traversal/overlap destination, malformed plan/manifest, omitted/extra/duplicate rows, unexpected files/dirs (even empty) → refuse/invalid, preflight cases with zero writes.
6. `test_drift_at_prefinal_seams` — inject State/control/proposal/staged/KEEP drift after P1 but before manifest publish; only injected + owned-output changes may remain; snapshot before any test cleanup; no cleanup in oracle; `FINALIZATION_REFUSED`/`REF_DRIFT`/`STABILITY_VIOLATION` as applicable.
7. `test_fault_short_write_close_readback_manifest` — short/write/close/readback + final-manifest faults (mocked `os.write/os.close` short/error + readback tamper + root-identity replacement via `lstat` swap); partials preserved + accurately classified (`WRITE_SHORT`/`CLOSE_FAILED`/`READBACK_MISMATCH`/`INCOMPLETE`/`INDETERMINATE`), live originals unchanged, subsequent `capture` refuses, `verify` rejects incomplete/bad.
8. `test_persistence_vs_eligibility` — after capture, mutate mutable live COPY original: `verify` may still succeed (persistence) while current eligibility expressly unproved (no P1 revalidation claim). Mutate retained COPY / required KEEP / bound proposal / staged reader → `verify` fails (`INVALID_RETENTION`). Exact manifest at wrong proposal path fails (same SHA ≠ path rebind).
9. `test_p1_refuses_after_capture_verify_without_p1` — unmodified P1 `validate_proposal` on same proposal after capture → `RETENTION_DEST_CONFLICT`; `verify_retention` succeeds without calling P1 or creating State authority. Ordinary P1 regressions only as affected (no decorative full-suite rerun).

Affected Gate/regression scope chosen after the implementation diff (not P1's 36). Snapshot equality is per-call evidence, not continuous proof. Concrete test commands/counts finalized post-diff for Astra review.

## 7. Complete patch / apply / evidence procedure (later, after Astra return — no action now)

- After Astra approves this interface, implementation creates a NEW independently byte-copied candidate worktree + whole available Git DB preserving P1 + apply copy (no hardlinks/alternates/shared objects; inert origin; sanitized routing `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`; validate every `.git` entry + config/remote; no new candidate branch/commit; fixtures may have meaningful independent history, never empty commits or reconstruct/Production DB writes).
- Save COMPLETE 16-path patch (13 P1 + 3 P2R) + independent application proof: apply directly to independent clean actual `409b292` (not layering old patches), check all16 bytes/modes + Git DB separation, never commit or active-index `add -N` (active source stays read-only; apply proof runs in disposable copy). Persist each runner/verifier BEFORE execution; never overwrite executed versions, failed raw outputs, or log names — fix to NEW version + NEW exclusive output names. Raw full source delta, pins/base/runtime/argv/env, pre/post status + cache observations saved; no filtered-status-only, no capture-at-run as static guard, no cleanup before comparison. Scripts are exact-run evidence, not general rerun tools.
- This PhaseA creates no patch, runs no tests, mutates no index.

## 8. Blockers

No concrete blocker to the 3A retention design. I1 chain resolves to unique `state:authority` COPY → retained State → exact `state.profile` → unique matching KEEP Profile (X Profile excluded, basename/current-State forbidden). I2 avoids `_Collector` wholesale via minimal local primitive + `input_hashes` binding + explicit mode/type/ancestor/inventory + exclusive-claim identity + manifest-last create/write/close/readback. I3 schema/results fit `2.0-rc1` + `EDITORIAL_RETENTION_V1` with strict unknown-field rejection, canonical `json_bytes`/`sha256_*`, no self-hash recursion, typed incomplete/invalid/indeterminate preserved. I4 fixtures/methods fit accepted-chain synthetic Longform/Weekly + R1 predecessor with no production/Human Gate. Any necessary change beyond 3A, any bound-Profile/history unresolvability, or any missing future-consumption identity discovered during implementation returns as exact blocker before scope expansion — none found in PhaseA.

---

**Request to Astra:** approve §2 API/return/error shapes, §3 Profile chain, §4 safe-read/snapshot/ownership (incl. no-temp + fd-identity), §5 schema/canonical/delta rules, §6 fixture/method plan, §7 patch/evidence procedure, or return concrete corrections. No code/tests until Astra return. STOP at Human Commit Point after this return; no subagents, commits, network, intake, or restoration.
