# Weekly regeneration witness — evidence closeout (documentary corrections, no new runs)

- Role: General author-side Co-Worker. Author-side evidence only; no independent review needed or claimed for this experiment.
- Scope of this document: residual limitations of the original packet (`logs/20260927T153429Z/`) and the supplement packet (`logs/20260927T160625Z/`), plus durable artifact preservation. NO code edits, NO runtime/tests/imports, NO fixture mutations, NO reset/clean were performed for this closeout. Original scripts and logs are preserved byte-identical (re-hashes in §F).
- Authority: root residual-limits review (items 1–6). The root decision and handoff are unedited.

## Core positive observations retained (first/repeat)

With commit-only and verify/refresh in distinct processes and real current-helper imports logged per run (`s-refresh-first.log`, `s-refresh-repeat.log`): comment-only control change with identical scope bytes + criteria → strict State and identical-surface derivation pass; old receipt/Gate reject (`Weekly receipt implementation or contract changed since renderer commit`); rebuilt receipt replays with accepted/authored refs list-equal to the superseded receipt; CLI-renewed Gate binds the new receipt; strict drift + gate-only pending basis; existing revalidation establishes r1 (`3f195000…`, 2026-09-27T16:12:03Z, supersedes null) and, with intact r1 predecessor, r2 (`b8f82855…`, 2026-09-27T16:12:57Z, supersedes r1, r1/checkpoint unchanged). No-op repeat refused with raw CLI logs saved.

## 1. N1/N2 oracle weakness (run_case lines 631–638)

`s_negatives.run_case` (`witness_harness_supplement.py:631-638`) catches bare `Exception` around the runtime call, so it also catches its own sentinel `AssertionError("<name> runtime unexpectedly admitted")`. A green N1/N2 therefore proves only that *some* exception was recorded — a weak reusable oracle, NOT an acceptance-safe test. Do not cite N1/N2 green alone for future acceptance.

What CAN be cited is the actually observed saved error text (read verbatim from the packet, not inferred):

- N1 (`sneg-n1-surface-runtime.err.txt`): `ValueError: Weekly reviewed reader input drift` — a genuine runtime `ValueError` from `validate_receipt`, not the sentinel.
- N2 (`sneg-n2-upstream-runtime.err.txt`): `AgentControlError: pending publication State invalid: Stage Checkpoint artifact drift: issue-architecture; Architecture Approval Record does not bind exact Architecture bytes` — a genuine runtime `AgentControlError`, not the sentinel.

N3 asserts its message separately (`check family differs`, `witness_harness_supplement.py:637-638`); N4 catches `AgentControlError` specifically (N4 block). No new tests were run to document this; the conclusion rests on the saved files above.

## 2. Verify-window correction (what “zero delta” actually covers)

Correction: the supplement report's blanket “verify-only ops assert zero delta” is NOT true as stated. `_refresh_common` (strict State, `load_derivation`, old receipt/Gate negatives) and `harness_preconditions` execute BEFORE `snap_pre` in both refresh phases, so their reads are not covered by any delta assertion.

Meaningful, exactly-windowed assertions that DID execute (exclusions for every delta: `.git/`, `.witness-evidence/` instrumentation, `__pycache__` — all disclosed):

- Receipt write window (`snap_pre` → post-receipt): delta == receipt file only.
- Gate CLI window (post-receipt → post-gate): delta == gate file only.
- Revalidation window (post-gate → post-record): delta == new revalidation record + State pointer file.
- Negative windows: M1 (post-mutation) == M2 (post-policy-refusal) == M2b (post-runtime-refusal); M3 (post-restore) == S0 baseline; plus State-sha and revalidation-record-listing invariance.

Durability distinction: supplement sidecars (`s-refresh-first/repeat.sidecar.json`, `s-negatives.sidecar.json`) store assertion OUTCOMES and hashes, NOT snapshot data — the deltas were computed in-process and are not re-derivable from the sidecars. The original W sidecars (`w0/w1/w2/w3/w4/w5/w6-sidecar.json`) DO embed full tree byte inventories (excluding `.git`), which remain the durable full inventory for the original run. Do not conflate the two.

## 3. Gate byte-retention gap (stated, not repaired)

`s-refresh-first` preserved the superseded H0-era receipt to edition `.witness-evidence/` but did NOT preserve the initial H0-era Gate bytes before CLI overwrite (code search: only receipt writes exist at supplement lines 388–389; gate preservation appears only in the repeat path, lines 512–534). Packet and edition-evidence listings confirm: no H0-era gate byte archive exists anywhere.

- H0-era Gate bytes: MISSING. The w0 hash `74fb5235…` and checkpoint references are references, not a byte archive. State explicitly; do NOT regenerate or backdate them.
- H1-era Gate bytes existed ONLY in edition `.witness-evidence/gate-superseded-repeat.json`; they are now copied into this packet (`preserved-artifacts/gate-superseded-H1.json`, sha `c48cef9b…`, 5034 B) as inert evidence, alongside H1-era receipt (`c93da8a1…`) and H0-era receipt (`4d98b3c7…`).
- Consequence: the first root decision's full superseded-Gate-retention condition is NOT fully met in the supplement. No complete operational-writer safety claim is made on this basis.

