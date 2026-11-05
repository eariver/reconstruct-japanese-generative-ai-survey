# Independent source review — W34 resume r2 (source-only, NO execution)

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human. Preserves r1 review untouched.

**Bounds:** Source/data-only, no active/project runtime imports/execution/tests/writes, no network/Production/reconstruct Git/readback, no subagents. `Read` + `sha256sum` + AST/text inspection only. Wrapper/launcher/checks NOT executed. Active source read only at e84 candidate-work. Creates only NEW r2 review files.

**Files (programmatic full SHAs):**
- Wrapper r2 `w34-operator-resume-r2-20261105.py` `9f27a6c39533888f1e70e22ee28d7c448ffef5d0e7b4c892141a84a66a6546fe` 37213B
- Launcher r2 `w34-resume-launcher-r2-20261105.sh` `ea7c0427fd34af7050c4aa204eb79723e955d53a79ef1a1c0db6c7eb639847af` 1095B
- Manifest UNCHANGED `w34-resume-expected-manifest-20261105.json` `13a3871067bedaa03c6208d31ac6a99ef4d3ea59d6abc2df58d6ae716cd6a1de` 807341B 1780f/80d
- Input r3 `15e87eef65753bd0eeff8c512651859d6cb3b8b57127d0243925628acbf1d112` 409/363/38/8; preflight READY `473bf85b…`; supp `ce6f977a…`; r6 `2c6f1aeb…`; dispo-r3 `48be58796e7ee2ef31ce0873e3223d7c0f78fb6de08aed3012f06b593f2846b8`
- Checks r2 `559e07f4a122a7f313063ec9854bbaeb3f1edce734cbc350b03f8e0808012f1b` + raw 9/9 PASS (helper scope only — NOT run proof, see §4)
- Actual e84 defs (read, not imported): `_build_card_core(task,meta,package,record,runner,source_authorities)`, `_validate_card_core(card,task,task_sha,package,get_sources)`, `rn.run(repo,state,input,supp?)->{evidence_result_count,completeness_status}`, `D3._check_post_run_layout(repo,src,base_plus1,base_dirs,staged_new,old_ledger,old_comp,old_ev,old_view,409,input_rel,sha,supp_rel,sha,439,3,LIMITED,umask)`, validators with EFFECTIVE439

## 1. R1 fixes verified (prepare-only path sound)

R1 rejections fixed in r2 code: fail-closed BEFORE import (`if errs: raise … BEFORE any project import`, AST order verified), 10-module re-hash (`rn.schema_gate` 10th + `__pycache__` refuse), single umask read/restore (`_umask_prev=os.umask(0); os.umask(prev); 0o666&~prev`), supp 428 rows from validated FILE `ce6f…` (file hash → 428/425 → per-Raw `_pin_live`, no `manifest.get(...,[])` skip), actual `core.json_bytes(card)` retained (no `views_checked` fiction), full guards BEFORE READY even `--prepare-only` (baseline+1/source771/State/absent2/backups/supp/input/self-manifest SAME hash), READY binds `exp_manifest_sha` (no reseal), distinct `preflight-journal.json` vs `journal.json` O_EXCL, full-branch reuses pinned dispo-r3 `48be5879…` (stdlib import verified, disposal never executed). Failure logger absolutizes (`rdn=normpath(absolute)`, PACKET containment, `O_EXCL|O_NOFOLLOW 0664`, `error[:4000]+partials`, numeric 2); launcher captures argv/cwd/HOME/utc/exit, no git/network. CONTINUE ABSENT (no `os.unlink`, no State writes), stage ONLY 1 NEW r3 (`O_EXCL+readback`), SP stable anchors only (no SP writes/freeze). Card-core ALL409 with correct arg types (`task,meta,package,by_id[did],runner,_auth` / `card,task,meta[sha256],package,lambda`), private `_finish_authority_phase` under current facade, retained card bytes optional (packet-local, NOT publish). Input/task binding via real `validate_screening/_resolve/_capture/_discovery/_merge` + `validate_interactive_input` (409/369/439). Oracle 9/9 proves exact 409 cover + tamper/journal/manifest/guards/card-bytes/umask (stdlib source-read, NOT run proof).

