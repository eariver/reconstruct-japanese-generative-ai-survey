# DM021 promotion/adoption contract analysis (design-only)

Co-Worker analysis for Astra. Design-only: no code/schema/test changes, no
fixtures, no runs, no adoption. Source pins and exact callsites are bound in
`source-binding.md`; citations below use candidate-relative `file:line`.
DM021 remains OPEN; whole NOT_READY, step4/B3 OPEN, canonical audit unstarted.

## 0. Source basis observed (not assumed)

Detached HEAD `409b292…`/tree `8ce36998…` + exact 13-file overlay (3M+10A),
all 13 sha256/mode re-observed equal to final `freeze-pre.json` (see
`source-binding.md` §§1–2). Assessment §4 scope governs: P1
(`prepare_proposal`/`validate_proposal` returning only `REVIEW_REQUIRED` /
`REVIEW_BOUND_PROPOSAL`, `proposal_v2.py:50-51`) establishes the before-graph
and retention **plan**, not retained bytes, writer, reason, or adoption.

## 1. Initial proposal (preserved; partially superseded below)

1. Reuse the existing `revalidate_publication_surface`
   (`agent_control_v2.py:1773`) record with `REVIEWED_CORE_CHANGE`
   (`:45`) and a truthful editorial reason string; carry the versioned
   proposal reader through materialization/receipt/Gate/QA; persist old bytes
   per P1's retention plan at promotion time; adopt State by updating
   `publication_revalidation_provenance`.
2. Keep both routes on their P1 derivation paths (Longform readback loader /
   Weekly current-State loader, `proposal_v2.py:431-445`).
3. Treat the existing Gate + receipt revalidation as sufficient changed-byte
   authority once the new bytes are installed.

Corrections to this initial proposal (§§2–4): item 3 is **rejected** — the old
seven-artifact revalidation rows bind OLD bytes only
(`agent_control_v2.py:1844-1886` compares live bytes to prior rows and
refuses drift outside the surface at `:1871-1872`); installing changed reader
bytes without fresh derivation/receipt/review/Gate/QA + a truthful new
adoption record is exactly the false completion this analysis must prevent.
Item 1's reason reuse is likewise **rejected** as a false core-change label
(contract decision §2.1; P1 adds no reason by design, `proposal_v2.py:1-23`).

## 2. Recommended architecture: three bounded increments, one contract

