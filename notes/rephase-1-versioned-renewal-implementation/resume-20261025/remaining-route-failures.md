# Remaining route failures — READ-ONLY analysis (run55 + run43/45/47/49/54/59/61)

2026-10-25. READ-ONLY Co-Worker analysis. No source writes / runtime / tests / Git mutation / network / old-runner exec / repair / rerun. No model stop-cause investigation (Human-explicit not needed).

Read (FILE-ref ONLY, not re-verified beyond cited bytes):

- `notes/rephase-1-versioned-renewal-implementation/resume-20261025/evidence-reconciliation.md` (§§1–7) + `evidence-reconciliation.json` (NOT TURN3-only; full run35–61 + high23/24 binding).
- Phase raw `notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z/run35-20261025T033000Z` … `run61-20261025T110000Z` (`commands.log` / `*-exit.txt` / `*-stdout.txt` / `*-stderr.txt` / `ed-probe-stacks.txt` / `head-*-*.txt` / `overlay-*.txt`), esp. run43/45/47/49/54/55/59/61.
- Actual FIXED source ` .rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work/scripts/` (+ schemas). Candidate `candidate-work` and mutable `versioned-renewal-high*` worktrees NOT read (per task: candidate being edited — use FIXED snapshot + phase raw + reconciliation pins only).
- Parallel independent reviews `resume-20261025/independent-operation-review.md` (B1–B3) + `independent-authority-review.md` (F1–F4) for ownership mapping only (no duplication).

Method: `Read` + `Grep` only. No imports, no `python -m unittest`, no TeX, no fixture scripts executed. All `{path,sha256}` below are FILE-byte SHA per ROOT §7 correction; SELF digests only inside artifact self fields.

Human HEAD / source pins (observed at task start, not mutated here): reconstruct `f84fcf5` assumed per packet; FIXED snapshot `snapshot-work` HEAD `409b292` tree `8ce36998`, HIGH `1620b92c482a5c0c731b27ce7bf27a4eac59c45817da0910b6a7cf4c7a0ba8a2` 174208 B 3045 lines = high24 G2+ epoch (NOT high22 T2 `f6a61245…`, NOT TURN3 `1ee…` bytes-never-saved). No new fixture commits in this round.

Whole unit NOT_READY. No `PASS` inferred from missing stdout. Missing `-exit.txt` reported explicitly as `SUCCESS_RAW_MISSING_EXIT` precursor only, never as acceptance. No Commit Point.

## 1. Longform U3 activate — run55 `SEAL_BIND / HISTORY_ANCESTOR`

Exact evidence (phase raw):

- `run55-20261025T100000Z/commands.log` (8 lines): G3LF fixture `git add/status/commit` → `head-g3lf-pre 140780f` → `head-g3lf-post dbdaf61` → HIGH `prepare → … → finalize → activate` (`activate … -> exit=2`).
- `head-g3lf-pre-longform-stdout.txt`: `140780fb9c87607c105165dfd5bd87489026a91e`.
- `head-g3lf-post-longform-stdout.txt`: `dbdaf611206050dbc98e7973787ab77076cc4c73` (G3LF P1-integration + current HIGH).
- `overlay-g3lf-longform.txt`: `mismatches=[]`.
- `u3-prepare-stdout.txt`: `REUSED_TARGETS`, `basis 61f3796df8…`, `retained_copy {path: …/high-u3-longform/retained/before/sources/SP001/production-state.json, sha256: 17b7aee049e…}`.
- `u3-prepare-exit.txt 0`, `u3-qa-exit.txt 0`, `u3-finalize-exit.txt 0` + `u3-finalize-stdout.txt REUSED_TARGETS` (set/proof/receipt/build/bundle/gate/candidate paths).
- `u3-activate-exit.txt`: `2`. `u3-activate-stdout.txt`: empty (0 B — no `ACTIVATED`). `u3-activate-stderr.txt` (sole verdict):
  `{"phase":"ACTIVATE","code":"SEAL_BIND","disposition":"PRESERVED_INCOMPLETE","detail":"low activation-record validation failed: versioned activation history invalid: HISTORY_ANCESTOR: history chain chronology must be nondecreasing"}`.
- No `u3-history-*` in dir → history SKIP. No overwrite (preserved incomplete, no rollback/adoption/deletion claimed).

