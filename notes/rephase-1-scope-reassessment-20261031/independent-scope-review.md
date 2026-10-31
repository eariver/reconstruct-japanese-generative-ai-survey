# Independent scope/economic sequencing review — 2026-10-31

Fresh independent reviewer. Not author of marginal / reduced / R4-transition analyses, not author of contract / precode assessments, not Root.
Scope is the investment-sequencing decision ONLY. No technical pre-code re-audit, no candidate validation, no seven-point audit PASS, no adoption approval, no savings claim.

Human objective understood: minimize TOTAL editorial lifecycle work; re-evaluate excessive remaining scope BEFORE Profile repair, especially extra implementation and R4 onward.
Standing AGENTS pre-code technical instructions are preserved as technical safeguards; this review tests only whether the new decision's economic sequencing and scope boundaries are coherent.

Method: docs/source-read ONLY. No Git commands, no Human Commit readback (Human reported Commit/Push and said readback unnecessary), no network, no source edits, no import/runtime/tests/build/fixtures/restore, no Production actions. Document hashes below are data-only `sha256sum`; no candidate execution. No subagents.

## 1. Files and sections read

Bound decision and packet (hashes data-only, 2026-10-31 workcopy):

- `outputs/rephase-1-scope-reassessment-20261031.md` — FULL, §§1–7. SHA256 `1c88049aa803c5e6fa5f41d64d889f87b629f0e4afc40ccaed3e1ce02d54a83a` /17092B.
- `notes/rephase-1-scope-reassessment-20261031/README.md` — FULL, §§Current authority / Author analyses / Usage evidence / Closeout. SHA256 `6ed8a5f17f00568fabe8ee750574c376717d407247656ffc94404ff118e264a9` /4661B.
- `notes/rephase-1-scope-reassessment-20261031/marginal-implementation-analysis.md` — FULL §§0–9, as AUTHOR alternative, not authority. SHA256 `489f84e69d7f65afaf03848f80439dced390a0ec6775de01dffe3b1fcb01c352`.
- `notes/rephase-1-scope-reassessment-20261031/reduced-repair-feasibility.md` — FULL, as AUTHOR alternative. SHA256 `15a2f8a8adb1197682e3075ff66cdff7b290525538557527fc5ab33c6d3db1a3`.
- `notes/rephase-1-scope-reassessment-20261031/r4-transition-analysis.md` — FULL §§1–9, as AUTHOR alternative. SHA256 `4f17ddd1ca946e26f3fadb9294bba390916e89597f46194e48e12ab8bff6bc73`.
- `brief/00-mission-and-success-criteria.md` — FULL Mission/constraints/success criteria. SHA256 `8aa4297818ac494dbf369219cc03c13d146cc94a84059bebbd77dbafac0baaf4`.
- `outputs/rephase-1-direction-assessment.md` — §§6–7 in full (plus §§1,4–5 for context). Total-work objective, remove-vs-move distinction, adoption/retirement path.
- `outputs/rephase-1-completion-roadmap-20261019.md` — §§1,4–5 (R3/R4/R5/R6 entry/exit, cost/quality method). Confirms R4 freeze→fresh audit, R5 limited adoption, R6 measured removal distinction.
- Prior Profile gates as context only, no re-audit: `outputs/rephase-1-profile-support-contract-decision.md` FULL incl §7; `notes/rephase-1-profile-support-contract/astra-review-resolution.md` incl §5; `outputs/rephase-1-profile-support-precode-assessment.md` FULL; `notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md` incl §7; `notes/rephase-1-profile-support-precode/independent-readiness-review.md` FINAL R5 + §8 FINAL-BINDING ROOT confirmation; `notes/rephase-1-profile-support-precode/README.md`.
- Source spot-check read-only at `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate/scripts/survey_research_authority_v2.py:783-799` (`_verify_adopted_graph_full` binds root to request Discovery DIRECT session basis) and `:1172-1297` (`derive_before_context` COPY SHA/byte-count, triplet, live re-hash, JSONL/SHA/IDs, non-DROP allowlist, exact-cover, old-graph load; no R/E split). Supports reduced-analysis coupling description; not a runtime proof.

No obligation to enumerate hundreds of old documents; no full 133/768/inode recertification in this unit.

## 2. Verdict

**BOUNDED SCOPE-DECISION PASS, with two minor documentation hardenings in §7.**

