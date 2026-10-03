# DM-001/019 joint implementation — internal design milestone (analysis/design only, no code)

General Co-Worker, first internal milestone of the DM-001/019 joint unit.
Parent candidate **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`** only. No code,
no tests executed, no refs created, no old packets touched.

Tool note: the task permits creation via `apply_patch`; that function is not
available in this session, so the two new files in
`notes/rephase-1-dm001-019-implementation/design/` were created with the
session `write` tool (new files only, no other edits).

## 0. Verified source ground (read-only, this session)

All Git inspection used
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`, no
inherited Git-root overrides, no writes, no network, no rerun of
recovery/old suites/Summary intake.

| Object | Verified value |
|---|---|
| Candidate HEAD (live DB + restored copy) | `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3` |
| Tree (both DBs) | `657032438c6ed8b1c055d5a120b67b4b261a5092` |
| Direct parent (both DBs) | `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (fixed production baseline) |
| Live DB | `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`, `status --porcelain=v1 --untracked-files=no` empty, `status_exit=0` |
| Restored copy | `/tmp/opencode/jgas-recovery-restore-20261003T0445Z`, same HEAD/tree/parent, tracked-clean, `status_exit=0` |
| Reconstruct worktree | `066436d6d43a4fcf0b96ed1e8678e7f1edb082c2` (matches `066436d` prefix), tracked-clean |
| Runtime (evidence only, not executed) | `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python3.12` → `Python 3.12.14` |
| Authoritative identity binding | `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections2-identity-20261003T0944Z/final-identity-binding.json` (SHA256 `559512d3e48e0101af543fe1b36c0cfded0a1b6304837b1b5bac253c1eaed75e`, see `binding.md`); use the **corrected** `tests/test_survey_findings_v2.py` blob `6e179887284026d1fb6fc33522b5fb28afc4788e`, NOT the typo'd m2/m3-pretty `6e178887...` |

Line citations below are at b40 HEAD (`git show HEAD:<path>`,
`ls-files -s` confirms `scripts/survey_publication_v2.py`
`af760e198a5d64e2e3998d600b91404e21e27078` and
`scripts/survey_profiled_freeze_v2.py`
`27e5bcb1ee4f892d9a57a3dfdd99e6166f0e98d9`, both `100644`,
both in the untouched-Freeze-9 of the final binding).

## 1. Existing caller APIs (what must keep working)

### 1.1 Canonical lower-level builder — `scripts/survey_publication_v2.py`

- `release_identity(publication_profile: str, issue_id: str) -> str` (71–76):
  `WEEKLY_MAGAZINE → weekly/{issue_id}`, `LONGFORM_SPECIAL → special/{issue_id}`.
  Called once in-tree at 371 for the canonical manifest.
- `build_candidate(...)` (79–157): binds manuscript/bundle/reviews to exact
  bytes; writes via `_write_immutable` (62–68). Not changed by this unit.
- `validate_candidate(repo_root, path, *, issue_id)` (160–225): full
  revalidation incl. `REPOSITORY_FILE`-only PDF (197–204), review byte/page
  binding (206–222). Not changed except as a callee.
- `build_preview_approval(...)` (228–263) / `validate_preview_approval(...)`
  (266–280): approval binds candidate file SHA (270–272) and candidate PDF
  path/sha/page (274–279) but **does not require approval Candidate
  path+hash == the Candidate actually passed to `build_freeze`**. That gap is
  DM-001/019 defect D2 (see §6, witness W2).
- `build_visual_review(...)` (283–316): legacy post-approval record. Docstring
  291–295 already states new production must not require it before Freeze.
  Keep function for historical compat only; do not call it from either Freeze
  path.
- `validate_visual_review(repo_root, path, approval_path)` (319–327): legacy
  validator. Wrapper-only current use (profiled 87). To be removed from the
  Freeze path (defect D1).
- `build_freeze(repo_root, candidate_path, approval_path, frozen_at, freeze_path,
  release_manifest_path)` (330–383): current canonical path.
  Visual authority 341–346 resolves `candidate["visual_review"]["path"]` and
  calls `reader.validate_review_record(..., expected_kind="VISUAL")` — this is
  the correct Candidate-bound pre-preview VISUAL authority to keep.
  Gap: authority check 347–348 compares **PDF SHAs only**
  (`candidate.pdf.sha256 == approval.pdf_sha256` and
  `review.pdf.sha256 == approval.pdf_sha256`); no Candidate path+hash equality.
  Freeze payload 349–365, `_write_immutable` 367, manifest 368–380 (identity
  via `release_identity(profile, issue_id)` at 371), `_write_immutable` 382.
  Gap: both-target preflight missing — freeze is installed before manifest
  conflicts are checked; same-path/alias/symlink/nonregular handling relies on
  generic `_safe_file`/`_rel` only at validation time, not as an explicit
  pre-write gate (defect D4).
- `validate_release_manifest(...)` (386–410): genuine consumer; checks
  freeze-SHA bind (388–390), manifest↔freeze field equality (392–394), source
  drift (395–397), candidate-SHA drift (398–400), candidate↔manifest PDF
  (401–407), freeze visual == candidate visual (408–409). **Reuse as-is** as
  the post-write consumer oracle; wrapper currently calls it after both writes
  (profiled 135), which is too late to prevent the partial write — preflight
  must move before either write (§3).
- `_rel` (31–37), `_safe_file` (40–45), `_authority` (48–50),
  `_validate_authority` (53–59), `_write_immutable` (62–68, returns `Path`,
  same-payload equality → return, divergent → `ValueError`).

### 1.2 Wrapper builder — `scripts/survey_profiled_freeze_v2.py`

- `public_issue_slug(profile)` (25–32): `Path(survey_root).name` with
  empty/`.`/`..`/slash guards. Pure (no imports beyond `pathlib`).
- `release_identity(profile)` (35–42): slug + profile-gated
  `weekly/{slug}` / `special/{slug}`. Pure. Name collides with
  `publication.release_identity(str, str)` — keep both names stable for the
  release workflow (see §1.4) or rename only via thin alias with compat
  shims; decision point for Astra (§9).
- `_safe_state_profile(repo_root, cfg, state_path)` (45–59): loads State,
  `agent.validate_agent_state` (47–49), requires `RELEASE_CANDIDATE` (50–51)
  and `human_gates.publication_preview == "approved"` (52–53), checks current
  Profile path+SHA (54–56), returns `(state, profile_path, profile,
  source_root)`. **Must not be stubbed in tests** (§5).
- `_write_immutable(path, payload, label)` (62–67): same semantics as
  canonical but returns `None`. Consolidate to one shared implementation.
- `build_profiled_freeze(repo_root, cfg, state_path, frozen_at)` (70–136):
  fixed output locations `publication_root = source_root/"publication/v2"`,
  `candidate_path = .../publication-candidate-v2.json` (78),
  legacy `visual_path = .../visual-review-v2.json` (79),
  approval from `state.human_gate_provenance.publication_preview` (80–83),
  `validate_candidate` (85) + `validate_preview_approval` (86) +
  `validate_visual_review` legacy (87) + bundle (88–89) + current-Profile bind
  (90–92) + profile-match (93–94) + PDF-only chain (95–96), then freeze write
  (100–118), manifest write (120–134, identity 123), final
  `publication.validate_release_manifest` (135). Defects: D1 legacy visual
  (79/87), D2 same PDF-only gap inherited (95–96), D3 internal-issue tag vs
  slug resolved correctly here via `release_identity(profile)` (123) but
  canonical still uses `release_identity(profile_str, issue_id)` (pub 371) —
  joint contract requires both to agree via one validated slug authority (§2),
  D4 late consumer (135) after two writes (118/134), D5 no joint
  Candidate-path+hash gate.
- `main()` CLI (139–158): thin wrapper over `build_profiled_freeze`; unchanged.

### 1.3 Import graph constraint (no circular imports)

```
survey_publication_v2.py imports: core, quality, reader, schema_gate (17–20)
survey_profiled_freeze_v2.py imports: agent, core, publication, quality, schema_gate (18–22)
survey_agent_control_v2.py imports: ..., publication, ... (line 34)
```

`agent → publication` already exists, so **`publication` must never import
`agent`** (would cycle `publication ↔ agent`). `profiled` already imports both.
Consequences:

- Pure slug authority (`public_issue_slug`, profile-based identity) **moves
  into `publication`** (leaf position: depends only on `core`/`pathlib`,
  no `agent`/`profiled` import). `profiled` re-exports thin compat wrappers
  so the release workflow and existing tests keep importing from `profiled`.
- State-gated preflight (`validate_agent_state`, lifecycle, Human gate,
  current-Profile/bundle checks) **stays in `profiled`** (the only module that
  may import `agent`). Canonical `build_freeze` takes already-resolved
  `(candidate, approval, profile, frozen_at)` inputs and never imports `agent`.
- Shared byte-level helpers (authority resolution, payload constructors,
  both-target preflight, installing writer) **live in `publication`** and take
  plain `Path`/`dict`/`datetime` arguments — no `agent`, no `profiled`, no
  State. Both builders call them. No new module, no generic framework.

### 1.4 Other callers that pin the interface

- Release workflow `.github/workflows/survey-production-v2-release.yml`
  59–103: genuine downstream consumer. Lines 84/96–97 already implement the
  joint identity predicate: `public_slug=profiled.public_issue_slug(profile)`,
  `expected_tag=profiled.release_identity(profile)`, `tag=manifest.tag`,
  `tag != expected_tag → SystemExit`. Also checks FROZEN State (79),
  `validate_agent_state` (80–81), Profile SHA (82–83), manifest SHA dispatch
  bind (87), `validate_release_manifest` (88), candidate revalidation (90),
  Candidate/Profile publication match (92). **No workflow change proposed** —
  the workflow predicate becomes the unmocked consumer oracle in tests (§7,
  method F-C3 re-executes lines 82–97 logic in-process; no live Actions).
  Existing `test_release_workflow_rederives_tag...` (profiled-test 34–42)
  asserts these exact lines; keep it green.
- Stage `scripts/survey_stage_validation_v2.py` RELEASE_CANDIDATE 575–596:
  requires Candidate pre-preview visual identity (582–585), exact
  Candidate/approval/visual binds (588–593), PDF-chain agreement (594–595).
  **No stage change proposed** — it is the genuine `FROZEN` consumer oracle
  (§7, methods S-1/S-2). Existing freeze-boundary tests already cover it.
- `agent.approve_publication_preview`, `build_stage_checkpoint`,
  `advance_with_checkpoint`, `validate_agent_state`, `revalidate_publication_surface`
  are callers/fixtures only; unchanged.

## 2. Shared-helper / interface plan (budget: two runtime files, no new framework)

All new shared code goes in `scripts/survey_publication_v2.py` (leaf).
`scripts/survey_profiled_freeze_v2.py` deletes its duplicates and calls the
shared helpers, adding only the State-gated wrapper preflight it alone may
own. Names below are proposed; Astra may rename but the placement and arity
are the design.

### 2.1 Slug authority consolidation (DM-019 core)

In `publication` (new, pure, no new imports):

```python
def public_issue_slug_from_profile(profile: dict[str, Any]) -> str
    # exact move of profiled.public_issue_slug lines 25–32

