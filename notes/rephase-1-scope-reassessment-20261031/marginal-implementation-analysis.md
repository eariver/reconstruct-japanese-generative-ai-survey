# Scope reassessment — marginal investment vs total editorial lifecycle work

2026-10-31, Astra docs-only. No implementation authorization. No commit readback,
no git status/HEAD, no network/restore/runtime/tests/build/fixtures/source edits.
Read-only inputs: `brief/00-mission-and-success-criteria.md`,
`outputs/rephase-1-direction-assessment.md` §§6–7,
`outputs/rephase-1-completion-roadmap-20261019.md` R3/R4/R5/R6,
`outputs/rephase-1-profile-support-contract-decision.md` FULL 62b14add…/20472B,
`notes/rephase-1-profile-support-contract/astra-review-resolution.md` FULL 021a0d7c…/7225B,
`outputs/rephase-1-profile-support-precode-assessment.md` +
`notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md`
FULL bfb72bf2…/20159B incl. §7, independent R5/§8,
`outputs/rephase-1-dm022-prearchitecture-implementation-assessment.md` (final133).

## 0. Readiness is not ROI; past spend is sunk

PRE_CODE_READY (precode assessment §1; ROOT §7) certifies a bounded
interface/design map only. It does not certify runtime correctness, all-Profile
acceptance, audit passage, or net work reduction. Direction §6 warns:
do not treat the next defect found as sufficient reason for the next investment.
Roadmap R3→R6 requires measured edition-level savings net of migration/dual-maintenance.
Prior contracts/precode rounds (R2 NOT_READY, R3 NOT_READY, R4→R5 hardening,
mistyped pins/optional-PATH/LIVE-vs-pure errors preserved as history) are sunk cost.
The question is marginal: what does the *next* implementation unit remove per use,
and what does it add in build/maintenance/review/audit/migration plus uncertainty?

## 1. Partition of the currently planned Profile/support code

| Partition | Content (per contract + ROOT §7) | Character |
|---|---|---|
| P1 necessary-canonical | DM016: 10 additive rows in `survey_evidence_v2` canonical mapper, old rows/labels KEEP; no v1-enum/URL/SOCIAL/default-SECONDARY expansion | Fixes present admission block |
| P2 necessary-ordinary | DM017: ordinary input initial-3 / named-only-5 → derived-7, U=initial+root+effective, every (parent,OID) via actual `parent_refs`, DECLARATION_LOSS refusal; direct/agent-first parity via same normal builder, closure-first residual union | Fixes present obligation loss/coercion |
| P3 new-admission hardening | Screening prepackage root/effective context before any package exists; ENOENT-only absence; claimed-root never DIRECT fallback; keyword-only PATH discipline; historical vs new-operation separation | Safety needed *because* P1/P2 open a previously refused route |
| P4 interface expansion | DM022 full true-R/E kernel: HIGH before first State COPY + adopt re-verify; LOW from pinned COPY through DCP/SCP + reloaded acceptances/JSONL; 4 LOW builders gain required keyword-only PATHs; private adopted-full keeps 3 args; no E-as-R/None fallback; G76 memberships as mapped | Generalizes historical/proposed-graph handling to all LOW/HIGH sites |

P1+P2+parity are the actual upstream repair. P3 is entailed safety if P1/P2 ship:
once unknown types become admittable and named obligations become creatable,
early refusal and loss checks must run before writes. P4 is the largest block:
it threads true R/E through every prior `None,None`/E-as-R content call and hardens
all LOW/HIGH boundaries. Precode map treats P1–P4 as one whole (assessment §5 /
ROOT §7.2). This analysis asks whether that bundling is marginal-optimal.

## 2. Known-present defect vs forward generalization vs advertised-route safety

- Known-present: v2 Discovery `source_type` open vocabulary vs canonical
  `SOURCE_CLASS_MAP` closed set blocks 67/160 TS-001 tasks across 10 types
  (intake §2); ordinary builder loops only Profile-initial IDs so named-only
  obligations (O13–O15 pattern) cannot enter without hand-append/loss.
  Both are observed on final133 source reads, not inferred futures.
- Advertised-route safety: existing normal + DM022-HIGH routes advertise
  acceptance of new discovery. Without P3, P1/P2 would widen admittable inputs
  while leaving late/coerced validation. This safety is not optional scope creep
  if P1/P2 ship; it is the fail-close condition from brief §mission.
- Forward generalization: P4's exhaustive LOW/HIGH propagation, adopted-full
  retention-COPY derivation, DCP/SCP/ECP disambiguation, FILE-SHA vs result-set
  digest separation, and G76 closure proof cover real historical/proposed graphs
  but also future DERIVED modes with no measured frequency. Distinguish: repairing
  the actual DIRECT path + actually observed DERIVED reissue shape is necessary;
  hardening every conceivable DERIVED/resume/readback combination is generalization
  whose payoff must not be assumed.