The decision to (a) keep whole P1–P4 shared upstream repair as the last PLANNED feature unit on the existing PRE_CODE_READY map with no new pre-code cycle, (b) remove the unconditional generic non-four-family/Retrospective complete-reader/correction gate before R4 (conditional-only reopen, not automatic after R4), then (c) require concrete Weekly/needed-Special rehearsal → one frozen candidate → fresh independent seven-point audit → permissioned limited adoption → measured savings/old-work removal, is economically coherent under UNKNOWN ROI and does not silently discard genuine Special needs or weaken quality/provenance/Human boundaries, subject to the §7 wording fixes.

No claimed savings, no candidate validation, no audit PASS in this review.

## 3. Why whole repair remains justified without measured ROI

- PRE_CODE_READY is correctly treated as interface/design readiness only, not runtime success, adoption, or savings (decision §1 para 2). Sunk design/test cost is explicitly not a justification (decision §2, §2.2 final para). This rejects the two most common sunk-cost fallacies.
- P1/P2 gaps are actual observed admission blocks on final133 source, not hypothetical futures: open-vocabulary `source_type` vs closed canonical map (67/160 TS-001 type gap per secondary defect/report, actual Raw/publisher unacquired — decision does not overclaim), and ordinary builder looping only Profile-initial IDs so named-only obligations (O13–O15 pattern) cannot enter without hand-append/loss. P3 is entailed fail-close because widening admittable inputs without pre-write unknown-type/DECLARATION_LOSS refusal would weaken crisp invariants. This matches mission constraints.
- P4 inclusion rests on shared-gap + coupling, not on "cheaper" measurement. Decision explicitly states "whole cheaper is NOT measured" and retains whole due to actual shared gaps and source coupling, not sunk cost/PRE_CODE_READY. Spot-check confirms the cited DIRECT-root assumption and COPY-bound checks exist where described; reduced analysis argues proving DIRECT *is* the kernel (COPY-bound DCP/SCP + root proof retained even in DIRECT-only cut) so a DIRECT-only fork saves little and adds a maintained refusal branch. That analysis is qualitative coupling (`M≈M`), not a price — README correctly labels it as such. Under UNKNOWN frequency/graph/total cost, choosing whole to avoid (i) paying a full audit on known-incomplete admission then re-auditing, and (ii) maintaining an unsupported-mode fork through LOW/HIGH, is a defensible bounded investment with explicit stop rules (§3 final bullet: missing authority/dependency/contract contradiction returns to Astra with location/impact/minimal-repair/limit/defer options; single caller wiring is same unit, new capability/contract change is separate investment).
- Evidence-first alternative (freeze final133 now, measure manual cost) was considered and rejected on audit-waste grounds, not ignored. Marginal option C is preserved as history. Rejection is sound: final133 has known admission/authority gaps before implementation; a full seven-point audit now would be invalidated by the subsequent repair. Decision §2.3 correctly notes limited prior quality/cost investigation remains possible as R4 preparation (target clarification, existing-record tidying) without duplicating workaround rehearsal on an unrepaired base.
- Proportionate testing is specified without bureaucracy: no suite-count decoration, predicate→oracle→affected-consumer selection, independent implementation review retained, CURRENT proof and meaningful affected regressions not cut, failed/partial/raw limits preserved, synthetic approval never promoted (decision §3). Costs from existing worklogs only (wall-clock/LLM usage/re-read/handoff/build/repair loops), missing token/time not reconstructed, break-even/rate currently UNKNOWN (§5). No invented numeric budget demanded or supplied.

## 4. R4 envelope does not silently discard real needs

