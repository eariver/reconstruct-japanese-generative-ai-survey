# Bounded NONPUBLISHING diagnosis — Selection preflight timeout (Root §20)

Root: `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md` FULL §20 ONLY.
Timeout report: `notes/rephase-1-repaired-correction-rehearsal-20261112/selection-preflight-20261115T042533Z/selection-preflight-20261115T042533Z-execution-report.md` + machine JSON.
This packet: `notes/rephase-1-repaired-correction-rehearsal-20261112/diagnostic-20261115T051801Z/`. No subagents.

## 1. Source / State / PREARCH verification (actual bytes, pre + post)

- Shadow `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work` HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, parent `cc1c7fd1cf979e71fda4ae2168828b37bc1b2325` — verified pre/post. Active `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` HEAD same `ae0dd1e` — verified pre/post unchanged.
- Source773: manifest `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B, head `409b292756dd1277b9dfae87679934c0d2ce251c`, 773 entries, 0 missing in shadow and active. Spot HIGH `f312f02e…`/97844, LOW `7f5fc9e0…`/240969, runner `553bf22b…`/27766 unchanged.
- States (EVIDENCE_REVIEWED): W34 `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`/4162, SP `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`/4266 — shadow active=pre=post, no drift. Profiles W34 `2a8c3089…`/2371, SP `aff05fd5…`/13748 — live bytes = commit blobs.
- PREARCH checkpoints: W34 `73ab28ea…`/6054, SP `2a528ed5…`/6300 unchanged. Completions W34 `80c12d0c…`/1972, SP `70d8c089…`/2009 unchanged. Guard absent both issues pre/post.
- Four refs (typed `artifact_refs`): W34 evidence `eef77479…`/126592, views `3727485a…`/159502, ledger `066230f4…`/186214, completeness `d869027a…`/71532; SP `7f04e9ad…`/49237, `45d60f9f…`/64222, `5cf81f8f…`/66850, `b4378609…`/34249 — all 8 actual file hashes match checkpoint record, pre/post unchanged.
- Seven slots: W34 0/7 absent pre/post; SP 3 present (`2f62e2a8…`/239359, `4e6884d6…`/76603, `4af84ab3…`/33219) + 4 absent pre/post, no overwrite. Shadow status 36 = active 33 + 3 SP partials, identical pre/post. See `before-hashes.json`, `before/after-*-status.txt`, `after-check.txt` (NONE).

## 2. Scoped owned-process status only

- Recorded outer PIDs `710005` (W34) / `712363` (SP) from preflight `*.pid`: both absent via `ps -o pid,ppid,etime,args -p <pid>` (no output). No live `pgrep -af selection-preflight-20261115T042533Z/candidate-work/scripts/run_selection` except own pgrep string. No kills, no inference that outer-shell PID equals Python child PID. Wall times from preflight report authoritative (W34 `20261115T042735Z`→`20261115T044750Z` exit 124, SP `20261115T044836Z`→`20261115T050841Z` exit 124, stdout/stderr 0B each).

## 3. Selected READ-ONLY entry (source-inspect basis)

Normal writer `scripts/run_selection_architecture_v2_interactive.py:run()` order before first write (`candidate-matrix-v2.json`):
`agent.validate_agent_state` (State schema/checkpoint) → `EVIDENCE_REVIEWED` check → `_dm022_require_ready` → `low.require_research_operation_ready(repo,state_path)` → discovery/ledger/completeness resolve (incl `resolve_research_authority` FULL) → `_dm022_preflight_seven` → `derive_candidate_matrix` → first `_dm022_require_ready` → first write.

Selected `low.require_research_operation_ready`: it plausibly preempts W34 first write because W34 produced 0/7 with zero stdout, and this gate runs before any matrix derivation/write, performs FULL completion verification (`_verify_completion_full` → 2× `_verify_adopted_graph_full` with complete evidence/views/ledger/completeness content validators + own-epoch pins) over 409 (W34) vs 160 (SP) assignments. `validate_agent_state` is lighter State/provenance checks; not selected as primary bottleneck. No `current_stage_basis_override` facade used — normal entry calls READY outside that override, so direct call matches; no bypass to later site, no writer/prepare/adopt, no canonical artifacts, no monkeypatch/cache/projection.

## 4. Diagnostic invocations (ONE per edition, MAX 90s)

External helper `diagnose_ready_profile.py` (packet only, no source edits): source guard (HEAD `ae0dd1e`, LOW sha/bytes, State file) BEFORE shadow import; `sys.path.insert(0, shadow)` after guard; `PYTHONDONTWRITEBYTECODE=1`, `GIT_NO_LAZY_FETCH=1`, `PYTHONPATH=ABSshadow`, `cwd=ABSshadow`, no `GIT_*` overrides besides allowlisted, `HOME=/home/eariver` unchanged, no network/Production/reconstruct Git. cProfile + `faulthandler.dump_traceback`; same-process `/proc/self/io` rchar/read_bytes + `resource` cpu + wall before/after saved raw; `SIGTERM`/`SIGALRM` handler flushes `*.pstats.txt/*.pstats.bin/*.traceback-*.txt` + partial raw then `os._exit(124)`. Internal `alarm(85)` + external `timeout -s TERM 90`.

- W34-ready: PID `740047`, argv/env in `W34-ready.argv/.env`, wall-start `20261115T051840Z`, wall-end `20261115T052010Z`, exit `124`, stdout 0B, stderr `received signal 14, flushed stats`. Guard PASS. Timeout-signal-14 partial: wall 85.01s, utime 0.24→78.75 (Δ78.51s), stime 0.02→5.68 (Δ5.66s), maxrss 85952KB, rchar 4826432→8859139015 (Δ8854312583 ≈8.85GB logical), read_bytes 98304→139264 (Δ40960 ≈40KB disk). cProfile 90176914 calls (87096096 primitive) in 84.998s. No `W34-ready.raw.json` (timeout by design); `W34-ready.partial-signal.json` + pstats preserved.
- SP-ready: PID `747458`, wall-start `20261115T052048Z`, wall-end per file, exit `0`, stdout 0B wrapper + `SP-ready.stdout.txt` READY, stderr 0B, `SP-ready.raw.json` outcome `returned`, result `None` (READY returns None). Wall 27.98s, utime 0.24→26.08 (Δ25.83s), stime 0.03→2.09 (Δ2.06s), maxrss 56636KB, rchar 4826432→1180697679 (Δ1175871247 ≈1.18GB logical), read_bytes 0→0 (Δ0, page-cached). cProfile 37064332 calls in 27.98s.

Before/after source/State/slots unchanged (see §1, `after-check.txt` NONE, HEAD/status identical, no `__pycache__`/pyc in shadow). One invocation each, no repeat/fix.

## 5. Observed scope (not disk claim / deadlock proof) + hotspots

Timeout bound is observation limit only, not proof of deadlock or universal performance. Actual same-process observation: CPU-bound (W34 78.5s utime / 85s wall, SP 25.8s / 28s wall) with huge logical `rchar` vs tiny `read_bytes` (page cache), not disk-wait claim. Concrete call hotspots (cumulative, W34 / SP):

- `require_research_operation_ready:4087` 84.998s / 27.980s → `_verify_completion_full:996` 84.997 / 27.978 → `_verify_adopted_graph_full:802` ×2 84.825 (42.4 avg) / 27.794 (13.9 avg).
- `_validate_evidence_acceptance_content:1738` 61.743 (8 calls) / 19.972 (12 calls); `_validate_materiality_ledger_content:2724` 37.788 (2) / 15.578 (4); `_validate_edition_views_acceptance_content:1856` 32.975 (4) / 13.376 (6).
- `_assert_pin_repo_ancestors:280` 23.034 (20937 calls) / 15.888 (14532); `openssl_sha256` 23.321 (66230) / 3.096 (33837); `Path.relative_to:475` 19.461 (127743) / 7.939 (50302); `_validate_profile_completeness_content` 18.788 / 7.901; `_repo_file:131` 18.625 (21089) / 12.903 (14760); `lstat` 14.111 (2154321) / 6.039 (771906); `derive_ordinary_root_effective_context:1861` 13.711 (2) / 2.386 (2); schema `validate_instance` + `referencing` descend ~10s / ~4s.
- W34 timeout stack (via controlled signal): `survey_evidence_v2.py:515 _supplement_source_file` (`Path.relative_to`) ← `:372 _resolve_phase_supplement_context` ← `:1779 _validate_evidence_acceptance_content` ← `:1876 _validate_edition_views_acceptance_content` ← `survey_research_authority_v2.py:950 _verify_adopted_graph_full` ← `:1073 _verify_completion_full` ← `:4139 require_research_operation_ready`. SP same chain returns.

Interpretation: per-record FULL revalidation cost scales with assignments/context (W34 409 >3× SP 160 in calls: 90M vs 37M, rchar 8.85GB vs 1.18GB); READY gate alone exceeds 90s for W34 and consumes ~28s for SP, before any matrix/write work. This explains 1200s writer timeouts (W34 0/7, SP 3/7) as honest per-record cost, not cheap/neutral. Next requires root decision on lawful epoch continuation + independent review binding actual inputs/artifacts before any active canonical generation. No stage advance/Human/Draft/PDF/Approval/Production/readback/network/commits. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
