# Independent source review — W34 resume-only (source-only, NO execution)

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human.

**Bounds:** Source/data-only, no active/project runtime imports/execution/tests/writes, no network/Production/reconstruct Git/readback, no subagents. `Read` + `sha256sum` + stdlib text inspection only. Wrapper/manifest/launcher/checks NOT executed. Active source read only at e84 candidate-work. Creates only NEW review files. No removal/restore/State-advance authority.

**Files (programmatic full SHAs):**
- Wrapper `w34-operator-resume-20261105.py` `77b26d79e5e55f29c9fd0e24546072db652f60458ad1a146711591de32bd8f00` 30896B
- Manifest `w34-resume-expected-manifest-20261105.json` `13a3871067bedaa03c6208d31ac6a99ef4d3ea59d6abc2df58d6ae716cd6a1de` 807341B `clean true` 1780f/80d (derived old 1781 + staged r2 − exact2)
- Launcher `w34-resume-launcher-20261105.sh` `c6a1e589f1fb5de5a362761a7d4a5f1ee0a4ad101256c1b27a33db5a30b1b349` 1083B (PYTHONDONTWRITEBYTECODE=1, GIT_* refuse, argv/cwd/HOME/utc/exit, no git/network, single use)
- Input r3 `w34-corrected-input-r3-20261104.json` `15e87eef65753bd0eeff8c512651859d6cb3b8b57127d0243925628acbf1d112` 1576279B 409/363/38/8
- Oracle `w34-resume-oracle-checks-20261105.py` `deadd9143a5e0d3d2383ab962d2fbbfe1bb50400bdce7c26cea687fe32f95d57` + raw 5/5 PASS (helper scope only — counts/exact-set, NOT destruction/proof, see §4)
- Unchanged: old manifest `cede7e46…`, preflight READY `473bf85b…`, r2 input `1ea56297…`, supp `ce6f977a…`, r6 `2c6f1aeb…`; current W34 1780/80 exact2 absent, backups `retention-W34-dispose-20261105T003915Z/` old pins `76ac53f9…`186202B + `93dbefae…`71532B mode 0664 + State `7e6a50c2…`
- Actual e84 defs (read, not imported): `_build_card_core(task,meta,package,record,runner,source_authorities)->card`, `_validate_card_core(card,task,task_sha,package,get_sources)->list`, `validate_interactive_input(value,profile,expected_ids,task_source_ids,*,discovery_records,root_discovery_records)`, `_resolve_phase_supplement_context`, `_capture_phase_pins`, `_finish_authority_phase`, `validate_supplement/package/acceptance/views/ledger/completeness`, `rn.run(repo,state,input,supp?)->{evidence_result_count,completeness_status}`

## 1. CONTINUE ABSENT + current 1780/80 (no restoration/removal)

Root §9 selects CONTINUE ABSENT: exact2 stay absent, backups preserved, no restoration/removal. Wrapper has zero `os.unlink`, zero `write_json`/State writes; live 1780/80 verified vs `w34_tree_current` 1780/80 (old 1781 + staged r2 `1ea56297…` − exact2 Ledger/Completeness). Exact2 `R6._require_absent` (pre + pre-run recheck), backups O_EXCL packet + readback + StateSHA64 vs `backups_pinned` old SHAs, all old accepted (`bf208…/f744…`)/State CAND `7e6a50c2…`/Raw/source771 preserved. P0 source771-before-import + fail-closed before import; after-import 10-module re-hash (`rn.schema_gate` 10th) + `__pycache__` refuse. Stage ONLY 1 NEW r3 input (`O_EXCL 0664 + _require_absent + readback`, packet retention DIRECTLY under packet, `mkdir(exist_ok=False)`), no Raw/supplement change (supplement reused). `rn.run` exactly once, only after full preflight + pre-run recheck (baseline+1/source/State/absent2/backups/Raw/input/manifest); `--prepare-only` returns at READY (retained cards + journal) before any recheck/run — grounded, does NOT secretly run.

## 2. SAME canonical card-core ALL409 + bindings (correct arg types)

