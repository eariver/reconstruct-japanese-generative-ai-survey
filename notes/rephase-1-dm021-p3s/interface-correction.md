# DM021-P3S PhaseA — interface correction (COMPLETE supplement, read-only)

2026-10-17 JST. Co-Worker General internal precode return addressing Astra
`astra-interface-feedback.md` items 1–8. This file PRESERVES the initial
`interface-proposal.md` (302 lines, saved truncation marker
`...[truncated 3885 chars]` at line 302 acknowledged, not silently repaired)
and `source-binding.md` byte-for-byte, and supplies every missing part plus
precise corrections. Still NO code/copy/tests/imports/restoration/network:
all edges below were derived by `read` + `ast.parse` over file text
(`PYTHONDONTWRITEBYTECODE=1`, never importing candidate modules) plus
`sha256sum`/`stat`/sanitized `git` reads. Fixed contract SHA
`42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472` unchanged.
Staged production / PDF / Gate / Candidate / adoption UNSELECTED. This is an
internal precode return, not a Human Commit Point; STOP for Astra selection.

## 0. What was wrong and where the complete text lives

- F1 (truncation): `interface-proposal.md` ends mid-Weekly-deps; verifier
  V1–V6, oracle/fixture/evidence plan were claimed but NOT saved. This file
  contains them completely (§§6–7). The truncation marker is evidence of the
  gap, not reviewed content.
- F2 (S2 gaps): shared list omitted `schemas/editorial-correction-proposal-
  v2.schema.json` and `schemas/editorial-retention-manifest-v2.schema.json`
  although `verify_retention` safe_reads both before any validator reread
  (`survey_editorial_retention_v2.py:1741+` pins both schemas, then
  `schema_gate.validate_instance`). Corrected complete sorted lists in §3.
- F3 (blanket config exclusion): withdrawn in §4.
- F4 (order/ownership imprecision): corrected W0–W1/W4 in §5
  (`mkdir`-for-dirs vs `O_CREAT|O_EXCL`-for-files, alias-before-resolve,
  fstat-before-write, original-expected recheck after replay/P2V).
- F5 (manifest looseness): canonical sorted `code_deps`, strict 8-key
  `contract_identity`, sized style-input ref, `INDETERMINATE_INVOCATION`
  disposition, COPY-vs-KEEP prose fix, two-arg `col.safe(value,label)` in §2.
- F6 (runtime overclaim + W3 vagueness): bounded assumptions + decided W3
  (consume P2V digest, no redundant private pipeline) in §5.
- F7 (fixture recipe mixup): `source-binding.md:186–187` lists the genuine
  R1 owner (`refresh_mechanical_evidence`, non-emitted reason string) alongside
  `_commit_derivation_only_change` (emitted TeX-comment edit → `main.tex`
  only, generic Core-change, NOT the R1 owner). Corrected recipes in §7; the
  initial file is preserved, the correction lives here.
- F8 (missing verification plan): complete API→file/result/error/seam map,
  oracle matrix, and evidence plan in §§6–7 with no placeholders.

## 1. API signatures (unchanged) + P2V consumed-return contract (exact)

Signatures from the initial proposal stand:

```python
def materialize_staged_source(root, state_path, proposal_path,
    retention_manifest_path, scope_review_path) -> dict[str, Any]  # scope REQUIRED, no None default
def verify_staged_source(root, proposal_path, staged_manifest_path) -> dict[str, Any]  # no state/scope/live args
```

Exact P2V return consumed by W2/W6 (read at
`survey_editorial_current_authority_v2.py:575–595`): keys `result`,
`state_ref`, `proposal_ref`, `retention_manifest_ref`, `scope_review_ref`
(`{path,sha256}` or `None`), `observed_head` (40-hex), `measured`
(`before_graph_digest`, `preserved_upstream_digest`, `proposed_reader_sha256`,
`graph_nodes`, `graph_edges`, `copy_files`, `keep_refs`), `input_hashes`
(merged live+retained map — writer-INTERNAL stability check only, NEVER
persisted into the staged manifest, never full-map-compared across the two
observations). P2V returns NO surface/context/`proposed_canonical` bytes;
W3 must not assume them (§5, decided).

## 2. Manifest / error exactness corrections (F5)

- `code_deps` is CANONICAL ORDERED: array of `{path,sha256,byte_count}`,
  sorted ascending by `path`, unique, exact supported set per §3. Sorting is
  load-bearing for canonical file bytes (`core.json_bytes` of the manifest
  including digest); the initial "order insensitive but set-exact" is
  WITHDRAWN. Validation refuses unsorted/duplicated/superset/subset lists
  with `CODE_DEPS_MISMATCH` before any replay.
