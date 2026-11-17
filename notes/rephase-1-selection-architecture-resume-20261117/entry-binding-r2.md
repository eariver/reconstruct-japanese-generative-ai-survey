# Entry binding R2 — fresh stdlib verification (replaces reused-pin observation for stage dispatch)

Root authority: `notes/rephase-1-selection-architecture-resume-20261117/astra-operation-resolution.md` FULL §§1–2. This file is the requested fresh entry, not a reused documentary cert. No project imports, runtime, tests, stage/writer, network, source/State/output writes, subagents, reconstruct Git. Head is recorded-only (`3231a0c…`, parent `ae0dd1ee…`, tree `ff01b73…`); no fresh commit claim. Later operator will use explicitly isolated Git before execute. Static source-bound ready/log wrappers to be built later at root dispatch, not now.

Machine companion `entry-binding-r2-machine.json` holds machine-generated full rows (774 file rows + states/profiles/CP/completion/COPY/request/proof/report + 8 refs + 14 outputs + audit-inner). Values below are copied from that machine output, no hand types.

## 1. FULL774 fresh (stdlib hashlib/pathlib/stat, no project import)

- Manifest `notes/rephase-1-selection-scaling-repair-20261116/source-packaging/final-20261116T031000Z/complete-selection-scaling-manifest.json` `0dc361cb…`/187361B, intended 774.
- Selected runtime `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`: **774/774 match, 0 missing, 0 mismatch** (bytes + SHA256 + physical mode `0o664`/`0o775` all match manifest `physical_mode`; `git_mode` expected from manifest, not re-measured without Git).
- Verdict `PASS` for entry binding only; not stage PASS, Human approval, R4, CURRENT, delivery.
- Prior `continuation-observation-machine.json` `fresh_rehash_here:false` is superseded by this R2 for dispatch; prior file preserved, see annotation there. Prior malformed SP views pin (missing `f`) is corrected here via fresh re-hash.

## 2. States / Profiles (fresh file pins)