Fixture tool epoch (from raw + reconciliation, no mutable read):

- Longform chain `721a04d → 26c403f G1-base → 140780f G2 → dbdaf61 G3LF`; HIGH at G2+ = `1620b92…` (candidate-work HIGH). Old E uncommitted (`?? architecture-*/…` per worklog, tracked clean). Base retained `721a04d` (SOURCE R7b 721 files, ancestors `00397c3`/`ce90246`).
- Weekly `u3b (run46 r6) / u3c (run48 r7) / u3d (run51 r8) ACTIVATED` are WEEKLY-route repairs only. They do NOT repair longform U3. Longform U3 remains FAIL with no longform repair in evidence. Do not cite weekly `ACTIVATED r6/r7/r8` as longform transfer.

Source codepoints (FIXED snapshot):

- HIGH `scripts/survey_versioned_renewal_v2.py:2544-2673` `activate_renewal`: `2566 ts=_now_utc(recorded_at)` (harness `recorded_at` or wallclock `now(timezone.utc)`); `2633-2634 supersedes={prior_record_ref path+sha}` (exact prior, no fallback); `2660 _atomic_write_new` new record; `2669 setmod.validate_activation_record` → `2671-2673` wraps any `Exception` as `code or SEAL_BIND / PRESERVED_INCOMPLETE / low activation-record validation failed`.
- Low `scripts/survey_publication_set_v2.py:1339-1378` `_validate_versioned_activation` → `1375 hist.verify_versioned_history` → `1376-1377` wraps as `versioned activation history invalid`.
- H `scripts/survey_versioned_renewal_history_v2.py:2688-2745` `verify_versioned_history`: `2708 _walk_chain_backwards(supersedes)` + `2709 chronological=reversed(backwards)+[(record,head_ref)]`; `2719 previous_instant=None`; `2727-2730 _parse_instant(recorded_at)` (`371-381`: strict ISO, `Z→+00:00`, tz-required, `astimezone(utc)`); `2731-2732 if instant<previous_instant: raise HISTORY_ANCESTOR chronology must be nondecreasing`; `2734 _parse_sequence(ref[path])` (`600-612`: `publication-surface-revalidation-rN.json`, no leading zero); `2740-2741 sequence strictly increasing else HISTORY_ANCESTOR`; `2742-2743 mixed later-legacy unsupported`; `prior_checkpoint` must bind original validation for every link.
- New-record fields feeding this: HIGH `2649 recorded_at: ts`, `2631-2632 prior_checkpoint`, `2627-2644` full record (`supersedes`, `canonical_anchor`, `before_state_ref`, `retained_copy_ref`, `before_active_digest`, `before_candidate_ref`, `set/basis/proof_refs`). Any of `recorded_at` / `supersedes path+sha` / `prior_checkpoint` / sequence filename can trigger this exact string.

Discrimination (harness clock/record edge vs product missing predicate):

- CANNOT discriminate on current evidence. `recorded_at` instants for `r1–r5` chain, `supersedes {path,sha256}` of new r5, and `recorded_at` source (`recorded_at` arg vs `_now_utc` wallclock at `survey_versioned_renewal_v2.py:124-141`) are in mutable fixture record bytes NOT read here (candidate/fixture being edited). Phase raw contains no `r5-history` / record JSON / `stat` / profile timing.
- Therefore: do NOT claim “wrong harness clock”, do NOT claim “record edge”, do NOT claim “product predicate missing”. Both remain open:
  (a) harness `recorded_at` non-monotonic (wallclock regression, parallel-run clock, reused `ts` across rapid `u3b/c/d` vs longform branch) → `instant<previous_instant`;
  (b) `supersedes` mislink (prior is not immediate r4, prior SHA drift, or r5 filename sequence collision with already-claimed `r5 99554deb…` noted in reconciliation §5 as file-present-but-not-activated) → chronology/sequence/code mismatch surfacing as chronology string;
  (c) genuine product gap (new U3 `recorded_at`/`supersedes`/`prior_checkpoint` construction violates nondecreasing/strictly-increasing on longform branch while weekly branch passes).