- `basis.contract_identity` carries the STRICT 8 keys produced by
  `core.contract_identity` (`survey_production_v2.py:150`):
  `pipeline_contract_version`, `pipeline_contract_sha256`,
  `quality_contract_version`, `quality_contract_sha256`,
  `research_profile_version`, `research_profile_sha256`,
  `publication_profile_version`, `publication_profile_sha256` — copied
  losslessly proposal→manifest, schema-enforced (`additionalProperties:
  false`, all 8 required).
- `style_input_ref` is a SIZED ref `{path,sha256,byte_count}` with `path`
  const `templates/survey/jgaisurvey.sty` (measured 6547 B,
  `3b6d15627439b35a…f53e5cc`); the staged `outputs.style` ref must byte-equal
  it. `outputs` keeps the fixed 3 roles `main`/`bibliography`/`style` with
  canonical `<proposal_dir>/staged-source/{main.tex,references.bib,
  jgaisurvey.sty}` rel paths, `byte_count >= 1`, no aux/temp/unknown/empty-dir
  members, closed 4-file/ancestor inventory.
- Every input read for replay is PINNED BEFORE the validator that rereads it
  (schemas → `schema_gate.validate_instance` / `load_schema`, which reads the
  schema file at `survey_schema_v2.py:40–62` — hence every schema in §3 is a
  pinned S2 entry), and rechecked AFTER (`session.reverify`-equivalent plus
  byte re-compare against original pins).
- Dispositions: `REFUSED_PRE_WRITE` (nothing created), `INVALID`
  (verifier-only), `INCOMPLETE` (post-claim failure, bytes known incomplete),
  `INDETERMINATE_INVOCATION` (post-claim close/final-check failure where a
  COMPLETE valid set MAY remain: outcome unknown, never reported as success,
  never rewritten to a status; a later `verify_staged_source` may attest
  byte-consistency only). No `STAGED_INCOMPLETE` rewriting, no
  truncation/overwrite/rollback/cleanup/resume/takeover.
- Prose fixes: the retained historical State row is `COPY_BEFORE_REPLACEMENT`
  (`state:authority` COPY dest = retained State); only its `State.profile`
  pointer and the matching frozen rows are `KEEP_IMMUTABLE` — never "KEEP
  State". P1 `_validate_scope` invokes `col.safe(value, label)` with TWO
  arguments (`scope_review_value`, `"scope review record"` at P1 `:1778`);
  the adapter in §5 mirrors that exact arity.

## 3. S2 — complete fixed dependency lists, BOTH routes (F2)

Method: `ast.parse` over file text (top-level `tree.body` imports =
load-time; nested function-level imports classified separately); no imports.
Fixpoint over top-level edges terminates at the SAME 27-module load closure
for both routes (P1 top-level imports both derivation worlds, so the Weekly
route also loads the Longform modules and vice versa). Route differences are:
DIRECT-USE functions, FILE-PIN closure members, and reader/receipt schemas.

### 3.1 Shared load closure — 27 `.py`, ALL pinned, BOTH routes

Unique sorted (path | bytes mode | sha256 MEASURED read-only; role/edge):

- `scripts/render_article_draft_tex.py` | 11304 664 | `9c64ebce…6d6c328`
  IMPORT-ONLY for verifier (provides `tex_escape`, the ONLY renderer reuse;
  called THROUGH the route renderers, never directly). Top-level edge:
  imported by `survey_longform_generated_v2` (L35–39), `survey_weekly_derivation_v2` (L19).
- `scripts/survey_agent_control_v2.py` | 124636 664 | `278dc404…83aa7c4`
  IMPORT-ONLY (top-level import of P1 L33 + both derivations; verifier calls
  NO agent function). Nested-only `survey_weekly_mechanical_refresh_v2`
  import is on an unexecuted path → not pinned, not executed (§5 rule).
- `scripts/survey_agent_tool_v2.py` | 8207 664 | `0ff3bd9a…78f6f3eaa`
  IMPORT-ONLY (top-level of both derivations).
- `scripts/survey_architecture_v2.py` | 4407 664 | `b444bb43…f6962e21`
  IMPORT-ONLY (top-level chain via `drafting_base`; verifier calls nothing).
- `scripts/survey_architecture_v2_base.py` | 42252 664 | `e1d61713…e376764`
  IMPORT-ONLY (via `drafting_base`).
- `scripts/survey_bibliography_access_provenance_v2.py` | 9212 664 | `b51bcab8…6ecbe749`
  IMPORT-ONLY runtime helper (transitive via both derivations; citation/access
  helpers as actually used per contract).
- `scripts/survey_completeness_v2.py` | 10469 664 | `dd78603e…0496fe74b`
  IMPORT-ONLY (via `architecture_base`).
- `scripts/survey_drafting_citation_refs_v2.py` | 3805 664 | `57b62c5f…4e44c2b3e`
  IMPORT-ONLY runtime helper (`refs`, via both derivations).
- `scripts/survey_drafting_v2.py` | 20457 664 | `ac7d6942…f840d6d9`
  IMPORT-ONLY (via derivations + agent_control).
