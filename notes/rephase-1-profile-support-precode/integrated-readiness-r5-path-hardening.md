# R5 — required path interfaces and source-pin correction

2026-10-31. Astra integration delta, documentation only. R4's two remaining readiness findings are addressed here. R3/R4, the focused kernel and previous reviews remain unchanged. This file overrides their conflicting signatures, fallback sentences and transcription errors; it is not implementation or a readiness verdict.

## 1. Binding source identities

- Selected decision INCLUDING §7: `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`,20472B.
- Contract ROOT INCLUDING §5: `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`,7225B.
- Final133 patch: `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260`,4931836B.
- Final133 manifest: `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa`,185422B.
- Fixed production baseline **commit**: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. This is not a SHA256 field.

R3/R4's patch strings missing `f3`, the mistyped baseline, and C/C-R2 header hashes are invalid transcriptions. They identify no alternative artifact. The literal closure inventories are consumed only with the corrected source binding above and actual membership checks, not those headers.

## 2. Public LOW signatures — exact final delta

All paths are normalized and checked repository-locally by the existing no-follow/binding rules. No supplied record collection, Context object or verified flag is added to these public interfaces. Required arguments reject `None`; they never infer a COPY from the logical LIVE State path or from a convenient directory basename.

The existing positional arguments remain in their existing order. These four signatures gain **required**, keyword-only path arguments:

```python
def build_revision_cards_views_from_paths(
    repo_root: Path, package_path: Path, request_path: Path,
    results_dir: Path, views_dir: Path, *, before_copy_path: Path,
) -> dict[str, Any]: ...

def accept_revision_evidence_views_from_paths(
    repo_root: Path, package_path: Path, results_dir: Path, views_dir: Path,
    profile_path: Path, evidence_accepted_root: Path, views_accepted_root: Path,
    *, request_path: Path, before_copy_path: Path,
) -> dict[str, Any]: ...

def build_versioned_ledger_from_paths(
    repo_root: Path, profile_path: Path, discovery_path: Path,
    screening_acceptance_path: Path, evidence_acceptance_path: Path,
    views_acceptance_path: Path, *, request_path: Path, before_copy_path: Path,
) -> dict[str, Any]: ...

def build_versioned_completeness_from_paths(
    repo_root: Path, profile_path: Path, discovery_path: Path,
    screening_acceptance_path: Path, evidence_acceptance_path: Path,
    views_acceptance_path: Path, ledger_path: Path, request_path: Path,
    old_completeness_path: Path, *, before_copy_path: Path,
) -> dict[str, Any]: ...
```

The ellipses here denote omitted **bodies only**, not unspecified parameters or behavior. R4's full content/return predicates apply. HIGH prepare supplies `request_abs` and the existing `state_copy = rev_root / "retention/state-before.json"` after that COPY was created and verified. All direct test calls in the R3/R4 census must supply the same explicit keywords from their actual fixture artifacts. No test-only fallback, auto-discovered request or optional authority context is permitted. Acquired DATA driver files are not edited.

Unchanged public positional interfaces:

- `derive_before_context(repo_root, request_path, before_copy_path, previous_checkpoint_path)` retains four required path arguments. The supplied previous path must equal the **ECP** from request `before_checkpoint.evidence` and COPY `checkpoint_provenance.evidence`, with its file SHA checked. It is never derived from Discovery provenance. The new D/S context loader does not replace or recursively re-enter the existing ECP content/lineage validation.
- `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir)` already has the required paths.
- `prove_revision_from_paths(repo_root, revision_manifest_path, decision_path, before_copy_path)` obtains the request path from the manifest's verified SizedRef and uses the required COPY path.
- `check_supersession_record_from_paths(repo_root, checkpoint_path, report_path, before_copy_path)` retains all four required arguments and verifies the supplied COPY against the checkpoint's bound retention layout and before-State SHA/size.

The new path loaders from R4 remain: `derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)` in LOW and `derive_current_root_effective_context(repo_root, request_path, live_state_path)` in HIGH. The former has a real pinned COPY; the latter runs only after HIGH's strict LIVE eligibility and before first COPY, with current bytes bound to the request. No fake future COPY.

## 3. Bound-checkpoint derivation — private adopted readback only

`_verify_adopted_graph_full(repo_root, checkpoint_path, checkpoint_sha)` retains its existing **three required arguments**. Remove R4's optional `before_copy_path` addition. It reloads and verifies the checkpoint at the supplied exact SHA, the request SizedRef, revision identity/root, and the retention-plan SizedRef plus manifest binding. Only then may it derive the fixed recorded layout `revision_root/retention/state-before.json`, verify its bytes against `before_state.sha256/byte_count`, and invoke the LOW D/S context loader.

This is a record-bound internal derivation, not a public missing-argument fallback. It never reads `request.before_state.path` for historical bytes. Every existing adopted-full caller (resolver, full checker, completion/postread) retains its three-argument call; the internal loader returns true R/E. Context recovery loads DCP/SCP and their ordinary reports/content only; it does not call adopted-full, completion or the full ECP lineage walker. Existing ECP/parent lineage validation runs in its existing outer phase, preserving the one-direction acyclic graph.

The ordinary report contract is exactly the record-owned Contract8/implementation comparison with canonical historical State **path only**. Do not execute the `core.contract_identity` fallback while validating a historical ordinary checkpoint with a supplied record contract. Additional schema-valid reviews are allowed; exactly one matching CORE_STAGE_CONTRACT row is required and every deterministic result ref is checked. FILE SHA and result-set digest remain distinct.

## 4. Screening expected-path semantics

`resolve_prepackage_root_effective(repo_root, state_path, discovery_path, accepted_discovery_path)` retains the R4 path-only interface. A `None` expected path means no additional caller expectation; the helper still discovers the canonical marker and State provenance itself. It never suppresses a present marker. If a non-None expected path is supplied, it must match the independently derived canonical/State-bound authority; foreign/missing/mismatched paths refuse.

R4's phrase “optional expected path missing” is limited to a supplied path whose target is missing, not permission to ignore a marker and not an unconditional refusal of `None` when a valid canonical marker exists. ENOENT alone denotes absence. Any symlink, nonregular, unreadable or malformed marker refuses. An accepted Discovery claim in State must bind the DCP/acceptance chain; missing or different claimed authority cannot enter the initial DIRECT case. The initial marker-present/pending case retains the specific existing preparation semantics described in R4 without claiming a passed Discovery checkpoint.

Return `authorityKind` and `basisMode` separately as in R4. Every path in the initial/marker/claimed-root table has the same unknown-type and per-parent loss preflight before the first directory/COPY write. Shared historical resolvers and their legacy direct-basis behavior are not changed by this new operation gate.

## 5. No semantic expansion

R4's corrected 4+1+3 closure formulas, closure-first residual order, ordinary3/5 versus DM0227 separation, new-run/idempotent/history distinction, literal closure membership and current-source proof obligations stand. No new schema/module/family, no old record rewrite, no default class or caller permission token. This delta closes the interface/transcription findings for re-review; code stays blocked until independent readiness and Astra confirmation.
