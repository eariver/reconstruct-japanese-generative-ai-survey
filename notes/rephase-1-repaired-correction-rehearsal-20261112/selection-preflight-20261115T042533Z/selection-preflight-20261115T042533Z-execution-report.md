# Selection/Architecture normal-writer preflight — separate-copy execution report (TIMEOUT, no semantic PASS)

Root: `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md` FULL §19 ONLY. No other authority. No stage advance, Human Gate, Draft, PDF, Approval, Production, root Git readback, subagents, network, ordinary commits, config/HOME changes, source edits, State fake/reinit, manual normalization, mirrored producer, validator stubs.

## 1. Source authority (typed records, not typo prose)

- Active (MUST untouched, preserved): `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
  HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, parent `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`.
- Shadow (NEW preflight workspace, byte-copy): `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work`
  HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, parent `cc1c…`, tree `ec11…` — verified identical to active pre-run.
- Isolation: `.git` is dir (no symlink/file), no `commondir`, no `worktrees`, no `objects/info/alternates`, `find -links +1` 0, `find .git -type l` 0, HEAD/index/sample inodes differ active vs shadow (HEAD 22452579 vs 24925445, index 22452498 vs 24924016), object files 231 vs 231 same count no sharing. Origin inert `https://example.invalid/rephase-candidate-recovery.git`. No `GIT_*` overrides except controlled `GIT_NO_LAZY_FETCH=1`. `HOME=/home/eariver` unchanged, local config only inert remote, no new commits (shadow HEAD still `ae0dd1e`, status 33→36 = +3 SP partials only).
- Source773: manifest `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B, head `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, 773/773 existent active and shadow. Spot tools: HIGH `f312f02e…`/97844, LOW `7f5fc9e0…`/240969 unchanged.
- Epoch objects: restored `155b78cfd588eb9300349e4568ee7065ae498477` blob readable (`a6e3eb30…`/2371), artifact profiles `c2990d4f…` (W34 live `2a8c3089…`) and `9251f487…` (SP live `aff05fd5…`) at `ae0dd1e` readable, `ls-tree -r ae0dd1e -- <2 profiles>` exact.
- Profiles: W34 `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`/2371, SP `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`/13748 — live bytes = commit blobs.
- States (EVIDENCE_REVIEWED, init480, Human pending, guard absent): W34 `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`/4162, SP `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`/4266 — active = shadow pre/post, no drift.
- PREARCH checkpoints: W34 `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`/6054, SP `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`/6300. Completions: W34 `80c12d0c…`/1972, SP `70d8c089…`/2009. Guard absent both issues pre/post. Seven slots absent both issues pre-run (14/14 absent good).
- Four refs (typed `artifact_refs`, not prose prefixes):
  W34 R2: evidence `eef77479b8d9c003ee8daae7eb882ea2aa63063ea10aea3e43d1f951c747427d`/126592, views `3727485ac1f791d64c3d951520bfab7694821ad4584140b913f91a1c48f654ae`/159502, ledger `066230f48ff3d29e714be35e86968a4ec834f9dacefb4590f4b64ac1fb73b320`/186214, completeness `d869027aefce95cde4478b875204c7f930755d66cc4d86e330b82b3835d5fdc6`/71532.
  SP R2: evidence `7f04e9adeddb327b085ede65de70638777a77a99810952bfdd44b6053a9a3327`/49237, views `45d60f9f19371ba9ae55f528cd20f674f0fbf4315bdabbfa4a4bedde6ba90939`/64222, ledger `5cf81f8f2997d6784da12d805f5cfb54b6c9ebd3b94a2424983b5b591275bdc1`/66850, completeness `b43786099456346b2eaf6f6f63f9636b5407aeedb8ba2c77840bac9adc915757`/34249.
  Old canonicals preserved but NOT used. Prose prefix typos ignored; only file hashes above bind.

## 2. Frozen inputs + independent reviews (PROPOSAL_READY, no Selection PASS)

- `notes/rephase-1-repaired-correction-rehearsal-20261112/w34-selection-architecture-input.json` `15375476f308fbfeb79c4e8f3f4d53d85d5cf917e36d29d3c3777580301aab3a`/378396B — matches W34 review machine `input.bytes 378396/sha 15375476…`. Assignments 409, packages 5, 45 selected (24 PRIMARY +21 SUPPORTING), 364 HOLD, 30 nonMatrix. Review: `reviews/W34-selection-architecture-review.md` + machine verdict **PROPOSAL_READY_FOR_PREFLIGHT** (bounded DATA only, NOT Selection/Architecture PASS, NOT Human approval).
- `notes/rephase-1-repaired-correction-rehearsal-20261112/sp-selection-architecture-input.json` `072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd`/72613B (actual file hash/bytes, review lists shape only). Assignments 160, packages 9, 130 selected (14 PRIMARY +116 SUPPORTING), 30 HOLD, 5 nonMatrix EXCLUDED. Review: `reviews/SP-selection-architecture-review.md` + machine verdict **PROPOSAL_READY_FOR_PREFLIGHT** (bounded DATA, NOT Selection/Architecture/R4/Human PASS).
- No input alteration. No staging copies to active. Absolute packet inputs passed as `--input`. Runner `scripts/run_selection_architecture_v2_interactive.py` `553bf22bb7d218af3b20f7ba303110b7c7918da4de5e39e07c756675503f2b31`/27766 in shadow verified pre-run.

## 3. Normal-writer runs (one per edition, EXISTING CLI, no stubs)

