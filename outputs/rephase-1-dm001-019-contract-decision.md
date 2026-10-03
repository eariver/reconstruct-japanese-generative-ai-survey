# Re:Phase — updated intake and DM-001/019 contract decision

2026-10-03. Astra architecture/evidence review. Started at Human reconstruct commit `a6d834be7da6828740bcddd9b63477064015de80`, clean. **This unit completes one-document intake and a packet-bound Freeze contract decision. No runtime implementation, test execution or DB recovery.** Whole candidate **NOT_READY**, step 4/B3 OPEN, canonical seven-point audit unstarted.

## 1. New intake, fixed baseline

Production baseline remains **`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**. General resolved `main` metadata once, then fetched only the authorized Summary at that fixed SHA once:

- Capture commit: **`d6381568cc897a47d6de992189e20339350342b7`**.
- Document: `docs/core-v2-deferred-maintenance-summary.md`, r0.7, through W39; its own last-reviewed main is `239ef2703a93fa802f232978c7166d04d6cc3d49`.
- Blob: `ad86f1f2754366a0b30200c6b229121ba9290095`; SHA256: `a30ee17c309d96e0b59a4991a9a9d4a6cfc4d1407ad625589e932633c02bcb95`; 55,021 bytes; fetch recorded `2026-10-03T03:51:44Z`.
- [Exact capture/provenance](../notes/rephase-1-deferred-intake-20261003/README.md) and [all-20-item delta/mapping](../notes/rephase-1-deferred-intake-20261003/delta-analysis.md). Root independently checked capture blob/SHA256 and read the changed primary Summary sections. The earlier f85539c3 capture stays intact.

No linked primary defect, Issue/PR, edition artifact or terminology corpus was fetched. Recurrence, edition fixes, PDF quality and workflow success remain **Summary-reported secondary evidence**. Its maintenance-restart/update duties are not newly adopted Re:Phase duties.

### Dispositions adopted by Astra

| Items | Relation to existing work and acceptance |
|---|---|
| DM-001 + new DM-019 | Joint Freeze-interface prerequisite. Correct VISUAL authority and public identity must agree across both builders; a wrapper-only workaround is insufficient for joint closure. |
| DM-002 / DM-003 / DM-004 | Retain f1's bounded B2 overlap; broader checkpoint completeness remains separate; Release command/closure remains a separate prerequisite. Recurrence does not invalidate f1 or prove those other gaps repaired. |
| DM-005 / DM-010 / DM-011 / DM-012 / DM-015 | Keep existing reader/support/semantics/layout acceptance dispositions. B's complete input and derivation are partial coverage, not editorial or all-profile closure. |
| Expanded DM-006 | Preserve technical concept/entity/benchmark meaning and independent semantic judgment. Seed-zero is not acceptance. Referenced corpora have not been read/adopted; no automatic rewrite, new language engine or extra review role is selected. |
| Expanded DM-013 | Preserve distinct source/version/event dates and check same-event statements across reader/bibliography/notes. No source-date rewrite or collector repair is selected. |
| DM-007 / DM-008 / DM-009 | Research-intake responsibility and current role/clock discipline remain; generic intake/identity/chronology repairs remain separate. |
| DM-014 | W39 recurrence supports r2's removal of copied live status obligations. It is evidence for that decision, not proof of savings or authority to refresh historical indexes. |
| New DM-016 | Upstream Thematic source-class admission gap. Separate cross-profile Discovery/Screening/Evidence contract, **not** the same defect as reader supporting-TeX coverage. Must have a supported/deferred disposition before whole-Special claims. |
| New DM-017 | Separate post-initialization obligation/completeness producer-validator contract. Do not import edition-authored structural rows as a generic solution. |
| New DM-018 | Exact VISUAL binding does not prove rendered quality. Gross clipping/build-log→page review is a publication acceptance gap; edition-specific numeric thresholds are not adopted automatically. |
| New DM-020 | Citation resolution/derivation is not claim-to-source semantic fidelity. Existing semantic/editorial responsibility must preserve subject, novelty, strength, conditions, attribution and source roles; later acceptance must show substantive evidence. No automatic semantic PASS or new review authority selected. |

No item is declared upstream `CORE_FIXED`. All 20 have a disposition; they are not 20 implementation tasks. Claims in the Worker's mapping such as “proves recurrence” mean reported recurrence only, and proposed future corpora/guards are inputs to decisions, not imported requirements or completed work.

## 2. Missing DB and selected boundary

The expected `/tmp/jgas-rephase-r1-assembly-20260929T143833Z` and other documented `/tmp` candidates are absent in this environment. Old `481dec0` assembly evidence remains valid **for its recorded historical scope**; live HEAD/tree/history cannot now be reverified. No candidate was silently replaced.

Explore inventoried durable patches/copies and known local roots. [Recovery inventory](../notes/rephase-1-dm001-contract/recovery-inventory.md) records availability and limits. General then compared fixed-content sources using baseline-listing blob bindings plus the preserved patch chain; [source manifest](../notes/rephase-1-dm001-contract/fixed-content/SOURCE-BINDING.md). Root checked both Freeze-script blob hashes and read their actual code. This is static source evidence, not a fresh exact-head execution result.

**Chosen completed unit:** latest Summary intake + fixed-content DM-001/019 contract/oracles + recovery prerequisites + scoped independent documentary review. **Next executable unit:** isolated candidate recovery and source/runtime verification, ending at another Commit Point **before Freeze implementation**. This is justified by the missing DB and Git-aware authority needs; redoing the old R1/assembly tests for appearance would not restore ancestry.

## 3. Source findings and rejected recommendations

General's initial [blocked report](../notes/rephase-1-dm001-contract/report.md), [static analysis](../notes/rephase-1-dm001-contract/static-contract-analysis.md) and subsequent [corrections](../notes/rephase-1-dm001-contract/static-contract-corrections.md) are preserved separately. **The corrections and this decision supersede the initial recommendations.**

1. Profiled helper uses the legacy post-approval `visual-review-v2.json` and `validate_visual_review` (profiled lines 79/87). Canonical `build_freeze` uses Candidate-bound pre-preview VISUAL (publication lines 341–346). Stage uses that same Candidate-bound record. This is the DM-001 mismatch.
2. The wrapper does **not successfully accept** a legacy record divergent from Candidate authority: its final manifest validation (profiled 135 → publication 408–409) rejects it **after Freeze and Manifest writes** (118/134). The original “accepts legacy”/“no-write already correct” conclusions were overbroad. `_write_immutable` prevents a divergent overwrite of one file; it is not a multi-file transaction.
3. Canonical `build_freeze` uses internal issue ID for tag (publication 371), while wrapper and release workflow derive slug from the Profile. Deliberately preserving canonical workflow failure on divergent slugs would leave DM-019 open. Astra rejects that as the desired repaired behavior.
4. Both builders validate the supplied Candidate and the approval's own Candidate, but only compare their PDF hashes to each other. They do not directly require the **same Candidate path/hash**. The saved B stage's typed-approval extraction and exact Freeze pins reject a mixed pair at stage admission; that external protection is not sufficient for a builder claiming to freeze the exact approved Candidate. Astra rejects a post-repair “both PASS mixed Candidate” oracle.
5. Profiled State/lifecycle/Preview provenance/current Profile and bundle→Profile checks must stay. Existing profiled tests cover slug functions, workflow text and quality binding; they never invoke `build_profiled_freeze`. Their green status cannot establish builder equivalence. No test was executed now.

## 4. Selected future joint contract (design, not implemented)

The next Freeze implementation, after recovery, should address **DM-001 + DM-019 and their immediate authority/write boundary** in one bounded change:

- **One visual authority:** consume only the supplied, validated Candidate's exact pre-preview VISUAL path/hash via the canonical reader validator. No required legacy post-approval record or silent fallback. Preserve existing pre-preview order and Human Preview authority.
- **Exact approved Candidate:** require approval Candidate path/hash to equal the actual Candidate being frozen, in addition to existing issue/Profile/source/PDF/page checks. Same PDF bytes do not authorize another Candidate.
- **One public identity:** both builders derive release identity from the same validated, Candidate-bound Production Profile public slug. The wrapper additionally requires that authority equal the State's current Profile. No arbitrary caller-supplied tag/slug override. Keep existing Weekly and Special names; direct canonical and wrapper must agree for convergent and divergent slugs. Choose a small shared placement in the existing modules without circular imports or a generic resolver after recovery callsite verification.
- **Preserve wrapper guards:** actual State validation, RELEASE_CANDIDATE, approved typed Preview provenance, exact current Profile and bundle identity remain prerequisites. Do not drop guards to force equivalence or manufacture authority to satisfy tests.
- **Predictable failures before writes:** validate the complete pair, exact authority/identity and both target conflicts before installing either output. Malformed/stale/wrong authority, invalid slug and known divergent existing target must leave State and both targets unchanged. Same-payload retry remains idempotent. Installation-time I/O failure/partial-state handling must be explicitly specified and tested at the actual writer boundary; no claim of global CAS/crash atomicity. No overwriting/deleting pre-existing authority as automatic recovery.

Initial runtime scope: `scripts/survey_profiled_freeze_v2.py` and `scripts/survey_publication_v2.py`, with dedicated builder-equivalence/negative tests and affected existing tests. A small shared function in these modules is preferred over a new framework. Current workflow/schema/stage are comparison consumers; edit them only for a demonstrated necessary forwarding contract and return that path expansion to Astra first. This is a provisional path budget, **not permission to code before recovery and writer-preflight design review**.

### Required future evidence

| Boundary | Positive | Negative / oracle |
|---|---|---|
| Visual authority | Valid Candidate-bound VISUAL with no legacy file; both builders | Wrong kind, stale/missing Candidate VISUAL, legacy-only cannot substitute; preserve original parent failure including late residuals |
| Exact approval | Same Candidate/typed approval | Two individually valid Candidates with same issue and identical PDF but distinct Candidate identity; wrong-issue/stale approval; both builders reject before writes |
| Profile/public identity | Weekly convergent, Thematic Special convergent and divergent; Retrospective divergent identity coverage labelled by actual fixture reach | Wrong bound Profile/State/bundle, missing/unsupported slug; canonical parent divergent tag failure becomes a **pre-repair witness**, not a desired final outcome |
| Equivalence | Same inputs and `frozen_at`; exact Freeze and Manifest values/serialized bytes under identical output refs | If separate output paths are required, compare exact authority plus only the explicitly declared `freeze_record_path` rebinding; no normalization of identity, hashes or review refs |
| Consumers | Real manifest validator, actual isolated RELEASE_CANDIDATE→FROZEN admission for supported fixture, exact release-workflow identity predicate | Do not substitute a string grep or duplicated expected-tag assertion for the workflow-consumer contract; no live Actions/Release |
| Writer boundary | First write, same-payload retry | Pre-existing conflicting Freeze/Manifest, every predictable validation failure, relevant injected install failure; before/after output and State evidence, no generic exception-only oracle |

Use real validators and Git fixtures where required, no authority-success mocks. Synthetic reviews/Human records/PDFs prove type and identity, not semantic/visual quality or real Human approval. If DM-003 or another upstream contract blocks a valid fixture, return that concrete boundary before broadening; no filesystem scanning or unrelated backlog repair. DM-004, build transfer, Special supporting semantics, optional findings transport and whole-application audit remain separate.

## 5. Next task after Human continuation

Assign **General** the recovery/source-equivalence prerequisite from the recovery inventory, with **Explore** only for bounded read-only lookup if needed. Existing authorization permits independent fixed-baseline Git recovery; no rebaseline or general main tracking. Prefer a real available old DB; otherwise explicitly record a reconstructed new identity based on fixed baseline + saved patches, missing history limits and fresh affected verification needs. Do not forge 481/e4 ancestry or transfer old PASS. No new Freeze code in that recovery unit. Require durable recovery material with a stated/verifiable restoration scope, not merely another temporary path.

Astra reviews identity/source/evidence and scope; a fresh author-independent reviewer handles the recovery/implementation boundary as appropriate. Ordinary reconstruct Commit/Pull/Push stays Human-owned. **Stop at this unit's Commit Point now.** The completed [independent review](../notes/rephase-1-dm001-contract/independent-static-review.md) returned **BOUNDED_PASS for documentary intake + static contract only**, no blocker. It locally checked captured API base64/bytes/hash, the nine source blobs and relevant current B stage pins. Root read the report and requested corrections to its unchanged-item count (eight), both-builder invariant (already selected, only implementation placement deferred), and existing-test description; reviewer clarified its own report. This does not approve unimplemented code, absent DBs or the canonical seven-point audit.

Closeout checks: root `git diff --check` after entry synchronization exited 0; readback confirmed current AGENTS/handoff, corrected independent review and next-task ordering. `git check-attr text` reports `unset` for the new capture and fixed-content sample, preserving bytes through the new `-text` rules. This is documentary verification, not runtime testing; ordinary `git diff` does not include untracked packets, whose source hashes/capture were separately reviewed above. Two root entry-update patch attempts failed context matching before a successful corrected patch; no candidate/evidence bytes were changed by those failed attempts. Saved files and Human Git commit remain distinct; all current work is uncommitted at this Commit Point.