def profile_release_identity(profile: dict[str, Any]) -> str
    # exact move of profiled.release_identity lines 35–42, but named to avoid
    # collision with existing publication.release_identity(str, str) (71–76)

def require_convergent_release_identity(*, candidate_publication_profile: str,
    candidate_issue_id: str, profile: dict[str, Any]) -> str
    # returns profile_release_identity(profile); raises unless it equals
    # release_identity(candidate_publication_profile, candidate_issue_id)
    # for convergent cases. For divergent-but-valid cases (Retrospective
    # SP-2025-H2 → special/2025-H2) the caller passes the validated profile
    # and this function returns the profile-derived tag WITHOUT falling back
    # to issue_id; canonical build_freeze must then take the tag as an
    # explicit parameter (see §2.3) instead of recomputing from issue_id.
```

In `profiled`, replace bodies with compat shims (no logic duplication):

```python
def public_issue_slug(profile): return publication.public_issue_slug_from_profile(profile)
def release_identity(profile): return publication.profile_release_identity(profile)
```

Rationale: release workflow imports `profiled.public_issue_slug /
release_identity` (workflow 63/84); existing tests import `profiled.*`
(profiled-test 25–32). Shims keep those call sites stable while slug truth
lives in exactly one place. No caller-supplied tag/slug parameter is added
anywhere — no arbitrary override, per contract §4.

Open Astra choice (§9): whether canonical `build_freeze` keeps computing
`release_identity(profile_str, issue_id)` internally (then divergent Special
fixtures fail closed, which is wrong for Retrospective) or takes an explicit
validated `release_identity: str` argument. Design recommends the latter with
both builders deriving it from the same validated Profile object (see §2.3).

### 2.2 Authority resolution helpers (shared, both builders)

In `publication` (new, thin wrappers over existing `_rel`/`_safe_file`/
`_validate_authority`/`repo_local_path` semantics — no behavior change to
those primitives):

```python
def resolve_candidate_visual(repo_root, candidate: dict) -> tuple[Path, dict]
    # _safe_file(repo_root / candidate["visual_review"]["path"]) then
    # reader.validate_review_record(..., expected_kind="VISUAL") (cf. pub 341–346).
    # Raises on missing/legacy-substituted visual BEFORE any write.
    # Rejects: wrong kind (SEMANTIC passed as visual), stale/drifted bytes
    # (validator 556–623 raises), legacy post-approval file (schema/kind mismatch).