Common: `PYTHONPATH=ABSshadow`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_NO_LAZY_FETCH=1`, `cwd=ABSshadow`, `--repo-root ABSshadow`, `--state sources/<issue>/production-state.json` (relative, resolved under root), `--input ABSinput`. Packet dir `notes/rephase-1-repaired-correction-rehearsal-20261112/selection-preflight-20261115T042533Z/` holds raw `*.argv/*.env/*.pid/*.wall-start/*.wall-end/*.stdout/*.stderr/*.exit`.

- W34: `selection-preflight-W34-20261115T042533Z.*`
  argv: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ABSshadow GIT_NO_LAZY_FETCH=1 python3 ABSshadow/scripts/run_selection_architecture_v2_interactive.py --repo-root ABSshadow --state sources/2026-W34/production-state.json --input ABS/w34-selection-architecture-input.json`
  env whitelist: `HOME=/home/eariver`, `LANG=ja_JP.UTF-8`, `PATH=…`, `PWD=/home/eariver/git/reconstruct-japanese-generative-ai-survey`. PID file `710005` (outer persistent-shell PID; python child not separately polled — limitation noted, wall times authoritative). wall-start `20261115T042735Z`, wall-end `20261115T044750Z`, exit `124` (timeout 1200s), stdout 0B, stderr 0B. No retry/cleanup per §19 first-failure STOP.
- SP: `selection-preflight-SP-20261115T042533Z.*`
  same shape with `sources/SP-efficient-llm-2026/production-state.json` + `sp-selection-architecture-input.json`. PID `712363` (unique `timeout→python` wrapper PID via `$!`), wall-start `20261115T044836Z`, wall-end `20261115T050841Z`, exit `124` (timeout 1200s), stdout 0B, stderr 0B. Source intact pre-SP verified (States/Profiles/guards/7-absent unchanged after W34 timeout), so second edition single call permitted.

## 4. Post outputs (actual, no semantic PASS)

Seven expected slots per issue (`DM022_SEVEN_SLOTS`): `candidate-matrix-v2.json`, `candidate-selection-v2.json`, `architecture-v2.json`, `architecture-review-summary-v2.json`, `architecture-review-attention-v2.json`, `orchestration/v2/interactive/selection-architecture-input.json`, `orchestration/v2/interactive/selection-architecture-audit.json`. Writer may create only these; State must remain EVIDENCE_REVIEWED.

- W34: 0/7 created. `candidate-matrix-v2.json` absent, all 7 absent. No archive byte-eq, no audit, no closing shapes, no attention overflow to inspect. State `a858…` unchanged, no guard, HEAD `ae0dd1e` unchanged.
- SP: 3/7 created (partial, timeout mid-write):
  `candidate-matrix-v2.json` `2f62e2a82af38ce0d8d9eaa405399a1b24df5b70d62a9872f3d5aa8549d81a8b`/239359B rows 160 summary `MATERIAL 132/CONTEXT 28/PARTIAL 152/VERIFIED 8`.
  `candidate-selection-v2.json` `4e6884d6bb8e8f5ca92b3344501687b686cd6355a65de69dfc98a9ab2e262a1f`/76603B `ESTABLISHED` 160 assignments `SELECTED 130/HOLD 30`.
  `architecture-v2.json` `4af84ab37d60145407adf393a519077aeb5debaea33f0f8305fda636a858396c`/33219B `PROPOSED` 9 packages primary 14 (5+5+1+1+2) supporting 116 (3+19+15+22+6+14+15+3+19) page 60/75, boundaries 5/23/20/37/16/25/23/15/35 non-empty unique (inherited union present), basis pins `aff05…/b437…/5cf8…/2f62…/4e68…` consistent.
  Absent 4/7: `architecture-review-summary-v2.json` absent, `architecture-review-attention-v2.json` absent (no overflow check possible), archive `selection-architecture-input.json` absent (no input byte-eq possible), `selection-architecture-audit.json` absent. No `closing_summary`/`weekly_closing_summary` review shapes to validate (review-summary absent); SP `publication_extensions {}`/`profile_extensions {}` empty as built (no invent). No stdout JSON (timeout before `run()` return), so no `selected_count`/`review_readiness` to report.
- Schema: no validator run (would be mirrored validator stub if re-implemented). File JSON parses above; full schema-gate not claimed.
- Source/State preservation post both runs (shadow): States `a858…`/`38a…`, checkpoints `73ab…`/`2a528…`, four refs `eef7…/3727…/0662…/d869…` + `7f04…/45d6…/5cf8…/b437…` unchanged, source773 773/773, Profiles `2a8c…`/`aff05…` unchanged, guards absent, W34 7 absent, SP 4 absent +3 present (no overwrite of pre-existing, preflight `lstat` passed). Shadow status 36 = active 33 +3 SP partials. Active: HEAD `ae0dd1e` unchanged, status 33 unchanged, States/CPs/773/7-absent unchanged, no new files. Real ACTIVE untouched.

Actual pass/fail counts (mechanical only, no semantic PASS):
- Writer invocations: 2 attempted, 0 exited 0, 2 timed out (exit 124). W34 0/7 slots, SP 3/7 slots. No `READY_FOR_ARCHITECTURE_REVIEW`, no `ADOPTED`, no `ARCHITECTURE_ESTABLISHED`.
- No Selection PASS, no Architecture PASS, no Human approval, no Draft/PDF, no R4. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN preserved.

## 5. Minimal defect (instead of generic new features)

Both normal writers exceed 1200s with zero stdout: W34 (409 assignments) zero writes, SP (160 assignments) 3/7 writes then timeout. This is honest per-record cost, not cheap/performance-neutral. Do NOT auto-start active generation, retry, cleanup, or new features. Next requires root decision on lawful epoch continuation + independent review binding actual inputs/artifacts before any active canonical generation. Stop at Human Commit Point. Ordinary Commit/Push Human-owned.