- W34 `sources/2026-W34/production-state.json` 4162B `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`, `lifecycle_state: EVIDENCE_REVIEWED`, history len 4, init `48082356…`.
- SP `sources/SP-efficient-llm-2026/production-state.json` 4266B `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`, same lifecycle/history shape.
- W34 Profile `sources/2026-W34/production-profile.json` 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1` (`WEEKLY`/`WEEKLY_MAGAZINE`).
- SP Profile `sources/SP-efficient-llm-2026/production-profile.json` 13748B `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45` (`THEMATIC`/`LONGFORM_SPECIAL`).
- Both `human_gates pending/null`, `selection/architecture pending/null`, `target_gate: ARCHITECTURE_REVIEW`. No approval invented.

## 3. PREARCH checkpoint / completion COPY (fresh pins, paths from typed records)

- W34 CP `…/w34-repaired-20261112-r2/checkpoint/record.json` 6054B `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`, `kind: PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`.
- SP CP `…/sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`, same kind.
- Cleanup completion (PREARCH operational, not evidence quality): W34 `…/completion/cleanup-completion.json` 1972B `80c12d0c53a76f21e3000c4e48a8e4ab843c2c63ac9cc69aeb3c9f20ddc46835`, SP 2009B `70d8c0896d2ce37c0aea2dc4e92cc4ef5008c48eddd54d2994d1f9c9fe41b8eb`. Each `seven_plan: 7x absent_legitimate`, `expected_after_state: {W34 a8586351…/4162B, SP 38a63411…/4266B}`, `postread: {triplet_match true, artifacts_rehashed true}`.
- Retained COPY: W34 `retention/state-before.json` 4087B `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0`, SP 4194B `180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220`; `retention/inventory.json` W34/SP pinned in machine; `request.json` W34 1654899B `bb6042c6…`, SP 389945B `1587dbb7…`; `proof/proposed-graph-proof.json` + `proof/supersession-report.json` pinned in machine.
- Guard `orchestration/v2/acceptance-revision.guard.json` absent both (file-existence only).

## 4. Eight typed refs (fresh re-hash vs declared in CP record)

- W34 `evidence-acceptance` 126592B `eef77479b8d9c003ee8daae7eb882ea2aa63063ea10aea3e43d1f951c747427d` match.
- W34 `edition-views-acceptance` 159502B `3727485ac1f791d64c3d951520bfab7694821ad4584140b913f91a1c48f654ae` match.
- W34 `materiality-ledger` 186214B `066230f48ff3d29e714be35e86968a4ec834f9dacefb4590f4b64ac1fb73b320` match.
- W34 `profile-completeness` (retained candidate) 71532B `d869027aefce95cde4478b875204c7f930755d66cc4d86e330b82b3835d5fdc6` match.
- SP `evidence-acceptance` 49237B `7f04e9adeddb327b085ede65de70638777a77a99810952bfdd44b6053a9a3327` match.
- SP `edition-views-acceptance` 64222B `45d60f9f19371ba9ae55f528cd20f674f0fbf4315bdabbfa4a4bedde6ba90939` match (corrects prior 63-hex transcription missing `f`).
- SP `materiality-ledger` 66850B `5cf81f8f2997d6784da12d805f5cfb54b6c9ebd3b94a2424983b5b591275bdc1` match.
- SP `profile-completeness` (retained candidate) 34249B `b43786099456346b2eaf6f6f63f9636b5407aeedb8ba2c77840bac9adc915757` match.

## 5. Fourteen outputs + frozen input / archive / audit (fresh pins + audit-inner)

W34 (all `READY_FOR_ARCHITECTURE_REVIEW` in summary, `human_review null`):

- `candidate-matrix-v2.json` 683098B `f4469c85b819d8436d37eecbaac68e07551e4942f0d86f124e6b6469480261af`
- `candidate-selection-v2.json` 375063B `f3a5000fe3c5370ae0768dc993f28fc3c64d9086ead566427728a1a6ff39a030`
- `architecture-v2.json` 24447B `9a76294ef05688c11fa6e114e96c98723e47c418522998ce835385c12a595615` (corrects any truncated transcription; fresh 64hex here)
- `architecture-review-summary-v2.json` 314350B `1b7f6076b11c5b47f41ab838ce70da7e5b2f4d856a3d309f6e8859828040eff7`
- `architecture-review-attention-v2.json` 18437B `d68b5f319e996a73076338b939f6661e46648ef9fd5b3033346e17ccfe6f5b92`
- `orchestration/v2/interactive/selection-architecture-input.json` 378396B `15375476f308fbfeb79c4e8f3f4d53d85d5cf917e36d29d3c3777580301aab3a` == frozen packet input.
- `orchestration/v2/interactive/selection-architecture-audit.json` 1436B `61d6a0bc5d427ecfb2bf5a4a3f47cdda2f9c01bf55b6ff3906f41bc01e6fd982`, inner 6 pins (5 outputs + input) all match.

SP:

- `candidate-matrix-v2.json` 239359B `2f62e2a82af38ce0d8d9eaa405399a1b24df5b70d62a9872f3d5aa8549d81a8b`
- `candidate-selection-v2.json` 76603B `4e6884d6bb8e8f5ca92b3344501687b686cd6355a65de69dfc98a9ab2e262a1f`
- `architecture-v2.json` 33219B `4af84ab37d60145407adf393a519077aeb5debaea33f0f8305fda636a858396c`
- `architecture-review-summary-v2.json` 67700B `d0092e132ecb9d094cf04a8ee97b1603bfaa777a18508f834a7a5a55c022a341`
- `architecture-review-attention-v2.json` 15918B `482f3c215597e1d91726506149356f3dbd5190ac173233f1f6ee84acd362dd9f`
- `orchestration/v2/interactive/selection-architecture-input.json` 72613B `072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd` == frozen.
- `orchestration/v2/interactive/selection-architecture-audit.json` 1530B `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449` (64hex, superseded 61hex do not use), inner 6 pins all match.

## 6. LIMITED vs completion (separate)

- `profile-completeness LIMITED`: research result `overall_status: LIMITED` in `sources/<edition>/profile-completeness-v2.json` (W34 71532B `d869027a…`, SP 33683B active `…`; retained candidate SP 34249B `b4378609…` is versioned R ref, not active-file confusion) + obligations/residual/closure. This is evidence-quality status, not a stage PASS.
- `PREARCH cleanup completion`: operational receipt `completion/cleanup-completion.json` (`seven_plan absent_legitimate`, `expected_after_state` == current State, `postread` true). Verifies guard-absent + COPY-derived expected_after + retained-inventory bind + LIVE triplet + FULL graph; does not certify evidence quality or future stage cost.

## 7. Canonical checkpoints (existence only, no execute)

- `sources/2026-W34/orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json` absent, `SELECTION_COMPLETE.json` absent; SP same absent. `CANDIDATES_NORMALIZED/ISSUE_INITIALIZED/DISCOVERY_COLLECTED.json` exist. Absence checked as file existence only before later write; no stage execution here.

## 8. Write-set / stops

- New files in this R2: `entry-binding-r2.md` (this file) + `entry-binding-r2-machine.json` (full rows companion). No source/State/output/guard writes, no Git, no runtime.
- Original `continuation-observation.*` preserved with head annotation pointing here; `normal-stage-operation-map.md` corrected by addendum only.
- Blocker for binding: none. Missing 0, mismatch 0. Substantive review corrections (§1 bullets 2–5) remain separate packet-local work; map must close before root stage execution. Future Human-reviewed commit distinct from execution `3231a0c`; no extra Human Commit Point needed between internal review and next root dispatch in same authorized unit; stop at coherent completed/blocked boundary. Ordinary Commit/Push Human-owned.

(End of file)