def require_exact_approval_candidate(*, repo_root, candidate_path: Path,
    candidate: dict, approval: dict) -> None
    # NEW joint gate (closes D2): approval["publication_candidate_path"] must
    # equal _rel(repo_root, candidate_path) AND approval["publication_candidate_sha256"]
    # must equal sha256_file(candidate_path). Same PDF bytes with a different
    # Candidate path/hash → ValueError before writes. Keeps existing PDF-chain
    # checks (pub 347–348 / profiled 95–96) as additional gates, not replacements.
```

Both builders call both helpers. Canonical keeps its 341–348 logic but routed
through these two functions so wrapper and canonical share one oracle.

### 2.3 Payload constructors (pure, byte-deterministic)

In `publication` (new, extracted verbatim from current inline dicts):

```python
def build_freeze_payload(*, repo_root, candidate_path, candidate, approval_path,
    approval, visual_path, frozen_at) -> dict
    # exact current pub 349–365 shape; adds publication_candidate_path/sha from
    # the ACTUAL candidate_path args (not from approval), visual path/sha from
    # the resolved Candidate-bound visual. Schema-validated by caller.

def build_manifest_payload(*, repo_root, freeze_path, freeze_sha256: str,
    release_identity: str, source_path, source_sha256, pdf_path, pdf_sha256,
    page_count, issue_id) -> dict
    # exact current pub 368–380 / profiled 120–132 shape; freeze_record_sha256
    # passed explicitly (see §3.2) so Manifest hash is always over the true
    # installed Freeze bytes.
```

`build_freeze` signature change (requires Astra approval, §9): add explicit
keyword `release_identity: str | None = None`? Recommended: **required**,
derived by caller from the validated Profile via `profile_release_identity`.
Wrapper passes `profile_release_identity(profile)` after asserting
`_safe_state_profile` + bundle binds current Profile (profiled 88–94 stay).
Canonical caller (direct `publication.build_freeze` use + tests) passes the
same function over the same validated Profile object. Convergent Weekly and
convergent/divergent Special then agree by construction; divergent canonical
tag (old pub-371 issue-based behavior) disappears. If Astra prefers
zero-signature-change, alternative is internal `require_convergent...`
assertion only — but then Retrospective divergent fixtures cannot pass; that
limitation must be recorded as a bounded exclusion, not silently overridden.

### 2.4 Writer preflight + installing writer (shared, both builders)

Single shared implementation in `publication`, replacing both private
`_write_immutable` copies:

```python
def preflight_freeze_install(*, repo_root, freeze_path: Path, manifest_path: Path,
    freeze_payload: dict, manifest_payload_without_freeze_sha: ..., ) -> None
    # ALL predictable checks BEFORE either target write (§3.1 checklist).
    # Pure validation + target-conflict inspection; performs NO writes.

def install_freeze_pair(*, repo_root, freeze_path, manifest_path,
    freeze_payload, manifest_payload_factory, ...) -> tuple[Path, Path]
    # Calls preflight, then installs freeze, re-reads freeze bytes for
    # freeze_sha256, finalizes manifest payload, installs manifest.
    # Exclusive no-overwrite creates + bounded owned-file failure handling (§3.3).