- `scripts/survey_drafting_v2_base.py` | 44436 664 | `692e70c6…016b0bfff78c`
  IMPORT-ONLY (via `drafting`).
- `scripts/survey_editorial_correction_proposal_v2.py` | 113535 664 | `cdd69fe7…1c27eab`
  DIRECT-USE: `_validate_scope` (sole surface: `safe(value,label)` + passed
  metadata). Top-level world-load acknowledged; bounded by this list, not
  hand-waved.
- `scripts/survey_editorial_retention_v2.py` | 122231 664 | `3833b14a…480b73f5b2`
  DIRECT-USE: `_Session` (`__init__`, `safe_read`, `repinned`, `reverify`,
  `_close_all`), `verify_retention`, `_sanitized_git_env_ctx`. NOTE: its P1
  import is FUNCTION-LOCAL inside `capture_retention` (`:853`, capture path
  only); `verify_retention` never loads/calls P1 — loading P1 at verifier
  runtime comes from the new module's own top-level P1 import, already in
  this closure.
- `scripts/survey_evidence_v2.py` | 84889 664 | `f7478d86…64a07e4f2c`
  IMPORT-ONLY (top-level of derivations/agent_tool; P1's own evidence import
  is nested-only on an unexecuted-by-verifier path).
- `scripts/survey_longform_derivation_v2.py` | 62260 664 | `c09c5558…8ac84ea41149`
  DIRECT-USE on Longform route (`canonical_reader_bytes` `:949`,
  `validate_longform_reader_input` `:927`); IMPORT-ONLY on Weekly route
  (loaded via P1 top-level, never called).
- `scripts/survey_longform_generated_v2.py` | 39992 664 | `d480e11d…bebed97dfde376a163a58b0ebed97d3c2`
  DIRECT-USE on Longform route (`render_main` `:293`,
  `render_bibliography` `:468`, `validate_generated_closure` `:489`,
  `validate_heading_syntax` `:256`); IMPORT-ONLY on Weekly route.
  Its `survey_reader_fidelity_v2` import is NESTED-only → fidelity pinned via
  the gate's top-level edge instead.
- `scripts/survey_production_v2.py` | 55342 664 | `ba91a8ad…c99e4cc8b329e72c4`
  DIRECT-USE: `sha256_bytes/sha256_file/sha256_object/json_bytes/load_json/
  repository_commit_sha/contract_identity(DEFAULT_CONFIG path const)`.
  Top-level edge → `weekly_pipeline`.
- `scripts/survey_publication_v2.py` | 51835 664 | `f3b73d85…b807659acd8`
  IMPORT-ONLY (P1 top-level).
- `scripts/survey_quality_v2.py` | 13322 664 | `f8a3ef6a…52f090d4ae9a`
  IMPORT-ONLY (P1 top-level + publication/reader_publication chains).
- `scripts/survey_reader_fidelity_v2.py` | 20004 664 | `0d29b304…cb98266c61643`
  IMPORT-ONLY (top-level of `surface_gate`; no scripts imports of its own).
- `scripts/survey_reader_publication_v2.py` | 27385 664 | `d2145042…100e460c1ff69`
  IMPORT-ONLY (P1 top-level).
- `scripts/survey_reader_surface_gate_v2.py` | 94511 664 | `e7305884…bf0131d1f06bbe`
  DIRECT-USE: `load_and_validate_reader_surface_semantic_review` (`:958`,
  keyword-only expected_* + `require_pass`). Its derivation imports are
  NESTED-only route dispatch → already covered by the 27.
- `scripts/survey_review_attention_v2.py` | 7058 664 | `be50e5e3…9646c7a5`
  IMPORT-ONLY (agent_control top-level).
- `scripts/survey_schema_v2.py` | 3261 664 | `0406f327…a2a74200286032`
  DIRECT-USE: `load_schema` (reads schema FILE at `:40–62` — the F2-cited
  file-schema helper), `validate_instance`, `load_and_validate_json`.
- `scripts/survey_screening_v2.py` | 40864 664 | `9b7ff109…3b7cc201d970`
  IMPORT-ONLY (agent_tool/evidence/drafting_base top-level). Its nested
  agent/discovery imports are unexecuted paths → excluded by rule.
- `scripts/survey_weekly_derivation_v2.py` | 43603 664 | `1cb1f705…e86e42dbb45da7d0e2ed57fef0f3f7`
  DIRECT-USE on Weekly route (`render_main` `:400`, `render_bibliography`
  `:445`, `validate_reader_input` `:383`, `validate_generated_closure`
  `:464`); IMPORT-ONLY on Longform route.
- `scripts/validate_article_draft.py` | 17213 664 | `bef91a53…7c328fdb492d3`
  IMPORT-ONLY (top-level of `render_tex`; no scripts imports of its own).