- Minimum two representatives (one Weekly + one real-need Special) are explicitly not a coverage ceiling and not an automatic whole-format certification; unrepresented necessary routes must be listed as limits with validation-need judgment; Thematic four-family success is not横展開 to non-four-family/Retrospective; no all-format/all-period duplicate production replay presumed (§4.1). This prevents silent narrowing in both directions (no silent exclusion, no silent certification).
- Manual/direct-primary is correctly bounded: legitimate only under real stage/correction conditions; PRIMARY_ONLY is not complete-reader/reuse proof; pre-acceptance manual edits, genuine Human REQUEST_CHANGES re-entry, or another legitimate operation/new edition with costs must be shown; normal post-VALIDATED change that cannot be done without exception/fake Gate is a blocker, not closed by "manual handles it" (§4.1). Fabricated REQUEST_CHANGES and PRIMARY_ONLY-as-proof are explicitly forbidden. Known normal-correction failures therefore cannot be waved through.
- Audit entry/exit/adoption/completion are distinct: preparation (support table + rehearsal disposition, no open quality/authority/operation blocker on selected scope) vs exit gate to start audit vs R4 exit (fresh author-independent seven-point audit on exact bytes, remediation closed, no old-component PASS sum, changes handled by impact + necessary re-check without count-chasing) vs R5 (audited-scope limited adoption, non-degradation/rollback verified, never re-approves old RELEASED, never marks unconfirmed Special adopted) vs R6 (actual old-work abolition with investment/migration/dual-maintenance included, else adjust/withdraw/replace) (§§4.3,5). This matches roadmap R4/R5/R6 and direction §7.3.
- Reopen conditions are specific enough without creating standing bureaucracy: (a) needed edition/operation cannot complete with quality/authority via current routes, or (b) recurring manual/repair dominates — then compare with target callers, removed work, real alternative conditions, added maintenance/audit cost, minimal verification; Astra selects, contract changes keep independent review + Human boundaries; deferred items (generic reader, cadence bridges, Foundations engine, generic IR/resolver, all deferred maintenance, telemetry, hydration/main-refresh) explicitly do not imply capability completion; material quality/provenance defects are handled without waiting for frequency (§6). Future R4 prep must operationalize (a)/(b) with the roadmap §5 per-scenario rows, but no numeric threshold should be invented now.
- Exact identity accommodates overlay and future counts: one exact source identity = real HEAD/tree + all uncommitted overlay full patch/manifest/modes (adoption commit Human-owned), runtime/asset/dependency closure, restore/diagnostics/mandatory CI checks with exclusions; future bytes never frozen as "133paths/768"; partialDB never presented as full-history backup (§4.3, §7). Current final133 patch/manifest hashes in §7 are present-source identity only, not a future promise.

## 5. Rejected assumptions (not accepted as evidence)

- Past root "mandatory" as independent proof of economic necessity; PRE_CODE_READY as ROI/runtime proof; sunk spend as justification.
- `M≈M`, "negligible machine cost", DIRECT-only savings, "actual demand is DIRECT-only", "TS-001 DERIVED shape proved" as measured claims — all UNKNOWN; decision correctly refuses them (§2.3).
- Generic gate "moves automatically after R4"; marginal §8 and R4-transition mandatory-reader-at-design-scope as authority; truncated hash strings as alternative identities.
- "Three released" as normal lifecycle (TS-003 is exceptional release, normal State VALIDATED_DRAFT — decision §2.1 + README usage §25 correctly bound this); per-type counts as recurring-cost or 67-task execution proof; actual Raw/publisher proof from secondary intake; compat `.py` as CORE_FIXED; synthetic fixtures as genuine approval.
- Manual PRIMARY_ONLY as complete-reader proof; fabricated Gate/old-State execution as correction; rehearsal success as Production adoption/permission; preparation/support-table as audit; old PASS transfer; future counts frozen at 133/768.

## 6. Qualifications found sufficient, except §7 wording

README qualifications are necessary and — with §7 additions — sufficient:

- Attribution: README §18 correctly preserves marginal + R4-transition "Astra" author lines as mistakes (General A/B returns, sessions cited) and strips their "selected"/mandatory-reader assumptions of decision authority. No independent session verification was possible in this docs-only unit; reliance is on Root's session record, noted as a limit.
- Usage/cost: README §§18,22–26 correctly bounds Historical pattern matrix (15 Retrospective editions reported, not fresh PDF/current-operability/frequency proof), Summary ledger (TS-003 exceptional, not normal COMPLETE), four-doc intake (67 blocked/93 passthrough as reported counts, no per-record Raw/publisher or execution package, `.py` DATA never executed), source snippets (shared root-binding support, not exploit/reproduction or all-path proof), and `M≈M`/negligible-cost/DIRECT-only inferences as unestablished.
- TS-003 exceptional release is handled in both decision (§2.1) and README (§25); the earlier broad "three released" inventory cannot be misread as normal-lifecycle claim if §7 fix is applied.

## 7. Required small corrections (docs-only, Root to revise before implementation)