```

`profiled.build_profiled_freeze` keeps its State/bundle/approval-drift gates
(76–96, with 87 swapped to shared `resolve_candidate_visual` + 95–96 plus
`require_exact_approval_candidate`), then delegates payload+preflight+install
entirely to the shared functions. No second writer implementation.

## 3. Writer contract (preflight before either write; byte-exact hashes)

### 3.1 Preflight checklist — every item BEFORE the first target byte

Given resolved `(candidate, approval, visual, profile, release_identity_tag,
freeze_payload, manifest_fields)` and repo-relative target refs:

1. **Authority validity**: `validate_candidate` + `validate_preview_approval`
   + `resolve_candidate_visual` + `require_exact_approval_candidate` +
   `require_convergent_release_identity` (or explicit-tag path) all pass.
   Malformed/stale/wrong-kind/wrong-issue/mixed-Candidate/divergent-identity
   → `ValueError`, no target touched.
2. **Slug validity**: `public_issue_slug_from_profile` + profile
   `publication_profile` gate pass; missing/unsupported/empty slug →
   `ValueError`, no write.
3. **State/lifecycle/Human-gate/quality (wrapper only)**:
   `_safe_state_profile` (RELEASE_CANDIDATE + approved Preview + current
   Profile SHA) + bundle-current-Profile bind + publication-identity match
   (profiled 88–94) pass; else `ValueError`, no write. Canonical path has no
   State (unchanged); its callers supply the validated Profile explicitly.
4. **Both-target conflict scan** (new, the D4 fix): for each of
   `freeze_path`, `manifest_path`:
   - Resolve repo-relative ref via `_rel`-equivalent; reject absolute,
     traversal (`..`), backslash, empty (same rules as
     `repo_local_path` 215–231).
   - `samepath`: if both refs resolve to the same filesystem object →
     `ValueError` before either write.
   - `input-alias`: if either target resolves (`Path.resolve()`) to the same
     object as any input authority file (candidate/approval/visual/source/pdf/
     profile/bundle/manuscript) → `ValueError`.
   - `symlink`: if the target itself is a symlink OR any existing parent
     component resolves outside `repo_root` → `ValueError`. (Current
     `_safe_file` 40–45 covers inputs; targets need the same treatment
     pre-write because `core.write_json` 90–92 does `mkdir(parents=True)` +
     `write_bytes` with no symlink check.)
   - `existing nonregular`: if target exists and is not a regular file
     (dir, fifo, socket, symlink) → `ValueError`.
   - `existing conflicting bytes`: if target exists as a regular file and
     `core.load_json(target) != intended_payload` → `ValueError`
     (`refusing to overwrite divergent ...`, preserving current semantics).
     If equal → idempotent resume path (§3.2), still subject to the
     freeze→manifest hash chain.
   - Manifest-specific: manifest payload cannot be finalized until freeze is
     installed (freeze SHA unknown); preflight therefore checks the manifest
     target conflict against the *shape* (path validity + existing-byte
     compatibility if a manifest already exists: if existing manifest bytes
     exist and are fully equal to the would-be final payload they are
     resume-compatible, else preflight does NOT fail yet — the post-freeze
     equality gate (§3.2) decides; but a manifest that already exists with
     bytes that cannot possibly equal any final payload given the frozen
     inputs, e.g. wrong `issue_id`/`release_identity`, fails preflight).
5. **Schema pre-validation**: `schema_gate.validate_instance` on the freeze
   payload AND on the manifest payload shape (with a placeholder freeze SHA
   replaced post-freeze; or validate manifest shape minus `freeze_record_sha256`
   pre-write and full manifest post-freeze — implementation detail, but both
   validations must pass before the first write; a schema-invalid payload must
   never leave a half-installed freeze behind).

Any preflight failure → both targets and State unchanged (verified by
before/after byte assertions in tests, §7).

### 3.2 Exact serialized bytes + hash chain (first create vs retry)

- Serialization is `core.json_bytes` (86–87): `json.dumps(ensure_ascii=False,
  indent=2) + "\n"` → UTF-8. File hash is `core.sha256_file` (99–100) over
  those exact bytes. No canonicalization beyond this; tests compare
  `path.read_bytes()` equality, not parsed-JSON equality, for the
  equivalence oracle.
- **First create**: `install_freeze_pair` (a) preflights (§3.1), (b) installs
  freeze bytes via exclusive create (§3.3), (c) reads back
  `freeze_sha256 = sha256_file(freeze_path)` from disk (not from memory),
  (d) finalizes `manifest["freeze_record_path"] = rel(freeze_path)`,
  `manifest["freeze_record_sha256"] = freeze_sha256`, (e) schema-validates
  full manifest, (f) installs manifest bytes via exclusive create,
  (g) runs `validate_release_manifest` as post-condition. Manifest hash
  correctness follows because the manifest file bytes embed the on-disk
  freeze SHA.
- **Same-payload retry (idempotent)**: if freeze target already exists with
  byte-identical content (`read_bytes() == json_bytes(freeze_payload)`),
  skip freeze install (resume). Re-read freeze SHA from disk regardless.
  Finalize manifest; if manifest target already exists byte-identical → skip
  install, return. If either exists with divergent bytes → `ValueError`
  (preserve current `_write_immutable` refusal; no delete/overwrite of
  pre-existing authority as recovery).
- **Partial-write resume**: freeze exists identical + manifest missing →
  install manifest only. Freeze missing + manifest exists (any bytes) →
  `ValueError` before writing freeze (manifest-first state is never produced
  by this writer; its presence indicates foreign/pre-existing authority —
  do not delete it, do not install a freeze under it). Freeze identical +
  manifest divergent → `ValueError`, leave both unchanged.
- Equivalence oracle (contract §4 row 4): same inputs + same `frozen_at` +
  same output refs → `freeze.read_bytes()` and `manifest.read_bytes()`
  byte-identical across both builders. If separate output paths are required
  by a test, compare parsed authority fields plus only the declared
  `freeze_record_path` rebinding — never normalize identity/hashes/review refs.

### 3.3 Exclusive creates + bounded install-time failure handling (owned files only)

Current `core.write_json` (90–92) is `mkdir + write_bytes`: non-atomic,
follow-symlinks, truncate-overwrite. The joint fix stays within the two-file
budget by adding a small exclusive-create helper in `publication` (no new
module, no global CAS):

```python
def _install_owned_json(path: Path, data: bytes) -> None
    # Preconditions (already preflighted): parent chain validated, no symlink
    # escape, no input-alias, target absent OR byte-identical (handled by caller).
    # Semantics: open(path, "xb") exclusive; on FileExistsError re-read and
    #   compare: identical → treat as resume (no write); divergent → ValueError.
    #   Convert data via core.json_bytes upstream so hash chain stays exact.
    # Parent dirs: create with mkdir(parents=True) ONLY after validating no
    #   existing parent component is a symlink escaping repo_root.