## 3. Actual usage ground (not future-Derived assumed)

Four-doc capture `notes/rephase-1-profile-support-contract/intake-20261030T124140Z/`:
defect lists 67 blocked / 93 passthrough; validation-report confirms identical
per-type counts; compat `run_frozen_evidence_chain.py` is DATA-only workaround,
never CORE_FIXED (intake §§4–5). DM017 ground is 3 edition-authored rows O13–O15
(status LIMITATION, Profile-declared dimensions) on 160 records; declaring-ID/
dimension-membership proof absent in scope. That is: measured need = DIRECT
admission of 10 known types + ordinary 3/5 handling of few named rows + parity
so agent-first does not diverge. No captured evidence in scope measures frequency
of multi-parent shared-OID loss, LOW historical DERIVED correction, or repeated
PREARCH resume at scale. Do not assert substantial per-edition savings from
unmeasured modes; brief §success-criteria permits explicit UNKNOWN.

## 4. Options

### (A) Whole precode repair then broader complete-reader before R4 (current plan)

Implements P1+P2+P3+P4 as one unit, then mandatory non-four-family/Retrospective
complete-reader + normal correction contract, then representative quality, then
R4 fixed candidate/audit. Preserves authority: no guard/root-proof weakening,
no alias/obligation drop, old history kept under own contract.
Cost: largest immediate build + cross-profile oracles (all-10-type, shared-OID,
DIRECT/DERIVED, old-history-valid vs new-refusal, guard/no-overwrite/idempotence,
DM022 repeat + downstream consumers per ROOT §7.2) + independent implementation
review + exact-candidate audit later. Benefit: single coherent upstream; no interim
explicit-unsupported mode; DM022 LOW/HIGH fully bound. Risk: pays full P4
generalization before knowing R4 audit/adoption cost or per-edition reuse rate;
repeats the process pattern of §§5–6: another large map → long test hours/log
packaging/reviews → false-closure risk if any site missed.

### (B) Bounded actual-upstream repair + explicit fail-closed limitation, then R4

Implements P1+P2 + entailed P3 + minimal P4 needed for actually used modes
(e.g. DIRECT + observed TS-001 DERIVED shape), with any excluded mode (e.g.
unobserved DERIVED variants) given an explicit contract delta: new unsupported
entry refused before writes + tests, historical bytes kept under old predicates.
See §5 for coherence test. Benefit: unblocks measured 67-type/3-row flow sooner,
defers unmeasured generalization until a trigger fires. Cost: requires a precise
delta document + refusal oracles + migration path if the mode later opens;
reviewers must verify the refusal is fail-closed, not a weakened guard.
Trigger to reopen: observed new-operation request in excluded mode, or R4 audit
finding that the limitation blocks a necessary Special/Retrospective route.

### (C) R4 final133 now with precise support envelope + manual workarounds

Freeze final133 (actual409/tree8ce +133 paths/768 files, patch 25b48878…/4931836B)
as the R4 candidate with a written envelope: supported = currently admittable
types + Profile-initial-only obligations + DIRECT_PRIMARY/PRIMARY_ONLY manual path
within its honest limits; named-only/unknown-type inputs explicitly refused
before writes. Keep edition-local manual structural completion as recorded
workaround (frozen validators, no canonical authority), as contract §5 already
classifies it. Benefit: smallest new-code cost; forces R4 audit/adoption learning
early. Cost: every TS-001-like edition pays manual projection + conservative
re-review; per-edition cost recurs; workaround maintenance + dual bookkeeping
accumulate; DM022 LOW/HIGH true-R/E debt remains. Coherent only if manual cost
is measured per scenario (roadmap §5 table) and shown below P1–P4 amortized cost,
which current evidence does not yet show.

### (D) Feature generalization on measured future trigger

No new generic renderer/source-class framework, cadence engine, or opaque IR now
(contract §5 explicitly non-selected). Revisit only when: (i) non-four-family
Thematic or bounded Retrospective volume is decided necessary with actual callers,
(ii) complete-reader representation is shown reusable across ≥2 routes, or
(iii) manual workaround cost per edition is measured HIGH. Until then, keep
foundations planning convention as-is; do not build for hypothetical topics.

## 5. Is (B) coherent without weakened authority? (source-grounded)

Smaller repair is coherent *iff* all of the following hold; otherwise fall back to (A):

1. Classification stays canonical: single `survey_evidence_v2` mapper +10 rows,
   old rows unchanged; unknown refused before Screening/Evidence writes (contract
   §§3,7; ROOT §§1–2). No default SECONDARY, no URL sniff, no alias relabel.
2. U and loss gate stay full-strength on the supported path: U=initial+root+
   effective, every (parent,OID) carrier check, DECLARATION_LOSS refusal before
   owned/package writes, exact 3/5 shapes, derived 7 unchanged (contract §4).
   A bounded scope may refuse an entire *mode* up front; it must never drop a
   parent/OID check *within* an admitted mode to make it pass.