- `scripts/weekly_pipeline.py` | 21699 664 | `f6ceaf80…5812ca008b7f`
  IMPORT-ONLY (top-level of `production`; no scripts imports of its own).

Excluded by stated rule (never loaded on verifier paths; any new call edge
is an exact blocker requiring S2 extension, not silent execution):
`survey_editorial_current_authority_v2` (writer-only caller, never callee of
verifier), `survey_weekly_mechanical_refresh_v2` (nested-only in
agent_control), `survey_discovery_v2`/`survey_x_intake_v2` (nested-only),
`survey_drafting_citation_refs_v2` HAS no scripts imports (leaf) — pinned
above as helper. `jsonschema`/stdlib are external allowlisted runtimes, not
repo pins; `config/survey-production-v2.json` live bytes are NOT an S2 pin
(see §4).

### 3.2 Schemas + style + self (per route; unique sorted with §3.1)

SHARED (both routes), DIRECT-USE (parsed/validated during replay):
- `schemas/editorial-correction-proposal-v2.schema.json` | 3945 664 | `5623c0d9…333a4607`
  (F2-corrected: pinned BEFORE P2R verify rereads the proposal).
- `schemas/editorial-retention-manifest-v2.schema.json` | 5618 664 | `347e5499…549855c`
  (F2-corrected: pinned BEFORE P2R verify rereads the manifest).
- `schemas/reader-surface-semantic-review-v2.schema.json` | 4219 664 | `e8598239…38e73d6699b`
- `schemas/reader-surface-gate-v2.schema.json` | 6894 664 | `fe4a96f4…8133a22c`
- `schemas/editorial-staged-source-manifest-v2.schema.json` | NEW (self-pin from
  committed 3A diff at implementation; pinned before self-validation, rechecked
  after — same discipline as all schemas).
- `scripts/survey_editorial_staged_source_v2.py` | NEW (self-pin; runtime
  binding: importing module `__file__` must resolve to the pinned repo-rel
  path with matching bytes).

LONGFORM-only:
- `schemas/longform-reader-input-v2.schema.json` | 10624 664 | `7bae9d2a…b88fbd0643` DIRECT-USE (canonicalizer validation).
- `schemas/longform-publication-source-manifest-v2.schema.json` | 2720 664 | `4dadf873…601cf26043e8ca` FILE-PIN (route CURRENT_CLOSURE parity; safe_read +
  byte-compare, never parsed by the verifier).
- `scripts/survey_longform_semantic_publication_v2.py` | 36224 664 | `4d235a38…11f68cec6a229195` FILE-PIN (CURRENT_CLOSURE parity; never imported).

WEEKLY-only:
- `schemas/reader-surface-input-v2.schema.json` | 5676 664 | `8db11d4e…17dea4289c` DIRECT-USE.
- `schemas/weekly-publication-source-manifest-v2.schema.json` | 2714 664 | `c11ad525…62ce145143c3b578` FILE-PIN (closure parity).
- `scripts/survey_weekly_semantic_publication_v2.py` | 8233 664 | `53315030…d0e2ed57fef0f3f7` FILE-PIN (closure parity).

STYLE (both routes), DIRECT-USE sized input:
- `templates/survey/jgaisurvey.sty` | 6547 664 | `3b6d1562…f53e5cc` (`style_input_ref`
  `{path,sha256,byte_count}`; staged `outputs.style` must byte-equal it).

Counts: LONGFORM S2 = 27 py + 7 schemas (4 shared + self + 2 route) + 1
semantic_pub FILE-PIN + 1 style + 1 new module = 37 entries; WEEKLY S2 = same
shape with its 3 route-specific swaps = 37 entries. New TEST file is NOT a
runtime dependency and is NOT pinned. Canonical manifest `code_deps` order =
this sorted order.

## 4. Config / KEEP / current-authority categorization (F3)

The initial "live config EXCLUDED by construction" is WITHDRAWN as overbroad.
Categories:

- CURRENT-AUTHORITY inputs (writer-only, never verifier): live State bytes,
  live HEAD, live config, current-eligibility. The verifier performs NO
  current-State validation and NO `HEAD == producer_HEAD` comparison;
  `producer_head` in the manifest is provenance metadata only.
- ARTIFACT-DEPENDENCY inputs (verifier, required): every file the replay
  actually reads — §3 S2 pins (code/schemas/style) — PLUS every immutable
  retained row enforced through the CALLED `verify_retention` (all COPY and
  KEEP rows, including config/tool rows WHEN the retained set contains them).
  If a retained KEEP row binds config/tool bytes, those bytes are safe_read,
  hash-compared, and size-compared by P2R inside the verifier call; the
  verifier never substitutes live config bytes for them and never invents
  dummy HEAD/config/State values. No new dummy values, no flag-neutralized
  authority checks, no live `_Collector` in the verifier (which would pin
  live HEAD+config at P1 `:95–102`).

