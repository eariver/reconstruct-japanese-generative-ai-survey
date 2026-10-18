# DM021-P3S PhaseA — concrete implementation proposal (READ-ONLY, no code/copy/tests)

2026-10-17 JST. Co-Worker General PhaseA return per `task.md`: exact S1–S5
proposal BEFORE code/copy/tests for Astra selection. Fixed contract
`outputs/rephase-1-dm021-staged-source-contract-decision.md`
SHA256 `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`;
mandatory `notes/rephase-1-dm021-materialization/astra-review-resolution.md`
S1–S5 and independent review §7 govern. Source: P2V 18 actual HEAD
`409b292756dd1277b9dfae87679934c0d2ce251c` / tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2` + 18 source 3M15A + 84 caches
(separate census vs proof in `source-binding.md`). Reconstruct HEAD
`6dcbb89` clean (only `?? task.md` untracked before this return).
No new runtime, fixture, copy, restoration, or network in PhaseA.
Staged production / PDF / Gate / Candidate / adoption UNSELECTED.
STOP for Astra concrete selection before any implementation; no subagents used.

## 0. Shipping budget (fixed)

- ADD exactly 3 files (3A/0M), no edits to inherited 18 or any other
  existing module/schema/loader/renderer/receipt/Gate/controller/config/CLI:
  1. `scripts/survey_editorial_staged_source_v2.py`
  2. `schemas/editorial-staged-source-manifest-v2.schema.json`
  3. `tests/test_survey_editorial_staged_source_v2.py`
- Future composite is 21 paths 3M18A vs actual 409 (18 unchanged + 3 new).
  Any existing-source/schema change or 4th path is an exact blocker returned
  to Astra, not implicit permission. Current uncommitted review worktree is
  not a committed renderer basis.

## 1. Exact API signatures

```python
def materialize_staged_source(
    root: str | Path,
    state_path: str | Path,
    proposal_path: str | Path,
    retention_manifest_path: str | Path,
    scope_review_path: str | Path,
) -> dict[str, Any]: ...

def verify_staged_source(
    root: str | Path,
    proposal_path: str | Path,
    staged_manifest_path: str | Path,
) -> dict[str, Any]: ...
```

- Writer `scope_review_path` is REQUIRED positional (no `None` default):
  optional/no-block review is insufficient for materialization; missing /
  ordinary-without-block / stale scope refuses pre-write. (P1's
  `validate_proposal(..., scope_review_path=None)` stays unchanged; only the
  new writer requires the arg.)
- Verifier takes NO state/retention-manifest/scope/live-State args: it derives
  the expected retention path from the supplied staged manifest's
  `retention_manifest_ref` and the scope path from `scope_review_ref`. It
  never calls P2V and never validates current State. It requires exact
  immutable refs + full P2R verification + historical layout + scope binding
  + fixed replay deps below. No `HEAD == producer_HEAD` test anywhere.
- Both are importable functions only; no CLI in this increment.

## 2. Error / result shapes (self-contained, strict)

```python
class StagedSourceError(ValueError):
    def __init__(self, code: str, phase: str, disposition: str, detail: str,
                 owned: dict[str, Any] | None = None,
                 cause: BaseException | None = None) -> None: ...