A single whole-writer ("general correction promoter handling arbitrary
reader deltas") is not recommended: it couples retention durability, receipt/
Gate replay, reason taxonomy, and State adoption into one unreviewable blast
radius with unknown cost. Recommend instead a correction-specific admission
sequence with three separately contractable increments under one design
decision:

- **P2a — owned retention writer.** Realizes P1's plan: before any
  destructive replacement, copy every `COPY_BEFORE_REPLACEMENT` node byte to
  its deterministic `<proposal_dir>/retained/before/<path>` destination
  (`proposal_v2.py:1247`), verify path/sha/size into a typed manifest mapping
  original {path,hash,size} → retained path, and refuse on
  traversal/alias/overlap/conflict/pre-existing destination (the plan's own
  refusal catalogue at `proposal_v2.py:1235-1284` becomes writer preflight).
  `KEEP_IMMUTABLE` rows stay by reference (`retained_ref`, `:1244-1245`).
  Durability claimed is only what the writer implements and verifies
  (exclusive-create + readback, on the `agent_control_v2.py:2027-2046`
  pattern); no global CAS/crash-atomicity (`:1559-1567`).
- **P2b — correction admission (materialize → receipt → review → Gate →
  QA/build).** Installs the independently derived canonical proposed bytes
  (`proposal_v2.py:1386-1389`, inequality enforced at `:1388-1389`) to the
  canonical live reader path (NOT the versioned proposal path), then runs the
  complete fresh chain over the NEW bytes: route receipt validator (Longform
  `longform_generated_v2.py:665`, which itself reloads the review at
  `:686-693`, enforces canonical edition paths at `:721-730`, and replays
  exact FILE bytes + deterministic outputs at `:735-757`), fresh independent
  semantic review carrying the `EDITORIAL_CORRECTION_SCOPE_V1` block bound to
  exact before/after/upstream (`proposal_v2.py:1635-1695`), fresh visual
  review, Gate evaluation with mandatory semantic authority
  (`surface_gate_v2.py:1234-1260`) and record validation replaying derivation
  (`:1794-1839`), quality bundle (`quality_v2.py:232`), and deterministic
  build replay. The versioned proposal reader artifact and its review bytes
  are preserved immutable; the live installation references them, never
  re-targets them by same-SHA (§3).
- **P2c — truthful adoption (new record + State pointer + Candidate
  rebuild).** Writes a correction-supersession record and adopts it in State,
  then rebuilds the Candidate through the normal chain (§6). See §§4–5 for
  the record-vs-reuse decision and reason semantics.

Useful next contract if full promotion stays underdetermined: **P2a alone**
(retention writer + manifest verifier) — it converts plan into verifiable
persistence without touching reason/State/Gate authority, and every later
increment depends on it.

## 3. Immutable reviewed-path preservation (no same-SHA rebinding)

The Gate binds exact (path, sha) pairs: Longform reviewed-target and review
equality at `surface_gate_v2.py:1178-1181` with canonical-suffix enforcement
at `:1162-1169`; Weekly equivalents at `:1211-1214`; canonical edition paths
(`reader-surface-input-v2.json`, `interactive-semantic-publication-input.json`,
`validated-source-manifest.json` as edition siblings) at
`longform_generated_v2.py:721-730`. P1's active-before check already refuses
path rebinding (`ACTIVE_PATH_REBIND`, `proposal_v2.py:401-402`).

Promotion rule: the reviewed proposal artifact at
`<source_root>/publication/v2/editorial-corrections/<proposal_id>/reader-surface-input-v2.json`
(`proposal_v2.py:1329-1343`) is never moved, overwritten, or re-targeted. The
correction receipt/Gate for the LIVE canonical path must either explicitly
reference the reviewed proposal artifact (new correction-specific receipt
contract carrying both `reviewed_proposal_ref` and `installed_live_ref` with
byte equality proven) or obtain a genuine new review of the live path. A new
review of the installed live bytes (P2b default) is the simpler binding: it
reuses existing validators unchanged and leaves the no-rebinding invariant
untouched. Same content at a different path authorizes nothing.

## 4. Retention: actual bytes, owned writes, predictable failure

P1's graph policy is deterministic (mutable ⇒ COPY, else KEEP;
`proposal_v2.py:597-599`, mutable set `:574-595` including effective rows,
receipt outputs, receipt, reviewed reader, bundle results, State, pre-TeX
review, publication-authored inputs). P2a's writer owns: all
`<proposal_dir>/retained/before/**` destinations, verified against the
proposal's `retention_plan` row-for-row (path/sha/`byte_count`, KEEP vs COPY
per `proposal_v2.py:1240-1246`). Owned write set at promotion extends to: the
canonical live reader input, the new authored-input installation (if the
route's loader requires the authored file at its canonical live location),
the new receipt file, new review/Gate/QA records, the supersession record,
and the State file — each created exclusively from known bytes then
read-back verified, following `agent_control_v2.py:1995-2046`.

Predictable failures (fail-closed, operator-actionable): preflight —
traversal/alias/overlap/conflict/collision (`proposal_v2.py:1248-1284`,
`agent_control_v2.py:1955-1957,2022-2023`), stale basis or mid-call drift
(`proposal_v2.py:1623-1631,1813-1821` pattern; `:1996-2021`);
operation — record-created/State-not-adopted (orphan preserved, manual
recovery; `:2047-2090` disposition logic), State-adopted (never delete the
record; roll State back first; `:2091-2149`); retry — re-running against
already-current bytes refuses via nothing-to-supersede
(`:1796-1798`); drift of any upstream outside the surface refuses
(`:1871-1872`, `_verify_preserved_provenance` `:1500-1556`). State adoption
uses bounded temp+replace from known bytes with pre/post
`validate_agent_state` (`:348-350`) — never `write_json` truncation, never a
pending-basis bypass.

## 5. Truthful reason and three-identity binding; minimal adoption change

New correction record (recommended over reusing the existing revalidation
record — comparison in §8) carries: `reason_class` = a NEW literal (e.g.
`REVIEWED_EDITORIAL_CORRECTION`), a non-empty human-authored `reason`
naming `proposal_id`, before/after reader (path+sha), `preserved_upstream_digest`,
scope decision + reviewer identity, and refs to the `REVIEW_BOUND_PROPOSAL`
proposal and the fresh Gate/QA records. Reusing `REVIEWED_CORE_CHANGE` for
editorial bytes is rejected: the literal asserts a reviewed Core delta the
evidence does not contain. An enum-only addition without the binding fields
is likewise rejected — the fields ARE the truthfulness mechanism.

Identity binding: original checkpoint = State-pinned validation record
(`proposal_v2.py:355-377`); active-before = State-bound effective rows
(`:380-411`); new-after = installed canonical live bytes with byte equality
to the proposal's `proposed_reader_canonical_sha256` (`:1789-1801` pattern
for staged-vs-derived comparison, applied at install). Epoch/control
invariants: VALIDATED_DRAFT + approved Architecture + pending Preview without
provenance + pending downstream + inactive exception (P1 eligibility
`:327-342` mirrors controller guards at `agent_control_v2.py:1799-1812`);
receipt contract equality (`proposal_v2.py:1400-1403`, receipt validator
`longform_generated_v2.py:681-684`); HEAD/implementation pinning per the
pending-basis pattern (`:1838-1840`, `:1977-1980`). Minimum coherent
controller change: one new `promote_editorial_correction(...)` entry (or
narrow extension of `revalidate_publication_surface`) + one new reason
literal in the closed set (`:45`) + schema requiring correction bindings when
that reason is used; all existing revalidation QA callsites
(`:1898-1944`) are invoked unchanged against the new bytes. No exception
lifecycle, no pending bypass (`validate_agent_state` public strictness,
`:348-350`), no manufactured State.

