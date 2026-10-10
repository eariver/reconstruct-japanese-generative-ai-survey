# DM-021 intake and LF-2I impact

Packet: `notes/rephase-1-dm021-intake/evidence-20261009T171707Z/`
Pins: observed `main` **`afdb3df3faa20af3bb5798be429bba8dbd2100b1`**
(`docs(Core v2): keep TS-003 r0.8 ledger and revision history rows inside tables`,
parent `6014e57bee957befced8e03d77d2a220f60e4d92`);
doc blob SHA **`62ee6a6b9792cc96e42f378c5cff67faebaeef43`**
(`git hash-object` == Contents API `sha`), SHA-256
`7c84b6d8e805cfadf5f10ac0ba587d278fd808461d305231906dcbf79f0c9a51`,
62,505 bytes, 850 lines. Exactly two `gh` API calls (main metadata +
single contents fetch at exact SHA); both exit 0, stderr 0 bytes.
Raw responses, decode logs, argv/exit files preserved in packet.
Fixed baseline `774dd39a...` unchanged; prior `20261003` capture untouched.

Acquisition note: v1 script's decode step lacked its heredoc body (no-op;
decoded file absent, v1 run exit 1 preserved as evidence). V2 corrected
script performed NO new network call: it decoded exactly once from the
already-saved v1 raw JSON into the decoded file. No overwrite of any
existing evidence occurred.

## Exact reported problem (secondary evidence, not reproduced)

**CV2-DM-021 — Post-`VALIDATED_DRAFT` reader/editorial corrections have no
truthful revalidation reason class** (doc lines 690–727).

- Shared Core v2 has an immutable, State-bound post-validation
  publication-surface revalidation record, but `scripts/survey_agent_control_v2.py`
  **and** `schemas/publication-surface-revalidation.schema.json` allow only
  the `REVIEWED_CORE_CHANGE` reason. Post-`VALIDATED_DRAFT`
  independent/editorial/Human PDF-review corrections are not a reviewed
  shared-Core change; using that reason would misstate review authority,
  while rewriting immutable `DRAFT_COMPLETE.json` or publishing the stale
  PDF would violate exact-byte provenance.
- TS-003 (`SP-vision-multimodal-2026`) reproduction: old canonical PDF
  `0916bb5e…` / TeX `edcf8ef9…` bound in immutable `DRAFT_COMPLETE.json`;
  Human-approved corrected 39pp PDF `b2de84493f2215e26d16e569498c5f4b6476ebc314230cbb4e01540a72742093`
  (708,782 bytes). State stayed `VALIDATED_DRAFT`, `publication_preview = pending`.
- One-off Human-authorized bypass **conditional on logging the shared-Core
  defect**: Issue #560 opened; exact bytes + TeX/Bib/style + evidence
  Freeze-pinned with explicit `EXCEPTION_FROZEN` manifest (PR #561); public
  Release `special/vision-multimodal-2026` created, downloaded PDF reverified
  by run `37955511006`; distinct `EXCEPTION_RELEASED` record committed.
  Normal Core `FROZEN/RELEASED` lifecycle and formal Publication Preview
  approval are **not** claimed. The bypass solved TS-003 operationally, not
  the generic defect.

Reported status: **`OPEN_CORE / EDITION_WORKAROUND`**.
Affected boundary: shared-Core files `scripts/survey_agent_control_v2.py` +
`schemas/publication-surface-revalidation.schema.json` (reason taxonomy),
plus the absent `REVIEWED_EDITORIAL_CORRECTION`-equivalent reason,
supersession record, and normal candidate → Preview → Freeze → Release
continuation with the new PDF SHA. Explicit non-boundary: technical content
defects stay under DM-006/015/020; the TS-003 exception itself must **not**
be merged into Core v2 nor marked `CORE_FIXED`. Recurrences refreshed:
DM-006/015/020; ledger row (line 805) and r0.8 revision row (line 820)
record the same event.

## Does LF-2I change before implementation? No.

DM-021's generic fix (new revalidation reason, supersession record,
lifecycle continuation, Weekly/Special + illegitimate-reason coverage) is
Production shared-Core maintenance, explicitly deferred to a consolidated
batch. It falls squarely in LF-2 contract §6's excluded category
(`config/survey-production-v2.json`: "no dispatcher/lifecycle policy
repair") and contract §§2/5's declared non-scope ("Changed-Core pending
establishment and mechanical renewal are not implemented by this unit …
preserve that failure instead of adding a … bypass"). LF-2I's 7-path
budget contains no agent-control/revalidation-schema path, and its fixtures
are synthetic committed fixtures in an isolated DB — never the Production
`EXCEPTION_*` records, which must not be consumed as authorities or
readback fixtures.

Two contact points need discipline, not redesign:

1. **Revalidation-pointer rule (§5).** "An existing valid revalidation
   pointer must not be rejected merely for existing" does not license
   treating an editorial-correction context as `REVIEWED_CORE_CHANGE` or
   inventing a new reason. If LF-2I meets such a context, preserve the
   validator's refusal and document the precise unsupported operation, per
   §5/F3 — DM-021 confirms that refusal is correct behavior, not a bug to
   work around.
2. **Evidence item 5 / F3 readback.** "Renewed mechanical bindings …
   without stale PDF/visual/Human waiver" and healthy `FROZEN/RELEASED`
   readback via valid synthetic authorities are unaffected; TS-003's
   exception records (normal State `VALIDATED_DRAFT`) are not healthy
   authorities.

## Suggested bounded disposition

- Proceed with LF-2I on the selected contract `4795a586…` + F1–F3
  resolution unchanged; no path-budget or oracle edit for DM-021.
- Record DM-021 as an explicit LF-2I non-goal/unsupported scope at
  implementation entry: do not implement `REVIEWED_EDITORIAL_CORRECTION`,
  do not touch agent-control/revalidation-schema, do not consume
  `EXCEPTION_FROZEN/EXCEPTION_RELEASED`, do not mark anything `CORE_FIXED`.
- If the missing-reason refusal is hit during implementation, stop with the
  exact raw/source blocker per contract §5/F3 rather than bypassing.

## Unresolved questions (primary evidence deliberately not read)

- Issue #560, the TS-003 defect record
  (`…/defects/ts003-post-validation-editorial-revalidation-gap-20261010.md`),
  exception manifest/release record, PR #561, and run `37955511006` were
  **not** opened per the read-only boundary; the account above is reported
  secondary evidence from the Summary only.
- Pinned fetch commit `afdb3df3…` is newer than the doc's self-reported
  "Last reviewed `main`" `7c8e4b1e…`; the delta between them (commit message
  says TS-003 r0.8 table-row formatting) was not diffed — a second fetch is
  outside this authorization.
- Whether LF-2I's actual `_PendingPublicationBasis` call paths intersect the
  missing-reason gap is an implementation-task observation, not answered here.
  No code was read, tested, or edited in this intake.