## 5. S1 + S4 precision corrections (F4) and decided W3 + bounded runtime (F6)

S1 adapter (exact): P1 `_validate_scope(col, root, scope_review_value,
proposal, state, profile)` touches exactly one `col` method —
`col.safe(scope_review_value, "scope review record")` (P1 `:1778`, TWO args)
— plus passed data (`proposal.proposed.proposed_reader_ref` after-binding,
`state.issue_id`, `profile.publication_profile`, `proposal.basis`
before/upstream digests). The narrow shim exposes ONLY that surface:

```python
class _SessionScopeReader:
    def __init__(self, session) -> None: ...   # P2R _Session, root fd already held
    def safe(self, value: str | Path, label: str) -> Path: ...  # same arity as Collector.safe
```

`safe()` = `session.safe_read(value, label, "VERIFY", "INVALID")` then return
`session.root_resolved / rel`, recording `rel` for post-loader
`session.reverify("VERIFY","INVALID")` (brackets the reopening public review
loader read, mirroring P1 `:1802` switch check + `:1804–1807` digest rebinds).
Historical State/Profile = ACTUAL P2R-verified bytes along the I1 chain
`state:authority` COPY dest → retained State file → `State.profile` ref →
matching KEEP Profile file (retention `:1827–1896`, same typed
pin/ambiguity/shape checks) — a COPY State plus KEEP Profile/refs, never a
fabricated former-State dict, never dummy HEAD/config.

W0–W1 order/alias/ownership corrections:

- W0 FIRST: sanitize env (`GIT_*` inheritance refusal), then establish the
  strict canonical current root BEFORE any broad inventory: lexical raw-path
  validation (no backslash/NUL/absolute-escape/dot-dot/empty segments) and
  ancestor alias walk via `lstat`/`is_symlink` (no follow) BEFORE any
  `resolve()` — `resolve()` must never erase a caller alias before the raw
  checks. Only then: sanitized `git rev-parse HEAD` pin + `_Session` root-fd
  open with lstat-vs-fstat entry binding (`retention._Session.__init__`
  `:187–231` discipline).
- Narrow pins SECOND (State/config/State-bound Profile, proposal, probationary
  retention-manifest path + scope review + staged reader/authoring candidates +
  schemas + style + every §3 S2 file, each path/SHA/size). Broad snapshots
  (control/edition/retained dir-file-size inventories, tree map) only AFTER
  canonical roots are established — never the reverse.
- W4 directory claim: claim `<proposal_dir>/staged-source/` with an EXCLUSIVE
  dirfd-relative `mkdir` (leaf-symlink refuses with `EEXIST`; ancestors
  traversed no-follow from the pinned parent fd), then open/pin it
  (`O_RDONLY|O_DIRECTORY|O_NOFOLLOW`) + `fstat` + entry-vs-fd identity bind.
  `O_CREAT|O_EXCL` creates FILES only and is used exclusively for the 3 file
  writes (`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, explicit mode, dirfd-relative).
  A creation-`fstat` failure refuses BEFORE any file write; owned metadata is
  recorded only AFTER successful fstat binding (no stale owned entries).
- Post-replay/P2V recheck: EVERY original input/output byte and EVERY exact
  inventory is re-compared against the W0 ORIGINAL expected values (pins, not
  re-reads) AFTER `verify_staged_source` and after the second P2V; stable-fact
  comparison (refs + before/upstream/proposed-reader digests + within-call
  HEAD) — never self-including full input-map equality, never rebaselining
  changed output bytes in a later session.
- In-memory snapshot table (memory only, never persisted): `orig_live_map`
  (rel→bytes for every live-consumed file), `orig_ret_map` (retained), full
  control/edition/retained/staged file/dir/size inventories, expected output
  bytes/sizes, owned (dev,ino,mode) identities. Persisted: refs, digests,
  `code_deps`, `producer_head`, manifest bytes/digest. Full maps never leave
  the invocation.

Decided W3 (no redundant private pipeline): the writer CONSUMES the in-call
P2V result — match `proposal_ref`/`retention_manifest_ref`/`scope_review_ref`
to W0 pins; take `measured.proposed_reader_sha256`; independently
`safe_read` the staged reader file at
`proposal.proposed.proposed_reader_ref`, require its bytes' SHA to equal BOTH
`proposal.proposed.proposed_reader_canonical_sha256` AND the P2V measured
digest; validate via the route canonicalizer
(`validate_longform_reader_input` + `canonical_reader_bytes == file bytes`,
or Weekly `validate_reader_input` + byte equality); render via the actual
route `render_main`/`render_bibliography` + `validate_heading_syntax` (Longform)
+ `validate_generated_closure` + exact style-template bytes. Private
`_pipeline_data` rederivation is REJECTED (would duplicate P1 derivation,
require authoring inputs + full graph, and re-validate by accident); P1 public
`validate_proposal` is never called after retention. If a future route cannot
satisfy digest-bound-file + canonicalizer + serializer sufficiency, that is an
exact blocker, not a license to rebuild derivation.

Bounded runtime/import assumptions: pinned-byte equality of `__file__`
resolves + byte re-compare is a tripwire, NOT proof against arbitrary
in-process code substitution (no hotpatch attestation claimed). Boundaries:
(a) writer/verifier run in a fresh process with sanitized env; (b) all §3 S2
files are safe_read-pinned BEFORE first use and re-compared AFTER; (c)
fixture/oracle execution uses FRESH subprocesses (`sys.executable -c` /
fixture-code scripts with `PYTHONDONTWRITEBYTECODE=1`,
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`, no
`GIT_*` inheritance), whose failure/success is judged by exit code + stdout
contract, never by importing candidate code into the test runner for
behavioral assertions beyond the real API under test; (d) historical source
at any other commit is never executed; (e) artifact-only HEAD changes with
intact refs/KEEP/S2 pins stay replay-compatible without any HEAD comparison.