```

Message is `f"{code}: [{phase}/{disposition}] {detail}"` (mirrors
`RetentionError`); `owned` carries observed owned paths/identities
(`staged_dir`, `written_files`, `manifest_path`, per-file
`{path,sha256,byte_count}`, `secondary_close_errors`); `__cause__` chains the
original. Phases: `PIN`, `PRE_WRITE`, `CLAIM`, `WRITE_MAIN`, `WRITE_BIB`,
`WRITE_STYLE`, `MANIFEST`, `REPLAY`, `OBSERVE`, `FINAL`, `CLOSE`.
Dispositions: `REFUSED_PRE_WRITE` (nothing created), `INVALID` (verifier-only,
read-only, nothing written), `INCOMPLETE` (post-claim writer failure: owned
partials preserved, never reported as success). No `STAGED_INCOMPLETE` status
rewrite, no truncation/overwrite/rollback/cleanup/resume, no takeover of an
existing root (existing empty/partial/complete/same-byte/alias/foreign root
refuses, including byte-equal: verifier-only path for already-complete sets).

- Writer success: `{"result": "STAGED_SOURCE_MATERIALIZED", "proposal_ref":
  {path,sha256}, "retention_manifest_ref": {path,sha256},
  "scope_review_ref": {path,sha256}, "staged_manifest_ref": {path,sha256},
  "outputs": {"main": {path,sha256,byte_count}, "bibliography": {...},
  "style": {...}}, "style_input_ref": {path,sha256}, "code_deps":
  [{path,sha256,byte_count}...], "observed_head": 40-hex, "measured":
  {before_graph_digest, preserved_upstream_digest, proposed_reader_sha256,
  graph_nodes, graph_edges, stable_p2v: {before, upstream, proposed_reader,
  head_first, head_second}}, "manifest_digest": 64-hex}`. No `input_hashes`
  map is persisted or compared (self-inclusion forbidden; §5.6).
- Verifier success: `{"result": "STAGED_SOURCE_REPLAY_VERIFIED",
  "proposal_ref": {...}, "staged_manifest_ref": {...}, "observed_refs":
  {proposal, staged_outputs, style_input, code_deps...}, "measured":
  {proposed_reader_sha256, replay_main_sha256, replay_bib_sha256,
  style_match, closure_count}}`. Never current eligibility, publication
  admission, or a future write token.
- Failure taxonomy: pre-write refusal leaves no files/dirs (`owned == {}`);
  post-claim failure preserves owned partials with structured
  phase/per-file/primary+secondary disposition and live originals unchanged
  (staged-only write set). A failed manifest-write/close/final-check may leave
  partial OR complete valid bytes; the invocation reports `INCOMPLETE` /
  indeterminate (never `STAGED_SOURCE_MATERIALIZED`); a later
  `verify_staged_source` may truthfully report consistency of a complete
  matching set without attesting the prior invocation succeeded. Close errors
  attach to `secondary_close_errors` and fail even when bytes are complete.
  True immediate no-write is proven by before/after full inventories with the
  exact injected fault still present BEFORE any repair, not by post-repair
  equality.

## 3. Manifest schema (strict, self-contained)

File `schemas/editorial-staged-source-manifest-v2.schema.json`,
`$schema` draft 2020-12, `additionalProperties: false` everywhere,
duplicate-key refusal at parse (same `_parse_json_strict` hook shape as P2R),
unknown-field rejection via `schema_gate.validate_instance` pinned BEFORE any
consumer reread and rechecked AFTER. Top-level `required`:

`schema_version` (const `"2.0-rc1"`), `kind` (const
`"EDITORIAL_STAGED_SOURCE_V1"`), `status` (const `"STAGED_ONLY"`),
`proposal_ref` ({path,sha256,proposal_id,issue_id,research_profile,
publication_profile}), `retention_manifest_ref` ({path,sha256}),
`scope_review_ref` ({path,sha256}), `issue_id`, `research_profile`,
`publication_profile` (enum `WEEKLY_MAGAZINE`/`LONGFORM_SPECIAL`), `route`
(enum `LONGFORM_GENERATED_V1`/`WEEKLY_GENERATED_V2` — no other route),
`basis` (COMPLETE lossless: `state_ref`, `validation_checkpoint_ref`,
`active_revalidation_ref` (ref-or-null), `active_reader_input_ref`,
`before_graph_digest`, `preserved_upstream_digest`, `generated_receipt_ref`,
`renderer_commit` 40-hex, `contract_identity` object — no before identity
omitted to save bytes), `proposed` (`authoring_input_ref`,
`proposed_reader_ref`, `proposed_reader_canonical_sha256`,
`change_description` minLength 1), `outputs` (exact fixed roles `main` /
`bibliography` / `style`, each {path,sha256,byte_count}; paths must be the
canonical `<proposal_dir>/staged-source/{main.tex,references.bib,jgaisurvey.sty}`
rel posix strings, no caller override, no aux/temp/unknown files/empty dirs),
`style_input_ref` ({path const `templates/survey/jgaisurvey.sty`, sha256} —
pinned template input, distinct from the staged `style` output ref),
`code_deps` (array of {path,sha256,byte_count}, exact fixed set per §6, order
insensitive but set-exact), `producer_head` (40-hex provenance only),
`manifest_digest` (64-hex). `$defs`: `sha256` `^[0-9a-f]{64}$`, `ref`
exact `{path,sha256}`, `sized_ref` exact `{path,sha256,byte_count>=1}`.

Digest/format: all hashes lowercase hex; `sha256` = `core.sha256_bytes(file
bytes)`; `manifest_digest = core.sha256_object({k:v for k,v in manifest.items()
if k != "manifest_digest"})` (same precedent as `review_sha256`); file bytes =
`core.json_bytes(manifest-including-digest)`; readback compares exact file
bytes against originally pinned expected bytes (re-hashing freshly changed
output bytes into agreement is forbidden). Canonical paths are normalized
repo-rel posix; backslashes, absolute-into-elsewhere, dot segments, aliases,
and nonregular files refuse before any read.

## 4. S1 — scope adapter / historical canonical identity (exact contract)

P1 `_validate_scope(col, root, scope_review_value, proposal, state, profile)`
uses exactly ONE `_Collector` method: `col.safe(scope_review_value)` (read at
`survey_editorial_correction_proposal_v2.py:1778`), plus passed metadata
(`root`, `proposal` after-binding `proposed_reader_ref`, `state.issue_id`,
`profile.publication_profile`, `proposal.basis` before/upstream digests).
It never touches `col.files/head/config_sha/reverify/pinned/rel`. State and
Profile passed in are plain data for identity comparison, not admission.

Proposed adapter (new module, no P1 edit):

```python
class _SessionScopeReader:
    """Narrow safe-reader shim exposing ONLY the surface P1 scope uses."""
    def __init__(self, session) -> None: ...   # P2R _Session, already holding root fd
    def safe(self, value: str | Path, label: str) -> Path: ...