1. **README §18 — name the R4-transition mandatory-reader language as superseded.** After the existing "existing-reader-mandatory assumptions do not decide" sentence, append: "`r4-transition-analysis.md` §3 Selected step 2 ('Close mandatory non-four-family/Retrospective reader/correction contract at design scope only'), §§6–8 'Unsupported until gated' / 'Needed … reader/correction contract' / Gate G2 wording, and `marginal-implementation-analysis.md` §8 mandatory-gate sentence are superseded author proposals. Decision §§1/6 conditional-only reopen rule controls; no automatic post-repair or post-R4 design gate exists. Whole completion is withheld only if a genuinely needed route is unsupported per decision §§4/6, not by any unsupported format." Purpose: prevent future misreading of the General-B file's "Author: Astra" line as a standing gate.
2. **README §11 or §18 — bind reduced-analysis final sentence to the rejected alternative.** After the existing "Declared feature loss … describes the rejected DIRECT-only alternative" sentence, append: "It does not describe the selected whole repair and does not authorize a DERIVED new-admission refusal fork." Prevents quoting that sentence as whole-repair scope.

No new analysis, no numeric budget, no universal feature completeness, no code, no pre-code remap required by these fixes.

## 8. Limits of this review

- Binds ONLY the scope/economic sequencing decision identified in §1. Does not re-audit the technical pre-code map (reliance on prior FINAL R5/§8 + FULL ROOT `bfb72bf2…` for interface correctness, subject to their own stated bounds), does not validate any candidate, does not PASS any seven-point audit, does not authorize adoption, migration, CI/Actions/Release, rebaseline, or additional intake.
- Source verification limited to the two cited ranges; no full 133/768/inode recertification; prior 55 Gitlinks/child dirt, partialDB/missing26309/bulk31466, runtime/TeX nonbundled, qualified-composite bounds, and evidence-loss qualifications inherited as stated.
- Session provenance for General A/B vs Astra attribution taken from README record; not independently re-verified (no Git/network/readback per Human boundary).
- "Genuinely needed Special" remains an operational determination to be made concrete in R4 preparation with explicit topic/period/Raw permission (decision §4.1); this review does not select topics, grant permissions, or invent demand fixtures.
- Future implementation remains blocked until Root revises per §7 and the next Human continuation starts the shared-repair unit; this unit stops at Human Commit Point with Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN / quality/adoption/savings OPEN unchanged.

(End — independent scope-decision review; BOUNDED SCOPE-DECISION PASS subject to §7 doc hardenings.)

## 9. FINAL-BINDING confirmation — updated decision INCLUDING §8

Read: updated `outputs/rephase-1-scope-reassessment-20261031.md` FULL §§1–8 and updated packet `README.md` FULL (hashes below, data-only). No full rereview, no technical re-audit, no document-check duplication, no other file edits, no Git/network/runtime/tests/source/fixtures/restore/Human Commit readback.

- §7 hardening 1 satisfied: README §20 now explicitly names `r4-transition-analysis.md` §3 Selected step 2, §§6–8 unsupported-until-gated / Gate G2 / needed-reader-contract wording, and marginal §8 mandatory-gate sentence as superseded author proposals. Decision §§1/6 conditional-only reopen controls; no automatic post-repair or post-R4 reader design gate.
- §7 hardening 2 satisfied: README §§18/20 bind the reduced final feature-loss sentence to the rejected DIRECT-only alternative only; no DERIVED new-admission refusal fork authorized for the selected whole repair.
- Root §8 evidence-first qualification is consistent with review §3: audit-now (decision §2.3 row 3, rejected as full-audit-before-repair waste) and limited quality/cost investigation (decision §2.3 row 4, permitted as R4 preparation: target clarification / existing-record tidying) are separate options. Decision picks whole repair as the next unit to avoid duplicating workaround-loaded rehearsal on the unrepaired base. No conflation introduced.
- No conditional reader gate becomes automatic: unsupported format alone does not withhold whole completion; an unsupported genuinely needed operation does, per decision §§4/6 with unchanged quality/adoption/cost conditions. Decision §8 retains both the old mandatory-gate withdrawal and the needed-Special operability duty.

FINAL verdict: **BOUNDED SCOPE-DECISION PASS (FINAL-BINDING), planning-only.** No candidate validation, no seven-point audit PASS, no adoption approval, no savings claim.

Exact bound snapshot: decision FULL §§1–8 SHA256 `9a7a6f6d69fb6829aa391044475bec4f1eab3125aa0ebbf926bede2788fcf496` /18345B; packet README SHA256 `0a546b6fa2bfd2c9a0d4f8c47e8071b6f157fccec88402f167cfabd292c58190` /5834B. Prior §§1–8 review above stands; document-check is separate. Stop at Human Commit Point; Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN / quality/adoption/savings OPEN unchanged.

(End — FINAL-BINDING confirmation.)