## 6. Candidate, Human Preview, and independent review responsibilities

Existing approvals stay valid exactly where their bytes are unchanged:
Architecture approval via provenance (`agent_control_v2.py:1814-1822`),
upstream checkpoint bytes via `_verify_preserved_provenance` (`:1500-1556`),
and ordinary pre-TeX compatibility (P1 requires no re-review of ordinary
records; correction readiness additionally requires the scope block).
Invalid for new bytes until re-executed: semantic review, visual review,
Gate, quality bundle, receipt, and any Preview/Freeze/Release downstream of
them. The correction MUST rebuild the Candidate from corrected bytes and
obtain a FRESH Human Preview: `approve_publication_preview` (`:1465-1497`)
requires `RELEASE_CANDIDATE` + pending Preview (`:1475`) and validates the
canonical Candidate (`:1480-1483`) — a stale or reused Preview approval is
refused by construction (P1 eligibility already forbids Preview
decision/provenance at `proposal_v2.py:333-334`). The assessor remains the
existing independent ChatGPT semantic/editorial reviewer; material new
editorial/Architecture choices route to existing Owner/exception/upstream
authority (`REQUIRES_OWNER_DECISION`/`REJECT` scope decisions refuse binding
at `proposal_v2.py:1673-1675`). No new normal Human Gate or role is created;
`reviewed_by` text alone remains non-proof (contract decision §2.6).

## 7. Routes: Longform-primary, Weekly-envelope subset