- Required root-directed inspection (no blind retry of run55 `exit 2`): reload longform `r1 2bd14fc7… / r2 fae26722… / r3 3e3b72cc… / r4 610ae018… / r5 99554deb…` + new attempted r5 bytes + `supersedes` + `prior_checkpoint` + `recorded_at` instants + sequence numbers, with CURRENT tools on EVERY readback (detached check). Preserve `PRESERVED_INCOMPLETE` bytes; no rollback/adoption/deletion; no State rewind (see §4).

Missing-exit discipline: `u3-finalize-stdout REUSED_TARGETS` + `exit 0` is generation SUCCESS only, not activation. No history `HISTORICAL_IDENTITY_VERIFIED` for longform U3 exists. Do not infer U3-active.

## 2. Renewal→editorial — run43/45/47/49 `exit 1` (four distinct predicates)

All on weekly root (per `commands.log` cwd `…/renewal-weekly`), longform route not separately probed to success. No successful renewal→editorial proposal in evidence. OPEN.

- run43 `ed-probe-exit.txt 1`, `commands.log: probe ed-renew-2 -> exit=1`:
  `survey_editorial_correction_proposal_v2.py:1630 _pipeline_data → reader.validate_manuscript_manifest → survey_reader_publication_v2.py:388 ValueError: renewed manuscript requires explicit renewal proof context` → `ProposalError MANUSCRIPT_INVALID`.
  FIXED codepoint: `survey_reader_publication_v2.py:384-389` (C with `renewal_source` requires `renewal_source_proof_ref`, else `388` refusal); P1 `survey_editorial_correction_proposal_v2.py:79-109 _selected_renewal_proof_ref` (returns `None` on ordinary `VERSIONED_ACTIVE`-absent path, `1662-1673` passes `_proof_ctx` or `None`). Trace indicates probe hit stale-refusal branch (no explicit proof context derived from State-selected seal). Cannot tell harness probe omission (State not `VERSIONED_ACTIVE` at probe time / wrong `authoring-input.json` staging per `1645-1649` check) vs product predicate correct. Relates to F4-owned function (`_validate_manifest_semantics` / `_validate_renewal_manuscript_binding`) — see §5.

- run45 `exit 1`:
  `survey_versioned_renewal_source_v2.py:1275 RenewalSourceError BASIS_CURRENT_TOOL_DRIFT: proof closure drift: scripts/survey_editorial_correction_proposal_v2.py` via `survey_reader_publication_v2.py:208 _validate_renewal_manuscript_binding → 210 renewal proof Layer-B readback refused` → P1 `1673 MANUSCRIPT_INVALID`.
  FIXED codepoint: `survey_versioned_renewal_source_v2.py:1151-1296 verify_renewal_source_proof`, esp. `1263-1275` live-vs-proof member-wise + `1281-1283 proof==basis closure` + `1284-1296 contract_identity` from current disk. Firing here is the mandated detached CURRENT-tool check on EVERY readback (per root map), not a defect per se — proof pinned at older epoch, CURRENT disk has G4 (`9343b94` P1 proof context) tool change. Relates DIRECTLY to F3-owned function (Layer-B CURRENT closure lacks git-blob/HEAD binding — independent-authority F3). Repair ownership: S team (F3). Do not claim “fix won” — run45 proves refusal path only.

- run47 `exit 1`:
  `survey_editorial_correction_proposal_v2.py:1709 StopIteration` on `publication-semantic-input` → `1714 RECEIPT_REF_SHAPE: generated receipt routing refs unreadable`.
  FIXED codepoint: `survey_editorial_correction_proposal_v2.py:1689-1738` receipt-kind dispatch. `StopIteration` means `envelope_kind` fell to `else` branch (`1729-1736`: expects `authored_refs[].name==publication-semantic-input`), i.e. receipt `kind` was NOT `VERSIONED_RENEWAL_SOURCE_V1` nor `EDITORIAL_PUBLICATION_SOURCE_V1` at probe time (old synthetic receipt). Epoch: between G4 (`run44`) and G5 (`run48` P1-routing) — pre-routing fixture, so missing `authoring_refs/proposed-publication-authoring` expected on old receipt.

