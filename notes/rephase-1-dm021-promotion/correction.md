# Correction to initial promotion analysis + retention-only P2a design

2026-10-13 JST, design Co-Worker. `analysis.md` and `source-binding.md` are
preserved unmodified; this file corrects them and proposes a concrete
retention-only increment. Design-only: no code/schema/test changes, no
fixtures, no runs, no adoption. All citations are candidate-relative
`file:line` to observed source (full filenames; alias legend at §8).
DM021 remains OPEN; whole NOT_READY.

## 1. Errata to `analysis.md` (initial text preserved; these supersede it)

- **E1 — changed-byte revalidation semantics.** Analysis §1 claimed the
  existing revalidation only binds old bytes. Wrong:
  `scripts/survey_agent_control_v2.py:1844-1876` expressly compares original
  rows with live bytes and admits changed publication-surface rows (changed
  rows become `superseded` at `:1863-1870`; unchanged-outside-surface drift
  refuses at `:1871-1872`; empty superseded set refuses at `:1875-1876`).
  The existing API is a changed-byte-capable revalidator under its
  restricted reason. The real promotion gaps are: (a) no truthful editorial
  authority (closed reason set at `:45` admits only `REVIEWED_CORE_CHANGE`),
  (b) no full dependency/retention closure (seven roles at `:685-693` vs
  P1's typed graph), (c) no path/State/pending integration for the
  replacement window (§3 below). Corrected blocker: reason + closure +
  pending-cycle design, not "fresh QA" alone (fresh QA already exists at
  `:1898-1944`).
- **E2 — review/generation order.** Analysis §2/§9 ordered
  "materialize → receipt → review". Wrong for any path that includes TeX:
  the Longform publisher requires the persisted pre-TeX semantic PASS
  BEFORE TeX/BibTeX/style materialization
  (`scripts/survey_longform_semantic_publication_v2.py:462-497`,
  "materialization prohibited until semantic review PASS" at `:480-486`;
  pass1 surface-only at `:370-371,416-460`, pass2 generation at `:372-390`
  plus writes after `:558`). The receipt validator itself consumes that
  review (`scripts/survey_longform_generated_v2.py:686-693`). Correct order:
  derive + materialize reader surface (pass1) → pre-TeX scope/semantic PASS
  → generate TeX outputs (pass2) → receipt → Gate → QA bundle → post-build
  semantic/visual (distinct roles from pre-TeX scope review and from Human
  Preview; no conflation, no automatic PASS).
- **E3 — live-path second review is not the default.** A genuine second
  review of the installed live path avoids same-SHA rebinding but doubles
  independent semantic work and opens a live-invalid waiting window (new
  bytes installed, no passing review yet). The alternative — a
  versioned-target binding carried by a correction-specific receipt
  (`reviewed_proposal_ref` + `installed_live_ref` with proven byte equality)
  — must be compared on evidence cost and failure windows before either is
  selected. Analysis §3's "new review is the simpler binding" is withdrawn
  as an unmeasured default.
- **E4 — budget withdrawn.** The §9 "1A1A2M" total is unsupported: the
  consumer matrix (§3) shows readback/resolver/Gate/publisher/contract-closure
  integration questions that are not yet inventoried tightly enough to price.
  Replaced by cost drivers + comparison (§7); no tiny fixed total is offered.
- **E5 — blocker (iii) withdrawn.** Lack of a production-owned fixture is
  NOT a requirement for a new Human gate and does not block engineering
  verification: valid synthetic accepted-chain fixtures (real derivation
  through accepted authority, as P1's fixtures do) suffice for
  verification; genuine semantic/visual/Human approvals remain a separate
  future acceptance layer. Corrected blocker: author-independent review of
  THIS design + Astra's record/reason choice (§7).

## 2. Source-binding corrections

- **Mislabeled paths.** `scripts/survey_reader_surface_gate_v2.py`
  (`e7305884…`) and `schemas/reader-surface-gate-v2.schema.json`
  (`fe4a96f4…`) are LF2I-inherited modifications, NOT P1 modifications.
  P1's increment is 3A + 1M: added module (`5d2fde45…`), added proposal
  schema (`5623c0d9…`), added test (`f581fad0…`), and modified ONLY
  `schemas/reader-surface-semantic-review-v2.schema.json` (`e8598239…`,
  the optional scope block). The table's "(P1 M)" tags on the two Gate
  paths are corrected to "(LF2I M, inherited unchanged by P1)".
- **Transcripts vs summaries.** The Git/hash observations in
  `source-binding.md` §§1–2 were executed as described (sanitized env, all
  rc=0, `ALL_MATCH`) but raw command transcripts were NOT persisted to
  evidence files; the section is a contemporaneous summary, not a raw log.
  No further hashing/tests/restoration are required for this unit; source
  stays read-only.

## 3. Full-adoption consumer matrix (actual; why no unchanged-validator bridge)

If live bytes change, each consumer below must run against the NEW bytes,
but during the replacement window the tree is half-old/half-new while State
still pins old bytes — and a bare new State pointer (written only at the
END of adoption) cannot authorize the validators that must run BEFORE it.
This healthy-State/canonical-path pending cycle is the unselected core of
full promotion; enumerating it is not selecting it.

| Consumer (actual callsite) | What it demands | Breaks during replacement because |
|---|---|---|
| Initial Longform derivation `survey_longform_derivation_v2.py:1101-1139` | exact `DRAFT_COMPLETE` + configured handler (`:1117-1131`) | healthy `VALIDATED_DRAFT` correction State is ineligible; old State pins old bytes |
| Readback derivation `:1142-1182` (allowlist `:954`) | healthy lifecycle; explicitly excludes pending/editorial renewal (`:1149-1151`) | no staged/editorial authority exists yet — that exclusion is the gap |
| Weekly derivation `survey_weekly_derivation_v2.py:475-570` | strict State; auto pending-basis branch at `:481-487` | editorial has no equivalent checked-pending mechanism; Weekly's own branch shows the SHAPE of what would need designing, not a reusable path |
| Publisher two-pass `survey_longform_semantic_publication_v2.py:370-414,551-573` | pass1 refuses with pre-existing partial outputs (`:410-414`); S3 refuses existing artifacts before writes (`:551-553`); same-byte reuse only for healthy sets (`:436-455`) | old outputs occupy canonical paths; corrected install collides by design |
| Longform receipt `survey_longform_generated_v2.py:698-730` | strict healthy-State derivation reload + canonical surface/archive/receipt paths (`:721-730`) | half-replaced tree fails reload; canonical paths hold mixed bytes |
| Gate replay `survey_reader_surface_gate_v2.py:1794-1839` via `:1145-1231` | recorded route/receipt equality (`:1836-1837`) | old Gate record mismatches new derivation until a new Gate exists |
| Pending basis `survey_agent_control_v2.py:711-784` (`_collect_pending_rows`, `built_checked_pending_publication_basis`) | checked disk-bound context with pre/post rechecks | scoped to publication-surface rows under `REVIEWED_CORE_CHANGE`; editorial before-graph/retention/scope bindings are outside it |
| Record/State machinery `:657-683,1844-1886,1995-2046` | sequence paths, surface roots, exclusive create + atomic replace + disposition-classified rollback | assumes the pending basis above; no editorial equivalent selected |
| Contract closure `survey_production_v2.py:129,150` (`repository_commit_sha`, `contract_identity`) | HEAD/contract pinning in receipt + revalidation `core` blocks | uncommitted-overlay correction bytes have no HEAD identity; commit policy for corrections is unchosen |
| Candidate/Preview `survey_publication_v2.py:749,817`, `survey_agent_control_v2.py:1465-1497` | canonical Candidate + `RELEASE_CANDIDATE`/pending Preview | rebuilding the Candidate from corrected bytes re-enters the publisher cycle above |

Consequence: full promotion needs a designed pending/staged authority
mechanism (what evidence authorizes validators mid-replacement, and how it
terminates), not merely "run existing validators against new bytes."

## 4. Retention-only P2a contract (recommended next increment)

A bounded preparatory component: persist + prove old-byte retention for one
validated P1 proposal. No staged/live reader installation, no source/build/
QA writes, no reason/pointer changes, no adoption, no second State pointer
or reason anywhere in its schema.

- **APIs** (new module, e.g. `scripts/survey_editorial_retention_v2.py`):
  `capture_retention(root, state_path, proposal_path) -> manifest` (writes
  ONLY under the proposal's retained namespace + one manifest path, §5) and
  read-only `verify_retention(root, manifest_path) -> verdict` (§6).
  Input reads follow P1's raw-safe pattern: lexical traversal/alias checks
  before any read, FIFO/device refusal, pinned bytes, pre/post reverify
  (`scripts/survey_editorial_correction_proposal_v2.py:87-135`
  `_Collector.__init__`/`safe`, `:191-234` `reverify`).
- **Output paths (exact).** Per COPY node:
  `<proposal_dir>/retained/before/<original_repo_relative_path>`
  (destinations already fixed by P1's plan at `proposal_v2.py:1247`).
  Completion artifact, written LAST:
  `<proposal_dir>/retained/retention-manifest.json`.
  Owned inventory is exactly these paths — finite, closed, enumerated from
  the proposal's `retention_plan` at preflight; any other write refuses.
- **Manifest schema (strict keys).** Header: `schema_version`
  (`RETENTION_MANIFEST_V1`), `proposal_ref` {path, sha256},
  `before_graph_digest`, `preserved_upstream_digest`, `state_ref`
  {path, sha256-at-capture}, `validation_checkpoint_ref`,
  `active_revalidation_ref|null` (all COPIED from the validated proposal's
  `basis`, `proposal_v2.py:1462-1476` — fingerprints for staleness
  comparison, NOT authority; no State-pointer update, no `reason_class`,
  no `reason`, no adoption claim). Rows: one per plan row —
  `roles/path/sha256/byte_count/policy` plus EITHER `retained_ref`
  (KEEP: the live path+sha as observed, not a copy — KEEP refs stay live
  immutable references, this is not a self-contained backup) OR
  `retained_dest` + `retained_sha256` + `retained_byte_count` (COPY, verified
  equal to the plan row). Manifest bytes are canonical JSON; no unbound
  (plan-orphan) rows permitted.
- **Frozen proposal/before-graph relation.** `capture_retention` first
  re-runs P1 `validate_proposal` semantics against CURRENT bytes (proposal
  must still validate; drift ⇒ refuse — retention never blesses stale
  authority). Copies are verified byte-equal to plan rows before the manifest
  is exclusively created; manifest creation is the completion event. Before
  the manifest exists, retention is incomplete; after, it is complete.
- **P1 strictness preserved.** P1 `_retention_plan` refuses existing COPY
  destinations (`proposal_v2.py:1278-1282`) and P1 itself is unchanged by
  this component. Consequence, stated plainly: after a successful capture,
  unchanged P1 `validate_proposal` CANNOT re-validate (destinations now
  exist) — that is correct and intended. Post-write proof belongs to
  `verify_retention`, not to re-running P1. The writer MUST NOT delete
  retained bytes to make P1 pass (deletion-to-rerun bypass forbidden, §5).
- **Same-request retry / partial handling.** Failure before manifest:
  partial owned copies REMAIN (never silently deleted); no manifest ⇒
  incomplete, honestly reported per-node (copied / verified-present /
  failed + reason). Retry: verify-then-adopt — an existing destination with
  bytes exactly equal to the plan row is adopted (convergent retry); a
  divergent existing destination REFUSES (never overwritten, never deleted).
  Only when ALL rows verify does the writer exclusively create the manifest.
  Manifest existence + `verify_retention` PASS ⇒ complete; anything else ⇒
  explicitly incomplete. Cross-request reuse by future promotion is NOT
  claimed at capture time (§6).
- **Proof scope (explicit).** `verify_retention` proves ARTIFACT
  PERSISTENCE: retained COPY bytes == manifest == captured plan rows, and
  manifest self-consistency (no orphans, KEEP refs reported with live-drift
  status: KEEP drift is reported, never repaired). It does NOT prove
  CURRENT_ELIGIBILITY: whether the captured basis is still the active
  authority is a fresh-P1-run question at promotion time (compare fresh
  `before_graph_digest`/State pin/contract against the manifest's captured
  fingerprints; mismatch ⇒ stale evidence, stop — never force-fit).
  Future promotion MUST still recheck fresh authority; the manifest makes
  that check possible without inventing adopted authority.

## 5. Failure matrix (retention writer)

| Situation | Behavior |
|---|---|
| Traversal/alias/FIFO/device input, unsafe ancestor | refuse before any read (P1 `_Collector` pattern) |
| Proposal fails P1 validation at capture (drift/stale) | refuse, no writes |
| COPY destination absent | exclusive-create copy, readback-verify sha/size |
| COPY destination present, bytes equal plan row | adopt (convergent same-request retry) |
| COPY destination present, bytes differ | REFUSE (no overwrite, no delete); manifest withheld |
| KEEP live bytes drifted vs plan | record drift in result; refuse completion (cannot retain what changed) |
| Crash/mid-run failure | partial owned copies remain; no manifest ⇒ incomplete; retry converges per above |
| Manifest exists but a retained byte later changes | `verify_retention` FAILs that row (persistence broken, honestly reported) |
| Caller deletes retained bytes to re-run P1/capture | forbidden bypass; verifier cannot distinguish deletion from never-captured — manifest absence ⇒ incomplete either way |

## 6. Oracles (behavior-based, no execution in this unit)

Positive: one synthetic accepted-chain edition (real derivation through
accepted authority, both routes) reaching manifest-complete with
`verify_retention` PASS, plus pre-TeX-scope-bound proposal variant binding
the same manifest. Negatives/controls: divergent-destination refusal;
partial-failure ⇒ no manifest; post-capture byte tamper ⇒ verifier FAIL;
KEEP drift ⇒ reported (not repaired); stale-basis capture ⇒ P1-validation
refusal; deletion-to-rerun ⇒ still incomplete. Genuine semantic/visual/Human
judgment is NOT part of this oracle (future acceptance layer).

## 7. Cost comparison (drivers, not a fixed total)

- **P2a retention-only (recommended):** 1A writer module + 1A manifest
  schema + 1A focused test + narrow loader reuse of P1's `_Collector`
  discipline (no P1 behavior change). Cost drivers are bounded: closed
  inventory, exclusive-create I/O, byte-compare verification. No validator,
  receipt, Gate, publisher, contract, State, or Candidate integration —
  that is the point.
- **Full promotion (deferred):** additionally requires the pending/staged
  authority mechanism (§3 table: readback exclusion, publisher existing-
  output refusal, receipt healthy-State reload, Gate record mismatch,
  HEAD/contract pinning for uncommitted bytes, Candidate rebuild re-entering
  publishers, review-ordering with live-invalid window). Each row is a
  designed contract question, several with genuine alternatives (E3); pricing
  the sum now would repeat the withdrawn E4 error.
- Sequencing P2a first is justified investment even if promotion stalls:
  verified old-byte persistence is prerequisite to every alternative,
  including rollback and audit.

## 8. Alias legend + observation note

`proposal_v2.py` = `scripts/survey_editorial_correction_proposal_v2.py`;
`agent_control_v2.py` = `scripts/survey_agent_control_v2.py`;
`longform_generated_v2.py` = `scripts/survey_longform_generated_v2.py`;
`longform_derivation_v2.py` = `scripts/survey_longform_derivation_v2.py`;
`weekly_derivation_v2.py` = `scripts/survey_weekly_derivation_v2.py`;
`surface_gate_v2.py` = `scripts/survey_reader_surface_gate_v2.py`;
`core` = `scripts/survey_production_v2.py`;
`publication` = `scripts/survey_publication_v2.py`.
Prior Git/hash observations were executed as summarized (sanitized env, all
rc=0) without persisted raw transcripts; the summaries stand as
contemporaneous records, not replayable logs. No new hashing/tests/
restoration performed or needed; candidate source untouched.

## 9. Concrete P2a proposal + remaining blockers

Propose Astra select: retention-only P2a per §4 (capture + standalone
verifier + manifest schema + focused tests reusing P1 fixtures' accepted-
chain discipline), with the §5 failure matrix and §6 oracles as acceptance,
P1 behavior unchanged, and full promotion explicitly deferred pending the
§3 pending-authority design. Remaining blockers: (i) author-independent
review of THIS correction; (ii) Astra's P2a go/no-go (decline is coherent —
retention without a chosen promotion consumer is evidence without a reader,
though still rollback-useful); (iii) NO new Human gate and NO production
fixture required (E5). On selection, the next unit is P2a interface/fixture
return then bounded implementation — not adoption. DM021 OPEN.