- **Longform (primary feasible route).** P1 derives the proposal through the
  readback loader `load_derivation_for_readback`
  (`longform_derivation_v2.py:1142-1182`), which permits healthy later states
  while retaining accepted/Profile/Architecture/Draft attribution and the
  legacy-directive refusal. Promotion installs the authored prose delta and
  replays the same loader plus receipt/Gate/QA over live bytes. Authored-prose
  corrections are expressible here because the route's publication-authored
  input carries real prose within accepted-source constraints.
- **Weekly (supported subset, explicitly bounded).** The authored input is an
  envelope only — `cover/frontmatter/final_summary` with fixed shape
  (`weekly_derivation_v2.py:146-179`); body/headline/deck derive from accepted
  Draft and closing synthesis from accepted Synthesis (contract decision
  §2.5). Any Weekly correction touching body text via authoring metadata is
  refused (must route to upstream/Draft authority, out of scope). Weekly
  promotion otherwise mirrors Longform with `weekly.load_derivation`
  (`:475-570`) + Weekly receipt validator (`:726`).
- No split-brain: one proposal, one route (`proposal_v2.py:345-352`
  allowlist); mixed Core+editorial changes stop (contract decision §1).

## 8. Correction record vs reuse of the existing revalidation record

| Option | Cost | Risk if chosen |
|---|---|---|
| **A. New correction-supersession record type (recommended).** New schema + writer + State pointer (e.g. `correction_supersession_provenance`) alongside the existing revalidation chain. | 1A module (or narrow controller extension), 1A schema, 1M State schema, 1M controller reason/dispatch; existing receipt/Gate/review/QA validators reused unmodified. | Small schema surface; old `REVIEWED_CORE_CHANGE` semantics untouched; chain readers must follow two pointer kinds (bounded, explicit). |
| B. Reuse existing revalidation record with new reason literal + mandatory correction bindings. | 1M revalidation schema, 1M controller, 1M State schema (no new record path logic). | Revalidation history mixes Core-change and editorial semantics; every consumer must branch on reason; higher misreading risk. Acceptable fallback if a second pointer kind is deemed too costly. |
| C. Reuse existing record with `REVIEWED_CORE_CHANGE` (rejected). | Cheapest. | False core-change attribution; solicitar reason text cannot cure the literal. Rejected. |
| D. Whole-writer doing retention+admission+adoption in one component (rejected). | One large increment. | Unreviewable blast radius; failure attribution unclear; contradicts lifecycle-work minimization (large unprovable step). Rejected. |

Stage constraints preserved in all options: healthy VALIDATED_DRAFT
throughout preparation/review; later multi-file promotion may temporarily
fail closed rather than stay continuously valid (contract decision §6);
normal new Candidate→Preview→Freeze→Release chain after adoption.

## 9. Minimal concrete API/path budget (recommended option A)

- **A** promotion writer: `promote_editorial_correction(root, state_path,
  proposal_path, scope_review_path, reason, executor)` — preflight (P2a
  retention), install + fresh chain (P2b), record + State adopt (P2c); returns
  the supersession record path/ref; never a PASS/Gate/review producer.
- **A** schema: correction-supersession record (reason_class, reason,
  proposal/basis/before/after refs, scope-review ref, Gate/QA refs,
  retained-manifest ref, prior-checkpoint + superseded/preserved rows,
  establishment block mirroring `:1984-1993`).
- **M** `schemas/publication-surface-revalidation.schema.json`: none (left
  untouched under option A).
- **M** `scripts/survey_agent_control_v2.py`: State pointer field +
  resolution/validation in `validate_agent_state`/`resolve_active_*`;
  writer dispatch only.
- **M** `schemas/survey-production-state.schema.json`: one optional
  `correction_supersession_provenance` pointer (exact {path,sha256}).
- Reused unchanged: receipt validators, Gate evaluate/validate, quality
  bundle, manuscript/review validators, `approve_publication_preview`,
  Candidate builders.