- run49 `exit 1`:
  `survey_editorial_correction_proposal_v2.py:1709 raise RECEIPT_REF_SHAPE: renewal receipt lacks routing refs` (explicit, not `StopIteration`).
  FIXED codepoint: `1702-1713` `VERSIONED_RENEWAL_SOURCE_V1` branch (`_auth_by_name[proposed-publication-authoring]`, `reviewed_reader_ref`). Post-G5 (`053515d` P1-routing) but pre-G6 (`50b03a6 authoring_refs key`). Indicates renewal receipt still lacks `proposed-publication-authoring` / `reviewed_reader_ref` after G5. Product predicate (`authoring_refs` + `reviewed_reader_ref` required) vs harness stale-receipt (proof/receipt captured before routing fix, not recaptured) cannot be discriminated without reading mutable receipt bytes. Do NOT claim G5/G6 fixed it — no successful renewal→editorial probe after G6 exists.

Common P1/P2V/P3S/H/Reader callgraph (FIXED snapshot, for all four):

- P1 `prepare_proposal:2125/2165/2183-2187 → _pipeline:1844/1884/1902/1906 → _pipeline_data:1599-1749` → `1620 agent.validate_agent_state` (strict LIVE, prePreview/Exception window) → `1655 _original_checkpoint` → `1656 _active_effective` → `1668 _selected_renewal_proof_ref` → `1669-1673 reader.validate_manuscript_manifest(+proof_ctx)` → `1674-1688` gate/receipt load → `1692-1738` receipt-kind routing → `1739 _derive` (Weekly/Longform `load_derivation`) → `1745 _derive` proposed → content checks.
- Reader `survey_reader_publication_v2.py:171-260 _validate_renewal_manuscript_binding` → `208 srcmod.verify_renewal_source_proof` (S Layer-B) → `230 hist.verify_versioned_history` (H leaf on prior record) for stored-proof lineage.
- S `survey_versioned_renewal_source_v2.py:1151-1467 verify_renewal_source_proof` (Layer-B, no State): basis/proof linkage, trio live recheck, `supported==observed`, HIST verdict on `prior_record_ref`, CURRENT closure/contract, surface/trio re-derivation.
- H `survey_versioned_renewal_history_v2.py:2688-2972 verify_versioned_history` (no State/P1/P2R/P3S/Reader/Gate/Candidate calls): chain/anchor/E/T + observed==expected accumulator.
- P2V/P3S not reached in these four traces (refusal before `_derive` in run43/47/49; S+H reached in run45 via Reader→S→H). No `production.verify_state_basis` on these paths (docstring bans hold per independent reviews).

## 3. Renewal→editorial timeouts — run54/59/61 `Timeout (0:03:00)!` (stacks only)

Exact evidence:

- `run54/ed-probe-stacks.txt` 178 lines (9 dumps), `run59/ed-probe-stacks.txt` 343 lines, `run61/ed-probe-stacks.txt` 138 lines. Each file contains ONLY `Timeout (0:03:00)!` + `Thread … [python3]` faulthandler dumps. No `ed-probe-exit.txt`, no `ed-probe-stdout.txt`/`stderr.txt` JSON, no `commands.log` commands (`0 B` for 54/59/61 per reconciliation). Report as `FAIL_TIMEOUT` (stacks only), never as PASS.
- Recurring frames (all three runs, FIXED line numbers match fixture epoch ± drift):
  `survey_versioned_renewal_history_v2.py:450 _git_run (subprocess.run timeout=30, GIT_OPTIONAL_LOCKS=0)` via `465 _git_commit_exists`, `492 _git_tree_mode`, `473 _git_show_blob`, `488 _git_blob_sha`, `505-514 _verify_tool_blob`, `650-685 _verify_receipt_closure_exact`, `688-729 _verify_staged_code_deps_exact`, `779-860 _check_observed_binding_row_structural`, `1880 _norm_structural`, `1886/1924/1949/1952 _verify_versioned_ancestor`, `2853 verify_versioned_history` →
  `survey_publication_set_v2.py:1375 _validate_versioned_activation / 1402 validate_activation_record / 2101 resolve_publication_selection` →
  `survey_agent_control_v2.py:518 _validate_checkpoint_record / 640/674/599 validate_agent_state / 1375 _check_revalidation_chain / 1408 _check_revalidation_agreement / 1469/1569-1570 _resolve_publication_revalidation / 758/802-783 _resolve_checkpoint_artifact` →
  `survey_editorial_correction_proposal_v2.py:509 _active_effective / 595 _derive / 1620/1656/1739/1906/1984 _validated_state_profile_for_tree/_pipeline_data/_pipeline / 2184/2187 prepare_proposal` (+ one `jsonschema/validators.py:463 _validate_reference` frame in run54).