## 4. Independent-DB evidence (new fixture, read-only)

- `git rev-parse --git-dir` == `--git-common-dir` (`.git`): no split worktree/commondir.
- `objects/info/alternates`: absent; `git count-objects -v`: 683 loose, 0 packs, no alternate lines; `git config --list --show-origin`: local repo config only (formatversion/filemode/bare/logallrefupdates/inert origin), no alternate/worktree keys.
- Tracked tree: full `git ls-files -s` inspected — every entry mode `100644`, zero `120000` (symlink) / `160000` (gitlink) entries (head paths, `config/`, and full `docs/` listing verified line by line; remainder visually inspected in the saved output).
- Worktree: `find -xdev -type l -not -path '*/.git/*'` → empty; `find -xdev -type f -links +1 -not -path '*/.git/*'` → empty.
- Origin inert: `https://example.invalid/witness-edition.git` (fetch+push).
- Observation vs proof, distinguished: 12-file inode/nlink sample (distinct inodes, nlink==1) proves no sharing for the sample; alternates-absent + zero-hardlink-findings + no-split-dirs generalize to theRepo level as observation, not per-file proof. No shared objects are expected from `git init` (loose-object store confirmed), stated as expectation, not measurement.
- Source rechecks (read-only, this session): e4c8269 HEAD `e4c82692…`, status `?? scripts/__pycache__/`, `?? tests/__pycache__/` only; B HEAD `c04f32ad…`, status pycache-only; original fixture HEAD `4ddc88c9…` with prior untracked work files present, unmodified. Reconstruct HEAD `d665af89…`, status only the two pre-existing untracked paths.

## 5. Durable artifact preservation (this packet)

`logs/20260927T160625Z/preserved-artifacts/` (byte-faithful `cp` copies; manifest `manifest.json`, non-compact, short lines):

| Dest file | Bytes | SHA256 | Standing |
|---|---|---|---|
| `publication-surface-revalidation-r1.json` | 4717 | `3f195000…7cfb3c` | matches r1 sidecar; current |
| `publication-surface-revalidation-r2.json` | 4888 | `b8f82855…264f6e356` | matches r2 sidecar; current; its superseded gate `new_sha256 bc9c8958…` matches current gate copy |
| `production-state.json` | 5965 | `0bad3440…621f4d` | current snapshot (post-r2, post-negatives-restored); no run-time sidecar recorded it — labeled as current snapshot |
| `validation-checkpoint-DRAFT_COMPLETE.json` | 3006 | `a847a66f…282faf3` | matches w0 `validation_checkpoint_sha256` (immutable since W0) |
| `validated-source-manifest.current-H2.json` | 6775 | `90d05a8c…bc43fe` | current snapshot |
| `reader-surface-gate-v2.current-H2.json` | 5034 | `bc9c8958…7e2ce3342` | current snapshot; bound by r2 bytes above |
| `receipt-superseded-H0.json` | 6774 | `4d98b3c7…0f487f624` | matches S1 `receipt_old_raw_sha256`; also corrects original `receipt_old_sha256` (parsed-JSON hash, preserved untouched) |
| `receipt-superseded-H1.json` | 6775 | `c93da8a1…5d765fd3` | matches S1 `receipt_new_sha256` |
| `gate-superseded-H1.json` | 5034 | `c48cef9b…9d50365` | matches S1 `gate_new_sha256` |

This is a current snapshot plus available immutable records — NOT a claim that all of these were captured at run time (only sidecar-pinned values were). Fixture content is synthetic-only; no confidential material. Prior timestamp/procedural reset/raw-log-loss limits are unchanged and restated in §D of the supplement report.

## 6. Rerun and verification warnings

- Do NOT auto-rerun ANY saved harness (original or supplement) against an existing logs dir or fixture: supplement phases refuse to overwrite their own sidecar/log outputs (fail-closed; observed firing once), but error/CLI sub-logs and `--exit-file` paths are written unconditionally and WOULD be overwritten on an interrupted retry before any sidecar exists. A rerun needs a fresh run-id/logs dir (and, for commit phases, a fresh fixture state) — there is no safe in-place retry.
- `_git status` / `rev-parse HEAD` verify source-control head, NOT worktree bytes. All “intact” claims from these commands are after-the-fact head verifications; worktree-byte claims rest only on the snapshot/hash evidence cited per window above.
- Raw event info absent anywhere (the pre-file s-refresh-first attempt-1 traceback, pre-existing shell transcripts) is disclosed as missing, without further reconstruction.

## Outputs delivered by this closeout

- `notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/preserved-artifacts/` (9 files + `manifest.json`).
- This `evidence-closeout.md`.
- No other files created or modified.