## 6. Complete verifier V1–V6 (missing from initial proposal)

`verify_staged_source(root, proposal_path, staged_manifest_path)` (read-only;
any write attempt is a defect; disposition `INVALID`):

- V1 Safe-pin exact supplied `proposal_path` (`proposal.json` basename shape)
  and `staged_manifest_path` (`staged-source-manifest.json`) via dirfd
  no-follow reads + strict-duplicate-key JSON parse + byte pins; require
  `manifest.proposal_ref.{path,sha256}` == supplied proposal bytes; derive
  expected retention-manifest path from `manifest.retention_manifest_ref`
  (exact rel, no basename-only trust, no trusted-manifest-root); pin
  `scope_review_ref` path for V3. Schema-pin the staged manifest schema (self,
  §3) + proposal schema + retention schemas BEFORE any validator rereads
  them; `validate_instance` each; recheck pins after.
- V2 Call ACTUAL `verify_retention(root, proposal_path,
  retention_manifest_ref.path)`; compare returned `proposal_sha256`/
  `manifest_sha256` to V1 pins; walk the returned historical chain
  (`state:authority` COPY → retained State → `State.profile` → matching KEEP
  Profile, `:1827–1896` hops re-enforced on typed pins, no current-State
  shortcut, no arbitrary historical code execution). Derive
  `source_root`/`proposal_id`/canonical `<proposal_dir>/staged-source/`
  paths from the RETAINED Profile only.
- V3 Scope binding through the §5 `_SessionScopeReader` + ACTUAL retained
  State/Profile bytes: require `REVIEW_BOUND_PROPOSAL` with the full existing
  triple (version/decision/before/after/upstream), nonempty
  `change_summary`/`evidence_locations`, substantive
  `EDITORIAL_CORRECTION_SCOPE` PASS with detail/evidence; raw-pin bracket
  around the reopening public review loader + digest rebinds. Ordinary/
  malformed/no-block scope → `SCOPE_*-refusal` (`INVALID`).
- V4 Deterministic replay: validate the pinned staged reader through the
  route canonicalizer; re-render `main`/`bibliography` with the selected
  route functions; staged `style` must byte-equal the pinned style INPUT
  (`templates/survey/jgaisurvey.sty`), not a self-referential output hash;
  enforce the EXACT route S2 set from §3 (sorted-name + byte+size equality,
  `TOOL_DRIFT` refuses BEFORE historical code executes; runtime `__file__`
  binding per §5). No P2V call, no current-State/HEAD requirement, no
  creator/bearer/migration claim.
- V5 Closed-set verification: exact 4-file + ancestor inventory
  (`main.tex`, `references.bib`, `jgaisurvey.sty`,
  `staged-source-manifest.json`, no aux/PDF/temp/unknown/empty dirs),
  manifest self-digest (`sha256_object` minus `manifest_digest`), output
  expected hash/size/identity checks against ORIGINAL pins.
- V6 Final boundary: repeat full staged + retained inventories + original
  consumed-byte/identity checks AFTER all later helper reads; checked closes
  (primary-preserving secondary-close accounting; close failure fails even
  with complete bytes). Return `STAGED_SOURCE_REPLAY_VERIFIED` with observed
  refs/digests only — never eligibility/admission/token.

## 7. S5 — actual fixture/oracle/evidence plan (F7–F8, no placeholders)

### 7.1 Corrected recipes (actual helper names only; no invented helpers)