- Callers cycle across dumps (e.g. run54 shows `_git_commit_exists`, `_git_tree_mode`, `_git_show_blob`, `_git_blob_sha`, `_verify_tool_blob`, `jsonschema`, `_execute_child` in successive dumps; run59/61 similar rotation through `_check_observed_binding_row:957`, `_derive_versioned_own_bindings:2388`, `_validate_agent_state`, `_resolve_checkpoint_artifact`). This proves repeated historical Git + schema + replay calls on the renewal→editorial path, but provides NO per-call durations, NO counts, NO profile, NO `ps`/`iostat`, NO chain-length-at-time, NO receipt/closure sizes.

Verdict: hypothesis ONLY. Candidate explanations (all unproven):

- (a) legitimate cost blowup: `verify_versioned_history` per-record accumulator does `observed==expected` + per-row `_verify_tool_blob` (`cat-file -e` + `git show` + `ls-tree` → 3 subprocesses per tool row) × 63 NEW closure + 50 staged `code_deps` × chains `r1–r8` + repeated per-State-validation (`validate_agent_state` → `resolve_publication_selection` → history per checkpoint) → hundreds of `git` subprocesses inside a single `prepare_proposal`, each with `timeout=30`, under 3-min harness timeout;
- (b) environment slowness (loaded runner, cold FS, parallel disjoint repairs contending) — no evidence;
- (c) jsonschema + `_derive` replay cost — single frame, no proof.
- Do NOT attribute to product infinite loop / cycle (chain bound is `CHAIN_LIMIT=32` with cycle/depth fail-closed at H `589/597`; no cycle string in stacks). Do NOT claim any F/B fix resolves timeouts — no equivalence evidence. Required: root-ordered isolated re-probe with `GIT_TRACE` off, per-phase timing, and bounded chain (fresh fixture, not r1–r8 accumulation) before any performance claim. Task ownership for profiling is root + H/P1 joint, not F1–F4/B1–B3 alone.

## 4. Prior prePreview State — reproducible vs already-RELEASED

- Current States (reconciliation §5, stdlib JSON): high24 weekly `…/2026-W37/production-state.json` `7fd02fcb5d43…` `VALIDATED_DRAFT`, longform `…/SP001/production-state.json` `17b7aee049e…` `VALIDATED_DRAFT`; `checkpoints: null`, `selected_record/selected_set: null` in both (no selection inference). NOT `RELEASED` States. `run58 merge-release-stdout approval OK candidate 10d9bd… HEAD 50b03a6 merge/release OK` is normal Release-path stdout on weekly U3d (SUCCESS_RAW_MISSING_EXIT — no exit file), not a State `RELEASED` promotion. Do not cite as State RELEASED.
- Pinned retention COPYs exist per prepare (e.g. longform U3 `retained/before/…/production-state.json 17b7aee…`; weekly U1–U3d retained copies per run dirs). These are the ONLY sanctioned prior-State source. The `retained COPY` is live/COPY, never tool-commit; detached proof checks CURRENT tools on EVERY readback (per root map).
- Reproducibility:
  - Longform: latest activated = `r4 (high-u2-longform)`; `high-u3-longform` finalized (`REUSED_TARGETS`) but NOT activated. Prior prePreview State = r4-active State + retained COPY already on disk — reproducible by inspection (reload pinned bytes), NOT by rewind. Do NOT synthesize State rewind, do NOT rerun old runner, do NOT forge `ALREADY_ACTIVE` on U3 (no U3 `ALREADY_ACTIVE` success exists).
  - Weekly: latest activated = `r8 (high-u3d-weekly)` with `r8-history 8 refs HISTORICAL_IDENTITY_VERIFIED` raw (no exit). Prior prePreview States for `r6/r7/r8` are superseded links in the same chain (`EDITORIAL→U1→C1→U2→U3→U3b→U3c→U3d`), reloadable via `_walk_chain_backwards` from retained bytes. Do NOT revert workdir HIGH or rerun `g1/g2/g3/u3b/c/d` positives except as explicitly ordered repeat-chain with fresh epochs.