```

Failure handling (explicit, bounded, no global-crash-atomicity claim):

- Predictable validation/conflict failures (§3.1): raised before either
  write; tests assert both targets' before/after bytes unchanged + State file
  bytes unchanged.
- Install-time I/O failure injection (§4): `OSError` during freeze install →
  freeze target absent-or-untouched (exclusive create never truncated a
  pre-existing file), manifest never attempted; `OSError` during manifest
  install → freeze installed (owned, byte-verified), manifest absent-or-untouched,
  error propagates with a resume-safe message; retry with identical inputs
  resumes per §3.2. Cleanup rule: the writer removes **only files it created
  in this call** (tracked by existence-before-call probe) and only when they
  are byte-identical to the intended payload and the install did not complete;
  it never deletes/truncates pre-existing divergent authority, never deletes
  inputs, never touches State. Partial-install tests assert exactly this.
- What is NOT claimed: no global CAS, no crash-atomicity across the pair,
  no cross-process locking, no fsync/dir-fsync durability promise. Two-file
  atomicity is explicitly out of scope; the contract is fail-closed +
  resume-idempotent, matching the release workflow's
  `VERIFY_EXACT_BYTES_THEN_RESUME` (workflow 70) and FROZEN `max_attempts: 2`
  retry (workflow 72 / config FROZEN `retry_policy`).

### 3.4 Preserved guards (non-negotiable)

- Wrapper keeps: `validate_agent_state` non-empty → fail (profiled 47–49,
  real function, no stub); `RELEASE_CANDIDATE` (50–51); approved Preview
  (52–53); approval drift (82–83); bundle-current-Profile (90–92);
  publication-identity match (93–94). Canonical keeps: full candidate/review
  revalidation, `REPOSITORY_FILE`-only PDF (pub 197–204), review byte/page
  binds (206–222), approval candidate-SHA + PDF binds (270–279).
- No new caller-supplied tag/slug/authority override parameter except the
  explicit validated-Profile-derived `release_identity` threading (§2.3),
  which is itself validated, not trusted.

## 4. Failure-injection plan (real write boundary, no authority/Git mocks)

Allowed: monkeypatch/file-system-level fault injection **at the real write
boundary only** (`pathlib.Path.write_bytes` / `open(..., "xb")` / the new
`_install_owned_json`), plus real pre-existing conflicting files. Forbidden:
mocking `validate_candidate`, `validate_preview_approval`,
`validate_review_record`, `validate_bundle`, `validate_agent_state`,
`_safe_state_profile`, `sha256_file`, Git success, or State-pass results.

Concrete cases (each asserts before/after bytes of both targets + State):

1. `I-FREEZE-IO`: make freeze parent read-only (chmod) or inject `OSError`
   on first `open(freeze,"xb")` → expect `OSError`/`ValueError`, freeze
   absent-or-unchanged, manifest absent-or-unchanged, State unchanged; retry
   after restoring perms with identical inputs succeeds with identical bytes.
2. `I-MANIFEST-IO`: allow freeze install, inject `OSError` on manifest
   `open(...,"xb")` → freeze present with exact expected bytes + SHA,
   manifest absent-or-unchanged; identical-input retry installs manifest and
   both files then equal the uninterrupted-run bytes.
3. `I-PARTIAL-RESUME`: hand-craft freeze-identical + manifest-missing state
   (by running vietor then deleting manifest in fixture setup — fixture-owned
   files only) → retry installs only manifest, final bytes equal
   uninterrupted run.
4. `I-DIVERGENT-FREEZE` / `I-DIVERGENT-MANIFEST`: pre-existing divergent
   regular files at either target → `ValueError("refusing to overwrite
   divergent ...")` before any write to the other target (preflight §3.1-4);
   both targets unchanged.
5. `I-SYMLINK-TARGET` / `I-SAMEPATH` / `I-INPUT-ALIAS` / `I-NONREGULAR`:
   symlink target, freeze==manifest path, target aliasing candidate/approval,
   directory at target path → `ValueError` pre-write, nothing installed.

All injection tests use `tmp_path`-style isolated Git-less fixture roots
under the test's own temp dir (repo_root = fixture root, real
`core.write_json`/`sha256_file` semantics), plus one full Git-fixture
variant for the wrapper path (§5) to prove `_safe_state_profile` interlock.

## 5. Fixture plan (real validators, no `_safe_state_profile`/`validate_agent_state` stubs)

### 5.1 Reused fixtures — validity and current-field risks

- **Weekly synthetic positive base**: reuse
  `tests/test_survey_publication_revalidation_v2.py::Fixture`
  (constructor 50ff, `survey_dirname="survey"` default 50/469–471) via the
  same `importlib` pattern as
  `tests/test_survey_freeze_stage_boundary_v2.py` (17–30). It builds real
  manuscript/bundle/SEMANTIC+VISUAL reviews/surface-gate with real
  `reader.build_*` + `quality.build_bundle` (fixture `_publication_authority`
  ~318–400), real PDF via `pypdf.PdfWriter` (`_write_pdf`), and real
  checkpoint/State chains. **Known risk**: default `survey_dirname="survey"`
  means `profile.paths.survey_root` basename is `"survey"`, NOT the issue id;
  `public_issue_slug` would yield `"survey"` and any wrapper-derived
  `expected_tag` would be `weekly/survey`. The existing revalidation fixture
  never calls the wrapper so this never mattered. New wrapper tests MUST
  construct the fixture with an issue-matching `survey_dirname` (e.g.
  Weekly `2026-W35` → `survey_dirname="2026-W35"`, or a `surveys/weekly/...`
  tree) OR explicitly assert the derived tag from the actual
  `survey_root` basename rather than assuming `weekly/{ISSUE}`. Prefer the
  former (faithful production shape: profile `_profile` in
  `test_survey_publication_v2.py` 54–109 uses
  `surveys/{weekly|special}/{issue_id}`). The one existing
  `survey-special` variant (revalidation-test 706) proves the parameter works.
