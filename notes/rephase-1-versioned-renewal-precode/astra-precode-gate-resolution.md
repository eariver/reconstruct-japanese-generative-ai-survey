# Astra pre-code gate resolution — mandatory binding correction

2026-10-24. Author-side review of the pre-code returns after Human commit `ce0de1a`. Selected contract remains [478f0051, including §11](../../outputs/rephase-1-versioned-renewal-contract-decision.md). No implementation/source changes or runtime tests in this unit. **Final readiness review pending; code remains blocked until the final disposition below is confirmed.**

## 1. Precedence and rejected claims

R1/R2, integrated R3, and R4–R6 are preserved author submissions. Their `MAP-COMPLETE`, `MAP-CLOSED` and `GO-CONDITIONAL` labels are not acceptance. Independent review rejected the submitted maps repeatedly. Use R3 only with the explicit R4/R5/R6 deltas **and this resolution**, never a saved earlier plan by itself. Markdown/JSON twins are documentary maps, not runnable schemas or safe runners.

Root rejected and corrected: null predecessor/Candidate, fresh authoring in a same-reader renewal, audit-only tool-blob checks, invented C P3S manifest, serialized U proof changing old manuscript, reopening the fixed four-schema choice, incomplete digest field counts, scope/epoch omissions, incorrect closure arithmetic, original-P target fallback after C, global `(kind,name)` epoch uniqueness, array-order-insensitive digest claims, and failure of C→U→U reuse. The independent review's final R6 assessment is NOT READY as submitted. This document addresses its three remaining findings; it does not overwrite that assessment.

## 2. B.1 — strict LIVE State validation is retained, not replaced by Profile checks

R6 §1.1's ban on `agent.validate_agent_state` even for the LIVE entry, and its claim that `_profile_and_source` alone suffices, are **rejected**. Actual `survey_agent_control_v2._validate_agent_state:503–649` deliberately preserves initialization provenance while validating separately recorded stage contracts. It does **not** call `production.verify_state_basis`; these are different interfaces. The latter's current-contract-versus-initialization-contract equality (`survey_production_v2:980–981`) must not be imported into the renewal entry.

Binding entry procedure in `survey_versioned_renewal_v2`:

1. Read the canonical candidate State and config through strict, no-follow pinned bytes. Validate the State against `agent.STATE_SCHEMA` before indexing fields. Derive the sole canonical State path from its exact Profile ref and `cfg.state_authority.authoritative_filename`, using the same source-root rule as P1 `1575–1583`. Supplied history/copy/alias paths refuse; no basename inference. Load and check Profile through `agent._profile_and_source` (live immutable Profile binding; State/Profile initialization contracts remain equal).
2. Apply private pure `_require_renewal_entry_window(state)` in the new high module: exact predicates of P1 `_eligibility:414–429`: lifecycle `VALIDATED_DRAFT`; Architecture approved; Preview pending with no Preview Human provenance; publication_preview/freeze/release machine checkpoints all pending; Exception inactive. This function examines the just-pinned State, never synthesizes it. It is a named operation eligibility check, not a caller flag or replacement State validator.
3. Call **public** `agent.validate_agent_state(root,cfg,state)` with no pending argument, on those same LIVE bytes; any error refuses. Recheck pinned bytes after this call. Preserve every predicate in the table below. This call is allowed only in the high invocation/normal State consumers, **never** in history, accepted-authority content assembly, `validate_renewal_basis`, or `verify_renewal_source_proof`.
4. Require the State pointer to select a nonnull versioned record/set/Candidate, derive its prior history using the new typed structural branch, and bind current nonpublication checkpoint selection to the same graph used for source proof. Existing canonical-only entry refuses. Apply current committed-tool, control-root, mode/recipe/contract compatibility and epoch predicates; record old-vs-new proof separately. `_observe_renewal_entry` returns invocation-local pins only. Capture writes COPY/basis; `observe_renewal_authority` repeats these LIVE checks plus exact basis/COPY/predecessor equality at later write boundaries.

| Required LIVE predicate | Existing owner retained / explicit new check |
|---|---|
| Strict State schema, recognized lifecycle | agent `516–520`; high precheck uses the same schema |
| Exact Profile path/hash/labels/initial contract | agent `_profile_and_source:208–236`, invoked at `522`; Profile is never rebound |
| Canonical State input path | high explicit comparison equivalent to P1 `1575–1583` (public agent validator takes a dict, so cannot prove this path itself) |
| Renewal prePreview window and inactive Exception | new pure high `_require_renewal_entry_window`, exact P1 `414–429` predicates above |
| Legacy compatibility bytes | agent `526–535` |
| Expected completed checkpoint set, passed/pending/provenance discipline | agent `537–577` and `_validate_checkpoint_record:382–495` |
| Stage producer/schema/Profile/recorded-core/review/artifact identity | `_validate_checkpoint_record`, preserving historical `expected_contract` and implementation values **derived internally from that exact record**, not caller-supplied overrides |
| History lifecycle path, implementation SHA format, monotonic instants | agent `579–600` |
| Architecture Human provenance, canonical review/approval refs and actual approval validation | agent `602–631`, `drafting.validate_architecture_approval` |
| Preview lifecycle/provenance/Human-checkpoint equality | agent `538–570`, `633–638`; renewal entry window rejects already decided Preview first |
| Derived next_action/terminal_reason | agent `640–648`, `core.derive_control_fields` |
| Exact predecessor, chain/canonical anchor, research/checkpoint graph, retained COPY and current tools | new typed history/low structural branches and high binding checks; source proof independently reloads graph/content/current tool closure on every readback |