- Failure/resume preservation: run55 `PRESERVED_INCOMPLETE` (no overwrite), run35 RENDER refusal, run37 doubled-path seal, run39 overwrite guard, run42 `REFUSED_TARGET_EXISTS` are oracles, not defects to “fix” by retry. Explicit `ALREADY_ACTIVE`/resume (weekly r8 raw, longform pending), IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor oracles from worklog Turn2 remain OPEN for affected scope (no new R1×2 anchor proof here).

## 5. Ownership — relate only where trace points into owned functions

Other agents repair F1–F4 (authority) + B1–B3 (operation) in parallel. Relate blockers ONLY on actual trace:

- run45 `BASIS_CURRENT_TOOL_DRIFT: proof closure drift: scripts/survey_editorial_correction_proposal_v2.py` → S `verify_renewal_source_proof:1263-1275` (F3-owned Layer-B CURRENT closure). Ownership: S team, F3 (`git-blob + mode + HEAD` binding). After F3 repair, run45-class probes must be re-executed on fresh epochs (stale proof MUST still refuse; new proof on new epoch must pass) — cannot claim current code passes.
- run43 `renewed manuscript requires explicit renewal proof context` → Reader `_validate_manifest_semantics:384-392` + P1 `_selected_renewal_proof_ref:79-109` (F4-owned exact-target bypass area). Ownership: S/Reader team, F4 (refuse neither-with-proof except canonical; require serialized `renewal_source` for NEW trio under `R/`). Run43 is the oracle that F4 closes; no new C manuscript in evidence passes it yet.
- run47/49 `RECEIPT_REF_SHAPE` → P1 `_pipeline_data:1692-1738` receipt-kind/routing (pre-G5/G6 gap). NOT F1 (reverify fresh-vs-fresh at S `248-288` — not in these stacks), NOT F2 (Discovery JSONL at S `805-836` — not in these stacks), NOT B1 (Freeze `_preflight` overlap — not in renewal→editorial path), NOT B2/B3 (alias/`ALREADY_ACTIVE` string compare — run55 refused before `ALREADY_ACTIVE` branch at HIGH `2585-2601`; B3 helper unification pending but not triggered here).
- run55 `HISTORY_ANCESTOR chronology` → H `verify_versioned_history:2719-2741` + Low `pubset:1339-1378` + HIGH `activate:2544-2673`. NOT B1–B3, NOT F1–F4 (F3 closure not reached — refusal is chronology/sequence, not closure drift). Ownership: H team + root (chronology/binding inspection per §1), no blind retry.
- run54/59/61 timeouts → H (`_git_run` family, `_verify_*`, `_check_observed_binding_row*`) + P1 (`_active_effective`, `_derive`, `_validated_state_profile_for_tree`) + agent control (`validate_agent_state`, `resolve_publication_selection`) + `jsonschema`. Hypothesis only (see §3); NOT assigned to F1–F4/B1–B3 as defect without profile evidence.

## 6. Least-duplicative root-ordered fresh-fixture sequence (once fixed combined snapshot ready)

Preserve: real old `721a04d` ancestry (ancestors `00397c3`/`ce90246`), source-committed-before-authority (tool commits `3d456e5/26c403f → c3a96f0/140780f → a858237 → 9343b94 → 053515d → 50b03a6 / dbdaf61` pattern), genuine changed-tool epochs (G1 `37d67561…` vs G2+ `1620b92…` + post-fix new epoch), isolated synthetic DBs (no alternates/hardlinks, inert `example.invalid` origins, no reconstruct-DB fixtures, no saved-runner reuse). Do NOT revert workdir HIGH, do NOT rerun `run34/g1/g2/g3/u3b/c/d` positives except as ordered repeat-chain.

Root order (each with exit-proved `*-exit.txt 0/2` + stdout JSON, not raw-only):