- **Thematic Special full-authority base**: reuse
  `tests/test_survey_publication_v2.py::_candidate(issue_id="SP001",
  research_profile="THEMATIC", publication_profile="LONGFORM_SPECIAL")`
  (255–369): builds real profile/architecture/bundle/reviews/candidate with
  longform source (`_longform_fixture_source` 236–253), 12-page real PDF
  (`_fixture_pdf` 42ff), profile-bound review checks (`_review_checks`
  196–235, incl. `LONGFORM_MIXED_LAYOUT` evidence). This is the convergent
  Special fixture (`survey_root=surveys/special/SP001` → slug `SP001` →
  `special/SP001`, matching issue-based canonical tag). Valid for both
  positive equivalence and mixed-Candidate negatives.
- **Divergent Special (Retrospective)**: no full publication-authority
  fixture exists at b40. `test_survey_publication_v2.py::_profile` supports
  `RETROSPECTIVE_PERIOD` (temporal `BOUNDED_PERIOD` 59–65) and
  `_review_checks` covers Retrospective semantics (498–512:
  `REQUIRED_SYNTHESIS_SURVIVAL`, `LONGFORM_TECHNICAL_DEPTH`), and the
  profiled unit test proves slug divergence
  (`SP-2025-H2` + `surveys/special/2025-H2` → `2025-H2`/`special/2025-H2`,
  profiled-test 21–26). But `_candidate` for Retrospective has no proven
  manuscript/review/bundle chain (fidelity `validate_review_depth`,
  architecture coverage, and check-family gates at reader 620–633 may need
  Retrospective-specific requirements). **Explicitly bounded**: Retrospective
  gets (a) pure slug/identity unit coverage via real `core.validate_profile`
  + shared slug helpers, plus (b) ONE attempted full-chain wrapper test
  marked as feasibility probe — if `DM-016` (upstream Thematic source-class
  admission) or `DM-017` (obligation completeness) blocks valid
  manuscript/review construction, the test records the concrete validator
  error as an upstream-blocker result and the design returns that boundary
  to Astra instead of broadening scope (per contract §4 / §77: return the
  concrete boundary, no filesystem scanning, no backlog repair). No
  Retrospective FROZEN-consumer claim without that chain.
- **Canonical output comparison risk**: revalidation `Fixture` pins
  `contract.*_sha256 = "0"*64` (fixture `_profile` contract block) and
  `repository_commit_sha` from the live repo; wrapper tests must not assert
  State/contract bytes across repos — assert only Freeze/Manifest bytes +
  `release_identity` + validator acceptance, and run the real workflow
  predicate (release 82–97) against the fixture's own Profile/Manifest
  objects rather than golden files.

### 5.2 New fixture work (minimal, in focused test files only)

- Extend the revalidation-`Fixture` import pattern with a wrapper-ready
  helper: `advance_to_release_candidate_via_real_stage()` =
  freeze-boundary `build_candidate_and_advance` (freeze-boundary-test
  ~50–103: `build_candidate` → `validate_stage` → `build_stage_checkpoint` →
  `advance_with_checkpoint` → `RELEASE_CANDIDATE`/`HUMAN_GATE_REACHED`) then
  `agent.approve_publication_preview(...)` (real Human-gate transition, cf.
  freeze-boundary `approve_and_build_freeze` 105–127). This exercises the
  genuine `_safe_state_profile` path: real `validate_agent_state`,
  real lifecycle, real approval provenance. **No stubbing of either
  function** — tests that need failure modes mutate real fixture files
  (drift bytes, break Profile SHA, unlink approval) and assert the real
  validator's error.
- Special fixtures: add `thematic_convergent` (SP001 via `_candidate`) and
  `retrospective_divergent_probe` (SP-2025-H2-shape via `_profile` +
  attempted `_candidate`-equivalent chain) builders in the new focused test
  module, reusing `test_survey_publication_v2.py` helpers by import (same
  pattern as freeze-boundary 17–30), not by copy-paste.
- All fixture I/O under per-test temp dirs (`tempfile.TemporaryDirectory(dir=root)`
  as in existing tests); no fixture objects in reconstruct's DB; no
  production-State writes.

## 6. Parent defect witnesses (pre-repair failures, exact oracles)

Each witness runs at b40 **before** the fix (expected failure recorded), then
re-runs post-repair expecting the corrected behavior (§7). Oracles are
`ValueError`/`StageValidationError` message regexes + before/after byte
equality (both targets + State unchanged on rejection).

- **W1 — legacy visual rejection + residuals.** Setup: valid Weekly fixture
  advanced to `RELEASE_CANDIDATE` + approved Preview. Call current
  `profiled.build_profiled_freeze`: passes today by consuming legacy
  `visual-review-v2.json` via `validate_visual_review` (profiled 79/87).
  Witness A (pre-repair characterization): delete the Candidate-bound
  pre-preview visual file but keep legacy file → current wrapper still
  succeeds (proves legacy dependence). Witness B (residual): supply a legacy
  file whose PDF SHA diverges from approval → fails only at 95–96 with
  `"Freeze exact-PDF authority chain diverged"` AFTER no writes yet today
  (writes happen later) — record that the gate is PDF-only, not authority
  identity. Post-repair oracle: wrapper with legacy-only (no Candidate-bound
  visual) → `ValueError` matching `"Candidate pre-preview visual"` (new
  `resolve_candidate_visual`) before either write; both targets + State
  byte-unchanged. Stage consumer (stage 582–585) already rejects swapped
  visuals (`"must be the Candidate pre-preview Visual Review"`,
  freeze-boundary-test `wrong` subcase) — keep that test green as the
  independent residual guard.