3. Historical separation preserved: shared `validate_discovery_expansion`/detached
   validators unchanged; new policy only at new-operation gates (contract §4.1;
   precode ROOT §§2–4). Old accepted bytes never rewritten/gated retroactively.
4. Refusal is before-write and tested: excluded DERIVED variant refused at
   eligibility/preflight with recorded oracles, not discovered by late schema
   failure; guard/no-overwrite/idempotence unchanged; resume only completes an
   already-admitted bound intent (ROOT §§2,6–7).
5. Contract delta is explicit: the unsupported entry, its refusal predicate,
   affected callers/tests, and historical-kept behavior are written before code
   and reviewed; qualitative cost = one small delta + refusal oracles + future
   reopen vs full P4 kernel (all LOW/HIGH sites + retention-COPY + DCP/SCP/ECP +
   digest separation + G76 proof). If the delta itself needs new schema/module/
   family or rewrites history, (B) collapses into (A) — do not ship a weakened
   substitute.

## 6. Real process cost (no fabricated totals)

Do not invent wall-clock/token/test-count savings. Known cost drivers from this
lineage: repeated contract→precode→readiness cycles with false closures
(R2/R3 NOT_READY, R4→R5 hardening, §3 corrections); multi-hundred-second test
routes and qualified composites that cannot be summed into one full-suite claim
(DM022 assessment §§3–4: FinalB 2000s, control, 87/87, 24/24, depth, regressions,
PDF visual pages — each scoped, not additive); log/packaging/manifest/hash
discipline (20159B ROOT, 50891B review, 185422B manifest); independent
authority/operation/readiness reviews with FINAL-BINDING addenda. Any option
pays: implementation build + behavioral oracles + regression scope + independent
review + R4 exact-candidate seven-point audit + adoption/migration + dual-maintenance
while old path lives. (A) pays most now; (B) splits into small-now + contingent-later;
(C) pays least now but recurs per edition; (D) pays only on trigger.

## 7. Work removed vs work added per use

Per-use removal if P1/P2 ship: no per-edition type projection table; no hand-appended
named rows or repeated derived-ID entry; no adapter monkey-patch divergence.
Per-use addition: new preflight/eligibility checks (negligible machine cost,
small reasoning to interpret DECLARATION_LOSS/unknown-type refusals); residual-union
maintenance (one owner, not per-edition copies). Uncertainty: frequency of
editions needing named rows; share of sources falling in 10 new classes;
whether parity actually removes adapter debugging. Stop/reopen trigger: if after
bounded repair, representative-quality or R4 audit shows per-edition manual work
unchanged or new-check triage dominates, stop and reassess before broader reader;
if excluded-mode requests appear, reopen P4 slice only. Do not reflexively delete
existing DIRECT_PRIMARY/manual, compat, or G76 machinery: removal itself costs
review/migration/regression and may destroy the only path for a necessary Special.
Keep what is used; explicitly bound what is not.

## 8. Adoption scope vs whole finish line; proportionate testing

Roadmap R4 (fixed candidate + independent audit) is not whole finish line (R5
adoption/operation, R6 measured reduction + old-path retirement). (C) reaching R4
faster does not equal finishing. No option silently drops Special: non-four-family
Thematic and bounded Retrospective complete-reader/correction remain mandatory
gates (contract §§2,5; precode assessment §5); manual PRIMARY_ONLY is preserved
capability with honest limits, not a substitute. Testing guidance: require
genuine quality oracles (real v2 task/card acceptance per type, real many-to-many/
shared-OID, real DIRECT/DERIVED/history/guard boundaries, three research Profiles)
over duplicate full replays; do not sum scoped runs into a single PASS count;
retain independent implementation review and exact-candidate audit regardless of
option — they are not duplication to cut.

## 9. Precise root decision questions (no code)

1. Does Human accept (A) whole-kernel now, or (B) bounded P1+P2+P3+minimal-P4 with
   an explicit unsupported-mode refusal delta, or (C) R4-envelope now with measured
   manual cost — with (D) deferred until a stated trigger?
2. If (B): which DERIVED/LOW modes are in vs explicitly refused, with exact refusal
   predicates, caller/test lists, and historical-kept behavior — and does the delta
   satisfy §5.1–5.5 without new schema/module or history rewrite?
3. What per-scenario table (roadmap §5: new Weekly, needed Special, mechanical update,
   editorial correction, accepted-upstream correction, failure resume) will decide
   reopen/retire, and what UNKNOWNs must be measured in R4/R5 rather than asserted now?
4. What is the R4 audit/Migration/dual-maintenance budget under each option, and what
   stop condition returns scope to Astra before broadening (per ROOT §7: any new
   import/reader/authority gap returns before broadening)?