```

- `safe()` calls `session.safe_read(value, label, "VERIFY", "INVALID")`
  (dirfd/no-follow, lexical checks, stability pins — the Session-safe
  equivalent of `Collector.safe`), returns
  `session.root_resolved / rel` for the public review loader, and records the
  rel so the post-loader `session.reverify("VERIFY","INVALID")` brackets the
  reopening read (mirrors P1's `raw_path.read_bytes() != captured` switch
  check plus digest rebinds at P1 `:1802–1807`).
- Historical State/Profile bytes are the ACTUAL P2R-verified retained bytes:
  `session.safe_read` of the `state:authority` COPY dest → retained State →
  `State.profile` ref → matching KEEP Profile (same I1 hops as §5, typed
  pin/ambiguity/shape checks). Never a fabricated former-State dict, never a
  live `_Collector` (which would pin live HEAD+config at `P1:95–102`), never
  dummy HEAD/config values or flag-neutralized authority checks.
- Full existing scope triple + substantive PASS is required
  (`REVIEW_BOUND_PROPOSAL`, version/decision/before/after/upstream bindings,
  nonempty `change_summary`/`evidence_locations`,
  `EDITORIAL_CORRECTION_SCOPE` PASS with substantive detail/evidence);
  ordinary/invalid review → `SCOPE_ORDINARY_INVALID`-family refusal; no-block
  (`editorial_correction_scope` absent → `REVIEW_REQUIRED`) refuses the writer.
- Exact supplied proposal path + bound `retention_manifest_ref` + historical
  Profile-derived `source_root/proposal_id` canonical paths are established
  BEFORE any broad inventory; missing/ambiguous/unconstructible binding is an
  exact blocker returned within 3A (no weakened scope subset, no live
  `_Collector`, no public-loader substitution — correction2's public-loader
  fallback is a comparison point only, final `_Session`-adapter is
  authoritative).

## 5. Writer call graph S4 + original-snapshot boundaries (contract §5 order)

W0 sanitized env + strict current-root validation (resolve once, symlink-root
refusal, `GIT_*` inheritance refusal) BEFORE any broad walk; record actual
HEAD via sanitized `git rev-parse` + `session` root-fd identity; narrow raw
pins FIRST: State/config/State-bound Profile, proposal, retention manifest
(probationary path derived from proposal dir, canonically revalidated later),
scope review, staged reader/authoring candidates, schemas, style input, and
every S2 dep file (§6) — each with path/SHA/size pins.
W1 snapshot full validated input/control/edition sets (files/dirs/types/sizes)
including existing retention inventory; establish strict canonical roots
(`_validated_state_profile_for_tree`-equivalent checks via pinned bytes, never
untrusted Profile roots or manifest prefixes).
W2 call actual `observe_current_authority(..., scope_review_path)` INSIDE this
invocation; require `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`; match its returned
`state_ref/proposal_ref/retention_manifest_ref/scope_review_ref/measured`
against the W0 pins; pin every dynamically discovered consumed byte against
the original expected hashes. Missing/invalid scope, stale
basis/retention/upstream, alias/overlap/TOOL drift, or existing
`<proposal_dir>/staged-source/` root (any state incl. byte-equal) refuses
with `REFUSED_PRE_WRITE`. P1 public validate is never called after retention.
W3 use the already independently rederived byte-bound proposed reader from
this invocation (P1 `_pipeline_data` derivation, never destination-accepting;
Weekly pending fallback never editorial); compare canonical FILE bytes to the
exact reviewed `proposed_reader_ref`; render via actual route
`render_main`/`render_bibliography` + `validate_heading_syntax` +
`validate_generated_closure` + exact fixed style-template bytes; no arbitrary
raw TeX, extra payload, or hand-edit override.
W4 preflight all 4 prospective outputs + parent relationships + schema bytes +
closed-set inventory BEFORE claiming the root; exclusively create the absent
root (dirfd `O_CREAT|O_EXCL|O_NOFOLLOW`, ancestor alias checks, entry-vs-fd
identity); exclusive no-follow `O_CREAT|O_EXCL` short-write/close-checked
writes of ONLY the 3 source files (pinned/rederived expected bytes, never a
second reading that moves the basis).
W5 before manifest: compare ALL original consumed inputs/HEAD/control/edition
inventories allowing ONLY the exact owned 4-file/ancestor delta (no
proposal-subtree prefix exemption); verify 3 output bytes/sizes + closed
directory set; serialize manifest (digest §3) and exclusively write it LAST,
close + read back exact bytes.
W6 invoke actual standalone `verify_staged_source` (this module, §6), then
fresh `observe_current_authority` SCOPE_BOUND again while live
publication/State are still unchanged. Compare STABLE facts only:
State/proposal/retention/scope refs, before/upstream/proposed-reader digests,
within-call HEAD. Newly materialized files legitimately appear in the second
observation's input map — NEVER demand full-map equality, NEVER rebaseline
changed output bytes in a later session.
W7 final original-input/control/edition/retained/staged inventories + output
expected hashes/sizes + owned identities AFTER the later helpers; checked
closes of every fd (primary-preserving secondary-close accounting); return
`STAGED_SOURCE_MATERIALIZED` only then. A fresh self-readback session
compares against the ORIGINAL expected output bytes.

## 6. S2 — fixed route-specific replay dependency closure + import/use graph

Policy: implementation-derived exact NAME set (manifest-chosen names never
define it); every entry pinned `{path,sha256,byte_count}` at materialization
and re-pinned at replay; `TOOL_DRIFT` refuses on name-set or byte mismatch
BEFORE executing historical code; schemas pinned before parsers reread them
and rechecked after; runtime import binding asserts each imported S2 `.py`
resolves to the pinned repo-rel path with matching bytes (not merely another
file at the same path). Producer HEAD is provenance only. Post-live-State
artifact replay stays usable ONLY while all S2 + KEEP + immutable refs stay
intact.

Shared base (both routes) — measured pins this unit (path | bytes mode | sha256):
`survey_editorial_correction_proposal_v2.py` 113535 664 `cdd69fe7…` (scope
rules `_validate_scope`); `survey_editorial_retention_v2.py` 122231 664
`3833b14a…` (`_Session`/`verify_retention`); `survey_reader_surface_gate_v2.py`
94511 664 `e7305884…` (review loader); `survey_reader_fidelity_v2.py` 20004
664 `0d29b304…` (transitive via gate); `survey_production_v2.py` 55342 664
`ba91a8ad…` (sha/json/HEAD/contract helpers); `weekly_pipeline.py` 21699 664
`f6ceaf80…` (transitive via core import); `survey_schema_v2.py` 3261 664
`0406f327…`; `render_article_draft_tex.py` 11304 664 `9c64ebce…`
(`tex_escape`, the ONLY renderer reuse); `validate_article_draft.py` 17213 664
`bef91a53…` (transitive via render_tex import); `survey_drafting_citation_refs_v2.py`
3805 664 `57b62c5f…`; `survey_bibliography_access_provenance_v2.py` 9212 664
`b51bcab8…`; `survey_agent_control_v2.py` 124636 664 `278dc404…`,
`survey_agent_tool_v2.py` 8207 664 `0ff3bd9a…`, `survey_drafting_v2.py` 20457
664 `ac7d6942…`, `survey_evidence_v2.py` 84889 664 `f7478d86…`,
`survey_publication_v2.py` 51835 664 `f3b73d85…`, `survey_quality_v2.py` 13322
664 `f8a3ef6a…`, `survey_reader_publication_v2.py` 27385 664 `d2145042…`
(runtime-transitive via P1 import chain — pinned because importing P1 loads
them; excluding them would leave runtime identity unbound);
`schemas/reader-surface-semantic-review-v2.schema.json` 4219 664 `e8598239…`;
`schemas/reader-surface-gate-v2.schema.json` 6894 664 `fe4a96f4…`;
`templates/survey/jgaisurvey.sty` 6547 664 `3b6d1562…` (style INPUT; staged
`style` output must byte-equal it); new module + new schema (bytes pinned at
implementation from the committed 3A diff — self-pins, checked like all
others). Live `config/survey-production-v2.json` is EXCLUDED by construction
(verifier uses retained KEEP Profile, never live config/HEAD).

Route additions:
- LONGFORM (`LONGFORM_GENERATED_V1`): `survey_longform_generated_v2.py` 39992
  664 `d480e11d…` (render_main/render_bibliography/closure/heading checks);
  `survey_longform_derivation_v2.py` 62260 664 `c09c5558…`
  (`canonical_reader_bytes`/`validate_longform_reader_input`);
  `survey_longform_semantic_publication_v2.py` 36224 664 `4d235a38…`
  (CURRENT_CLOSURE pinned file); `survey_weekly_derivation_v2.py` 43603 664
  `1cb1f705…` (runtime-transitive via P1 import — pinned, not executed for
  Longform replay); `schemas/longform-reader-input-v2.schema.json` 10624 664
  `7bae9d2a…`; `schemas/longform-publication-source-manifest-v2.schema.json`
  2720 664 `4dadf873…`.
- WEEKLY (`WEEKLY_GENERATED_V2`): `survey_weekly_derivation_v2.py` 43603 664
  `1cb1f705…` (renderer + `validate_reader_input`); 
...[truncated 3885 chars]