- Owned paths: `<proposal_dir>/retained/before/**` (new), canonical live
  reader input + authored installation target (modified), new receipt/Gate/
  review/QA records (new), supersession record (new), State file (modified).
  No other live/State/config paths are writable by this writer.

## 10. Real-fixture stop conditions and oracle plan (no execution)

Real fixtures required (synthetic PASS never counts as review): a healthy
generated Longform `VALIDATED_DRAFT` edition with a meaningful
publication-authored prose correction (before≠after canonical bytes,
`proposal_v2.py:1388-1389`), and a Weekly envelope-only correction (cover/
frontmatter/summary within `:146-179`, body-immutable negatives). Behavior
oracles, all refusal-based except the positive chain: same-byte input
refuses (`NO_EDITORIAL_CHANGE`); frozen-field/authored-drift refuses
(`_proposed_upstream_check`, `:1390-1391`); stale State/accepted/code epoch
refuses; absent scope block yields `REVIEW_REQUIRED` not adoption
(`:1668-1670`); wrong-before/wrong-after/stale-upstream/REJECT or
non-WITHIN scope refuses (`:1673-1694`); uncanonical staged reader refuses
(`:1800-1801`); alias/traversal/overlap/collision refuses (`:1235-1284`);
sequence collision refuses (`agent_control_v2.py:1955-1957`); post-adoption
`validate_agent_state` must be clean and the new record byte-verified after
exclusive create (`:2036-2046`). Positive oracle: one end-to-end corrected
edition reaching a fresh Candidate + pending Preview with all fresh QA PASS,
bindable to exact path/sha pins — genuine Human Preview/Freeze/Release and
rendered-PDF acceptance remain OUTSIDE the oracle (operator/Human-owned).

## 11. Cost/benefit and remaining underdetermination

Lifecycle-work reading: P1 already paid for machine-checkable proposal/closure
semantics; P2a–P2c each convert one unverified trust assumption (retention
actually happened; new bytes actually replay; adoption actually points at
verified bytes) into checked evidence, reusing all existing validators — no
new oracle machinery except the writer and one record schema. Whole-writer
(D) gambles all three assumptions in one increment; its apparent cheapness is
unknown-cost-zero fallacy plus reviewer overload. Sequencing P2a first bounds
loss: if P2b/P2c stall, the retention writer still serves any future
correction or rollback need.

Underdetermined (must NOT be assumed by the design; each is a future blocker
or explicit non-goal): rendered-PDF/visual acceptance bar for corrected
output; Candidate rebuild mechanics for the correction route (which stage
handler re-runs publishers and under whose authority); Freeze/Release
eligibility of correction-adopted States; concurrent-correction serialization
across proposals; retention media durability beyond exclusive-create/readback
(fsync/replica policy is operator scope); executor identity/provenance
standard for the truthful reason string; Preview evidence standard for
editorial deltas (same bar as normal Preview — no editorial fast lane).
If any of these blocks P2b/P2c, the useful selected next component is P2a,
not an assumed full promotion.

## 12. Recommendation and material blockers

Recommend Astra select option A (§8) as the promotion/adoption contract with
the P2a→P2b→P2c sequence (§2) under the §9 budget, Longform-primary with
Weekly-envelope subset (§7), fresh Candidate/Preview with existing review
roles (§6), and the §10 oracle plan as acceptance. Material blockers to
implementation start: (i) this design's own author-independent review (task
requires a separate General review; no code until resolved); (ii) reason
literal + record-type choice (A vs fallback B) as an explicit Astra contract
decision; (iii) a real accepted Longform fixture path committed to by the
affected edition owner (synthetic fixtures prove types only). No new role/
Gate, no same-SHA retargeting, no false core-change, no migration/exception
or pending bypass is authorized by this analysis. Full promotion remains
NOT_READY; DM021 stays OPEN.
