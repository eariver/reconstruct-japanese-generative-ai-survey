# Closeout evidence index — repaired-correction rehearsal (20261112 packet)

Scope: real W34/SP correction bounded complete + Selection/Architecture PARTIAL/BLOCKED by substantial repeated validation cost (observed, not conclusively localized full-writer cause). No Selection/Human/R4/PDF/production PASS, no net savings. Independent closeout `independent-closeout-review.md` + machine is recorded **BOUNDED_CLOSEOUT_PASS** (bounded real-correction/Selection PARTIAL closeout, documentary only, no fresh full773 runtime certification; WITH reviewer FINAL-BINDING — recheck after these docs updates is pending, not claimed here).

## 0. Authority and epoch pins

- Root operation FULL §§1–21: `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md`
- Root closeout FULL (existing): `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-closeout-resolution.md`
- Independent closeout (recorded): `notes/rephase-1-repaired-correction-rehearsal-20261112/independent-closeout-review.md` + `independent-closeout-review-machine.json` — **BOUNDED_CLOSEOUT_PASS** (documentary only, no fresh full773 runtime certification; WITH reviewer FINAL-BINDING — recheck after these docs updates is pending, not claimed here)
- Packet entry: `notes/rephase-1-repaired-correction-rehearsal-20261112/README.md`
- Author assessment (this unit): `outputs/rephase-1-repaired-correction-rehearsal-assessment.md`
- Active: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` — HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` parent `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`
- Shadow (preflight/diagnostic only): `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work` — same HEAD/tree/parent, byte-copy, no shared objects
- Source773: manifest `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B, BASE head `409b292` (BASE tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`; runtime HEAD `ae0dd1e`とは区別), 773/773 in both runtimes
- Final delivery (prior shipping unchanged): DIRECT409 patch `171812f686c05d8494de8bd32a6c00e043dc5ff1aa7452204a8e35f16848600d`, manifest `a7e40c47…` (supplement-carry final141)

## 1. Terminal correction outcome (bounded)

- Adoption review: `adoption-outcome-independent-review.md` + `adoption-outcome-independent-review-machine.json` — verdict `BOTH_RESEARCH_CORRECTIONS_COMPLETE` (bounded, no Selection/R4/Human PASS)
- W34 State `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`/4162, CP `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`/6054, completion `80c12d0c…`/1972, guard absent, PREARCH/triplet/completion true; lifecycle `EVIDENCE_REVIEWED`, Human承認なし（activeなpending Gate activationなし）
- SP State `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`/4266, CP `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`/6300, completion `70d8c089…`/2009, guard absent; lifecycle `EVIDENCE_REVIEWED`, Human承認なし
- W34 R2: manifest `867eba96242eab0cf3e34277048e8497952c804f0805b4d09feacdb51b392a7b`/438583B, decision `09b2feae6dbae50762d66eae849088736c25cda58ba08b95dfcc62fb624cdc11`/4030B (`w34-supplied-decision-r2.json`)
- SP R2: manifest `de462dc79294da41e84d8eb1116a698cbbd23df715285ef0acddee039cf79ee4`/183765B, decision `9fd82385…`/4765B (`sp-supplied-decision-r2.json`), request `1587dbb793…`/389945B
- Four refs (typed `artifact_refs`, file-hash binding; prose prefix typos ignored):
  - W34 R2: evidence `eef77479…`/126592, views `3727485a…`/159502, ledger `066230f4…`/186214, completeness `d869027a…`/71532
  - SP R2: evidence `7f04e9ad…`/49237, views `45d60f9f…`/64222, ledger `5cf81f8f…`/66850, completeness `b4378609…`/34249
- Byte preservation: W34 405 unchanged cards/Views byte+JSON equal, SP 156 unchanged byte+JSON equal, plus 3 SP task supplement-ID rotations; counts reuse existing semantic review, not recounted here
- Epoch mechanics: exact W34 missing blob `155b78cfd588eb9300349e4568ee7065ae498477` (`a6e3eb30…`/2371B from fixed774) added to cc1c DB only; artifact-only child `ae0dd1e` changes only 2 Profile tree entries (`c2990d4f…` W34 live `2a8c3089…`, `9251f487…` SP live `aff05fd5…`), all other modes/OIDs preserved including `b797…`; partial-tree experiment `partial-tree-experiment-20261114T124450Z/`, contract `partial-tree-contract-review.md`

## 2. Selection preflight (TIMEOUT, no semantic PASS)