- LONGFORM chain (real P1/LF recipe, narrative text delta): fixture worktree
  helper `_new_longform_helper` (lf2i two-pass gating owner +
  `lf1_tests.LongformDerivationV2Tests` worker, `_bound_authored` closure)
  → worker `_chain()` → `_complete_authorities(chain)` (lf1 `:401`;
  lf2i `_complete` delegates at lf2i `:249`) → `_current_state(chain)` /
  `_state_path(chain)` → `_advance(chain, "DRAFT_COMPLETE", {...}, 130)`.
  Authoring via REAL `_authored(chain, worker, review_reference)` (lf2i
  `:208`, lf1 `:529`) carrying a REAL narrative delta (cover/headline/deck,
  frontmatter lede, `final_summary` paragraphs, cross-family synthesis
  paragraphs/comparison rows — e.g. revised summary sentence), staged with
  `_stage_authoring_before_prepare` BEFORE `prepare_proposal` and
  `_stage_reader_and_proposal` after; scope via `_scope_review_for`.
  P2R staging via `_prepare_proposal_for`; NO invented `_build_validated`.
- WEEKLY chain (cover/envelope): `_new_weekly_helper`
  (`IncrementBWeeklyDerivationV2Tests.test_accepted_weekly_chain_probe`) →
  `_complete_authorities(_chain())` → `_current_state(chain)` →
  `_build_weekly_validated` (straight-line healthy `VALIDATED_DRAFT`: real
  `--materialize-surface-only` pass, synthetic semantic review
  `review_sha256`-bound, pass2, receipt `validate_receipt`, manuscript
  (`build_manuscript_manifest`), gate (`build_reader_surface_gate` +
  `validate_reader_surface_gate`), minimal PDF + quality bundle
  (`build_bundle`), semantic+visual `build_review_record`, `_advance` to
  `VALIDATED_DRAFT`).
- R1 owner (genuine, CORRECTED): committed-fixture-code
  `_R1_REFRESH_SCRIPT` calling ACTUAL
  `refresh_mechanical_evidence(repo_root, cfg, state_path, "fixture R1
  non-emitted refresh", "synthetic P1 R1 fixture", recorded_at)` — the reason
  string is a NON-EMITTED Python provenance argument (never rendered into
  reader/TeX output); R1 installs the State-bound active record. The P2V
  `_R1_SAMEBYTE_SCRIPT` / `_R1_PREPARE_CASCADE` bind replay to the fixture's
  committed R1 basis. `_commit_derivation_only_change` is EXPLICITLY NOT the
  R1 owner: it edits the EMITTED TeX comment anchor
  (`DERIVATION_COMMENT_ANCHOR` → `DERIVATION_COMMENT_REVISED` in
  `survey_weekly_derivation_v2.py`, flowing to `main.tex` only) — a generic
  Core-change/tool-replay seam, classified under output-tamper/TOOL_DRIFT
  oracles, never as R1 authority. `source-binding.md:186–187` is corrected
  accordingly (initial file preserved; correction lives here).
- Fixture source rule: independent worktree built by
  `_make_source_root`/`_make_p2r_source_root`/`_make_p2v_source_root`
  (tracked `.github`/`config`/`schemas`/`scripts`/`templates`/`prompts`/
  `docs`/`data`/`tests` byte-copy + UNTRACKED lists + `P2R_EXTRA`) with the
  NEW 3 files (`survey_editorial_staged_source_v2.py`,
  `editorial-staged-source-manifest-v2.schema.json`,
  `test_survey_editorial_staged_source_v2.py`) materialized and COMMITTED
  (`git add -A` + process-scoped synthetic identity + `example.invalid`
  inert origin + clean-status assert) BEFORE any authority-producing step;
  `.github` controls materialize with the new code. Candidate repo itself is
  never committed (no candidate commit authorized).

### 7.2 Behavior oracle matrix (each row = implemented method(s); actual seams)