- **W2 — mixed valid Candidate, same PDF.** Setup: two individually valid
  Candidates C1≠C2, same `issue_id`, same publication profile, byte-identical
  PDFs (copy `main.pdf` bytes to a second source tree with distinct
  `main.tex` history → distinct `candidate_sha256`/file-SHA, identical
  `pdf_sha256`). Approval A1 bound to C1. Call `publication.build_freeze(C2,
  A1, ...)` and `profiled.build_profiled_freeze` with C2 installed at the
  wrapper's fixed candidate path + A1 in State provenance. Pre-repair:
  both succeed (PDF-only checks 347–348 / 95–96 pass) — record as defect
  demonstration (rejected contract: post-repair "both PASS mixed" is NOT
  acceptable). Post-repair oracle: both builders raise `ValueError`
  matching `"approved Candidate.*path|publication_candidate"` (new
  `require_exact_approval_candidate`) before either write; targets + State
  unchanged.
- **W3 — divergent canonical identity (DM-019).** Setup: Retrospective-shape
  profile (`issue_id=SP-2025-H2`, `survey_root=surveys/special/2025-H2`) with
  a valid full chain if feasible (§5.1), else Thematic-convergent profile
  mutated so `survey_root` basename ≠ issue. Call canonical
  `publication.build_freeze` (issue-based tag, pub 371) and compute wrapper
  tag via `profile_release_identity`. Pre-repair: tags differ
  (`special/SP-2025-H2` vs `special/2025-H2`) while both builders
  individually succeed — canonical stage/Release predicates that compare
  against Profile slug would then fail downstream (release 96–97
  `Release Manifest public identity mismatch`; stage equivalent). Record the
  canonical divergent tag as the **pre-repair witness**, NOT desired behavior
  (contract §72 row 3). Post-repair oracle: both builders emit identical
  `release_identity == special/2025-H2` (profile-derived), byte-equal
  manifests for same `frozen_at`; the old issue-based tag is gone. If the
  full Retrospective chain is blocked upstream, W3 reduces to the pure
  slug-witness + convergent Special equivalence, with the block recorded.
- **W4 — existing-manifest partial write.** Setup: valid Weekly fixture.
  Pre-existing divergent `release-manifest-v2.json` bytes at the wrapper's
  fixed manifest path (simulating a prior partial/foreign install), then call
  current `profiled.build_profiled_freeze`. Pre-repair: freeze is installed
  (118) BEFORE the manifest conflict surfaces at final validation (135 →
  pub 408–409), leaving a half-installed pair — assert freeze appeared while
  manifest raised. Post-repair oracle: `ValueError` matching
  `"refusing to overwrite divergent Release manifest|manifest conflict"`
  raised by preflight (§3.1-4) with NEITHER target created/modified
  (freeze absent-or-unchanged, manifest unchanged, State unchanged).

## 7. Exact per-method test plan (no execution in this milestone)

New focused module(s) only, e.g.
`tests/test_survey_dm001_019_freeze_equivalence_v2.py` (+ minimal edits to
existing fixture helpers if needed — no existing test semantics changed).
Each method uses real validators/real files; artifact oracles are
`read_bytes()` comparisons; no-write oracles assert before/after
`sha256_file` equality of both targets + State. `frozen_at` fixed per test
(`T0 + delta`, cf. freeze-boundary tests).

**Lower-level canonical (`publication.build_freeze`, shared helpers):**

- `L-1 positive Weekly`: valid Weekly chain (revalidation Fixture,
  issue-matching survey dirname) → `build_freeze` succeeds; assert
  `validate_release_manifest` passes, freeze bytes embed exact
  candidate/approval/visual path+SHA, manifest `freeze_record_sha256 ==
  sha256_file(freeze)`, `release_identity == weekly/{ISSUE}`.
- `L-2 positive Thematic Special convergent`: SP001 `_candidate` chain →
  same assertions with `special/SP001`; assert wrapper-built pair (W-1) has
  byte-identical freeze+manifest for same `frozen_at` (equivalence oracle).
- `L-3 negative legacy-only visual`: remove Candidate-bound visual, leave
  legacy file → `ValueError` pre-write (W1 post-repair oracle); targets+State
  unchanged.
- `L-4 negative mixed Candidate same PDF`: W2 setup → `ValueError`
  (Candidate path+hash gate); targets+State unchanged.
- `L-5 negative divergent identity`: divergent-slug fixture → canonical
  emits profile-derived tag (W3 post-repair); old issue-tag bytes absent
  (compare against pre-repair golden captured in W3, not against live run).
- `L-6 writer conflict matrix`: divergent freeze / divergent manifest /
  samepath / input-alias / symlink / nonregular (each a subcase, cf. §4
  I-cases at unit level for canonical paths) → `ValueError` pre-write,
  nothing installed.
- `L-7 same-payload retry`: run L-1 twice identical → second run returns same
  paths, bytes unchanged, exit normal (idempotent).
- `L-8 install-failure resume`: §4 I-FREEZE-IO / I-MANIFEST-IO /
  I-PARTIAL-RESUME against canonical entry points.

**Wrapper (`profiled.build_profiled_freeze`, real State, no stubs):**

- `W-1 positive Weekly`: full State advancement via real stage+checkpoint+
  `approve_publication_preview` → `build_profiled_freeze` succeeds WITHOUT
  any legacy file present (delete `visual-review-v2.json` legacy path after
  advancing; Candidate-bound visual remains); assert byte-equality with L-1
  for same `frozen_at` (modulo only `freeze_record_path` if output roots
  differ — test uses SAME roots so full byte equality expected).
- `W-2 positive Special convergent`: SP001 State chain (via `_candidate` +
  State scaffolding mirroring revalidation Fixture `_write_state` but with
  `sources/SP001` roots) → byte-equality with L-2.