- Report + machine: `selection-preflight-20261115T042533Z/selection-preflight-20261115T042533Z-execution-report.md` + `selection-preflight-20261115T042533Z-execution-report-machine.json` (both editions stdout 0B/stderr 0B)
- Call map: `selection-preflight-20261115T042533Z/selection-revalidation-call-map.md` (finite DAG; 60/92/full162 AGはsource見積り、exact auditなし; derived pass積算の詳細は省略)
- Frozen inputs: `w34-selection-architecture-input.json` `15375476…`/378396B (409/45/5), `sp-selection-architecture-input.json` `072f90b6…`/72613B (160/130/9); reviews `reviews/W34-selection-architecture-review.md`, `reviews/SP-selection-architecture-review.md` (both `PROPOSAL_READY_FOR_PREFLIGHT`, input-scope only; W34 15/16pp, SP 60/75pp proposals)
- Runs (existing CLI, one per edition, 1200s cap, preflight-scope only; unit全体ではadoptがStateを書換え済み): W34 `selection-preflight-W34-20261115T042533Z.{argv,env,pid,wall-start,wall-end,exit,stdout,stderr}` exit 124, stdout 0B/stderr 0B, 0/7 slots; SP `selection-preflight-SP-20261115T042533Z.{...}` exit 124, stdout 0B/stderr 0B, 3/7 slots (`2f62e2a8…`/239359 matrix, `4e6884d6…`/76603 selection, `4af84ab3…`/33219 architecture; 4 absent)
- Run domain: active `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` untouched (HEAD `ae0dd1e`, status 33, 7-absent); shadow `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work` byte-copy (hardlinks 0, inodes differ, objects 231/231, origin inert, no commondir/alternates/worktrees, no new commit, shadow status 36 = 33 + 3 SP partials). No reconstruct Git/status/log/HEAD/readback, network, Production, ordinary commit/push, source edit, State fake, retry/cleanup.

## 3. Bounded diagnostic (READY gate only, 90s cap)

- Report + machine: `diagnostic-20261115T051801Z/diagnostic-report.md` + `diagnostic-report-machine.json`
- Helper (packet-only, no source edit): `diagnostic-20261115T051801Z/diagnose_ready_profile.py`
- Raw: `W34-ready.partial-signal.json`, `W34-ready.pstats.txt`, `SP-ready.raw.json`, `SP-ready.pstats.txt`, `before-hashes.json`, `before/after-*-status.txt`, `after-check.txt` (NONE), `W34/SP-ready.{argv,env,pid,wall-start,wall-end,exit,stdout,stderr,guard.json,start.json}`
- Results (diagnostic-scope only; profiler計測下の観測): W34-ready PID 740047 wall 85.01s exit 124 (alarm85+timeout90, 90s超の証明ではない), rchar Δ8854312583, read_bytes Δ40960, 90176914 calls; SP-ready PID 747458 wall 27.98s exit 0 (returned None), rchar Δ1175871247, read_bytes Δ0, 37064332 calls; same-process `/proc/self/io`+`resource` only, no child split; cProfile overhead未分離、hotspot相対順序の保証なし（root限定が優先）; CPU-bound page-cached logical work, not disk/deadlock/physical-savings proof
- Timeout stack: `survey_evidence_v2.py:515 _supplement_source_file (relative_to)` ← `:372` ← `:1779` ← `:1876 views` ← `:950 AG` ← `:1073 completion` ← `:4139 READY`
- Run domain: shadow only, one invocation per edition, `PYTHONDONTWRITEBYTECODE=1`, `GIT_NO_LAZY_FETCH=1`, `HOME` unchanged, guard HEAD `ae0dd1e`+LOW sha/bytes before import; source/State/slots unchanged after; diagnostic-scopeではno writer/prepare/adopt, no validator/cache patch, no subagents（unit全体のadoptとは区別）
- Parent-hash correction: diagnostic-report `…2168828…` is a typo; correct parent is `…2164828…` (`cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`). SP proposal review §0 parent `…2168282b…` / tree `…03d6b3e…` are also typos; correct parent is same cc1c, correct tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58` (root §4.5 explicit). Diagnostic machine `shadow` leading space is formatting only. Typed records and machine hashes bind, not prose.

## 4. Independent scaling review

- `independent-selection-scaling-review.md` + `independent-selection-scaling-review-machine.json` (fresh reviewer, root §20 only, read-only, no imports/tests/Git/network/Production/active writes/subagents)
- Confirms: 60/92/162AG as source-derived estimates (not measured totals, exact auditなし); EU 15-multiplier spot-checked, not validator-by-validator audited; READY-gate repetition measured, full-runner slow-pass vs repetition undistinguished beyond READY; hotspot相対順序の保証なし（root限定が優先）; SP 3 partials actual but not adoptable
- Judgment: REJECT unlimited timeout; REJECT copying shadow partials; SELECT bounded existing PREARCH-readiness/Selection scaling repair with private invocation-scoped checked-authority/freshness context + redundant-path elimination, preserving all predicates; requires Astra pre-code map + independent readiness confirmation BEFORE code

## 5. Preserved failures and deviations

- Operator/path: relative repo-root join (R1 refusal, Raw+request preserved); R1 sorted-key serialization drift (decision withdrawn, R2 order-preserving `core.json_bytes` recovery); D142 1-char pin transcription (r7 DATA correction vs c8 3751B); SP 3-field → 8-field closure correction (r8 factual copy, O10 not auto-SAT)
- Scope deviation: broad 542-DB + 2-DB diagnostic probes quarantined, not global-absence evidence; no repeat
- Partial DB: `b797…` and missing26309/bulk31466, runtime/TeX nonbundled remain; no hydration/fetch/substitution
- Placement: post-prepare reviews at workspace-root `reviews/` vs packet `reviews/` — originals preserved, qualified copy/addendum in packet
- Authorship: SP author shared-README rewrite preserved as `sp-author-entry-draft.md`, current README + root resolution control; authors limited to edition-prefixed DATA
- Semantics preserved as input-scope: W34 45/5 15target16max, SP 130/9 60target75max are proposals, not quota/approval; semantic reviews neither invalidated nor promoted by timeout
- No new fetch (source permission completed), no R4/generic-reader/PDF/ordinary commit/readback/Production