## 2. Concrete blockers — NOT RESUME_AND_RUN_READY (full branch NameError)

Full branch (post `--prepare-only`) cannot run as written:

- **B1 undefined `_derive_old_accepted_dirs`:** line 488 calls bare `_derive_old_accepted_dirs(manifest)`, but r2 defines NO such function (module funcs: `_load_r6/_load_dispo_r3/_require_under_packet/_stage_bytes_exclusive_packet/_strict_w34_state/stage_resume/_strict_w34_state_resume/main`). D3 (dispo-r3) defines it, but r2 never calls `D3._derive_old_accepted_dirs`. `NameError` on every full run before `_check_post_run_layout`. Prepare-only path returns before line 488, so prepare-only unaffected — full run always fails.
- **B2 undefined `LEDGER_REL/COMP_REL`:** line 494 passes `LEDGER_REL.as_posix(), COMP_REL.as_posix()`, but r2 defines NO module `LEDGER_REL/COMP_REL` (dispo-r3 defines them; resume r2 uses string literals elsewhere for exact2). Same `NameError` in full branch only. Prepare-only unaffected.
- Fix: define `LEDGER_REL=SRC_REL/"materiality-ledger-v2.json"`, `COMP_REL=SRC_REL/"profile-completeness-v2.json"` at module top (as dispo-r3) OR inline `SRC_REL` literals, and call `D3._derive_old_accepted_dirs(manifest)` (or duplicate frozen-tree+pin-parents helper in resume wrapper). Re-verify full-branch AST + dry NameError scan; re-run 9/9 + new full-branch name-resolution check (no execution).

No other invented defaults found (authority/count/READY keys exact, no `.get(...,[])` for authority; remaining `.get(...,[])` only for output-file content length checks). Module import has no side effects (top-level only constants + function defs + `PYTHONDONTWRITEBYTECODE` guard; `sys.path.insert/from scripts import` only inside `stage_resume` after fail-closed gate; `_load_dispo_r3` stdlib import verified by hash, disposal never executed). Layout baseline (`w34_tree_current` 1780 + NEW + old `bf208/f744` sets) + old canonical hashes (bytes/sha/mode/nlink) + EFFECTIVE439 validators + archive/umask bindings otherwise match dispo-r3 proven shapes — blocked only by B1/B2 names.

## 3. Verdict

**NOT RESUME_AND_RUN_READY (source-only blockers B1-B2 in full branch).** Wrapper r2 `9f27a6c3…`, launcher `ea7c0427…` valid for prepare-only preflight + cards, but full `rn.run` + post-run path raises `NameError` before any active write. Do NOT authorize FULL resume on r2. Preserve r1 + preflight-actual `READY 473bf85b…` (no removal yet). No semantic PASS, no `EVIDENCE_REVIEWED`/Selection/SP mutation.

**Required:** Minimal r3 (or r2-patch) defining `LEDGER_REL/COMP_REL` + qualified `D3._derive_old_accepted_dirs` call, no other behavior change; independent re-review + fresh 9/9 + NameError scan; separate Root FULL-resume auth. Prepare-only READY remains available on r2 (no full-run names hit) — authorize prepare-only only, NOT full run.

**NEW paths:** `reviews/w34-resume-r2-independent-review-20261105.md` + `w34-resume-r2-independent-findings-20261105.json` (this addendum). Human Commit Point — stop; do NOT execute.

Attribution: Independent reviewer. No execution/network/Production/reconstructGit/project imports/subagents. Binds §§1-2 SHAs/paths/lines/shapes. Helpers 9/9 scope ≠ run proof.