- `W-3 divergent Special probe`: Retrospective-shape attempt (§5.1); either
  full byte-equality with a canonical direct call carrying the same validated
  Profile tag, or a recorded upstream-blocker error (DM-016/017 boundary)
  with no broadening.
- `W-4 negatives (each asserts no-write + State unchanged)`:
  (a) stale approval SHA in `human_gate_provenance`,
  (b) `lifecycle_state != RELEASE_CANDIDATE`,
  (c) `publication_preview != approved`,
  (d) Profile SHA drift,
  (e) bundle-not-bound-to-current-Profile (mutate bundle profile ref),
  (f) mixed Candidate same PDF (W2),
  (g) legacy-only visual (W1),
  (h) divergent pre-existing freeze/manifest (W4).
- `W-5 State-gate interlock proof`: mutate State to pending Preview but leave
  an inert approval file (mirrors freeze-boundary `pending_preview` test) →
  wrapper refuses via `_safe_state_profile` (`RELEASE_CANDIDATE`/approved
  gates), proving `validate_agent_state` is on the path (assert error
  originates from the State gate, not the writer).
- `W-6 install-failure resume`: §4 I-cases through the wrapper entry point.

**Consumers (genuine, no string-grep-only, no live Actions):**

- `S-1 stage FROZEN consumer`: feed each positive pair (L-1/W-1, L-2/W-2)
  into `stage_validation.validate_stage` with
  `{visual-review-record, freeze-record, release-manifest}` (cf.
  freeze-boundary `validate_freeze_stage`) → `PASS`; then
  `agent.build_stage_checkpoint` + `advance_with_checkpoint` → `FROZEN`
  with `validate_agent_state == []` (mirrors freeze-boundary positive 146–178).
  Negative: feed a W4-rejected case's (non-)artifacts → stage raises without
  relying on the builder (independent oracle).
- `S-2 release-workflow identity predicate (in-process, no live run)`:
  execute workflow lines 82–97 logic verbatim against each positive fixture
  (Profile SHA check, `public_issue_slug`/`release_identity` recompute,
  `validate_release_manifest`, candidate revalidation, `tag == expected_tag`,
  title/asset derivation) → passes; against W3 pre-repair canonical bytes →
  `Release Manifest public identity mismatch` (proves the predicate catches
  the old divergence). No `gh`/network/Actions execution.
- `F-C1/C2/C3`: keep existing `test_survey_profiled_freeze_v2.py` slug tests
  (21–33) + workflow-text test (34–42, asserts workflow imports
  `profiled.public_issue_slug/release_identity` — constrains the shim design)
  + quality-Profile test (44–144) green unchanged (affected-module regression,
  §8).

**Minimal affected existing modules (regression only, no edits expected):**
`tests/test_survey_publication_v2.py` (canonical chain),
`tests/test_survey_freeze_stage_boundary_v2.py` (Weekly FROZEN consumer),
`tests/test_survey_profiled_freeze_v2.py` (slug/workflow/quality pins),
`tests/test_survey_publication_revalidation_v2.py` (fixture source),
`.github/workflows/survey-production-v2-release.yml` (read-only consumer —
no edit). New tests import from these; they do not modify their semantics.
If fixture.helper edits are needed (issue-matching survey dirname helper,
Special State scaffolding), they go in the NEW test module, not in the
existing files, unless Astra approves a minimal shared-fixture edit on
review.

## 8. Budget, non-goals, stop conditions

- **Budget**: `scripts/survey_publication_v2.py` + `scripts/survey_profiled_freeze_v2.py`
  (shared helpers in the former, shims + State preflight in the latter) +
  ONE new focused test module + fixture scaffolding inside it. No other
  runtime files.
- **No schema / workflow / stage / config changes**: schemas already require
  the exact Freeze/Manifest fields (freeze-schema required list incl.
  `visual_review_path/sha`, `publication_candidate_path/sha`;
  manifest-schema required incl. `release_identity`, `freeze_record_sha256`);
  stage already enforces Candidate-bound visual (stage 582–585); workflow
  already predicates Profile-slug identity (release 84/96–97). If
  implementation discovers a forwarding gap requiring such an edit, return
  the demonstrated path expansion to Astra BEFORE editing (per contract).
- **Non-goals**: DM-003/004, build-transfer, DM-016/017 upstream contracts,
  DM-018 rendered QA, DM-020 semantic fidelity, findings transport,
  all-profile/application, Windows/Actions execution, lifecycle-cost claims.
- **Stop**: implementation + runtime tests are delegated AFTER this design
  review in the same unit; then an independent reviewer distinct from General.
  No Human approval required for this design return; ordinary
  Commit/Push stays Human-owned; do not start code on this milestone.

## 9. Decisions required from Astra (selection, not implementation)

1. Canonical `build_freeze` signature: (A, recommended) add required
   validated `release_identity: str` param threaded from the validated
   Profile by both callers, vs (B) keep signature and assert internal
   convergence (excludes divergent Retrospective from full equivalence —
   record as bounded exclusion).
2. Confirm shim retention (`profiled.public_issue_slug/release_identity`
   delegating to `publication.*`) vs hard rename with workflow+test updates
   (design recommends shims: zero workflow/stage churn).
3. Confirm exclusive-`xb`-create + owned-file-only cleanup (§3.3) vs
   temp-file+rename (design recommends `xb` within budget; rename adds
   fsync/ordering questions without changing the no-global-atomicity bound).
4. Confirm Retrospective full-chain probe scope: attempt in-unit with
   upstream-blocker return vs defer to DM-016/017 unit (design recommends
   attempt-with-bounded-return).
5. Confirm per-method list (§7) is the implementation work order, including
   genuine `FROZEN` consumer (S-1) and in-process workflow predicate (S-2)
   as mandatory acceptance (not string-grep substitutes).