### Required low/agent wiring and recursion boundary

Before using this entry in the successor, the planned low/agent changes must recognize **both** explicit versioned kind/reason pairs through an internal `_is_versioned_record` discriminator (or equivalent exact two-branch dispatch), not by treating arbitrary reasons as editorial. Add renewal branches in `_resolve_publication_revalidation`, low `validate_activation_record`, chain/anchor projection and `_validate_checkpoint_record`'s versioned guard. Original canonical/legacy shapes stay unchanged. Versioned predecessor verification uses the finite historian's structural evidence/tool-epoch checks; no low→full current source-proof call is introduced.

That low projection proves selected identity/structure; it is **not current publication eligibility**. The high renewal entry may admit a historically intact predecessor whose old full current receipt correctly fails. Normal stage/Preview/Freeze/Release must still call the Candidate/Gate/current detached proof validators specified in R3–R6, and they refuse stale current tools. Do not change those current predicates to history checks merely to make `validate_agent_state` pass. Ordinary `validate-state` remains State validation, not a substitute for publication admission.

On the entry's exact prePreview window there is no decided Preview branch to re-enter Candidate from `agent:564`. At later lifecycle readback, agent may validate Preview→Candidate→Reader→source proof; that proof never calls agent/State validation, so the path terminates. This preserves current State validation and the acyclic source-proof boundary simultaneously. `production.verify_state_basis`, generic pending/context overrides and synthetic State remain forbidden on new renewal history/source/high entry paths. Existing stage machinery may use its existing stage override under its original conditions; this does not authorize a new renewal bypass.

## 3. B.2 — O17 is a whole-document schema check

R6 O17's `/editorial_correction_scope` is a **document field pointer**, not a schema pointer. For the historical SCHEMA binding use `schema_path=schemas/reader-surface-semantic-review-v2.schema.json` and `schema_pointer=""` (JSON Pointer empty string = whole schema root; URI fragment representation `#`). Validate the entire review object against that recognized schema at its staged producer epoch. If identifying the scope subschema for inventory purposes, the schema pointer is `/properties/editorial_correction_scope`, not `/editorial_correction_scope`; no second weaker subschema-only approval path is created.

Retain all original scope predicates (`survey_editorial_correction_proposal_v2._validate_scope:2125–2185`): exact captured bytes/self-digest and ordinary review-loader digest, same issue/Profile, exact after reader path/SHA, block version and `WITHIN_APPROVED_AUTHORITY`, exact proposal before-reader and preserved-upstream digest, nonempty change summary/evidence locations, required PASS scope check with substantive detail/evidence. Its old before-reader is historical proposal authority, not the new renewal's fresh before-State. Resolve the original scope through typed materialization/history lineage when the predecessor is renewal; renewal receipts do not gain a fake `scope_review_ref` or new P3S manifest. No fresh P2V PASS or Core-change approval is inferred.

## 4. B.3 — no Screening `Path(".")` repair

R6 §1.3's `Path(".") fix retained` is withdrawn. Actual `survey_screening_v2.expected_result_basis:595–603` does not use its root argument; `_validate_result_batch:670` passing `Path(".")` is not a defect in this task. R2's correction is binding. Preserve the existing result-basis fields, including original historical package State SHA; the content-addressed accepted-package evolution rule does not rewrite package or result bytes.

## 5. Gate and next boundary

The candidate implementation map is the integrated R3 material with R4/R5/R6 corrections **as further corrected by §§2–4 above**. Rejected drafts remain evidence, not alternate authority. Exact closure sets/fingerprints and finite typed snapshot enumeration are design artifacts to be checked against the actual implementation as it is written; no test PASS, execution equivalence, build success, genuine review or runtime safety is inferred now.

Final independent review must confirm the live-State predicate table and the historic/current separation above. Until then no code. If accepted, close this substantial pre-code readiness work unit at Human Commit Point and make the next unit the complete selected implementation: bootstrap + both U/C routes, repeat (including C→U→U), renewal→editorial, normal direct Preview/Freeze/Release, exact failure/resume and meaningful affected regressions. No detached helper-only completion. Ordinary Commit/Push remains Human-owned; whole NOT_READY/DM021+022/quality/Profile/audit/adoption/savings remain open.

## 6. Final disposition and schema-pointer erratum

The independent review's **Final-binding ROOT resolution review** confirmed **PRE_CODE_READY (design map only)** against this document's original §§1–5, snapshot SHA256 `a8053b2d367b7ed7508c82cca2b52e273519f5f68c989581c44da9a5e0d2076a`. Those sections are preserved verbatim above; their earlier pending wording describes that review request, superseded by this closeout.

One binding shape erratum implements that review's B.2 note: `observedSourceBinding.schema_pointer` is a **string allowing the empty string**; remove the old `minLength:1` requirement. The typed registry still requires exact pointer equality. Whole-document schema validation uses `""` only. **Do not substitute `"/"`**: in standard JSON Pointer it selects a property with the empty name, not the document root. `/properties/editorial_correction_scope` is a schema-node inventory pointer, never an alternative to whole-document scope-review validation. This corrects both the R5 minimum-length constraint and the review's suggested slash shorthand; it adds no authority or schema family.

With that erratum, Astra confirms the bounded pre-code map. No executable source, fixture, test, build or adoption acceptance follows. The next implementation unit must apply the full typed map and verify its actual imports/closures/predicates/oracles; any mismatch is a correction/contract-return condition, not permission to weaken checks. **Human Commit Point now.** After Human continuation delegate the complete selected implementation to General, keeping ordinary candidate/reconstruct Commit/Push Human-owned.
