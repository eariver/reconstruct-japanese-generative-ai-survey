# DM021 changed-reader materialization/admission/promotion — General contract analysis (NEW proposal)

2026-10-16 JST. General (Co-Worker) design-only analysis for the NEW DM021
changed-reader materialization/admission/promotion contract unit, following
P2V assessment §4. **This file is a NEW proposal, not a decision, not runtime
evidence, not approval.** Astra reviews actual callsites and selects/corrects;
a fresh author-independent General reviews the selected design. No
implementation, no fixtures, no tests executed, no code/schema/ref/commit
changes in this unit. Whole NOT_READY, step4/B3 OPEN, audit unstarted,
DM021 OPEN.

Read-only method (no subagents): `sha256`/`stat` recomputation over the 18
pinned paths, `git rev-parse`/`git status`/`git diff --stat` with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`, plus
`grep`/`read` of candidate source. No candidate-module imports, no suite/proof
runs, no copies/restores, no network/intake refresh. All `file:line` cites
below are measured against the verified active source (§0); line numbers are
observations at those pinned bytes, not standing references.

There is no prior materialization analysis in this directory to preserve —
`task.md` is the only pre-existing file — so nothing is carried forward or
corrected here. Fixed prior bases (unchanged, still authority):
P1 contract `outputs/rephase-1-dm021-contract-decision.md` (07e89990),
P2R contract `outputs/rephase-1-dm021-retention-contract-decision.md`
(194fd7de), P2V contract
`outputs/rephase-1-dm021-current-authority-contract-decision.md` (2ea1d98f),
with P2V assessment + mandatory Astra closeout + independent final
resolution as evidence bounds.

## 0. Verified source identity for every claim below

Active
`/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`:

- Detached actual HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (measured `rev-parse`, rc 0).
- Full status: 3 modified tracked
  (`schemas/reader-surface-gate-v2.schema.json`,
  `schemas/reader-surface-semantic-review-v2.schema.json`,
  `scripts/survey_reader_surface_gate_v2.py`) + 15 new source paths + 84
  `__pycache__/*.pyc` = 18 source + 84 caches (measured `status
  --porcelain=v1 --untracked-files=all`; cache count exactly 84, all `.pyc`).
- All 18 source paths match static
  `notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json`
  on sha256 + byte count + mode (`0o664`): **18/18 MATCH** (recomputed, no
  mismatches). Pins include P1 `cdd69fe7…` (113535 B), observer `79a3396c…`
  (37896 B), test `c567715d…` (74061 B); complete-18 patch `dc5ae07b…`
  (948373 B) recorded in P2V evidence, not rehashed here.
- Cache accounting (qualified): the 84 `.pyc` are preserved/isolated
  execution side effects, pinned only as byte rows in P2V guards — not source
  proof, not executed or imported in this unit. Byte-content equality of
  caches was NOT re-verified here (only path count + extension census);
  P2V TB1 proof remains the authority for cache bytes.
- Preceding reconstruct commit `5595d214375f77c93fc3376799fb29b145bc5e32`
  (Human-authorized `git add .`/commit/push of completed P2V work) is
  recorded as boundary context only — not candidate-commit, production, or
  adoption authority, and it authorizes nothing in this unit.

## 1. Actual callsite trace (Q1) — producers through admission

All paths relative to the active worktree root. "Producer" = derives reader
bytes; "serializer" = renders bytes; "receipt" = binds bytes to authority;
"Gate/manuscript/QA" = admits bytes toward Candidate; "controller/State" =
owns lifecycle truth.

### 1.1 Reader producers (derivation contexts)

| Function | Location | Restriction relevant to corrections |
|---|---|---|
| Longform `load_derivation` | `scripts/survey_longform_derivation_v2.py:1101` | DRAFT_COMPLETE-only (`:1122`), exact action (`:1127`), strict State (`:1119`), THEMATIC/LONGFORM_SPECIAL (`:1134`). A correction builder reuses this shape but must NOT run under DRAFT_COMPLETE semantics for a VALIDATED_DRAFT edition without an explicit staged-context decision (§4). |
| Longform `load_derivation_for_readback` | same file `:1142` | Healthy-lifecycle allowlist DRAFT_COMPLETE/VALIDATED_DRAFT/RELEASE_CANDIDATE/FROZEN/RELEASED (`:1166`), refuses pending/revalidation contexts and manufactured former-State (`:1142–1152`). This is the readback side of the §4 cycle. |
| Weekly `load_derivation` | `scripts/survey_weekly_derivation_v2.py:475` | Strict State, falling back ONLY to a checked pending basis (`:481–487`): `validate_agent_state` → `_collect_pending_rows(require_change=False)` → `built_checked_pending_publication_basis`. P2R §1 already rules this is not editorial authority; §4 below forbids routing correction derivation through that fallback. |
| Weekly `validate_reader_input` / Longform `validate_longform_reader_input` | weekly `:726` (via `:756`); longform derivation module | Schema + semantic validation of reader bytes; reused unchanged by any staged builder. |

### 1.2 Serializers (renderers)

| Function | Location | Note |
|---|---|---|
| Longform `render_main` / `render_bibliography` | `scripts/survey_longform_generated_v2.py:293` / `:468` | Deterministic bytes replayed by receipt `:745–757`. |
| Weekly `render_main` / `render_bibliography` | `scripts/survey_weekly_derivation_v2.py:400` / `:445` | Deterministic bytes replayed by receipt `:760–772`. |
| TeX/BSD/style materialization gate | `scripts/survey_longform_semantic_publication_v2.py:481,486` | **"TeX/BibTeX/style materialization prohibited until semantic review PASS"** — the existing staged-ordering precedent. Pass 1 (`--materialize-surface-only`, `:60`, `:370–460`) writes ONLY the reader surface with preflight (no partial outputs `:410–414`, exclusive write `:423`, readback `:430`, same-byte reuse rules `:436–455`); pass 2 refuses to silently do pass 1 (`:372–390`) and requires the review artifact on disk BEFORE any further write (`:474–487`). A correction materializer mirrors this shape at versioned paths (§6). |

### 1.3 Source receipt validators (canonical-path enforcement)

| Function | Location | Binding that blocks naive staged reuse |
|---|---|---|
| Longform `verify_tool_basis` | `scripts/survey_longform_generated_v2.py:519` | Renderer commit must be an ancestor of HEAD; exact control/contract equality commit↔HEAD; clean HEAD + no uncommitted control source; every closure row byte-equal at BOTH commit and HEAD (`:519–582`). Docstring states the consequence: **"An uncommitted exact-source overlay therefore refuses as a committed implementation basis."** Any correction fixture source must be independently committed before it can ground authority (P2V contract §4.6). |
| Longform `validate_receipt` | same file, `:660–758` | Reviewed-target mismatch refuses (`:694–697`); canonical edition siblings required for surface, archive, receipt (`:720–730`); **canonical FILE-byte replay** (`:741–742`); deterministic output replay (`:753–757`). |
| Weekly `_verify_head_bytes` | `scripts/survey_weekly_derivation_v2.py:577` | Same tool-basis shape for Weekly (`:577–631`). |
| Weekly `validate_receipt` | same file `:726` (+ envelope `:669`, closure-at-commit `:699`, `build_receipt` `:634`) | Accepted-refs/archive equality, canonical survey_root outputs, recomputed-surface equality, deterministic replay (`:737–772`). |

Consequence (feeds Q2/Q4): every live receipt validator demands canonical
live paths AND committed tool closure. Staged (versioned-target) bytes cannot
pass any of them unmodified — not a bug to patch around, but the exact
touchpoint list for the versioned-target relation (§2) and the reason a
staged-only receipt object with no accepting validator would be a dead end
(§6).

### 1.4 Gate binding (route selection)

`_derivation_for_manuscript`
(`scripts/survey_reader_surface_gate_v2.py:1145`) selects exactly three
routes: DIRECT_PRIMARY (`:1156–1159`), THEMATIC/LONGFORM_GENERATED
(`:1160–1198`), WEEKLY generated (`:1199–1231`). For generated routes it
requires the canonical `publication/v2/reader-surface-input-v2.json` suffix
(`:1162–1169`, `:1201–1203`), a receipt NEXT TO the reviewed surface
(`receipt_path = surface_path.parent / "validated-source-manifest.json"`,
`:1173`, `:1206`), receipt↔surface↔review triple equality
(`:1178–1181`, `:1211–1214`), and receipt-outputs ↔ manuscript
primary/support equality with exactly 2 supporting files
(`:1183–1198`, `:1215–1231`). Entry `evaluate_reader_surface_gate` at
`:1234`; revalidation calls `validate_reader_surface_gate` at
`scripts/survey_agent_control_v2.py:1931`. Any versioned-target admission
must add an explicit fourth alternative here with its own binding rules —
it cannot fall through to an existing route (§2).

### 1.5 Manuscript / reviews / quality bundle

- `build_manuscript_manifest` (`scripts/survey_reader_publication_v2.py:297`):
  binds Profile/Architecture/approval/primary source/supporting files,
  refuses overwrite (`:352–354`). Consumes reviewed bytes; does not review.
- `validate_manuscript_manifest` (`:358`), `validate_review_record` (`:544`,
  digest `:579`, manuscript/profile agreement `:586–602`).
- `validate_bundle` (`scripts/survey_quality_v2.py:232`);
  `bind_pdf_authority` (`:60`) matches materialized PDF bytes against durable
  authority — the pattern for any staged-QA PDF handling.
- Revalidation QA block (`scripts/survey_agent_control_v2.py:1900–1944`):
  manuscript + bundle + semantic + visual + Gate + all-PASS quality checks;
  semantic/visual via `validate_review_record` (`:1921–1925`), both required
  (`:1929`).

### 1.6 Candidate / Preview / Freeze / Release (normal chain — unchanged)

- `build_candidate` (`scripts/survey_publication_v2.py:668`): consumes
  ALREADY-reviewed source/PDF/manuscript/bundle/reviews, writes ONE immutable
  Candidate (`:745`). It never re-enters publishers and never provisions
  correction bytes — Candidate-as-publisher remains forbidden (§5).
- `validate_candidate` (`:749`), `build_preview_approval` (`:817`),
  `validate_preview_approval` (`:855`).
- Stage handlers: `validate_publication_candidate`
  (`scripts/survey_handlers_v2.py:378`), `validate_freeze` (`:394`,
  exact authority match `:409–430`), `validate_release` (`:434`).
- Stage map (`scripts/survey_stage_validation_v2.py:60–77`):
  DRAFT_COMPLETE admits 7 roles (manuscript, validated-source,
  publication-pdf, quality-regression-bundle, semantic-review, visual-review,
  reader-surface-gate); VALIDATED_DRAFT admits ONLY `publication-candidate`
  (`:75`). Post-adoption correction flow therefore re-enters the NORMAL
  chain (fresh Candidate → Preview → Freeze → Release) with zero handler
  changes (§5). Approval-artifact binding `:126–156` ties the approved
  Candidate into transitions so no substituted Candidate can pass.

### 1.7 Controller / State / revalidation (adoption end)

- `validate_agent_state` (`scripts/survey_agent_control_v2.py:348`); pending
  predicates `:696`; `_collect_pending_rows` (`:711`): changed rows must be
  canonical role paths (`:737–740`) — a changed live reader-input file is
  NOT a role (roles in §1.6 list contain no reader JSON/authoring/receipt),
  so live replacement alone hits "changed noncanonical or upstream
  role/path". This is measured confirmation that adoption needs a role +
  reason change, never live-byte installation alone (§5).
- `revalidate_publication_surface` (`:1773`): reason gate `:1789` admits
  ONLY `REVIEWED_CORE_CHANGE` (`REVALIDATION_REASON_CLASSES`, `:45`);
  superseded-vs-preserved computed against the checked pending basis
  (`:1844–1886`); pre-mutation snapshot/basis recheck + exclusive record
  create + State update (`:1996–2032`). The writer/adoption design (§3/§5)
  extends this function family; it does not bypass it.
- R1 owner precedent (`scripts/survey_weekly_mechanical_refresh_v2.py`):
  `REASON_CLASS = "REVIEWED_CORE_CHANGE"` (`:36`), canonical
  surface/receipt/Gate/manuscript-role asserts before any retained write
  (`:690–718`), roles via `agent._publication_revalidation_roles` (`:920`).
  R1 is a same-edition writer that still replays receipts — the closest
  existing writer discipline to copy, but it is Weekly-code-only and
  unchanged-reader; it is not a correction owner.

### 1.8 P1 / P2R / P2V (fixed composition surface)

- P1 `prepare_proposal` (`scripts/survey_editorial_correction_proposal_v2.py:1741`,
  staged authoring must pre-exist `:1746–1759`, final receipt recheck `:1764`);
  `validate_proposal` (`:1838`: layout pins `:1851`, rederive `:1862`,
  exact supplied-vs-rederived compare incl. staged FILE bytes `:1865–1867`,
  scope `:1875–1878`, final receipt recheck AFTER scope `:1880`, stability
  `:1882–1887`); `_validate_scope` (`:1775`: after-binding is the persisted
  `proposed_reader_ref` path+sha `:1786–1793`, WITHIN_APPROVED_AUTHORITY +
  exact before/after/upstream + substantive PASS check `:1811–1835`).
- Data factoring for reuse: `_retention_plan` (`:1302`), `_pipeline_data`
  (`:1309`), `_pipeline` (`:1514`), `_validated_state_profile_for_tree`
  (`:1576`), `_eligibility` (`:327`), `_active_effective` (`:380`).
  P1 already observes-but-never-adopts an existing Candidate
  (`:828–862`, `CANDIDATE_OBSERVED unadopted`, divergence refuses).
- P2R `capture_retention` (`scripts/survey_editorial_retention_v2.py:851`,
  HEAD pin `:880`, exclusive owned writes, manifest-last) /
  `verify_retention` (`:1731`).
- P2V `observe_current_authority`
  (`scripts/survey_editorial_current_authority_v2.py:101`, live + retained
  checks in one invocation, observation only, never a write token).

### 1.9 Affected-consumer matrix for ANY changed-reader promotion

| Consumer | Demands on changed bytes | Change needed for versioned-target admission (§2/§5) |
|---|---|---|
| Route loaders (LF `:1101`, Weekly `:475`) | Accepted authority + canonical authored input | None for staged derivation reuse; staged-context entry rule is new documentation, not a loader change |
| Serializers (LF `:293/:468`, Weekly `:400/:445`) | Valid surface object | None (pure functions) |
| Receipt validators (LF `:660–758`, Weekly `:726`) | Canonical live paths + committed closure | Versioned-target binding alternative (P4) |
| Gate `_derivation_for_manuscript` (`:1145`) | One of 3 routes, canonical suffix, receipt-next-to-surface | Explicit 4th correction-target alternative (P4) |
| Manuscript builder/validator (`:297`/`:358`) | Reviewed bytes + Architecture authority | Versioned primary/support binding rule (P4) |
| Quality bundle (`quality:232`) | Deterministic checks over built outputs | None if staged QA reuses it read-only; binding rule for staged outputs (P4) |
| Semantic scope review (P1 `:1775`) | Staged after path+sha, before + upstream | None — ALREADY consumes staged targets; P3's direct consumer |
| Revalidation (`control:1773`) | Role-path changed rows + reason class + full QA | New reason class + corrected-input role(s) (P4) |
| Candidate/Preview/Freeze/Release | Already-reviewed bytes, exact authority | None — normal fresh chain re-entered after adoption |
| P1/P2R/P2V | Staged refs, retention plan, observation | None — P3 outputs feed existing checks |

No "unchanged-validator bridge" is assumed: the table names exactly which
validators change (receipt ×2, Gate, manuscript binding, revalidation
reason+roles) and which do not.

## 2. Immutable staged reader + scope review; versioned-target vs second live review (Q2)

### 2.1 What is already immutable and preserved

- The reviewed artifact is the STAGED proposed reader at the versioned path
  `<source_root>/publication/v2/editorial-corrections/<proposal_id>/reader-surface-input-v2.json`
  (P1 layout `proposal_v2.py:1350–1364`, `PROPOSAL_FILES :47`). P1
  `validate_proposal` compares exact staged FILE bytes (`:1865–1867`).
- The scope review binds that exact path+sha as its after-target
  (`_validate_scope :1786–1835`; `surface_path`/`surface_sha256` authority).
  The review record itself is byte-pinned (`SCOPE_BYTES_SWITCHED`,
  digest checks `:1802–1807`).
- **Same SHA never rebinds a path:** the binding is always the
  (path, sha256) pair; an equal-sha file at any other path satisfies
  nothing. Any downstream admission must carry the triple
  {versioned_reader_ref, installed_reader_ref, sha256} with path equality
  checked at every use — never sha-only matching.

### 2.2 The two alternatives, with costs

**Alternative V — explicit versioned-target + installed-output relation.**
The staged (reviewed) bytes stay immutable at the versioned path; a bounded,
explicitly new admission alternative in receipt/Gate/manuscript validators
accepts a versioned target paired with its installed live output, checking:
(1) versioned bytes == reviewed (path, sha256) from the scope review;
(2) installed bytes == versioned bytes (exact FILE bytes);
(3) installed path == the canonical live path for that route/profile;
(4) upstream digests (before-graph, preserved-upstream, accepted refs) still
equal the proposal basis; (5) tool closure still committed-clean per
`verify_tool_basis`/Weekly `:577` at install time. Cost: bounded code
parameterization in exactly the validators named in §1.9 (receipt ×2, Gate
4th route, manuscript binding, bundle staged-output rule) + their tests;
one genuine pre-TeX scope review on staged bytes (already the existing
reviewer role, no new role); zero invalid-live window because live bytes are
untouched until the writer's preflighted install. Non-default work: none at
review time — the review happens on staged bytes through the normal
assessor channel.

**Alternative L — genuine second live-path review after installation.**
Install changed bytes at live canonical paths first, then obtain a full new
semantic review (+ downstream editorial/visual + Human Preview) against live
paths. Costs: (a) **invalid-live window** — between install and review
completion the edition is live-unhealthy: old State authority no longer
matches live bytes (`_collect_pending_rows` refuses non-role changes;
revalidation cannot establish authority without reviews; reviews need
installed bytes to examine — circular); (b) a second GENUINE review is real
semantic labor (assessor time, evidence, possibly iteration) on the critical
path of every correction, non-default scheduling, unbounded cost per
correction; (c) rollback on REJECT means a second live mutation with its own
retention/authority hazard. Nothing in the current validators supports a
"pending-review live" state — Weekly's pending fallback (`:481–487`) covers
mechanical refresh replay, not editorial scope, and P2R §1 forbids the
blanket bypass reading.

### 2.3 Proposal (Astra selects)

Select **Alternative V**. It preserves the already-reviewed immutable
staged-reader/scope authority end-to-end, confines code change to named
validators, creates no invalid-live window, and adds no Human role or Gate:
pre-TeX semantic/scope review stays the existing ChatGPT assessor duty on
staged bytes (P1 contract §5); later post-PDF semantic/visual review and
exact Human Preview remain separate mandatory obligations AFTER the writer
installs and the normal generation/QA chain runs — they are never generated
PASS, never waived, never merged into the scope review. Alternative L is
rejected for the invalid-live window + circular-authority + unbounded
per-correction review cost above. If Astra disagrees, the exact consequence
is: P4 must first design a supported pending-review live state (State
validator, receipt, Gate, stage map changes) — a larger architecture unit
than this proposal budgets.

## 3. Writer preflight, owned writes, failure contract (Q3)

### 3.1 Fresh preflight in its own invocation — P2V is observation, not a token

The future writer (P4) MUST, inside its own invocation and after pinning its
inputs, call the actual read-only authorities itself:

1. P1 `validate_proposal` on the exact (proposal, scope review) — must
   return the SCOPE-bound-equivalent success (not merely REVIEW_REQUIRED).
2. P2R `verify_retention` on the exact (proposal, manifest) — retained set
   intact.
3. P2V `observe_current_authority` on the exact
   (state, proposal, manifest, scope) — current basis observed, scope-bound.

A returned dict from any earlier call — including a P2V observation from
seconds ago — is NEVER carried in as proof: the writer re-runs all three
against its own pins and compares returned path/sha refs to those pins
(P2V contract §5 ordering: pin → authority-before-walk → P2R → derivation
→ scope → full receipt recheck → final window). Rationale, already fixed in
P2V contract §2: "This is a bounded observation of present facts, not a
durable authorization token … A future writer must establish its own fresh
authority." Any design passing a `verified_set`/token/caller flag is the
already-rejected P2V-initial-enum bypass in new clothes.

### 3.2 Exact owned write set (P4 writer; P3 writes less — §6)

P4 writer owns, per invocation, ONLY:

1. Live canonical reader input
   (`<source_root>/publication/v2/reader-surface-input-v2.json`, route-specific
   edition dir) — exclusive create-or-exact-replace from pinned staged bytes.
2. Deterministically regenerated live outputs for that route
   (`survey_root/main.tex`, `references.bib`, `jgaisurvey.sty` copy) —
   byte-equal to the serializer replay of the installed reader (same oracle
   as receipt `:753–757` / `:768–772`).
3. Live receipt (`validated-source-manifest.json`) + Gate/manuscript/quality
   artifacts produced by the NORMAL generation chain operating on installed
   bytes (the writer invokes the existing producers; it does not hand-write
   their outputs).
4. The revalidation record file (exclusive create, next sequence;
   collision refuses — `control:1956–1957`) + the State-file update
   (exact expected-bytes rewrite pattern `:1999–2011`).

Everything else (reviews, Candidate, Preview approval, Freeze/Release
records, State-bound Profile, config, checkpoints) is NEVER writer-owned.
P3 (next unit, §6) owns only the single staged reader file at the
versioned path — a strict subset, same exclusive-write discipline.

### 3.3 Snapshots, ownership, failures, retry, recovery

- Snapshots (read-only, before any write): validated Profile/source/survey
  roots, DEFAULT_CONFIG + implementation_control_roots + style + contract
  files (the `verify_tool_basis` control set), the full P1 input-hash set,
  retained COPY/KEEP bytes, current HEAD (sanitized routing, no inherited
  overrides — P2V §5). Source/survey snapshot comparison at the end must
  allow EXACTLY the owned write set, nothing else (P2R §5 pattern).
- Cooperative ownership: root/ancestor identity rechecked before, between,
  and after writes (P2R §5.3 pattern); unexpected replacement stops with NO
  foreign cleanup; creation failure confers no ownership.
- Predictable no-write failures (preflight): invalid State/authority,
  scope/retention/basis negative, alias/traversal/nonregular inputs,
  namespace overlap of owned destinations with live inputs, pre-existing
  owned outputs (refuse — never overwrite-to-rerun), tool-closure drift,
  HEAD drift. All leave live bytes untouched (P2R §5.2: "No
  directories/files are written on predictable preflight failure").
- Partial state: owned partials are PRESERVED and reported with
  path/status/phase classification (pass-1 precedent `:425–429`,
  `:430–435`); live originals must be byte-proven unchanged in the failure
  report. Manifest/record completion is observational — a crash may leave a
  physically valid record without a delivered success (P2R §5.5); readback
  can establish consistency but never invents the success event.
- Retry/recovery: NO automatic retry, rollback, truncation, cleanup,
  or partial-resume. Retry against any existing owned output refuses; a
  stale/incomplete tree needs a separately authorized recovery decision
  (P2R §5.4). No global CAS, no crash atomicity, no hostile-writer
  exclusion, no durability beyond close+readback (P2R §5.5, P2V §5).
- Retention-before-replacement (hard rule): mutable live bytes must not be
  replaced before their old bytes are safely retained — P2R capture + P2V
  observation in the writer's own invocation prove the retained set FIRST;
  the writer's first mutation follows. This order is load-bearing for the
  whole design.

## 4. Staged-only vs live adoption; the readback cycle (Q4)

### 4.1 Exact validation-context boundary

| Context | May run on staged bytes | Must run on live bytes | Authority claimed |
|---|---|---|---|
| Staged replay check (P3, §6) | YES (only context) | — | None — deterministic recomputation, STAGED_ONLY labeled |
| Scope review (existing) | YES (after path+sha) | — | Reviewer judgment on staged delta, not adoption |
| P1 validate / P2R / P2V | Staged refs + live basis as today | Live basis/current State | Proposal validity, persistence, current-basis observation — never adoption |
| Receipt / Gate / manuscript / bundle / Candidate validators | NO (canonical live paths required) | YES | Publication authority — only post-install |
| Revalidation adoption (`control:1773`) | NO | YES | New authority record — only post-QA |

Staged receipts/QA validate WITHOUT manufactured State/Profile and WITHOUT
any public permissive pending flag: the staged replay check recomputes
surface→canonical-bytes→serializer-bytes equality (the receipt FILE-byte
oracle `:741–742` scoped to versioned paths) and schema validity, producing
an in-memory result labeled `STAGED_ONLY`, consumed solely by the scope
reviewer and the writer's preflight. It references the REAL healthy State
only to prove the basis it was derived from (P1 data), never to bless staged
bytes as live. No `live=False` synthesis, no pending-basis bypass (Weekly
`:481–487` explicitly out of scope), no public flag any live validator
could mistake for permission.

### 4.2 After-adoption readback avoids the healthy-State cycle

The apparent cycle: readback (`load_derivation_for_readback :1142`)
requires healthy State, but adoption changes the bytes State blesses — so
which comes first? Resolution: **authority flows adoption → readback, not
readback → adoption.**

1. Writer installs bytes under fully preflighted old authority (retention
   proven, §3.1) — installation is a guarded mechanical act, not an
   authority claim.
2. The normal generation/QA/review/Candidate chain runs on installed bytes;
   `revalidate_publication_surface` establishes the NEW immutable record
   (truthful reason, §5) and updates the State pointer — THIS is the moment
   new authority is born, grounded in fresh QA + genuine reviews, not in
   the old State.
3. Subsequent `load_derivation_for_readback` under the NEW State validates
   new bytes normally. No former-State dictionary is ever manufactured, no
   pending bypass invoked, no public flag consulted.

The existing revalidation mechanics already support changed surface rows —
`_collect_pending_rows` (`:711–743`) classifies kept vs canonically-changed,
and `revalidate_publication_surface` rebinds superseded rows with fresh QA
(`:1844–1886`, `:1900–1944`). What is missing — and what no relabeling
supplies — is (a) the corrected-reader role in the role set (§1.7: reader
JSON is not among the 7 roles, so changed reader bytes cannot appear as a
legitimate changed row today), (b) a truthful reason class (§5), and (c) the
versioned-target provenance binding (§2). An enum-only patch (adding a
reason string, or renaming REVIEWED_CORE_CHANGE) fixes none of these; the
old-byte-only reading of revalidation is equally false — the mechanism
handles new bytes fine, it is the editorial authority/closure/ownership
integration that is absent. Both misreadings are rejected here explicitly.

## 5. Truthful reason/record, State bindings, chain vs pointer, normal chain (Q5)

### 5.1 Required record semantics

The adoption record (P4) carries a truthful reason object — not a bare enum:

- `reason_class`: a NEW, explicitly selected class (name selected by Astra;
  General proposes `REVIEWED_EDITORIAL_CORRECTION` as a candidate ONLY —
  selected only if Astra agrees it denotes exactly: staged-reviewed
  editorial delta within approved authority, installed via versioned-target
  admission, with retained old bytes).
- `reason`: structured, machine-checked bindings — proposal ref (path+sha),
  retention manifest ref, scope review ref (with its before/after/upstream
  triple), versioned→installed byte-equality proof refs, retained-set
  verification summary, installer identity + recorded_at. Every ref is a
  (path, sha256, byte_count) triple rechecked at adoption, not copied text.
- State bindings: `original_checkpoint` (immutable validation checkpoint,
  unchanged — history is never rewritten), `active_before` (the exact
  State-bound revalidation chain head being superseded, resolved via
  `_active_effective` semantics, never filename-selected), `new_after`
  (the new record; State pointer advances to it with the expected-bytes
  rewrite pattern `control:1999–2011`).

### 5.2 Existing-chain extension (Alternative E) vs separate pointer/record (Alternative S)

**E — extend the publication_surface_revalidation chain.** New record with
the new reason class appended to the existing sequence
(`_revalidation_record_path`, sequence+1 `:1954`, collision refuses
`:1956`); `publication_revalidation_provenance` advances; prior records
 byte-identical. Consumers already traverse this chain
(`_resolve_publication_revalidation`, stage `_prior_artifacts`,
`_publication_approval_artifacts`). Touchpoints: `REVALIDATION_REASON_CLASSES`
(`:45`) + revalidation schema (new class + reason bindings + corrected
role(s)) + role set (add corrected-reader-input role and/or generated-output
coverage confirmation) + reason-shape validation in
`revalidate_publication_surface`. Full consumer budget: revalidation readers
(control chain resolvers, stage validation, human-gate approval binding)
need NO logic change — they consume the chain generically; only the
admission predicate (reason class + roles + QA) is extended. History stays
one chain; `supersedes` links (§1.7 `:1953`, `:1983`) give the audit trail.

**S — separate editorial-adoption pointer/record.** New State field (e.g.
`editorial_correction_provenance`) + new schema + new resolver, with every
chain consumer taught to consider two heads (active-record resolution,
pending-basis construction, stage prior-artifacts, approval binding,
mechanical-refresh inventory). Larger touch surface, two-head precedence
rules to specify and test, and a permanent fork in authority resolution for
a one-shot-per-correction event. Benefit claimed: zero change to the
revalidation reason enum. But §4.2 already shows the enum is not the hard
part — roles + bindings are — so S pays the fork cost without avoiding the
real work.

Proposal: **E**. S is rejected on full-consumer-budget grounds (every
authority resolver × two-head logic, forever) for no offsetting gain.
Under E, the "existing chain" concern — that old revalidation records were
earned under REVIEWED_CORE_CHANGE — is answered by immutability: old
records are never edited; the new record's new reason class is explicit at
its own sequence number.

### 5.3 Normal fresh Candidate/Preview/Freeze/Release; no Candidate-as-publisher

After the State pointer advances, the edition is a healthy VALIDATED_DRAFT
with new authority. What follows is the ORDINARY chain with zero special
cases: `build_manuscript_manifest` → generation → Gate → bundle → genuine
post-build semantic + visual reviews → `build_candidate` (`:668`, consumes
reviewed bytes, immutable output) → `validate_publication_candidate`
(handlers `:378`) → Human Preview approval → Freeze (`:394`) → Release
(`:434`). `build_candidate` is never given provisioning duties: it takes
(exact paths to already-reviewed artifacts) and emits one immutable file.
Any design letting the Candidate builder fetch, derive, or bless correction
bytes is the already-superseded Candidate-as-publisher conflation (P2R §1,
P1 contract §6) and is refused here again.

## 6. Recommended next implementation boundary (Q6)

### 6.1 Considered and rejected: single full end-to-end implementation unit

A single unit spanning staged builder + versioned-target validator
parameterization (receipt ×2, Gate, manuscript, bundle rule) + writer +
revalidation reason/roles + State adoption + fresh-chain proof would touch
~10 production validators plus the State writer in one diff, with oracle
scope covering staged determinism, admission binding, ownership/fault
mechanics, AND full-chain acceptance. That diff is not independently
reviewable in the P1/P2R/P2V scoped-unit precedent (2–3 paths per unit with
exact budgets), its failure attribution would be ambiguous, and its budget
can only be guessed before the versioned-target relation is selected. It is
rejected as one unit — NOT as a goal: the end-to-end shape is fully
specified across §§2–5 so no unit forks.

### 6.2 Recommended: P3 staged correction builder + staged replay admission

**Boundary:** deterministically derive the staged proposed-reader bytes
from the already-staged authoring input through the REAL route loaders, and
prove staged FILE-byte determinism — ending at bytes the EXISTING
validators (P1, scope review, P2R, P2V) already consume. No receipt/Gate/
manuscript/Candidate objects emitted, no live writes, no State change.

Concrete consumer (no dead end): P1 `validate_proposal`'s exact staged
FILE-byte comparison (`:1865–1867`) + `_validate_scope`'s after-binding
(`:1786–1835`) + P2R staged-ref verification + P2V staged equality all read
the staged reader file TODAY (currently staged opaquely by fixtures). P3
replaces opaque staging with derived-and-replay-proven staging; every output
is consumed the day it lands. The explicitly remaining adoption debt is P4
(§§2,3,5 specified here, implemented after Astra selection) — listed, not
dropped.

Exact budget — **2A / 0M / 0 schema** (any more is a blocker back to Astra):

1. A `scripts/survey_editorial_correction_builder_v2.py`:
   `build_staged_reader(root, state_path, proposal_id) -> result` (in-memory
   dict: `STAGED_MATERIALIZED` | `STAGED_REUSED_SAME_BYTES`, staged refs
   with path/sha/size, canonical digest, `input_hashes`; structured
   `CorrectionBuilderError` with code/phase/cause). Behavior: pin State +
   Profile + staged authoring (raw-first, alias/traversal/nonregular
   refusal); require P1-equivalent healthy basis (strict State, eligibility,
   canonical State path — reuse P1 private data helpers where feasible per
   the P2V factoring pattern, no logic duplication); derive surface via the
   actual route loader for the validated Profile (Longform readback-shaped
   derivation / Weekly strict derivation, pending fallback FORBIDDEN);
   assert proposed ≠ active reader (same-byte is a no-editorial-change
   refusal, not R1 routing); exclusive-create the staged
   `reader-surface-input-v2.json` from canonical bytes; readback-compare
   FILE bytes; final pin reverify. Pre-existing different bytes refuse (no
   overwrite-to-rerun); same bytes reuse only after full rederivation
   equality (pass-1 S3 precedent `:436–455`).
2. A `tests/test_survey_editorial_correction_builder_v2.py`: real
   accepted-chain synthetic fixtures (Longform authored prose primary,
   Weekly envelope-only, real R1-predecessor active-before distinction —
   never genuine approvals), oracles: staged determinism (rebuild → same
   bytes), canonical-FILE-byte equality (noncanonical serialization
   refused), Longform/Weekly positives, immutable-body/upstream negatives,
   same-byte-reuse vs different-byte-refusal, alias/FIFO/traversal,
   State/control/authoring drift preflight refusal with owned-tree no-write
   except the single staged file, close-fault partial classification.
   Estimated 10–14 methods; runtime class ~P2V full3 (no number promised
   before the diff).
3. 0 schema (result dict only, P2V pattern), 0 modifications (P1/P2R/P2V,
   loaders, validators all read-only in P3). If the diff cannot fit —
   e.g. a loader cannot run in staged context without behavior change —
   that is an EXACT blocker returned to Astra, not implicit edit authority.

Acceptance before P4: scoped green on the new tests + affected P1/P2R/P2V
regression evidence (no decorative full-suite rerun, P2V B1 precedent);
saved-patch proof pattern reused; stop at Human Commit Point.

### 6.3 P4 entry contract (designed here, implemented after selection)

P4 implements §§2–5: versioned-target admission parameters in receipt ×2 +
Gate 4th route + manuscript binding + bundle staged rule; writer with §3
preflight/ownership/failure contract; revalidation reason class + role(s)
under Alternative E; normal fresh Candidate chain proof. P4's oracles:
versioned→installed byte-equality adoption on synthetic Longform + Weekly +
R1 editions, invalid-live-window absence (live bytes untouched until writer
preflight passes), second-review-free admission with genuine scope review
only, post-adoption readback health under new authority, full refusal
matrix of §3.3.

### 6.4 Explicit blockers (none hidden, none manufactured)

- **No hard blocker for P3.** All inputs exist: route loaders, canonical
  byte functions, staged path layout, and four existing consumers.
- **One Astra selection required before P4 implementation:** Alternative V
  (§2.3) and Alternative E (§5.2) are General proposals; if Astra selects L
  or S instead, P4's budget and touch list change accordingly — P3 is
  unaffected either way (staged bytes + scope review are common to all
  futures).
- **No new Human role/Gate and no production-owned fixture are required**
  at any point: oracles use synthetic accepted-chain fixtures per the
  P1/P2R/P2V precedent; genuine semantic/visual/Human approvals remain
  real-world obligations at correction USE time, never test fixtures.

## 7. Preserved boundaries and real lifecycle costs (Q7)

Preserved unless Astra explicitly decides otherwise with stated justification:
accepted Draft/upstream/Architecture authority; healthy-VALIDATED_DRAFT +
approved-Architecture + pending-Preview entry predicates; no
exception-lifecycle import, no false Core-change reason, no authoring
override of frozen fields, no generic resolver/framework/dashboard, no
deferred-maintenance batch. DM021 stays OPEN; whole NOT_READY; step4/B3
OPEN; audit unstarted.

Real total costs named (unknown ≠ zero, savings unclaimed):

- P3: ~10–14 new test methods (P2V-class runtime, minutes-to-hours of
  machine time), fixture construction (accepted-chain synthetic editions ×
  2 routes + R1 predecessor), General implementation + Astra review +
  independent review labor, saved-patch/proof packaging.
- P4: validator parameterization + writer + adoption record across ~10
  touchpoints with per-touchpoint oracles; full-chain synthetic proof.
- Per-correction USE cost (not component cost, but must not be hidden):
  one genuine scope review + normal post-build reviews + Human Preview per
  correction; staged storage per proposal (`authoring-input.json`,
  staged reader, proposal, manifest, retained tree); repeated full receipt
  derivations inside every preflight (P2V §7 pattern — measured, not
  optimized away by caching authority).
- What is NOT paid: no new standing role, no production fixture pipeline,
  no second live review per correction under Alternative V, no re-audit of
  the 21 deferred items.

Stop here for Astra review of the selected architecture — not a Human final
unit closeout until the design is selected and independently reviewed.