Pre-normal-run: retained 409-task package at preflight READY exact path + hash + `validate_package_basis` (no glob); `validate_screening_acceptance` + `_resolve_phase_supplement_context` + `_capture_phase_pins` (facade); `task_source_ids` via real `_discovery_task_sources`/`_merge_supplement_task_sources(run_ctx[entries])`; `validate_interactive_input(r3,profile,set(task_meta),task_source_ids,discovery_records=disc_recs/root_discovery_records=root_recs)` — `disc_recs/effective 439`, `root_recs 369` (validated lists, not tokens; root JSONL 369 lines vs effective 439 distinct). SAME phase as runner: `_rnmod.validate_interactive_input` (existing private helpers, no bypass/mirror). Then SAME `_build_card_core(task,meta,package,by_id[did],runner,_auth)` + `_validate_card_core(card,task,meta[sha256],package,lambda: _merge(_discovery(task),task,entries))` for ALL 409 sorted real tasks; `card==409 else refuse`; private `_finish_authority_phase(run_ctx,run_pins,revalidate_owner=validate_package_basis)` under current facade. Retained `cards/{did}.sha256` hashes only (optional, packet-local, NOT publish). Arg types match defs (dicts/lists, `task_sha=meta[sha256]`, `get_sources=callable`). Oracle proves r3 singles match ALL409 exact task-target sets + `363/38/8` preserved; r2 14-mismatch (c001 missing 1/extra 2) reproduced from REAL package tasks + packet inputs (stdlib source-read, controlled seam — helper scope, NOT semantic PASS).

## 3. Pre/post, audit, failure logger, SP anchors

- Pre/post: P0/P1 full source/READY/manifest/State/tree/absent2/backups/preserved authority + Raw via `validate_supplement` facade (explicit 428-row pin list absent in resume manifest — loop over `supplement428/supplement_rows` is empty; Raw closure covered transitively via pinned supplement file `ce6f…` + API `raw_refs/basis_refs`, weaker than preflight explicit rows — noted, not a prepare-only blocker). Pre-run recheck baseline+1/source/State/absent2/backups/Raw/input/manifest before run. Post-run layout/ledger/comp/archive/umask validators NOT in resume wrapper (unlike dispose r3) — full-run path therefore unvalidated; see verdict.
- Audit: archived NEW input path+bytes + `package.authority_supplement==existing supp` enforced pre-run via retained package + card input binding; post-run archive/umask/EFFECTIVE439 ledger/comp checks absent in this wrapper (see verdict).
- Failure logger: `rdn=normpath(absolute)`, PACKET containment, `is_dir+not islink`, partials sorted, `O_EXCL|O_NOFOLLOW 0664` + `fsync/close/chmod`, payload `error[:4000]+partials` unmasked original verbatim, numeric exit 2, raw stdout/stderr; `--prepare-only` stops at READY (no run). Source-grounded.
- SP anchors: SP state `4865998b…`/profile `aff05fd5…` + SP READY `c7cd05a8…`/DISPOSE `cf26a23c…` snapshot only; no SP writes, no SP ledger freeze (future SP ledger NOT required/frozen). Stable old retention sources only. Correct while SP final retry pending.
- Defect (non-blocking for prepare-only, must-fix before full run): P0 `umask_val,umask_file_mode = os.umask(0),(0o666&~os.umask(0))` double-`umask(0)` always yields `0o666` (not `0o666&~prev`); journal umask misrecorded. No post-run mode gate in this wrapper, so no unsafe pass now, but fix before any full-run mode audit.

## 4. Helpers 5/5 scope (NOT proof)

Oracle 5/5 proves REAL task-target exact-set (409 single-target, r2 14 mismatch incl c001, r3 0 mismatch, counts) from retained package + packet inputs (stdlib, no runtime). Counts/exact-set/archival only — NOT card/ledger/destruction/run proof. Do NOT cite as semantic PASS.

## 5. Verdict

**RESUME_READY narrow (prepare-only ONLY).** Wrapper `77b26d79…`, manifest `13a38710…`, launcher `c6a1e589…` valid for ONE bounded Root-authorized `--prepare-only` invocation: full preflight + r3 `15e87eef…` exact 409/schema + SAME card-core 409 + facade finish + packet READY/journal, CONTINUE ABSENT preserved, no remove/State change, no synthetic approval/cache/bypass/source fix. Preserves v1/r2 + preflight-actual. No semantic PASS, no `EVIDENCE_REVIEWED`/Selection/SP mutation.

**NOT READY for full `rn.run`:** resume full-run path lacks post-run layout/ledger/comp/archive/umask validators (dispose r3 had them). Authorize prepare-only READY now; full guard+run needs separate post-run audit wrapper + re-review. Human Commit Point — stop.

Attribution: Independent reviewer. No execution/network/Production/reconstructGit/project imports/subagents. Binds §§1-4 SHAs/paths/shapes.