1. Freeze fixed combined snapshot (post-F1–F4/B1–B3) as NEW immutable review source; re-pin HIGH/H/S/test + 4 schemas + consumers + `closure 63/route / 66 union / pipeline 67→71` memberships. Fresh independent re-review of F1–F4/B1–B3 diffs first.
2. Fresh isolated fixtures from `721a04d`: weekly + longform bootstrap (R3-format, `head-pre 721a04d → post G1-base`, `overlay mismatches=[]`), then genuine second epoch (current HIGH + P1/H fixes) — two tool commits minimum per route, nonsquashed, `git log` + `HEAD^{tree}` + tool-blob SHA pinned.
3. Weekly: `U1 → C1 (new trio/current proof/manuscript/build + receipt AFTER build + new postrender reviews) → U2 → U3` (`C→U→U`), each `prepare(exit 0) → finalize(exit 0, REUSED vs NEW as appropriate) → activate(exit 0, ACTIVATED rN) → history(HISTORICAL_IDENTITY_VERIFIED, FILE bindings, schema_pointer "") → current readback`. Then repeat `U3b/c/d` or single repeat + `ALREADY_ACTIVE`/resume oracle (exit 0, no new record, preserved bytes).
4. Longform: same `U1 → C1 → U2 → U3` chain to match weekly (U3 MUST NOT be blind-retried — root-directed chronology/binding inspection of run55 r5 first; fresh `recorded_at` monotonic, `supersedes`=immediate r4, sequence `r5`, `prior_checkpoint`=original validation). `prepare/finalize exit 0 → activate exit 0 → history exit 0`.
5. Renewal→editorial (both routes, after P1 receipt/routing + F3/F4 fixes): `prepare_proposal` on U-active prior with changed reader → proposal → review → activate/resume. Must show one SUCCESS per route; prior `run43/45/47/49` FAILs remain as oracles, not erased.
6. Normal direct Candidate/Preview/Freeze/Release (both routes): on weekly latest-U + longform U2/U3-after-activation, with real PDF where C (disposable build + transfer + digest), plus `R1×2` anchor retained (existing R1/canonical after versioned refusal stays pre-write refused).
7. Explicit failure/resume + affected regressions + independent final implementation review: RENDER refusal, overwrite guard, `REFUSED_TARGET_EXISTS`, `PRESERVED_INCOMPLETE` no-rollback, `RECORD_COLLISION` vs `ALREADY_ACTIVE` vs `INDETERMINATE` (incl. B3 alias cases), original-routes/R1-slow/DM004 `7/7` + publication/quality/gate/stage/pubset/revalidation/freeze/staged-EDQUOT, whole-pipeline `63/66/67→71` measured (not map-membership claim).

## 7. Exact remaining tests for parallel Weekly/Longform verification (post-fix snapshot)

No test is marked PASS here. Each requires exit-proved raw (`*-exit.txt` + stdout) + CURRENT-tool detached readback + independent review:

- Weekly: (a) fresh `C→U→U` chain activations + histories (r2–r5 equivalents, `HISTORICAL_IDENTITY_VERIFIED`, `schema_pointer ""`); (b) repeat-U + `ALREADY_ACTIVE rN` / resume (exit 0, `observed new`, no divergent record); (c) renewal→editorial `prepare_proposal` SUCCESS (post-F3/F4, post-G6 routing: `authoring_refs/proposed-publication-authoring` + `reviewed_reader_ref` present); (d) normal lifecycle on latest-U (`stage/approval/freeze/manifest/merge/release OK`, real PDF for C, overwrite-guard oracle preserved); (e) failure oracles (`RENDER refusal`, `REFUSED_TARGET_EXISTS`, `RECORD_COLLISION/PRESERVED_INCOMPLETE` no-overwrite).
- Longform: (a) `U3` activate SUCCESS (exit 0, NOT `exit 2`; new `r5` history, chronology nondecreasing + sequence strictly increasing, `prior_checkpoint` binds original); (b) `C→U→U` parity with weekly (`r1→r2→r3→r4→r5` histories); (c) renewal→editorial SUCCESS (longform route, `LONGFORM_GENERATED_V1` dispatch); (d) normal lifecycle on U2 + post-activation U3; (e) `ALREADY_ACTIVE`/resume on U3 (pending — no longform `ALREADY_ACTIVE` exists yet).
- Both: affected regressions (original routes, R1-slow incl. R1×2 anchor, DM004, publication/quality/gate/stage, pubset/revalidation/freeze/staged) + independent final implementation review. Synthetic reviews are never genuine approvals. Production semantic NO-GO retained.

Whole implementation remains incomplete; whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN. This is NOT a Commit Point and NOT implementation acceptance. Ordinary Commit/Push Human-owned.