| # | Case | API / seam | Expected |
|---|---|---|---|
| O1 | Healthy Longform staged + independent replay | `materialize→verify` via §7.1 LF chain; meaningful prose delta ⇒ changed `main.tex` bytes (never copied old live bytes) | `STAGED_SOURCE_MATERIALIZED` + `STAGED_SOURCE_REPLAY_VERIFIED`; exact 4-file footprint; live originals/State/retention unchanged (before/after full inventories) |
| O2 | Healthy Weekly staged + replay | §7.1 Weekly chain | same as O1 on Weekly route |
| O3 | Coexistence | P1 `validate_proposal` post-retention on staged proposal dir; P2R `verify_retention`; fresh P2V `observe_current_authority` | P1 still destination-conflict REFUSAL; P2R `RETAINED_SET_VERIFIED`; P2V `SCOPE_BOUND`; staged files never consumed by observers |
| O4 | Live-State/source mutation, KEEP+S2 intact | mutate live State bytes / unrelated source; replay old staged set; attempt fresh materialize | replay still `VERIFIED` (conditional artifact independence); materializer REFUSES (stale basis) — not a simulated adoption |
| O5 | Producer-HEAD independence | artifact-only commit (no S2/KEEP/ref change) | replay `VERIFIED`; no HEAD comparison anywhere |
| O6 | TOOL_DRIFT | change one S2 byte (e.g. emitted-comment literal) with KEEP/refs intact | writer/replay `TOOL_DRIFT` BEFORE historical execution |
| O7 | KEEP drift | alter one retained KEEP byte | P2R-backed refusal inside replay (`PROFILE_DRIFT`/retained mismatch) |
| O8 | Scope refusals | missing / ordinary-without-block / malformed / stale-upstream scope review via `_scope_review_for` variants | writer `REFUSED_PRE_WRITE` (`SCOPE_*`); immediate no-write proven BEFORE repair |
| O9 | Path/ref/schema/inventory tamper | wrong-path same-SHA refs, alias/FIFO staged reader, FIFO scope file (with `_observe_with_timeout` hang-guard precedent), duplicate-key manifest, unknown-field manifest, unsorted `code_deps` | typed refusal; no-read special files never opened (refuse on lstat/type, no block) |
| O10 | Same-inode output tamper after self-readback | replace staged output same bytes→same inode swap / content swap post-readback | `FILE_REPLACED`/`STABILITY_VIOLATION` at V5/V6 vs ORIGINAL pins |
| O11 | Mid-call drift / ownership | drift before write, drift after helper, self-readback edit, root/file owner replacement | refusal at declared later boundary; owned delta still exact-4-file |
| O12 | Fault injection | short write, zero write, `fsync`/flush failure, close failure, partial manifest, root-create race, ancestor-replace, per-file failure | phase/per-file/primary+secondary disposition; close failure ⇒ `INDETERMINATE_INVOCATION` when complete valid bytes may remain, else `INCOMPLETE`; later verifier attests consistency only |
| O13 | Immediate no-write | every refusal case asserts before/after full inventories EQUAL with the fault still present, before any repair | no post-repair equality masquerading as no-write |
| O14 | Existing-root refusal | empty / partial / complete / byte-equal / alias / foreign `staged-source/` preexisting | writer refuses (verifier-only path for complete sets) |

Counting rule: only IMPLEMENTED behavioral methods count (real API calls,
real assertions on files/results/errors/inventories). `mock.patch.object`
on `sys.argv` is harness for CLI entry shapes, never the oracle itself; no
mocked mock tested as functionality; no decorative old13+1/25/36 reruns; no
PASS transfer. Final method count follows the diff and is reported with
method names post-implementation.

### 7.3 Runtime / evidence plan (bounded, concrete)

- Code budget/helper reuse: 1 module reusing `retention._Session`,
  `retention.verify_retention`, `p1mod._validate_scope` (via §5 shim),
  `surface_gate.load_and_validate_reader_surface_semantic_review`,
  `core.*`, `schema_gate.*`, route renderers/canonicalizers/closures; 1
  strict schema; 1 test file with groups O1–O14. No edits to inherited 18.
- Finalization: complete 21-path patch applies DIRECTLY to clean actual409
  (all overlays included); saved-patch proof on a NEW independent actual409
  worktree + declared overlay reversion; all-21 hash/size/mode/status +
  all-entry `.git` isolation checks + current-copy content mapping preserved.
- Evidence hygiene: temp worktrees/indexes stay OUTSIDE `notes/` (under fresh
  `/tmp/opencode` locations, no hardlinks/alternates/shared objects, inert
  origins, checked `GIT_*` sanitization); packet keeps durable logs/manifests/
  patches only. Every executed tool version + direct raw stdout/stderr/logs
  preserved, including failures; no output overwrites (direct exclusive child
  streams, PIDs/argv/cwd/deps/forced-env recorded, timeout + process-group
  reap). Cheap syntax via `ast.parse` only; `PYTHONDONTWRITEBYTECODE=1`;
  no cache cleanup. Old helpers' scripts are qualified design evidence, never
  blindly rerun.
- Blockers (exact): existing-source/schema change required; S2 unclosable
  within 3A; shim cannot preserve after-binding/substantive-PASS/raw-equality
  exactly; route needs private rederivation beyond §5 W3. Any one returns to
  Astra before code — never worked around.

## 8. Saved-line counts + truncation-marker check

- `interface-proposal.md`: 301 lines per `wc -l` (302 content rows; final
  row lacks trailing newline), preserved; contains the 1 saved truncation
  marker `...[truncated 3885 chars]` on its final row — the acknowledged F1
  gap this file completes.
- `source-binding.md`: 191 lines (preserved; §§186–187 mixup corrected by
  §7.1 here, initial bytes untouched).
- `astra-interface-feedback.md`: 14 lines (8 items, all addressed:
  F1→§§0,6,7,8; F2→§3; F3→§4; F4→§5; F5→§2; F6→§5; F7→§7.1; F8→§§6,7.2,7.3).
- This file: 527 lines per `wc -l`; `grep -c "truncated 3885"` over this
  file returns 3 — all are quoted F1 references (§0, twice in §8), not a
  content truncation marker of its own. No `...[truncated` content gap exists here.

(End of complete correction — STOP for Astra selection; no implementation.)
