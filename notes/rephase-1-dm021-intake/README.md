# DM-021 — limited later-evidence intake and disposition

2026-10-10. Human explicitly reported new Production DM-021 and requested checking/incorporation without disrupting current work. Intake was completed before LF-2I code changes; ordinary Production read-only/baseline boundaries remain.

- [Astra applicability disposition](astra-disposition.md) governs the [General report](evidence-20261009T171707Z/intake-and-impact.md).
- [Exact Summary capture](evidence-20261009T171707Z/deferred-maintenance-summary.md), [pins](evidence-20261009T171707Z/dm021-source.json), raw main-commit/Contents API responses and v1/v2 scripts/logs are preserved in `evidence-20261009T171707Z/`.
- Capture commit **afdb3df3faa20af3bb5798be429bba8dbd2100b1**, blob **62ee6a6b9792cc96e42f378c5cff67faebaeef43**, SHA256 **7c84b6d8e805cfadf5f10ac0ba587d278fd808461d305231906dcbf79f0c9a51**,62,505 bytes. Observed main commit, document self-reported last-reviewed main and fixed baseline774 are distinct identities.
- Exactly two network API calls are recorded. The v1 decode step was a no-op and the overall run failed on missing decoded output; v2 decoded the saved raw response without refetch. Prior d6381568 capture remains intact. Saved acquisition scripts are historical evidence, not reusable fetch instructions.

DM-021 reports missing truthful revalidation reason/authority rebind for **reader/editorial corrections after VALIDATED_DRAFT**: only REVIEWED_CORE_CHANGE is supported, while genuine editorial corrections are not shared-Core changes. Root statically confirmed that restriction in fixed409 controller/schema. Reported TS-003 exception Freeze/Release remains secondary evidence, `OPEN_CORE / EDITION_WORKAROUND`, not a generic Core fix; linked Issue560/PR561/run37955511006/edition records were not separately opened or adopted.

LF-2I remained an INITIAL generation + healthy normal readback unit. No new reason, immutable-checkpoint rewrite, stale-PDF waiver or `EXCEPTION_*` fixture was introduced. See [LF-2I completion](../../outputs/rephase-1-longform-lf2-implementation-assessment.md).

**Next selected contract-analysis unit:** examine DM-021's post-validation editorial-correction authority/reason/retention/normal continuation boundary against the current exact LF-2I composite, before selecting code. Preserve existing Weekly Core-change/mechanical-refresh behavior, original Architecture/Evidence/Draft authority, old immutable checkpoints and exact new reader/source/PDF/reviews/Preview binding. Determine the minimum justified scope and real fixture/oracles; no automatic reason enum expansion, no reuse of the TS-003 exception, no broad backlog batch. Additional primary intake is not automatic; reuse this capture and report any concrete evidence gap.

This adds a scoped21st disposition. Earlier20 dispositions keep their recorded scopes; the captured document's other refreshed recurrences were not independently re-audited. No CORE_FIXED/adoption/rebaseline/standing-refresh authority follows. Stop at the LF-2I Human Commit Point before the next contract unit.
