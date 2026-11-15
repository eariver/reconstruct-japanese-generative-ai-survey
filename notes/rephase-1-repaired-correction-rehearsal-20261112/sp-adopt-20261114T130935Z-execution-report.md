# SP normal adopt — COMPLETED (no Selection, no semantic claim beyond independent decision)

Root §17, new epoch `ae0dd1e…`/tree `ec11cf6c…` (parent cc1c). Verified pre-adopt: source773 `a7e40c…`, SP State `180db8c3…` EVIDENCE_REVIEWED/init480, CP `1233b1f6…`, Profile `aff05fd5…` 13748B, Contract8 pipeline `3adfbda2…`, 4Raw `14ae3118…/253542, 35770834…/307198, 97a5dd74…/350662, f7eeec68…18672662/3751` FULLDID/literal, supp `ff3ba775…`/31530, request `67fa3d9e…`-derived R2 `1587dbb793…`/389945 order-preserving, R2 manifest `de462dc7…`/183765 (160 tasks/cards/views), 7 slots absent, Human pending/null/inactive, guard absent; W34 active `a8586351…`/`73ab28ea…`/completion + R1/R2/old graphs preserved.

## Decision (verbatim OEXCL, no R1 rebind)
- Packet `sp-supplied-decision-r2.json` `9fd82385045988b15af67d918013da783ea67274a94aaf5edb1633da77d29554`/4765 (genuine independent research, NOT R1 `b7a78bfa…`) → repo `sources/SP-efficient-llm-2026/research/v2/acceptance-revision-inputs/sp-repaired-20261112-r2-decision.json` same hash/size/mode `0o664`.

## Adopt (ONE HIGH CLI, ABS repo, CWD ABS, PYTHONPATH=ABS, bytecode off, clean Git env, unique raw)
- `adopt --repo-root ABS --state-path …/production-state.json --revision-path …/sp-repaired-20261112-r2 --decision-path …/sp-repaired-20261112-r2-decision.json` → exit 0, `status ADOPTED`, `guard_released true`, expected-after `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`, checkpoint `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`, 7 slots `absent_legitimate` ×7. HIGH proved/guarded/switched/completed/read-back/released internally; no manual State/guard/schema/source operation.
- New State `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde` EVIDENCE_REVIEWED/init480, history 4 rows last `EVIDENCE_REVIEWED@e84` (no append); CP evidence/materiality/completeness → R2 `record.json 2a528ed5…`; active four refs evidence `7f04e9ad…`/49237, views `45d60f9f1…`/64222, ledger `5cf81f8f…`/66850, completeness `b4378609…`/34249 via typed supersession; old CP `1233b1f6…` + old four `1557fef7…/65784e69…/b7c85b4d…/d67f7f83…` preserved as lineage/parent; old canonical Ledger/Comp/Profile/accepted sets + R1 (`694f5e49…`/`67fa3d9e…`/`b7a78bfa…`) unadopted-preserved. 773 `a7e40c…` unchanged.

## Resume + readback (completed-operation verification only)
- `resume` exit 0 `ALREADY_ACTIVE` (`State already after with guard absent + completion verified; no new acceptance or approval`).
- `readback --revision-path …/sp-repaired-20261112-r2` exit 0: `family PREARCH, triplet true, checkpoint 2a528ed5…, completion_present true, original_anchor=parent_checkpoint=1233b1f6…`. Strict State/readiness/active-four-refs verified current; no Selection/Architecture.

Classification: actual COMPLETED (adopt + ALREADY_ACTIVE + triplet readback), not guarded-partial. No semantic/human-approval claim beyond independent decision `9fd82385…`.
